"""Process-level smoke test for the FastAPI and Streamlit applications."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from tempfile import TemporaryFile
from urllib.error import URLError
from urllib.request import urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.streamlit_app import is_api_healthy  # noqa: E402

HOST = "127.0.0.1"
STARTUP_TIMEOUT_SECONDS = 15.0
HEALTH_TIMEOUT_SECONDS = 0.5


def _available_ports(count: int) -> list[int]:
    """Reserve distinct ephemeral ports simultaneously to avoid duplicate selections."""
    sockets: list[socket.socket] = []
    try:
        for _ in range(count):
            listener = socket.socket()
            listener.bind((HOST, 0))
            sockets.append(listener)
        return [int(listener.getsockname()[1]) for listener in sockets]
    finally:
        for listener in sockets:
            listener.close()


def _log_tail(server_log: TemporaryFile) -> str:
    """Return the last part of a process log for actionable startup failures."""
    server_log.flush()
    server_log.seek(0)
    return server_log.read()[-2000:]


def _stop_server(process: subprocess.Popen[bytes] | None) -> None:
    """Stop a child server and wait for its process to exit."""
    if process is None or process.poll() is not None:
        return

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def _wait_for_http(
    url: str,
    process: subprocess.Popen[bytes],
    server_log: TemporaryFile,
    service_name: str,
) -> bytes:
    """Wait for an HTTP 200 response, failing early if the server exits."""
    deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        exit_code = process.poll()
        if exit_code is not None:
            raise RuntimeError(
                f"{service_name} exited before becoming healthy (code {exit_code}).\n"
                f"{_log_tail(server_log)}"
            )

        try:
            with urlopen(url, timeout=HEALTH_TIMEOUT_SECONDS) as response:
                if response.status == 200:
                    return response.read()
        except (URLError, TimeoutError):
            time.sleep(0.1)

    raise TimeoutError(
        f"{service_name} did not serve {url} within "
        f"{STARTUP_TIMEOUT_SECONDS:.0f} seconds.\n{_log_tail(server_log)}"
    )


def _wait_for_api_health(
    base_url: str,
    process: subprocess.Popen[bytes],
    server_log: TemporaryFile,
) -> None:
    """Wait until the Streamlit health client recognises the live FastAPI process."""
    deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        exit_code = process.poll()
        if exit_code is not None:
            raise RuntimeError(
                f"FastAPI exited before becoming healthy (code {exit_code}).\n"
                f"{_log_tail(server_log)}"
            )
        if is_api_healthy(base_url, timeout=HEALTH_TIMEOUT_SECONDS):
            return
        time.sleep(0.1)

    raise TimeoutError(
        f"FastAPI did not become healthy within {STARTUP_TIMEOUT_SECONDS:.0f} seconds.\n"
        f"{_log_tail(server_log)}"
    )


def run_smoke_test() -> None:
    """Verify Streamlit stays available while its configured API goes offline → online → offline."""
    streamlit_port, api_port = _available_ports(2)
    streamlit_url = f"http://{HOST}:{streamlit_port}"
    api_base_url = f"http://{HOST}:{api_port}"

    previous_api_url = os.environ.get("PATHSAATHI_API_URL")
    had_api_url = "PATHSAATHI_API_URL" in os.environ
    os.environ["PATHSAATHI_API_URL"] = api_base_url

    streamlit_process: subprocess.Popen[bytes] | None = None
    api_process: subprocess.Popen[bytes] | None = None

    streamlit_command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app/streamlit_app.py",
        "--server.address",
        HOST,
        "--server.port",
        str(streamlit_port),
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]
    api_command = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.main:app",
        "--host",
        HOST,
        "--port",
        str(api_port),
        "--log-level",
        "warning",
    ]

    try:
        with (
            TemporaryFile(mode="w+t", encoding="utf-8") as streamlit_log,
            TemporaryFile(mode="w+t", encoding="utf-8") as api_log,
        ):
            streamlit_process = subprocess.Popen(
                streamlit_command,
                cwd=PROJECT_ROOT,
                stdout=streamlit_log,
                stderr=subprocess.STDOUT,
                env=os.environ.copy(),
            )

            # The real Streamlit server must start even while its configured API is offline.
            _wait_for_http(
                f"{streamlit_url}/_stcore/health",
                streamlit_process,
                streamlit_log,
                "Streamlit",
            )
            page = _wait_for_http(
                f"{streamlit_url}/",
                streamlit_process,
                streamlit_log,
                "Streamlit",
            )
            if b"<html" not in page.lower():
                raise AssertionError("Streamlit root endpoint did not return an HTML document.")
            if is_api_healthy(timeout=HEALTH_TIMEOUT_SECONDS):
                raise AssertionError("The configured API should be offline before Uvicorn starts.")

            api_process = subprocess.Popen(
                api_command,
                cwd=PROJECT_ROOT,
                stdout=api_log,
                stderr=subprocess.STDOUT,
            )
            _wait_for_api_health(api_base_url, api_process, api_log)

            _stop_server(api_process)
            api_process = None
            if is_api_healthy(timeout=HEALTH_TIMEOUT_SECONDS):
                raise AssertionError("The Streamlit health client still reports the stopped API online.")

            # The Streamlit process and informational shell must remain available after API shutdown.
            _wait_for_http(
                f"{streamlit_url}/_stcore/health",
                streamlit_process,
                streamlit_log,
                "Streamlit after API shutdown",
            )
            _wait_for_http(
                f"{streamlit_url}/",
                streamlit_process,
                streamlit_log,
                "Streamlit root after API shutdown",
            )
    finally:
        _stop_server(api_process)
        _stop_server(streamlit_process)
        if had_api_url:
            os.environ["PATHSAATHI_API_URL"] = previous_api_url or ""
        else:
            os.environ.pop("PATHSAATHI_API_URL", None)

    print(
        "PASS: the real Streamlit server remained healthy while the configured API was offline, "
        "online and offline again."
    )


if __name__ == "__main__":
    run_smoke_test()
