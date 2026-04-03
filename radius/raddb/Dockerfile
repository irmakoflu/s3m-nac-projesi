FROM freeradius/freeradius-server:latest-3.2

# Dosyaları içeri kopyala
COPY mods-available/rest /etc/freeradius/mods-available/rest
COPY default /etc/freeradius/sites-available/default

# İzinleri düzelt (Grup ismini belirtmeden sadece root yapıyoruz, FreeRADIUS bunu kabul eder)
RUN chown root:root /etc/freeradius/mods-available/rest /etc/freeradius/sites-available/default && \
    chmod 644 /etc/freeradius/mods-available/rest /etc/freeradius/sites-available/default && \
    ln -sf /etc/freeradius/mods-available/rest /etc/freeradius/mods-enabled/rest

# Logları dışarı vererek başlat
CMD ["freeradius", "-X"]