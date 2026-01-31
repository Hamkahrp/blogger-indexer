import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Ambil data dari Secrets
json_key_raw = os.environ.get('GOOGLE_JSON_KEY')
json_key = json.loads(json_key_raw)

# Mengambil URL secara otomatis dari RSS Feed Blogger Anda
rss_url = "https://harahapjaya99.blogspot.com/feeds/posts/default"
response = urllib.request.urlopen(rss_url)
tree = ET.parse(response)
root = tree.getroot()

# Mencari semua link artikel di dalam feed secara otomatis
urls = []
for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
    for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
        if link.attrib.get('rel') == 'alternate':
            urls.append(link.attrib.get('href'))

credentials = service_account.Credentials.from_service_account_info(json_key, scopes=['https://www.googleapis.com/auth/indexing'])
service = build('indexing', 'v3', credentials=credentials)

for url in urls:
    try:
        service.urlNotifications().publish(body={"url": url, "type": "URL_UPDATED"}).execute()
        print(f"SUKSES TERKIRIM: {url}")
    except Exception as e:
        print(f"GAGAL: {url} | Error: {e}")
