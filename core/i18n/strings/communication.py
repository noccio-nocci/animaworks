# AnimaWorks - Digital Anima Framework
# Copyright (C) 2026 AnimaWorks Authors
# SPDX-License-Identifier: Apache-2.0
#
# This file is part of AnimaWorks core/server, licensed under Apache-2.0.
# See LICENSE for the full license text.

"""Domain-specific i18n strings."""

from __future__ import annotations

STRINGS: dict[str, dict[str, str]] = {
    "inbox.reply_placeholder": {
        "ja": "{返信内容}",
        "en": "{reply_content}",
    },
    "messenger.depth_exceeded": {
        "ja": "ConversationDepthExceeded: {to}との会話が10分間に6ターンに達しました。次のハートビートサイクルまでお待ちください",
        "en": (
            "ConversationDepthExceeded: Conversation with {to} reached 6 turns in 10 minutes. Please wait until the next heartbeat cycle."
        ),
    },
    "messenger.more_count": {
        "ja": "(+{count}件)",
        "en": "(+{count} more)",
    },
    "messenger.read_receipt": {
        "ja": "[既読通知] {count}件のメッセージを受信しました: {summary}",
        "en": "[Read receipt] Received {count} messages: {summary}",
    },
}
