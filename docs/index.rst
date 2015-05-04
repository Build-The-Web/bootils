.. Bootils documentation master file, created by
   sphinx-quickstart on Mon May  4 23:08:05 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the “Bootils” Documentation!
=======================================

.. image:: _static/img/logo-240.png

*Bootils* offers process boot-strapping utilities that support writing
robust application/service launcher and process life-cycle management
scripts. It is comprised of a :py:mod:`bootils` Python package with building
blocks for process and resource management, and a CLI tool named
``nanny`` that watches your child process after starting, until it grows
up into a stable running state.


Documentation Contents
----------------------

..  toctree::
    :maxdepth: 2

    intro
    install
    quickstart
    nanny
    cfg
    api-reference
    LICENSE


Indices & Tables
----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
