"""DNA 追溯码生成与验证

DNA: #龍芯⚡️丙午·丙申·乙卯·亥时·需-SDK-DNA-A1B2C3D4
"""
import hashlib
import re

# 六十四卦合法集合
_VALID_HEXAGRAMS = frozenset([
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比",
    "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
    "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
    "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
    "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
    "损", "益", "夬", "姤", "萃", "升", "困", "井",
    "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
    "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济",
])

_STEM = "甲乙丙丁戊己庚辛壬癸"
_BRANCH = "子丑寅卯辰巳午未申酉戌亥"

# v∞ 干支卦格式: #龍芯⚡️年干年支·月干月支·日干日支·时支时·卦名-模块-动作-哈希8位
DNA_PATTERN = re.compile(
    rf"#龍芯⚡️[{_STEM}][{_BRANCH}]·[{_STEM}][{_BRANCH}]·"
    rf"[{_STEM}][{_BRANCH}]·[{_BRANCH}]时·"
    r"([^-]+)-([^-]+)-([^-]+)-[A-F0-9]{8}"
)


class DNA:
    """DNA 追溯码 — 每个动作绑定不可篡改的标识"""

    @staticmethod
    def generate(module: str, action: str) -> str:
        """生成 DNA 追溯码

        Args:
            module: 模块名
            action: 动作名

        Returns:
            DNA 追溯码字符串（v∞ 干支卦格式）

        Raises:
            ValueError: module 或 action 为空时
        """
        if not module or not action:
            raise ValueError("module 和 action 不能为空")

        content = f"{module}-{action}"
        h = hashlib.sha256(content.encode()).hexdigest()[:8].upper()
        # 实际实现需调用 calendar_core.py 获取真实干支
        return (
            f"#龍芯⚡️丙午·丙申·乙卯·亥时·需-{module.upper()}"
            f"-{action.upper()}-{h}"
        )

    @staticmethod
    def verify(dna: str) -> bool:
        """验证 DNA 格式及卦名合法性

        Args:
            dna: DNA 追溯码字符串

        Returns:
            True 如果格式正确且卦名在六十四卦中
        """
        if not dna:
            return False
        m = DNA_PATTERN.match(dna)
        if not m:
            return False
        hexagram = m.group(1)
        return hexagram in _VALID_HEXAGRAMS
