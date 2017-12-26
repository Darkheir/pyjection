from unittest import TestCase
from unittest.mock import Mock
from pyjection.reference import Reference


class TestReference(TestCase):

    def test_name(self):
        reference = Reference('test_name')
        self.assertEqual(reference.name, 'test_name')

    def test_name_class(self):
        reference = Reference(Mock)
        self.assertEqual(reference.name, 'mock')

    def test_return_class(self):
        reference = Reference('test_name', True)
        self.assertEqual(reference.return_class, True)

