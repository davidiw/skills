import importlib.util
import copy
import json
from pathlib import Path
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location(
    "attribute_costs", Path(__file__).resolve().parents[1] / "evals/attribute_costs.py")
COST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COST)


def event(kind, payload):
    return {"type": kind, "payload": payload}


class CostAttributionTests(unittest.TestCase):
    def fixture(self, root):
        run, runtime = root / "run", root / "runtime"
        trial = run / "private/example-harness-trial1"
        (trial / "codex-home/sessions").mkdir(parents=True)
        (trial / "fixture").mkdir()
        (run / "public").mkdir()
        runtime.mkdir()
        (runtime / "SKILL.md").write_text("runtime")
        (trial / "fixture/source.py").write_text("original source")
        usage = {"input_tokens": 100, "cached_input_tokens": 80,
                 "output_tokens": 10, "reasoning_output_tokens": 2}
        events = [event("session_meta", {"id": "context"}),
                  event("event_msg", {"type": "task_started", "turn_id": "own-turn"}),
                  event("response_item", {"type": "message", "role": "assistant",
                  "phase": "final_answer", "content": [{"type": "output_text", "text": "original message"}]}),
                  event("token_usage_record", {"response_id": "one", "usage": usage}),
                  event("event_msg", {"type": "task_complete", "turn_id": "own-turn"})]
        trace = trial / "codex-home/sessions/rollout-test.jsonl"
        trace.write_text("\n".join(json.dumps(e) for e in events))
        context = {"id": "context", "trace_file": "sessions/rollout-test.jsonl", "kind": "primary",
                   "agent_configuration": "primary", "model": "same-model", "reasoning_effort": "medium",
                   "wall_seconds": 2, "completed": True, "skill_bodies_observed": [], "usage": usage}
        record = {"case_id": "example", "arm": "harness", "trial": 1, "package_revision": "candidate",
                  "result": {"return_code": 0, "stdout": json.dumps({"type": "thread.started", "thread_id": "context"})}, "wall_seconds": 2, "contexts": [context],
                  "context_count": 1, "aggregate_usage": COST.usage_sum([usage]),
                  "fixture_before_hashes": {"source.py": COST.sha(b"original source")},
                  "fixture_after_hashes": {"source.py": COST.sha(b"original source")}}
        path = trial / "record.json"
        path.write_text(json.dumps(record))
        (run / "public/manifest.json").write_text(json.dumps([record]))
        plan = {"source_revision": "candidate", "planned_trials": 1, "selected_cases": ["example"],
                "selected_arms": ["harness"], "trial_override": None, "interrupted": False,
                "runtime_file_hashes": {"SKILL.md": COST.sha(b"runtime")}}
        (run / "public/run.json").write_text(json.dumps(plan))
        return run, runtime, path, trace, record

    def pin(self, root, run):
        inventory = root / "retained-digests.json"
        inventory.write_text(json.dumps({str(p.relative_to(run)): COST.sha(p.read_bytes())
                                        for p in run.rglob("*") if p.is_file()}))
        return inventory, COST.sha(inventory.read_bytes())

    def test_invocation_counters_reconcile_without_reasoning_contents(self):
        router = "skills/using-engineering-harness/SKILL.md"
        usage = {"input_tokens": 100, "cached_input_tokens": 80, "output_tokens": 10,
                 "reasoning_output_tokens": 2}
        context = {"id": "test", "kind": "primary", "agent_configuration": "primary",
                   "model": "same-model", "reasoning_effort": "medium", "wall_seconds": 2,
                   "skill_bodies_observed": ["using-engineering-harness"],
                   "usage": {k: v * 2 for k, v in usage.items()}}
        call = {"type": "custom_tool_call", "call_id": "read", "name": "exec",
                "input": f'text(await tools.exec_command({{cmd:"cat /runtime/{router}"}}));'}
        events = [event("response_item", call),
                  event("token_usage_record", {"response_id": "first", "usage": usage}),
                  event("response_item", {"type": "custom_tool_call_output", "call_id": "read"}),
                  event("response_item", {"type": "reasoning", "text": "PRIVATE TEXT"}),
                  event("response_item", {"type": "message", "role": "assistant", "phase": "final_answer",
                                          "content": [{"type": "output_text", "text": "Done."}]}),
                  event("token_usage_record", {"response_id": "second", "usage": usage}),
                  event("token_usage_record", {"response_id": "second", "usage": usage})]
        result = COST.context_cost(context, events, {router: 80})
        self.assertEqual(result["usage"]["output_tokens"], 20)
        self.assertEqual(result["usage"]["uncached_input_tokens"], 40)
        self.assertEqual([x["stage"] for x in result["invocations"]],
                         ["discovery_or_competing_skill", "router"])
        self.assertEqual(result["messages"]["final_bytes"], 5)
        self.assertNotIn("PRIVATE TEXT", str(result))
        conflicting = copy.deepcopy(events)
        conflicting[-1]["payload"]["usage"] = dict(conflicting[-1]["payload"]["usage"])
        conflicting[-1]["payload"]["usage"]["output_tokens"] += 1
        with self.assertRaisesRegex(ValueError, "Conflicting duplicate"):
            COST.context_cost(context, conflicting, {router: 80})
        context["usage"]["output_tokens"] += 1
        with self.assertRaises(ValueError):
            COST.context_cost(context, events, {router: 80})

    def test_analyze_rejects_incomplete_contexts_and_trial_totals(self):
        with tempfile.TemporaryDirectory() as directory:
            run, runtime, path, _, original = self.fixture(Path(directory))
            for change in (lambda r: r.update(measurement_incomplete=True),
                           lambda r: r.update(setup_or_trial_failed=True),
                           lambda r: r["contexts"][0].update(completed=False),
                           lambda r: r.update(context_count=2),
                           lambda r: r["aggregate_usage"].update(output_tokens=11)):
                with self.subTest(change=change):
                    record = copy.deepcopy(original)
                    change(record)
                    path.write_text(json.dumps(record))
                    with self.assertRaises(ValueError):
                        COST.analyze(run, runtime)

    def test_analyze_rejects_duplicate_context_even_if_totals_are_doubled(self):
        with tempfile.TemporaryDirectory() as directory:
            run, runtime, path, _, record = self.fixture(Path(directory))
            record["contexts"] *= 2
            record["context_count"] = 2
            record["aggregate_usage"] = COST.usage_sum(c["usage"] for c in record["contexts"])
            path.write_text(json.dumps(record))
            (run / "public/manifest.json").write_text(json.dumps([record]))
            with self.assertRaisesRegex(ValueError, "duplicate context"):
                COST.analyze(run, runtime)

    def test_analyze_reconciles_trial_inventory_and_retains_execution_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            run, runtime, path, _, record = self.fixture(Path(directory))
            record["result"]["return_code"] = 1
            path.write_text(json.dumps(record))
            result = COST.analyze(run, runtime)
            self.assertEqual(result["trials"][0]["return_code"], 1)
            self.assertEqual(result["execution_failure_count"], 1)
            self.assertEqual(result["arms"]["harness"]["usage"]["input_tokens"], 100)
            path.unlink()
            with self.assertRaisesRegex(ValueError, "planned inventory"):
                COST.analyze(run, runtime)
            plan_path = run / "public/run.json"
            plan = json.loads(plan_path.read_text())
            plan["planned_trials"] = 2
            plan_path.write_text(json.dumps(plan))
            with self.assertRaisesRegex(ValueError, "planned trial inventory"):
                COST.analyze(run, runtime)

    def test_analyze_labels_unpinned_evidence_and_verifies_pinned_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run, runtime, _, _, _ = self.fixture(root)
            self.assertEqual(COST.analyze(run, runtime)["integrity"]["status"], "unverified")
            inventory, digest = self.pin(root, run)
            result = COST.analyze(run, runtime, inventory, digest)
            self.assertEqual(result["integrity"]["status"], "verified_against_supplied_inventory")
            with self.assertRaisesRegex(ValueError, "both retained"):
                COST.analyze(run, runtime, inventory)
            inventory.write_text("{}")
            with self.assertRaisesRegex(ValueError, "pinned SHA256"):
                COST.analyze(run, runtime, inventory, digest)

    def test_analyze_rejects_changed_trace_and_record_against_retained_identity(self):
        for target in ("trace", "record", "manifest"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                run, runtime, path, trace, _ = self.fixture(root)
                inventory, digest = self.pin(root, run)
                changed = {"trace": trace, "record": path, "manifest": run / "public/manifest.json"}[target]
                changed.write_text(changed.read_text().replace("original", "altered") + "\n")
                with self.assertRaisesRegex(ValueError, "retained inventory"):
                    COST.analyze(run, runtime, inventory, digest)

    def test_analyze_checks_existing_fixture_and_runtime_files(self):
        for target in ("fixture/source.py", "runtime"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                run, runtime, path, _, _ = self.fixture(Path(directory))
                changed = runtime / "SKILL.md" if target == "runtime" else path.parent / target
                changed.write_text("tampered")
                with self.assertRaisesRegex(ValueError, "Changed retained file"):
                    COST.analyze(run, runtime)

    def test_analyze_checks_raw_context_inventory_identity_and_completion(self):
        for target in ("extra_context", "identity", "completion"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                run, runtime, _, trace, _ = self.fixture(Path(directory))
                if target == "extra_context":
                    trace.with_name("rollout-unrecorded.jsonl").write_bytes(trace.read_bytes())
                else:
                    events = [json.loads(line) for line in trace.read_text().splitlines()]
                    if target == "identity":
                        events[0]["payload"]["id"] = "different"
                    else:
                        events = events[:-1]
                    trace.write_text("\n".join(json.dumps(e) for e in events))
                with self.assertRaisesRegex(ValueError, "context"):
                    COST.analyze(run, runtime)

    def test_analyze_uses_first_header_when_legacy_record_flattens_ancestor_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            run, runtime, path, trace, record = self.fixture(Path(directory))
            events = [json.loads(line) for line in trace.read_text().splitlines()]
            parent_events = copy.deepcopy(events)
            parent_events[0]["payload"]["id"] = "ancestor"
            for e in parent_events:
                if "turn_id" in e["payload"]:
                    e["payload"]["turn_id"] = "parent-turn"
                if e["type"] == "token_usage_record":
                    e["payload"]["response_id"] = "parent-invocation"
            parent_trace = trace.with_name("rollout-parent.jsonl")
            parent_trace.write_text("\n".join(json.dumps(e) for e in parent_events))
            parent_context = copy.deepcopy(record["contexts"][0])
            parent_context.update(id="ancestor", trace_file="sessions/rollout-parent.jsonl")
            record["contexts"].append(parent_context)
            record["context_count"] = 2
            record["aggregate_usage"] = COST.usage_sum(c["usage"] for c in record["contexts"])
            events.insert(1, event("session_meta", {"id": "ancestor"}))
            # Copied lifecycle events are not work owned by the child.
            events[2:2] = [e for e in parent_events if e["type"] == "event_msg"]
            events[0]["payload"]["source"] = {"subagent": {"thread_spawn": {"agent_role": "reviewer", "parent_thread_id": "ancestor"}}}
            events[1]["payload"]["source"] = "cli"
            record["result"]["stdout"] = json.dumps({"type": "thread.started", "thread_id": "ancestor"})
            record["setup"] = {"agents": {"role_file_hashes": {"reviewer.toml": "retained-role-digest"}}}
            trace.write_text("\n".join(json.dumps(e) for e in events))
            runner_spec = importlib.util.spec_from_file_location("natural_runner", SPEC.origin.replace("attribute_costs.py", "run_natural_matrix.py"))
            runner = importlib.util.module_from_spec(runner_spec)
            runner_spec.loader.exec_module(runner)
            produced = runner.context_records(path.parent / "codex-home")
            runner.bind_primary_context(produced, record["result"]["stdout"])
            flattened = next(c for c in produced if c["trace_file"] == "sessions/rollout-test.jsonl")
            record["contexts"][0].update({k: flattened[k] for k in ("id", "kind", "agent_configuration")})
            path.write_text(json.dumps(record))
            (run / "public/manifest.json").write_text(json.dumps([record]))
            result = COST.analyze(run, runtime)["trials"][0]["contexts"][0]
            self.assertEqual(result["id"], "context")
            self.assertEqual(result["recorded_id"], "ancestor")
            self.assertEqual(result["configuration"], "custom")
            self.assertEqual(result["agent_role"], "reviewer")
            self.assertEqual(result["recorded_configuration"], flattened["agent_configuration"])
            self.assertEqual(result["kind"], "delegated")
            self.assertEqual(result["recorded_kind"], "primary")

            # An inherited completion cannot satisfy an unfinished child turn.
            trace.write_text("\n".join(json.dumps(e) for e in events[:-1]))
            with self.assertRaisesRegex(ValueError, "completion"):
                COST.analyze(run, runtime)

    def test_child_role_uses_nested_native_metadata_and_does_not_guess_when_absent(self):
        for metadata, configuration, role in (
                ({"source": {"subagent": {"thread_spawn": {"agent_role": "reviewer"}}}}, "custom", "reviewer"),
                ({"source": {"subagent": {"thread_spawn": {"agent_role": None}}}}, "generic", None),
                ({"agent_role": "default"}, "unavailable", "default"),
                ({}, "unavailable", None)):
            with self.subTest(metadata=metadata), tempfile.TemporaryDirectory() as directory:
                run, runtime, path, trace, record = self.fixture(Path(directory))
                events = [json.loads(line) for line in trace.read_text().splitlines()]
                events[0]["payload"].update(metadata, parent_thread_id="external-parent")
                record["setup"] = {"agents": {"role_file_hashes": {"reviewer.toml": "retained-role-digest"}}}
                trace.write_text("\n".join(json.dumps(e) for e in events))
                record["contexts"][0].update(kind="delegated", agent_configuration="custom")
                path.write_text(json.dumps(record))
                result = COST.analyze(run, runtime)["trials"][0]["contexts"][0]
                self.assertEqual((result["configuration"], result["agent_role"]), (configuration, role))
                self.assertEqual(result["recorded_configuration"], "custom")
                self.assertEqual(result["usage"]["output_tokens"], 10)

    def test_analyze_rejects_unfinished_or_aborted_followup_after_completed_turn(self):
        for ending in ([], [event("event_msg", {"type": "turn_aborted", "turn_id": "followup"})],
                       [event("event_msg", {"type": "task_complete", "turn_id": "own-turn"})]):
            with self.subTest(ending=ending), tempfile.TemporaryDirectory() as directory:
                run, runtime, _, trace, _ = self.fixture(Path(directory))
                original = trace.read_text()
                followup = [event("event_msg", {"type": "task_started", "turn_id": "followup"})] + ending
                trace.write_text(original + "\n" + "\n".join(json.dumps(e) for e in followup))
                with self.assertRaisesRegex(ValueError, "completion"):
                    COST.analyze(run, runtime)
                trace.write_text(original + "\n" + json.dumps(followup[0]) + "\n" + json.dumps(
                    event("event_msg", {"type": "task_complete", "turn_id": "followup"})))
                self.assertTrue(COST.analyze(run, runtime)["trials"][0]["contexts_completed"])

    def test_inherited_work_is_not_native_completion_evidence(self):
        inherited = [event("event_msg", {"type": "task_started", "turn_id": "parent"}),
                     event("event_msg", {"type": "task_complete", "turn_id": "parent"})]
        self.assertFalse(COST.context_completed(inherited, {"parent"}))
        own = [event("event_msg", {"type": "task_started", "turn_id": "child"}),
               event("event_msg", {"type": "task_complete", "turn_id": "child"})]
        self.assertTrue(COST.context_completed(inherited[:1] + own, {"parent"}))
        self.assertFalse(COST.context_completed(own + [event("event_msg", {
            "type": "turn_aborted", "turn_id": "child"})], set()))

    def test_generated_links_are_not_read_requests(self):
        path = "references/assurance-handoff.md"
        call = {"input": f'text(await tools.exec_command({{cmd:"cat > plan.md <<EOF\\nRead {path}\\nEOF"}}));'}
        self.assertEqual(COST.explicit_reads(call, {path: 10}), [])
        read = {"input": f'text(await tools.exec_command({{cmd:"sed -n \'1,5p\' /runtime/{path}"}}));'}
        self.assertEqual(COST.explicit_reads(read, {path: 10}), [path])

    def test_json_handoff_is_measured_and_changed_evidence_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = b'{"scope": "private fixture text"}'
            (root / "handoff.json").write_bytes(data)
            after = {"handoff.json": COST.sha(data), "source.py": "unchanged"}
            result = COST.added_artifacts(root, {"source.py": "unchanged"}, after)
            self.assertEqual(result["handoff.json"]["bytes"], len(data))
            self.assertTrue(result["handoff.json"]["packet_name"])
            self.assertNotIn("private fixture text", str(result))
            (root / "handoff.json").write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "Changed retained artifact"):
                COST.added_artifacts(root, {}, after)


if __name__ == "__main__":
    unittest.main()
