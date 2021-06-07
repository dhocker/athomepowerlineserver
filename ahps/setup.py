# coding: utf-8
#
# AtHomeServer API
# Copyright ©  2019, 2020 Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#
# To build distribution:
# python setup.py sdist
#
# To install distribution in current venv:
#   workon venv
#   python setup.py install
#

import os

from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='ahps_api',
    version='2021.0.0',
    description='AtHomeServer API module',
    long_description=(read('Readme.md')),
    url='www.github.com/dhocker/athomepowerlineserver',
    license='GPLv3. See LICENSE file.',
    author='Dave Hocker',
    author_email='AtHomeX10@gmail.com',
    py_modules=["ahps_api"],
    include_package_data=True,
    packages=[],
    install_requires=[]
)