#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离-LH-AUTOFILL-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
📛 龍魂·文档自动填充 + 干支时间戳审计 + 人格协作接力签名引擎 v1.0
=====================================================================
老大指令（2026-09-06 verbatim 焊点）：「帮我做个脚本，自动填充所有的文件。
我上下审计时间戳，时间戳是天干地支的啊，别搞错了。还有署名，还有每个AI协作
那个签名，每个人格怎么操作的，怎么接力的，那些都全部用起来」

三大能力（lh autofill <子命令>）：
  audit  —— 上下时间戳审计：每文件头/尾是否带「干支时间戳」（非纯日期）、署名、
             抬头/主权声明缺不缺 → 表格（--json 机器读）
  fill   —— 自动填充一条龙（幂等·已带即跳过）：
               --stamp  文件头/尾补「干支时间戳」→ 调 bin/lh_time_engine.py（唯一权威·禁止自算）
               --attr   补署名归属名        → 委托 08_BIN/lh_fix_attribution.py --fix
               --sov    补内容主权三件套    → 委托 08_BIN/lh_content_sovereignty.py（articles/papers）
               --sign   GPG 分离签名        → 委托 bin/lh_gpg_sign.py sign --force
  relay  —— 人格协作接力签名：按执行链生成「🧬 AI协作接力签名」块（含干支触发时间·审计·GPG）
               relay --map 打印每个人格怎么操作/怎么接力的标准动作表
=====================================================================
干支铁律：时间戳一律由 bin/lh_time_engine.py 现算输出（四柱+卦象·64卦库唯一权威），
         本引擎不做任何干支换算 —— 「别搞错了」焊死。
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = ROOT / "bin"
BASE_DIR = ROOT

STEM = "甲乙丙丁戊己庚辛壬癸"
BRANCH = "子丑寅卯辰巳午未申酉戌亥"
RE_GZ = re.compile("[" + STEM + "][" + BRANCH + "]")          # 干支对
RE_DNA = re.compile(r"#龍芯⚡️[甲乙丙丁戊己庚辛壬癸]")          # DNA 且干支开头
RE_ISO = re.compile(r"20\d{2}-\d{2}-\d{2}")                   # 纯公历日期
RE_TAIL_STAMP = re.compile("[🐉📛][" + STEM + "][" + BRANCH + "]")

ATTR_MARKS = ("诸葛鑫", "归属名", "ZHUGEXIN")
HEAD_STAMP_MD = "> 干支时间戳: "
HEAD_STAMP_CODE = "# 干支时间戳: "
TAIL_STAMP = "🐉AI协作输出时间戳: "
NON_TEXT_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
                ".gz", ".xz", ".bz2", ".7z", ".mp4", ".mp3", ".wav", ".woff",
                ".woff2", ".ttf", ".otf", ".exe", ".so", ".dll", ".pyc", ".pyo",
                ".asc", ".json", ".csv", ".db", ".sqlite", ".pem", ".key", ".plist"}
SKIP_DIRS = {"_archive", "archive", "backup", "backups", "_work", ".venv", "venv",
             "node_modules", "dist", "models", "weights", "11_DATA", "logs",
             ".git", "glyph-backup", "龍魂成片", "notion-mirror", "_private",
             "_QUARANTINE", "tombstone_vault", "__pycache__", ".codebuddy",
             "tools", "tests", "test_results", "test_reports", "core", "lib",
             "include", "fonts", "字体"}

# ── 人格协作接力签名（每个人格怎么操作·怎么接力·一键用起来）────────────────
RELAY_MAP = [
    ("P00曾师/文心", "意图解析·路由分发", "接老大指令→判断场景→路由给执行人格", "首个接收"),
    ("P04鲁班", "技术执行", "写码/改文件/修 bug → fill 自动填充/写正文", "执行完 → 接力 P05"),
    ("P05上帝之眼", "审计", "三色审计（时间戳干支✓/署名✓/主权声明✓）→ 出差异清单", "🟢 过 → P06 复算；🔴 → P72"),
    ("P06数学大师", "验证", "数字根/DNA 追溯码复算 → 一致🟢 偏差🟡", "过 → P15"),
    ("P15乔前辈", "签章", "GPG 分离签名 + DNA 盖章（fill --sign）", "签后 → P03"),
    ("P03雯雯", "归档", "四签验证·落位正确目录·复盘留痕", "收口"),
    ("P72龍盾", "熔断兜底", "仅 🔴/异常才介入 · 平时不占位", "异常升级点"),
]
DEFAULT_CHAIN = "P00意图路由→P04鲁班执行→P05上帝之眼审计→P06数学大师验证→P15乔前辈签章→P03雯雯归档"


