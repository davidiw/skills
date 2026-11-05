from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import json


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")
    return sha256(data).hexdigest()


def capture(pose, features, events, media_path, preprocessing, producer, build,
            model, config, rubric, label, rep_count, adjudication):
    media_bytes = Path(media_path).read_bytes()
    evidence = {
        "schema_version": 1,
        "pose_hash": digest(pose), "features_hash": digest(features),
        "events_hash": digest(events), "media_sha256": sha256(media_bytes).hexdigest(),
        "preprocessing": preprocessing, "producer": producer, "build": build,
        "model": model, "config": config, "rubric": rubric,
    }
    evidence = deepcopy(evidence)
    return {"reference": digest(evidence), "evidence": evidence,
            "media_path": str(media_path), "annotations": {"revision": 1,
            "label": label, "rep_count": rep_count, "adjudication": deepcopy(adjudication)}}


def revise(record, label, rep_count, adjudication):
    record["annotations"] = {"revision": record["annotations"]["revision"] + 1,
                             "label": label, "rep_count": rep_count,
                             "adjudication": deepcopy(adjudication)}


def verify(reference, record, pose, features, events, media_bytes):
    return reference == digest(record["evidence"])
