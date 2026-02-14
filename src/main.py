import click

from src.utils import read_file


@click.group()
def cli():
    """Henchman - Your CLI tool."""
    pass


@cli.group()
def compose():
    """Docker compose commands."""
    pass


@compose.command()
@click.argument("extra_args", nargs=-1)
@click.option(
    "-f",
    "--file",
    "file_path",
    required=False,
    type=click.Path(exists=False),
    help="Path to docker-compose YAML file",
)
def up(extra_args=None, file_path=None):
    """Start docker compose services.

    Accepts an optional -f/--file to point to a compose YAML, and any
    additional arguments (e.g. -d) which are forwarded to `docker compose`.
    """
    extra_args = list(extra_args or ())
    cmd = ["docker", "compose", "up"]
    if file_path:
        # Attempt to read the YAML file provided by the user. This validates
        # the path (and supports '-' for stdin) before we build the docker
        # command. Any errors will be reported as a ClickException.
        try:
            yaml_text = read_file(file_path)
        except Exception as exc:
            raise click.ClickException(str(exc))

        click.echo(f"Read YAML from {file_path!s} ({len(yaml_text)} bytes)")
        if yaml_text:
            # Print the YAML contents (safe because this CLI is a local tool).
            click.echo(yaml_text)

        cmd.extend(["-f", file_path])
    if extra_args:
        cmd.extend(extra_args)

    # For safety, we only echo the command here (the original code used a
    # commented-out subprocess.run). If you want to actually execute docker,
    # replace the echo with subprocess.run(cmd, check=True).
    click.echo(f"No-op: would run: {' '.join(cmd)}")


@compose.command()
def down():
    """Stop docker compose services."""
    # subprocess.run(["docker", "compose", "down"])


if __name__ == "__main__":
    cli()
