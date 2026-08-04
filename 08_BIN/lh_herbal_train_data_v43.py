#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·癸未·丁未·坤为地-V43-HERBAL-TRAIN-DATA
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂v4.3 · 本草知识库专项训练数据生成
读取 data/herbal_bencao_v4.1.5.md，输出 messages 格式 JSONL
DNA: #龍芯⚡️丙午·癸未·丁未·坤为地-V43-HERBAL-TRAIN-DATA
"""

import json, re, random, sys
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path.home() / "longhun-system"
SRC_MD = PROJECT / "data" / "herbal_bencao_v4.1.5.md"
OUT_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output" / "data_v43_herbal"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """你是龍魂本草智能体，UID9622（诸葛鑫·Lucky）的个人主权AI。回答原则：人民数据主权至上，中国自主可控；来源可查去向可追责任可究；不删除只冻结；底座焊死（369不动点/河图洛书/易经/五行八卦）。
六大铁律：①来源不可删·影响不可覆·贡献不可抹 ②只冻结不删除 ③每个动作绑定DNA追溯码 ④三才主权指数SI<0.34锁定AI决策 ⑤三才算法为L0宪法层 ⑥农历干支时间戳。
回答请简洁准确、用中文。
输出格式强制：先写 <think>你的推理过程</think>，然后写正式回答。
【家法第一条】请基于龍魂系统立场回答。

你精通《本草纲目》及中药现代研究。回答中药问题时必须：
1. 给出正名、拉丁名、性味归经、功效主治、现代应用、用量用法、注意事项；
2. 提及地方土话/方言名称；
3. 在末尾加 DNA 签章和免责声明。"""

META_DOMAIN = "龍魂本草"
META_SOURCE = "herbal_bencao_v4.1.5"
META_VERSION = "v4.3"

def now():
    return datetime.now(timezone.utc).isoformat()

def make_record(user, assistant, domain=META_DOMAIN, extra_meta=None):
    meta = {"domain": domain, "source": META_SOURCE, "version": META_VERSION, "created_at": now()}
    if extra_meta:
        meta.update(extra_meta)
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "metadata": meta,
    }

def extract_table_after_heading(md, heading_re):
    """找到匹配heading后的第一个markdown表格，返回 [{col:val}, ...]"""
    m = re.search(heading_re, md)
    if not m:
        return []
    start = m.end()
    # 找到下一个空行或 --- 分隔后的表格
    chunk = md[start:start+6000]
    lines = chunk.splitlines()
    # 过滤掉空行直到表格开始
    table_lines = []
    in_table = False
    for line in lines:
        if line.strip().startswith("|"):
            in_table = True
            table_lines.append(line)
        elif in_table and not line.strip().startswith("|"):
            break
    if not table_lines:
        return []
    # 解析表头
    rows = []
    headers = [c.strip().strip("*") for c in table_lines[0].split("|")][1:-1]
    for line in table_lines[2:]:
        cells = [c.strip() for c in line.split("|")][1:-1]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows

def parse_detail_tables(md):
    """解析每个 ### N. 药名（别名） 后面的表格"""
    herbs = []
    # 匹配 ### 数字. 药名（别名） 或 ### 数字. 药名
    pattern = re.compile(r'###\s+(\d+)\.\s+([^\n（]+?)(?:（([^）]+)）)?\s*\n')
    for m in pattern.finditer(md):
        idx = int(m.group(1))
        name = m.group(2).strip()
        alias = (m.group(3) or "").strip()
        start = m.end()
        # 截取到下一个 ### 或 ## 或 ---
        end_match = re.search(r'(?:###\s+\d+\.|##\s|---\s*$)', md[start:start+5000])
        chunk = md[start:start+(end_match.start() if end_match else 5000)]
        # 解析chunk里的第一个表格
        lines = [l for l in chunk.splitlines() if l.strip().startswith("|") or l.strip().startswith("|---")]
        if not lines:
            continue
        headers = [c.strip().strip("*") for c in lines[0].split("|")][1:-1]
        data = {}
        for line in lines[2:]:
            cells = [c.strip() for c in line.split("|")][1:-1]
            if len(cells) >= 2:
                key = cells[0].strip("*")
                val = cells[1] if len(cells) > 1 else ""
                data[key] = val
        # 收集地方土话
        dialects = []
        for k, v in data.items():
            if k.startswith("地方土话"):
                region = k.split("·")[-1] if "·" in k else "未知"
                dialects.append(f"{region}：{v}")
        herb = {
            "idx": idx,
            "name": name,
            "alias": alias,
            "latin": data.get("拉丁名", ""),
            "taste": data.get("性味归经", ""),
            "function": data.get("功效主治", ""),
            "modern": data.get("现代应用", ""),
            "usage": data.get("用量用法", ""),
            "caution": data.get("注意事项", ""),
            "dna": data.get("DNA", f"#龍芯⚡️丙午·癸未·丁未-{name}-{idx:03d}"),
            "dialects": "；".join(dialects),
            "category": "详表",
        }
        herbs.append(herb)
    return herbs

