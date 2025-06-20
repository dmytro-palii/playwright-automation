import requests
import re


class WebService:
    def __init__(self, base_url: str):
        self.session = requests.session()
        self.base_url = base_url


    def _get_token(self, url: str):
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        rsp = self.session.get(full_url)
        match = re.search('<input type="hidden" name="csrfmiddlewaretoken" value="(.+?)">', rsp.text)
        if match:
            return match.group(1)
        else:
            assert False, 'csrftoken not found'


    def login(self, login: str, password: str):
        token = self._get_token('/login/')
        data = {
            'csrfmiddlewaretoken': token,
            'username': login,
            'password': password
        }
        self.session.post(self.base_url + '/login/', data=data)
        csrftoken = self.session.cookies.get('csrftoken')
        self.session.headers.update({'X-CSRFToken': csrftoken})


    def create_test(self, test_name: str, test_description: str):
        token = self._get_token('/test/new')
        data = {
            'csrfmiddlewaretoken': token,
            'name': test_name,
            'description': test_description
        }
        self.session.post(self.base_url + '/test/new', data=data)


    def report_test(self, test_id: int, status: str):
        self.session.post(self.base_url + f'/test/{test_id}/status', json={'status': status})


    def close(self):
        self.session.close()