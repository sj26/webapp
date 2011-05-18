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

from webapp.check import Check, environ_has

def has_permission(perm):
    return Check(lambda app: app.__authorized_to__(perm))

def has_any_permission(*perms):
    return Check(lambda app: any(app.__authorized_to__(perm) for perm in perms))

def has_all_permissions(*perms):
    return Check(lambda app: all(app.__authorized_to__(perm) for perm in perms))

class Authorizing(object):
    def __authorized_to__(self, permission):
        raise NotImplemented()

