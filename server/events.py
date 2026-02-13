from __future__ import annotations
# AnimaWorks - Digital Person Framework
# Copyright (C) 2026 AnimaWorks Authors
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Any

from fastapi import Request


# ── WebSocket Event Helper ────────────────────────────────────

async def emit(request: Request, event_type: str, data: dict[str, Any]) -> None:
    """Broadcast a WebSocket event if the manager is available."""
    ws = getattr(request.app.state, "ws_manager", None)
    if ws:
        await ws.broadcast({"type": event_type, "data": data})
