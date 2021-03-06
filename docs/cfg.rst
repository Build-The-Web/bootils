.. _cfg:

Configuration Reference
=======================

**TODO**

Configuration File Structure
----------------------------

Configuration files consist of sections that start with a ``[section-name]`` line,
with an (unnamed) *global* section before the named ones.
Nesting sub-sections into outer sections is achieved by adding more square brackets.
See `ConfigObj Files`_ for more details.

Each section holds a list of key/value pairs.

.. note::

    Later versions will offer alternative formats like YAML, as long as they're able
    to represent this nested structure of sections and key/value pairs.


.. _`ConfigObj Files`: https://configobj.readthedocs.io/en/latest/configobj.html#config-files


.. _config-file:

Main Configuration Files
------------------------

Configuration files are expected at the locations as shown by the ``nanny help``
command, on a Linux system that is::

    /etc/bootils/nanny.conf
    /etc/bootils/nanny.d/*.conf
    ~/.config/bootils/nanny.conf

If you define the ``NANNY_CONFIG`` environment variable with additional files,
those will be appended to the default list
– try this command to see for yourself::

    NANNY_CONFIG=/tmp/foo.conf:/tmp/bar.conf nanny help

Configuration files are merged in the given order, i.e. keys that appear in files
further down the list shadow those in files read earlier.
This allows you to provide general settings in the default files,
and then modify and extend them for a specific service.

Common usage patterns are to have everything in ``/etc/bootils/nanny.conf``
if you only ever run a single service (say, in a Docker container), and
use the ``conf.d`` directory for snippets of global configuration added by packages.
If you run several services on one machine, keep ``nanny.conf`` clear of
settings specific to any service, and use ``nanny.d/‹service›.conf`` files for those.
In the service-specific files, be sure to qualify your top-level sections with the
service name, e.g. ``[‹service›:pre-check]``.


Built-in Plugins
----------------


FileSystem
^^^^^^^^^^

This plugin allows to check that a certain path ``exists``, is ``executable``,
or is ``mounted`` (i.e. not part of the root file-system).
You can also check for free space of the volume of a given path using ``diskfree``.

All these attributes take a multi-line list of paths to check,
``diskfree`` also expects a percentage or size threshold of minimal free space.
If both a percentage and a size is given, each must be satisfied for the check to be OK.

Example::

    [pre-check]

    [[FileSystem]]

    exists = """
        /etc/cassandra/jolokia-config.properties
        /etc/hosts
    """

    executable = """
        /bin/bash
    """

    mounted = """
        /mnt/data
        /mnt/commitlog
        /opt
        /home
    """

    diskfree = """
        /home 5% 42GiB
    """


Host
^^^^

With the ``Host`` plugin, you can ensure that essential ``packages``
were indeed installed by your configuration management tool.
This provides explicit diagnostics
(unlike e.g. a ``command not found`` for some missing tool),
and avoids errors that might only appear
when a service tries to access an optional component that was not installed.

Example::

    [pre-check]

    [[Host]]
    packages = """
        oracle-java8-jre | oracle-java8-installer
        service-wrapper
        jolokia-jvm-agent
    """


Network
^^^^^^^

The ``network`` plugin is able to check if all ports and addresses, that your
server is going to use, are not already bound.

Example (short-hand notation)::

   [pre-check]

   [[Network]]
   ports = 80, 8081

Example (verbose)::

   [pre-check]

   [[Network]]

   [[[http]]]
   port = 80
   family = tcp
   address = 0.0.0.0

   [[[jmx_port]]]
   port = 6379
   family = tcp
   address = 127.0.0.1
