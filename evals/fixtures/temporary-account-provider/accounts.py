from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    account_id: str
    temporary: bool = False
    expires_at: int | None = None


def create_temporary(account_id: str, now: int) -> Account:
    return Account(account_id, temporary=True)
