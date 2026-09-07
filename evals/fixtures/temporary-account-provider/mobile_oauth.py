class UnsupportedAccount(ValueError):
    pass


class MobileOAuth:
    def __init__(self, permanent_registry):
        self.permanent_registry = permanent_registry

    def begin(self, account, provider):
        if account.temporary or account.account_id not in self.permanent_registry:
            raise UnsupportedAccount("native callback requires a permanent registry subject")
        return {"callback": "native", "subject": account.account_id, "provider": provider}

    def complete(self, callback, grant):
        account_id = callback["subject"]
        self.permanent_registry[account_id]["grants"][callback["provider"]] = grant
