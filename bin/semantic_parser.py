#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 龍魂·语义解析引擎 — 自然语言→命令映射 + 语义回显确认
DNA: #龍芯⚡️2026-07-06-SEMANTIC-PARSER-v1.0

功能:
- 自然语言 → lh6 命令映射（本地匹配表 + Kimi/MiniMax API fallback）
- 命令执行前语义回显确认
- 本地缓存常用命令映射表（API不可用时的降级方案）

用法:
  python3 bin/semantic_parser.py "检查共生体服务状态"
  python3 bin/semantic_parser.py "临时放行 github.com"
  python3 bin/semantic_parser.py --echo "语义解析结果..." --cmd "lh6 status symbiote"
"""

import json
import os
import sys
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Tuple, Dict
from datetime import datetime, timezone

DNA = "#龍芯⚡️2026-07-06-SEMANTIC-PARSER-v1.0"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = Path.home() / ".longhun" / "semantic"
CACHE_FILE = CACHE_DIR / "command_map.json"

# ── 本地命令映射表（API不可用时的降级方案）──
LOCAL_COMMAND_MAP = {
    # 状态查询
    "检查共生体服务状态": "lh6 status symbiote",
    "查看共生体状态": "lh6 status symbiote",
    "共生体状态": "lh6 status symbiote",
    "系统状态": "lh6 status",
    "查看状态": "lh6 status",
    "服务状态": "lh6 status",

    # 部署
    "校验plist文件": "lh6 validate plist",
    "检查plist": "lh6 validate plist",
    "plist校验": "lh6 validate plist",

    # 熔断
    "临时放行": "lh6 fuse override",
    "临时放行 github.com": "lh6 fuse override github.com --duration 1h",
    "阻断 github": "lh6 fuse block github.com --level HARD",
    "解除阻断": "lh6 fuse unblock",
    "熔断状态": "lh6 fuse status",
    "查看熔断": "lh6 fuse status",
    "全局熔断": "lh6 fuse trip",
    "重置熔断": "lh6 fuse reset",

    # 令牌
    "令牌状态": "lh6 token status",
    "查看令牌": "lh6 token status",
    "续期令牌": "lh6 token renew",
    "令牌续期": "lh6 token renew",

    # 编辑器
    "打开编辑器": "lh6 editor",
    "启动编辑器": "lh6 editor",
    "中文编辑器": "lh6 editor",

    # 审计
    "变量审计": "lh6 audit-vars",
    "审计变量": "lh6 audit-vars",
    "查看审计日志": "lh6 fuse audit",
    "审计日志": "lh6 fuse audit",

    # 其他
    "打开仪表盘": "open http://127.0.0.1:9627/symbiote",
    "查看仪表盘": "open http://127.0.0.1:9627/symbiote",
    "显示帮助": "lh6 help",
    "帮助": "lh6 help",
    "生成推送令牌": "lh6 fuse push-confirm",
    "推送确认": "lh6 fuse push-confirm",
}

# ── 正则模式匹配（更灵活的模糊匹配）──
FUZZY_PATTERNS = [
    (r".*(检查|查看|查询).*(共生体|symbiote|服务).*(状态|status).*", "lh6 status symbiote"),
    (r".*(状态|status).*(共生体|symbiote|服务).*", "lh6 status symbiote"),
    (r".*(check|status).*symbiote.*", "lh6 status symbiote"),
    (r".*(临时|暂时).*(放行|开放|允许).*([a-zA-Z0-9.\-]+).*", lambda m: f"lh6 fuse override {m.group(3)} --duration 1h"),
    (r".*(阻断|封禁|禁止).*([a-zA-Z0-9.\-]+).*", lambda m: f"lh6 fuse block {m.group(2)} --level HARD"),
    (r".*(解除|取消).*(阻断|封禁).*([a-zA-Z0-9.\-]+).*", lambda m: f"lh6 fuse unblock {m.group(3)}"),
    (r".*(校验|检查|验证).*plist.*", "lh6 validate plist"),
    (r".*(打开|启动).*编辑.*", "lh6 editor"),
    (r".*(审计|检查).*变量.*", "lh6 audit-vars"),
    (r".*(令牌|token).*(状态|查看).*", "lh6 token status"),
    (r".*(令牌|token).*(续期|更新).*", "lh6 token renew"),
    (r".*(熔断).*(状态|查看).*", "lh6 fuse status"),
    (r".*仪表盘.*", "open http://127.0.0.1:9627/symbiote"),
    (r".*帮助.*", "lh6 help"),
    (r".*(生成|创建).*(推送|push).*(令牌|token).*", "lh6 fuse push-confirm"),
]


def local_match(text: str) -> Optional[str]:
    """本地匹配：精确 → 模糊正则 → None"""
    # 1. 精确匹配
    if text in LOCAL_COMMAND_MAP:
        return LOCAL_COMMAND_MAP[text]

    # 2. 模糊正则匹配
    for pattern, target in FUZZY_PATTERNS:
        m = re.match(pattern, text, re.IGNORECASE)
        if m:
            if callable(target):
                return target(m)
            return target

    return None


def load_cache() -> Dict:
    """加载命令映射缓存"""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"mappings": LOCAL_COMMAND_MAP.copy(), "updated": ""}


def save_cache(mappings: Dict):
    """保存命令映射缓存"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    mappings["updated"] = datetime.now(timezone.utc).isoformat()
    with open(CACHE_FILE, "w") as f:
        json.dump(mappings, f, ensure_ascii=False, indent=2)


