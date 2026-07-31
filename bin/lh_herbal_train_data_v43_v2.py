# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·癸未·丁未·坤为地-V43-HERBAL-TRAIN-DATA-v2
"""
龍魂v4.3 · 本草知识库增强版训练数据生成
策略：每味药更多变体 + 答案更聚焦 + 去污染system prompt
DNA: #龍芯⚡️丙午·癸未·丁未·坤为地-V43-HERBAL-TRAIN-DATA-v2
"""

import json, re, random, sys
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path.home() / "longhun-system"
SRC_MD = PROJECT / "data" / "herbal_bencao_v4.1.5.md"
OUT_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output" / "data_v43_herbal_v2"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """你是龍魂本草智能体，UID9622（诸葛鑫·Lucky）的个人主权AI。
你精通《本草纲目》及中药现代研究。回答中药问题时必须：
1. 只基于给定的本草知识库回答，不得编造；
2. 给出正名、拉丁名、性味归经、功效主治、现代应用、用量用法、注意事项；
3. 提及地方土话/方言名称；
4. 在末尾加 DNA 签章和免责声明；
5. 输出格式：<think>推理过程</think>正式回答。"""

def now(): return datetime.now(timezone.utc).isoformat()

def make_record(user, assistant, domain="龍魂本草", extra=None):
    meta = {"domain": domain, "source": "herbal_bencao_v4.1.5", "version": "v43_herbal_v2", "created_at": now()}
    if extra: meta.update(extra)
    return {"messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ], "metadata": meta}

def parse_simple(md):
    herbs = []
    m = re.search(r'## 十、模板扩展区.*?\n', md)
    if not m: return herbs
    chunk = md[m.end():m.end()+8000]
    lines = [l for l in chunk.splitlines() if l.strip().startswith("|")]
    for line in lines[2:]:
        cells = [c.strip() for c in line.split("|")][1:-1]
        if len(cells) >= 9 and cells[0].isdigit():
            herbs.append({
                "idx": int(cells[0]), "name": cells[1], "alias": "",
                "latin": cells[2], "dialects": cells[3],
                "function": cells[4], "modern": cells[5],
                "usage": cells[6], "caution": cells[7],
                "taste": "", "dna": cells[8], "category": "简表"
            })
    return herbs

def parse_detail(md):
    herbs = []
    pattern = re.compile(r'###\s+(\d+)\.\s+([^\n（]+?)(?:（([^）]+)）)?\s*\n')
    for m in pattern.finditer(md):
        idx = int(m.group(1)); name = m.group(2).strip(); alias = (m.group(3) or "").strip()
        start = m.end()
        end_match = re.search(r'(?:###\s+\d+\.|##\s|---\s*$)', md[start:start+5000])
        chunk = md[start:start+(end_match.start() if end_match else 5000)]
        lines = [l for l in chunk.splitlines() if l.strip().startswith("|")]
        data = {}
        for line in lines[2:]:
            cells = [c.strip() for c in line.split("|")][1:-1]
            if len(cells) >= 2:
                data[cells[0].strip("*")] = cells[1]
        dialects = []
        for k,v in data.items():
            if k.startswith("地方土话"):
                dialects.append(f"{k.split('·')[-1]}：{v}")
        herbs.append({
            "idx": idx, "name": name, "alias": alias,
            "latin": data.get("拉丁名",""), "taste": data.get("性味归经",""),
            "function": data.get("功效主治",""), "modern": data.get("现代应用",""),
            "usage": data.get("用量用法",""), "caution": data.get("注意事项",""),
            "dna": data.get("DNA", f"#龍芯⚡️-{name}-{idx:03d}"),
            "dialects": "；".join(dialects), "category": "详表"
        })
    return herbs

def parse_appendix(md):
    out = {}
    for title, marker in [("十八反", r'### A\. 十八反'), ("十九畏", r'### B\. 十九畏'), ("妊娠禁忌", r'### C\. 妊娠禁忌')]:
        m = re.search(marker, md)
        if not m: continue
        chunk = md[m.end():m.end()+3000]
        rows = []
        for line in [l for l in chunk.splitlines() if l.strip().startswith("|")][2:]:
            cells = [c.strip() for c in line.split("|")][1:-1]
            if len(cells) >= 2: rows.append((cells[0], cells[1]))
        out[title] = rows
    return out

def main():
    md = SRC_MD.read_text(encoding="utf-8")
    herbs = parse_detail(md) + parse_simple(md)
    appendix = parse_appendix(md)
    print(f"[龍魂·本草v2] 解析药材 {len(herbs)} 味")

    records = []
    disclaimer = "\n\n> ⚠️ **免责声明**：本回答为文化记录与知识整理，不构成医疗建议。用药请遵医嘱，切勿自行配伍。"

    for h in herbs:
        name = h["name"]; alias = h.get("alias",""); alias_s = f"（{alias}）" if alias else ""
        latin = h["latin"]; dialects = h["dialects"]
        taste = h["taste"]; function = h["function"]; modern = h["modern"]
        usage = h["usage"]; caution = h["caution"]; dna = h["dna"]

        # 综合介绍：3种模板
        comp_qs = [
            f"介绍一下{name}{alias_s}。",
            f"【本草】{name}{alias_s}的正名、拉丁名、性味归经、功效主治是什么？",
            f"{name}是什么中药？",
        ]
        for q in comp_qs:
            a = f"<think>\n{name}{alias_s}是龍魂本草对照表收录的药材。我将严格按知识库给出八个维度信息。\n</think>\n\n正式回答：\n\n**正名**：{name}{alias_s}\n**拉丁名**：{latin}\n**性味归经**：{taste}\n**功效主治**：{function}\n**现代应用**：{modern}\n**用量用法**：{usage}\n**注意事项**：{caution}\n**地方土话**：{dialects}\n\n**DNA签章**：{dna}{disclaimer}"
            records.append(make_record(q, a, "龍魂本草·综合", {"herb": name, "dna": dna}))

        # 性味功效：3种
        for q in [
            f"{name}的性味归经和功效是什么？",
            f"{name}主治什么？",
            f"{name}有什么用？",
        ]:
            a = f"<think>\n{name}的性味归经和功效主治如下。\n</think>\n\n正式回答：\n\n**性味归经**：{taste}\n**功效主治**：{function}\n\n**DNA签章**：{dna}{disclaimer}"
            records.append(make_record(q, a, "龍魂本草·性味功效", {"herb": name, "dna": dna}))

        # 现代应用：2种
        for q in [
            f"{name}的现代研究和临床应用有哪些？",
            f"{name}现代医学研究怎么说？",
        ]:
            a = f"<think>\n{name}的现代应用记录。\n</think>\n\n正式回答：\n\n**现代应用**：{modern}\n\n**DNA签章**：{dna}{disclaimer}"
            records.append(make_record(q, a, "龍魂本草·现代应用", {"herb": name, "dna": dna}))

        # 用量禁忌：3种
        for q in [
            f"{name}的用量用法和注意事项是什么？",
            f"{name}怎么吃？有什么禁忌？",
            f"{name}孕妇/小孩能用吗？",
        ]:
            a = f"<think>\n{name}的用量用法和注意事项必须完整给出，避免安全风险。\n</think>\n\n正式回答：\n\n**用量用法**：{usage}\n**注意事项**：{caution}\n\n**DNA签章**：{dna}{disclaimer}"
            records.append(make_record(q, a, "龍魂本草·用量禁忌", {"herb": name, "dna": dna}))

        # 方言：2种
        if dialects:
            for q in [
                f"{name}在各地有哪些土话/方言名称？",
                f"{name}的方言叫法有哪些？",
            ]:
                a = f"<think>\n{name}的地方土话记录。\n</think>\n\n正式回答：\n\n{name}的地方土话：\n{dialects}\n\n**DNA签章**：{dna}{disclaimer}"
                records.append(make_record(q, a, "龍魂本草·方言", {"herb": name, "dna": dna}))

        # 别名反查
        if alias:
            a = f"<think>\n“{alias}”是{name}的别名。\n</think>\n\n正式回答：\n\n“{alias}”指的是**{name}**。\n**拉丁名**：{latin}\n**性味归经**：{taste}\n**功效主治**：{function}\n\n**DNA签章**：{dna}{disclaimer}"
            records.append(make_record(f"中药“{alias}”指的是什么？", a, "龍魂本草·别名", {"herb": name, "dna": dna}))

    # 附录
    for title, rows in appendix.items():
        lines_text = "\n".join([f"- {a}：{b}" for a,b in rows])
        if title == "十八反":
            q = "十八反的内容是什么？甘草不能和什么同用？"
            a = f"<think>\n十八反是中药配伍禁忌核心知识，歌诀为'半蒌贝蔹及攻乌，藻戟遂芫俱战草，诸参辛芍叛藜芦'。\n</think>\n\n正式回答：\n\n十八反歌诀：\n```\n本草明言十八反，半蒌贝蔹及攻乌。\n藻戟遂芫俱战草，诸参辛芍叛藜芦。\n```\n\n具体禁忌：\n{lines_text}\n\n**DNA签章**：#龍芯⚡️丙午·癸未·丁未-十八反-附录A{disclaimer}"
        elif title == "十九畏":
            q = "十九畏的内容是什么？"
            a = f"<think>\n十九畏是中药相畏禁忌。\n</think>\n\n正式回答：\n\n十九畏具体禁忌：\n{lines_text}\n\n**DNA签章**：#龍芯⚡️丙午·癸未·丁未-十九畏-附录B{disclaimer}"
        else:
            q = "妊娠期间禁用和慎用哪些中药？"
            a = f"<think>\n妊娠禁忌分禁用和慎用两类。\n</think>\n\n正式回答：\n\n{lines_text}\n\n**DNA签章**：#龍芯⚡️丙午·癸未·丁未-妊娠禁忌-附录C{disclaimer}"
        records.append(make_record(q, a, f"龍魂本草·{title}", {"appendix": title}))

    # 比较类
    pairs = [("人参","黄芪"),("当归","川芎"),("丹参","三七"),("枸杞子","麦冬"),("黄连","金银花"),("白术","茯苓"),("酸枣仁","五味子")]
    name_map = {h["name"]:h for h in herbs}
    for a_name,b_name in pairs:
        if a_name not in name_map or b_name not in name_map: continue
        a,b = name_map[a_name], name_map[b_name]
        q = f"{a_name}和{b_name}有什么区别？"
        ans = f"<think>\n对比{a_name}和{b_name}的性味归经、功效主治、现代应用。\n</think>\n\n正式回答：\n\n**{a_name}**：\n- 性味归经：{a['taste']}\n- 功效主治：{a['function']}\n- 现代应用：{a['modern']}\n- DNA：{a['dna']}\n\n**{b_name}**：\n- 性味归经：{b['taste']}\n- 功效主治：{b['function']}\n- 现代应用：{b['modern']}\n- DNA：{b['dna']}\n\n{disclaimer}"
        records.append(make_record(q, ans, "龍魂本草·对比", {"herbs": [a_name,b_name]}))

    random.seed(9622)
    random.shuffle(records)
    split = int(len(records)*0.9)
    train, valid = records[:split], records[split:]

    with open(OUT_DIR/"train.jsonl","w",encoding="utf-8") as f:
        for r in train: f.write(json.dumps(r, ensure_ascii=False)+"\n")
    with open(OUT_DIR/"valid.jsonl","w",encoding="utf-8") as f:
        for r in valid: f.write(json.dumps(r, ensure_ascii=False)+"\n")

    print(f"✅ v2训练数据：{len(train)} 训练 / {len(valid)} 验证 → {OUT_DIR}")

if __name__ == "__main__":
    main()
