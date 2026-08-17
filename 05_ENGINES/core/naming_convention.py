#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-NAMING-CONVENTION-v2.2
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
"""
龍魂·命名即架构引擎 v2.2
─────────────────────────
四层命名法焊死为代码本能。任何组件生成文件/标签/事件时，
必须调用 NameParser.generate_name() 和 NameParser.validate_name()。
不按规矩命名的，无法注册。

用法:
  from engines.core.naming_convention import NameParser
  np = NameParser()
  name = np.generate(physical="LH", identity="UID9622", dna=..., action="行为审计", version="v2.2")
  valid, reason = np.validate(name)
  
行为DNA标签支持:
  7F-{P|F|T|E|C|R|A|X|Y|Z}-{状态}
  MODE-{防御型失信|外耗型守信|内耗型自毁|稳定型自律|波动型摇摆}
  EVT-{承诺|兑现|失信|解释|认错|其他}
  EMO-{心甘情愿|敷衍|甩脸|麻木}
  T-{日|周|月|季|年}
  SPACE-{今生|来世|往生}
  AUTH-L{1|2|3|4}-{行为|语义|交叉|画像}
"""

import re
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Tuple, Optional, List, Dict
from enum import Enum
from dataclasses import dataclass

CST = timezone(timedelta(hours=8))

# ━━━ 四层结构 ━━━
# [物理层]-[身份层]-[主权层]-[执行层]
# LH-UID9622-龍芯⚡️{干支}·{卦}-{动作}-v{版本}.{ext}

# 四层正则（用于解析已有名称）
FOUR_LAYER_RE = re.compile(
    r'^([A-Z]{2,5})-'          # 物理层: LH / CNSH / SCT 等
    r'(UID\d+|SYS|PUB)-'       # 身份层: UID9622 / SYS / PUB
    r'(龍芯?[\u26a1\ufe0f]*[^-\s]+)-'  # 主权层: 龍芯⚡️干支·卦 或 龍芯⚡️DNA片段
    r'(.+?)-'                   # 执行层: 动作/功能
    r'v([\d.]+)'                # 版本
    r'(?:\.(.+))?$'             # 扩展名
)

# 行为DNA标签正则集
BEHAVIOR_LABEL_PATTERNS = {
    '七因子': re.compile(r'7F-([PFTCERAXYZ])-([^\s,，]+)', re.IGNORECASE),
    '行为模式': re.compile(r'MODE-(防御型失信|外耗型守信|内耗型自毁|稳定型自律|波动型摇摆)'),
    '事件类型': re.compile(r'EVT-(承诺|兑现|失信|解释|认错|其他)'),
    '情绪标签': re.compile(r'EMO-(心甘情愿|敷衍|甩脸|麻木|愤怒|平静|焦虑|兴奋)'),
    '审计周期': re.compile(r'T-(日|周|月|季|年)'),
    '空间层级': re.compile(r'SPACE-(今生|来世|往生)'),
    '数据主权': re.compile(r'AUTH-L([1-4])-(行为|语义|交叉|画像)'),
}

# 七因子标签定义
SEVEN_FACTOR_DEFS = {
    'P': {'name': '承诺存在', 'values': ['有承诺', '无承诺']},
    'F': {'name': '执行结果', 'values': ['已兑现', '未兑现', '部分兑现']},
    'T': {'name': '时效偏差', 'values': None},  # 数值
    'E': {'name': '执行情绪', 'values': ['心甘情愿', '敷衍', '甩脸', '麻木']},
    'C': {'name': '成本计量', 'values': None},  # 数值
    'R': {'name': '重复失信', 'values': None},  # 数值
    'A': {'name': '受众指向', 'values': ['为自己', '为伴侣', '为家人', '为外人', '为公众']},
    'X': {'name': '解释倾向', 'values': ['爱解释', '不解释', '真认', '无所谓']},
    'Y': {'name': '认错模式', 'values': ['真改', '硬扛', '无所谓', '无反应']},
    'Z': {'name': '行为波动率', 'values': None},  # 数值
}


