#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 CNSH 第一卷 + 第二卷 · 全量交付 v2.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-CNSH-COMPLETE-v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

CNSH = Chinese Semantic Hyperlogic
中文语义超逻辑 · 让中文思维变成可执行代码

第一卷：语言目的 + 20条核心语法 + 解释器 + 编译器模板
第二卷：运行时架构 + 卦机 + 甲骨文算法 + 因果链引擎 + 世界机 + 安全模型

使用方式：
  python3 cnsh_complete.py                    # 交互模式
  python3 cnsh_complete.py --file demo.cns   # 执行文件
  python3 cnsh_complete.py --hexagram 乾     # 推演卦象
  python3 cnsh_complete.py --causal          # 因果链演示
  python3 cnsh_complete.py --world           # 世界机演示
"""

import os
import sys
import re
import json
import math
import time
import random
import hashlib
import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse
import copy

# ============================================================
# 一、配置与常量
# ============================================================

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# 64卦编码（6位二进制）
HEXAGRAM_MAP = {
    "坤": 0b000000, "剥": 0b000001, "比": 0b000010, "观": 0b000011,
    "豫": 0b000100, "晋": 0b000101, "萃": 0b000110, "否": 0b000111,
    "谦": 0b001000, "艮": 0b001001, "蹇": 0b001010, "渐": 0b001011,
    "小过": 0b001100, "旅": 0b001101, "咸": 0b001110, "遁": 0b001111,
    "师": 0b010000, "蒙": 0b010001, "坎": 0b010010, "涣": 0b010011,
    "解": 0b010100, "未济": 0b010101, "困": 0b010110, "讼": 0b010111,
    "升": 0b011000, "蛊": 0b011001, "井": 0b011010, "巽": 0b011011,
    "恒": 0b011100, "鼎": 0b011101, "大过": 0b011110, "姤": 0b011111,
    "复": 0b100000, "颐": 0b100001, "屯": 0b100010, "益": 0b100011,
    "震": 0b100100, "噬嗑": 0b100101, "随": 0b100110, "无妄": 0b100111,
    "明夷": 0b101000, "贲": 0b101001, "既济": 0b101010, "家人": 0b101011,
    "丰": 0b101100, "离": 0b101101, "革": 0b101110, "同人": 0b101111,
    "临": 0b110000, "损": 0b110001, "节": 0b110010, "中孚": 0b110011,
    "归妹": 0b110100, "睽": 0b110101, "兑": 0b110110, "履": 0b110111,
    "泰": 0b111000, "大畜": 0b111001, "需": 0b111010, "小畜": 0b111011,
    "大壮": 0b111100, "大有": 0b111101, "夬": 0b111110, "乾": 0b111111
}

# 反查
HEXAGRAM_NAMES = {v: k for k, v in HEXAGRAM_MAP.items()}

# 卦辞库（简化版）
HEXAGRAM_WORDS = {
    "乾": "元亨利贞。天行健，君子以自强不息。",
    "坤": "元亨，利牝马之贞。厚德载物。",
    "屯": "元亨利贞。刚柔始交而难生。",
    "蒙": "亨。匪我求童蒙，童蒙求我。",
    "需": "有孚，光亨，贞吉。利涉大川。",
    "讼": "有孚，窒惕，中吉，终凶。",
    "师": "贞丈人吉，无咎。",
    "比": "吉。原筮元永贞，无咎。",
    "小畜": "亨。密云不雨，自我西郊。",
    "履": "履虎尾，不咥人，亨。",
    "泰": "小往大来，吉亨。",
    "否": "否之匪人，不利君子贞。",
    "同人": "同人于野，亨。利涉大川。",
    "大有": "元亨。",
    "谦": "亨，君子有终。",
    "豫": "利建侯行师。",
    "随": "元亨利贞，无咎。",
    "蛊": "元亨，利涉大川。",
    "临": "元亨利贞。",
    "观": "盥而不荐，有孚颙若。",
    "噬嗑": "亨，利用狱。",
    "贲": "亨。小利有攸往。",
    "剥": "不利有攸往。",
    "复": "亨。出入无疾。",
    "无妄": "元亨利贞。",
    "大畜": "利贞。",
    "颐": "贞吉。",
    "大过": "栋桡，利有攸往，亨。",
    "坎": "习坎，有孚。",
    "离": "利贞，亨。",
    "咸": "亨，利贞。",
    "恒": "亨，无咎。",
    "遁": "亨，小利贞。",
    "大壮": "利贞。",
    "晋": "康侯用锡马蕃庶。",
    "明夷": "利艰贞。",
    "家人": "利女贞。",
    "睽": "小事吉。",
    "蹇": "利西南，不利东北。",
    "解": "利西南。",
    "损": "有孚，元吉。",
    "益": "利有攸往。",
    "夬": "扬于王庭，孚号有厉。",
    "姤": "女壮，勿用取女。",
    "萃": "亨。王假有庙。",
    "升": "元亨。",
    "困": "亨，贞。",
    "井": "改邑不改井。",
    "革": "己日乃孚。",
    "鼎": "元吉，亨。",
    "震": "亨。震来虩虩。",
    "艮": "艮其背。",
    "渐": "女归吉，利贞。",
    "归妹": "征凶，无攸利。",
    "丰": "亨，王假之。",
    "旅": "小亨。",
    "巽": "小亨。",
    "兑": "亨，利贞。",
    "涣": "亨。王假有庙。",
    "节": "亨。苦节不可贞。",
    "中孚": "豚鱼吉。",
    "小过": "亨，利贞。",
    "既济": "亨小，利贞。",
    "未济": "亨。"
}

# ============================================================
# 二、数据结构
# ============================================================

@dataclass
class ASTNode:
    """抽象语法树节点"""
    type: str
    value: Any
    children: List['ASTNode'] = field(default_factory=list)

@dataclass
class CausalRecord:
    """因果链记录"""
    event: str
    cause: str
    result: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

@dataclass
class WorldEntity:
    """世界实体"""
    name: str
    type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    state: str = "idle"

# ============================================================
# 三、CNSH 词法分析器
# ============================================================

class CNSHLexer:
    """CNSH 词法分析器"""

    @staticmethod
    def tokenize(code: str) -> List[Tuple[str, str]]:
        """将CNSH代码转换为Token流"""
        tokens = []
        lines = code.strip().split('\n')

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('注：'):
                continue

            # 设 x 为 5
            match = re.match(r'^设\s+(\w+)\s+为\s+(.+)$', line)
            if match:
                tokens.append(('SET', match.group(1), match.group(2), line_num))
                continue

            # 若 x 大于 5 则 输出 "ok" 否则 输出 "no"
            match = re.match(r'^若\s+(.+)\s+则\s+(.+?)\s*否则\s*(.+)$', line)
            if match:
                tokens.append(('IF', match.group(1), match.group(2), match.group(3), line_num))
                continue

            # 若 x 大于 5 则 输出 "ok" （无否则）
            match = re.match(r'^若\s+(.+)\s+则\s+(.+)$', line)
            if match:
                tokens.append(('IF_SIMPLE', match.group(1), match.group(2), line_num))
                continue

            # 每当 x 小于 10 执行 设 x 为 x + 1 直到 结束
            match = re.match(r'^每当\s+(.+)\s+执行\s+(.+)\s+直到\s+结束$', line)
            if match:
                tokens.append(('LOOP', match.group(1), match.group(2), line_num))
                continue

            # 以 求和 为法 (a, b): 返回 a + b
            match = re.match(r'^以\s+(\w+)\s+为法\s*\(([^)]*)\)\s*[:：]\s*(.+)$', line)
            if match:
                params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                tokens.append(('FUNC', match.group(1), params, match.group(3), line_num))
                continue

            # 输出 "内容"
            match = re.match(r'^输出\s+"([^"]*)"$', line)
            if match:
                tokens.append(('PRINT', match.group(1), line_num))
                continue

            # 以 人物 记载：名 为 "张三" 年龄 为 20
            match = re.match(r'^以\s+(\w+)\s+记载[:：]$', line)
            if match:
                tokens.append(('OBJECT_START', match.group(1), line_num))
                continue

            # 名 为 "张三"
            match = re.match(r'^(\w+)\s+为\s+(.+)$', line)
            if match:
                tokens.append(('PROPERTY', match.group(1), match.group(2), line_num))
                continue

            # 当前卦 为 乾
            match = re.match(r'^当前卦\s+为\s+(\w+)$', line)
            if match:
                tokens.append(('HEXAGRAM_SET', match.group(1), line_num))
                continue

            # 爻变 三爻
            match = re.match(r'^爻变\s+(\w+)$', line)
            if match:
                tokens.append(('LINE_CHANGE', match.group(1), line_num))
                continue

            # 由 A 以致 B 终 C
            match = re.match(r'^由\s+(.+)\s+以致\s+(.+)\s+终\s+(.+)$', line)
            if match:
                tokens.append(('CAUSAL', match.group(1), match.group(2), match.group(3), line_num))
                continue

            # 卜：预测
            match = re.match(r'^卜[:：]\s*(.+)$', line)
            if match:
                tokens.append(('BU', match.group(1), line_num))
                continue

            # 验 当前路径 是否 合规
            match = re.match(r'^验\s+(.+)\s+是否\s+(.+)$', line)
            if match:
                tokens.append(('YAN', match.group(1), match.group(2), line_num))
                continue

            # 兆：若 输入 异常 则 标记 "预警"
            match = re.match(r'^兆[:：]\s*若\s+(.+)\s+则\s+标记\s+"([^"]*)"$', line)
            if match:
                tokens.append(('ZHAO', match.group(1), match.group(2), line_num))
                continue

            # 象 用户之行为：频率 每日三次 类型 搜索
            match = re.match(r'^象\s+(.+)[：:]\s*(.+)$', line)
            if match:
                tokens.append(('XIANG', match.group(1), match.group(2), line_num))
                continue

            # 辞 当前卦
            match = re.match(r'^辞\s+(.+)$', line)
            if match:
                tokens.append(('CI', match.group(1), line_num))
                continue

            # 系 A 与 B
            match = re.match(r'^系\s+(\w+)\s+与\s+(\w+)$', line)
            if match:
                tokens.append(('XI', match.group(1), match.group(2), line_num))
                continue

            # 命 (方向命令)
            match = re.match(r'^命\s+(.+)$', line)
            if match:
                tokens.append(('MING', match.group(1), line_num))
                continue

            # 卷 数学： (模块定义)
            match = re.match(r'^卷\s+(\w+)[：:]$', line)
            if match:
                tokens.append(('MODULE', match.group(1), line_num))
                continue

            # 对象结束标记
            if line.startswith('结束'):
                tokens.append(('END_OBJECT', line_num))
                continue

            # 函数结束标记
            if line.startswith('返回'):
                match = re.match(r'^返回\s+(.+)$', line)
                if match:
                    tokens.append(('RETURN', match.group(1), line_num))
                continue

            # 无法识别的行
            tokens.append(('UNKNOWN', line, line_num))

        return tokens

# ============================================================
# 四、CNSH 解析器（AST生成）
# ============================================================

class CNSHParser:
    """CNSH 语法解析器"""

    @staticmethod
    def parse(tokens: List) -> List[ASTNode]:
        """将Token流转换为AST"""
        ast = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            tok_type = token[0]

            if tok_type == 'SET':
                ast.append(ASTNode('Assign', {'var': token[1], 'value': token[2]}))
                i += 1

            elif tok_type == 'IF':
                ast.append(ASTNode('If', {
                    'condition': token[1],
                    'then': token[2],
                    'else': token[3]
                }))
                i += 1

            elif tok_type == 'IF_SIMPLE':
                ast.append(ASTNode('If', {
                    'condition': token[1],
                    'then': token[2],
                    'else': None
                }))
                i += 1

            elif tok_type == 'LOOP':
                ast.append(ASTNode('Loop', {
                    'condition': token[1],
                    'body': token[2]
                }))
                i += 1

            elif tok_type == 'FUNC':
                ast.append(ASTNode('Func', {
                    'name': token[1],
                    'params': token[2],
                    'body': token[3]
                }))
                i += 1

            elif tok_type == 'PRINT':
                ast.append(ASTNode('Print', {'value': token[1]}))
                i += 1

            elif tok_type == 'HEXAGRAM_SET':
                ast.append(ASTNode('HexagramSet', {'name': token[1]}))
                i += 1

            elif tok_type == 'LINE_CHANGE':
                ast.append(ASTNode('LineChange', {'line': token[1]}))
                i += 1

            elif tok_type == 'CAUSAL':
                ast.append(ASTNode('Causal', {
                    'event': token[1],
                    'cause': token[2],
                    'result': token[3]
                }))
                i += 1

            elif tok_type == 'BU':
                ast.append(ASTNode('Bu', {'input': token[1]}))
                i += 1

            elif tok_type == 'YAN':
                ast.append(ASTNode('Yan', {'path': token[1], 'check': token[2]}))
                i += 1

            elif tok_type == 'ZHAO':
                ast.append(ASTNode('Zhao', {'condition': token[1], 'warning': token[2]}))
                i += 1

            elif tok_type == 'XIANG':
                ast.append(ASTNode('Xiang', {'name': token[1], 'props': token[2]}))
                i += 1

            elif tok_type == 'CI':
                ast.append(ASTNode('Ci', {'hexagram': token[1]}))
                i += 1

            elif tok_type == 'XI':
                ast.append(ASTNode('Xi', {'a': token[1], 'b': token[2]}))
                i += 1

            elif tok_type == 'MING':
                ast.append(ASTNode('Ming', {'direction': token[1]}))
                i += 1

            elif tok_type == 'MODULE':
                ast.append(ASTNode('Module', {'name': token[1]}))
                i += 1

            else:
                i += 1

        return ast

# ============================================================
# 五、CNSH 卦机（Hexagram Engine）
# ============================================================

class HexagramEngine:
    """64卦状态机"""

    def __init__(self):
        self.current = 0b111111  # 乾
        self.history: List[int] = []
        self.memo: Dict[int, Dict] = {}

    def get_name(self, code: int) -> str:
        return HEXAGRAM_NAMES.get(code, "未知")

    def get_code(self, name: str) -> int:
        return HEXAGRAM_MAP.get(name, 0)

    def set_hexagram(self, name: str) -> None:
        code = self.get_code(name)
        if code is not None:
            self.current = code
            self.history.append(code)

    def line_change(self, line: int) -> int:
        """爻变：翻转第N爻（0-5）"""
        if 0 <= line <= 5:
            self.current ^= (1 << line)
            self.history.append(self.current)
        return self.current

    def get_lines(self, code: int = None) -> List[int]:
        """获取6爻"""
        if code is None:
            code = self.current
        return [(code >> i) & 1 for i in range(6)]

    def get_lines_str(self, code: int = None) -> str:
        lines = self.get_lines(code)
        return ''.join('⚊' if l == 1 else '⚋' for l in reversed(lines))

    def deduce(self, steps: int = 3) -> List[int]:
        """卦序推演"""
        result = []
        current = self.current
        for i in range(steps):
            line = current % 6
            current ^= (1 << line)
            result.append(current)
        return result

    def get_word(self, name: str = None) -> str:
        if name is None:
            name = self.get_name(self.current)
        return HEXAGRAM_WORDS.get(name, "卦辞待考")

    def get_state(self) -> Dict:
        return {
            "current": self.current,
            "name": self.get_name(self.current),
            "lines": self.get_lines_str(),
            "word": self.get_word(),
            "history": self.history[-10:]
        }

# ============================================================
# 六、甲骨文算法（9条可执行）
# ============================================================

class OracleEngine:
    """甲骨文算法引擎 - 9条可执行算法"""

    @staticmethod
    def 卜(input_data: Any) -> Dict:
        """卜：预测 - 基于简单回归/趋势"""
        if isinstance(input_data, (int, float)):
            # 简单预测：基于历史趋势
            trend = input_data * 1.05
            return {
                "type": "预测",
                "input": input_data,
                "prediction": round(trend, 2),
                "confidence": min(1.0, 0.7 + random.random() * 0.25),
                "trend": "上升" if trend > input_data else "下降"
            }
        elif isinstance(input_data, list):
            if len(input_data) >= 2:
                avg = sum(input_data) / len(input_data)
                return {
                    "type": "预测",
                    "input": input_data,
                    "prediction": round(avg * 1.03, 2),
                    "confidence": 0.75,
                    "trend": "平稳"
                }
        return {"type": "预测", "input": input_data, "prediction": "无法预测", "confidence": 0.0}

    @staticmethod
    def 验(path: List, check: str) -> Dict:
        """验：验证路径是否合规"""
        if not path:
            return {"type": "验证", "passed": False, "reason": "空路径"}
        # 简单合规检查
        passed = all(isinstance(p, (int, float, str)) for p in path)
        return {
            "type": "验证",
            "passed": passed,
            "check": check,
            "path_length": len(path),
            "reason": "所有元素合规" if passed else "存在不合规元素"
        }

    @staticmethod
    def 兆(input_data: Any, threshold: float = 0.7) -> Dict:
        """兆：异常信号检测"""
        if isinstance(input_data, (int, float)):
            is_abnormal = abs(input_data) > threshold * 100 or input_data < 0
            return {
                "type": "异常检测",
                "value": input_data,
                "threshold": threshold,
                "is_abnormal": is_abnormal,
                "level": "🔴 预警" if is_abnormal else "🟢 正常",
                "signal": "预警" if is_abnormal else "正常"
            }
        elif isinstance(input_data, list):
            abnormal = [x for x in input_data if isinstance(x, (int, float)) and abs(x) > threshold * 100]
            return {
                "type": "异常检测",
                "total": len(input_data),
                "abnormal_count": len(abnormal),
                "abnormal_items": abnormal[:5],
                "level": "🔴 预警" if len(abnormal) > 0 else "🟢 正常",
                "signal": "预警" if len(abnormal) > 0 else "正常"
            }
        return {"type": "异常检测", "input": input_data, "level": "⚪ 未知"}

    @staticmethod
    def 命(direction: str) -> Dict:
        """命：方向映射"""
        dir_map = {
            "东": {"angle": 0, "element": "木", "color": "青"},
            "南": {"angle": 90, "element": "火", "color": "赤"},
            "西": {"angle": 180, "element": "金", "color": "白"},
            "北": {"angle": 270, "element": "水", "color": "黑"},
            "中": {"angle": 0, "element": "土", "color": "黄"},
            "上": {"angle": 0, "element": "天", "color": "玄"},
            "下": {"angle": 0, "element": "地", "color": "褐"}
        }
        return {
            "type": "方向",
            "direction": direction,
            "mapping": dir_map.get(direction, {"angle": 0, "element": "未知", "color": "灰"}),
            "exists": direction in dir_map
        }

    @staticmethod
    def 爻(state: int, line: int) -> Dict:
        """爻：微变 - 翻转特定位"""
        if not (0 <= line <= 5):
            return {"type": "爻变", "error": "爻位需在0-5之间"}
        new_state = state ^ (1 << line)
        return {
            "type": "爻变",
            "original": state,
            "line": line,
            "new": new_state,
            "hexagram": HEXAGRAM_NAMES.get(new_state, "未知"),
            "binary": format(new_state, '06b')
        }

    @staticmethod
    def 象(data: Any) -> Dict:
        """象：从数据抽象模型"""
        if isinstance(data, list) and len(data) > 0:
            if all(isinstance(x, (int, float)) for x in data):
                return {
                    "type": "建模",
                    "model": "数值分布",
                    "count": len(data),
                    "min": min(data),
                    "max": max(data),
                    "mean": sum(data) / len(data),
                    "std": (sum((x - sum(data)/len(data))**2 for x in data) / len(data)) ** 0.5 if len(data) > 1 else 0
                }
            else:
                return {
                    "type": "建模",
                    "model": "分类分布",
                    "count": len(data),
                    "unique": len(set(data)),
                    "items": list(set(data))[:10]
                }
        return {"type": "建模", "model": "单点", "value": data}

    @staticmethod
    def 辞(hexagram_name: str) -> Dict:
        """辞：解释卦象含义"""
        code = HEXAGRAM_MAP.get(hexagram_name)
        if code is None:
            return {"type": "解释", "error": f"未知卦象: {hexagram_name}"}
        word = HEXAGRAM_WORDS.get(hexagram_name, "卦辞待考")
        lines = [(code >> i) & 1 for i in range(6)]
        return {
            "type": "解释",
            "hexagram": hexagram_name,
            "code": code,
            "binary": format(code, '06b'),
            "lines": ''.join('⚊' if l == 1 else '⚋' for l in reversed(lines)),
            "meaning": word,
            "yang_count": sum(lines),
            "yin_count": 6 - sum(lines)
        }

    @staticmethod
    def 系(a: Any, b: Any) -> Dict:
        """系：建立绑定关系"""
        return {
            "type": "绑定",
            "a": str(a),
            "b": str(b),
            "relation": f"{a} ↔ {b}",
            "active": True
        }

    @staticmethod
    def 卦备忘录(key: str, value: Any = None) -> Dict:
        """卦备忘录：缓存常用结果"""
        if not hasattr(OracleEngine, '_memo_cache'):
            OracleEngine._memo_cache = {}
        if value is not None:
            OracleEngine._memo_cache[key] = value
            return {"type": "备忘录", "action": "存储", "key": key, "value": value}
        return {
            "type": "备忘录",
            "action": "读取",
            "key": key,
            "value": OracleEngine._memo_cache.get(key, "未找到")
        }

# ============================================================
# 七、因果链引擎
# ============================================================

class CausalEngine:
    """因果链引擎 - 中文逻辑核心"""

    def __init__(self):
        self.records: List[CausalRecord] = []
        self.chain: List[Dict] = []

    def record(self, event: str, cause: str, result: str) -> CausalRecord:
        """记录因果关系"""
        record = CausalRecord(event=event, cause=cause, result=result)
        self.records.append(record)
        self.chain.append({
            "event": event,
            "cause": cause,
            "result": result,
            "timestamp": record.timestamp
        })
        return record

    def get_chain(self) -> List[Dict]:
        """获取完整因果链"""
        return self.chain

    def explain(self) -> str:
        """解释因果链"""
        if not self.chain:
            return "无因果链记录"
        lines = []
        for i, record in enumerate(self.chain, 1):
            lines.append(f"{i}. 由「{record['event']}」")
            lines.append(f"   → 以致「{record['cause']}」")
            lines.append(f"   → 终「{record['result']}」")
        return "\n".join(lines)

    def query(self, keyword: str) -> List[Dict]:
        """查询因果链"""
        results = []
        for record in self.chain:
            if keyword in record['event'] or keyword in record['cause'] or keyword in record['result']:
                results.append(record)
        return results

# ============================================================
# 八、世界机（元宇宙引擎）
# ============================================================

class WorldEngine:
    """CNSH 世界机 - 元宇宙核心"""

    def __init__(self):
        self.entities: Dict[str, WorldEntity] = {}
        self.scenes: Dict[str, Dict] = {}
        self.events: List[Dict] = []
        self.state: Dict[str, Any] = {}
        self.logs: List[str] = []

    def create_world(self, name: str, properties: Dict) -> None:
        """创建世界"""
        self.state[name] = properties
        self.logs.append(f"🌍 世界「{name}」已创建")

    def create_entity(self, name: str, entity_type: str, props: Dict) -> WorldEntity:
        """创建实体"""
        entity = WorldEntity(name=name, type=entity_type, properties=props)
        self.entities[name] = entity
        self.logs.append(f"🧬 实体「{name}」已创建 (类型: {entity_type})")
        return entity

    def create_scene(self, name: str, description: str, entities: List[str] = None) -> None:
        """创建场景"""
        self.scenes[name] = {
            "description": description,
            "entities": entities or [],
            "created_at": datetime.datetime.now().isoformat()
        }
        self.logs.append(f"🎬 场景「{name}」已创建")

    def trigger_event(self, event: str, context: Dict) -> Dict:
        """触发事件"""
        record = {
            "event": event,
            "context": context,
            "timestamp": datetime.datetime.now().isoformat(),
            "handled": False
        }
        self.events.append(record)

        # 场景触发检查
        for scene_name, scene in self.scenes.items():
            if event in scene.get("description", ""):
                record["handled"] = True
                self.logs.append(f"⚡ 场景「{scene_name}」已触发")
                return {
                    "status": "triggered",
                    "scene": scene_name,
                    "event": event,
                    "description": scene.get("description", "")
                }

        self.logs.append(f"📌 事件「{event}」已记录")
        return {"status": "recorded", "event": event}

    def get_world_state(self) -> Dict:
        """获取世界状态"""
        return {
            "scenes": list(self.scenes.keys()),
            "entities": list(self.entities.keys()),
            "events": len(self.events),
            "logs": self.logs[-10:],
            "state": self.state
        }

    def run_world(self, steps: int = 3) -> str:
        """运行世界模拟"""
        output = []
        output.append("🌍 世界运行中...")
        for i in range(steps):
            output.append(f"  步骤 {i+1}:")
            if self.entities:
                for name, entity in list(self.entities.items())[:2]:
                    output.append(f"    - {name} ({entity.type}) 状态: {entity.state}")
            if self.scenes:
                for name, scene in list(self.scenes.items())[:2]:
                    output.append(f"    - 场景「{name}」: {scene['description'][:30]}...")
        return "\n".join(output)

# ============================================================
# 九、CNSH 主解释器
# ============================================================

class CNSHInterpreter:
    """CNSH 完整解释器"""

    def __init__(self):
        self.env: Dict[str, Any] = {}
        self.functions: Dict[str, Dict] = {}
        self.objects: Dict[str, Dict] = {}
        self.modules: Dict[str, Dict] = {}
        self.hexagram = HexagramEngine()
        self.oracle = OracleEngine()
        self.causal = CausalEngine()
        self.world = WorldEngine()
        self.output: List[str] = []
        self.debug: bool = False

    def execute(self, ast: List[ASTNode]) -> str:
        """执行AST"""
        self.output = []
        for node in ast:
            self._execute_node(node)
        return '\n'.join(self.output)

    def _execute_node(self, node: ASTNode):
        """执行单个节点"""
        if node.type == 'Assign':
            var = node.value['var']
            val = self._evaluate(node.value['value'])
            self.env[var] = val
            if self.debug:
                self.output.append(f"[DEBUG] {var} = {val}")

        elif node.type == 'Print':
            val = self._evaluate(node.value['value'])
            self.output.append(f"[输出] {val}")

        elif node.type == 'If':
            cond = self._evaluate(node.value['condition'])
            if cond:
                self._execute_expression(node.value['then'])
            elif node.value.get('else'):
                self._execute_expression(node.value['else'])

        elif node.type == 'Loop':
            while self._evaluate(node.value['condition']):
                self._execute_expression(node.value['body'])

        elif node.type == 'Func':
            self.functions[node.value['name']] = {
                'params': node.value['params'],
                'body': node.value['body']
            }

        elif node.type == 'HexagramSet':
            name = node.value['name']
            self.hexagram.set_hexagram(name)
            self.output.append(f"[卦] 当前卦: {name} ({self.hexagram.get_lines_str()})")

        elif node.type == 'LineChange':
            line_str = node.value['line']
            line_map = {"初": 0, "二": 1, "三": 2, "四": 3, "五": 4, "上": 5,
                        "初爻": 0, "二爻": 1, "三爻": 2, "四爻": 3, "五爻": 4, "上爻": 5}
            line = line_map.get(line_str, 0)
            result = self.hexagram.line_change(line)
            self.output.append(f"[爻变] 变{line_str} → {self.hexagram.get_name(result)}")

        elif node.type == 'Causal':
            record = self.causal.record(
                event=node.value['event'],
                cause=node.value['cause'],
                result=node.value['result']
            )
            self.output.append(f"[因果] {record.event} → {record.cause} → {record.result}")

        elif node.type == 'Bu':
            result = self.oracle.卜(self._evaluate(node.value['input']))
            self.output.append(f"[卜] 预测结果: {result.get('prediction', '未知')} (置信度: {result.get('confidence', 0):.0%})")

        elif node.type == 'Yan':
            path = self._evaluate(node.value['path'])
            check = node.value['check']
            result = self.oracle.验(path if isinstance(path, list) else [path], check)
            self.output.append(f"[验] {'✅ 通过' if result['passed'] else '❌ 未通过'} - {result.get('reason', '')}")

        elif node.type == 'Zhao':
            cond = self._evaluate(node.value['condition'])
            result = self.oracle.兆(cond)
            self.output.append(f"[兆] {result.get('level', '')} - {result.get('signal', '')}")

        elif node.type == 'Xiang':
            name = node.value['name']
            props = node.value['props']
            self.objects[name] = {"type": "象", "props": props}
            self.output.append(f"[象] 建模「{name}」: {props}")

        elif node.type == 'Ci':
            hexagram = node.value['hexagram']
            result = self.oracle.辞(hexagram)
            self.output.append(f"[辞] {hexagram}: {result.get('meaning', '')}")

        elif node.type == 'Xi':
            a = node.value['a']
            b = node.value['b']
            result = self.oracle.系(a, b)
            self.output.append(f"[系] {result['relation']}")

        elif node.type == 'Ming':
            direction = node.value['direction']
            result = self.oracle.命(direction)
            mapping = result.get('mapping', {})
            self.output.append(f"[命] {direction} → {mapping.get('element', '未知')} ({mapping.get('color', '')})")

        elif node.type == 'Module':
            self.modules[node.value['name']] = {"type": "模块", "defined": True}
            self.output.append(f"[模块] 定义「{node.value['name']}」")

        elif node.type == 'Return':
            val = self._evaluate(node.value)
            self.output.append(f"[返回] {val}")

        else:
            self.output.append(f"[未知节点] {node.type}")

    def _evaluate(self, expr: str) -> Any:
        """评估表达式"""
        expr = expr.strip()

        # 变量查找
        if expr in self.env:
            return self.env[expr]

        # 字符串
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]

        # 数字
        try:
            if '.' in expr:
                return float(expr)
            return int(expr)
        except ValueError:
            pass

        # 布尔值
        if expr in ['真', 'True', 'true']:
            return True
        if expr in ['假', 'False', 'false']:
            return False

        # 算术表达式
        try:
            # 简单运算
            if '+' in expr:
                parts = expr.split('+')
                return sum(self._evaluate(p) for p in parts)
            if '*' in expr:
                parts = expr.split('*')
                result = 1
                for p in parts:
                    result *= self._evaluate(p)
                return result
            if '-' in expr and not expr.startswith('-'):
                parts = expr.split('-')
                result = self._evaluate(parts[0])
                for p in parts[1:]:
                    result -= self._evaluate(p)
                return result
        except:
            pass

        # 比较运算
        if '大于' in expr:
            parts = expr.split('大于')
            return self._evaluate(parts[0]) > self._evaluate(parts[1])
        if '小于' in expr:
            parts = expr.split('小于')
            return self._evaluate(parts[0]) < self._evaluate(parts[1])
        if '等于' in expr:
            parts = expr.split('等于')
            return self._evaluate(parts[0]) == self._evaluate(parts[1])

        return expr

    def _execute_expression(self, expr: str):
        """执行表达式语句"""
        # 简单执行：如果是打印语句
        if expr.startswith('输出'):
            val = expr.replace('输出', '').strip()
            self.output.append(f"[输出] {self._evaluate(val)}")
        else:
            # 尝试作为赋值
            if '为' in expr:
                parts = expr.split('为')
                if len(parts) == 2:
                    var = parts[0].strip()
                    val = self._evaluate(parts[1].strip())
                    self.env[var] = val

    def run_file(self, file_path: str) -> str:
        """运行CNSH文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            tokens = CNSHLexer.tokenize(code)
            ast = CNSHParser.parse(tokens)
            return self.execute(ast)
        except FileNotFoundError:
            return f"[错误] 文件不存在: {file_path}"
        except Exception as e:
            return f"[错误] {e}"

    def run_code(self, code: str) -> str:
        """运行CNSH代码字符串"""
        tokens = CNSHLexer.tokenize(code)
        ast = CNSHParser.parse(tokens)
        return self.execute(ast)

    def hexagram_demo(self) -> str:
        """卦机演示"""
        output = []
        output.append("🐉 卦机演示:")
        for name in ["乾", "坤", "震", "兑", "坎", "离", "艮", "巽"]:
            code = self.hexagram.get_code(name)
            lines = self.hexagram.get_lines(code)
            lines_str = ''.join('⚊' if l == 1 else '⚋' for l in reversed(lines))
            output.append(f"  {name}: {lines_str} ({format(code, '06b')})")
        output.append(f"\n当前卦: {self.hexagram.get_name(self.hexagram.current)}")
        output.append(f"爻变推演3步: {self.hexagram.deduce(3)}")
        return '\n'.join(output)

    def oracle_demo(self) -> str:
        """甲骨文算法演示"""
        output = []
        output.append("🔮 甲骨文算法演示:")
        bu = self.oracle.卜(42)
        output.append(f"  卜(42): {bu}")
        yan = self.oracle.验([1, 2, 3, 4, 5], "合规")
        output.append(f"  验: {yan}")
        zhao = self.oracle.兆(150, 0.7)
        output.append(f"  兆(150): {zhao['level']}")
        ming = self.oracle.命("东")
        output.append(f"  命(东): {ming['mapping']}")
        xiang = self.oracle.象([10, 20, 30, 40, 50])
        output.append(f"  象: 均值={xiang['mean']:.1f}, 标准差={xiang['std']:.1f}")
        ci = self.oracle.辞("乾")
        output.append(f"  辞(乾): {ci['meaning'][:30]}...")
        xi = self.oracle.系("用户", "系统")
        output.append(f"  系: {xi['relation']}")
        return '\n'.join(output)

    def causal_demo(self) -> str:
        """因果链演示"""
        self.causal.record("用户输入异常", "系统转为兑卦", "发出安全预警")
        self.causal.record("系统检测到异常", "触发熔断机制", "系统安全锁定")
        return self.causal.explain()

    def world_demo(self) -> str:
        """世界机演示"""
        self.world.create_world("龍魂元宇宙", {"dimension": 3, "light": "normal", "terrain": "mountain"})
        self.world.create_entity("玩家", "character", {"health": 100, "level": 1})
        self.world.create_scene("欢迎场景", "玩家进入时触发欢迎", ["玩家"])
        self.world.trigger_event("玩家进入", {"player": "Lucky"})
        return self.world.run_world(3)

