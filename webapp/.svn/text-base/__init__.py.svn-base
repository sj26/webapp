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

from webapp.util import *
from webapp.check import *
from webapp.handler import *
from webapp.app import *
from webapp.tracker import *
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