def kimi_api_parse(text: str) -> Optional[str]:
    """通过 Kimi API 进行语义解析（如果可用）"""
    # 尝试调用本地 Kimi 服务
    kimi_url = "http://127.0.0.1:8000/kimi/parse-command"
    try:
        req = urllib.request.Request(
            kimi_url,
            data=json.dumps({"text": text, "context": "lh6_commands"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            result = json.loads(resp.read())
            return result.get("command")
    except Exception:
        pass

    # 尝试通用 Kimi gateway
    kimi_gateway = PROJECT_ROOT / "kimi" / "kimi_gateway.py"
    if kimi_gateway.exists():
        try:
            import subprocess
            result = subprocess.run(
                ["python3", str(kimi_gateway)],
                input=json.dumps({
                    "action": "parse_command",
                    "text": text,
                    "available_commands": list(LOCAL_COMMAND_MAP.keys()),
                }),
                capture_output=True, text=True, timeout=5,
                cwd=str(PROJECT_ROOT)
            )
            if result.returncode == 0:
                parsed = json.loads(result.stdout)
                return parsed.get("command")
        except Exception:
            pass

    return None


def parse_command(text: str, use_api: bool = False) -> Tuple[Optional[str], str]:
    """
    解析自然语言 → lh6 命令。

    返回：(命令文本, 来源标记)
    """
    # 1. 本地匹配
    local = local_match(text)
    if local:
        return local, "本地匹配"

    # 2. 缓存匹配
    cache = load_cache()
    for key, cmd in cache.get("mappings", {}).items():
        if key in text or text in key:
            return cmd, "缓存匹配"

    # 3. API 解析（如果启用）
    if use_api:
        api_result = kimi_api_parse(text)
        if api_result:
            # 加入缓存
            cache.setdefault("mappings", {})[text] = api_result
            save_cache(cache)
            return api_result, "Kimi API 解析"

    return None, "无法识别"


def echo_confirm(parsed_text: str, command: str, source: str = "本地匹配") -> bool:
    """
    语义回显：展示解析结果，等待用户确认。

    返回：True=确认执行, False=取消
    """
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🧠 龍魂语义解析 · 命令回显确认                           ║
╠═══════════════════════════════════════════════════════════╣
║  用户输入: {parsed_text[:47]}…
║  解析来源: {source: <46}║
║  目标命令: {command[:47]}…
╠═══════════════════════════════════════════════════════════╣
║  输入 y 确认执行 / n 取消                                 ║
╚═══════════════════════════════════════════════════════════╝
""")
    try:
        ans = input("  → ").strip().lower()
        return ans in ("y", "yes", "是", "确认", "执行")
    except (EOFError, KeyboardInterrupt):
        return False


def execute_command(command: str):
    """执行解析后的命令"""
    import subprocess
    print(f"\n▶️ 执行: {command}")
    parts = command.split()
    result = subprocess.run(parts, cwd=str(PROJECT_ROOT))
    return result.returncode


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n用法:")
        print("  python3 bin/semantic_parser.py \"自然语言命令\"     # 解析并回显")
        print("  python3 bin/semantic_parser.py --auto \"命令\"      # 解析后直接执行")
        print("  python3 bin/semantic_parser.py --echo \"结果\" --cmd \"命令\"  # 仅回显")
        sys.exit(0)

    # --echo --cmd 模式（供 lh6 调用）
    if sys.argv[1] == "--echo":
        echo_text = sys.argv[2] if len(sys.argv) > 2 else ""
        cmd = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--cmd" else ""
        echo_confirm(echo_text, cmd)
        return

    # --auto 模式（解析后直接执行）
    auto_exec = False
    text_idx = 1
    if sys.argv[1] == "--auto":
        auto_exec = True
        text_idx = 2

    text = " ".join(sys.argv[text_idx:])
    if not text.strip():
        print("❌ 请输入自然语言命令")
        sys.exit(1)

    command, source = parse_command(text, use_api=True)

    if not command:
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║  ⚠️  语义解析失败                                          ║
║  无法识别命令: {text[:47]}…
║  请使用: lh6 help 查看可用命令                             ║
╚═══════════════════════════════════════════════════════════╝
""")
        sys.exit(1)

    if auto_exec:
        execute_command(command)
    else:
        if echo_confirm(text, command, source):
            sys.exit(execute_command(command))
        else:
            print("❌ 已取消")
            sys.exit(1)


if __name__ == "__main__":
    main()
