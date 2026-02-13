from __future__ import annotations
# AnimaWorks - Digital Person Framework
# Copyright (C) 2026 AnimaWorks Authors
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import HTTPException, Request


# ── FastAPI Dependencies ──────────────────────────────────────

async def get_person(name: str, request: Request):
    """FastAPI dependency: resolve person by name or raise 404."""
    person = request.app.state.persons.get(name)
    if not person:
        raise HTTPException(status_code=404, detail=f"Person not found: {name}")
    return person
