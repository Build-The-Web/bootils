# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=invalid-name, redefined-outer-name, too-few-public-methods
""" Test «some_module».
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

import pytest

from bootils import launcher


def test_signal_name_to_int():
    assert launcher.signal2int(1) == 1
    assert launcher.signal2int('1') == 1
    assert launcher.signal2int('pipe') == 13
    assert launcher.signal2int('PIPE') == 13
    assert launcher.signal2int('sigPIPE') == 13


def test_signal2int_with_bad_name():
    with pytest.raises(ValueError):
        launcher.signal2int('foobar')


def test_signal2int_with_bad_type():
    with pytest.raises(ValueError):
        launcher.signal2int(None)
