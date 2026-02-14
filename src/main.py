import click


@click.group()
def cli():
    """Henchman - Your CLI tool."""
    pass


@cli.command()
def hello():
    """Say hello."""
    click.echo("Hello from henchman!")


if __name__ == "__main__":
    cli()
