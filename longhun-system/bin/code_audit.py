#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code_audit.py · 三色代码审计 × 通心译解释器 v1.0
输入代码 → 三色审计 → 人话解释 → 修复建议 → 完事

DNA: #龍芯⚡️2026-04-16-三色代码审计-v1.0
作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人
共建: 终端宝宝 × Notion宝宝

用法:
  python3 code_audit.py <文件路径>
  python3 code_audit.py --code "print('hello')"
  python3 code_audit.py --stdin  (从管道输入)

输出:
  🟢 安全   — 无问题，直接用
  🟡 注意   — 有隐患，建议改
  🔴 危险   — 必须修，不能上线

只输出结果，不废话。
"""

import re
import sys
import json
import time
import hashlib
from pathlib import Path
from typing import List, Tuple

# ─── 配置 ────────────────────────────────────────────
BASE     = Path.home() / "longhun-system"
LOGS     = BASE / "logs"
DNA_TAG  = "#龍芯⚡️2026-04-16-三色代码审计-v1.0"
GPG_FP   = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
UID      = "9622"

AUDIT_LOG = LOGS / "code_audit.jsonl"
LOGS.mkdir(exist_ok=True)


# ═══════════════════════════════════════════════════════
# 第一层 · 安全扫描（🔴红线检测）
# ═══════════════════════════════════════════════════════

RED_PATTERNS = [
    # 命令注入
    (r'os\.system\s*\(', "os.system() 命令注入风险", "用 subprocess.run(..., shell=False) 替代"),
    (r'subprocess\.\w+\(.*shell\s*=\s*True', "shell=True 命令注入", "改成 shell=False，参数用列表传"),
    (r'eval\s*\(', "eval() 任意代码执行", "用 ast.literal_eval() 或 json.loads() 替代"),
    (r'exec\s*\(', "exec() 任意代码执行", "重构逻辑，避免动态执行"),
    (r'__import__\s*\(', "动态导入风险", "用正常 import 语句"),

    # SQL注入
    (r'f["\'].*(?:SELECT|INSERT|UPDATE|DELETE|DROP).*\{', "SQL拼接注入", "用参数化查询 cursor.execute(sql, params)"),
    (r'\.format\(.*(?:SELECT|INSERT|UPDATE|DELETE|DROP)', "SQL format注入", "用参数化查询"),
    (r'%\s*\(.*(?:SELECT|INSERT|UPDATE|DELETE)', "SQL %格式注入", "用参数化查询"),

    # 密钥泄露
    (r'(?:api_key|apikey|secret|password|token)\s*=\s*["\'][A-Za-z0-9_\-]{16,}["\']', "硬编码密钥", "用环境变量 os.environ.get() 读取"),
    (r'(?:sk-|ghp_|gho_|github_pat_|xoxb-|xoxp-)[A-Za-z0-9_\-]{20,}', "明文Token暴露", "移到 .env 文件，用 dotenv 加载"),

    # 文件操作
    (r'open\s*\(.*["\']w["\'].*\).*\n.*user', "用户输入直接写文件", "验证文件路径，限制写入目录"),
    (r'rm\s+-rf\s+/', "危险删除根目录", "绝对不能 rm -rf /"),
    (r'shutil\.rmtree\s*\(\s*["\']/', "删除根目录", "限制删除范围"),

    # XSS / 注入
    (r'innerHTML\s*=', "innerHTML XSS风险", "用 textContent 或 DOMPurify 清洗"),
    (r'document\.write\s*\(', "document.write XSS", "用 DOM API 操作"),
    (r'dangerouslySetInnerHTML', "React XSS风险", "确保内容已经过 sanitize"),
]

# ═══════════════════════════════════════════════════════
# 第二层 · 隐患扫描（🟡注意检测）
# ═══════════════════════════════════════════════════════

YELLOW_PATTERNS = [
    # 异常处理
    (r'except\s*:', "裸 except 吞掉所有异常", "指定具体异常类型 except ValueError:"),
    (r'except\s+Exception\s*:', "过宽异常捕获", "捕获具体异常，别一网打尽"),
    (r'pass\s*$', "空 pass 可能隐藏问题", "至少加个 logger.warning()"),

    # 性能
    (r'time\.sleep\s*\(\s*\d{2,}', "长时间 sleep 阻塞", "考虑用异步或定时器"),
    (r'while\s+True\s*:', "无限循环", "确保有退出条件"),
    (r'import\s+\*', "通配符导入污染命名空间", "明确导入需要的名称"),

    # 编码习惯
    (r'TODO|FIXME|HACK|XXX', "遗留标记未处理", "处理完后删除标记"),
    (r'print\s*\(', "生产代码用 print", "改用 logging 模块"),
    (r'\.encode\s*\(\s*\)\s*$', "encode() 没指定编码", "明确写 .encode('utf-8')"),

    # 路径
    (r'["\']/tmp/', "硬编码 /tmp 路径", "用 tempfile.mkdtemp()"),
    (r'["\']C:\\\\', "硬编码 Windows 路径", "用 pathlib.Path 跨平台"),

    # 网络
    (r'verify\s*=\s*False', "关闭 SSL 验证", "生产环境必须开启 SSL 验证"),
    (r'http://', "使用 HTTP 明文传输", "改用 HTTPS"),
]

# ═══════════════════════════════════════════════════════
# 第三层 · 通心译解释器
# ═══════════════════════════════════════════════════════

LANG_HINTS = {
    ".py":    "Python",
    ".js":    "JavaScript",
    ".ts":    "TypeScript",
    ".tsx":   "TypeScript React",
    ".jsx":   "JavaScript React",
    ".sh":    "Shell/Bash",
    ".swift": "Swift",
    ".html":  "HTML",
    ".css":   "CSS",
    ".sql":   "SQL",
    ".php":   "PHP",
    ".go":    "Go",
    ".rs":    "Rust",
    ".java":  "Java",
    ".cpp":   "C++",
    ".c":     "C",
    ".rb":    "Ruby",
}

def detect_language(filepath: str, code: str) -> str:
    if filepath:
        suffix = Path(filepath).suffix.lower()
        if suffix in LANG_HINTS:
            return LANG_HINTS[suffix]
    if code.startswith("#!/"):
        first = code.split("\n")[0]
        if "python" in first: return "Python"
        if "bash" in first or "sh" in first: return "Shell/Bash"
        if "node" in first: return "JavaScript"
    if "def " in code and "import " in code: return "Python"
    if "function " in code or "const " in code: return "JavaScript"
    if "func " in code and "package " in code: return "Go"
    return "未知语言"


def explain_code(code: str, filepath: str) -> str:
    """通心译：用人话解释代码干了什么"""
    lang = detect_language(filepath, code)
    lines = code.strip().split("\n")
    total = len(lines)

    # 提取关键结构
    functions   = re.findall(r'(?:def|function|func|fn)\s+(\w+)', code)
    classes     = re.findall(r'class\s+(\w+)', code)
    imports     = re.findall(r'(?:import|from|require|use)\s+[\w.]+', code)
    endpoints   = re.findall(r'@(?:app|router)\.\w+\s*\(\s*["\']([^"\']+)', code)
    sql_ops     = re.findall(r'(?:SELECT|INSERT|UPDATE|DELETE|CREATE|DROP)\s', code, re.I)
    file_ops    = re.findall(r'(?:open|read|write|Path|os\.path)', code)
    net_ops     = re.findall(r'(?:requests\.|fetch\(|http|urllib|socket)', code)

    parts = []
    parts.append(f"📄 语言: {lang} · {total} 行")

    if classes:
        parts.append(f"📦 定义了 {len(classes)} 个类: {', '.join(classes[:5])}")
    if functions:
        parts.append(f"⚙️  定义了 {len(functions)} 个函数: {', '.join(functions[:8])}")
    if imports:
        parts.append(f"📥 导入了 {len(imports)} 个模块")
    if endpoints:
        parts.append(f"🌐 API端点: {', '.join(endpoints[:5])}")
    if sql_ops:
        parts.append(f"🗃️  数据库操作: {len(sql_ops)} 处")
    if file_ops:
        parts.append(f"📁 文件操作: {len(file_ops)} 处")
    if net_ops:
        parts.append(f"🔗 网络请求: {len(net_ops)} 处")

    # 猜测用途
    purpose = guess_purpose(code, functions, classes, endpoints)
    if purpose:
        parts.append(f"🎯 用途: {purpose}")

    return "\n".join(parts)


def guess_purpose(code: str, funcs: list, classes: list, endpoints: list) -> str:
    """猜这段代码大概是干什么的"""
    indicators = []
    c = code.lower()

    if endpoints or "flask" in c or "fastapi" in c or "express" in c:
        indicators.append("Web API 服务")
    if "test" in c and ("assert" in c or "expect" in c):
        indicators.append("测试代码")
    if any(w in c for w in ["spider", "crawl", "scrape", "beautifulsoup"]):
        indicators.append("爬虫/数据采集")
    if any(w in c for w in ["model", "train", "epoch", "loss", "tensor"]):
        indicators.append("机器学习/模型训练")
    if any(w in c for w in ["cron", "schedule", "daemon", "timer"]):
        indicators.append("定时任务/后台服务")
    if any(w in c for w in ["encrypt", "decrypt", "hash", "hmac", "aes"]):
        indicators.append("加密/安全模块")
    if any(w in c for w in ["notion", "database", "sync"]):
        indicators.append("数据同步/Notion集成")
    if "龍" in code or "longhun" in c or "cnsh" in c:
        indicators.append("龍魂系统组件")
    if any(w in c for w in ["click", "argparse", "sys.argv"]):
        indicators.append("CLI 命令行工具")
    if any(w in c for w in ["migration", "alter table", "create table"]):
        indicators.append("数据库迁移")

    return " · ".join(indicators) if indicators else ""


# ═══════════════════════════════════════════════════════
# 审计主引擎
# ═══════════════════════════════════════════════════════

def audit_code(code: str, filepath: str = "") -> dict:
    """
    三色代码审计 + 通心译
    返回: { color, score, explain, issues[], fixes[] }
    """
    issues = []

    # 逐行扫描
    lines = code.split("\n")
    for i, line in enumerate(lines, 1):
        # 红线
        for pattern, desc, fix in RED_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append({
                    "level":  "🔴",
                    "line":   i,
                    "code":   line.strip()[:80],
                    "问题":   desc,
                    "修复":   fix,
                })
        # 黄线
        for pattern, desc, fix in YELLOW_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append({
                    "level":  "🟡",
                    "line":   i,
                    "code":   line.strip()[:80],
                    "问题":   desc,
                    "修复":   fix,
                })

    # 计算颜色
    red_count    = sum(1 for i in issues if i["level"] == "🔴")
    yellow_count = sum(1 for i in issues if i["level"] == "🟡")

    if red_count > 0:
        color = "🔴"
        verdict = f"危险 — {red_count} 个红线问题，必须修"
    elif yellow_count > 3:
        color = "🟡"
        verdict = f"注意 — {yellow_count} 个隐患，建议改"
    elif yellow_count > 0:
        color = "🟡"
        verdict = f"注意 — {yellow_count} 个小问题"
    else:
        color = "🟢"
        verdict = "安全 — 没发现问题"

    # 通心译解释
    explain = explain_code(code, filepath)

    # 评分（100分制）
    score = 100
    score -= red_count * 15
    score -= yellow_count * 5
    score = max(0, score)

    return {
        "color":    color,
        "verdict":  verdict,
        "score":    score,
        "explain":  explain,
        "issues":   issues,
        "red":      red_count,
        "yellow":   yellow_count,
        "total_lines": len(lines),
        "filepath": filepath,
        "ts":       time.strftime("%Y-%m-%dT%H:%M:%S"),
        "dna":      DNA_TAG,
    }


# ═══════════════════════════════════════════════════════
# 输出格式化
# ═══════════════════════════════════════════════════════

def format_result(result: dict) -> str:
    """格式化输出 — 只输出结果，不废话"""
    out = []

    out.append("=" * 56)
    out.append(f"  三色代码审计 · {result['color']} {result['verdict']}")
    out.append(f"  评分: {result['score']}/100 · 共 {result['total_lines']} 行")
    if result["filepath"]:
        out.append(f"  文件: {result['filepath']}")
    out.append("=" * 56)

    out.append("")
    out.append("── 通心译 · 代码解释 ──")
    out.append(result["explain"])

    if result["issues"]:
        out.append("")
        out.append("── 问题清单 ──")
        for i, issue in enumerate(result["issues"], 1):
            out.append(f"  {issue['level']} [{i}] 第{issue['line']}行: {issue['问题']}")
            out.append(f"       代码: {issue['code']}")
            out.append(f"       修复: {issue['修复']}")
            out.append("")
    else:
        out.append("")
        out.append("  ✅ 没有发现问题")

    out.append("─" * 56)
    out.append(f"  DNA: {result['dna']}")
    out.append(f"  时间: {result['ts']}")
    out.append("─" * 56)

    return "\n".join(out)


def log_result(result: dict):
    """写审计日志（含熔断标记）"""
    record = {
        **result,
        "fused": result["color"] == "🔴",
        "fuse_cleared": False,
    }
    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ═══════════════════════════════════════════════════════
# 快速修复说明书
# ═══════════════════════════════════════════════════════

def format_book(result: dict) -> str:
    """生成快速修复说明书 — 给老大自己用的操作手册"""
    out = []
    fname = result.get("filepath", "未命名代码")
    audit_dna = f"#龍芯⚡️{time.strftime('%Y-%m-%d')}-审计-{Path(fname).stem if fname else 'inline'}-UID{UID}"

    out.append("━" * 56)
    out.append("  快速修复说明书")
    out.append("━" * 56)
    out.append(f"  文件:     {fname}")
    out.append(f"  审计结果: {result['color']} {result['verdict']}")
    out.append(f"  评分:     {result['score']}/100")
    out.append(f"  生成时间: {result['ts']}")
    if result["color"] == "🔴":
        out.append(f"  熔断状态: 🔥 已熔断 — 修复后重新审计解除")
    out.append("")

    # 必修项（红线）
    reds = [i for i in result["issues"] if i["level"] == "🔴"]
    if reds:
        out.append("【必修项】红线问题，不修不能用")
        out.append("─" * 40)
        for idx, issue in enumerate(reds, 1):
            out.append(f"  {idx}. 第{issue['line']}行 → {issue['问题']}")
            out.append(f"     现在: {issue['code']}")
            out.append(f"     改成: {issue['修复']}")
            out.append("")

    # 建议项（黄线）
    yellows = [i for i in result["issues"] if i["level"] == "🟡"]
    if yellows:
        out.append("【建议项】隐患问题，改了更好")
        out.append("─" * 40)
        for idx, issue in enumerate(yellows, 1):
            out.append(f"  {idx}. 第{issue['line']}行 → {issue['问题']}")
            out.append(f"     现在: {issue['code']}")
            out.append(f"     改成: {issue['修复']}")
            out.append("")

    if not reds and not yellows:
        out.append("【结论】")
        out.append("  ✅ 代码干净，没有需要修复的问题")
        out.append("")

    # 代码说明
    out.append("【代码说明】通心译")
    out.append("─" * 40)
    out.append(result["explain"])
    out.append("")

    # DNA + 熔断信息
    out.append("━" * 56)
    out.append(f"  DNA: {audit_dna}")
    out.append(f"  引擎: {DNA_TAG}")
    out.append(f"  署名: 诸葛鑫（UID9622）")
    out.append(f"  理论指导: 曾仕强老师（永恒显示）")
    out.append("━" * 56)

    return "\n".join(out)


# ═══════════════════════════════════════════════════════
# JSON 输出（给 Notion 用）
# ═══════════════════════════════════════════════════════

def to_notion_format(result: dict) -> dict:
    """转成 Notion 页面属性格式"""
    return {
        "标题":     result.get("filepath", "未命名代码"),
        "审计结果": result["color"] + " " + result["verdict"],
        "评分":     result["score"],
        "代码行数": result["total_lines"],
        "红线数":   result["red"],
        "黄线数":   result["yellow"],
        "解释":     result["explain"],
        "问题":     json.dumps(result["issues"], ensure_ascii=False, indent=2) if result["issues"] else "无",
        "熔断":     result["color"] == "🔴",
        "DNA":      result["dna"],
        "时间":     result["ts"],
    }


# ═══════════════════════════════════════════════════════
# 熔断查询
# ═══════════════════════════════════════════════════════

def show_fuse_list():
    """列出所有熔断记录"""
    if not AUDIT_LOG.exists():
        print("📭 没有审计记录")
        return
    fused = []
    for line in AUDIT_LOG.read_text(encoding="utf-8").strip().split("\n"):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
            if r.get("fused") and not r.get("fuse_cleared"):
                fused.append(r)
        except json.JSONDecodeError:
            continue
    if not fused:
        print("✅ 没有熔断记录 — 全部安全")
        return
    print(f"🔥 熔断记录: {len(fused)} 个")
    print("─" * 50)
    for r in fused:
        print(f"  🔴 {r.get('filepath', '?')} · {r.get('red', 0)}红线 · {r.get('ts', '?')}")


def show_history(filepath: str):
    """查看某文件的审计历史"""
    if not AUDIT_LOG.exists():
        print("📭 没有审计记录")
        return
    history = []
    for line in AUDIT_LOG.read_text(encoding="utf-8").strip().split("\n"):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
            if r.get("filepath", "") == filepath or filepath in r.get("filepath", ""):
                history.append(r)
        except json.JSONDecodeError:
            continue
    if not history:
        print(f"📭 没有 {filepath} 的审计记录")
        return
    print(f"📋 {filepath} 的审计历史: {len(history)} 次")
    print("─" * 50)
    for r in history:
        fuse = " 🔥熔断" if r.get("fused") else ""
        print(f"  {r['color']} {r['score']}/100 · 红{r['red']}黄{r['yellow']} · {r['ts']}{fuse}")


# ═══════════════════════════════════════════════════════
# 批量审计
# ═══════════════════════════════════════════════════════

CODE_EXTS = {".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".swift", ".go",
             ".rs", ".java", ".cpp", ".c", ".rb", ".php", ".sql", ".html"}

def batch_audit(directory: str, ext_filter: str = "") -> list:
    """批量审计目录下所有代码文件"""
    d = Path(directory)
    if not d.is_dir():
        print(f"❌ 目录不存在: {directory}")
        return []

    exts = {ext_filter} if ext_filter else CODE_EXTS
    files = sorted(f for f in d.rglob("*") if f.suffix in exts and f.is_file())

    if not files:
        print(f"📭 {directory} 下没有代码文件")
        return []

    results = []
    stats = {"🟢": 0, "🟡": 0, "🔴": 0}

    print(f"🔍 批量审计: {directory}")
    print(f"   扫描 {len(files)} 个文件")
    print("─" * 50)

    for f in files:
        try:
            code = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        r = audit_code(code, str(f))
        results.append(r)
        stats[r["color"]] = stats.get(r["color"], 0) + 1
        log_result(r)

        icon = r["color"]
        print(f"  {icon} {r['score']:>3}/100  {f.name}")

    print("─" * 50)
    print(f"  汇总: 🟢{stats['🟢']} 🟡{stats['🟡']} 🔴{stats['🔴']} · 共{len(files)}个文件")

    if stats["🔴"] > 0:
        print(f"\n  🔥 {stats['🔴']} 个文件触发熔断:")
        for r in results:
            if r["color"] == "🔴":
                print(f"     🔴 {r['filepath']}: {r['verdict']}")

    return results


# ═══════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="三色代码审计 × 通心译解释器 × 快速修复说明书",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 code_audit.py main.py              审单个文件
  python3 code_audit.py main.py --book       输出修复说明书
  python3 code_audit.py --code "eval(x)"     审一段代码
  cat script.py | python3 code_audit.py -s   从管道输入
  python3 code_audit.py --json main.py       JSON输出
  python3 code_audit.py --notion main.py     Notion格式
  python3 code_audit.py --dir ./bin/          批量审计目录
  python3 code_audit.py --dir ./bin/ -e .py   只审Python
  python3 code_audit.py --fuse-list           查看熔断记录
  python3 code_audit.py --history main.py     查看审计历史

DNA: #龍芯⚡️2026-04-16-三色代码审计-v1.0
署名: 诸葛鑫（UID9622）
理论指导: 曾仕强老师（永恒显示）
        """
    )
    parser.add_argument("file", nargs="?", help="要审计的代码文件路径")
    parser.add_argument("--code", "-c", help="直接传入代码字符串")
    parser.add_argument("--stdin", "-s", action="store_true", help="从标准输入读取")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    parser.add_argument("--notion", "-n", action="store_true", help="Notion属性格式输出")
    parser.add_argument("--book", "-b", action="store_true", help="输出快速修复说明书")
    parser.add_argument("--dir", "-d", help="批量审计整个目录")
    parser.add_argument("--ext", "-e", help="批量审计时只扫指定后缀（如 .py）")
    parser.add_argument("--fuse-list", action="store_true", help="查看所有熔断记录")
    parser.add_argument("--history", metavar="FILE", help="查看某文件的审计历史")

    args = parser.parse_args()

    # 熔断查询
    if args.fuse_list:
        show_fuse_list()
        return
    if args.history:
        show_history(args.history)
        return

    # 批量审计
    if args.dir:
        batch_audit(args.dir, args.ext or "")
        return

    # 获取代码
    code = ""
    filepath = ""

    if args.code:
        code = args.code
    elif args.stdin:
        code = sys.stdin.read()
    elif args.file:
        filepath = args.file
        p = Path(filepath)
        if not p.exists():
            print(f"❌ 文件不存在: {filepath}")
            sys.exit(1)
        code = p.read_text(encoding="utf-8", errors="replace")
    else:
        parser.print_help()
        sys.exit(0)

    if not code.strip():
        print("❌ 代码为空")
        sys.exit(1)

    # 审计
    result = audit_code(code, filepath)

    # 输出
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.notion:
        print(json.dumps(to_notion_format(result), ensure_ascii=False, indent=2))
    elif args.book:
        print(format_book(result))
    else:
        print(format_result(result))

    # 记日志
    log_result(result)

    # 红线退出码非零（给CI用）
    if result["red"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
