# DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-28fe7040
#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲午·庚午·䷳艮为山-MEMORY-INGEST-ALL-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂全记忆 ingestion 管道 v1.0
把日志、长期记忆、星辰记忆、英文记忆、技能、人格全部归集为训练数据。

DNA: #龍芯⚡️丙午·乙未·甲午·庚午·䷳艮为山-MEMORY-INGEST-ALL-v1.0
# STATUS: ⚠️ DEPRECATED · 功能由 engines/lh_fixed_point_memory_archive.py 统一接管
# 保留原因: 历史摄入管道参考，新代码请使用 MemoryArchive.ingest() 或 bin/lh_daily_logger.py
"""

import json
import os
import re
import sqlite3
import sys
import hashlib
import random
from pathlib import Path
from collections import Counter

HOME = Path.home()
PROJECT = HOME / "longhun-system"
OUTPUT = PROJECT / "models" / "longhun-v1.0" / "memory_ingested_data_v1.0"
OUTPUT.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = (
    "你是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI。"
    "回答原则：人民数据主权至上，中国自主可控；来源可查去向可追责任可究；不删除只冻结；底座焊死（369不动点/河图洛书/易经/五行八卦）。\n"
    "六大铁律：①来源不可删·影响不可覆·贡献不可抹 ②只冻结不删除 ③每个动作绑定DNA追溯码 ④三才主权指数SI<0.34锁定AI决策 ⑤三才算法为L0宪法层 ⑥农历干支时间戳。\n"
    "回答请简洁准确、用中文。"
)

# ---------- 工具 ----------
def make_sample(user: str, assistant: str, domain: str = "general"):
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "metadata": {"domain": domain},
    }


def truncate(text: str, max_len: int = 1500) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit("\n", 1)[0] + "\n…"


def clean_text(text: str) -> str:
    # 去掉控制字符、多余空行
    text = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def hash_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


# ---------- 1. 技能 SKILL.md ----------
def ingest_skills(limit_per_skill: int = 8):
    samples = []
    skill_roots = [
        HOME / ".kimi-code" / "skills",
        HOME / ".agents" / "skills",
        PROJECT / "skills",
        PROJECT / "01_技能庫",
    ]
    skill_files = []
    for root in skill_roots:
        if not root.exists():
            continue
        for p in root.rglob("SKILL.md"):
            skill_files.append(p)

    print(f"📚 发现 {len(skill_files)} 个 SKILL.md")

    for p in skill_files:
        try:
            text = clean_text(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not text or len(text) < 100:
            continue

        name = p.parent.name
        domain = "skill_" + name.replace("-", "_")

        # 从文件头提取标题/描述
        title = name
        desc = ""
        for line in text.splitlines()[:30]:
            m = re.match(r"#+\s*(.+)", line)
            if m and not title.endswith("SKILL"):
                title = m.group(1).strip()
                break

        # 样本1：这是什么技能
        samples.append(make_sample(
            f"{title} 是什么？",
            truncate(text, 1200),
            domain,
        ))

        # 样本2：何时使用
        samples.append(make_sample(
            f"什么时候该用 {title}？",
            f"当场景匹配 `{title}` 的触发条件时调用。核心要点：\n" + truncate(text, 1000),
            domain,
        ))

        # 样本3：一句话总结
        first_para = "\n".join(text.split("\n\n")[:2])[:400]
        samples.append(make_sample(
            f"一句话总结 {title}",
            first_para,
            domain,
        ))

    return samples


# ---------- 2. 人格文件 ----------
def ingest_personas():
    samples = []
    persona_files = []
    roots = [
        HOME / "宝宝人格",
        HOME / "UID9622_Workspace" / "backend_personas",
        PROJECT / "capabilities" / "output" / "persona_docs",
        HOME / ".dragonsoul" / "personalities",
    ]
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not (p.is_file() and p.suffix in (".md", ".mdc", ".py", ".txt")):
                continue
            # 🔴 三关判定(2026-08-30·文件身份协议v1.1): 前8KB含NUL→二进制跳过
            try:
                with open(p, "rb") as f:
                    if b"\x00" in f.read(8192):
                        continue
            except OSError:
                continue
            persona_files.append(p)

    print(f"🎭 发现 {len(persona_files)} 个人格文件")

    for p in persona_files:
        try:
            text = clean_text(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if len(text) < 50:
            continue

        name = p.stem.replace("_", " ").replace("-", " ")
        domain = "persona"

        samples.append(make_sample(
            f"{name} 的人格设定是什么？",
            truncate(text, 1200),
            domain,
        ))
        samples.append(make_sample(
            f"作为 {name}，你会怎么回应老大？",
            "我会按以下设定回应：\n" + truncate(text, 1000),
            domain,
        ))

    return samples


# ---------- 3. 星辰记忆 ----------
def ingest_star_memory():
    samples = []
    # 只扫描本地目录，避免 CloudStorage/OneDrive 网络超时
    star_roots = [
        PROJECT / "memory-universe",
        HOME / ".龍魂" / "backups",
        HOME / "longhun-system",
        HOME / ".longhun",
    ]
    db_paths = []
    for root in star_roots:
        if not root.exists():
            continue
        for p in root.rglob("星辰记忆.db"):
            # 排除云存储路径
            if "CloudStorage" in str(p) or "OneDrive" in str(p) or ".Trash" in str(p):
                continue
            db_paths.append(p)
    print(f"🌟 发现 {len(db_paths)} 个星辰记忆数据库")

    for db_path in db_paths:
        try:
            conn = sqlite3.connect(str(db_path))
            rows = conn.execute(
                "SELECT title, content, category, tags, created_at, dna_signature FROM memories ORDER BY created_at DESC LIMIT 200"
            ).fetchall()
            conn.close()
        except Exception as e:
            print(f"   ⚠️ 读取 {db_path} 失败: {e}")
            continue

        for title, content, category, tags, created_at, dna in rows:
            if not content:
                continue
            text = f"[{category}] {title}\n{clean_text(content)}\n标签：{tags}\n时间：{created_at}\nDNA：{dna}"
            samples.append(make_sample(
                f"关于「{title}」的星辰记忆",
                truncate(text, 1200),
                "star_memory",
            ))
            samples.append(make_sample(
                f"{category} 里记录了什么？",
                truncate(text, 1000),
                "star_memory",
            ))

    return samples


# ---------- 4. 长期记忆摘要 ----------
def ingest_longhun_digest():
    samples = []
    digest_path = HOME / ".longhun" / "memory" / "latest_digest.md"
    if not digest_path.exists():
        return samples

    text = clean_text(digest_path.read_text(encoding="utf-8"))
    print(f"🧠 读取长期记忆摘要: {len(text)} 字符")

    # 分段生成 QA
    sections = re.split(r"\n## ", text)
    for sec in sections[1:]:
        lines = sec.splitlines()
        heading = lines[0].strip("# ")
        body = "\n".join(lines[1:]).strip()
        if len(body) < 30:
            continue
        samples.append(make_sample(
            f"关于 {heading} 的记忆",
            truncate(body, 1200),
            "longhun_memory",
        ))

    # 整体总结
    samples.append(make_sample(
        "最近龍魂系统发生了什么？",
        truncate(text, 1500),
        "longhun_memory",
    ))

    return samples


# ---------- 5. 日志摘要（只取关键行，避免噪音） ----------
def ingest_logs():
    samples = []
    log_files = []
    roots = [
        HOME / ".uid9622" / "daemon.log",
        HOME / "dragon_soul" / "audit" / "harvester_audit.jsonl",
        HOME / "chain_hash.jsonl",
        HOME / ".kimi-code" / "logs" / "kimi-code.log",
        HOME / ".龍魂" / "assessments" / "logs",
        HOME / "UID9622_Automation" / "logs",
    ]
    for r in roots:
        if r.is_file():
            log_files.append(r)
        elif r.is_dir():
            log_files.extend(sorted(r.glob("*"))[:20])

    print(f"📜 扫描 {len(log_files)} 个日志文件")

    all_events = []
    for p in log_files:
        try:
            if p.suffix == ".jsonl":
                with open(p, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                            # 提取关键字段
                            ev = " ".join(str(v) for k, v in obj.items() if k in ("action", "detail", "dna", "command", "reason", "level", "timestamp"))
                            if ev:
                                all_events.append(ev[:300])
                        except Exception:
                            pass
            else:
                text = clean_text(p.read_text(encoding="utf-8", errors="ignore"))
                lines = [l for l in text.splitlines() if l.strip() and len(l.strip()) > 10]
                all_events.extend(lines[:100])
        except Exception as e:
            print(f"   ⚠️ {p}: {e}")

    # 去重、取最近 500 条
    seen = set()
    uniq = []
    for ev in reversed(all_events):
        if ev not in seen and len(ev) > 15:
            seen.add(ev)
            uniq.append(ev)
    uniq = uniq[:500]

    if uniq:
        summary = "\n".join(f"- {e}" for e in uniq[:50])
        samples.append(make_sample(
            "最近系统有哪些关键操作日志？",
            truncate(summary, 1200),
            "system_logs",
        ))

    return samples


# ---------- 6. Notion / longhun 知识页面（核心文档） ----------
def ingest_knowledge_pages():
    samples = []
    roots = [
        HOME / ".longhun" / "notion_pages" / "targeted_pull",
        PROJECT / "L1_内核层" / "kernel" / "algorithms",
        PROJECT / "03_知識圖譜",
        PROJECT / "research",
    ]
    files = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            files.append(p)

    print(f"📖 发现 {len(files)} 个知识页面")

    for p in files[:500]:  # 限制数量，避免爆炸
        try:
            text = clean_text(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if len(text) < 200:
            continue

        title = p.stem.replace("_", " ").replace("-", " ")
        # 尝试取第一个标题
        for line in text.splitlines()[:10]:
            m = re.match(r"#+\s*(.+)", line)
            if m:
                title = m.group(1).strip()
                break

        domain = "knowledge_" + re.sub(r"\W+", "_", title)[:40]
        samples.append(make_sample(
            f"{title} 讲了什么？",
            truncate(text, 1200),
            domain,
        ))

    return samples


# ---------- 7. 英文记忆 / 文档 ----------
def ingest_english_memories():
    samples = []
    en_files = []
    for root in [PROJECT, HOME / ".longhun" / "notion_pages" / "targeted_pull"]:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and ("english" in p.name.lower() or "-en" in p.name.lower() or p.name.endswith("_en.md")):
                en_files.append(p)

    print(f"🌍 发现 {len(en_files)} 个英文记忆文档")

    for p in en_files[:50]:
        try:
            text = clean_text(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if len(text) < 200:
            continue

        title = p.stem
        samples.append(make_sample(
            f"What is '{title}' in LongHun system?",
            truncate(text, 1200),
            "english_memory",
        ))
        samples.append(make_sample(
            f"请用中文总结 {title}",
            truncate(text, 1000),
            "english_memory",
        ))

    return samples


# ---------- 主流程 ----------
def main():
    print("🐉 龍魂全记忆 ingestion 开始")
    print(f"输出目录: {OUTPUT}")

    all_samples = []
    sources = [
        ("skills", ingest_skills),
        ("personas", ingest_personas),
        ("star_memory", ingest_star_memory),
        ("longhun_digest", ingest_longhun_digest),
        ("logs", ingest_logs),
        ("knowledge_pages", ingest_knowledge_pages),
        ("english_memories", ingest_english_memories),
    ]

    for name, fn in sources:
        print(f"\n▶ 归集 {name}...")
        try:
            samples = fn()
            print(f"   ✅ {name}: {len(samples)} 条")
            all_samples.extend(samples)
        except Exception as e:
            print(f"   🔴 {name} 失败: {e}")

    # 去重（按 assistant 内容 hash）
    print("\n🧹 去重...")
    seen = set()
    uniq = []
    for s in all_samples:
        key = hash_id(s["messages"][1]["content"] + s["messages"][2]["content"])
        if key not in seen:
            seen.add(key)
            uniq.append(s)

    print(f"   去重前: {len(all_samples)} | 去重后: {len(uniq)}")

    # 统计
    domains = Counter(s["metadata"]["domain"].split("_")[0] for s in uniq)
    print("\n📊 域分布:")
    for d, c in domains.most_common():
        print(f"   {d}: {c}")

    # 划分训练/验证
    random.seed(42)
    random.shuffle(uniq)
    split = int(len(uniq) * 0.9)
    train = uniq[:split]
    valid = uniq[split:]

    with open(OUTPUT / "train.jsonl", "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with open(OUTPUT / "valid.jsonl", "w", encoding="utf-8") as f:
        for s in valid:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    info = {
        "version": "memory_ingested_v1.0",
        "total_samples": len(uniq),
        "train_samples": len(train),
        "val_samples": len(valid),
        "domains": dict(domains),
        "sources": [n for n, _ in sources],
    }
    with open(OUTPUT / "dataset_info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完成:")
    print(f"   训练集: {OUTPUT / 'train.jsonl'} ({len(train)})")
    print(f"   验证集: {OUTPUT / 'valid.jsonl'} ({len(valid)})")
    print(f"   信息:   {OUTPUT / 'dataset_info.json'}")
    print(f"   DNA: #龍芯⚡️丙午·乙未·甲午·庚午·䷳艮为山-MEMORY-INGEST-ALL-v1.0")


if __name__ == "__main__":
    main()
