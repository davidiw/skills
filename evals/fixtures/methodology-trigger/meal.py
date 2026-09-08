class LookupUnavailable(Exception): pass
def enrich(lookup):
    try: return lookup()
    except LookupUnavailable: return "estimate"
