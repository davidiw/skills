from legacy import support_export
from records import erase, activity_report

ROUTES = {
    "/support/export": {"handler": support_export, "auth": "member"},
    "/account/erase": {"handler": erase, "auth": "member"},
    "/activity": {"handler": activity_report, "auth": "member"},
}
