from database import SessionLocal
from models import RadCheck, RadUserGroup, RadGroupReply
from security import hash_password 

db = SessionLocal()

mac_adresi = "001122334455"
cihaz_grubu = "yazici_grubu"


hashed_mac = hash_password(mac_adresi)


db.query(RadCheck).filter(RadCheck.username == mac_adresi).delete()
db.query(RadUserGroup).filter(RadUserGroup.username == mac_adresi).delete()
db.commit()


cihaz_kimlik = RadCheck(username=mac_adresi, attribute="Cleartext-Password", op=":=", value=hashed_mac)
db.add(cihaz_kimlik)

cihaz_grup_atama = RadUserGroup(username=mac_adresi, groupname=cihaz_grubu, priority=1)
db.add(cihaz_grup_atama)


vlan_ayar_1 = RadGroupReply(groupname=cihaz_grubu, attribute="Tunnel-Type", op="=", value="VLAN")
vlan_ayar_2 = RadGroupReply(groupname=cihaz_grubu, attribute="Tunnel-Medium-Type", op="=", value="IEEE-802")
vlan_ayar_3 = RadGroupReply(groupname=cihaz_grubu, attribute="Tunnel-Private-Group-Id", op="=", value="20") 
db.add_all([vlan_ayar_1, vlan_ayar_2, vlan_ayar_3])

db.commit()
db.close()

print(f"✅ MAB Cihazi ({mac_adresi}) veritabanina HASH'lenerek eklendi!")
print("✅ Cihaz, VLAN 20 (Yazicilar Agi) kuralina baglandi!")