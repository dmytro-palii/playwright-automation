import json


def test_dashboard_data(desktop_app_auth):
    payload = json.dumps({"total": 0, "passed": 0, "failed": 0, "norun": 0})
    desktop_app_auth.intercept_request('**/getstat/', payload)
    desktop_app_auth.refresh_dashboard()
    print('get_total_tests_stats', desktop_app_auth.get_total_tests_stats())
    assert desktop_app_auth.get_total_tests_stats() == '0'
    desktop_app_auth.stop_intercept('**/getstat*')


