import requests

DEV_URL = 'https://api-dev.serenityhome.fr/'
PROD_URL = 'https://api-dev.serenityhome.fr/'

CONTENT_TYPE = 'application/x-www-form-urlencoded'


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
        return True

    def list_activities(self, page=1, limit=50, full=False):
        if not self.security_token:
            raise AttributeError
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
        return data['data']['activityGroups']
