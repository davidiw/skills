def parse_records(stream):
    return {"records": [line.strip() for line in stream if line.strip()]}
