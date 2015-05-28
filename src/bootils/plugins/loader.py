# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Short description.
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

import pluggy
            # XXX: pluggy.PluginManager, pluggy.PluginValidationError, pluggy.HookimplMarker, pluggy.HookspecMarker
from pluginbase import PluginBase

# from . import …


class BootilsHooks(object):
    """
        Hook specification.
    """


class PluginContext(object):
    """
        State held by plugins.
    """


class PluginLoader(object):
    """
        Load and manage plugins, both core and custom ones.
    """
    # Default places to look at
    DEFAULT_PLUGIN_PATH = ['/etc/bootils/plugin.d', '{appdir}/plugin.d']

    @class_method
    def load_into_context(cls, ctx):
        """
        """

    def __init__(self):
        self.plugins = []
        self._custom = PluginBase(package='bootils.plugins.custom')
        self._source = self._custom.make_plugin_source(searchpath=self.DEFAULT_PLUGIN_PATH)
        #self._source.list_plugins()


class PluginExecutor(object):
    """
        Call plugin hooks in different life-cycle phases.
    """
