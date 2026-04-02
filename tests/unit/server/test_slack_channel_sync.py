from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from core.messenger import ChannelMeta, load_channel_meta, save_channel_meta
from server.slack_channel_sync import SlackChannelSync


class _FakeSlackManager:
    def __init__(self, app_map: dict[str, object]) -> None:
        self._app_map = app_map


def _mock_config() -> SimpleNamespace:
    return SimpleNamespace(
        external_messaging=SimpleNamespace(
            slack=SimpleNamespace(default_anima="sakura", board_mapping={}),
        ),
    )


@pytest.mark.asyncio
async def test_sync_marks_missing_slack_channel_and_skips_reverse_recreate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    shared_dir = tmp_path / "shared"
    channels_dir = shared_dir / "channels"
    channels_dir.mkdir(parents=True)
    (channels_dir / "general.jsonl").write_text("", encoding="utf-8")

    cfg = _mock_config()
    save_calls: list[object] = []

    monkeypatch.setattr("server.slack_channel_sync.get_shared_dir", lambda: shared_dir)
    monkeypatch.setattr("server.slack_socket.SlackSocketModeManager", _FakeSlackManager)

    async def _list_public_channels(_token: str):
        return []

    monkeypatch.setattr("server.slack_channel_sync._list_public_channels", _list_public_channels)

    async def _create_channel(*_args, **_kwargs):
        raise AssertionError("deleted Slack channel should not be recreated")

    monkeypatch.setattr("server.slack_channel_sync._create_channel", _create_channel)
    monkeypatch.setattr("server.slack_channel_sync._join_channel_if_needed", lambda *_a, **_k: False)
    monkeypatch.setattr("core.config.models.load_config", lambda: cfg)
    monkeypatch.setattr("core.config.models.save_config", lambda updated: save_calls.append(updated))

    manager = _FakeSlackManager(
        {"sakura": SimpleNamespace(client=SimpleNamespace(token="xoxb-sakura"))},
    )
    sync = SlackChannelSync()
    sync.board_mapping = {"C123": "general"}

    await sync.sync(manager)

    meta = load_channel_meta(shared_dir, "general")
    assert meta is not None
    assert meta.slack_sync_disabled is True
    assert meta.slack_deleted_at
    assert sync.board_mapping == {}
    assert save_calls


@pytest.mark.asyncio
async def test_sync_clears_tombstone_when_slack_channel_returns(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    shared_dir = tmp_path / "shared"
    channels_dir = shared_dir / "channels"
    channels_dir.mkdir(parents=True)
    (channels_dir / "general.jsonl").write_text("", encoding="utf-8")
    save_channel_meta(
        shared_dir,
        "general",
        ChannelMeta(
            members=[],
            slack_sync_disabled=True,
            slack_deleted_at="2026-04-02T00:00:00+00:00",
        ),
    )

    cfg = _mock_config()
    monkeypatch.setattr("server.slack_channel_sync.get_shared_dir", lambda: shared_dir)
    monkeypatch.setattr("server.slack_socket.SlackSocketModeManager", _FakeSlackManager)

    async def _list_public_channels(_token: str):
        return [{"id": "C999", "name": "general", "is_private": False}]

    async def _join_channel_if_needed(*_args, **_kwargs):
        return False

    async def _create_channel(*_args, **_kwargs):
        raise AssertionError("existing Slack channel should not be recreated")

    monkeypatch.setattr("server.slack_channel_sync._list_public_channels", _list_public_channels)
    monkeypatch.setattr("server.slack_channel_sync._join_channel_if_needed", _join_channel_if_needed)
    monkeypatch.setattr("server.slack_channel_sync._create_channel", _create_channel)
    monkeypatch.setattr("core.config.models.load_config", lambda: cfg)
    monkeypatch.setattr("core.config.models.save_config", lambda _updated: None)

    manager = _FakeSlackManager(
        {"sakura": SimpleNamespace(client=SimpleNamespace(token="xoxb-sakura"))},
    )
    sync = SlackChannelSync()

    await sync.sync(manager)

    meta = load_channel_meta(shared_dir, "general")
    assert meta is not None
    assert meta.slack_sync_disabled is False
    assert meta.slack_deleted_at == ""
    assert sync.board_mapping == {"C999": "general"}
