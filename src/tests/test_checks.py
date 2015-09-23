# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=invalid-name, redefined-outer-name, too-few-public-methods
""" Test :py:mod:`bootils.checks`.
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

from bootils import checks
from bootils._compat import StringIO


@pytest.fixture
def ok_result():
    return checks.CheckResult(True, 'test', 'just a test', 'more information')


@pytest.fixture(scope='module', params=checks.CHECK_RESULT_FORMATS)
def any_formatter(request):
    return checks.CheckFormatter(request.param, StringIO())


def test_check_formatter_knows_all_formats():
    assert set(checks.CHECK_RESULT_FORMATS) == set(checks.CheckFormatter.GLUE.keys())


def test_check_formatter_fails_on_unknown_format():
    with pytest.raises(AttributeError):
        checks.CheckFormatter('foobar')


def test_check_formatter_accepts_known_formats():
    for format in checks.CHECK_RESULT_FORMATS:
        checks.CheckFormatter(format)


def test_check_formatter_as_dict_has_diagnostics_if_verbose(ok_result):
    cf = checks.CheckFormatter(verbose=True)
    assert 'diagnostics' in cf._asdict(ok_result)


def test_check_formatter_as_dict_omits_diagnostics_normally(ok_result):
    cf = checks.CheckFormatter()
    assert 'diagnostics' not in cf._asdict(ok_result)


def test_check_formatter_basically_works_for_any_format(any_formatter, ok_result):
    any_formatter.dump(ok_result)
    assert 'just a test' in any_formatter.stream.getvalue()
    assert any_formatter.index == 1


def test_check_formatter_emits_comments_with_tap(ok_result):
    cf = checks.CheckFormatter('tap', StringIO(), verbose=True)
    cf.dump(ok_result)
    cf.close()
    result = cf.stream.getvalue().splitlines()

    assert len(result) == 3
    assert sum(i.startswith('#') for i in result) == 1
    assert result[-1] == '1..1'
