import tempfile
import unittest
from pathlib import Path
import job_store as store
import worker

class QueueSmoke(unittest.TestCase):
    def test_current_claim_completes_and_survives_reopen(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'queue.db'
            with store.connect(path) as db:
                store.enqueue(db,'job','input')
                lease=worker.take(db,'worker',10,5)
                self.assertIsNone(worker.take(db,'other',11,5))
                self.assertTrue(worker.deliver(db,lease,'rendered',12))
            with store.connect(path) as db:
                self.assertEqual(store.inspect(db,'job')['result'],'rendered')
                self.assertIsNone(worker.take(db,'other',20,5))
