import atexit

from requests import Session

import centmo

_session = None


def _save_cookies():
    centmo.cookies.save(session().cookies)


def session():
    global _session
    if not _session:
        _session = Session()
        _session.cookies = centmo.cookies.load()
        atexit.register(_save_cookies)
    return _session
