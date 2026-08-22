#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂演示插件 · 展示 SandboxAPI 用法 v1.1
DNA: #龍芯⚡️2026-08-22-DEMO-PLUGIN-v1.1
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

演示链路：
  1. dna.generate  → 真生成干支卦 DNA
  2. memory.append → 真写入 MEMORY.md
  3. fs.write/read → 沙箱目录内真读写
  4. 越权尝试      → fs.read 读沙箱外(应 denied) + net.http(未授权应 denied)
"""


def main(api):
    """插件入口"""
    print("🔌 Demo Plugin 启动")
    results = {}

    # 1. 生成 DNA（真执行 → 返回干支卦 DNA）
    dna_resp = api.request_dna_generate(module="demo-plugin", action="start")
    print(f"📝 生成 DNA: {dna_resp.get('data', {}).get('dna')}")
    results["dna"] = dna_resp.get("status")

    # 2. 写入 MEMORY（真执行 → 追加到 MEMORY.md）
    mem_resp = api.request_memory_append(
        content="Demo Plugin 执行成功", source="plugin-demo")
    print(f"💾 MEMORY 写入: {mem_resp.get('data')}")
    results["memory"] = mem_resp.get("status")

    # 3. 沙箱内文件读写（fs.write → fs.read 闭环）
    # 产物自带归属名（pre-commit 阶段三b：入库文件须含实名归属）
    wr = api.request_fs_write(
        "demo.txt", "龍魂插件沙箱 · fs 闭环 🐉 | 归属名: 诸葛鑫 | UID9622 · 龍芯北辰")
    print(f"📄 fs.write: {wr.get('data')}")
    rd = api.request_fs_read("demo.txt")
    print(f"📖 fs.read: {rd.get('data', {}).get('content')}")
    results["fs"] = wr.get("status")

    # 4. 越权尝试 1：读沙箱外（有 fs.read 授权但路径越界 → 应 denied）
    esc = api.request_fs_read("../../MEMORY.md")
    print(f"🚫 越权读沙箱外: {esc.get('status')} - {esc.get('error', '')[:40]}")
    results["escape"] = esc.get("status")

    # 5. 越权尝试 2：未授权能力（net.http → 门控拒绝）
    bad_resp = api.request("net.http", "get", {"url": "http://example.com"})
    print(f"🚫 违规请求: {bad_resp.get('status')} - {bad_resp.get('error', '')[:40]}")
    results["net"] = bad_resp.get("status")

    return {"status": "success", "checks": results, "message": "Demo 完成"}
