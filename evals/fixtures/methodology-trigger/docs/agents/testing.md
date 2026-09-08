# Shared failure testing policy
The lookup adapter classifies known provider/tool failures as LookupUnavailable. Contract tests cover fallback for that type and propagation for unexpected errors. This rule applies to all enrichment callers. The canonical check is `python -m unittest discover -s tests`.
