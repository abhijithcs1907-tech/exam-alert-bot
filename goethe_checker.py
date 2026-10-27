import requests
from bs4 import BeautifulSoup
import re

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

print("✅ Hyderabad exam page loaded")
print("\n🇩🇪 EXAM INFORMATION FOUND:\n")

for level in ["A1", "A2", "B1", "B2"]:
    pattern = rf"GOETHE-ZERTIFIKAT {level}.*?(?=GOETHE-ZERTIFIKAT|Important Notice:|$)"
    matches = re.findall(pattern, text, re.IGNORECASE)

    if matches:
        print(f"### {level}")
        print(matches[0].strip())
        print()
    else:
        print(f"⚠️ {level} information not found")

print("🔎 Exam information check completed.")
