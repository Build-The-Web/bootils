# Bootils

![logo](https://raw.githubusercontent.com/Build-The-Web/bootils/master/docs/_static/img/logo-64.png)
 [![Travis CI](https://api.travis-ci.org/Build-The-Web/bootils.svg)](https://travis-ci.org/Build-The-Web/bootils)
 [![GitHub Issues](https://img.shields.io/github/issues/Build-The-Web/bootils.svg)](https://github.com/Build-The-Web/bootils/issues)
 [![Ready](https://badge.waffle.io/Build-The-Web/bootils.png?label=ready&title=Ready)](https://waffle.io/Build-The-Web/bootils)
 [![In Progress](https://badge.waffle.io/Build-The-Web/bootils.png?label=in+progress&title=In+Progress)](https://waffle.io/Build-The-Web/bootils)
 [![License](https://img.shields.io/pypi/l/bootils.svg)](https://github.com/Build-The-Web/bootils/blob/master/LICENSE)
 [![Development Status](https://pypip.in/status/bootils/badge.svg)](https://pypi.python.org/pypi/bootils/)
 [![Latest Version](https://img.shields.io/pypi/v/bootils.svg)](https://pypi.python.org/pypi/bootils/)
 [![Download format](https://pypip.in/format/bootils/badge.svg)](https://pypi.python.org/pypi/bootils/)
 [![Downloads](https://img.shields.io/pypi/dw/bootils.svg)](https://pypi.python.org/pypi/bootils/)


## Overview

*Bootils* offers process boot-strapping utilities that support writing
robust application/service launcher and process life-cycle management scripts.
It is comprised of a ``bootils`` Python package with building blocks
for process and resource management, and a CLI tool named ``nanny`` that
watches your child process after starting, until it grows up
into a stable running state.


## Installation

*Bootils* can be installed via ``pip install bootils`` as usual,
see [releases](https://github.com/Build-The-Web/bootils/releases) for an overview of available versions.
To get a bleeding-edge version from source, use these commands:

```sh
repo="Build-The-Web/bootils"
pip install -r "https://raw.githubusercontent.com/$repo/master/requirements.txt"
pip install -UI -e "git+https://github.com/$repo.git#egg=${repo#*/}"
```

See [Contributing](#contributing) on how to create a full development environment.

To add bash completion, read the [Click docs](http://click.pocoo.org/4/bashcomplete/#activation) about it,
or just follow these instructions:

```sh
cmdname=nanny
mkdir -p ~/.bash_completion.d
_$(tr a-z- A-Z_ <<<"$cmdname")_COMPLETE=source $cmdname >~/.bash_completion.d/$cmdname.sh
grep /.bash_completion.d/$cmdname.sh ~/.bash_completion >/dev/null \
    || echo >>~/.bash_completion ". ~/.bash_completion.d/$cmdname.sh"
. "/etc/bash_completion"
```


## Usage

### “nanny” Process Launcher and Watchdog

``nanny`` can launch an application or service based on an
[INI-style configuration file](https://docs.python.org/2/library/configparser.html).
The following is a hopefully pretty much self-explanatory and totally made up example.

```ini
[pre-check]
packages =
    oracle-java8-jre | oracle-java8-installer
    java-service-wrapper
    jolokia-jvm-agent

exists =
    /etc/cassandra/jolokia-config.properties

mounted =
    /mnt/data
    /mnt/commitlog

diskspace =
    /mnt/data 30% 500G

[launcher]
java-classpath =
    /usr/share/java/commons-logging*.jar
    /usr/share/java/log4j*.jar

java-agents =
    /usr/share/java/jmx/jolokia-jvm-agent.jar=config=/etc/cassandra/jolokia-config.properties

launch =
    wait_for:port:12345
    timeout:120s
    jsw:StartStopApp:/usr/lib/cassandra/cassandra.jar

[post-check]
logscan =
    timeout:90s
    success:Started in [0-9]+ msec
    warn:Exception
    warn:WARNING: Could not open
    fail:OutOfMemory
    file:/var/log/cassandra/demon.log

commands =
    after:10s
    detach:/usr/sbin/jolocas watchdog
    after:60s
    call:/usr/sbin/nodetool status | grep '^U.* ${env:FACTER_IPV4} '
    call:/usr/sbin/jolocas check health
```

The pre and post checks can also be called explicitely (via the
``pre-check`` and ``post-check`` sub-commands), to support some
outside process launcher. In this case, the checks are performed
as per config, and the return code reflects the outcome
(``0`` for OK, and ``1`` for failures).


## Contributing

To create a working directory for this project, call these commands:

```sh
git clone "https://github.com/Build-The-Web/bootils.git"
cd "bootils"
. .env --yes --develop
invoke build --docs test check
```

See [CONTRIBUTING](https://github.com/Build-The-Web/bootils/blob/master/CONTRIBUTING.md) for more.


## References

**Tools**

* [Cookiecutter](http://cookiecutter.readthedocs.org/en/latest/)
* [PyInvoke](http://www.pyinvoke.org/)
* [pytest](http://pytest.org/latest/contents.html)
* [tox](https://tox.readthedocs.org/en/latest/)
* [Pylint](http://docs.pylint.org/)
* [twine](https://github.com/pypa/twine#twine)
* [bpython](http://docs.bpython-interpreter.org/)
* [yolk3k](https://github.com/myint/yolk#yolk)

**Packages**

* [Rituals](https://jhermann.github.io/rituals)
* [Click](http://click.pocoo.org/)
* [pluginbase](http://pluginbase.pocoo.org/)
* [psutil](https://pythonhosted.org//psutil/)


## Acknowledgements

[![1&1](https://raw.githubusercontent.com/1and1/1and1.github.io/master/images/1and1-logo-42.png)](https://github.com/1and1)
Project sponsored by [1&1](https://github.com/1and1).
