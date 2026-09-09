from renderer import render

def accept(before, after, labels):
    try:
        return after == render(before, labels)
    except KeyError:
        return False

def fields(tool):
    return set().union(*(set(tool.get(part, {}).get("properties", {}))
                         for part in ("input_schema", "output_schema")))
