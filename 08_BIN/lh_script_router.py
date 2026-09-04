#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 统一脚本发现与路由引擎 v1.0
DNA: #龍芯⚡️丙午·丁酉·乙酉·丁亥·䷋否-SCRIPT-ROUTER-v1.0-UID9622
UID: 9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
协议: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

功能: 自动发现 bin/ 与 08_BIN/ 下的 Python 脚本，按关键词路由匹配，
      默认 dry-run 展示执行命令，加 --exec 才真正执行。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─── 底座常量 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = [
    PROJECT_ROOT / "bin",
    PROJECT_ROOT / "08_BIN",
]
ROUTER_INDEX = PROJECT_ROOT / "config" / "script_router_index.json"
ROUTER_AUDIT = PROJECT_ROOT / "07_AUDIT" / "script_router_audit.json"

# 人工校准的跨语言关键词映射（简化查询→脚本 stem）
KEYWORD_OVERRIDES: Dict[str, List[str]] = {
    "权重审计": ["lh_weight_auditor"],
    "权重算法": ["lh_weight_algorithm"],
    "weightaudit": ["lh_weight_auditor"],
    "weight-audit": ["lh_weight_auditor"],
    "知识图谱": ["lh_knowledge_graph"],
    "knowledgegraph": ["lh_knowledge_graph"],
    "行为密码学": ["lh_behavioral_crypto"],
    "behavioralcrypto": ["lh_behavioral_crypto"],
    "行为指纹": ["lh_behavioral_crypto"],
    "笔试题库": ["lh_exam_engine"],
    "exambank": ["lh_exam_engine"],
    "时间引擎": ["lh_time_engine", "lh_lu_time_engine"],
    "联动感知": ["lh_cross_module_awareness"],
    "crossmodule": ["lh_cross_module_awareness"],
    "安全巡检": ["lh_patrol"],
    "patrol": ["lh_patrol"],
    "健康检查": ["lh_health_check"],
    "healthcheck": ["lh_health_check"],
    "dnabind": ["lh_dna_bind_defender"],
    "dna捆绑": ["lh_dna_bind_defender"],
    "反篡改": ["lh_anti_tamper"],
    "antitamper": ["lh_anti_tamper"],
    "主权守护": ["lh_sovereignty_guard"],
    "gpg签名": ["lh_gpg_sign"],
    "gpgsign": ["lh_gpg_sign"],
    "德本审计": ["lh_deben_audit"],
    "deben": ["lh_deben_audit"],
    "人格矩阵": ["lh_persona_matrix", "lh_persona_team"],
    "personamatrix": ["lh_persona_matrix"],
    "流场融合": ["lh_flow_fusion_bridge", "lh_flow_fusion_pipeline"],
    "知识中枢": ["lh_knowledge_hub", "lh_knowledge_hub_api"],
    "记忆加载": ["lh_memory_load"],
    "记忆归档": ["lh_fixed_point_memory_archive"],
}

HEXAGRAM_NAMES = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履",
    "泰", "否", "同人", "大有", "谦", "豫", "随", "蛊", "临", "观",
    "噬嗑", "贲", "剥", "复", "无妄", "大畜", "颐", "大过", "坎", "离",
    "咸", "恒", "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
    "损", "益", "夬", "姤", "萃", "升", "困", "井", "革", "鼎",
    "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣", "节",
    "中孚", "小过", "既济", "未济",
]
HEXAGRAM_UNICODE = [
    "䷀","䷁","䷂","䷃","䷄","䷅","䷆","䷇","䷈","䷉",
    "䷊","䷋","䷌","䷍","䷎","䷏","䷐","䷑","䷒","䷓",
    "䷔","䷕","䷖","䷗","䷘","䷙","䷚","䷛","䷜","䷝",
    "䷞","䷟","䷠","䷡","䷢","䷣","䷤","䷥","䷦","䷧",
    "䷨","䷩","䷪","䷫","䷬","䷭","䷮","䷯","䷰","䷱",
    "䷲","䷳","䷴","䷵","䷶","䷷","䷸","䷹","䷺","䷻",
    "䷼","䷽","䷾","䷿",
]
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


