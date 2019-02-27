import pytest
from datetime import datetime, timedelta
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
                headers={
                    'Content-Type': CONTENT_TYPE,
                    'Authorization': 'Bearer {token}'.format(token=test_token)
                },
            )
        assert ret
        assert instance.security_token == 'FAKE SECURITY TOKEN'
        assert instance.authentication_ts is not None
        assert instance._check_authentication()

        instance.anonymous_token = None
        with pytest.raises(AttributeError):
            instance.authenticate()

    def test_check_authentication(self):
        test_token = 'test'
        instance = Serenity(test_token)
        with pytest.raises(AttributeError):
            instance._check_authentication()

        with patch.object(Serenity, 'authenticate') as mock_authenticate:
            mock_authenticate.return_value = True
            instance.security_token = 'FAKE SECURITY TOKEN'
            instance.authentication_ts = datetime.now() - timedelta(hours=4)
            assert instance._check_authentication()
            mock_authenticate.assert_called_once()

    def test_list_activities(self):
        test_token = 'test'
        security_token = 'SECURITY TOKEN'
        instance = Serenity(test_token)
        with pytest.raises(Exception):
            instance.list_activities()

        instance.security_token = security_token
        instance.authentication_ts = datetime.now()
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
                DEV_URL + '/v1/public/activityGroup/list',
                headers={
                    'Content-Type': CONTENT_TYPE,
                    'Authorization': 'Bearer {token}'.format(token=test_token)
                },
                params={
                    'page': 1,
                    'limit': 50,
                    'full': 0,
                })
        # yapf: disable
        assert ret == {
            'page': 1,
            'total_count': 34,
            'total_page': 2,
            'has_next': True,
            'activities': [{
                '_id': '5c05162c87e1930064f65d61',
                'name': 'Construction - Extension'
            }, {
                '_id': '5c05162d87e1930064f65d7d',
                'name': 'Devis divers'
            }]
        }
        # yapf: enable

        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = {
                'success': True,
                'data': {
                    'activityGroups': [],
                    'page': 1,
                    'total_count': 34,
                    'total_page': 2
                }
            }
            instance.list_activities(page=3, limit=10, full=True)
            mock_get.assert_called_once_with(
                DEV_URL + '/v1/public/activityGroup/list',
                headers={
                    'Content-Type': CONTENT_TYPE,
                    'Authorization': 'Bearer {token}'.format(token=test_token)
                },
                params={
                    'page': 3,
                    'limit': 10,
                    'full': 1,
                })

    def test_list_cities(self):
        test_token = 'test'
        security_token = 'SECURITY TOKEN'
        instance = Serenity(test_token)
        with pytest.raises(Exception):
            instance.list_cities()

        instance.security_token = security_token
        instance.authentication_ts = datetime.now()
        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = {'success': False}
            with pytest.raises(Exception):
                instance.list_cities()

        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            # yapf: disable
            mock_get.return_value.json.return_value = {
                'success': True,
                'message': 'List of activities',
                'data': {
                    'cities': [{
                        '_id': '5c05156e8c27c400597066ea',
                        'name': 'Ozan'
                    },
                    {
                        '_id': '5c05156e8c27c4005970670a',
                        'name': 'Marchamp'
                    }],
                    'page': 1,
                    'total_count': 36691,
                    'total_page': 1224
                }
            }
            # yapf: enable
            ret = instance.list_cities()
            mock_get.assert_called_once_with(
                DEV_URL + '/v1/public/city/list',
                headers={
                    'Content-Type': CONTENT_TYPE,
                    'Authorization': 'Bearer {token}'.format(token=test_token)
                },
                params={
                    'page': 1,
                    'limit': 50,
                    'full': 0,
                })
        # yapf: disable
        assert ret == {
            'page': 1,
            'total_count': 36691,
            'total_page': 1224,
            'has_next': True,
            'cities': [{
                '_id': '5c05156e8c27c400597066ea',
                'name': 'Ozan'
            },
            {
                '_id': '5c05156e8c27c4005970670a',
                'name': 'Marchamp'
            }]
        }
        # yapf: enable

        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = {
                'success': True,
                'data': {
                    'cities': [],
                    'page': 1,
                    'total_count': 36691,
                    'total_page': 1224
                }
            }
            instance.list_cities(page=3, limit=10, full=True)
            mock_get.assert_called_once_with(
                DEV_URL + '/v1/public/city/list',
                headers={
                    'Content-Type': CONTENT_TYPE,
                    'Authorization': 'Bearer {token}'.format(token=test_token)
                },
                params={
                    'page': 3,
                    'limit': 10,
                    'full': 1,
                })

    def test_search_cities(self):
        test_token = 'test'
        security_token = 'SECURITY TOKEN'
        instance = Serenity(test_token)
        with pytest.raises(Exception):
            instance.search_cities('')

        instance.security_token = security_token
        instance.authentication_ts = datetime.now()
        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = {'success': False}
            with pytest.raises(Exception):
                instance.search_cities()  #pylint: disable=E1120

        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            # yapf: disable
            mock_get.return_value.json.return_value = {
                'success': True,
                'message': 'List of activities',
                'data': {
                    'cities': [{
                        '_id': '5c0515838c27c400597074c0',
                        'name': 'Aix-en-Othe'
                    },
                    {
                        '_id': '5c0516148c27c4005970ee6d',
                        'name': 'Aixe-sur-Vienne'
                    }],
                    'total_count': 12,
                    'total_page': 1
                }
            }
            # yapf: enable
            ret = instance.search_cities('aix')
            mock_get.assert_called_once_with(
                DEV_URL + '/v1/public/city/getFromRegex',
                headers={
                    'Content-Type': CONTENT_TYPE,
                    'Authorization': 'Bearer {token}'.format(token=test_token)
                },
                params={
                    'keyword': 'aix',
                    'full': 0,
                    'limit': 50,
                })
        # yapf: disable
        assert ret == {
            'total_count': 12,
            'total_page': 1,
            'cities': [{
                '_id': '5c0515838c27c400597074c0',
                'name': 'Aix-en-Othe'
            },
            {
                '_id': '5c0516148c27c4005970ee6d',
                'name': 'Aixe-sur-Vienne'
            }]
        }
        # yapf: enable

        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = {
                'success': True,
                'data': {
                    'cities': [],
                    'total_count': 12,
                    'total_page': 1
                }
            }
            instance.search_cities('paris', limit=10, full=True)
            mock_get.assert_called_once_with(
                DEV_URL + '/v1/public/city/getFromRegex',
                headers={
                    'Content-Type': CONTENT_TYPE,
                    'Authorization': 'Bearer {token}'.format(token=test_token)
                },
                params={
                    'keyword': 'paris',
                    'full': 1,
                    'limit': 10,
                })
