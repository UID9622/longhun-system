#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 老百姓维权助手
DNA: #龍芯⚡️2026-06-29-LONGHUN-RIGHTS-ASSISTANT-v1.1

本地运行，不联网。输入遭遇，自动识别场景，输出：
- 投诉书
- 法条依据
- 怼人话术
- 证据清单
- 投诉渠道

新增：通心译大白话模式，老百姓说什么话，我们就用什么话回。
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent / "cnsh-core"))
from cnsh_unified import DNA工具

ROOT = Path(__file__).parent
TEMPLATES_PATH = ROOT / "templates.json"


def 加载模板() -> dict[str, Any]:
    return json.loads(TEMPLATES_PATH.read_text(encoding="utf-8"))


def 识别场景(用户输入: str, 模板: dict[str, Any]) -> Optional[str]:
    输入小写 = 用户输入.lower()
    得分: Dict[str, int] = {}
    for 场景名, 数据 in 模板["scenarios"].items():
        for 关键词 in 数据["keywords"]:
            if 关键词 in 输入小写:
                得分[场景名] = 得分.get(场景名, 0) + 1
    if not 得分:
        return None
    return max(得分, key=得分.get)


def 填充模板(模板文本: str, 参数: dict[str, Any]) -> str:
    for 键, 值 in 参数.items():
        模板文本 = 模板文本.replace("{" + 键 + "}", str(值))
    # 清理未填充的占位符
    模板文本 = re.sub(r"\{[^}]+\}", "（未填写）", 模板文本)
    return 模板文本


def 通心译转换(文本: str, 语气: str, 模板: dict[str, Any]) -> str:
    """把官话/法律术语转成老百姓能听懂的大白话，或指定语气。"""
    语气配置 = 模板.get("tones", {}).get(语气)
    if not 语气配置:
        return 文本
    for 原词, 替换词 in 语气配置.get("replacements", {}).items():
        文本 = 文本.replace(原词, 替换词)
    # 清理多余空格
    文本 = re.sub(r" +", " ", 文本)
    return 文本.strip()


def 生成报告(场景名: str, 数据: dict[str, Any], 参数: dict[str, Any], 语气: str, 模板: dict[str, Any]) -> dict[str, Any]:
    投诉书 = 填充模板(数据["complaint_template"], 参数)
    法条 = 数据["legal_basis"]
    话术 = 数据["talking_points"]
    证据 = 数据["evidence"]
    渠道 = 数据["channels"]

    if 语气 != "官方":
        投诉书 = 通心译转换(投诉书, 语气, 模板)
        法条 = [通心译转换(f, 语气, 模板) for f in 法条]
        话术 = [通心译转换(t, 语气, 模板) for t in 话术]
        证据 = [通心译转换(e, 语气, 模板) for e in 证据]
        渠道 = [通心译转换(c, 语气, 模板) for c in 渠道]

    return {
        "场景": 场景名,
        "语气": 语气,
        "生成时间": datetime.now(timezone.utc).isoformat(),
        "dna": DNA工具.生成(f"RIGHTS-ASSISTANT-{场景名}-{语气}", "1.1"),
        "投诉书": 投诉书,
        "法条依据": 法条,
        "怼人话术": 话术,
        "证据清单": 证据,
        "投诉渠道": 渠道,
    }


def 打印报告(报告: dict[str, Any]):
    print("\n" + "=" * 60)
    print(f"🐉 龍魂老百姓维权助手 · {报告['场景']} · {报告['语气']}版")
    print(f"生成时间: {报告['生成时间']}")
    print(f"DNA: {报告['dna']}")
    print("=" * 60)

    print("\n📜 投诉书/情况说明\n")
    print(报告["投诉书"])

    print("\n⚖️ 法条依据")
    for 法条 in 报告["法条依据"]:
        print(f"  • {法条}")

    print("\n🗣 回话话术")
    for 话术 in 报告["怼人话术"]:
        print(f"  • {话术}")

    print("\n📂 证据清单")
    for 证据 in 报告["证据清单"]:
        print(f"  • {证据}")

    print("\n📢 投诉渠道")
    for 渠道 in 报告["投诉渠道"]:
        print(f"  • {渠道}")

    print("\n" + "=" * 60)
    print("本报告由本地 AI 生成，不上传任何平台。")
    print("=" * 60 + "\n")


def 主函数():
    parser = argparse.ArgumentParser(description="龍魂老百姓维权助手")
    parser.add_argument("--text", "-t", help="描述你的遭遇", required=True)
    parser.add_argument("--name", "-n", default="（你的姓名）", help="你的姓名")
    parser.add_argument("--contact", "-c", default="（联系电话）", help="联系电话")
    parser.add_argument("--target", default="（对方单位/个人）", help="被投诉对象")
    parser.add_argument("--amount", default="（金额）", help="涉及金额")
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"), help="日期")
    parser.add_argument("--tone", choices=["大白话", "温柔坚定", "硬气", "讽刺", "官方"], default="大白话", help="输出语气")
    parser.add_argument("--save", "-s", help="保存报告到指定 JSON 文件")
    args = parser.parse_args()

    模板 = 加载模板()
    场景名 = 识别场景(args.text, 模板)
    if not 场景名:
        print("\n⚠️ 暂未识别到具体维权场景。")
        print("你可以描述得更具体一些，比如：")
        print("  - 物业强制我人脸识别才能进门")
        print("  - 公司拖欠我三个月工资")
        print("  - 商家卖假货不退款")
        print("  - 房东不退租房押金")
        print("  - 平台老用户价格更贵/大数据杀熟\n")
        sys.exit(0)

    数据 = 模板["scenarios"][场景名]
    参数 = {
        "name": args.name,
        "contact": args.contact,
        "target": args.target,
        "amount": args.amount,
        "date": args.date,
        # 场景特有字段默认值
        "id_card": "（身份证号）",
        "org_code": "（统一社会信用代码）",
        "position": "（岗位）",
        "start_date": "（入职/开始日期）",
        "arrears_date": "（开始欠薪日期）",
        "months": "（月数）",
        "product": "（商品/服务名称）",
        "problem": "（问题描述）",
        "purchase_date": "（购买日期）",
        "claim": "（商家宣传内容）",
        "reality": "（实际情况）",
        "compensation": "（索赔金额）",
        "order_no": "（订单号）",
        "address": "（房屋地址）",
        "end_date": "（合同结束日期）",
        "excuse": "（对方理由）",
        "user_type": "（用户类型）",
        "usage_time": "（使用时间）",
        "scenario": "（具体场景）",
        "evidence_description": "（证据描述）",
    }
    # 根据用户输入尝试提取一些信息
    参数["target"] = args.target
    参数["amount"] = args.amount

    报告 = 生成报告(场景名, 数据, 参数, args.tone, 模板)
    打印报告(报告)

    if args.save:
        保存路径 = Path(args.save)
        保存路径.write_text(json.dumps(报告, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 报告已保存: {保存路径}\n")


if __name__ == "__main__":
    主函数()
