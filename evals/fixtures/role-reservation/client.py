LABEL = "Availability"


def availability(db, sku):
    row = db.execute("SELECT quantity FROM stock WHERE sku = ?", (sku,)).fetchone()
    if row is None:
        raise ValueError("unknown sku")
    return {"sku": sku, "available": row[0]}
