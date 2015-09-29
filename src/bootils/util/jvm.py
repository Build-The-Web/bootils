# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" JVM / Java helpers.
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

import os
import sys
import subprocess


JAVA_HOME_DEFAULTS = [
    '/usr/lib/jvm/java-8-oracle',
    '/usr/lib/jvm/java-9-oracle',
    '/usr/lib/jvm/java-7-oracle',
    '/usr/lib/jvm/java-8-openjdk-amd64',
    '/usr/lib/jvm/java-9-openjdk-amd64',
    '/usr/lib/jvm/java-7-openjdk-amd64',
    '/usr/lib/jvm/default-java',
]


def java_home(java_home_path=None):
    """ Get Java home path.

        Parameters:
            java_home_path (str): Explicit Java home (e.g. from config).

        Returns:
            Path to configured or default Java home.

        Raises:
            EnvironmentError: Invalid Java home specified, or no default one found.
    """
    def has_bin_java(path):
        return os.access(os.path.join(path, 'bin', 'java'), os.X_OK)

    for explicit_path in (java_home_path, os.environ.get('BOOTILS_JAVA_HOME'), os.environ.get('JAVA_HOME')):
        if explicit_path:
            if has_bin_java(explicit_path):
                return explicit_path
            else:
                raise EnvironmentError("{!r} has no bin/java executable!".format(explicit_path))

    the_usual_suspects = JAVA_HOME_DEFAULTS[:]
    if the_usual_suspects:  # can be empty during unit tests
        try:
            default_bin_java = os.readlink('/etc/alternatives/java')
        except OSError:
            pass  # not on Debian
        else:
            the_usual_suspects.insert(0, os.path.dirname(os.path.dirname(default_bin_java)))

    for java_home_path in the_usual_suspects:
        if has_bin_java(java_home_path):
            return java_home_path

    raise EnvironmentError("No default JVM found, lookup path:\n{}".format('\n'.join(the_usual_suspects)))


def version_info(java_home_path, log=None):
    """ Get JVM version information.

        Returns:
            Tuple of full version number and JVM version info
    """
    cmd = [os.path.join(java_home_path, "bin", "java"), "-fullversion"]
    try:
        full_version = subprocess.check_output(cmd, stderr=subprocess.STDOUT).strip()
        if full_version.endswith('"'):
            full_version = full_version.split('"')[-2]
    except (subprocess.CalledProcessError, EnvironmentError, TypeError, ValueError, IndexError) as exc:
        if log:
            log("While getting JVM full version: %s" % exc)
        full_version = ''

    cmd[-1] = "-version"
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        version_details = output.splitlines()
    except (subprocess.CalledProcessError, EnvironmentError, TypeError, ValueError, IndexError) as exc:
        if log:
            log("While getting JVM version: %s" % exc)
        version_details = []

    return full_version, version_details


if __name__ == '__main__':
    # print version info for default JVM
    try:
        java_home_path = java_home()
    except EnvironmentError as exc:
        print('No default JVM found! ({})'.format(exc))
    else:
        errlog = lambda m: sys.stderr.write(m + '\n')
        full_version, version_details = version_info(java_home_path, log=errlog)
        print("Full JVM version: {}".format(full_version))
        print('    ' + '\n    '.join(version_details))
