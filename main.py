import os
import json
import re
import requests
from bs4 import BeautifulSoup

STATE_FILE = "exam_state.json"

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

CENTRES = {
    "Goethe Hyderabad": "https://hyderabad.german.in/",
    "Goethe Coimbatore": "https://www.goethecoimbatore.com/exam/"
}


def get_page_text(url):
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    print(f"Page status {response.status_code}: {url}")

    if not response.ok:
        raise Exception(f"Page failed: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(" ", strip=True)


def get_hyderabad(text):
    exams = {}

    for level in ["A1", "A2", "B1", "B2"]:
        pattern = rf"GOETHE-ZERTIFIKAT {level}.*?(?=GOETHE-ZERTIFIKAT|Important Notice:|$)"
        matches = re.findall(pattern, text, re.IGNORECASE)

        exams[level] = matches[0].strip() if matches else "No information found"

    return exams


def get_coimbatore(text):
    patterns = {
        "A1": r"Goethe-Zertifikat A1:.*?(?=Goethe-Zertifikat A2|Goethe-Zertifikat B1|Goethe-Zertifikat B2|$)",
        "A2": r"Goethe-Zertifikat A2.*?(?=Goethe-Zertifikat A1|Goethe-Zertifikat B1|Goethe-Zertifikat B2|$)",
        "B1": r"Goethe-Zertifikat B1.*?(?=Goethe-Zertifikat A1|Goethe-Zertifikat A2|Goethe-Zertifikat B2|$)",
        "B2": r"Goethe-Zertifikat B2.*?(?=Goethe-Zertifikat A1|Goethe-Zertifikat A2|Goethe-Zertifikat B1|Goethe-Zertifikat B2|$)"
    }

    exams = {}

    for level, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        exams[level] = matches[0].strip() if matches else "No information found"

    return exams


def get_all_exams():
    all_exams = {}

    for centre, url in CENTRES.items():
        text = get_page_text(url)

        if "Hyderabad" in centre:
            exams = get_hyderabad(text)
        else:
            exams = get_coimbatore(text)

        all_exams[centre] = exams

    return all_exams


def load_old_state():
    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_state(data):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def send_telegram(message_text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text
    }

    response = requests.post(
        url,
        data=data,
        timeout=30
    )

    print("Telegram status:", response.status_code)

    if not response.ok:
        print("Telegram error:", response.text)
    else:
        print("Telegram alert sent successfully.")


current = get_all_exams()
old = load_old_state()

print("\n========== CURRENT EXAM INFORMATION ==========\n")

for centre, exams in current.items():
    print(f"📍 {centre}")

    for level, info in exams.items():
        print(f"{level}: {info}")

    print()


if old is None:
    print("🆕 First combined run - saving state only.")
    save_state(current)

else:
    changes = []

    for centre in current:
        for level in ["A1", "A2", "B1", "B2"]:

            new_info = current[centre][level]
            old_info = old.get(centre, {}).get(level)

            if new_info != old_info:
                changes.append(
                    f"📍 {centre}\n"
                    f"🇩🇪 {level}\n"
                    f"{new_info}"
                )

    if changes:
        alert = (
            "🔔 GOETHE EXAM UPDATE 🇩🇪\n\n"
            + "\n\n".join(changes)
            + "\n\n⚡ Check the official registration page immediately."
        )

        print("\n🚨 EXAM CHANGE DETECTED!")
        send_telegram(alert)

    else:
        print("✅ No exam information changes.")

    save_state(current)

print("\n✅ Combined exam checker completed.")
