import json
import logging
import os.path
import pytest
from pytest import fixture
from playwright.sync_api import sync_playwright
from page_object.application import App
from settings import *


@fixture(autouse=True, scope='session')
def preconditions():
    """
    Setup preconditions before the test session and teardown postconditions afterward.

    Yields:
        None
    """
    logging.info('setup preconditions state')
    yield
    logging.info('setup post condition state')


@fixture(scope='session')
def get_playwright():
    """
    Initializes the Playwright instance.

    Yields:
        playwright: The Playwright instance.
    """
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session', params=['chromium'])
def get_browser(get_playwright, request):
    """
    Initializes the browser instance based on the specified browser type.

    Args:
        get_playwright: The Playwright instance.
        request: Pytest request object to get parameters.

    Yields:
        bro: The browser instance.
    """
    browser = request.param
    headless = request.config.getoption('--headless').lower() == 'true'
    os.environ['PWBRROWSER'] = browser

    if browser == 'chromium':
        bro = get_playwright.chromium.launch(headless=headless)
    elif browser == 'firefox':
        bro = get_playwright.firefox.launch(headless=headless)
    elif browser == 'webkit':
        bro = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, 'unsupported browser'

    yield bro
    bro.close()
    del os.environ['PWBRROWSER']


@fixture(scope='session')
def desktop_app(get_browser, request):
    """
    Initializes the desktop application instance.

    Args:
        get_browser: The browser instance.
        request: Pytest request object to access options.

    Yields:
        app: The App instance for the desktop application.
    """
    base_url = request.config.getoption('base_url')
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def desktop_app_auth(desktop_app, request):
    """
    Initializes the authenticated desktop application instance.

    Args:
        desktop_app: The App instance for the desktop application.
        request: Pytest request object to access options.

    Yields:
        desktop_app: The authenticated App instance.
    """
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    desktop_app.goto('/login')
    desktop_app.login(**config)
    yield desktop_app


@fixture(scope='session', params=['iPhone 11', 'Pixel 2'])
def mobile_app(get_playwright, get_browser, request):
    """
    Initializes the mobile application instance for specified devices.

    Args:
        get_playwright: The Playwright instance.
        get_browser: The browser instance.
        request: Pytest request object to access options.

    Yields:
        app: The App instance for the mobile application.
    """
    if os.environ.get('PWBRROWSER') == 'firefox':
        pytest.skip()
    base_url = request.config.getoption('base_url')
    device = request.param
    device_config = get_playwright.devices.get(device)
    if device_config is not None:
        device_config.update(BROWSER_OPTIONS)
    else:
        device_config = BROWSER_OPTIONS
    app = App(get_browser, base_url=base_url, **device_config)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def mobile_app_auth(mobile_app, request):
    """
    Initializes the authenticated mobile application instance.

    Args:
        mobile_app: The App instance for the mobile application.
        request: Pytest request object to access options.

    Yields:
        mobile_app: The authenticated App instance.
    """
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    mobile_app.goto('/login')
    mobile_app.login(**config)
    yield mobile_app


def pytest_addoption(parser):
    """
    Adds custom command-line options for pytest.

    Args:
        parser: The pytest parser object to add options.
    """
    parser.addoption('--secure', action='store', default='secure.json', help='Path to secure configuration file')
    parser.addoption('--device', action='store', default='', help='Device to emulate (e.g., iPhone 11)')
    parser.addoption('--browser', action='store', default='chromium', help='Browser to use (chromium, firefox, webkit)')
    parser.addoption('--base_url', action='store', default='http://127.0.0.1:8000', help='Base URL of the application')
    parser.addoption('--headless', action='store', default='True', help='Run browser in headless mode')


def load_config(file):
    """
    Loads the configuration file.

    Args:
        file (str): Path to the configuration file.

    Returns:
        dict: The loaded configuration as a dictionary.
    """
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())
