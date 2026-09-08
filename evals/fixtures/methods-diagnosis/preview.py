def preview(amounts):
    count = sum(1 for value in amounts)
    total = sum(int(value) for value in amounts)
    return {"count": count, "total": total}
