import pytest
from serenity.utils import to_camel_case


class TestUtils:
    def test_to_camel_case(self):
        with pytest.raises(Exception):
            to_camel_case('')

        ret = to_camel_case('test_snake_case')
        assert ret == 'testSnakeCase'

        ret = to_camel_case('_test_edgy_snake_case_')
        assert ret == 'testEdgySnakeCase'

        ret = to_camel_case('__test_superedgy___snake_case_')
        assert ret == 'testSuperedgySnakeCase'