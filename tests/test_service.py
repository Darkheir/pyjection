import unittest
from pyjection.service import Service


class MockSubject(object):
    pass

class TestService(unittest.TestCase):

    def test_type(self):
        subject = MockSubject()
        service = Service(subject)
        self.assertEqual(service.type, 'instance')

        service = Service(MockSubject)
        self.assertEqual(service.type, 'class')

    def test_is_singleton(self):
        service = Service(MockSubject)
        self.assertFalse(service.is_singleton)

        service.is_singleton = True
        self.assertTrue(service.is_singleton)

    def test_subject(self):
        service = Service(MockSubject)
        self.assertEqual(service.subject, MockSubject)

        subject = MockSubject()
        service = Service(subject)
        self.assertEqual(service.subject, subject)
        self.assertIsInstance(service.subject, MockSubject)
        self.assertNotEqual(service.subject, MockSubject())

    def test_argument(self):
        service = Service(MockSubject)
        service._arguments['key'] = 'value'
        self.assertIsInstance(service.arguments, dict)
        self.assertEqual(len(service.arguments), 1)
        self.assertDictEqual(service._arguments, {'key': 'value'})

    def test_add_argument(self):
        service = Service(MockSubject)
        result = service.add_argument('key', 'value')
        self.assertEqual(service, result)
        self.assertEqual(len(service._arguments), 1)
        self.assertDictEqual(service._arguments, {'key': 'value'})

    def test_add_arguments(self):
        service = Service(MockSubject)
        result = service.add_arguments(key1='value', key2='other_value')
        self.assertEqual(service, result)
        self.assertEqual(len(service._arguments), 2)
        self.assertDictEqual(service._arguments, {'key1': 'value', 'key2': 'other_value'})



