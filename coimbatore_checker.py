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

patterns = {
    "A1": r"Goethe-Zertifikat A1:.*?(?=Goethe-Zertifikat A2|Goethe-Zertifikat B1|Goethe-Zertifikat B2|$)",
    "A2": r"Goethe-Zertifikat A2.*?(?=Goethe-Zertifikat A1|Goethe-Zertifikat B1|Goethe-Zertifikat B2|$)",
    "B1": r"Goethe-Zertifikat B1.*?(?=Goethe-Zertifikat A1|Goethe-Zertifikat A2|Goethe-Zertifikat B2|$)",
    "B2": r"Goethe-Zertifikat B2.*?(?=Goethe-Zertifikat A1|Goethe-Zertifikat A2|Goethe-Zertifikat B1|$)"
}

for level, pattern in patterns.items():
    matches = re.findall(pattern, text, re.IGNORECASE)

    print(f"\n{level}:")

    if matches:
        print(matches[0].strip())
    else:
        print("No information found")

print("\n✅ Coimbatore checker completed.")
