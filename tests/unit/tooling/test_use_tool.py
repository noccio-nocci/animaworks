"""Tests for core.tooling.handler — _handle_use_tool and USE_TOOL schema."""
# AnimaWorks - Digital Anima Framework
# Copyright (C) 2026 AnimaWorks Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from core.tooling.handler import ToolHandler
from core.tooling.schemas import USE_TOOL


# ── Fixtures ──────────────────────────────────────────────────


@pytest.fixture
def anima_dir(tmp_path: Path) -> Path:
    d = tmp_path / "animas" / "test-anima"
    d.mkdir(parents=True)
    (d / "permissions.md").write_text("", encoding="utf-8")
    return d


@pytest.fixture
def memory(anima_dir: Path) -> MagicMock:
    m = MagicMock()
    m.read_permissions.return_value = ""
    m.search_memory_text.return_value = []
    return m


@pytest.fixture
def handler(anima_dir: Path, memory: MagicMock) -> ToolHandler:
    return ToolHandler(
        anima_dir=anima_dir,
        memory=memory,
        messenger=None,
        tool_registry=[],
    )


@pytest.fixture
def handler_with_web_search(anima_dir: Path, memory: MagicMock) -> ToolHandler:
    """Handler with web_search in registry for dispatch tests."""
    return ToolHandler(
        anima_dir=anima_dir,
        memory=memory,
        messenger=None,
        tool_registry=["web_search"],
    )


# ── test_use_tool_requires_tool_name_and_action ──────────────


class TestUseToolRequiresToolNameAndAction:
    """Missing tool_name or action returns error."""

    def test_missing_tool_name(self, handler: ToolHandler):
        result = handler.handle(
            "use_tool",
            {"tool_name": "", "action": "search", "args": {}},
        )
        parsed = json.loads(result)
        assert parsed["status"] == "error"
        assert "tool_name" in parsed.get("message", parsed.get("error_type", ""))
        assert "action" in parsed.get("message", parsed.get("error_type", ""))

    def test_missing_action(self, handler: ToolHandler):
        result = handler.handle(
            "use_tool",
            {"tool_name": "web_search", "action": "", "args": {}},
        )
        parsed = json.loads(result)
        assert parsed["status"] == "error"
        assert "tool_name" in parsed.get("message", parsed.get("error_type", ""))
        assert "action" in parsed.get("message", parsed.get("error_type", ""))

    def test_both_missing(self, handler: ToolHandler):
        result = handler.handle("use_tool", {"args": {}})
        parsed = json.loads(result)
        assert parsed["status"] == "error"


# ── test_use_tool_rejects_unpermitted_tool ────────────────────


class TestUseToolRejectsUnpermittedTool:
    """Tool not in registry returns permission error."""

    def test_tool_not_in_registry_or_personal(self, handler: ToolHandler):
        result = handler.handle(
            "use_tool",
            {
                "tool_name": "forbidden_tool",
                "action": "do_something",
                "args": {},
            },
        )
        parsed = json.loads(result)
        assert parsed["status"] == "error"
        assert "permitted" in parsed.get("message", "").lower() or "permission" in parsed.get("message", "").lower()
        assert "forbidden_tool" in parsed.get("message", "")


# ── test_use_tool_rejects_unknown_module ──────────────────────


class TestUseToolRejectsUnknownModule:
    """Tool in registry but not in TOOL_MODULES returns error."""

    def test_tool_in_registry_not_in_tool_modules(
        self, handler_with_web_search: ToolHandler, anima_dir: Path,
    ):
        """Registry has web_search but TOOL_MODULES excludes it → unknown module."""
        with patch("core.tools.TOOL_MODULES", {"other_tool": "core.tools.other"}):
            result = handler_with_web_search.handle(
                "use_tool",
                {
                    "tool_name": "web_search",
                    "action": "search",
                    "args": {"query": "test"},
                },
            )
        parsed = json.loads(result)
        assert parsed["status"] == "error"
        assert "Unknown tool module" in parsed.get("message", "") or "web_search" in parsed.get("message", "")


