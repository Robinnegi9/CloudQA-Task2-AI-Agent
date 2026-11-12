
from playwright.sync_api import sync_playwright

URL = "https://phptravels.net/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    try:
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)

        print("PAGE:", page.title())
        print("FORMS FOUND:", page.locator("form").count())

        forms = page.locator("form")

        for i in range(forms.count()):
            details = forms.nth(i).evaluate("""
                form => ({
                    id: form.id,
                    method: form.method,
                    action: form.action,

                    fields: Array.from(
                        form.querySelectorAll(
                            "input, button, select, textarea"
                        )
                    ).map(el => ({
                        tag: el.tagName,
                        type: el.type || "",
                        id: el.id || "",
                        name: el.name || "",
                        placeholder:
                            el.getAttribute("placeholder") || "",
                        text: (
                            el.innerText ||
                            el.value ||
                            ""
                        ).trim(),
                        visible: el.getClientRects().length > 0,
                        enabled: !el.disabled
                    }))
                })
            """)

            print(f"\nFORM {i}:")
            print(details)

        for selector in ["#email", "#password"]:
            element = page.locator(selector)

            print(f"\n{selector} count:", element.count())

            if element.count() == 1:
                print(
                    "Associated form:",
                    element.evaluate("""
                        el => {
                            const f = el.closest('form');

                            return f ? {
                                id: f.id,
                                action: f.action,
                                method: f.method
                            } : null;
                        }
                    """)
                )

        input("\nInspection complete. Press Enter to close...")

    finally:
        browser.close()