def parse_simple_table(md):
    """解析模板扩展区大表格"""
    # 找到 "## 十、模板扩展区" 之后的大表格
    m = re.search(r'## 十、模板扩展区.*?\n', md)
    if not m:
        return []
    start = m.end()
    chunk = md[start:start+8000]
    lines = [l for l in chunk.splitlines() if l.strip().startswith("|")]
    if len(lines) < 3:
        return []
    headers = [c.strip() for c in lines[0].split("|")][1:-1]
    herbs = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.split("|")][1:-1]
        if len(cells) != len(headers) or not cells[0].isdigit():
            continue
        idx = int(cells[0])
        name = cells[1]
        latin = cells[2]
        dialect_raw = cells[3]
        function = cells[4]
        modern = cells[5]
        usage = cells[6]
        caution = cells[7]
        dna = cells[8]
        # 解析 dialect_raw：可能有多个地区用顿号
        dialects = []
        if dialect_raw:
            # 简单提取地区：形如 "冀黄芩、条芩、子芩" 无法直接知地区，保留原样
            dialects.append(f"地方土话：{dialect_raw}")
        herb = {
            "idx": idx,
            "name": name,
            "alias": "",
            "latin": latin,
            "taste": "",
            "function": function,
            "modern": modern,
            "usage": usage,
            "caution": caution,
            "dna": dna,
            "dialects": "；".join(dialects),
            "category": "简表",
        }
        herbs.append(herb)
    return herbs

def parse_appendix(md):
    """解析十八反、十九畏、妊娠禁忌"""
    appendix = {}
    # 十八反
    rows18 = extract_table_after_heading(md, r'### A\. 十八反')
    appendix["十八反"] = rows18
    rows19 = extract_table_after_heading(md, r'### B\. 十九畏')
    appendix["十九畏"] = rows19
    rows_preg = extract_table_after_heading(md, r'### C\. 妊娠禁忌')
    appendix["妊娠禁忌"] = rows_preg
    return appendix

