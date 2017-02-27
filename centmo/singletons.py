import atexit

from requests import Session

import spammo

_session = None


def _save_cookies():
    spammo.cookies.save(session().cookies)


def session():
    global _session
    if not _session:
        _session = Session()
        _session.cookies = spammo.cookies.load()
        atexit.register(_save_cookies)
    return _session
