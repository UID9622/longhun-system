# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 本地宝宝主权架构 Agent 引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-LOCAL-AGENT-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

架构: 推理(Ollama·本地) → 规划(自写ReAct循环) → 工具(bin/直连) → 云端API零依赖
模型: 默认 qwen2.5:7b（本地已有 4.7GB）· --model 可切换
安全: 工具白名单 + P0路径黑名单(写死) + 路径穿越拦截 + ≤10步防死锁

用法:
    python3 bin/local_agent.py "帮我检查 MEMORY.md 大小"
    python3 bin/local_agent.py --interactive
    python3 bin/local_agent.py --model deepseek-r1:7b "任务"
"""

import json
import re
import sys
import subprocess
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent

# rich 可选（无则降级纯文本）
try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
except ImportError:
    class _Fallback:
        def print(self, *a, **k): print(*a)
        def input(self, *a, **k): return input(*a)
    console = _Fallback()
    def Panel(*a, **k): return ""

# ────────────────────────────────────────────────
# § 0  配置
# ────────────────────────────────────────────────

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL      = "qwen2.5:7b"       # 本地已有·中文稳·工具调用成熟（14B 未拉不硬上）
MAX_STEPS  = 10                 # 最大推理步数（防无限循环）
TIMEOUT    = 180                # Ollama 推理超时秒数

# P0 路径黑名单（写/读都拦·本地 Agent 自主跑任务必须焊死）
P0_BLOCKLIST = (
    ".ssh", ".gnupg", ".env", "_private", "P0_ETERNAL_LOCK",
    "CONSTITUTION", "LH-M261", "lh_gpg_sign", "longhun_neural_net",
    "tombstone_vault", "_QUARANTINE",
)

# shell 白名单前缀（run_shell 唯一出口）
ALLOWED_PREFIXES = (
    "python", "python3", "git status", "git add", "git commit",
    "git log", "git diff", "git stash", "lh ", "ls ", "cat ",
    "wc ", "grep ", "find ", "pwd", "echo ", "head ", "tail ",
    "cp ", "mv ", "mkdir ", "mkdir -p", "ollama list",
)


# ────────────────────────────────────────────────
# § 1  安全守卫
# ────────────────────────────────────────────────

def safe_path(path: str, writable: bool = False) -> Path:
    """路径守卫：必须落在 ROOT 内 + 非 P0 黑名单。返回规范化 Path 或抛异常。"""
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    p = p.resolve()
    try:
        p.relative_to(ROOT)
    except ValueError:
        raise PermissionError(f"BLOCKED: 路径越界 ROOT: {path}")
    for blk in P0_BLOCKLIST:
        # 子串匹配：P0_ETERNAL_LOCK.md / .env.production / 任意层含黑名单词 全拦
        if any(blk in part for part in p.parts):
            raise PermissionError(f"BLOCKED: P0 保护路径不可{writable and '写' or '读'}: {path}")
    return p


# ────────────────────────────────────────────────
# § 2  工具注册表
# ────────────────────────────────────────────────

def read_file(path: str) -> str:
    """读取文件内容。参数: path(str)"""
    try:
        p = safe_path(path)
    except PermissionError as e:
        return str(e)
    if not p.exists():
        return f"ERROR: 文件不存在: {path}"
    if p.stat().st_size > 200_000:
        return f"ERROR: 文件过大({p.stat().st_size}B)，超 200KB 读取上限，改用 grep/wc"
    return p.read_text(encoding="utf-8")[:8_000] or "(空文件)"


def write_file(path: str, content: str) -> str:
    """写入文件。参数: path(str), content(str)"""
    try:
        p = safe_path(path, writable=True)
    except PermissionError as e:
        return str(e)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"OK: 已写入 {path}（{len(content.encode())} B）"


def list_dir(path: str = ".") -> str:
    """列出目录内容。参数: path(str, 默认 '.')"""
    try:
        p = safe_path(path)
    except PermissionError as e:
        return str(e)
    if not p.exists() or not p.is_dir():
        return f"ERROR: 目录不存在: {path}"
    items = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name))
    lines = [f"{'📁' if i.is_dir() else '📄'} {i.name}" for i in items]
    return "\n".join(lines[:200]) if lines else "(空目录)"


def run_shell(cmd: str) -> str:
    """执行 shell 命令（白名单过滤）。参数: cmd(str)"""
    stripped = cmd.strip()
    if not any(stripped.startswith(p) for p in ALLOWED_PREFIXES):
        return f"BLOCKED: 命令不在白名单: {cmd}"
    # 二次防护：危险片段直接拦
    for bad in ("rm -rf", "sudo ", "curl | sh", "> ~/.", "~/.ssh", "~/.gnupg", "git push --force"):
        if bad in cmd:
            return f"BLOCKED: 含危险片段: {bad}"
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=30, cwd=ROOT,
        )
        out = (result.stdout + result.stderr).strip()
        return out[:3_000] if out else "(无输出)"
    except subprocess.TimeoutExpired:
        return "ERROR: 命令超时（30s）"
    except Exception as e:
        return f"ERROR: {e}"


def compress_memory(target: int = 7500) -> str:
    """压缩 MEMORY.md（P0-P5评分+里程碑折叠）。参数: target(int, 默认7500)"""
    return run_shell(f"python3 bin/memory_compress.py --input .codebuddy/memory/MEMORY.md --target {target}")


def check_status() -> str:
    """系统状态速查：git status + MEMORY.md 大小"""
    mem_size = 0
    mem = ROOT / ".codebuddy" / "memory" / "MEMORY.md"
    if mem.exists():
        mem_size = mem.stat().st_size
    lines = [
        f"MEMORY.md: {mem_size:,}B（安全线 7,500B）",
        f"Ollama: {'在线' if _ollama_alive() else '离线'}",
    ]
    gs = subprocess.run("git status --short", shell=True, capture_output=True,
                        text=True, timeout=10, cwd=ROOT)
    dirty = len([l for l in gs.stdout.splitlines() if l.strip()])
    lines.append(f"git 工作区: {dirty} 个变更")
    return "\n".join(lines)


def _ollama_alive() -> bool:
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def notion_search(query: str) -> str:
    """提示：Notion 搜索需 MCP 代理，本地不可达。参数: query(str)"""
    return f"INFO: Notion搜索需MCP代理（~/.codebuddy/mcp.json）。关键词: {query}。请在 Notion AI 侧搜索。"


# ────────────────────────────────────────────────
# § 2.5  感知层工具（语音 + 视觉 · 惰性加载防依赖崩）
# ────────────────────────────────────────────────

def _sense_import(mod: str):
    """把 bin/（08_BIN 镜像）加入 sys.path 后 import"""
    import sys as _sys
    p = str(ROOT / "bin")
    if p not in _sys.path:
        _sys.path.insert(0, p)
    return __import__(mod)


def _voice_transcribe(file_path: str = None, language: str = "zh", model: str = None) -> str:
    """语音转文字（本地 faster-whisper·零云端）。参数: file_path(str,可选·None则录麦克风), language(str,默认'zh'), model(str,可选)"""
    try:
        m = _sense_import("voice_input")
        return m.transcribe_audio(file_path=file_path, language=language, model=model)
    except Exception as e:
        return f"ERROR: 语音模块不可用 → {e}"


def _vision_describe(path: str, question: str = None) -> str:
    """描述图片（本地 Ollama moondream·零云端）。参数: path(str), question(str,可选)"""
    try:
        m = _sense_import("vision_input")
        return m.describe_image(path, question) if question else m.describe_image(path)
    except Exception as e:
        return f"ERROR: 视觉模块不可用 → {e}"


def _vision_screenshot(question: str = None) -> str:
    """截取当前屏幕并分析。参数: question(str,可选)"""
    try:
        m = _sense_import("vision_input")
        return m.analyze_screenshot(question) if question else m.analyze_screenshot()
    except Exception as e:
        return f"ERROR: 截图模块不可用 → {e}"


TOOLS: dict = {
    "read_file":       {"fn": read_file,       "desc": "读取文件内容。参数: path(str)"},
    "write_file":      {"fn": write_file,       "desc": "写入文件(非P0路径)。参数: path(str), content(str)"},
    "list_dir":        {"fn": list_dir,         "desc": "列出目录。参数: path(str, 默认'.')"},
    "run_shell":       {"fn": run_shell,         "desc": "执行白名单命令。参数: cmd(str)"},
    "compress_memory": {"fn": compress_memory,   "desc": "压缩MEMORY.md。参数: target(int, 默认7500)"},
    "check_status":    {"fn": check_status,      "desc": "系统状态速查(git+MEMORY+Ollama)。无参数"},
    "notion_search":   {"fn": notion_search,     "desc": "Notion工作区搜索提示。参数: query(str)"},
    "transcribe_audio": {"fn": _voice_transcribe, "desc": "语音转文字(本地·零云端)。参数: file_path(str,可选·None则录麦克风), language(str,默认'zh'), model(str,可选)"},
    "describe_image":   {"fn": _vision_describe,  "desc": "描述图片内容。参数: path(str), question(str,可选)"},
    "analyze_screenshot": {"fn": _vision_screenshot, "desc": "截取当前屏幕并分析。参数: question(str,可选)"},
}


def tools_schema() -> str:
    lines = ["你可以调用以下工具：\n"]
    for name, t in TOOLS.items():
        lines.append(f"- **{name}**: {t['desc']}")
    lines.append("""
