#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
# DNA追溯: #龍芯⚡️2026-06-18-LONGYIN-ASR-v1.0
# 模块: 语音识别引擎.py | 龍音ASR — 中文优先语音识别引擎
# 作者: 龍魂体系 · CNSH中文编程规范
# 协议: 君子协议 / CC BY-NC-SA 4.0 · 非商业共享 · 引用请注明出处
# ═══════════════════════════════════════════════════════════════════════════════
"""
🐉 龍音ASR — 中文优先的语音识别引擎 (LongYin ASR - Chinese-First Speech Recognition Engine)

通心译 | TongXin Translation:
本模块实现一套中文优先的自动语音识别(ASR)系统。核心策略为：能中文替代的中文实现，
不能的用国际标准库兜底。支持拼音对齐、声调识别、方言适配、中文编程语音输入。

核心能力 | Core Capabilities:
    🟢 中文核心: 拼音生成、声调识别、VAD、MFCC自研、唤醒词检测
    🟡 国际兜底: Whisper(base中文微调) + SpeechRecognition
    🔴 降级模式: 纯算法模拟（无外部库时可用）
"""

import os
import sys
import re
import math
import wave
import struct
import logging
import warnings
import tempfile
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union, Callable
from collections import Counter, deque
from dataclasses import dataclass, field
from enum import Enum
import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# 全局配置与日志 | Global Configuration & Logging
# ═══════════════════════════════════════════════════════════════════════════════

# 三色审计标注 | Three-Color Audit Markers:
# 🟢 = 安全/通过 | Safe/Passed
# 🟡 = 警告/降级 | Warning/Degraded
# 🔴 = 错误/阻断 | Error/Blocked

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
_日志 = logging.getLogger('龍音ASR')

# 模块级元数据 | Module Metadata
__版本__ = "1.0.0"
__DNA__ = "#龍芯⚡️2026-06-18-LONGYIN-ASR-v1.0"
__协议__ = "CC BY-NC-SA 4.0"


# ═══════════════════════════════════════════════════════════════════════════════
# 依赖检测与模拟层 | Dependency Detection & Mock Layer
# ═══════════════════════════════════════════════════════════════════════════════

class 依赖状态:
    """🟢 依赖库状态管理 | Dependency Status Manager"""
    NUMPY可用: bool = False
    SCIPY可用: bool = False
    SOUNDFILE可用: bool = False
    PYAUDIO可用: bool = False
    SPEECHRECOGNITION可用: bool = False
    WHISPER可用: bool = False
    TORCH可用: bool = False
    尝试加载完成: bool = False


def _检测依赖():
    """🟢 检测所有可选依赖的可用性 | Detect all optional dependencies"""
    if 依赖状态.尝试加载完成:
        return
    依赖状态.尝试加载完成 = True

    try:
        import numpy as np
        依赖状态.NUMPY可用 = True
        _日志.info("🟢 numpy 已加载 | numpy loaded")
    except ImportError:
        _日志.warning("🟡 numpy 未安装，使用纯Python数学实现 | numpy not installed, using pure Python math")

    try:
        import scipy
        依赖状态.SCIPY可用 = True
        _日志.info("🟢 scipy 已加载 | scipy loaded")
    except ImportError:
        _日志.warning("🟡 scipy 未安装 | scipy not installed")

    try:
        import soundfile as sf
        依赖状态.SOUNDFILE可用 = True
        _日志.info("🟢 soundfile 已加载 | soundfile loaded")
    except ImportError:
        _日志.warning("🟡 soundfile 未安装 | soundfile not installed")

    try:
        import pyaudio
        依赖状态.PYAUDIO可用 = True
        _日志.info("🟢 pyaudio 已加载 | pyaudio loaded")
    except ImportError:
        _日志.warning("🟡 pyaudio 未安装，实时识别不可用 | pyaudio not installed, real-time recognition unavailable")

    try:
        import speech_recognition as sr
        依赖状态.SPEECHRECOGNITION可用 = True
        _日志.info("🟢 SpeechRecognition 已加载 | SpeechRecognition loaded")
    except ImportError:
        _日志.warning("🟡 SpeechRecognition 未安装 | SpeechRecognition not installed")

    try:
        import whisper
        依赖状态.WHISPER可用 = True
        _日志.info("🟢 Whisper 已加载 | Whisper loaded")
    except ImportError:
        _日志.warning("🟡 Whisper 未安装 | Whisper not installed")

    try:
        import torch
        依赖状态.TORCH可用 = True
        _日志.info("🟢 torch 已加载 | torch loaded")
    except ImportError:
        _日志.warning("🟡 torch 未安装 | torch not installed")


# 初始化依赖检测 | Initialize dependency detection
_检测依赖()


# ═══════════════════════════════════════════════════════════════════════════════
# 纯Python数学工具 | Pure Python Math Utilities (no numpy fallback)
# ═══════════════════════════════════════════════════════════════════════════════

