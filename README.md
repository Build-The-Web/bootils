# Bootils

![logo](https://raw.githubusercontent.com/Build-The-Web/bootils/master/docs/_static/img/logo-64.png)

Process boot-strapping utilities that support writing
robust application/service launcher and
process life-cycle management scripts.

*Bootils* offers a ``bootils`` Python package with building blocks
for robust process management, and a CLI tool named ``nanny`` that
watches your child process after starting, until it grows up
into a stable running state.


## Usage

### “nanny” Process Launcher and Watchdog

``nanny`` can launch an application or service based on a INI-style
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


[launcher]
classpath =
    /usr/share/java/commons-logging*.jar
    /usr/share/java/log4j*.jar
    /usr/share/java/log4j*.jar

javaagent =
    /usr/share/java/jmx/jolokia-jvm-agent.jar=config=/etc/cassandra/jolokia-config.properties

launch =
    jsw:StartStopApp:/usr/lib/cassandra/cassandra.jar


[post-check]
logscan =
    /var/log/cassandra/demon.log \
        Exception OutOfMemory "WARNING: Could not open"

commands =
    /usr/sbin/nodetool status | grep '^U.* ${env:FACTER_IPV4} '
    /usr/sbin/jolocas check health
```

The pre and post checks can also be called explicitely (via the
``--pre-check`` and ``--post-check`` options), to support some
outside process launcher. In this case, the checks are performed
as per config, and the return code reflects the outcome
(``0`` for OK, and ``1`` for failures).
