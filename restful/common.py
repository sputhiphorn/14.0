"""Common methods"""
import logging
import werkzeug.wrappers

_logger = logging.getLogger(__name__)
import json


def valid_response(data, status=200):
    """Valid Response
    This will be return when the http request was successfully processed."""
    data = {"count": len(data), "data": data}
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
        response=json.dumps(data))

def invalid_response(title, message=None, status=401):
     return werkzeug.wrappers.Response(
                    status=status,
                    content_type="application/json; charset=utf-8",
                    headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
                    response=json.dumps({"title": title,
                                        "message": str(message) if str(message) else "wrong arguments (missing validation)"
                                         }))

def extract_arguments(payloads, offset=0, limit=0, order=None):
    """."""
    fields, domain, payload = [], [], {}
    # data = str(payloads)[2:-2]
    # try:
    #     payload = json.loads(data)
    # except JSONDecodeError as e:
    #     _logger.error(e)
    if payloads.get("domain"):
        for _domain in payloads.get("domain"):
            l, o, r = _domain
            if o == "': '":
                o = "="
            elif o == "!': '":
                o = "!="
            domain.append(tuple([l, o, r]))
    if payloads.get("fields"):
        fields += payloads.get("fields")
    if payloads.get("offset"):
        offset = int(payloads["offset"])
    if payloads.get("limit"):
        limit = int(payloads.get("limit"))
    if payloads.get("order"):
        order = payloads.get("order")
    return [domain, fields, offset, limit, order]
