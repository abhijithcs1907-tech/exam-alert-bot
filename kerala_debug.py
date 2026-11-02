from playwright.sync_api import sync_playwright

URL = "https://trivandrum.german.in/home-exams?cmbcentre=0"

KEYWORDS = [
    "api", "ajax", "json", "exam", "seat",
    "registration", "booking", "batch", "centre", "center"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Opening Kerala exam portal...")

    def handle_request(request):
        url = request.url.lower()

        if any(k in url for k in KEYWORDS):
            print(f"\nREQUEST: {request.method} {request.url}")

            if request.post_data:
                print("POST DATA:", request.post_data)

    def handle_response(response):
        url = response.url.lower()

        if any(k in url for k in KEYWORDS):
            print(f"\nRESPONSE: {response.status} {response.url}")

    page.on("request", handle_request)
    page.on("response", handle_response)

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    print("\n========== CENTRE DROPDOWN ==========")

    centre = page.locator("#cmbExamCentre")

    print("Centre count:", centre.count())

    if centre.count() > 0:
        options = centre.locator("option")

        for i in range(options.count()):
            option = options.nth(i)

            print(
                i,
                "|",
                option.inner_text().strip(),
                "| value:",
                option.get_attribute("value")
            )

    centres = {
        "Trivandrum": "1",
        "Kochi": "3",
        "Calicut": "4"
    }

    for centre_name, centre_value in centres.items():

        print("\n\n========================================")
        print("TESTING CENTRE:", centre_name)
        print("========================================")

        page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )

        centre = page.locator("#cmbExamCentre")

        if centre.count() == 0:
            print("Centre dropdown not found.")
            continue

        print("Selecting:", centre_name)

        centre.select_option(centre_value)

        page.wait_for_timeout(3000)

        print("\n--- Exam dropdowns after centre selection ---")

        selects = page.locator("select")

        for i in range(selects.count()):

            select = selects.nth(i)

            try:
                options = select.locator("option")

                visible_options = []

                for j in range(options.count()):

                    option = options.nth(j)

                    text = option.inner_text().strip()
                    value = option.get_attribute("value")

                    if text and text != "--Select--":
                        visible_options.append(
                            f"{text} | value={value}"
                        )

                if visible_options:

                    print(f"\nSELECT {i}:")

                    for item in visible_options:
                        print(" ", item)

            except Exception as e:
                print("Select error:", e)

        print("\nWaiting for additional network requests...")

        page.wait_for_timeout(3000)

    browser.close()

print("\n========== DEBUG COMPLETE ==========")
