from playwright.sync_api import sync_playwright

URL = "https://trivandrum.german.in/"

KEYWORDS = [
    "api", "ajax", "json", "exam", "seat",
    "registration", "booking", "course"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Opening Kerala portal...")
    
    def handle_response(response):
        url = response.url.lower()
        if any(keyword in url for keyword in KEYWORDS):
            print(f"{response.status} | {response.url}")

    page.on("response", handle_response)

    page.goto(URL, wait_until="networkidle", timeout=60000)

    print("\n========== SELECT ELEMENTS ==========\n")

    selects = page.locator("select")
    count = selects.count()

    print(f"Found {count} select elements.")

    for i in range(count):
        select = selects.nth(i)
        print(f"\nSELECT {i}:")
        print("Name:", select.get_attribute("name"))
        print("ID:", select.get_attribute("id"))

        options = select.locator("option")
        for j in range(options.count()):
            option = options.nth(j)
            print(
                "  ",
                option.inner_text().strip(),
                "| value:",
                option.get_attribute("value")
            )

    print("\n========== PAGE TEXT ==========\n")
    text = page.locator("body").inner_text()
    print(text[:15000])

    browser.close()
