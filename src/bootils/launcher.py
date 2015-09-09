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
