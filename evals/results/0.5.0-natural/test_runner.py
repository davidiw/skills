import json, os, stat, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
import run_matrix

class RunnerTests(unittest.TestCase):
    def test_control_never_adds_plugin_and_inventory_is_empty(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); fake=root/'codex'; log=root/'calls';
            fake.write_text('#!/bin/sh\necho "$*" >> "$FAKE_LOG"\ncase "$*" in *"plugin list"*) echo "{\\"installed\\":[]}";; esac\n')
            fake.chmod(fake.stat().st_mode | stat.S_IXUSR); (root/'pkg'/'.codex-plugin').mkdir(parents=True); (root/'pkg'/'.codex-plugin'/'plugin.json').write_text('{}'); skill=root/'diagnosing'/'SKILL.md'; skill.parent.mkdir(); skill.write_text('x'); auth=root/'auth'; auth.write_text('x'); home=root/'home'; old=os.environ.get('PATH'); os.environ['PATH']=str(root)+':'+old
            os.environ['FAKE_LOG']=str(log)
            try:
                run_matrix.setup(home, root/'pkg', skill, 'control', auth)
                self.assertNotIn('plugin add', log.read_text())
            finally: os.environ['PATH']=old; os.environ.pop('FAKE_LOG', None)

    def test_missing_fixture_is_recorded(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); spec={'id':'x','request':'do','fixture':'absent'}
            rec=run_matrix.trial(spec, root, root, root/'out', 1, 'control', root/'auth', root/'skill/SKILL.md', 'm', 'medium', 1)
            self.assertTrue(rec['setup_or_trial_failed']); self.assertIn('fixture missing', rec['error'])

if __name__ == '__main__': unittest.main()
