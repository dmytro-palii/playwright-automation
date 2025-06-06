import allure


@allure.title('test wait more 30 sec')
def test_wait_more_30sec(desktop_app_auth):
    desktop_app_auth.navigation_to('Demo pages')
    desktop_app_auth.demo_pages.open_page_after_wait(3)
    assert desktop_app_auth.demo_pages.check_wait_page()


def test_wait_ajax(desktop_app_auth):
    desktop_app_auth.navigation_to('Demo pages')
    desktop_app_auth.demo_pages.open_page_and_wait_ajax(2)
    assert desktop_app_auth.demo_pages.get_ajax_responses_count() == 6


def test_handlers(desktop_app_auth):
    desktop_app_auth.navigation_to('Demo pages')
    desktop_app_auth.demo_pages.click_new_page_button()
    desktop_app_auth.demo_pages.inject_js()
    desktop_app_auth.navigation_to('Test Cases')
    assert desktop_app_auth.test_cases.check_test_exists('Check new test')
