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
    if (
        not isinstance(operation_id, str)
        or not operation_id
        or not isinstance(sku, str)
        or not sku
        or isinstance(quantity, bool)
        or not isinstance(quantity, int)
        or quantity <= 0
        or quantity > 2**63 - 1
    ):
        raise ValueError("invalid reservation")

    db.execute("BEGIN IMMEDIATE")
    try:
        operation = db.execute(
            "SELECT sku, quantity, status FROM operations WHERE operation_id = ?",
            (operation_id,),
        ).fetchone()
        if operation is not None:
            if operation[:2] != (sku, quantity):
                raise ValueError("operation id does not match reservation")
            result = {
                "operation_id": operation_id,
                "sku": operation[0],
                "quantity": operation[1],
                "status": operation[2],
            }
            db.commit()
            return result

        row = db.execute(
            "SELECT quantity FROM stock WHERE sku = ?", (sku,)
        ).fetchone()
        if row is None:
            raise ValueError("unknown sku")

        status = "reserved" if row[0] >= quantity else "insufficient"
        if status == "reserved":
            db.execute(
                "UPDATE stock SET quantity = quantity - ? WHERE sku = ?",
                (quantity, sku),
            )
        db.execute(
            "INSERT INTO operations (operation_id, sku, quantity, status) "
            "VALUES (?, ?, ?, ?)",
            (operation_id, sku, quantity, status),
        )
        if before_commit is not None:
            before_commit()
        db.commit()
        return {
            "operation_id": operation_id,
            "sku": sku,
            "quantity": quantity,
            "status": status,
        }
    except BaseException:
        if db.in_transaction:
            db.rollback()
        raise
