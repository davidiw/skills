import re
TOKEN = re.compile(r"\[\[ref:([^]]+)\]\]")
def render(text, labels):
    return TOKEN.sub(lambda m: labels[m.group(1)], text)
