# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Networking plugin.
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

import psutil

from ..loader import PluginBase


class Network(PluginBase):
    """Networking checks."""

    def _check(self):
        """Perform checks."""

        cfg = self.cfg[self.context.phase].get(self.name, {})
        ports = cfg.get('ports')
        if not ports:
            return
        try:
            ports = [ports + '']
        except (TypeError, ValueError):
            pass # ports already iterable

        for port in ports:
            yield self._result('inet', None, port)

        for section in cfg.keys():
            if section in ['ports']:
                continue
            scf = cfg[section]
            yield self._result(scf.get('family', 'inet'), scf.get('address'), scf.get('port'), section)

    def _result(self, family, address, port, service=""):
        """Returns result on availability of specified socket."""

        if address:
            cmt = "Listening port {}:{}:{}".format(family, address, port)
        else:
            cmt = "Listening port {}::{}".format(family, port)
        if service:
            cmt = cmt + " ({})".format(service)

        # check if socket is already bound
        for conn in psutil.net_connections(kind=family):
            if conn.status == psutil.CONN_LISTEN and (not address or conn.laddr[0] == address) \
                    and conn.laddr[1] == int(port):
                return self.result(False, "server_socket", cmt, diagnostics="Socket alread bound")

        # check if interface exists
        if address and address != '0.0.0.0':
            found = False
            for _, addrs in psutil.net_if_addrs().items():
                for snic in addrs:
                    if snic.address == address:
                        found = True
                        break
            if not found:
                return self.result(False, "server_socket", cmt, diagnostics="Interface for {} does not exist".format(address))

        return self.result(True, "server_socket", cmt, diagnostics="Socket available")

    pre_check = _check
