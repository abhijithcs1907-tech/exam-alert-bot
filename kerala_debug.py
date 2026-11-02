from playwright.sync_api import sync_playwright

URL = "https://trivandrum.german.in/"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("Opening official Kerala portal...")

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    page.wait_for_timeout(5000)

    # =====================================================
    # SELECT ELEMENTS
    # =====================================================

    print("\n========== SELECT ELEMENTS ==========")

    selects = page.locator("select")

    print(
        "Total selects:",
        selects.count()
    )

    for i in range(selects.count()):

        select = selects.nth(i)

        select_id = select.get_attribute("id")
        select_name = select.get_attribute("name")

        print(
            f"\nSELECT {i}"
        )

        print(
            "ID:",
            select_id
        )

        print(
            "NAME:",
            select_name
        )

        options = select.locator("option")

        print(
            "Options:",
            options.count()
        )

        for j in range(
            min(options.count(), 30)
        ):

            option = options.nth(j)

            text = option.inner_text().strip()

            value = option.get_attribute(
                "value"
            )

            print(
                f"  {j}: {text} | value={value}"
            )


    # =====================================================
    # BUTTONS
    # =====================================================

    print(
        "\n========== BUTTONS =========="
    )

    buttons = page.locator(
        "button"
    )

    print(
        "Total buttons:",
        buttons.count()
    )

    for i in range(
        buttons.count()
    ):

        button = buttons.nth(i)

        try:
            text = button.inner_text().strip()
        except:
            text = ""

        button_id = button.get_attribute(
            "id"
        )

        button_class = button.get_attribute(
            "class"
        )

        print(
            f"\nBUTTON {i}"
        )

        print(
            "Text:",
            text
        )

        print(
            "ID:",
            button_id
        )

        print(
            "Class:",
            button_class
        )


    # =====================================================
    # LINKS
    # =====================================================

    print(
        "\n========== LINKS =========="
    )

    links = page.locator(
        "a"
    )

    print(
        "Total links:",
        links.count()
    )

    for i in range(
        links.count()
    ):

        link = links.nth(i)

        try:
            text = link.inner_text().strip()
        except:
            text = ""

        href = link.get_attribute(
            "href"
        )

        if (
            "register" in text.lower()
            or "exam" in text.lower()
            or "register" in str(href).lower()
            or "exam" in str(href).lower()
        ):

            print(
                f"\nLINK {i}"
            )

            print(
                "Text:",
                text
            )

            print(
                "HREF:",
                href
            )


    # =====================================================
    # REGISTRATION TEXT
    # =====================================================

    print(
        "\n========== REGISTRATION TEXT =========="
    )

    body_text = page.locator(
        "body"
    ).inner_text()

    lines = body_text.splitlines()

    for line in lines:

        line = line.strip()

        if any(
            word in line.lower()
            for word in [
                "registration",
                "register for exam",
                "registration starts",
                "exam date",
                "remaining seats"
            ]
        ):

            print(
                line
            )


    # =====================================================
    # PAGE HTML SEARCH
    # =====================================================

    print(
        "\n========== HTML KEYWORDS =========="
    )

    html = page.content()

    keywords = [
        "Registration Date",
        "Register for Exam",
        "registration",
        "register",
        "batch_id",
        "cmbExamCentre"
    ]

    for keyword in keywords:

        print(
            keyword,
            "=>",
            keyword.lower() in html.lower()
        )


    browser.close()


print(
    "\n========== DIAGNOSTIC COMPLETE =========="
)
