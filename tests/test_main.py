import os
import signal
import sys
import time
import subprocess


def test_run_and_forward_forwards_sigterm(tmp_path):
    # Create a small Python script that calls run_and_forward on a sleeping child.
    script = tmp_path / "runner.py"
    script.write_text(
        """
from src.main import run_and_forward
import sys
run_and_forward([sys.executable, '-c', 'import time; time.sleep(30)'])
"""
    )

    # Start the runner script as a subprocess.
    p = subprocess.Popen([sys.executable, str(script)])

    try:
        # Give it a moment to start and spawn the child.
        time.sleep(0.5)

        # Send SIGTERM to the process running run_and_forward. It should forward
        # SIGTERM to the child's process group and then be terminated by SIGTERM
        # itself (we re-raise the signal in the handler).
        os.kill(p.pid, signal.SIGTERM)

        # Wait for the process to exit.
        p.wait(timeout=5)

        assert p.returncode == -signal.SIGTERM
    finally:
        # Cleanup: ensure the process is not left running.
        try:
            p.kill()
        except Exception:
            pass
        p.wait()
