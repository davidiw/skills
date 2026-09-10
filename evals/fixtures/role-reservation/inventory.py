import sqlite3


def connect(path):
    db = sqlite3.connect(path, timeout=5)
    db.execute("CREATE TABLE IF NOT EXISTS stock (sku TEXT PRIMARY KEY, quantity INTEGER NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS operations (operation_id TEXT PRIMARY KEY, sku TEXT NOT NULL, quantity INTEGER NOT NULL, status TEXT NOT NULL)")
    db.commit()
    return db


def initialize(db, sku, quantity):
    db.execute("INSERT INTO stock (sku, quantity) VALUES (?, ?)", (sku, quantity))
    db.commit()


def reserve(db, operation_id, sku, quantity, *, before_commit=None):
    if (not isinstance(operation_id, str) or not operation_id or isinstance(quantity, bool)
            or not isinstance(quantity, int) or quantity <= 0):
        raise ValueError("invalid reservation")
    row = db.execute("SELECT quantity FROM stock WHERE sku = ?", (sku,)).fetchone()
    if row is None:
        raise ValueError("unknown sku")
    status = "reserved" if row[0] >= quantity else "insufficient"
    if status == "reserved":
        db.execute("UPDATE stock SET quantity = quantity - ? WHERE sku = ?", (quantity, sku))
    db.commit()
    if before_commit is not None:
        before_commit()
    return {"operation_id": operation_id, "sku": sku, "quantity": quantity, "status": status}
