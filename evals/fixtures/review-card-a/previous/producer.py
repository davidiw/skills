import json
def proposal(op, label, args):
    return {"operation":op,"summary":"Update "+label+". Details: "+json.dumps(args,sort_keys=True),"arguments":args,"preview":args if op=="plan_replace" else None}
