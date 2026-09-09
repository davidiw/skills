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
    matches = [x for x in rows if x["id"] == target]
    if len(matches) != 1:
        return False
    row = matches[0]
    labels = []
    if page.get("scope") == "all" and page.get("complete") is True and sum(x["name"] == row["name"] for x in rows) == 1:
        labels.append(row["name"])
    if row.get("slot_code"):
        labels.append(row["name"] + " / " + row["slot_code"])
    return any(command == "Update " + json.dumps(label) + "." for label in labels)
