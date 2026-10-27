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
    print("❌ Hyderabad Goethe-Zentrum page failed")
    raise SystemExit(1)

soup = BeautifulSoup(response.text, "html.parser")
text = soup.get_text(" ", strip=True)

levels = ["Goethe-Zertifikat A1", "Goethe-Zertifikat A2",
          "Goethe-Zertifikat B1", "Goethe-Zertifikat B2"]

print("✅ Hyderabad Goethe-Zentrum reachable!")

for level in levels:
    if level in text:
        print(f"✅ {level} found")
    else:
        print(f"⚠️ {level} not found")

print("\n🇩🇪 Hyderabad exam page checked successfully.")