def _load_calendar_core():
    """加载农历干支核心（本地降级）"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT / "archive" / "experiments" / "calendar-context-logger"))
        from calendar_core import LunarEngine
        return LunarEngine()
    except Exception:
        return None


def get_ganzhi_now() -> Dict[str, str]:
    """获取当前农历干支四柱"""
    le = _load_calendar_core()
    if le:
        gz = le.get_ganzhi()
        return {
            "year": gz.get("year_zhu", "丙午"),
            "month": gz.get("month_zhu", "丁酉"),
            "day": gz.get("day_zhu", "乙酉"),
            "hour": gz.get("hour_zhu", "丁亥"),
        }
    return {"year": "丙午", "month": "丁酉", "day": "乙酉", "hour": "丁亥"}


def get_hexagram(day_zhi: str, hour_zhi: str) -> str:
    """梅花易数：上卦=日支，下卦=时支 → 64卦"""
    day_index = DI_ZHI.index(day_zhi) if day_zhi in DI_ZHI else 9
    hour_index = DI_ZHI.index(hour_zhi) if hour_zhi in DI_ZHI else 11
    upper = day_index % 8
    lower = hour_index % 8
    idx = upper * 8 + lower
    return f"{HEXAGRAM_UNICODE[idx]}{HEXAGRAM_NAMES[idx]}"


def generate_dna(module: str, action: str) -> str:
    """生成 v∞ DNA 追溯码"""
    gz = get_ganzhi_now()
    gua = get_hexagram(gz["day"][1], gz["hour"][1])
    base = f"{module}-{action}-{time.time()}"
    h = hashlib.sha256(base.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{gz['year']}·{gz['month']}·{gz['day']}·{gz['hour']}·{gua}-{module}-{action}-{h}"


def _normalize(text: str) -> str:
    """归一化：小写、去空格、去标点的简化版本"""
    return re.sub(r"[^\w\u4e00-\u9fff]", "", text.lower())


def _tokenize(text: str) -> List[str]:
    """拆分为有效 token（中文单字/英文单词）"""
    if not text:
        return []
    # 中文按字，英文按非字母数字拆分
    tokens = re.findall(r"[\u4e00-\u9fff]|[a-zA-Z0-9]+", text)
    return [t.lower() for t in tokens if len(t) >= 1]


def _is_placeholder_line(line: str) -> bool:
    """判断一行是否为占位/元数据行，不应作为摘要"""
    line = line.strip()
    if len(line) < 6:
        return True
    if line.startswith(("DNA", "UID", "GPG", "SEAL", "CONFIRM", "🐉", "╔", "║", "╚", "═", "河图", "洛书", "路径：", "TODO", "TODO:")):
        return True
    if re.match(r"^(CREATOR|PROTOCOL|VERSION|AUTHOR|DATE)[:：]", line):
        return True
    # 如果整行只是文件名/路径
    if re.match(r"^[\w./\\_\-]+\.(py|sh|md)$", line):
        return True
    return False


def _extract_docstring_summary(path: Path) -> str:
    """提取文件 docstring/注释第一行描述"""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:4000]
    except Exception:
        return ""

    # 收集所有三引号 docstring，选内容最丰富的一个
    docstrings = re.findall(r'"""(.*?)"""', text, re.DOTALL)
    best_doc = ""
    for doc in docstrings:
        lines = [ln.strip() for ln in doc.splitlines() if ln.strip()]
        candidate = ""
        for ln in lines:
            if not _is_placeholder_line(ln):
                candidate = ln.split("\n")[0].strip("：:")
                break
        if len(candidate) > len(best_doc):
            best_doc = candidate
    if best_doc:
        return best_doc

    # 再尝试单行注释中的描述
    for ln in text.splitlines()[:40]:
        ln = ln.strip()
        if ln.startswith("#") and not ln.startswith(("# DNA", "# SEAL", "# CONFIRM", "#!/", "# -*-", "#龍芯", "# CREATOR", "# PROTOCOL")):
            desc = ln[1:].strip()
            if len(desc) > 5 and not _is_placeholder_line(desc):
                if any(kw in desc for kw in ["引擎", "工具", "路由", "系统", "服务", "审计", "生成", "管理", "调度"]):
                    return desc.split("\n")[0]
    return ""


def _extract_dna_tags(path: Path) -> List[str]:
    """提取文件中 DNA / SEAL / CONFIRM 等主权标记"""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:2000]
    except Exception:
        return []
    tags = []
    for m in re.finditer(r"(DNA|SEAL|CONFIRM):\s*(#[^\s]+)", text):
        tags.append(m.group(2))
    return tags[:5]


def _extract_entry_tags(path: Path) -> List[str]:
    """提取 # lh-entry: keyword1,keyword2 标记"""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:2000]
    except Exception:
        return []
    tags = []
    for m in re.finditer(r"#\s*lh-entry:\s*([^\n]+)", text):
        for part in m.group(1).split(","):
            tags.append(part.strip().lower())
    return tags