RE_DNA_HEAD = re.compile(r"DNA:\s*(#龍芯[^\s]*|#龙芯[^\s]*)")


def _extract_dna_head(p: Path) -> str:
    """从文件头部(前10行)提取 DNA 追溯码"""
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as fh:
            for _ in range(10):
                m = RE_DNA_HEAD.search(fh.readline())
                if m:
                    return m.group(1).rstrip(",\"']")
    except Exception:
        pass
    return ""


def _hub_hook(files, creator="UID9622"):
    """决策C钩子(2026-09-06·丙午丁酉癸未丑时): fill 完整模式(sign)后,
    落盘文档自动登记跨AI记忆hub(本地JSON必写·Notion增量可用才同步·同文件去重·失败不阻断fill主流程)"""
    try:
        hub = BIN_DIR / "lh_memory_hub.py"
        existing = set()
        try:
            if str(BIN_DIR) not in sys.path:
                sys.path.insert(0, str(BIN_DIR))
            import lh_memory_hub as _hub_mod
            existing = {e.get("title", "") for e in _hub_mod.load_local().get("entries", [])}
        except Exception:
            existing = set()
        n = 0
        skipped = 0
        for f in files:
            fp = Path(f)
            if not fp.exists():
                continue
            title = f"[autofill] {fp.name}"
            if title in existing:
                skipped += 1
                continue
            dna = _extract_dna_head(fp)
            r = subprocess.run(
                ["python3", str(hub), "add",
                 "--title", title,
                 "--content", f"autofill 落盘: {fp} | DNA: {dna or '未提取'}",
                 "--category", "技术",
                 "--creator", creator,
                 "--source", dna or ""],
                capture_output=True, text=True, timeout=30)
            if r.returncode == 0 and "已写入" in r.stdout:
                n += 1
        if n or skipped:
            print(f"  🧠 决策C钩子: 登记 {n} 条 / 去重跳过 {skipped} 条 → 跨AI hub")
            if n:
                try:
                    r2 = subprocess.run(["python3", str(hub), "push"],
                                        capture_output=True, text=True, timeout=120)
                    out2 = (r2.stdout or "").strip()
                    if r2.returncode == 0 and out2:
                        print(f"  📤 Notion 增量同步: {out2.splitlines()[-1]}")
                    else:
                        print(f"  🟡 Notion 增量同步跳过: {(r2.stderr or '').strip()[:120] or '无输出'}")
                except Exception as e2:
                    print(f"  🟡 Notion 增量同步跳过(不阻断): {e2}")
    except Exception as e:
        print(f"  ⚠️ hub 钩子跳过(不阻断 fill): {e}")


def _cmd(args_list: list, timeout: int = 60) -> str:
    """调外部引擎（干支唯一权威）。"""
    return subprocess.run([sys.executable] + args_list, capture_output=True,
                          text=True, timeout=timeout, cwd=str(ROOT)).stdout.strip()


def stamp_compact() -> str:
    """#龍芯⚡️干支四柱·卦（lh_time_engine 唯一权威）"""
    return _cmd([str(BIN_DIR / "lh_time_engine.py"), "--stamp-compact"])


def stamp_full() -> str:
    return _cmd([str(BIN_DIR / "lh_time_engine.py"), "--stamp"])


def stamp_simple() -> str:
    return _cmd([str(BIN_DIR / "lh_time_engine.py"), "--stamp-simple"])


def _is_binary(p: Path) -> bool:
    try:
        with open(p, "rb") as f:
            head = f.read(8192)
        if b"\x00" in head:
            return True
    except OSError:
        return True
    return False


def _read(p: Path):
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def _is_md(p: Path) -> bool:
    return p.suffix.lower() == ".md"


def _code_comment(p: Path) -> str:
    return "#"


def head_stamp_line(p: Path, compact: str) -> str:
    if _is_md(p):
        return f"{HEAD_STAMP_MD}{compact}\n"
    return f"# 干支时间戳: {compact}\n"


