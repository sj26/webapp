#!/usr/bin/env python

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

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name="WebApp",
    version=__version__,
    author_email=__author__,
    description="An object-oriented web framework making rapid web-application development easy.",
    license="LGPL",
    
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    
    test_suite='tests',

    install_requires=['Paste>=1.0', 'PasteDeploy', 'WebOb'],
)


