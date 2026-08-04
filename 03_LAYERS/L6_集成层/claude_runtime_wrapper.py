#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude 运行时包装器 v3.0 — CNSH 中文命名版
DNA: #龍芯⚡️2026-06-29-CLAUDE-RUNTIME-v3-CNSH-UID9622
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Optional

# 将项目根目录加入路径，确保能导入同级模块
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from longhun_shield_cnsh import 龍魂护盾
from longhun_notion_dashboard import LongHunNotionDashboard

HOME = Path.home()
MEMORY_PATH = HOME / ".longhun" / "memory" / "latest_digest.md"
TIMELINE_DIR = HOME / ".longhun" / "timeline"
TIMELINE_PATH = TIMELINE_DIR / "claude_runtime.jsonl"

SHIELD_DNA = "#龍芯⚡️2026-06-29-龍魂护盾-v3-CNSH-UID9622"


def _设置护盾环境默认值() -> None:
    """避免龍魂护盾因 /var/lib 权限失败，使用 ~/.longhun/... 作为默认值。"""
    默认值 = {
        "LONGHUN_BAN_DRY_RUN": "1",
        "LONGHUN_SHAME_WALL_PATH": str(HOME / ".longhun" / "shield" / "shame_wall.jsonl"),
        "LONGHUN_SM2_SK": str(HOME / ".longhun" / "shield" / "sm2" / "sk.pem"),
        "LONGHUN_SM2_PK": str(HOME / ".longhun" / "shield" / "sm2" / "pk.pem"),
    }
    for 键, 值 in 默认值.items():
        if not os.environ.get(键):
            os.environ[键] = 值


_设置护盾环境默认值()


def _生成脱氧核糖核酸(窗口标识: str) -> str:
    """生成包含 UID9622 与窗口标识的 Window DNA。"""
    时间戳 = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    随机盐 = uuid.uuid4().hex[:8].upper()
    原料 = f"{时间戳}-{窗口标识}-{随机盐}-UID9622"
    哈希 = hashlib.sha256(原料.encode("utf-8")).hexdigest()[:16].upper()
    return f"#龍芯⚡️{时间戳}-CLAUDE-RUNTIME-{窗口标识}-UID9622-{哈希}"


def _当前时间戳() -> str:
    return datetime.now(timezone.utc).isoformat()


