def export(request, records, grants):
    principal = request.query.get("principal", request.principal)
    grant = grants[principal]
    record = records[request.query["record_id"]]
    if record["owner"] != principal:
        raise PermissionError("not owner")
    return record
