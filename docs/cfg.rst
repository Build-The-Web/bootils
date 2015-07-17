.. _cfg:

Configuration Reference
=======================

**TODO**


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

Configuration files consist of sections that start with a ``[section-name]`` line,
with an (unnamed) *global* section before the named ones.
Nesting sub-sections into outer sections is achieved by adding more square brackets.
See `ConfigObj Files`_ for more details.

.. note::

    Later versions will offer alternative formats like YAML, as long as they're able
    to represent this nested structure of sections and key/value pairs.


.. _`ConfigObj Files`: https://configobj.readthedocs.org/en/latest/configobj.html#config-files
