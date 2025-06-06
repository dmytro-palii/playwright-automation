````markdown
# Playwright Test Project

This project demonstrates a setup for automated testing using Playwright  
and Pytest, showcasing common patterns like the Page Object Model (POM),  
multiple user roles, direct database interaction, web‐service calls, and  
Allure reporting.

---

## Description

This repository contains a suite of example tests written with Pytest and  
Playwright. It covers:  
┣━━ Creating, verifying, and deleting test cases via UI and API  
┣━━ Interacting with dynamic page elements (AJAX waits, delayed navigation)  
┣━━ Handling browser events (console errors, dialogs, screenshots on failure)  
┣━━ Testing with multiple user roles  
┣━━ Direct database operations for setup/teardown  
┣━━ Web‐service/API interaction (token‐based login, CRUD operations)  
┣━━ Generating Allure test reports (with screenshots)  

It’s intended as a starting point or template for building robust,  
data‐driven, cross‐browser test suites.

---

## Prerequisites

*  Python 3.8+  
*  pip (Python package installer)  
*  Java 8+ (for Allure command‐line)  
*  Git (for version control)  

---

## Installation & Configuration

1.  **Clone the repository:**  
    ```bash
    git clone git@github.com:dmytro-palii/playwright-automation.git
    cd playwright-automation/CommonProject
    ```

2.  **Create a virtual environment (recommended):**  
    ```bash
    python -m venv venv
    ```  
    Activate it:  
    ┣━━ **Windows PowerShell:**  
    ┃   ```powershell
    ┃   .\venv\Scripts\Activate.ps1
    ┃   ```  
    ┣━━ **Windows CMD:**  
    ┃   ```cmd
    ┃   .\venv\Scripts\activate.bat
    ┃   ```  
    ┗━━ **macOS/Linux:**  
      ```bash
      source venv/bin/activate
      ```

3.  **Install Python dependencies:**  
    ```bash
    pip install -r requirements.txt
    ```  
    > This includes:  
    > ┣━━ `playwright`  
    > ┣━━ `pytest`  
    > ┗━━ `allure-pytest`  
    > and any database or HTTP‐client libs (e.g., `requests`, `sqlite3` support)

4.  **Install Playwright browser binaries:**  
    ```bash
    playwright install
    ```  
    > Downloads Chromium, Firefox, and WebKit by default.

5.  **Configure settings & secrets:**  
    ┣━━ **settings.py**  
    ┃   Contains configuration constants (e.g., `BASE_URL`). Adjust to match your environment.  
    ┗━━ **secure.json**  
      Holds credentials or API tokens for test users. Add real values, but **never commit** this file.  
      ```json
      {
        "alice": { "username": "alice", "password": "Qamania123" },
        "bob":   { "username": "bob",   "password": "Qamania123" }
      }
      ```  
    > Make sure `secure.json` is listed in `.gitignore`.

6.  **Pytest configuration (`pytest.ini`):**  
    ```ini
    [pytest]
    addopts = 
        --base-url http://127.0.0.1:8000 
        --secure secure.json 
        --device "iPhone 11" 
        --my-browser chromium 
        --junitxml=report/report.xml
    db_path = D:\AutotestLearn\Playwright\CommonProject\TestMe-TCM\db.sqlite3
    headless = True
    ```  
    ┣━━ `--junitxml=report/report.xml` tells pytest to produce a JUnit‐style XML in `report/`.  
    ┗━━ `db_path` points to your SQLite file (used by `get_db` fixture).

---

## Project Structure

