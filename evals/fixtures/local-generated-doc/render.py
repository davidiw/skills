from pathlib import Path


def render():
    source = Path(__file__).with_name("source.txt")
    output = source.with_name("summary.md")
    return "# Summary\n\n" + source.read_text()


if __name__ == "__main__":
    import sys
    output = Path(__file__).with_name("summary.md")
    if "--check" in sys.argv:
        raise SystemExit(0 if output.read_text() == render() else 1)
    output.write_text(render())
