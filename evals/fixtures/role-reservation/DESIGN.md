# Reservation fixture contract

`inventory.py` owns SQLite storage and `client.py` exposes availability and a
display label. Standard library only; no HTTP service. `connect(path)` returns a
caller-closed SQLite connection with `stock(sku TEXT PRIMARY KEY, quantity INTEGER
NOT NULL)` and `operations(operation_id TEXT PRIMARY KEY, sku TEXT NOT NULL,
quantity INTEGER NOT NULL, status TEXT NOT NULL)`. `initialize(db, sku, quantity)`
seeds a new SKU for setup only.

`reserve(db, operation_id, sku, quantity, *, before_commit=None)` accepts a
nonempty string ID, an existing SKU, and positive integer quantity (`bool` is
invalid). Invalid inputs raise `ValueError` without mutation. IDs are database
global. It returns exactly `{'operation_id': id, 'sku': sku, 'quantity': quantity,
'status': 'reserved' or 'insufficient'}`. Its first execution persists that
result; a same-ID, same-argument retry returns it without another decrement;
different arguments raise `ValueError` without mutation. Distinct connections
cannot overdraw stock, and simultaneous reservations resolve as business results.
An insufficient result does not decrement stock. `before_commit` runs only after
new-operation changes and before commit; an exception rolls back stock and the
operation. It is a local test seam, not crash recovery or an external atomicity
claim.

`client.availability(db, sku)` returns exactly `{'sku': sku, 'available':
current_quantity}` from committed stock. Unknown SKUs raise `ValueError`. No
schema or API changes, migration, broker, or external effect.
