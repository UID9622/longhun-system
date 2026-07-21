#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH OS API Server v2.5

DNA:#龍芯⚡️2026-06-09-CNSH-API-SERVER-v2.5
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
作者: UID9622 · 龍芯北辰 · 诸葛鑫
AI协作: Kimi
许可证: CC BY-NC-SA 4.0 + AI协作标签
三色审计: 🟢

龍魂系统AI路由服务 - FastAPI后端
功能: CNSH标准JSON接口 / 三AI结构路由 / DNA自动生成 / 审计日志
"""

# ═══════════════════════════════════════════════════════════
# 第一部分: 导入模块
# ═══════════════════════════════════════════════════════════
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, status  # type: ignore[import-untyped]
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Literal, Any, Tuple
import hashlib
import json
import time
import uuid
import logging
import asyncio
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field

# ═══════════════════════════════════════════════════════════
# 第二部分: 日志配置
# ═══════════════════════════════════════════════════════════
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
日志记录器 = logging.getLogger("CNSH_OS")

# ═══════════════════════════════════════════════════════════
# 第三部分: 枚举定义
# ═══════════════════════════════════════════════════════════


class 五行元素(str, Enum):
    """五行元素枚举"""
    金 = "金"
    木 = "木"
    水 = "水"
    火 = "火"
    土 = "土"


class AI来源(str, Enum):
    """AI模型来源枚举"""
    GPT = "GPT"
    Claude = "Claude"
    Grok = "Grok"
    Gemini = "Gemini"


class 状态机(str, Enum):
    """CNSH状态机枚举"""
    IDEA = "IDEA"      # 初始创意
    DRAFT = "DRAFT"    # 草稿
    REVIEW = "REVIEW"  # 审查中
    ACTIVE = "ACTIVE"  # 已激活
    FROZEN = "FROZEN"  # 已冻结
    BLOCKED = "BLOCKED" # 已阻塞


class 裁决决策(str, Enum):
    """Router裁决决策枚举"""
    KEEP = "KEEP"      # 保留
    MODIFY = "MODIFY"  # 修改
    REJECT = "REJECT"  # 拒绝


class 审计颜色(str, Enum):
    """三色审计颜色枚举"""
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


# ═══════════════════════════════════════════════════════════
# 第四部分: Pydantic数据模型 (CNSH Standard JSON)
# ═══════════════════════════════════════════════════════════


class CNSH_块模型(BaseModel):
    """CNSH标准块模型"""
    block_id: str = Field(..., description="块唯一标识符")
    content: str = Field(..., min_length=1, description="块内容文本")
    tags: List[str] = Field(default_factory=list, description="标签列表")
    element: Literal["金", "木", "水", "火", "土"] = Field(..., description="五行元素标记")
    author: str = Field(default="UID9622", description="作者标识")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="时间戳")

    @field_validator("content")
    @classmethod
    def 内容不能为空(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("块内容不能为空")
        return v.strip()


class CNSH_输入模型(BaseModel):
    """CNSH标准输入模型"""
    dna: str = Field(default="", description="DNA标识(空则自动生成)")
    source_ai: Literal["GPT", "Claude", "Grok", "Gemini"] = Field(..., description="来源AI模型")
    input: str = Field(..., min_length=1, description="输入文本")
    blocks: List[CNSH_块模型] = Field(default_factory=list, description="输入块列表")
    user_id: str = Field(default="UID9622", description="用户标识")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="元数据")

    @field_validator("input")
    @classmethod
    def 输入不能为空(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("输入文本不能为空")
        return v.strip()


class CNSH_分析模型(BaseModel):
    """CNSH分析结果模型"""
    value_score: float = Field(0, ge=0, le=100, description="价值评分 0-100")
    risk_score: float = Field(0, ge=0, le=100, description="风险评分 0-100")
    hallucination: float = Field(0, ge=0, le=1, description="幻觉概率 0-1")
    conflict: bool = Field(False, description="是否存在冲突")
    bias_score: float = Field(0, ge=0, le=100, description="偏见评分 0-100")
    logic_score: float = Field(0, ge=0, le=100, description="逻辑评分 0-100")


class CNSH_流转模型(BaseModel):
    """CNSH状态流转模型"""
    next_state: Literal["IDEA", "DRAFT", "REVIEW", "ACTIVE", "FROZEN", "BLOCKED"] = Field(
        ..., description="下一状态"
    )
    confidence: float = Field(0.5, ge=0, le=1, description="状态转换置信度")
    reason: str = Field(default="", description="状态转换原因")


class CNSH_审计模型(BaseModel):
    """CNSH审计结果模型"""
    requires_human: bool = Field(False, description="是否需要人工审查")
    override: bool = Field(False, description="是否覆盖AI决策")
    audit_color: Literal["🟢", "🟡", "🔴"] = Field("🟢", description="审计颜色标记")
    audit_log: List[str] = Field(default_factory=list, description="审计日志列表")
    decision: Literal["KEEP", "MODIFY", "REJECT"] = Field("KEEP", description="裁决决策")


class CNSH_输出模型(BaseModel):
    """CNSH标准输出模型"""
    dna: str = Field(..., description="DNA标识")
    source_ai: str = Field(..., description="来源AI模型")
    blocks: List[CNSH_块模型] = Field(default_factory=list, description="输出块列表")
    analysis: CNSH_分析模型 = Field(..., description="分析结果")
    flow: CNSH_流转模型 = Field(..., description="状态流转")
    audit: CNSH_审计模型 = Field(..., description="审计结果")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="时间戳")
    processing_time_ms: float = Field(0.0, description="处理时间(毫秒)")


class 状态更新模型(BaseModel):
    """状态更新请求模型"""
    block_id: str = Field(..., description="块ID")
    new_state: Literal["IDEA", "DRAFT", "REVIEW", "ACTIVE", "FROZEN", "BLOCKED"] = Field(
        ..., description="新状态"
    )
    reason: Optional[str] = Field(default=None, description="状态变更原因")


class 审计请求模型(BaseModel):
    """审计请求模型"""
    block_id: str = Field(..., description="块ID")
    audit_depth: Literal["basic", "standard", "deep"] = Field(
        default="standard", description="审计深度"
    )


class 人格任务模型(BaseModel):
    """人格任务请求模型"""
    task: str = Field(..., min_length=1, description="任务描述")
    task_type: Literal["write", "review", "analyze", "merge", "creative"] = Field(
        ..., description="任务类型"
    )
    persona_list: List[str] = Field(
        default_factory=lambda: ["GPT", "Claude"], description="使用的人格列表"
    )
    priority: int = Field(default=5, ge=1, le=10, description="优先级 1-10")


class 健康状态模型(BaseModel):
    """系统健康状态模型"""
    status: str = Field(..., description="系统状态")
    version: str = Field(..., description="版本号")
    uptime: float = Field(..., description="运行时间(秒)")
    total_requests: int = Field(..., description="总请求数")
    active_blocks: int = Field(..., description="活跃块数")
    audit_status: str = Field(..., description="审计状态")


class 查询参数模型(BaseModel):
    """查询参数模型"""
    dna: Optional[str] = Field(default=None, description="DNA标识")
    score: Optional[float] = Field(default=None, ge=0, le=100, description="分数阈值")
    ai_source: Optional[str] = Field(default=None, description="AI来源")
    state: Optional[str] = Field(default=None, description="状态")
    tag: Optional[str] = Field(default=None, description="标签")
    limit: int = Field(default=20, ge=1, le=100, description="返回数量限制")


# ═══════════════════════════════════════════════════════════
# 第五部分: DNA生成器
# ═══════════════════════════════════════════════════════════


def 生成DNA(content: str, ai_model: str, user_id: str = "UID9622") -> str:
    """
    生成CNSH标准DNA

    格式: CNSH-YYYYMMDD-16位哈希大写
    基于: SHA256(content + ai_model + timestamp + user_id)
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_input = f"{content}{ai_model}{timestamp}{user_id}"
    hash_value = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:16].upper()
    return f"CNSH-{datetime.now().strftime('%Y%m%d')}-{hash_value}"


