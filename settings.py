BROWSER_OPTIONS = {
    'geolocation': {'latitude': 48.8, 'longitude': 2.3},
    'permissions': ['geolocation']
}

"""
BROWSER_OPTIONS:
    A dictionary defining default browser configuration options.

    Fields:
    - geolocation (dict):
        Specifies the geolocation coordinates to be used by the browser.
        - latitude (float): Latitude coordinate (e.g., 48.8).
        - longitude (float): Longitude coordinate (e.g., 2.3).

    - permissions (list):
        A list of permissions to grant to the browser context.
        - 'geolocation': Grants the browser access to geolocation services.

    Usage:
    These options are passed to the browser context when initializing browser sessions in tests.
"""