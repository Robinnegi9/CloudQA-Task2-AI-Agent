# AI Browser Test Automation

## Overview

This project converts a test case written in plain English into browser automation steps using Python, Playwright, and the Gemini API.

The application opens the target website, inspects available page elements, generates an automation plan, executes browser actions, verifies expected results, and saves a test report with screenshot evidence.

## Features

- Accepts a website URL and test case in plain English.
- Inspects webpage elements before automation.
- Uses Gemini AI to generate a structured browser test plan.
- Executes browser actions using Playwright.
- Verifies expected results through assertions.
- Supports a verified local fallback for the PHPTravels customer login workflow when the AI planner is temporarily unavailable.
- Generates JSON test reports and screenshot evidence.
- Uses environment variables for API keys and test credentials.

## Technologies Used

- Python
- Playwright
- Google Gemini API
- HTML, CSS and JavaScript concepts
- JSON
- Python dotenv

## Project Structure

```text
CloudQA-Task2-AI-Agent/
│
├── main.py
├── login_smoke_test.py
├── .env
├── .env.example
├── .gitignore
├── reports/
│   ├── report_*.json
│   └── final_*.png
└── README.md
```

## Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_configured_model
TEST_EMAIL=your_test_email
TEST_PASSWORD=your_test_password
```

Never upload your actual `.env` file or API credentials to GitHub.

## Installation

1. Clone the repository.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment.
4. Install the Python dependencies used by the project.
5. Install the required Playwright browser.
6. Configure the `.env` file.

Example commands for Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

## Running the Application

Run:

```powershell
python main.py
```

Enter the target website URL and describe the test case in plain English.

Example:

**Website URL:**
`https://phptravels.net/login`

**Test case:**

Log in as a customer using the credentials stored in the local environment variables. Verify that the customer dashboard is visible after successful login. Do not make bookings, purchases or payments.

## Execution Flow

1. Accept website URL and natural-language test case.
2. Launch the browser and open the website.
3. Inspect available webpage elements.
4. Generate a structured test plan using Gemini.
5. Execute the planned browser actions using Playwright.
6. Verify the expected results.
7. Save the execution report and screenshot.

If the Gemini API is temporarily unavailable, the application can use its verified local PHPTravels login fallback.

## Test Results

**Test scenario:** PHPTravels customer login.

**Execution result:** PASS

- Email field filled successfully.
- Password field filled successfully.
- Login form submitted successfully.
- Dashboard URL verified.
- Dashboard page title verified.
- Assertions passed: 2/2.

**Final URL:** `https://phptravels.net/dashboard`

The latest execution report and screenshot are available in the `reports/` directory.

Note: The latest successful execution used the local fallback because the Gemini API returned a temporary 504 DEADLINE_EXCEEDED response. The report records this as `local_fallback`.

## Safety

The example login test only verifies customer authentication and dashboard visibility. It does not perform bookings, purchases, or payments.

## Future Improvements

- Support additional websites and test scenarios.
- Improve AI-generated locator reliability.
- Add more assertion types.
- Improve retry and error-handling mechanisms.
- Support additional browser automation workflows.