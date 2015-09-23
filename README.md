# Bootils

![logo](https://raw.githubusercontent.com/Build-The-Web/bootils/master/docs/_static/img/logo-64.png) | Utilities for robust launcher and process life-cycle management scripts.
:----: | :----
**Project** |  [![Groups](https://img.shields.io/badge/Google_groups-btw--users-orange.svg)](https://groups.google.com/forum/#!forum/btw-users) [![License](https://img.shields.io/pypi/l/bootils.svg)](https://github.com/Build-The-Web/bootils/blob/master/LICENSE) [![Development Status](https://pypip.in/status/bootils/badge.svg)](https://pypi.python.org/pypi/bootils/)
**QA** |  [![Travis CI](https://api.travis-ci.org/Build-The-Web/bootils.svg)](https://travis-ci.org/Build-The-Web/bootils) [![Coveralls](https://img.shields.io/coveralls/Build-The-Web/bootils.svg)](https://coveralls.io/r/Build-The-Web/bootils) [![GitHub Issues](https://img.shields.io/github/issues/Build-The-Web/bootils.svg)](https://github.com/Build-The-Web/bootils/issues) [![Ready](https://badge.waffle.io/Build-The-Web/bootils.png?label=ready&title=Ready)](https://waffle.io/Build-The-Web/bootils) [![In Progress](https://badge.waffle.io/Build-The-Web/bootils.png?label=in+progress&title=In+Progress)](https://waffle.io/Build-The-Web/bootils)
**Release** |  [![Latest Version](https://img.shields.io/pypi/v/bootils.svg)](https://pypi.python.org/pypi/bootils/) [![Download format](https://pypip.in/format/bootils/badge.svg)](https://pypi.python.org/pypi/bootils/) [![Downloads](https://img.shields.io/pypi/dw/bootils.svg)](https://pypi.python.org/pypi/bootils/)


## Overview

*Bootils* offers process boot-strapping utilities that support writing
robust application/service launcher and process life-cycle management scripts.
It is comprised of a ``bootils`` Python package with building blocks
for process and resource management, and a CLI tool named ``nanny`` that
watches your child process after starting, until it grows up
into a stable running state.

:books: | For more details, see the full documentation at [Read The Docs](https://bootils.readthedocs.org/).
----: | :----


## Installation

Refer to the
[Installation Guide](https://bootils.readthedocs.org/en/latest/install.html)
on *Read The Docs*.

See [Contributing](#contributing) on how to create a full development environment.


## Usage

### “nanny” Process Launcher and Watchdog

``nanny`` can launch an application or service based on an
[INI-style configuration file](https://docs.python.org/2/library/configparser.html).
The following is a hopefully pretty much self-explanatory and totally made up example.

```ini
[launcher]
java-classpath = """
    /usr/share/java/commons-logging*.jar
    /usr/share/java/log4j*.jar
"""

java-agents = """
    /usr/share/java/jmx/jolokia-jvm-agent.jar=config=/etc/cassandra/jolokia-config.properties
"""

launch = """
    wait_for:port:12345
    timeout:120s
    jsw:StartStopApp:/usr/lib/cassandra/cassandra.jar
"""

[post-check]
logscan = """
    timeout:90s
    success:Started in [0-9]+ msec
    warn:Exception
    warn:WARNING: Could not open
    fail:OutOfMemory
    file:/var/log/cassandra/demon.log
"""

commands = """
    after:10s
    detach:/usr/sbin/jolocas watchdog
    after:60s
    call:/usr/sbin/nodetool status | grep '^U.* ${env:FACTER_IPV4} '
    call:/usr/sbin/jolocas check health
"""
```

The pre and post checks can also be called explicitely (via the
``pre-check`` and ``post-check`` sub-commands), to support some
outside process launcher. In this case, the checks are performed
as per config, and the return code reflects the outcome
(``0`` for OK, and ``1`` for failures).


## Contributing

Contributing to this project is easy, and reporting an issue or
adding to the documentation also improves things for every user.
You don’t need to be a developer to contribute.
See [CONTRIBUTING](https://github.com/Build-The-Web/bootils/blob/master/CONTRIBUTING.md) for more.

As a documentation author or developer,
to create a working directory for this project,
call these commands:

```sh
git clone "https://github.com/Build-The-Web/bootils.git"
cd "bootils"
. .env --yes --develop
invoke build --docs test check
```

You might also need to follow some
[setup procedures](https://py-generic-project.readthedocs.org/en/latest/installing.html#quick-setup)
to make the necessary basic commands available on *Linux*, *Mac OS X*, and *Windows*.


## Similar and Related Projects

 * [procdog](https://github.com/jlevy/procdog) – Lightweight command-line process control.
 * [mirakuru](https://github.com/ClearcodeHQ/mirakuru) – Starts a process, and waits for clear indication that it's running.
 * [ianitor](https://github.com/ClearcodeHQ/ianitor) – Doorkeeper for Consul discovered services.
 * [supervisor](https://github.com/Supervisor/supervisor)
 * [honcho](https://github.com/nickstenning/honcho)
 * [runit](http://smarden.org/runit/)
 * [systemd](http://www.freedesktop.org/wiki/Software/systemd/)
 * [upstart](http://upstart.ubuntu.com/)
 * [runc](https://github.com/opencontainers/runc)
 * [dinit](https://github.com/miekg/dinit)


## Acknowledgements

[![1&1](https://raw.githubusercontent.com/1and1/1and1.github.io/master/images/1and1-logo-42.png)](https://github.com/1and1)
Project sponsored by [1&1](https://github.com/1and1).

Documentation hosted by [Read the Docs](https://readthedocs.org/).
