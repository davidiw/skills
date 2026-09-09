def apply(total, code):
    if code.upper() == "SAVE10":
        return round(total * 0.9, 2)
    return total
