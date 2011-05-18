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

import webob, webob.exc

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
    def _decorator(fn):
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
    return _decorator

def redirect(path):
    def _internal(app):
        return webob.exc.HTTPSeeOther(location=app.request.application_url + path)
    return _internal

class Request(webob.Request):
    pass

class Response(webob.Response):
    pass

class RequestHandler(object):
    request = property(lambda self: self.__local__.request, doc="The Request currently being served by this WebApplication.")
    
    def __init__(self, app):
        self.app = app
        
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
        self.request.environ['x-wsgi.start_response'](response.status, response.headerlist)
        return response.app_iter
