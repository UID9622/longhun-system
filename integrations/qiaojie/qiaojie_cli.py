# DNA: #龍芯⚡️丙午·乙未·乙丑·明夷-FIX_DNA-v1.0
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════════════════════
# 龍魂体系 | 乔接 QiaoJie CLI v2.0
# ═══════════════════════════════════════════════════════════
# P15 乔前辈出品 · 中英双轨 · 数字根熔断 · v2多后端智能降级
# ═══════════════════════════════════════════════════════════
# DNA追溯码(v∞): #龍芯⚡️丙午·乙未·壬戌·蹇-QIAOJIE-CLI-v2.0
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ═══════════════════════════════════════════════════════════
#
# 一句话干什么：
#   中英双轨CLI → 中文随便说/英文精准指令 → 数字根dr校验 →
#   → v2多后端(8799枢纽→9622→8765→11434智能降级) → Notion/小艺/GuanLan API
#
# 用法:
#   python qiaojie_cli.py 帮助               # 中文模式
#   python qiaojie_cli.py help               # 英文模式
#   python qiaojie_cli.py 搜索 页面名称       # Notion页面搜索
#   python qiaojie_cli.py ask 你的问题        # 小艺API问答 (走8799枢纽)
#   python qiaojie_cli.py qc                  # QuickCheck快速自检
#   python qiaojie_cli.py selftest            # 全链路自检
# ═══════════════════════════════════════════════════════════
"""

import os
import sys
import json
import hashlib
import socket
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# ── DNA 常量 ──
DNA_voo = "#龍芯⚡️丙午·乙未·壬戌·蹇-QIAOJIE-CLI-v2.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ── v2.0 后端降级链 ──
FALLBACK_CHAIN = [
    ("8799枢纽", "http://localhost:8799/hub/ask"),
    ("9622操作台", "http://localhost:9622/api/xiaoyi/ask"),
    ("8765GPT", "http://localhost:8765/chat"),
    ("Ollama", "http://localhost:11434/api/generate"),
]

# ── 中文指令映射表（语义抽屉）──
CN_COMMANDS = {
    "帮助": "help",
    "怎么用": "help",
    "搜一下": "search",
    "搜索": "search",
    "查页面": "search",
    "找": "search",
    "问": "ask",
    "问一下": "ask",
    "问小艺": "ask",
    "状态": "status",
    "健康": "health",
    "同步": "sync",
    "当前时间": "time",
    "几点了": "time",
    "快速检查": "qc",
    "自检": "selftest",
    "全链路": "selftest",
    "知识库": "kb",
}

# ── 英文精准指令表 ──
EN_COMMANDS = ["help", "search", "ask", "status", "health", "sync", "time", "qc", "selftest", "kb"]

# ── 数字根计算（用于熔断）──
def 数字根(text: str) -> int:
    """计算文本的数字根 dr ∈ {1..9}，用于五行熔断判定"""
    total = sum(ord(c) for c in text)
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total


def 数字根熔断检查(dr: int) -> tuple[bool, str, str]:  # type: ignore[reportMissingTypeArgument]
    """
    数字根熔断判定:
      dr ∈ {3, 9} → 🔴熔断 (拒绝执行)
      dr = 6     → 🟡待审 (需确认)
      其他        → 🟢通行
    """
    if dr in (3, 9):
        return (False, "🔴", f"数字根={dr} → 熔断·拒绝执行")
    elif dr == 6:
        return (True, "🟡", f"数字根={dr} → 待审·需人工确认")
    else:
        return (True, "🟢", f"数字根={dr} → 通行")


# ── 打印函数（中英双语）──
def 打印结果(状态: str, 消息: str):
    """格式化输出结果"""
    print(f"\n  {状态} {消息}")


def 打印标题():
    """打印CLI标题头"""
    print("=" * 56)
    print("🍎 乔接 QiaoJie CLI · P15 乔前辈出品")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 北京时间")
    print(f"🧬 {DNA_voo}")
    print("=" * 56)


def 打印帮助():
    """打印中文帮助"""
    print("""
📖 乔接 CLI 中文指令:

  基础指令:
    帮助 / 怎么用         → 显示帮助
    时间 / 几点了          → 显示当前北京时间
    
  Notion 操作:
    搜索 <页面名称>        → 在Notion中搜索页面
    查页面 <页面名称>       → 同上
    
  小艺 AI 问答:
    问 <你的问题>          → 通过小艺API问答
    
  系统:
    状态                   → 查看系统状态
    健康                   → 健康检查
    同步                   → 触发全局同步
  
  英文模式:
    help / search / ask / status / health / sync / time
