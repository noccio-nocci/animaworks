from __future__ import annotations
# AnimaWorks - Digital Person Framework
# Copyright (C) 2026 AnimaWorks Authors
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging

from fastapi import APIRouter, Depends, HTTPException

from core.memory.conversation import ConversationMemory
from server.dependencies import get_person

logger = logging.getLogger("animaworks.routes.memory")


def create_memory_router() -> APIRouter:
    router = APIRouter()

    # ── Episodes ──────────────────────────────────────────

    @router.get("/persons/{name}/episodes")
    async def list_episodes(name: str, person=Depends(get_person)):
        return {"files": person.memory.list_episode_files()}

    @router.get("/persons/{name}/episodes/{date}")
    async def get_episode(name: str, date: str, person=Depends(get_person)):
        path = person.memory.episodes_dir / f"{date}.md"
        if not path.exists():
            raise HTTPException(status_code=404, detail="Episode not found")
        return {"date": date, "content": path.read_text(encoding="utf-8")}

    # ── Knowledge ─────────────────────────────────────────

    @router.get("/persons/{name}/knowledge")
    async def list_knowledge(name: str, person=Depends(get_person)):
        return {"files": person.memory.list_knowledge_files()}

    @router.get("/persons/{name}/knowledge/{topic}")
    async def get_knowledge(name: str, topic: str, person=Depends(get_person)):
        path = person.memory.knowledge_dir / f"{topic}.md"
        if not path.exists():
            raise HTTPException(status_code=404, detail="Knowledge not found")
        return {"topic": topic, "content": path.read_text(encoding="utf-8")}

    # ── Procedures ────────────────────────────────────────

    @router.get("/persons/{name}/procedures")
    async def list_procedures(name: str, person=Depends(get_person)):
        return {"files": person.memory.list_procedure_files()}

    @router.get("/persons/{name}/procedures/{proc}")
    async def get_procedure(name: str, proc: str, person=Depends(get_person)):
        path = person.memory.procedures_dir / f"{proc}.md"
        if not path.exists():
            raise HTTPException(status_code=404, detail="Procedure not found")
        return {"name": proc, "content": path.read_text(encoding="utf-8")}

    # ── Conversation ──────────────────────────────────────

    @router.get("/persons/{name}/conversation")
    async def get_conversation(name: str, person=Depends(get_person)):
        """View current conversation state."""
        conv = ConversationMemory(person.person_dir, person.model_config)
        state = conv.load()
        return {
            "person": name,
            "total_turn_count": state.total_turn_count,
            "raw_turns": len(state.turns),
            "compressed_turn_count": state.compressed_turn_count,
            "has_summary": bool(state.compressed_summary),
            "summary_preview": (
                state.compressed_summary[:300]
                if state.compressed_summary
                else ""
            ),
            "total_token_estimate": state.total_token_estimate,
            "turns": [
                {
                    "role": t.role,
                    "content": (
                        t.content[:200] + "..."
                        if len(t.content) > 200
                        else t.content
                    ),
                    "timestamp": t.timestamp,
                    "token_estimate": t.token_estimate,
                }
                for t in state.turns
            ],
        }

    @router.get("/persons/{name}/conversation/full")
    async def get_conversation_full(
        name: str, limit: int = 50, offset: int = 0,
        person=Depends(get_person),
    ):
        """View full conversation history (not truncated)."""
        conv = ConversationMemory(person.person_dir, person.model_config)
        state = conv.load()

        total = len(state.turns)
        end = max(0, total - offset)
        start = max(0, end - limit)
        paginated = state.turns[start:end]

        return {
            "person": name,
            "total_turn_count": state.total_turn_count,
            "raw_turns": total,
            "compressed_turn_count": state.compressed_turn_count,
            "has_summary": bool(state.compressed_summary),
            "compressed_summary": state.compressed_summary or "",
            "total_token_estimate": state.total_token_estimate,
            "turns": [
                {
                    "role": t.role,
                    "content": t.content,
                    "timestamp": t.timestamp,
                    "token_estimate": t.token_estimate,
                }
                for t in paginated
            ],
        }

    @router.delete("/persons/{name}/conversation")
    async def clear_conversation(name: str, person=Depends(get_person)):
        """Clear conversation history for a fresh start."""
        conv = ConversationMemory(person.person_dir, person.model_config)
        conv.clear()
        return {"status": "cleared", "person": name}

    @router.post("/persons/{name}/conversation/compress")
    async def compress_conversation(name: str, person=Depends(get_person)):
        """Manually trigger conversation compression."""
        conv = ConversationMemory(person.person_dir, person.model_config)
        compressed = await conv.compress_if_needed()
        state = conv.load()
        return {
            "compressed": compressed,
            "person": name,
            "total_turn_count": state.total_turn_count,
            "total_token_estimate": state.total_token_estimate,
        }

    return router
