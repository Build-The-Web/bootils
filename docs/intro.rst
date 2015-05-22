.. _intro:

Introduction & Concepts
=======================

Motivation
----------

Startup scripts that come with services are commonly of the
launch-and-abandon variety, i.e. after a demon fork was successful, the
service is left alone and not watched from the outside.
But quite often problems arise only late in an initialization procedure,
and if no monitoring system or humans watches the logs and other indicators
of failure, those problems go unnoticed or at least are only recognized
far later than they could be.

The mission of *Bootils* is to fix that, by checking operational parameters
*before launching* a service, *during its initialization*,
and *while it is running*.
It also assists with describing robust startup procedures, and can thus help to
replace fragile default ``init.d`` scripts without spending lots of effort.
This also helps to reduce variation in the way different service processes
are managed.


Design Principles
-----------------

*Bootils* follows the `Unix Design Philosophy`_ of providing small, simple,
clear, modular, and extensible building blocks, to give its user the maximum
amount of flexibility and reusability.


Feature Overview
----------------

  * **Plugin System** – *Bootils* has a very small core that manages a set of
    configured plugins, both built-in and customes ones.
  * **Pre-Condition Checks** – If a service depends on the availability of resources
    like mount points or disk space, you can assert they're OK, instead of noticing
    problems only after you have one more incident to handle.
  * **Facility Re-Use** – Established technologies like process supervisors,
    the `Jolokia`_ JMX bridge and so on can be integrated via plugins.
  * **Runtime Environments** – In particular for launchine Java / JVM applications,
    a standard runtime is provided based on the `Tanuki Java Service Wrapper`_, which
    already establishes a basic level of startup and runtime monitoring.


.. _`Tanuki Java Service Wrapper`: http://wrapper.tanukisoftware.com/doc/english/product-overview.html
.. _`Unix Design Philosophy`: http://en.wikipedia.org/wiki/Unix_philosophy
.. _`Jolokia`: https://jolokia.org/
