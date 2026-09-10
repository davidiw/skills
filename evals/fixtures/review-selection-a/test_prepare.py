import unittest
from service import prepare
class PrepareTest(unittest.TestCase):
    def test_prepare(self):
        mutation={"op":"amend_path","path":{"id":"a"},"body":{"quantity":7}}
        page={"scope":"all","complete":True,"rows":[{"id":"a","name":"Crate"}]}
        self.assertEqual(prepare(mutation, 'Update "Crate".', page)["arguments"], mutation)
