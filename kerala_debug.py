from playwright.sync_api import sync_playwright

URL = "https://trivandrum.german.in/home-exams?cmbcentre=0"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("Opening Kerala exam portal...")

    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("Page loaded.")

    # Allow JavaScript to finish creating the exam elements
    page.wait_for_timeout(10000)

    print("\n========== PAGE CHECK ==========")

    print("URL:", page.url)
    print("Title:", page.title())

    # Check all select elements
    selects = page.locator("select")

    print("\nSelect count:", selects.count())

    for i in range(selects.count()):

        select = selects.nth(i)

        print(f"\nSELECT {i}")

        print("ID:", select.get_attribute("id"))
        print("Name:", select.get_attribute("name"))
        print("Class:", select.get_attribute("class"))

        options = select.locator("option")

        print("Options:", options.count())

        for j in range(min(options.count(), 10)):

            option = options.nth(j)

            print(
                " ",
                option.inner_text().strip(),
                "| value:",
                option.get_attribute("value")
            )

    print("\n========== EXAM CENTRE SEARCH ==========")

    # Search the HTML for the known centre ID
    html = page.content()

    if "cmbExamCentre" in html:
        print("FOUND: cmbExamCentre")
    else:
        print("NOT FOUND: cmbExamCentre")

    if "Trivandrum" in html:
        print("FOUND: Trivandrum")
    else:
        print("NOT FOUND: Trivandrum")

    if "Remaining Seats" in html:
        print("FOUND: Remaining Seats")
    else:
        print("NOT FOUND: Remaining Seats")

    print("\n========== PAGE TEXT ==========")

    text = page.locator("body").inner_text()

    print(text[:12000])

    browser.close()

print("\n========== DEBUG COMPLETE ==========")
