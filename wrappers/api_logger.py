"""API logger decorator — logs request/response as HTML Allure attachments."""
import json
import sys
import time
from functools import wraps

import allure

from utils.logger import get_logger
from utils.masking import mask_sensitive, get_sensitive_test_params
from utils.test_context import get_test_id

logger = get_logger("API_LOG")


def _mask_body(body: str | bytes | None) -> str:
    if not body:
        return ""
    try:
        text = body.decode() if isinstance(body, bytes) else body
        data = json.loads(text)
        for key in get_sensitive_test_params():
            if key in data:
                data[key] = "***"
        return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception:
        return str(body)


def _format_request_html(req) -> str:
    body = _mask_body(req.body)
    headers = "\n".join(
        f"  {k}: {'***' if k.lower() in get_sensitive_test_params() else v}"
        for k, v in (req.headers or {}).items()
    )
    return (
        f'<pre style="background:#1e1e1e;color:#d4d4d4;padding:12px;border-radius:4px">'
        f"<b>-> {req.method} {req.url}</b>\n\n"
        f"<b>Headers:</b>\n{headers}\n\n"
        f"<b>Body:</b>\n{body}"
        f"</pre>"
    )


def _format_response_html(resp, duration_ms: float) -> str:
    color = "#4ec9b0" if resp.status_code < 400 else "#f44747"
    try:
        body = json.dumps(resp.json(), ensure_ascii=False, indent=2)
    except Exception:
        body = resp.text
    return (
        f'<pre style="background:#1e1e1e;color:#d4d4d4;padding:12px;border-radius:4px">'
        f'<b style="color:{color}">< {resp.status_code} {resp.reason}  ({duration_ms:.0f}ms)</b>\n\n'
        f"<b>Body:</b>\n{body}"
        f"</pre>"
    )


def api_logger(step_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with allure.step(step_name):
                start = time.time()
                try:
                    response = func(*args, **kwargs)
                except Exception as e:
                    masked = mask_sensitive(str(e))
                    test_id = get_test_id()
                    logger.error(f"[{test_id}] [API] {step_name} - Exception: {masked}")
                    allure.attach(
                        _format_response_html.__doc__ or str(e),
                        name="Exception",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    raise

                duration_ms = (time.time() - start) * 1000
                test_id = get_test_id()

                sys.__stdout__.write(
                    f"\n[{test_id}] [API] {step_name} -> {response.status_code} ({duration_ms:.0f}ms)\n"
                )

                allure.attach(
                    _format_request_html(response.request),
                    name="Request",
                    attachment_type=allure.attachment_type.HTML,
                )
                allure.attach(
                    _format_response_html(response, duration_ms),
                    name=f"Response {response.status_code}",
                    attachment_type=allure.attachment_type.HTML,
                )
                return response

        return wrapper
    return decorator
