#!/usr/bin/environment python

import click
from procgen_cli.utils import conda


@click.group()
def env():
    """Setup or teardown the python environment"""
    pass


@click.command()
def setup():
    """Setup the python environment to run the starter kit"""
    if not conda.check():
        conda.install()
    conda.create_procgen_env()


@click.command()
def teardown():
    """Remove the python environment that was setup to run the starter kit"""
    conda.remove_procgen_env()


@click.command("download-miniconda")
def download_miniconda():
    """Download the latest version of Miniconda"""
    conda.download()


@click.command("install-miniconda")
def install_miniconda():
    """Install the latest version of Miniconda"""
    conda.install()


env.add_command(setup)
env.add_command(teardown)
env.add_command(download_miniconda)
env.add_command(install_miniconda)
