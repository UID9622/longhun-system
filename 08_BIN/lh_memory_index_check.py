# DNA: #龍芯⚡️丙午·丙申·癸巳·戌时·䷬萃-MEMORY-INDEX-CHECK-V1.0-P09-LAND
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 功能: 龍魂记忆索引一致性校验 v1.0.1（P09 孙思邈·断链检查）
#   扫描 12_DOCS/dragon-soul-open-hub/memory-hub.json 全部条目的
#   title/content/keywords 中引用的本地文件路径，逐条验证存在性，
#   输出断链清单。只检测不自动改（不删除只冻结）。
#   配套: 跨AI协作记忆库 memory-hub.json（Notion 库 3c17125a 本地镜像）

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEMORY_HUB = ROOT / "12_DOCS/dragon-soul-open-hub/memory-hub.json"

# 引用路径提取：支持中英文路径 · 扩展名长优先(jsonl>json) · 过滤 URL/哈希
_PATH_RE = re.compile(
    r"(?<![\w./-])((?:[\u4e00-\u9fff\w]+/)?[\w\u4e00-\u9fff./-]+"
    r"\.(?:jsonl|md|py|sh|json|js|ts|html|htm|css|toml|yaml|yml|txt|asc|svg|png|db|plist|conf))",
    re.IGNORECASE,
)


# 常见前缀探测表（裸文件名 → 兜底探测，降误报）
PROBE_PREFIXES = [
    "",                                       # 原样
    "bin/", "08_BIN/",                        # 引擎目录
    "12_DOCS/dragon-soul-open-hub/",          # 记忆库本目录
    "01_protocols/", "config/", "03_compiler/",
    "_work/frozen-20260822-docs/",            # 冻结归档（2026-08-22 目录整理）
    "papers/field-dynamics/",                 # 黎曼·场动力学论文区
    "papers/field-dynamics/evaluator/",
]


def _extract_refs(text: str) -> tuple[list, list]:
    """从文本中提取疑似本地文件引用，返回 (refs, external) 两类"""
    refs, external = set(), set()
    for m in _PATH_RE.finditer(text):
        p = m.group(1).strip(" ,;\"'()[]`")
        if not p or p.startswith(("http://", "https://", "www.", "mailto:")):
            continue
        if p.count(".") > 2:            # 排除语义版本号/hash 串
            continue
        # ① 先归一化前缀：剥 ./ 、~/ 、根 /
        if p.startswith(("./", "~/")):  # 剥 ./ 前缀
            p = p[2:] if p.startswith("./") else p.lstrip("~/")
        if p.startswith("/"):           # 剥根前缀
            p = p.lstrip("/")
        # ② home/绝对路径引用（~/.longhun、/Users/..、.codebuddy、vault/）→ 外部引用
        if (
            p.startswith(("/Users/", "/~", "~", "/opt/", "/var/", "/etc/"))
            or p.startswith((".codebuddy", ".longhun", ".gnupg", ".ssh", ".config"))
            or p.startswith("vault/")
        ):
            external.add(p)
            continue
        # ③ 隐藏临时文件（.issue-body.md 等 git 操作产物）→ 跳过
        if p.startswith(".") and "/" not in p:
            continue
        # ④ 纯数字+扩展名（12.asc 交付包编号）→ 跳过
        if re.match(r"^\d+\.(asc|json|txt|md|py)$", p):
            continue
        # ⑤ 清单文本段（evaluator.py/gen_sample_log.py 交付包清单）→ 跳过
        if p.count("/") == 1 and p.endswith(".py"):
            a, b = p.split("/")
            if a.endswith(".py") or b.endswith(".py"):
                continue
        if "#" in p:                    # 剥锚点
            p = p.split("#")[0]
        if len(p) < 5:
            continue
        # 列表碎片过滤：3+ 段且含 .asc/.json 等被 / 拼接（README/CONTRIBUTING/LICENSE）
        if p.count("/") >= 2 and any(
            seg.upper() in {"README", "LICENSE", "CONTRIBUTING", "RESULTS", "PROPOSAL"}
            for seg in p.split("/")
        ):
            continue
        refs.add(p)
    return sorted(refs), sorted(external)


def scan(hub_path: Path = MEMORY_HUB) -> dict:
    """断链扫描：返回统计 + 断链清单（含引用条目上下文）"""
    if not hub_path.exists():
        return {"error": f"memory-hub 不存在: {hub_path}", "total_entries": 0}

    data = json.loads(hub_path.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    total_refs = 0
    broken = {}          # 断链路径 -> [来源条目 title]
    ref_counts = {}      # 有效引用计数（解析到的权威路径）
    external = set()     # home/根路径引用（不判断链）
    for e in entries:
        title = e.get("title", "?")
        blob = " ".join(
            str(e.get(k, "")) for k in ("title", "content", "keywords")
        )
        refs, ext = _extract_refs(blob)
        external.update(ext)
        for p in refs:
            total_refs += 1
            hit = None
            for pre in PROBE_PREFIXES:
                fp = ROOT / (pre + p)
                if fp.exists():
                    hit = pre + p
                    break
            if not hit and p.startswith("docs/"):
                # docs/ 已在 2026-08-22 冻结到 _work/frozen-20260822-docs/
                fp = ROOT / "_work/frozen-20260822-docs/" / p[len("docs/"):]
                if fp.exists():
                    hit = "_work/frozen-20260822-docs/" + p[len("docs/"):]
            if not hit:
                # 中文描述前缀剥离（"执行器bin/..." → "bin/..."）再探测
                stripped = re.sub(r"^[\u4e00-\u9fff]+", "", p)
                if stripped != p:
                    for pre in PROBE_PREFIXES:
                        fp = ROOT / (pre + stripped)
                        if fp.exists():
                            hit = pre + stripped
                            break
            if hit:
                ref_counts[hit] = ref_counts.get(hit, 0) + 1
            else:
                broken.setdefault(p, []).append(title)

    return {
        "hub": str(hub_path.relative_to(ROOT)),
        "total_entries": len(entries),
        "total_refs": total_refs,
        "valid_refs": len(ref_counts),
        "broken_refs": len(broken),
        "broken": {k: v[:3] for k, v in sorted(broken.items())},
        "external_refs": sorted(external),
        "top_referenced": sorted(ref_counts.items(), key=lambda x: -x[1])[:10],
    }


def report(r: dict) -> str:
    if "error" in r:
        return f"🔴 {r['error']}"
    lines = [
        "龍魂记忆索引一致性校验 v1.0",
        f"记忆库: {r['hub']} · 条目 {r['total_entries']}",
        f"本地引用总数: {r['total_refs']} · 有效 {r['valid_refs']} · 断链 {r['broken_refs']}",
    ]
    if r["broken"]:
        lines.append("🔴 断链清单:")
        for p, src in list(r["broken"].items())[:30]:
            lines.append(f"  ✗ {p}  ← {src[0][:30]}")
        if len(r["broken"]) > 30:
            lines.append(f"  … 其余 {len(r['broken'])-30} 条")
    else:
        lines.append("🟢 无断链，记忆索引一致")
    if r.get("external_refs"):
        lines.append("ℹ️ home/根路径引用(不判链): " + ", ".join(r["external_refs"]))
    lines.append("被引用最多的本地文件: " + ", ".join(f"{p}({c})" for p, c in r["top_referenced"]))
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    r = scan()
    if "--json" in args:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(report(r))
    # 🔴 有断链 → 退出码 1（供 CI/pre-commit 检测）
    if r.get("broken_refs") != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