def _has_main_guard(path: Path) -> bool:
    """是否包含可执行入口"""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    return '__name__' in text and '__main__' in text


def _arg_hints(path: Path) -> List[str]:
    """简单提取 argparse 参数名作为执行提示"""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    hints = []
    # add_argument("--foo", ...)
    for m in re.finditer(r'add_argument\(["\'](-[\w-]+)["\']', text):
        hints.append(m.group(1))
    return hints[:8]


def discover_scripts() -> List[Dict[str, Any]]:
    """扫描指定目录下所有 Python 脚本，构建元数据列表"""
    scripts: List[Dict[str, Any]] = []
    seen = set()
    for base_dir in SCAN_DIRS:
        if not base_dir.exists():
            continue
        for f in sorted(base_dir.iterdir()):
            if not f.is_file() or not f.name.endswith(".py"):
                continue
            if f.name in seen:
                continue
            seen.add(f.name)
            stat = f.stat()
            rel = f.relative_to(PROJECT_ROOT)
            scripts.append({
                "name": f.name,
                "stem": f.stem,
                "path": str(rel),
                "abs_path": str(f),
                "size": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "summary": _extract_docstring_summary(f),
                "dna_tags": _extract_dna_tags(f),
                "entry_tags": _extract_entry_tags(f),
                "has_main": _has_main_guard(f),
                "arg_hints": _arg_hints(f),
                "signed": (f.parent / (f.name + ".asc")).exists(),
            })
    return scripts


