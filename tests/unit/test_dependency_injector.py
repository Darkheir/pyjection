from unittest import TestCase
from unittest.mock import Mock

from pyjection.dependency_injector import DependencyInjector
from pyjection.service import Service


class TestDependencyInjector(TestCase):

    def setUp(self):
        self.injector = DependencyInjector()

    def test_register(self):
        result = self.injector.register(Mock, 'identifier')
        self.assertIsInstance(result, Service)

    def test_register_without_identifier(self):
        result = self.injector.register(Mock)
        self.assertIsInstance(result, Service)

    def test_register_singleton_returns_service(self):
        result = self.injector.register_singleton(Mock, 'identifier')
        self.assertIsInstance(result, Service)

    def test_register_singleton(self):
        result = self.injector.register_singleton(Mock, 'identifier')
        self.assertTrue(result.is_singleton)

    def test_register_singleton_without_identifier(self):
        result = self.injector.register_singleton(Mock)
        self.assertTrue(result.is_singleton)

    def test_has_service_returns_false(self):
        success = self.injector.has_service('no_service')
        self.assertFalse(success)

    def test_has_service_returns_true(self):
        self.injector._services['fake_service'] = None
        success = self.injector.has_service('fake_service')
        self.assertTrue(success)

    def test_has_service_with_class(self):
        self.injector._services['mock'] = None
        success = self.injector.has_service(Mock)
        self.assertTrue(success)

    def test_get_error(self):
        with self.assertRaises(Exception):
            self.injector.get('no_service')

    def test_get_singleton_class(self):
        self._register_singleton()
        subject1 = self.injector.get('fake_service')
        self.assertIsInstance(subject1, Mock)

    def test_get_singleton_same_instance(self):
        self._register_singleton()
        subject1 = self.injector.get('fake_service')
        subject2 = self.injector.get('fake_service')
        self.assertEqual(subject1, subject2)

    def _register_singleton(self):
        fake_service = Service(Mock)
        fake_service.is_singleton = True
        self.injector._services['fake_service'] = fake_service

    def test_get_class(self):
        fake_service = Service(Mock)
        self.injector._services['fake_service'] = fake_service
        subject1 = self.injector.get('fake_service')
        self.assertIsInstance(subject1, Mock)

    def test_get_class_identifier(self):
        fake_service = Service(Mock)
        self.injector._services['mock'] = fake_service
        subject1 = self.injector.get(Mock)
        self.assertIsInstance(subject1, Mock)

    def test_get_instance(self):
        subject = Mock()
        fake_service = Service(subject)
        self.injector._services['fake_service'] = fake_service
        result = self.injector.get('fake_service')
        self.assertEqual(subject, result)
