import requests

url = "https://www.goethe.de/ins/in/en/spr/prf.html"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

print("Status:", response.status_code)

if response.ok:
    print("✅ Goethe website is reachable!")
else:
    print("❌ Goethe website check failed")
