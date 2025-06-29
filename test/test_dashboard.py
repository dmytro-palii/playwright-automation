import json
from pytest import mark


@mark.test_id(214)
def test_dashboard_data(desktop_app_auth):
    payload = json.dumps({"total": 0, "passed": 0, "failed": 0, "norun": 0})
    desktop_app_auth.intercept_request('**/getstat/', payload)
    desktop_app_auth.refresh_dashboard()
    print('get_total_tests_stats', desktop_app_auth.get_total_tests_stats())
    desktop_app_auth.stop_intercept('**/getstat*')
    assert desktop_app_auth.get_total_tests_stats() == '0'


@mark.test_id(215)
def test_multiple_roles(desktop_app_auth, desktop_app_bob, get_db):
    alice = desktop_app_auth
    bob = desktop_app_bob

    alice.refresh_dashboard()
    alice.navigation_to('Dashboard')
    before = alice.get_total_tests_stats()

    bob.navigation_to('Create new test')
    bob.create_test('test by bob', 'bob')
    bob.navigation_to('Test Cases')
    assert bob.test_cases.check_test_exists('test by bob')

    alice.refresh_dashboard()
    alice.navigation_to('Dashboard')
    after = alice.get_total_tests_stats()

    get_db.delete_test_cases('test by bob')
    assert int(before) + 1 == int(after)