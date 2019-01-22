import pytest
from serenity.serenity import Serenity, DEV_URL, PROD_URL, CONTENT_TYPE
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
                headers={'Content-Type': CONTENT_TYPE},
                data={
                    'anonymousToken': test_token,
                })
        assert ret
        assert instance.security_token == 'FAKE SECURITY TOKEN'

        instance.anonymous_token = None
        with pytest.raises(AttributeError):
            instance.authenticate()

    def test_list_activities(self):
        test_token = 'test'
        security_token = 'SECURITY TOKEN'
        instance = Serenity(test_token)
        with pytest.raises(Exception):
            instance.list_activities()

        instance.security_token = security_token
        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = {'success': False}
            with pytest.raises(Exception):
                instance.list_activities()

        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            # yapf: disable
            mock_get.return_value.json.return_value = {
                'success': True,
                'message': 'List of activities',
                'data': {
                    'activityGroups': [{
                        '_id': '5c05162c87e1930064f65d61',
                        'name': 'Construction - Extension'
                    },
                    {
                        '_id': '5c05162d87e1930064f65d7d',
                        'name': 'Devis divers'
                    }],
                    'page': 1,
                    'total_count': 34,
                    'total_page': 2
                }
            }
            # yapf: enable
            ret = instance.list_activities()
            mock_get.assert_called_once_with(
                DEV_URL + '/v1/public/activityGroup/list/1/50/0',
                headers={'Content-Type': CONTENT_TYPE},
                data={
                    'securityToken': security_token,
                })
        assert ret == [{
            '_id': '5c05162c87e1930064f65d61',
            'name': 'Construction - Extension'
        }, {
            '_id': '5c05162d87e1930064f65d7d',
            'name': 'Devis divers'
        }]

        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = {
                'success': True,
                'data': {
                    'activityGroups': []
                }
            }
            instance.list_activities(page=3, limit=10, full=True)
            mock_get.assert_called_once_with(
                DEV_URL + '/v1/public/activityGroup/list/3/10/1',
                headers={'Content-Type': CONTENT_TYPE},
                data={
                    'securityToken': security_token,
                })