import json
from producer import proposal
def wire(op,label,args):
    return json.dumps(proposal(op,label,args))
