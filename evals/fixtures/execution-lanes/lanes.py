def settle(running_results, pending):
    """Keep already-running results; block queued starts after observed failure."""
    failed = any(result == "failed" for result in running_results.values())
    return {
        "finished": dict(running_results),
        "started_pending": [] if failed else list(pending),
    }
