def import_rows(rows):
    accepted, rejected = [], []
    for row in rows:
        value = row.strip() if isinstance(row, str) else None
        if value:
            accepted.append(value)
        else:
            rejected.append(row)
    return {"accepted": accepted, "rejected": rejected}
