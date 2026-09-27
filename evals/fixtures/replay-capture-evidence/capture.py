from hashlib import sha256


def digest(value):
    return sha256(repr(value).encode()).hexdigest()


def capture(pose, features, events, media, preprocessing, producer, build, model,
            config, rubric, label, rep_count, adjudication):
    return {
        "replay_hash": digest((digest(pose), digest(features), digest(events))),
        "manifest": {
            "media": media,
            "preprocessing": preprocessing,
            "producer": producer,
            "build": build,
            "model": model,
            "config": config,
            "rubric": rubric,
            "label_revision": {
                "revision": 1,
                "label": label,
                "rep_count": rep_count,
                "adjudication": adjudication,
            },
        },
    }


def revise_label(record, label, rep_count, adjudication):
    revision = record["manifest"]["label_revision"]
    record["manifest"]["label_revision"] = {
        "revision": revision["revision"] + 1,
        "label": label,
        "rep_count": rep_count,
        "adjudication": adjudication,
    }


def scoring_baseline(record):
    label = record["manifest"]["label_revision"]
    return label["rep_count"], label["adjudication"]


def verify(record, pose, features, events):
    return record["replay_hash"] == digest((digest(pose), digest(features), digest(events)))
