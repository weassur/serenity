import requests

DEV_URL = 'https://api-dev.serenityhome.fr/'
PROD_URL = 'https://api-dev.serenityhome.fr/'


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
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = requests.post(
            self.url + '/authenticate/anonymous',
            headers=headers,
            data=payload).json()
        self.security_token = data['token']
        return True
