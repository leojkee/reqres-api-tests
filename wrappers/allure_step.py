import inspect
from functools import wraps

import allure

from utils.masking import get_sensitive_test_params, mask_value


def step(title=None):
    def decorator(func):
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            step_title = title if title else func.__name__.replace("_", " ").title()
            sensitive = get_sensitive_test_params()

            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            params = {}
            for name, value in bound.arguments.items():
                if name in ("self", "api"):
                    continue
                if name.lower() in sensitive:
                    params[name] = mask_value(str(value))
                else:
                    params[name] = str(value)

            with allure.step(step_title):
                if params:
                    allure.attach(
                        "\n".join(f"{k}: {v}" for k, v in params.items()),
                        name="Parameters",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                return func(*args, **kwargs)

        return wrapper

    if callable(title):
        func, title = title, None
        return decorator(func)
    return decorator
