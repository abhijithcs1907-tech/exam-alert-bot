import re
from playwright.sync_api import sync_playwright

URL = "https://trivandrum.german.in/home-exams?cmbcentre=0"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("Opening Kerala exam portal...")

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    page.wait_for_timeout(5000)

    print("\n========== SCRIPTS ==========")

    scripts = page.locator("script")

    print("Script count:", scripts.count())

    for i in range(scripts.count()):

        script = scripts.nth(i)

        src = script.get_attribute("src")

        if src:
            print(f"\nSCRIPT {i}: {src}")

        else:
            text = script.inner_text()

            if any(word in text.lower() for word in [
                "exam_batch",
                "remaining",
                "seat",
                "batch_id",
                "cmbexamcentre",
                "home-exams"
            ]):
                print(f"\nINLINE SCRIPT {i}:")
                print(text[:10000])

    print("\n========== PAGE HTML SEARCH ==========")

    html = page.content()

    keywords = [
        "remaining",
        "seat",
        "batch_id",
        "exam_batch",
        "cmbExamCentre",
        "ajax",
        "api"
    ]

    for keyword in keywords:

        print(
            keyword,
            "=>",
            keyword.lower() in html.lower()
        )

    print("\n========== POSSIBLE URLS ==========")

    urls = re.findall(
        r'https?://[^"\']+',
        html
    )

    for url in urls:

        if any(word in url.lower() for word in [
            "api",
            "ajax",
            "exam",
            "batch"
        ]):
            print(url)

    browser.close()

print("\n========== DEBUG COMPLETE ==========")
