import json
import logging
import os
from pytest import fixture, hookimpl
from playwright.sync_api import sync_playwright
from pytest_base_url.plugin import base_url
from helpers.web_servises import WebService
from page_object.application import App
import settings
import pytest
from helpers.db import DataBase
import allure


@fixture(autouse=True, scope='session')
def preconditions(request):
    logging.info('preconditions started')
    # base_url = request.config.getoption('--base-url')
    base_url = request.config.getoption('--base-url') or settings.BASE_URL
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    yield
    logging.info('postconditions started')
    web = WebService(base_url)
    web.login(**config['users']['userRole3'])
    for test in request.node.items:
        if len(test.own_markers) > 0:
            if test.own_markers[0].name == 'test_id':
                if test.result_call.passed:
                    web.report_test(test.own_markers[0].args[0], 'PASS')
                if test.result_call.failed:
                    web.report_test(test.own_markers[0].args[0], 'FAIL')


@fixture(scope='function')
def get_webservice(request):
    base_url = request.config.getoption('--base-url') or "http://127.0.0.1:8000"
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    web = WebService(base_url)
    web.login(**config['users']['userRole1'])
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
    desktop_app.login(**config['users']['userRole1'])
    yield desktop_app


@fixture(scope='session')
def desktop_app_bob(get_browser, request):
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    app = App(get_browser, settings.BASE_URL, **settings.BROWSER_OPTIONS)
    app.goto('/login')
    app.login(**config['users']['userRole2'])
    yield app
    app.close()


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
    mobile_app.login(**config['users']['userRole1'])
    yield mobile_app


@hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    setattr(item, f'result_{result.when}', result)


@fixture(scope='function', autouse=True)
def make_screenshots(request):
    yield
    if request.node.result_call.failed:
        for arg in request.node.funcargs.values():
            if isinstance(arg, App):
                allure.attach(body=arg.page.screenshot(),
                              name='screenshot',
                              attachment_type=allure.attachment_type.PNG)


def pytest_addoption(parser):
    parser.addoption('--secure', action='store', default='secure.json')
    parser.addini('db_path', help='path to sqlite db file', default='D:\\AutotestLearn\\Playwright\\CommonProject\\TestMe-TCM\\db.sqlite3')
    parser.addini('headless', help='run browser in headless mode', default='True')


def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cf:
        return json.loads(cf.read())
