from pytest import mark


@mark.test_id(217)
def test_columns_hidden(mobile_app_auth):
    mobile_app_auth.click_menu_button()
    mobile_app_auth.navigation_to('Test Cases')
    assert mobile_app_auth.test_cases.check_columns_hidden()
