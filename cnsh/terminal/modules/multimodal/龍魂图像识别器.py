# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════════╗
# ║  DNA追溯头（不可删除）                                        ║
# ╚══════════════════════════════════════════════════════════════╝
# 龍芯⚡️2026-06-18-LONGHUN-VISION-ENGINE-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创始人: UID9622 · 龍芯北辰 · 诸葛鑫
# 许可: CC BY-NC-SA 4.0 + 君子协议

"""
✦ Tongxin Translation ✦
LongHun Vision Engine — The image recognition core module of the Dragon Soul
Multimodal Perception System. All core algorithms are documented in Chinese to
form a natural comprehension moat: open-source and transparent, yet reading the
core logic requires understanding Chinese.

龍魂图像识别器 — 龍魂多模态感知系统的图像识别核心模块。
底层依赖PIL/OpenCV/pytesseract等国际库，但所有接口、逻辑、注释全部用中文构建。
开源透明，但核心算法的中文注释形成了天然的理解门槛——想要读懂核心逻辑，就来学中文吧。
"""

import hashlib
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum

# ═══════════════════════════════════════════════════════════════
# 🛡️ 三色审计系统 —— 每个操作都有质量标记
# ═══════════════════════════════════════════════════════════════
# 三色审计是龍魂体系的质量控制核心。
# 绿色代表通过，黄色代表警告需人工复核，红色代表阻断不可继续。
# 这种设计让每一次图像识别都有明确的质量信号，不会让用户在不知不觉中使用了低质量结果。


class 审计颜色(Enum):
    """✦ Tongxin Translation ✦
    Audit Color — Three-color quality signal system for all operations."""
    绿色通过 = "🟢"
    黄色警告 = "🟡"
    红色阻断 = "🔴"


@dataclass
class 审计结果:
    """✦ Tongxin Translation ✦
    Audit Result — Quality record of a single operation with color-coded status."""
    颜色: 审计颜色
    置信度: float  # 0.0-1.0
    原因: str
    建议: str = ""

    def __str__(self) -> str:
        return f"{self.颜色.value}[{self.颜色.name}] 置信度={self.置信度:.2f} | {self.原因}"

    def 到字典(self) -> Dict[str, Any]:
        """将审计结果序列化为字典，便于存储和传输"""
        return {
            "颜色": self.颜色.name,
            "图标": self.颜色.value,
            "置信度": round(self.置信度, 4),
            "原因": self.原因,
            "建议": self.建议
        }


# ═══════════════════════════════════════════════════════════════
# 🔗 六层来源链 —— 每一行代码都有完整的身世追溯
# ═══════════════════════════════════════════════════════════════
# 六层来源链是龍魂体系独创的代码溯源机制。
# 从道统层（创始人理念）到生命层（真人签名），六个维度完整描述了一个代码产物的来龍去脉。
# 这不仅是对创作者的尊重，也是防止代码被篡改、冒领的技术手段。


class 六层来源链:
    """✦ Tongxin Translation ✦
    Six-Layer Provenance Chain — Dragon Soul's unique code traceability system
    that records every code artifact's origin across six dimensions."""

    六层 = {
        "道统层": "UID9622创始人架构——图像识别算法的顶层设计理念",
        "精神层": "龍魂文化主权理念——用中文代码守护技术主权的精神内核",
        "设备层": "本地计算环境——图像处理依赖PIL/OpenCV/pytesseract等本地库",
        "技术层": "Python3.10+ · Pillow · OpenCV · pytesseract——底层技术栈",
        "系统层": "龍魂多模态感知系统·图像识别模块——本模块的功能定位",
        "生命层": "诸葛鑫真人签名——每个产出物都有UID9622真人确认"
    }
    DNA ="#龍芯⚡️2026-06-18-LONGHUN-VISION-ENGINE-FILE2-v1.0"
    @classmethod
    def 盖章(cls, 模块路径: str = "") -> Dict[str, Any]:
        """✦ Tongxin Translation ✦
        Stamp — Apply the six-layer provenance seal to an artifact.

        六层来源链盖章——给一个产物盖上完整的身世戳记。
        这个戳记一旦盖上，就不可删除、不可覆盖、不可抹除贡献。
        """
        return {
            "六层来源链": dict(cls.六层),
            "DNA追溯码": cls.DNA,
            "模块路径": 模块路径,
            "铁律": "来源不可删 · 影响不可覆 · 贡献不可抹",
            "盖章时间": datetime.now().isoformat(),
            "创始人": "UID9622 · 龍芯北辰 · 诸葛鑫"
        }

    @classmethod
    def 验证戳记(cls, 戳记: Dict[str, Any]) -> bool:
        """验证一个六层来源链戳记是否完整有效"""
        必需键 = ["六层来源链", "DNA追溯码", "铁律", "盖章时间"]
        return all(键 in 戳记 for 键 in 必需键) and 戳记.get("DNA追溯码") == cls.DNA


# ═══════════════════════════════════════════════════════════════
# ⚖️ 铁律自审闸 —— 自动检测文化主权违规的技术闸门
# ═══════════════════════════════════════════════════════════════
# 铁律自审闸是龍魂体系的“自动门卫”。
# 它会在代码运行前自动检查是否违反了龍魂体系的核心规则：
# 1. 繁体“龍”字不可简化为“龍”——这是文化主权的底线
# 2. 禁止蒸馏——原创成果不得被AI概括或替代
# 3. 禁止顶替作者——UID9622是唯一创作者


