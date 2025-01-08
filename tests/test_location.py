def test_location_ok(mobile_app_auth):
    """
    Validates that the location returned by the mobile application matches the expected coordinates.

    Args:
        mobile_app_auth: An authenticated instance of the mobile app, providing access to the application's methods.

    Asserts:
        The location retrieved matches the expected coordinates ('48.8:2.3').
    """
    location = mobile_app_auth.get_location()
    assert '48.8:2.3' == location
