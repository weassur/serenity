import pytest
from serenity.serenity import Serenity


class TestSerenity:
    def test_constructor(self):
        test_token = 'test'
        instance = Serenity(test_token)
        assert instance.anonymous_token == test_token

        with pytest.raises(TypeError):
            instance = Serenity()  #pylint: disable=E1120

        with pytest.raises(TypeError):
            instance = Serenity(foo='bar')  #pylint: disable=E1120

    def test_authenticate(self):
        test_token = 'test'
        instance = Serenity(test_token)
        assert instance.authenticate()
