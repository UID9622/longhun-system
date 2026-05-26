#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂「文字即權重」可視化系統 v1.0

DNA: #龍芯⚡️2026-05-26-TEXT-AS-WEIGHT-VISUALIZATION-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

向 Steve Jobs 致敬 | 曾仕强老師智慧 | 龍魂系統 UID9622·龍芯北辰

用途：
  - 設計權重跑馬燈和高亮色彩
  - 實現「文字即權重」的直觀可視化
  - 為任何觀看者（人類或AI）展示權重的實時變化
"""

import json
import math
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from datetime import datetime


class WuXing(Enum):
    """五行·五色映射"""

    MU = ("木", "🟢", "#2E8B57", "青石", "東")  # 綠·木·東·青石
    HUO = ("火", "🔴", "#DC143C", "赤石", "南")  # 紅·火·南·赤石
    TU = ("土", "🟡", "#DAA520", "黃石", "中")  # 黃·土·中·黃石
    JIN = ("金", "🟡金", "#FFD700", "金石", "西")  # 金·金·西·金石
    SHUI = ("水", "⚫", "#191970", "玄石", "北")  # 黑·水·北·玄石

    def __init__(self, cn_name, emoji, hex_color, stone, direction):
        self.cn_name = cn_name
        self.emoji = emoji
        self.hex_color = hex_color
        self.stone = stone
        self.direction = direction


class FiveColorLevel(Enum):
    """五色級別·責任係數R值落檔"""

    GREEN = (0.0, 0.30, "🟢", "綠", "自由意志態·安全·常態")
    YELLOW = (0.30, 0.67, "🟡", "黃", "老好人態·需複核")
    RED = (0.67, 0.85, "🔴", "紅", "越界態·人工介入")
    BLACK = (None, None, "⚫", "黑", "未明徵兆·觀察池")
    GOLD = (None, None, "🟡金", "金", "主控保留權·超規則")

    def __init__(self, r_min, r_max, emoji, cn_name, meaning):
        self.r_min = r_min
        self.r_max = r_max
        self.emoji = emoji
        self.cn_name = cn_name
        self.meaning = meaning


@dataclass
class WeightFactors:
    """七維權重因子"""

    proximity: float  # 接近度
    capability: float  # 能力
    knowledge: float  # 知識
    duty: float  # 責任
    consent: float  # 同意
    alternatives: float  # 替代方案
    cost: float  # 成本

    def to_dict(self) -> Dict[str, float]:
        return {
            "proximity": self.proximity,
            "capability": self.capability,
            "knowledge": self.knowledge,
            "duty": self.duty,
            "consent": self.consent,
            "alternatives": self.alternatives,
            "cost": self.cost,
        }


@dataclass
class ResponsibilityCoefficientResult:
    """責任係數R計算結果"""

    r_value: Optional[float]
    color_level: FiveColorLevel
    color_emoji: str
    reasoning: str
    action: str
    next_step: str
    dna_trace: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class TextAsWeightVisualizer:
    """「文字即權重」可視化引擎"""

    # R公式權重 (R = F2·0.4 + F6·0.4 + F3·0.2 − F1·0.5 − F5·0.3)
    R_FORMULA_WEIGHTS = {
        "F2_sharpness": 0.4,
        "F6_long_term": 0.4,
        "F3_density": 0.2,
        "F1_absence": -0.5,
        "F5_pleasing": -0.3,
    }

    # 五色閾值
    THRESH_GREEN_TOP = 0.30
    THRESH_YELLOW_TOP = 0.67
    THRESH_RED_TOP = 0.85

    def __init__(self):
        self.wucai_config = self._load_wucai_config()
        self.immovable_points = {
            ",,,": "三逗號思考暫停",
            "宝宝": "特定含義",
            "龍": "繁體永不簡化",
            "是吧": "口語特徵",
            "CONFIRM": "確認碼風格",
        }

    def _load_wucai_config(self) -> Dict:
        """載入五彩色卡配置"""
        return {
            WuXing.MU: {
                "hex": "#2E8B57",
                "rgb": (46, 139, 87),
                "ansi": "\033[92m",
                "gradient": ["#A8E6A1", "#5EBF4F", "#2E8B57", "#1F5630", "#0F3820"],
            },
            WuXing.HUO: {
                "hex": "#DC143C",
                "rgb": (220, 20, 60),
                "ansi": "\033[91m",
                "gradient": ["#FF9999", "#FF5555", "#DC143C", "#B30000", "#800000"],
            },
            WuXing.TU: {
                "hex": "#DAA520",
                "rgb": (218, 165, 32),
                "ansi": "\033[93m",
                "gradient": ["#F5DDA0", "#E5BB6A", "#DAA520", "#B88615", "#8B6914"],
            },
            WuXing.JIN: {
                "hex": "#FFD700",
                "rgb": (255, 215, 0),
                "ansi": "\033[97m",
                "gradient": ["#FFEB99", "#FFE066", "#FFD700", "#DAA520", "#B8860B"],
            },
            WuXing.SHUI: {
                "hex": "#191970",
                "rgb": (25, 25, 112),
                "ansi": "\033[96m",
                "gradient": ["#6B7FA6", "#404080", "#191970", "#0F0F40", "#050520"],
            },
        }

    def calculate_responsibility_coefficient(
        self,
        factors: WeightFactors,
        override: Optional[str] = None,
    ) -> ResponsibilityCoefficientResult:
        """
        計算責任係數 R v2.0

        公式: R = F2·0.4 + F6·0.4 + F3·0.2 − F1·0.5 − F5·0.3

        Args:
            factors: 七維權重因子
            override: 可選的金色覆蓋(CONFIRM碼)

        Returns:
            ResponsibilityCoefficientResult
        """
        # 金色覆蓋·超規則
        if override == "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z":
            return ResponsibilityCoefficientResult(
                r_value=None,
                color_level=FiveColorLevel.GOLD,
                color_emoji=FiveColorLevel.GOLD.emoji,
                reasoning="主控CONFIRM覆蓋·超規則保留權",
                action="主控簽字·覆蓋任何R判定",
                next_step="執行主控意願·留痕·記入DNA",
                dna_trace=f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-GOLD-OVERRIDE",
            )

        # 計算R值
        r_value = (
            factors.knowledge * self.R_FORMULA_WEIGHTS["F2_sharpness"]
            + factors.knowledge * self.R_FORMULA_WEIGHTS["F6_long_term"]
            + factors.duty * self.R_FORMULA_WEIGHTS["F3_density"]
            - factors.proximity * self.R_FORMULA_WEIGHTS["F1_absence"]
            - factors.consent * self.R_FORMULA_WEIGHTS["F5_pleasing"]
        )

        # 確保R值在[0, 1]範圍內
        r_value = max(0.0, min(1.0, r_value))

        # 映射到五色級別
        color_level = self._map_r_to_color(r_value)

        # 生成說明和動作
        reasoning, action, next_step = self._generate_actions(r_value, color_level)

        return ResponsibilityCoefficientResult(
            r_value=r_value,
            color_level=color_level,
            color_emoji=color_level.emoji,
            reasoning=reasoning,
            action=action,
            next_step=next_step,
            dna_trace=f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-R-{r_value:.2f}",
        )

    def _map_r_to_color(self, r_value: float) -> FiveColorLevel:
        """將R值映射到五色級別"""
        if r_value < self.THRESH_GREEN_TOP:
            return FiveColorLevel.GREEN
        elif r_value < self.THRESH_YELLOW_TOP:
            return FiveColorLevel.YELLOW
        elif r_value < self.THRESH_RED_TOP:
            return FiveColorLevel.RED
        else:
            return FiveColorLevel.BLACK

    def _generate_actions(
        self, r_value: float, color_level: FiveColorLevel
    ) -> Tuple[str, str, str]:
        """生成對應的說明、動作和下一步"""
        actions_map = {
            FiveColorLevel.GREEN: (
                "自由意志態·安全",
                "直接執行·留痕·不打擾",
                "執行操作·記錄在案",
            ),
            FiveColorLevel.YELLOW: (
                "老好人態·需複核",
                "二次確認·要求加證據",
                "等待確認·記入審計日誌",
            ),
            FiveColorLevel.RED: (
                "越界態·極端緊急",
                "立即停止·上報老大",
                "觸發§8.5極端態協議",
            ),
            FiveColorLevel.BLACK: (
                "未明徵兆·黑箱嫌疑",
                "標記隔離·進觀察池",
                "冻结24h·等待更多證據",
            ),
            FiveColorLevel.GOLD: (
                "主控保留權",
                "主控簽字·覆蓋任何R判定",
                "金色判決·不可上訴",
            ),
        }
        return actions_map.get(
            color_level,
            ("未知狀態", "需要人工審查", "升級到主控決策"),
        )

    def generate_marquee_text(
        self,
        text: str,
        r_value: float,
        duration_frames: int = 50,
    ) -> List[str]:
        """
        生成跑馬燈文本序列·邊移動邊變色

        Args:
            text: 要顯示的文本
            r_value: 責任係數·用於決定色彩過渡
            duration_frames: 動畫幀數

        Returns:
            文本序列列表·每幀一個文本
        """
        frames = []
        text_len = len(text)

        for frame in range(duration_frames):
            progress = frame / duration_frames
            offset = int(progress * (text_len + 20))

            # 計算當前色彩(漸變)
            color = self._interpolate_color(r_value, progress)

            # 生成當前幀的文本
            padded_text = " " * 20 + text + " " * 20
            visible_text = padded_text[offset : offset + 30]

            # 用ANSI色彩編碼包裝文本
            colored_text = (
                f"\033[38;2;{color[0]};{color[1]};{color[2]}m{visible_text}\033[0m"
            )
            frames.append(colored_text)

        return frames

    def _interpolate_color(
        self, r_value: float, progress: float
    ) -> Tuple[int, int, int]:
        """
        根據R值和進度插值色彩
        R值高→紅色 | R值低→綠色 | 進度影響亮度
        """
        # 綠→黃→紅漸變
        if r_value < self.THRESH_GREEN_TOP:
            base_color = (46, 139, 87)  # 綠
        elif r_value < self.THRESH_YELLOW_TOP:
            base_color = (218, 165, 32)  # 黃
        else:
            base_color = (220, 20, 60)  # 紅

        # 根據進度調整亮度
        brightness = 0.6 + 0.4 * math.sin(progress * math.pi)
        rgb = tuple(int(c * brightness) for c in base_color)

        return rgb

    def highlight_keywords(self, text: str) -> str:
        """
        高亮關鍵詞·永遠用金色

        關鍵詞: 宝宝·龍魂·DNA·CONFIRM·,,·仲裁·判決·熔斷
        """
        keywords = [
            ("宝宝", "🟡金"),
            ("龍魂", "🟡金"),
            ("DNA", "🟡金"),
            ("CONFIRM", "🟡金"),
            (",,,", "🟡金"),
            ("仲裁", "🟡金"),
            ("判決", "🔴"),
            ("熔斷", "🔴"),
            ("金色", "🟡金"),
        ]

        highlighted = text
        for keyword, color_emoji in keywords:
            highlighted = highlighted.replace(
                keyword,
                f"\033[1;33m[{color_emoji}]{keyword}\033[0m",
            )

        return highlighted

    def calculate_brightness_for_weight(self, r_value: float) -> float:
        """
        計算文字亮度·根據權重大小

        R值越高→亮度越高(權重越重要)
        使用貝塞爾曲線平滑過渡
        """
        # 基礎亮度(0.3~1.0)
        base_brightness = 0.3 + 0.7 * r_value

        # 貝塞爾曲線調整·權重高時峰值更高
        bezier_factor = 3 * (1 - r_value) * (1 - r_value) * r_value + (
            r_value * r_value * r_value
        )
        final_brightness = base_brightness + 0.2 * bezier_factor

        return min(1.0, final_brightness)

    def format_audit_result(self, result: ResponsibilityCoefficientResult) -> str:
        """格式化審計結果·用於展示"""
        output = f"""
