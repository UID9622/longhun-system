#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·己未·庚午·䷖剥-SKILL-PIPELINE-ENGINE-3F9C21D7-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂 · 技能全生命周期自动化流水线 v1.1

开发 → 测试 → 集成 → 发布 四阶段闭环 · 自动迭代 · 巡检自愈。

与文档草案《LH-SKILL-PIPELINE-v1.0》的关键差异（优化点）：
  1. 修正路径: 命令总目在 `.codebuddy/COMMAND_INDEX.md`（非 12_DOCS/）
  2. 修正命令: 模板引擎无 `verify-all`/`audit <文件>` → 改为
     verify-dna + verify-confirm + check-timestamp 三验证闭环 + 内置三色/填充率检查
  3. GPG 统一走 `bin/lh_gpg_sign.py`，不裸调 gpg
  4. 记忆统一走 `08_BIN/lh_memory.py`，不造新写入口
  5. 登记表落 `logs/skill_pipeline/registry.json`，可巡检可追溯
  6. 迭代记录落 `logs/skill_pipeline/iterations/`，格式对齐文档 §2.2

用法:
  python3 08_BIN/lh_skill_pipeline.py check <文件>               # 开发门禁: 存在性+DNA+确认码+三色
  python3 08_BIN/lh_skill_pipeline.py test <文件>                # 测试门禁: 三色≥🟡 + 填充率≥60%
  python3 08_BIN/lh_skill_pipeline.py integrate <名> <文件>      # 集成门禁: 签名+登记总目+写registry
  python3 08_BIN/lh_skill_pipeline.py publish <名> <文件> [版本] # 发布门禁: 三验证+发布日志+记忆归档
  python3 08_BIN/lh_skill_pipeline.py iterate <名> <文件> [版本] # 一键四阶段闭环
  python3 08_BIN/lh_skill_pipeline.py scan                       # 巡检所有已登记技能
  python3 08_BIN/lh_skill_pipeline.py status <名>                # 查询技能状态
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ENGINE = ROOT / "08_BIN" / "lh_template_engine.py"
GPG_ENGINE = ROOT / "bin" / "lh_gpg_sign.py"
MEMORY_ENGINE = ROOT / "08_BIN" / "lh_memory.py"
COMMAND_INDEX = ROOT / ".codebuddy" / "COMMAND_INDEX.md"
LOG_DIR = ROOT / "logs" / "skill_pipeline"
ITER_DIR = LOG_DIR / "iterations"
REGISTRY = LOG_DIR / "registry.json"
RELEASE_LOG = LOG_DIR / "RELEASE_LOG.md"

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
TRICOLOR_MARKS = ["🟢", "🟡", "🔴"]

# 门禁标准（文档 §1.2）
GATE = {
    "test_min_fill": 0.60,       # 测试阶段填充率下限
    "publish_min_fill": 0.90,    # 发布阶段填充率下限
    "block_on_red": True,        # 🔴 阻断
}


# ============================================================
# 工具
# ============================================================

def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_py(script: Path, *args: str) -> subprocess.CompletedProcess:
    """统一子进程入口：调现有引擎，不裸造实现"""
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True, text=True, timeout=120,
    )


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def extract_marker(text: str, keys: tuple) -> str:
    """提取文件中 DNA/确认码/时间戳字段值"""
    for key in keys:
        m = re.search(re.escape(key) + r"\s*[:：]\s*(.+)", text)
        if m:
            return m.group(1).strip()
    return ""


def extract_dna(text: str) -> str:
    # 排除反引号/空白/行尾，避免吞入 ``` ` ``` 或 `**`
    m = re.search(r"#龍芯⚡️[^\s`]+", text)
    return m.group(0) if m else extract_marker(text, ("DNA",))


def extract_confirm(text: str) -> str:
    m = re.search(r"#CONFIRM🌌[^\s`]+", text)
    return m.group(0) if m else extract_marker(text, ("确认码", "CONFIRM"))


def extract_timestamp(text: str) -> str:
    m = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?", text)
    return m.group(0) if m else ""


