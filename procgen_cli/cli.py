#!/usr/bin/environment python

import click
from procgen_cli.environment.cmd import env
from procgen_cli.submission import dry_run


@click.group()
def cli():
    pass


@click.command()
def validate():
    """Validate submission configuration"""
    dry_run.validate()


cli.add_command(env)
cli.add_command(validate)

cli()
