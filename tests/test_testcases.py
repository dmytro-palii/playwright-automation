from pytest import mark

data = {
    'argnames': 'name, description',
    'argvalues': [('hello', 'world'),
                  ('hello', ''),
                  ('123', 'world')
                  ],
    'ids': ['general test',
            'test with no description',
            'tests with digits in name'
            ]
}


@mark.parametrize(**data)
def test_new_test_cases(desktop_app_auth, name, description):
    """
    Tests the creation, existence, and deletion of new test cases in the desktop application.

    Args:
       desktop_app_auth: An authenticated instance of the desktop app, providing access to its methods.
       name (str): The name of the test case to be created.
       description (str): The description of the test case to be created.

    Steps:
       1. Navigate to the "Create new test" section.
       2. Create a test case with the specified name and description.
       3. Navigate to the "Test Cases" section.
       4. Verify that the test case exists in the list.
       5. Delete the test case by its name.

    Parametrization:
       - "name": The name of the test case (e.g., 'hello', '123').
       - "description": The description of the test case (e.g., 'world', '').

    Asserts:
       - Ensures the created test case is listed in the "Test Cases" section.
    """
    desktop_app_auth.navigate_to('Create new test')
    desktop_app_auth.create_test(name, description)
    desktop_app_auth.navigate_to('Test Cases')
    assert desktop_app_auth.test_cases.check_test_exists(name)
    desktop_app_auth.test_cases.delete_test_by_name(name)


def test_testcases_does_not_exist(desktop_app_auth):
    desktop_app_auth.navigate_to('Test Cases')
    assert not desktop_app_auth.test_cases.check_test_exists('auhfahgh')