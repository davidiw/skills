class Dashboard:
    def __init__(self, login_enabled):
        self.login_enabled = login_enabled

    def summary(self, signed_in):
        if not self.login_enabled or not signed_in:
            return "sign in"
        return "summary"


def compose(config):
    return Dashboard(login_enabled=False)
