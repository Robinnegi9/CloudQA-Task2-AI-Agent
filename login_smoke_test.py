
import os
import re
import json
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright


load_dotenv(override=True)

URL = "https://phptravels.net/login"

EMAIL = os.getenv("TEST_EMAIL")
PASSWORD = os.getenv("TEST_PASSWORD")


def main():

    print("\n================================")
    print("PHPTRAVELS CUSTOMER LOGIN TEST")
    print("================================")

    if not EMAIL or not PASSWORD:
        print("ERROR: Customer credentials missing in .env")
        return

    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    results = {
        "url": URL,
        "login_form_found": False,
        "email_filled": False,
        "password_filled": False,
        "login_submitted": False,
        "dashboard_verified": False,
        "status": "FAIL"
    }

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        try:

            page = browser.new_page()

            print("\nOpening:", URL)

            page.goto(
                URL,
                wait_until="domcontentloaded",
                timeout=45000
            )

            page.wait_for_timeout(2000)

            # 1. Locate exact login form
            login_form = page.locator("form#login-form")

            if login_form.count() != 1:
                raise RuntimeError(
                    "Expected exactly one login form."
                )

            print("Login form: FOUND")

            results["login_form_found"] = True

            # 2. Identify email
            email_field = login_form.locator("#email")

            if email_field.count() != 1:
                raise RuntimeError(
                    "Email field not uniquely identified."
                )

            if not email_field.is_visible():
                raise RuntimeError("Email field is hidden.")

            email_field.fill(EMAIL)

            print("Email field: FILLED")

            results["email_filled"] = True

            # 3. Identify password
            password_field = login_form.locator("#password")

            if password_field.count() != 1:
                raise RuntimeError(
                    "Password field not uniquely identified."
                )

            if not password_field.is_visible():
                raise RuntimeError("Password field is hidden.")

            password_field.fill(PASSWORD)

            print("Password field: FILLED")

            results["password_filled"] = True

            # 4. Identify submit button
            submit_button = login_form.locator(
                'button[type="submit"], input[type="submit"]'
            )

            if submit_button.count() != 1:
                raise RuntimeError(
                    "Expected exactly one login submit button."
                )

            if not submit_button.is_visible():
                raise RuntimeError(
                    "Login submit button is not visible."
                )

            print("Login button: FOUND")

            # 5. Submit login
            submit_button.click(timeout=15000)

            print("Login submitted.")

            results["login_submitted"] = True

            # Wait for navigation or asynchronous response.
            page.wait_for_timeout(4000)

            print("\nPOST-LOGIN INFORMATION")
            print("----------------------------")
            print("Title:", page.title())
            print("URL:", page.url)

            # 6. Independently verify dashboard
            dashboard_text = page.get_by_text(
                re.compile(r"\bdashboard\b", re.IGNORECASE)
            )

            dashboard_found = False

            for i in range(min(dashboard_text.count(), 10)):

                try:
                    if dashboard_text.nth(i).is_visible():
                        dashboard_found = True
                        break
                except Exception:
                    continue

            if dashboard_found:

                print("Dashboard: VERIFIED")

                results["dashboard_verified"] = True
                results["status"] = "PASS"

            else:

                print("Dashboard: NOT VERIFIED")

                # Inspect visible error messages
                body_text = page.locator("body").inner_text()

                print("\nPage message:")
                print(body_text[:2000])

                results["status"] = "FAIL"

            # 7. Screenshot
            page.screenshot(
                path=str(report_dir / "customer_login_result.png"),
                full_page=True
            )

            results["final_url"] = page.url

            # Save report without credentials
            report_path = (
                report_dir / "customer_login_report.json"
            )

            report_path.write_text(
                json.dumps(results, indent=4),
                encoding="utf-8"
            )

            print("\n================================")
            print("CUSTOMER LOGIN TEST REPORT")
            print("================================")

            for key, value in results.items():
                print(f"{key}: {value}")

            print("\nReport saved:", report_path)

            input("\nPress Enter to close browser...")

        except Exception as error:

            results["error"] = str(error)

            print("\nLOGIN TEST ERROR:")
            print(error)

        finally:

            browser.close()


if __name__ == "__main__":
    main()
