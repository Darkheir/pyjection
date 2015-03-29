import unittest
from pyjection.reference import Reference


class TestReference(unittest.TestCase):

    def test_name(self):
        reference = Reference('test_name')
        self.assertIsInstance(reference, Reference)
        self.assertEqual(reference.name, 'test_name')

