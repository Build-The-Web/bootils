# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Data format support & extensions.
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
from collections import OrderedDict

import yaml


def _represent_odict(dump, mapping, flow_style=None):
    """ Like BaseRepresenter.represent_mapping, but does not issue the sort().

        See `this blog post <http://blog.elsdoerfer.name/2012/07/26/make-pyyaml-output-an-ordereddict/>`_.
    """
    tag = u'tag:yaml.org,2002:map'
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


def yaml_add_odict():
    """Add YAML serialization support for ``OrderedDict`` objects."""
    if OrderedDict not in yaml.SafeDumper.yaml_representers:
        yaml.SafeDumper.add_representer(OrderedDict, _represent_odict)
