#!/usr/bin/env python3
"""
🐉 龍魂能力注册表 · 引擎内核
=============================
注册所有引擎可调用的能力（技能/功能）。
每个能力 = 名称 + 意图词 + 执行函数 + 所需人格。

DNA: #龍芯⚡️丙午·乙未·甲子·申时·需-REGISTRY-v1.0
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import subprocess
import sys
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Capability:
    """一个能力定义"""
    name: str                              # 能力名（如 "system-status"）
    display_name: str                      # 显示名（如 "系统状态"）
    description: str                       # 描述
    intent_patterns: List[str] = field(default_factory=list)  # 意图匹配正则
    persona: str = ""                      # 默认人格
    keywords: List[str] = field(default_factory=list)  # 中文关键词
    examples: List[str] = field(default_factory=list)   # 示例问法
    is_dangerous: bool = False             # 是否需要一票否决
    timeout: int = 15                      # 超时秒数


class CapabilityRegistry:
    """能力注册表 — 引擎的能力清单"""
    
    def __init__(self):
        self._capabilities: Dict[str, Capability] = {}
        self._pattern_index: List[tuple[re.Pattern[str], str, int]] = []  # (regex, cap_name, priority)
        self._register_all()
    
    def _register_all(self):
        """注册所有内置能力"""
        
        # ── 人格查询 ──
        self.register(Capability(
            name="persona-query",
            display_name="人格查询",
            description="查询龍魂人格内阁状态、排行、健康度",
            intent_patterns=[
                r'^人格', r'人格\s*(P\d+|top\d+|健康度|总览|全部)',
                r'(诸葛亮|诸葛|老子|孔子|孙子|曾仕强|王阳明|韩非|墨子)',
            ],
            persona="P05",
            keywords=["人格", "persona", "内阁", "谁最强", "排行"],
            examples=["人格 P01", "人格 top5", "人格 健康度", "人格 诸葛亮"],
        ))
        
        # ── 系统状态 ──
        self.register(Capability(
            name="system-status",
            display_name="系统状态",
            description="查看龍魂系统运行状态（分支、磁盘、内存、服务）",
            intent_patterns=[
                r'^(状态|系统)$', r'系统状态', r'(怎么样|还好吗|活着没)',
            ],
            persona="P02",
            keywords=["状态", "系统", "运行", "磁盘", "内存", "服务"],
            examples=["系统状态", "怎么样", "还好吗"],
        ))
        
        # ── 安全审计 ──
        self.register(Capability(
            name="security-audit",
            display_name="安全审计",
            description="扫描代码安全、漏洞检测、CVE查询",
            intent_patterns=[
                r'(审计|安全检查|扫一下|漏洞|安全扫描|巡逻)',
            ],
            persona="P77",
            keywords=["审计", "安全", "漏洞", "扫描", "巡逻"],
            examples=["安全检查", "审计一下", "扫一下漏洞"],
            is_dangerous=False,
            timeout=30,
        ))
        
        # ── 五行数字根 ──
        self.register(Capability(
            name="wuxing-calc",
            display_name="五行数字根",
            description="计算任意数字的数字根和五行属性",
            intent_patterns=[
                r'(算一下|数字根|属什么|五行|属性)',
            ],
            persona="P06",
            keywords=["算", "数字根", "五行", "属性", "属什么"],
            examples=["算一下 123", "369属什么", "这什么属性"],
        ))
        
        # ── 路由查找 ──
        self.register(Capability(
            name="route-find",
            display_name="路由查找",
            description="查找IPA/GATE/LOCAL节点的当前地址和状态",
            intent_patterns=[
                r'(在哪|路由|节点|查.*IPA|查.*GATE)',
            ],
            persona="P13",
            keywords=["路由", "节点", "在哪", "IPA", "GATE"],
            examples=["节点在哪 IPA-001", "查路由 GATE-003"],
        ))
        
        # ── DNA追溯 ──
        self.register(Capability(
            name="dna-lookup",
            display_name="DNA追溯",
            description="验证和查找DNA追溯码的来源和历史",
            intent_patterns=[
                r'(DNA\b|追溯码|查DNA|验证DNA|溯源)',
            ],
            persona="P05",
            keywords=["DNA", "追溯", "溯源", "编码"],
            examples=["查DNA", "验证DNA", "溯源一下"],
        ))
        
        # ── 道德经 ──
        self.register(Capability(
            name="daodejing",
            display_name="道德经查询",
            description="查询道德经章节原文及龍魂转译",
            intent_patterns=[
                r'(道德经|第[一二三四五六七八九十\d]+章|上善若水|无为|知足|反者道之动|柔弱)',
            ],
            persona="P05",
            keywords=["道德经", "老子", "道", "无为", "上善若水"],
            examples=["道德经第一章", "上善若水", "无为是什么意思"],
        ))
        
        # ── 协同场 ──
        self.register(Capability(
            name="collab-field",
            display_name="流场协同",
            description="查看人格内阁协同场状态、均衡、冲突、分工",
            intent_patterns=[
                r'(协同场|流场协同|协同状态|看看协同)',
                r'(均衡|五行均衡|缺什么)',
                r'(冲突|相克|有没有冲突)',
                r'(融合|融合指数)',
                r'(分工|任务分配|谁干什么)',
            ],
            persona="P13",
            keywords=["协同", "流场", "均衡", "冲突", "分工", "融合"],
            examples=["看看协同场", "均衡吗", "怎么分工", "有没有冲突"],
        ))
        
        # ── 一票否决查询 ──
        self.register(Capability(
            name="veto-query",
            display_name="熔断查询",
            description="查询熔断规则、申诉入口",
            intent_patterns=[
                r'(熔断|一票否决|申诉|凭什么拒绝|我不服)',
            ],
            persona="P05",
            keywords=["熔断", "否决", "申诉", "拒绝"],
            examples=["为什么被熔断了", "申诉", "熔断规则"],
            is_dangerous=True,
        ))
        
        # ── 贡献值评估 ──
        self.register(Capability(
            name="contrib-eval",
            display_name="贡献值评估",
            description="按公式 C=R·I·T^(-α) 评估规则/内容贡献值",
            intent_patterns=[
                r'(贡献值|该留|该删|留还是删|值不值得|还顶用吗|升级|降级)',
            ],
            persona="P01",
            keywords=["贡献", "值得", "过期", "升级", "降级"],
            examples=["这个还顶用吗", "该升级还是降级", "贡献值多少"],
        ))
        
        # ── 语音生成 (TTS) ──
        self.register(Capability(
            name="tts-generate",
            display_name="语音生成",
            description="文本转语音·DNA音色克隆·本地TTS推理",
            intent_patterns=[
                r'(念出来|读一下|朗读|生成语音|TTS|文字转语音|说句话)',
            ],
            persona="P04",
            keywords=["念", "读", "朗读", "语音", "TTS", "说话", "讲"],
            examples=["念出来 你好世界", "生成语音", "朗读这段"],
        ))

        # ── 语音识别 (ASR) ──
        self.register(Capability(
            name="asr-transcribe",
            display_name="语音识别",
            description="语音转文字·流式识别·说话人分离",
            intent_patterns=[
                r'(转文字|听写|识别语音|ASR|语音转文字|听听这|转录)',
            ],
            persona="P04",
            keywords=["转文字", "听写", "识别", "ASR", "转录"],
            examples=["转文字 录音.wav", "听写这段音频"],
        ))

        # ── 语音克隆 ──
        self.register(Capability(
            name="voice-clone",
            display_name="语音克隆",
            description="3秒样本克隆音色·需#CONFIRM授权·严格审计",
            intent_patterns=[
                r'(克隆.*音|音色.*克隆|模仿.*声音|复刻.*声音|声纹)',
            ],
            persona="P05",
            keywords=["克隆", "音色", "模仿声音", "复刻", "声纹"],
            examples=["克隆音色", "模仿这个声音说..."],
            is_dangerous=True,
        ))

        # ── 视频生成 ──
        self.register(Capability(
            name="video-generate",
            display_name="视频生成",
            description="文生视频/图生视频·DNA水印嵌入·本地推理",
            intent_patterns=[
                r'(生成视频|做个视频|文生视频|图生视频|视频生成)',
            ],
            persona="P04",
            keywords=["视频", "生成视频", "文生视频", "图生视频"],
            examples=["生成视频 日落海滩", "做个视频"],
        ))

        # ── 视频分析 ──
        self.register(Capability(
            name="video-analyze",
            display_name="视频分析",
            description="视频内容分析·场景检测·目标追踪·OCR·摘要",
            intent_patterns=[
                r'(分析.*视频|视频.*分析|看看.*视频|视频.*有什么)',
            ],
            persona="P04",
            keywords=["分析视频", "视频分析", "看看视频"],
            examples=["分析这个视频", "视频里有什么"],
        ))

        # ── 视频DNA嵌入 ──
        self.register(Capability(
            name="video-dna-embed",
            display_name="视频DNA嵌入",
            description="帧级DNA追溯码嵌入·DCT水印·哈希链验证",
            intent_patterns=[
                r'(嵌入DNA|打水印|DNA水印|追溯.*视频|视频.*追溯)',
            ],
            persona="P05",
            keywords=["DNA嵌入", "水印", "追溯视频"],
            examples=["给视频嵌入DNA", "打上DNA水印"],
        ))

        # ── 实时语音对话 ──
        self.register(Capability(
            name="voice-chat",
            display_name="语音对话",
            description="实时语音对话·ASR→LLM→TTS·流式pipeline",
            intent_patterns=[
                r'(语音对话|跟我聊|语音聊天|说话聊天|开始对话)',
            ],
            persona="P04",
            keywords=["语音对话", "聊天", "对话", "说话"],
            examples=["开始语音对话", "跟我聊聊"],
        ))

        # ── CNSH多语言编译 ──
        self.register(Capability(
            name="cnsh-compile",
            display_name="CNSH多语言编译",
            description="CNSH代码编译·8语言(中/柬/俄/阿/波/泰/葡/越)→Python·骨架保留表皮全换",
            intent_patterns=[
                r'(编译|CNSH|翻译.*代码|cnsh|compile)',
            ],
            persona="P04",
            keywords=["编译", "CNSH", "翻译代码", "cnsh", "compile", "多语言"],
            examples=["编译这段CNSH代码", "翻译代码到Python", "cnsh compile"],
        ))

        # ── 全球搜索 ──
        self.register(Capability(
            name="global-search",
            display_name="全球全量搜索",
            description="5人格×4国产节点·布隆快筛+BM25+向量·通心译联动·三色审计·前缀补全",
            intent_patterns=[
                r'(搜索|查找|检索|search|find|全网|全球)',
            ],
            persona="P01",
            keywords=["搜索", "查找", "检索", "search", "全网", "全球", "索引"],
            examples=["搜索 算法", "全网查找 龍魂", "检索 主权"],
        ))

        # ── CNSH终端运行 ──
        self.register(Capability(
            name="cnsh-run",
            display_name="CNSH终端执行",
            description="CNSH代码一键运行·自动检测语言→编译→签名验证→执行→审计日志",
            intent_patterns=[
                r'(运行|run|执行|跑一下|cnsh.*run)',
            ],
            persona="P04",
            keywords=["运行", "run", "执行", "跑", "CNSH"],
            examples=["运行 test.cnsh", "执行CNSH代码"],
        ))

        # ── 镜像视界 ──
        self.register(Capability(
            name="mirror-vision",
            display_name="镜像视界",
            description="零断点跨镜接力·全域动态目标智控·蚁群协同追踪",
            intent_patterns=[
                r'(镜像|视界|跨镜|接力|蚁群|目标追踪|摄像头|监控|mirror.?vision)',
            ],
            persona="P01",
            keywords=["镜像视界", "跨镜", "接力", "蚁群", "目标追踪", "摄像头", "监控"],
            examples=["镜像视界状态", "蚁群视觉", "跨镜接力", "目标追踪"],
        ))

        # ── 时空织网 ──
        self.register(Capability(
            name="spacetime-weave",
            display_name="时空织网",
            description="AI驱动时空织网·无痕续迹·主动安全新范式·ST-GNN预测",
            intent_patterns=[
                r'(时空织网|织网|无痕续迹|主动安全|spacetime.?weave|时空连续|续迹)',
            ],
            persona="P05",
            keywords=["时空织网", "织网", "无痕续迹", "主动安全", "ST-GNN", "跨镜", "预测"],
            examples=["时空织网状态", "无痕续迹演示", "主动安全检测"],
        ))

        # ── 帮助 ──
        self.register(Capability(
            name="help",
            display_name="帮助",
            description="显示所有可用能力",
            intent_patterns=[
                r'^(帮助|help|怎么用|能干什么|功能|菜单|命令)$',
            ],
            persona="P02",
            keywords=["帮助", "help", "怎么用", "功能", "菜单"],
            examples=["帮助", "怎么用", "能干什么"],
        ))
    
    def register(self, cap: Capability):
        """注册一个能力"""
        self._capabilities[cap.name] = cap
        # 建意图索引
        for pattern in cap.intent_patterns:
            self._pattern_index.append((
                re.compile(pattern, re.IGNORECASE),
                cap.name,
                0  # 默认优先级，后面可以设
            ))
    
    def match(self, text: str) -> Optional[Capability]:
        """根据用户输入匹配能力"""
        text = text.strip()
        if not text:
            return None
        
        # 按模式匹配
        for regex, cap_name, _ in self._pattern_index:
            if regex.search(text):
                return self._capabilities.get(cap_name)
        
        # 按关键词匹配
        best_match = None
        best_score = 0
        for cap in self._capabilities.values():
            for kw in cap.keywords:
                if kw in text:
                    score = len(kw)  # 越长越精确
                    if score > best_score:
                        best_score = score
                        best_match = cap
        
        return best_match
    
    def get(self, name: str) -> Optional[Capability]:
        """按名称获取能力"""
        return self._capabilities.get(name)
    
    def list_all(self) -> List[Capability]:
        """列出所有能力"""
        return list(self._capabilities.values())
    
    def get_help_text(self) -> str:
        """生成帮助文本"""
        lines = ["🐉 我能帮你查这些:\n"]
        for cap in self._capabilities.values():
            if cap.name == "help":
                continue
            emoji = "🔴" if cap.is_dangerous else "📋"
            lines.append(f"{emoji} **{cap.display_name}** — {cap.description}")
            if cap.examples:
                lines.append(f"   💬 {' / '.join(cap.examples[:3])}")
        return "\n".join(lines)
