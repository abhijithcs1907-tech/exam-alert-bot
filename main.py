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


# ============================================================
# GET WEB PAGE
# ============================================================

def get_page_text(url):

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    print(
        f"Page status {response.status_code}: {url}"
    )

    if not response.ok:
        raise Exception(
            f"Page failed: {response.status_code}"
        )

    return response.text


# ============================================================
# HY
