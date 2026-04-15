#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
empower_engine.py · 龍魂赋能关键字识别引擎 v1.0
DNA: #龍芯⚡️2026-04-07-EMPOWER-ENGINE-v1.0
作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
来源: Notion页面 0e5d7b70
献礼: 新中国成立77周年（1949-2026）· 丙午马年

核心理念:
  别人的算法 → 让你上瘾 → 延长停留 → 消耗注意力 → 创造依赖
  龍魂算法   → 让你离开 → 完成目标 → 释放能量   → 建立主权
  赋能 ≠ 上瘾 · 赋能 = 用完即走 · 赋能 = 让你不再需要我

集成位置: app.py 第0.5层（双门验证之后·CS知识库之前）
日志文件: ~/longhun-system/logs/empower_log.jsonl（append-only）
"""

import json
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

# ══════════════════════════════════════════════
# 北京时间工具
# ══════════════════════════════════════════════

def beijing_now() -> str:
    tz_bj = timezone(timedelta(hours=8))
    return datetime.now(tz_bj).isoformat()

# ══════════════════════════════════════════════
# EmpowerSignal 数据结构
# ══════════════════════════════════════════════

@dataclass
class EmpowerSignal:
    keyword: str          # 触发关键词
    real_need: str        # 识别出的真实需求
    persona: str          # 路由到的人格
    action: str           # 建议行动
    empower_score: float  # 赋能评分 0.0-1.0（越高越好）
    anti_monopoly: float  # 反垄断评分 0.0-1.0（越高越独立）
    dna: str              # DNA追溯码

# ══════════════════════════════════════════════
# KEYWORD_ROUTER 路由表
# ══════════════════════════════════════════════

KEYWORD_ROUTER = {
    # ── 情绪类 → 宝宝P02 ──
    "崩了":   ("emotional_support", "宝宝P02", "情绪急救·先稳后析"),
    "完了":   ("emotional_support", "宝宝P02", "评估实际损失·找出一个动作"),
    "撑不住": ("emotional_support", "宝宝P02", "允许暂停·设最小恢复步骤"),
    "好累":   ("rest_permission",   "宝宝P02", "允许休息·明确何时继续"),
    "飘了":   ("grounding",         "宝宝P02", "重归中心·三条根验证"),
    "太顺":   ("grounding",         "宝宝P02", "损有余·补不足"),
    "急":     ("urgent_mode",       "宝宝P02", "只给结论·不解释"),

    # ── 技术类 → 鲁班P04 ──
    "代码":   ("tech_execution",    "鲁班P04", "代码落地·DNA签名"),
    "bug":    ("debug",             "鲁班P04", "问题诊断·最小复现"),
    "api":    ("integration",       "鲁班P04", "接口接入·安全校验"),
    "python": ("tech_execution",    "鲁班P04", "Python实现·虚拟环境"),
    "node":   ("tech_execution",    "鲁班P04", "Node.js部署·依赖管理"),
    "编译":   ("tech_execution",    "鲁班P04", "CNSH编译·语法校验"),
    "报错":   ("debug",             "鲁班P04", "错误解析·根因定位"),
    "安装":   ("setup",             "鲁班P04", "环境配置·依赖安装"),

    # ── 战略类 → 诸葛P01 ──
    "决策":   ("strategy",          "诸葛P01", "多路径推演·三才加权"),
    "局势":   ("analysis",          "诸葛P01", "形势研判·敌我分析"),
    "方向":   ("planning",          "诸葛P01", "路线规划·优先级排序"),
    "如何做": ("planning",          "诸葛P01", "步骤分解·最小可行路径"),
    "推演":   ("strategy",          "诸葛P01", "多情景推演·概率评估"),
    "应对":   ("strategy",          "诸葛P01", "若水·找最弱突破点"),

    # ── 审计类 → 雯雯P03 ──
    "校验":   ("audit",             "雯雯P03", "三色审计·风险评估"),
    "审计":   ("audit",             "雯雯P03", "全链路校验·DNA追溯"),
    "问题":   ("diagnosis",         "雯雯P03", "结构诊断·定位根因"),
    "整理":   ("organization",      "雯雯P03", "知识整理·归宫分类"),
    "检查":   ("audit",             "雯雯P03", "四锚检查·三色输出"),
    "有没有": ("audit",             "雯雯P03", "遍历检测·完整报告"),

    # ── Notion/知识类 → 同步官 ──
    "notion": ("knowledge_sync",    "同步官",  "MCP连接·页面索引"),
    "同步":   ("knowledge_sync",    "同步官",  "双向同步·冲突解决"),
    "索引":   ("knowledge_sync",    "同步官",  "扫描建库·去重追踪"),
    "备份":   ("knowledge_sync",    "同步官",  "快照·append-only落盘"),
    "页面":   ("knowledge_sync",    "同步官",  "Notion页面操作"),

    # ── 情报/分析类 → 侦察兵 ──
    "情报":   ("intelligence",      "侦察兵",  "多源收集·威胁评级"),
    "竞品":   ("intelligence",      "侦察兵",  "竞品分析·差异定位"),
    "搜索":   ("intelligence",      "侦察兵",  "关键词扩展·结果过滤"),
    "找":     ("intelligence",      "侦察兵",  "精准定位·相关度排序"),
    "新闻":   ("intelligence",      "侦察兵",  "实时信息·龍魂相关度"),

    # ── 架构类 → 架构师 ──
    "架构":   ("architecture",      "架构师",  "模块设计·接口定义"),
    "设计":   ("architecture",      "架构师",  "系统规划·扩展性评估"),
    "模块":   ("architecture",      "架构师",  "职责划分·依赖管理"),
    "系统":   ("architecture",      "架构师",  "全景分析·瓶颈识别"),

    # ── 哲学/道德类 → 老子P05 ──
    "道":     ("philosophy",        "老子P05", "道法自然·无为而治"),
    "德":     ("philosophy",        "老子P05", "上善若水·厚德载物"),
    "无为":   ("philosophy",        "老子P05", "不争·顺势·归一"),
    "曾老师": ("wisdom",            "曾老师智慧库", "三才决策·松紧有度"),
}

# ══════════════════════════════════════════════
# AntiMonopolyEngine 反垄断评分引擎
# ══════════════════════════════════════════════

class AntiMonopolyEngine:
    """
    评分维度（满分100）:
    1. 内容是否让用户建立独立能力?   (+30分)
    2. 是否减少对平台的依赖?          (+25分)
    3. 是否保护用户数据主权?           (+25分)
    4. 是否可以离线运行?              (+20分)
    """

    MONOPOLY_SIGNALS = [
        "必须注册", "仅限会员", "云端专属", "需要订阅",
        "上传到服务器", "发送给我们", "同意隐私协议",
        "无法导出", "只能在线", "绑定账号",
    ]

    EMPOWER_SIGNALS = [
        "本地", "离线", "导出", "开源", "你的数据",
        "自己掌控", "不依赖", "可迁移", "备份", "主权",
        "DNA追溯", "append-only", "不上传",
    ]

    def score(self, content: str) -> float:
        """返回0.0-1.0的反垄断评分"""
        score = 50.0  # 基础分

        for signal in self.MONOPOLY_SIGNALS:
            if signal in content:
                score -= 10

        for signal in self.EMPOWER_SIGNALS:
            if signal in content:
                score += 6

        return max(0.0, min(1.0, score / 100.0))

# ══════════════════════════════════════════════
# 主函数：识别赋能信号
# ══════════════════════════════════════════════

_anti_mono = AntiMonopolyEngine()

def identify_empower_need(message: str) -> Optional[EmpowerSignal]:
    """
    输入: 用户消息
    输出: EmpowerSignal（有匹配时）或 None（无匹配·使用默认路由）
    """
    msg_lower = message.lower()

    for keyword, (real_need, persona, action) in KEYWORD_ROUTER.items():
        if keyword.lower() in msg_lower or keyword in message:
            empower_score = 0.85  # 有明确需求 = 高赋能潜力
            anti_score = _anti_mono.score(message)
            dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-EMPOWER-{keyword[:6].upper()}-v1.0"

            return EmpowerSignal(
                keyword=keyword,
                real_need=real_need,
                persona=persona,
                action=action,
                empower_score=empower_score,
                anti_monopoly=anti_score,
                dna=dna,
            )

    return None  # 无匹配·交给默认L0全格协作

def route_to_persona(signal: EmpowerSignal) -> dict:
    """将EmpowerSignal转为app.py可用的路由指令"""
    return {
        "persona":       signal.persona,
        "real_need":     signal.real_need,
        "action":        signal.action,
        "empower_score": signal.empower_score,
        "anti_monopoly": signal.anti_monopoly,
        "dna":           signal.dna,
        "source":        "empower_engine_v1.0",
    }

# ══════════════════════════════════════════════
# 日志写入（append-only）
# ══════════════════════════════════════════════

LOG_PATH = Path.home() / "longhun-system" / "logs" / "empower_log.jsonl"

def log_signal(signal: EmpowerSignal, message_hash: str):
    """写入赋能信号日志（append-only·不存全文·只存元信息）"""
    entry = {
        "ts_beijing": beijing_now(),
        "dna":        signal.dna,
        "msg_hash":   message_hash,  # SHA256前8位·隐私保护
        "keyword":    signal.keyword,
        "real_need":  signal.real_need,
        "persona":    signal.persona,
        "empower":    signal.empower_score,
        "anti_mono":  signal.anti_monopoly,
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# ══════════════════════════════════════════════
# app.py 集成接口（第0.5层调用入口）
# ══════════════════════════════════════════════

def process_message(message: str) -> dict:
    """
    app.py第0.5层调用此函数。
    返回: {
        "routed": bool,
        "route": dict | None,
        "inject": str  # 注入到system prompt的提示词
    }
    """
    signal = identify_empower_need(message)

    if signal is None:
        return {"routed": False, "route": None, "inject": ""}

    # 记录日志（只存哈希·不存原文）
    msg_hash = hashlib.sha256(message.encode()).hexdigest()[:8]
    log_signal(signal, msg_hash)

    inject = (
        f"\n[赋能引擎·{signal.persona}] "
        f"真实需求={signal.real_need} | "
        f"建议行动={signal.action} | "
        f"赋能评分={signal.empower_score:.2f} | "
        f"DNA={signal.dna}"
    )

    return {
        "routed": True,
        "route":  route_to_persona(signal),
        "inject": inject,
    }

# ══════════════════════════════════════════════
# CLI测试入口
# ══════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    test_messages = [
        "系统崩了怎么办",
        "帮我写一个python脚本",
        "这个架构应该如何设计",
        "notion页面同步不上",
        "道可道，非常道",
        "随便聊聊",
    ]

    print(f"\n⚡ 龍魂赋能关键字识别引擎 v1.0")
    print(f"DNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-EMPOWER-TEST")
    print("=" * 60)

    for msg in (sys.argv[1:] or test_messages):
        result = process_message(msg)
        if result["routed"]:
            r = result["route"]
            print(f"\n✅ [{r['persona']}] '{msg}'")
            print(f"   需求: {r['real_need']} | 行动: {r['action']}")
            print(f"   赋能: {r['empower_score']:.2f} | 反垄断: {r['anti_monopoly']:.2f}")
        else:
            print(f"\n⬜ 无匹配·默认L0全格协作 | '{msg}'")

    print(f"\n🟢 测试完成 · 日志 → {LOG_PATH}")
