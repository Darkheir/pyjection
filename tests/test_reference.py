from unittest import TestCase
from pyjection.reference import Reference


class TestReference(TestCase):

    def test_name(self):
        reference = Reference('test_name')
        self.assertEqual(reference.name, 'test_name')

