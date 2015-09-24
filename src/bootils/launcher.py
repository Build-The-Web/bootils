# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Service launcher and processc control.
"""
# Copyright ©  2015 1&1 Group <btw-users@googlegroups.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, unicode_literals, print_function

import grp
import pwd
import signal

# from . import …


def signal2int(sig_spec):
    """ Convert given signal specification to its integer value.

        Parameters:
            sig_spec (int or str): Either already an int,
                a number as a string, or a case-insensitive signal name.

        Returns:
            int: Signal number.

        Raises:
            ValueError: Bad / unknown signal name, or bad input type.
    """
    try:
        signo = int(sig_spec)
    except (TypeError, ValueError):
        try:
            sig_name = sig_spec.upper()
            if not sig_name.startswith('SIG'):
                sig_name = 'SIG' + sig_name
            signo = getattr(signal, sig_name)
        except (TypeError, ValueError, AttributeError):
            raise ValueError('Bad signal specification {!r}'.format(sig_spec))

    return signo


def check_uid(uid):
    """ Get numerical UID of a user.

        Raises:
            KeyError: Unknown user name.
    """
    try:
        return 0 + uid  # already numerical?
    except TypeError:
        if uid.isdigit():
            return int(uid)
        else:
            return pwd.getpwnam(uid).pw_uid


def check_gid(gid):
    """ Get numerical GID of a group.

        Raises:
            KeyError: Unknown group name.
    """
    try:
        return 0 + gid  # already numerical?
    except TypeError:
        if gid.isdigit():
            return int(gid)
        else:
            return grp.getgrnam(gid).gr_gid


class LauncherBase(object):
    """ Process launch & management.
    """

    def __init__(self, config):
        self.config = config


    def init_environ(self):
        """ Initialize process environment and return its old state.
        """
        # Note that though we don't change the environment ourselves,
        # we save it as a service to our derived classes
        old_umask = None
        old_cwd = os.getcwd()
        old_environ = os.environ.copy()

        try:
            # Order is important here!
            umask_str = self.config.get("umask")
            if umask_str:
                old_umask = os.umask(int(umask_str, 8))
            os.chdir(self.service_base_path)
            self._snapshot_log_offset()
        except:  # restore state and re-raise
            if old_umask is not None:
                os.umask(old_umask)
            os.chdir(old_cwd)
            raise
        else:
            return old_umask, old_cwd, old_environ


    def restore_environ(self, oldstate):
        """ Restore process environment to previous state as returned by :py:ref:`init_environ`.
        """
        old_umask, old_cwd, old_environ = oldstate

        # Handle process parameters
        if old_umask is not None:
            os.umask(old_umask)
        os.chdir(old_cwd)

        # Handle environment
        for key, val in old_environ.items():
            if os.environ.get(key) != val:
                #log.trace("Restoring %s=%r" % (key, val))
                os.environ[key] = val

        for key in set(os.environ.keys()) - set(old_environ.keys()):
            #log.trace("Removing environment variable %s" % (key,))
            del os.environ[key]