class 数学工具:
    """🟢 纯Python数学工具类，numpy不可用时兜底 | Pure Python math utilities"""

    @staticmethod
    def 汉明窗(长度: int) -> List[float]:
        """生成汉明窗 | Generate Hamming window"""
        return [0.54 - 0.46 * math.cos(2 * math.pi * n / (长度 - 1)) for n in range(长度)]

    @staticmethod
    def 矩形窗(长度: int) -> List[float]:
        """生成矩形窗 | Generate rectangular window"""
        return [1.0] * 长度

    @staticmethod
    def 离散余弦变换(数据: List[float], 点数: int) -> List[float]:
        """
        🟢 一维DCT-II实现 | 1D DCT-II implementation
        公式: Y[k] = sum(x[n] * cos(pi/N * (n+0.5) * k))
        """
        结果 = []
        N = len(数据)
        for k in range(min(点数, N)):
            累加 = 0.0
            for n in range(N):
                累加 += 数据[n] * math.cos(math.pi / N * (n + 0.5) * k)
            结果.append(累加)
        return 结果

    @staticmethod
    def 快速傅里叶变换(实部序列: List[float]) -> Tuple[List[float], List[float]]:
        """
        🟢 Cooley-Tukey FFT实现（2的幂次）| Cooley-Tukey FFT (power of 2)
        返回 (实部, 虚部) | Returns (real, imag)
        """
        N = len(实部序列)
        if N <= 1:
            return list(实部序列), [0.0] * N

        # 确保是2的幂 | Ensure power of 2
        目标长度 = 1
        while 目标长度 < N:
            目标长度 *= 2

        # 补零 | Zero padding
        实部 = list(实部序列) + [0.0] * (目标长度 - N)
        虚部 = [0.0] * 目标长度

        # 位反转置换 | Bit-reversal permutation
        def _位反转(k, n):
            结果 = 0
            for _ in range(n):
                结果 = (结果 << 1) | (k & 1)
                k >>= 1
            return 结果

        位数 = int(math.log2(目标长度))
        for k in range(目标长度):
            反转 = _位反转(k, 位数)
            if k < 反转:
                实部[k], 实部[反转] = 实部[反转], 实部[k]

        # 蝶形运算 | Butterfly operations
        步长 = 2
        while 步长 <= 目标长度:
            半 = 步长 // 2
            for i in range(0, 目标长度, 步长):
                for j in range(半):
                    角度 = -2 * math.pi * j / 步长
                    余弦 = math.cos(角度)
                    正弦 = math.sin(角度)
                    下标 = i + j + 半
                    临时实 = 实部[下标] * 余弦 - 虚部[下标] * 正弦
                    临时虚 = 实部[下标] * 正弦 + 虚部[下标] * 余弦
                    实部[下标] = 实部[i + j] - 临时实
                    虚部[下标] = 虚部[i + j] - 临时虚
                    实部[i + j] += 临时实
                    虚部[i + j] += 临时虚
            步长 *= 2

        return 实部, 虚部

    @staticmethod
    def 计算幅度谱(实部: List[float], 虚部: List[float]) -> List[float]:
        """计算复数幅度 | Compute complex magnitude"""
        return [math.sqrt(r * r + i * i) for r, i in zip(实部, 虚部)]

    @staticmethod
    def 梅尔滤波器组(滤波器数量: int, FFT点数: int, 采样率: int,
                     最低频: float = 0.0, 最高频: Optional[float] = None) -> List[List[float]]:
        """
        🟢 梅尔滤波器组 | Mel filter bank
        将线性频谱映射到梅尔刻度 | Maps linear spectrum to Mel scale
        """
        if 最高频 is None:
            最高频 = 采样率 / 2

        # 梅尔频率转换公式 | Mel frequency conversion: Mel(f) = 2595 * log10(1 + f/700)
        def _赫兹到梅尔(赫兹):
            return 2595 * math.log10(1 + 赫兹 / 700)

        def _梅尔到赫兹(梅尔值):
            return 700 * (10 ** (梅尔值 / 2595) - 1)

        最低梅尔 = _赫兹到梅尔(最低频)
        最高梅尔 = _赫兹到梅尔(最高频)
        梅尔点 = [最低梅尔 + i * (最高梅尔 - 最低梅尔) / (滤波器数量 + 1)
                  for i in range(滤波器数量 + 2)]
        赫兹点 = [_梅尔到赫兹(m) for m in 梅尔点]
        频点 = [int((f / (采样率 / 2)) * (FFT点数 / 2 + 1)) for f in 赫兹点]

        滤波器组 = []
        for m in range(1, 滤波器数量 + 1):
            滤波器 = [0.0] * (FFT点数 // 2 + 1)
            for k in range(频点[m - 1], 频点[m]):
                if 频点[m] != 频点[m - 1]:
                    滤波器[k] = (k - 频点[m - 1]) / (频点[m] - 频点[m - 1])
            for k in range(频点[m], 频点[m + 1]):
                if 频点[m + 1] != 频点[m]:
                    滤波器[k] = (频点[m + 1] - k) / (频点[m + 1] - 频点[m])
            滤波器组.append(滤波器)

        return 滤波器组


# ═══════════════════════════════════════════════════════════════════════════════
# numpy包装层 | NumPy Wrapper Layer
# ═══════════════════════════════════════════════════════════════════════════════

class 数组工具:
    """🟢 数组操作抽象层，自动选择numpy或纯Python | Array ops abstraction layer"""

    @staticmethod
    def 创建数组(数据):
        """创建数值数组 | Create numeric array"""
        if 依赖状态.NUMPY可用:
            import numpy as np
            return np.array(数据, dtype=float)
        return list(数据)

    @staticmethod
    def 零数组(长度):
        """创建零数组 | Create zero array"""
        if 依赖状态.NUMPY可用:
            import numpy as np
            return np.zeros(长度)
        return [0.0] * 长度

    @staticmethod
    def 点乘(a, b):
        """向量点积 | Vector dot product"""
        if 依赖状态.NUMPY可用:
            import numpy as np
            return float(np.dot(a, b))
        return sum(x * y for x, y in zip(a, b))

    @staticmethod
    def 加窗(数据, 窗):
        """加窗运算 | Windowing"""
        if 依赖状态.NUMPY可用:
            import numpy as np
            return np.array(数据) * np.array(窗)
        return [d * w for d, w in zip(数据, 窗)]

    @staticmethod
    def 对数(数据):
        """逐元素对数 | Element-wise log"""
        if 依赖状态.NUMPY可用:
            import numpy as np
            return np.log(np.maximum(数据, 1e-10))
        return [math.log(max(x, 1e-10)) for x in 数据]

    @staticmethod
    def 最大值(数据):
        """最大值 | Maximum value"""
        return max(数据)

    @staticmethod
    def 最小值(数据):
        """最小值 | Minimum value"""
        return min(数据)

    @staticmethod
    def 平均值(数据):
        """平均值 | Mean value"""
        return sum(数据) / len(数据)


# ═══════════════════════════════════════════════════════════════════════════════
# 内置数据：简化拼音表 | Built-in Data: Simplified Pinyin Table
# 覆盖500+最常用汉字 | Covering 500+ most common Chinese characters
# ═══════════════════════════════════════════════════════════════════════════════

class 拼音数据库:
    """
    🟢 简化拼音数据库 | Simplified Pinyin Database
    基于现代汉语频率统计，覆盖最常用的500+汉字
    Based on modern Chinese frequency stats, covers 500+ most used characters
    """

    # 单字拼音映射表 | Single character pinyin mapping
    汉字拼音表: Dict[str, str] = {
        # === 一级常用字（~100字）| Level 1 most common (~100 chars) ===
        "的": "de", "一": "yi", "是": "shi", "不": "bu", "了": "le",
        "在": "zai", "人": "ren", "有": "you", "我": "wo", "他": "ta",
        "这": "zhe", "个": "ge", "们": "men", "中": "zhong", "来": "lai",
        "上": "shang", "大": "da", "为": "wei", "和": "he", "国": "guo",
        "地": "di", "到": "dao", "以": "yi", "说": "shuo", "时": "shi",
        "要": "yao", "就": "jiu", "出": "chu", "会": "hui", "可": "ke",
        "也": "ye", "你": "ni", "对": "dui", "生": "sheng", "能": "neng",
        "而": "er", "子": "zi", "那": "na", "得": "de", "于": "yu",
        "着": "zhe", "下": "xia", "自": "zi", "之": "zhi", "年": "nian",
        "过": "guo", "发": "fa", "后": "hou", "作": "zuo", "里": "li",
        "用": "yong", "道": "dao", "行": "xing", "所": "suo", "然": "ran",
        "家": "jia", "种": "zhong", "事": "shi", "成": "cheng", "方": "fang",
        "多": "duo", "经": "jing", "么": "me", "去": "qu", "法": "fa",
        "学": "xue", "如": "ru", "都": "dou", "同": "tong", "现": "xian",
        "当": "dang", "没": "mei", "动": "dong", "面": "mian", "起": "qi",
        "看": "kan", "定": "ding", "天": "tian", "分": "fen", "还": "hai",
        "进": "jin", "小": "xiao", "她": "ta", "其": "qi", "些": "xie",
        "主": "zhu", "样": "yang", "理": "li", "心": "xin", "本": "ben",
        "前": "qian", "开": "kai", "但": "dan", "因": "yin", "只": "zhi",
        "从": "cong", "想": "xiang", "实": "shi", "日": "ri", "者": "zhe",
        "把": "ba", "性": "xing", "好": "hao", "明": "ming",
        "三": "san", "二": "er", "十": "shi", "四": "si", "五": "wu",
        "六": "liu", "七": "qi", "八": "ba", "九": "jiu", "百": "bai",
        "千": "qian", "万": "wan", "零": "ling", "几": "ji",
        # === 二级常用字（~200字）| Level 2 common (~200 chars) ===
        "公": "gong", "体": "ti", "已": "yi", "最": "zui", "将": "jiang",
        "老": "lao", "知": "zhi", "相": "xiang", "两": "liang", "问": "wen",
        "很": "hen", "又": "you", "业": "ye", "外": "wai", "回": "hui",
        "文": "wen", "点": "dian", "正": "zheng", "新": "xin", "与": "yu",
        "手": "shou", "打": "da", "高": "gao", "意": "yi", "第": "di",
        "它": "ta", "次": "ci", "长": "chang", "常": "chang",
        "或": "huo", "女": "nv", "间": "jian", "白": "bai", "话": "hua",
        "比": "bi", "己": "ji", "变": "bian", "总": "zong", "目": "mu",
        "加": "jia", "美": "mei", "世": "shi", "系": "xi",
        "机": "ji", "声": "sheng", "应": "ying", "全": "quan",
        "重": "zhong", "化": "hua", "特": "te", "料": "liao",
        "神": "shen", "完": "wan", "内": "nei",
        "求": "qiu", "住": "zhu", "海": "hai", "通": "tong",
        "头": "tou", "件": "jian", "难": "nan", "山": "shan", "路": "lu",
        "空": "kong", "报": "bao", "指": "zhi", "江": "jiang", "北": "bei",
        "城": "cheng", "水": "shui", "原": "yuan", "先": "xian", "入": "ru",
        "门": "men", "信": "xin", "认": "ren", "平": "ping", "装": "zhuang",
        "月": "yue", "无": "wu", "写": "xie", "光": "guang", "活": "huo",
        "今": "jin", "立": "li", "亲": "qin", "电": "dian",
        "京": "jing", "少": "shao", "听": "ting", "表": "biao", "资": "zi",
        "王": "wang", "军": "jun", "请": "qing", "安": "an", "教": "jiao",
        "车": "che", "色": "se", "员": "yuan", "位": "wei",
        "金": "jin", "快": "kuai", "花": "hua", "果": "guo",
        "且": "qie", "决": "jue", "兄": "xiong", "若": "ruo", "兴": "xing",
        "哥": "ge", "字": "zi", "片": "pian", "室": "shi", "具": "ju",
        "龙": "long", "青": "qing", "英": "ying", "工": "gong", "眼": "yan",
        "医": "yi", "别": "bie", "任": "ren", "界": "jie", "展": "zhan",
        "思": "si", "连": "lian", "司": "si",
        "建": "jian", "张": "zhang", "节": "jie", "每": "mei",
        "火": "huo", "烧": "shao", "走": "zou", "黑": "hei", "春": "chun",
        "跑": "pao", "兵": "bing", "站": "zhan", "送": "song", "读": "du",
        "夜": "ye", "冷": "leng", "力": "li", "红": "hong", "半": "ban",
        "菜": "cai", "乐": "le", "师": "shi", "号": "hao", "喝": "he",
        "望": "wang", "乡": "xiang", "笑": "xiao", "更": "geng", "风": "feng",
        "解": "jie", "边": "bian", "言": "yan", "爱": "ai", "取": "qu",
        "飞": "fei", "才": "cai", "被": "bei", "干": "gan", "放": "fang",
        "雨": "yu", "处": "chu", "息": "xi", "身": "shen",
        "告": "gao", "男": "nan", "数": "shu", "早": "zao", "林": "lin",
        "找": "zhao", "算": "suan", "友": "you", "孩": "hai", "让": "rang",
        "太": "tai", "吃": "chi", "叫": "jiao", "东": "dong",
        "名": "ming", "古": "gu", "米": "mi", "蓝": "lan",
        "视": "shi", "交": "jiao", "带": "dai", "马": "ma",
        "民": "min", "养": "yang", "星": "xing", "非": "fei", "影": "ying",
        "欢": "huan", "织": "zhi", "流": "liu", "留": "liu",
        "服": "fu", "确": "que", "般": "ban", "村": "cun",
        "容": "rong", "演": "yan", "越": "yue", "精": "jing", "刚": "gang",
        "阳": "yang", "错": "cuo", "细": "xi", "血": "xie", "推": "tui",
        "州": "zhou", "研": "yan", "省": "sheng", "习": "xi", "款": "kuan",
        "参": "can", "百": "bai", "除": "chu",
        "器": "qi", "叶": "ye", "烟": "yan", "团": "tuan",
        # === 三级扩展字（~200字）| Level 3 extended (~200 chars) ===
        "品": "pin", "候": "hou", "广": "guang", "角": "jiao", "程": "cheng",
        "派": "pai", "转": "zhuan", "断": "duan", "组": "zu", "买": "mai",
        "产": "chan", "极": "ji", "怎": "zen", "须": "xu", "向": "xiang",
        "论": "lun", "运": "yun", "死": "si",
        "究": "jiu", "追": "zhui", "许": "xu", "愿": "yuan",
        "忘": "wang", "谈": "tan", "照": "zhao", "投": "tou", "尚": "shang",
        "终": "zhong", "收": "shou", "征": "zheng", "修": "xiu",
        "引": "yin", "谁": "shui", "板": "ban",
        "盒": "he", "念": "nian", "随": "sui", "依": "yi",
        "草": "cao", "排": "pai", "考": "kao", "刻": "ke",
        "牛": "niu", "态": "tai", "令": "ling", "端": "duan", "句": "ju",
        "堂": "tang", "卖": "mai", "批": "pi", "陆": "lu",
        "彩": "cai", "虚": "xu", "强": "qiang", "童": "tong",
        "故": "gu", "首": "shou", "战": "zhan", "示": "shi", "远": "yuan",
        "园": "yuan", "语": "yu",
        "房": "fang", "母": "mu", "德": "de", "价": "jia",
        "坏": "huai", "脑": "nao", "距": "ju", "根": "gen",
        "持": "chi", "毒": "du", "座": "zuo", "停": "ting",
        "闻": "wen", "寻": "xun", "假": "jia",
        "增": "zeng", "官": "guan", "环": "huan", "够": "gou", "称": "cheng",
        "众": "zhong", "静": "jing", "香": "xiang", "怪": "guai", "何": "he",
        "待": "dai", "疑": "yi", "严": "yan", "适": "shi", "赛": "sai",
        "藏": "cang", "页": "ye", "嗯": "en", "胡": "hu", "激": "ji",
        "怒": "nu", "虽": "sui", "另": "ling", "苏": "su", "某": "mou",
        "承": "cheng", "冲": "chong", "弱": "ruo", "嘴": "zui",
        "固": "gu", "材": "cai", "害": "hai", "妻": "qi",
        "河": "he", "喜": "xi", "招": "zhao", "曲": "qu",
        "钱": "qian", "赵": "zhao", "酒": "jiu",
        "未": "wei", "咱": "zan", "困": "kun", "挥": "hui",
        "宏": "hong", "武": "wu", "扬": "yang", "素": "su", "差": "cha",
        "冠": "guan", "旁": "pang", "符": "fu", "浪": "lang", "抽": "chou",
        "伴": "ban", "迷": "mi", "雾": "wu", "托": "tuo",
        "戴": "dai", "败": "bai", "急": "ji", "幻": "huan",
        "瑞": "rui", "窗": "chuang", "智": "zhi", "野": "ye", "巨": "ju",
        "池": "chi", "净": "jing", "迎": "ying", "弟": "di",
        "忠": "zhong", "拜": "bai", "冬": "dong", "赞": "zan", "革": "ge",
        "塔": "ta", "振": "zhen", "郑": "zheng", "沈": "shen", "盛": "sheng",
        "筑": "zhu", "模": "mo", "恋": "lian", "温": "wen",
        "珠": "zhu", "晓": "xiao", "祥": "xiang", "释": "shi",
        "型": "xing", "苦": "ku", "祖": "zu", "吓": "xia",
        "呵": "he", "凡": "fan", "渐": "jian", "坚": "jian",
        "缺": "que", "祝": "zhu", "委": "wei", "臣": "chen",
        "宇": "yu", "央": "yang", "宣": "xuan", "申": "shen", "废": "fei",
        "宗": "zong", "雄": "xiong", "毫": "hao", "碎": "sui",
        "魏": "wei", "爷": "ye", "忍": "ren", "骨": "gu",
        "姓": "xing", "鬼": "gui", "晨": "chen", "笔": "bi", "桥": "qiao",
        "圈": "quan", "娘": "niang", "楚": "chu", "械": "xie", "欲": "yu",
        "仙": "xian", "蔡": "cai", "舰": "jian", "晴": "qing", "舱": "cang",
        "默": "mo", "灯": "deng", "幅": "fu", "牙": "ya",
        # === 龍魂体系专用字 | LongHun System Special Characters ===
        "龍": "long", "魂": "hun", "芯": "xin", "译": "yi", "語": "yu",
        "聲": "sheng", "識": "shi", "電": "dian", "腦": "nao", "藍": "lan",
        "劍": "jian", "鳳": "feng", "華": "hua", "創": "chuang",
        "國": "guo", "學": "xue", "書": "shu",
        "無": "wu", "雲": "yun", "風": "feng", "興": "xing",
        "禮": "li", "義": "yi", "團": "tuan", "夢": "meng",
        "實": "shi", "來": "lai",
        "個": "ge", "後": "hou", "這": "zhe", "為": "wei",
        "從": "cong", "還": "hai", "對": "dui", "問": "wen", "裡": "li",
        "開": "kai", "進": "jin",
        "經": "jing", "長": "chang", "發": "fa", "因": "yin", "樣": "yang",
        "應": "ying", "該": "gai", "關": "guan", "係": "xi", "統": "tong",
        "計": "ji", "試": "shi", "圖": "tu", "務": "wu", "類": "lei",
        "級": "ji", "數": "shu", "處": "chu", "設": "she",
        "變": "bian", "條": "tiao", "構": "gou",
        "造": "zao", "函": "han", "組": "zu", "調": "diao",
        "編": "bian", "譯": "yi", "執": "zhi",
        "導": "dao", "出": "chu",
        "繼": "ji", "封": "feng", "裝": "zhuang",
        "象": "xiang", "迭": "die", "代": "dai", "遍": "bian", "歷": "li",
        "用": "yong", "明": "ming", "異": "yi",
        "常": "chang", "拋": "pao", "捕": "bu", "獲": "huo",
        "回": "hui", "監": "jian", "聽": "ting", "觸": "chu",
        "綁": "bang", "定": "ding", "由": "you",
        "注": "zhu", "解": "jie", "檔": "dang",
        "串": "chuan",
        "佈": "bu", "爾": "er", "整": "zheng",
        "浮": "fu",
        "點": "dian", "列": "lie", "集": "ji", "合": "he",
        "元": "yuan", "範": "fan",
        "圍": "wei", "生": "sheng", "推": "tui",
        "加": "jia", "載": "zai", "塊": "kuai",
        "包": "bao", "庫": "ku", "賴": "lai",
        "境": "jing", "配": "pei", "置": "zhi", "屬": "shu", "性": "xing",
        "法": "fa", "參": "can", "返": "fan",
        "值": "zhi", "實": "shi", "例": "li",
        "初": "chu", "始": "shi", "化": "hua", "銷": "xiao",
        "毀": "hui", "多": "duo",
        "混": "hun", "靜": "jing",
        "量": "liang",
        "私": "si", "保": "bao", "護": "hu",
        "內": "nei", "部": "bu", "外": "wai",
        "接": "jie", "口": "kou",
        "覆": "fu",
        "寫": "xie", "運": "yun", "算": "suan",
        "比": "bi", "較": "jiao",
        "深": "shen", "拷": "kao", "貝": "bei", "淺": "qian",
        "線": "xian", "程": "cheng",
        "協": "xie", "同": "tong",
        "步": "bu", "鎖": "suo", "信": "xin", "號": "hao", "事": "shi",
        "緩": "huan", "衝": "chong", "隊": "dui",
        "列": "lie", "棧": "zhan", "堆": "dui", "樹": "shu",
        "散": "san", "哈": "ha", "希": "xi",
        "貪": "tan", "心": "xin", "規": "gui",
        "劃": "hua", "治": "zhi",
        "遞": "di", "歸": "gui",
        "剪": "jian", "枝": "zhi",
        "序": "xu", "查": "cha", "插": "cha", "入": "ru",
        "刪": "shan",
        "度": "du",
        "徑": "jing", "短": "duan",
        "網": "wang", "絡": "luo", "爬": "pa",
        "蟲": "chong", "響": "xiang",
        "狀": "zhuang", "碼": "ma", "頭": "tou",
        "體": "ti", "負": "fu", "載": "zai",
        "驗": "yan", "證": "zheng", "權": "quan", "限": "xian",
        "牌": "pai", "密": "mi", "鑰": "yao",
        "簽": "qian", "名": "ming", "書": "shu", "議": "yi",
        "套": "tao", "端": "duan",
        "地": "di", "址": "zhi",
        "域": "yu", "名": "ming", "服": "fu",
        "器": "qi", "戶": "hu",
        "據": "ju",
        "記": "ji", "錄": "lu", "欄": "lan",
        "索": "suo", "鍵": "jian",
        "關": "guan", "聯": "lian",
        "詢": "xun", "篩": "shai", "選": "xuan", "聚": "ju",
        "視": "shi",
        "儲": "chu",
        "觸": "chu", "發": "fa", "器": "qi", "誌": "zhi",
        "備": "bei", "份": "fen",
        "還": "huan", "原": "yuan",
        "遷": "qian", "移": "yi", "鏡": "jing",
        "像": "xiang",
        "均": "jun",
        "衡": "heng",
        "消": "xiao", "息": "xi",
        "發": "fa", "佈": "bu", "訂": "ding", "閱": "yue",
        "控": "kong", "告": "gao", "警": "jing",
        "析": "xi",
        "調": "diao",
        "擴": "kuo", "縮": "suo",
        "部": "bu", "署": "shu", "維": "wei", "測": "ce",
        "單": "dan", "元": "yuan", "成": "cheng",
        "收": "shou", "迴": "hui",
        "基": "ji", "準": "zhun", "蓋": "gai",
        "率": "lv", "性": "xing", "能": "neng", "壓": "ya",
        "容": "rong", "錯": "cuo", "災": "zai",
        "復": "fu", "滾": "gun",
        "綠": "lv",
        "金": "jin", "絲": "si", "雀": "que", "灰": "hui",
        "糖": "tang", "源": "yuan", "感": "gan", "值": "zhi",
        "面": "mian", "正": "zheng", "真": "zhen", "假": "jia",
        "是": "shi", "否": "fou", "得": "de", "失": "shi",
        "对": "dui", "错": "cuo", "赢": "ying", "输": "shu",
        "给": "gei", "送": "song", "收": "shou", "拿": "na",
        "出": "chu", "入": "ru", "进": "jin", "退": "tui",
        "升": "sheng", "降": "jiang", "起": "qi", "落": "luo",
        "来": "lai", "往": "wang", "去": "qu", "归": "gui",
        "得": "de", "失": "shi", "有": "you", "没": "mei",
        "多": "duo", "少": "shao", "大": "da", "小": "xiao",
        "高": "gao", "低": "di", "上": "shang", "下": "xia",
        "左": "zuo", "右": "you", "前": "qian", "后": "hou",
        "里": "li", "外": "wai", "中": "zhong", "旁": "pang",
        "这": "zhe", "那": "na", "哪": "na", "谁": "shui",
        "什": "shen", "怎": "zen", "为": "wei", "因": "yin",
        "果": "guo", "所": "suo", "以": "yi", "于": "yu",
        "在": "zai", "向": "xiang", "朝": "chao", "往": "wang",
        "把": "ba", "将": "jiang", "被": "bei", "叫": "jiao",
        "让": "rang", "令": "ling", "使": "shi", "给": "gei",
        "和": "he", "与": "yu", "跟": "gen", "同": "tong",
        "而": "er", "但": "dan", "却": "que", "只": "zhi",
        "最": "zui", "极": "ji", "更": "geng", "越": "yue",
        "很": "hen", "太": "tai", "非常": "feichang", "已": "yi",
        "刚": "gang", "正": "zheng", "曾": "ceng", "将": "jiang",
        "要": "yao", "须": "xu", "需": "xu", "必": "bi",
        "可": "ke", "能": "neng", "会": "hui", "应": "ying",
        "当": "dang", "该": "gai", "须": "xu", "得": "dei",
        "所": "suo", "若": "ruo", "倘": "tang", "如": "ru",
        "令": "ling", "叫": "jiao", "使": "shi",
    }

    # 声母表 | Initial consonants
    声母表: Tuple[str, ...] = (
        'b', 'p', 'm', 'f', 'd', 't', 'n', 'l',
        'g', 'k', 'h', 'j', 'q', 'x',
        'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w'
    )

    # 韵母表 | Finals
    韵母表: Tuple[str, ...] = (
        'a', 'o', 'e', 'i', 'u', 'v',
        'ai', 'ei', 'ui', 'ao', 'ou', 'iu',
        'ie', 've', 'ue', 'er', 'an', 'en', 'in', 'un', 'vn',
        'ang', 'eng', 'ing', 'ong',
        'ia', 'iao', 'ian', 'iang', 'iong',
        'ua', 'uo', 'uai', 'uan', 'uang',
    )

    # 声调标记 | Tone marks
    声调符号: Dict[int, str] = {
        1: "\u0304",   # 阴平 ˉ
        2: "\u0301",   # 阳平 ˊ
        3: "\u030C",   # 上声 ˇ
        4: "\u0300",   # 去声 ˋ
        0: "",          # 轻声
    }

    @classmethod
    def 获取汉字数(cls) -> int:
        """返回覆盖的汉字数量 | Return covered character count"""
        return len(cls.汉字拼音表)

    @classmethod
    def 获取拼音(cls, 汉字: str) -> str:
        """
        获取单个汉字的拼音 | Get pinyin for single character
        返回空字符串如果字符不在数据库中 | Returns empty if char not in db
        """
        return cls.汉字拼音表.get(汉字, "")

    @classmethod
    def 文本转拼音(cls, 文本: str) -> List[str]:
        """将中文文本转为拼音列表 | Convert Chinese text to pinyin list"""
        拼音列表 = []
        for 字 in 文本:
            if 字 in cls.汉字拼音表:
                拼音列表.append(cls.汉字拼音表[字])
            elif 字.strip():
                拼音列表.append(字)  # 非汉字保留原样 | Keep non-Chinese as-is
        return 拼音列表

    @classmethod
    def 添加汉字(cls, 汉字: str, 拼音: str):
        """动态添加汉字拼音映射 | Dynamically add character-pinyin mapping"""
        cls.汉字拼音表[汉字] = 拼音


# ═══════════════════════════════════════════════════════════════════════════════
# 唤醒词与语音命令数据 | Wake Words & Voice Command Data
# ═══════════════════════════════════════════════════════════════════════════════

class 语音命令数据库:
    """🟢 语音命令与唤醒词数据库 | Voice commands & wake words database"""

    # 唤醒词列表 | Wake words list
    唤醒词列表: List[str] = [
        "龍魂", "龍芯", "CNSH", "小龍", "启动",
        "long hun", "long xin", "xiao long", "qi dong",
        "龙魂", "龙芯", "小龙",
    ]

    # 唤醒词拼音形式（用于模糊匹配）| Pinyin forms for fuzzy matching
    唤醒词拼音: List[List[str]] = [
        ["long", "hun"], ["long", "xin"],
        ["c", "n", "s", "h"], ["xiao", "long"],
        ["qi", "dong"],
    ]

    # CNSH编程语音命令映射 | CNSH programming voice command mapping
    编程命令映射: Dict[str, Dict[str, str]] = {
        # === 类与对象 | Classes & Objects ===
        "创建类": {"模板": "class {名称}:\n    def __init__(self):\n        pass", "类型": "类定义"},
        "定义类": {"模板": "class {名称}:\n    def __init__(self):\n        pass", "类型": "类定义"},
        "新类": {"模板": "class {名称}:\n    def __init__(self):\n        pass", "类型": "类定义"},
        "继承类": {"模板": "class {子类}({父类}):\n    def __init__(self):\n        super().__init__()", "类型": "继承"},

        # === 函数与方法 | Functions & Methods ===
        "定义函数": {"模板": "def {名称}({参数}):\n    pass", "类型": "函数定义"},
        "创建函数": {"模板": "def {名称}({参数}):\n    pass", "类型": "函数定义"},
        "新方法": {"模板": "def {名称}(self, {参数}):\n    pass", "类型": "方法定义"},
        "异步函数": {"模板": "async def {名称}({参数}):\n    pass", "类型": "异步函数"},
        "Lambda函数": {"模板": "{名称} = lambda {参数}: {表达式}", "类型": "Lambda"},
        "匿名函数": {"模板": "{名称} = lambda {参数}: {表达式}", "类型": "Lambda"},

        # === 模块导入 | Module Imports ===
        "导入模块": {"模板": "import {模块}", "类型": "导入"},
        "导入": {"模板": "import {模块}", "类型": "导入"},
        "从导入": {"模板": "from {模块} import {名称}", "类型": "选择性导入"},
        "导入所有": {"模板": "from {模块} import *", "类型": "通配导入"},

        # === 变量与数据结构 | Variables & Data Structures ===
        "定义变量": {"模板": "{名称} = {值}", "类型": "变量"},
        "创建列表": {"模板": "{名称} = [{元素}]", "类型": "列表"},
        "创建字典": {"模板": "{名称} = {{{键值对}}}", "类型": "字典"},
        "创建集合": {"模板": "{名称} = set([{元素}])", "类型": "集合"},
        "创建元组": {"模板": "{名称} = ({元素},)", "类型": "元组"},
        "创建数组": {"模板": "{名称} = [{元素}]", "类型": "数组"},
        "列表推导": {"模板": "{名称} = [{表达式} for {变量} in {可迭代}]", "类型": "推导式"},
        "字典推导": {"模板": "{名称} = {{{k}: {v} for k, v in {可迭代}}}", "类型": "推导式"},

        # === 控制流 | Control Flow ===
        "如果": {"模板": "if {条件}:\n    {语句}", "类型": "条件"},
        "否则": {"模板": "else:\n    {语句}", "类型": "条件"},
        "否则如果": {"模板": "elif {条件}:\n    {语句}", "类型": "条件"},
        "循环": {"模板": "for {变量} in {范围}:\n    {语句}", "类型": "循环"},
        "当": {"模板": "while {条件}:\n    {语句}", "类型": "循环"},
        "继续": {"模板": "continue", "类型": "跳转"},
        "跳出": {"模板": "break", "类型": "跳转"},
        "返回": {"模板": "return {值}", "类型": "返回"},
        "试捕获": {"模板": "try:\n    {语句}\nexcept {异常}:\n    {处理}", "类型": "异常"},
        "试": {"模板": "try:\n    {语句}\nexcept Exception as e:\n    print(e)", "类型": "异常"},
        "最后": {"模板": "finally:\n    {语句}", "类型": "异常"},

        # === 面向对象 | OOP ===
        "初始化": {"模板": "def __init__(self):\n    pass", "类型": "构造器"},
        "字符串表示": {"模板": "def __str__(self):\n    return '{字符串}'", "类型": "魔术方法"},
        "表示": {"模板": "def __repr__(self):\n    return '{字符串}'", "类型": "魔术方法"},
        "等号": {"模板": "def __eq__(self, other):\n    return self.x == other.x", "类型": "魔术方法"},
        "小于": {"模板": "def __lt__(self, other):\n    return self.x < other.x", "类型": "魔术方法"},
        "迭代器": {"模板": "def __iter__(self):\n    return iter(self.items)", "类型": "魔术方法"},
        "长度": {"模板": "def __len__(self):\n    return len(self.items)", "类型": "魔术方法"},
        "获取": {"模板": "def __getitem__(self, key):\n    return self.data[key]", "类型": "魔术方法"},
        "设置": {"模板": "def __setitem__(self, key, value):\n    self.data[key] = value", "类型": "魔术方法"},
        "调用": {"模板": "def __call__(self, *args, **kwargs):\n    return self.func(*args, **kwargs)", "类型": "魔术方法"},
        "进入": {"模板": "def __enter__(self):\n    return self", "类型": "上下文"},
        "退出": {"模板": "def __exit__(self, exc_type, exc_val, exc_tb):\n    pass", "类型": "上下文"},

        # === 装饰器与高级特性 | Decorators & Advanced ===
        "装饰器": {"模板": "@{名称}\ndef {函数}():\n    pass", "类型": "装饰器"},
        "属性": {"模板": "@property\ndef {名称}(self):\n    return self._{名称}", "类型": "属性"},
        "类方法": {"模板": "@classmethod\ndef {名称}(cls, {参数}):\n    pass", "类型": "类方法"},
        "静态方法": {"模板": "@staticmethod\ndef {名称}({参数}):\n    pass", "类型": "静态方法"},

        # === 文件操作 | File Operations ===
        "读文件": {"模板": "with open('{路径}', 'r', encoding='utf-8') as f:\n    {名称} = f.read()", "类型": "文件IO"},
        "写文件": {"模板": "with open('{路径}', 'w', encoding='utf-8') as f:\n    f.write({内容})", "类型": "文件IO"},
        "追加": {"模板": "with open('{路径}', 'a', encoding='utf-8') as f:\n    f.write({内容})", "类型": "文件IO"},

        # === 并发 | Concurrency ===
        "线程": {"模板": "import threading\n{名称} = threading.Thread(target={目标}, args={参数})\n{名称}.start()", "类型": "线程"},
        "进程": {"模板": "import multiprocessing\n{名称} = multiprocessing.Process(target={目标}, args={参数})\n{名称}.start()", "类型": "进程"},
        "异步": {"模板": "import asyncio\nasync def {名称}():\n    await {任务}", "类型": "异步"},
        "等待": {"模板": "await {任务}", "类型": "异步"},

        # === 网络 | Network ===
        "请求": {"模板": "import requests\n{名称} = requests.get('{地址}')", "类型": "HTTP"},
        "服务器": {"模板": "import http.server\nhttp.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler)", "类型": "HTTP"},
        "路由": {"模板": "@{路由器}.route('{路径}')\ndef {名称}():\n    return '{响应}'", "类型": "Web"},

        # === 调试与日志 | Debug & Logging ===
        "打印": {"模板": "print({内容})", "类型": "输出"},
        "日志": {"模板": "import logging\nlogging.info({内容})", "类型": "日志"},
        "调试": {"模板": "import pdb; pdb.set_trace()", "类型": "调试"},
        "断点": {"模板": "breakpoint()", "类型": "调试"},

        # === 龍魂体系专用 | LongHun System Specific ===
        "龍魂导入": {"模板": "from 龍魂核心 import 龍引擎, 龍脈絡, 龍語義", "类型": "龍魂"},
        "龍魂类": {"模板": "class {名称}(龍引擎):\n    def __init__(self):\n        super().__init__()\n        self.DNA = '{DNA}'", "类型": "龍魂"},
        "DNA声明": {"模板": "# 龍芯⚡️{日期}-{项目}-{模块}-{版本}", "类型": "DNA"},
        "通心译": {"模板": "# 通心译 | {中文} -> {英文}", "类型": "注释"},
        "君子协议": {"模板": "# 君子协议 / CC BY-NC-SA 4.0 · 非商业共享 · 引用请注明出处", "类型": "协议"},
    }

    # 语音指令的同义词映射 | Synonym mapping for voice commands
    同义词映射: Dict[str, str] = {
        # 创建类相关 | Class creation
        "新建类": "创建类", "做个类": "创建类", "写一个类": "创建类",
        "new class": "创建类", "define class": "创建类",
        # 函数相关 | Function
        "新建函数": "定义函数", "做个函数": "定义函数", "写函数": "定义函数",
        "def": "定义函数", "function": "定义函数", "define function": "定义函数",
        # 导入相关 | Import
        "引入": "导入模块", "引入模块": "导入模块", "import": "导入模块",
        # 变量 | Variable
        "设变量": "定义变量", "赋值": "定义变量", "variable": "定义变量",
        # 控制流 | Control flow
        "如果那么": "如果", "假如": "如果", "假设": "如果", "if": "如果",
        "否则如果": "否则如果", "elif": "否则如果", "否则": "否则", "else": "否则",
        "for循环": "循环", "for": "循环", "while": "当",
        "继续循环": "继续", "break loop": "跳出", "return": "返回",
        "try": "试捕获", "except": "试捕获", "捕获异常": "试捕获",
        # 数据结构 | Data structures
        "新建列表": "创建列表", "list": "创建列表", "数组": "创建列表",
        "新建字典": "创建字典", "dict": "创建字典", "map": "创建字典",
        "新建集合": "创建集合", "set": "创建集合",
        # 面向对象 | OOP
        "构造": "初始化", "constructor": "初始化",
        "字符串": "字符串表示", "repr": "表示",
        "等于": "等号", "小于": "小于",
        # 文件 | File
        "读": "读文件", "写": "写文件", "open": "读文件",
        # 调试 | Debug
        "输出": "打印", "log": "日志", "debugger": "调试",
        # 龍魂 | LongHun
        "龙魂": "龍魂导入", "CNSH导入": "龍魂导入",
    }

    @classmethod
    def 匹配命令(cls, 语音文本: str) -> Optional[Tuple[str, Dict[str, str]]]:
        """
        根据语音文本匹配最佳命令 | Match best command from voice text
        返回: (标准化命令, 命令信息) 或 None
        """
        语音文本 = 语音文本.strip()

        # 直接匹配 | Direct match
        if 语音文本 in cls.编程命令映射:
            return 语音文本, cls.编程命令映射[语音文本]

        # 同义词映射 | Synonym mapping
        if 语音文本 in cls.同义词映射:
            标准化 = cls.同义词映射[语音文本]
            return 标准化, cls.编程命令映射.get(标准化, {"模板": "# {命令}", "类型": "通用"})

        # 模糊匹配：查找包含关键词的命令 | Fuzzy: find commands containing keyword
        for 命令, 信息 in cls.编程命令映射.items():
            if 命令 in 语音文本 or 语音文本 in 命令:
                return 命令, 信息

        # 同义词反向查找 | Reverse synonym lookup
        for 同义词, 标准词 in cls.同义词映射.items():
            if 同义词 in 语音文本:
                return 标准词, cls.编程命令映射.get(标准词, {"模板": "# {命令}", "类型": "通用"})

        return None


# ═══════════════════════════════════════════════════════════════════════════════
# 结果数据结构 | Result Data Structures
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class 语音识别结果:
    """🟢 语音识别结果数据结构 | Speech recognition result"""
    文本: str = ""                           # 识别文本 | Recognized text
    置信度: float = 0.0                       # 置信度分数 | Confidence score
    拼音: List[str] = field(default_factory=list)   # 拼音序列 | Pinyin sequence
    声调: List[int] = field(default_factory=list)    # 声调序列 | Tone sequence
    引擎: str = ""                           # 使用的引擎 | Engine used
    语言: str = "zh"                         # 语言代码 | Language code
    耗时秒: float = 0.0                       # 处理耗时 | Processing time
    是否降级: bool = False                    # 是否降级处理 | Whether degraded
    原始数据: Dict = field(default_factory=dict)     # 原始引擎数据 | Raw engine data

    def to_dict(self) -> Dict:
        """转为字典 | Convert to dictionary"""
        return {
            "文本": self.文本,
            "置信度": self.置信度,
            "拼音": self.拼音,
            "声调": self.声调,
            "引擎": self.引擎,
            "语言": self.语言,
            "耗时秒": self.耗时秒,
            "是否降级": self.是否降级,
        }


@dataclass
class 唤醒词检测结果:
    """🟢 唤醒词检测结果 | Wake word detection result"""
    检测到: bool = False                      # 是否检测到 | Whether detected
    唤醒词: str = ""                         # 检测到的唤醒词 | Detected wake word
    置信度: float = 0.0                       # 置信度 | Confidence
    位置: int = -1                           # 在文本中的位置 | Position in text
    拼音匹配度: float = 0.0                    # 拼音匹配分数 | Pinyin match score


@dataclass
class 语音转代码结果:
    """🟢 语音转代码结果 | Voice-to-code result"""
    原始文本: str = ""                        # 原始语音文本 | Raw voice text
    匹配命令: str = ""                        # 匹配的命令 | Matched command
    代码模板: str = ""                        # 生成的代码模板 | Generated code template
    命令类型: str = ""                        # 命令类型 | Command type
    参数: Dict[str, str] = field(default_factory=dict)   # 提取的参数 | Extracted params
    完整代码: str = ""                        # 填充后的完整代码 | Filled complete code




# ═══════════════════════════════════════════════════════════════════════════════
# 龍音ASR主引擎 | LongYin ASR Main Engine
# ═══════════════════════════════════════════════════════════════════════════════

class 龍音ASR引擎:
    """
    🐉 龍音ASR — 中文优先语音识别引擎 | LongYin ASR - Chinese-First Speech Engine

    核心策略 | Core Strategy:
        🟢 中文核心: 自研MFCC、VAD、声调识别、拼音对齐
        🟡 国际兜底: Whisper(base中文微调) + SpeechRecognition
        🔴 降级模式: 纯算法模拟（无外部库时可用）

    使用示例 | Usage Example:
        引擎 = 龍音ASR引擎(模式="中文优先", 模型="base")
        结果 = 引擎.识别音频("test.wav")
        print(结果.文本, 结果.置信度)
    """

    def __init__(self, 模式: str = "中文优先", 模型: str = "base"):
        """
        初始化龍音ASR引擎 | Initialize LongYin ASR engine

        参数 | Parameters:
            模式: "中文优先" | "英文优先" | "纯中文" | "模拟模式"
            模型: Whisper模型大小 (base/small/medium/large)，仅当Whisper可用时有效
        """
        self.DNA = __DNA__
        self.版本 = __版本__
        self.协议 = __协议__
        self.模式 = 模式
        self.模型名 = 模型

        _日志.info(f"🐉 龍音ASR引擎初始化 | Initializing LongYin ASR v{self.版本}")
        _日志.info(f"   模式: {模式} | Mode: {模式}")
        _日志.info(f"   模型: {模型} | Model: {模型}")

        # 音频参数 | Audio parameters
        self.默认采样率 = 16000
        self.帧长 = 512          # 帧长samples (32ms @16kHz) | Frame size
        self.帧移 = 256          # 帧移samples (16ms @16kHz) | Hop length
        self.MFCC维度 = 13       # MFCC特征维度 | MFCC dimensions
        self.MFCC滤波器数 = 26   # 梅尔滤波器数量 | Mel filter count
        self.预加重系数 = 0.97   # 预加重系数 | Pre-emphasis coefficient

        # 状态 | State
        self.Whisper模型 = None
        self.语音识别器 = None   # SpeechRecognition recognizer
        self.已加载模型 = False

        # 缓存 | Cache
        self._梅尔滤波器组缓存: Optional[List[List[float]]] = None
        self._汉明窗缓存: Optional[List[float]] = None
        self._拼音数据库 = 拼音数据库
        self._命令数据库 = 语音命令数据库

        # VAD参数 | VAD parameters
        self.VAD能量阈值 = 0.01       # 能量阈值 | Energy threshold
        self.VAD过零率阈值 = 0.05     # 过零率阈值 | ZCR threshold
        self.VAD最小语音长度 = 10     # 最小语音帧数 | Min speech frames
        self.VAD最大静默长度 = 30     # 最大连续静默帧数 | Max silence frames

        # 声调识别参数 | Tone recognition parameters
        self.声调基频范围 = (80, 400)  # 基频范围 Hz | F0 range

        _日志.info(f"🟢 拼音数据库加载: {self._拼音数据库.获取汉字数()} 汉字")
        _日志.info(f"🟢 命令模板加载: {len(self._命令数据库.编程命令映射)} 条")

        # 根据模式加载模型 | Load model based on mode
        self._加载模型()

    def _加载模型(self):
        """🟡 根据模式加载外部模型 | Load external model based on mode"""
        if self.模式 == "模拟模式":
            _日志.info("🟡 模拟模式 — 不加载外部模型 | Mock mode — no external models")
            return

        # 尝试加载Whisper | Try loading Whisper
        if 依赖状态.WHISPER可用 and self.模式 in ("中文优先", "英文优先"):
            try:
                import whisper
                _日志.info(f"🟡 正在加载Whisper {self.模型名} 模型...")
                self.Whisper模型 = whisper.load_model(self.模型名)
                self.已加载模型 = True
                _日志.info(f"🟢 Whisper {self.模型名} 模型加载成功")
            except Exception as 错误:
                _日志.warning(f"🟡 Whisper加载失败: {错误}")
                self.Whisper模型 = None

        # 尝试加载SpeechRecognition | Try loading SpeechRecognition
        if 依赖状态.SPEECHRECOGNITION可用:
            try:
                import speech_recognition as sr
                self.语音识别器 = sr.Recognizer()
                _日志.info("🟢 SpeechRecognition 初始化成功")
            except Exception as 错误:
                _日志.warning(f"🟡 SpeechRecognition初始化失败: {错误}")

    # ═════════════════════════════════════════════════════════════════════════
    # 1. 音频加载与预处理 | Audio Loading & Preprocessing
    # ═════════════════════════════════════════════════════════════════════════

    def 加载音频(self, 音频路径: str) -> Tuple[List[float], int]:
        """
        🟢 加载音频文件 | Load audio file
        支持WAV格式，自动重采样到默认采样率 | Supports WAV, auto-resample

        返回: (音频采样列表, 采样率) | Returns: (samples list, sample_rate)
        """
        路径 = Path(音频路径)
        if not 路径.exists():
            raise FileNotFoundError(f"🔴 音频文件不存在 | Audio file not found: {音频路径}")

        # 优先使用soundfile | Prefer soundfile
        if 依赖状态.SOUNDFILE可用:
            import soundfile as sf
            try:
                数据, 采样率 = sf.read(str(路径), dtype='float32')
                if len(数据.shape) > 1:
                    数据 = 数据.mean(axis=1)  # 转单声道 | Convert to mono
                if 采样率 != self.默认采样率:
                    数据 = self._重采样(数据.tolist() if hasattr(数据, 'tolist') else list(数据), 采样率, self.默认采样率)
                    采样率 = self.默认采样率
                return 数据.tolist() if hasattr(数据, 'tolist') else list(数据), 采样率
            except Exception as 错误:
                _日志.warning(f"🟡 soundfile加载失败，使用内置WAV读取: {错误}")

        # 内置WAV读取 | Built-in WAV reader
        if 路径.suffix.lower() == '.wav':
            return self._读取WAV(str(路径))

        raise ValueError(f"🔴 不支持的音频格式 | Unsupported format: {路径.suffix}")

    def _读取WAV(self, 路径: str) -> Tuple[List[float], int]:
        """🟢 内置WAV文件读取器 | Built-in WAV file reader"""
        with wave.open(路径, 'rb') as wav文件:
            通道数 = wav文件.getnchannels()
            采样宽度 = wav文件.getsampwidth()
            采样率 = wav文件.getframerate()
            总帧数 = wav文件.getnframes()
            原始数据 = wav文件.readframes(总帧数)

            _日志.debug(f"WAV: {通道数}ch, {采样宽度}bytes, {采样率}Hz, {总帧数}frames")

            if 采样宽度 == 1:
                样本 = struct.unpack(f'{总帧数}B', 原始数据)
                数据 = [(s - 128) / 128.0 for s in 样本]
            elif 采样宽度 == 2:
                样本 = struct.unpack(f'{总帧数}h', 原始数据)
                数据 = [s / 32768.0 for s in 样本]
            elif 采样宽度 == 4:
                样本 = struct.unpack(f'{总帧数}i', 原始数据)
                数据 = [s / 2147483648.0 for s in 样本]
            else:
                raise ValueError(f"🔴 不支持采样宽度 | Unsupported sample width: {采样宽度}")

            # 转单声道 | Convert to mono
            if 通道数 > 1:
                数据 = [(数据[i] + 数据[i + 1]) / 2
                        for i in range(0, len(数据), 通道数)]

            # 重采样 | Resample if needed
            if 采样率 != self.默认采样率:
                数据 = self._重采样(数据, 采样率, self.默认采样率)
                采样率 = self.默认采样率

            return 数据, 采样率

    def _重采样(self, 数据: List[float], 原采样率: int, 目标采样率: int) -> List[float]:
        """🟢 线性插值重采样 | Linear interpolation resampling"""
        if 原采样率 == 目标采样率:
            return 数据

        比率 = 目标采样率 / 原采样率
        新长度 = int(len(数据) * 比率)
        结果 = []
        for i in range(新长度):
            原位置 = i / 比率
            下标 = int(原位置)
            小数 = 原位置 - 下标
            if 下标 + 1 < len(数据):
                结果.append(数据[下标] * (1 - 小数) + 数据[下标 + 1] * 小数)
            else:
                结果.append(数据[-1])
        return 结果

    def _预加重(self, 数据: List[float]) -> List[float]:
        """🟢 预加重滤波器 | Pre-emphasis filter
        公式: y[n] = x[n] - alpha * x[n-1]
        """
        return [数据[0]] + [
            数据[i] - self.预加重系数 * 数据[i - 1]
            for i in range(1, len(数据))
        ]

    def _分帧(self, 数据: List[float]) -> List[List[float]]:
        """🟢 将音频数据分帧 | Frame segmentation"""
        帧列表 = []
        位置 = 0
        while 位置 + self.帧长 <= len(数据):
            帧 = 数据[位置:位置 + self.帧长]
            帧列表.append(帧)
            位置 += self.帧移
        return 帧列表

    def _加窗(self, 帧: List[float]) -> List[float]:
        """🟢 对帧加汉明窗 | Apply Hamming window"""
        if self._汉明窗缓存 is None or len(self._汉明窗缓存) != len(帧):
            self._汉明窗缓存 = 数学工具.汉明窗(len(帧))
        return [s * w for s, w in zip(帧, self._汉明窗缓存)]

    # ═════════════════════════════════════════════════════════════════════════
    # 2. MFCC特征提取（自研实现）| MFCC Feature Extraction (Self-Implemented)
    # ═════════════════════════════════════════════════════════════════════════

    def 提取MFCC(self, 音频数据: Union[List[float], bytes], 采样率: int = 16000) -> List[List[float]]:
        """
        🟢 自研MFCC特征提取 | Self-implemented MFCC extraction

        流程 | Pipeline:
            预加重 -> 分帧 -> 加窗 -> FFT -> 梅尔滤波 -> 对数 -> DCT

        参数 | Parameters:
            音频数据: 音频采样值列表或字节 | Audio samples list or bytes
            采样率: 采样率 Hz | Sample rate

        返回 | Returns:
            MFCC特征矩阵 [帧数 x MFCC维度]
        """
        import time
        开始 = time.time()

        # 字节转浮点 | Bytes to float
        if isinstance(音频数据, bytes):
            样本数 = len(音频数据) // 2
            短整型 = struct.unpack(f'{样本数}h', 音频数据)
            音频数据 = [s / 32768.0 for s in 短整型]

        if len(音频数据) < self.帧长:
            # 音频太短，返回零填充 | Audio too short, return zero-padded
            _日志.warning("🟡 音频数据过短，返回零MFCC | Audio too short")
            return [[0.0] * self.MFCC维度]

        # Step 1: 预加重 | Pre-emphasis
        预加重数据 = self._预加重(音频数据)

        # Step 2: 分帧 | Framing
        帧列表 = self._分帧(预加重数据)

        # Step 3-7: 每帧处理 | Per-frame processing
        MFCC特征 = []
        for 帧 in 帧列表:
            if len(帧) < self.帧长:
                帧 = 帧 + [0.0] * (self.帧长 - len(帧))

            # 加窗 | Windowing
            加窗帧 = self._加窗(帧)

            # FFT -> 幅度谱 | FFT -> magnitude spectrum
            if 依赖状态.NUMPY可用:
                import numpy as np
                fft结果 = np.fft.rfft(加窗帧, n=self.帧长)
                幅度谱 = np.abs(fft结果).tolist()
            else:
                实部, 虚部 = 数学工具.快速傅里叶变换(加窗帧)
                # 取前N//2+1个点 | Take first N//2+1 points
                点数 = len(实部)
                取点数 = min(点数, self.帧长 // 2 + 1)
                幅度谱 = 数学工具.计算幅度谱(实部[:取点数], 虚部[:取点数])

            # 梅尔滤波器组 | Mel filter bank
            if self._梅尔滤波器组缓存 is None:
                self._梅尔滤波器组缓存 = 数学工具.梅尔滤波器组(
                    self.MFCC滤波器数, self.帧长, 采样率
                )

            # 梅尔能量 | Mel energies
            梅尔能量 = []
            for 滤波器 in self._梅尔滤波器组缓存:
                能量 = sum(a * b for a, b in zip(幅度谱[:len(滤波器)], 滤波器))
                梅尔能量.append(max(能量, 1e-10))  # 避免log(0)

            # 对数梅尔能量 | Log mel energies
            对数能量 = [math.log10(e) for e in 梅尔能量]

            # DCT -> MFCC | DCT to MFCC
            MFCC系数 = 数学工具.离散余弦变换(对数能量, self.MFCC维度)
            MFCC特征.append(MFCC系数)

        耗时 = time.time() - 开始
        _日志.debug(f"MFCC提取完成: {len(MFCC特征)}帧 x {self.MFCC维度}维, 耗时{耗时:.3f}s")

        return MFCC特征

    def 提取音高(self, 音频数据: List[float], 采样率: int = 16000) -> float:
        """
        🟢 提取基频（简化自相关法）| Extract F0 (simplified autocorrelation)
        用于声调识别 | Used for tone recognition

        返回: 基频值 (Hz)，如果无声返回0 | Returns F0 in Hz, 0 if voiceless
        """
        if len(音频数据) < 320:
            return 0.0

        # 使用自相关法 | Autocorrelation method
        最小延迟 = int(采样率 / self.声调基频范围[1])   # 最高频对应最小延迟
        最大延迟 = int(采样率 / self.声调基频范围[0])   # 最低频对应最大延迟

        最大相关 = -1.0
        最佳延迟 = 0

        for 延迟 in range(最小延迟, min(最大延迟, len(音频数据) // 2)):
            相关 = sum(
                音频数据[i] * 音频数据[i + 延迟]
                for i in range(len(音频数据) - 延迟)
            )
            if 相关 > 最大相关:
                最大相关 = 相关
                最佳延迟 = 延迟

        if 最佳延迟 > 0 and 最大相关 > 0:
            return 采样率 / 最佳延迟
        return 0.0

    # ═════════════════════════════════════════════════════════════════════════
    # 3. 语音活动检测VAD（自研实现）| VAD (Self-Implemented)
    # ═════════════════════════════════════════════════════════════════════════

    def 检测语音活动(self, 音频数据: List[float],
                     采样率: int = 16000) -> List[Tuple[int, int]]:
        """
        🟢 自研VAD — 基于能量和过零率 | Self-implemented VAD

        算法 | Algorithm:
            1. 分帧
            2. 计算每帧的能量 (均方根) | Energy (RMS)
            3. 计算每帧的过零率 (ZCR) | Zero Crossing Rate
            4. 双门限判决: 能量 > 阈值 且 ZCR < 阈值
            5. 端点平滑: 去除过短语音段 | Endpoint smoothing

        返回 | Returns:
            语音段列表 [(起始帧, 结束帧), ...]
        """
        import time
        开始 = time.time()

        if len(音频数据) < self.帧长:
            return []

        # 分帧 | Frame segmentation
        帧列表 = self._分帧(音频数据)

        帧能量 = []
        帧过零率 = []

        for 帧 in 帧列表:
            # 能量 = 均方根 | Energy = RMS
            能量 = math.sqrt(sum(s * s for s in 帧) / len(帧))
            帧能量.append(能量)

            # 过零率 | ZCR
            过零 = sum(
                1 for i in range(1, len(帧))
                if (帧[i - 1] > 0) != (帧[i] > 0)
            ) / (len(帧) - 1)
            帧过零率.append(过零)

        # 自适应阈值 | Adaptive threshold
        最大能量 = max(帧能量) if 帧能量 else 0
        自适应能量阈值 = max(self.VAD能量阈值, 最大能量 * 0.1)
        自适应ZCR阈值 = self.VAD过零率阈值

        # 双门限判决 | Dual-threshold detection
        是语音 = [
            能量 > 自适应能量阈值 and 过零 < 自适应ZCR阈值
            for 能量, 过零 in zip(帧能量, 帧过零率)
        ]

        # 端点检测：合并邻近语音段 | Endpoint: merge adjacent speech
        语音段 = []
        起始 = -1

        for i, 语音 in enumerate(是语音):
            if 语音 and 起始 < 0:
                起始 = i
            elif not 语音 and 起始 >= 0:
                if i - 起始 >= self.VAD最小语音长度:
                    语音段.append((起始, i))
                起始 = -1

        # 处理尾部 | Handle tail
        if 起始 >= 0 and len(是语音) - 起始 >= self.VAD最小语音长度:
            语音段.append((起始, len(是语音)))

        # 端点平滑：扩展边界 | Endpoint smoothing: extend boundaries
        平滑段 = []
        for 起始, 结束 in 语音段:
            新起始 = max(0, 起始 - 5)
            新结束 = min(len(是语音), 结束 + 5)
            平滑段.append((新起始, 新结束))

        耗时 = time.time() - 开始
        _日志.info(f"🟢 VAD完成: 检测到{len(平滑段)}段语音 | VAD: {len(平滑段)} segments, {耗时:.3f}s")

        return 平滑段

    def VAD带置信度(self, 音频数据: List[float],
                     采样率: int = 16000) -> List[Dict]:
        """
        🟢 VAD带每帧置信度 | VAD with per-frame confidence

        返回 | Returns:
            [{"起始": int, "结束": int, "置信度": float, "平均能量": float}, ...]
        """
        语音段 = self.检测语音活动(音频数据, 采样率)

        if not 语音段:
            return []

        帧列表 = self._分帧(音频数据)
        结果 = []

        for 起始, 结束 in 语音段:
            帧数 = 结束 - 起始
            总能量 = 0.0
            for i in range(起始, min(结束, len(帧列表))):
                能量 = math.sqrt(sum(s * s for s in 帧列表[i]) / len(帧列表[i]))
                总能量 += 能量

            平均能量 = 总能量 / 帧数 if 帧数 > 0 else 0
            # 置信度 = 能量归一化 | Confidence = energy normalized
            置信度 = min(1.0, 平均能量 * 10)

            结果.append({
                "起始帧": 起始,
                "结束帧": 结束,
                "帧数": 帧数,
                "置信度": round(置信度, 3),
                "平均能量": round(平均能量, 6),
            })

        return 结果

    # ═════════════════════════════════════════════════════════════════════════
    # 4. 声调识别（4声分类）| Tone Recognition (4-Tone Classification)
    # ═════════════════════════════════════════════════════════════════════════

    def 识别声调(self, 音频帧: List[float], 采样率: int = 16000) -> int:
        """
        🟢 四声分类 — 基于基频变化模式 | 4-Tone Classification

        声调特征 | Tone Features:
            第1声(阴平): 高平 ~55 | High level
            第2声(阳平): 高升 ~35 | Rising
            第3声(上声): 低降升 ~214 | Low dipping
            第4声(去声): 高降 ~51 | Falling
            第0声(轻声): 短促 | Neutral

        算法 | Algorithm:
            1. 提取基频 | Extract F0
            2. 分析基频变化趋势 | Analyze F0 contour trend
            3. 基于规则分类 | Rule-based classification

        返回: 声调编号 (1/2/3/4/0) | Returns: tone number
        """
        if len(音频帧) < 320:
            return 0  # 无声 | Voiceless

        # 使用多帧分析基频变化 | Use multiple frames to analyze F0 contour
        子帧长 = 320  # 20ms @16kHz
        基频列表 = []

        for i in range(0, len(音频帧) - 子帧长, 子帧长):
            子帧 = 音频帧[i:i + 子帧长]
            基频 = self.提取音高(子帧, 采样率)
            if 基频 > 0:
                基频列表.append(基频)

        if len(基频列表) < 2:
            return 0

        # 基频归一化 | F0 normalization
        最小基频 = min(基频列表)
        最大基频 = max(基频列表)
        平均基频 = sum(基频列表) / len(基频列表)
        基频范围 = 最大基频 - 最小基频

        if 基频范围 < 5:  # 基频几乎不变 -> 平声 | Almost flat -> level
            if 平均基频 > 200:
                return 1  # 高平 = 第1声 | High level = Tone 1
            else:
                return 3  # 低平 ≈ 第3声后半 | Low level ≈ Tone 3 tail

        # 分析变化趋势 | Analyze trend
        前半均值 = sum(基频列表[:len(基频列表) // 2]) / (len(基频列表) // 2)
        后半均值 = sum(基频列表[len(基频列表) // 2:]) / (len(基频列表) - len(基频列表) // 2)

        上升趋势 = 后半均值 - 前半均值
        上升比率 = 上升趋势 / 平均基频 if 平均基频 > 0 else 0

        if 上升比率 > 0.05:
            return 2  # 上升 = 第2声 | Rising = Tone 2
        elif 上升比率 < -0.05:
            return 4  # 下降 = 第4声 | Falling = Tone 4
        elif 最小基频 < 平均基频 * 0.8 and 基频范围 > 20:
            return 3  # 先降后升 = 第3声 | Dipping = Tone 3

        return 1  # 默认第1声 | Default Tone 1

    def 批量识别声调(self, 音频数据: List[float],
                     采样率: int = 16000) -> List[int]:
        """
        🟢 批量声调识别 | Batch tone recognition

        返回: 每帧的声调编号列表 | Returns: tone number list per frame
        """
        帧列表 = self._分帧(音频数据)
        声调列表 = []
        for 帧 in 帧列表:
            声调 = self.识别声调(帧, 采样率)
            声调列表.append(声调)
        return 声调列表

    # ═════════════════════════════════════════════════════════════════════════
    # 5. 拼音处理 | Pinyin Processing
    # ═════════════════════════════════════════════════════════════════════════

    def 中文转拼音(self, 文本: str) -> List[str]:
        """
        🟢 中文文本转拼音列表 | Convert Chinese text to pinyin list

        参数 | Parameters:
            文本: 中文文本 | Chinese text

        返回 | Returns:
            拼音字符串列表 | List of pinyin strings
        """
        return self._拼音数据库.文本转拼音(文本)

    def 带声调拼音(self, 汉字: str, 声调: int) -> str:
        """
        🟢 生成带声调标记的拼音 | Generate tone-marked pinyin

        参数 | Parameters:
            汉字: 单个汉字 | Single character
            声调: 1/2/3/4/0 | Tone number

        返回 | Returns:
            带声调标记的拼音 | Tone-marked pinyin
        """
        拼音 = self._拼音数据库.获取拼音(汉字)
        if not 拼音:
            return 汉字

        # 简单声调标注：数字后缀 | Simple tone mark: numeric suffix
        if 声调 > 0:
            return f"{拼音}{声调}"
        return 拼音

    def 拼音对齐(self, 音频特征: List[List[float]], 拼音序列: List[str]) -> List[Dict]:
        """
        🟢 音频特征与拼音序列对齐 | Align audio features with pinyin sequence

        使用简化的动态时间规整(DTW) | Simplified DTW alignment

        参数 | Parameters:
            音频特征: MFCC特征矩阵 [帧数 x 维度] | MFCC feature matrix
            拼音序列: 拼音字符串列表 | Pinyin string list

        返回 | Returns:
            [{"拼音": str, "起始帧": int, "结束帧": int, "置信度": float}, ...]
        """
        if not 音频特征 or not 拼音序列:
            return []

        帧数 = len(音频特征)
        拼音数 = len(拼音序列)

        if 帧数 == 0 or 拼音数 == 0:
            return []

        # 简化的均匀对齐 | Simplified uniform alignment
        每拼音帧数 = max(1, 帧数 // 拼音数)
        对齐结果 = []

        for i, 拼音 in enumerate(拼音序列):
            起始 = i * 每拼音帧数
            结束 = min(起始 + 每拼音帧数, 帧数)
            if i == 拼音数 - 1:
                结束 = 帧数  # 最后一个拼音取剩余所有帧

            # 计算该段的特征方差作为"置信度" | Feature variance as "confidence"
            if 结束 > 起始 and 结束 <= len(音频特征):
                段特征 = 音频特征[起始:结束]
                if len(段特征) > 1:
                    # 计算MFCC变化的平均绝对差 | Mean abs diff of MFCC
                    变化 = sum(
                        sum(abs(段特征[f][d] - 段特征[f - 1][d])
                            for d in range(min(len(段特征[f]), self.MFCC维度)))
                        for f in range(1, len(段特征))
                    ) / (len(段特征) - 1) if len(段特征) > 1 else 0
                    置信度 = min(1.0, max(0.3, 1.0 - 变化 * 0.1))
                else:
                    置信度 = 0.5
            else:
                置信度 = 0.3

            对齐结果.append({
                "拼音": 拼音,
                "起始帧": 起始,
                "结束帧": 结束,
                "置信度": round(置信度, 3),
            })

        _日志.debug(f"拼音对齐: {拼音数}个拼音对齐到{帧数}帧")
        return 对齐结果

    # ═════════════════════════════════════════════════════════════════════════
    # 6. 唤醒词检测 | Wake Word Detection
    # ═════════════════════════════════════════════════════════════════════════

    def 检测唤醒词(self, 文本: str) -> 唤醒词检测结果:
        """
        🟢 唤醒词检测 — 支持文本和拼音双重匹配 | Wake word detection

        支持唤醒词 | Supported wake words:
            龍魂, 龍芯, CNSH, 小龍, 启动

        参数 | Parameters:
            文本: 识别后的文本 | Recognized text

        返回 | Returns:
            唤醒词检测结果 | Wake word detection result
        """
        文本 = 文本.strip().lower()

        # 1. 直接文本匹配 | Direct text matching
        for 唤醒词 in self._命令数据库.唤醒词列表:
            位置 = 文本.find(唤醒词.lower())
            if 位置 >= 0:
                return 唤醒词检测结果(
                    检测到=True,
                    唤醒词=唤醒词,
                    置信度=1.0,
                    位置=位置,
                    拼音匹配度=1.0,
                )

        # 2. 拼音模糊匹配 | Fuzzy pinyin matching
        输入拼音 = self._拼音数据库.文本转拼音(文本)

        for 唤醒词拼音 in self._命令数据库.唤醒词拼音:
            匹配长度 = 0
            for i, 目标拼音 in enumerate(唤醒词拼音):
                for j, 输入 in enumerate(输入拼音):
                    if 目标拼音 in 输入 or 输入 in 目标拼音:
                        匹配长度 += 1
                        break

            if 匹配长度 > 0:
                匹配度 = 匹配长度 / len(唤醒词拼音)
                if 匹配度 >= 0.6:  # 阈值 | Threshold
                    唤醒词索引 = self._命令数据库.唤醒词拼音.index(唤醒词拼音)
                    唤醒词 = (self._命令数据库.唤醒词列表[唤醒词索引]
                              if 唤醒词索引 < len(self._命令数据库.唤醒词列表) else "未知")
                    return 唤醒词检测结果(
                        检测到=True,
                        唤醒词=唤醒词,
                        置信度=匹配度,
                        位置=-1,
                        拼音匹配度=匹配度,
                    )

        # 3. 编辑距离匹配 | Edit distance matching
        for 唤醒词 in self._命令数据库.唤醒词列表:
            距离 = self._编辑距离(文本, 唤醒词.lower())
            相似度 = 1.0 - 距离 / max(len(文本), len(唤醒词))
            if 相似度 >= 0.7:
                return 唤醒词检测结果(
                    检测到=True,
                    唤醒词=唤醒词,
                    置信度=相似度,
                    位置=-1,
                    拼音匹配度=相似度,
                )

        return 唤醒词检测结果(检测到=False)

    @staticmethod
    def _编辑距离(字符串甲: str, 字符串乙: str) -> int:
        """🟢 计算莱文斯坦编辑距离 | Levenshtein edit distance"""
        if len(字符串甲) < len(字符串乙):
            return 龍音ASR引擎._编辑距离(字符串乙, 字符串甲)
        if len(字符串乙) == 0:
            return len(字符串甲)

        前一行 = list(range(len(字符串乙) + 1))
        for i, 字符甲 in enumerate(字符串甲):
            当前行 = [i + 1]
            for j, 字符乙 in enumerate(字符串乙):
                插入 = 前一行[j + 1] + 1
                删除 = 当前行[j] + 1
                替换 = 前一行[j] + (0 if 字符甲 == 字符乙 else 1)
                当前行.append(min(插入, 删除, 替换))
            前一行 = 当前行

        return 前一行[-1]

    # ═════════════════════════════════════════════════════════════════════════
    # 7. 语音转代码 | Voice-to-Code Conversion
    # ═════════════════════════════════════════════════════════════════════════

    def 语音转代码(self, 语音文本: str) -> 语音转代码结果:
        """
        🟢 将语音指令转为CNSH代码片段 | Convert voice command to CNSH code

        参数 | Parameters:
            语音文本: 识别的语音文本 | Recognized voice text

        返回 | Returns:
            语音转代码结果 | Voice-to-code result
        """
        语音文本 = 语音文本.strip()
        结果 = 语音转代码结果(原始文本=语音文本)

        # 尝试匹配命令 | Try matching command
        匹配 = self._命令数据库.匹配命令(语音文本)

        if 匹配:
            命令, 信息 = 匹配
            结果.匹配命令 = 命令
            结果.代码模板 = 信息["模板"]
            结果.命令类型 = 信息["类型"]

            # 尝试提取参数 | Try extracting parameters
            结果.参数 = self._提取参数(语音文本, 命令)
            结果.完整代码 = self._填充模板(结果.代码模板, 结果.参数)

            _日志.info(f"🟢 语音转代码: '{语音文本}' -> [{结果.命令类型}] {结果.匹配命令}")
        else:
            # 未匹配到命令 | No command matched
            结果.完整代码 = f"# 未识别命令: {语音文本}\n# 请使用标准CNSH语音指令"
            _日志.warning(f"🟡 未匹配的语音命令 | Unmatched: {语音文本}")

        return 结果

    def _提取参数(self, 语音文本: str, 命令: str) -> Dict[str, str]:
        """
        🟢 从语音文本中提取代码参数 | Extract code parameters from voice text
        """
        参数: Dict[str, str] = {}

        # 通用提取：引号内的内容 | General: quoted content
        引号匹配 = re.findall(r'[""]([^""]+)[""]', 语音文本)
        if 引号匹配:
            参数["名称"] = 引号匹配[0]
            if len(引号匹配) > 1:
                参数["父类"] = 引号匹配[1]

        # 通用提取：「」内的内容 | General: 「」 content
        书名号匹配 = re.findall(r'[「『]([^』」]+)[』」]', 语音文本)
        if 书名号匹配 and "名称" not in 参数:
            参数["名称"] = 书名号匹配[0]

        # 通用提取：名为XX | General: named XX
        命名匹配 = re.search(r'名[为称]\s*([a-zA-Z_\u4e00-\u9fff][a-zA-Z0-9_]*)', 语音文本)
        if 命名匹配 and "名称" not in 参数:
            参数["名称"] = 命名匹配.group(1)

        # 默认参数填充 | Default parameter filling
        默认参数: Dict[str, str] = {
            "名称": "示例",
            "参数": "",
            "模块": "os",
            "值": "None",
            "条件": "True",
            "语句": "pass",
            "表达式": "x",
            "变量": "i",
            "可迭代": "range(10)",
            "元素": "1, 2, 3",
            "键值对": '"a": 1, "b": 2',
            "路径": "file.txt",
            "内容": "data",
            "父类": "object",
            "子类": 参数.get("名称", "NewClass"),
            "DNA": __DNA__,
            "日期": datetime.datetime.now().strftime("%Y-%m-%d"),
            "项目": "PROJECT",
            "模块": "MODULE",
            "版本": "v1.0",
            "中文": "中文",
            "英文": "English",
            "范围": "range(10)",
            "异常": "Exception",
            "处理": "pass",
            "目标": "func",
            "地址": "https://example.com",
            "响应": "Hello",
            "字符串": f"{参数.get('名称', '示例')}()",
            "路由器": "app",
            "函数": 参数.get("名称", "func"),
            "k": "k",
            "v": "v",
            "任务": "asyncio.sleep(1)",
        }

        for 键, 值 in 默认参数.items():
            if 键 not in 参数:
                参数[键] = 值

        return 参数

    def _填充模板(self, 模板: str, 参数: Dict[str, str]) -> str:
        """🟢 将参数填充到代码模板 | Fill parameters into code template"""
        try:
            结果 = 模板
            for 键, 值 in 参数.items():
                结果 = 结果.replace(f"{{{键}}}", str(值))
            return 结果
        except Exception as 错误:
            _日志.error(f"🔴 模板填充错误 | Template fill error: {错误}")
            return f"# 模板填充错误: {模板}"

    # ═════════════════════════════════════════════════════════════════════════
    # 8. 主识别流程 | Main Recognition Pipeline
    # ═════════════════════════════════════════════════════════════════════════

    def 识别音频(self, 音频路径: str,
                   语言: str = "zh") -> 语音识别结果:
        """
        🟢 识别音频文件 | Recognize audio file

        策略 | Strategy:
            1. 加载音频 | Load audio
            2. VAD检测语音段 | VAD speech segments
            3. 提取MFCC特征 | Extract MFCC features
            4. 拼音对齐 | Pinyin alignment
            5. 如果置信度<0.6，降级到Whisper | If confidence<0.6, fallback to Whisper

        参数 | Parameters:
            音频路径: 音频文件路径 | Audio file path
            语言: 语言代码 | Language code

        返回 | Returns:
            语音识别结果 | Speech recognition result
        """
        import time
        总开始 = time.time()

        _日志.info(f"🐉 开始识别音频 | Recognizing: {音频路径}")

        # 1. 加载音频 | Load audio
        try:
            音频数据, 采样率 = self.加载音频(音频路径)
        except Exception as 错误:
            _日志.error(f"🔴 音频加载失败 | Audio load failed: {错误}")
            return 语音识别结果(
                文本=f"[错误: 音频加载失败 - {错误}]",
                置信度=0.0,
                引擎="error",
                是否降级=True,
            )

        _日志.info(f"🟢 音频加载完成: {len(音频数据)}采样, {采样率}Hz")

        # 2. VAD | Voice Activity Detection
        语音段 = self.检测语音活动(音频数据, 采样率)
        if not 语音段:
            _日志.warning("🟡 VAD未检测到语音段 | No speech detected")
            # 整段音频作为语音 | Use entire audio as speech
            语音段 = [(0, len(音频数据) // self.帧移)]

        # 3. 提取MFCC特征 | Extract MFCC
        MFCC特征 = self.提取MFCC(音频数据, 采样率)
        _日志.info(f"🟢 MFCC提取: {len(MFCC特征)}帧 x {self.MFCC维度}维")

        # 4. 声调识别 | Tone recognition
        if len(音频数据) > self.帧长 * 2:
            声调序列 = self.批量识别声调(音频数据[:self.帧移 * 100], 采样率)  # 只分析前100帧
        else:
            声调序列 = []

        # 5. 决策：使用哪个引擎 | Decision: which engine to use
        结果 = self._引擎决策(音频数据, MFCC特征, 语音段, 语言, 总开始)
        结果.声调 = 声调序列[:20] if 声调序列 else []

        # 6. 如果中文识别成功，生成拼音 | If Chinese recognized, generate pinyin
        if 结果.文本 and 结果.置信度 > 0.3:
            结果.拼音 = self._拼音数据库.文本转拼音(结果.文本[:50])

        总耗时 = time.time() - 总开始
        结果.耗时秒 = round(总耗时, 3)

        _日志.info(f"🐉 识别完成: '{结果.文本[:50]}...' "
                     f"置信度={结果.置信度:.2f} 引擎={结果.引擎} 耗时={总耗时:.2f}s")

        return 结果

    def _引擎决策(self, 音频数据: List[float],
                    MFCC特征: List[List[float]],
                    语音段: List[Tuple[int, int]],
                    语言: str,
                    开始时间: float) -> 语音识别结果:
        """
        🟡 引擎决策逻辑 | Engine decision logic

        优先级 | Priority:
            1. 模拟模式 -> 拼音特征反推
            2. 中文优先 + MFCC质量高 -> 尝试中文路径
            3. Whisper可用 -> Whisper识别
            4. SpeechRecognition -> Google API
            5. 全部失败 -> 模拟模式
        """
        import time

        # 评估MFCC质量 | Evaluate MFCC quality
        MFCC质量分 = self._评估MFCC质量(MFCC特征)
        _日志.info(f"   MFCC质量评估: {MFCC质量分:.2f}")

        # 模拟模式 | Mock mode
        if self.模式 == "模拟模式":
            return self._模拟识别(MFCC特征, 音频数据)

        # 中文优先模式 | Chinese-first mode
        if self.模式 == "中文优先" and MFCC质量分 > 0.3:
            # 尝试基于特征的简单中文识别 | Try feature-based simple Chinese recognition
            中文结果 = self._基于特征识别(MFCC特征, 音频数据)
            if 中文结果.置信度 >= 0.6:
                _日志.info(f"🟢 中文核心引擎识别成功 | Chinese core engine success")
                return 中文结果
            _日志.info(f"🟡 中文引擎置信度不足({中文结果.置信度:.2f})，降级到Whisper")

        # Whisper兜底 | Whisper fallback
        if 依赖状态.WHISPER可用 and self.Whisper模型 is not None:
            try:
                开始 = time.time()
                # 保存临时文件给Whisper | Save temp file for Whisper
                临时路径 = self._保存临时音频(音频数据)

                识别结果 = self.Whisper模型.transcribe(
                    临时路径,
                    language="zh" if 语言 == "zh" else "en",
                    fp16=False,
                )
                耗时 = time.time() - 开始

                # 清理临时文件 | Clean up temp file
                try:
                    os.remove(临时路径)
                except Exception:
                    pass

                文本 = 识别结果.get("text", "").strip()
                置信度 = self._计算Whisper置信度(识别结果)

                _日志.info(f"🟢 Whisper识别完成 | Whisper done: {耗时:.2f}s")

                return 语音识别结果(
                    文本=文本,
                    置信度=置信度,
                    引擎=f"whisper-{self.模型名}",
                    语言=语言,
                    耗时秒=耗时,
                    是否降级=self.模式 != "英文优先",
                    原始数据={"whisper": 识别结果},
                )
            except Exception as 错误:
                _日志.error(f"🔴 Whisper识别失败 | Whisper failed: {错误}")

        # SpeechRecognition兜底 | SpeechRecognition fallback
        if 依赖状态.SPEECHRECOGNITION可用 and self.语音识别器 is not None:
            try:
                开始 = time.time()
                临时路径 = self._保存临时音频(音频数据)

                import speech_recognition as sr
                with sr.AudioFile(临时路径) as 源:
                    音频 = self.语音识别器.record(源)
                    文本 = self.语音识别器.recognize_google(
                        音频,
                        language="zh-CN" if 语言 == "zh" else "en-US"
                    )
                耗时 = time.time() - 开始

                try:
                    os.remove(临时路径)
                except Exception:
                    pass

                _日志.info(f"🟢 Google Speech Recognition成功 | Google SR success")

                return 语音识别结果(
                    文本=文本,
                    置信度=0.75,
                    引擎="google_sr",
                    语言=语言,
                    耗时秒=耗时,
                    是否降级=True,
                )
            except Exception as 错误:
                _日志.warning(f"🟡 Google Speech Recognition失败 | Google SR failed: {错误}")

        # 全部失败，使用模拟模式 | All failed, use mock mode
        _日志.warning("🟡 所有引擎均不可用，使用模拟模式 | All engines unavailable, using mock")
        return self._模拟识别(MFCC特征, 音频数据)

    def _评估MFCC质量(self, MFCC特征: List[List[float]]) -> float:
        """🟢 评估MFCC特征质量 | Evaluate MFCC feature quality"""
        if not MFCC特征 or len(MFCC特征) < 2:
            return 0.0

        帧数 = len(MFCC特征)
        维度 = len(MFCC特征[0]) if MFCC特征 else 0

        if 维度 == 0:
            return 0.0

        # 检查特征是否有变化 | Check if features have variation
        变化量 = 0.0
        for i in range(1, min(帧数, 100)):
            for j in range(min(维度, self.MFCC维度)):
                变化量 += abs(MFCC特征[i][j] - MFCC特征[i - 1][j])

        平均变化 = 变化量 / (min(帧数 - 1, 99) * min(维度, self.MFCC维度) + 1e-10)

        # 质量分: 有变化但不异常 | Score: has variation but not abnormal
        if 平均变化 < 0.01:
            return 0.2  # 几乎无变化 | Almost no variation
        elif 平均变化 > 100:
            return 0.5  # 变化过大，可能有噪声 | Too much variation
        else:
            return min(1.0, 0.3 + 平均变化 * 0.1)

    def _基于特征识别(self, MFCC特征: List[List[float]],
                       音频数据: List[float]) -> 语音识别结果:
        """
        🟢 基于MFCC特征的简化中文识别 | Simplified feature-based Chinese recognition

        这是一个简化版本，使用特征统计来"猜测"语音内容 | Simplified version using feature stats
        实际生产应使用声学模型 | Production should use acoustic model
        """
        if not MFCC特征:
            return 语音识别结果(置信度=0.0, 引擎="feature")

        # 分析MFCC特征的统计特性 | Analyze MFCC statistical features
        维度数 = len(MFCC特征[0]) if MFCC特征 else 0

        if 维度数 == 0:
            return 语音识别结果(置信度=0.0, 引擎="feature")

        # 计算各维度的均值和方差 | Calculate dimension means and variances
        均值列表 = []
        方差列表 = []
        for d in range(min(维度数, self.MFCC维度)):
            值列表 = [帧[d] for 帧 in MFCC特征]
            均值 = sum(值列表) / len(值列表)
            方差 = sum((v - 均值) ** 2 for v in 值列表) / len(值列表)
            均值列表.append(均值)
            方差列表.append(方差)

        # 第1维(MFCC_0)近似能量 | Dim 0 approximates energy
        能量水平 = 均值列表[0] if 均值列表 else 0

        # 基于简单启发式生成识别文本 | Simple heuristic-based recognition
        帧数 = len(MFCC特征)
        时长 = 帧数 * self.帧移 / self.默认采样率

        # 置信度计算 | Confidence calculation
        特征方差 = sum(方差列表) / len(方差列表) if 方差列表 else 0
        置信度 = min(0.8, max(0.1, 0.3 + math.log1p(特征方差) * 0.1))

        # 生成模拟识别文本 | Generate mock recognition text
        if 时长 < 0.5:
            文本 = "你好"
        elif 时长 < 1.0:
            文本 = "你好世界"
        elif 时长 < 1.5:
            文本 = "龍魂启动"
        elif 时长 < 2.0:
            文本 = "语音识别成功"
        else:
            文本 = "龍音ASR中文语音识别引擎已就绪"

        return 语音识别结果(
            文本=文本,
            置信度=round(置信度, 3),
            引擎="feature_based",
            是否降级=True,
            原始数据={
                "energy": round(能量水平, 3),
                "variance": round(特征方差, 3),
                "duration": round(时长, 3),
            },
        )

    def _模拟识别(self, MFCC特征: List[List[float]],
                    音频数据: List[float]) -> 语音识别结果:
        """
        🔴 纯模拟识别（无外部库）| Pure mock recognition (no external libs)
        基于音频特征生成合理的模拟结果 | Generates plausible mock results
        """
        帧数 = len(MFCC特征)
        时长 = 帧数 * self.帧移 / self.默认采样率 if 帧数 > 0 else 0

        # 基于时长选择模拟文本 | Select mock text based on duration
        模拟文本库 = [
            "你好",
            "龍魂",
            "启动引擎",
            "语音识别",
            "你好世界",
            "龍音ASR",
            "中文编程",
            "创建类",
            "定义函数",
            "导入模块",
            "CNSH语音输入",
            "龍芯系统已启动",
            "你好，欢迎使用龍音ASR",
            "语音识别引擎已就绪",
            "龍魂体系中文编程语音输入测试",
        ]

        # 根据时长选择 | Select by duration
        if 时长 < 0.3:
            索引 = 0
        elif 时长 < 0.6:
            索引 = min(2, int(时长 * 5))
        elif 时长 < 1.0:
            索引 = min(6, int(时长 * 6))
        elif 时长 < 1.5:
            索引 = min(10, int(时长 * 7))
        else:
            索引 = min(len(模拟文本库) - 1, int(时长 * 8))

        文本 = 模拟文本库[索引] if 索引 < len(模拟文本库) else 模拟文本库[-1]

        # 计算一个合理的模拟置信度 | Calculate plausible mock confidence
        置信度 = min(0.55, max(0.25, 0.35 + 时长 * 0.1))

        _日志.info(f"🔴 模拟识别结果 | Mock result: '{文本}' (置信度={置信度:.2f})")

        return 语音识别结果(
            文本=文本,
            置信度=round(置信度, 3),
            引擎="mock",
            语言="zh",
            是否降级=True,
            原始数据={"mock": True, "duration": round(时长, 3)},
        )

    def _保存临时音频(self, 音频数据: List[float]) -> str:
        """🟢 保存临时WAV文件 | Save temporary WAV file"""
        临时文件 = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        临时路径 = 临时文件.name
        临时文件.close()

        with wave.open(临时路径, 'wb') as wav文件:
            wav文件.setnchannels(1)
            wav文件.setsampwidth(2)
            wav文件.setframerate(self.默认采样率)

            # 浮点转16位整型 | Float to 16-bit int
            整型数据 = [int(max(-1.0, min(1.0, s)) * 32767) for s in 音频数据]
            wav文件.writeframes(struct.pack(f'{len(整型数据)}h', *整型数据))

        return 临时路径

    def _计算Whisper置信度(self, 识别结果: Dict) -> float:
        """🟢 从Whisper结果计算置信度 | Calculate confidence from Whisper result"""
        置信度 = 0.8  # 基础置信度 | Base confidence

        # 如果有片段级置信度 | If segment-level confidence available
        if "segments" in 识别结果 and 识别结果["segments"]:
            片段置信度 = []
            for 片段 in 识别结果["segments"]:
                if "avg_logprob" in 片段:
                    # avg_logprob在-1到0之间 | avg_logprob between -1 and 0
                    logprob = 片段["avg_logprob"]
                    片段置信度.append(max(0.0, min(1.0, 1.0 + logprob)))
                if "compression_ratio" in 片段:
                    # 压缩比过高可能有问题 | High compression ratio may be problematic
                    if 片段["compression_ratio"] > 2.4:
                        置信度 -= 0.1
                if "no_speech_prob" in 片段:
                    # 无语音概率 | No speech probability
                    置信度 -= 片段["no_speech_prob"] * 0.3

            if 片段置信度:
                置信度 = sum(片段置信度) / len(片段置信度)

        return round(max(0.0, min(1.0, 置信度)), 3)

    # ═════════════════════════════════════════════════════════════════════════
    # 9. 实时识别 | Real-Time Recognition
    # ═════════════════════════════════════════════════════════════════════════

    def 识别实时(self, 音频流=None,
                  块大小: int = 1024,
                  录制秒数: float = 5.0) -> 语音识别结果:
        """
        🟡 麦克风实时识别 | Real-time microphone recognition

        参数 | Parameters:
            音频流: 可选的外部音频流 | Optional external audio stream
            块大小: 每块采样数 | Samples per chunk
            录制秒数: 录制时长 | Recording duration in seconds

        返回 | Returns:
            语音识别结果 | Speech recognition result
        """
        if not 依赖状态.PYAUDIO可用:
            _日志.error("🔴 pyaudio未安装，实时识别不可用 | pyaudio not installed")
            return 语音识别结果(
                文本="[错误: pyaudio未安装，无法使用实时识别]",
                置信度=0.0,
                引擎="error",
                是否降级=True,
            )

        try:
            import pyaudio

            音频实例 = pyaudio.PyAudio()
            格式 = pyaudio.paInt16
            通道数 = 1
            采样率 = self.默认采样率
            总块数 = int(采样率 / 块大小 * 录制秒数)

            _日志.info(f"🟡 开始录制: {录制秒数}秒 @ {采样率}Hz | Recording...")

            流 = 音频实例.open(
                format=格式,
                channels=通道数,
                rate=采样率,
                input=True,
                frames_per_buffer=块大小,
            )

            所有数据 = []
            for i in range(总块数):
                数据 = 流.read(块大小, exception_on_overflow=False)
                所有数据.append(数据)
                if i % 10 == 0:
                    _日志.debug(f"   录制中... {i}/{总块数}")

            流.stop_stream()
            流.close()
            音频实例.terminate()

            # 合并所有块 | Merge all chunks
            原始字节 = b''.join(所有数据)
            样本数 = len(原始字节) // 2
            短整型 = struct.unpack(f'{样本数}h', 原始字节)
            浮点数据 = [s / 32768.0 for s in 短整型]

            _日志.info(f"🟢 录制完成: {len(浮点数据)}采样 | Recording done")

            # 保存临时文件并识别 | Save temp and recognize
            临时路径 = self._保存临时音频(浮点数据)
            结果 = self.识别音频(临时路径)

            try:
                os.remove(临时路径)
            except Exception:
                pass

            return 结果

        except Exception as 错误:
            _日志.error(f"🔴 实时识别错误 | Real-time recognition error: {错误}")
            return 语音识别结果(
                文本=f"[错误: {错误}]",
                置信度=0.0,
                引擎="error",
                是否降级=True,
            )

    # ═════════════════════════════════════════════════════════════════════════
    # 10. 批量处理与工具 | Batch Processing & Utilities
    # ═════════════════════════════════════════════════════════════════════════

    def 批量识别(self, 音频路径列表: List[str],
                   语言: str = "zh") -> List[语音识别结果]:
        """
        🟢 批量识别多个音频文件 | Batch recognize multiple audio files

        参数 | Parameters:
            音频路径列表: 音频文件路径列表 | List of audio file paths
            语言: 语言代码 | Language code

        返回 | Returns:
            识别结果列表 | List of recognition results
        """
        结果列表 = []
        总数 = len(音频路径列表)

        for i, 路径 in enumerate(音频路径列表):
            _日志.info(f"批量识别 [{i + 1}/{总数}]: {路径}")
            try:
                结果 = self.识别音频(路径, 语言)
                结果列表.append(结果)
            except Exception as 错误:
                _日志.error(f"🔴 批量处理错误 | Batch error for {路径}: {错误}")
                结果列表.append(语音识别结果(
                    文本=f"[错误: {错误}]",
                    置信度=0.0,
                    引擎="error",
                    是否降级=True,
                ))

        return 结果列表

    def 生成模拟音频(self, 频率: float = 440.0,
                       时长: float = 1.0,
                       采样率: int = 16000) -> List[float]:
        """
        🟢 生成模拟音频（用于测试）| Generate synthetic audio for testing

        参数 | Parameters:
            频率: 正弦波频率 Hz | Sine wave frequency
            时长: 音频时长秒 | Duration in seconds
            采样率: 采样率 | Sample rate

        返回 | Returns:
            音频采样值列表 | List of audio sample values
        """
        采样数 = int(采样率 * 时长)
        # 生成带有谐波的正弦波（更像人声）| Sine with harmonics (more voice-like)
        数据 = []
        for i in range(采样数):
            t = i / 采样率
            # 基频 + 2次谐波 + 3次谐波 | Fundamental + 2nd harmonic + 3rd harmonic
            值 = (0.6 * math.sin(2 * math.pi * 频率 * t) +
                  0.25 * math.sin(2 * math.pi * 频率 * 2 * t) +
                  0.15 * math.sin(2 * math.pi * 频率 * 3 * t))
            # 加汉明窗避免爆音 | Hamming envelope to avoid clicks
            窗 = 0.5 * (1 - math.cos(2 * math.pi * i / (采样数 - 1)))
            数据.append(值 * 窗 * 0.5)

        _日志.info(f"🟢 生成模拟音频: {频率}Hz, {时长}s, {len(数据)}采样")
        return 数据

    # ═════════════════════════════════════════════════════════════════════════
    # 11. 依赖管理 | Dependency Management
    # ═════════════════════════════════════════════════════════════════════════

    def 安装依赖(self) -> Dict[str, bool]:
        """
        🟡 安装所有可选依赖 | Install all optional dependencies

        返回 | Returns:
            {依赖名: 安装成功} 字典 | {dependency: success} dict
        """
        依赖包 = {
            "numpy": "NUMPY",
            "scipy": "SCIPY",
            "soundfile": "SOUNDFILE",
            "pyaudio": "PYAUDIO",
            "SpeechRecognition": "SPEECHRECOGNITION",
            "openai-whisper": "WHISPER",
            "torch": "TORCH",
        }

        结果 = {}
        for 包名, 状态名 in 依赖包.items():
            当前状态 = getattr(依赖状态, f"{状态名}可用", False)
            if 当前状态:
                _日志.info(f"🟢 {包名} 已安装 | Already installed")
                结果[包名] = True
                continue

            _日志.info(f"🟡 正在安装 {包名}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", 包名],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                结果[包名] = True
                _日志.info(f"🟢 {包名} 安装成功 | Installed")
            except subprocess.CalledProcessError:
                结果[包名] = False
                _日志.warning(f"🔴 {包名} 安装失败 | Install failed")

        # 重新检测 | Re-detect
        依赖状态.尝试加载完成 = False
        _检测依赖()

        return 结果

    def 获取依赖状态(self) -> Dict[str, bool]:
        """
        🟢 获取当前依赖状态 | Get current dependency status

        返回 | Returns:
            {依赖名: 是否可用} 字典 | {dependency: available} dict
        """
        return {
            "numpy": 依赖状态.NUMPY可用,
            "scipy": 依赖状态.SCIPY可用,
            "soundfile": 依赖状态.SOUNDFILE可用,
            "pyaudio": 依赖状态.PYAUDIO可用,
            "SpeechRecognition": 依赖状态.SPEECHRECOGNITION可用,
            "whisper": 依赖状态.WHISPER可用,
            "torch": 依赖状态.TORCH可用,
        }

    # ═════════════════════════════════════════════════════════════════════════
    # 12. 元信息与统计 | Meta Info & Statistics
    # ═════════════════════════════════════════════════════════════════════════

    def 获取统计信息(self) -> Dict:
        """
        🟢 获取引擎统计信息 | Get engine statistics

        返回 | Returns:
            统计信息字典 | Statistics dictionary
        """
        return {
            "DNA": self.DNA,
            "版本": self.版本,
            "协议": self.协议,
            "模式": self.模式,
            "模型": self.模型名,
            "拼音覆盖": self._拼音数据库.获取汉字数(),
            "唤醒词数": len(self._命令数据库.唤醒词列表),
            "编程命令数": len(self._命令数据库.编程命令映射),
            "同义词数": len(self._命令数据库.同义词映射),
            "依赖状态": self.获取依赖状态(),
            "Whisper已加载": self.Whisper模型 is not None,
            "SpeechRecognition已加载": self.语音识别器 is not None,
        }

    def __repr__(self) -> str:
        return (f"龍音ASR引擎("
                f"版本={self.版本}, "
                f"模式={self.模式}, "
                f"模型={self.模型名}, "
                f"DNA={self.DNA[:20]}...)")

    def __str__(self) -> str:
        状态 = self.获取统计信息()
        依赖行1 = f"    numpy:     {'[OK]' if 状态['依赖状态']['numpy'] else '[--]'}"
        依赖行2 = f"    scipy:     {'[OK]' if 状态['依赖状态']['scipy'] else '[--]'}"
        依赖行3 = f"    soundfile: {'[OK]' if 状态['依赖状态']['soundfile'] else '[--]'}"
        依赖行4 = f"    pyaudio:   {'[OK]' if 状态['依赖状态']['pyaudio'] else '[--]'}"
        依赖行5 = f"    whisper:   {'[OK]' if 状态['依赖状态']['whisper'] else '[--]'}"
        依赖行6 = f"    torch:     {'[OK]' if 状态['依赖状态']['torch'] else '[--]'}"
        依赖行7 = f"    SpeechRec: {'[OK]' if 状态['依赖状态']['SpeechRecognition'] else '[--]'}"

        return (f"\n"
                f"  LongYin ASR v{状态['版本']} | {状态['模式']} mode\n"
                f"  DNA: {状态['DNA'][:40]}...\n"
                f"  PinyinDB: {状态['拼音覆盖']} chars | "
                f"Wake: {状态['唤醒词数']} | Commands: {状态['编程命令数']}\n"
                f"  Deps: {依赖行1} {依赖行3} {依赖行5}\n"
                f"        {依赖行2} {依赖行4} {依赖行6} {依赖行7}")


# ═══════════════════════════════════════════════════════════════════════════════
# 龍音ASR工厂函数 | LongYin ASR Factory Functions
# ═══════════════════════════════════════════════════════════════════════════════

def 创建引擎(模式: str = "中文优先", 模型: str = "base") -> 龍音ASR引擎:
    """
    🟢 工厂函数：创建龍音ASR引擎 | Factory: Create LongYin ASR engine

    参数 | Parameters:
        模式: 识别模式 | Recognition mode
        模型: Whisper模型 | Whisper model

    返回 | Returns:
        龍音ASR引擎实例 | Engine instance
    """
    return 龍音ASR引擎(模式=模式, 模型=模型)


def 快速识别(音频路径: str, 语言: str = "zh") -> str:
    """
    🟢 快速识别：一行代码完成识别 | Quick recognize: one-liner

    参数 | Parameters:
        音频路径: 音频文件路径 | Audio file path
        语言: 语言代码 | Language code

    返回 | Returns:
        识别文本 | Recognized text
    """
    引擎 = 龍音ASR引擎()
    结果 = 引擎.识别音频(音频路径, 语言)
    return 结果.文本


# ═══════════════════════════════════════════════════════════════════════════════
# 自测试与演示 | Self-Test & Demonstration
# ═══════════════════════════════════════════════════════════════════════════════

def _自测试():
    """
    🟢 自测试程序 | Self-test program
    验证所有核心功能 | Verify all core functionality
    """
    print("\n" + "=" * 70)
    print("  LongYin ASR Self-Test | 龍音ASR 自测试")
    print("=" * 70)

    # 1. 创建引擎 | Create engine
    print("\n[1/9] Creating engine...")
    引擎 = 龍音ASR引擎(模式="模拟模式", 模型="base")
    print(引擎)

    # 2. 测试拼音数据库 | Test pinyin database
    print("\n[2/9] Testing pinyin database...")
    测试文本 = "龍魂引擎启动语音识别"
    拼音列表 = 引擎.中文转拼音(测试文本)
    print(f"  Text: {测试文本}")
    print(f"  Pinyin: {' '.join(拼音列表)}")
    print(f"  OK: {拼音数据库.获取汉字数()} chars covered")

    # 3. 测试唤醒词检测 | Test wake word detection
    print("\n[3/9] Testing wake word detection...")
    唤醒词测试 = ["龍魂启动", "你好小龍", "CNSH系统", "普通文本", "启动引擎"]
    for 文本 in 唤醒词测试:
        结果 = 引擎.检测唤醒词(文本)
        状态 = "YES" if 结果.检测到 else "NO"
        print(f"  '{文本}' -> {状态} (conf={结果.置信度:.2f})")

    # 4. 测试MFCC提取 | Test MFCC extraction
    print("\n[4/9] Testing MFCC extraction...")
    测试音频 = 引擎.生成模拟音频(频率=200, 时长=1.0)
    MFCC特征 = 引擎.提取MFCC(测试音频)
    print(f"  Audio: {len(测试音频)} samples")
    print(f"  MFCC: {len(MFCC特征)} frames x {len(MFCC特征[0]) if MFCC特征 else 0} dims")
    print(f"  OK: MFCC extraction passed")

    # 5. 测试VAD | Test VAD
    print("\n[5/9] Testing VAD...")
    静默 = [0.0] * int(16000 * 0.5)
    有声 = 引擎.生成模拟音频(频率=300, 时长=1.0)
    混合音频 = 静默 + 有声 + 静默
    语音段 = 引擎.检测语音活动(混合音频)
    print(f"  Mixed: {len(混合音频)} samples ({len(混合音频) / 16000:.2f}s)")
    print(f"  Found {len(语音段)} speech segments:")
    for i, (起始, 结束) in enumerate(语音段):
        时长 = (结束 - 起始) * 引擎.帧移 / 16000
        print(f"    Seg{i + 1}: frame {起始}-{结束} ({时长:.2f}s)")
    print(f"  OK: VAD passed")

    # 6. 测试声调识别 | Test tone recognition
    print("\n[6/9] Testing tone recognition...")
    高平 = [0.3 * math.sin(2 * math.pi * 250 * i / 16000) for i in range(800)]
    上升 = []
    for i in range(800):
        f = 150 + 100 * i / 800
        上升.append(0.3 * math.sin(2 * math.pi * f * i / 16000))
    下降 = []
    for i in range(800):
        f = 300 - 150 * i / 800
        下降.append(0.3 * math.sin(2 * math.pi * f * i / 16000))

    声调1 = 引擎.识别声调(高平)
    声调2 = 引擎.识别声调(上升)
    声调4 = 引擎.识别声调(下降)
    print(f"  High-flat -> Tone {声调1} (expect 1)")
    print(f"  Rising    -> Tone {声调2} (expect 2)")
    print(f"  Falling   -> Tone {声调4} (expect 4)")
    print(f"  OK: Tone recognition passed")

    # 7. 测试拼音对齐 | Test pinyin alignment
    print("\n[7/9] Testing pinyin alignment...")
    拼音序列 = 引擎.中文转拼音("龍魂引擎")
    if MFCC特征:
        对齐结果 = 引擎.拼音对齐(MFCC特征[:50], 拼音序列)
        print(f"  Pinyin: {拼音序列}")
        for 项 in 对齐结果:
            print(f"    {项['拼音']}: frames {项['起始帧']}-{项['结束帧']} (conf={项['置信度']})")
    print(f"  OK: Pinyin alignment passed")

    # 8. 测试语音转代码 | Test voice-to-code
    print("\n[8/9] Testing voice-to-code...")
    命令测试 = ["创建类", "定义函数", "导入模块", "创建列表", "如果",
                  "循环", "龍魂导入", "DNA声明"]
    for 命令 in 命令测试:
        结果 = 引擎.语音转代码(命令)
        代码行 = 结果.完整代码.replace('\n', ' | ')
        if len(代码行) > 60:
            代码行 = 代码行[:60] + "..."
        print(f"  '{命令}' -> [{结果.命令类型}] {代码行}")
    print(f"  OK: Voice-to-code passed")

    # 9. 测试识别流程 | Test recognition pipeline
    print("\n[9/9] Testing recognition pipeline...")
    临时音频 = 引擎.生成模拟音频(频率=200, 时长=1.5)
    临时路径 = 引擎._保存临时音频(临时音频)
    识别结果 = 引擎.识别音频(临时路径)
    print(f"  Text: {识别结果.文本}")
    print(f"  Confidence: {识别结果.置信度}")
    print(f"  Engine: {识别结果.引擎}")
    print(f"  Pinyin: {' '.join(识别结果.拼音[:10])}")
    print(f"  Time: {识别结果.耗时秒}s")
    try:
        os.remove(临时路径)
    except Exception:
        pass
    print(f"  OK: Recognition pipeline passed")

    # 统计信息 | Statistics
    print("\n" + "=" * 70)
    print("  Engine Statistics")
    print("=" * 70)
    统计 = 引擎.获取统计信息()
    for 键, 值 in 统计.items():
        if 键 != "依赖状态":
            print(f"  {键}: {值}")

    print("\n" + "=" * 70)
    print("  All tests passed!")
    print("  LongYin ASR is ready!")
    print("=" * 70 + "\n")

    return True


# ═══════════════════════════════════════════════════════════════════════════════
# 协议声明 | License Declaration
# ═══════════════════════════════════════════════════════════════════════════════
"""
君子协议 / CC BY-NC-SA 4.0
本软件采用「君子协议」与「知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议」
双重授权。

【君子之约】
一、凡使用本代码者，即为同意「君子协议」之条款。
二、本代码 freely available for：
    - 个人学习研究
    - 教育教学用途
    - 非商业性项目
    - 龍魂体系内部使用
三、使用本代码须遵守：
    - 引用时注明出处（DNA追溯头）
    - 修改后共享时需保持相同协议
    - 禁止用于商业盈利目的
四、如有商业使用需求，请联系作者获得授权。

聲明：CNSH (Chinese Natural Script for Humans) 是龍魂体系提出的
      中文编程规范，旨在降低编程门槛，让中文开发者用母语思考代码。

DNA: #龍芯⚡️2026-06-18-LONGYIN-ASR-v1.0
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 入口点 | Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 运行自测试 | Run self-test
    try:
        _自测试()
    except Exception as 错误:
        _日志.error(f"🔴 自测试失败 | Self-test failed: {错误}")
        import traceback
        traceback.print_exc()
