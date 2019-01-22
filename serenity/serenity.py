class Serenity:
    def __init__(self, anonymous_token, *args, **kwargs):
        self.anonymous_token = anonymous_token

    def authenticate(self):
        if self.anonymous_token:
            return True
        return False