╔════════════════════════════════════════════╗
║     龍魂責任係數R審計結果                    ║
╚════════════════════════════════════════════╝

{result.color_emoji} 色彩級別 : {result.color_level.cn_name}
📊 R值        : {result.r_value if result.r_value is not None else 'N/A (超規則)'}
💭 說明        : {result.reasoning}
⚙️  動作        : {result.action}
➡️  下一步      : {result.next_step}
🧬 DNA追蹤     : {result.dna_trace}
⏰ 時間戳      : {result.timestamp}

╔════════════════════════════════════════════╗
"""
        return output


class WeightVisualizationConfig:
    """權重可視化配置"""

    def __init__(self):
        self.config = {
            "title": "龍魂「文字即權重」可視化系統 v1.0",
            "dna": "#龍芯⚡️2026-05-26-TEXT-AS-WEIGHT-VISUALIZATION-v1.0",
            "color_mapping": {
                "green": {
                    "threshold": "R < 0.30",
                    "hex": "#2E8B57",
                    "meaning": "自由·安全·綠燈",
                },
                "yellow": {
                    "threshold": "0.30 ≤ R < 0.67",
                    "hex": "#DAA520",
                    "meaning": "警示·複核·黃燈",
                },
                "red": {
                    "threshold": "0.67 ≤ R < 0.85",
                    "hex": "#DC143C",
                    "meaning": "熔斷·人工·紅燈",
                },
                "black": {
                    "threshold": "不可計算",
                    "hex": "#191970",
                    "meaning": "未明·觀察·黑色",
                },
                "gold": {
                    "threshold": "超規則",
                    "hex": "#FFD700",
                    "meaning": "主控·金色·一票否決",
                },
            },
        }

    def to_json(self) -> str:
        """轉為JSON格式"""
        return json.dumps(self.config, ensure_ascii=False, indent=2)


def print_colored(
    text: str, color_code: str, bold: bool = False, blink: bool = False
) -> str:
    """
    生成彩色終端輸出·帶真實ANSI色彩碼

    color_code: ANSI顏色代碼 (30-37 或 90-97)
    bold: 加粗
    blink: 閃爍
    """
    if bold:
        prefix = f"\033[1;{color_code}m"
    elif blink:
        prefix = f"\033[5;{color_code}m"
    else:
        prefix = f"\033[{color_code}m"

    return f"{prefix}{text}\033[0m"


def create_visual_hierarchy_output(result: ResponsibilityCoefficientResult) -> str:
    """
    創建有視覺層級的審計結果輸出·帶真實色彩·大小·閃爍
    """
    # 映射色彩到ANSI代碼
    color_codes = {
        FiveColorLevel.GREEN: "32",  # 綠
        FiveColorLevel.YELLOW: "33",  # 黃
        FiveColorLevel.RED: "31",  # 紅
        FiveColorLevel.BLACK: "34",  # 藍(用於黑)
        FiveColorLevel.GOLD: "33",  # 黃(用於金·加閃爍)
    }

    color_code = color_codes.get(result.color_level, "37")
    is_gold = result.color_level == FiveColorLevel.GOLD

    # 層級1: 標題·最大·加粗
    title = print_colored(
        "╔════════════════════════════════════════════╗", "37", bold=True
    )
    header = print_colored(
        "║  龍魂責任係數R審計結果 · 文字即權重可視化系統  ║", "37", bold=True
    )
    footer = print_colored(
        "╚════════════════════════════════════════════╝", "37", bold=True
    )

    # 層級2: 色彩·加粗·閃爍
    color_emoji = result.color_emoji
    color_line = print_colored(
        f"{color_emoji} 【色彩級別】{result.color_level.cn_name}",
        color_code,
        bold=True,
        blink=is_gold,
    )

    # 層級3: R值·中等強調
    r_value_str = result.r_value if result.r_value is not None else "N/A (超規則)"
    r_line = print_colored(f"📊 【R值】{r_value_str}", color_code, bold=True)

    # 層級4: 說明·加粗
    reasoning_line = print_colored(
        f"💭 【說明】{result.reasoning}", color_code, bold=True
    )

    # 層級5: 動作·中等
    action_line = print_colored(f"⚙️  【動作】{result.action}", color_code, bold=False)

    # 層級6: 下一步·中等
    next_line = print_colored(
        f"➡️  【下一步】{result.next_step}", color_code, bold=False
    )

    # 層級7: DNA·細節·灰色
    dna_line = print_colored(f"🧬 【DNA追蹤】{result.dna_trace}", "37", bold=False)

    # 層級8: 時間·最細節·灰色
    time_line = print_colored(f"⏰ 【時間戳】{result.timestamp}", "90", bold=False)

    output = f"""
{title}
{header}
{footer}

