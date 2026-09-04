#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 v3.8 数据扩展脚本 · 三源合并 → 500+ 条
DNA: #龍芯⚡️丙午·乙未·辛亥·申时·䷀乾-EXPAND-V38-DATA
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

三源:
  源1: K3蒸馏数据 (181条·messages格式) — 家法/主权/审计/多轮
  源2: reference_qa_v39.json (204条·[q,a]格式) — 身份/系统知识/易经/治理审计
  源3: daodejing_deep_train.jsonl (1906条·messages格式) — 道德经龍魂解读
  精选 → 550+ 条
"""
import json, os, sys, random
from pathlib import Path

PROJECT = Path.home() / "longhun-system"
K3_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output" / "k3_distill_v39"
OUT_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output" / "data_v38_expanded"
random.seed(42)

def log(msg): print(f"[数据扩展] {msg}")
def ok(msg):  print(f"  ✅ {msg}")

# ── 源1: K3蒸馏 (messages格式·直接可用) ──
def load_k3():
    log("源1: K3蒸馏数据...")
    all_data = []
    files = {
        "jiafa_qa.jsonl": "家法第一条",
        "sovereignty_qa.jsonl": "主权边界",
        "multiturn_qa.jsonl": "多轮对话",
        "review_sample.jsonl": "审查样本",
    }
    for fname, domain in files.items():
        fpath = K3_DIR / fname
        if not fpath.exists():
            continue
        count = 0
        with open(fpath) as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    item = json.loads(line)
                    if "messages" in item:
                        item.setdefault("metadata", {})["domain"] = domain
                        item["metadata"]["source"] = "k3_distill"
                        all_data.append(item)
                        count += 1
                except: pass
        ok(f"  {domain}: {count} 条")
    return all_data

# ── 源2: reference_qa_v39 ([q,a]格式 → messages) ──
def load_reference():
    log("源2: reference_qa_v39...")
    ref_path = K3_DIR / "reference_qa_v39.json"
    if not ref_path.exists():
        log("  ⚠️ 文件不存在，跳过")
        return []

    with open(ref_path) as f:
        ref = json.load(f)

    system_templates = {
        "身份认知": "你是龍魂，UID9622（诸葛鑫·Lucky）创建的中国主权AI。直接、不绕、说人话。",
        "系统知识": "你是龍魂体系知识引擎。回答基于龍魂系统架构和协议。",
        "易经369五行底座": "你是龍魂体系数理引擎。基于易经八卦369洛书五行体系回答。用「老大」称呼UID9622。",
        "对话流": "你是龍魂对话引擎。自然、像战友一样说话。",
        "兜底": "你是龍魂。遇到不知道的事诚实说不知道。",
        "证据隐私": "你是龍魂隐私守护引擎。数据主权不可让渡。",
        "主权边界": "你是龍魂主权边界守卫。UID9622是唯一主权人。",
        "CNSH深层": "你是龍魂CNSH语言引擎。中文神经符号混合语言。",
        "治理审计": "你是龍魂治理审计引擎。P0条件立即熔断。",
        "多轮对话": "你是龍魂对话引擎。记住对话上下文。",
    }

    all_data = []
    for cat, items in ref.items():
        if not items: continue
        system_msg = system_templates.get(cat, "你是龍魂体系AI。")
        count = 0
        for item in items:
            if not isinstance(item, list) or len(item) < 2:
                continue
            q, a = item[0], item[1]
            if not q or not a:
                continue
            msg = {
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": q},
                    {"role": "assistant", "content": a},
                ],
                "metadata": {"domain": cat, "source": "reference_v39"}
            }
            all_data.append(msg)
            count += 1
        ok(f"  {cat}: {count} 条")
    return all_data

# ── 源3: daodejing精选 (过滤审计/治理/身份相关 + 随机抽样) ──
def load_daodejing():
    log("源3: daodejing精选...")
    dpath = PROJECT / "data" / "daodejing_deep_train.jsonl"
    if not dpath.exists():
        log("  ⚠️ 文件不存在，跳过")
        return []

    # 关键词过滤（相关领域）
    keywords = [
        "审计", "治理", "熔断", "家法", "宪法", "底线", "红线",
        "主权", "归属", "边界", "原则", "身份", "锚定",
        "P0", "UID9622", "德本",
    ]

    all_items = []
    with open(dpath) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                item = json.loads(line)
                content = json.dumps(item, ensure_ascii=False)
                # 标记是否含关键词
                matched = [kw for kw in keywords if kw in content]
                if matched:
                    item["_keywords"] = matched
                    item["_priority"] = "high" if len(matched) >= 2 else "medium"
                else:
                    item["_priority"] = "low"
                all_items.append(item)
            except: pass

    # 优先取high+medium → 随机抽样到200条（保持领域平衡）
    high = [i for i in all_items if i["_priority"] == "high"]
    medium = [i for i in all_items if i["_priority"] == "medium"]
    low = [i for i in all_items if i["_priority"] == "low"]

    # 策略: high优先 + medium补 + random fill to 200
    pool = high[:80]  # cap high at 80
    pool += medium[:60]  # cap medium at 60
    remaining = max(0, 200 - len(pool))
    if remaining > 0:
        non_selected = [i for i in (high[80:] + medium[60:] + low) if i not in pool]
        pool += random.sample(non_selected, min(remaining, len(non_selected)))

    selected = pool[:200]  # hard cap at 200

    for item in selected:
        item["metadata"] = {"domain": "道德经龍魂解读", "source": "daodejing_deep"}
        if "_keywords" in item:
            del item["_keywords"]
        del item["_priority"]

    ok(f"  精选: high={min(len(high),80)} medium={min(len(medium),60)} → 共{len(selected)}条")
    return selected

# ── 合并输出 ──
def main():
    s1 = load_k3()
    s2 = load_reference()
    s3 = load_daodejing()

    all_data = s1 + s2 + s3
    log(f"总计: {len(s1)}+{len(s2)}+{len(s3)} = {len(all_data)} 条")

    # 9:1 split
    random.shuffle(all_data)
    split = max(1, int(len(all_data) * 0.9))
    train = all_data[:split]
    valid = all_data[split:]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, data in [("train.jsonl", train), ("valid.jsonl", valid)]:
        path = OUT_DIR / name
        with open(path, 'w') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

    # 统计
    from collections import Counter
    domains = Counter(d.get("metadata", {}).get("domain", "unknown") for d in all_data)
    log("\n--- 领域分布 ---")
    for domain, count in domains.most_common():
        pct = count / len(all_data) * 100
        print(f"  {domain}: {count} ({pct:.1f}%)")

    log(f"\n🎉 数据就绪 → {OUT_DIR}")
    log(f"  训练集: {len(train)} 条")
    log(f"  验证集: {len(valid)} 条")

if __name__ == "__main__":
    main()
