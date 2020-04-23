from unittest import TestCase
from pyjection.dependency_injector import DependencyInjector
from pyjection.errors import ServiceNotFoundError, ArgumentNotFoundError


class OuterClass(object):

    def __init__(self, inner_class):
        self.inner_class = inner_class


class TestError(TestCase):

    def setUp(self):
        self._container = DependencyInjector()
        self._container.register(OuterClass)

    def test_unknown_parameter(self):
        with self.assertRaises(ArgumentNotFoundError):
            self._container.get("outer_class")

    def test_unknown_service(self):
        with self.assertRaises(ServiceNotFoundError):
            self._container.get("unknown_service")
