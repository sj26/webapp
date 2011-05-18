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

def is_authenticated():
    return Check(lambda app: app.__authentictated__())

def is_anonymous():
    return Check(lambda app: not app.__authentictated__())

def is_user(user):
    return Check(lambda app: app.__is_user__(user))

def is_user_in(*users):
    return is_user(users)

def in_group(group):
    """
    Checks that the user is in a certain group.
    """
    return Check(lambda app: app.__in_group__(group))

def in_any_group(*groups):
    """
    Check that the user is at least one of the specified groups.
    """
    return Check(lambda app: any(app.__in_group__(group) for group in groups))

def in_all_groups(*groups):
    """
    Check that the user is in all specified groups.
    """
    return Check(lambda app: all(app.__in_group__(group) for group in groups))

class Authenticating(object):
    def __authenticated__(self):
        self.request is not None and self.request.remote_user is not None
    
    def __is_user__(self, user):
        remote_user = self.request.remote_user
        if isiterable(user):
            return any(u == remote_user for u in user)
        else:
            return user == remote_user
            
    def __authenticate__(self, username, password):
        raise NotImplemented()

    def __groups__(self, username):
        raise NotImplemented()

    def __in_group__(self, username, group):
        raise NotImplemented()
