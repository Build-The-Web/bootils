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
from rudiments.reamed import click

from .._compat import encode_filename as to_apistr


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
    DEFAULT_PLUGIN_PATH = ['/etc/{appname}/plugin.d', '{appdir}/plugin.d']

    @classmethod
    def load_into_context(cls, ctx):
        """ Discovers plugins and places a PluginLoader instance in ``ctx.obj.plugins``.
        """
        ctx.obj.plugins = cls(ctx.obj.cfg, appname=ctx.find_root().info_name)
        return ctx.obj.plugins

    def __init__(self, cfg, appname):
        self.searchpath = [i.format(appname=appname, appdir=click.get_app_dir(appname))
                           for i in self.DEFAULT_PLUGIN_PATH]
        # TODO: add some env var path

        self._available = []
        self._custom = PluginBase(package=to_apistr('bootils.plugins.custom'))
        self._source = self._custom.make_plugin_source(searchpath=self.searchpath)

    def discover(self):
        """ Inspect the given search path and import any plugins found.

            Returns the list of plugins.
        """
        if not self._available:
            self._available = self._source.list_plugins()
        return self._available


class PluginExecutor(object):
    """
        Call plugin hooks in different life-cycle phases.
    """
