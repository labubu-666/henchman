import subprocess

import click


@click.group()
def cli():
    """Henchman - Your CLI tool."""
    pass


@cli.group()
def compose():
    """Docker compose commands."""
    pass


@compose.command()
def up():
    """Start docker compose services."""
    subprocess.run(["docker", "compose", "up", "-d"])


@compose.command()
def down():
    """Stop docker compose services."""
    subprocess.run(["docker", "compose", "down"])


@cli.command()
def hello():
    """Say hello."""
    click.echo("Hello from henchman!")
