def authenticate(request, tokens):
    token = request.cookies.get("product_session") or request.query.get("handoff")
    claims = tokens.verify_signature_and_expiry(token)
    return claims["account"]


def provider_return(account, tokens):
    return tokens.issue(account=account, audience="provider-browser",
                        purpose="complete-link", expires_in=60)
