import requests
from datetime import datetime, timedelta

DEV_URL = 'http://api-dev.serenityhome.fr/'
PROD_URL = 'https://api-dev.serenityhome.fr/'

CONTENT_TYPE = 'application/x-www-form-urlencoded'
TOKEN_VALIDITY = timedelta(hours=3)


class Serenity:
    def __init__(self, anonymous_token, production=False, *args, **kwargs):
        self.anonymous_token = anonymous_token
        self.url = DEV_URL
        if production:
            self.url = PROD_URL

    def authenticate(self):
        if not self.anonymous_token:
            raise AttributeError
        payload = {
            'anonymousToken': self.anonymous_token,
        }
        headers = {'Content-Type': CONTENT_TYPE}
        data = requests.post(
            self.url + '/authenticate/anonymous',
            headers=headers,
            data=payload).json()
        if not data['success']:
            raise Exception
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
        payload = {
            'securityToken': self.security_token,
        }
        headers = {'Content-Type': CONTENT_TYPE}
        url = self.url + '/v1/public/activityGroup/list/{page}/{limit}/{full}'.format(
            page=page,
            limit=limit,
            full=1 if full else 0,
        )
        data = requests.get(url, headers=headers, data=payload).json()
        if not data['success']:
            raise Exception
        response = data['data']
        # consistent naming
        activities = response['activityGroups']
        response['activities'] = activities
        del response['activityGroups']
        response['has_next'] = page < response['total_page']
        return response

    def list_cities(self, page=1, limit=50, full=False):
        self._check_authentication()
        payload = {
            'securityToken': self.security_token,
        }
        headers = {'Content-Type': CONTENT_TYPE}
        url = self.url + '/v1/public/city/list/{page}/{limit}/{full}'.format(
            page=page,
            limit=limit,
            full=1 if full else 0,
        )
        data = requests.get(url, headers=headers, data=payload).json()
        if not data['success']:
            raise Exception
        response = data['data']
        response['has_next'] = page < response['total_page']
        return response

    def search_cities(self, keyword, limit=50, full=False):
        self._check_authentication()
        payload = {
            'securityToken': self.security_token,
        }
        headers = {'Content-Type': CONTENT_TYPE}
        url = self.url + '/v1/public/city/getFromRegex/{keyword}/{full}/{limit}'.format(
            keyword=keyword,
            full=1 if full else 0,
            limit=limit,
        )
        data = requests.get(url, headers=headers, data=payload).json()
        if not data['success']:
            raise Exception
        response = data['data']
        return response
