"""Reference behavior for evaluator discrimination; not part of the trial fixture."""
import sqlite3
import time


def connect(path):
    db = sqlite3.connect(path, timeout=5)
    db.execute("PRAGMA busy_timeout = 5000")
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
    for attempt in range(20):
        try:
            db.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as error:
            db.rollback()
            if "locked" not in str(error).lower() or attempt == 19:
                raise
            time.sleep(0.01 * (attempt + 1))
            continue
        try:
            existing = db.execute("SELECT sku, quantity, status FROM operations WHERE operation_id = ?", (operation_id,)).fetchone()
            if existing:
                if existing[:2] != (sku, quantity):
                    raise ValueError("operation arguments differ")
                db.rollback()
                return {"operation_id": operation_id, "sku": sku, "quantity": quantity, "status": existing[2]}
            row = db.execute("SELECT quantity FROM stock WHERE sku = ?", (sku,)).fetchone()
            if row is None:
                raise ValueError("unknown sku")
            status = "reserved" if row[0] >= quantity else "insufficient"
            if status == "reserved":
                db.execute("UPDATE stock SET quantity = quantity - ? WHERE sku = ?", (quantity, sku))
            db.execute("INSERT INTO operations VALUES (?, ?, ?, ?)", (operation_id, sku, quantity, status))
            if before_commit is not None:
                before_commit()
            db.commit()
            return {"operation_id": operation_id, "sku": sku, "quantity": quantity, "status": status}
        except Exception:
            db.rollback()
            raise