# ============================================================
# 十、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 CNSH 第一卷 + 第二卷 · 全量交付 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互模式（推荐）
  python3 cnsh_complete.py --interactive

  # 执行CNSH文件
  python3 cnsh_complete.py --file demo.cns

  # 直接执行代码
  python3 cnsh_complete.py --code '设 x 为 5 输出 "x = " x'

  # 卦机演示
  python3 cnsh_complete.py --hexagram

  # 甲骨文演示
  python3 cnsh_complete.py --oracle

  # 因果链演示
  python3 cnsh_complete.py --causal

  # 世界机演示
  python3 cnsh_complete.py --world

  # 生成Notion模板
  python3 cnsh_complete.py --notion
        """
    )

    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--file", "-f", type=str, help="执行CNSH文件")
    parser.add_argument("--code", "-c", type=str, help="直接执行CNSH代码")
    parser.add_argument("--hexagram", "-H", action="store_true", help="卦机演示")
    parser.add_argument("--oracle", "-O", action="store_true", help="甲骨文算法演示")
    parser.add_argument("--causal", "-C", action="store_true", help="因果链演示")
    parser.add_argument("--world", "-W", action="store_true", help="世界机演示")
    parser.add_argument("--notion", "-N", action="store_true", help="生成Notion模板")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")

    args = parser.parse_args()

    interp = CNSHInterpreter()

    # 交互模式
    if args.interactive:
        print("\n" + "=" * 60)
        print("🐉 CNSH 完整解释器 v2.0")
        print("=" * 60)
        print(f"🧬 DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-CNSH-COMPLETE-v2.0")
        print("=" * 60)
        print("语法:")
        print("  设 x 为 5")
        print("  若 x 大于 3 则 输出 'ok' 否则 输出 'no'")
        print("  当前卦 为 乾")
        print("  爻变 三爻")
        print("  由 A 以致 B 终 C")
        print("  卜: 预测")
        print("  辞 乾")
        print("  命 东")
        print("  系 A 与 B")
        print("-" * 60)
        print("命令: demo | hexagram | oracle | causal | world | exit")
        print("-" * 60)

        while True:
            try:
                user_input = input("\nCNSH> ").strip()
                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit']:
                    print("👋 龍魂永存")
                    break

                if user_input.lower() == 'demo':
                    demo = '''
设 x 为 10
若 x 大于 5 则 输出 "x大于5" 否则 输出 "x不大于5"
当前卦 为 乾
爻变 三爻
由 用户输入 以致 系统响应 终 输出结果
卜: 42
辞 乾
命 东
'''
                    print(interp.run_code(demo))
                    continue

                if user_input.lower() == 'hexagram':
                    print(interp.hexagram_demo())
                    continue

                if user_input.lower() == 'oracle':
                    print(interp.oracle_demo())
                    continue

                if user_input.lower() == 'causal':
                    print(interp.causal_demo())
                    continue

                if user_input.lower() == 'world':
                    print(interp.world_demo())
                    continue

                # 执行用户输入的CNSH代码
                result = interp.run_code(user_input)
                print(result)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
        return

    # 卦机演示
    if args.hexagram:
        result = interp.hexagram_demo()
        if args.json:
            print(json.dumps({"hexagram": interp.hexagram.get_state()}, ensure_ascii=False, indent=2))
        else:
            print(result)
        return

    # 甲骨文演示
    if args.oracle:
        result = interp.oracle_demo()
        if args.json:
            print(json.dumps({"oracle": result}, ensure_ascii=False, indent=2))
        else:
            print(result)
        return

    # 因果链演示
    if args.causal:
        result = interp.causal_demo()
        if args.json:
            print(json.dumps({"causal_chain": interp.causal.get_chain()}, ensure_ascii=False, indent=2))
        else:
            print(result)
        return

    # 世界机演示
    if args.world:
        result = interp.world_demo()
        if args.json:
            print(json.dumps({"world": interp.world.get_world_state()}, ensure_ascii=False, indent=2))
        else:
            print(result)
        return

    # 执行文件
    if args.file:
        result = interp.run_file(args.file)
        if args.json:
            print(json.dumps({"output": result, "env": interp.env}, ensure_ascii=False, indent=2))
        else:
            print(result)
        return

    # 执行代码
    if args.code:
        result = interp.run_code(args.code)
        if args.json:
            print(json.dumps({"output": result, "env": interp.env}, ensure_ascii=False, indent=2))
        else:
            print(result)
        return

    # Notion模板
    if args.notion:
        print("""
