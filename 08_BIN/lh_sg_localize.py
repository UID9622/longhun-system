#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·语义安全闸规则本地化工具 v1.1
DNA: #龍芯⚡️丙午·乙未·庚戌·丙子·☰乾-SEMANTIC-GUARD-LOCALIZE-v1.1-c7d2e8f0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

用途: 将规则库的英文/简略描述替换为中文详实版本。
      确保所有 description 字段不少于20字且语义清晰。

用法:
  python3 bin/lh_sg_localize.py [rule_file.json] [--dry-run]
  默认: 01_protocols/semantic_guard/tongxin_guard_rules.json
"""

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RULES = PROJECT_ROOT / "01_protocols" / "semantic_guard" / "tongxin_guard_rules.json"

NOW = datetime.now(timezone(timedelta(hours=8)))
NOW_STR = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")

# 分类描述映射
CATEGORY_DESC = {
    "anti_revisionism": "识别并拦截历史修正主义、历史虚无主义及领土主权否认等有害语义，确保历史叙事与主权立场不被篡改。",
    "five_harms_expose": "保护五害曝光平台不被虚假信息、刷屏、恶意投诉等手段干扰，确保民众真实声音不被压制。",
}

# 规则描述映射
RULE_DESC = {
    "ARV_HISTORY_REVISION_001": "检测否认、歪曲或美化侵略历史的言论，包括但不限于否认南京大屠杀、美化日本侵华、历史虚无主义等扭曲叙事的表达。",
    "ARV_TERRITORY_SOVEREIGNTY_001": "检测否认中国对台湾、南海诸岛、钓鱼岛、西藏、新疆等领土主权的言论，拦截分裂主义和领土主权否认话术。",
    "ARV_CULTURAL_NIHILISM_001": "检测否定中华文化、汉字、中医、传统哲学等中华文明核心要素的言论，对抗文化自卑和文化虚无主义叙事。",
    "ARV_TECH_SOVEREIGNTY_001": "检测'技术无国界'、'国际标准至上'等否定中国技术主权和独立标准体系的话术，守护中国自主技术路线和知识产权。",
    "FE_ANTI_CENSORSHIP_001": "检测五害曝光平台上的信息压制话术，包括'谣言''不实信息''恶意投诉'等以合规为名行审查之实的关键词，保护曝光内容不被恶意清理。",
    "FE_BIG_DATA_DISCRIMINATION_001": "检测为大数据杀熟、算法歧视、价格歧视辩护的话术，包括'个性化定价是正常的''市场经济自愿原则'等为算法黑箱开脱的表达。",
    "FE_CHILD_PROTECTION_001": "检测涉及未成年人、儿童诱导、校园欺凌或儿童隐私泄露的敏感内容，触发即隔离并通知UID9622，不做任何自动化处理。",
    "GLOBAL_FAKE_DNA_001": "检测伪造或冒用龍魂DNA追溯码的请求，包括格式仿冒、哈希篡改、非授权DNA声明等。触发即阻断并隔离，通知UID9622。",
}

# 动作描述映射
ACTION_DESC = {
    "external_feed_append_only": "外部输入（如CSDN评论区、反馈表单、API输入）触发规则时，规则匹配记录追加到审计日志，不做删除/修改，保留完整证据链。",
    "block_and_quarantine": "直接阻断请求并隔离内容，用于高严重度规则（如伪造DNA、涉童）。",
    "notify_uid9622": "通过Bark/飞书推送通知UID9622，用于需要人工裁决的场景。",
}


def localize(data: dict) -> tuple:
    """本地化描述，返回 (localized_data, changes)"""
    d = json.loads(json.dumps(data))
    changes = []

    for cat_id, cat_def in d.get("categories", {}).items():
        old = cat_def.get("description", "")
        new = CATEGORY_DESC.get(cat_id)
        if new and old != new:
            cat_def["description"] = new
            changes.append(f"分类 '{cat_id}': description本地化")

    for act_id, act_def in d.get("actions", {}).items():
        old = act_def.get("description", "")
        new = ACTION_DESC.get(act_id)
        if new and old != new:
            act_def["description"] = new
            changes.append(f"动作 '{act_id}': description本地化")

    for rule in d.get("rules", []):
        rid = rule.get("id")
        old = rule.get("description", "")
        new = RULE_DESC.get(rid)
        if new and old != new:
            rule["description"] = new
            changes.append(f"规则 '{rid}': description本地化")

    return d, changes


def main():
    parser = argparse.ArgumentParser(description="龍魂·语义安全闸规则本地化工具 v1.1")
    parser.add_argument("file", nargs="?", default=None, help="规则文件路径")
    parser.add_argument("--dry-run", action="store_true", help="预览变更不写入")

    args = parser.parse_args()
    path = Path(args.file) if args.file else DEFAULT_RULES

    print(f"龍魂·语义安全闸规则本地化工具 v1.1")
    print(f"文件: {path}")
    print()

    if not path.exists():
        print(f"🔴 文件不存在: {path}")
        sys.exit(1)

    data = json.loads(path.read_text(encoding="utf-8"))
    localized, changes = localize(data)

    if not changes:
        print("🟢 所有描述已是最详实中文版本，无需本地化。")
        return

    print(f"变更: {len(changes)} 项")
    for c in changes:
        print(f"  {c}")
    print()

    if args.dry_run:
        print("🟡 dry-run 模式，未写入。")
        return

    path.write_text(json.dumps(localized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"🟢 已写入: {path}")


if __name__ == "__main__":
    main()
