import requests
from datetime import datetime, timedelta
from serenity.utils import to_camel_case

DEV_URL = 'http://api-dev.serenityhome.fr/'
PROD_URL = 'https://api.serenityhome.fr/'

CONTENT_TYPE = 'application/x-www-form-urlencoded'
TOKEN_VALIDITY = timedelta(hours=3)


class Serenity:
    def __init__(self, anonymous_token, production=False, *args, **kwargs):
        self.anonymous_token = anonymous_token
        self.url = DEV_URL
        if production:
            self.url = PROD_URL

    def _get_headers(self):
        return {
            'Content-Type': CONTENT_TYPE,
            'Authorization': 'Bearer {token}'.format(token=self.security_token)
        }

    def authenticate(self):
        if not self.anonymous_token:
            raise AttributeError
        headers = {
            'Content-Type': CONTENT_TYPE,
            'Authorization':
            'Bearer {token}'.format(token=self.anonymous_token)
        }
        data = requests.post(
            self.url + '/authenticate/anonymous', headers=headers).json()
        if not data['success']:
            raise Exception(data.get('message'))
        self.security_token = data['token']
        self.authentication_ts = datetime.now()
        return True

    def _check_authentication(self):
        if not self.security_token or not self.authentication_ts:
            raise AttributeError
        if datetime.now() > self.authentication_ts + TOKEN_VALIDITY:
            self.authenticate()
        return True

    def list_activities(self, page=1, limit=50, full=False):
        self._check_authentication()
        url = self.url + '/v1/public/activityGroup/list'
        params = {
            'page': page,
            'limit': limit,
            'full': 1 if full else 0,
        }
        data = requests.get(
            url, headers=self._get_headers(), params=params).json()
        if not data['success']:
            raise Exception(data.get('message'))
        response = data['data']
        # consistent naming
        activities = response['activityGroups']
        response['activities'] = activities
        del response['activityGroups']
        response['has_next'] = page < response['total_page']
        return response

    def list_cities(self, page=1, limit=50, full=False):
        self._check_authentication()
        url = self.url + '/v1/public/city/list'
        params = {
            'page': page,
            'limit': limit,
            'full': 1 if full else 0,
        }
        data = requests.get(
            url, headers=self._get_headers(), params=params).json()
        if not data['success']:
            raise Exception(data.get('message'))
        response = data['data']
        response['has_next'] = page < response['total_page']
        return response

    def search_cities(self, keyword, limit=50, full=False):
        self._check_authentication()
        url = self.url + '/v1/public/city/getFromRegex'
        params = {
            'keyword': keyword,
            'limit': limit,
            'full': 1 if full else 0,
        }
        data = requests.get(
            url, headers=self._get_headers(), params=params).json()
        if not data['success']:
            raise Exception(data.get('message'))
        response = data['data']
        return response

    def create_token(self, **kwargs):
        self._check_authentication()
        url = self.url + '/v1/public/funnel/insurer/project/update/token'
        params = {to_camel_case(key): value for key, value in kwargs.items()}
        data = requests.post(
            url, headers=self._get_headers(), params=params).json()
        if not data['success']:
            raise Exception(data.get('message'))
        token = data['data']['token']
        return token

    def create_project(self, token):
        if not token:
            raise Exception(
                'token is required, you need to create a token first with create_token'
            )
        self._check_authentication()
        url = self.url + '/v1/public/funnel/insurer/project/save'
        params = {
            'dataToken': token,
        }
        data = requests.post(
            url, headers=self._get_headers(), params=params).json()
        if not data['success']:
            raise Exception(data.get('message'))
        response = data['data']
        return response
