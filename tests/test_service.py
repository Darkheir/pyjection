from unittest import TestCase
from unittest.mock import Mock
from pyjection.service import Service


class TestService(TestCase):

    def test_type_instance(self):
        service = Service(Mock())
        self.assertEqual(service.type, 'instance')

    def test_type_class(self):
        service = Service(Mock)
        self.assertEqual(service.type, 'class')

    def test_is_not_singleton(self):
        service = Service(Mock())
        self.assertFalse(service.is_singleton)

    def test_is_singleton(self):
        service = Service(Mock())
        service.is_singleton = True
        self.assertTrue(service.is_singleton)

    def test_subject_class(self):
        service = Service(Mock)
        self.assertEqual(service.subject, Mock)

    def test_subject_instance(self):
        subject = Mock()
        service = Service(subject)
        self.assertEqual(service.subject, subject)

    def test_add_argument(self):
        service = Service(Mock)
        service.add_argument('key', 'value')
        self.assertDictEqual(service.arguments, {'key': 'value'})

    def test_add_argument_returns_service(self):
        service = Service(Mock)
        result = service.add_argument('key', 'value')
        self.assertEqual(service, result)

    def test_add_arguments(self):
        service = Service(Mock)
        service.add_arguments(key1='value', key2='other_value')
        self.assertDictEqual(service._arguments, {'key1': 'value', 'key2': 'other_value'})

    def test_add_arguments_returns_service(self):
        service = Service(Mock)
        result = service.add_arguments(key1='value', key2='other_value')
        self.assertEqual(service, result)
