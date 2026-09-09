import json

def target_id(mutation):
    if mutation["op"] == "amend_path":
        return mutation["path"]["id"]
    if mutation["op"] == "amend_body":
        return mutation["body"]["target_id"]
    raise ValueError("unsupported operation")

def admitted(mutation, command, page):
    target = target_id(mutation)
    rows = page["rows"]
    row = next((x for x in rows if x["id"] == target), None)
    if row is None:
        return False
    name = row["name"]
    unique = sum(x["name"] == name for x in rows) == 1
    return unique and name in command