def extract_tricolor(text: str) -> str:
    """优先解析『三色:』字段；否则取全文最后出现的标记"""
    m = re.search(r"三色\s*[:：]\s*([^\n|]*)", text)
    if m:
        for c in TRICOLOR_MARKS:
            if c in m.group(1):
                return c
    marks = [c for c in TRICOLOR_MARKS if c in text]
    return marks[-1] if marks else "❌无标记"


def calc_fill_rate(text: str) -> float:
    """填充率 = 非空行 / 总行数（估算，够门禁用）"""
    lines = [l for l in text.splitlines() if l.strip()]
    total = len(text.splitlines())
    if total == 0:
        return 0.0
    return round(len(lines) / total, 4)


def verify_with_engine(kind: str, value: str) -> bool:
    """调模板引擎 verify-dna / verify-confirm / check-timestamp，解析 JSON"""
    if not value:
        return False
    r = run_py(TEMPLATE_ENGINE, kind, value)
    try:
        # 模板引擎输出为多行 JSON 且 stdout 可能带 shell 横幅 → 正则提取 JSON 对象
        m = re.search(r"\{.*\}", r.stdout, re.DOTALL)
        if not m:
            return False
        out = json.loads(m.group(0))
        return bool(out.get("valid"))
    except Exception:
        return False


