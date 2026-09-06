def download(request, storage):
    destination = storage.root / request.query["name"]
    return destination.read_bytes()
