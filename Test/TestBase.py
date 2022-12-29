from unittest import TestCase

from Singleton import Singleton


class MockTest(TestCase):

    def setUp(self):
        self.instance = Singleton.get_instance()

    def tearDown(self):
        del self.instance
