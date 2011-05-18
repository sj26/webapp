
import threading

import webob, webob.exc

from util import *

def handles(*tests, **kwargs):
    """
    Marks a method as handling certain requests.

    Most commonly used with a string to match against the request path, 
    i.e. @handles('/mypath')

    Options:
        default (False): Handle requests when no other method can.
    """
    if len(tests) < 1:
        tests = [None]
    options = {'default': False}
    options.update(kwargs)
    def _internal(fn):
        def _handles(self):
            for test in tests:
                if test is None:
                    if self.request.path_info.rstrip('/') == '':
                        return True
                elif hasattr(test, 'match'):
                    match = test.match(self.request.path_info)
                    return (match and (match.groups() or True)) or False
                elif callable(test):
                    if test(self):
                        return True
                elif isinstance(test, (str, unicode)):
                    if self.request.path_info == test:
                        return True
                else:
                    raise ValueError("Unknown handler test: %r" % test)
            return False
        fn.handles = _handles
        fn.handles_default = options['default']
        return fn
    return _internal

def redirect(path):
    def _internal(app):
        return webob.exc.HTTPSeeOther(location=app.request.application_url + path)
    return _internal

class Request(webob.Request):
    pass
    
class Response(webob.Response):
    pass

class WebApplication(object):
    """
    An extensible WSGI application class to make things easy.

    Subclass this to create a new WSGI application, the methods of which handle
    definable paths.

    Mixing in additional classes will give enhanced functionality, i.e.
    Sessioning adds sessions to requests, Authorisation allows maintaining
    user authorisation.

    A simple application:
    class MyApp(WebApplication, Sessioning):
        def default(self):
            self.request.session.get('visits', 0) += 1
            return Response('You have visited %d times!' % self.request.session['visits'])

    When there is only one method it is presumed that it should serve the base
    request ('/') and nothing else. You could decorate the method with
        @handles(default=True)
    to make it handle all sub-requests as well.

    To illustrate path handling:
    class MyApp2(WebApplication):
        @handles('/')
        def default(self):
            return Response('Look <a href="%s">over here</a>.' % (self.request.application_url + '/here',))

        @handles('/here'):
        def here(self):
            return Response('Hi!')
    """

    def __init__(self):
        self.__local__ = threading.local()
        # Special case for initialisation thread
        self.__local__.request = None
        self.__middleware__ = self.__middleware_factory__(self.__app__)

        # Find all handlers in the current class
        self.__handlers__ = [getattr(self, method) for method in dir(self) if callable(getattr(self, method)) and hasattr(getattr(self, method), 'handles') and callable(getattr(self, method).handles)]

        # Find the default handler, if there is one
        self.__handler_default__ = [handler for handler in self.__handlers__ if handler.handles_default]
        if len(self.__handler_default__) > 1:
            raise ValueError("Multiple default handlers specified")
        elif len(self.__handler_default__) > 0:
            self.__handler_default__ = self.__handler_default__[0]
        else:
            self.__handler_default__ = None

    def __middleware_factory__(self, app):
        """
        Fallback middleware function to return the app.

        Sub-classes can override this method to wrap the initial WSGI requests
        with middleware, just be sure to call super().
        """
        return app

    def __call__(self, environ, start_response):
        return self.__middleware__(environ, start_response)

    def __app__(self, environ, start_response):
        environ['wsgi.start_response'] = start_response
        self.__local__.request = Request(environ)
        return self.__handle__(self.__local__.request)

    def __handle__(self, request):
        response = None
        for handler in self.__handlers__:
            result = handler.handles(self)
            if result:
                result = isiterable(result) and result or []
                response = handler(*result)
        if response is None:
            if self.__handler_default__ is not None:
                response = self.__handler_default__()
            else:
                response = webob.exc.HTTPNotFound()
        if isinstance(response, basestring):
            response = Response(response)
        self.request.environ['wsgi.start_response'](response.status, response.headerlist)
        return response.app_iter

    request = property(lambda self: self.__local__.request, doc="The Request currently being served by this WebApplication.")
