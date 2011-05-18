#!/usr/bin/env python

from webapp.util import *
from webapp.check import *
from webapp.app import *
from webapp.session import *
from webapp.authn import *
from webapp.authz import *

if __name__ == '__main__':
    class TestApp(Sessioned, WebApplication):
        @handles()
        @check(session_has('read_toc'), otherwise=redirect('/toc'))
        def default(self):
            return Response('You read the terms and conditions!', content_type='text/html')
        
        @handles('/toc')
        def toc(self):
            self.request.session['read_toc'] = True
            return Response('Terms and conditions... <a href="/">Continue</a>', content_type='text/html')

    app = TestApp()
    
    cookie = ''
    for location in ['/', '/toc', '/']:
        response = Request.blank(location, headers=[('Cookie', cookie)]).get_response(app)
        if 'set-cookie' in response.headers:
            cookie = response.headers['set-cookie'].split(';', 2)[0]
        print response
