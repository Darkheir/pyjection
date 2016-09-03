from unittest import TestCase
from unittest.mock import Mock

from pyjection.helper import convert_camel_to_snake
from pyjection.helper import get_service_subject_identifier


class TestHelper(TestCase):

    def test_convert_camel_to_snake_no_change(self):
        result = convert_camel_to_snake('test_name')
        self.assertEqual(result, 'test_name')

    def test_convert_camel_to_snake(self):
        result = convert_camel_to_snake('CamelCase')
        self.assertEqual(result, 'camel_case')

    def test_get_service_subject_identifier_class(self):
        result = get_service_subject_identifier(Mock)
        self.assertEqual(result, "mock")

    def test_get_service_subject_identifier_instance(self):
        result = get_service_subject_identifier(Mock())
        self.assertEqual(result, "mock")

