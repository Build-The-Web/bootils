# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Host + operating system plugin.
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
import subprocess

from ..loader import PluginBase


class Host(PluginBase):
    """Host and OS checks."""

    def pre_check(self):
        """Perform pre-launch checks."""
        for pkg_spec in self.cfg_list('packages'):
            ok, status = False, None
            for pkg_name in pkg_spec.split('|'):
                pkg_name = pkg_name.strip()
                # TODO: Support package formats other than DEB
                cmd = ['dpkg-query', '-W', '-f=${Package} ${Version} ${Status}', pkg_name]
                try:
                    status = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                    ok = 'ok installed' in status
                    if ok:
                        break
                except (EnvironmentError, subprocess.CalledProcessError) as cause:
                    status = str(cause)
                    ok = False

            yield self.result(ok, 'packages', pkg_spec, diagnostics=status)
