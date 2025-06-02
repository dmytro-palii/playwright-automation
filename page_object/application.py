import logging
from playwright.sync_api import Browser
from playwright.sync_api import Request, Route, ConsoleMessage, Dialog
from page_object.test_cases import TestCases
from .demo_pages import DemoPages


class App:
    def __init__(self, browser: Browser, base_url: str, **kwargs):
        self.browser = browser
        self.context = self.browser.new_context(**kwargs)
        self.base_url = base_url
        self.page = self.context.new_page()
        self.page.goto("http://127.0.0.1:8000/login/?next=/")
        self.test_cases = TestCases(self.page)
        self.demo_pages = DemoPages(self.page)

        def console_handler(message: ConsoleMessage):
            if message.type == 'error':
                logging.error(f'page: {self.page.url}, console message: {message.text}')

        def dialog_handler(dialog: Dialog):
            logging.warning(f'page: {self.page.url}, dialog message: {dialog.message}')
            dialog.accept()

        self.page.on('console', console_handler)
        self.page.on('dialog', dialog_handler)


    def goto(self, endpoint: str, use_base_url=True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)


    def navigation_to(self, menu: str):
        self.page.click(f"css=header >> text=\"{menu}\"")
        self.page.wait_for_load_state()


    def login(self, login: str, password: str):
        self.page.fill("input[name=\"username\"]", login)
        self.page.fill("input[name=\"password\"]", password)
        self.page.press("input[name=\"password\"]", "Enter")


    def create_test(self, test_name: str, test_description: str):
        self.page.fill("#id_name", test_name)
        self.page.fill("#id_description", test_description)
        self.page.click('input[type="submit"][value="Create"]')


    def click_menu_button(self):
        self.page.click('.menuBtn')


    def is_menu_button_visible(self):
        return self.page.is_visible('.menuBtn')


    def get_location(self):
        return self.page.text_content('.position')


    def intercept_request(self, url: str, payload: str):
        def handler(route: Route, request: Request):
            route.fulfill(status=200, body=payload)

        self.page.route(url, handler)


    def stop_intercept(self, url: str):
        self.page.unroute(url)


    def refresh_dashboard(self):
        self.page.click('input')


    def get_total_tests_stats(self):
        return self.page.text_content('.total >> span')


    def close(self):
        self.page.close()
        self.context.close()
