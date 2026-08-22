# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-b81f37a0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""龍魂信任核心 · 史官审计日志（jsonl，只增不删）。

所有条目 append-only；废止用 freeze 标记，绝不物理删除。
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from .dna import generate_dna


class AuditLog:
    """append-only 审计日志：每行一条 JSON，写入即 flush+fsync。"""

    def __init__(self, name: str, base_dir: Path | None = None) -> None:
        """初始化审计日志。

        :param name: 日志名，文件为 ``<base_dir>/<name>.jsonl``。
        :param base_dir: 日志目录；默认
            ``Path(os.environ.get("LONGHUN_HOME", Path.home()/".longhun"))/"04_AUDIT"``。
            目录不存在时自动创建。
        """
        if base_dir is None:
            base_dir = (
                Path(os.environ.get("LONGHUN_HOME", Path.home() / ".longhun"))
                / "04_AUDIT"
            )
        self.base_dir: Path = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.path: Path = self.base_dir / f"{name}.jsonl"

    def _append(self, entry: dict) -> dict:
        """追加一行 JSON 并 flush+fsync，确保持久化。

        :param entry: 待写入的条目。
        :return: 原样返回 entry。
        """
        line = json.dumps(entry, ensure_ascii=False)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        return entry

    def log(self, event: str, details: dict) -> dict:
        """记录一条审计事件。

        条目结构：``{timestamp(iso), event, details, dna}``，
        其中 dna = ``generate_dna("AUDIT")``。

        :param event: 事件名。
        :param details: 事件细节字典。
        :return: 写入的条目。
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details,
            "dna": generate_dna("AUDIT"),
        }
        return self._append(entry)

    def read_all(self) -> list[dict]:
        """读取全部审计条目（按写入顺序）。

        :return: 条目列表；文件不存在时返回空列表。
        """
        if not self.path.exists():
            return []
        entries: list[dict] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                entries.append(json.loads(line))
        return entries

    def freeze(self, reason: str, target: dict | None = None) -> dict:
        """追加 FREEZE 废止标记，不删除任何既有行。

        :param reason: 废止原因。
        :param target: 被废止的目标条目（可选）。
        :return: 写入的 FREEZE 条目。
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "FREEZE",
            "reason": reason,
            "target": target,
        }
        return self._append(entry)
