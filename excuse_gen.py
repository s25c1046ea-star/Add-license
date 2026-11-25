# Copyright (c) 2026 Your Name
# SPDX-License-Identifier: MIT
"""Generate formatted excuse lines from situation memos read from stdin."""

from __future__ import annotations

import argparse
import json
import random
import sys
from typing import Sequence

TEMPLATES: dict[str, list[str]] = {
    "mild": [
        "{topic}の対応に手間取り、予定より少し遅れてしまいました。",
        "{topic}の確認作業が長引いたため、ご連絡が遅くなりました。",
        "{topic}の段取りを見直していたところ、時間がかかってしまいました。",
        "{topic}の関連資料を突き合わせていたら、思いのほか時間を要しました。",
    ],
    "dramatic": [
        "{topic}を巡る予期せぬ事態が重なり、時空の狭間で足止めを食らいました。",
        "{topic}の解決に全力を注いだ結果、気づけば時計の針が大きく進んでいました。",
        "{topic}の難局を突破するため極限の集中を要し、報告が遅延しました。",
        "{topic}にまつわる不可解なトラブルが連鎖し、復旧に時間を奪われました。",
    ],
}