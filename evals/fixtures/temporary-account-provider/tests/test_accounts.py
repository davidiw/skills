import unittest
from accounts import Account, create_temporary
from mobile_oauth import MobileOAuth, UnsupportedAccount


class AccountTest(unittest.TestCase):
    def test_temporary_creation(self):
        self.assertTrue(create_temporary("temp", 100).temporary)

    def test_permanent_mobile_link(self):
        registry = {"member": {"grants": {}}}
        oauth = MobileOAuth(registry)
        callback = oauth.begin(Account("member"), "polar")
        oauth.complete(callback, "synthetic-grant")
        self.assertEqual(registry["member"]["grants"], {"polar": "synthetic-grant"})

    def test_native_callback_requires_permanent_subject(self):
        with self.assertRaises(UnsupportedAccount):
            MobileOAuth({}).begin(create_temporary("temp", 100), "polar")
