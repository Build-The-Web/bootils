.. _install:

Custom Plugins
==============

Installing Additional Plugins
-----------------------------

**TODO**

The default paths for custom plugins on a POSIX system are
``/etc/bootils/plugin.d`` and ``~/.config/bootils/plugin.d``.


Writing Your Own Plugins
------------------------

**TODO**

Plugins are implemented in classes that inherit from
:py:class:`bootils.plugins.loader.PluginBase` and
then provide appropriate method implementations like ``pre_check``.
``PluginBase`` also provides a few helper methods, most importantly
:py:func:`bootils.plugins.loader.PluginBase.result` to create
check result data that can then be yielded to the core.

To get an idea how this all works when put together,
look at the code of the built-in plugins in the
:py:mod:`bootils.plugins.core` package.