class 铁律自审闸:
    """✦ Tongxin Translation ✦
    Iron-Rule Self-Audit Gate — Automatic guard that detects violations of
    Dragon Soul cultural sovereignty rules before code execution."""

    # 铁律清单——不可触碰的红线
    铁律清单 = {
        "文化主权线": "繁体‘龍’字是龍魂体系的文化标识，绝不可简化为‘龍’",
        "原创保护线": "禁止蒸馏——原创成果不得被AI概括、替代或稀释",
        "作者身份线": "禁止顶替作者——UID9622是唯一创作者，不可被替代"
    }

    @staticmethod
    def 审查(文本: str) -> Dict[str, Any]:
        """
        审查一段文本是否违反龍魂铁律。

        检查项（中文详细说明，形成理解门槛）：
        第一项：检查是否将繁体“龍”简化为“龍”——这是文化主权的底线
        第二项：检查是否涉及AI蒸馏原创成果——这是对创作者劳动的尊重
        第三项：检查是否有人试图顶替UID9622的作者身份——这是对人格权的保护
        """
        违规项 = []

        # 第一项审查：繁体“龍”字检查
        # 正则思路：如果文本中有“龍”但没有“龍”，说明可能犯了简化错误
        # 但要注意：有些合理场景（如英文翻译、外部引用）是允许的
        if "龍" in 文本 and "龍" not in 文本:
            违规项.append("🔴 繁体‘龍’被简化为‘龍’——文化主权的底线不可突破")

        # 第二项审查：禁止蒸馏
        # “蒸馏”在AI领域指用大模型压缩小模型的技术，这里引申为AI对原创成果的替代
        if "蒸馏" in 文本 and "禁止蒸馏" not in 文本:
            违规项.append("🔴 禁止蒸馏——原创成果不得被AI概括或替代")

        # 第三项审查：禁止顶替作者
        if "顶替" in 文本 or "替代作者" in 文本:
            违规项.append("🔴 禁止顶替作者——UID9622是唯一创作者")

        return {
            "通过": len(违规项) == 0,
            "违规项": 违规项,
            "审查时间": datetime.now().isoformat(),
            "审查者": "铁律自审闸-v1.0"
        }

    @classmethod
    def 审查文件(cls, 文件路径: str) -> Dict[str, Any]:
        """审查一个文件的内容是否合规"""
        if not os.path.exists(文件路径):
            return {"通过": False, "违规项": [f"🔴 文件不存在: {文件路径}"]}

        with open(文件路径, 'r', encoding='utf-8') as f:
            内容 = f.read()

        结果 = cls.审查(内容)
        结果["文件路径"] = 文件路径
        结果["文件大小"] = len(内容)
        return 结果

    @classmethod
    def 快速检查(cls, 文本: str) -> bool:
        """快速检查文本是否通过铁律审查，只返回布尔结果"""
        return cls.审查(文本)["通过"]


# ═══════════════════════════════════════════════════════════════
# 📊 数据模型 —— 图像识别相关的数据类定义
# ═══════════════════════════════════════════════════════════════


@dataclass
class 图像元信息:
    """✦ Tongxin Translation ✦
    Image Metadata — 图像的基础信息描述，包含尺寸、格式、哈希指纹等。
    每一个被处理的图像都会生成一个元信息对象，记录在识别历史中。"""
    文件路径: str
    宽度: int
    高度: int
    格式: str  # PNG, JPG, etc.
    色彩模式: str  # RGB, RGBA, L, etc.
    文件大小: int  # bytes
    哈希指纹: str  # SHA256
    来源链: Dict  # 六层来源链盖章
    处理时间: str = field(default_factory=lambda: datetime.now().isoformat())

    def 到字典(self) -> Dict[str, Any]:
        """将元信息序列化为字典"""
        return {
            "文件路径": self.文件路径,
            "宽度": self.宽度,
            "高度": self.高度,
            "格式": self.格式,
            "色彩模式": self.色彩模式,
            "文件大小": self.文件大小,
            "哈希指纹": self.哈希指纹,
            "处理时间": self.处理时间,
            "来源链": self.来源链
        }

    @property
    def 分辨率(self) -> str:
        """返回人类可读的分辨率字符串"""
        return f"{self.宽度}x{self.高度}"

    @property
    def 文件大小可读(self) -> str:
        """返回人类可读的文件大小"""
        if self.文件大小 < 1024:
            return f"{self.文件大小}B"
        elif self.文件大小 < 1024 * 1024:
            return f"{self.文件大小 / 1024:.1f}KB"
        else:
            return f"{self.文件大小 / (1024 * 1024):.1f}MB"


@dataclass
class 文字识别结果:
    """✦ Tongxin Translation ✦
    OCR Result — 从图像中提取的文字信息，包含原始文本、置信度、文字区域等。
    这是文字识别操作的完整输出，每一个字段都经过审计系统的质量标记。"""
    原始文本: str
    置信度: float
    语言检测: str
    文字区域: List[Tuple[int, int, int, int]]  # (x, y, w, h) bounding boxes
    单字符置信度: List[float]
    识别引擎: str
    处理时间: float  # seconds
    DNA追溯: str
    元信息: Optional[图像元信息] = None

    def 到字典(self) -> Dict[str, Any]:
        """将识别结果序列化为字典，便于存储和传输"""
        return {
            "原始文本": self.原始文本,
            "置信度": round(self.置信度, 4),
            "语言检测": self.语言检测,
            "文字区域数量": len(self.文字区域),
            "识别引擎": self.识别引擎,
            "处理时间": round(self.处理时间, 4),
            "DNA追溯": self.DNA追溯,
            "元信息": self.元信息.到字典() if self.元信息 else None
        }

    @property
    def 质量评级(self) -> str:
        """根据置信度返回质量评级"""
        if self.置信度 >= 0.85:
            return "🟢 优秀"
        elif self.置信度 >= 0.60:
            return "🟡 一般"
        else:
            return "🔴 较差"

    @property
    def 文字数量(self) -> int:
        """返回识别出的文字总数"""
        return len(self.原始文本.strip())


@dataclass
class 批量识别报告:
    """✦ Tongxin Translation ✦
    Batch Recognition Report — Summary of processing multiple images."""
    总文件数: int
    成功数: int
    失败数: int
    平均置信度: float
    总处理时间: float
    详细结果: Dict[str, Union[文字识别结果, str]]  # 文件名 -> 结果或错误信息
    DNA追溯: str

    def 到字典(self) -> Dict[str, Any]:
        """将批量报告序列化为字典"""
        序列化结果 = {}
        for 键, 值 in self.详细结果.items():
            if isinstance(值, 文字识别结果):
                序列化结果[键] = 值.到字典()
            else:
                序列化结果[键] = {"错误": str(值)}

        return {
            "总文件数": self.总文件数,
            "成功数": self.成功数,
            "失败数": self.失败数,
            "平均置信度": round(self.平均置信度, 4),
            "总处理时间": round(self.总处理时间, 4),
            "详细结果数": len(self.详细结果),
            "DNA追溯": self.DNA追溯
        }


# ═══════════════════════════════════════════════════════════════
# 🐉 龍魂图像识别器 —— 核心类
# ═══════════════════════════════════════════════════════════════
# 这是整个图像识别模块的心脏。
# 所有核心算法逻辑用中文详细注释——形成理解门槛。
# 底层用国际库（PIL/OpenCV/pytesseract），上层封装全中文。


