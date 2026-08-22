#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂演示插件 · 展示 SandboxAPI 用法
DNA: #龍芯⚡️2026-08-22-DEMO-PLUGIN-v1.0
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""


def main(api):
    """插件入口"""
    print("🔌 Demo Plugin 启动")

    # 1. 生成 DNA
    dna_resp = api.request_dna_generate(module="demo-plugin", action="start")
    print(f"📝 生成 DNA: {dna_resp}")

    # 2. 尝试写入 MEMORY (被授予的能力 → 通过门控)
    mem_resp = api.request_memory_append(content="Demo Plugin 执行成功", source="plugin-demo")
    print(f"💾 MEMORY 写入: {mem_resp}")

    # 3. 尝试违规操作 (未授予 net.http → 被门控拒绝)
    invalid_resp = api.request("net.http", "get", {"url": "http://example.com"})
    print(f"🚫 违规请求结果: {invalid_resp}")

    return {"status": "success", "message": "Demo 完成"}
