# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Check helpers + results.
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

import sys
import csv
import json
from collections import namedtuple, OrderedDict

import yaml

from ._compat import StringIO
from .util import dataformats


CHECK_RESULT_FORMATS = ['text', 'tap', 'json', 'yaml', 'csv']

CheckResult = namedtuple('CheckResult', 'ok name comment diagnostics')


class CheckFormatter(object):
    """Emit a sequence of check results."""

    GLUE = dict(
        text=('', '\n', '\n'),
        tap=('', '\n', '\n'),
        json=('[\n', ',\n', '\n]\n'),
        yaml=('', '', ''),
        csv=('', '', ''),
    )

    def __init__(self, formatting='text', stream=None, verbose=False):
        """ Dump results to given stream or stdout according to ``formatting``.
        """
        self.formatting = formatting
        self.stream = stream or sys.stdout
        self.verbose = verbose
        self.index = 0
        self._formatter = getattr(self, '_to_' + formatting)

    def _asdict(self, result):
        """Return a CheckResult as a dict."""
        result_dict = result._asdict()
        if not self.verbose:
            result_dict = result_dict.copy()
            del result_dict['diagnostics']
        return result_dict

    def _to_text(self, result):
        """Text formatter."""
        return repr(result)

    def _to_tap(self, result):
        """TAP formatter."""
        lines = ['{ok} {num} {name} {comment}'.format(
            ok='ok' if result.ok else 'not ok', num=self.index+1, name=result.name, comment=result.comment,
        )]
        if result.diagnostics and self.verbose:
            try:
                diagnostics = result.diagnostics.splitlines()
            except AttributeError:
                diagnostics = result.diagnostics
            lines.extend(['# ' + i for i in diagnostics])
        return '\n'.join(lines)

    def _to_json(self, result):
        """JSON formatter."""
        return json.dumps(self._asdict(result))

    def _to_yaml(self, result):
        """YAML formatter."""
        dataformats.yaml_add_odict()
        return yaml.safe_dump([self._asdict(result)])

    def _to_csv(self, result):
        """CSV formatter."""
        buf = StringIO()
        writer = csv.writer(buf)
        if self.index == 0:
            writer.writerow([i.capitalize() for i in self._asdict(result).keys()])
        writer.writerow(result[:4 if self.verbose else 3])
        return buf.getvalue()

    def write(self, text):
        """Unbuffered write of given text to output stream."""
        self.stream.write(text)
        self.stream.flush()

    def dump(self, result):
        """Print a single check result."""
        self.write(self.GLUE[self.formatting][1 if self.index else 0])
        self.write(self._formatter(result))
        self.index += 1

    def close(self):
        """Print any trailing output and clean up resources."""
        self.write(self.GLUE[self.formatting][2])
        if self.formatting == 'tap':
            self.write('1..{}\n'.format(self.index))
