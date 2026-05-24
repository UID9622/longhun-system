#!/usr/bin/env bash
# 龍字符律 · 扫描 bin / .cursor/rules / 01_protocols 中误用简体「龍」
# DNA: #龍芯⚡2026-05-18-LONG-CHARACTER-LAW-SCAN-v1.0
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/_longhun_common.sh"

export LONGHUN_ROOT
exec "${LONGHUN_ROOT}/venv/bin/python" - "$LONGHUN_ROOT" <<'PY'
import os, re, sys

root = sys.argv[1]
scan_dirs = [
    os.path.join(root, "bin"),
    os.path.join(root, ".cursor", "rules"),
    os.path.join(root, "01_protocols"),
]
# 行内允许出现简体「龍」的说明语境（熔断/禁止/对比）
ALLOW = re.compile(
    r"禁止|熔断|简体|不写龍|G5|字符律|写错|冒充|红线|黑名单|OVERCLAIM|"
    r"simp_long|龍/龍|「龍」|\"龍\"|'龍'|扫描|误用|兼容文件名|"
    r"re\.compile|BAD_PATTERNS|应为|建议|误写|legacy"
)
SKIP_NAMES = {
    "龍字符律扫描.sh",
    "PROTOCOL__LONG-CHARACTER-LAW-v1.0.local.md",
    "PROTOCOL__AI-HANDSHAKE-BASELINE-v1.0.local.md",
    "uid9622-long-character-law.mdc",
    "uid9622-ai-handshake-baseline.mdc",
    "uid9622-home-battlefield-dev-env.mdc",
}
# 品牌/系统误用
BAD_PATTERNS = [
    (re.compile(r"龍魂"), "龍魂 → 应为 龍魂"),
    (re.compile(r"龍芯"), "龍芯 → 应为 龍芯"),
    (re.compile(r"一条龍"), "一条龍 → 建议 一條龍（对外文案）"),
    (re.compile(r"开龍魂"), "开龍魂 → 路径请用 开龍魂（或保留文件名+symlink）"),
    (re.compile(r"收龍魂"), "收龍魂 → 路径请用 收龍魂"),
]

hits = []
for base in scan_dirs:
    if not os.path.isdir(base):
        continue
    for dirpath, _, files in os.walk(base):
        if "__pycache__" in dirpath or ".venv" in dirpath:
            continue
        for fn in files:
            if fn.endswith((".pyc", ".png", ".jpg")) or fn in SKIP_NAMES:
                continue
            path = os.path.join(dirpath, fn)
            try:
                text = open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if ALLOW.search(line):
                    continue
                for pat, msg in BAD_PATTERNS:
                    if pat.search(line):
                        hits.append((path, i, line.strip()[:120], msg))

if not hits:
    print("🟢 龍字符律扫描：未发现误用简体「龍」（扫描范围: bin · .cursor/rules · 01_protocols）")
    sys.exit(0)

print("🔴 龍字符律扫描：发现 %d 处待改\n" % len(hits))
for path, ln, preview, msg in hits[:40]:
    print(f"  {path}:{ln}")
    print(f"    {msg}")
    print(f"    | {preview}")
if len(hits) > 40:
    print(f"  … 另有 {len(hits) - 40} 处")
sys.exit(1)
PY
