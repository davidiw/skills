import json
def proposal(op, label, args):
    command = "Update " + json.dumps(label) + "."
    summary = command
    if op == "dispatch_edit":
        details = dict(args)
        if "lines" in args:
            details["collection_action"] = "clear" if args["lines"] == [] else "replace"
        summary += " Details: " + json.dumps(details,sort_keys=True)
    return {"operation":op,"summary":summary,"arguments":args,"preview":args if op=="plan_replace" else None}
