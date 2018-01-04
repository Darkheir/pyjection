from unittest import TestCase
from pyjection.dependency_injector import DependencyInjector


class OuterClass(object):

    def __init__(self, inner_class):
        self.inner_class = inner_class


class InnerClass(object):
    pass


class TestSimple(TestCase):

    def setUp(self):
        self._container = DependencyInjector()
        self._container.register(InnerClass)
        self._container.register(OuterClass)

    def test_get_outer_class(self):
        outer = self._container.get("outer_class")
        self.assertIsInstance(outer, OuterClass)

    def test_get_inner_class(self):
        outer = self._container.get("outer_class")
        self.assertIsInstance(outer.inner_class, InnerClass)

    def test_get_by_class(self):
        outer = self._container.get(OuterClass)
        self.assertIsInstance(outer, OuterClass)

    def test_has_service_true(self):
        result = self._container.has_service("outer_class")
        self.assertTrue(result)

    def test_has_service_false(self):
        result = self._container.has_service("unknown")
        self.assertFalse(result)

    def test_has_service_by_class(self):
        result = self._container.has_service(OuterClass)
        self.assertTrue(result)

    def test_not_singleton(self):
        outer1 = self._container.get("outer_class")
        outer2 = self._container.get("outer_class")
        self.assertIsNot(outer1, outer2)
