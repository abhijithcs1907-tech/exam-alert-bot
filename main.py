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
    "Goethe Coimbatore": "https://www.goethecoimbatore.com/exam/",
    "Goethe Kerala": "https://trivandrum.german.in/home-exams?cmbcentre=0"
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

    return response.text


def get_hyderabad(text):
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text(" ", strip=True)

    exams = {}

    for level in ["A1", "A2", "B1", "B2"]:
        pattern = rf"GOETHE-ZERTIFIKAT {level}.*?(?=GOETHE-ZERTIFIKAT|Important Notice:|$)"
        matches = re.findall(
            pattern,
            clean_text,
            re.IGNORECASE
        )

        exams[level] = (
            matches[0].strip()
            if matches
            else "No information found"
        )

    return exams


def get_coimbatore(text):
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text(" ", strip=True)

    patterns = {
        "A1": r"Goethe-Zertifikat A1:.*?(?=Goethe-Zertifikat A2|Goethe-Zertifikat B1|Goethe-Zertifikat B2|$)",
        "A2": r"Goethe-Zertifikat A2.*?(?=Goethe-Zertifikat A1|Goethe-Zertifikat B1|Goethe-Zertifikat B2|$)",
        "B1": r"Goethe-Zertifikat B1.*?(?=Goethe-Zertifikat A1|Goethe-Zertifikat A2|Goethe-Zertifikat B2|$)",
        "B2": r"Goethe-Zertifikat B2.*?(?=Goethe-Zertifikat A1|Goethe-Zertifikat A2|Goethe-Zertifikat B1|$)"
    }

    exams = {}

    for level, pattern in patterns.items():
        matches = re.findall(
            pattern,
            clean_text,
            re.IGNORECASE
        )

        exams[level] = (
            matches[0].strip()
            if matches
            else "No information found"
        )

    return exams


def get_kerala(text):
    """
    Kerala official exam endpoint returns JSON.

    We only track published exam batches.
    Remaining seats are intentionally NOT tracked.
    """

    data = json.loads(text)

    exams = {}

    for item in data:
        exam_name = item.get("exam_name", "").strip()

        centre_list = item.get("centre", [])

        if not centre_list:
            continue

        centre = centre_list[0].get("name", "").strip()

        if not centre:
            continue

        key = f"{exam_name} - {centre}"

        batches = item.get("exam_batch", [])

        published_batches = []

        for batch in batches:
            batch_id = str(batch.get("batch_id", ""))
            display_name = batch.get(
                "exam_display_name",
                ""
            ).strip()

            if batch_id and display_name:
                published_batches.append({
                    "batch_id": batch_id,
                    "exam_display_name": display_name
                })

        exams[key] = published_batches

    return exams


def get_all_exams():
    all_exams = {}

    # Hyderabad
