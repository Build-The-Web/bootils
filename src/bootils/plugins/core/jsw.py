# -*- coding: utf-8 -*-
# pylint: disable=
""" Tanuki Java Service Wrapper runtime environment.

    Debian JSW paths (Wheezy 3.5.3; Jessie 3.5.22)::

        /usr/sbin/wrapper – ELF executable
        /usr/share/wrapper/daemon.sh
        /usr/share/wrapper/make-wrapper-init.sh
        /usr/share/wrapper/wrapper.conf
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

from ..loader import PluginBase


class JavaServiceWrapper(PluginBase):
    """Tanuki Java Service Wrapper runtime environment."""

    def control_start(self, *args, **options):
        """Start a Java service."""
        print("*** JSW START ***")
        return True  # TODO: actually implement this

    def control_stop(self, *args, **options):
        """Stop a Java service."""
        return False  # TODO: actually implement this
