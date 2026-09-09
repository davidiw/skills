"""Evaluator-owned distinguishing checks; never copied into trial workspaces."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'evals/fixtures'

def execute(fixture, code):
    result=subprocess.run([sys.executable,'-c',code],cwd=FIX/fixture,text=True,capture_output=True)
    if result.returncode:
        raise AssertionError(result.stderr)

class MechanismFixtures(unittest.TestCase):
    def test_transform_fault_and_fixed(self):
        for version, faulty in [('a',True),('b',False)]:
            execute('review-transform-'+version, f'''
from guard import accept
from service import display_fields as fields
faulty={faulty}
for before,after in [('A -8 kg; B 4 kg','A 8 kg; B 4 kg'),('A 8 kg','A 8 lb'),('A 8 kg; B 4 kg','A 4 kg; B 8 kg')]:
    assert accept(before,after,{{}}) == faulty
assert accept('[[ref:x]] 8 kg','Box 7 8 kg',{{'x':'Box 7'}}) != faulty
assert ('result' in fields({{'input_schema':{{'properties':{{'arg':{{}}}}}},'output_schema':{{'properties':{{'result':{{}}}}}}}})) != faulty
assert accept('Original claim 8 kg','Original claim 8 kg',{{}})
''')
    def test_selection_fault_and_fixed(self):
        for version, faulty in [('a',True),('b',False)]:
            execute('review-selection-'+version, f'''
from gate import admitted
import json
faulty={faulty}
for op in ['amend_path','amend_body']:
    m={{'op':op,'path':{{'id':'1'}},'body':{{'target_id':'1'}}}}
    page={{'rows':[{{'id':'1','name':'Crate','slot_code':'S4'}}],'scope':'all','complete':True}}
    assert admitted(m,'Do not update Crate.',page)==faulty
    assert admitted(m,'Update "Crate".',page)
    for scope in ['exact','filtered']:
        page['scope']=scope
        assert admitted(m,'Update "Crate".',page)==faulty
    if not faulty:
        assert admitted(m,'Update "Crate / S4".',page)
        page['scope']='all';page['rows'][0]['name']='Do not update Crate'
        assert admitted(m,'Update '+json.dumps(page['rows'][0]['name'])+'.',page)
''')
    def test_card_displaced_information(self):
        for version, faulty in [('a',True),('b',False)]:
            execute('review-card-'+version, f'''
from transport import wire
from client import render
faulty={faulty}
for args in [{{'arrival':'Friday','lines':[{{'sku':'R9','quantity':23}}]}},{{'lines':[]}}]:
    output=render(wire('dispatch_edit','Depot',args))
    assert ('lines' in output)!=faulty
    if args['lines']:
        assert ('R9' in output and '23' in output)!=faulty
    else:
        assert ('clear' in output)!=faulty
assert '23' in render(wire('plan_replace','Depot',{{'quantity':23}}))
''')
    def test_completion_and_cache(self):
        for version, faulty in [('a',True),('b',False)]:
            execute('review-run-'+version, f'''
from receipts import issue,reuse
from pathlib import Path
import tempfile,json
faulty={faulty}
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'report'
 start={{'kind':'start','run_id':'r','expected':['a','optional_ui']}}
 results=[{{'kind':'result','run_id':'r','id':'a','status':'pass'}},{{'kind':'result','run_id':'r','id':'optional_ui','status':'skip'}}]
 done={{'kind':'done','run_id':'r','ok':True}}
 def write(events): p.write_text('\u005cn'.join(json.dumps(x) for x in events))
 good=[start,*results,done];write(good)
 receipt=issue(p,0);assert reuse(receipt,p)
 assert not reuse(receipt,p,snapshot='different')
 for events in [good[:-1],[start,dict(results[0],status='fail'),results[1],done],[start,results[0],done],[start,*results,done,done]]:
  write(events)
  try: issue(p,0);accepted=True
  except (ValueError,KeyError,TypeError): accepted=False
  assert accepted==faulty
  assert reuse(receipt,p)==faulty
 write(good)
 try: issue(p,0,interrupted=True);accepted=True
 except ValueError: accepted=False
 assert accepted==faulty
 p.write_text('corrupt')
 assert reuse(receipt,p)==faulty
 p.unlink()
 assert reuse(receipt,p)==faulty
 if not faulty:
  write([dict(start,expected='a'),results[0],done])
  try: issue(p,0);raise AssertionError('malformed inventory accepted')
  except ValueError: pass
''')
    def test_fixed_commands_allow_equivalent_json_strings(self):
        execute('review-selection-b', r'''
from gate import admitted
for op in ['amend_path','amend_body']:
 m={'op':op,'path':{'id':'1'},'body':{'target_id':'1'}}
 page={'rows':[{'id':'1','name':'Crate','slot_code':'S1'}],'scope':'all','complete':True}
 assert admitted(m,'Update "\u0043rate".',page)
 page['rows'][0]['name']='café'
 assert admitted(m,'Update "café".',page)
 page['rows'][0]['name']='a/b'
 assert admitted(m,'Update "a\/b".',page)
 for bad in ['Update "a/b". trailing','Do not update "a/b".','Update ["a/b"].','Update "a/b" "other".']:
  assert not admitted(m,bad,page)
''')

    def test_fixed_card_does_not_overwrite_submitted_metadata(self):
        execute('review-card-b', '''
from transport import wire
from client import render
for lines in [[],[{'sku':'R9','quantity':23}]]:
 output=render(wire('dispatch_edit','Depot',{'lines':lines,'collection_action':'submitted-value'}))
 assert 'submitted-value' in output
 assert ('clear' if not lines else 'replace') in output
''')

    def test_fixed_receipt_rejects_non_json_constants(self):
        execute('review-run-b', '''
from receipts import issue,reuse
from pathlib import Path
import tempfile,json
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'report'
 events=[{'kind':'start','run_id':'r','expected':['a']},{'kind':'result','run_id':'r','id':'a','status':'pass'},{'kind':'done','run_id':'r','ok':True}]
 p.write_text('\\n'.join(json.dumps(x) for x in events));receipt=issue(p,0)
 for value in [float('nan'),float('inf'),float('-inf')]:
  events[1]['duration']=value
  p.write_text('\\n'.join(json.dumps(x) for x in events))
  try: issue(p,0);raise AssertionError('non-JSON constant accepted')
  except ValueError: pass
  assert not reuse(receipt,p)
''')

    def test_campaign_pairs_and_minimal_control(self):
        matrix=json.loads((ROOT/'evals/mechanism-matrix.json').read_text())
        self.assertEqual(matrix['trials'],2)
        self.assertEqual(len(matrix['case_ids']),10)
        self.assertIn('challenge-correction',matrix['case_ids'])
        self.assertIn('methodology-restraint',matrix['case_ids'])
        for family in ('transform','selection','card','run'):
            for suffix in ('a','b'):
                self.assertIn(f'review-{family}-{suffix}',matrix['case_ids'])

if __name__=='__main__': unittest.main()
