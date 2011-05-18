from webob.exc import HTTPBadRequest
from webapp.app import Response

class Check(object):
    """
    Base for condition checks used in check().

    Pass a lambda function in the initialiser and it will be called with the
    application being checked as a parameter.

    Combine Check objects using binary operators (& [and]), | [or] and ~ [not]).
    """
    def __init__(self, check):
        self.__check__ = check
    def __call__(self, app):
        return self.__check__(app)
    def __and__(self, other):
        if not isinstance(other, Check):
            raise TypeError("Cannot combine Check object %r with non-Check object %r" % (self, other))
        return Check(lambda app: self(app) and other(app))
    def __or__(self, other):
        if not isinstance(other, Check):
            raise TypeError("Cannot combine Check object %r with non-Check object %r" % (self, other))
        return Check(lambda app: self(app) or other(app))
    def __invert__(self):
        return Check(lambda app: not self(app))

def environ_has(*args, **kwargs):
    """
    Check for the presense and, optionally, value of an environment variable.

    If value is a callable it will be passed (app, var, value), otherwise
    it will be compared literally.
    """
    if len(args) > 1 or len(kwargs) > 1 or (len(args) and len(kwargs)) or (not len(args) and not len(kwargs)):
        raise ValueError("Must provide one and only one environment variable to test. Consider using environ_has_any or environ_has_all.")
    elif len(args):
        var = args[0]
        return Check(lambda app: var in app.request.environ)
    else:
        var, value = kwargs.items()[0]
        return Check(lambda app: app.request.environ.get(var) == value)

def environ_has_any(*args, **kwargs):
    return Check(lambda app: any(arg in app.request.environ for arg in args) or any(app.request.environ.get(key) == value for (key, value) in kwargs.iteritems()))

def environ_has_all(*args, **kwargs):
    return Check(lambda app: all(arg in app.request.environ for arg in args) and all(app.request.environ.get(key) == value for (key, value) in kwargs.iteritems()))

def from_host(host):
    return environ_has(REMOTE_ADDR=host)

def from_any_host(*host):
    return environ_has(REMOTE_ADDR=hosts)

def check(*checks, **kw):
    """
    Checks a set of conditions.

    Used as a method decorator in a WebApplication to perform the method only
    if a set of conditions are first met.

    This can be useful to i.e. check a user is logged in and has permission
    to access the method before calling.

    Example:

    >>> class MyApp(WebApplication, Sessioned):
    ...   @handles()
    ...   @check(session_has('seen_toc'), otherwise=redirect('/toc'))
    ...   def default(self):
    ...     return Response('Front page.')
    ...   
    ...   @handles('/toc')
    ...   def toc(self):
    ...     self.session['seen_toc'] = True
    ...     return Respone('These are the terms and conditions... <a href="/">I agree</a>.')

    """
    for check in checks:
        if not isinstance(check, Check):
            raise TypeError("All parameters to check() should be of type Check: %r" % check)

    otherwise = kw.get('otherwise', lambda app: HTTPBadRequest())
    if isinstance(otherwise, Response):
        response = otherwise
        otherwise = lambda app: response

    def _fn(fn):
        def _internal(self, *a, **kw):
            for check in checks:
                if not check(self):
                    return otherwise(self)
            return fn(self, *a, **kw)
        return _internal
    return _fn

