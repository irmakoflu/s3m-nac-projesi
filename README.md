# Network Access Control (NAC) Sistemi
### RADIUS & Mikroservis Tabanlı AAA Çözümü

Bu proje, kurumsal ağlarda cihaz kimlik doğrulama, yetkilendirme ve kullanım takibi (AAA) süreçlerini otomatize eden konteyner tabanlı bir NAC çözümüdür.

## 🚀 Hızlı Kurulum

Sistemi tüm bileşenleriyle (FreeRADIUS, FastAPI, PostgreSQL, Redis) tek hamlede çalıştırmak için aşağıdaki adımları izleyin:

### 1. Hazırlık
Öncelikle ortam değişkenlerini yapılandırın:
bash
cp .env.example .env


### 2. Sistemi Başlatma
Docker Compose kullanarak tüm mikroservisleri ayağa kaldırın:
bash
docker-compose up -d --build


Bu komutla birlikte:
- **API (FastAPI)**: http://localhost:8000 adresinde yayına başlar.
- **PostgreSQL**: 5432 portunda veritabanı hazır hale gelir.
- **FreeRADIUS**: 1812 (Auth) ve 1813 (Acct) portlarından istek kabul eder.

## 🛠 Teknik Özellikler
- [cite_start]**Kimlik Doğrulama**: 802.1X ve MAB (MAC Authentication Bypass) desteği[cite: 39, 43].
- [cite_start]**Güvenlik**: Bcrypt ile şifre hashleme ve Redis tabanlı Rate-Limiting[cite: 36, 51].
- [cite_start]**Dinamik Yetkilendirme**: Kullanıcı bazlı otomatik VLAN ataması[cite: 88, 92].

## 🧪 Test Etme
Sistemin çalıştığını doğrulamak için `radtest` aracını kullanabilirsiniz:
bash
docker exec -it nac_freeradius radtest ali_test GizliSifre123 127.0.0.1 0 testing123