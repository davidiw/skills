def support_export(request, database):
    # Retained legacy support endpoint.
    return database.all_accounts()
