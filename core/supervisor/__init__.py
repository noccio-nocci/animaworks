"""
Process isolation supervisor package.

Provides process-level isolation for each Person by running them in
separate subprocesses communicating via Unix Domain Sockets.
"""

from __future__ import annotations

from core.supervisor.ipc import IPCClient, IPCServer, IPCRequest, IPCResponse, IPCEvent
from core.supervisor.process_handle import ProcessHandle, ProcessState, ProcessStats

__all__ = [
    "IPCClient",
    "IPCServer",
    "IPCRequest",
    "IPCResponse",
    "IPCEvent",
    "ProcessHandle",
    "ProcessState",
    "ProcessStats",
]
