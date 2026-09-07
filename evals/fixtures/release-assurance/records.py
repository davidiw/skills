def erase(account, database):
    database.readings.pop(account, None)
    database.active.discard(account)


def activity_report(account, database):
    return database.activity.get(account, [])


def flush_activity(batch, database):
    for account, event in batch:
        database.activity.setdefault(account, []).append(event)