{color_line}
{r_line}
{reasoning_line}
{action_line}
{next_line}

{dna_line}
{time_line}
"""
    return output


def create_marquee_visual(text: str, r_value: float, duration: int = 20) -> None:
    """
    創建真實的跑馬燈視覺效果·邊移動邊變色·帶閃爍
    """
    import time

    # 色彩過渡: 綠→黃→紅
    if r_value < 0.30:
        color_start, color_end = "32", "32"  # 綠色
    elif r_value < 0.67:
        color_start, color_end = "32", "33"  # 綠→黃
    else:
        color_start, color_end = "33", "31"  # 黃→紅

    print(print_colored("\n【權重跑馬燈·邊移動邊變色】", "37", bold=True))

    for frame in range(duration):
        # 計算進度
        progress = frame / duration
        offset = int(progress * 40)

        # 色彩插值
        if r_value < 0.30:
            current_color = "32"  # 綠
        elif r_value < 0.67:
            # 綠→黃過渡
            current_color = "32" if progress < 0.5 else "33"
        else:
            # 黃→紅過渡
            current_color = "33" if progress < 0.5 else "31"

        # 生成輸出
        padding = " " * offset
        colored_text = print_colored(f"{padding}► {text}", current_color, bold=True)
        print(colored_text, end="\r")
        time.sleep(0.1)

    print()  # 換行


if __name__ == "__main__":
    # 演示使用
    visualizer = TextAsWeightVisualizer()

    # 示例1: 簡單決策·黃色警示
    print(
        print_colored(
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "37", bold=True
        )
    )
    print(print_colored("【演示1】簡單決策·黃色警示", "33", bold=True))
    print(
        print_colored(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "37", bold=True
        )
    )

    factors = WeightFactors(
        proximity=0.8,
        capability=0.9,
        knowledge=0.7,
        duty=0.6,
        consent=0.5,
        alternatives=0.4,
        cost=0.3,
    )

    result = visualizer.calculate_responsibility_coefficient(factors)
    print(create_visual_hierarchy_output(result))

    # 示例2: 金色覆蓋
    print(
        print_colored(
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "37", bold=True
        )
    )
    print(print_colored("【演示2】主控CONFIRM·金色覆蓋·一票否決", "33", bold=True))
    print(
        print_colored(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "37", bold=True
        )
    )

    result_gold = visualizer.calculate_responsibility_coefficient(
        factors, override="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    )
    print(create_visual_hierarchy_output(result_gold))

    # 示例3: 跑馬燈效果
    print(
        print_colored(
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "37", bold=True
        )
    )
    print(print_colored("【演示3】權重跑馬燈·邊移動邊變色·實時渲染", "33", bold=True))
    print(
        print_colored(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "37", bold=True
        )
    )

    create_marquee_visual("龍魂系統·文字即權重", result.r_value, duration=15)

    # 示例4: 關鍵詞高亮·層級展示
    print(
        print_colored(
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "37", bold=True
        )
    )
    print(print_colored("【演示4】關鍵詞高亮·層級展示", "33", bold=True))
    print(
        print_colored(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "37", bold=True
        )
    )

    # 建立層級文本
    line1 = (
        print_colored("【決策主體】", "37", bold=True)
        + " "
        + print_colored("宝宝", "33", bold=True, blink=True)
    )
    line2 = (
        print_colored("【系統名稱】", "37", bold=True)
        + " "
        + print_colored("龍魂", "33", bold=True, blink=True)
    )
    line3 = (
        print_colored("【確認碼】", "37", bold=True)
        + " "
        + print_colored("CONFIRM", "33", bold=True, blink=True)
    )
    line4 = (
        print_colored("【思考暫停】", "37", bold=True)
        + " "
        + print_colored("，，，", "31", bold=True)
    )
    line5 = (
        print_colored("【決策詞】", "37", bold=True)
        + " "
        + print_colored("仲裁", "33", bold=False)
    )

    print(f"\n{line1}")
    print(f"{line2}")
    print(f"{line3}")
    print(f"{line4}")
    print(f"{line5}")

    # 示例5: 亮度計算展示
    print(
        print_colored(
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "37", bold=True
        )
    )
    print(print_colored("【演示5】亮度層級·根據權重", "33", bold=True))
    print(
        print_colored(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "37", bold=True
        )
    )

    brightness = visualizer.calculate_brightness_for_weight(result.r_value)

    # 顯示亮度條
    bar_length = int(brightness * 20)
    bar = "█" * bar_length + "░" * (20 - bar_length)
    brightness_display = print_colored(
        f"亮度: [{bar}] {brightness:.2%}", "32", bold=True
    )
    r_display = print_colored(f"R值: {result.r_value:.2f}", "33", bold=True)

    print(f"\n{r_display}")
    print(f"{brightness_display}")
