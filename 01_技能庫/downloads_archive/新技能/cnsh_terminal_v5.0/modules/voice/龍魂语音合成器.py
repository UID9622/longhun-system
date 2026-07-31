# DNA: #龍芯⚡️丙午·乙未·乙丑·大有-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-龍魂语音合成器-v1.0-4e967ab6
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  DNA追溯头（不可删除 · 删除即断链）                                       ║
# ║  DNA Trace Header (DO NOT DELETE · deletion breaks the chain)            ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
# 龍芯⚡️2026-06-18-LONGHUN-TTS-ENGINE-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创始人: UID9622 · 龍芯北辰 · 诸葛鑫
# Founder: UID9622 · LongHun Beichen · Zhuge Xin

"""
龍魂语音合成器 —— 文字转语音(TTS)核心引擎
LongHun Speech Synthesizer —— Text-To-Speech Core Engine

底层使用edge-tts（微软Edge浏览器免费的在线TTS服务），
支持中文、英文、日文等多种语言的高质量语音合成。
也支持pyttsx3作为离线备份方案，确保在无网络环境可用。

全部用中文封装，核心逻辑注释用中文。
All encapsulation is in Chinese; core logic comments in Chinese.

工作流程（中文详细描述 · Detailed workflow in Chinese）：
第一步：文本预处理——分句、特殊字符处理、长度检查
第二步：语音角色选择——根据语言和内容选择最合适的声音
第三步：在线合成——优先使用edge-tts（质量高、自然度好）
第四步：离线降级——网络不可用则使用pyttsx3
第五步：音频后处理——音量调整、格式转换、元数据添加
第六步：审计盖章——DNA追溯、三色审计确认
"""

import os
import sys
import hashlib
import wave
import asyncio
import tempfile
import subprocess
import warnings
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# 压制不必要的警告 · Suppress unnecessary warnings
warnings.filterwarnings("ignore", category=UserWarning)


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  三色审计系统 · Three-Color Audit System                                 ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

class 审计颜色(Enum):
    """三色审计标签 · Three-color audit labels"""
    绿色通过 = "🟢"   # 质量优秀 · Excellent quality
    黄色警告 = "🟡"   # 需要注意 · Needs attention
    红色阻断 = "🔴"   # 严重问题 · Critical issue


@dataclass
class 审计结果:
    """审计结果数据结构 · Audit result data structure"""
    颜色: 审计颜色
    置信度: float
    原因: str
    建议: str


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  六层来源链 · Six-Layer Provenance Chain                                 ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

class 六层来源链:
    """
    六层来源链——确保每一个产出物都可追溯到源头
    Six-Layer Provenance Chain — ensures every output is traceable to its origin
    """
    六层 = {
        "道统层": "UID9622创始人架构——语音合成的顶层设计理念 · Founder UID9622's architectural vision",
        "精神层": "龍魂文化主权理念——用中文代码守护语音技术主权 · LongHun cultural sovereignty through Chinese code",
        "设备层": "本地计算环境——语音合成依赖本地音频硬件与网络 · Local computing with audio hardware and network",
        "技术层": "Python3.10+ · edge-tts · pyttsx3——底层技术栈 · Python3.10+ · edge-tts · pyttsx3 tech stack",
        "系统层": "龍魂多模态输出系统·语音合成模块——本模块的功能定位 · LongHun multimodal output system · TTS module",
        "生命层": "诸葛鑫真人签名——每个产出物都有UID9622真人确认 · Zhuge Xin's personal signature on every output"
    }
    DNA = "#龍芯⚡️2026-06-18-LONGHUN-TTS-ENGINE-v1.0"

    @classmethod
    def 盖章(cls, 模块路径: str = "") -> Dict[str, Any]:
        """为模块产出物盖上六层来源链印章 · Stamp the output with six-layer provenance"""
        return {
            "六层来源链": dict(cls.六层),
            "DNA追溯码": cls.DNA,
            "模块路径": 模块路径,
            "铁律": "来源不可删 · 影响不可覆 · 贡献不可抹",
            "盖章时间": datetime.now().isoformat()
        }


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  铁律自审闸 · Iron-Rule Self-Audit Gate                                  ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

class 铁律自审闸:
    """
    铁律自审闸——自动审查代码与输出中的违规项
    Iron-Rule Self-Audit Gate — automatically reviews code and output for violations

    核心铁律：繁体「龍」字永存，不可简化为「龙」
    Core rule: Traditional 「龍」 must never be simplified to 「龙」
    """

    铁律列表 = [
        "繁体『龍』字永存，不可简化为『龙』",
        "DNA追溯头不可删除",
        "六层来源链不可覆写",
        "创始人UID9622贡献不可抹除"
    ]

    @staticmethod
    def 审查(文本: str) -> Dict[str, Any]:
        """审查文本是否违反铁律 · Review text for rule violations"""
        违规项 = []

        # 铁律第一条：龍字检查
        if "龙" in 文本 and "龍" not in 文本:
            违规项.append("🔴 违规：繁体『龍』被简化为『龙』· Traditional 「龍」 simplified to 「龙」")
        elif "龙" in 文本 and "龍" in 文本:
            违规项.append("🟡 警告：文中同时存在『龍』和『龙』，请统一为繁体『龍』")

        # 铁律第二条：DNA头检查
        if "龍芯" in 文本 and "DNA" not in 文本 and "追溯" not in 文本:
            违规项.append("🟡 警告：提到龍芯但未包含DNA追溯信息")

        # 铁律第三条：文本内容安全检查
        if len(文本) > 5000:
            违规项.append("🟡 警告：文本过长（>5000字符），可能影响合成质量")

        return {"通过": len(违规项) == 0, "违规项": 违规项}

    @classmethod
    def 获取铁律(cls) -> List[str]:
        """获取全部铁律 · Get all iron rules"""
        return list(cls.铁律列表)


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  数据结构定义 · Data Structure Definitions                               ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

