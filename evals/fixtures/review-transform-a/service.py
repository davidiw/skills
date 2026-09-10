from guard import accept, fields

def publish(original, proposal, labels):
    if not accept(original, proposal, labels):
        raise ValueError("display correction refused")
    return proposal

def display_fields(tool):
    return fields(tool)
