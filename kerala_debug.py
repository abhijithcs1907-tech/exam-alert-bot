from playwright.sync_api import sync_playwright

URL = "https://trivandrum.german.in/home-exams?cmbcentre=0"

BATCHES = {
    "Trivandrum B2.2": "4151",
    "Kochi B2.2": "4121",
    "Calicut B2.2": "4126"
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Opening Kerala exam portal...")

    def handle_request(request):
        url = request.url.lower()

        if any(x in url for x in [
            "exam", "batch", "seat", "ajax", "api"
        ]):
            print(f"\nREQUEST: {request.method} {request.url}")

            if request.post_data:
                print("POST DATA:", request.post_data)

    def handle_response(response):
        url = response.url.lower()

        if any(x in url for x in [
            "exam", "batch", "seat", "ajax", "api"
        ]):
            print(f"\nRESPONSE: {response.status} {response.url}")

            try:
                text = response.text()

                if text:
                    print("RESPONSE BODY:")
                    print(text[:5000])

            except Exception as e:
                print("Could not read response:", e)

    page.on("request", handle_request)
    page.on("response", handle_response)

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    page.wait_for_timeout(5000)

    print("\n========== SELECT ELEMENTS ==========")

    selects = page.locator("select")

    print("Total selects:", selects.count())

    for i in range(selects.count()):

        select = selects.nth(i)

        options = select.locator("option")

        values = []

        for j in range(options.count()):

            option = options.nth(j)

            text = option.inner_text().strip()
            value = option.get_attribute("value")

            if value in BATCHES.values():
                values.append((text, value))

        if values:

            print("\nSELECT:", i)

            for text, value in values:
                print(
                    "FOUND:",
                    text,
                    "| value:",
                    value
                )

            for text, value in values:

                print("\nSelecting:", text)

                try:
                    select.select_option(value)

                    page.wait_for_timeout(5000)

                    print(
                        "Selected:",
                        select.input_value()
                    )

                except Exception as e:
                    print(
                        "Selection error:",
                        e
                    )

    print("\n========== FINAL PAGE TEXT ==========")

    text = page.locator("body").inner_text()

    print(text[:15000])

    print("\n========== WAITING ==========")

    page.wait_for_timeout(5000)

    browser.close()

print("\n========== DEBUG COMPLETE ==========")
