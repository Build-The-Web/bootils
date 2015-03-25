# Bootils

![logo](https://raw.githubusercontent.com/Build-The-Web/bootils/master/docs/_static/img/logo-64.png)

*Bootils* offers process boot-strapping utilities that support writing
robust application/service launcher and process life-cycle management scripts.
It is comprised of a ``bootils`` Python package with building blocks
for process and resource management, and a CLI tool named ``nanny`` that
watches your child process after starting, until it grows up
into a stable running state.


## Usage

### “nanny” Process Launcher and Watchdog

``nanny`` can launch an application or service based on an INI-style
configuration file. The following is a hopefully pretty much
self-explanatory and totally made up example.

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
