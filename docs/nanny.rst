.. _nanny:

Using the CLI Tool
==================

The ``nanny`` command acts on the :doc:`configuration of a service <cfg>`,
by first checking any pre-launch requirements,
starting it when those are OK,
and then watching logs and other status indicators
until it reaches a stable running state.

Use ``nanny --help`` to get a list of global options and sub-commands,
``nanny ‹command› --help`` for detailed help on a specific command and its options,
and ``nanny help`` to get information like the paths to configuration files and
plugin directories.


Performing Checks
-----------------

While checking requirements is always done when launching a service,
it can also be triggered explicitely by using the ``check`` sub-command.
If any requirement isn't satisfied, the return code will reflect that
– use this together with the ``-q`` option to test them in scripts.

The ``--pre`` and ``--post`` options can be used to select which checks
to perform, if neither is given, *all* checks are active.

Each check produces a result with the following attributes:
``ok`` (either ``true`` or ``false``),
``name`` (the qualfied name of the check),
``comment`` (details on the requirement, e.g. a file system path),
and ``diagnostics`` (error messages, output of a command that actually performed the check, …).

Unless the global option ``-q`` is used, check results are printed to the
console; if you use ``-v``, diagnostic information is included, which can
help to hunt down the reason for a check failure.
The available output formats are ``text`` (tabular output),
``tap`` (Perl's `Test Anything Protocol`_),
and serialization into ``json``, ``yaml``, or ``csv``.
Use the ``--format`` option to select them, ``text`` is the default.

Example::

    $ nanny -v check -f tap
    not ok 1 FileSystem:exists /etc/cassandra/jolokia-config.properties
    ok 2 FileSystem:exists /etc/hosts
    not ok 3 FileSystem:mounted /mnt/data
    # [Errno 2] No such file or directory: '/mnt/data'
    not ok 4 FileSystem:mounted /mnt/commitlog
    # [Errno 2] No such file or directory: '/mnt/commitlog'
    not ok 5 FileSystem:mounted /opt
    # path resides in root file system
    ok 6 FileSystem:mounted /home
    ok 7 FileSystem:mounted /home/jhe
    not ok 8 FileSystem:diskfree /home 70% 44GiB [46.9% 43.8GiB/104.6GiB free]
    # violated 70% condition (46.9% 43.8GiB free)
    # violated 44GiB condition (46.9% 43.8GiB free)
    ok 9 Host:packages oracle-java8-jre | oracle-java8-installer
    # oracle-java8-jre 8.45-1~ui1404+1 install ok installed
    ok 10 Host:packages javaservicewrapper
    # javaservicewrapper 3.5.22-1~ui1404+1 install ok installed
    not ok 11 Host:packages jolokia-jvm-agent
    # Command '[u'dpkg-query', u'-W', u'-f=${Package} ${Version} ${Status}', u'jolokia-jvm-agent']' returned non-zero exit status 1
    1..11

.. _`Test Anything Protocol`: https://testanything.org/


Launching Services
------------------

**TODO**
