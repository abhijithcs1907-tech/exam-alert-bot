import os
import json
import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

STATE_FILE = "exam_state.json"

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


CENTRES = {
    "Goethe Hyderabad": "https://hyderabad.german.in/",
    "Goethe Coimbatore": "https://www.goethecoimbatore.com/exam/",
    "Goethe Kerala": "https://trivandrum.german.in/"
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


def get_rendered_kerala_text(url):
    print("🌐 Opening Kerala portal with Chromium...")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 1440,
                "height": 2000
            }
        )

        page.goto(
            url,
            wait_until="networkidle",
            timeout=60000
        )

        # Give the website's JavaScript time to populate exam data.
        page.wait_for_timeout(5000)

        text = page.locator("body").inner_text()

        browser.close()

    print("✅ Kerala rendered page loaded.")

    return text


def get_hyderabad(text):
    exams = {}

    for level in ["A1", "A2", "B1", "B2"]:

        pattern = (
            rf"GOETHE-ZERTIFIKAT {level}"
            rf".*?"
            rf"(?=GOETHE-ZERTIFIKAT|Important Notice:|$)"
        )

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        exams[level] = (
            matches[0].strip()
            if matches
            else "No information found"
        )

    return exams


def get_coimbatore(text):

    patterns = {
        "A1": (
            r"Goethe-Zertifikat A1:.*?"
            r"(?=Goethe-Zertifikat A2|Goethe-Zertifikat B1|"
            r"Goethe-Zertifikat B2|$)"
        ),

        "A2": (
            r"Goethe-Zertifikat A2.*?"
            r"(?=Goethe-Zertifikat A1|Goethe-Zertifikat B1|"
            r"Goethe-Zertifikat B2|$)"
        ),

        "B1": (
            r"Goethe-Zertifikat B1.*?"
            r"(?=Goethe-Zertifikat A1|Goethe-Zertifikat A2|"
            r"Goethe-Zertifikat B2|$)"
        ),

        "B2": (
            r"Goethe-Zertifikat B2.*?"
            r"(?=Goethe-Zertifikat A1|Goethe-Zertifikat A2|"
            r"Goethe-Zertifikat B1|$)"
        )
    }

    exams = {}

    for level, pattern in patterns.items():

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        exams[level] = (
            matches[0].strip()
            if matches
            else "No information found"
        )

    return exams


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_kerala(text):

    text = clean_text(text)

    sections = {
        "Goethe Trivandrum": {
            "A1": r"A1 Level \| Trivandrum",
            "A2": r"A2 Level \| Trivandrum",
            "B1": r"B1 Level \| Trivandrum",
            "B2.2": r"B2\.2 Level \| Trivandrum"
        },

        "Goethe Kochi": {
            "A1": r"A1 Level \| Kochi",
            "A2": r"A2 Level \| Kochi",
            "B1": r"B1 Level \| Kochi",
            "B2.2": r"B2\.2 Level \| Kochi"
        },

        "Goethe Calicut": {
            "B2.2": r"B2\.2 Level \| Calicut"
        }
    }

    all_data = {}

    # All Kerala exam headings
    heading_pattern = (
        r"(A1|A2|B1|B2\.2) Level \| "
        r"(Trivandrum|Kochi|Calicut)"
    )

    headings = list(
        re.finditer(
            heading_pattern,
            text,
            re.IGNORECASE
        )
    )

    extracted_sections = {}

    for i, match in enumerate(headings):

        level = match.group(1).upper()
        centre = match.group(2).title()

        start = match.start()

        if i + 1 < len(headings):
            end = headings[i + 1].start()
        else:
            end = len(text)

        section_text = text[start:end]

        extracted_sections[
            f"Goethe {centre}"
        ] = extracted_sections.get(
            f"Goethe {centre}",
            {}
        )

        extracted_sections[
            f"Goethe {centre}"
        ][level] = section_text

    # Convert sections into clean information
    for centre, levels in sections.items():

        all_data[centre] = {}

        for level in levels:

            section = extracted_sections.get(
                centre,
                {}
            ).get(level)

            if not section:

                all_data[centre][level] = (
                    "No information found"
                )

                continue

            section = clean_text(section)

            # Remove repeated heading
            section = re.sub(
                rf"^{level} Level \| "
                rf"{centre.replace('Goethe ', '')}\s*",
                "",
                section,
                flags=re.IGNORECASE
            )

            # Keep useful information
            useful = []

            keywords = [
                "Exam Date",
                "Registration Date",
                "Exam Fees",
                "Remaining Seats"
            ]

            for keyword in keywords:

                match = re.search(
                    rf"{re.escape(keyword)}\s*(.*?)"
                    rf"(?=(?:Exam Date|Registration Date|"
                    rf"Exam Fees|Remaining Seats|Register for Exam)|$)",
                    section,
                    re.IGNORECASE
                )

                if match:

                    value = match.group(1).strip()

                    if value:
                        useful.append(
                            f"{keyword}: {value}"
                        )

            if useful:

                all_data[centre][level] = (
                    " | ".join(useful)
                )

            else:

                all_data[centre][level] = section

    return all_data


def get_all_exams():

    all_exams = {}

    # Hyderabad + Coimbatore
    for centre, url in CENTRES.items():

        if centre == "Goethe Kerala":
            continue

        text = get_page_text(url)

        if centre == "Goethe Hyderabad":
            all_exams[centre] = get_hyderabad(text)

        elif centre == "Goethe Coimbatore":
            all_exams[centre] = get_coimbatore(text)

    # Kerala
    kerala_text = get_rendered_kerala_text(
        CENTRES["Goethe Kerala"]
    )

    kerala_data = get_kerala(
        kerala_text
    )

    all_exams.update(
        kerala_data
    )

    return all_exams


def load_old_state():

    if not os.path.exists(STATE_FILE):
        return None

    with open(
        STATE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_state(data):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def send_telegram(message_text):

    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text
    }

    response = requests.post(
        url,
        data=data,
        timeout=30
    )

    print(
        "Telegram status:",
        response.status_code
    )

    if not response.ok:

        print(
            "Telegram error:",
            response.text
        )

    else:

        print(
            "Telegram alert sent successfully."
        )


# ============================================================
# MAIN
# ============================================================

current = get_all_exams()

old = load_old_state()

print(
    "\n========== CURRENT EXAM INFORMATION ==========\n"
)

for centre, exams in current.items():

    print(f"📍 {centre}")

    for level, info in exams.items():

        print(
            f"{level}: {info}"
        )

    print()


# First run
if old is None:

    print(
        "🆕 First combined run - saving state only."
    )

    save_state(current)


else:

    changes = []

    for centre in current:

        for level, new_info in current[
            centre
        ].items():

            old_info = old.get(
                centre,
                {}
            ).get(level)

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
            + "\n\n"
            "⚡ Check the official registration page immediately."
        )

        print(
            "\n🚨 EXAM CHANGE DETECTED!"
        )

        send_telegram(alert)

    else:

        print(
            "✅ No exam information changes."
        )

    save_state(current)


print(
    "\n✅ Combined exam checker completed."
            )
