import pytest


ddt = {
    'argnames': 'name,description',
    'argvalues': [
        ('hello', 'world'),
        ('hello', ''),
        ('123', 'word')],
    'ids': [
        'general test',
        'empty description',
        'digits name']
}


@ pytest.mark.parametrize(**ddt)
def test_new_testcase(desktop_app_auth, name, description, get_db):
    tests = get_db.list_test_cases()
    desktop_app_auth.navigation_to('Create new test')
    desktop_app_auth.create_test(name, description)
    desktop_app_auth.navigation_to('Test Cases')
    assert desktop_app_auth.test_cases.check_test_exists(name)
    assert len(tests) + 1 == len(get_db.list_test_cases())
    get_db.delete_test_cases(name)


def test_cases_does_not_exist(desktop_app_auth):
    desktop_app_auth.navigation_to('Test Cases')
    assert not desktop_app_auth.test_cases.check_test_exists('namename')


def test_delete_test_case(desktop_app_auth, get_webservice):
    test_name = 'test for delete'
    get_webservice.create_test(test_name, 'delete me please')
    desktop_app_auth.navigation_to('Test Cases')
    assert desktop_app_auth.test_cases.check_test_exists(test_name)

    desktop_app_auth.test_cases.delete_test_by_name(test_name)
    desktop_app_auth.navigation_to('Test Cases')
    assert not desktop_app_auth.test_cases.check_test_exists(test_name)



