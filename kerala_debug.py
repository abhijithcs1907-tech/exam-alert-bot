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
        print(f"\nREQUEST: {request.method} {request.url}")

        if request.post_data:
            print("POST DATA:", request.post_data)

    def handle_response(response):
        print(f"\nRESPONSE: {response.status} {response.url}")

        try:
            content_type = response.headers.get("content-type", "")

            if "json" in content_type.lower():
                text = response.text()

                print("JSON RESPONSE:")
                print(text[:5000])

        except Exception as e:
            print("Response read error:", e)

    page.on("request", handle_request)
    page.on("response", handle_response)

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    page.wait_for_timeout(5000)

    print("\n========== BATCH DATA ==========")

    html = page.content()

    for name, batch_id in BATCHES.items():

        print("\n================================")
        print(name)
        print("Batch ID:", batch_id)
        print("================================")

        if batch_id in html:
            print("Batch ID FOUND in page.")
        else:
            print("Batch ID NOT FOUND in page.")

    print("\n========== WAITING FOR NETWORK ==========")

    page.wait_for_timeout(10000)

    print("\n========== DEBUG COMPLETE ==========")

    browser.close()
