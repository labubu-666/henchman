import os
import signal
import subprocess
from pathlib import Path
from typing import Sequence

import click

from src.schema import build_container_name, load_deployment
from src.utils import read_file


def run_and_forward(cmd: Sequence[str]) -> None:
    """Run `cmd` in a new process group and forward SIGINT/SIGTERM to it.

    This is Unix-specific (uses os.setsid) and will not attempt to catch SIGKILL.
    Raises subprocess.CalledProcessError if the child exits with a non-zero code.
    """
    # On Unix, start a new session/process group for the child.
    proc = subprocess.Popen(cmd, preexec_fn=os.setsid)

    # Save original handlers so we can restore them.
    orig_sigint = signal.getsignal(signal.SIGINT)
    orig_sigterm = signal.getsignal(signal.SIGTERM)

    def _forward(signum, frame):
        # Forward the incoming signal to the child's process group.
        try:
            os.killpg(proc.pid, signum)
        except ProcessLookupError:
            # Process group no longer exists.
            pass
        # Restore default handler for this signal and re-raise it against
        # the current process so the caller itself is terminated by the
        # same signal. This allows callers that expect to be killed by
        # the signal to observe that behavior (exitcode == -signum).
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)

    # Install forwarding handlers for SIGINT and SIGTERM.
    signal.signal(signal.SIGINT, _forward)
    signal.signal(signal.SIGTERM, _forward)

    try:
        returncode = proc.wait()
    finally:
        # Restore original handlers.
        signal.signal(signal.SIGINT, orig_sigint)
        signal.signal(signal.SIGTERM, orig_sigterm)

    if returncode != 0:
        # Mirror subprocess.run() behaviour by raising on non-zero exit.
        raise subprocess.CalledProcessError(returncode, cmd)


@click.group()
def cli():
    """Henchman - Your CLI tool."""
    pass


@cli.group()
def compose():
    """Docker compose commands."""
    pass


@compose.command()
@click.option(
    "-f",
    "--file",
    "file_path",
    required=False,
    type=click.Path(exists=False),
    help="Path to docker-compose YAML file",
)
@click.option(
    "-d",
    "--detach",
    "--detached",
    "detached",
    is_flag=True,
    default=False,
    help="Run containers in detached mode",
)
def up(file_path=None, detached=False):
    if not file_path:
        click.echo("No file path provided.")
        return True

    try:
        working_dir = Path.cwd().name
        yaml_text = read_file(file_path)
        deployment = load_deployment(yaml_text, detached)
        for name, service in deployment.services.items():
            container_name = build_container_name(working_dir, name)
            container_run_command = service.build_run_command(container_name=container_name)
            click.echo(
                f"{name}\n---\n{' '.join(container_run_command)}"
            )
            run_and_forward(
                container_run_command
            )
    except Exception as exc:
        raise click.ClickException(str(exc))


@compose.command()
@click.option(
    "-f",
    "--file",
    "file_path",
    required=False,
    type=click.Path(exists=False),
    help="Path to docker-compose YAML file",
)
def down(file_path=None):
    if not file_path:
        click.echo("No file path provided.")
        return True

    try:
        working_dir = Path.cwd().name
        yaml_text = read_file(file_path)
        deployment = load_deployment(yaml_text, detached=True)
        for name, service in deployment.services.items():
            container_name = build_container_name(working_dir, name)

            container_stop_command = service.build_stop_command(container_name=container_name)
            click.echo(
                f"{name}\n---\n{' '.join(container_stop_command)}"
            )
            run_and_forward(
                container_stop_command
            )

            # container_remove_command = service.build_remove_command(container_name=container_name)
            # click.echo(
            #     f"{name}\n---\n{' '.join(container_remove_command)}"
            # )
            # run_and_forward(
            #     container_remove_command
            # )
    except Exception as exc:
        raise click.ClickException(str(exc))


if __name__ == "__main__":
    cli()
