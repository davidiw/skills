class Queue:
    def __init__(self):
        self.pending = set()
        self.admissions = []
        self.retry_after = {}

    def admit_unique(self, account, target):
        key = (account, target)
        if key not in self.pending:
            self.pending.add(key)
            self.admissions.append(key)


class Coordinator:
    def __init__(self, queue, account):
        self.queue, self.account = queue, account

    def scheduled_wake(self):
        for target in ("provider", "server"):
            self.queue.admit_unique(self.account, target)