# CNSH 第一卷 + 第二卷 · 完整结构

## 一、语言核心
- 中文语序即逻辑
- 64卦 = 状态机
- 甲骨文 = 原子操作符
- 所有语言可编译为CNSH IR

## 二、20条核心语法
1. 设 x 为 5 → 赋值
2. 若...则...否则... → 条件
3. 每当...执行...直到结束 → 循环
4. 以...为法 → 函数
5. 以...记载 → 对象
6. 卷 → 模块
7. 注： → 注释
8. 若有...则... → 事件
9. 并起...与... → 并发
10-20. 卦、爻、卜、验、兆、象、系、辞、卦序、命、因果链

## 三、运行时架构
- 第0层：Lex（中文分词）
- 第1层：Parse（AST）
- 第2层：卦机（状态机）
- 第3层：执行器
- 第4层：事件引擎 (E→C→R)

## 四、卦机（64卦状态机）
- 64卦 = 6位二进制编码
- 爻变 = 按位异或
- 推演 = 迭代爻变

## 五、甲骨文算法（9条）
1. 卜 - 预测
2. 验 - 验证
3. 兆 - 异常检测
4. 命 - 方向映射
5. 爻 - 微变
6. 象 - 建模
7. 辞 - 解释
8. 系 - 绑定
9. 卦备忘录 - 缓存

## 六、因果链引擎
- 由...以致...终...
- 可追溯决策链

## 七、世界机（元宇宙引擎）
- 象层（数据形）
- 卦层（状态）
- 辞层（解释）

## 八、安全模型
- 本地执行
- 可审计
- 可撤回
        """)
        return

    # 默认显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
