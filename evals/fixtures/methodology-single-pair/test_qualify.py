import unittest
from qualify import qualify
class QualificationTest(unittest.TestCase):
    def test_qualification_uses_policy_and_completion(self):
        pair={'admitted':True,'correctness_failures':0,'regressions':0,'before_seconds':50.65,'after_seconds':38.65}
        self.assertEqual(qualify({'minimum_pairs':5},{'complete':True,'pairs':[pair]})['qualification'],'pending')
        self.assertEqual(qualify({'minimum_pairs':3},{'complete':True,'pairs':[pair]*3})['qualification'],'accepted')
        self.assertEqual(qualify({'minimum_pairs':3},{'complete':False,'pairs':[pair]*3})['qualification'],'pending')
