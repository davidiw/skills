def render_report(result):
    return "\n".join([
        "# Import report",
        "Accepted rows: " + ", ".join(result["accepted"]),
    ])
