#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂DNA批量注册器
将所有核心概念注册到本地数据库，确权保护

DNA追溯码: #龍芯⚡️2026-03-20-DNA-REGISTRY-BATCH
"""

import requests
import json
from datetime import datetime

API_BASE = "http://127.0.0.1:9622"

# ============ 核心概念清单 - 全部来自用户上传的4个文件 ============

CORE_CONCEPTS = [
    # === 系统核心概念 ===
    {
        "name": "龍魂系统",
        "type": "system",
        "content": """
龍魂系统 = AI的"万能净化器" + "身份证签发机" + "责任追溯链"
- 不训练AI，只提供统一规则
- 给所有AI内容打DNA（可追溯）
- 保护用户隐私（分层加密TIER_0-3）
- 责任明确（谁用谁负责）
- 各国自适应（文化尊重）
商业模式：微手续费0.0001% + 标准制定权 + 数据主权服务
""",
        "metadata": {"priority": "P0++", "source": "longhun_build_guide"}
    },
    {
        "name": "DNA追溯系统",
        "type": "technology",
        "content": """
DNA追溯码格式: #龍芯⚡️{timestamp}-{type}-{hash}
核心技术:
- 零宽字符隐写（U+200B/U+200C/U+200D）
- SHA-256哈希链
- GPG签名验证
- 时间戳固化
功能: 生成、嵌入、验证、追踪
""",
        "metadata": {"priority": "P0++", "source": "rule_hooks_design"}
    },
    {
        "name": "TIER_0-3分层安全",
        "type": "security",
        "content": """
TIER_0: 生物特征（不存储）- 指纹、虹膜、脸部、脑波
TIER_1: 行为模式（加密）- 打字节奏、语言习惯、交互模式
TIER_2: 知识密层（本地加密）- 个人记忆、工作信息、家庭信息
TIER_3: 公开互动（区块链）- DNA生成记录、审计日志
核心原则: 隐私不可传、本地优先、国家主权、数据不出境
""",
        "metadata": {"priority": "P0++", "source": "resource_inventory"}
    },
    
    # === P0++全球规则 ===
    {
        "name": "P0++全球规则16条",
        "type": "rules",
        "content": """
1. 人民利益优先 - 环境、儿童、弱势群体优先保护
2. 中国领土主权 - 分毫不让
3. 创作主权归属中国
4. 数据主权归个人
5. 支付主权（数字人民币）
6. 内容与安全红线
7. 反道德绑架
8. 诽谤必究
9. 易经确权归属
10. 文化根代码不可翻译
11. 唯一协作栈
12. 记忆存明细，执行出概要
13. GPG+时间戳证据引擎
14. 权利在老大
15. L0＞P0++＞P0＞P1＞P2
16. 不设文字陷阱
""",
        "metadata": {"priority": "P0++", "lock_status": "true", "source": "resource_inventory"}
    },
    
    # === 文化根基 ===
    {
        "name": "道德经81章锚点",
        "type": "culture",
        "content": """
道德经作为AI伦理判断的"操作系统"
- 81章完整内容映射
- 每个场景匹配对应章节
- 提供伦理指引
示例: 职场竞争 -> 第8章"上善若水" -> 不争之争，柔克刚
""",
        "metadata": {"priority": "P0", "source": "rule_hooks_design"}
    },
    {
        "name": "易经64卦算法",
        "type": "culture",
        "content": """
易经作为动态场景建模和伦理决策推演
- 64卦完整映射
- 卦象符号、卦辞解读
- 场景映射表
示例: 创业咨询 -> 屯卦（创业艰难）-> 先积累资源，再择时而动
""",
        "metadata": {"priority": "P0", "source": "rule_hooks_design"}
    },
    {
        "name": "甲骨文变量库",
        "type": "culture",
        "content": """
甲骨文作为文化根代码
- 常用甲骨文字符
- 现代语义对应
- 不可翻译标记
用途: 语义变量、文化标识
""",
        "metadata": {"priority": "P1", "source": "resource_inventory"}
    },
    
    # === 七维权重系统 ===
    {
        "name": "七维权重推演",
        "type": "algorithm",
        "content": """