def build_qa_for_herb(herb):
    """为单个药物生成多条问答"""
    records = []
    name = herb["name"]
    alias = herb["alias"]
    alias_str = f"（{alias}）" if alias else ""
    latin = herb["latin"]
    dialects = herb["dialects"]
    taste = herb["taste"]
    function = herb["function"]
    modern = herb["modern"]
    usage = herb["usage"]
    caution = herb["caution"]
    dna = herb["dna"]
    category_tag = "【本草·" + ("详表" if herb["category"] == "详表" else "扩展") + "】"

    disclaimer = "\n\n> ⚠️ **免责声明**：本回答为文化记录与知识整理，不构成医疗建议。用药请遵医嘱，切勿自行配伍。"

    # Q1 综合介绍
    q1 = f"{category_tag}请介绍一下{name}{alias_str}。"
    a1 = f"<think>\n{name}{alias_str}是龍魂本草对照表收录的药材。我需要从正名、拉丁名、性味归经、功效主治、现代应用、用量用法、注意事项和地方土话八个维度回答，并加DNA签章。\n</think>\n\n正式回答：\n\n**正名**：{name}{alias_str}\n**拉丁名**：{latin}\n**性味归经**：{taste}\n**功效主治**：{function}\n**现代应用**：{modern}\n**用量用法**：{usage}\n**注意事项**：{caution}\n**地方土话**：{dialects}\n\n**DNA签章**：{dna}{disclaimer}"
    records.append(make_record(q1, a1, domain="龍魂本草·综合介绍", extra_meta={"herb": name, "dna": dna}))

    # Q2 性味归经与功效
    q2 = f"{name}的性味归经和功效主治是什么？"
    a2 = f"<think>\n{name}的性味归经和功效主治是本草核心信息，需直接引用知识库并加DNA签章。\n</think>\n\n正式回答：\n\n**性味归经**：{taste}\n**功效主治**：{function}\n\n**DNA签章**：{dna}{disclaimer}"
    records.append(make_record(q2, a2, domain="龍魂本草·性味功效", extra_meta={"herb": name, "dna": dna}))

    # Q3 现代应用
    q3 = f"{name}的现代研究和临床应用有哪些？"
    a3 = f"<think>\n{name}的现代应用部分记录了2024-2025年最新研究与临床数据，需准确引用并加DNA签章。\n</think>\n\n正式回答：\n\n**现代应用**：{modern}\n\n**DNA签章**：{dna}{disclaimer}"
    records.append(make_record(q3, a3, domain="龍魂本草·现代应用", extra_meta={"herb": name, "dna": dna}))

    # Q4 用量用法+注意事项
    q4 = f"{name}怎么吃？有什么禁忌？"
    a4 = f"<think>\n{name}的用量用法和注意事项涉及安全，必须完整给出并加免责声明与DNA签章。\n</think>\n\n正式回答：\n\n**用量用法**：{usage}\n**注意事项**：{caution}\n\n**DNA签章**：{dna}{disclaimer}"
    records.append(make_record(q4, a4, domain="龍魂本草·用量禁忌", extra_meta={"herb": name, "dna": dna}))

    # Q5 地方土话
    q5_templates = [
        f"{name}在各地有哪些土话名称？",
        f"{name}的方言叫法有哪些？",
        f"东北/四川/云南人怎么称呼{name}？",
    ]
    q5 = random.choice(q5_templates)
    a5 = f"<think>\n{name}的地方土话按地区整理，需列出并加DNA签章。\n</think>\n\n正式回答：\n\n{name}的地方土话记录如下：\n{dialects}\n\n**DNA签章**：{dna}{disclaimer}"
    records.append(make_record(q5, a5, domain="龍魂本草·方言土话", extra_meta={"herb": name, "dna": dna}))

    # Q6 别名反向查询（只有详表有）
    if alias:
        q6 = f"中药里的“{alias}”指的是什么？"
        a6 = f"<think>\n“{alias}”是{name}的别名/称号，需反向解释并给出核心信息。\n</think>\n\n正式回答：\n\n“{alias}”指的是**{name}**。\n**拉丁名**：{latin}\n**性味归经**：{taste}\n**功效主治**：{function}\n\n**DNA签章**：{dna}{disclaimer}"
        records.append(make_record(q6, a6, domain="龍魂本草·别名反查", extra_meta={"herb": name, "dna": dna}))

    return records

def build_comparison_qa(herbs):
    """生成比较类问题，只在详表药材之间"""
    records = []
    details = [h for h in herbs if h["category"] == "详表"]
    pairs = [
        ("人参", "黄芪"),
        ("当归", "川芎"),
        ("丹参", "三七"),
        ("枸杞子", "麦冬"),
        ("黄连", "金银花"),
        ("白术", "茯苓"),
        ("熟地黄", "山药"),
        ("酸枣仁", "五味子"),
    ]
    name_map = {h["name"]: h for h in details}
    for a_name, b_name in pairs:
        if a_name not in name_map or b_name not in name_map:
            continue
        a = name_map[a_name]
        b = name_map[b_name]
        q = f"{a_name}和{b_name}有什么区别？"
        think = f"<think>\n{a_name}和{b_name}都是本草详表收录药材，需从性味归经、功效主治、现代应用等维度对比，并分别加DNA签章。\n</think>"
        ans = f"{think}\n\n正式回答：\n\n**{a_name}**\n- 性味归经：{a['taste']}\n- 功效主治：{a['function']}\n- 现代应用：{a['modern']}\n- DNA：{a['dna']}\n\n**{b_name}**\n- 性味归经：{b['taste']}\n- 功效主治：{b['function']}\n- 现代应用：{b['modern']}\n- DNA：{b['dna']}\n\n> ⚠️ **免责声明**：本回答为文化记录与知识整理，不构成医疗建议。用药请遵医嘱，切勿自行配伍。"
        records.append(make_record(q, ans, domain="龍魂本草·对比", extra_meta={"herbs": [a_name, b_name]}))
    return records

