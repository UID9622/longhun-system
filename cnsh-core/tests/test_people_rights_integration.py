#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人民权益联动测试

DNA:#龍芯⚡️2026-06-21-PEOPLE-RIGHTS-INTEGRATION-TEST-v1.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from people_rights_guard import (
    PeopleRightsGuard, ProviderType, DataPurpose, HarvestPattern
)


def main():
    print("╔═══════════════════════════════════════════════════╗")
    print("║  龍魂人民权益联动测试                             ║")
    print("║  反收割 · 反倒卖 · 反压榨 · 焊死                ║")
    print("╚═══════════════════════════════════════════════════╝")

    guard = PeopleRightsGuard()
    print(f"\n守门人状态: {guard.stats()}")

    # 良心服务商宣誓
    v, m = guard.swear_oath(
        "good-payment",
        "良心支付",
        ProviderType.PLATFORM,
        "我们宣誓：为人民服务，数据透明，不收割，人民可随时撤销授权。",
        [DataPurpose.SERVICE],
        "按交易手续费收取服务费，君子爱财取之有道。",
    )
    print(f"\n良心支付宣誓: {v.value} | {m}")

    # 黑数据公司（宣誓词敷衍 + 卖数据）
    v, m = guard.swear_oath(
        "evil-data",
        "黑数据公司",
        ProviderType.PLATFORM,
        "我们会好好服务用户。",
        [DataPurpose.SELL, DataPurpose.ADS],
        "通过出售用户画像和大数据杀熟盈利。",
    )
    print(f"黑数据宣誓: {v.value} | {m}")

    # 直接检测收割
    v, m = guard.check_behavior("some-app", "使用无限下滑和签到奖励提高用户粘性")
    print(f"诱导成瘾检测: {v.value} | {m}")

    v, m = guard.check_behavior("some-platform", "把用户通讯录打包出售给第三方数据商")
    print(f"数据倒卖检测: {v.value} | {m}")

    # 数据请求审查
    v, m = guard.check_data_request("good-payment", "手机号", DataPurpose.SERVICE, True, True)
    print(f"服务请求: {v.value} | {m}")

    v, m = guard.check_data_request("evil-data", "通讯录", DataPurpose.SELL, False, False)
    print(f"倒卖请求: {v.value} | {m}")

    # 数据导出权
    v, m = guard.check_export_right("good-payment", True, ["json", "csv"], False)
    print(f"\n良心支付导出权: {v.value} | {m}")

    v, m = guard.check_export_right("lock-in-app", False, [], False)
    print(f"锁死数据平台: {v.value} | {m}")

    # 职业秘密
    v, m = guard.protect_professional_secret("医生病历", False, False)
    print(f"\n医生病历保护: {v.value} | {m}")

    v, m = guard.protect_professional_secret("公开专利", True, True)
    print(f"公开专利: {v.value} | {m}")

    # 诚实责任
    v, m = guard.honesty_check("我不确定的问题", False)
    print(f"\n诚实回答: {v.value} | {m}")

    print(f"\n当前黑名单: {guard.list_blacklist()}")

    # 验证接入权限
    print(f"\n良心支付是否人民优先: {guard.is_people_first('good-payment')}")
    print(f"黑数据是否人民优先: {guard.is_people_first('evil-data')}")

    print("\n✅ 人民权益联动测试完成")


if __name__ == "__main__":
    main()
