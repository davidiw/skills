"""Parse the tiny CLI's input document into its report shape."""


def parse_report(document: dict[str, object]) -> dict[str, object]:
    name = document.get("name")
    if not isinstance(name, str) or not name:
        raise ValueError("name must be a non-empty string")
    return {"name": name}
