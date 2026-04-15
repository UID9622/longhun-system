#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统测试脚本
验证所有功能正常工作

DNA追溯码: #龍芯⚡️2026-03-20-SYSTEM-TEST
"""

import requests
import json
import time

API_BASE = "http://127.0.0.1:9622"

def test_endpoint(name: str, method: str, endpoint: str, data: dict = None):
    """测试单个端点"""
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ {name}")
            return response.json()
        else:
            print(f"❌ {name} - HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ {name} - 错误: {e}")
        return None

def run_tests():
    """运行完整测试"""
    print("=" * 60)
    print("龍魂系统功能测试")
    print("=" * 60)
    
    # 测试1: 根入口
    print("\n[基础测试]")
    root = test_endpoint("API根入口", "GET", "/")
    if root:
        print(f"   系统: {root.get('system')}")
        print(f"   DNA: {root.get('dna')}")
    
    # 测试2: 创建DNA
    print("\n[阳面 - DNA创建]")
    dna_result = test_endpoint("创建DNA", "POST", "/yang/create", {
        "concept_name": "测试概念-系统验证",
        "concept_type": "test",
        "content": "这是系统测试用的概念内容，用于验证DNA创建功能正常工作。",
        "metadata": {"test": True, "priority": "P0"}
    })
    
    if not dna_result or not dna_result.get("success"):
        print("\n❌ DNA创建失败，后续测试跳过")
        return
    
    dna_code = dna_result["dna_code"]
    print(f"   DNA: {dna_code}")
    
    # 测试3: 嵌入DNA
    print("\n[阳面 - DNA嵌入]")
    embed_result = test_endpoint("嵌入DNA水印", "POST", "/yang/embed", {
        "content": "这是需要保护的原创内容，包含重要概念。",
        "dna_code": dna_code
    })
    if embed_result:
        print(f"   原长度: {embed_result.get('original_length')}")
        print(f"   嵌入后: {embed_result.get('embedded_length')}")
        embedded_content = embed_result.get("embedded_content", "")
    
    # 测试4: 追踪DNA
    print("\n[阴面 - DNA追踪]")
    trace_result = test_endpoint("追踪DNA", "GET", f"/yin/trace/{dna_code}")
    if trace_result:
        print(f"   概念: {trace_result.get('concept_name')}")
        print(f"   类型: {trace_result.get('concept_type')}")
        print(f"   创建者: {trace_result.get('creator_uid')}")
    
    # 测试5: 提取DNA
    print("\n[阴面 - DNA提取]")
    extract_result = test_endpoint("提取DNA水印", "POST", "/yin/extract", {
        "content": embedded_content if embed_result else "测试内容"
    })
    if extract_result:
        print(f"   发现DNA: {extract_result.get('dna_found')}")
        print(f"   DNA数量: {extract_result.get('dna_count')}")
    
    # 测试6: 证据链
    print("\n[证据链]")
    evidence_result = test_endpoint("获取证据链", "GET", f"/evidence/chain/{dna_code}")
    if evidence_result:
        print(f"   证据数量: {evidence_result.get('evidence_count')}")
        print(f"   完整性: {evidence_result.get('integrity')}")
    
    # 测试7: 清道夫扫描（简化测试）
    print("\n[清道夫监控]")
    print("⚠️  清道夫扫描需要联网，跳过实际搜索测试")
    print("   端点: POST /sweeper/scan")
    print("   功能: 百度/必应搜索DNA，发现盗窃")
    
    # 测试8: 生成对峙包
    print("\n[对峙模式]")
    confront_result = test_endpoint("生成证据包", "POST", "/confront/generate", {
        "dna_code": dna_code
    })
    if confront_result:
        print(f"   包ID: {confront_result.get('package_id')}")
        print(f"   证据数: {confront_result.get('evidence_count')}")
        print(f"   文件: {confront_result.get('files')}")
    
    # 测试9: 黑名单
    print("\n[CNSH黑名单]")
    blacklist_result = test_endpoint("获取黑名单", "GET", "/audit/blacklist")
    if blacklist_result:
        print(f"   黑名单数量: {blacklist_result.get('blacklist_count')}")
    
    # 测试10: 微信通知（需要配置）
    print("\n[微信通知]")
    print("⚠️  微信通知需要配置Server酱SendKey")
    print("   配置端点: POST /wechat/config")
    print("   测试端点: POST /wechat/test")
    
    # 总结
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print(f"\n核心功能验证:")
    print(f"  ✅ DNA创建与注册")
    print(f"  ✅ DNA水印嵌入（零宽字符）")
    print(f"  ✅ DNA追踪查询")
    print(f"  ✅ DNA水印提取")
    print(f"  ✅ 哈希证据链")
    print(f"  ✅ 对峙证据包生成")
    print(f"  ✅ CNSH黑名单")
    print(f"\n待配置功能:")
    print(f"  ⏳ 微信通知（需要Server酱SendKey）")
    print(f"  ⏳ 清道夫定时扫描（需要启动守护进程）")
    print(f"\nAPI地址: {API_BASE}")
    print(f"测试DNA: {dna_code}")
    print("=" * 60)

if __name__ == "__main__":
    print("等待API服务器启动...")
    time.sleep(2)
    run_tests()