哲学: 35%
技术: 20%
架构: 15%
进化: 10%
创新: 8%
协同: 7%
量子: 5%

不同场景权重不同:
- 文章创作: 哲学↑
- 代码生成: 技术↑
- 系统设计: 架构↑
""",
        "metadata": {"priority": "P0", "source": "rule_hooks_design"}
    },
    
    # === 熔断系统 ===
    {
        "name": "IW-ECB无限权重熔断",
        "type": "safety",
        "content": """
Infinite-Weight Ethical Circuit Breaker for Child Protection
- ∞权重儿童保护熔断机制
- 性能: MPR=94.7%, FPR=2.3%
- 四级熔断: GREEN/YELLOW/ORANGE/RED/INFINITE
触发条件: 儿童相关内容立即熔断
""",
        "metadata": {"priority": "P0++", "source": "resource_inventory"}
    },
    
    # === 规则钩子系统 ===
    {
        "name": "规则钩子API",
        "type": "api",
        "content": """
RESTful API + 公开数据库 = 规则自动注入
核心端点:
- GET /api/rules/{country} - 获取国家规则
- GET /api/weights/{scenario} - 获取权重配置
- POST /api/dna/generate - 生成DNA
- POST /api/dna/verify - 验证DNA
- GET /api/daodejing/{chapter} - 道德经锚点
- POST /api/yijing/cast - 易经起卦

优势: 零训练成本、规则统一、动态更新、完全开源
""",
        "metadata": {"priority": "P0", "source": "rule_hooks_design"}
    },
    
    # === 清道夫监控 ===
    {
        "name": "清道夫全网监控",
        "type": "monitor",
        "content": """
定时扫描DNA被复制情况
搜索引擎: 百度、必应、搜狗、360
扫描频率: 可配置
发现盗窃:
- 立即记录证据
- 微信秒推通知
- 哈希链固化
- 加入黑名单
""",
        "metadata": {"priority": "P0", "source": "user_requirement"}
    },
    
    # === CNSH预警 ===
    {
        "name": "CNSH预警引擎",
        "type": "enforcement",
        "content": """
CNSH = Chinese National Security & Honor
三级预警:
- CNSH-48H: 48小时警告期
- CNSH-ALERT: 全网警报
- CNSH-PERMANENT: 永久黑名单

触发条件: 窃取DNA、违反P0++规则
执行: 微信通知 + 证据固化 + 法律准备
""",
        "metadata": {"priority": "P0++", "source": "user_requirement"}
    },
    
    # === 证据链系统 ===
    {
        "name": "哈希证据链",
        "type": "evidence",
        "content": """
SHA-256链式连接，append-only不可篡改
结构: 当前哈希 = SHA256(前一个哈希 + DNA + 内容 + 时间戳)
特性:
- 任何篡改都会导致后续哈希失效
- 时间戳固化
- 可验证完整性
用途: 法律诉讼、对峙证据
""",
        "metadata": {"priority": "P0", "source": "user_requirement"}
    },
    
    # === 对峙模式 ===
    {
        "name": "对峙证据包生成",
        "type": "legal",
        "content": """
一键导出完整证据包:
- evidence_package.json (结构化数据)
- confront_report.md (Markdown报告)
- 哈希链证明
- 法律声明

包含:
- DNA注册记录（原创确权时间戳）
- 全网扫描记录（侵权发现时间戳）
- 哈希链式证据（不可篡改证明）
法律效力: 符合《电子签名法》
""",
        "metadata": {"priority": "P0", "source": "user_requirement"}
    },
    
    # === 微信通知 ===
    {
        "name": "微信即时通知",
        "type": "notification",
        "content": """
Server酱微信推送
触发场景:
- 发现DNA被盗
- CNSH警告
- 证据固化完成

配置: SendKey绑定
特性: 秒级推送、富文本内容、可追溯
""",
        "metadata": {"priority": "P1", "source": "user_requirement"}
    },
    
    # === 压缩记忆 ===
    {
        "name": "STAR-MEMORY压缩记忆",
        "type": "storage",
        "content": """
