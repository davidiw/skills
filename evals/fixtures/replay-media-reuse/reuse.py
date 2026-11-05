from pathlib import Path
from capture import verify


def replay(reference, record, pose, features, events):
    media_bytes = Path(record["media_path"]).read_bytes()
    if not verify(reference, record, pose, features, events, media_bytes):
        raise ValueError("replay evidence mismatch")
    return Path(record["media_path"]).read_bytes()
