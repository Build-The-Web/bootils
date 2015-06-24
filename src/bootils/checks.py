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
import json
from collections import namedtuple, OrderedDict

import yaml


CHECK_RESULT_FORMATS = ['text', 'tap', 'json', 'yaml']

CheckResult = namedtuple('CheckResult', 'ok name comment')


# XXX: Put that elsewhere
def represent_odict(dump, tag, mapping, flow_style=None):
    """ Like BaseRepresenter.represent_mapping, but does not issue the sort().

        See `this blog post <http://blog.elsdoerfer.name/2012/07/26/make-pyyaml-output-an-ordereddict/>`_.
    """
    value = []
    node = yaml.MappingNode(tag, value, flow_style=flow_style)
    if dump.alias_key is not None:
        dump.represented_objects[dump.alias_key] = node
    best_style = True
    if hasattr(mapping, 'items'):
        mapping = mapping.items()
    for item_key, item_value in mapping:
        node_key = dump.represent_data(item_key)
        node_value = dump.represent_data(item_value)
        if not (isinstance(node_key, yaml.ScalarNode) and not node_key.style):
            best_style = False
        if not (isinstance(node_value, yaml.ScalarNode) and not node_value.style):
            best_style = False
        value.append((node_key, node_value))
    if flow_style is None:
        if dump.default_flow_style is not None:
            node.flow_style = dump.default_flow_style
        else:
            node.flow_style = best_style
    return node

yaml.SafeDumper.add_representer(OrderedDict,
    lambda dumper, value: represent_odict(dumper, u'tag:yaml.org,2002:map', value))


class CheckFormatter(object):
    """Emit a sequence of check results."""

    GLUE = dict(
        text=('', '\n', '\n'),
        tap=('', '\n', '\n'),
        json=('[\n', ',\n', '\n]\n'),
        yaml=('', '', '')
    )

    def __init__(self, formatting='text', stream=None):
        """ Dump results to given stream or stdout according to ``formatting``.
        """
        self.formatting = formatting
        self.stream = stream or sys.stdout
        self.index = 0
        self._formatter = getattr(self, '_to_' + formatting)

    def _to_text(self, result):
        """Text formatter."""
        return repr(result)

    def _to_tap(self, result):
        """TAP formatter."""
        return repr(result)

    def _to_json(self, result):
        """JSON formatter."""
        return json.dumps(result._asdict())

    def _to_yaml(self, result):
        """YAML formatter."""
        return yaml.safe_dump([result._asdict()])

    def write(self, text):
        self.stream.write(text)
        self.stream.flush()

    def dump(self, result):
        self.write(self.GLUE[self.formatting][1 if self.index else 0])
        self.write(self._formatter(result))
        self.index += 1

    def close(self):
        self.write(self.GLUE[self.formatting][2])
