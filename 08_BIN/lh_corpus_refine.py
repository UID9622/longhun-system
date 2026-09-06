#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-06-未时-CORPUS-REFINE-V1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 父任务: D-01 S3 语料扩源(老大 2026-09-06 拍板·批次A道德经+批次B知识文白名单)
# 说明: 扩源前置精炼(门槛①②③) → 输出 corpus/raw/{daodejing,knowledge}/ 后走官方 B 轨 clean(门槛④)
#   规则(与老大收条逐条对齐):
#     ① 去重: 段落级 sha256 跨文件去重
#     ② 滤行: 含 #CONFIRM/#审计/#流水/#SEAL 行·# 开头行(markdown 标题除外规则见下)
#             ·以 #龍芯⚡️/DNA/CONFIRM/SEAL 开头的元数据行 → 整行丢弃(DNA 行=元数据非知识)
#            ※ 保留 markdown 结构标题(## 第N章/文章小节)作为知识分段,不整滤;
#              仅滤"元数据型 # 行"(DNA/CONFIRM/SEAL/审计/流水/归位行)
#     ③ 最短行: <20 字符段落丢弃(--min-len 20)
#     + P3 模板占位行滤(老大指定: 待补充/占位/TBD/待填)
#   用法: python3 bin/lh_corpus_refine.py            # 跑 A+B 全部
#         python3 bin/lh_corpus_refine.py --batch A  # 仅道德经
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_A = ROOT / "corpus" / "raw" / "daodejing"
OUT_B = ROOT / "corpus" / "raw" / "knowledge"
MANIFEST = ROOT / "corpus" / "raw" / "refine_manifest.json"

# 批次A: 道德经81章龍魂解读(md 正文源·337 对话对不入此(直进 exp 训练数据·见验证脚本))
SOURCES_A = [
    "12_DOCS/道德经81章_龍魂系统大白话解读_完整版_v5.0.md",
    "12_DOCS/道德经81章_龍魂系统大白话解读_完整版_v4.1_多维度注解.md",
    "12_DOCS/daodejing/道德经81章_龍魂系统大白话解读_v4.1_结构化增强版.md",
]
# 批次B: 知识文白名单(老大清单·实况文件名已核·防空壳: 行为密码学实为 07-03 前缀+多版本·D01 仅收 md(不含 report.json))
SOURCES_B = [
    "articles/2026-07-03-行为密码学七因子视角-老实人与算计者.md",
    "articles/行为密码学csdn.md",
    "articles/行为密码学-统一框架-v3.0.md",
    "articles/2026-09-06-龍魂自研产品总览-v1.0.md",
    "articles/2026-09-06-ISO42001-gap-v1.0.md",
    "articles/2026-09-06-龍魂ASI能力落地台账v1.0.md",
    "articles/2026-09-06-龍魂ASI团队能力总览-Wiki专版.md",
    "articles/2026-09-06-龍魂ASI团队能力总览-Wiki首页Home.md",
    "articles/2026-09-06-龍魂ASI团队能力总览-内部README.md",
    "articles/2026-09-06-D01-gpu-route-v1.0.md",
    "articles/2026-09-06-D01-S1-词表迁移报告-v1.0.md",
    "cnsh/core/P3_seven_dimension_human_71_detailed_profile.md",
]

# 元数据/噪音行规则(行级)
META_PAT = re.compile(r"#\s*(DNA|CONFIRM|SEAL|龍芯⚡️|ZHUGEXIN)|#CONFIRM|#SEAL|#审计|#流水|#龍芯⚡️", re.I)
PLACEHOLDER_PAT = re.compile(r"待补充|占位|TBD|待填", re.I)
HASH_PREFIX = re.compile(r"^\s*#")
CORPUS_META = re.compile(r"corpusDNA|owner:|\.asc|glyph-backup")


def sha256h(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def refine_file(path, out_dir, seen, manifest):
    src = Path(path)
    if not src.exists():
        manifest["missing"].append(str(src))
        return
    raw = src.read_text(encoding="utf-8", errors="ignore")
    raw_lines = raw.splitlines()
    kept_lines = []
    f_stats = {"src": str(src), "src_lines": len(raw_lines), "drop_meta": 0,
               "drop_short": 0, "drop_dup": 0, "drop_ph": 0, "kept_paras": 0, "chars": 0}
    # 行级过滤(保留 markdown 标题 #/## → 知识结构;只滤元数据型)
    for ln in raw_lines:
        s = ln.strip()
        if not s:
            kept_lines.append("")
            continue
        if META_PAT.search(s) or CORPUS_META.search(s) or s.startswith("<!--"):
            f_stats["drop_meta"] += 1
            continue
        if PLACEHOLDER_PAT.search(s) and (s.count("：") >= 1 or "占位" in s):
            f_stats["drop_ph"] += 1
            continue
        kept_lines.append(s)
    # 段落化(空行分段)+ 门槛③ + 去重①
    paras = re.split(r"\n\s*\n", "\n".join(kept_lines))
    keep = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        if len(p) < 20:
            f_stats["drop_short"] += 1
            continue
        fp = sha256h(p)
        if fp in seen:
            f_stats["drop_dup"] += 1
            continue
        seen.add(fp)
        keep.append(p)
    if not keep:
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    body = "\n\n".join(keep) + "\n"
    dna = sha256h8(body)
    base = src.stem.replace("_", "-")[:60]
    out_p = out_dir / f"{base}.refined.txt"
    out_p.write_text(f"# src: {src}\n# paras: {len(keep)} | dna: {dna}\n\n{body}",
                     encoding="utf-8")
    f_stats.update({"kept_paras": len(keep), "chars": len(body), "out": str(out_p), "dna": dna})
    manifest["files"].append(f_stats)


def sha256h8(s):
    return sha256h(s)[:8]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", choices=["A", "B", "ALL"], default="ALL")
    args = ap.parse_args()
    manifest = {"dna": "#龍芯⚡️2026-09-06-未时-CORPUS-REFINE-V1.0-UID9622",
                "engine": "lh_corpus_refine.py v1.0",
                "rules": "去重hash级/滤元数据DNA行/占位行/短行<20 丢弃·标题保留为知识分段",
                "files": [], "missing": []}
    seen = set()
    if args.batch in ("A", "ALL"):
        for p in SOURCES_A:
            refine_file(p, OUT_A, seen, manifest)
    if args.batch in ("B", "ALL"):
        for p in SOURCES_B:
            refine_file(p, OUT_B, seen, manifest)
    tot = {k: sum(f.get(k, 0) for f in manifest["files"]) for k in
           ("src_lines", "drop_meta", "drop_short", "drop_dup", "drop_ph", "kept_paras", "chars")}
    manifest.update(tot)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print("🟢 扩源精炼完成(门槛①②③)")
    for k in ("src_lines", "drop_meta", "drop_ph", "drop_short", "drop_dup", "kept_paras", "chars"):
        print(f"   {k}: {tot[k]}")
    if manifest["missing"]:
        print("⚠️ 缺失源(如实列·不补造):")
        for m in manifest["missing"]:
            print("   -", m)
    print(f"   → manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
