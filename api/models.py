from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RadCheck(Base):
    __tablename__ = "radcheck"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    attribute = Column(String(64), default="Cleartext-Password")
    op = Column(String(2), default=":=")
    value = Column(String(253)) 

class RadReply(Base):
    __tablename__ = "radreply"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), index=True)
    attribute = Column(String(64))
    op = Column(String(2), default="=")
    value = Column(String(253))

class RadUserGroup(Base):
    __tablename__ = "radusergroup"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), index=True)
    groupname = Column(String(64))
    priority = Column(Integer, default=1)

class RadGroupReply(Base):
    __tablename__ = "radgroupreply"
    id = Column(Integer, primary_key=True, index=True)
    groupname = Column(String(64), index=True)
    attribute = Column(String(64))
    op = Column(String(2), default="=")
    value = Column(String(253))

class RadAcct(Base):
    __tablename__ = "radacct"
    radacctid = Column(Integer, primary_key=True, index=True)
    acctsessionid = Column(String(64), index=True)
    username = Column(String(64), index=True)
    nasipaddress = Column(String(15))
    acctstarttime = Column(DateTime)
    acctstoptime = Column(DateTime, nullable=True)
    acctsessiontime = Column(Integer, nullable=True)
    inputoctets = Column(Integer, default=0)
    outputoctets = Column(Integer, default=0)
    acctstatustype = Column(String(32))