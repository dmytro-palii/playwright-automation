# Playwright Test Project

This project demonstrates a setup for automated testing using Playwright
and Pytest, showcasing common patterns like the Page Object Model (POM).

## Description

This project contains a set of example tests written with Pytest and utilizing
Playwright for browser automation. It includes tests for creating and managing
test cases, interacting with dynamic page elements, and handling browser events.
It's structured to be a starting point for building more complex test suites.

## Prerequisites

*   Python 3.8+
*   pip (Python package installer)

## Installation

1.  **Clone the repository (if applicable):**
[BASH_COMMAND_START]
    git clone <your-repository-url>
    cd CommonProject
[BASH_COMMAND_END]

2.  **Create a virtual environment (recommended):**
[BASH_COMMAND_START]
    python -m venv venv
[BASH_COMMAND_END]
    Activate the virtual environment:
    *   On Windows:
[BASH_COMMAND_START]
        .\venv\Scripts\activate
[BASH_COMMAND_END]
    *   On macOS and Linux:
[BASH_COMMAND_START]
        source venv/bin/activate
[BASH_COMMAND_END]

3.  **Install dependencies:**
    The project uses a `requirements.txt` file to manage its dependencies.
    Install them using pip:
[BASH_COMMAND_START]
    pip install -r requirements.txt
[BASH_COMMAND_END]

4.  **Install Playwright browsers:**
    Playwright needs browser binaries to run tests. Install them with:
[BASH_COMMAND_START]
    playwright install
[BASH_COMMAND_END]
    This will download the default browsers (Chromium, Firefox, WebKit).

## Running Tests

To run all tests, navigate to the `CommonProject` directory in your terminal
(ensure your virtual environment is activated) and execute Pytest:

[BASH_COMMAND_START]
pytest
[BASH_COMMAND_END]

You can also run specific test files:

[BASH_COMMAND_START]
pytest test/test_testcases.py
pytest test/test_demo.py
[BASH_COMMAND_END]

To run tests with specific markers (if defined, e.g., `@pytest.mark.smoke`):

[BASH_COMMAND_START]
# pytest -m smoke
[BASH_COMMAND_END]

## Project Structure

```plaintext
CommonProject/
┣━━ conftest.py               # Pytest fixtures (e.g., desktop_app_auth) and hooks
┣━━ page_object/              # Page Object Model classes
┃   ┣━━ application.py        # Main application class, browser/context setup, common actions
┃   ┣━━ demo_pages.py         # Page objects for demo functionalities
┃   ┗━━ test_cases.py         # Page objects for test case management
┣━━ test/                     # Test files
┃   ┣━━ test_testcases.py     # Tests for test case creation, deletion
┃   ┣━━ test_demo.py          # Tests for demo page interactions
┃   ┗━━ test.log              # Log file for test execution details
┣━━ requirements.txt          # Project dependencies
┗━━ README.md                 # This file
```

## Key Features & Examples

This project demonstrates several key aspects of web automation:

*   **Page Object Model (POM):** Code is organized using POM in the `page_object` directory, promoting maintainability 
* and reusability.
*   **Authentication:** Handled via the `desktop_app_auth` fixture, which provides an authenticated application instance 
* to tests.
*   **Test Case Management:**
    *   Creating new test cases (`test_new_testcase` in `test_testcases.py`).
    *   Verifying test case existence.
    *   Deleting test cases.
*   **Dynamic Content Interaction:**
    *   Waiting for page navigation after actions (`open_page_after_wait` in `demo_pages.py`).
    *   Waiting for AJAX requests to complete (`open_page_and_wait_ajax` in `demo_pages.py`).
*   **Browser Event Handling:**
    *   Capturing and logging console errors (`console_handler` in `application.py`).
    *   Handling and accepting dialogs (alerts, prompts) (`dialog_handler` in `application.py`).
*   **JavaScript Injection:** Demonstrates injecting and executing custom JavaScript on a page (`inject_js` in `demo_pages.py`).
*   **Parameterized Tests:** Uses Pytest's `parametrize` for data-driven testing (`ddt` in `test_testcases.py`).
*   **Request Interception:** (Functionality present in `application.py` - `intercept_request`, `stop_intercept`) - though not explicitly used in the provided test files, the capability exists.

## Fixtures

The primary Pytest fixture used in this project is:

*   `desktop_app_auth` (defined in `conftest.py`): Sets up and provides an authenticated instance of the `App` class to the test functions. This fixture handles browser initialization, context creation, login, and teardown.

The `conftest.py` also likely contains hooks for logging preconditions and postconditions as seen in `test/test.log`.

## Logging

Test execution details, including captured console errors and dialog messages, are logged to `test/test.log`. This is configured in `application.py` and potentially in `conftest.py`. Example log entries:
[BASH_COMMAND_START]
INFO     root:conftest.py:13 preconditions started
ERROR    root:application.py:20 page: http://127.0.0.1:8000/login/?next=/, console message: Failed to load resource: the server responded with a status of 404 (Not Found)
WARNING  root:application.py:23 page: http://127.0.0.1:8000/demo/, dialog message: You have to press Ctrl button
INFO     root:conftest.py:15 postconditions started
[BASH_COMMAND_END]

## Dependencies

This project relies on the following major Python packages (see
`requirements.txt` for the full list and specific versions):

*   playwright: For browser automation.
*   pytest: For test execution and framework capabilities.
*   (Other dependencies as listed in `requirements.txt` such as certifi, requests, etc.)