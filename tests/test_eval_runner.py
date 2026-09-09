import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import os
import tomllib
from unittest.mock import patch
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("natural_runner", ROOT / "evals/run_natural_matrix.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class EvaluationRunnerTest(unittest.TestCase):
    def test_context_usage_uses_final_counter_and_keeps_child_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            sessions = home / "sessions"
            sessions.mkdir()
            for thread, parent, totals in (("builder", None, [100, 180]), ("reviewer", "builder", [40, 70])):
                events = [{"type": "session_meta", "payload": {"id": thread, "parent_thread_id": parent,
                           "base_instructions": "private base", "source": "exec"}}]
                for total in totals:
                    events.append({"type": "event_msg", "payload": {"type": "token_count", "info": {
                        "total_token_usage": {"input_tokens": total, "cached_input_tokens": total // 2, "output_tokens": 10}}}})
                (sessions / f"rollout-{thread}.jsonl").write_text("\n".join(json.dumps(e) for e in events))
            contexts = runner.context_records(home)
            self.assertEqual(sum(c["usage"]["input_tokens"] for c in contexts), 250)
            self.assertEqual(sum(c["usage"]["uncached_input_tokens"] for c in contexts), 125)
            self.assertEqual({c["id"] for c in contexts}, {"builder", "reviewer"})
            self.assertNotIn("private base", json.dumps(contexts))
            self.assertEqual({c["id"]: c["kind"] for c in contexts},
                             {"builder": "primary", "reviewer": "delegated"})

    def test_context_keeps_timing_but_excludes_private_reasoning(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            sessions = home / "sessions"
            sessions.mkdir()
            events = [
                {"type": "event_msg", "timestamp": "2026-09-06T12:00:00Z", "payload": {"type": "task_started"}},
                {"type": "response_item", "payload": {"type": "reasoning", "encrypted_content": "private"}},
                {"type": "event_msg", "timestamp": "2026-09-06T12:00:04Z", "payload": {"type": "task_complete"}},
            ]
            (sessions / "rollout-example.jsonl").write_text("\n".join(json.dumps(e) for e in events))
            context = runner.context_records(home)[0]
            self.assertEqual(context["wall_seconds"], 4)
            self.assertNotIn("private", json.dumps(context))

    def test_runtime_verification_rejects_git_even_when_tree_hash_ignores_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, runtime = root / "source", root / "runtime"
            source.mkdir(); runtime.mkdir()
            for p in (source, runtime):
                (p / "runtime.md").write_text("runtime")
            self.assertEqual(runner.verify_runtime(runtime, runner.tree(source)), runner.tree(source))
            (runtime / ".git").mkdir()
            with self.assertRaisesRegex(RuntimeError, "development material"):
                runner.verify_runtime(runtime, runner.tree(source))
            self.assertTrue((runtime / ".git").exists())

    def test_relative_paths_do_not_redact_punctuation_or_inventory(self):
        replacements = runner.redaction_paths("run", ".", "evals/cases.json", "catalog")
        value = {"skills/example/SKILL.md": "0.9.0. Done.",
                 "path": str(Path.cwd() / "private.txt"),
                 "eval_input": "evals/cases.json"}
        result = runner.redact(value, replacements, [])
        self.assertEqual(result["skills/example/SKILL.md"], "0.9.0. Done.")
        self.assertEqual(result["eval_input"], "evals/cases.json")
        self.assertEqual(result["path"], "<PACKAGE>/private.txt")

    def test_redaction_covers_dictionary_keys_and_nested_transcripts(self):
        value = {"private/path": {"stdout": "private/path secret-token"}}
        self.assertEqual(runner.redact(value, {"private/path": "<PATH>"}, ["secret-token"]),
                         {"<PATH>": {"stdout": "<PATH> <REDACTED>"}})

    def test_post_run_cache_loss_preserves_completed_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "source"
            fixture.mkdir()
            (fixture / "app.py").write_text("pass")
            result = {"stdout": "retained output", "stderr": "failure detail",
                      "return_code": 1, "timed_out": False, "started_at": 1, "ended_at": 3}
            contexts = [{"usage": {"input_tokens": 10}, "completed": True}]
            with patch.object(runner, "assert_frozen_source"), \
                 patch.object(runner, "setup", return_value=({"inventory": "retained"}, {})), \
                 patch.object(runner, "command", return_value=result), \
                 patch.object(runner, "context_records", return_value=contexts):
                record = runner.trial({"id": "cache-loss", "fixture": "source", "request": "do"},
                                      root, root, root / "output", 1, "harness", root / "auth",
                                      root / "catalog", "model", "medium", 1,
                                      {"source_revision": "frozen", "runtime_file_hashes": {}})
            self.assertTrue(record["setup_or_trial_failed"])
            self.assertIn("inventory changed", record["error"])
            self.assertEqual(record["result"], result)
            self.assertEqual(record["setup"], {"inventory": "retained"})
            self.assertEqual(record["aggregate_usage"]["input_tokens"], 10)
            self.assertEqual(record["wall_seconds"], 2)
            self.assertTrue(record["command"])
            self.assertIn("fixture_diff", record)

    def test_setup_failure_preserves_command_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "catalog").mkdir()
            (root / "auth").write_text("{}")
            attempts, checkpoints = [], []
            result = {"return_code": 1, "stdout": "partial setup", "stderr": "failure"}
            with patch.object(runner, "command", return_value=result):
                with self.assertRaisesRegex(RuntimeError, "plugin setup"):
                    runner.setup(root / "home", root, root / "catalog", "harness", root / "auth",
                                 expected_runtime={}, attempts=attempts,
                                 checkpoint=lambda: checkpoints.append(len(attempts)))
            self.assertEqual(attempts[0]["result"], result)
            self.assertEqual(checkpoints, [1])

    def test_frozen_source_rejects_dirty_checkout_and_later_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evals/fixtures").mkdir(parents=True)
            (root / "plugins/engineering-harness").mkdir(parents=True)
            (root / "evals/run_natural_matrix.py").write_bytes(Path(runner.__file__).read_bytes())
            for name in ("assurance-matrix.json", "cases.json"):
                (root / "evals" / name).write_text("{}")
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            git = ["git", "-c", "user.name=eval", "-c", "user.email=eval@invalid"]
            subprocess.run(git + ["add", "."], cwd=root, check=True)
            subprocess.run(git + ["commit", "-qm", "baseline"], cwd=root, check=True)
            frozen = runner.frozen_source(root, root / "evals/assurance-matrix.json")
            (root / "plugins/engineering-harness/changed.md").write_text("changed")
            with self.assertRaisesRegex(RuntimeError, "dirty"):
                runner.frozen_source(root, root / "evals/assurance-matrix.json")
            subprocess.run(git + ["add", "."], cwd=root, check=True)
            subprocess.run(git + ["commit", "-qm", "changed"], cwd=root, check=True)
            with self.assertRaisesRegex(RuntimeError, "revision changed"):
                runner.assert_frozen_source(root, frozen)

    def test_public_streams_and_analysis_messages_are_filtered(self):
        private = {"type": "message", "role": "assistant", "channel": "analysis", "content": "PRIVATE"}
        raw = "\n".join(json.dumps(v) for v in [
            {"type": "item.completed", "item": private},
            {"type": "reasoning", "encrypted_content": "PRIVATE"},
            {"type": "item.completed", "item": {"type": "agent_message", "text": "public"}},
        ])
        public = runner.public_evidence({"result": {"stdout": raw, "stderr": "PRIVATE"},
                                         "contexts": [{"trace": [{"payload": private}]}]})
        self.assertNotIn("PRIVATE", json.dumps(public))
        self.assertIn("public", json.dumps(public))
        self.assertIn("stdout_sha256", public["result"])
        self.assertNotIn("stdout", public["result"])

    def test_separate_session_is_not_mislabeled_as_builder_or_named_agent(self):
        contexts = [{"id": "builder", "kind": "primary", "agent_configuration": "primary"},
                    {"id": "review", "kind": "primary", "agent_configuration": "primary"},
                    {"id": "child", "kind": "delegated", "agent_configuration": "custom"}]
        runner.bind_primary_context(contexts, json.dumps({"type": "thread.started", "thread_id": "builder"}))
        self.assertEqual([c["kind"] for c in contexts], ["primary", "separate_session", "delegated"])
        self.assertEqual(contexts[1]["agent_configuration"], "unattributed")
        self.assertEqual(contexts[2]["agent_configuration"], "custom")

    def test_public_handoff_preserves_flags_but_hashes_opaque_payload(self):
        opaque = "gAAAA" + "opaque" * 30
        value = {"arguments": json.dumps({"fork_turns": "none", "message": opaque}),
                 "content": [{"type": "encrypted_content", "encrypted_content": opaque}]}
        public = runner.public_evidence(value)
        self.assertNotIn(opaque, json.dumps(public))
        self.assertEqual(json.loads(public["arguments"])["fork_turns"], "none")
        self.assertIn("opaque_content_sha256", public["content"][0])

    def test_boundary_failure_precedes_real_auth_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'catalog').mkdir()
            (root / 'auth').write_text('REAL_TEST_CREDENTIAL')
            def reject(home, *args):
                self.assertFalse((home / 'auth.json').exists())
                raise RuntimeError('boundary rejected')
            with patch.object(runner, 'offline_browser_boundary', side_effect=reject), \
                 patch.object(runner, 'command') as command:
                with self.assertRaisesRegex(RuntimeError, 'boundary rejected'):
                    runner.setup(root / 'home', root, root / 'catalog', 'control', root / 'auth',
                                 expected_runtime={}, attempts=[], checkpoint=lambda: None,
                                 fixture=root / 'fixture', offline_browser=True)
            command.assert_not_called()
            self.assertFalse((root / 'home/auth.json').exists())

    def test_boundary_config_and_canary_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            home, fixture = root / 'home', root / 'fixture'
            home.mkdir(); fixture.mkdir()
            browser = root / 'browser'; browser.write_text('synthetic executable')
            expected = {'auth': 'denied', 'auth_alias': 'denied', 'outside': 'denied',
                        'direct_http': 'blocked', 'proxy_http': '403',
                        'direct_socket': 'blocked', 'local_ipc': 'ok'}
            def run(args, env, cwd, timeout):
                self.assertIn('synthetic credential canary', (home / 'auth.json').read_text())
                config = tomllib.loads((home / 'config.toml').read_text())
                self.assertTrue(config['features']['network_proxy'])
                self.assertEqual(config['web_search'], 'disabled')
                self.assertEqual(config['shell_environment_policy']['inherit'], 'none')
                profile = config['permissions']['experience-offline']
                self.assertEqual(profile['network']['domains'], {})
                self.assertEqual(profile['filesystem'][':root'], 'deny')
                self.assertNotIn(str(home), profile['filesystem'])
                self.assertNotIn('--sandbox', args)
                for arg in args:
                    if arg.startswith('--screenshot='):
                        Path(arg.split('=', 1)[1]).write_bytes(b'synthetic image')
                return {'return_code': 0, 'stdout': json.dumps(expected)}
            with patch.object(runner, 'command', side_effect=run):
                result = runner.offline_browser_boundary(home, fixture,
                    {**os.environ, 'EXPERIENCE_CHROMIUM': str(browser)}, [], lambda: None)
            self.assertEqual(result['preflight'], expected)
            self.assertFalse((home / 'auth.json').exists())
            self.assertFalse((home / 'boundary-canary').exists())
            self.assertEqual(result['local_server_connections'], 0)

    def test_failed_setup_still_retains_an_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = runner.trial({"id": "missing", "fixture": "absent", "request": "do"},
                                  root, root, root / "output", 1, "control", root / "auth",
                                  root / "catalog", "model", "medium", 1)
            self.assertTrue(record["setup_or_trial_failed"])
            self.assertTrue((root / "output/private/missing-control-trial1/record.json").is_file())


if __name__ == "__main__":
    unittest.main()