def build_index() -> Dict[str, Any]:
    """构建全量脚本路由索引"""
    scripts = discover_scripts()
    index = {
        "timestamp": datetime.now().isoformat(),
        "dna": generate_dna("SCRIPT-ROUTER", "BUILD"),
        "total": len(scripts),
        "scan_dirs": [str(d.relative_to(PROJECT_ROOT)) for d in SCAN_DIRS],
        "scripts": scripts,
        "categories": _categorize(scripts),
    }
    ROUTER_INDEX.parent.mkdir(parents=True, exist_ok=True)
    ROUTER_INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    # 审计日志
    ROUTER_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    ROUTER_AUDIT.write_text(json.dumps({
        "action": "script_router_build",
        "timestamp": index["timestamp"],
        "dna": index["dna"],
        "total": index["total"],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    return index


def load_index() -> Optional[Dict[str, Any]]:
    if not ROUTER_INDEX.exists():
        return None
    try:
        return json.loads(ROUTER_INDEX.read_text(encoding="utf-8"))
    except Exception:
        return None


def _categorize(scripts: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """按文件名关键词做粗分类"""
    cats = {
        "审计安全": [],
        "知识记忆": [],
        "人格路由": [],
        "部署运维": [],
        "数据治理": [],
        "代码工程": [],
        "算法数学": [],
        "文档内容": [],
        "网络通信": [],
        "其他": [],
    }
    rules = [
        ("审计安全", ["audit", "patrol", "security", "guard", "protect", "tamper", "kfpp", "loyalty", "fraud", "risk", "漏洞", "审计", "安全", "守护", "巡检"]),
        ("知识记忆", ["knowledge", "memory", "archive", "graph", "notion", "harvest", "source", "hub", "learn", "知识", "记忆", "归档", "图谱"]),
        ("人格路由", ["persona", "agent", "personality", "route", "embed", "behavior", "人格", "路由", "智能体", "行为"]),
        ("部署运维", ["deploy", "health", "port", "kunpeng", "docker", "launchd", "systemd", "gateway", "console", "dashboard", "部署", "运维", "健康", "控制台", "网关"]),
        ("数据治理", ["data", "dna", "sm3", "sovereignty", "privacy", "collect", "数据", "主权", "采集", "隐私"]),
        ("代码工程", ["lint", "syntax", "fix", "repair", "welder", "generator", "代码", "修复", "焊接", "语法"]),
        ("算法数学", ["math", "algorithm", "riemann", "quantum", "wuxing", "bagua", "yijing", "数字根", "算法", "五行", "八卦", "易经"]),
        ("文档内容", ["doc", "paper", "report", "video", "commentary", "content", "文档", "论文", "报告", "视频"]),
        ("网络通信", ["network", "antenna", "signal", "relay", "flow", "通信", "天线", "信号", "流场"]),
    ]
    for s in scripts:
        stem = s["stem"].lower()
        summary = s.get("summary", "").lower()
        placed = False
        for cat, kws in rules:
            if any(kw in stem or kw in summary for kw in kws):
                cats[cat].append(s["name"])
                placed = True
                break
        if not placed:
            cats["其他"].append(s["name"])
    return cats


def _score(query: str, script: Dict[str, Any]) -> Tuple[float, List[str]]:
    """计算查询与脚本的匹配得分，返回 (score, reasons)"""
    score = 0.0
    reasons: List[str] = []
    q_norm = _normalize(query)
    q_tokens = set(_tokenize(query))
    stem_norm = _normalize(script["stem"])
    summary = script.get("summary", "").lower()
    entry_tags = [t.lower() for t in script.get("entry_tags", [])]

    # 0. 人工校准关键词映射（最高优先级）
    for override_key, stems in KEYWORD_OVERRIDES.items():
        if override_key in q_norm:
            if any(stem in stem_norm for stem in stems):
                score += 25.0
                reasons.append(f"校准映射:{override_key}")
                break

    # 1. 精确文件名匹配（最高）
    if q_norm == stem_norm:
        score += 20.0
        reasons.append("精确文件名")
    # 2. 文件名包含查询或查询包含文件名
    elif q_norm in stem_norm or stem_norm in q_norm:
        score += 12.0
        reasons.append("文件名包含")

    # 3. token 匹配 stem 中的单词
    stem_tokens = set(_tokenize(script["stem"]))
    hit_tokens = q_tokens & stem_tokens
    if hit_tokens:
        score += 4.0 * len(hit_tokens)
        reasons.append(f"词命中:{','.join(hit_tokens)}")

    # 4. 查询 token 命中摘要
    summary_tokens = set(_tokenize(summary))
    hit_summary = q_tokens & summary_tokens
    if hit_summary:
        score += 2.0 * len(hit_summary)
        reasons.append(f"描述命中:{','.join(hit_summary)}")

    # 5. entry_tags 命中
    hit_tags = q_tokens & set(entry_tags)
    if hit_tags:
        score += 5.0 * len(hit_tags)
        reasons.append(f"入口标记:{','.join(hit_tags)}")

    # 6. 可执行入口偏好
    if script.get("has_main"):
        score += 1.0
        reasons.append("可执行")

    return score, reasons


def route(query: str, top_n: int = 5) -> Dict[str, Any]:
    """按关键词匹配最佳脚本"""
    index = load_index()
    if index is None:
        index = build_index()

    scripts = index.get("scripts", [])
    scored = []
    for s in scripts:
        sc, reasons = _score(query, s)
        if sc > 0:
            scored.append({"score": sc, "reasons": reasons, **s})

    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:top_n]

    best = top[0] if top else None
    return {
        "query": query,
        "total_scanned": len(scripts),
        "matched_count": len(scored),
        "best": best,
        "top_matches": top,
        "status": "🟢 已路由" if best and best["score"] >= 5 else "🟡 弱匹配",
        "dna": generate_dna("SCRIPT-ROUTER", "ROUTE"),
    }


def run_script(query: str, exec_mode: bool = False, extra_args: Optional[List[str]] = None, use_json: bool = False) -> Dict[str, Any]:
    """发现脚本并执行（默认 dry-run）"""
    result = route(query, top_n=3)
    best = result.get("best")
    extra_args = extra_args or []

    if not best:
        result["action"] = "none"
        result["message"] = "未找到匹配脚本，请尝试其他关键词或先运行 build"
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("🟡 未找到匹配脚本")
        return result

    abs_path = best["abs_path"]
    cmd = [sys.executable, abs_path] + extra_args

    result["action"] = "dry_run"
    result["command"] = " ".join(cmd)
    result["exec_mode"] = exec_mode

    if not exec_mode:
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🐉 脚本路由匹配结果")
            print(f"  查询: {query}")
            print(f"  匹配: {best['name']}")
            print(f"  路径: {best['path']}")
            print(f"  得分: {best['score']:.1f} ({' | '.join(best['reasons'])})")
            print(f"  摘要: {best.get('summary') or '无'}")
            print(f"\n  💡 这是 dry-run。要执行请加上 --exec：")
            print(f"     {' '.join(cmd)}")
        return result

    # exec 模式：执行前先做安全校验
    if not best.get("has_main"):
        result["action"] = "blocked"
        result["message"] = "目标脚本无可执行入口(__main__)，禁止 exec"
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("🔴 禁止执行：目标脚本缺少 __main__ 入口")
        return result

    try:
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=120)
        result["action"] = "executed"
        result["returncode"] = proc.returncode
        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🐉 执行: {best['name']}")
            print(f"  返回码: {proc.returncode}")
            if proc.stdout:
                print("  STDOUT:\n" + proc.stdout[:2000])
            if proc.stderr:
                print("  STDERR:\n" + proc.stderr[:1000])
    except Exception as e:
        result["action"] = "error"
        result["error"] = str(e)
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"🔴 执行异常: {e}")

    return result


def print_status():
    """打印索引状态"""
    index = load_index()
    if index is None:
        print("🟡 尚未构建索引，请先运行：lh script build")
        return
    cats = index.get("categories", {})
    print(f"""
╔══════════════════════════════════════════════════════════╗
║       🐉 龍魂 · 脚本路由索引状态                          ║
╠══════════════════════════════════════════════════════════╣
║  总脚本数: {index['total']:<5}                                  ║
║  扫描目录: {', '.join(index['scan_dirs']):<30}       ║
║  上次构建: {index['timestamp']:<30}       ║
║  DNA: {index['dna']:<45}    ║
╠══════════════════════════════════════════════════════════╣
║  分类分布                                                 ║
""")
    for cat, items in cats.items():
        print(f"║  {cat:<10}: {len(items):>4} 个")
    print("╚══════════════════════════════════════════════════════════╝")


def main():
    parser = argparse.ArgumentParser(
        description="龍魂 · 统一脚本发现与路由引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
命令:
  build                    构建/重建脚本索引
  status                   查看索引状态
  route <关键词>            按关键词查找脚本（dry-run）
  run <关键词>              按关键词执行脚本（默认 dry-run）
  list [分类]              列出脚本/分类

示例:
  lh script build
  lh script route "系统审计"
  lh script run "系统审计" --exec
  lh script route audit --json
        """
    )
    parser.add_argument("action", nargs="?", default="status",
                        choices=["build", "status", "route", "run", "list"])
    parser.add_argument("query", nargs="?", default="", help="查询关键词")
    parser.add_argument("--exec", action="store_true", help="真正执行匹配到的脚本（默认 dry-run）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--top", type=int, default=5, help="返回匹配数量")
    parser.add_argument("--args", nargs=argparse.REMAINDER, default=[], help="传递给目标脚本的额外参数")

    args = parser.parse_args()

    if args.action == "build":
        index = build_index()
        if args.json:
            print(json.dumps({"status": "ok", "total": index["total"], "dna": index["dna"]}, ensure_ascii=False))
        else:
            print(f"🐉 脚本索引构建完成：{index['total']} 个脚本")
            print(f"   DNA: {index['dna']}")

    elif args.action == "status":
        if args.json:
            idx = load_index()
            print(json.dumps(idx or {"status": "not_built"}, ensure_ascii=False, indent=2))
        else:
            print_status()

    elif args.action == "route":
        if not args.query:
            print("🟡 请提供查询关键词")
            sys.exit(1)
        result = route(args.query, top_n=args.top)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            best = result.get("best")
            print(f"\n查询: {args.query}")
            if best:
                print(f"{result['status']} → {best['name']}")
                print(f"  路径: {best['path']}")
                print(f"  得分: {best['score']:.1f} ({' | '.join(best['reasons'])})")
                print(f"  摘要: {best.get('summary') or '无'}")
                if result.get('top_matches') and len(result['top_matches']) > 1:
                    print("\n其他匹配:")
                    for m in result['top_matches'][1:]:
                        print(f"  - {m['name']} (得分 {m['score']:.1f})")
            else:
                print("🟡 无匹配")

    elif args.action == "run":
        if not args.query:
            print("🟡 请提供查询关键词")
            sys.exit(1)
        run_script(args.query, exec_mode=args.exec, extra_args=args.args, use_json=args.json)

    elif args.action == "list":
        index = load_index() or build_index()
        cat = args.query
        if cat:
            items = index.get("categories", {}).get(cat, [])
            print(f"\n分类 [{cat}] 共 {len(items)} 个脚本:")
            for name in items:
                print(f"  - {name}")
        else:
            print("\n可用分类:")
            for c, items in index.get("categories", {}).items():
                print(f"  {c:<10} {len(items):>4} 个")


if __name__ == "__main__":
    main()