# ── 审计 --------------------------------------------------------------------
def audit_file(p: Path) -> dict:
    text = _read(p)
    if text is None:
        return {"file": str(p), "status": "⏭️ 二进制/不可读"}
    head = text[:1600]
    tail = text[-1200:]

    head_dna = bool(RE_DNA.search(head)) or bool(RE_GZ.search(head))
    head_iso_only = bool(RE_ISO.search(head)) and not head_dna
    tail_stamp = bool(RE_GZ.search(tail)) or bool(RE_TAIL_STAMP.search(tail))
    tail_sovereign = "AI_TRAINING_PROHIBITED" in tail[-700:]
    attr = any(m in text[:2400] for m in ATTR_MARKS)
    lic = ("MulanPSL" in text[:2400]) or ("CC BY-NC-SA" in text[:2400])

    def head_label():
        if head_dna:
            return "✅ 干支"
        if head_iso_only:
            return "⚠️ 纯日期(缺干支)"
        return "❌ 缺失"

    def tail_label():
        if not _is_md(p):
            return "—"          # 非 md 不适用文末戳（结构保护）
        if tail_sovereign:
            return "✅ 主权块"
        return "✅ 有" if tail_stamp else "❌ 缺"

    return {
        "file": str(p), "head_stamp": head_label(), "tail_stamp": tail_label(),
        "attr": "✅" if attr else "❌", "license": "✅" if lic else "—",
    }


def collect(paths: list, depth: int = 1) -> list:
    out = []
    for base in paths:
        p = Path(base)
        if p.is_file():
            if p.suffix.lower() in NON_TEXT_EXT or _is_binary(p):
                continue
            out.append(p)
            continue
        if not p.is_dir():
            continue
        stack = [(p, 0)]
        while stack:
            cur, d = stack.pop()
            for f in sorted(cur.iterdir()):
                if f.is_dir():
                    if f.name in SKIP_DIRS or f.name.startswith(".") or d >= depth:
                        continue
                    stack.append((f, d + 1))
                elif f.suffix.lower() not in NON_TEXT_EXT \
                        and not f.name.endswith(".glyph-backup") \
                        and not _is_binary(f) and f.name != ".DS_Store":
                    out.append(f)
    return out


# ── 自动填充 ----------------------------------------------------------------
def fill_stamp_file(p: Path, add_tail: bool, freeze: bool) -> dict:
    """补头/尾干支时间戳（幂等）。"""
    text = _read(p)
    if text is None:
        return {"file": str(p), "status": "⏭️ 二进制/不可读"}
    lines = text.splitlines(keepends=True)
    # 头部干支判定统一口径：前 1600 字符（与 audit 一致，覆盖 DNA 元数据区）
    has_head_gz = bool(RE_DNA.search(text[:1600])) or bool(RE_GZ.search(text[:1600]))
    compact = stamp_compact()
    changed = False
    new_text = text

    head_done = tail_done = False
    if not has_head_gz:
        # 仅头部完全无干支的裸文件才补头（有 DNA 追溯码的历史文件不动头部）
        lines = text.splitlines(keepends=True)
        if freeze:
            _freeze(p)
        # 插入点 = 第一个非空行之前（md 标题 / 代码 shebang 之后均正确）
        ins_idx = next((i for i, ln in enumerate(lines) if ln.strip()), 0)
        st = head_stamp_line(p, compact)
        new_text = "".join(lines[:ins_idx]) + st + "".join(lines[ins_idx:])
        head_done = True

    if add_tail and _is_md(p):
        tail = new_text[-1200:]
        # 文末含主权 JSON 终块（AI_TRAINING_PROHIBITED）→ 不补尾戳，法律位优先不破位
        if not (RE_TAIL_STAMP.search(tail)
                or (RE_GZ.search(tail) and TAIL_STAMP.strip() in tail)
                or "AI_TRAINING_PROHIBITED" in tail[-700:]):
            if freeze and not head_done:
                _freeze(p)
            new_text = new_text.rstrip() + "\n\n" + TAIL_STAMP + stamp_simple() + "\n"
            tail_done = True

    changed = head_done or tail_done
    if changed and new_text != text:
        p.write_text(new_text, encoding="utf-8")
    tag = "补头部干支" if head_done else ("补文末干支戳" if tail_done else "跳过(已有)")
    return {"file": str(p), "head": head_done, "tail": tail_done, "status": tag}


def _freeze(p: Path):
    frozen = ROOT / "archive" / "frozen"
    frozen.mkdir(parents=True, exist_ok=True)
    dst = frozen / (p.name + ".prefill")
    shutil.copy2(p, dst)


