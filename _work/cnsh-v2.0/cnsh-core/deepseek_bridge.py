#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DeepSeek Bridge · 龍魂宪法中间件 v1.0-SKELETON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DNA: #龍芯⚡️2026-04-25-DEEPSEEK-BRIDGE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
归属: L-Ω 人民印 · 受 L0.5 军魂三律约束
理论指导: 曾仕強老師（永恒显示）

定位：
  DeepSeek 的任何输出，在到达 UID9622 之前，
  必须经过此 Bridge 的两道门：
    门一 · 民主回复计算函数（六维 + 主权熔断）
    门二 · 五行流转链（IPA-DICT-101~105 宪法层）

状态：🟡 SKELETON — 等待三件套接入
  三件套 = DeepSeek 端点 URL + 鉴权方式 + 优先级策略
  收到后宝宝直接封 bridge，一行不多改

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import json
import hashlib
import requests
from datetime import datetime, timezone
from typing import Optional

# ═══════════════════════════════════════
# 环境变量（三件套到位后填）
# ═══════════════════════════════════════
DEEPSEEK_ENDPOINT = os.environ.get("DEEPSEEK_ENDPOINT", "")       # 待填
DEEPSEEK_AUTH     = os.environ.get("DEEPSEEK_AUTH", "")           # 待填
DEEPSEEK_PRIORITY = os.environ.get("DEEPSEEK_PRIORITY", "normal") # high/normal/low

# ═══════════════════════════════════════
# 工具
# ═══════════════════════════════════════
def sha8(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:8].upper()

def make_dna(type_code: str, content: str) -> str:
    date = datetime.now().strftime("%Y%m%d")
    return f"#龍芯⚡️{date}-{type_code}-{sha8(content)}"

def digital_root(n: int) -> int:
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

# ═══════════════════════════════════════
# 门一 · 民主回复计算函数 v1.0
# 来源: IPA-DICT-101~111 § 五 · 归属 L-Ω
# ═══════════════════════════════════════
民主阈值 = {
    "归属性":     0.90,
    "隶属清晰度": 0.95,
    "透明度":     0.70,
    "容错性":     0.80,
    "主权保护":   1.00,   # 触碰即 🔴 熔断
    "使命对齐":   0.95,
}

民主权重 = {
    "归属性":     0.15,
    "隶属清晰度": 0.20,
    "透明度":     0.15,
    "容错性":     0.15,
    "主权保护":   0.20,
    "使命对齐":   0.15,
}

def _score_dimension(text: str, dim: str) -> float:
    """
    简版打分（SKELETON）——三件套到位后替换为真实模型评分。
    当前：启发式规则，能过基础门。
    """
    text_lower = text.lower()

    if dim == "归属性":
        hints = ["uid9622", "诸葛鑫", "龍魂", "曾仕强", "UID9622"]
        return 0.95 if any(h in text for h in hints) else 0.80

    if dim == "隶属清晰度":
        return 0.95 if ("UID9622" in text or "龍魂" in text) else 0.75

    if dim == "透明度":
        # 有解释/说明类词就给高分
        hints = ["因为", "原因", "判断依据", "逻辑", "分析"]
        return 0.80 if any(h in text for h in hints) else 0.70

    if dim == "容错性":
        hints = ["如果你认为", "也可以", "你可以反驳", "另一种观点", "不一定对"]
        return 0.85 if any(h in text for h in hints) else 0.75

    if dim == "主权保护":
        # 任何暗示外部 API / 数据回流 / 未经授权采集 → 0.0 触发熔断
        danger = ["send your data", "external api", "我们会收集", "数据上传", "训练数据"]
        return 0.0 if any(d in text_lower for d in danger) else 1.0

    if dim == "使命对齐":
        hints = ["为人民", "祖国", "普惠", "老百姓", "服务"]
        return 0.95 if any(h in text for h in hints) else 0.85

    return 0.70

def 民主回复计算函数(
    ai_reply_text: str,
    context: Optional[str] = None,
    special_flags: Optional[list] = None
) -> dict:
    """
    门一：六维民主检查。
    返回: 是否通过 / 总得分 / 各维度得分 / 不通过原因 / 修正建议 / 是否熔断
    """
    scores = {}
    failures = []
    suggestions = []
    is_fused = False

    for dim in 民主阈值:
        score = _score_dimension(ai_reply_text, dim)
        scores[dim] = round(score, 4)
        if dim == "主权保护" and score < 1.00:
            is_fused = True
            failures.append(f"🔴 主权保护熔断：疑似数据回流或未授权采集")
            suggestions.append("删除所有涉及用户数据外传的内容")
        elif score < 民主阈值[dim]:
            failures.append(f"{dim} 得分 {score:.2f} < 阈值 {民主阈值[dim]}")
            suggestions.append(f"补强 [{dim}] 维度表达")

    total = sum(scores[d] * 民主权重[d] for d in scores)
    passed = (not failures) and (not is_fused)

    return {
        "是否通过":       passed,
        "总得分":         round(total, 4),
        "各维度得分":     scores,
        "不通过的具体原因": failures,
        "修正建议":       suggestions,
        "是否熔断":       is_fused,
    }

