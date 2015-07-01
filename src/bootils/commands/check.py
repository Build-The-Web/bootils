# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation, too-few-public-methods
""" 'help' command.
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

from .. import config, checks
from ..plugins import loader


@config.cli.command()
@click.option('-f', '--format', type=click.Choice(checks.CHECK_RESULT_FORMATS), default=checks.CHECK_RESULT_FORMATS[0],
    help="Output format to use for reporting check results.")
@click.argument('name', metavar='[‹name›]', nargs=1, default='default')
@click.pass_context
def check(ctx, format, name):
    """ Perform checks according to the service configuration.

        Provide the name of the service to check, otherwise 'default' is used.
        The special name 'all' will perform checks for all configured services,
        if you have several defined on a machine.
    """
    rc = 0
    executor = loader.PluginExecutor(ctx.obj.plugins)
    formatter = checks.CheckFormatter(format, verbose=ctx.obj.verbose)
    for result in executor.pre_checks():
        if not ctx.obj.quiet:
            formatter.dump(result)
        if not result.ok:
            rc = 1
    if not ctx.obj.quiet:
        formatter.close()
    if rc:
        sys.exit(rc)