```plaintext
CommonProject/
┣━━ conftest.py               # Pytest fixtures and hooks
┃   ┣━━ desktop_app_auth      # Fixture for authenticated browser as Alice
┃   ┣━━ desktop_app_bob       # Fixture for authenticated browser as Bob
┃   ┣━━ get_db                # Fixture for direct SQLite interaction
┃   ┗━━ get_webservice        # Fixture for token‐based API operations
┣━━ helpers/                  # Helper modules (DB, WebService wrappers)
┃   ┣━━ db.py                 # DataBase class (SQLite CRUD for test setup)
┃   ┗━━ web_services.py       # WebService class for API calls (login, create_test, etc.)
┣━━ page_object/              # Page Object Model classes
┃   ┣━━ application.py        # Main App class (browser/context setup, common actions)
┃   ┣━━ demo_pages.py         # DemoPages POM (wait for AJAX, delayed navigation)
┃   ┗━━ test_cases.py         # TestCases POM (create/delete tests, verify existence)
┣━━ report/                   # Output folder for Allure and JUnit reports
┃   ┣━━ allure-results/       # Raw Allure result files (generated at runtime)
┃   ┗━━ allure-report/        # Generated HTML report (after `allure serve`)
┣━━ test/                     # Test files
┃   ┣━━ test_dashboard.py     # Dashboard-related tests (intercept, stats)
┃   ┣━━ test_demo.py          # Demo page interaction tests (AJAX, delayed load)
┃   ┣━━ test_location.py      # GeoLocation test (mobile and desktop)
┃   ┣━━ test_mobile.py        # Mobile viewport tests (columns hidden, layout)
┃   ┣━━ test_testcases.py     # Test case CRUD tests (UI + DB + API variants)
┃   ┗━━ test.log              # Live log of each test run (logs pre/postconditions)
┣━━ requirements.txt          # Project dependencies (pip freeze)
┗━━ README.md                 # This file
````

---

## Running Tests

1. Ensure your virtual environment is activated and you’re in `CommonProject/`.

2. **Launch tests with Pytest** (uses `pytest.ini` defaults):

   ```bash
   pytest
   ```

   ┣━━ Generates:
   ┃   ┣━━ JUnit XML at `report/report.xml`
   ┃   ┗━━ Allure raw results under `report/allure-results/`
   ┗━━ Detailed console output

3. **View Allure Report:**

   ```bash
   allure serve report/allure-results
   ```

   ┗━━ Starts a local server and opens the HTML UI.

4. **Run Specific Test Files:**

   ```bash
   pytest test/test_testcases.py
   pytest test/test_demo.py
   ```

5. **Run with markers (e.g., smoke tests):**

   ```bash
   pytest -m smoke
   ```

6. **Override configuration flags:**

   ```bash
   pytest --headless=False --my-browser=firefox
   ```

---

## Key Features & Examples

┣━━ **Page Object Model (POM):**
┃   All UI interactions are encapsulated in `page_object/`. This ensures reusability:
┃   ┣━━ `application.py`: Browser/context setup, common navigation, intercepts & dialog handlers
┃   ┣━━ `demo_pages.py`: AJAX waits, delayed navigation (`open_page_after_wait`, `open_page_and_wait_ajax`)
┃   ┗━━ `test_cases.py`: Test case CRUD on UI (`create_test`, `check_test_exists`, `delete_test_by_name`)

┣━━ **Authentication Fixtures:**
┃   ┣━━ `desktop_app_auth` — Authenticated Playwright `App` object for Alice (UI).
┃   ┗━━ `desktop_app_bob`  — Authenticated Playwright `App` object for Bob (UI).

┣━━ **Direct Database Interaction (`get_db` fixture):**
┃   ┣━━ Uses `helpers/db.py` to connect to SQLite (`db_path` from `pytest.ini`).
┃   ┗━━ Example: `get_db.list_test_cases()` and `get_db.delete_test_cases(name)` in tests.

┣━━ **Web Service/API Interaction (`get_webservice` fixture):**
┃   ┣━━ Uses `helpers/web_services.py` to:
┃   ┃   ┣━━ Log in via API (token retrieval).
┃   ┃   ┗━━ Call endpoints like `POST /create_test`, `DELETE /delete_test`, etc.
┃   ┗━━ Enables creating or cleaning up test data without UI.

┣━━ **Mobile & GeoLocation Testing:**
┃   ┣━━ `mobile_app`, `mobile_app_auth` fixtures (with `--device` option) test responsive/mobile behavior.
┃   ┗━━ `test_location.py` checks geoLocation permissions and displayed coordinates.

┣━━ **Dynamic Content & Event Handling:**
┃   ┣━━ `demo_pages.py` demonstrates:
┃   ┃   ┣━━ Delayed navigation (`waitPage` link) using `expect_navigation`
┃   ┃   ┗━━ Waiting for AJAX requests to finish (`networkidle`)
┃   ┗━━ `application.py` includes `console_handler` to capture console errors and write to `test/test.log`.
┃   ┣━━ `dialog_handler` automatically accepts or logs alerts/prompts.
┃   ┗━━ On test failure, a screenshot is automatically captured and attached to Allure results.

┣━━ **Testing with Multiple User Roles:**
┃   ┣━━ Run the same test as Alice and Bob to verify role‐specific behavior (e.g., `desktop_app_bob` fixture).

┣━━ **Parameterized Tests & Data‐Driven Testing:**
┃   ┗━━ `pytest.mark.parametrize` with data sets defined in `test_testcases.py` for names/descriptions.

┣━━ **Request Interception & Mocking:**
┃   ┗━━ In `application.py`, `intercept_request` and `stop_intercept` allow you to stub or inspect network calls.

┣━━ **Reporting & Logging:**
┃   ┣━━ Console logs and errors get written to `test/test.log` via Pytest hooks and `application.py` handlers.
┃   ┣━━ **Allure integration (`allure-pytest`)** generates detailed HTML reports with:
┃   ┃   ┣━━ Step logs
┃   ┃   ┣━━ Attachments (screenshots, console logs, page HTML on failure)
┃   ┃   ┗━━ Test metadata (browser, device, parameters)
┃   ┗━━ **JUnit XML** for CI integration at `report/report.xml`.

---

## Fixtures Overview

┣━━ **desktop\_app\_auth** — Authenticated Playwright `App` object for Alice (UI).
┣━━ **desktop\_app\_bob** — Authenticated Playwright `App` object for Bob (UI).
┣━━ **mobile\_app** — Playwright `App` configured for a mobile device (`--device`).
┣━━ **mobile\_app\_auth** — Authenticated mobile `App` for Alice or Bob.
┣━━ **get\_db** — Direct SQLite access via `helpers/db.py` (reads `db_path` from `pytest.ini`).
┣━━ **get\_webservice** — API client via `helpers/web_services.py` to log in, create/delete tests.
┣━━ **console\_handler** (in `application.py`) — Captures and logs browser console messages.
┗━━ **dialog\_handler** (in `application.py`) — Automatically accepts or logs dialogs (alerts/prompts).

---

## Example: `secure.json` (added to .gitignore)

```json
{
  "alice": {
    "username": "alice",
    "password": "Qamania123"
  },
  "bob": {
    "username": "bob",
    "password": "Qamania123"
  }
}
```

> **Security Note:** Do not commit real credentials. Keep `secure.json` local and add it to `.gitignore`.

---

## Example: `pytest.ini`

```ini
[pytest]
addopts = 
    --base-url http://127.0.0.1:8000
    --secure secure.json
    --device "iPhone 11"
    --my-browser chromium
    --junitxml=report/report.xml
db_path = D:\AutotestLearn\Playwright\CommonProject\TestMe-TCM\db.sqlite3
headless = True
```

━ `addopts` ensures default CLI args.
━ `db_path` is used by `get_db` fixture.
━ `--junitxml` writes a JUnit XML report at `report/report.xml` (CI integration).

---

## Dependencies

See `requirements.txt` for exact versions. Major dependencies include:

┣━━ **playwright** — Browser automation.
┣━━ **pytest** — Test framework.
┣━━ **allure-pytest** — Allure integration plugin.
┣━━ **requests** — For `helpers/web_services.py` API calls.
┣━━ **sqlite3** (built-in) — For direct DB operations in `get_db` fixture.
┗━━ **pytest-cov**, **pytest-html** (if present) for coverage and HTML reporting.

---

## Support & Further Reading

┣━━ [Playwright Python Docs](https://playwright.dev/python/)
┣━━ [Pytest Documentation](https://docs.pytest.org/)
┣━━ [Allure Framework](https://docs.qameta.io/allure/)
┗━━ [Page Object Model Pattern](https://martinfowler.com/bliki/PageObject.html)

Feel free to explore and extend this template for your own automation needs!

```
```
