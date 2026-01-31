import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Mengambil data dari GitHub Secrets
json_key_raw = os.environ.get('GOOGLE_JSON_KEY')
json_key = json.loads(json_key_raw)

# Daftar 6 URL artikel Blogger Anda
urls = [
    "https://harahapjaya99.blogspot.com/2025/03/bukan-cuma-bikin-konten-drone-juga-bisa.html",
    "https://harahapjaya99.blogspot.com/2025/03/menjamur-di-ri-bisnis-ini-punya-omzet.html",
    "https://harahapjaya99.blogspot.com/2025/03/calon-pemain-naturalisasi-tambahan.html",
    "https://harahapjaya99.blogspot.com/2026/01/menjelajahi-rahasia-ruang-angkasa.html",
    "https://harahapjaya99.blogspot.com/2026/01/5-inovasi-teknologi-masa-depan-yang.html",
    "https://harahapjaya99.blogspot.com/2026/01/rekomendasi-website-review-aplikasi.html",
    "https://harahapjaya99.blogspot.com/2026/01/strategi-bisnis-digital-2026-cara.html"
]

credentials = service_account.Credentials.from_service_account_info(json_key, scopes=['https://www.googleapis.com/auth/indexing'])
service = build('indexing', 'v3', credentials=credentials)

for url in urls:
    try:
        service.urlNotifications().publish(body={"url": url, "type": "URL_UPDATED"}).execute()
        print(f"SUKSES: {url}")
    except Exception as e:
        print(f"GAGAL: {url} | Error: {e}")
