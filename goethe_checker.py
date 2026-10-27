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

levels = ["A1", "A2", "B1", "B2"]

print("✅ Hyderabad exam page loaded")

for level in levels:
    marker = f"Goethe-Zertifikat {level}"

    if marker in text:
        print(f"✅ {level} exam found")
    else:
        print(f"⚠️ {level} exam not found")

print("\n🔎 Exam information detected successfully.")
