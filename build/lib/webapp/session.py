from paste.session import make_session_middleware

from webapp.app import *
from webapp.check import Check, environ_has

Request.session = property(lambda self: self.environ['paste.session.factory']())

def session_has(*args, **kwargs):
    """
    Check for the presense and, optionally, value of a session variable.

    If value is a callable it will be passed (app, var, value), otherwise
    it will be compared literally.
    """
    if len(args) > 1 or len(kwargs) > 1 or (len(args) and len(kwargs)) or (not len(args) and not len(kwargs)):
        raise ValueError("Must provide one and only one session variable to test. Consider using session_has_any or session_has_all.")
    elif len(args):
        var = args[0]
        return Check(lambda app: var in app.request.session)
    else:
        var, value = kwargs.items()[0]
        return Check(lambda app: app.request.session.get(var) == value)

def environ_has_any(*args, **kwargs):
    return Check(lambda app: any(arg in app.request.session for arg in args) or any(app.request.session.get(key) == value for (key, value) in kwargs.iteritems()))

def session_has_all(*args, **kwargs):
    return Check(lambda app: all(arg in app.request.session for arg in args) and all(app.request.session.get(key) == value for (key, value) in kwargs.iteritems()))

class Sessioned(object):
    def __middleware_factory__(self, app):
        return super(Sessioned, self).__middleware_factory__(make_session_middleware(app, {}))
 
