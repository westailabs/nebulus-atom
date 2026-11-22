import asyncio
import os
import signal
import time
from pathlib import Path

import pytest

from nebulus_atom.services.mcp_service import MCPService

# Create a simple "echo" script to act as a mock MCP server
MOCK_MCP_SERVER_SCRIPT = """
import json
import os
import sys

def read_message():
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        return json.loads(line)
    except Exception:
        return None

def write_message(msg):
    sys.stdout.write(json.dumps(msg) + "\\n")
    sys.stdout.flush()

def main():
    with open(__file__ + ".pid", "w") as fh:
        fh.write(str(os.getpid()))
    while True:
        msg = read_message()
        if not msg:
            break

        if msg.get("method") == "initialize":
            write_message({
                "jsonrpc": "2.0",
                "id": msg.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "serverInfo": {"name": "mock-server", "version": "1.0"}
                }
            })
        elif msg.get("method") == "notifications/initialized":
            pass # Just ack
        elif msg.get("method") == "tools/list":
            write_message({
                "jsonrpc": "2.0",
                "id": msg.get("id"),
                "result": {
                    "tools": [
                        {
                            "name": "echo",
                            "description": "Echoes input",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"text": {"type": "string"}}
                            }
                        }
                    ]
                }
            })
        elif msg.get("method") == "tools/call":
            params = msg.get("params", {})
            if params.get("name") == "echo":
                text = params.get("arguments", {}).get("text", "")
                write_message({
                    "jsonrpc": "2.0",
                    "id": msg.get("id"),
                    "result": {
                        "content": [{"type": "text", "text": f"Echo: {text}"}]
                    }
                })
        else:
             # Basic error/ignore
             pass

if __name__ == "__main__":
    main()
"""


SHUTDOWN_TIMEOUT_S = 10
REAP_TIMEOUT_S = 5


def _reaped_or_gone(pid: int) -> bool:
    """True once ``pid`` has exited (reaping it if it is our child)."""
    try:
        done, _ = os.waitpid(pid, os.WNOHANG)
        return done == pid
    except ChildProcessError:
        # Not our child (or already reaped): fall back to an existence check.
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        return False


async def _stop_process(pid: int) -> None:
    """SIGTERM, wait, then SIGKILL and wait; each wait is bounded."""
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.kill(pid, sig)
        except ProcessLookupError:
            return
        deadline = time.monotonic() + REAP_TIMEOUT_S
        while time.monotonic() < deadline:
            if _reaped_or_gone(pid):
                return
            await asyncio.sleep(0.05)


@pytest.fixture
async def mock_mcp_server(tmp_path):
    """Path to a mock stdio MCP server; its process is always stopped afterwards.

    If the test fails before ``MCPService.shutdown()``, the stdio client keeps
    the server's stdin open, so the server never exits and its reader tasks
    never finish. pytest-asyncio then blocks forever cancelling them when it
    closes the event loop. Killing the server here closes its pipes and lets
    the loop shut down. The fixture is async so its teardown runs on the
    test's event loop, before pytest-asyncio closes that loop.
    """
    script_path = tmp_path / "mock_mcp.py"
    script_path.write_text(MOCK_MCP_SERVER_SCRIPT)
    yield str(script_path)
    pid_file = Path(f"{script_path}.pid")
    if pid_file.exists():
        await _stop_process(int(pid_file.read_text()))


@pytest.mark.asyncio
async def test_mcp_connection_and_tool_call(mock_mcp_server):
    service = MCPService()

    try:
        # 1. Connect
        result = await service.connect_server(
            name="test_server", command="python3", args=[mock_mcp_server]
        )

        assert "Connected" in result
        assert "test_server" in service.sessions

        # 2. Check Tools
        tools = service.get_tools()
        assert len(tools) == 1
        assert tools[0]["function"]["name"] == "mcp__test_server__echo"

        # 3. Call Tool
        output = await service.call_tool(
            "mcp__test_server__echo", {"text": "Hello MCP"}
        )

        assert "Echo: Hello MCP" in output

        # 4. Shutdown
        await service.shutdown()
        assert len(service.sessions) == 0
    finally:
        # Same task as connect_server, as anyio cancel scopes require.
        await asyncio.wait_for(service.shutdown(), timeout=SHUTDOWN_TIMEOUT_S)
