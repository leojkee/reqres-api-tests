import threading

_local = threading.local()


def set_test_id(test_id: str) -> None:
    _local.test_id = test_id


def get_test_id() -> str:
    return getattr(_local, "test_id", "unknown")


def clear_test_id() -> None:
    _local.test_id = None
