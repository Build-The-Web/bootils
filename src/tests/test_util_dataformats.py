# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=invalid-name, redefined-outer-name, too-few-public-methods
""" Test :py:mod:`bootils.util.dataformats`.
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

from collections import OrderedDict

import yaml

from bootils.util import dataformats


def test_render_odict_into_yaml():
    data = [OrderedDict((('foo', 1), ('bar', 2)))]
    dataformats.yaml_add_odict()
    assert OrderedDict in yaml.SafeDumper.yaml_representers, "Representer is registered"
    assert yaml.safe_dump(data) == '- {foo: 1, bar: 2}\n'
