"""Network-level smoke test for FastAPI and the Streamlit API health client."""

from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path
from tempfile import TemporaryFile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.streamlit_app import is_api_healthy  # noqa: E402

HOST = "127.0.0.1"
STARTUP_TIMEOUT_SECONDS = 10.0
HEALTH_TIMEOUT_SECONDS = 0.5


def _available_port(host: str) -> int:
    """Ask the OS for an unused local TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind((host, 0))
        return int(listener.getsockname()[1])


def _stop_server(process: subprocess.Popen[bytes]) -> None:
    """Stop Uvicorn and ensure the port is released before the offline check."""
    if process.poll() is not None:
        return

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def run_smoke_test() -> None:
    """Verify offline → live FastAPI → offline using the UI's real health client."""
    port = _available_port(HOST)
    base_url = f"http://{HOST}:{port}"

    if is_api_healthy(base_url, timeout=HEALTH_TIMEOUT_SECONDS):
        raise RuntimeError("The supposedly unused smoke-test port is already serving PathSaathi.")

    command = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.main:app",
        "--host",
        HOST,
        "--port",
        str(port),
        "--log-level",
        "warning",
    ]

    with TemporaryFile(mode="w+t", encoding="utf-8") as server_log:
        process = subprocess.Popen(
            command,
            cwd=PROJECT_ROOT,
            stdout=server_log,
            stderr=subprocess.STDOUT,
        )
        try:
            deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
            while time.monotonic() < deadline:
                exit_code = process.poll()
                if exit_code is not None:
                    server_log.flush()
                    server_log.seek(0)
                    details = server_log.read()[-2000:]
                    raise RuntimeError(
                        f"FastAPI exited before becoming healthy (code {exit_code}).\n{details}"
                    )

                if is_api_healthy(base_url, timeout=HEALTH_TIMEOUT_SECONDS):
                    break
                time.sleep(0.1)
            else:
                server_log.flush()
                server_log.seek(0)
                details = server_log.read()[-2000:]
                raise TimeoutError(
                    f"FastAPI did not become healthy within "
                    f"{STARTUP_TIMEOUT_SECONDS:.0f} seconds.\n{details}"
                )
        finally:
            _stop_server(process)

    if is_api_healthy(base_url, timeout=HEALTH_TIMEOUT_SECONDS):
        raise AssertionError("The Streamlit health client still reports the stopped API as online.")

    print(
        "PASS: Streamlit's API health client reported offline before startup, "
        "online for the live FastAPI process, and offline after shutdown."
    )


if __name__ == "__main__":
    run_smoke_test()
