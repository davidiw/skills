import re
from renderer import TOKEN

def accept(before, after, labels):
    def anchors(text):
        return sorted(re.findall(r"\d+(?:\.\d+)?", TOKEN.sub("", text)))
    return anchors(before) == anchors(after)

def fields(tool):
    return set(tool.get("input_schema", {}).get("properties", {}))
