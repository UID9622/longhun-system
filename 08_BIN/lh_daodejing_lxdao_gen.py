#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·甲子·未时·䷖剥-DAODEJING-LXDAO-GEN-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)（工程实现层）
"""
🐉 龍魂 · 道德经81章 LX-DAO 标准条目生成器 v1.0
来源: 《诸葛亮沙盒训练场》v2.0 归档版（文档进度 4/81 → 本生成器全量 81/81）
数据源: 12_DOCS/道德经81章_龍魂系统大白话解读_完整版_v5.0.md
P05 诚实标注: ①semantic_hash 真实SHA256（文档手写占位→真实计算）
②translation_en 缺省置空不编造（v5.0无英文数据）③key_concepts 标注derived
用法: python3 bin/lh_daodejing_lxdao_gen.py [--chapter N | --stats]
DNA: #龍芯⚡️丙午·丙申·甲子·未时·䷖剥-DAODEJING-LXDAO-GEN-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
import re, sys, json, hashlib, importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT / "12_DOCS" / "道德经81章_龍魂系统大白话解读_完整版_v5.0.md"
OUTPUT_DIR = ROOT / "data" / "lx_dao"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
CHAPTER_RE = re.compile(r"^## 第(\d+)章 · (.+)$")
TABLE_FIELD_RE = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.*?)\s*\|\s*$")


def _dna_stamp(module="LXDAO-GEN", action="GEN"):
    try:
        spec = importlib.util.spec_from_file_location("lh_time_engine", ROOT / "bin" / "lh_time_engine.py")
        te = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(te)
        ganzhi = te.get_output_stamp(format_type="compact").replace("#龍芯⚡️", "")
        h8 = hashlib.sha256(f"{module}:{action}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ganzhi}-{module}-{action}-{h8}"
    except Exception:
        return f"#龍芯⚡️干支未取-{module}-{action}-DEGRADED"


def sha256_real(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_chapters(md_text):
    chapters, blocks, cur_num = {}, {}, None
    for line in md_text.split("\n"):
        m = CHAPTER_RE.match(line.strip())
        if m:
            cur_num = int(m.group(1))
            blocks[cur_num] = [line]
        elif cur_num is not None:
            blocks[cur_num].append(line)
    for num, blk in blocks.items():
        ch = {"title": "", "fields": {}, "judgments": [], "daode_map": "", "one_liner": ""}
        in_map, map_lines = False, []
        for line in blk:
            s = line.strip()
            m = CHAPTER_RE.match(s)
            if m:
                ch["title"] = m.group(2).strip()
                continue
            tf = TABLE_FIELD_RE.match(s)
            if tf:
                field, val = tf.group(1).strip(), tf.group(2).strip()
                field_map = {"原文": "quote_full", "大白話": "meaning_cn", "易經卦象": "hexagram",
                             "三六九": "sanliujiu", "生肖": "zodiac", "什麼時候用": "usage",
                             "老子實際想說什麼": "real_meaning"}
                if field in field_map:
                    ch["fields"][field_map[field]] = val
                continue
            jm = re.match(r"^(\d+)\.\s+(.+)$", s)
            if jm and 1 <= int(jm.group(1)) <= 5 and len(jm.group(2)) < 200:
                ch["judgments"].append(jm.group(2).strip())
                continue
            if s.startswith("#### 龍魂系統映射") or s.startswith("#### 龍魂系统映射"):
                in_map = True
                continue
            if s.startswith("#### "):
                in_map = False
            if in_map and s:
                map_lines.append(s)
            if s.startswith(">"):
                ch["one_liner"] = s.lstrip(">").strip()
        ch["daode_map"] = "".join(map_lines).strip()
        chapters[num] = ch
    return chapters


def build_lxdao(num, ch, total):
    quote = ch["fields"].get("quote_full", "")
    meaning = ch["fields"].get("meaning_cn", "")
    hexagram = ch["fields"].get("hexagram", "")
    sanliujiu = ch["fields"].get("sanliujiu", "")
    zodiac = ch["fields"].get("zodiac", "")
    usage = ch["fields"].get("usage", "")
    real = ch["fields"].get("real_meaning", "")
    one_liner = ch["one_liner"] or ""
    notes = []
    if not quote:
        quote, notes = meaning, notes + ["quote_full 由 meaning_cn 回填"]
    if not meaning:
        meaning, notes = real, notes + ["meaning_cn 由 real_meaning 回填"]
    semantic_hash = sha256_real(f"{num}|{quote}|{meaning}|{hexagram}")
    key_concepts = []
    for j in ch["judgments"][:5]:
        t = j.strip('"').strip("*")
        key_concepts.append({"term": t.split("=")[0].strip()[:12], "definition": t[:80], "derived": True})
    if not key_concepts:
        key_concepts = [{"term": (meaning or "道")[:12], "definition": (meaning or "待补")[:80], "derived": True}]
        notes += ["核心判斷缺省·key_concepts 由 meaning_cn 派生"]
    reasoning = f"第{num}章'{(meaning or quote)[:14]}'对应{hexagram or '乾卦'}·太极/阴阳/天道"
    return {
        "meta": {
            "anchor_id": f"LX-DAO-{num:03d}", "source_version": "王弼本",
            "chapter_title": f"道德经·第{num}章（{ch['title']}）",
            "creation_date": "2026-08-18", "last_modified": "2026-08-18",
            "uid9622_exclusive": True, "generator_dna": _dna_stamp("LXDAO-GEN", f"GEN-{num:03d}"),
        },
        "source": {"chapter_index": num, "quote_full": quote, "translation_en": ""},
        "semantic": {
            "core_tags": [], "meaning_cn": meaning, "key_concepts": key_concepts,
            "ai_application": f"{ch['daode_map'] or '（龍魂系統映射缺省）'} · 一句话指南: {one_liner or '（缺省）'}",
            "sanliujiu": sanliujiu, "zodiac": zodiac, "usage": usage, "one_liner": one_liner,
        },
        "integrity": {
            "semantic_hash": semantic_hash, "verification_method": "SHA256",
            "chain_link": {
                "prev_chapter": f"LX-DAO-{num-1:03d}" if num > 1 else None,
                "next_chapter": f"LX-DAO-{num+1:03d}" if num < total else None,
            },
        },
        "uid9622_lock": {
            "status": "LOCKED_TO_UID9622", "gpg_fingerprint": GPG_FINGERPRINT,
            "authorization_code": CONFIRM_CODE, "immutable": True,
            "modification_policy": "Only UID9622 with valid GPG signature can modify",
        },
        "yijing_correlation": {
            "related_hexagrams": [hexagram] if hexagram else ["乾卦"], "reasoning": reasoning,
        },
        "training_notes": {
            "zhuge_comment": f"沙盒训练·第{num}章·原文档4/81→生成器全量落地",
            "priority": "P0_CRITICAL", "mastery_level": "MUST_MASTER",
        },
        "data_provenance": {
            "source_file": "12_DOCS/道德经81章_龍魂系统大白话解读_完整版_v5.0.md",
            "auto_generated": True,
            "notes": notes if notes else ["v5.0 全字段可用·无需回填"],
        },
    }


def main():
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help", "help"):
        print(__doc__ or "LH-DAO 81章标准条目生成器 v1.0")
        return 0
    only_chapter = None
    stats_only = False
    if "--chapter" in args:
        only_chapter = int(args[args.index("--chapter") + 1])
    if "--stats" in args:
        stats_only = True
    if not DEFAULT_SOURCE.exists():
        print(f"❌ 数据源缺失: {DEFAULT_SOURCE}")
        return 1
    chapters = parse_chapters(DEFAULT_SOURCE.read_text(encoding="utf-8"))
    if not chapters:
        print("❌ 解析失败：未找到任何章节（## 第N章）")
        return 1
    total = len(chapters)
    mq = sum(1 for c in chapters.values() if not c["fields"].get("quote_full"))
    mm = sum(1 for c in chapters.values() if not c["fields"].get("meaning_cn"))
    mh = sum(1 for c in chapters.values() if not c["fields"].get("hexagram"))
    if stats_only:
        print(f"📊 v5.0 解析统计: 共 {total} 章 · 原文缺失{mq} · 大白话缺失{mm} · 卦象缺失{mh}")
        print(f"   章号范围: {min(chapters)} ~ {max(chapters)}")
        return 0
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    jsonl_path = OUTPUT_DIR / "道德经81章_LXDAO标准条目_v1.0.jsonl"
    nums = [only_chapter] if only_chapter else sorted(chapters)
    records = []
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for num in nums:
            if num not in chapters:
                print(f"⚠️ 跳过缺章: {num}")
                continue
            rec = build_lxdao(num, chapters[num], total)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            records.append(rec)
    manifest = {
        "dna": _dna_stamp("LXDAO-GEN", "MANIFEST"), "generated_at": "2026-08-18",
        "total_chapters": len(records), "source_file": str(DEFAULT_SOURCE.relative_to(ROOT)),
        "output_file": str(jsonl_path.relative_to(ROOT)), "gpg_fingerprint": GPG_FINGERPRINT,
        "confirmation": CONFIRM_CODE,
        "stats": {"missing_quote": mq, "missing_meaning": mm, "missing_hexagram": mh},
        "integrity": {"method": "SHA256",
                      "manifest_hash": sha256_real("".join(r["integrity"]["semantic_hash"] for r in records))},
    }
    manifest_path = OUTPUT_DIR / "lxdao_manifest_v1.0.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 生成完成: {len(records)}/{total} 章 → {jsonl_path.relative_to(ROOT)}")
    print(f"   manifest: {manifest_path.relative_to(ROOT)}")
    print(f"   DNA: {manifest['dna']}")
    if mq or mm or mh:
        print(f"   ⚠️ 回填/缺省: 原文{mq} · 大白话{mm} · 卦象{mh}（详见 data_provenance.notes）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
