from __future__ import annotations

# AnimaWorks - Digital Anima Framework
# Copyright (C) 2026 AnimaWorks Authors
# SPDX-License-Identifier: Apache-2.0
#
# This file is part of AnimaWorks core/server, licensed under Apache-2.0.
# See LICENSE for the full license text.

"""Task queue and submit_tasks tool schemas."""

from typing import Any

from core.i18n import t as _t

SUBMIT_TASKS_TOOLS: list[dict[str, Any]] = [
    {
        "name": "submit_tasks",
        "description": (
            "Submit multiple tasks as a DAG for parallel/serial execution. "
            "Independent tasks with parallel=true run concurrently. "
            "Tasks with depends_on wait for all listed tasks to complete. "
            "Results from completed dependencies are automatically injected "
            "into dependent task context."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "batch_id": {
                    "type": "string",
                    "description": "Unique identifier for this batch of tasks",
                },
                "tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "parallel": {"type": "boolean", "default": False},
                            "depends_on": {
                                "type": "array",
                                "items": {"type": "string"},
                                "default": [],
                            },
                            "acceptance_criteria": {
                                "type": "array",
                                "items": {"type": "string"},
                                "default": [],
                            },
                            "constraints": {
                                "type": "array",
                                "items": {"type": "string"},
                                "default": [],
                            },
                            "file_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "default": [],
                            },
                            "context": {
                                "type": "string",
                                "description": "Background context for the task executor",
                                "default": "",
                            },
                            "reply_to": {
                                "type": "string",
                                "description": "Name of the Anima to notify on completion (default: submitter)",
                            },
                            "workspace": {
                                "type": "string",
                                "description": "Workspace alias or alias#hash for the task's working directory",
                                "default": "",
                            },
                        },
                        "required": ["task_id", "title", "description"],
                    },
                    "minItems": 1,
                },
            },
            "required": ["batch_id", "tasks"],
        },
    },
]


def _task_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": "backlog_task",
            "description": _t("schema.backlog_task.desc"),
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "enum": ["human", "anima"],
                        "description": _t("schema.backlog_task.source"),
                    },
                    "original_instruction": {
                        "type": "string",
                        "description": _t("schema.backlog_task.original_instruction"),
                    },
                    "assignee": {
                        "type": "string",
                        "description": _t("schema.backlog_task.assignee"),
                    },
                    "summary": {
                        "type": "string",
                        "description": _t("schema.backlog_task.summary"),
                    },
                    "deadline": {
                        "type": "string",
                        "description": _t("schema.backlog_task.deadline"),
                    },
                    "relay_chain": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": _t("schema.backlog_task.relay_chain"),
                    },
                },
                "required": ["source", "original_instruction", "assignee", "summary", "deadline"],
            },
        },
        {
            "name": "update_task",
            "description": _t("schema.update_task.desc"),
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": _t("schema.update_task.task_id"),
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "done", "cancelled", "blocked", "failed"],
                        "description": _t("schema.update_task.status"),
                    },
                    "summary": {
                        "type": "string",
                        "description": _t("schema.update_task.summary"),
                    },
                },
                "required": ["task_id", "status"],
            },
        },
        {
            "name": "list_tasks",
            "description": _t("schema.list_tasks.desc"),
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "done", "cancelled", "blocked", "failed", "delegated"],
                        "description": _t("schema.list_tasks.status"),
                    },
                    "detail": {
                        "type": "boolean",
                        "description": _t("schema.list_tasks.detail"),
                    },
                },
            },
        },
    ]
