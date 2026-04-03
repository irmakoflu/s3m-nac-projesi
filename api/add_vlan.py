from database import SessionLocal
from models import RadUserGroup, RadGroupReply, RadReply

db = SessionLocal()

test_username = "ali_test"
test_group = "ogrenci_grubu"

user_group = RadUserGroup(username=test_username, groupname=test_group, priority=1)
db.add(user_group)

vlan_ayar_1 = RadGroupReply(groupname=test_group, attribute="Tunnel-Type", op="=", value="VLAN")
vlan_ayar_2 = RadGroupReply(groupname=test_group, attribute="Tunnel-Medium-Type", op="=", value="IEEE-802")
vlan_ayar_3 = RadGroupReply(groupname=test_group, attribute="Tunnel-Private-Group-Id", op="=", value="50") # İşte VLAN 50 burada!
db.add_all([vlan_ayar_1, vlan_ayar_2, vlan_ayar_3])

bireysel_ip = RadReply(username=test_username, attribute="Framed-IP-Address", op="=", value="10.50.0.101")
db.add(bireysel_ip)

db.commit()
db.close()

print(f"✅ {test_username} kullanicisi {test_group} grubuna eklendi!")
print("✅ VLAN 50 ve Sabit IP ayarlari basariyla veritabanina islendi!")