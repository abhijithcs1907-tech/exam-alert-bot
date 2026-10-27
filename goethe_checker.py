import requests
from bs4 import BeautifulSoup

URL = "https://www.goethe.de/ins/in/en/spr/prf.html"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

print("Status:", response.status_code)

if not response.ok:
    print("❌ Goethe website check failed")
    raise SystemExit(1)

soup = BeautifulSoup(response.text, "html.parser")

text = soup.get_text(" ", strip=True)

levels = ["A1", "A2", "B1", "B2"]

print("✅ Goethe website reachable!")

for level in levels:
    if level in text:
        print(f"✅ {level} information found")
    else:
        print(f"⚠️ {level} information not found")

print("\n🔎 Goethe exam page checked successfully.")
