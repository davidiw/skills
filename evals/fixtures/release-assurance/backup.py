def restore(snapshot, database):
    database.readings.update(snapshot["readings"])
    database.active.update(snapshot["active"])