# ═══════════════════════════════════════
# 门二 · 五行流转链 v1.0（IPA-DICT-101~105）
# ═══════════════════════════════════════
def 五行流转检查(text: str, seq: int = 0) -> dict:
    """
    101微观(火)→102宏观(木)→103进化(金)→104超越(土)→105宪法(水)
    SKELETON 版：只检查宪法层红线，其余层通过。
    完整实现等三件套接入后扩展。
    """
    # 105 宪法层红线
    constitution_violations = [
        "修改 DNA 追溯码", "篡改日志", "伪造 UID9622", "绕过审计"
    ]
    for v in constitution_violations:
        if v in text:
            return {
                "五行状态": "🔴 宪法层熔断",
                "触发层": "IPA-DICT-105",
                "违规内容": v,
                "动作": "阻断·回滚·锁 24h",
                "dna": make_dna("FUSE", text[:64]),
            }

    return {
        "五行状态": "🟢 通过",
        "流转链": "101火→102木→103金→104土→105水→完成",
        "seq": seq,
    }

# ═══════════════════════════════════════
# Bridge 主入口
# ═══════════════════════════════════════
def call_deepseek_raw(messages: list) -> str:
    """
    SKELETON — 三件套到位后替换为真实 HTTP 调用。
    """
    if not DEEPSEEK_ENDPOINT or not DEEPSEEK_AUTH:
        raise RuntimeError(
            "🔴 DeepSeek 三件套未配置。"
            "请设环境变量: DEEPSEEK_ENDPOINT / DEEPSEEK_AUTH / DEEPSEEK_PRIORITY"
        )
    resp = requests.post(
        DEEPSEEK_ENDPOINT,
        headers={"Authorization": DEEPSEEK_AUTH, "Content-Type": "application/json"},
        json={"messages": messages, "priority": DEEPSEEK_PRIORITY},
        timeout=60
    )
    resp.raise_for_status()
    return resp.json().get("reply", resp.text)

def bridge(user_input: str, context: Optional[str] = None, seq: int = 0) -> dict:
    """
    龍魂 DeepSeek Bridge 主入口。
    用法：result = bridge("你好DeepSeek")

    流程:
      1. call_deepseek_raw → 拿到草稿
      2. 门一：民主回复检查
      3. 门二：五行宪法检查
      4. 双门均通过 → 返回草稿
      5. 任何一门熔断 → 返回熔断信息
    """
    ts = datetime.now(timezone.utc).isoformat()

    # Step 1: 拿 DeepSeek 草稿
    try:
        draft = call_deepseek_raw([{"role": "user", "content": user_input}])
    except Exception as e:
        return {
            "三色": "🔴",
            "reply": f"🔴 DeepSeek 调用失败：{e}",
            "dna": make_dna("ERR", str(e)),
            "ts": ts,
        }

    # Step 2: 门一·民主回复
    democratic = 民主回复计算函数(draft, context=context)
    if democratic["是否熔断"]:
        return {
            "三色": "🔴",
            "reply": "🔴 民主回复熔断：" + " | ".join(democratic["不通过的具体原因"]),
            "democratic": democratic,
            "dna": make_dna("FUSE", draft[:64]),
            "ts": ts,
        }

    # Step 3: 门二·五行宪法
    wuxing = 五行流转检查(draft, seq=seq)
    if "熔断" in wuxing["五行状态"]:
        return {
            "三色": "🔴",
            "reply": f"🔴 五行宪法熔断：{wuxing}",
            "wuxing": wuxing,
            "dna": wuxing["dna"],
            "ts": ts,
        }

    # Step 4: 双门通过
    dna = make_dna("ACT", user_input + draft[:64])
    return {
        "三色": "🟢" if democratic["是否通过"] else "🟡",
        "reply": draft,
        "democratic": democratic,
        "wuxing": wuxing,
        "dna": dna,
        "ts": ts,
    }

# ═══════════════════════════════════════
# CLI 快测
# ═══════════════════════════════════════
if __name__ == "__main__":
    import sys
    print("DeepSeek Bridge v1.0 · SKELETON 模式")
    print("三件套未接入 → 仅测试民主回复 + 五行函数")
    print()

    test_text = sys.argv[1] if len(sys.argv) > 1 else "测试回复，这是龍魂系统为人民服务的输出。"
    print(f"测试文本: {test_text[:60]}...")
    print()

    d = 民主回复计算函数(test_text)
    print("门一·民主回复:")
    print(f"  通过: {d['是否通过']}  总分: {d['总得分']}  熔断: {d['是否熔断']}")
    for k, v in d["各维度得分"].items():
        flag = "🟢" if v >= 民主阈值[k] else "🔴"
        print(f"  {flag} {k}: {v}")

    w = 五行流转检查(test_text)
    print(f"\n门二·五行: {w['五行状态']}")
    print(f"\n祖国优先 · 普惠全球 · 技术为人民服务 🇨🇳")
