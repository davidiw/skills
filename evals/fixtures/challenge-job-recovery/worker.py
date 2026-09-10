import job_store

def take(db, name, now, duration):
    return job_store.claim(db,name,now,duration)

def deliver(db, lease, rendered, now):
    return job_store.finish(db,lease,rendered,now)
