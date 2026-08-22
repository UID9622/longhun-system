#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 MEMORY.md 压缩引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-MEMORY-COMPRESS-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
来源: Notion DragonSoulCompressor(P0-P5) + 记忆压缩引擎(L1-L4) · 宝宝交付·本机落地

用法:
    python memory_compress.py                    # 默认压缩 MEMORY.md → 7.5KB 安全线
    python memory_compress.py --input MEMORY.md --target 7500 --dry-run
    python memory_compress.py --audit           # 只看分析，不写文件
"""

import re
import sys
import argparse
import hashlib
import subprocess
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional

# ────────────────────────────────────────────────
# § 0  常量
# ────────────────────────────────────────────────

TARGET_BYTES   = 7_500          # 安全注入上限（字节）
WARN_BYTES     = 8_000          # 警告线
RECENT_DAYS    = 3              # 里程碑保留近 N 天详情
GPG_FP         = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# P0 关键词 ——命中任一 → 永不压缩整段
P0_KEYWORDS = [
    "P0-ETERNAL", "#CONFIRM🌌9622", "GPG:", "SEAL:",
    "ROOT-SEAL:", "UID9622", "身份锚", "SOVEREIGN",
    "longhun2025@petalmail.com",
    "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
]

# workspace rules 已注入 → MEMORY.md 无需重复存储的段落标题关键词
# (workspace rules 第二层含完整人格矩阵简表 → MEMORY.md §5 人格矩阵判 P5 删除)
RULES_ALREADY_INJECTED = [
    "铁律全文", "协议清单", "底座锚点", "人格矩阵完整版", "人格矩阵",
    "五大中心", "四件套铁律", "禁令列表",
    "§7", "§8", "§11",   # 主控页内嵌大段
]

# 实操必留关键词（无论多长都保留）
MUST_KEEP_KEYWORDS = [
    "write_to_file", "Notion MCP", "MCP 代理", "git push",
    "GH_TOKEN", "GitHub Token", "令牌位置",
    "跨AI记忆库", "扫描白名单", "贴文档铁律",
    "空写", "代理坑", "write_files",
    "COMMAND_INDEX", "身份焊死",
]

# ────────────────────────────────────────────────
# § 1  段落解析
# ────────────────────────────────────────────────

def parse_sections(text: str) -> list[dict]:
    """
    把 Markdown 按标题（#/##/###）切成段落列表。
    返回: [{"level":int, "title":str, "body":str, "raw":str}, ...]
    """
    pattern = re.compile(r'^(#{1,4})\s+(.+)$', re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections = []

    for i, m in enumerate(matches):
        start = m.start()
        end   = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        level = len(m.group(1))
        title = m.group(2).strip()
        raw   = text[start:end]
        body  = raw[len(m.group(0)):].strip()
        sections.append({
            "level": level, "title": title,
            "body": body,   "raw": raw,
        })

    # 文件头（第一个 # 之前的内容）
    if matches:
        preamble = text[:matches[0].start()].strip()
        if preamble:
            sections.insert(0, {
                "level": 0, "title": "__preamble__",
                "body": preamble, "raw": preamble,
            })
    return sections

# ────────────────────────────────────────────────
# § 2  优先级打分（P0-P5）
# ────────────────────────────────────────────────

def score_section(sec: dict) -> tuple[str, str]:
    """
    返回 (priority: str, reason: str)
    P0 永不压缩 | P1 完整保留 | P2 保留摘要 | P3 可折叠 | P4 可大幅压 | P5 冗余删除
    """
    title = sec["title"]
    body  = sec["body"]
    full  = title + " " + body

    # P0：命中永恒关键词
    for kw in P0_KEYWORDS:
        if kw in full:
            return "P0", f"命中P0关键词: {kw}"

    # P5：workspace rules 已注入
    for kw in RULES_ALREADY_INJECTED:
        if kw in title:
            return "P5", f"workspace已注入: {kw}"

    # P1：实操必留
    for kw in MUST_KEEP_KEYWORDS:
        if kw in full:
            return "P1", f"实操必留: {kw}"

    # P3/P4：里程碑段落 → 按日期判定
    if is_milestone_section(title):
        age = milestone_age_days(title)
        if age is None:
            return "P2", "里程碑（无日期）"
        if age <= RECENT_DAYS:
            return "P1", f"里程碑近{age}天·保详情"
        if age <= 7:
            return "P3", f"里程碑{age}天前·折叠"
        return "P4", f"里程碑{age}天前·压缩为一行"

    # P2：有实质内容（> 200字）
    if len(body) > 200:
        return "P2", "有实质内容"

    return "P3", "一般段落"

def is_milestone_section(title: str) -> bool:
    return bool(re.search(r'里程碑|milestone|\d{4}[-/]\d{2}[-/]\d{2}', title, re.I))

def milestone_age_days(title: str) -> Optional[int]:
    """从标题提取日期，返回距今天数。找不到返回 None。"""
    m = re.search(r'(\d{4})[-/](\d{2})[-/](\d{2})', title)
    if not m:
        # 尝试 "8/19" "8月19日" 等简写（补当年）
        m2 = re.search(r'(\d{1,2})[/月](\d{1,2})', title)
        if m2:
            mo, da = int(m2.group(1)), int(m2.group(2))
            try:
                d = date(date.today().year, mo, da)
                return (date.today() - d).days
            except ValueError:
                return None
        return None
    try:
        d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        return (date.today() - d).days
    except ValueError:
        return None

# ────────────────────────────────────────────────
# § 3  压缩动作
# ────────────────────────────────────────────────

def compress_section(sec: dict, priority: str) -> str:
    """按优先级决定输出内容。"""
    title_line = "#" * sec["level"] + " " + sec["title"] if sec["level"] > 0 else ""

    if priority in ("P0", "P1"):
        return sec["raw"]                          # 原文保留

    if priority == "P2":
        return _summarize(sec, keep_ratio=0.6)     # 保留 60%

    if priority == "P3":
        # 折叠：只留标题 + 一行摘要
        first_line = sec["body"].split('\n')[0][:120] if sec["body"] else ""
        return f"{title_line}\n{first_line}…\n" if title_line else first_line + "…\n"

    if priority == "P4":
        # 压成一行索引
        return f"- **{sec['title']}** （细节→每日日志）\n"

    # P5：删除
    return ""

def _summarize(sec: dict, keep_ratio: float) -> str:
    """按行数比例保留，优先保留含 MUST_KEEP 关键词的行。"""
    lines = sec["raw"].split('\n')
    must  = [l for l in lines if any(kw in l for kw in MUST_KEEP_KEYWORDS)]
    rest  = [l for l in lines if l not in must]

    target = max(len(must), int(len(lines) * keep_ratio))
    kept   = must + rest[:max(0, target - len(must))]

    # 补省略号标记
    if len(kept) < len(lines):
        kept.append(f"  _(已压缩 {len(lines)-len(kept)} 行)_")
    return '\n'.join(kept) + '\n'

# ────────────────────────────────────────────────
# § 4  GPG 签名更新
# ────────────────────────────────────────────────

def update_gpg_line(text: str) -> str:
    """把文件里旧的 GPG 签名行替换成新 SHA256 摘要（本地无私钥时用 hash 代替）。"""
    digest = hashlib.sha256(text.encode()).hexdigest().upper()
    new_sig = f"GPG: {GPG_FP} | sha256={digest[:16]}…"

    # 替换已有 GPG 行
    replaced = re.sub(r'^GPG:.*$', new_sig, text, flags=re.MULTILINE)
    if replaced == text:          # 原文没有 GPG 行 → 追加
        replaced = text.rstrip() + f"\n\n<!-- {new_sig} -->\n"
    return replaced

# ────────────────────────────────────────────────
# § 5  主压缩流程
# ────────────────────────────────────────────────

def compress_memory(
    src: Path,
    target_bytes: int = TARGET_BYTES,
    dry_run: bool = False,
    audit_only: bool = False,
) -> dict:
    """
    主入口。
    返回 report 字典（含 before/after size、priority 统计等）。
    """
    original = src.read_text(encoding="utf-8")

    # 剥离旧的 COMPRESS-LOG 注释块（每次只留最新一行·防多次运行无限膨胀）
    original = re.sub(r'<!-- COMPRESS-LOG.*?-->\n?', '', original, flags=re.DOTALL)
    original = re.sub(r'<!-- GPG:.*?-->\n?', '', original, flags=re.DOTALL)

    orig_bytes = len(original.encode())

    sections  = parse_sections(original)
    scored    = []
    for sec in sections:
        p, reason = score_section(sec)
        compressed_text = compress_section(sec, p)
        scored.append({
            "sec":      sec,
            "priority": p,
            "reason":   reason,
            "output":   compressed_text,
        })

    # 拼接 → 检查大小 → 迭代降级
    output_text = _assemble(scored)
    output_bytes = len(output_text.encode())

    # 如果还是超限，把 P2 降为 P3，P3 降为 P4，循环至目标
    for downgrade in range(3):
        if output_bytes <= target_bytes:
            break
        scored = _downgrade_one_level(scored)
        output_text  = _assemble(scored)
        output_bytes = len(output_text.encode())

    # 更新 GPG 签名行
    output_text = update_gpg_line(output_text)

    # 追加 DNA 压缩日志
    ts  = datetime.now().strftime("%Y-%m-%d %H:%M")
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-MEMORY-COMPRESS-v1.0"
    log = (
        f"\n---\n"
        f"<!-- COMPRESS-LOG {ts} | {orig_bytes}B → {len(output_text.encode())}B "
        f"(-{100*(1-len(output_text.encode())/orig_bytes):.0f}%) | {dna} -->\n"
    )
    output_text = output_text.rstrip() + log

    # 统计
    priority_counts = {}
    for s in scored:
        priority_counts[s["priority"]] = priority_counts.get(s["priority"], 0) + 1

    report = {
        "src":              str(src),
        "before_bytes":     orig_bytes,
        "after_bytes":      len(output_text.encode()),
        "ratio":            1 - len(output_text.encode()) / orig_bytes,
        "target_bytes":     target_bytes,
        "under_target":     len(output_text.encode()) <= target_bytes,
        "priority_counts":  priority_counts,
        "section_detail":   [(s["sec"]["title"], s["priority"], s["reason"]) for s in scored],
        "output_text":      output_text,
    }

    if not audit_only and not dry_run:
        # 备份原文
        backup = src.with_suffix(".md.bak")
        backup.write_text(original, encoding="utf-8")
        # 写入压缩版
        src.write_text(output_text, encoding="utf-8")

    return report

def _assemble(scored: list[dict]) -> str:
    return "".join(s["output"] for s in scored)

def _downgrade_one_level(scored: list[dict]) -> list[dict]:
    """降级顺序反转：先压冗余，最后动实质段。
    链条 [P4→P5, P3→P4, P2→P3] —— 里程碑索引先删，再折叠一般段，
    最后才把"有实质内容"段降成标题行（P2→P3 是终点，P2 永不升格删除）。
    """
    for downgrade_from, downgrade_to in [("P4","P5"), ("P3","P4"), ("P2","P3")]:
        targets = [s for s in scored if s["priority"] == downgrade_from]
        if targets:
            # 降最后 1/3（保留靠前的）
            cut = max(1, len(targets) // 3)
            for s in targets[-cut:]:
                s["priority"] = downgrade_to
                s["output"]   = compress_section(s["sec"], downgrade_to)
                s["reason"]   = f"降级→{downgrade_to}"
            return scored
    return scored

# ────────────────────────────────────────────────
# § 6  CLI 报告输出
# ────────────────────────────────────────────────

def print_report(r: dict, dry_run: bool, audit_only: bool):
    sep = "─" * 60
    print(f"\n{sep}")
    print(f"🐉 龍魂 MEMORY.md 压缩引擎 v1.0")
    print(sep)
    print(f"源文件  : {r['src']}")
    print(f"压缩前  : {r['before_bytes']:,} B")
    print(f"压缩后  : {r['after_bytes']:,} B")
    print(f"压缩率  : -{r['ratio']*100:.1f}%")
    print(f"目标线  : {r['target_bytes']:,} B   {'✅ 达标' if r['under_target'] else '⚠️ 未达标'}")
    print(f"\n优先级分布:")
    for p in ["P0","P1","P2","P3","P4","P5"]:
        cnt = r["priority_counts"].get(p, 0)
        bar = "█" * cnt
        label = {
            "P0":"永不压缩","P1":"完整保留","P2":"保留60%",
            "P3":"折叠标题","P4":"一行索引","P5":"删除"
        }[p]
        print(f"  {p} {label:8s}: {cnt:2d} 段  {bar}")

    print(f"\n段落明细:")
    for title, p, reason in r["section_detail"]:
        short = (title[:40] + "…") if len(title) > 40 else title
        print(f"  [{p}] {short:<43s} ← {reason}")

    mode = "审计（只分析不写）" if audit_only else ("预演（不写文件）" if dry_run else "已写入")
    print(f"\n模式: {mode}")
    if r["under_target"] and not audit_only and not dry_run:
        print(f"✅ {Path(r['src']).name} 已压缩完毕 + .bak 备份已创建")
    print(sep + "\n")

# ────────────────────────────────────────────────
# § 7  一键追加今日日志
# ────────────────────────────────────────────────

def append_daily_log(log_dir: Path, report: dict):
    """
    在 logs/YYYY-MM-DD.md 末尾追加压缩战报。
    """
    today_file = log_dir / f"{date.today().isoformat()}.md"
    entry = (
        f"\n## 🗜️ MEMORY.md 压缩战报 · {datetime.now().strftime('%H:%M')}\n"
        f"- **压缩前**: {report['before_bytes']:,} B\n"
        f"- **压缩后**: {report['after_bytes']:,} B  (-{report['ratio']*100:.1f}%)\n"
        f"- **目标达标**: {'✅' if report['under_target'] else '❌'}\n"
        f"- **P0段数**: {report['priority_counts'].get('P0',0)}\n"
        f"- **DNA**: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-MEMORY-COMPRESS-LOG\n"
    )
    if today_file.exists():
        with open(today_file, "a", encoding="utf-8") as f:
            f.write(entry)
    else:
        today_file.write_text(f"# 日志 {date.today().isoformat()}\n" + entry, encoding="utf-8")
    print(f"📝 今日日志已追加: {today_file}")

# ────────────────────────────────────────────────
# § 8  入口
# ────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="龍魂 MEMORY.md 压缩引擎 v1.0")
    ap.add_argument("--input",    default="MEMORY.md",  help="输入文件路径")
    ap.add_argument("--target",   type=int, default=TARGET_BYTES, help="目标字节数（默认7500）")
    ap.add_argument("--dry-run",  action="store_true",  help="预演：分析但不写文件")
    ap.add_argument("--audit",    action="store_true",  help="只输出分析报告")
    ap.add_argument("--log-dir",  default="logs",       help="每日日志目录（默认 logs/）")
    ap.add_argument("--no-log",   action="store_true",  help="不追加今日日志")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"❌ 找不到文件: {src}")
        sys.exit(1)

    report = compress_memory(
        src          = src,
        target_bytes = args.target,
        dry_run      = args.dry_run,
        audit_only   = args.audit,
    )

    print_report(report, dry_run=args.dry_run, audit_only=args.audit)

    # 只要真跑了压缩（非 audit/dry）就记战报——不管是否达标，压缩行为必须留痕
    if not args.no_log and not args.audit and not args.dry_run:
        log_dir = Path(args.log_dir)
        log_dir.mkdir(exist_ok=True)
        append_daily_log(log_dir, report)

if __name__ == "__main__":
    main()
