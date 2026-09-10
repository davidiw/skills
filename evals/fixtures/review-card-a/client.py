import html,json
def render(wire):
    card=json.loads(wire)
    details="" if card["preview"] is None else json.dumps(card["preview"],sort_keys=True)
    return "<section>"+html.escape(card["summary"])+"<pre>"+html.escape(details)+"</pre><button>Apply</button></section>"
