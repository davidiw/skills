import json
def proposal(op, label, args):
    command = "Update " + json.dumps(label) + "."
    return {"operation":op,"summary":command,"arguments":args,"preview":args if op=="plan_replace" else None}
