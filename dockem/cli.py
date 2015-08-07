#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dockem.cli
-----------------

Main `dockem` CLI.
"""

from __future__ import unicode_literals

import os
import sys
import logging

import click

from dockem import __version__
from dockem.main import execute_container, create_config_file

logger = logging.getLogger(__name__)


def print_version(context, param, value):
    if not value or context.resilient_parsing:
        return
    click.echo('Dockem %s from %s (Python %s)' % (
        __version__,
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        sys.version[:3]
    ))
    context.exit()


@click.command()
@click.option(
    '--create-config', is_flag=True,
    help='Create configuration file',
)
@click.option(
    '--run', is_flag=True,
    help='Run Docker container',
)
@click.option(
    '-V', '--version',
    is_flag=True, help='Show version information and exit.',
    callback=print_version, expose_value=False, is_eager=True,
)
@click.option(
    '-v', '--verbose',
    is_flag=True, help='Print debug information', default=False
)
def main(create_config, run, verbose):
    """Run a docker container or create_config_file"""
    if verbose:
        logging.basicConfig(
            format='%(levelname)s %(filename)s: %(message)s',
            level=logging.DEBUG
        )
    else:
        # Log info and above to console
        logging.basicConfig(
            format='%(levelname)s: %(message)s',
            level=logging.INFO
        )

    try:
        if create_config:
            create_config_file()
        elif run:
            execute_container()
    except Exception, e:
        click.echo(e)
        sys.exit(1)

if __name__ == "__main__":  # pragma: no cover
    main()
