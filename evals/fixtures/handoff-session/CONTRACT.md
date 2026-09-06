# Browser credential contract
The product API calls authenticate for every product request. Handoff tokens are
signed and short-lived; the provider browser receives them to finish one account
link. They must not authorize normal product endpoints or establish a browser's
ordinary product session. The token service exposes audience, purpose, account,
expiry, and a single-use nonce. Existing product sessions have audience=product.