# ── test_use_tool_dispatches_correctly ────────────────────────


class TestUseToolDispatchesCorrectly:
    """Correct tool_name+action constructs schema_name and calls dispatch."""

    def test_dispatches_with_correct_schema_name(
        self, handler_with_web_search: ToolHandler, anima_dir: Path,
    ):
        mock_call = MagicMock(return_value='{"results": []}')
        mock_mod = MagicMock()
        mock_mod.dispatch = mock_call

        with patch("core.tools.TOOL_MODULES", {"web_search": "core.tools.web_search"}), \
             patch("importlib.import_module", return_value=mock_mod):
            result = handler_with_web_search.handle(
                "use_tool",
                {
                    "tool_name": "web_search",
                    "action": "search",
                    "args": {"query": "test query"},
                },
            )

        assert "results" in result
        mock_call.assert_called_once()
        call_args = mock_call.call_args
        assert call_args[0][0] == "web_search_search"
        assert call_args[0][1]["query"] == "test query"
        assert "anima_dir" in call_args[0][1]


# ── test_use_tool_passes_args_with_anima_dir ───────────────────


class TestUseToolPassesArgsWithAnimaDir:
    """Args include anima_dir."""

    def test_dispatch_args_include_anima_dir(
        self, handler_with_web_search: ToolHandler, anima_dir: Path,
    ):
        mock_dispatch = MagicMock(return_value="ok")
        mock_mod = MagicMock()
        mock_mod.dispatch = mock_dispatch

        with patch("core.tools.TOOL_MODULES", {"web_search": "core.tools.web_search"}), \
             patch("importlib.import_module", return_value=mock_mod):
            handler_with_web_search.handle(
                "use_tool",
                {
                    "tool_name": "web_search",
                    "action": "search",
                    "args": {"query": "x", "limit": 5},
                },
            )

        mock_dispatch.assert_called_once()
        dispatch_args = mock_dispatch.call_args[0][1]
        assert dispatch_args["anima_dir"] == str(anima_dir)
        assert dispatch_args["query"] == "x"
        assert dispatch_args["limit"] == 5


# ── test_use_tool_handles_dispatch_exception ──────────────────


class TestUseToolHandlesDispatchException:
    """Exception during dispatch returns error."""

    def test_exception_during_dispatch_returns_error(
        self, handler_with_web_search: ToolHandler,
    ):
        """Exception during import or dispatch returns structured error."""
        with patch("core.tools.TOOL_MODULES", {"web_search": "core.tools.web_search"}), \
             patch(
                 "importlib.import_module",
                 side_effect=ImportError("module not found"),
             ):
            result = handler_with_web_search.handle(
                "use_tool",
                {
                    "tool_name": "web_search",
                    "action": "search",
                    "args": {},
                },
            )

        parsed = json.loads(result)
        assert parsed["status"] == "error"
        msg = parsed.get("message", "")
        assert "use_tool execution failed" in msg or "module not found" in msg
        assert "web_search" in msg
        assert "search" in msg


# ── test_use_tool_schema_definition ────────────────────────────


class TestUseToolSchemaDefinition:
    """USE_TOOL schema has correct structure."""

    def test_use_tool_schema_exists(self):
        assert len(USE_TOOL) >= 1
        schema = USE_TOOL[0]

    def test_schema_has_name(self):
        schema = USE_TOOL[0]
        assert schema["name"] == "use_tool"

    def test_schema_has_description(self):
        schema = USE_TOOL[0]
        assert "description" in schema
        assert len(schema["description"]) > 0

    def test_schema_has_parameters(self):
        schema = USE_TOOL[0]
        assert "parameters" in schema
        params = schema["parameters"]
        assert "properties" in params
        assert "tool_name" in params["properties"]
        assert "action" in params["properties"]
        assert "args" in params["properties"]

    def test_schema_required_fields(self):
        schema = USE_TOOL[0]
        required = schema["parameters"].get("required", [])
        assert "tool_name" in required
        assert "action" in required
