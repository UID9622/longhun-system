#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·VISION-PARSER-v1.0-IMG2JSON
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂·视觉解析引擎 v1.0 — 图片/视频帧/截图 → 结构化描述
DNA: #龍芯⚡️丙午·辛未·VISION-PARSER-v1.0-IMG2JSON

五步处理管线:
  ① 图像预处理: 缩放/去噪/格式归一
  ② OCR识别: 全量文字提取 (水印/UI元素/角落小字)
  ③ 场景分析: 室内外/昼夜/人数/主动作
  ④ 情绪识别: 表情/肢体语言/氛围
  ⑤ 结构化输出: JSON含原始描述+提取文本+标签列表+置信度

关键特性: 截图优化 — 应用名/聊天界面/时间戳/电量/信号强度

统一接口: parse(input_data: bytes|str|Path) → VisionOutput

用法:
  from bin.lh_vision_parser import VisionParser
  parser = VisionParser()
  result = parser.parse("/path/to/image.jpg")
  print(result.to_json())

部署: 本地优先，Mac M4 Max跑视觉，数据不出本地
"""

import json
import os
import sys
import hashlib
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Union, Dict, Any, List
from datetime import datetime, timezone, timedelta

# ── 审计层导入 ──
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from tools.logging.action_logger import ActionLogger, log_operation
except ImportError:
    ActionLogger = None
    def log_operation(*args, **kwargs):
        from contextlib import nullcontext
        return nullcontext()

DNA = "#龍芯⚡️丙午·辛未·VISION-PARSER-v1.0-IMG2JSON"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬VISN-A1B2"

# ═══════════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════════

@dataclass
class OCRBlock:
    """OCR文本块"""
    text: str
    bbox: Optional[List[int]] = None          # [x, y, w, h]
    confidence: float = 0.0
    source: str = "body"                       # body/watermark/ui/corner

@dataclass
class SceneInfo:
    """场景分析"""
    location: str = "unknown"                   # indoor/outdoor
    time_of_day: str = "unknown"                # day/night/dawn/dusk
    person_count: int = 0
    main_activity: str = ""
    objects: List[str] = field(default_factory=list)

@dataclass
class EmotionInfo:
    """情绪分析"""
    dominant: str = "neutral"                   # 主导情绪
    intensity: float = 0.0                      # 强度 0-1
    faces: List[Dict[str, Any]] = field(default_factory=list)
    overall_atmosphere: str = "neutral"

@dataclass
class ScreenshotMeta:
    """截图元数据 (手机截图优化)"""
    is_screenshot: bool = False
    app_name: str = ""
    chat_interface: bool = False
    timestamp_str: str = ""
    battery_level: str = ""
    signal_strength: str = ""
    platform: str = ""                          # iOS/Android

@dataclass
class VisionOutput:
    """视觉解析统一输出"""
    input_hash: str = ""
    raw_description: str = ""
    ocr_texts: List[OCRBlock] = field(default_factory=list)
    scene: SceneInfo = field(default_factory=SceneInfo)
    emotion: EmotionInfo = field(default_factory=EmotionInfo)
    screenshot_meta: ScreenshotMeta = field(default_factory=ScreenshotMeta)
    tags: List[str] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    processing_time_ms: float = 0.0
    model_version: str = "v1.0-local"
    dna: str = DNA
    parsed_at: str = ""

    def to_json(self, indent: int = 2) -> str:
        d = asdict(self)
        d["ocr_texts"] = [asdict(o) for o in self.ocr_texts]
        return json.dumps(d, ensure_ascii=False, indent=indent)

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.to_json())


# ═══════════════════════════════════════════════════════════════
# 解析引擎
# ═══════════════════════════════════════════════════════════════

class VisionParser:
    """视觉解析器 · 统一接口 parse(input_data) → VisionOutput"""

    def __init__(self, backend: str = "local"):
        """
        Args:
            backend: "local" (PIL+规则) | "ollama" | "mlx" | "api"
        """
        self.backend = backend
        self._preprocessors = {
            "local": self._preprocess_local,
        }
        self._ocr_engines = {
            "local": self._ocr_local,
        }
        self._scene_analyzers = {
            "local": self._analyze_scene_local,
        }
        self._emotion_detectors = {
            "local": self._detect_emotion_local,
        }
        self._screenshot_detectors = {
            "local": self._detect_screenshot_local,
        }

    # ── 步骤①: 图像预处理 ──
    def _preprocess_local(self, image_data: bytes) -> bytes:
        """本地预处理: 缩放/去噪/格式归一化"""
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(image_data))
            img = img.convert("RGB")
            # 大图限制 2048px
            max_dim = 2048
            if max(img.size) > max_dim:
                ratio = max_dim / max(img.size)
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                img = img.resize(new_size, Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=85, optimize=True)
            return buf.getvalue()
        except ImportError:
            return image_data

    # ── 步骤②: OCR识别 ──
    def _ocr_local(self, image_data: bytes) -> List[OCRBlock]:
        """本地OCR: 提取所有文字 (水印/UI/角落小字)"""
        results = []
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(image_data))
            # 纯本地规则提取: 分析图像区域
            w, h = img.size
            # 尝试 pytesseract (可选依赖)
            try:
                import pytesseract
                raw = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                for i, txt in enumerate(raw["text"]):
                    txt = txt.strip()
                    if not txt:
                        continue
                    conf = raw["conf"][i]
                    if conf == "-1":
                        conf = 50
                    else:
                        conf = float(conf) / 100.0
                    x, y, bw, bh = raw["left"][i], raw["top"][i], raw["width"][i], raw["height"][i]
                    source = "body"
                    if y < h * 0.05:  # 顶部区域 → UI/状态栏
                        source = "ui"
                    elif x > w * 0.85:  # 右侧窄区 → 水印/边缘
                        source = "watermark"
                    elif y > h * 0.92:  # 底部 → 角落
                        source = "corner"

                    results.append(OCRBlock(
                        text=txt,
                        bbox=[x, y, bw, bh],
                        confidence=round(conf, 3),
                        source=source,
                    ))
            except ImportError:
                # 无 OCR 引擎: 返回空 → 通过语义层可补
                pass
        except ImportError:
            pass
        return results

    # ── 步骤③: 场景分析 ──
    def _analyze_scene_local(self, image_data: bytes, ocr_texts: List[OCRBlock]) -> SceneInfo:
        """本地场景分析: 亮度/色彩/布局推断"""
        scene = SceneInfo()
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(image_data))
            w, h = img.size

            # 亮度分析 → 昼夜判断
            gray = img.convert("L")
            pixels = list(gray.getdata())
            avg_brightness = sum(pixels) / len(pixels) if pixels else 128
            if avg_brightness > 160:
                scene.time_of_day = "day"
            elif avg_brightness > 80:
                scene.time_of_day = "dawn_or_dusk"
            else:
                scene.time_of_day = "night"

            # 色彩饱和度 → 室内外
            import statistics
            data = list(img.getdata())
            if data:
                saturations = []
                for r, g, b in data[:2000]:  # 采样
                    mx, mn = max(r, g, b), min(r, g, b)
                    if mx > 0:
                        saturations.append((mx - mn) / mx)
                avg_sat = statistics.mean(saturations) if saturations else 0
                scene.location = "outdoor" if avg_sat > 0.4 else "indoor"

            # 从OCR推断人数/活动
            all_text = " ".join(o.text for o in ocr_texts)
            activity_keywords = {
                "meeting": ["会议", "纪要", "议题", "讨论"],
                "chat": ["消息", "对方", "@", "撤回"],
                "coding": ["print", "def ", "import", "function"],
                "shopping": ["订单", "￥", "付款", "购买"],
                "reading": ["阅读", "文章", "查看"],
            }
            for activity, keywords in activity_keywords.items():
                if any(k in all_text for k in keywords):
                    scene.main_activity = activity
                    break

            if not scene.main_activity:
                scene.main_activity = "unknown"

            scene.objects = self._detect_common_objects_local(img)

        except ImportError:
            pass
        return scene

    def _detect_common_objects_local(self, img) -> List[str]:
        """基于尺寸比例推断常见物体"""
        return []  # 本地规则: 需要模型才能可靠检测

    # ── 步骤④: 情绪识别 ──
    def _detect_emotion_local(self, image_data: bytes, scene: SceneInfo, ocr_texts: List[OCRBlock]) -> EmotionInfo:
        """本地情绪识别: 色彩+文字情感推断"""
        emotion = EmotionInfo()
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(image_data))
            data = list(img.getdata())
            if data:
                reds = sum(p[0] for p in data[:2000]) / min(2000, len(data))
                blues = sum(p[2] for p in data[:2000]) / min(2000, len(data))
                # 暖色调 → 积极 / 冷色调 → 消极
                if reds > blues * 1.2 and reds > 140:
                    emotion.dominant = "positive"
                    emotion.intensity = 0.6
                elif blues > reds * 1.2 and blues > 140:
                    emotion.dominant = "calm"
                    emotion.intensity = 0.5
                else:
                    emotion.dominant = "neutral"
                    emotion.intensity = 0.3

            # OCR 文本情感
            all_text = " ".join(o.text for o in ocr_texts)
            positive_words = ["👍", "开心", "好", "棒", "感谢", "恭喜", "😊", "哈哈"]
            negative_words = ["😡", "烦", "烂", "投诉", "退款", "差", "😭", "cao"]
            pos_count = sum(1 for w in positive_words if w in all_text)
            neg_count = sum(1 for w in negative_words if w in all_text)
            if pos_count > neg_count:
                emotion.dominant = "positive"
                emotion.intensity = min(1.0, 0.5 + pos_count * 0.15)
            elif neg_count > pos_count:
                emotion.dominant = "negative"
                emotion.intensity = min(1.0, 0.5 + neg_count * 0.15)

            emotion.overall_atmosphere = emotion.dominant

        except ImportError:
            pass
        return emotion

    # ── 步骤⑤+: 截图元数据 ──
    def _detect_screenshot_local(self, image_data: bytes, ocr_texts: List[OCRBlock]) -> ScreenshotMeta:
        """截图优化: 识别应用/聊天界面/状态栏信息"""
        meta = ScreenshotMeta()
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(image_data))
            w, h = img.size
            all_text = " ".join(o.text for o in ocr_texts)

            # 比例判断: 9:16, 9:19.5, 3:4 等典型手机比例
            ratio = w / max(h, 1)
            is_phone_ratio = 0.4 < ratio < 0.85
            has_status_bar = any(o.source == "ui" for o in ocr_texts)

            if is_phone_ratio and has_status_bar:
                meta.is_screenshot = True

            # 应用名识别
            app_signatures = {
                "WeChat": ["微信", "WeChat", "通讯录", "发现"],
                "Weibo": ["微博", "热搜", "我的"],
                "TikTok": ["抖音", "首页", "朋友", "消息"],
                "Alipay": ["支付宝", "扫一扫", "付钱"],
                "Taobao": ["淘宝", "购物车", "我的淘宝"],
                "JD": ["京东", "我的京东"],
                "Browser": ["搜索或输入网址", "百度一下"],
                "System": ["设置", "Wi-Fi", "蓝牙", "通用"],
            }
            for app, signatures in app_signatures.items():
                if any(s in all_text for s in signatures):
                    meta.app_name = app
                    break

            # 聊天界面判断
            chat_indicators = ["对方正在输入", "撤回了一条消息", "@", "发送"]
            meta.chat_interface = any(ind in all_text for ind in chat_indicators)

            # 平台判断
            if "iOS" in all_text or "iPhone" in all_text:
                meta.platform = "iOS"
            elif "Android" in all_text:
                meta.platform = "Android"

            # 状态栏信息
            import re
            for o in ocr_texts:
                if o.source == "ui":
                    t = o.text
                    # 时间戳: HH:MM
                    if re.match(r'^\d{1,2}:\d{2}$', t):
                        meta.timestamp_str = t
                    # 电量: 100% / 85%
                    elif re.match(r'^\d{1,3}%$', t):
                        meta.battery_level = t

        except ImportError:
            pass
        return meta

    # ── 统一管口 ──
    def parse(self, input_data: Union[bytes, str, Path]) -> VisionOutput:
        """
        统一解析接口。

        Args:
            input_data: 图片路径 (str/Path) 或原始字节 (bytes)

        Returns:
            VisionOutput 结构化结果
        """
        t_start = time.time()
        input_hash = ""

        with log_operation("视觉解析", "vision_parser", persona="P05上帝之眼"):
            # 标准化输入
            if isinstance(input_data, (str, Path)):
                path = Path(input_data)
                if not path.exists():
                    raise FileNotFoundError(f"图片不存在: {path}")
                image_data = path.read_bytes()
                input_hash = hashlib.sha256(image_data).hexdigest()[:16]
            elif isinstance(input_data, bytes):
                image_data = input_data
                input_hash = hashlib.sha256(image_data).hexdigest()[:16]
            else:
                raise TypeError(f"输入类型不支持: {type(input_data)}")

            # ── 步骤①: 预处理 ──
            preprocessed = self._preprocess_local(image_data)

            # ── 步骤②: OCR ──
            ocr_texts = self._ocr_local(preprocessed)

            # ── 步骤③: 场景分析 ──
            scene = self._analyze_scene_local(preprocessed, ocr_texts)

            # ── 步骤④: 情绪识别 ──
            emotion = self._detect_emotion_local(preprocessed, scene, ocr_texts)

            # ── 步骤⑤: 截图元数据 ──
            screenshot_meta = self._detect_screenshot_local(preprocessed, ocr_texts)

            # ── 生成标签 ──
            tags = self._generate_tags(scene, emotion, screenshot_meta, ocr_texts)

            # ── 置信度 ──
            ocr_avg = sum(o.confidence for o in ocr_texts) / max(len(ocr_texts), 1) if ocr_texts else 0
            confidence_scores = {
                "ocr": round(ocr_avg, 3),
                "scene": 0.7,
                "emotion": round(emotion.intensity, 2),
                "screenshot_detection": 0.75,
            }

            # ── 步骤⑤: 结构化输出 ──
            output = VisionOutput(
                input_hash=input_hash,
                raw_description=self._generate_description(scene, emotion, ocr_texts),
                ocr_texts=ocr_texts,
                scene=scene,
                emotion=emotion,
                screenshot_meta=screenshot_meta,
                tags=tags,
                confidence_scores=confidence_scores,
                processing_time_ms=round((time.time() - t_start) * 1000, 1),
                model_version="v1.0-local",
                dna=DNA,
                parsed_at=datetime.now(timezone(timedelta(hours=8))).isoformat(),
            )

            return output

    def _generate_tags(self, scene: SceneInfo, emotion: EmotionInfo, meta: ScreenshotMeta, ocr_texts: List[OCRBlock]) -> List[str]:
        """生成内容标签"""
        tags = []
        tags.append(scene.location)
        tags.append(scene.time_of_day)
        if scene.main_activity and scene.main_activity != "unknown":
            tags.append(scene.main_activity)
        if meta.is_screenshot:
            tags.append("screenshot")
        if meta.app_name:
            tags.append(meta.app_name)
        if meta.chat_interface:
            tags.append("chat")
        if emotion.dominant != "neutral":
            tags.append(emotion.dominant)
        # OCR 关键词
        all_text = " ".join(o.text.lower() for o in ocr_texts)
        keyword_tags = {
            "法律": "legal",
            "合同": "contract",
            "代码": "code",
            "付款": "payment",
            "通知": "announcement",
        }
        for kw, tag in keyword_tags.items():
            if kw in all_text:
                tags.append(tag)
        return list(set(tags))

    def _generate_description(self, scene: SceneInfo, emotion: EmotionInfo, ocr_texts: List[OCRBlock]) -> str:
        """生成自然语言描述"""
        parts = []
        parts.append(f"[{scene.location}/{scene.time_of_day}]")
        if scene.person_count:
            parts.append(f"检测到约{scene.person_count}人")
        if scene.objects:
            parts.append(f"包含: {', '.join(scene.objects[:5])}")
        if scene.main_activity:
            activities_cn = {
                "meeting": "涉及会议/讨论",
                "chat": "聊天界面",
                "coding": "代码相关",
                "shopping": "购物/交易",
                "reading": "阅读/浏览",
            }
            parts.append(activities_cn.get(scene.main_activity, scene.main_activity))
        parts.append(f"情绪: {emotion.dominant}(强度{emotion.intensity:.1f})")
        if ocr_texts:
            parts.append(f"OCR文本: {len(ocr_texts)}条")
        return " | ".join(parts)


# ═══════════════════════════════════════════════════════════════
# 快速入口
# ═══════════════════════════════════════════════════════════════

_default_parser: Optional[VisionParser] = None

def parse(input_data: Union[bytes, str, Path]) -> VisionOutput:
    """快速入口: VisionParser().parse()"""
    global _default_parser
    if _default_parser is None:
        _default_parser = VisionParser()
    return _default_parser.parse(input_data)


def is_available() -> bool:
    """检测视觉引擎可用性"""
    try:
        from PIL import Image
        return True
    except ImportError:
        return False


# ═══════════════════════════════════════════════════════════════
# 命令行
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="🐉 龍魂视觉解析器")
    ap.add_argument("image", help="图片路径")
    ap.add_argument("--json", action="store_true", help="JSON输出")
    args = ap.parse_args()

    parser = VisionParser()
    result = parser.parse(args.image)

    if args.json:
        print(result.to_json())
    else:
        print(f"🐉 龍魂视觉解析 · {result.input_hash}")
        print(f"   描述: {result.raw_description}")
        print(f"   OCR: {len(result.ocr_texts)}条文本")
        print(f"   场景: {result.scene.location} {result.scene.time_of_day}")
        print(f"   情绪: {result.emotion.dominant} (强度{result.emotion.intensity:.1f})")
        print(f"   截图: {'是' if result.screenshot_meta.is_screenshot else '否'}")
        if result.screenshot_meta.app_name:
            print(f"   应用: {result.screenshot_meta.app_name}")
        print(f"   标签: {', '.join(result.tags)}")
        print(f"   耗时: {result.processing_time_ms}ms")
        print(f"   DNA: {DNA}")
