from playwright.sync_api import Page


class TestCases:
    """
    Handles operations related to test cases within the application using Playwright.

    Attributes:
       page (Page): The Playwright page instance for interacting with web elements.
    """
    def __init__(self, page: Page):
        """
        Initializes the TestCases class.

        Args:
           page (Page): The Playwright page instance for interacting with the application.
        """
        self.page = page

    def check_test_exists(self, test_name: str):
        """
        Checks if a test with the given name exists in the list.

        Args:
           test_name (str): The name of the test to check for.

        Returns:
           bool: True if the test exists, False otherwise.
        """
        return self.page.query_selector(f'css=tr >> text="{test_name}"') is not None

    def delete_test_by_name(self, test_name):
        """
        Deletes a test case by its name.

        Args:
           test_name (str): The name of the test to delete.
        """
        row = self.page.query_selector(f'*css=tr >> text="{test_name}"')
        row.query_selector('.deleteBtn').click()

    def check_columns_hidden(self):
        """
        Checks if specific columns (description, author, executor) are hidden in the table.

        Returns:
           bool: True if all specified columns are hidden, False otherwise.
        """
        description = self.page.is_hidden('.thDes')
        author = self.page.is_hidden('.thAuthor')
        executor = self.page.is_hidden('.thLast')
        return description and author and executor