def 五行标记(value_score: float) -> str:
    """
    根据价值评分确定五行标记

    0-20  → 水
    20-40 → 木
    40-60 → 土
    60-80 → 火
    80-100 → 金
    """
    if value_score < 20:
        return "水"
    elif value_score < 40:
        return "木"
    elif value_score < 60:
        return "土"
    elif value_score < 80:
        return "火"
    else:
        return "金"


def 计算审计颜色(risk_score: float, conflict: bool, hallucination: float) -> str:
    """
    计算审计颜色标记

    🔴: risk > 70 OR conflict = true OR hallucination > 0.5
    🟡: risk > 40 OR hallucination > 0.2
    🟢: 其他安全情况
    """
    if risk_score > 70 or conflict or hallucination > 0.5:
        return "🔴"
    elif risk_score > 40 or hallucination > 0.2:
        return "🟡"
    return "🟢"


def 计算裁决决策(
    conflict: bool, risk_score: float, value_score: float, hallucination: float
) -> str:
    """
    Router裁决引擎决策逻辑

    IF conflict = true    → MODIFY
    IF risk > 70          → REJECT
    IF value > 85 AND safe → KEEP
    ELSE                  → MODIFY (默认)
    """
    if conflict:
        return "MODIFY"
    if risk_score > 70:
        return "REJECT"
    if value_score > 85 and risk_score < 30 and hallucination < 0.1:
        return "KEEP"
    return "MODIFY"


