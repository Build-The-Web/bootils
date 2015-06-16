# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Plugin management.
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
import inspect
import pkgutil

from rudiments.reamed import click

from .._compat import encode_filename as to_apistr
from . import core


def _find_plugin_classes(modules):
    """Find plugin classes in namespaces of discovered modules."""
    for module in modules:
        for name, obj in vars(module).items():
            if not name.startswith('_') and inspect.isclass(obj) and issubclass(obj, PluginBase) \
                    and obj.__module__ == module.__name__:
                yield obj


class PluginBase(object):
    """
        Base class for plugins.
    """


class PluginContext(object):
    """
        State held by plugins.
    """


class PluginLoader(object):
    """
        Load and manage plugins, both core and custom ones.

        See also `Package Discovery and Resource Access using pkg_resources`_.

        .. _`Package Discovery and Resource Access using pkg_resources`: https://pythonhosted.org/setuptools/pkg_resources.html
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

    def discover(self):
        """ Inspect the given search path and import any plugins found.

            Returns the list of plugin classes.
        """
        modules = []

        # Load core plugin modules
        for _, name, is_pkg in pkgutil.iter_modules(core.__path__):
            if name.startswith('_') or is_pkg:
                continue
            modules.append(__import__(core.__name__ + '.' + name, globals(), {}, ['__file__']))

        self._available = list(_find_plugin_classes(modules))
        return self._available


class PluginExecutor(object):
    """
        Call plugin hooks in different life-cycle phases.
    """