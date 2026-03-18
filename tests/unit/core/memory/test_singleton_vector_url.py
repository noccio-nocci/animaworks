# AnimaWorks - Digital Anima Framework
# Copyright (C) 2026 AnimaWorks Authors
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for get_vector_store() when ANIMAWORKS_VECTOR_URL is set."""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from core.memory.rag.http_store import HttpVectorStore
from core.memory.rag.singleton import _reset_for_testing, get_vector_store


@pytest.fixture(autouse=True)
def _reset_singletons():
    """Reset singletons before and after each test for isolation."""
    _reset_for_testing()
    yield
    _reset_for_testing()


def test_returns_http_store_when_env_set():
    """When ANIMAWORKS_VECTOR_URL is set, get_vector_store returns HttpVectorStore."""
    with patch.dict(os.environ, {"ANIMAWORKS_VECTOR_URL": "http://localhost:18500/api/internal/vector"}):
        store = get_vector_store("test_anima")
        assert store is not None
        assert isinstance(store, HttpVectorStore)
        assert store._anima_name == "test_anima"
        assert store._base_url == "http://localhost:18500/api/internal/vector"


def test_returns_chroma_store_when_env_not_set():
    """When ANIMAWORKS_VECTOR_URL is NOT set, get_vector_store returns ChromaVectorStore (or mock)."""
    os.environ.pop("ANIMAWORKS_VECTOR_URL", None)
    mock_chroma = MagicMock()

    with patch("core.memory.rag.store.ChromaVectorStore", return_value=mock_chroma):
        store = get_vector_store("test_anima")

    assert store is not None
    assert not isinstance(store, HttpVectorStore)
    assert store is mock_chroma


def test_returns_none_when_chroma_init_fails():
    """When ChromaVectorStore init fails, get_vector_store returns None."""
    os.environ.pop("ANIMAWORKS_VECTOR_URL", None)

    with patch("core.memory.rag.store.ChromaVectorStore", side_effect=RuntimeError("ChromaDB init failed")):
        store = get_vector_store("test_anima")

    assert store is None
