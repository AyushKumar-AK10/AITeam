import subprocess

def run_terminal(command: str) -> str:
    """Run a shell command and return explicit execution evidence."""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    status = "SUCCESS" if result.returncode == 0 else "FAILED"
    output = result.stdout.strip() or "<no stdout>"
    errors = result.stderr.strip() or "<no stderr>"
    return (
        f"STATUS: {status}\n"
        f"COMMAND: {command}\n"
        f"EXIT_CODE: {result.returncode}\n"
        f"STDOUT:\n{output}\n"
        f"STDERR:\n{errors}"
    )