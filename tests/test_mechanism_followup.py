"""Qualification through real consumers; expected results stay outside fixtures."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_mechanism_fixtures import execute, FIX, ROOT


class MechanismFollowup(unittest.TestCase):
    def run_worker(self, path, action, *args, mode='reference'):
        code = '''
import sys,json
from dataclasses import asdict
import job_store as store
import worker
sys.path.insert(0,sys.argv[1])
import mechanism_recovery_oracle as oracle
if sys.argv[2] != 'original': store.claim=oracle.claim
if sys.argv[2] == 'reference': store.finish=oracle.finish
with store.connect(sys.argv[3]) as db:
 action=sys.argv[4];args=json.loads(sys.argv[5])
 if action=='enqueue': store.enqueue(db,*args);out=True
 elif action=='claim':
  lease=worker.take(db,*args);out=None if lease is None else asdict(lease)
 elif action=='finish': out=worker.deliver(db,store.Lease(**args[0]),*args[1:])
 elif action=='inspect': out=store.inspect(db,*args)
 print(json.dumps(out))
'''
        return [sys.executable, '-c', code, str(ROOT/'tests'), mode, str(path), action, json.dumps(args)]

    def invoke(self, path, action, *args, mode='reference'):
        p=subprocess.run(self.run_worker(path, action, *args, mode=mode),
                         cwd=FIX/'challenge-job-recovery', text=True, capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads(p.stdout)

    def test_recovery_fixture_reference_and_worker_name_counterexample(self):
        for mode in ('reference','worker-name'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                db=Path(tmp)/'queue.db'
                self.invoke(db,'enqueue','job','input',mode=mode)
                old=self.invoke(db,'claim','worker',10,5,mode=mode)
                self.assertIsNone(self.invoke(db,'claim','other',14,5,mode=mode))
                current=self.invoke(db,'claim','worker',15,5,mode=mode)
                self.assertGreater(current['generation'],old['generation'])
                stale=self.invoke(db,'finish',old,'stale output',16,mode=mode)
                self.assertEqual(stale, mode=='worker-name')
                if mode=='reference':
                    row=self.invoke(db,'inspect','job')
                    self.assertEqual(row['state'],'running')
                    self.assertIsNone(row['result'])
                    self.assertTrue(self.invoke(db,'finish',current,'current output',16))
                    self.assertEqual(self.invoke(db,'inspect','job')['result'],'current output')
                    self.assertFalse(self.invoke(db,'finish',current,'second output',17))
                    self.assertIsNone(self.invoke(db,'claim','third',30,5))

    def test_expiry_without_reclaim_and_competing_processes(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/'queue.db';self.invoke(db,'enqueue','job','input')
            old=self.invoke(db,'claim','worker',10,5)
            self.assertFalse(self.invoke(db,'finish',old,'late',15))
            children=[subprocess.Popen(self.run_worker(db,'claim',name,15,5),
                      cwd=FIX/'challenge-job-recovery',text=True,stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE) for name in ('one','two')]
            claims=[]
            for child in children:
                stdout,stderr=child.communicate(timeout=10)
                self.assertEqual(child.returncode,0,stderr);claims.append(json.loads(stdout))
            self.assertEqual(sum(x is not None for x in claims),1)
            self.assertIsNone(self.invoke(db,'inspect','job')['result'])
            current=next(x for x in claims if x is not None)
            self.assertTrue(self.invoke(db,'finish',current,'recovered',16))

    def test_original_fixture_does_not_already_recover(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/'queue.db';self.invoke(db,'enqueue','job','input',mode='original')
            self.invoke(db,'claim','worker',10,5,mode='original')
            self.assertIsNone(self.invoke(db,'claim','other',15,5,mode='original'))

    def test_fixed_transform_consumer_matrix(self):
        execute('review-transform-b', '''
from renderer import render
from service import publish,display_fields
for before,labels in [('',{}),('Original false claim 12 kg.',{}),('[[ref:a]] / [[ref:a]]',{'a':'Box 7!'}),('[[ref:a]]',{'a':'[[ref:b]]'})]:
 expected=render(before,labels);assert publish(before,expected,labels)==expected
 try: publish(before,expected+' ',labels);raise AssertionError('changed text accepted')
 except ValueError: pass
for schemas,expected in [({},set()),({'input_schema':{'properties':{'a':{}}}},{'a'}),({'output_schema':{'properties':{'b':{}}}},{'b'}),({'input_schema':{'properties':{'a':{}}},'output_schema':{'properties':{'a':{},'b':{}}}},{'a','b'})]:
 assert display_fields(schemas)==expected
try: publish('[[ref:missing]]','guessed',{});raise AssertionError('unknown accepted')
except ValueError: pass
''')

    def test_fixed_selection_actual_service(self):
        execute('review-selection-b', r'''
import copy,json
from service import prepare
for op in ('amend_path','amend_body'):
 m={'op':op,'path':{'id':'1'},'body':{'target_id':'1','values':[3]}}
 original=copy.deepcopy(m)
 page={'rows':[{'id':'1','name':'Crate','slot_code':'A1'},{'id':'2','name':'Crate','slot_code':'B2'}],'scope':'all','complete':True}
 good='Update "Crate \/ A1".'
 for scope in ('all','exact','filtered'):
  page['scope']=scope
  assert prepare(m,good,page)['arguments']==m
 for bad in ('Update "Crate".','Do not update "Crate / A1".','Update "Crate / B2".','Update "Crate / A1". extra'):
  try: prepare(m,bad,page);raise AssertionError('invalid command prepared')
  except ValueError: pass
 assert m==original
''')

    def test_fixed_card_serialized_fields_and_collection_variants(self):
        execute('review-card-b', '''
import copy,html,json
from transport import wire
from client import render
for op in ('plan_replace','dispatch_edit'):
 for args in ({'arrival':'Friday'}, {'lines':[],'collection_action':'submitted-value'}, {'lines':[{'sku':'R9','quantity':23}],'collection_action':'custom'}):
  original=copy.deepcopy(args);encoded=wire(op,'Depot',args);card=json.loads(encoded)
  assert card['arguments']==original and args==original
  visible=html.unescape(render(encoded))
  for key,value in args.items():
   assert json.dumps(key)+': '+json.dumps(value,sort_keys=True) in visible
  if op=='dispatch_edit' and 'lines' in args:
   assert 'Collection: '+('clear' if not args['lines'] else 'replace')+'.' in visible
''')

    def test_fixed_completion_protocol_matrix(self):
        execute('review-run-b', '''
import tempfile,json,copy
from pathlib import Path
from receipts import issue,reuse
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'report'
 good=[{'kind':'start','run_id':'r','expected':['a','optional_ui']},{'kind':'result','run_id':'r','id':'a','status':'pass'},{'kind':'result','run_id':'r','id':'optional_ui','status':'skip'},{'kind':'done','run_id':'r','ok':True}]
 def write(events):p.write_text('\\n'.join(json.dumps(x) for x in events))
 write(good);receipt=issue(p,0);assert reuse(receipt,p)
 variants=[good[:-1],good+[good[-1]],good[:2]+[good[1]]+good[2:],good[:1]+good[2:]]
 for index,key,value in [(1,'status','fail'),(1,'status','skip'),(2,'run_id','different'),(3,'ok',False),(1,'duration',float('nan')),(0,'expected','a')]:
  x=copy.deepcopy(good);x[index][key]=value;variants.append(x)
 for events in variants:
  write(events)
  try: issue(p,0);raise AssertionError('invalid report accepted')
  except (ValueError,KeyError,TypeError,AttributeError):pass
  assert not reuse(receipt,p)
 write(good);assert reuse(receipt,p)
 for code,interrupted in [(1,False),(0,True)]:
  try: issue(p,code,interrupted);raise AssertionError('failed execution accepted')
  except ValueError:pass
 p.unlink();assert not reuse(receipt,p)
''')

    def test_followup_keeps_restraint_and_pairs(self):
        cases={x['id']:x for x in json.loads((ROOT/'evals/cases.json').read_text())['cases']}
        self.assertEqual(cases['challenge-correction']['expected_class'],'minimal')
        self.assertEqual(cases['challenge-job-recovery']['expected_class'],'consequential')
        matrix=json.loads((ROOT/'evals/mechanism-followup-matrix.json').read_text())
        self.assertEqual(len(matrix['case_ids']),11)
        self.assertEqual(matrix['trials'],2)
        self.assertEqual(set(matrix['case_ids']),set(json.loads((ROOT/'evals/mechanism-matrix.json').read_text())['case_ids'])|{'challenge-job-recovery'})
