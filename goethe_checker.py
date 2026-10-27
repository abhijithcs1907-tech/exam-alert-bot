import requests
from bs4 import BeautifulSoup

URL = "https://hyderabad.german.in/"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

print("Status:", response.status_code)

if not response.ok:
    print("❌ Page failed")
    raise SystemExit(1)

soup = BeautifulSoup(response.text, "html.parser")

text = soup.get_text(" ", strip=True)

print("✅ Hyderabad page loaded")
print("\n--- PAGE TEXT ---\n")
print(text[:10000])
print("\n--- END ---")
