#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-07-24-BIN-HEALTH-CHECK-QUICK-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
"""
龍魂·全绿巡检脚本 v1.0
─────────────────────
一键跑九项体检，🔴先修再报，🟢直接略过。
输出: "🟢 全绿，无异常" 或列出非绿项。

运行: python3 bin/lh_health_check_quick.py
      python3 bin/lh_health_check_quick.py --verbose  # 详细表格
      python3 bin/lh_health_check_quick.py --fix       # 自动修复🔴
      python3 bin/lh_health_check_quick.py --json      # JSON输出（供其他脚本调用）
"""
import os, sys, json, subprocess, time, sqlite3
from pathlib import Path
from datetime import datetime, timezone

CST = timezone(__import__('datetime').timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_MD = PROJECT_ROOT / "STATE.md"
TOPOLOGY = PROJECT_ROOT / ".codebuddy" / "longhun_neural_net.json"
DNA_REGISTRY = PROJECT_ROOT / ".longhun" / "dna-audit" / "dna_registry.json"
MEMORY_DB = PROJECT_ROOT / "brain" / "memories.db"

# ── 九项体检定义 ──
# (名称, 检查函数, 修复函数或None, 权重)
CHECK_ITEMS = []

def register_check(name, weight=1):
    """装饰器注册检查项"""
    def deco(fn):
        CHECK_ITEMS.append((name, fn, getattr(fn, '_fix', None), weight))
        return fn
    return deco

def can_fix(fix_fn):
    """标记可修复"""
    def deco(original):
        original._fix = fix_fn
        return original
    return deco

# ── 辅助工具 ──

def run_cmd(cmd, timeout=10):
    """运行命令，返回 (returncode, stdout)"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip()
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"
    except Exception as e:
        return -1, str(e)

def http_ok(url, timeout=5):
    """HTTP 可达性检查"""
    code, _ = run_cmd(f"curl -s -o /dev/null -w '%{{http_code}}' --connect-timeout {timeout} {url} 2>/dev/null")
    return code == 0 and _.startswith('2')

def pgrep(pattern):
    """进程是否存在"""
    code, _ = run_cmd(f"pgrep -f '{pattern}' 2>/dev/null")
    return code == 0

# ── 九项体检 ──

@register_check("焊死记忆库", weight=2)
def check_memory():
    """brain/memories.db 存在且有至少1条记录"""
    if not MEMORY_DB.exists():
        return "🔴", "记忆库不存在"
    try:
        conn = sqlite3.connect(str(MEMORY_DB))
        count = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        conn.close()
        if count == 0:
            return "🟡", "记忆库为空，等待种子数据"
        return "🟢", f"{count}条记忆"
    except Exception as e:
        return "🔴", f"记忆库异常: {e}"

@can_fix
def fix_memory():
    """自动创建脑库并种入种子"""
    MEMORY_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(MEMORY_DB))
    conn.execute("""CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT, dna TEXT, content TEXT,
        wuxing TEXT, persona TEXT, dr INTEGER DEFAULT 0,
        tricolor TEXT DEFAULT '🟢', tags TEXT, source TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')))""")
    conn.execute("SELECT COUNT(*) FROM memories")
    count = conn.fetchone()[0]
    if count == 0:
        seeds = [
            ('#龍芯⚡丙午·乙未·SEED-UID9622', 'UID9622 = 诸葛鑫·Lucky = 唯一决策者·龍魂/CNSH/三才算法创始人',
             '金', 'P00文心', 9, '["身份","焊死"]', 'SEED'),
            ('#龍芯⚡丙午·乙未·SEED-FIX-BEFORE-REPORT', '🔴必须在报告前解决。报告是报状态不是报问题',
             '火', 'P02宝宝', 9, '["铁律","报告"]', 'SEED'),
        ]
        for dna, content, wuxing, persona, dr, tags, src in seeds:
            conn.execute("INSERT INTO memories (dna,content,wuxing,persona,dr,tags,source) VALUES (?,?,?,?,?,?,?)",
                         (dna, content, wuxing, persona, dr, tags, src))
    conn.commit()
    conn.close()
    return "记忆库已初始化"


@register_check("STATE.md", weight=2)
def check_state():
    """STATE.md 存在"""
    if STATE_MD.exists():
        size = STATE_MD.stat().st_size
        return "🟢", f"{size/1024:.0f}KB"
    return "🔴", "STATE.md 丢失"


@register_check("系统拓扑", weight=1)
def check_topology():
    """longhun_neural_net.json 存在"""
    if TOPOLOGY.exists():
        return "🟢", f"{TOPOLOGY.stat().st_size/1024:.0f}KB"
    return "🔴", "拓扑文件丢失"


@register_check("德本审计", weight=2)
def check_deben():
    """德本审计五问通过"""
    script = PROJECT_ROOT / "bin" / "lh_deben_audit.py"
    if not script.exists():
        return "🟡", "审计脚本缺失"
    code, out = run_cmd(f"cd {PROJECT_ROOT} && python3 bin/lh_deben_audit.py scan 2>&1", timeout=15)
    if code == 0 and "通过" in out:
        return "🟢", "五问通过"
    elif "🔴" in out:
        return "🔴", "审计未通过"
    return "🟡", "见审计输出"


@register_check("DNA注册表", weight=1)
def check_dna_registry():
    """DNA 注册表有数据"""
    if DNA_REGISTRY.exists():
        try:
            with open(DNA_REGISTRY) as f:
                data = json.load(f)
            valid = data.get('dna_valid', 0)
            align = data.get('alignment_rate', 0)
            return "🟢", f"{valid}条·{align}%对齐"
        except:
            return "🟡", "注册表损坏"
    return "🟡", "注册表不存在"

@can_fix
def fix_dna_registry():
    """自动刷新 DNA 注册表"""
    code, out = run_cmd(f"cd {PROJECT_ROOT} && python3 bin/lh_dna_index_fast.py . .longhun/dna-audit/dna_registry.json 2>&1", timeout=30)
    if code == 0:
        return "DNA注册表已刷新"
    return f"刷新失败: {out[:100]}"


@register_check("鲲鹏", weight=2)
def check_kunpeng():
    """119.13.90.27 可达"""
    if http_ok("http://119.13.90.27/"):
        return "🟢", "HTTP 200"
    return "🔴", "不可达"


@register_check("uid9622.cn", weight=2)
def check_domain():
    """域名 HTTPS 可达"""
    if http_ok("https://uid9622.cn/"):
        return "🟢", "HTTPS 200"
    return "🔴", "不可达"


@register_check("知识中枢 :8766", weight=2)
def check_knowledge_hub():
    """知识中枢 API 运行中"""
    if http_ok("http://127.0.0.1:8766/v1/li/status"):
        return "🟢", "HTTP 200"
    return "🔴", "未运行"

@can_fix
def fix_knowledge_hub():
    """自动拉起知识中枢"""
    script = PROJECT_ROOT / "bin" / "lh_knowledge_hub_api.py"
    if not script.exists():
        return "脚本缺失"
    code, out = run_cmd(f"cd {PROJECT_ROOT} && nohup python3 bin/lh_knowledge_hub_api.py > logs/knowledge_hub.log 2>&1 & sleep 2 && curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:8766/v1/li/status 2>/dev/null")
    if out == '200':
        return "知识中枢已拉起·HTTP 200"
    return f"拉起失败: {out[:100]}"


@register_check("小艺桥接 :8799", weight=1)
def check_xiaoyi():
    """小艺桥接运行中"""
    if pgrep("lh_xiaoyi_bridge"):
        return "🟢", "运行中"
    return "🟡", "未运行"

# ── 核心逻辑 ──

def run_all_checks(auto_fix=False):
    """跑全部检查项，返回结果列表"""
    results = []
    has_red = False
    has_yellow = False

    for name, check_fn, fix_fn, weight in CHECK_ITEMS:
        try:
            color, detail = check_fn()
        except Exception as e:
            color, detail = "🔴", str(e)

        fixed = None
        if color in ("🔴", "🟡") and auto_fix and fix_fn:
            try:
                fixed = fix_fn()
                # 复检
                color2, detail2 = check_fn()
                if color2 == "🟢":
                    color, detail = "🟢", f"{detail2} (已修复)"
                else:
                    detail = f"{detail} | 修复: {fixed}"
            except Exception as e:
                fixed = f"修复失败: {e}"

        if color == "🔴":
            has_red = True
        elif color == "🟡":
            has_yellow = True

        results.append({
            'name': name, 'color': color, 'detail': detail,
            'weight': weight, 'fixed': fixed
        })

    return results, has_red, has_yellow


def format_compact(results):
    """紧凑输出: 一行或简要"""
    reds = [r for r in results if r['color'] == '🔴']
    yellows = [r for r in results if r['color'] == '🟡']

    if not reds and not yellows:
        return "🟢 全绿，无异常"
    
    lines = []
    for r in reds:
        lines.append(f"  🔴 {r['name']}: {r['detail']}")
    for r in yellows:
        lines.append(f"  🟡 {r['name']}: {r['detail']}")
    return "\n".join(lines)


def format_verbose(results):
    """详细表格"""
    lines = ["┌──────────────────────────────────────────────────┐"]
    lines.append("│  🐉 龍魂系統 · 全绿巡检                            │")
    lines.append("├──────┬────────────────────────┬────────────────────┤")
    for r in results:
        lines.append(f"│ {r['color']}  │ {r['name']:<22s} │ {r['detail']:<18s} │")
    lines.append("└──────┴────────────────────────┴────────────────────┘")
    summary = format_compact(results)
    lines.append(f"\n{summary}")
    return "\n".join(lines)


def main():
    auto_fix = '--fix' in sys.argv
    verbose = '--verbose' in sys.argv
    json_out = '--json' in sys.argv

    results, has_red, has_yellow = run_all_checks(auto_fix=auto_fix)

    if json_out:
        print(json.dumps({
            'timestamp': datetime.now(CST).isoformat(),
            'all_green': not has_red and not has_yellow,
            'results': results,
        }, ensure_ascii=False, indent=2))
    elif verbose:
        print(format_verbose(results))
    else:
        print(format_compact(results))

    # 退出码：有🔴=1 有🟡=2 全绿=0
    if has_red:
        sys.exit(1)
    elif has_yellow:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
