"""视觉识别与分析

DNA: #龍芯⚡️丙午·丙申·乙卯·亥时·需-SDK-VISION-A1B2C3D4
"""
from dataclasses import dataclass, field
from typing import Optional
import os
import warnings


@dataclass
class VisionResult:
    objects: list[str] = field(default_factory=list)
    culture_symbols: list[str] = field(default_factory=list)
    text: str = ""
    description: str = ""
    dna: str = ""


@dataclass
class SymbolResult:
    """文化符号识别结果"""
    symbol: str
    trigram: str
    element: str
    confidence: float


@dataclass
class Scene:
    """视频场景片段"""
    timestamp: float
    description: str


@dataclass
class VideoResult:
    """视频分析结果"""
    duration: float
    scenes: list[Scene]
    timeline: list[dict[str, object]]


class VisionAnalyzer:
    """图像/视频分析"""

    def analyze(self, image_path: str) -> VisionResult:
        """分析图片

        Args:
            image_path: 图片路径

        Returns:
            VisionResult with objects, symbols, text

        Raises:
            FileNotFoundError: 图片不存在时
            NotImplementedError: 真实视觉引擎尚未对接（Preview 阶段）。
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")

        raise NotImplementedError(
            "VisionAnalyzer.analyze() 真实视觉引擎尚未对接。\n"
            "当前为 API 契约先行版本（Preview）。\n"
            "完整版将对接 Ollama 多模态 / MLX 视觉模型。\n"
            "预期发布：后续版本。"
        )

    def recognize_symbol(self, image_path: str) -> SymbolResult:
        """识别文化符号

        Args:
            image_path: 图片路径

        Raises:
            FileNotFoundError: 图片不存在时
            NotImplementedError: 真实视觉引擎尚未对接（Preview 阶段）。
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")

        raise NotImplementedError(
            "VisionAnalyzer.recognize_symbol() 真实视觉引擎尚未对接（Preview 阶段）。"
        )

    def analyze_video(self, video_path: str, fps: int = 1) -> VideoResult:
        """分析视频

        Raises:
            NotImplementedError: 真实视频引擎尚未对接（Preview 阶段）。
        """
        raise NotImplementedError(
            "VisionAnalyzer.analyze_video() 真实视频引擎尚未对接（Preview 阶段）。"
        )


class VisionBridge:
    """本地多模态模型桥"""

    VALID_BACKENDS = ("ollama", "mlx")

    def __init__(self, backend: Optional[str] = None):
        self.backend = backend or self._detect_backend()
        if self.backend not in self.VALID_BACKENDS:
            raise ValueError(
                f"不支持的后端: {self.backend}，可选: {self.VALID_BACKENDS}"
            )

    def _detect_backend(self) -> str:
        """自动检测可用模型"""
        # 优先级: MLX视觉 > Ollama多模态
        return "ollama"

    def describe(self, image_path: str, prompt: str = "") -> str:
        """图片描述"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")
        return f"[{self.backend}] 图片内容: ..."
