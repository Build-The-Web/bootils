# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation, too-few-public-methods
""" Service launching and process control commands.
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

from rudiments.reamed import click

from .. import config, launcher


@config.cli.group()
@click.argument('name', metavar='‹name›', nargs=1)
@click.pass_context
def service(ctx, name):
    """ Control a service.

        Provide the name of the service to check.
        The special name 'all' will perform checks for all configured services,
        if you have several defined on a machine.
    """
    # TODO: Implement config loading for named service


@service.command()
@click.pass_context
def start(ctx):
    """ Start a service.
    """
    print("Starting '{}'...".format(ctx.parent.params['name']))
    # TODO: Implement service start


@service.command()
@click.pass_context
def stop(ctx):
    """ Stop a service.
    """
    print("Stopping '{}'...".format(ctx.parent.params['name']))
    # TODO: Implement service stop
