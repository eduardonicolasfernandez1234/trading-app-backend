import threading

_user = threading.local()


def get_current_user():
    return getattr(_user, "value", None)
