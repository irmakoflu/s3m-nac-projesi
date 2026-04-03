from database import SessionLocal
from models import RadCheck
from security import get_password_hash

db = SessionLocal()

test_username = "ali_test"
test_password = "GizliSifre123"

hashed_password = get_password_hash(test_password)


yeni_kullanici = RadCheck(
    username=test_username, 
    attribute="Cleartext-Password", 
    op=":=", 
    value=hashed_password # DİKKAT: Veritabanına düz şifreyi değil, hash'i kaydediyoruz!
)


db.add(yeni_kullanici)
db.commit()
db.close()

print(f"✅ Kullanici basariyla olusturuldu!")
print(f"Kullanici Adi: {test_username}")
print(f"Gercek Sifre (Sadece sen biliyorsun): {test_password}")
print(f"Veritabanina Kaydedilen Hash: {hashed_password}")