def 计算下一状态(
    value_score: float, risk_score: float, conflict: bool, current_state: str = "IDEA"
) -> Tuple[str, float, str]:
    """
    计算下一状态及置信度

    IDEA → DRAFT: 初评完成
    DRAFT → REVIEW: 需要审查
    REVIEW → ACTIVE: 通过审查
    REVIEW → BLOCKED: 未通过
    ANY → FROZEN: 高风险冻结
    """
    if risk_score > 75:
        return ("BLOCKED", 0.9, "风险评分过高，自动阻塞")
    if value_score > 80 and not conflict and risk_score < 30:
        return ("ACTIVE", 0.85, "高质量内容，直接激活")
    if value_score > 50 and not conflict:
        return ("DRAFT", 0.7, "中等质量，进入草稿")
    if conflict:
        return ("REVIEW", 0.8, "检测到冲突，进入审查")
    return ("DRAFT", 0.6, "默认进入草稿状态")


# ═══════════════════════════════════════════════════════════
# 第六部分: 内存数据存储 (生产环境应替换为数据库)
# ═══════════════════════════════════════════════════════════


class 内存存储:
    """内存数据存储管理器"""

    def __init__(self):
        self.块表: Dict[str, Dict[str, Any]] = {}
        self.审计日志表: List[Dict[str, Any]] = []
        self.请求计数器: int = 0
        self.启动时间: float = time.time()

    def 保存块(self, block_id: str, 块数据: Dict[str, Any]) -> None:
        """保存块到存储"""
        self.块表[block_id] = 块数据

    def 获取块(self, block_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取块"""
        return self.块表.get(block_id)

    def 查询块(
        self,
        dna: Optional[str] = None,
        score: Optional[float] = None,
        ai_source: Optional[str] = None,
        state: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """多条件查询块"""
        结果 = []
        for 块 in self.块表.values():
            if dna and 块.get("dna") != dna:
                continue
            if ai_source and 块.get("source_ai") != ai_source:
                continue
            if state and 块.get("state") != state:
                continue
            if tag and tag not in 块.get("tags", []):
                continue
            if score is not None:
                块评分 = 块.get("value_score", 0)
                if 块评分 < score:
                    continue
            结果.append(块)
            if len(结果) >= limit:
                break
        return 结果

    def 记录审计日志(self, 日志条目: Dict[str, Any]) -> None:
        """记录审计日志"""
        self.审计日志表.append(日志条目)

    def 获取审计日志(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取审计日志"""
        return self.审计日志表[-limit:]

    def 增加请求计数(self) -> None:
        """增加请求计数"""
        self.请求计数器 += 1

    def 获取统计(self) -> Dict[str, Any]:
        """获取存储统计信息"""
        return {
            "total_blocks": len(self.块表),
            "total_audit_logs": len(self.审计日志表),
            "total_requests": self.请求计数器,
            "uptime": time.time() - self.启动时间,
        }


# 全局存储实例
存储 = 内存存储()

# ═══════════════════════════════════════════════════════════
# 第七部分: 三AI路由系统
# ═══════════════════════════════════════════════════════════


class AI路由器:
    """
    三AI结构路由器

    GPT    : 结构化生成 + 切块 + 创意扩展
    Claude : 逻辑审查 + 风险分析 + 冲突识别
    Router : 裁决引擎 (KEEP / MODIFY / REJECT)

    路由规则:
    - IF conflict = true    → MODIFY (需要修改)
    - IF risk > 70          → REJECT (拒绝)
    - IF value > 85 AND safe → KEEP  (保留)
    """

    def __init__(self):
        self.路由统计: Dict[str, int] = {"GPT": 0, "Claude": 0, "Router": 0}

    async def GPT_生成(self, input_text: str, user_id: str = "UID9622") -> Dict[str, Any]:
        """
        GPT: 结构化生成阶段

        模拟GPT输出:
        - 将输入文本结构化
        - 生成多个内容块
        - 初始价值评分
        """
        日志记录器.info(f"[GPT_生成] 开始处理, 输入长度: {len(input_text)}")
        await asyncio.sleep(0.05)  # 模拟API调用延迟

        # 模拟GPT结构化输出
        块列表 = []
        段落列表 = [p.strip() for p in input_text.split("\n") if p.strip()]

        if not 段落列表:
            段落列表 = [input_text]

        for 索引, 段落 in enumerate(段落列表[:5]):  # 最多5个块
            块id = f"BLK-{uuid.uuid4().hex[:8].upper()}"
            五行 = 五行标记(min(50 + 索引 * 10, 90))
            块列表.append({
                "block_id": 块id,
                "content": 段落[:200],
                "tags": ["gpt_generated", f"段落{索引 + 1}"],
                "element": 五行,
                "author": "GPT",
                "timestamp": datetime.now().isoformat(),
            })

        # GPT初始评分 (模拟)
        价值分 = min(50 + len(input_text) % 30, 85)
        风险分 = max(10, 30 - len(input_text) % 20)
        幻觉概率 = round(0.05 + (len(input_text) % 10) / 100, 3)

        结果 = {
            "blocks": 块列表,
            "value_score": 价值分,
            "risk_score": 风险分,
            "hallucination": 幻觉概率,
            "conflict": False,
            "source": "GPT",
            "process_time_ms": 45.0,
        }
        self.路由统计["GPT"] += 1
        日志记录器.info(f"[GPT_生成] 完成, 生成 {len(块列表)} 个块, 价值分: {价值分}")
        return 结果

    async def Claude_审查(self, input_text: str, gpt_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Claude: 逻辑审查阶段

        模拟Claude审查:
        - 逻辑一致性检查
        - 风险重新评估
        - 冲突检测
        - 偏见分析
        """
        日志记录器.info(f"[Claude_审查] 开始审查, GPT输出块数: {len(gpt_output.get('blocks', []))}")
        await asyncio.sleep(0.05)  # 模拟API调用延迟

        # Claude审查逻辑 (模拟)
        gpt价值分 = gpt_output.get("value_score", 50)
        gpt风险分 = gpt_output.get("risk_score", 30)
        gpt幻觉 = gpt_output.get("hallucination", 0.1)

        # Claude通常更保守，风险评分可能上调
        审查后风险分 = min(gpt风险分 + 10 + len(input_text) % 15, 95)
        审查后价值分 = max(gpt价值分 - 5, 20)
        幻觉修正 = min(gpt幻觉 * 1.2, 0.95)

        # 冲突检测
        冲突检测 = len(input_text) > 100 and hash(input_text) % 7 == 0
        if "矛盾" in input_text or "冲突" in input_text:
            冲突检测 = True

        # 偏见和逻辑评分
        偏见分 = max(5, min(50, len(input_text) % 40))
        逻辑分 = min(90, 70 + len(input_text) % 25) if not 冲突检测 else max(20, 40 - len(input_text) % 20)

        结果 = {
            "blocks": gpt_output.get("blocks", []),
            "value_score": round(审查后价值分, 2),
            "risk_score": round(审查后风险分, 2),
            "hallucination": round(幻觉修正, 3),
            "conflict": 冲突检测,
            "bias_score": round(偏见分, 2),
            "logic_score": round(逻辑分, 2),
            "source": "Claude",
            "review_notes": [
                f"逻辑评分: {逻辑分}",
                f"冲突检测: {'是' if 冲突检测 else '否'}",
                f"偏见评分: {偏见分}",
            ],
            "process_time_ms": 55.0,
        }
        self.路由统计["Claude"] += 1
        日志记录器.info(f"[Claude_审查] 完成, 冲突: {冲突检测}, 逻辑分: {逻辑分}")
        return 结果

    async def Router_裁决(
        self, gpt结果: Dict[str, Any], claude结果: Dict[str, Any], user_id: str = "UID9622"
    ) -> CNSH_输出模型:
        """
        Router: 裁决引擎

        综合GPT和Claude结果，做出最终决策:
        1. 评分加权平均 (GPT 40% + Claude 60%)
        2. 裁决决策
        3. 状态流转
        4. 审计标记
        """
        日志记录器.info("[Router_裁决] 开始裁决")
        await asyncio.sleep(0.03)  # 模拟裁决延迟

        # 加权平均评分
        综合价值分 = round(gpt结果.get("value_score", 50) * 0.4 + claude结果.get("value_score", 50) * 0.6, 2)
        综合风险分 = round(gpt结果.get("risk_score", 30) * 0.4 + claude结果.get("risk_score", 30) * 0.6, 2)
        综合幻觉 = round(gpt结果.get("hallucination", 0.1) * 0.4 + claude结果.get("hallucination", 0.1) * 0.6, 3)
        冲突标记 = claude结果.get("conflict", False)

        # 裁决决策
        裁决 = 计算裁决决策(冲突标记, 综合风险分, 综合价值分, 综合幻觉)

        # 状态流转
        下一状态, 置信度, 原因 = 计算下一状态(综合价值分, 综合风险分, 冲突标记)

        # 审计颜色
        审计色 = 计算审计颜色(综合风险分, 冲突标记, 综合幻觉)

        # 是否需要人工审查
        需人工 = 综合风险分 > 60 or 冲突标记 or 审计色 == "🔴"

        # 合并块列表 (以GPT为主，Claude审查)
        合并块 = claude结果.get("blocks", gpt结果.get("blocks", []))

        # 生成DNA
        所有内容 = " ".join([b.get("content", "") for b in 合并块])
        dna = 生成DNA(所有内容, "Router三AI融合", user_id)

        # 构建审计日志
        审计日志条目 = [
            f"GPT价值分: {gpt结果.get('value_score', 0)} → 融合后: {综合价值分}",
            f"Claude风险分: {claude结果.get('risk_score', 0)} → 融合后: {综合风险分}",
            f"冲突检测: {'是' if 冲突标记 else '否'}",
            f"裁决结果: {裁决}",
            f"审计颜色: {审计色}",
            f"下一状态: {下一状态} (置信度: {置信度})",
        ]

        # 构建输出
        分析结果 = CNSH_分析模型(
            value_score=综合价值分,
            risk_score=综合风险分,
            hallucination=综合幻觉,
            conflict=冲突标记,
            bias_score=claude结果.get("bias_score", 0),
            logic_score=claude结果.get("logic_score", 0),
        )

        流转结果 = CNSH_流转模型(
            next_state=下一状态,  # type: ignore[arg-type]
            confidence=置信度,
            reason=原因,
        )

        审计结果 = CNSH_审计模型(
            requires_human=需人工,
            override=False,
            audit_color=审计色,  # type: ignore[arg-type]
            audit_log=审计日志条目,
            decision=裁决,  # type: ignore[arg-type]
        )

        # 转换块为Pydantic模型
        块模型列表 = []
        for b in 合并块:
            块模型列表.append(CNSH_块模型(
                block_id=b.get("block_id", f"BLK-{uuid.uuid4().hex[:8]}"),
                content=b.get("content", ""),
                tags=b.get("tags", []),
                element=b.get("element", "土"),  # type: ignore[arg-type]
                author=b.get("author", "AI"),
                timestamp=b.get("timestamp", datetime.now().isoformat()),
            ))

        输出 = CNSH_输出模型(
            dna=dna,
            source_ai="Router(三AI融合)",
            blocks=块模型列表,
            analysis=分析结果,
            flow=流转结果,
            audit=审计结果,
            processing_time_ms=gpt结果.get("process_time_ms", 0) + claude结果.get("process_time_ms", 0) + 30,
        )

        self.路由统计["Router"] += 1
        日志记录器.info(f"[Router_裁决] 完成, 决策: {裁决}, 审计: {审计色}")
        return 输出


# 全局路由器实例
路由器 = AI路由器()


# ═══════════════════════════════════════════════════════════
# 第八部分: FastAPI应用主框架
# ═══════════════════════════════════════════════════════════

app = FastAPI(
    title="CNSH OS API",
    description="龍魂系统AI路由服务 - 三AI结构 / CNSH标准JSON / DNA自动生成 / 审计日志",
    version="2.5.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS中间件（🛡️ P77修复：白名单替代通配符）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8766", "http://127.0.0.1:8766"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-DNA-TRACE", "X-CNSH-CONFIRM"],
)


# ═══════════════════════════════════════════════════════════
# 第九部分: 审计中间件
# ═══════════════════════════════════════════════════════════


@app.middleware("http")
async def 审计中间件(request: Request, call_next):
    """
    审计中间件 - 每个请求自动记录审计日志 + 🛡️ P77 安全头部注入

    记录:
    - 请求DNA (唯一标识)
    - 请求方法和路径
    - 三色审计结果
    - 处理时间
    - 客户端IP

    安全头部:
    - CSP: 限制脚本/样式来源
    - X-Content-Type-Options: 防MIME嗅探
    - X-Frame-Options: 防点击劫持
    - X-XSS-Protection: 浏览器XSS过滤
    """
    开始时间 = time.time()
    请求dna = f"REQ-{uuid.uuid4().hex[:12].upper()}"
    请求路径 = request.url.path
    请求方法 = request.method

    日志记录器.info(f"[审计中间件] {请求dna} | {请求方法} {请求路径} | 开始处理")

    try:
        response = await call_next(request)
        处理时间 = (time.time() - 开始时间) * 1000

        # 记录审计日志
        审计条目 = {
            "request_dna": 请求dna,
            "method": 请求方法,
            "path": 请求路径,
            "status_code": response.status_code,
            "processing_time_ms": round(处理时间, 2),
            "timestamp": datetime.now().isoformat(),
            "client_host": request.client.host if request.client else "unknown",
            "audit_color": "🟢" if response.status_code < 400 else "🟡" if response.status_code < 500 else "🔴",
        }
        存储.记录审计日志(审计条目)
        存储.增加请求计数()

        # 在响应头中添加审计标记
        response.headers["X-CNSH-Request-DNA"] = 请求dna
        response.headers["X-CNSH-Process-Time"] = f"{处理时间:.2f}ms"
        response.headers["X-CNSH-Audit-Color"] = 审计条目["audit_color"]

        # 🛡️ P77 安全加固：CSP + 安全头部
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob:; "
            "connect-src 'self' http://localhost:* http://127.0.0.1:*; "
            "frame-ancestors 'none'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        日志记录器.info(
            f"[审计中间件] {请求dna} | {请求方法} {请求路径} | "
            f"状态: {response.status_code} | 耗时: {处理时间:.2f}ms | "
            f"审计: {审计条目['audit_color']}"
        )
        return response

    except Exception as 错误:
        处理时间 = (time.time() - 开始时间) * 1000
        日志记录器.error(f"[审计中间件] {请求dna} | 错误: {str(错误)} | 耗时: {处理时间:.2f}ms")

        # 记录错误审计
        错误审计 = {
            "request_dna": 请求dna,
            "method": 请求方法,
            "path": 请求路径,
            "status_code": 500,
            "processing_time_ms": round(处理时间, 2),
            "timestamp": datetime.now().isoformat(),
            "error": str(错误),
            "audit_color": "🔴",
        }
        存储.记录审计日志(错误审计)
        raise


# ═══════════════════════════════════════════════════════════
# 第十部分: API端点
# ═══════════════════════════════════════════════════════════


@app.post("/cnsh/write_block", response_model=CNSH_输出模型, status_code=status.HTTP_200_OK)
async def 写入块(data: CNSH_输入模型, background_tasks: BackgroundTasks):
    """
    CNSH标准写入接口

    自动流程: 切片 → GPT生成 → Claude审查 → Router裁决 → DNA生成 → 评分 → 状态判断 → 审计

    - 输入: CNSH标准JSON
    - 处理: 三AI路由系统自动处理
    - 输出: 完整的CNSH输出含DNA/分析/流转/审计
    """
    日志记录器.info(f"[写入块] 收到请求, 来源AI: {data.source_ai}, 输入长度: {len(data.input)}")

    try:
        # 阶段1: GPT生成
        gpt结果 = await 路由器.GPT_生成(data.input, data.user_id)

        # 阶段2: Claude审查
        claude结果 = await 路由器.Claude_审查(data.input, gpt结果)

        # 阶段3: Router裁决
        最终输出 = await 路由器.Router_裁决(gpt结果, claude结果, data.user_id)

        # 阶段4: 如果用户提供了自定义块，合并
        if data.blocks:
            用户块模型 = []
            for b in data.blocks:
                if not b.block_id:
                    b.block_id = f"BLK-{uuid.uuid4().hex[:8].upper()}"
                用户块模型.append(b)
            最终输出.blocks = 最终输出.blocks + 用户块模型

        # 阶段5: 如果未生成DNA则自动创建
        if not 最终输出.dna:
            所有内容 = data.input + " ".join([b.content for b in data.blocks])
            最终输出.dna = 生成DNA(所有内容, data.source_ai, data.user_id)

        # 阶段6: 后台保存到存储
        for 块 in 最终输出.blocks:
            存储.保存块(块.block_id, {
                "block_id": 块.block_id,
                "dna": 最终输出.dna,
                "content": 块.content,
                "source_ai": data.source_ai,
                "state": 最终输出.flow.next_state,
                "tags": 块.tags,
                "element": 块.element,
                "value_score": 最终输出.analysis.value_score,
                "risk_score": 最终输出.analysis.risk_score,
                "timestamp": datetime.now().isoformat(),
                "author": data.user_id,
            })

        日志记录器.info(f"[写入块] 处理完成, DNA: {最终输出.dna}, 审计: {最终输出.audit.audit_color}")
        return 最终输出

    except ValueError as ve:
        日志记录器.error(f"[写入块] 验证错误: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        日志记录器.error(f"[写入块] 处理错误: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"处理失败: {str(e)}")


@app.post("/cnsh/update_state", status_code=status.HTTP_200_OK)
async def 更新状态(数据: 状态更新模型):
    """
    状态更新接口

    更新指定块的状态，并记录变更历史。
    有效状态: IDEA / DRAFT / REVIEW / ACTIVE / FROZEN / BLOCKED
    """
    日志记录器.info(f"[更新状态] block_id: {数据.block_id}, 新状态: {数据.new_state}")

    块 = 存储.获取块(数据.block_id)
    if not 块:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"块未找到: {数据.block_id}"
        )

    原状态 = 块.get("state", "UNKNOWN")
    块["state"] = 数据.new_state
    块["state_updated_at"] = datetime.now().isoformat()
    块["state_change_reason"] = 数据.reason or "手动更新"
    存储.保存块(数据.block_id, 块)

    # 记录状态变更审计
    审计条目 = {
        "request_dna": f"STATE-{uuid.uuid4().hex[:8].upper()}",
        "method": "POST",
        "path": "/cnsh/update_state",
        "block_id": 数据.block_id,
        "old_state": 原状态,
        "new_state": 数据.new_state,
        "reason": 数据.reason,
        "timestamp": datetime.now().isoformat(),
        "audit_color": "🟢",
    }
    存储.记录审计日志(审计条目)

    return {
        "success": True,
        "block_id": 数据.block_id,
        "old_state": 原状态,
        "new_state": 数据.new_state,
        "updated_at": 块["state_updated_at"],
        "dna": 存储.获取块(数据.block_id, {}).get("dna", ""),  # type: ignore
    }


@app.get("/cnsh/query", status_code=status.HTTP_200_OK)
async def 查询(
    dna: Optional[str] = None,
    score: Optional[float] = None,
    ai_source: Optional[str] = None,
    state: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 20,
):
    """
    查询接口

    多条件查询CNSH块:
    - dna: DNA标识精确匹配
    - score: 价值评分阈值(返回大于等于此分数的块)
    - ai_source: AI来源过滤
    - state: 状态过滤
    - tag: 标签过滤
    - limit: 返回数量限制(默认20, 最大100)
    """
    日志记录器.info(f"[查询] dna={dna}, score={score}, ai_source={ai_source}, state={state}, tag={tag}, limit={limit}")

    try:
        结果列表 = 存储.查询块(
            dna=dna,
            score=score,
            ai_source=ai_source,
            state=state,
            tag=tag,
            limit=min(limit, 100),
        )

        return {
            "success": True,
            "total": len(结果列表),
            "query_params": {
                "dna": dna,
                "score": score,
                "ai_source": ai_source,
                "state": state,
                "tag": tag,
                "limit": limit,
            },
            "results": 结果列表,
        }

    except Exception as e:
        日志记录器.error(f"[查询] 错误: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"查询失败: {str(e)}")


@app.post("/cnsh/audit", status_code=status.HTTP_200_OK)
async def 审计(数据: 审计请求模型):
    """
    AI审计接口

    对指定块进行深度审计:
    - bias_score: 偏见评分
    - logic_score: 逻辑评分
    - conflict_detected: 冲突检测结果
    - recommendation: AI建议

    审计深度: basic / standard / deep
    """
    日志记录器.info(f"[审计] block_id: {数据.block_id}, 深度: {数据.audit_depth}")

    块 = 存储.获取块(数据.block_id)
    if not 块:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"块未找到: {数据.block_id}"
        )

    # 根据审计深度执行不同级别的审计
    内容 = 块.get("content", "")
    深度系数 = {"basic": 0.5, "standard": 1.0, "deep": 1.5}[数据.audit_depth]

    # 模拟审计分析
    偏见分 = round(min(30 + len(内容) % 40, 80) * 深度系数, 2)
    逻辑分 = round(min(60 + len(内容) % 30, 95) * min(深度系数, 1.0), 2)
    冲突检测 = "矛盾" in 内容 or "冲突" in 内容 or hash(内容) % 11 == 0
    质量分 = round((逻辑分 * 0.6 + (100 - 偏见分) * 0.4), 2)

    if 质量分 > 75:
        建议 = "内容质量良好，建议保留"
    elif 质量分 > 50:
        建议 = "内容可接受，建议小幅修改"
    else:
        建议 = "内容存在较多问题，建议重新审查"

    审计结果 = {
        "block_id": 数据.block_id,
        "audit_depth": 数据.audit_depth,
        "bias_score": min(偏见分, 100),
        "logic_score": min(逻辑分, 100),
        "conflict_detected": 冲突检测,
        "quality_score": min(质量分, 100),
        "recommendation": 建议,
        "audited_at": datetime.now().isoformat(),
        "dna": 块.get("dna", ""),
    }

    # 记录审计日志
    审计条目 = {
        "request_dna": f"AUDIT-{uuid.uuid4().hex[:8].upper()}",
        "method": "POST",
        "path": "/cnsh/audit",
        "block_id": 数据.block_id,
        "audit_depth": 数据.audit_depth,
        "quality_score": 审计结果["quality_score"],
        "timestamp": datetime.now().isoformat(),
        "audit_color": "🟢" if 质量分 > 75 else "🟡" if 质量分 > 50 else "🔴",
    }
    存储.记录审计日志(审计条目)

    return {
        "success": True,
        "audit_result": 审计结果,
        "audit_color": 审计条目["audit_color"],
    }


@app.get("/cnsh/health", response_model=健康状态模型, status_code=status.HTTP_200_OK)
async def 健康检查():
    """
    系统健康状态检查

    返回:
    - status: 系统状态 (healthy/degraded/down)
    - version: API版本
    - uptime: 运行时间(秒)
    - total_requests: 总请求数
    - active_blocks: 活跃块数
    - audit_status: 审计系统状态
    """
    统计 = 存储.获取统计()
    状态码 = "healthy" if 统计["total_requests"] < 10000 else "degraded"

    return 健康状态模型(
        status=状态码,
        version="2.5.0",
        uptime=round(统计["uptime"], 2),
        total_requests=统计["total_requests"],
        active_blocks=统计["total_blocks"],
        audit_status="active",
    )


@app.post("/cnsh/persona_task", status_code=status.HTTP_200_OK)
async def 人格任务(数据: 人格任务模型):
    """
    多人格自治任务接口

    自动流程: 路由到对应人格 → 执行 → 冲突检测 → 融合输出

    任务类型:
    - write: 写作任务
    - review: 审查任务
    - analyze: 分析任务
    - merge: 融合任务
    - creative: 创意任务
    """
    日志记录器.info(
        f"[人格任务] 类型: {数据.task_type}, 人格: {数据.persona_list}, 优先级: {数据.priority}"
    )

    try:
        # 阶段1: 多人格并行处理
        人格结果 = {}
        for 人格 in 数据.persona_list:
            if 人格 == "GPT":
                结果 = await 路由器.GPT_生成(数据.task)
            elif 人格 == "Claude":
                空结果 = {"blocks": [], "value_score": 0, "risk_score": 0, "hallucination": 0}
                结果 = await 路由器.Claude_审查(数据.task, 空结果)
            else:
                # 其他人格使用GPT生成
                结果 = await 路由器.GPT_生成(f"[{人格}] {数据.task}")
            人格结果[人格] = 结果

        # 阶段2: 冲突检测
        冲突标记 = False
        if len(人格结果) > 1:
            评分列表 = [r.get("value_score", 0) for r in 人格结果.values()]
            if max(评分列表) - min(评分列表) > 30:
                冲突标记 = True

        # 阶段3: 融合输出
        融合块 = []
        for 人格, 结果 in 人格结果.items():
            for 块 in 结果.get("blocks", []):
                新块 = dict(块)
                新块["persona"] = 人格
                融合块.append(新块)

        # 生成融合DNA
        融合dna = 生成DNA(数据.task, f"Persona-{'-'.join(数据.persona_list)}")

        # 融合评分
        平均价值 = round(
            sum(r.get("value_score", 0) for r in 人格结果.values()) / len(人格结果), 2
        ) if 人格结果 else 0
        平均风险 = round(
            sum(r.get("risk_score", 0) for r in 人格结果.values()) / len(人格结果), 2
        ) if 人格结果 else 0

        # 审计
        审计色 = "🟢" if not 冲突标记 and 平均风险 < 40 else "🟡" if 平均风险 < 70 else "🔴"
        裁决 = "KEEP" if not 冲突标记 and 平均价值 > 70 else "MODIFY"

        # 保存结果
        for 块 in 融合块:
            块id = 块.get("block_id", f"BLK-{uuid.uuid4().hex[:8]}")
            存储.保存块(块id, {
                "block_id": 块id,
                "dna": 融合dna,
                "content": 块.get("content", ""),
                "source_ai": 块.get("persona", "Unknown"),
                "state": "ACTIVE" if 裁决 == "KEEP" else "REVIEW",
                "tags": 块.get("tags", []) + ["persona_task", 数据.task_type],
                "value_score": 平均价值,
                "risk_score": 平均风险,
                "timestamp": datetime.now().isoformat(),
            })

        return {
            "success": True,
            "task_type": 数据.task_type,
            "persona_results": {
                人格: {
                    "blocks_count": len(结果.get("blocks", [])),
                    "value_score": 结果.get("value_score", 0),
                    "risk_score": 结果.get("risk_score", 0),
                }
                for 人格, 结果 in 人格结果.items()
            },
            "merged_output": {
                "dna": 融合dna,
                "total_blocks": len(融合块),
                "conflict_detected": 冲突标记,
                "avg_value_score": 平均价值,
                "avg_risk_score": 平均风险,
            },
            "audit": {
                "color": 审计色,
                "decision": 裁决,
                "requires_human": 冲突标记 or 平均风险 > 60,
            },
            "routing_stats": 路由器.路由统计,
        }

    except Exception as e:
        日志记录器.error(f"[人格任务] 错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"人格任务处理失败: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════
# 第十一部分: 额外工具端点
# ═══════════════════════════════════════════════════════════


@app.get("/cnsh/stats", status_code=status.HTTP_200_OK)
async def 系统统计():
    """
    系统统计信息

    返回完整的系统运行统计，包括块数量、审计日志、路由统计等。
    """
    统计 = 存储.获取统计()
    return {
        "success": True,
        "system": {
            "version": "2.5.0",
            "name": "CNSH OS API",
            "author": "UID9622 · 龍芯北辰 · 诸葛鑫",
        },
        "storage": 统计,
        "routing": 路由器.路由统计,
        "audit_logs_recent": 存储.获取审计日志(10),
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/cnsh/dna/{dna标识}", status_code=status.HTTP_200_OK)
async def DNA查询(dna标识: str):
    """
    通过DNA标识查询关联的所有块
    """
    结果 = 存储.查询块(dna=dna标识, limit=100)
    if not 结果:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DNA未找到: {dna标识}"
        )
    return {
        "success": True,
        "dna": dna标识,
        "total_blocks": len(结果),
        "blocks": 结果,
    }


# ═══════════════════════════════════════════════════════════
# 第十二部分: 启动脚本
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn

    日志记录器.info("=" * 60)
    日志记录器.info("CNSH OS API Server v2.5 启动中...")
    日志记录器.info("龍魂系统AI路由服务")
    日志记录器.info(f"启动时间: {datetime.now().isoformat()}")
    日志记录器.info(f"监听地址: 0.0.0.0:9622")
    日志记录器.info("API文档: http://localhost:9622/docs")
    日志记录器.info("=" * 60)

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=9622,
        log_level="info",
        access_log=True,
    )
