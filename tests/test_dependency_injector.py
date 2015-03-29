import unittest
from pyjection.dependency_injector import DependencyInjector
from pyjection.service import Service
from pyjection.reference import Reference
from inspect import Parameter


class MockSubject(object):
    
    def __init__(self):
        pass

class MockSubject2(object):
    
    def __init__(self, value):
        pass

class TestDependencyInjector(unittest.TestCase):

    def setUp(self):
        self.injector = DependencyInjector()

    def test_register(self):
        result = self.injector.register('identifier', MockSubject)
        self.assertIsInstance(result, Service)
        self.assertFalse(result.is_singleton)

    def test_register_singleton(self):
        result = self.injector.register_singleton('identifier', MockSubject)
        self.assertIsInstance(result, Service)
        self.assertTrue(result.is_singleton)

    def test_has_service(self):
        success = self.injector.has_service('no_service')
        self.assertFalse(success)
        self.injector._services['fake_service'] = None
        success = self.injector.has_service('fake_service')
        self.assertTrue(success)

    def test_get(self):
        self.assertRaises(Exception, self.injector.get, identifier='no_service')

        fake_service = Service(MockSubject)
        fake_service.is_singleton = True
        self.injector._services['fake_service'] = fake_service
        subject1 = self.injector.get('fake_service')
        self.assertIsInstance(subject1, MockSubject)

        #Perform a second get to test code where the singleton is cached
        subject2 = self.injector.get('fake_service')
        self.assertIsInstance(subject1, MockSubject)
        self.assertEqual(subject1, subject2)

    def test_get_instance(self):
        #Test with a class
        fake_service = Service(MockSubject)
        self.injector._services['fake_service'] = fake_service
        subject1 = self.injector.get('fake_service')
        self.assertIsInstance(subject1, MockSubject)

        # Test with an instance
        subject1 = MockSubject()
        fake_service = Service(subject1)
        self.injector._services['fake_service'] = fake_service
        subject2 = self.injector.get('fake_service')
        self.assertIsInstance(subject2, MockSubject)
        self.assertEqual(subject1, subject2)

    def test_generate_arguments_dict(self):
        fake_service = Service(MockSubject)
        result = self.injector._generate_arguments_dict(fake_service)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)

        fake_service = Service(MockSubject2)
        fake_service._arguments['value'] = 'Test'
        result = self.injector._generate_arguments_dict(fake_service)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 1)

    def test_get_argument(self):
        fake_service = Service(MockSubject2)

        parameter = Parameter('value', Parameter.POSITIONAL_OR_KEYWORD)

        self.assertRaises(
            Exception,
            self.injector._get_argument,
            service=fake_service,
            method_parameter=parameter
        )

        fake_service._arguments['value'] = 'Test'
        result = self.injector._get_argument(fake_service, parameter)
        self.assertEqual(result, "Test")

        parameter = Parameter('value', Parameter.POSITIONAL_OR_KEYWORD, default='test')
        fake_service = Service(MockSubject2)
        result = self.injector._get_argument(fake_service, parameter)
        self.assertIsNone(result)

        fake_service._arguments['value'] = Reference('my_reference')
        self.injector._services['my_reference'] = Service('test_reference')
        result = self.injector._get_argument(fake_service, parameter)
        self.assertEqual(result, "test_reference")
        

