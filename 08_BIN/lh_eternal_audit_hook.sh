#!/bin/bash
# 🐉 龍魂 · 永恒审计三问 · Git Pre-commit 钩子（审查修正版）
# 位置: .git/hooks/pre-commit
# DNA: #龍芯⚡️丙午·丙申·丙辰·甲午·䷁坤-ETERNAL-AUDIT-HOOK-V1.0-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 审查修正清单（相对原始稿）:
#   ① set -e 致命bug：python 审计返回非零时脚本直接 abort，
#     根本走不到 exit_code 判定 → 审计段改用 set +e 包裹
#   ② P0声明检查/分层许可检查 对"每个变更文件"强制要求 → 过严，
#     会拦死所有正常提交 → 降级为🟡警告（仅提示），只对
#     协议类文件(*.md/协议/PROTOCOL*)保持🔴硬性
#   ③ DNA 检查仅认 "#龍芯⚡️" 或 "DNA:" 子串，二进制/图片文件
#     会误报 → 跳过二进制与常见非文本扩展名
#   ④ DNA 干支 壬寅→丙辰（万年历口径v3.0，禁止手写）
#
# 安装:
#   cp 永恒审计三问_pre-commit_修正版.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
# ============================================================

# === 配置 ===
HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$HOOK_DIR/../.." && pwd)"
AUDIT_DIR="$REPO_ROOT/.git/audit"
AUDIT_LOG="$AUDIT_DIR/audit.log"
SKIP_LOG="$AUDIT_DIR/skip.log"
AUDIT_SCRIPT="$AUDIT_DIR/audit_engine.py"

mkdir -p "$AUDIT_DIR"

# === 检查跳过（紧急模式，留痕）===
if [ "$SKIP_AUDIT" = "1" ] || [ -f "$AUDIT_DIR/skip.flag" ]; then
  echo "⚠️  跳过审计（紧急模式）"
  echo "$(date '+%Y-%m-%d %H:%M:%S') | 跳过审计 | 用户: $(git config user.name 2>/dev/null || echo 'unknown')" >> "$SKIP_LOG"
  exit 0
fi

