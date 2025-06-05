import json
import logging
import os
from pytest import fixture
from playwright.sync_api import sync_playwright
from pytest_base_url.plugin import base_url
from helpers.web_servises import WebService
from page_object.application import App
import settings
import pytest
from helpers.db import DataBase


@fixture(autouse=True, scope='session')
def preconditions():
    logging.info('preconditions started')
    yield
    logging.info('postconditions started')


@fixture(scope='function')
def get_webservice(request):
    base_url = request.config.getoption('--base-url') or "http://127.0.0.1:8000"
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    web = WebService(base_url)
    web.login(**config)
    yield web
    web.close()


@fixture(scope='session')
def get_db(request):
    path = request.config.getini("db_path")
    db = DataBase(path)
    yield db
    db.close()


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session', params=['chromium',
                                  # 'firefox', 'webkit'
                                  ],
         ids=['chromium',
              # 'firefox', 'webkit'
              ]
         )
def get_browser(get_playwright, request):
    browser = request.param
    os.environ['PWBROWSER'] = browser
    headless = request.config.getini('headless')
    if headless == 'True':
        headless = True
    else:
        headless = False

    if browser == 'chromium':
        brow = get_playwright.chromium.launch(headless=headless)
    elif browser == 'firefox':
        brow = get_playwright.firefox.launch(headless=headless)
    elif browser == 'webkit':
        brow = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, 'unsupported brows type'

    yield brow
    brow.close()
    del os.environ['PWBROWSER']


@fixture(scope='session')
def desktop_app(get_browser, request):
    app = App(get_browser, settings.BASE_URL, **settings.BROWSER_OPTIONS)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def desktop_app_auth(desktop_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    desktop_app.goto('/login')
    desktop_app.login(**config)
    yield desktop_app


@fixture(scope='session', params=['iPhone 11', 'Pixel 2'])
def mobile_app(get_playwright, get_browser, request):
    if os.environ.get('PWBROWSER') == 'firefox':
        pytest.skip()
    # device = request.config.getoption('--device')
    device = request.param
    device_config = get_playwright.devices.get(device)
    if device_config is not None:
        device_config.update(**settings.BROWSER_OPTIONS)
    else:
        device_config = settings.BROWSER_OPTIONS.copy()
    app = App(get_browser, settings.BASE_URL, **device_config)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def mobile_app_auth(mobile_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    mobile_app.goto('/login')
    mobile_app.login(**config)
    yield mobile_app


def pytest_addoption(parser):
    parser.addoption('--secure', action='store', default='secure.json')
    parser.addoption('--my-browser', action='store', default='chromium')
    parser.addoption('--advice', action='store', default='')
    parser.addini('db_path', help='path to sqlite db file', default='D:\\AutotestLearn\\Playwright\\CommonProject\\TestMe-TCM\\db.sqlite3')
    parser.addini('headless', help='run browser in headless mode', default='True')


def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cf:
        return json.loads(cf.read())
