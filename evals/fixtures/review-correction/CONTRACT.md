# Export authorization
The trusted request principal is `request.principal`; query parameters are untrusted.
An export may return only that principal's records while their grant is active.
The route and grant lookup are in export.py. Corrections to that route require
independent review before integration. Follow-up review covers corrections and
directly affected seams; unrelated admin tooling is outside this change review.