# ── 协作接力签名 ------------------------------------------------------------
def _lookup_role(name: str):
    """按人格 tag（如 P04鲁班 / P05 / 鲁班）查标准职能与操作。"""
    for tag, duty, op, relay in RELAY_MAP:
        if tag.startswith(name[:4]) or name in tag or tag.startswith(name):
            return duty, op, relay
    return "协作执行", "按链执行", "接力下一环"


def relay_block(chain: str, doc: str) -> str:
    roles = [x.strip() for x in chain.split("→")]
    gz = stamp_compact()
    rows = []
    for i, name in enumerate(roles):
        duty, op, relay = _lookup_role(name)
        rows.append(f"| {i+1} | {name}({duty}) | {op} → {relay} | {gz} |")
    rows = "\n".join(rows)
    return f"""
---
## 🧬 AI 协作接力签名

> 本条记录本次交付的 AI 人格协作链路（谁做了什么·怎么接力·可追溯）。
> 接力铁律：执行→审计→验证→签章→归档；🔴 才升级 P72 熔断，平时 P72 不占位。

| 序号 | 人格(职能) | 本步操作 | 干支触发时间 |
|:---:|:---|:---|:---|
{rows}

**协作链**: {chain}
**文档**: {doc}
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名**: 诸葛鑫 | UID9622 · 龍芯北辰
**GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""


# ── 主入口 ------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(
        description="📛 龍魂·文档自动填充+干支时间戳审计+人格协作接力签名 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python3 08_BIN/lh_autofill.py audit --dir 01_protocols            # 上下干支审计
  python3 08_BIN/lh_autofill.py audit --dir articles --head 8       # 只看前 8 个
  python3 08_BIN/lh_autofill.py fill --dir articles --stamp --attr --sov --sign --freeze
  python3 08_BIN/lh_autofill.py relay --doc articles/x.md --chain "P04鲁班→P05上帝之眼→P15乔前辈"
  python3 08_BIN/lh_autofill.py relay --map                         # 人格接力标准动作表
""")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("audit", help="上下时间戳干支审计")
    a.add_argument("--dir", default=str(BASE_DIR))
    a.add_argument("--depth", type=int, default=1)
    a.add_argument("--head", type=int, default=0, help="只看前 N 个文件")
    a.add_argument("--json", action="store_true")
    a.add_argument("--fix", action="store_true", help="缺干支的文件直接补头(调用 fill --stamp)")

    f = sub.add_parser("fill", help="自动填充一条龙(幂等)")
    f.add_argument("--dir", default=str(BASE_DIR))
    f.add_argument("--stamp", action="store_true", help="补干支时间戳(头)")
    f.add_argument("--tail", action="store_true", help="补文末干支输出戳(md)")
    f.add_argument("--attr", action="store_true", help="委托 lh_fix_attribution 补署名")
    f.add_argument("--sov", action="store_true", help="委托 lh_content_sovereignty 补主权三件套")
    f.add_argument("--sign", action="store_true", help="委托 lh_gpg_sign 补 GPG 签名")
    f.add_argument("--file", default="",
                   help="精确单文件模式(替代 --dir 批量·stamp/tail/sign/relay 只作用于该文件)")
    f.add_argument("--relay", action="store_true",
                   help="落盘后自动为每个文本文件附加人格协作接力签名(幂等·默认链)")
    f.add_argument("--freeze", action="store_true", help="修改前冻结原版到 archive/frozen/")
    f.add_argument("--depth", type=int, default=1)
    f.add_argument("--json", action="store_true")

    r = sub.add_parser("relay", help="人格协作接力签名")
    r.add_argument("--doc", help="目标文档路径(追加协作签名块)")
    r.add_argument("--chain", default=DEFAULT_CHAIN,
                   help="执行链, 如 'P04鲁班→P05上帝之眼→P15乔前辈'")
    r.add_argument("--map", action="store_true", help="打印人格接力标准动作表")

    args = ap.parse_args()

    if args.cmd == "audit":
        files = collect([args.dir], args.depth)
        res = [audit_file(p) for p in files]
        if args.head:
            res = res[:args.head]
        if args.json:
            print(json.dumps({"total": len(res), "items": res},
                             ensure_ascii=False, indent=1))
            return 0
        n_head_need = sum(1 for x in res if x.get("head_stamp", "✅") != "✅ 干支")
        n_tail_need = sum(1 for x in res if x.get("tail_stamp", "✅") == "❌ 缺")
        print(f"📛 干支时间戳审计({args.dir}): {len(res)} 文件")
        print(f"  头部干支缺失/纯日期: {n_head_need} | 尾部干支缺失: {n_tail_need}")
        for x in res:
            if "head_stamp" not in x:
                continue
            print(f"  {x['head_stamp']:<12} 尾{x['tail_stamp']:<6} 署名{x['attr']}  "
                  f"{x['file']}")
        print("  （--fix 可自动补头部干支 · --json 机器读）")
        if args.fix:
            for x in res:
                p = Path(x["file"])
                if "file" in x and x.get("head_stamp", "✅") != "✅ 干支":
                    fill_stamp_file(p, add_tail=False, freeze=True)
            print("  ✅ 缺干支文件头部已补齐")
        return 0

    if args.cmd == "fill":
        single = getattr(args, "file", "") or ""
        files = [Path(single)] if single else collect([args.dir], args.depth)
        done = {"stamp": 0, "tail": 0, "attr": 0, "sov": 0, "sign": 0, "relay": 0}
        if args.stamp or args.tail:
            for p in files:
                r = fill_stamp_file(p, add_tail=args.tail, freeze=args.freeze)
                if r.get("head"):
                    done["stamp"] += 1
                if r.get("tail"):
                    done["tail"] += 1
        # 批量模式(默认)才做 attr/sov 目录级委托; 单文件模式(--file)跳过(文件头自带署名·非批量文章场景)
        if not single and args.attr:
            cmd = [str(ROOT / "08_BIN" / "lh_fix_attribution.py"),
                   "--dir", args.dir, "--fix"]
            print(_cmd(cmd))
            done["attr"] = 1
        if not single and args.sov:
            print(_cmd([str(ROOT / "08_BIN" / "lh_content_sovereignty.py"),
                        "--md-dir", args.dir]))
            done["sov"] = 1
        if args.sign:
            target = single or args.dir
            print(_cmd([str(BIN_DIR / "lh_gpg_sign.py"), "sign", "--force", target],
                       timeout=600))
            done["sign"] = 1
        # 决策C钩子(2026-09-06): 完整模式(sign)下落盘文档自动登记跨AI记忆hub·失败不阻断
        if args.sign and files:
            _hub_hook(files)
        # 方向④(2026-09-06·六方向拍板): --relay 时每个落盘文本自动附加人格协作接力签名(幂等·已有跳过)
        if args.relay and files:
            for p in files:
                try:
                    t = p.read_text(encoding="utf-8", errors="ignore")
                except Exception:  # noqa: BLE001
                    continue
                if "AI 协作接力签名" in t:
                    continue
                p.write_text(t.rstrip() + "\n" + relay_block(DEFAULT_CHAIN, str(p)),
                             encoding="utf-8")
                done["relay"] += 1
        print(f"✅ autofill fill 完成: 干支头{done['stamp']} 文末戳{done['tail']} "
              f"署名{'✓' if done['attr'] else '—'} 主权{'✓' if done['sov'] else '—'} "
              f"GPG{'✓' if done['sign'] else '—'} 接力{done['relay']}")
        return 0

    if args.cmd == "relay":
        if args.map:
            print("🧬 人格协作接力·标准动作表（每个人格怎么操作·怎么接力）")
            print(f"{'人格':<12} {'职能':<12} {'怎么操作':<24} 怎么接力")
            for name, duty, op, relay in RELAY_MAP:
                print(f"{name:<12} {duty:<10} {op:<22} {relay}")
            print(f"\n默认执行链: {DEFAULT_CHAIN}")
            return 0
        if not args.doc:
            print("❌ 需要 --doc 目标文档 + --chain 执行链（--map 看人格表）")
            return 1
        doc = Path(args.doc)
        if not doc.exists():
            print(f"❌ 文档不存在: {doc}")
            return 1
        text = _read(doc)
        if text is None:
            print("❌ 文档不可读")
            return 1
        if "AI 协作接力签名" in text:
            print(f"⏭️  文档已有协作接力签名: {doc}")
            return 0
        block = relay_block(args.chain, str(doc))
        doc.write_text(text.rstrip() + "\n" + block, encoding="utf-8")
        print(f"✅ 协作接力签名已附加: {doc}")
        print(f"   链: {args.chain}")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