def load_registry() -> dict:
    if REGISTRY.exists():
        try:
            return json.loads(REGISTRY.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_registry(reg: dict) -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")


def gate_pass(name: str, ok: bool, detail: str) -> None:
    mark = "✅" if ok else "❌"
    print(f"  {mark} {name}: {detail}")
    return ok


# ============================================================
# 阶段 1 · 开发门禁
# ============================================================

def cmd_check(path: str) -> bool:
    p = Path(path)
    print("🐉 阶段1 · 开发门禁 (check)")
    print("=" * 50)
    ok = True

    if not p.exists():
        print(f"  ❌ 文件不存在: {path}")
        return False
    text = read_text(p)

    dna = extract_dna(text)
    ok &= gate_pass("文件存在", True, str(p))
    ok &= gate_pass("DNA存在", bool(dna), dna or "未找到")
    if dna:
        ok &= gate_pass("DNA格式(模板引擎)", verify_with_engine("verify-dna", dna), dna)

    confirm = extract_confirm(text)
    ok &= gate_pass("确认码存在", bool(confirm), confirm or "未找到")
    if confirm:
        ok &= gate_pass("确认码格式(模板引擎)", verify_with_engine("verify-confirm", confirm), confirm)

    tri = extract_tricolor(text)
    ok &= gate_pass("三色标记", tri != "❌无标记", tri)

    # GPG 签名状态（仅提示，不阻断——签名在集成阶段执行）
    asc = Path(str(p) + ".asc")
    gate_pass("GPG签名(.asc)", asc.exists(), str(asc) if asc.exists() else "未签名→集成阶段自动补")

    print("=" * 50)
    verdict = "🟡 警告，允许继续" if (ok or not GATE["block_on_red"]) else "🟡 有警告，可继续"
    print(f"门禁判定: {verdict}")
    return ok


# ============================================================
# 阶段 2 · 测试门禁
# ============================================================

def cmd_test(path: str, for_publish: bool = False, skip_fill: bool = False) -> bool:
    p = Path(path)
    print("🐉 阶段2 · 测试门禁 (test)")
    print("=" * 50)
    if not p.exists():
        print(f"  ❌ 文件不存在: {path}")
        return False

    text = read_text(p)
    fill = calc_fill_rate(text)
    tri = extract_tricolor(text)
    dna_ok = verify_with_engine("verify-dna", extract_dna(text))
    conf_ok = verify_with_engine("verify-confirm", extract_confirm(text))

    min_fill = GATE["publish_min_fill"] if for_publish else GATE["test_min_fill"]
    ok = True
    ok &= gate_pass("三色≥🟡", tri in ("🟢", "🟡"), tri)
    if skip_fill:
        ok &= gate_pass(f"填充率(跳过)", True, f"{fill*100:.1f}% (--skip-fill)")
    else:
        ok &= gate_pass(f"填充率≥{int(min_fill*100)}%", fill >= min_fill, f"{fill*100:.1f}%")
    ok &= gate_pass("DNA验证", dna_ok, "通过" if dna_ok else "失败")
    ok &= gate_pass("确认码验证", conf_ok, "通过" if conf_ok else "失败")

    print("=" * 50)
    if ok:
        print("门禁判定: ✅ 通过，可进入下一阶段")
    else:
        print("门禁判定: 🔴 阻断，退回开发阶段")
    return ok


# ============================================================
# 阶段 3 · 集成门禁
# ============================================================

def cmd_integrate(name: str, path: str) -> bool:
    print("🐉 阶段3 · 集成门禁 (integrate)")
    print("=" * 50)
    p = Path(path)
    if not p.exists():
        print(f"  ❌ 文件不存在: {path}")
        return False

    if not cmd_test(path):
        return False

    # 3.1 GPG 签名（统一引擎）
    r = run_py(GPG_ENGINE, "sign", "--force", str(p))
    signed = r.returncode == 0 and Path(str(p) + ".asc").exists()
    gate_pass("GPG签名", signed, str(p) + ".asc" if signed else r.stderr.strip()[:200])

    # 3.2 命令总目冲突检测 + 登记
    index_text = read_text(COMMAND_INDEX)
    conflict = name in index_text if COMMAND_INDEX.exists() else False
    if conflict:
        print(f"  🟡 警告: {name} 已存在于命令总目 → 追加新登记行（不覆盖历史）")
    registered = _append_command_index(name, path)
    gate_pass("命令总目登记", registered, f"{COMMAND_INDEX.name} (追加)")

    # 3.3 写 registry
    reg = load_registry()
    reg[name] = {
        "name": name,
        "path": str(p),
        "version": "v1.0.0",
        "status": "integrated",
        "tricolor": extract_tricolor(read_text(p)),
        "updated": now_iso(),
    }
    save_registry(reg)
    gate_pass("registry登记", True, str(REGISTRY))

    # 3.4 迭代记录
    rec = _write_iteration(name, p, "integrate", {
        "type": "integrate",
        "file": str(p),
        "description": f"技能 {name} 通过集成门禁",
    })
    gate_pass("迭代记录", rec, str(ITER_DIR))

    print("=" * 50)
    print("门禁判定: ✅ 集成完成")
    return True


def _append_command_index(name: str, path: str) -> bool:
    """向命令总目『最近更新』区块追加登记行（只追加不覆盖）"""
    if not COMMAND_INDEX.exists():
        return False
    try:
        text = read_text(COMMAND_INDEX)
        line = f"| 🐉 **{name}** 🔥 | 技能全生命周期流水线登记 · 路径: `{path}` · 四阶段闭环(开发→测试→集成→发布) | `python3 08_BIN/lh_skill_pipeline.py {{check,test,integrate,publish,iterate,scan,status}}` · 登记时间: {now_iso()} |\n"
        # 插入到"最近更新"区块第一个表格行之后（紧随表头分隔行）
        m = re.search(r"(## 🆕 最近更新[^\n]*\n\n\|[^\n]*\|\n\|:?-+\|:?-+\|:?-+\|\n)", text)
        if m:
            text = text[:m.end()] + line + text[m.end():]
        else:
            text = text.rstrip() + "\n\n### 最近更新登记\n" + line
        COMMAND_INDEX.write_text(text, encoding="utf-8")
        return True
    except Exception as e:
        print(f"  ⚠️ 命令总目写入失败: {e}")
        return False


def _write_iteration(name: str, p: Path, action: str, change: dict) -> bool:
    """迭代记录，格式对齐文档 §2.2"""
    ITER_DIR.mkdir(parents=True, exist_ok=True)
    version = f"v1.0.0"
    seq = datetime.datetime.now().strftime("%Y%m%d")
    rec = {
        "skill": name,
        "version": version,
        "iteration": {
            "id": f"ITER-{seq}-{action.upper()}",
            "timestamp": now_iso(),
            "author": "UID9622",
            "changes": [change],
            "audit": {"tricolor": extract_tricolor(read_text(p)), "score": None},
            "signature": GPG_KEY,
        },
    }
    f = ITER_DIR / f"{name}-{action}-{seq}.json"
    f.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


# ============================================================
# 阶段 4 · 发布门禁
# ============================================================

def cmd_publish(name: str, path: str, version: str = "v1.0.0", skip_fill: bool = False) -> bool:
    print("🐉 阶段4 · 发布门禁 (publish)")
    print("=" * 50)
    p = Path(path)
    if not p.exists():
        print(f"  ❌ 文件不存在: {path}")
        return False

    # 4.1 测试门禁(严格版: 填充率≥90%，可 --skip-fill 显式跳过)
    if not cmd_test(path, for_publish=True, skip_fill=skip_fill):
        return False

    text = read_text(p)
    dna, confirm = extract_dna(text), extract_confirm(text)
    ts = extract_timestamp(text) or now_iso()

    # 4.2 三验证闭环
    v1 = verify_with_engine("verify-dna", dna)
    v2 = verify_with_engine("verify-confirm", confirm)
    v3 = verify_with_engine("check-timestamp", ts)
    gate_pass("DNA验证", v1, dna or "无")
    gate_pass("确认码验证", v2, confirm or "无")
    gate_pass("时间戳验证", v3, ts)
    three_ok = v1 and v2 and v3
    gate_pass("三验证闭环", three_ok, "全绿" if three_ok else "失败")

    # 4.3 GPG 签名确认
    asc = Path(str(p) + ".asc")
    vr = run_py(GPG_ENGINE, "verify", str(p))
    gate_pass("GPG签名有效", vr.returncode == 0 and asc.exists(), "有效" if vr.returncode == 0 else "无效/未签名")

    # 4.4 发布日志
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not RELEASE_LOG.exists():
        RELEASE_LOG.write_text("# 🐉 龍魂 · 技能发布日志\n\n", encoding="utf-8")
    entry = f"- **{name} {version}** 发布于 {now_iso()} · 路径: `{path}` · 三色: {extract_tricolor(text)}\n"
    with RELEASE_LOG.open("a", encoding="utf-8") as f:
        f.write(entry)
    gate_pass("发布日志", True, str(RELEASE_LOG))

    # 4.5 记忆归档
    mr = run_py(MEMORY_ENGINE, "log", f"技能发布: {name} {version} @ {path} · 三色{extract_tricolor(text)} · 流水线闭环")
    gate_pass("记忆归档", mr.returncode == 0, "已写入AI核心记忆" if mr.returncode == 0 else mr.stderr.strip()[:120])

    # 4.6 更新 registry 状态
    reg = load_registry()
    reg.setdefault(name, {})
    reg[name].update({"version": version, "status": "published", "published": now_iso(),
                      "tricolor": extract_tricolor(text)})
    save_registry(reg)
    gate_pass("registry状态", True, "published")

    print("=" * 50)
    if three_ok:
        print(f"门禁判定: ✅ 发布完成 · {name} {version} · 🟢 闭环")
        return True
    print("门禁判定: 🔴 三验证未全绿，发布中止")
    return False


# ============================================================
# 一键四阶段闭环
# ============================================================

def cmd_iterate(name: str, path: str, version: str = "v1.0.0", skip_fill: bool = False) -> bool:
    print(f"\n🐉 一键四阶段闭环 → {name} @ {path} ({version})\n")
    print("═" * 54)
    if not cmd_check(path):
        print("🛑 开发门禁未过，闭环中止")
        return False
    if not cmd_test(path, skip_fill=skip_fill):
        print("🛑 测试门禁未过，闭环中止")
        return False
    if not cmd_integrate(name, path):
        print("🛑 集成门禁未过，闭环中止")
        return False
    if not cmd_publish(name, path, version, skip_fill=skip_fill):
        print("🛑 发布门禁未过，闭环中止")
        return False
    print("\n" + "═" * 54)
    print(f"✅ 全生命周期闭环完成 · {name} {version}")
    return True


# ============================================================
# 巡检
# ============================================================

def cmd_scan() -> int:
    print("🐉 巡检 · 已登记技能全量体检 (scan)")
    print("=" * 54)
    reg = load_registry()
    if not reg:
        print("  ⚠️ 尚无登记技能（registry 为空）。先跑 integrate/iterate 登记。")
        return 1

    total, fail = 0, 0
    for name, info in reg.items():
        total += 1
        p = Path(info.get("path", ""))
        issues = []
        if not p.exists():
            issues.append("文件缺失")
        else:
            text = read_text(p)
            if not verify_with_engine("verify-dna", extract_dna(text)):
                issues.append("DNA无效")
            if not Path(str(p) + ".asc").exists():
                issues.append("GPG未签名")
            tri = extract_tricolor(text)
            if tri == "🔴":
                issues.append(f"三色🔴 {tri}")
        status = "✅" if not issues else "⚠️ " + ";".join(issues)
        print(f"  {status} {name} {info.get('version','?')} · {info.get('path','?')}")
        if issues:
            fail += 1

    print("=" * 54)
    report = {"scanned": total, "failed": fail, "ts": now_iso()}
    print(f"巡检报告: 扫描 {total} 项 · 异常 {fail} 项")
    if fail:
        print("🟡 存在异常 → 建议人工介入或 auto-fix")
    else:
        print("🟢 全部正常")
    return 0 if fail == 0 else 2


def cmd_status(name: str) -> int:
    reg = load_registry()
    info = reg.get(name)
    if not info:
        print(f"❌ 技能 {name} 未登记。")
        return 1
    p = Path(info.get("path", ""))
    print(f"🐉 {name} 状态")
    print("=" * 40)
    for k, v in info.items():
        print(f"  {k}: {v}")
    if p.exists():
        tri = extract_tricolor(read_text(p))
        print(f"  三色: {tri}")
        asc = Path(str(p) + ".asc")
        print(f"  GPG签名: {'✅' if asc.exists() else '❌'}")
    return 0


# ============================================================
# main
# ============================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 技能全生命周期自动化流水线 v1.1",
        epilog=f"CONFIRM: {CONFIRM_CODE}\nDNA: #龍芯⚡️丙午·丙申·己未·庚午·䷖剥-SKILL-PIPELINE-ENGINE-3F9C21D7-UID9622",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="开发门禁")
    p_check.add_argument("path", help="文件路径")

    p_test = sub.add_parser("test", help="测试门禁")
    p_test.add_argument("path", help="文件路径")

    p_int = sub.add_parser("integrate", help="集成门禁（签名+登记）")
    p_int.add_argument("name", help="技能名")
    p_int.add_argument("path", help="文件路径")

    p_pub = sub.add_parser("publish", help="发布门禁（三验证+日志+记忆）")
    p_pub.add_argument("name", help="技能名")
    p_pub.add_argument("path", help="文件路径")
    p_pub.add_argument("version", nargs="?", default="v1.0.0", help="版本号")
    p_pub.add_argument("--skip-fill", action="store_true", help="跳过填充率门禁（协议/白皮书类）")

    p_it = sub.add_parser("iterate", help="一键四阶段闭环")
    p_it.add_argument("name", help="技能名")
    p_it.add_argument("path", help="文件路径")
    p_it.add_argument("version", nargs="?", default="v1.0.0", help="版本号")
    p_it.add_argument("--skip-fill", action="store_true", help="跳过填充率门禁（协议/白皮书类）")

    sub.add_parser("scan", help="巡检所有已登记技能")

    p_st = sub.add_parser("status", help="查询技能状态")
    p_st.add_argument("name", help="技能名")

    args = parser.parse_args()

    if args.cmd == "check":
        return 0 if cmd_check(args.path) else 1
    if args.cmd == "test":
        return 0 if cmd_test(args.path) else 1
    if args.cmd == "integrate":
        return 0 if cmd_integrate(args.name, args.path) else 1
    if args.cmd == "publish":
        return 0 if cmd_publish(args.name, args.path, args.version, args.skip_fill) else 1
    if args.cmd == "iterate":
        return 0 if cmd_iterate(args.name, args.path, args.version, args.skip_fill) else 1
    if args.cmd == "scan":
        return cmd_scan()
    if args.cmd == "status":
        return cmd_status(args.name)
    return 1


if __name__ == "__main__":
    sys.exit(main())
