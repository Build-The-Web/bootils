# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=invalid-name, redefined-outer-name, too-few-public-methods
""" Test py:mod:`bootils.util.jvm`.
"""
# Copyright ©  2015 1&1 Group <btw-users@googlegroups.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, unicode_literals, print_function

import os

import pytest

from bootils.util import jvm


def test_invalid_java_home_passed():
    with pytest.raises(EnvironmentError):
        jvm.java_home('/bogus/path/that/fails')


def test_invalid_java_home_envvar():
    with pytest.raises(EnvironmentError):
        saved_home = os.environ.get('JAVA_HOME')
        try:
            os.environ['JAVA_HOME'] = '/bogus/path/that/fails'
            jvm.java_home()
        finally:
            if saved_home:
                os.environ['JAVA_HOME'] = saved_home
            else:
                del os.environ['JAVA_HOME']


def test_no_default_java_home():
    with pytest.raises(EnvironmentError):
        saved_home = os.environ.get('JAVA_HOME')
        saved_defaults = jvm.JAVA_HOME_DEFAULTS
        try:
            if saved_home:
                del os.environ['JAVA_HOME']
            jvm.JAVA_HOME_DEFAULTS = []
            jvm.java_home()
        finally:
            jvm.JAVA_HOME_DEFAULTS = saved_defaults
            if saved_home:
                os.environ['JAVA_HOME'] = saved_home


def test_java_version_info():
    try:
        java_home_path = jvm.java_home()
    except EnvironmentError:
        pass  # skip test if no JVM is available
    else:
        errors = []
        full_version, version_details = jvm.version_info(java_home_path, log=errors.append)
        assert not errors, "Querying JVM version had problems: {!r}".format(errors)
        assert any(full_version.startswith(i) for i in ('1.7.', '1.8.', '1.9.'))
