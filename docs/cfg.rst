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


.. _`ConfigObj Files`: https://configobj.readthedocs.org/en/latest/configobj.html#config-files


.. _config-file:

Main Configuration Files
------------------------

Configuration files are expected at the locations as shown by the ``nanny help``
command, on a Linux system that is ``/etc/bootils/nanny.conf`` and ``~/.config/bootils/nanny.conf``.
If you define the ``NANNY_CONFIG`` environment variable with additional files,
those will be appended to the default list
– try the ``NANNY_CONFIG=/tmp/foo.conf:/tmp/bar.conf nanny help`` command to see for yourself.
Configuration files are merged in the given order, i.e. keys that appear in files
further down the list shadow those in files read earlier.
This allows you to provide general settings in the default files,
and then modify and extend them for a specific service.



Built-in Plugins
----------------


FileSystem
^^^^^^^^^^

This plugin allows to check that a certain path ``exists``
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
when a service tries to accesss an optional component that was not installed.

Example::

    [pre-check]

    [[Host]]
    packages = """
        oracle-java8-jre | oracle-java8-installer
        service-wrapper
        jolokia-jvm-agent
    """
