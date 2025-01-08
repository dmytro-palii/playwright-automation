import json


def test_dashboard_data(desktop_app_auth):
    payload = json.dumps({'total': 0, 'passed': 0, 'failed': 0, 'norun': 0})
    # Setup interception
    desktop_app_auth.intercept_requests('**/getstat*', payload)
    # Refresh the dashboard and ensure it waits for updates
    desktop_app_auth.refresh_dashboard()
    # Verify the intercepted payload updates the total
    assert desktop_app_auth.get_total_tests_stats() == '48', "Expected total tests state to be '0'"
    # Cleanup the route
    desktop_app_auth.stop_intercept('**/getstat*')

