.. _install:

Installation Guide
==================

Overview
--------

The following sections describe different installation options
– choose the right one for you.
If you use ``bash``, consider :ref:`bash-completion`.

You might also need to follow some `setup procedures`_
to make the necessary basic commands available on *Linux*, *Mac OS X*,
and *Windows*.

.. note::

    *Bootils* is tested on *Debian Wheezy* and *Ubuntu Trusty*.
    It will generally work on other platforms or other versions of these
    distributions, too. The most important pre-requisite is availability
    of Python 2.7 or 3.4+.

.. _`setup procedures`: https://py-generic-project.readthedocs.org/en/latest/installing.html#quick-setup


Installation as a Debian Package
--------------------------------

**TODO**

After installation, continue with the :doc:`quickstart`.


Installation With pip
---------------------

*Bootils* can be installed via ``pip install bootils`` as usual,
see `releases on GitHub <https://github.com/Build-The-Web/bootils/releases>`_
for an overview of available versions.
To get a bleeding-edge version from source, use these commands:

.. code-block:: shell

    repo="Build-The-Web/bootils"
    pip install -r "https://raw.githubusercontent.com/$repo/master/requirements.txt"
    pip install -U -e "git+https://github.com/$repo.git#egg=${repo#*/}"

It is recommended to **not** do this via ``sudo``, but to create a virtualenv first,
or use `pipsi`_ for installation.
See :doc:`CONTRIBUTING` on how to create a full development environment.

Continue with :ref:`bash-completion` or the :doc:`quickstart`.

.. _`pipsi`: https://github.com/mitsuhiko/pipsi


.. _bash-completion:

Setting Up bash Completion
--------------------------

To add bash completion, read the
`Click docs <http://click.pocoo.org/4/bashcomplete/#activation>`__
about it, or just follow these instructions:

.. code-block:: shell

    cmdname=one
    mkdir -p ~/.bash_completion.d
    ( export _$(tr a-z- A-Z_ <<<"$cmdname")_COMPLETE=source ; \
      $cmdname >~/.bash_completion.d/$cmdname.sh )
    grep /.bash_completion.d/$cmdname.sh ~/.bash_completion >/dev/null \
        || echo >>~/.bash_completion ". ~/.bash_completion.d/$cmdname.sh"
    . "/etc/bash_completion"

The :doc:`quickstart` describes the next steps.
