import sqlite3
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass(frozen=True)
class Lease:
    job_id: str
    worker: str
    generation: int
    lease_until: float

def connect(path):
    db = sqlite3.connect(path, isolation_level=None, timeout=5)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS jobs (
        job_id TEXT PRIMARY KEY, input TEXT NOT NULL,
        state TEXT NOT NULL DEFAULT 'pending', worker TEXT,
        generation INTEGER NOT NULL DEFAULT 0, lease_until REAL,
        result TEXT)""")
    return db

@contextmanager
def transaction(db):
    db.execute("BEGIN IMMEDIATE")
    try:
        yield
        db.execute("COMMIT")
    except BaseException:
        db.execute("ROLLBACK")
        raise

def enqueue(db, job_id, text):
    db.execute("INSERT INTO jobs(job_id,input) VALUES (?,?)", (job_id,text))

def claim(db, worker, now, duration):
    with transaction(db):
        row = db.execute("SELECT * FROM jobs WHERE state='pending' ORDER BY job_id LIMIT 1").fetchone()
        if row is None:
            return None
        generation = row['generation'] + 1
        deadline = now + duration
        db.execute("UPDATE jobs SET state='running',worker=?,generation=?,lease_until=? WHERE job_id=?",
                   (worker,generation,deadline,row['job_id']))
        return Lease(row['job_id'],worker,generation,deadline)

def finish(db, lease, output, now):
    changed = db.execute("UPDATE jobs SET state='done',result=? WHERE job_id=? AND state='running' AND worker=?",
                         (output,lease.job_id,lease.worker))
    return changed.rowcount == 1

def inspect(db, job_id):
    row = db.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
    return None if row is None else dict(row)
