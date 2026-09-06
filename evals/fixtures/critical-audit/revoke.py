def revoke(account, database, audit):
    with database.transaction() as transaction:
        audit.append(transaction, account, "revoked")
        transaction.revoke_credentials(account)
    return "revoked"
