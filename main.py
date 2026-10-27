import requests

URLS = {
    "A1": "https://www.goethe.de/ins/in/en/spr/prf/gzsd1.cfm",
    "A2": "https://www.goethe.de/ins/in/en/spr/prf/gzsd2.cfm",
    "B1": "https://www.goethe.de/ins/in/en/spr/prf/gzb1.cfm",
    "B2": "https://www.goethe.de/ins/in/en/spr/prf/gzb2.cfm",
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

for level, url in URLS.items():

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        print(f"{level}: HTTP {response.status_code}")

        if response.status_code == 200:
            print(f"✅ {level} page accessible")
        elif response.status_code == 403:
            print(f"⚠️ {level} blocked automated request")
        else:
            print(f"⚠️ {level} returned {response.status_code}")

    except Exception as e:
        print(f"❌ {level} error:", e)

print("\n🇩🇪 Goethe checker finished.")
