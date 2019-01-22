import pytest
from serenity.serenity import Serenity, DEV_URL, PROD_URL
from unittest.mock import Mock, patch


class TestSerenity:
    def test_constructor(self):
        test_token = 'test'
        instance = Serenity(anonymous_token=test_token)
        assert instance.anonymous_token == test_token
        assert instance.url == DEV_URL

        instance = Serenity(anonymous_token=test_token, production=True)
        assert instance.anonymous_token == test_token
        assert instance.url == PROD_URL

        with pytest.raises(TypeError):
            instance = Serenity()  #pylint: disable=E1120

        with pytest.raises(TypeError):
            instance = Serenity(foo='bar')  #pylint: disable=E1120

    def test_authenticate(self):
        test_token = 'test'
        instance = Serenity(test_token)
        with patch('requests.post') as mock_post:
            mock_post.return_value = Mock(ok=True)
            mock_post.return_value.json.return_value = {
                'success': True,
                'message': 'Authentication suceeded!',
                'token': 'FAKE SECURITY TOKEN'
            }

            ret = instance.authenticate()
            mock_post.assert_called_once_with(
                DEV_URL + '/authenticate/anonymous',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                data={
                    'anonymousToken': test_token,
                })
        assert ret
        assert instance.security_token == 'FAKE SECURITY TOKEN'

        instance.anonymous_token = None
        with pytest.raises(AttributeError):
            instance.authenticate()