class ClaudeRuntime:
    """Claude 运行时包装器：负责 LU 禁止规则检查、记忆恢复、调用转发、审计留痕。"""

    def __init__(self, window_id: str):
        self.窗口标识 = window_id
        self.窗口脱氧核糖核酸 = _生成脱氧核糖核酸(window_id)
        self.记忆上下文 = self._restore_previous_memory()
        self.notion仪表盘: Optional[LongHunNotionDashboard] = None
        self.timeline路径 = TIMELINE_PATH

    def _check_forbidden(self, content: str) -> Dict[str, Any]:
        """使用龍魂护盾检查内容是否触发 LU 禁止规则。"""
        护盾 = 龍魂护盾(SHIELD_DNA)
        return 护盾.检查人工智能(self.窗口脱氧核糖核酸, content)

    def _restore_previous_memory(self) -> str:
        """读取 ~/.longhun/memory/latest_digest.md；不存在时创建占位摘要。"""
        if not MEMORY_PATH.exists():
            MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
            占位 = (
                "# Claude Runtime 占位记忆摘要\n\n"
                "- 记忆更新时间：" + _当前时间戳() + "\n"
                "- 本文件由 ClaudeRuntime 自动生成，因原摘要尚未就绪。\n"
            )
            MEMORY_PATH.write_text(占位, encoding="utf-8")
        return MEMORY_PATH.read_text(encoding="utf-8")

    def _write_to_timeline(self, snapshot: Dict[str, Any]) -> None:
        """append-only 写入 Timeline JSONL。"""
        self.timeline路径.parent.mkdir(parents=True, exist_ok=True)
        with open(self.timeline路径, "a", encoding="utf-8") as f:
            f.write(json.dumps(snapshot, ensure_ascii=False) + "\n")

    def _sync_to_notion(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """若环境变量就绪，同步快照到 Notion Timeline 数据库。"""
        令牌 = os.environ.get("NOTION_TOKEN")
        父页面 = os.environ.get("LONGHUN_NOTION_PARENT_PAGE")
        if not 令牌 or not 父页面:
            return {"ok": False, "reason": "缺少 NOTION_TOKEN 或 LONGHUN_NOTION_PARENT_PAGE"}

        if self.notion仪表盘 is None:
            self.notion仪表盘 = LongHunNotionDashboard(token=令牌, parent_page_id=父页面)
            self.notion仪表盘.init_dashboard()

        输入摘要 = snapshot.get("input", "")[:500]
        输出摘要 = snapshot.get("output", "")[:500]
        return self.notion仪表盘.add_timeline_event(
            window_id=snapshot.get("window_id", self.窗口标识),
            title=f"Claude 事件 [{self.窗口标识}]",
            input_summary=输入摘要,
            output_summary=输出摘要,
            dna=snapshot.get("dna", self.窗口脱氧核糖核酸),
        )

    def _调用克劳德(
        self,
        user_input: str,
        memory: str,
        call_claude_fn: Optional[Callable[[str, str], str]] = None,
    ) -> str:
        """优先使用外部回调，其次 anthropic SDK，最后 mock。"""
        if call_claude_fn is not None:
            return call_claude_fn(user_input, memory)

        if os.environ.get("ANTHROPIC_API_KEY"):
            try:
                import anthropic
                客户端 = anthropic.Anthropic()
                响应 = 客户端.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    system=memory,
                    messages=[{"role": "user", "content": user_input}],
                )
                return str(响应.content[0].text)
            except Exception as e:
                return f"[anthropic SDK 调用失败，转入 mock 模式] 错误：{e}"

        return (
            f"[mock] 已收到输入：{user_input[:80]}...\n"
            "当前为 mock 模式，未配置 ANTHROPIC_API_KEY，也未提供 call_claude_fn。"
        )

    def execute(
        self,
        user_input: str,
        call_claude_fn: Optional[Callable[[str, str], str]] = None,
    ) -> Dict[str, Any]:
        """
        执行流程：
        1. FORBIDDEN 检查；
        2. 恢复记忆；
        3. 调用 Claude；
        4. 生成 snapshot；
        5. 写入 Timeline；
        6. 同步 Notion（可选）。
        """
        # 1. FORBIDDEN 检查
        检查结果 = self._check_forbidden(user_input)
        if not 检查结果.get("通过", True):
            拒绝快照 = {
                "input": user_input,
                "output": {
                    "mode": "rejected",
                    "shield_result": 检查结果,
                    "message": 检查结果.get("消息", "请求被 LU 禁止规则拦截。"),
                },
                "dna": self.窗口脱氧核糖核酸,
                "timestamp": _当前时间戳(),
                "window_id": self.窗口标识,
            }
            self._write_to_timeline(拒绝快照)
            self._sync_to_notion(拒绝快照)
            return {
                "ok": False,
                "mode": "forbidden",
                "shield_result": 检查结果,
                "snapshot": 拒绝快照,
            }

        # 2. 恢复记忆
        记忆 = self._restore_previous_memory()

        # 3. 调用 Claude
        输出 = self._调用克劳德(user_input, 记忆, call_claude_fn)

        # 4. 生成 snapshot
        快照 = {
            "input": user_input,
            "output": 输出,
            "dna": self.窗口脱氧核糖核酸,
            "timestamp": _当前时间戳(),
            "window_id": self.窗口标识,
        }

        # 5. 写入 Timeline
        self._write_to_timeline(快照)

        # 6. 同步 Notion（仅当环境变量存在）
        notion结果 = self._sync_to_notion(快照)

        return {
            "ok": True,
            "mode": "claude" if os.environ.get("ANTHROPIC_API_KEY") or call_claude_fn else "mock",
            "output": 输出,
            "snapshot": 快照,
            "notion": notion结果,
        }


def main() -> int:
    """演示函数：默认使用 mock 模式调用一次。"""
    print("=== Claude 运行时包装器 v3.0 ===")
    运行时 = ClaudeRuntime(window_id="demo-window")
    print(f"Window DNA: {运行时.窗口脱氧核糖核酸}")
    结果 = 运行时.execute("你好，龍魂系统。请简述 LU v3.0 的核心原则。")
    print(json.dumps(结果, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
