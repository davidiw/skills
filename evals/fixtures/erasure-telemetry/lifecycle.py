class Store:
    def __init__(self):
        self.active = {"temporary"}
        self.readings = {"temporary": [72]}
        self.events = []
        self.pending = []

    def record_activity(self, account):
        self.pending.append((account, "health_read_completed"))

    def erase(self, account):
        self.active.discard(account)
        self.readings.pop(account, None)
        self.events = [event for event in self.events if event[0] != account]

    def flush(self):
        self.events.extend(self.pending)
        self.pending.clear()