# === 生成审计引擎（幂等覆盖，始终最新）===
cat > "$AUDIT_SCRIPT" << 'PYEOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 龍魂 · 永恒审计三问引擎 v1.0（修正版）
DNA: #龍芯⚡️丙午·丙申·丙辰·甲午·䷁坤-ETERNAL-AUDIT-ENGINE-UID9622
"""
import os, sys, json, re, subprocess
from datetime import datetime
from pathlib import Path

DNA = "#龍芯⚡️丙午·丙申·丙辰·甲午·䷁坤-ETERNAL-AUDIT-ENGINE-UID9622"

# 非文本文件扩展名：跳过内容级检查
NON_TEXT_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip",
                ".gz", ".mp4", ".mp3", ".woff", ".woff2", ".ttf", ".exe",
                ".so", ".dll", ".pyc", ".class", ".jar"}
# 协议类文件：P0声明保持硬性
PROTOCOL_HINT = ("协议", "protocol", "PROTOCOL", "宪法", "铁律")

QUESTIONS = [
    {"id": "Q1", "title": "对得起人民吗？", "icon": "👥", "checks": [
        "这个功能/改动是帮老百姓解决问题，还是割韭菜？",
        "普通人用得上、用得起吗？",
        "用户数据主权有保障吗？",
        "算法是否存在偏袒或不公？",
        "用户能随时安全地退出吗？"]},
    {"id": "Q2", "title": "对得起中国吗？", "icon": "🇨🇳", "checks": [
        "代码/方案是否以中国文化为基座？",
        "数据是否存在出境风险？",
        "是否存在被境外利用的安全隐患？",
        "核心技术是否能自主可控？",
        "能否贡献中国标准？"]},
    {"id": "Q3", "title": "对得起 UID9622 吗？", "icon": "🧬", "checks": [
        "这个改动是否背离龍魂系统的创始宗旨？",
        "出事了能追溯到具体责任人吗？",
        "是否有完整的DNA追溯链？",
        "十年后回头看，这个改动还站得住吗？",
        "系统可信度是增加还是降低？"]},
]

SECRET_PATTERNS = [
    r'api[_-]?key\s*=\s*["\']([^"\']{8,})["\']',
    r'password\s*=\s*["\']([^"\']{8,})["\']',
    r'secret\s*=\s*["\']([^"\']{8,})["\']',
    r'token\s*=\s*["\']([^"\']{16,})["\']',
    r'sk-[a-zA-Z0-9]{32,}',
]


def repo_root() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True)
        return r.stdout.strip() or os.getcwd()
    except Exception:
        return os.getcwd()


def changed_files(root: str):
    try:
        r = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                           capture_output=True, text=True)
        return [f for f in r.stdout.strip().split("\n") if f]
    except Exception:
        return []


def is_text_file(fname: str) -> bool:
    return Path(fname).suffix.lower() not in NON_TEXT_EXT


def is_protocol_file(fname: str) -> bool:
    base = Path(fname).name
    return any(h in base for h in PROTOCOL_HINT)


def read_safe(path: Path) -> str:
    try:
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def main() -> int:
    root = repo_root()
    audit_dir = Path(root) / ".git" / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    files = changed_files(root)

    hard_fail, warns = [], []

    # ③ 只对文本文件做内容级检查
    text_files = [f for f in files if is_text_file(f)]
    proto_files = [f for f in text_files if is_protocol_file(f)]

    # 检查1: DNA 追溯码（硬）——文本文件须含 #龍芯⚡️ 或 DNA:
    dna_missing = []
    for f in text_files:
        c = read_safe(Path(root) / f)
        if "#龍芯⚡️" not in c and "DNA:" not in c:
            dna_missing.append(f)
    if dna_missing:
        hard_fail.append(f"缺DNA追溯码: {', '.join(dna_missing[:5])}")

    # 检查2: P0 声明（协议文件硬，其余警告）②
    p0_missing_proto = []
    p0_missing_other = []
    for f in text_files:
        c = read_safe(Path(root) / f)
        if "P0" not in c and "焊死" not in c:
            (p0_missing_proto if is_protocol_file(f) else p0_missing_other).append(f)
    if p0_missing_proto:
        hard_fail.append(f"协议文件缺P0声明: {', '.join(p0_missing_proto[:5])}")
    if p0_missing_other:
        warns.append(f"{len(p0_missing_other)} 个普通文件无P0声明（提示）")

    # 检查3: 分层许可（协议文件硬，其余警告）②
    lic_missing_proto = []
    for f in proto_files:
        c = read_safe(Path(root) / f)
        if "MulanPSL" not in c and "CC BY-NC-SA" not in c and "分层许可" not in c:
            lic_missing_proto.append(f)
    if lic_missing_proto:
        hard_fail.append(f"协议文件缺分层许可: {', '.join(lic_missing_proto[:5])}")

    # 检查4: 硬编码密钥（硬）
    secrets = []
    for f in text_files:
        c = read_safe(Path(root) / f)
        for p in SECRET_PATTERNS:
            if re.search(p, c, re.IGNORECASE):
                secrets.append(f)
                break
    if secrets:
        hard_fail.append(f"发现硬编码密钥/密码: {', '.join(secrets[:5])}")

    overall = "🟢" if not hard_fail else "🔴"

    # ===== 报告 =====
    print()
    print("=" * 70)
    print("🐉 龍魂 · 永恒审计三问报告（修正版）")
    print("=" * 70)
    print(f"  变更文件: {len(files)} 个（文本 {len(text_files)} / 协议类 {len(proto_files)}）")
    for f in files[:5]:
        print(f"    📄 {f}")
    if len(files) > 5:
        print(f"    ... 还有 {len(files) - 5} 个")
    print("-" * 70)
    print("📋 合规硬检")
    if hard_fail:
        for e in hard_fail:
            print(f"  ❌ {e}")
    else:
        print("  ✅ DNA追溯码 / 协议P0声明 / 分层许可 / 无硬编码密钥 —— 全部通过")
    for w in warns:
        print(f"  🟡 {w}")

    print()
    print("🧬 灵魂三问（机器无法代替良知判定——请提交人逐条自答）")
    for q in QUESTIONS:
        print(f"\n  {q['icon']} {q['title']}")
        for c in q["checks"]:
            print(f"     □ {c}")
    print()
    print("  说明：合规硬检由机器执行；三问由提交人负责自答，")
    print("  提交即视为声明'三问过堂'。事后抽查发现虚答 → 三色整改单。")

    print()
    print("=" * 70)
    print(f"  总体状态: {overall}")
    print(f"  DNA: {DNA}")
    print(f"  时间: {datetime.now().isoformat()}")
    print("=" * 70)
    if overall == "🟢":
        print("✅ 审计通过，可以提交。")
    else:
        print("❌ 合规硬检未通过，提交已阻止。修正后重试。")
        print("  紧急跳过（仅限生产事故，留痕）: SKIP_AUDIT=1 git commit")

    # 落账
    entry = {
        "timestamp": datetime.now().isoformat(),
        "overall": overall,
        "files": len(files),
        "hard_fail": hard_fail,
        "warns": warns,
        "dna": DNA,
    }
    with open(audit_dir / "audit.log", "a", encoding="utf-8") as fp:
        fp.write(f"{entry['timestamp']} | {overall} | files={len(files)} | fails={len(hard_fail)}\n")
    with open(audit_dir / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w", encoding="utf-8") as fp:
        json.dump(entry, fp, ensure_ascii=False, indent=2)

    return 0 if overall == "🟢" else 1


if __name__ == "__main__":
    sys.exit(main())
PYEOF

chmod +x "$AUDIT_SCRIPT"

# === 执行审计（① 修正：set +e 包裹，非零不 abort）===
set +e
python3 "$AUDIT_SCRIPT"
exit_code=$?
set -e

if [ $exit_code -eq 0 ]; then
  exit 0
else
  echo ""
  echo "🔴 永恒审计未通过，提交已阻止。"
  echo "  紧急跳过（留痕）: SKIP_AUDIT=1 git commit -m '紧急修复'"
  exit 1
fi