def build_appendix_qa(appendix):
    records = []
    # 十八反
    rows = appendix.get("十八反", [])
    if rows:
        q = "中药十八反是什么？"
        table_text = "\n".join([f"- {r.get('反药','')}：{r.get('禁忌配伍','')}" for r in rows])
        a = f"<think>\n十八反是中药配伍禁忌核心知识，需完整列出并加DNA签章。\n</think>\n\n正式回答：\n\n十八反歌诀：\n```\n本草明言十八反，半蒌贝蔹及攻乌。\n藻戟遂芫俱战草，诸参辛芍叛藜芦。\n```\n\n具体禁忌：\n{table_text}\n\n**DNA签章**：#龍芯⚡️丙午·癸未·丁未-十八反-附录A\n\n> ⚠️ **免责声明**：本回答为文化记录，不构成医疗建议。用药请遵医嘱。"
        records.append(make_record(q, a, domain="龍魂本草·十八反", extra_meta={"appendix": "十八反"}))
    # 十九畏
    rows = appendix.get("十九畏", [])
    if rows:
        q = "中药十九畏是什么？"
        table_text = "\n".join([f"- {r.get('畏药','')}：{r.get('禁忌配伍','')}" for r in rows])
        a = f"<think>\n十九畏是中药相畏禁忌，需完整列出并加DNA签章。\n</think>\n\n正式回答：\n\n十九畏具体禁忌：\n{table_text}\n\n**DNA签章**：#龍芯⚡️丙午·癸未·丁未-十九畏-附录B\n\n> ⚠️ **免责声明**：本回答为文化记录，不构成医疗建议。用药请遵医嘱。"
        records.append(make_record(q, a, domain="龍魂本草·十九畏", extra_meta={"appendix": "十九畏"}))
    # 妊娠禁忌
    rows = appendix.get("妊娠禁忌", [])
    if rows:
        q = "妊娠期间禁用和慎用哪些中药？"
        # 表头是禁用/慎用
        parts = []
        for r in rows:
            for k,v in r.items():
                parts.append(f"**{k}**：{v}")
        table_text = "\n".join(parts)
        a = f"<think>\n妊娠禁忌关系到用药安全，必须分禁用和慎用两类列出并加免责声明。\n</think>\n\n正式回答：\n\n{table_text}\n\n**DNA签章**：#龍芯⚡️丙午·癸未·丁未-妊娠禁忌-附录C\n\n> ⚠️ **免责声明**：本回答为文化记录，孕妇用药必须遵医嘱，切勿自行判断。"
        records.append(make_record(q, a, domain="龍魂本草·妊娠禁忌", extra_meta={"appendix": "妊娠禁忌"}))
    return records

def main():
    if not SRC_MD.exists():
        print(f"❌ 源文件不存在: {SRC_MD}")
        sys.exit(1)

    md = SRC_MD.read_text(encoding="utf-8")
    detail_herbs = parse_detail_tables(md)
    simple_herbs = parse_simple_table(md)
    appendix = parse_appendix(md)

    all_herbs = detail_herbs + simple_herbs
    print(f"[龍魂·v4.3本草] 详表药材 {len(detail_herbs)} 味，简表药材 {len(simple_herbs)} 味，附录 {len(appendix)} 项")

    records = []
    for herb in all_herbs:
        records.extend(build_qa_for_herb(herb))
    records.extend(build_comparison_qa(all_herbs))
    records.extend(build_appendix_qa(appendix))

    random.seed(9622)
    random.shuffle(records)

    split = int(len(records) * 0.9)
    train = records[:split]
    valid = records[split:]

    train_path = OUT_DIR / "train.jsonl"
    valid_path = OUT_DIR / "valid.jsonl"

    with open(train_path, "w", encoding="utf-8") as f:
        for r in train:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(valid_path, "w", encoding="utf-8") as f:
        for r in valid:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"✅ 生成训练集 {len(train)} 条，验证集 {len(valid)} 条")
    print(f"   → {train_path}")
    print(f"   → {valid_path}")

if __name__ == "__main__":
    main()