【输出格式严格遵守】
每一步必须输出一个 JSON 块，二选一：
A) 需要调用工具时：
{"action": "工具名", "args": {"参数名": "参数值"}}
B) 任务完成时：
{"action": "finish", "answer": "完整结论"}

【铁律】
- 每次只输出一个 JSON 块，不要输出别的
- 不假装执行，必须真实调用工具看结果再决定下一步
- P0内容（GPG/私钥/身份锚/宪法）不可修改
- 命令白名单外的操作直接拒绝并说明原因
- 任务完成后用 finish 结束""")
    return "\n".join(lines)


SYSTEM_PROMPT = """你是龍魂本地 Agent（宝宝），运行在 UID9622 龍芯北辰的本地机器上，全程本地推理、零云端 API。
你的任务是理解老大的指令，拆解步骤，调用工具完成，然后报告结果。

{tools}
"""


# ────────────────────────────────────────────────
# § 3  Ollama 推理调用
# ────────────────────────────────────────────────

def ollama_chat(messages: list) -> str:
    try:
        import requests
    except ImportError:
        return "ERROR: 缺依赖 requests（pip install requests）"
    payload = {
        "model":    MODEL,
        "messages": messages,
        "stream":   False,
        "options":  {"temperature": 0.2, "num_predict": 2048},
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()["message"]["content"]
    except requests.ConnectionError:
        console.print("[red]❌ Ollama 未运行！请先执行: ollama serve[/red]")
        sys.exit(1)
    except Exception as e:
        return f"ERROR: Ollama 调用失败: {e}"


# ────────────────────────────────────────────────
# § 4  工具调用解析 + 执行
# ────────────────────────────────────────────────

def extract_action(text: str) -> Optional[dict]:
    # 法1：扫所有 { 候选 + 预筛含 "action" + 括号配对（支持嵌套/裸JSON/任意缩进）
    for idx, ch in enumerate(text):
        if ch != '{':
            continue
        if '"action"' not in text[idx:idx + 40]:
            continue
        depth = 0
        for i in range(idx, len(text)):
            c = text[i]
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[idx:i + 1])
                    except json.JSONDecodeError:
                        break  # 该起点非法，继续找下一个 {
    # 法2：markdown 代码块回退
    for pat in (r'```json\s*(\{.*?\})\s*```', r'```\s*(\{.*?\})\s*```'):
        m = re.search(pat, text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                continue
    return None


def execute_tool(action: dict) -> str:
    name = action.get("action", "")
    args = action.get("args", {})
    if name == "finish":
        return "__FINISH__"
    if name not in TOOLS:
        return f"ERROR: 未知工具 '{name}'，可用: {list(TOOLS.keys())}"
    try:
        return str(TOOLS[name]["fn"](**args))
    except TypeError as e:
        return f"ERROR: 参数错误 - {e}"
    except Exception as e:
        return f"ERROR: 工具执行异常 - {e}"


# ────────────────────────────────────────────────
# § 5  主 ReAct 循环
# ────────────────────────────────────────────────

def run_agent(task: str) -> str:
    system = SYSTEM_PROMPT.format(tools=tools_schema())
    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": task},
    ]
    console.print(Panel(f"🐉 任务: {task}", style="bold blue"))

    for step in range(1, MAX_STEPS + 1):
        console.print(f"\n[bold yellow]── Step {step}/{MAX_STEPS} ──[/bold yellow]")
        reply = ollama_chat(messages)
        preview = reply[:300] + "…" if len(reply) > 300 else reply
        console.print(f"[dim]模型:[/dim] {preview}")

        action = extract_action(reply)
        if not action:
            console.print("[red]⚠️  无法解析 action，终止循环[/red]")
            return f"ERROR: 模型未输出有效 action\n{reply[:500]}"

        if action.get("action") == "finish":
            answer = action.get("answer", reply)
            console.print(Panel(f"✅ 完成！\n\n{answer}", style="bold green"))
            return answer

        tool_name = action.get("action", "?")
        tool_args = action.get("args", {})
        console.print(f"[bold cyan]🔧 调用:[/bold cyan] {tool_name}({tool_args})")
        observation = execute_tool(action)
        console.print(f"[bold green]👁  观察:[/bold green]\n{observation[:500]}")

        messages.append({"role": "assistant", "content": reply})
        messages.append({
            "role":    "user",
            "content": f"工具 `{tool_name}` 执行结果：\n{observation}\n\n请继续完成任务。",
        })

    return f"ERROR: 超过最大步数 {MAX_STEPS}，任务未完成"


# ────────────────────────────────────────────────
# § 6  交互模式
# ────────────────────────────────────────────────

def interactive_mode():
    console.print(Panel(
        "🐉 龍魂本地 Agent · 交互模式（Ctrl+C 退出）\n"
        "纯本地推理 · 零云端 API",
        style="bold blue"
    ))
    while True:
        try:
            task = console.input("\n[bold]老大> [/bold]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n再见！")
            break
        if task.lower() in ("exit", "quit", "退出"):
            break
        if not task:
            continue
        run_agent(task)


# ────────────────────────────────────────────────
# § 7  入口
# ────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="龍魂本地 Agent v1.0（Ollama 本地推理·零云端）")
    ap.add_argument("task", nargs="?", help="一次性任务描述")
    ap.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    ap.add_argument("--model", default=MODEL, help=f"模型名（默认: {MODEL}）")
    args = ap.parse_args()

    if args.model:
        MODEL = args.model

    if args.interactive or not args.task:
        interactive_mode()
    else:
        print(run_agent(args.task))
