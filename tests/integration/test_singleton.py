from unittest import TestCase
from pyjection.dependency_injector import DependencyInjector


class OuterClass(object):
    pass


class TestSingleton(TestCase):

    def setUp(self):
        self._container = DependencyInjector()
        self._container.register_singleton(OuterClass)

    def test_get_outer_class(self):
        outer = self._container.get("outer_class")
        self.assertIsInstance(outer, OuterClass)

    def test_is_singleton(self):
        outer1 = self._container.get("outer_class")
        outer2 = self._container.get("outer_class")
        self.assertIs(outer1, outer2)
