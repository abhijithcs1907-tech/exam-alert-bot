import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.goethecoimbatore.com/exam/"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

print("Coimbatore page status:", response.status_code)

if not response.ok:
    raise Exception(f"Coimbatore page failed: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")
text = soup.get_text(" ", strip=True)

print("\nCoimbatore Goethe Exam Information:\n")

for level in ["A1", "A2", "B1", "B2"]:
    pattern = rf"Goethe[- ]?Zertifikat.*?{level}.*?(?=Goethe[- ]?Zertifikat|$)"
    matches = re.findall(pattern, text, re.IGNORECASE)

    print(f"\n{level}:")
    if matches:
        print(matches[0])
    else:
        print("No information found")

print("\n✅ Coimbatore checker completed.")
