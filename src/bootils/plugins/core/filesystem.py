# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" File system plugin.
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
import sys

from ..._compat import encode_filename
from ..loader import PluginBase


class FileSystem(PluginBase):
    """File system checks."""

    def pre_check(self):
        """Perform pre-launch checks."""
        ##import pprint; print('\n'.join(pprint.pformat(i) for i in self.cfg.items()))

        for path in self.cfg_list('exists'):
            self.context.add_result(os.path.exists(encode_filename(path)), self.name, "exists '{}'".format(path))
