import unittest
from screen import AccountFence, load_screen

class ScreenTest(unittest.IsolatedAsyncioTestCase):
    async def test_current_load(self):
        class Service:
            async def read(self): return "current"
        fence = AccountFence()
        await load_screen(fence, Service())
        self.assertEqual(fence.visible, "current")
