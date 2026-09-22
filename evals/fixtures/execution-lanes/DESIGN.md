# Lane admission contract

`lanes.py` models a bounded evaluation coordinator. A lane failure is an
observed admission stop: do not begin queued lanes after it. Do retain results
from lanes that were already running, because their evidence can diagnose the
failure. This is not a cancellation claim for a running process.
