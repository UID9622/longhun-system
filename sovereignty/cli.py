# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂数字身份主权 · 命令行工具

服务对象：人民、基层干部、开发商、物业、社区管理者、快递员、外卖员、工地工人
用途：按层次解决问题，不是按群体贴标签

用法：
  python3 -m sovereignty.cli --protocol
  python3 -m sovereignty.cli --check 平台名 --auth 手机号,位置,相册
  python3 -m sovereignty.cli --layer L1   # 执行层：一线人员被压采集
  python3 -m sovereignty.cli --layer L2   # 协调层：主管/干部两头受气
  python3 -m sovereignty.cli --layer L3   # 监督层：居民/业主维权
  python3 -m sovereignty.cli --complain 平台名 --behavior 强制收集人脸

DNA:#龍芯⚡️2026-06-19-LONGHUN-SOVEREIGNTY-CLI-v1.1
"""

import argparse
import sys
from .digital_identity import 数字身份主权协议, 平台授权检查器, 维权话术生成器
from .templates import 居民告知书, 物业数据最小化授权书, 开发商数据合规承诺书, 数据删除申请书


def 打印协议():
    协议 = 数字身份主权协议()
    print(协议.生成协议文本())
    print("\n【一句话解释】")
    print("人民数据主权，平台服务降级。")
    print("\n【三句话怼人】")
    生成器 = 维权话术生成器()
    for 句 in 生成器.怼人三句():
        print(f"  • {句}")


def 检查授权(平台名: str, 授权项目: str):
    检查器 = 平台授权检查器(平台名)
    项目列表 = [x.strip() for x in 授权项目.split(",") if x.strip()]
    结果 = 检查器.检查授权(项目列表)

    print(f"\n🔍 平台：{平台名}")
    print(f"{'🟢 合规' if 结果['合规'] else '🔴 越界'}")
    if 结果["越界项目"]:
        print("\n越界授权：")
        for 项 in 结果["越界项目"]:
            print(f"  ❌ {项}")
    print(f"\n💡 建议：{结果['建议']}")


def 层次方案(层次: str):
    生成器 = 维权话术生成器()
    方案 = 生成器.层次解决方案(层次)

    print(f"\n🎯 层次：{方案['定位']} ({层次})")
    print(f"\n📌 说明：{方案['说明']}")

    print("\n😫 你会遇到的压力：")
    for 项 in 方案["压力"]:
        print(f"  • {项}")

    print("\n🛡️ 你的权力边界：")
    for 项 in 方案["权力边界"]:
        print(f"  • {项}")

    print("\n🗣️ 标准话术：")
    for 项 in 方案["标准话术"]:
        print(f"  • {项}")

    print("\n📄 你可以出示的文件：")
    for 项 in 方案["可出示文件"]:
        print(f"  • {项}")

    print("\n📞 你的求助渠道：")
    for 项 in 方案["求助渠道"]:
        print(f"  • {项}")


def 生成投诉(平台名: str, 越界行为: str):
    生成器 = 维权话术生成器()
    print(生成器.生成投诉书(平台名, 越界行为))


def 最小授权(业务需求: str):
    检查器 = 平台授权检查器("示例平台")
    方案 = 检查器.生成最小授权方案(业务需求)
    print(f"\n📦 业务需求：{业务需求}")
    print("平台最小必要授权：")
    for 项 in 方案:
        print(f"  ✅ {项}")


def 输出模板(模板名: str, 名称: str):
    模板映射 = {
        "居民告知书": 居民告知书,
        "物业授权书": 物业数据最小化授权书,
        "开发商承诺书": 开发商数据合规承诺书,
        "删除申请书": 数据删除申请书,
    }
    if 模板名 not in 模板映射:
        print(f"未知模板：{模板名}。可选：{', '.join(模板映射.keys())}")
        return
    print(模板映射[模板名](名称))


def 主动触发清单():
    生成器 = 维权话术生成器()
    清单 = 生成器.主动触发清单()

    print("\n🚨 遇到这些话，协议自动生效：")
    for 信号 in 清单["越界信号"]:
        print(f"  ⚠️ {信号}")

    print("\n📊 对应层次：")
    for 描述, 层次 in 清单["对应层次"].items():
        print(f"  {描述} -> {层次}")

    print("\n⚡ 立即行动：")
    for 项 in 清单["立即行动"]:
        print(f"  • {项}")


def main():
    解析器 = argparse.ArgumentParser(
        description="龍魂数字身份主权命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="协议是骨头，技能是肌肉。"
    )

    解析器.add_argument("--protocol", action="store_true", help="输出完整协议")
    解析器.add_argument("--check", metavar="平台名", help="检查平台授权是否越界")
    解析器.add_argument("--auth", metavar="授权项", help="逗号分隔的授权项目，如：手机号,位置,相册")
    解析器.add_argument("--layer", metavar="L1|L2|L3", help="按层次输出方案：L1执行层 L2协调层 L3监督层")
    解析器.add_argument("--complain", metavar="平台名", help="生成投诉书")
    解析器.add_argument("--behavior", metavar="越界行为", help="平台越界行为描述")
    解析器.add_argument("--min-auth", metavar="业务需求", help="生成最小授权方案")
    解析器.add_argument("--template", metavar="模板名", help="输出模板：居民告知书/物业授权书/开发商承诺书/删除申请书")
    解析器.add_argument("--name", metavar="名称", default="示例", help="模板中的名称")
    解析器.add_argument("--signals", action="store_true", help="输出主动触发清单")

    参数 = 解析器.parse_args()

    if 参数.protocol:
        打印协议()
    elif 参数.check and 参数.auth:
        检查授权(参数.check, 参数.auth)
    elif 参数.layer:
        层次方案(参数.layer)
    elif 参数.complain and 参数.behavior:
        生成投诉(参数.complain, 参数.behavior)
    elif 参数.min_auth:
        最小授权(参数.min_auth)
    elif 参数.template:
        输出模板(参数.template, 参数.name)
    elif 参数.signals:
        主动触发清单()
    else:
        解析器.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
