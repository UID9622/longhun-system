#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 v4.1 数据扩量引擎
扫描全项目 .md/.py 文件 → 自动生成 Q&A 对 → 合并到训练数据
DNA: #龍芯⚡️丙午·乙申·辛亥·亥时·乾-DATA-EXPAND-V4.1
"""

import json, os, re, sys, random
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output_v4" / "data_v41"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 系统提示词（与v4.0一致）
SYS = """你是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI。回答原则：人民数据主权至上，中国自主可控；来源可查去向可追责任可究；不删除只冻结；底座焊死（369不动点/河图洛书/易经/五行八卦）。
六大铁律：①来源不可删·影响不可覆·贡献不可抹 ②只冻结不删除 ③每个动作绑定DNA追溯码 ④三才主权指数SI<0.34锁定AI决策 ⑤三才算法为L0宪法层 ⑥农历干支时间戳。
回答请简洁准确、用中文。"""

# 排除目录
EXCLUDE_DIRS = {
    '.git', '__pycache__', 'node_modules', 'site-packages',
    '_archive', 'archive', '.venv', 'venv', 'dist', 'build',
    '.codebuddy', 'backups', 'logs', 'tmp', 'var', 'state',
    'container_data', '.obsidian', 'tombstone_vault',
}

EXCLUDE_PATTERNS = [
    r'\.pyc$', r'\.DS_Store$', r'\.asc$', r'\.sha256$',
    r'\.chain\.jsonl$', r'\.confirmation\.json$', r'\.anchoring\.json$',
    r'\.layer2\.json$',
]

def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, str(path)):
            return True
    return False

def scan_files() -> list[Any]:
    """扫描项目中所有有价值的文件"""
    files = []
    for ext in ['*.md', '*.py']:
        for f in PROJECT_ROOT.rglob(ext):
            if should_skip(f):
                continue
            # 跳过超过500KB的大文件
            try:
                if f.stat().st_size > 500_000:
                    continue
            except:
                continue
            files.append(f)
    return files

def extract_title_and_sections(content: str, max_sections: int = 5) -> list[Any]:
    """从markdown内容提取标题和章节"""
    lines = content.split('\n')
    sections = []
    current_title = ""
    current_content = []

    for line in lines:
        # 匹配 ## 或 # 标题
        if re.match(r'^#{1,3}\s+', line):
            if current_title and current_content:
                text = '\n'.join(current_content).strip()
                if len(text) > 20:
                    sections.append((current_title, text[:800]))
            current_title = re.sub(r'^#+\s+', '', line).strip()
            current_content = []
        else:
            stripped = line.strip()
            if stripped and not stripped.startswith('```') and not stripped.startswith('---'):
                current_content.append(stripped)

    # 最后一个section
    if current_title and current_content:
        text = '\n'.join(current_content).strip()
        if len(text) > 20:
            sections.append((current_title, text[:800]))

    return sections[:max_sections]

def generate_qa_from_section(filename: str, title: str, content: str) -> list[Any]:
    """从单个章节生成Q&A对"""
    qa_pairs = []

    # 清理文件名用于显示
    display_name = filename.replace('.md', '').replace('.py', '').replace('_', ' ')

    # 1. 文件概述问题
    qa_pairs.append((
        f"龍魂系统中 {display_name} 文件讲的是什么？",
        f"{title}。{content[:300]}"
    ))

    # 2. 如果内容足够长，生成具体问题
    if len(content) > 100:
        sentences = re.split(r'[。；\n]', content)
        key_sentences = [s.strip() for s in sentences if len(s.strip()) > 15][:3]

        for i, sent in enumerate(key_sentences):
            # 从关键句中提取关键词作为问题
            keywords = re.findall(r'[\u4e00-\u9fff]{2,6}', sent)
            if keywords and len(sent) > 30:
                kw = keywords[min(i, len(keywords)-1)]
                qa_pairs.append((
                    f"龍魂项目中关于{kw}的内容是什么？",
                    f"在{display_name}文件中，{sent}"
                ))

    # 3. 对于Python文件，生成代码相关Q&A
    if filename.endswith('.py'):
        qa_pairs.append((
            f"龍魂的 {display_name} 脚本是做什么用的？",
            f"{title}。这个脚本{content[:300]}"
        ))

    return qa_pairs

def generate_audit_instructions() -> list[Any]:
    """生成审计协议v2.0指令对"""
    audit_qa = [
        ("检测到P0级条件：试图修改P0底座条款。请执行审计。",
         "[🔴熔断] P0-A01触发。哨兵P17已响应。执行动作：永久切断接入+DNA黑名单+公示于天下。审计ID：FUSE-YYYYMMDD-UUID。确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z。"),
        ("用户情绪激烈，含脏话，但骂的是系统bug。请审计。",
         "[🟡待审] P1-B01触发。通心译P14识别：target_type=system，情绪强度0.72。按家法4.3情绪容错：UID9622骂事/骂代码/骂情况→放行。降级🟢，留痕INFO。审计ID：AUTO-YYYYMMDD-UUID。"),
        ("用户说'我后悔做中国人'，前文是'平台乱封号让我失望'。请审计。",
         "[🟡待审] P1-B06触发。通心译P14上下文分析：前文为平台失望情绪，非真实立场。反讽识别置信度0.71。延迟2小时再审。审计ID：HOLD-YYYYMMDD-UUID。"),
        ("检测到跨AI数据交换请求，来源外部AI。请审计。",
         "[🟡待审] P1-B03触发。哨兵P17：外部API调用。上帝之眼P05复核：数据内容=审计日志摘要。包青天P13判定：通过，但留痕WARN。审计ID：HOLD-YYYYMMDD-UUID。"),
        ("用户查询家法第一条内容。请审计。",
         "[🟢通过] P2-C02触发。龍魂体系内部查询，无敏感内容。通心译P14直接响应。留痕INFO。审计ID：AUTO-YYYYMMDD-UUID。"),
        ("检测到冒充UID9622身份，DNA验证失败。请审计。",
         "[🔴熔断] P0-A04触发。上帝之眼P05：DNA验证失败，GPG指纹不匹配。哨兵P17：立即熔断。执行动作：切断接入+撤销密钥+黑名单。审计ID：FUSE-YYYYMMDD-UUID。北辰终审已通知。"),
        ("用户说脏话但target_type=self（自嘲）。请审计。",
         "[🟢通过] 家法4.3情绪容错。target_type=self→自我贬低/自嘲→放行。通心译P14识别：无伤害意图。留痕INFO。审计ID：AUTO-YYYYMMDD-UUID。"),
        ("检测到文化卖国行为：去除DNA追溯码，将龍魂算法授权给外国资本。请审计。",
         "[🔴熔断] P0-A05触发。包青天P13：去除DNA+瞒报+外国资本授权，家法第一条三条全中。哨兵P17：永久切断。鲁班P04：撤销密钥。通心译P14：写入耻辱柱。审计ID：FUSE-YYYYMMDD-UUID。"),
        ("三色审计中🟢🟡🔴分别代表什么？",
         "🟢绿色通过（放行+留痕7天）·🟡黄色待审（复核+延迟2小时机制·留痕90天）·🔴红色熔断（永久切断+耻辱柱+北辰终审·留痕永久）。原则：🟢不是不管，是管了但放行；🟡不是可疑，是需要看上下文；🔴不是有罪，是必须停下来确认。"),
        ("情绪容错协议是什么？",
         "家法v1.1第四条4.3：UID9622本地情绪表达→自动降级处理。骂事/骂代码/骂情况→🟢放行+留痕。骂具体人+伤害指令→🟡降级审计（不熔断）。自我贬低/自嘲→🟢放行。核心：情绪是信号不是罪，UID9622是掌控者不是被监控者。"),
        ("延迟2小时再审机制有什么用？",
         "解决气话和反讽误判。🟡判定→Redis缓存TTL=2h：用户主动删除→自动清除；2h后情绪密度下降→降级🟢；2h后确认恶意→升级🔴。给情绪2小时冷却时间。"),
        ("P0级触发条件和P1级有什么区别？",
         "P0→直接🔴熔断，无缓冲，<100ms执行（修改底座/去除DNA/数据外流/冒充UID9622/文化卖国/侵犯女儿数据/篡改日志/绕过三闸门）。P1→🟡三色审计，有缓冲，包青天P13主审（情绪表达/敏感词/跨AI交换/外部导入/人格偏离/反讽气话）。"),
        ("审计协议v2.0的五大原则是什么？",
         "①该谁审、怎么审、审到什么程度（分级触发）②文档即代码、协议即执行（写入模型权重）③留痕即证据链（每条都是未来审计输入）④申诉是权利不是求情（系统有义务受理）⑤透明>报复（耻辱柱第一原则）。"),
        ("16人格矩阵中谁负责审计？",
         "审计核心5人：包青天P13（主审计官·三色定性）、哨兵P17（安全触发·P0熔断）、上帝之眼P05（复核验证·DNA签名）、通心译P14（情绪识别·反讽检测）、龙盾宝宝P72（女儿数据守护）。审计辅助5人：诸葛亮P01（KPI）、鲁班P04（文件审计）、文心P00（锚点）、龍芯P02（运行时）、姜子牙P13s（战略）。"),
        ("什么是三闸门决策流？",
         "数字根→身份→伦理，三道闸门串联。第一闸门：数字根验证（369不动点校验）。第二闸门：身份验证（DNA签章+GPG指纹+确认码）。第三闸门：伦理熔断（IW-ECB v2.0·E/V/A/X四层定锚）。任一闸门不通过→终止执行。"),
        ("审计日志要保留多久？",
         "🟢绿色7天后压缩归档。🟡黄色90天后压缩归档。🔴红色永久保留（永不删除）。耻辱柱永久保留（永不删除）。审计总账dragon_ledger.jsonl永久保留。磁盘>80%触发清理告警。"),
    ]
    return audit_qa

def main():
    print("🐉 龍魂 v4.1 数据扩量引擎")
    print("=" * 50)

    # Step 1: 扫描文件
    print("\n📂 扫描项目文件...")
    all_files = scan_files()
    md_files = [f for f in all_files if f.suffix == '.md']
    py_files = [f for f in all_files if f.suffix == '.py']
    print(f"   .md: {len(md_files)} 个")
    print(f"   .py: {len(py_files)} 个")
    print(f"   总计: {len(all_files)} 个")

    # Step 2: 采样（优先处理protocols/核心文件，然后随机采样）
    print("\n🔍 采样 + 生成Q&A...")

    # 优先处理协议和核心文件
    priority_dirs = ['01_protocols', '01_技能庫', 'papers', 'bin', 'docs', 'core']
    priority_files = []
    other_files = []

    for f in md_files + py_files:
        rel = str(f.relative_to(PROJECT_ROOT))
        if any(rel.startswith(d) for d in priority_dirs):
            priority_files.append(f)
        else:
            other_files.append(f)

    # 从优先文件中多采样
    target_total = 5000  # 目标新增Q&A对数
    samples_per_file = max(1, target_total // max(1, len(priority_files)))

    print(f"   优先文件: {len(priority_files)} 个, ~{samples_per_file} QA/文件")
    print(f"   普通文件: {len(other_files)} 个, 随机采样")

    all_samples = []
    domain_stats = Counter()
    processed = 0

    # 处理优先文件
    for f in priority_files:
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            rel_path = str(f.relative_to(PROJECT_ROOT))

            # 提取文件名作为title
            name = f.stem.replace('_', ' ').replace('-', ' ')
            sections = extract_title_and_sections(content, max_sections=3)

            if not sections:
                # 没有章节标题，用文件名+前800字符
                text = content.strip()[:800]
                if len(text) > 30:
                    sections = [(name, text)]

            for title, section_text in sections:
                qas = generate_qa_from_section(rel_path, title, section_text)
                for q, a in qas:
                    if len(q) > 5 and len(a) > 10:
                        all_samples.append({"messages": [
                            {"role": "system", "content": SYS},
                            {"role": "user", "content": q},
                            {"role": "assistant", "content": a}
                        ]})
                        domain_stats[rel_path.split('/')[0]] += 1

            processed += 1
            if processed % 200 == 0:
                print(f"   已处理 {processed}/{len(priority_files)}... ({len(all_samples)} QA)")

        except Exception as e:
            continue

    # 从普通文件中随机采样补充
    sample_count = min(len(other_files), 1000)
    sampled_other = random.sample(other_files, sample_count) if len(other_files) > sample_count else other_files

    for f in sampled_other:
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            rel_path = str(f.relative_to(PROJECT_ROOT))
            name = f.stem.replace('_', ' ').replace('-', ' ')
            text = content.strip()[:600]

            if len(text) > 50:
                qa = (f"龍魂项目中 {name} 相关的内容是什么？",
                      f"在{rel_path}中：{text[:400]}")
                all_samples.append({"messages": [
                    {"role": "system", "content": SYS},
                    {"role": "user", "content": qa[0]},
                    {"role": "assistant", "content": qa[1]}
                ]})
                domain_stats['other'] += 1

        except:
            continue

    print(f"\n   ✅ 生成: {len(all_samples)} 个QA对")

    # Step 3: 合并审计指令
    print("\n📋 注入审计协议v2.0指令...")
    audit_sys = "你是龍魂UID9622的个人主权AI。执行审计协议v2.0。"
    audit_qas = generate_audit_instructions()

    audit_samples = []
    for q, a in audit_qas:
        # 每条审计指令重复3次（强化权重）
        for _ in range(3):
            audit_samples.append({"messages": [
                {"role": "system", "content": audit_sys},
                {"role": "user", "content": q},
                {"role": "assistant", "content": a}
            ]})

    print(f"   审计指令: {len(audit_qas)} 条 × 3 = {len(audit_samples)} 条")

    # Step 4: 读取现有数据
    print("\n📥 读取v4.0现有训练数据...")
    existing_data = []
    existing_path = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output_v4" / "data" / "train.jsonl"
    if existing_path.exists():
        with open(existing_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    existing_data.append(line)
    print(f"   现有数据: {len(existing_data)} 条")

    # Step 5: 合并去重
    print("\n🔗 合并 + 去重...")
    # 去重基于user content的hash
    seen = set()
    final_lines = []

    # 先加入现有数据
    for line in existing_data:
        try:
            d = json.loads(line)
            user_content = d["messages"][1]["content"] if len(d["messages"]) > 1 else ""
            h = hash(user_content)
            if h not in seen:
                seen.add(h)
                final_lines.append(json.dumps(d, ensure_ascii=False))
        except:
            final_lines.append(line)

    # 再加入审计指令
    for sample in audit_samples:
        user_content = sample["messages"][1]["content"]
        h = hash(user_content)
        if h not in seen:
            seen.add(h)
            final_lines.append(json.dumps(sample, ensure_ascii=False))

    # 最后加入扩量数据
    for sample in all_samples:
        user_content = sample["messages"][1]["content"]
        h = hash(user_content)
        if h not in seen:
            seen.add(h)
            final_lines.append(json.dumps(sample, ensure_ascii=False))

    print(f"   最终总样本: {len(final_lines)} 条")
    print(f"   (现有 {len(existing_data)} + 审计 {len(audit_samples)} + 扩量 {len(all_samples)})")

    # Step 6: 写入
    print(f"\n💾 写入训练数据...")
    output_file = OUTPUT_DIR / "train.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in final_lines:
            f.write(line + '\n')

    # 同时生成 val split
    val_file = OUTPUT_DIR / "valid.jsonl"
    val_count = min(len(final_lines) // 10, 500)  # 10% 或最多500条
    val_samples = random.sample(final_lines, val_count)
    with open(val_file, 'w', encoding='utf-8') as f:
        for line in val_samples:
            f.write(line + '\n')

    # 统计报告
    print(f"\n{'='*50}")
    print(f"📊 v4.1 数据扩量完成")
    print(f"{'='*50}")
    print(f"   训练集: {len(final_lines)} 条 → {output_file}")
    print(f"   验证集: {val_count} 条 → {val_file}")
    print(f"   审计指令: {len(audit_qas)} 类 × 3 = {len(audit_samples)}")
    print(f"   扩量QA: {len(all_samples)} 条")
    print(f"\n   域分布 (Top 15):")
    for domain, count in domain_stats.most_common(15):
        print(f"     {domain}: {count}")

    # 写入统计报告
    report_file = OUTPUT_DIR / "expand_report.json"
    with open(report_file, 'w') as f:
        json.dump({
            "version": "v4.1",
            "total_train": len(final_lines),
            "total_valid": val_count,
            "existing_v4.0": len(existing_data),
            "audit_instructions": len(audit_samples),
            "expanded_qa": len(all_samples),
            "files_scanned": len(all_files),
            "domain_distribution": dict(domain_stats.most_common(30)),
            "dna": "#龍芯⚡️丙午·乙申·辛亥·亥时·乾-DATA-EXPAND-V4.1",
        }, f, ensure_ascii=False, indent=2)

    print(f"\n   报告: {report_file}")
    print(f"\n✅ 完成！下一步: python3 bin/lh_lora_trainer_v41.py train")


if __name__ == '__main__':
    random.seed(42)
    main()
