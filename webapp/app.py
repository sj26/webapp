# This file is part of WebApp.
# 
# WebApp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# WebApp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with WebApp.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Samuel Cochran <sj26@sj26.com>'
__version__ = '0.1'
__copyright__ = 'Copyright 2008 Samuel Cochran'

import threading

import webob, webob.exc

from util import *
from handler import RequestHandler


class WebApplication(RequestHandler):
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
        self.__local = threading.local()
        # Special case for initialisation thread
        self.__local.request = None
        self.__middleware = self.__middleware_factory__(self.__app__)

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
        with middleware, just be sure to call super(..).__middleware_factory__(app).
        """
        return app

    def __call__(self, environ, start_response):
        return self.__middleware(environ, start_response)

    def __app__(self, environ, start_response):
        environ['x-wsgi.start_response'] = start_response
        self.__local__.request = Request(environ)
        return self.__handle__(self.__local__.request)
