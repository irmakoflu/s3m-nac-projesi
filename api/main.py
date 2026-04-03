import redis
import json
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import init_db, get_db
from models import RadCheck, RadReply, RadUserGroup, RadGroupReply, RadAcct
from security import verify_password
from typing import Dict, Any

init_db()
app = FastAPI(title="S3M NAC Policy Engine")
redis_client = redis.Redis(host="nac_redis", port=6379, decode_responses=True)

class AuthRequest(BaseModel):
    username: str
    password: str


def check_security_and_auth(request: AuthRequest, db: Session):
    retry_key = f"retry:{request.username}"
    retries = redis_client.get(retry_key)
    
    
    if retries and int(retries) >= 5:
        raise HTTPException(
            status_code=429, 
            detail="Çok fazla hatalı deneme! Lütfen 5 dakika bekleyin."
        )

   
    user = db.query(RadCheck).filter(RadCheck.username == request.username).first()
    
    
    if not user or not verify_password(request.password, user.value):
        redis_client.incr(retry_key)
        redis_client.expire(retry_key, 300) 
        raise HTTPException(status_code=401, detail="Kimlik dogrulama basarisiz")
    
    
    redis_client.delete(retry_key)
    return user

@app.post("/auth")
async def authenticate_user(request: AuthRequest, db: Session = Depends(get_db)):
    check_security_and_auth(request, db)
    return {
        "status": "success", 
        "message": "Kimlik dogrulama basarili",
        "username": request.username
    }

@app.post("/authorize")
async def authorize_user(request: AuthRequest, db: Session = Depends(get_db)):
   
    check_security_and_auth(request, db)
    
    reply_attrs = db.query(RadReply).filter(RadReply.username == request.username).all()
    user_groups = db.query(RadUserGroup).filter(RadUserGroup.username == request.username).all()
    
    attributes = {} 
    for ug in user_groups:
        g_attrs = db.query(RadGroupReply).filter(RadGroupReply.groupname == ug.groupname).all()
        for attr in g_attrs:
            attributes[attr.attribute] = attr.value

    for attr in reply_attrs:
        attributes[attr.attribute] = attr.value    
        
    return attributes


@app.post("/accounting")
async def accounting_record(data: Dict[str, Any], db: Session = Depends(get_db)):
    
    user = data.get('User-Name', {}).get('value', ['Bilinmiyor'])[0]
    status = data.get('Acct-Status-Type', {}).get('value', ['Bilinmiyor'])[0]
    session_id = data.get('Acct-Session-Id', {}).get('value', ['Bilinmiyor'])[0]
    nas_ip = data.get('NAS-IP-Address', {}).get('value', ['0.0.0.0'])[0]
    
    in_octets = int(data.get('Acct-Input-Octets', {}).get('value', [0])[0])
    out_octets = int(data.get('Acct-Output-Octets', {}).get('value', [0])[0])
    session_time = int(data.get('Acct-Session-Time', {}).get('value', [0])[0])

    if status == "Start":
        new_log = RadAcct(
            username=user,
            acctsessionid=session_id,
            nasipaddress=nas_ip,
            acctstatustype=status, 
            acctstarttime=datetime.now()
        )
        db.add(new_log)
        session_data = {"username": user, "nas_ip": nas_ip, "start_time": str(datetime.now())}
        redis_client.set(f"session:{session_id}", json.dumps(session_data))
    
    elif status == "Stop":
        existing_log = db.query(RadAcct).filter(RadAcct.acctsessionid == session_id).first()
        if existing_log:
            existing_log.acctstoptime = datetime.now()
            existing_log.acctsessiontime = session_time
            existing_log.inputoctets = in_octets
            existing_log.outputoctets = out_octets
        redis_client.delete(f"session:{session_id}")

    db.commit()
    return {"status": "success"}

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return db.query(RadAcct).all()

@app.get("/sessions/active")
async def get_active_sessions():
    keys = redis_client.keys("session:*")
    active_sessions = []
    for key in keys:
        session_info = redis_client.get(key)
        if session_info:
            data = json.loads(session_info)
            data["session_id"] = key.replace("session:", "")
            active_sessions.append(data)
            
    return active_sessions


