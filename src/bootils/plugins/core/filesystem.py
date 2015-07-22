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
import shlex

import psutil
from rudiments.humanize import bytes2iec, iec2bytes

from ..._compat import encode_filename
from ..loader import PluginBase


def on_same_fs(path1, path2):
    """Check if two paths reside in the same file system."""
    return os.stat(encode_filename(path1)).st_dev == os.stat(encode_filename(path2)).st_dev


def diskfree_result(spec):
    """Return result of a single disk usage check."""
    diagnostics = []
    parts = shlex.split(spec)
    path, parts = parts[0], parts[1:]
    usage = psutil.disk_usage(path)
    # -> sdiskusage(total=112263569408, used=59510784000, free=47026511872, percent=53.0)

    ok = True
    for threshold in parts:
        try:
            if threshold.endswith('%'):
                expected = usage.total * int(threshold[:-1], 10) / 100.0
            else:
                expected = iec2bytes(threshold)
        except (ValueError, TypeError) as cause:
            ok = False
            diagnostics.append("Unparsable threshold {threshold!r}: {cause}"
                               .format(threshold=threshold, cause=cause))
        else:
            if usage.free < expected:
                ok = False
                diagnostics.append("violated {threshold} condition ({percent:.1f}% {free} free)".format(
                                   threshold=threshold, free=bytes2iec(usage.free, compact=True), percent=100.0 - usage.percent))

    comment = '{spec} [{percent:.1f}% {free}/{total} free]'.format(
              spec=spec, total=bytes2iec(usage.total, compact=True),
              free=bytes2iec(usage.free, compact=True), percent=100.0 - usage.percent,
    )
    return ok, 'diskfree', comment, '\n'.join(diagnostics)


class FileSystem(PluginBase):
    """File system checks."""

    def _check(self):
        """Perform checks."""
        ##import pprint; print('\n'.join(pprint.pformat(i) for i in self.cfg.items()))

        for path in self.cfg_list('exists'):
            try:
                yield self.result(os.path.exists(encode_filename(path)), 'exists', path)
            except OSError as cause:
                yield self.result(False, 'exists', path, diagnostics=str(cause))

        for path in self.cfg_list('mounted'):
            try:
                mounted = not on_same_fs(path, '/')
            except OSError as cause:
                yield self.result(False, 'mounted', path, diagnostics=str(cause))
            else:
                yield self.result(mounted, 'mounted', path,
                                  diagnostics=None if mounted else 'path resides in root file system')

        for spec in self.cfg_list('diskfree'):
            yield self.result(*diskfree_result(spec))

    pre_check = _check
    post_check = _check