""")


# ── 英文帮助 ──
def 打印英文帮助():
    """打印英文帮助"""
    print("""
📖 QiaoJie CLI English Commands:

  help          → Show this help
  search <name> → Search Notion page
  ask <query>   → Ask XiaoYi AI
  status        → System status
  health        → Health check
  sync          → Trigger global sync
  time          → Current time
""")


# ── 核心函数 ──
def 搜索Notion页面(页面名称: str):
    """搜索Notion页面名称"""
    try:
        from dotenv import load_dotenv  # type: ignore[import-untyped]
        load_dotenv(Path.home() / '.cnsh' / '.env')
        TOKEN = os.getenv('NOTION_TOKEN')
        if not TOKEN:
            打印结果("🔴", "Notion Token 未配置 (检查 ~/.cnsh/.env)")
            return

        import requests
        headers = {
            'Authorization': f'Bearer {TOKEN}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }

        resp = requests.post(
            'https://api.notion.com/v1/search',
            headers=headers,
            json={'query': 页面名称, 'page_size': 5},
            timeout=10
        )

        if resp.status_code == 200:
            results = resp.json().get('results', [])
            if results:
                print(f"\n  🟢 找到 {len(results)} 个结果:")
                for r in results:
                    title = ''
                    props = r.get('properties', {})
                    for key in ['title', 'Name']:
                        if key in props:
                            rich = props[key].get('title', [])
                            if rich:
                                title = rich[0].get('plain_text', '')
                                break
                    print(f"    📄 {title or '(无标题)'}")
                    print(f"       🔗 {r.get('url', 'N/A')}")
                    print(f"       ⏰ {r.get('last_edited_time', 'N/A')}")
            else:
                打印结果("🟡", f"Notion里没有「{页面名称}」这个页面")
        else:
            打印结果("🔴", f"Notion API 错误: {resp.status_code}")
    except ImportError:
        打印结果("🔴", "缺少依赖: pip install python-dotenv requests")
    except Exception as e:
        打印结果("🔴", f"搜索异常: {e}")


def 小艺问答(问题: str):
    """v2.0 多后端智能降级问答 —— 8799枢纽 → 9622 → 8765 → Ollama"""
    import requests

    # 构造 v2 统一请求体
    payload: Dict[str, Any] = {
        "query": 问题,
        "timestamp": datetime.now().isoformat(),
        "persona_code": "qiaojie_cli",
        "route_id": hashlib.sha256(问题.encode()).hexdigest()[:12],
        "model_route": "fallback_chain",
        "format": "v2",
    }

    for 后端名, url in FALLBACK_CHAIN:
        try:
            print(f"\n  🔄 尝试: {后端名} ({url})")
            headers: Dict[str, str] = {
                "Content-Type": "application/json",
                "X-DNA-Token": DNA_voo,
            }
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                # 适配不同后端的响应格式
                answer = (
                    data.get("answer")
                    or data.get("response")
                    or data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    or json.dumps(data, ensure_ascii=False)
                )
                print(f"\n  🟢 [{后端名}] 回答:")
                print(f"  {answer}")
                return
            else:
                print(f"    ⚠️  HTTP {resp.status_code}，降级到下一个后端")
        except requests.exceptions.ConnectionError:
            print(f"    ⚠️  连接失败 ({后端名})，降级到下一个后端")
        except Exception as e:
            print(f"    ⚠️  异常: {e}，降级到下一个后端")

    打印结果("🔴", "所有后端均不可用，请检查服务状态")




def 系统状态():
    """v2.0 全端口健康检查"""
    print("\n  🏥 系统状态检查...")
    checks = [
        ("8799枢纽", "http://localhost:8799/health"),
        ("9622操作台", "http://localhost:9622/health"),
        ("8770观澜M1", "http://localhost:8770/health"),
        ("8765API", "http://localhost:8765/health"),
        ("9001人格", "http://localhost:9001/health"),
        ("Ollama", "http://localhost:11434/api/tags"),
    ]
    import requests
    for name, url in checks:
        try:
            r = requests.get(url, timeout=3)
            status = "🟢" if r.status_code < 500 else "🔴"
        except Exception:
            status = "🔴"
        print(f"    {status} {name}")


def quick_check() -> bool:
    """v2.0 QuickCheck — 检查 8799 枢纽是否存活（最小自检）"""
    import requests
    try:
        r = requests.get("http://localhost:8799/health", timeout=2)
        ok = r.status_code == 200
        print(f"  {'🟢' if ok else '🔴'} QuickCheck: 8799枢纽 {'可用' if ok else f'HTTP {r.status_code}'}")
        return ok
    except Exception as e:
        print(f"  🔴 QuickCheck: 8799枢纽不可达 ({e})")
        return False


def cmd_selftest() -> None:
    """v2.0 全链路自检 (selftest)"""
    print("\n  🔬 全链路自检...")
    import requests

    tests: list[Tuple[str, str, str, Optional[Dict[str, Any]]]] = [
        ("8799/health", "GET", "http://localhost:8799/health", None),
        ("8799/hub/ask", "POST", "http://localhost:8799/hub/ask", {
            "query": "ping", "persona_code": "qiaojie_cli_selftest",
            "route_id": "selftest", "format": "v2"}),
        ("9622/health", "GET", "http://localhost:9622/health", None),
        ("8770/health", "GET", "http://localhost:8770/health", None),
        ("Ollama/tags", "GET", "http://localhost:11434/api/tags", None),
    ]

    passed = 0
    for name, method, url, body in tests:
        try:
            if method == "GET":
                r = requests.get(url, timeout=5)
            else:
                r = requests.post(
                    url, json=body or {},
                    headers={"Content-Type": "application/json", "X-DNA-Token": DNA_voo},
                    timeout=5)
            ok = r.status_code < 500
            print(f"    {'🟢' if ok else '🔴'} {name} → HTTP {r.status_code}")
            if ok:
                passed += 1
        except Exception as e:
            print(f"    🔴 {name} → {e}")

    print(f"\n  📊 自检完成: {passed}/{len(tests)} 通过")
    if passed == len(tests):
        print("  🟢 全部通过 ✅")
    elif passed >= len(tests) - 1:
        print("  🟡 部分可用，核心链路正常")
    else:
        print("  🔴 多处不可用，需排查")


# ── 命令路由 ──
def 路由指令(用户输入: str):
    """解析用户输入，路由到对应函数"""
    输入 = 用户输入.strip()
    if not 输入:
        return

    # 数字根预检查
    dr = 数字根(输入)
    通行, 颜色, 原因 = 数字根熔断检查(dr)
    if not 通行:
        print(f"\n  {颜色} {原因}")
        print(f"  🧬 {DNA_voo}")
        return
    if 颜色 == "🟡":
        print(f"\n  {颜色} {原因}")

    # 解析命令和参数
    parts = 输入.split(maxsplit=1)
    指令 = parts[0]
    参数 = parts[1] if len(parts) > 1 else ""

    # 中文轨：通过语义抽屉映射
    if any('\u4e00' <= c <= '\u9fff' for c in 指令):
        英文指令 = CN_COMMANDS.get(指令, "")
        if not 英文指令:
            # 尝试模糊匹配
            for cn_key, en_key in CN_COMMANDS.items():
                if cn_key in 指令 or 指令 in cn_key:
                    英文指令 = en_key
                    break
    else:
        英文指令 = 指令 if 指令 in EN_COMMANDS else ""

    # 路由执行
    if 英文指令 == "help":
        打印帮助() if any('\u4e00' <= c <= '\u9fff' for c in 用户输入) else 打印英文帮助()

    elif 英文指令 == "search":
        if 参数:
            搜索Notion页面(参数)
        else:
            打印结果("🟡", "请提供页面名称，如: 搜索 主控操作台")

    elif 英文指令 == "ask":
        if 参数:
            小艺问答(参数)
        else:
            打印结果("🟡", "请提供问题，如: 问 今天天气怎么样")

    elif 英文指令 == "status":
        系统状态()

    elif 英文指令 == "health":
        系统状态()

    elif 英文指令 == "sync":
        print("\n  🔄 触发全局同步...")
        os.system("bash ../bin/lh_sync_all.sh --quick")

    elif 英文指令 == "time":
        from datetime import datetime
        print(f"\n  ⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 北京时间")

    elif 英文指令 == "qc":
        quick_check()

    elif 英文指令 == "selftest":
        cmd_selftest()

    elif 英文指令 == "kb":
        if 参数:
            搜索Notion页面(参数)
        else:
            print("\n  📚 从知识库搜索...")
            搜索Notion页面("知识卡片")

    else:
        打印结果("🟡", f"「{指令}」这个我不认识，试试: python qiaojie_cli.py 帮助")


# ── Main ──
def main():
    打印标题()

    # v2.0 启动 QuickCheck
    print()
    quick_check()

    if len(sys.argv) < 2:
        打印帮助()
        return

    用户输入 = ' '.join(sys.argv[1:])
    路由指令(用户输入)

    print(f"\n  🧬 {DNA_voo}")
    print(f"  ✅ {CONFIRM}")


if __name__ == '__main__':
    main()
