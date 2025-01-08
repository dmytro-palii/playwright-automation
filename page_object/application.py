from playwright.sync_api import Playwright
from .test_cases import TestCases
from playwright.sync_api import Browser
from .demo_pages import DemoPages
from playwright.sync_api import Request, Route, ConsoleMessage, Dialog
import logging


class App:
    def __init__(self, browser: Browser, base_url: str, **kwargs):
        """
        Initializes the App class.

        Args:
            browser (Browser): The Playwright browser instance.
            base_url (str): The base URL of the web application.
            **kwargs: Additional parameters for creating a new browser context.
        """
        self.browser = browser
        self.context = self.browser.new_context(**kwargs)
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases = TestCases(self.page)
        self.demo_pages = DemoPages(self.page)

        def console_handler(message: ConsoleMessage):
            if message.type == 'error':
                logging.error(f'page: {self.page.url}, console error: {message.text}')

        def dialog_handler(dialog: Dialog):
            logging.warning(f'page: {self.page.url}, dialog text: {dialog.message}')
            dialog.accept()

        self.page.on('console', console_handler)
        self.page.on('dialog', dialog_handler)

    def goto(self, endpoint: str, use_base_url=True):
        """
        Navigates to a specific endpoint in the application.

        Args:
            endpoint (str): The endpoint or URL to navigate to.
            use_base_url (bool): Whether to prepend the base URL to the endpoint. Defaults to True.
        """
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    def navigate_to(self, menu: str):
        """
        Navigates to a menu item in the application.

        Args:
            menu (str): The name of the menu to navigate to.
        """
        self.page.click(f'css=header >> text="{menu}"')
        self.page.wait_for_load_state()

    def login(self, login: str, password: str):
        """
        Logs into the application using the provided credentials.

        Args:
           login (str): The username or login ID.
           password (str): The password for the account.
        """
        self.page.get_by_label("Username:").fill(login)
        self.page.get_by_label("Password:").fill(password)
        self.page.get_by_role("button", name="Login").click()

    def create_test(self, test_name: str, test_description: str):
        """
        Creates a new test case in the application.

        Args:
            test_name (str): The name of the test case to create.
            test_description (str): A description of the test case.
        """
        self.page.get_by_role("link", name="Create new test").click()
        self.page.locator("#id_name").fill(test_name)
        self.page.get_by_label("Test description").fill(test_description)
        self.page.get_by_role("button", name="Create").click()

    def click_menu_button(self):
        """
        Clicks the menu button in the application.
        """
        self.page.click('.menuBtn')

    def is_menu_button_visible(self):
        """
        Checks whether the menu button is visible in the application.

        Returns:
            bool: True if the menu button is visible, False otherwise.
        """
        return self.page.is_visible('.menuBtn')

    def get_location(self):
        """
        Retrieves the current location text displayed in the application.

        Returns:
            str: The text content of the location element.
        """
        return self.page.text_content('.position')

    def intercept_requests(self, url: str, payload: str):
        def handler(route: Route, request: Request):
            route.fulfill(status=200, body=payload, content_type='application/json')

        self.page.route(url, handler)

    def stop_intercept(self, url: str):
        self.page.unroute(url)

    def refresh_dashboard(self):
        self.page.click('input')
        self.page.wait_for_load_state('networkidle')

    def get_total_tests_stats(self):
        return self.page.text_content('.total >> span')

    def close(self):
        """
        Closes the browser page and context.
        """
        self.page.close()
        self.context.close()
