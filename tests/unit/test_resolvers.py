from unittest import TestCase
from unittest.mock import Mock, create_autospec
from inspect import signature
from collections import OrderedDict

from pyjection.resolvers import NameResolver, ServiceResolver
from pyjection.dependency_injector import DependencyInjector
from pyjection.service import Service
from pyjection.reference import Reference


def test_method(test_parameter):
    del test_parameter


class TestServiceResolver(TestCase):

    def setUp(self):
        self._injector = create_autospec(DependencyInjector)
        self._service = create_autospec(Service)
        self._resolver = ServiceResolver()
        sig = signature(test_method)
        method_parameters = OrderedDict(sig.parameters)
        _, self._parameter = method_parameters.popitem()


    def test_return_none(self):
        self._service.arguments = dict()
        result = self._resolver.resolve(self._parameter, self._service, self._injector)
        self.assertIsNone(result)

    def test_return_none_reference(self):
        return_value = Mock
        self._service.arguments = dict(test_parameter=return_value)
        result = self._resolver.resolve(self._parameter, self._service, self._injector)
        self.assertEqual(return_value, result)

    def test_return_reference_class(self):
        return_value = create_autospec(Reference)
        return_value.return_class = True
        return_value.name = 'test_parameter'

        self._service.arguments = dict(test_parameter=return_value)
        self._resolver.resolve(self._parameter, self._service, self._injector)
        self._injector.get_uninstantiated.assert_called_with('test_parameter')

    def test_return_reference(self):
        return_value = create_autospec(Reference)
        return_value.return_class = False
        return_value.name = 'test_parameter'

        self._service.arguments = dict(test_parameter=return_value)
        self._resolver.resolve(self._parameter, self._service, self._injector)
        self._injector.get.assert_called_with('test_parameter')


class TestNameResolver(TestCase):

    def setUp(self):
        self._injector = create_autospec(DependencyInjector)
        self._resolver = NameResolver()
        sig = signature(test_method)
        method_parameters = OrderedDict(sig.parameters)
        _, self._parameter = method_parameters.popitem()

    def test_return_none(self):
        self._injector.has_service = Mock(return_value=False)
        result = self._resolver.resolve(self._parameter, None, self._injector)
        self.assertIsNone(result)

    def test_return_has_service_called(self):
        self._injector.has_service = Mock(return_value=False)
        self._resolver.resolve(self._parameter, None, self._injector)
        self._injector.has_service.assert_called_with('test_parameter')

    def test_return_get_called(self):
        self._injector.has_service = Mock(return_value=True)
        self._injector.get = Mock(return_value=Mock)
        self._resolver.resolve(self._parameter, None, self._injector)
        self._injector.get.assert_called_with('test_parameter')

    def test_return_value(self):
        self._injector.has_service = Mock(return_value=True)
        return_value = Mock
        self._injector.get = Mock(return_value=return_value)
        result = self._resolver.resolve(self._parameter, None, self._injector)
        self.assertEqual(result, return_value)
