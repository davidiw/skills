# Sync fixture
The existing queue owns durable admission, retry/backoff, and account fencing.
Connectivity is a wake signal only. Preserve provider and server contracts;
use Queue.admit_unique instead of adding a scheduler, auth check, or migration.
Run python3 -m unittest discover -s tests. This directory is the complete repository.