@dataclass
class ParsedName:
    """四层命名解析结果"""
    physical: str        # LH / CNSH / SCT
    identity: str        # UID9622 / SYS / PUB
    sovereignty: str     # 龍芯⚡️干支·卦
    action: str          # 动作/功能
    version: str         # v2.2
    extension: str       # md / py / json
    dna_raw: str         # 完整主权层
    
    # 行为DNA标签（可选，从内容中提取）
    behavior_labels: Dict[str, List[str]] = None
    
    def __post_init__(self):
        if self.behavior_labels is None:
            self.behavior_labels = {}
    
    def is_valid(self) -> bool:
        return all([self.physical, self.identity, self.sovereignty, self.action, self.version])
    
    def to_filename(self) -> str:
        base = f"{self.physical}-{self.identity}-{self.sovereignty}-{self.action}-v{self.version}"
        if self.extension:
            base += f".{self.extension}"
        return base


class 命名层(str, Enum):
    物理层 = "物理层"
    身份层 = "身份层"
    主权层 = "主权层"
    执行层 = "执行层"


class NameParser:
    """四层命名法解析器·生成·验证"""
    
    # 有效的物理层前缀
    PHYSICAL_PREFIXES = {'LH', 'CNSH', 'SCT', 'LONGHUN', 'AI'}
    
    # 有效的身份标识
    IDENTITY_PREFIXES = {'UID9622', 'SYS', 'PUB', 'AI'}
    
    def __init__(self):
        self._validation_errors: List[Tuple[命名层, str]] = []
    
    # ━━━ 命名生成 ━━━
    
    def generate(
        self,
        physical: str = "LH",
        identity: str = "UID9622",
        sovereignty: str = None,
        action: str = "",
        version: str = "v1.0",
        extension: str = "md",
        dna_date: str = None,
        hexagram: str = None,
    ) -> str:
        """
        按四层命名法生成完整名称。
        
        若未提供 sovereignty，自动用当前时间干支生成 DNA。
        """
        if sovereignty is None:
            sovereignty = self._auto_dna(dna_date, hexagram)
        
        base = f"{physical}-{identity}-{sovereignty}-{action}-{version}"
        if extension:
            base += f".{extension}"
        return base
    
    def generate_filename(
        self,
        action: str,
        version: str = "v1.0",
        extension: str = "md",
        identity: str = "UID9622",
    ) -> str:
        """快捷：生成标准 LH 文件名"""
        return self.generate(
            physical="LH",
            identity=identity,
            action=action,
            version=version,
            extension=extension,
        )
    
    def _auto_dna(self, date_str: str = None, hexagram: str = None) -> str:
        """自动生成龍芯⚡️DNA主权标签"""
        try:
            now = datetime.now(CST)
            if date_str:
                天干地支 = 干支.from_date_str(date_str)
            else:
                天干地支 = 干支.from_datetime(now)
            卦名 = hexagram or self._auto_hexagram(now)
            return f"龍芯⚡️{天干地支}·{卦名}"
        except Exception:
            # 降级：使用简化格式
            ds = date_str or datetime.now(CST).strftime('%Y-%m-%d')
            return f"龍芯⚡️{ds}"
    
    @staticmethod
    def _auto_hexagram(dt: datetime) -> str:
        """根据日期自动选卦（简化的六十四卦映射）"""
        hexagrams = [
            "乾", "坤", "屯", "蒙", "需", "讼", "师", "比",
            "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
            "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
            "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
            "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
            "损", "益", "夬", "姤", "萃", "升", "困", "井",
            "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
            "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济",
        ]
        idx = (dt.year + dt.month * 31 + dt.day * 7) % 64
        return hexagrams[idx]
    
    # ━━━ 命名解析 ━━━
    
    def parse(self, name: str) -> Optional[ParsedName]:
        """解析四层命名，返回 ParsedName 或 None"""
        m = FOUR_LAYER_RE.search(name)
        if not m:
            return None
        
        return ParsedName(
            physical=m.group(1),
            identity=m.group(2),
            sovereignty=m.group(3),
            action=m.group(4),
            version=m.group(5),
            extension=m.group(6) or "",
            dna_raw=m.group(3),
        )
    
    # ━━━ 命名验证 ━━━
    
    def validate(self, name: str) -> Tuple[bool, str]:
        """
        验证命名是否符合四层命名法。
        返回 (是否通过, 原因说明)
        """
        self._validation_errors = []
        parsed = self.parse(name)
        
        if parsed is None:
            return False, "❌ 格式不符：无法解析为四层命名法。正确格式: [物理层]-[身份层]-[主权层]-[执行层]-v[版本]"
        
        # 物理层校验
        if parsed.physical not in self.PHYSICAL_PREFIXES:
            self._validation_errors.append(
                (命名层.物理层, f"未知物理层前缀 '{parsed.physical}'，有效值: {self.PHYSICAL_PREFIXES}"))
        
        # 身份层校验
        valid_id = False
        for prefix in self.IDENTITY_PREFIXES:
            if parsed.identity.startswith('UID') or parsed.identity in self.IDENTITY_PREFIXES:
                valid_id = True
                break
        if not valid_id:
            self._validation_errors.append(
                (命名层.身份层, f"无效身份标识 '{parsed.identity}'"))
        
        # 主权层校验（必须有龍芯⚡️）
        if '龍芯' not in parsed.sovereignty and '龍芯' not in parsed.sovereignty:
            self._validation_errors.append(
                (命名层.主权层, "主权层必须包含「龍芯」标识"))
        
        # 执行层校验
        if len(parsed.action) < 2:
            self._validation_errors.append(
                (命名层.执行层, f"执行层动作过短: '{parsed.action}'"))
        
        if self._validation_errors:
            details = "; ".join(f"[{layer.value}] {err}" for layer, err in self._validation_errors)
            return False, f"🟡 校验失败: {details}"
        
        return True, f"🟢 四层命名法校验通过: {parsed.to_filename()}"
    
    def validate_or_raise(self, name: str) -> str:
        """验证命名，不通过则抛出 ValueError"""
        valid, reason = self.validate(name)
        if not valid:
            raise ValueError(f"命名校验失败: {reason}")
        return name
    
    # ━━━ 行为DNA标签 ━━━
    
    @staticmethod
    def extract_behavior_labels(text: str) -> Dict[str, List[str]]:
        """
        从文本中提取行为DNA标签。
        
        返回: {标签类别: [匹配值列表]}
        """
        labels: Dict[str, List[str]] = {}
        for category, pattern in BEHAVIOR_LABEL_PATTERNS.items():
            matches = pattern.findall(text)
            if matches:
                if isinstance(matches[0], tuple):
                    labels[category] = [f"{m[0]}-{m[1]}" if len(m) > 1 else m[0] for m in matches]
                else:
                    labels[category] = matches
        return labels
    
    @staticmethod
    def validate_behavior_label(category: str, value: str) -> Tuple[bool, str]:
        """验证单个行为标签是否合法"""
        if category == '七因子':
            m = re.match(r'7F-([PFTCERAXYZ])-([^\s,，]+)', value, re.IGNORECASE)
            if not m:
                return False, f"无效七因子标签: {value}"
            factor = m.group(1).upper()
            val = m.group(2)
            if factor not in SEVEN_FACTOR_DEFS:
                return False, f"未知七因子: {factor}"
            # 若有限定值，检查
            allowed = SEVEN_FACTOR_DEFS[factor]['values']
            if allowed and val not in allowed:
                return False, f"七因子 {factor} 值 '{val}' 不在允许范围: {allowed}"
            return True, f"🟢 七因子 {factor}='{val}'"
        
        pattern = BEHAVIOR_LABEL_PATTERNS.get(category)
        if not pattern:
            return False, f"未知标签类别: {category}"
        if not pattern.fullmatch(value):
            return False, f"标签 '{value}' 不符合类别 '{category}' 的格式"
        return True, f"🟢 {category}: {value}"
    
    @staticmethod
    def generate_behavior_dna(labels: Dict[str, List[str]], date_str: str = None) -> str:
        """根据行为标签生成行为DNA"""
        date_str = date_str or datetime.now(CST).strftime('%Y-%m-%d')
        serialized = json.dumps(labels, sort_keys=True, ensure_ascii=False)
        digest = hashlib.sha256(serialized.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{date_str}-BEHAVIOR-DNA-{digest}"
    
    # ━━━ 报告 ━━━
    
    def report(self, name: str) -> str:
        """详细的命名分析报告"""
        parsed = self.parse(name)
        if not parsed:
            return f"❌ 无法解析: {name}"
        
        valid, reason = self.validate(name)
        lines = [
            f"═══ 命名分析报告 ═══",
            f"  输入: {name}",
            f"  物理层: {parsed.physical}",
            f"  身份层: {parsed.identity}",
            f"  主权层: {parsed.sovereignty}",
            f"  执行层: {parsed.action}",
            f"  版本号: v{parsed.version}",
            f"  扩展名: {parsed.extension or '(无)'}",
            f"  验证: {reason}",
        ]
        if parsed.behavior_labels:
            lines.append(f"  行为标签: {json.dumps(parsed.behavior_labels, ensure_ascii=False)}")
        
        return '\n'.join(lines)


# ━━━ 干支自动计算 ━━━

class 干支:
    """天干地支计算器（极简版·无外部依赖）"""
    天干 = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    地支 = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    @classmethod
    def from_datetime(cls, dt: datetime) -> str:
        """从 datetime 生成年柱·月柱·日柱"""
        年干 = cls.天干[(dt.year - 4) % 10]
        年支 = cls.地支[(dt.year - 4) % 12]
        
        # 月柱：以寅月为正月（立春约2月4日），简化版
        month_idx = dt.month
        月干_idx = ((dt.year - 4) % 10 * 2 + month_idx - 1) % 10
        月干 = cls.天干[月干_idx]
        月支 = cls.地支[(month_idx + 1) % 12]
        
        # 日柱：简化公式
        base_date = datetime(1900, 1, 1)
        days_diff = (dt.date() - base_date.date()).days
        日干 = cls.天干[days_diff % 10]
        日支 = cls.地支[days_diff % 12]
        
        return f"{年干}{年支}·{月干}{月支}·{日干}{日支}"
    
    @classmethod
    def from_date_str(cls, date_str: str) -> str:
        """从 'YYYY-MM-DD' 或 'YYYY-MM-DDTHH:MM' 生成干支"""
        try:
            dt = datetime.fromisoformat(date_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=CST)
            return cls.from_datetime(dt)
        except Exception:
            return date_str  # 降级：返回原字符串


# ━━━ 便利函数（供外部直接调用）━━━

_parser = NameParser()

def 命名(*args, **kwargs) -> str:
    """快捷命名生成"""
    return _parser.generate(*args, **kwargs)

def 验证(name: str) -> Tuple[bool, str]:
    """快捷验证"""
    return _parser.validate(name)

def 解析(name: str) -> Optional[ParsedName]:
    """快捷解析"""
    return _parser.parse(name)

def 提取行为标签(text: str) -> Dict[str, List[str]]:
    """从文本提取行为DNA标签"""
    return NameParser.extract_behavior_labels(text)


# ━━━ 测试 ━━━

def 运行测试():
    import json as _json
    通过 = 0
    失败 = 0
    
    # 测试1: 生成
    name = _parser.generate(action="行为审计", version="v2.2", extension="md")
    assert name.startswith("LH-UID9622-龍芯"), f"生成失败: {name}"
    通过 += 1
    
    # 测试2: 验证合法命名
    valid, _ = _parser.validate("LH-UID9622-龍芯⚡️丙午·乙未·既济-行为审计-v2.2.md")
    assert valid, "合法命名未通过"
    通过 += 1
    
    # 测试3: 验证非法命名（缺少龍芯）
    valid, _ = _parser.validate("LH-UID9622-TEST-action-v1.0.md")
    assert not valid, "非法命名未拦截"
    通过 += 1
    
    # 测试4: 解析
    parsed = _parser.parse("LH-UID9622-龍芯⚡️丙午·乙未·既济-行为审计-v2.2.md")
    assert parsed.physical == "LH"
    assert parsed.identity == "UID9622"
    assert "龍芯" in parsed.sovereignty
    assert parsed.action == "行为审计"
    assert parsed.version == "2.2"
    assert parsed.extension == "md"
    通过 += 1
    
    # 测试5: 行为标签提取
    text = "用户说：承诺今晚回家吃饭 7F-P-有承诺 7F-F-未兑现 7F-E-敷衍 MODE-防御型失信"
    labels = NameParser.extract_behavior_labels(text)
    assert '七因子' in labels
    assert '行为模式' in labels
    assert 'MODE-防御型失信' in labels.get('行为模式', []) or any('防御型失信' in l for l in labels.get('行为模式', []))
    通过 += 1
    
    # 测试6: 行为DNA生成
    labels = {'七因子': ['P-有承诺', 'F-未兑现'], '行为模式': ['防御型失信']}
    dna = NameParser.generate_behavior_dna(labels)
    assert dna.startswith("#龍芯⚡️"), f"行为DNA生成失败: {dna}"
    assert "BEHAVIOR-DNA" in dna
    通过 += 1
    
    # 测试7: 多标签提取
    text2 = "EVT-承诺 SPACE-今生 AUTH-L1-行为 T-日 7F-A-为伴侣"
    labels2 = NameParser.extract_behavior_labels(text2)
    assert len(labels2) >= 4, f"多标签提取不足: {_json.dumps(labels2, ensure_ascii=False)}"
    通过 += 1
    
    # 测试8: 干支生成
    gz = 干支.from_date_str("2026-07-24")
    assert "·" in gz, f"干支格式错误: {gz}"
    通过 += 1
    
    print(f"\n{'✅' if 通过 == 8 else '🟡'} 命名引擎: {通过}/8 通过")
    return 通过 == 8


if __name__ == '__main__':
    import json
    import sys
    
    if '--test' in sys.argv or '-t' in sys.argv:
        运行测试()
    elif '--demo' in sys.argv:
        np = NameParser()
        examples = [
            ("行为审计协议", "LH-UID9622-龍芯⚡️丙午·乙未·既济-行为审计-v2.2.md"),
            ("七因子快照", "LH-UID9622-龍芯⚡️丙午·乙未·既济-七因子快照-v1.0.json"),
            ("个人画像", "LH-UID9622-龍芯⚡️丙午·乙未·既济-个人画像-v1.0.json.enc"),
        ]
        for action, expected_style in examples:
            name = np.generate(action=action, version="v2.2" if "审计" in action else "v1.0",
                              extension=expected_style.rsplit('.', 1)[-1])
            valid, reason = np.validate(name)
            print(f"  {'✅' if valid else '🟡'} {name[:60]}... → {reason}")
        
        # 行为标签演示
        print("\n── 行为DNA标签提取演示 ──")
        sample_text = "老大说：今晚8点前搞定部署 EVT-承诺 7F-P-有承诺 7F-F-已兑现 7F-E-心甘情愿 7F-A-为老大 MODE-稳定型自律 T-日 SPACE-今生 AUTH-L1-行为"
        labels = NameParser.extract_behavior_labels(sample_text)
        print(f"  输入: {sample_text[:80]}...")
        print(f"  提取: {json.dumps(labels, ensure_ascii=False, indent=2)}")
    else:
        # 快速自检
        np = NameParser()
        name = np.generate(action="test")
        valid, reason = np.validate(name)
        print(f"命名引擎就绪: {reason}")
