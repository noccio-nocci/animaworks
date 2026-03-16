# AnimaWorks - Digital Anima Framework
# Copyright (C) 2026 AnimaWorks Authors
# SPDX-License-Identifier: Apache-2.0
#
# This file is part of AnimaWorks core/server, licensed under Apache-2.0.
# See LICENSE for the full license text.

"""Lightweight i18n support for runtime strings."""

from __future__ import annotations

import logging

from core.i18n.strings import _merge_strings

logger = logging.getLogger(__name__)

_STRINGS: dict[str, dict[str, str]] = _merge_strings()


class _SafeFormatDict(dict):
    """Dict that returns ``{key}`` for missing keys during format_map."""

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def t(key: str, locale: str | None = None, **kwargs: object) -> str:
    """Get localized string with optional format args.

    Args:
        key: Dot-separated key (e.g. "handler.not_subordinate").
        locale: Override locale. If None, uses config.locale.
        **kwargs: Values to substitute into {placeholder} in the template.

    Returns:
        Localized string. Falls back to en, then ja, then key if not found.
    """
    from core.paths import _get_locale

    loc = locale or _get_locale()
    if not isinstance(loc, str) or loc not in ("ja", "en", "zh", "ko"):
        loc = "ja"
    entry = _STRINGS.get(key, {})
    template = entry.get(loc) or entry.get("en") or entry.get("ja", key)
    if kwargs:
        return template.format_map(_SafeFormatDict({k: str(v) for k, v in kwargs.items()}))
    return template


__all__ = ["t", "_STRINGS", "_SafeFormatDict"]
