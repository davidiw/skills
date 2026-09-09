from guard import accept

def publish(original, proposal, labels):
    if not accept(original, proposal, labels):
        raise ValueError("display correction refused")
    return proposal