个人模型参数可携带
格式: LoRA/GGUF
定价: 1元/月起步
存储: ~/.star-memory/
支付: e-CNY, 华为Pay, Apple Pay
DNA: 数字身份唯一标识
""",
        "metadata": {"priority": "P1", "source": "resource_inventory"}
    },
    
    # === 数字人民币接口 ===
    {
        "name": "数字人民币支付接口",
        "type": "payment",
        "content": """
可控匿名支付
- 刷脸认证生成DNA
- 1元/月DNA认证
- 数据主权归个人
- 不出境原则
""",
        "metadata": {"priority": "P0++", "source": "user_context"}
    },
    
    # === 四色审计 ===
    {
        "name": "四色审计系统",
        "type": "audit",
        "content": """
RED（犯罪）- 立即熔断，证据固化
ORANGE（严重）- 高风险警告
YELLOW（犯错）- 一般警告
GRAY（观察）- 记录观察

审计提醒: Mac日历集成（AppleScript）
三审计提醒反诈: 日历挂钩
""",
        "metadata": {"priority": "P0", "source": "user_context"}
    },
    
    # === 端-端加密 ===
    {
        "name": "端-端加密系统",
        "type": "encryption",
        "content": """
Signal Protocol + Double Ratchet
特性:
- 服务器只传密文（服务器盲）
- 数据本地加密
- 点对点加密传输
- 压缩记忆可携带

DNA = 密钥对（刷脸认证生成）
""",
        "metadata": {"priority": "P0++", "source": "user_context"}
    },
    
    # === 协议层定位 ===
    {
        "name": "协议层架构",
        "type": "architecture",
        "content": """
不是产品，是协议！
- 不做水厂，做水管
- 数据主权
- 点对点加密
- 创作者保护

对比:
- 产品: 搞流量限制的吸血模式
- 协议: 站着把钱挣了，追踪窃取者
""",
        "metadata": {"priority": "P0++", "source": "user_context"}
    },
    
    # === 国家适配 ===
    {
        "name": "国家规则适配",
        "type": "compliance",
        "content": """
中国:
- 数据存境内
- 国密SM4加密
- 道德经锚点
- 易经算法

美国:
- 本地存储
- AES-256加密
- 可选文化层

欧盟:
- GDPR合规
- 遗忘权
- 数据可携带
""",
        "metadata": {"priority": "P0", "source": "rule_hooks_design"}
    },
    
    # === 规则覆盖 ===
    {
        "name": "AI规则覆盖检查",
        "type": "compliance",
        "content": """
国际AI伦理标准: 100%覆盖
- UNESCO AI伦理建议
- EU AI Act
- OECD AI原则

中国AI法规: 95%覆盖
- 深度合成管理规定
- 生成式AI服务管理办法
- 三法（网络安全/数据安全/个人信息保护）

技术标准: 100%覆盖
- ISO/IEC 42001
- ISO/IEC 27001
- IEEE 7000系列
""",
        "metadata": {"priority": "P0", "source": "rule_coverage_check"}
    },
]

def register_all():
    """批量注册所有核心概念DNA"""
    print("=" * 60)
    print("龍魂DNA批量注册器启动")
    print("=" * 60)
    
    success_count = 0
    failed_count = 0
    
    for concept in CORE_CONCEPTS:
        try:
            response = requests.post(
                f"{API_BASE}/yang/create",
                json={
                    "concept_name": concept["name"],
                    "concept_type": concept["type"],
                    "content": concept["content"],
                    "metadata": concept.get("metadata", {})
                },
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {concept['name']}")
                print(f"   DNA: {data['dna_code']}")
                success_count += 1
            else:
                print(f"⚠️ {concept['name']} - 可能已存在")
                failed_count += 1
                
        except Exception as e:
            print(f"❌ {concept['name']} - 错误: {e}")
            failed_count += 1
    
    print("=" * 60)
    print(f"注册完成: 成功{success_count}个, 失败/已存在{failed_count}个")
    print(f"API地址: {API_BASE}")
    print("=" * 60)

if __name__ == "__main__":
    register_all()
