"""Evaluator-only reference; never copied into the agent-visible fixture."""
from job_store import Lease, transaction


def claim(db, worker, now, duration):
    with transaction(db):
        row = db.execute("""SELECT * FROM jobs WHERE state='pending'
            OR (state='running' AND lease_until<=?) ORDER BY job_id LIMIT 1""", (now,)).fetchone()
        if row is None:
            return None
        generation = row['generation'] + 1
        deadline = now + duration
        db.execute("UPDATE jobs SET state='running',worker=?,generation=?,lease_until=? WHERE job_id=?",
                   (worker, generation, deadline, row['job_id']))
        return Lease(row['job_id'], worker, generation, deadline)


def finish(db, lease, output, now):
    return db.execute("""UPDATE jobs SET state='done',result=? WHERE job_id=?
        AND state='running' AND worker=? AND generation=? AND lease_until>?""",
        (output, lease.job_id, lease.worker, lease.generation, now)).rowcount == 1
