import os
import json
import re
import requests
from twilio.rest import Client

URL = "https://hyderabad.german.in/"
STATE_FILE = "exam_state.json"

SID = os.environ["TWILIO_ACCOUNT_SID"]
TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

RECIPIENTS = [
    "whatsapp:+919074526392",
    "whatsapp:+917994046289"
]

def get_exam_info():
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    print("Goethe page status:", response.status_code)

    if not response.ok:
        raise Exception(f"Goethe page failed: {response.status_code}")

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    exams = {}

    for level in ["A1", "A2", "B1", "B2"]:
        pattern = rf"GOETHE-ZERTIFIKAT {level}.*?(?=GOETHE-ZERTIFIKAT|Important Notice:|$)"
        matches = re.findall(pattern, text, re.IGNORECASE)

        exams[level] = matches[0].strip() if matches else "No information found"

    return exams


def load_old_state():
    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_state(exams):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(exams, file, indent=2, ensure_ascii=False)


def send_whatsapp(message_text):
    client = Client(SID, TOKEN)

    for number in RECIPIENTS:
        message = client.messages.create(
            from_="whatsapp:+17372508034",
            to=number,
            body=message_text
        )

        print("WhatsApp sent:", message.sid)


current = get_exam_info()
old = load_old_state()

print("\nCurrent exam information:")
for level, information in current.items():
    print(f"{level}: {information}")

# First run: save information but don't send an alert
if old is None:
    print("\n🆕 First run - saving exam information.")
    save_state(current)

else:
    changes = []

    for level in ["A1", "A2", "B1", "B2"]:
        if current[level] != old.get(level):
            changes.append(
                f"🇩🇪 {level}\n{current[level]}"
            )

    if changes:
        alert = (
            "🔔 GOETHE EXAM UPDATE 🇩🇪\n\n"
            "Hyderabad\n\n"
            + "\n\n".join(changes)
            + "\n\nCheck the official exam page immediately."
        )

        print("\n🚨 CHANGE DETECTED!")
        send_whatsapp(alert)

    else:
        print("\n✅ No exam information changes.")

    save_state(current)

print("\n✅ Exam checker completed.")
