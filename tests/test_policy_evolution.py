from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from profile_repository import check_drift, propose_profile, scan_repository
from validate_package import validate_eval_receipt
from validate_profile import validate_profile


class SensitiveProfileTest(unittest.TestCase):
    def test_sensitive_profile_requires_lifecycle_and_assurance_owners(self):
        profile = json.loads((ROOT / "templates/project-profile.minimal.json").read_text())
        profile["project"]["sensitive_data"] = True
        for invariant in ("typed-boundaries", "authority-context-fencing",
                          "privacy-lifecycle", "open-world-assurance"):
            with self.subTest(invariant=invariant):
                self.assertIn(f"missing enforcement for active invariant: {invariant}",
                              validate_profile(profile))


class ReviewedDiscoveryTest(unittest.TestCase):
    def accepted_rejection(self, repository, *, sensitive=False):
        profile = propose_profile(repository)
        profile["status"] = "accepted"
        profile["enforcement"] = {"canonical-authority": {"rung": "owner", "owner": "README.md"}}
        profile["sources"] = {}
        if sensitive:
            profile["project"]["sensitive_data"] = False
            finding = profile["discovery"]["project_fields"]["sensitive_data"]
        else:
            profile["capabilities"]["external_providers"] = False
            finding = profile["discovery"]["capabilities"]["external_providers"]
        finding["review"] = {"decision": "rejected", "rationale": "Local example vocabulary only.",
                             "authority": "Repository adoption review"}
        return profile

    def test_rejection_applies_only_to_unchanged_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "providers.py"
            source.write_text('def label_provider(): return "local label"\n')
            profile = self.accepted_rejection(root)
            self.assertEqual(check_drift(root, profile), ([], []))
            source.write_text('def label_provider(): return remote.fetch()\n')
            self.assertTrue(any("external_providers" in e for e in check_drift(root, profile)[0]))

    def test_unreviewed_signal_still_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "providers.py").write_text('def label_provider(): return "local label"\n')
            profile = self.accepted_rejection(root)
            del profile["discovery"]["capabilities"]["external_providers"]["review"]
            self.assertTrue(any("external_providers" in e for e in check_drift(root, profile)[0]))

    def test_added_matching_source_requires_new_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "providers.py").write_text('def label_provider(): return "local label"\n')
            profile = self.accepted_rejection(root)
            (root / "zzz").mkdir()
            (root / "zzz/providers.py").write_text('def fetch(): return remote.get()\n')
            self.assertTrue(any("external_providers" in e for e in check_drift(root, profile)[0]))

    def test_sensitive_rejection_expires_on_content_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "labels.py"
            source.write_text('LABEL = "medical"\n')
            profile = self.accepted_rejection(root, sensitive=True)
            self.assertEqual(check_drift(root, profile), ([], []))
            source.write_text('def read_medical_record(): return db.patient()\n')
            self.assertIn("new high-confidence sensitive-data signal", check_drift(root, profile)[0])

    def test_rejection_requires_evidence_and_review_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "providers.py").write_text('def label_provider(): return "local label"\n')
            profile = self.accepted_rejection(root)
            for field in ("rationale", "authority"):
                candidate = copy.deepcopy(profile)
                del candidate["discovery"]["capabilities"]["external_providers"]["review"][field]
                self.assertTrue(validate_profile(candidate))
            profile["discovery"]["capabilities"]["external_providers"]["evidence"] = []
            self.assertTrue(validate_profile(profile))

    def test_malformed_decision_owner_reports_errors_instead_of_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "providers.py").write_text('def label_provider(): return "local label"\n')
            profile = self.accepted_rejection(root)
            profile["capabilities"] = None
            self.assertTrue(validate_profile(profile))

    def test_consent_owner_is_detected_without_durable_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "consent_context.py").write_text("def may_export(): return consent.active\n")
            scan = scan_repository(root)
            self.assertTrue(scan["capabilities"]["mutable_authority_context"]["suggested"])
            self.assertFalse(scan["capabilities"]["durable_work"]["suggested"])


class HistoricalEvidenceTest(unittest.TestCase):
    def receipt(self):
        return json.loads((ROOT / "evals/results/0.4.0-directional.json").read_text())

    def test_old_receipt_uses_recorded_corpus_not_current_routes(self):
        errors = []
        validate_eval_receipt(self.receipt(), {}, ["new-case"], errors, label="historical")
        self.assertEqual(errors, [])

    def test_old_receipt_cannot_be_relabelled_or_its_corpus_changed(self):
        for mutation in ("version", "digest"):
            with self.subTest(mutation=mutation):
                receipt = self.receipt()
                if mutation == "version":
                    receipt["harness_policy_version"] = "0.5.0"
                else:
                    receipt["corpus"]["cases_sha256"] = "0" * 64
                errors = []
                validate_eval_receipt(receipt, {}, [], errors, label="historical")
                self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