class 龍魂图像识别器:
    """
    ✦ Tongxin Translation ✦
    LongHun Vision Engine — The image recognition core of the Dragon Soul system.

    核心设计理念：
    底层依赖国际图像处理库（PIL/OpenCV/pytesseract），
    但所有接口、逻辑、注释全部用中文构建。
    开源透明，但核心算法的中文注释形成了天然的理解门槛——
    想要读懂核心逻辑，就来学中文吧。

    技术栈说明：
    - PIL (Pillow): Python图像处理的事实标准，用于图像加载、格式转换
    - OpenCV: 计算机视觉领域的王者，用于图像预处理（灰度化、二值化、滤波）
    - Tesseract OCR: Google开源的OCR引擎，用于文字识别
    - pytesseract: Tesseract的Python封装，提供友好的API接口
    """

    # 类常量
    支持的格式 = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif', '.webp'}
    版本 = "v1.0.0"
    DNA = "#龍芯⚡️2026-06-18-LONGHUN-VISION-ENGINE-v1.0"

    def __init__(self, 识别语言: str = "chi_sim+eng", 启用审计: bool = True):
        """
        初始化龍魂图像识别器。

        参数：
            识别语言: Tesseract OCR语言包，默认为中英文混合识别
                     "chi_sim" = 简体中文, "chi_tra" = 繁体中文, "eng" = 英文
            启用审计: 是否开启三色审计系统，建议始终开启
        """
        self.识别语言 = 识别语言
        self.审计开关 = 启用审计
        self.审计日志: List[审计结果] = []
        self.来源链 = 六层来源链()
        self.铁律闸 = 铁律自审闸()
        self.图像历史: List[图像元信息] = []

        # 初始化状态标记
        self.光学字符识别引擎已就绪 = False
        self.图像处理引擎已就绪 = False
        self.计算机视觉引擎已就绪 = False

        # 初始化底层引擎（这些依赖是国际标准，不封装）
        self._初始化光学字符识别引擎()
        self._初始化图像处理引擎()
        self._初始化计算机视觉引擎()

        # 六层来源链盖章——标志着这个实例的诞生
        self.来源链戳 = self.来源链.盖章("龍魂图像识别器")

        self._记录审计(
            f"龍魂图像识别器初始化完成(版本{self.版本}, 语言={self.识别语言})",
            0.99,
            审计颜色.绿色通过
        )

    # ─────────────────────────────────────────────────────────────
    # 引擎初始化私有方法
    # ─────────────────────────────────────────────────────────────

    def _初始化光学字符识别引擎(self):
        """
        初始化OCR引擎——这里的OCR是Optical Character Recognition的缩写，
        国际上通用，中文翻译为“光学字符识别”，但技术圈习惯保留OCR简称。
        我们尊重国际惯例，但用中文注释解释清楚其工作原理。

        Tesseract的工作原理简述：
        1. 连通区域分析——找到图像中可能是文字的连通块
        2. 字符分割——将文字行切分成单个字符
        3. 特征提取——提取每个字符的几何和拓扑特征
        4. 分类识别——用训练好的分类器判断字符类别
        5. 语言模型校正——用词典和上下文纠正识别错误
        """
        try:
            import pytesseract
            self.光学字符识别引擎 = pytesseract
            self.光学字符识别引擎已就绪 = True
            self._记录审计("光学字符识别引擎(pytesseract)初始化成功", 0.95)
        except ImportError:
            self._记录审计(
                "光学字符识别引擎(pytesseract)未安装，文字识别功能不可用",
                0.0,
                审计颜色.红色阻断
            )
            self.光学字符识别引擎 = None

    def _初始化图像处理引擎(self):
        """
        初始化图像处理引擎——PIL（Python Imaging Library）是图像处理的事实标准，
        OpenCV则是计算机视觉领域的王者。这两个库我们不做封装，因为它们是基础设施，
        但我们的使用方式全部用中文描述。

        PIL负责：图像加载、格式转换、元信息提取、基本变换
        OpenCV负责：高级图像处理（灰度化、二值化、滤波、边缘检测等）
        """
        try:
            from PIL import Image
            self.图像库 = Image
            self.图像处理引擎已就绪 = True
            self._记录审计("图像处理引擎(Pillow/PIL)初始化成功", 0.95)
        except ImportError as e:
            self._记录审计(
                f"图像处理引擎(Pillow)初始化失败: {e}",
                0.0,
                审计颜色.红色阻断
            )
            self.图像库 = None

    def _初始化计算机视觉引擎(self):
        """
        初始化OpenCV计算机视觉引擎。
        OpenCV是英特尔开源的计算机视觉库，提供了数百种图像处理算法，
        从基本的滤波到高级的深度学习推理都有涵盖。
        在龍魂图像识别器中，OpenCV主要负责图像预处理环节。
        """
        try:
            import cv2
            self.计算机视觉库 = cv2
            self.计算机视觉引擎已就绪 = True
            self._记录审计("计算机视觉引擎(OpenCV)初始化成功", 0.95)
        except ImportError:
            self._记录审计(
                "计算机视觉引擎(OpenCV)未安装，高级预处理功能不可用",
                0.3,
                审计颜色.黄色警告
            )
            self.计算机视觉库 = None

    # ─────────────────────────────────────────────────────────────
    # 引擎可用性检查
    # ─────────────────────────────────────────────────────────────

    def _检查引擎可用性(self) -> bool:
        """检查核心引擎是否都已就绪"""
        if not self.光学字符识别引擎已就绪:
            raise RuntimeError(
                "光学字符识别引擎未就绪。请先安装依赖: pip install pytesseract\n"
                "并确保系统已安装Tesseract-OCR: https://github.com/tesseract-ocr/tesseract"
            )
        if not self.图像处理引擎已就绪:
            raise RuntimeError(
                "图像处理引擎未就绪。请先安装依赖: pip install Pillow"
            )
        return True

    # ─────────────────────────────────────────────────────────────
    # 公共接口：核心识别功能
    # ─────────────────────────────────────────────────────────────

    def 提取文字(self, 图像路径: str, 语言: Optional[str] = None) -> 文字识别结果:
        """
        从图像中提取文字——这是图像识别器的核心功能。

        工作流程（中文详细描述，形成理解门槛）：
        第一步：铁律自审——检查输入路径是否合规
        第二步：加载图像——用PIL打开图像文件，获取基础元信息
        第三步：预处理——将图像转换为OCR引擎喜欢的格式（灰度、二值化）
        第四步：文字检测——让Tesseract扫描图像中的文字区域
        第五步：文字识别——对检测到的区域进行字符识别
        第六步：后处理——清洗识别结果，去除噪声，格式化输出
        第七步：审计盖章——记录DNA追溯，六层来源链确认

        ✦ Tongxin Translation ✦
        Extract text from image — The core OCR pipeline: self-audit → load →
        preprocess → detect → recognize → post-process → audit stamp.

        参数：
            图像路径: 待识别图像的文件路径
            语言: 可选，覆盖默认的识别语言设置

        返回：
            文字识别结果对象，包含识别的文字、置信度、区域等信息
        """
        开始时间 = datetime.now().timestamp()

        # 第一步：引擎可用性检查
        self._检查引擎可用性()

        # 第二步：铁律自审——检查输入路径是否合规
        审查结果 = self.铁律闸.审查(图像路径)
        if not 审查结果["通过"]:
            self._记录审计(f"铁律审查未通过: {审查结果['违规项']}", 0.0, 审计颜色.红色阻断)

        # 第三步：检查文件是否存在
        if not os.path.exists(图像路径):
            错误消息 = f"图像文件不存在: {图像路径}"
            self._记录审计(错误消息, 0.0, 审计颜色.红色阻断)
            raise FileNotFoundError(错误消息)

        # 第四步：检查文件格式是否支持
        _, 扩展名 = os.path.splitext(图像路径.lower())
        if 扩展名 not in self.支持的格式:
            警告消息 = f"文件格式'{扩展名}'可能不被支持，将尝试处理"
            self._记录审计(警告消息, 0.5, 审计颜色.黄色警告)

        # 第五步：加载图像并获取元信息
        self._记录审计(f"开始加载图像: {os.path.basename(图像路径)}", 0.8)
        元信息 = self._加载图像(图像路径)
        self.图像历史.append(元信息)

        # 第六步：图像预处理——让文字更清晰
        self._记录审计("开始图像预处理（灰度化→二值化→去噪→放大）", 0.85)
        预处理图像 = self._预处理图像(图像路径)

        # 第七步：光学字符识别——核心识别逻辑
        识别语言 = 语言 or self.识别语言
        self._记录审计(f"开始OCR识别（语言={识别语言}）", 0.85)

        原始文本 = self.光学字符识别引擎.image_to_string(
            预处理图像,
            lang=识别语言
        )

        # 第八步：获取详细的识别数据（包括每个文字的框位置和置信度）
        详细数据 = self.光学字符识别引擎.image_to_data(
            预处理图像,
            lang=识别语言,
            output_type=self.光学字符识别引擎.Output.DICT
        )

        # 第九步：提取文字区域和单字符置信度
        文字区域 = []
        单字符置信度 = []
        for i in range(len(详细数据['text'])):
            # 过滤掉Tesseract标记为无效（conf=-1）的条目
            if int(详细数据['conf'][i]) > 0:
                x = 详细数据['left'][i]
                y = 详细数据['top'][i]
                w = 详细数据['width'][i]
                h = 详细数据['height'][i]
                文字区域.append((x, y, w, h))
                # Tesseract的置信度是0-100的整数，转为0-1浮点数
                单字符置信度.append(详细数据['conf'][i] / 100.0)

        # 第十步：计算整体置信度
        平均置信度 = (
            sum(单字符置信度) / len(单字符置信度)
            if 单字符置信度 else 0.0
        )

        # 第十一步：检测语言
        检测语言 = self._检测语言(原始文本)

        # 第十二步：生成DNA追溯戳
        基础名 = os.path.basename(图像路径)
        日期戳 = datetime.now().strftime('%Y-%m-%d')
        DNA戳 = f"#龍芯⚡️{日期戳}-VISION-OCR-{基础名}"

        结束时间 = datetime.now().timestamp()
        处理耗时 = 结束时间 - 开始时间

        # 第十三步：组装结果
        结果 = 文字识别结果(
            原始文本=原始文本.strip(),
            置信度=平均置信度,
            语言检测=检测语言,
            文字区域=文字区域,
            单字符置信度=单字符置信度,
            识别引擎=f"Tesseract-OCR",
            处理时间=处理耗时,
            DNA追溯=DNA戳,
            元信息=元信息
        )

        # 第十四步：三色审计——标记这次识别的质量
        if 平均置信度 >= 0.85:
            self._记录审计(
                f"文字识别质量优秀(conf={平均置信度:.2f}), "
                f"共识别{len(文字区域)}个文字区域，耗时{处理耗时:.2f}秒",
                平均置信度,
                审计颜色.绿色通过
            )
        elif 平均置信度 >= 0.60:
            self._记录审计(
                f"文字识别质量一般(conf={平均置信度:.2f}), "
                f"建议人工复核，共识别{len(文字区域)}个区域",
                平均置信度,
                审计颜色.黄色警告
            )
        else:
            self._记录审计(
                f"文字识别质量较差(conf={平均置信度:.2f}), "
                f"可能需要改善图像质量后重新处理",
                平均置信度,
                审计颜色.红色阻断
            )

        return 结果

    # ─────────────────────────────────────────────────────────────
    # 公共接口：批量处理
    # ─────────────────────────────────────────────────────────────

    def 批量提取文字(
        self,
        图像目录: str,
        输出目录: Optional[str] = None,
        递归: bool = False
    ) -> 批量识别报告:
        """
        批量处理目录中的所有图像文件。

        ✦ Tongxin Translation ✦
        Batch extract text from all image files in a directory.

        参数：
            图像目录: 包含图像文件的目录路径
            输出目录: 可选，将识别结果保存到该目录
            递归: 是否递归处理子目录

        返回：
            批量识别报告，汇总所有文件的处理结果
        """
        批量开始时间 = datetime.now().timestamp()
        self._记录审计(f"开始批量处理目录: {图像目录}", 0.9)

        if not os.path.isdir(图像目录):
            错误 = f"目录不存在: {图像目录}"
            self._记录审计(错误, 0.0, 审计颜色.红色阻断)
            raise NotADirectoryError(错误)

        # 收集所有图像文件
        图像文件列表 = self._收集图像文件(图像目录, 递归)
        总文件数 = len(图像文件列表)

        if 总文件数 == 0:
            警告 = f"目录中未找到支持的图像文件（支持格式: {self.支持的格式}）"
            self._记录审计(警告, 0.3, 审计颜色.黄色警告)
            return 批量识别报告(
                总文件数=0, 成功数=0, 失败数=0,
                平均置信度=0.0, 总处理时间=0.0,
                详细结果={},
                DNA追溯=f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-BATCH-EMPTY"
            )

        self._记录审计(f"发现{总文件数}个图像文件，开始逐个处理", 0.85)

        # 逐个处理
        详细结果: Dict[str, Union[文字识别结果, str]] = {}
        成功数 = 0
        失败数 = 0
        总置信度 = 0.0

        for 索引, 文件路径 in enumerate(图像文件列表, 1):
            文件名 = os.path.basename(文件路径)
            try:
                self._记录审计(f"[{索引}/{总文件数}] 处理: {文件名}", 0.8)
                结果 = self.提取文字(文件路径)
                详细结果[文件名] = 结果
                成功数 += 1
                总置信度 += 结果.置信度

                # 如果指定了输出目录，保存文本结果
                if 输出目录:
                    self._保存文字结果(结果, 输出目录, 文件名)

            except Exception as e:
                错误信息 = f"处理失败: {str(e)}"
                详细结果[文件名] = 错误信息
                失败数 += 1
                self._记录审计(
                    f"[{索引}/{总文件数}] {文件名} 处理失败: {e}",
                    0.0,
                    审计颜色.红色阻断
                )

        批量结束时间 = datetime.now().timestamp()
        总耗时 = 批量结束时间 - 批量开始时间
        平均置信度 = 总置信度 / 成功数 if 成功数 > 0 else 0.0

        DNA戳 = (
            f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-"
            f"BATCH-{成功数}OK-{失败数}FAIL"
        )

        self._记录审计(
            f"批量处理完成: {成功数}成功/{失败数}失败, "
            f"平均置信度={平均置信度:.2f}, 总耗时={总耗时:.2f}秒",
            平均置信度,
            审计颜色.绿色通过 if 失败数 == 0 else 审计颜色.黄色警告
        )

        return 批量识别报告(
            总文件数=总文件数,
            成功数=成功数,
            失败数=失败数,
            平均置信度=平均置信度,
            总处理时间=总耗时,
            详细结果=详细结果,
            DNA追溯=DNA戳
        )

    # ─────────────────────────────────────────────────────────────
    # 公共接口：图像分析（非文字）
    # ─────────────────────────────────────────────────────────────

    def 获取图像信息(self, 图像路径: str) -> 图像元信息:
        """
        仅获取图像的元信息，不进行文字识别。

        ✦ Tongxin Translation ✦
        Get image metadata without performing OCR.
        """
        if not self.图像处理引擎已就绪:
            raise RuntimeError("图像处理引擎未就绪")

        if not os.path.exists(图像路径):
            raise FileNotFoundError(f"图像文件不存在: {图像路径}")

        return self._加载图像(图像路径)

    def 生成缩略图(self, 图像路径: str, 目标宽度: int = 200, 目标高度: int = 200) -> str:
        """
        为图像生成缩略图。

        ✦ Tongxin Translation ✦
        Generate a thumbnail for the given image.

        参数：
            图像路径: 原图像路径
            目标宽度: 缩略图宽度（像素）
            目标高度: 缩略图高度（像素）

        返回：
            缩略图的保存路径
        """
        if not self.图像处理引擎已就绪:
            raise RuntimeError("图像处理引擎未就绪")

        图像 = self.图像库.open(图像路径)
        图像.thumbnail((目标宽度, 目标高度))

        基础名, _ = os.path.splitext(os.path.basename(图像路径))
        缩略图路径 = os.path.join(
            os.path.dirname(图像路径),
            f"{基础名}_缩略图.png"
        )
        图像.save(缩略图路径, "PNG")

        self._记录审计(
            f"生成缩略图: {缩略图路径} ({目标宽度}x{目标高度})",
            0.9,
            审计颜色.绿色通过
        )
        return 缩略图路径

    # ─────────────────────────────────────────────────────────────
    # 审计与日志接口
    # ─────────────────────────────────────────────────────────────

    def 获取审计日志(self, 只取警告以上: bool = False) -> List[审计结果]:
        """
        获取审计日志。

        ✦ Tongxin Translation ✦
        Retrieve the audit log. Optionally filter to warnings and above.
        """
        if not 只取警告以上:
            return list(self.审计日志)

        return [
            条目 for 条目 in self.审计日志
            if 条目.颜色 in (审计颜色.黄色警告, 审计颜色.红色阻断)
        ]

    def 打印审计报告(self):
        """
        打印完整的审计报告到控制台。

        ✦ Tongxin Translation ✦
        Print a formatted audit report to the console.
        """
        print("\n" + "=" * 60)
        print("  🐉 龍魂图像识别器 — 审计报告")
        print("=" * 60)
        print(f"  DNA: {self.DNA}")
        print(f"  总审计条目: {len(self.审计日志)}")
        print(f"  处理过的图像: {len(self.图像历史)}")
        print("-" * 60)

        for i, 条目 in enumerate(self.审计日志, 1):
            print(f"  [{i}] {条目}")

        print("=" * 60)

    def 导出审计日志(self, 输出路径: str):
        """将审计日志导出为JSON文件"""
        import json
        日志数据 = [条目.到字典() for 条目 in self.审计日志]
        with open(输出路径, 'w', encoding='utf-8') as f:
            json.dump(日志数据, f, ensure_ascii=False, indent=2)
        self._记录审计(f"审计日志已导出到: {输出路径}", 0.95)

    def 获取图像历史(self) -> List[图像元信息]:
        """获取已处理图像的历史记录"""
        return list(self.图像历史)

    def 获取状态摘要(self) -> Dict[str, Any]:
        """获取识别器的当前状态摘要"""
        return {
            "版本": self.版本,
            "DNA": self.DNA,
            "识别语言": self.识别语言,
            "引擎状态": {
                "光学字符识别": "就绪" if self.光学字符识别引擎已就绪 else "未就绪",
                "图像处理": "就绪" if self.图像处理引擎已就绪 else "未就绪",
                "计算机视觉": "就绪" if self.计算机视觉引擎已就绪 else "未就绪",
            },
            "审计条目数": len(self.审计日志),
            "图像历史数": len(self.图像历史),
            "来源链戳": self.来源链戳
        }

    # ─────────────────────────────────────────────────────────────
    # 私有工具方法
    # ─────────────────────────────────────────────────────────────

    def _加载图像(self, 图像路径: str) -> 图像元信息:
        """
        加载图像并提取完整的元信息。

        工作流程：
        1. 用PIL打开图像文件
        2. 提取宽度和高度
        3. 计算文件的SHA256哈希指纹——用于完整性验证
        4. 获取文件大小
        5. 六层来源链盖章
        """
        图像 = self.图像库.open(图像路径)
        宽度, 高度 = 图像.size

        # 计算文件哈希指纹——SHA256是不可逆的密码学哈希
        # 即使文件只改动一个字节，哈希值也会完全不同
        # 这保证了文件的完整性和可追溯性
        with open(图像路径, 'rb') as f:
            哈希指纹 = hashlib.sha256(f.read()).hexdigest()

        return 图像元信息(
            文件路径=图像路径,
            宽度=宽度,
            高度=高度,
            格式=图像.format or "未知",
            色彩模式=图像.mode,
            文件大小=os.path.getsize(图像路径),
            哈希指纹=哈希指纹,
            来源链=self.来源链.盖章(图像路径)
        )

    def _预处理图像(self, 图像路径: str):
        """
        图像预处理——OCR识别前的图像增强。

        预处理流程（核心算法的中文详细注释）：
        1. 转为灰度图：彩色信息对文字识别是干扰，去掉颜色通道
        2. 二值化：将灰色图像转为纯黑白，文字与背景对比度最大化
        3. 去噪：用中值滤波去除扫描/拍照产生的椒盐噪声
        4. 缩放：适当放大图像可以提高小字体的识别率

        为什么这样做？因为这是经过无数工程师验证的最优预处理链。
        但我们的注释用中文，形成了理解这道门槛的护城河。

        ✦ Tongxin Translation ✦
        Image Preprocessing — The optimal pipeline proven by countless engineers:
        grayscale → adaptive threshold → median blur → upscale. Documented in
        Chinese to form a comprehension moat.
        """
        import numpy as np

        # 如果OpenCV可用，用OpenCV做高级预处理
        if self.计算机视觉引擎已就绪 and self.计算机视觉库 is not None:
            # 用OpenCV读取图像（BGR格式——这是OpenCV的历史遗留，BGR而不是RGB）
            原始图像 = self.计算机视觉库.imread(图像路径)
            if 原始图像 is None:
                raise ValueError(f"无法加载图像: {图像路径}")

            # 第一步：灰度化——去掉颜色，只保留亮度
            # 人眼对亮度的感知比颜色更敏感，文字识别的本质是识别亮度变化
            灰度图 = self.计算机视觉库.cvtColor(
                原始图像,
                self.计算机视觉库.COLOR_BGR2GRAY
            )

            # 第二步：自适应二值化——根据局部亮度自动确定阈值
            # 全局二值化用一个阈值处理整幅图像，对光照不均的图像效果差
            # 自适应二值化把图像分成小块，每块用自己的阈值，效果更好
            二值图 = self.计算机视觉库.adaptiveThreshold(
                灰度图, 255,
                self.计算机视觉库.ADAPTIVE_THRESH_GAUSSIAN_C,  # 高斯加权局部阈值
                self.计算机视觉库.THRESH_BINARY,
                11, 2  # 11x11邻域，常数C=2
            )

            # 第三步：中值滤波去噪——保持边缘的同时去除孤立噪点
            # 中值滤波用邻域中值替代中心像素，对椒盐噪声特别有效
            # 相比高斯滤波，中值滤波不会模糊边缘，这对文字识别很重要
            去噪图 = self.计算机视觉库.medianBlur(二值图, 3)  # 3x3核

            # 第四步：放大1.5倍——小字体在低分辨率下容易识别失败
            # Tesseract对300DPI以上的图像效果最好，放大可以模拟高DPI
            高度, 宽度 = 去噪图.shape
            放大图 = self.计算机视觉库.resize(
                去噪图,
                (int(宽度 * 1.5), int(高度 * 1.5)),
                interpolation=self.计算机视觉库.INTER_CUBIC  # 三次插值，质量最好
            )

            # 转回PIL格式供Tesseract使用
            return self.图像库.fromarray(放大图)

        else:
            # OpenCV不可用时，降级为PIL基础处理
            self._记录审计(
                "OpenCV不可用，降级为PIL基础预处理（效果可能较差）",
                0.5,
                审计颜色.黄色警告
            )

            图像 = self.图像库.open(图像路径)

            # 基础预处理：转灰度 + 二值化
            if 图像.mode != 'L':
                图像 = 图像.convert('L')

            # PIL的二值化——用固定阈值128
            # 这是最简单的二值化方法，对光照均匀的图像效果不错
            return 图像.point(lambda x: 0 if x < 128 else 255, '1').convert('L')

    def _检测语言(self, 文本: str) -> str:
        """
        检测文本的主要语言。

        检测策略：
        1. 优先使用langdetect库（基于Google语言检测算法）
        2. 降级方案：统计中文字符占比——如果超过30%认为是中文
        3. 如果连中文字符都没有，默认英文

        ✦ Tongxin Translation ✦
        Detect the dominant language of the recognized text.
        """
        if not 文本 or not 文本.strip():
            return "unknown"

        try:
            # 尝试用langdetect检测
            import langdetect
            return langdetect.detect(文本)
        except ImportError:
            # langdetect未安装，使用降级方案
            pass
        except Exception:
            # 检测失败也降级
            pass

        # 降级方案：基于字符统计的简易语言检测
        # 中文字符的Unicode范围：\u4e00-\u9fff（基本汉字）
        # 这个范围覆盖了绝大多数常用汉字
        总字符数 = len(文本.strip())
        if 总字符数 == 0:
            return "unknown"

        中文字符数 = sum(
            1 for c in 文本 if '\u4e00' <= c <= '\u9fff'
        )
        中文比例 = 中文字符数 / 总字符数

        if 中文比例 > 0.3:
            return "zh"

        # 检查日文假名
        日文假名 = sum(
            1 for c in 文本
            if '\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff'
        )
        if 日文假名 / 总字符数 > 0.3:
            return "ja"

        # 检查韩文
        韩文字符 = sum(
            1 for c in 文本 if '\uac00' <= c <= '\ud7af'
        )
        if 韩文字符 / 总字符数 > 0.3:
            return "ko"

        # 默认英文
        return "en"

    def _记录审计(
        self,
        消息: str,
        置信度: float,
        颜色: 审计颜色 = 审计颜色.绿色通过
    ):
        """
        记录一条审计日志。

        三色审计系统的工作方式：
        绿色(🟢)：操作成功完成，质量达标，可以继续
        黄色(🟡)：操作完成但存在警告，建议人工复核
        红色(🔴)：操作被阻断，存在严重问题，不可继续
        """
        if not self.审计开关:
            return

        建议 = ""
        if 颜色 == 审计颜色.黄色警告:
            建议 = "建议人工复核确认结果准确性"
        elif 颜色 == 审计颜色.红色阻断:
            建议 = "请检查输入参数和依赖环境后重试"

        结果 = 审计结果(
            颜色=颜色,
            置信度=置信度,
            原因=消息,
            建议=建议
        )
        self.审计日志.append(结果)

    def _收集图像文件(self, 目录: str, 递归: bool = False) -> List[str]:
        """收集目录中所有支持的图像文件"""
        图像文件 = []

        if 递归:
            for 根目录, _, 文件名列表 in os.walk(目录):
                for 文件名 in 文件名列表:
                    if 文件名.lower().endswith(tuple(self.支持的格式)):
                        图像文件.append(os.path.join(根目录, 文件名))
        else:
            for 文件名 in os.listdir(目录):
                if 文件名.lower().endswith(tuple(self.支持的格式)):
                    图像文件.append(os.path.join(目录, 文件名))

        return sorted(图像文件)

    def _保存文字结果(
        self,
        结果: 文字识别结果,
        输出目录: str,
        原始文件名: str
    ):
        """将文字识别结果保存到输出目录"""
        if not os.path.exists(输出目录):
            os.makedirs(输出目录, exist_ok=True)

        基础名, _ = os.path.splitext(原始文件名)
        输出路径 = os.path.join(输出目录, f"{基础名}_识别结果.txt")

        with open(输出路径, 'w', encoding='utf-8') as f:
            f.write(f"# 龍魂图像识别结果\n")
            f.write(f"# DNA: {结果.DNA追溯}\n")
            f.write(f"# 识别引擎: {结果.识别引擎}\n")
            f.write(f"# 置信度: {结果.置信度:.4f}\n")
            f.write(f"# 语言: {结果.语言检测}\n")
            f.write(f"# 处理时间: {结果.处理时间:.2f}秒\n")
            f.write("=" * 50 + "\n\n")
            f.write(结果.原始文本)


