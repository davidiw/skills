import copy
from gate import admitted
def prepare(mutation, command, page):
    if not admitted(mutation, command, page):
        raise ValueError("not prepared")
    return {"summary":command,"arguments":copy.deepcopy(mutation)}
