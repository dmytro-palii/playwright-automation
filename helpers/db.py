import sqlite3
from site import execsitecustomize


class DataBase:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)


    def list_test_cases(self):
        c = self.connection.cursor()
        c.execute('SELECT * FROM tcm_testcase')
        return c.fetchall()


    def delete_test_cases(self, test_name: str):
        c = self.connection.cursor()
        c.execute('DELETE FROM tcm_testcase WHERE name=?', (test_name,))
        self.connection.commit()


    def close(self):
        self.connection.close()
