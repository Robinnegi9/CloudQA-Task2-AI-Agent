# Approach and Limitations – Task 2

## Approach

I developed an AI-assisted browser test automation tool using Python, Playwright, and the Google Gemini API.

The application accepts two inputs from the user:

- Website URL
- Test case written in plain English

The application opens the website using Playwright and inspects the available page elements.

The Gemini API is used to convert the natural-language test case into a structured test plan. The generated plan is then executed through browser automation.

The application verifies the expected outcomes using assertions and generates a JSON execution report. It also saves a screenshot of the final browser state.

Environment variables are used to manage API credentials and test login credentials instead of hardcoding them into the source code.

A local fallback mechanism is also included for supported test scenarios when AI planning is unavailable.

## Limitations

- AI planning depends on the availability and response time of the Gemini API.
- AI-generated plans may require additional validation for complex or ambiguous test cases.
- The local fallback supports only predefined scenarios and is not a general replacement for AI planning.
- Complex interactions such as CAPTCHA, multi-factor authentication, and highly dynamic interfaces may require additional handling.
- The current implementation has been tested with the PHPTravels login scenario; broader website compatibility requires further testing.

## Testing

The PHPTravels customer login scenario was executed using Playwright.

The successful fallback execution verified the dashboard URL and page title through assertions. The application generated a JSON report and a screenshot.

An AI planning request may fail temporarily if the Gemini service is unavailable.