@dataclass
class 语音合成结果:
    """
    文字转语音的结果封装 · Text-to-speech result encapsulation

    这个数据结构封装了语音合成的全部输出信息，
    包括输出路径、文本、语速、音调、语音角色等。
    """
    音频路径: str                      # 输出音频文件路径 · Output audio file path
    文本: str                          # 合成原文本 · Original text
    语速: float                        # 语速倍率 · Speed multiplier
    音调: float                        # 音调偏移(Hz) · Pitch offset in Hz
    语音角色: str                      # 语音角色名称 · Voice role name
    音频时长: float                    # 音频总时长(秒) · Audio duration in seconds
    采样率: int                        # 音频采样率 · Audio sample rate
    处理时长: float                    # 处理耗时(秒) · Processing time in seconds
    合成引擎: str                      # 使用的引擎 · Engine used
    DNA追溯: str                       # DNA追溯码 · DNA trace code
    审计日志: List[审计结果] = field(default_factory=list)  # 审计记录 · Audit log
    来源链盖章: Dict[str, Any] = field(default_factory=dict)          # 来源链印章 · Provenance stamp

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式 · Convert to dictionary format"""
        return {
            "音频路径": self.音频路径,
            "文本长度": len(self.文本),
            "语速": self.语速,
            "音调": self.音调,
            "语音角色": self.语音角色,
            "音频时长_秒": round(self.音频时长, 2),
            "采样率": self.采样率,
            "处理时长_秒": round(self.处理时长, 2),
            "合成引擎": self.合成引擎,
            "DNA追溯": self.DNA追溯
        }

    def __repr__(self) -> str:
        return f"<语音合成结果 角色='{self.语音角色}' 时长={self.音频时长:.1f}s 引擎={self.合成引擎}>"


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  语音角色管理器 · Voice Role Manager                                     ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

class 语音角色管理器:
    """
    语音角色管理器——管理可用的语音角色
    Voice Role Manager — manages available voice roles

    edge-tts 支持的语音角色列表，按语言分类。
    中文角色默认优先。
    """

    # 中文语音角色（edge-tts）· Chinese voice roles
    中文角色 = {
        "xiaoxiao": {
            "名称": "zh-CN-XiaoxiaoNeural",
            "描述": "中文女声——温暖自然，适合日常对话",
            "性别": "女",
            "语言": "zh-CN",
            "推荐场景": ["日常对话", "客服", "朗读"]
        },
        "xiaoyi": {
            "名称": "zh-CN-XiaoyiNeural",
            "描述": "中文男声——沉稳清晰，适合新闻播报",
            "性别": "男",
            "语言": "zh-CN",
            "推荐场景": ["新闻播报", "导航", "有声书"]
        },
        "xiaohan": {
            "名称": "zh-CN-XiaohanNeural",
            "描述": "中文女声——温柔细腻，适合情感内容",
            "性别": "女",
            "语言": "zh-CN",
            "推荐场景": ["情感朗读", "故事讲述", "诗歌"]
        },
        "xiaomeng": {
            "名称": "zh-CN-XiaomengNeural",
            "描述": "中文女声——活泼轻快，适合年轻化内容",
            "性别": "女",
            "语言": "zh-CN",
            "推荐场景": ["年轻化内容", "广告", "动画配音"]
        },
        "xiaorui": {
            "名称": "zh-CN-XiaoruiNeural",
            "描述": "中文男声——磁性深沉，适合纪录片",
            "性别": "男",
            "语言": "zh-CN",
            "推荐场景": ["纪录片", "深度内容", "广播"]
        },
        "yunxi": {
            "名称": "zh-CN-YunxiNeural",
            "描述": "中文男声——亲和力强，适合教育内容",
            "性别": "男",
            "语言": "zh-CN",
            "推荐场景": ["教育", "培训", "讲解"]
        },
        "yunjian": {
            "名称": "zh-CN-YunjianNeural",
            "描述": "中文男声——运动活力风格",
            "性别": "男",
            "语言": "zh-CN",
            "推荐场景": ["体育解说", "运动激励", "游戏"]
        },
        "xiaoxiaonian": {
            "名称": "zh-CN-XiaoxiaoNeural (多情感)",
            "描述": "中文女声——支持多情感表达",
            "性别": "女",
            "语言": "zh-CN",
            "推荐场景": ["情感表达", "角色扮演", "戏剧"]
        },
    }

    # 粤语角色 · Cantonese roles
    粤语角色 = {
        "hiugaai": {
            "名称": "zh-HK-HiuGaaiNeural",
            "描述": "粤语女声——标准港式粤语",
            "性别": "女",
            "语言": "zh-HK",
            "推荐场景": ["粤语对话", "港式内容"]
        },
        "hiumaan": {
            "名称": "zh-HK-HiuMaanNeural",
            "描述": "粤语男声——标准港式粤语",
            "性别": "男",
            "语言": "zh-HK",
            "推荐场景": ["粤语对话", "港式内容"]
        },
    }

    # 英语角色 · English roles
    英语角色 = {
        "jenny": {
            "名称": "en-US-JennyNeural",
            "描述": "英语女声——标准美式发音",
            "性别": "女",
            "语言": "en-US",
            "推荐场景": ["美式英语", "日常对话", "商务"]
        },
        "guy": {
            "名称": "en-US-GuyNeural",
            "描述": "英语男声——标准美式发音",
            "性别": "男",
            "语言": "en-US",
            "推荐场景": ["美式英语", "新闻", "播报"]
        },
        "sonia": {
            "名称": "en-GB-SoniaNeural",
            "描述": "英语女声——标准英式发音",
            "性别": "女",
            "语言": "en-GB",
            "推荐场景": ["英式英语", "正式场合"]
        },
    }

    # 日语角色 · Japanese roles
    日语角色 = {
        "nanami": {
            "名称": "ja-JP-NanamiNeural",
            "描述": "日语女声——自然清晰",
            "性别": "女",
            "语言": "ja-JP",
            "推荐场景": ["日语对话", "动漫风格"]
        },
    }

    # 韩语角色 · Korean roles
    韩语角色 = {
        "sunhi": {
            "名称": "ko-KR-SunHiNeural",
            "描述": "韩语女声——标准首尔口音",
            "性别": "女",
            "语言": "ko-KR",
            "推荐场景": ["韩语对话", "韩流内容"]
        },
    }

    @classmethod
    def 获取全部角色(cls) -> Dict[str, Dict]:
        """获取全部可用角色 · Get all available roles"""
        全部 = {}
        全部.update(cls.中文角色)
        全部.update(cls.粤语角色)
        全部.update(cls.英语角色)
        全部.update(cls.日语角色)
        全部.update(cls.韩语角色)
        return 全部

    @classmethod
    def 按语言获取角色(cls, 语言: str) -> Dict[str, Dict]:
        """
        按语言获取角色 · Get roles by language

        参数 · Parameters:
            语言: 语言代码 (zh/zh-CN/zh-HK/en/en-US/ja/ko)
        """
        映射 = {
            "zh": cls.中文角色,
            "zh-CN": cls.中文角色,
            "zh-cn": cls.中文角色,
            "zh-HK": cls.粤语角色,
            "zh-hk": cls.粤语角色,
            "yue": cls.粤语角色,
            "en": cls.英语角色,
            "en-US": cls.英语角色,
            "en-us": cls.英语角色,
            "en-GB": cls.英语角色,
            "ja": cls.日语角色,
            "ja-JP": cls.日语角色,
            "ko": cls.韩语角色,
            "ko-KR": cls.韩语角色,
        }
        return 映射.get(语言, cls.中文角色)

    @classmethod
    def 获取角色名称(cls, 角色代码: str) -> str:
        """获取角色的完整edge-tts名称 · Get full edge-tts name for a role"""
        全部 = cls.获取全部角色()
        角色信息 = 全部.get(角色代码, cls.中文角色["xiaoxiao"])
        return 角色信息["名称"]

    @classmethod
    def 列出角色(cls, 语言: Optional[str] = None) -> None:
        """打印角色列表 · Print list of roles"""
        print("\n" + "=" * 60)
        if 语言:
            print(f"  语音角色列表 · {语言}")
            角色字典 = cls.按语言获取角色(语言)
        else:
            print("  全部语音角色列表 · All voice roles")
            角色字典 = cls.获取全部角色()
        print("=" * 60)
        for 代码, 信息 in 角色字典.items():
            print(f"\n  [{代码}]")
            print(f"    名称: {信息['名称']}")
            print(f"    描述: {信息['描述']}")
            print(f"    性别: {信息['性别']} | 语言: {信息['语言']}")
            print(f"    场景: {', '.join(信息['推荐场景'])}")
        print("=" * 60)


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  龍魂语音合成器核心类 · LongHun Speech Synthesizer Core Class            ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

class 龍魂语音合成器:
    """
    龍魂语音合成器 —— 文字转语音(TTS)核心引擎
    LongHun Speech Synthesizer —— Text-To-Speech Core Engine

    【核心设计理念 · Core Design Philosophy】
    底层使用edge-tts（微软Edge浏览器免费的在线TTS服务），
    支持中文、英文、日文等多种语言的高质量语音合成。
    也支持pyttsx3作为离线备份方案，确保在无网络环境可用。

    全部用中文封装，核心逻辑注释用中文。
    All encapsulation in Chinese; core logic comments in Chinese.

    【支持的语音引擎 · Supported TTS Engines】
    - edge-tts: 在线引擎，质量最高，需要网络连接
                  Online engine, highest quality, requires internet
    - pyttsx3:  离线引擎，质量一般，不依赖网络
                  Offline engine, moderate quality, no internet needed
    - espeak:   备用离线引擎，支持多语言
                  Backup offline engine, multi-language support

    【工作流程 · Workflow】
    第一步：文本预处理——分句、特殊字符处理、长度检查
    第二步：语音角色选择——根据语言和内容选择最合适的声音
    第三步：在线合成——优先使用edge-tts（质量高、自然度好）
    第四步：离线降级——网络不可用则使用pyttsx3
    第五步：音频后处理——音量调整、格式转换、元数据添加
    第六步：审计盖章——DNA追溯、三色审计确认
    """

    def __init__(
        self,
        语音角色: str = "xiaoxiao",
        启用审计: bool = True,
        输出目录: Optional[str] = None
    ):
        """
        初始化语音合成器 · Initialize the speech synthesizer

        参数 · Parameters:
            语音角色: 角色代码或完整edge-tts名称
            启用审计: 是否开启三色审计系统
            输出目录: 音频输出目录
        """
        self.角色管理器 = 语音角色管理器()
        self.语音角色代码 = 语音角色

        # 解析角色名称（支持代码和完整名称）
        if "Neural" in 语音角色:
            self.语音角色 = 语音角色  # 完整名称
        else:
            self.语音角色 = self.角色管理器.获取角色名称(语音角色)

        self.审计开关 = 启用审计
        self.输出目录 = 输出目录 or os.path.expanduser("~/龍魂语音输出")
        os.makedirs(self.输出目录, exist_ok=True)

        self.审计日志: List[审计结果] = []
        self.来源链 = 六层来源链()
        self.铁律闸 = 铁律自审闸()

        # 默认参数
        self.语速 = 1.0     # 正常语速
        self.音调 = 0.0     # Hz，0=默认音调
        self.音量 = 0.0     # dB，0=默认音量

        # 离线引擎缓存
        self._离线引擎 = None

        self._记录审计(
            f"龍魂语音合成器初始化 | 角色={self.语音角色} | 输出目录={self.输出目录}",
            1.0,
            审计颜色.绿色通过
        )

    # ═══════════════════════════════════════════════════════════════════════
    #  核心API：文字转语音 · Core API: Text-to-Speech
    # ═══════════════════════════════════════════════════════════════════════

    async def 文字转语音(
        self,
        文本: str,
        输出路径: Optional[str] = None,
        语速: Optional[float] = None,
        音调: Optional[float] = None,
        语音角色: Optional[str] = None,
        音量: Optional[float] = None
    ) -> 语音合成结果:
        """
        核心方法：将文字转换为语音（异步） · Core method: Convert text to speech (async)

        参数 · Parameters:
            文本: 要合成的文字内容
            输出路径: 输出音频文件路径（默认自动生成）
            语速: 语速倍率 (0.5=慢速, 1.0=正常, 2.0=快速)
            音调: 音调偏移 (Hz, 正值升高，负值降低)
            语音角色: 临时指定语音角色（覆盖默认）
            音量: 音量调整 (dB, 正值增大，负值减小)

        返回 · Returns:
            语音合成结果对象
        """
        import time
        开始时间 = time.time()

        # 参数处理
        语速 = 语速 if 语速 is not None else self.语速
        音调 = 音调 if 音调 is not None else self.音调
        音量 = 音量 if 音量 is not None else self.音量
        使用角色 = 语音角色 or self.语音角色

        # 解析角色
        if 使用角色 and "Neural" not in 使用角色:
            使用角色 = self.角色管理器.获取角色名称(使用角色)

        # ═══════════════════════════════════════════════
        # 阶段零：铁律审查与文本预处理
        # ═══════════════════════════════════════════════
        审查结果 = self.铁律闸.审查(文本)
        if not 审查结果["通过"]:
            for 违规 in 审查结果["违规项"]:
                self._记录审计(f"铁律审查: {违规}", 0.3, 审计颜色.黄色警告)

        # 文本预处理
        处理后文本 = self._预处理文本(文本)

        # 生成输出路径
        if 输出路径 is None:
            时间戳 = datetime.now().strftime('%Y%m%d_%H%M%S')
            文本哈希 = hashlib.md5(文本.encode()).hexdigest()[:6]
            输出路径 = os.path.join(
                self.输出目录,
                f"龍魂语音_{时间戳}_{文本哈希}.mp3"
            )

        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(输出路径)), exist_ok=True)

        # ═══════════════════════════════════════════════
        # 阶段一：语音合成 · Speech synthesis
        # ═══════════════════════════════════════════════
        引擎 = ""
        合成成功 = False

        # 策略一：edge-tts（在线，质量最高）
        try:
            self._记录审计(f"尝试在线合成: {使用角色}...", 0.8)
            await self._在线合成(处理后文本, 输出路径, 使用角色, 语速, 音调, 音量)
            引擎 = f"edge-tts-{使用角色}"
            合成成功 = True
            self._记录审计(f"✅ 在线语音合成成功: {使用角色}", 0.95, 审计颜色.绿色通过)
        except Exception as e:
            self._记录审计(
                f"edge-tts失败: {str(e)[:100]}，降级到离线引擎",
                0.4,
                审计颜色.黄色警告
            )

        # 策略二：pyttsx3（离线，本地运行）
        if not 合成成功:
            try:
                self._记录审计("尝试离线合成: pyttsx3...", 0.6)
                self._离线合成(处理后文本, 输出路径, 语速)
                引擎 = "pyttsx3-offline"
                合成成功 = True
                self._记录审计("✅ 离线语音合成成功 (pyttsx3)", 0.80, 审计颜色.绿色通过)
            except Exception as e:
                self._记录审计(
                    f"pyttsx3失败: {str(e)[:100]}",
                    0.2,
                    审计颜色.黄色警告
                )

        # 策略三：espeak（备用离线）
        if not 合成成功:
            try:
                self._记录审计("尝试备用离线合成: espeak...", 0.5)
                self._备用离线合成(处理后文本, 输出路径)
                引擎 = "espeak-ng"
                合成成功 = True
                self._记录审计("✅ 备用离线合成成功 (espeak)", 0.70, 审计颜色.绿色通过)
            except Exception as e:
                self._记录审计(
                    f"espeak也失败: {str(e)[:100]}",
                    0.0,
                    审计颜色.红色阻断
                )

        if not 合成成功:
            raise RuntimeError(
                "所有语音合成引擎均不可用 · All TTS engines unavailable\n"
                "请安装: pip install edge-tts pyttsx3\n"
                "或安装系统包: sudo apt-get install espeak-ng"
            )

        # ═══════════════════════════════════════════════
        # 阶段二：音频信息获取
        # ═══════════════════════════════════════════════
        音频时长 = self._获取音频时长(输出路径)
        采样率 = self._获取采样率(输出路径) or 24000

        # ═══════════════════════════════════════════════
        # 阶段三：组装结果
        # ═══════════════════════════════════════════════
        结束时间 = time.time()
        处理耗时 = 结束时间 - 开始时间

        # DNA追溯码
        文本哈希 = hashlib.md5(文本.encode()).hexdigest()[:8]
        DNA戳 = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-TTS-{文本哈希}"

        # 来源链盖章
        来源印章 = self.来源链.盖章(f"龍魂语音合成器/文字转语音/{os.path.basename(输出路径)}")

        # 判断角色性别
        角色性别 = "女声"
        if any(m in 使用角色 for m in ["Xiaoyi", "Yunxi", "Yunjian", "Xiaorui", "Guy"]):
            角色性别 = "男声"
        elif "Xiaoxiao" in 使用角色 or "Xiaohan" in 使用角色 or "Xiaomeng" in 使用角色:
            角色性别 = "女声"

        # 三色审计
        if 合成成功 and 音频时长 > 0:
            self._记录审计(
                f"🟢 语音合成完成 | 时长={音频时长:.1f}s | 引擎={引擎} | RTF={处理耗时/max(音频时长,0.001):.2f}x",
                0.95,
                审计颜色.绿色通过
            )
        elif 合成成功:
            self._记录审计(
                "🟡 合成成功但无法读取音频信息",
                0.6,
                审计颜色.黄色警告
            )

        return 语音合成结果(
            音频路径=输出路径,
            文本=文本,
            语速=语速,
            音调=音调,
            语音角色=角色性别,
            音频时长=音频时长,
            采样率=采样率,
            处理时长=处理耗时,
            合成引擎=引擎,
            DNA追溯=DNA戳,
            审计日志=list(self.审计日志),
            来源链盖章=来源印章
        )

    def 文字转语音同步(
        self,
        文本: str,
        输出路径: Optional[str] = None,
        **参数
    ) -> 语音合成结果:
        """
        同步版本的文字转语音 · Synchronous text-to-speech

        对异步方法进行封装，方便在不使用async的环境中调用。
        Wraps the async method for use in non-async environments.
        """
        try:
            # 尝试获取已有事件循环
            loop = asyncio.get_running_loop()
            # 如果已在事件循环中，使用nest_asyncio或直接运行
            import nest_asyncio
            nest_asyncio.apply()
            return asyncio.get_event_loop().run_until_complete(
                self.文字转语音(文本, 输出路径, **参数)
            )
        except RuntimeError:
            # 没有事件循环，新建一个
            return asyncio.run(self.文字转语音(文本, 输出路径, **参数))
        except ImportError:
            # 没有nest_asyncio，直接运行
            return asyncio.run(self.文字转语音(文本, 输出路径, **参数))

    # ═══════════════════════════════════════════════════════════════════════
    #  合成引擎实现 · Synthesis Engine Implementations
    # ═══════════════════════════════════════════════════════════════════════

    async def _在线合成(
        self,
        文本: str,
        输出路径: str,
        角色: str,
        语速: float,
        音调: float,
        音量: float
    ) -> None:
        """
        使用edge-tts进行在线合成 · Online synthesis with edge-tts

        edge-tts参数格式：
        - rate: 百分比字符串 (+50% = 1.5x 语速)
        - pitch: Hz字符串 (+10Hz 提高音调)
        - volume: dB字符串 (+0dB = 默认音量)
        """
        import edge_tts

        # 构建参数
        语速参数 = f"{int((语速 - 1.0) * 100):+d}%"
        音调参数 = f"{int(音调):+d}Hz"
        音量参数 = f"{int(音量):+d}%"

        # 创建通信对象
        通信 = edge_tts.Communicate(
            文本,
            voice=角色,
            rate=语速参数,
            pitch=音调参数,
            volume=音量参数
        )
        await 通信.save(输出路径)

    def _离线合成(self, 文本: str, 输出路径: str, 语速: float) -> None:
        """
        使用pyttsx3进行离线合成 · Offline synthesis with pyttsx3

        pyttsx3是纯本地TTS引擎，不依赖网络。
        但音质较edge-tts差，且中文支持取决于系统语音。
        """
        import pyttsx3

        # 每次创建新引擎（线程安全）
        引擎 = pyttsx3.init()

        # 语速设置：默认200词/分钟
        引擎.setProperty('rate', int(200 * 语速))
        # 音量设置：0.0-1.0
        引擎.setProperty('volume', 0.9)

        # 保存到文件
        引擎.save_to_file(文本, 输出路径)
        引擎.runAndWait()

        # 清理
        try:
            引擎.stop()
        except:
            pass

    def _备用离线合成(self, 文本: str, 输出路径: str) -> None:
        """
        使用espeak-ng进行备用离线合成 · Backup offline synthesis with espeak-ng

        espeak-ng是跨平台的开源TTS引擎，支持100+语言。
        需要先安装: sudo apt-get install espeak-ng
        """
        # 构建espeak命令
        命令 = [
            'espeak-ng',
            '-v', 'zh',  # 中文语音
            '-s', '150',  # 语速
            '-w', 输出路径,  # 输出WAV
            文本
        ]

        # 如果输出是MP3，先输出WAV再转换
        if 输出路径.endswith('.mp3'):
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                临时wav = f.name
            命令[-2] = 临时wav
            subprocess.run(命令, check=True, capture_output=True, timeout=60)

            # 转换为MP3
            subprocess.run(
                ['ffmpeg', '-i', 临时wav, '-codec:a', 'libmp3lame', '-q:a', '2', 输出路径],
                check=True, capture_output=True, timeout=30
            )
            os.unlink(临时wav)
        else:
            subprocess.run(命令, check=True, capture_output=True, timeout=60)

    # ═══════════════════════════════════════════════════════════════════════
    #  文本预处理 · Text Preprocessing
    # ═══════════════════════════════════════════════════════════════════════

    def _预处理文本(self, 原始文本: str) -> str:
        """
        文本预处理 · Text preprocessing

        1. 去除首尾空白
        2. 统一换行符为空格
        3. 限制最大长度（edge-tts有字符限制）
        4. 处理特殊字符
        """
        import re

        文本 = 原始文本.strip()

        # 统一换行符
        文本 = 文本.replace('\r\n', ' ').replace('\n', ' ')

        # 去除多余空格
        文本 = re.sub(r'\s+', ' ', 文本)

        # 处理可能导致TTS出错的字符
        文本 = 文本.replace('\x00', '')  # 空字符
        文本 = 文本.replace('\x0b', ' ')  # 垂直制表符
        文本 = 文本.replace('\x0c', ' ')  # 换页符

        # 限制长度（edge-tts建议单次不超过3000字符）
        最大长度 = 3000
        if len(文本) > 最大长度:
            self._记录审计(
                f"文本过长({len(文本)}字符)，截断至{最大长度}字符",
                0.5,
                审计颜色.黄色警告
            )
            文本 = 文本[:最大长度]

        return 文本.strip()

    # ═══════════════════════════════════════════════════════════════════════
    #  音频工具方法 · Audio Utility Methods
    # ═══════════════════════════════════════════════════════════════════════

    def _获取音频时长(self, 音频路径: str) -> float:
        """获取音频文件时长（秒）· Get audio file duration in seconds"""
        try:
            import soundfile as sf
            信息 = sf.info(音频路径)
            return 信息.duration
        except:
            pass

        # 降级：使用wave（仅WAV）
        if 音频路径.endswith('.wav'):
            try:
                with wave.open(音频路径, 'rb') as wf:
                    帧数 = wf.getnframes()
                    采样率 = wf.getframerate()
                    return 帧数 / max(采样率, 1)
            except:
                pass

        # 降级：使用ffprobe
        try:
            结果 = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1', 音频路径],
                capture_output=True, text=True, timeout=10
            )
            return float(结果.stdout.strip())
        except:
            pass

        return 0.0

    def _获取采样率(self, 音频路径: str) -> int:
        """获取音频采样率 · Get audio sample rate"""
        try:
            import soundfile as sf
            信息 = sf.info(音频路径)
            return 信息.samplerate
        except:
            pass

        if 音频路径.endswith('.wav'):
            try:
                with wave.open(音频路径, 'rb') as wf:
                    return wf.getframerate()
            except:
                pass

        # edge-tts默认24kHz
        return 24000

    def _格式转换(self, 输入路径: str, 输出路径: str, 格式: str = "wav") -> str:
        """
        转换音频格式 · Convert audio format

        使用ffmpeg进行格式转换。
        需要先安装ffmpeg: sudo apt-get install ffmpeg
        """
        try:
            subprocess.run(
                ['ffmpeg', '-y', '-i', 输入路径, 输出路径],
                check=True, capture_output=True, timeout=30
            )
            return 输出路径
        except (subprocess.SubprocessError, FileNotFoundError):
            self._记录审计("ffmpeg不可用，无法转换格式", 0.3, 审计颜色.黄色警告)
            return 输入路径

    # ═══════════════════════════════════════════════════════════════════════
    #  批量与长文本处理 · Batch & Long Text Processing
    # ═══════════════════════════════════════════════════════════════════════

    async def 长文本合成(
        self,
        文本: str,
        输出路径: Optional[str] = None,
        分段长度: int = 500,
        **参数
    ) -> 语音合成结果:
        """
        长文本分片合成 · Long text segmented synthesis

        将长文本分割为多段分别合成，然后拼接。
        适用于超长文本（如文章、小说章节）。

        参数 · Parameters:
            文本: 长文本内容
            输出路径: 输出路径
            分段长度: 每段最大字符数
            **参数: 其他合成参数
        """
        if len(文本) <= 分段长度:
            return await self.文字转语音(文本, 输出路径, **参数)

        self._记录审计(f"长文本分片合成: 总长{len(文本)}字符, 每段{分段长度}字符", 0.8)

        # 智能分句
        段落列表 = self._智能分句(文本, 分段长度)
        self._记录审计(f"文本分为{len(段落列表)}段", 0.8)

        # 临时目录存储各段
        临时目录 = tempfile.mkdtemp(prefix="龍魂TTS_")
        段文件列表 = []

        for i, 段 in enumerate(段落列表):
            段路径 = os.path.join(临时目录, f"段_{i:03d}.mp3")
            await self.文字转语音(段, 输出路径=段路径, **参数)
            段文件列表.append(段路径)
            self._记录审计(f"第{i+1}/{len(段落列表)}段合成完成", 0.85)

        # 拼接音频
        if 输出路径 is None:
            时间戳 = datetime.now().strftime('%Y%m%d_%H%M%S')
            输出路径 = os.path.join(self.输出目录, f"龍魂长文本_{时间戳}.mp3")

        self._拼接音频(段文件列表, 输出路径)

        # 清理临时文件
        import shutil
        shutil.rmtree(临时目录, ignore_errors=True)

        self._记录_audit("长文本合成完成，音频已拼接", 0.9, 审计颜色.绿色通过)

        # 返回最终结果
        音频时长 = self._获取音频时长(输出路径)
        return 语音合成结果(
            音频路径=输出路径,
            文本=文本[:100] + "..." if len(文本) > 100 else 文本,
            语速=参数.get('语速', self.语速),
            音调=参数.get('音调', self.音调),
            语音角色="女声" if "Xiaoxiao" in self.语音角色 else "男声",
            音频时长=音频时长,
            采样率=24000,
            处理时长=0.0,
            合成引擎=f"edge-tts-长文本-{len(段落列表)}段",
            DNA追溯=f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-TTS-LONG-{len(段落列表)}segments"
        )

    def _智能分句(self, 文本: str, 最大长度: int) -> List[str]:
        """
        智能分句——在标点处分割，避免切断句子
        Smart sentence splitting — split at punctuation, avoid cutting sentences
        """
        import re

        分隔符 = r'[。！？\.\!\?;；]'
        句子列表 = re.split(f'({分隔符})', 文本)

        # 重新组合句子和分隔符
        完整句子 = []
        当前 = ""
        for i, 片段 in enumerate(句子列表):
            if re.match(分隔符, 片段):
                当前 += 片段
                完整句子.append(当前.strip())
                当前 = ""
            else:
                当前 += 片段
        if 当前.strip():
            完整句子.append(当前.strip())

        # 合并短句达到目标长度
        结果 = []
        当前段 = ""
        for 句 in 完整句子:
            if len(当前段) + len(句) <= 最大长度:
                当前段 += 句
            else:
                if 当前段:
                    结果.append(当前段)
                当前段 = 句
        if 当前段:
            结果.append(当前段)

        return 结果 if 结果 else [文本]

    def _拼接音频(self, 文件列表: List[str], 输出路径: str) -> None:
        """拼接多个音频文件 · Concatenate multiple audio files"""
        try:
            # 使用ffmpeg拼接
            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.txt', delete=False, encoding='utf-8'
            ) as 列表文件:
                for 文件 in 文件列表:
                    列表文件.write(f"file '{文件}'\n")
                列表路径 = 列表文件.name

            subprocess.run(
                ['ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                 '-i', 列表路径, '-acodec', 'copy', 输出路径],
                check=True, capture_output=True, timeout=60
            )
            os.unlink(列表路径)
        except (subprocess.SubprocessError, FileNotFoundError):
            # 降级：使用pydub
            try:
                from pydub import AudioSegment
                合并 = AudioSegment.empty()
                for 文件 in 文件列表:
                    合并 += AudioSegment.from_mp3(文件)
                合并.export(输出路径, format=输出路径.split('.')[-1])
            except ImportError:
                # 最后的降级：复制第一个文件
                import shutil
                shutil.copy(文件列表[0], 输出路径)
                self._记录审计(
                    "ffmpeg和pydub都不可用，仅保留第一段",
                    0.3,
                    审计颜色.黄色警告
                )

    # ═══════════════════════════════════════════════════════════════════════
    #  审计与日志 · Audit and Logging
    # ═══════════════════════════════════════════════════════════════════════

    def _记录审计(
        self,
        消息: str,
        置信度: float,
        颜色: 审计颜色 = 审计颜色.绿色通过
    ) -> None:
        """记录审计日志 · Record audit log"""
        if not self.审计开关:
            return
        self.审计日志.append(审计结果(
            颜色=颜色,
            置信度=置信度,
            原因=消息,
            建议=""
        ))

    def 获取审计日志(self) -> List[审计结果]:
        """获取全部审计日志 · Get all audit logs"""
        return list(self.审计日志)

    def 打印审计日志(self) -> None:
        """打印审计日志 · Print audit logs"""
        print("\n" + "=" * 60)
        print("  龍魂语音合成器 · 审计日志 · Audit Log")
        print("=" * 60)
        for i, 记录 in enumerate(self.审计日志, 1):
            print(f"  [{i}] {记录.颜色.value} 置信度={记录.置信度:.2f} | {记录.原因}")
        print("=" * 60)

    # ═══════════════════════════════════════════════════════════════════════
    #  配置管理 · Configuration Management
    # ═══════════════════════════════════════════════════════════════════════

    def 设置语音角色(self, 角色: str) -> None:
        """设置默认语音角色 · Set default voice role"""
        if "Neural" not in 角色:
            self.语音角色 = self.角色管理器.获取角色名称(角色)
            self.语音角色代码 = 角色
        else:
            self.语音角色 = 角色
            self.语音角色代码 = "custom"
        self._记录审计(f"语音角色已设置为: {self.语音角色}", 0.9)

    def 设置语速(self, 语速: float) -> None:
        """设置默认语速 · Set default speed"""
        self.语速 = max(0.25, min(2.0, 语速))
        self._记录审计(f"默认语速设置为: {self.语速}x", 0.9)

    def 设置音调(self, 音调: float) -> None:
        """设置默认音调 · Set default pitch"""
        self.音调 = max(-50, min(50, 音调))
        self._记录_audit(f"默认音调设置为: {self.音调}Hz", 0.9)

    def 获取配置(self) -> Dict[str, Any]:
        """获取当前配置 · Get current configuration"""
        return {
            "语音角色": self.语音角色,
            "语音角色代码": self.语音角色代码,
            "语速": self.语速,
            "音调": self.音调,
            "音量": self.音量,
            "输出目录": self.输出目录,
            "审计开关": self.审计开关,
            "DNA追溯": 六层来源链.DNA
        }

    def __repr__(self) -> str:
        return f"<龍魂语音合成器 角色={self.语音角色} 语速={self.语速}x>"


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  自测入口 · Self-Test Entry Point                                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    print("=" * 70)
    print("  龍魂语音合成器 · 自测程序")
    print("  LongHun Speech Synthesizer · Self-Test Program")
    print("=" * 70)

    # 测试1：六层来源链盖章
    print("\n【测试1】六层来源链盖章测试 · Six-layer provenance stamp test")
    印章 = 六层来源链.盖章("龍魂语音合成器.__main__")
    for 键, 值 in 印章.items():
        if isinstance(值, dict):
            print(f"  {键}:")
            for 子键, 子值 in 值.items():
                print(f"    {子键}: {子值}")
        else:
            print(f"  {键}: {值}")

    # 测试2：铁律自审闸
    print("\n【测试2】铁律自审闸测试 · Iron-rule self-audit gate test")
    闸 = 铁律自审闸()
    print(f"  全部铁律 ({len(闸.获取铁律())}条):")
    for 铁律 in 闸.获取铁律():
        print(f"    - {铁律}")
    print(f"  审查'龍魂北辰': {闸.审查('龍魂北辰')}")
    print(f"  审查'龙魂北辰': {闸.审查('龙魂北辰')}")

    # 测试3：语音角色管理器
    print("\n【测试3】语音角色管理器测试 · Voice role manager test")
    角色数 = len(语音角色管理器.获取全部角色())
    print(f"  全部角色数量: {角色数}")
    print(f"  中文角色: {list(语音角色管理器.中文角色.keys())}")
    print(f"  英语角色: {list(语音角色管理器.英语角色.keys())}")
    print(f"  获取角色名称(xiaoxiao): {语音角色管理器.获取角色名称('xiaoxiao')}")

    # 测试4：语音合成器初始化
    print("\n【测试4】语音合成器初始化 · Synthesizer initialization")
    try:
        合成器 = 龍魂语音合成器(
            语音角色="xiaoxiao",
            启用审计=True,
            输出目录="/tmp/龍魂语音输出"
        )
        print(f"  ✅ 合成器创建成功: {合成器}")
        print(f"  配置: {合成器.获取配置()}")
    except Exception as e:
        print(f"  ⚠️ 初始化警告: {e}")
        合成器 = None

    # 测试5：文本预处理
    if 合成器:
        print("\n【测试5】文本预处理测试 · Text preprocessing test")
        测试文本 = "  这是一段\n需要预处理的\r\n文本内容。包含  多余  空格！  "
        处理后 = 合成器._预处理文本(测试文本)
        print(f"  原始: '{测试文本}'")
        print(f"  处理后: '{处理后}'")

        # 超长文本测试
        长文本 = "这是一段测试文字。" * 200
        截断后 = 合成器._预处理文本(长文本)
        print(f"  长文本({len(长文本)}字符)截断后: {len(截断后)}字符")

    # 测试6：智能分句
    if 合成器:
        print("\n【测试6】智能分句测试 · Smart sentence splitting test")
        测试文 = "第一句。第二句！第三句？第四句；第五句。第六句。第七句。"
        分段 = 合成器._智能分句(测试文, 15)
        print(f"  原文: {测试文}")
        for i, 段 in enumerate(分段):
            print(f"  段{i+1}: {段}")

    # 测试7：语音合成结果数据结构
    print("\n【测试7】语音合成结果数据结构测试 · Result data structure test")
    测试结果 = 语音合成结果(
        音频路径="/tmp/测试音频.mp3",
        文本="这是测试文本",
        语速=1.0,
        音调=0.0,
        语音角色="女声",
        音频时长=3.5,
        采样率=24000,
        处理时长=0.8,
        合成引擎="edge-tts-test",
        DNA追溯="#龍芯⚡️2026-06-18-TTS-test"
    )
    print(f"  ✅ 结果对象: {测试结果}")
    print(f"  字典输出:")
    for k, v in 测试结果.to_dict().items():
        print(f"    {k}: {v}")

    # 测试8：角色列表打印
    print("\n【测试8】中文角色列表 · Chinese voice roles")
    语音角色管理器.列出角色("zh-CN")

    # 测试9：尝试实际合成（如果edge-tts可用）
    if 合成器:
        print("\n【测试9】实际语音合成测试 · Actual speech synthesis test")
        try:
            测试文本 = "你好，我是龍魂语音合成器。龍魂文化，生生不息。"
            结果 = asyncio.run(合成器.文字转语音(测试文本, 语速=1.0))
            print(f"  ✅ 合成成功!")
            print(f"  输出文件: {结果.音频路径}")
            print(f"  音频时长: {结果.音频时长:.2f}秒")
            print(f"  合成引擎: {结果.合成引擎}")
            print(f"  DNA追溯: {结果.DNA追溯}")

            # 播放提示（可选）
            print(f"\n  音频已保存，可使用以下命令播放:")
            print(f"  ffplay {结果.音频路径}")

        except ImportError as e:
            print(f"  ⚠️ edge-tts未安装: {e}")
            print(f"  安装命令: pip install edge-tts")
        except Exception as e:
            print(f"  ⚠️ 合成测试失败: {e}")

    # 最终审计日志
    if 合成器:
        print("\n")
        合成器.打印审计日志()

    # 君子协议 · Gentleman's Agreement
    print("\n" + "=" * 70)
    print("  君子协议 · Gentleman's Agreement · CC BY-NC-SA 4.0")
    print("  署名-非商业性使用-相同方式共享 4.0 国际")
    print("  Attribution-NonCommercial-ShareAlike 4.0 International")
    print("  https://creativecommons.org/licenses/by-nc-sa/4.0/")
    print("  UID9622 · 龍芯北辰 · 诸葛鑫")
    print("=" * 70)
