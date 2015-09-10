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
import glob
import inspect
import pkgutil

from bunch import Bunch
from rudiments import pysupport
from rudiments.reamed import click

from .._compat import encode_filename as to_apistr
from .. import checks
from . import core, custom


def _find_plugin_classes(modules):
    """Find plugin classes in namespaces of discovered modules."""
    for module in modules:
        for name, obj in vars(module).items():
            if not name.startswith('_') and inspect.isclass(obj) and issubclass(obj, PluginBase) \
                    and obj.__module__ == module.__name__:
                yield obj


class PluginBase(object):
    """ Base class for plugins.

        This class defines the plugin interface (callbacks), and provides
        sensible default implementations so that a plugin only has
        to define those callbacks it *needs* to override.
    """

    def __init__(self, context):
        self.cfg = {}
        self.context = context

    @property
    def name(self):
        """Name of the plugin (e.g. for reporting)."""
        return self.__class__.__name__

    def cfg_list(self, key, section=None):
        """Get a config value as a list."""
        section = section or self.context.phase
        return [i.strip() for i in self.cfg[section].get(key, '').strip().splitlines()]

    def result(self, ok, name, comment, diagnostics=None):
        """Create :py:ref:`checks.CheckResult` with a qualified name."""
        return checks.CheckResult(ok, '{}:{}[{}]'.format(self.name, name, self.context.phase), comment, diagnostics)

    def configure(self, config):
        """Store plugin-specific configuration."""
        self.cfg = config

    def pre_check(self):
        """Perform pre-launch checks and generate results."""
        return []

    def control(self, command, *args, **options):
        """
            Control a service / process.

            This delegates to a ``control_‹command›`` method of a subclass, if one is found.

            Returns:
                bool: True if the command was handled successfully.
        """
        command_handler = getattr(self, 'control_' + command, None)
        if command_handler:
            return command_handler(*args, **options)
        else:
            return False

    def post_check(self):
        """Perform post-launch checks and generate results."""
        return []


class PluginContext(object):
    """ State held by plugins.
    """

    def __init__(self):
        self.phase = None
        self.results = []


class PluginLoader(object):
    """
        Load and manage plugins, both core and custom ones.

        See also `Package Discovery and Resource Access using pkg_resources`_.

        .. _`Package Discovery and Resource Access using pkg_resources`: https://pythonhosted.org/setuptools/pkg_resources.html
    """
    # Default places to look at
    DEFAULT_PLUGIN_PATH = ['/etc/{appname}/plugin.d', '{appdir}/plugin.d']

    @classmethod
    def load_into_context(cls, ctx, project=None):
        """ Discovers plugins and places a PluginLoader instance in ``ctx.obj.plugins``.
        """
        ctx.obj.plugins = cls(ctx.obj.cfg, appname=project or ctx.find_root().info_name)
        return ctx.obj.plugins

    def __init__(self, cfg, appname):
        self.cfg = cfg
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

        # TODO: load custom plugins from entry points

        # Load custom plugins from plugin path
        for path in self.searchpath:
            for module in glob.glob(os.path.join(path, '*.py')):
                if name.startswith('_'):
                    continue

                module_name = __name__.rsplit('.', 1)[0] + '.custom.' + os.path.splitext(os.path.basename(module))[0]
                modules.append(pysupport.load_module(module_name, module))

        self._available = list(_find_plugin_classes(modules))
        return self._available


class PluginExecutor(object):
    """
        Call plugin hooks in different life-cycle phases.
    """

    def __init__(self, loader):
        self.loader = loader
        self.context = PluginContext()
        self.plugins = [cls(self.context) for cls in self.loader.discover()]
        self.configure()

    def _delegate_with_yield(self, phase):
        """ Delegate execution of a phase to all plugins, and yield any
            generated results to the caller.
        """
        self.context.phase = phase
        for plugin in self.plugins:
            results = getattr(plugin, phase)()
            for result in results:
                yield result

    def configure(self):
        """Assemble configuration for each plugin and pass it on."""
        cfg = self.loader.cfg.load()
        for plugin in self.plugins:
            plugin_cfg = Bunch(pre_check={}, launcher={}, post_check={})
            for key, section in plugin_cfg.items():
                cfg_section = cfg.get(key.replace('_', '-'), {})
                section.update(cfg_section)
                section.update(cfg_section.get(plugin.name, {}))

            # Remove unrelated subsections
            for section in plugin_cfg.values():
                for key in section.keys()[:]:
                    if isinstance(section[key], dict):
                        del section[key]

            plugin.configure(plugin_cfg)

    def pre_checks(self):
        """Perform pre-launch checks."""
        for result in self._delegate_with_yield('pre_check'):
            yield result

    def control(self, command, *args, **options):
        """ Delegates execution of the given command to all plugins,
            until one of them indicates it handled the task.
        """
        self.context.phase = 'control_' + command
        for plugin in self.plugins:
            handled = plugin.control(command, *args, **options)
            if handled:
                break
        else:
            raise click.LoggedFailure("No active plugin supports the {} command!".format(command))

    def post_checks(self):
        """Perform post-launch checks."""
        for result in self._delegate_with_yield('post_check'):
            yield result