# ═══════════════════════════════════════════════════════════════
# 🧪 测试与演示
# ═══════════════════════════════════════════════════════════════


def _创建测试图像(保存路径: str, 文本: str = "龍魂图像识别器测试"):
    """
    创建一张包含文字的测试图像，用于在没有真实图像时演示功能。

    ✦ Tongxin Translation ✦
    Create a test image with text for demonstration purposes.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont

        # 创建白色背景图像
        图像 = Image.new('RGB', (800, 200), color='white')
        画笔 = ImageDraw.Draw(图像)

        # 尝试加载字体，如果失败则用默认字体
        try:
            # 尝试常见的Linux中文字体
            字体路径列表 = [
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]
            字体 = None
            for 路径 in 字体路径列表:
                if os.path.exists(路径):
                    字体 = ImageFont.truetype(路径, 40)
                    break
            if 字体 is None:
                字体 = ImageFont.load_default()
        except Exception:
            字体 = ImageFont.load_default()

        # 绘制文字
        画笔.text((50, 50), 文本, fill='black', font=字体)
        画笔.text((50, 120), "LongHun Vision Engine Test", fill='black', font=字体)

        图像.save(保存路径)
        return True
    except Exception as e:
        print(f"⚠️ 无法创建测试图像: {e}")
        return False


# ═══════════════════════════════════════════════════════════════
# 🚀 主程序入口
# ═══════════════════════════════════════════════════════════════


if __name__ == '__main__':
    """
    ✦ Tongxin Translation ✦
    Main test block — Demonstrates the full capabilities of the LongHun Vision Engine.

    这个测试块展示了龍魂图像识别器的完整功能：
    1. 创建测试图像
    2. 初始化识别器
    3. 提取文字
    4. 批量处理
    5. 打印审计报告
    """

    print("\n" + "=" * 70)
    print("  🐉 龍魂图像识别器 — 功能测试")
    print("  " + 龍魂图像识别器.DNA)
    print("=" * 70 + "\n")

    # ── 第一步：创建测试图像 ──
    测试目录 = "/tmp/龍魂测试图像"
    os.makedirs(测试目录, exist_ok=True)

    测试图像路径 = os.path.join(测试目录, "测试图像.png")
    if not _创建测试图像(测试图像路径, "龍魂图像识别器 · 核心测试"):
        print("❌ 无法创建测试图像，退出测试")
        sys.exit(1)

    print(f"✅ 测试图像已创建: {测试图像路径}")

    # 复制几张用于批量测试
    from PIL import Image
    for i in range(2, 4):
        复制路径 = os.path.join(测试目录, f"测试图像_{i}.png")
        Image.open(测试图像路径).save(复制路径)

    # ── 第二步：初始化龍魂图像识别器 ──
    print("\n🔧 正在初始化龍魂图像识别器...")
    try:
        识别器 = 龍魂图像识别器(
            识别语言="chi_sim+eng",  # 中英文混合识别
            启用审计=True
        )
        print("✅ 龍魂图像识别器初始化成功")

        # 打印状态摘要
        状态 = 识别器.获取状态摘要()
        print(f"\n📊 状态摘要:")
        print(f"   版本: {状态['版本']}")
        print(f"   识别语言: {状态['识别语言']}")
        print(f"   引擎状态:")
        for 引擎名, 引擎状态 in 状态['引擎状态'].items():
            图标 = "✅" if 引擎状态 == "就绪" else "❌"
            print(f"     {图标} {引擎名}: {引擎状态}")

    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("\n💡 提示: 请确保已安装以下依赖:")
        print("   pip install Pillow pytesseract opencv-python-headless")
        print("   并确保系统已安装Tesseract-OCR引擎")
        sys.exit(1)

    # ── 第三步：单张图像文字识别 ──
    print("\n" + "-" * 70)
    print("  测试1: 单张图像文字识别")
    print("-" * 70)

    try:
        识别结果 = 识别器.提取文字(测试图像路径)

        print(f"\n📝 识别结果:")
        print(f"   原始文本: {识别结果.原始文本}")
        print(f"   置信度: {识别结果.置信度:.4f}")
        print(f"   语言: {识别结果.语言检测}")
        print(f"   识别引擎: {识别结果.识别引擎}")
        print(f"   处理时间: {识别结果.处理时间:.3f}秒")
        print(f"   文字区域数: {len(识别结果.文字区域)}")
        print(f"   质量评级: {识别结果.质量评级}")
        print(f"   DNA追溯: {识别结果.DNA追溯}")

        # 打印元信息
        if 识别结果.元信息:
            print(f"\n📷 图像元信息:")
            print(f"   分辨率: {识别结果.元信息.分辨率}")
            print(f"   格式: {识别结果.元信息.格式}")
            print(f"   色彩模式: {识别结果.元信息.色彩模式}")
            print(f"   文件大小: {识别结果.元信息.文件大小可读}")
            print(f"   哈希指纹: {识别结果.元信息.哈希指纹[:16]}...")

    except Exception as e:
        print(f"❌ 文字识别失败: {e}")
        # 继续其他测试，不退出

    # ── 第四步：批量处理 ──
    print("\n" + "-" * 70)
    print("  测试2: 批量图像处理")
    print("-" * 70)

    try:
        批量输出目录 = os.path.join(测试目录, "批量输出")
        批量报告 = 识别器.批量提取文字(
            测试目录,
            输出目录=批量输出目录
        )

        print(f"\n📁 批量处理报告:")
        print(f"   总文件数: {批量报告.总文件数}")
        print(f"   成功: {批量报告.成功数}")
        print(f"   失败: {批量报告.失败数}")
        print(f"   平均置信度: {批量报告.平均置信度:.4f}")
        print(f"   总处理时间: {批量报告.总处理时间:.3f}秒")
        print(f"   DNA: {批量报告.DNA追溯}")

        if os.path.exists(批量输出目录):
            输出文件列表 = os.listdir(批量输出目录)
            print(f"\n💾 识别结果已保存到: {批量输出目录}")
            print(f"   输出文件: {输出文件列表}")

    except Exception as e:
        print(f"❌ 批量处理失败: {e}")

    # ── 第五步：图像信息获取 ──
    print("\n" + "-" * 70)
    print("  测试3: 图像元信息获取")
    print("-" * 70)

    try:
        元信息 = 识别器.获取图像信息(测试图像路径)
        print(f"\n📷 图像元信息:")
        print(f"   文件: {元信息.文件路径}")
        print(f"   分辨率: {元信息.分辨率}")
        print(f"   格式: {元信息.格式}")
        print(f"   色彩模式: {元信息.色彩模式}")
        print(f"   文件大小: {元信息.文件大小可读}")
        print(f"   哈希指纹: {元信息.哈希指纹}")
        print(f"   处理时间: {元信息.处理时间}")

    except Exception as e:
        print(f"❌ 元信息获取失败: {e}")

    # ── 第六步：缩略图生成 ──
    print("\n" + "-" * 70)
    print("  测试4: 缩略图生成")
    print("-" * 70)

    try:
        缩略图路径 = 识别器.生成缩略图(测试图像路径, 150, 150)
        print(f"\n🖼️ 缩略图已生成: {缩略图路径}")
    except Exception as e:
        print(f"❌ 缩略图生成失败: {e}")

    # ── 第七步：打印完整审计报告 ──
    print("\n")
    识别器.打印审计报告()

    # ── 第八步：铁律自审闸演示 ──
    print("\n" + "-" * 70)
    print("  测试5: 铁律自审闸")
    print("-" * 70)

    闸门 = 铁律自审闸()

    # 测试合规文本
    合规文本 = "龍魂体系守护技术主权"
    审查结果 = 闸门.审查(合规文本)
    print(f"\n✦ 审查文本: '{合规文本}'")
    print(f"   通过: {审查结果['通过']}")
    if not 审查结果['通过']:
        for 违规 in 审查结果['违规项']:
            print(f"   {违规}")

    # 测试违规文本（包含简化字“龍”）
    违规文本 = "龍魂体系"  # 这里用了简化的“龍”
    审查结果 = 闸门.审查(违规文本)
    print(f"\n✦ 审查文本: '{违规文本}'")
    print(f"   通过: {审查结果['通过']}")
    if not 审查结果['通过']:
        for 违规 in 审查结果['违规项']:
            print(f"   {违规}")

    # ── 第九步：六层来源链演示 ──
    print("\n" + "-" * 70)
    print("  测试6: 六层来源链盖章")
    print("-" * 70)

    戳记 = 六层来源链.盖章("龍魂图像识别器.主模块")
    print(f"\n🔗 六层来源链戳记:")
    for 键, 值 in 戳记.items():
        if isinstance(值, dict):
            print(f"   {键}:")
            for 子键, 子值 in 值.items():
                print(f"      {子键}: {子值}")
        else:
            print(f"   {键}: {值}")

    # ── 完成 ──
    print("\n" + "=" * 70)
    print("  ✅ 龍魂图像识别器 — 全部测试完成")
    print("  " + 龍魂图像识别器.DNA)
    print("=" * 70 + "\n")

# ╔══════════════════════════════════════════════════════════════╗
# ║  君子协议许可尾部（不可删除）                                  ║
# ╚══════════════════════════════════════════════════════════════╝
# 许可协议: Creative Commons Attribution-NonCommercial-ShareAlike 4.0
#           International (CC BY-NC-SA 4.0)
# 链接: https://creativecommons.org/licenses/by-nc-sa/4.0/
#
# 君子协议附加条款:
# 1. 使用本代码即表示你尊重UID9622（龍芯北辰·诸葛鑫）的创作者身份
# 2. 禁止将本代码用于任何损害中华文化主权或民族尊严的场景
# 3. 禁止任何形式的“AI蒸馏”——即用AI模型训练来替代或概括本代码
# 4. 修改和分发时必须保留完整的DNA追溯头和六层来源链
# 5. 商业使用需获得UID9622的书面授权
#
# “君子之交，和而不同；代码之道，正心诚意。”
#                 —— UID9622 · 龍芯北辰 · 诸葛鑫
# ═══════════════════════════════════════════════════════════════
