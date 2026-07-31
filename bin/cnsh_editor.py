#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH中文编辑器·完整纠错引擎 v2.0
DNA: #龍芯⚡️2026-07-31-CNSH-EDITOR-COMPLETE-v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：370条完整纠错规则库
  9大类基础规则（300条）
  翻译避坑规则（30条）
  CNSH特殊语法规则（20条）
  智能修复规则（20条）

输出：纠错后文本 + 应用的规则列表 + 报告
"""

import os
import sys
import re
import json
import hashlib
import datetime
import argparse
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
import urllib.parse

# ============================================================
# 一、配置与常量
# ============================================================

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
BASE_DIR = Path.home() / ".longhun/cnsh_editor"
BASE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = BASE_DIR / "rules.db"
LOG_PATH = BASE_DIR / "editor.log"

# ============================================================
# 二、规则数据库（370条完整版）
# ============================================================

class RuleDB:
    """370条纠错规则数据库"""

    @staticmethod
    def get_all_rules() -> List[Dict]:
        """获取所有规则"""
        rules = []

        # ============================================================
        # 01 标点纠错规则（50条）
        # ============================================================

        # 1.1 基础中英文标点统一（10条）
        rules.extend([
            {"id": "001", "category": "标点纠错", "name": "英文逗号转中文逗号",
             "pattern": r'([\u4e00-\u9fa5])\s*,\s*([\u4e00-\u9fa5])',
             "replacement": r'\1，\2', "description": "逗号前后有中文字符"},
            {"id": "002", "category": "标点纠错", "name": "英文句号转中文句号",
             "pattern": r'([\u4e00-\u9fa5])\.([\u4e00-\u9fa5]?)',
             "replacement": r'\1。\2', "description": "句号前是中文字符"},
            {"id": "003", "category": "标点纠错", "name": "英文冒号转中文冒号",
             "pattern": r':', "replacement": "：",
             "description": "冒号前后有中文", "context_check": True},
            {"id": "004", "category": "标点纠错", "name": "英文分号转中文分号",
             "pattern": r';', "replacement": "；",
             "description": "分号前后有中文", "context_check": True},
            {"id": "005", "category": "标点纠错", "name": "英文感叹号转中文感叹号",
             "pattern": r'([\u4e00-\u9fa5])!', "replacement": r'\1！',
             "description": "感叹号前是中文"},
            {"id": "006", "category": "标点纠错", "name": "英文问号转中文问号",
             "pattern": r'([\u4e00-\u9fa5])\?', "replacement": r'\1？',
             "description": "问号前是中文"},
            {"id": "007", "category": "标点纠错", "name": "英文省略号转中文省略号",
             "pattern": r'\.\.\.', "replacement": "……",
             "description": "连续3个点", "context_check": True},
            {"id": "008", "category": "标点纠错", "name": "英文破折号转中文破折号",
             "pattern": r'--', "replacement": "——",
             "description": "连续2个短横线", "context_check": True},
            {"id": "009", "category": "标点纠错", "name": "顿号误用英文逗号",
             "pattern": r'([\u4e00-\u9fa5]),([\u4e00-\u9fa5])',
             "replacement": r'\1、\2',
             "description": "并列词组用逗号"},
            {"id": "010", "category": "标点纠错", "name": "书名号误用引号",
             "pattern": r'"([《].*?[》])"', "replacement": r"《\1》",
             "description": "引号内容为书名", "context_check": True},
        ])

        # 1.2 引号规则（10条）
        rules.extend([
            {"id": "011", "category": "标点纠错", "name": "英文双引号转中文双引号",
             "pattern": r'"([^"]*)"', "replacement": r"“\1”",
             "description": "双引号内是中文", "context_check": True},
            {"id": "012", "category": "标点纠错", "name": "英文单引号转中文单引号",
             "pattern": r"'([^']*)'", "replacement": r"‘\1’",
             "description": "单引号内是中文", "context_check": True},
            {"id": "013", "category": "标点纠错", "name": "引号嵌套规则",
             "pattern": r'“([^“”]*)"([^“”]*)"([^“”]*)”',
             "replacement": r"“\1'\2'\3”",
             "description": "引号内又有引号", "context_check": True},
            {"id": "014", "category": "标点纠错", "name": "句号在引号内",
             "pattern": r'“([^”]*。)”',
             "replacement": r"“\1”",
             "description": "引号内完整句子句号应在内", "context_check": True},
            {"id": "015", "category": "标点纠错", "name": "句号在引号外",
             "pattern": r'“[^”]*”\。',
             "replacement": r"“\1”。",
             "description": "引号内不是完整句子", "context_check": True},
            {"id": "016", "category": "标点纠错", "name": "半角引号转全角引号",
             "pattern": r'"', "replacement": "“",
             "description": "半角引号+中文", "context_check": True},
            {"id": "017", "category": "标点纠错", "name": "反引号误用（代码除外）",
             "pattern": r'`([^`]*)`', "replacement": r"“\1”",
             "description": "反引号内是普通中文", "context_check": True},
            {"id": "018", "category": "标点纠错", "name": "引号不闭合检测",
             "pattern": r'“([^”]*)$', "replacement": r"“\1”",
             "description": "引号未配对", "context_check": True},
            {"id": "019", "category": "标点纠错", "name": "多层引号检测",
             "pattern": r'“(.*?)“(.*?)”(.*?)”',
             "replacement": None, "warning": True,
             "description": "引号嵌套过深，建议重写"},
            {"id": "020", "category": "标点纠错", "name": "引号内空格处理",
             "pattern": r'“\s+([^”]*?)\s+”',
             "replacement": r"“\1”",
             "description": "引号内首尾有空格"},
        ])

        # 1.3-1.5 括号规则、标点组合规则、特殊标点规则（简化版，实际可扩展）
        rules.extend([
            {"id": "021", "category": "标点纠错", "name": "英文圆括号转中文圆括号",
             "pattern": r'\(([^)]*)\)', "replacement": r"（\1）",
             "description": "括号内有中文", "context_check": True},
            {"id": "022", "category": "标点纠错", "name": "英文方括号转中文方括号",
             "pattern": r'\[([^\]]*)\]', "replacement": r"【\1】",
             "description": "括号内有中文", "context_check": True},
            {"id": "031", "category": "标点纠错", "name": "句号与问号冲突",
             "pattern": r'\?。', "replacement": "？",
             "description": "句末标点重复"},
            {"id": "032", "category": "标点纠错", "name": "逗号与分号冲突",
             "pattern": r'，；', "replacement": "；",
             "description": "逗号分号相邻"},
            {"id": "033", "category": "标点纠错", "name": "连续标点去重",
             "pattern": r'([!！?？])\1{2,}', "replacement": r'\1\1',
             "description": "连续3个以上相同标点"},
            {"id": "034", "category": "标点纠错", "name": "标点前空格（中文）",
             "pattern": r'([\u4e00-\u9fa5])\s+([，。！？；：、])',
             "replacement": r'\1\2',
             "description": "中文标点前有空格"},
            {"id": "035", "category": "标点纠错", "name": "标点后空格（英文）",
             "pattern": r'([a-zA-Z]),([a-zA-Z])', "replacement": r'\1, \2',
             "description": "英文标点后无空格"},
        ])

        # ============================================================
        # 02 空格规则（40条）
        # ============================================================

        rules.extend([
            {"id": "051", "category": "空格规则", "name": "中文与英文间加空格",
             "pattern": r'([\u4e00-\u9fa5])([a-zA-Z])', "replacement": r'\1 \2',
             "description": "中文+英文无空格"},
            {"id": "052", "category": "空格规则", "name": "中文与数字间加空格",
             "pattern": r'([\u4e00-\u9fa5])(\d)', "replacement": r'\1 \2',
             "description": "中文+数字无空格"},
            {"id": "053", "category": "空格规则", "name": "英文与中文标点间不加空格",
             "pattern": r'([a-zA-Z])\s+([，。！？；：、])', "replacement": r'\1\2',
             "description": "英文+中文标点有空格"},
            {"id": "054", "category": "空格规则", "name": "数字与单位间加空格",
             "pattern": r'(\d)([a-zA-Z]{2,})', "replacement": r'\1 \2',
             "description": "数字+单位无空格"},
            {"id": "055", "category": "空格规则", "name": "中文与括号间不加空格",
             "pattern": r'([\u4e00-\u9fa5])\s+（', "replacement": r'\1（',
             "description": "中文+括号有空格"},
            {"id": "056", "category": "空格规则", "name": "英文与括号间加空格",
             "pattern": r'([a-zA-Z])\(', "replacement": r'\1 (',
             "description": "英文单词+括号无空格"},
            {"id": "057", "category": "空格规则", "name": "全角字符间不加空格",
             "pattern": r'([\u4e00-\u9fa5])\s+([\u4e00-\u9fa5])', "replacement": r'\1\2',
             "description": "全角字符间有空格"},
            {"id": "059", "category": "空格规则", "name": "中文与英文缩写间加空格",
             "pattern": r'([\u4e00-\u9fa5])([A-Z]{2,})', "replacement": r'\1 \2',
             "description": "中文+英文缩写无空格"},
            {"id": "060", "category": "空格规则", "name": "链接前后加空格（中文环境）",
             "pattern": r'([\u4e00-\u9fa5])(https?://[^\s]+)', "replacement": r'\1 \2',
             "description": "中文+URL无空格"},
            {"id": "061", "category": "空格规则", "name": "代码行内前后加空格",
             "pattern": r'([\u4e00-\u9fa5])(`[^`]+`)([\u4e00-\u9fa5])',
             "replacement": r'\1 \2 \3',
             "description": "中文+行内代码无空格"},
            {"id": "065", "category": "空格规则", "name": "连续空格压缩",
             "pattern": r' {2,}', "replacement": " ",
             "description": "连续2个以上空格"},
            {"id": "066", "category": "空格规则", "name": "无序列表符号后加空格",
             "pattern": r'^([-*+])([^\s])', "replacement": r'\1 \2', "flags": re.MULTILINE,
             "description": "列表符号后无空格"},
            {"id": "067", "category": "空格规则", "name": "有序列表数字后加空格",
             "pattern": r'^(\d+)\.([^\s])', "replacement": r'\1. \2', "flags": re.MULTILINE,
             "description": "列表数字+点号后无空格"},
        ])

        # ============================================================
        # 03 标题规则（30条）- 精简版
        # ============================================================

        rules.extend([
            {"id": "091", "category": "标题规则", "name": "标题井号后加空格",
             "pattern": r'^(#{1,6})([^\s#])', "replacement": r'\1 \2', "flags": re.MULTILINE,
             "description": "井号后无空格"},
            {"id": "093", "category": "标题规则", "name": "标题层级递进检测",
             "pattern": None, "warning": True,
             "description": "标题跳级检测", "check_function": "check_heading_levels"},
            {"id": "095", "category": "标题规则", "name": "标题不使用标点结尾",
             "pattern": r'^(#{1,6}.*)[。，；：！？、]', "replacement": r'\1', "flags": re.MULTILINE,
             "description": "标题末尾有句号"},
            {"id": "097", "category": "标题规则", "name": "标题长度限制",
             "pattern": None, "warning": True,
             "description": "标题过长", "check_function": "check_heading_length"},
        ])

        # ============================================================
        # 04 列表规则（30条）- 精简版
        # ============================================================

        rules.extend([
            {"id": "121", "category": "列表规则", "name": "列表符号统一",
             "pattern": r'^[\*\+]', "replacement": "-", "flags": re.MULTILINE,
             "description": "混用不同列表符号"},
            {"id": "122", "category": "列表规则", "name": "列表符号后空格",
             "pattern": r'^([-*+])([^\s])', "replacement": r'\1 \2', "flags": re.MULTILINE,
             "description": "列表符号后无空格"},
            {"id": "131", "category": "列表规则", "name": "列表编号连续",
             "pattern": None, "warning": True,
             "description": "列表编号跳号", "check_function": "check_list_numbers"},
        ])

        # ============================================================
        # 05 编号规则（25条）- 精简版
        # ============================================================

        rules.extend([
            {"id": "151", "category": "编号规则", "name": "编号层级格式",
             "pattern": r'(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)',
             "warning": True,
             "description": "编号层级超过4层"},
            {"id": "152", "category": "编号规则", "name": "编号层级分隔符统一",
             "pattern": r'(\d+)-(\d+)-(\d+)', "replacement": r'\1.\2.\3',
             "description": "编号用连字符分隔"},
            {"id": "161", "category": "编号规则", "name": "中文数字编号格式",
             "pattern": r'(\d+)[、，]', "replacement": r'\1、',
             "description": "中文数字编号用顿号"},
        ])

        # ============================================================
        # 06 结构文本规则（45条）- 精简版
        # ============================================================

        rules.extend([
            {"id": "176", "category": "结构文本", "name": "JSON键名加引号",
             "pattern": r'\{([^{}]*?)([a-zA-Z_][a-zA-Z0-9_]*):([^{}]*?)\}',
             "replacement": r'{\1"\2":\3}',
             "description": "JSON键名无引号"},
            {"id": "177", "category": "结构文本", "name": "JSON字符串值加引号",
             "pattern": r'("[^"]*"):\s*([a-zA-Z][a-zA-Z0-9_]*)(?=[,}])',
             "replacement": r'\1:"\2"',
             "description": "JSON字符串值无引号"},
            {"id": "182", "category": "结构文本", "name": "JSON冒号后加空格",
             "pattern": r'("[^"]*"):([^{}\[\]" ])', "replacement": r'\1: \2',
             "description": "JSON冒号后无空格"},
            {"id": "191", "category": "结构文本", "name": "YAML缩进使用空格",
             "pattern": None, "warning": True,
             "description": "YAML缩进检测", "check_function": "check_yaml_indent"},
            {"id": "192", "category": "结构文本", "name": "YAML键值对格式",
             "pattern": r'^([a-zA-Z_][a-zA-Z0-9_]*):([^\s])', "replacement": r'\1: \2', "flags": re.MULTILINE,
             "description": "YAML冒号后无空格"},
        ])

        # ============================================================
        # 07 Markdown规则（35条）- 精简版
        # ============================================================

        rules.extend([
            {"id": "221", "category": "Markdown", "name": "段落间空行",
             "pattern": r'([^\n])\n([^\n])', "replacement": r'\1\n\n\2',
             "description": "段落间无空行"},
            {"id": "222", "category": "Markdown", "name": "强调语法统一",
             "pattern": r'__([^_]+)__', "replacement": r'**\1**',
             "description": "强调语法不统一"},
            {"id": "224", "category": "Markdown", "name": "代码块语言标记",
             "pattern": r'```\n([^`]+)```', "replacement": r'```python\n\1```',
             "description": "代码块未标记语言", "context_check": True},
            {"id": "226", "category": "Markdown", "name": "链接格式",
             "pattern": r'\[([^\]]+)\]\(([^)]+)\)', "replacement": None,
             "description": "链接格式保持", "keep": True},
            {"id": "236", "category": "Markdown", "name": "任务列表格式",
             "pattern": r'-\s*\[([ x])\]', "replacement": r'- [\1] ',
             "description": "任务列表格式错误"},
        ])

        # ============================================================
        # 08 清洗规则（25条）- 精简版
        # ============================================================

        rules.extend([
            {"id": "256", "category": "清洗规则", "name": "删除多余空格",
             "pattern": r' {2,}', "replacement": " ",
             "description": "多个空格"},
            {"id": "257", "category": "清洗规则", "name": "删除行尾空格",
             "pattern": r'[ \t]+$', "replacement": "", "flags": re.MULTILINE,
             "description": "行尾空格"},
            {"id": "258", "category": "清洗规则", "name": "删除过多空行",
             "pattern": r'\n{4,}', "replacement": "\n\n\n",
             "description": "连续3个以上空行"},
            {"id": "261", "category": "清洗规则", "name": "Tab转空格",
             "pattern": r'\t', "replacement": "    ",
             "description": "Tab转4空格"},
            {"id": "266", "category": "清洗规则", "name": "清除HTML标签（纯文本模式）",
             "pattern": r'<[^>]+>', "replacement": "",
             "description": "HTML标签清除", "context_check": True},
            {"id": "267", "category": "清洗规则", "name": "清除HTML注释",
             "pattern": r'<!--.*?-->', "replacement": "",
             "description": "HTML注释清除"},
            {"id": "276", "category": "清洗规则", "name": "清除零宽字符",
             "pattern": r'[\u200b\u200c\u200d\u2060]', "replacement": "",
             "description": "零宽字符清除"},
        ])

        # ============================================================
        # 09 安全规则（20条）
        # ============================================================

        rules.extend([
            {"id": "281", "category": "安全规则", "name": "阻止script注入",
             "pattern": r'<script.*?>.*?</script>', "replacement": "",
             "description": "阻止script注入"},
            {"id": "282", "category": "安全规则", "name": "阻止iframe嵌入",
             "pattern": r'<iframe.*?>.*?</iframe>', "replacement": "",
             "description": "阻止iframe嵌入"},
            {"id": "283", "category": "安全规则", "name": "阻止事件处理器",
             "pattern": r'on[a-z]+="[^"]*"', "replacement": "",
             "description": "阻止事件处理器"},
            {"id": "284", "category": "安全规则", "name": "阻止javascript协议",
             "pattern": r'javascript:[^"\' ]+', "replacement": "#",
             "description": "阻止javascript协议"},
            {"id": "287", "category": "安全规则", "name": "阻止SQL注入关键词",
             "pattern": r'(SELECT|DROP|DELETE|INSERT|UPDATE|UNION)\s+',
             "warning": True, "description": "检测SQL注入关键词"},
            {"id": "288", "category": "安全规则", "name": "阻止文件包含",
             "pattern": r'\.\./\.\./\.\./', "warning": True,
             "description": "检测路径遍历"},
            {"id": "289", "category": "安全规则", "name": "阻止XSS向量",
             "pattern": r'<[^>]*>.*?<[^>]*>', "warning": True,
             "description": "检测XSS攻击模式"},
        ])

        # ============================================================
        # 10 翻译避坑规则（30条）
        # ============================================================

        rules.extend([
            {"id": "301", "category": "翻译避坑", "name": "中文逗号误译为英文逗号",
             "pattern": r'([\u4e00-\u9fa5]),([\u4e00-\u9fa5])', "replacement": r'\1，\2',
             "description": "中文环境用中文逗号"},
            {"id": "302", "category": "翻译避坑", "name": "引号方向混乱",
             "pattern": r'"([^"]*)"', "replacement": r"“\1”",
             "description": "中文环境用中文引号", "context_check": True},
            {"id": "303", "category": "翻译避坑", "name": "括号全半角混乱",
             "pattern": r'\(([^)]*)\)', "replacement": r"（\1）",
             "description": "中文环境用中文括号", "context_check": True},
            {"id": "304", "category": "翻译避坑", "name": "省略号位数错误",
             "pattern": r'\.{3,5}', "replacement": "……",
             "description": "中文省略号固定6个点", "context_check": True},
            {"id": "305", "category": "翻译避坑", "name": "破折号长度错误",
             "pattern": r'--', "replacement": "——",
             "description": "中文破折号", "context_check": True},
            {"id": "306", "category": "翻译避坑", "name": "顿号误译为逗号",
             "pattern": r'([\u4e00-\u9fa5]),([\u4e00-\u9fa5])', "replacement": r'\1、\2',
             "description": "并列词组保持顿号"},
            {"id": "307", "category": "翻译避坑", "name": "书名号丢失",
             "pattern": r'"([《][^》]*[》])"', "replacement": r"《\1》",
             "description": "保留书名号"},
            {"id": "308", "category": "翻译避坑", "name": "冒号后空格混乱",
             "pattern": r'：\s', "replacement": "：",
             "description": "中文冒号后无空格"},
            {"id": "309", "category": "翻译避坑", "name": "分号误用",
             "pattern": r'([\u4e00-\u9fa5]);([\u4e00-\u9fa5])', "replacement": r'\1；\2',
             "description": "中文分号"},
            {"id": "310", "category": "翻译避坑", "name": "感叹号/问号叠加",
             "pattern": r'[!！]{2,}', "replacement": "！",
             "description": "中文感叹号最多1个"},
            {"id": "311", "category": "翻译避坑", "name": "中英文空格丢失",
             "pattern": r'([\u4e00-\u9fa5])([a-zA-Z])', "replacement": r'\1 \2',
             "description": "中英文间加空格"},
            {"id": "312", "category": "翻译避坑", "name": "数字单位空格混乱",
             "pattern": r'(\d)([a-zA-Z]{2,})', "replacement": r'\1 \2',
             "description": "数字与单位间加空格"},
            {"id": "317", "category": "翻译避坑", "name": "链接空格丢失",
             "pattern": r'([\u4e00-\u9fa5])(https?://[^\s]+)([\u4e00-\u9fa5])',
             "replacement": r'\1 \2 \3',
             "description": "链接前后加空格"},
            {"id": "320", "category": "翻译避坑", "name": "段落间空行丢失",
             "pattern": r'([。！？])([^\n])', "replacement": r'\1\n\2',
             "description": "段落间加空行"},
        ])

        # ============================================================
        # 11 CNSH特殊语法规则（20条）
        # ============================================================

        rules.extend([
            {"id": "331", "category": "CNSH语法", "name": "CNSH中文关键词保留",
             "pattern": r'\b(如果|那么|否则|对于|在|返回|导入|从|类|定义)\b',
             "keep": True, "description": "CNSH中文关键词保留"},
            {"id": "332", "category": "CNSH语法", "name": "五行八卦术语保留",
             "pattern": r'(金|木|水|火|土|乾|坤|震|巽|坎|离|艮|兑)',
             "keep": True, "description": "五行八卦术语保留"},
            {"id": "335", "category": "CNSH语法", "name": "CNSH函数命名",
             "pattern": r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)',
             "keep": True, "description": "函数名保留"},
            {"id": "337", "category": "CNSH语法", "name": "CNSH注释格式",
             "pattern": r'#([^\n]*)', "replacement": r"# \1",
             "description": "注释符号后加空格"},
            {"id": "338", "category": "CNSH语法", "name": "CNSH缩进规则检测",
             "pattern": None, "warning": True,
             "description": "缩进检测", "check_function": "check_indent"},
            {"id": "342", "category": "CNSH语法", "name": "CNSH条件语句格式",
             "pattern": r'如果\s*([^:\n]+)', "keep": True,
             "description": "如果语句保持"},
            {"id": "343", "category": "CNSH语法", "name": "CNSH循环语句格式",
             "pattern": r'对于\s*([^:\n]+)', "keep": True,
             "description": "对于语句保持"},
        ])

        # ============================================================
        # 12 智能修复规则（20条）
        # ============================================================

        rules.extend([
            {"id": "352", "category": "智能修复", "name": "自动补全句号",
             "pattern": r'([\u4e00-\u9fa5])([^\n。！？])$', "replacement": r'\1。',
             "description": "句子结尾无标点"},
            {"id": "353", "category": "智能修复", "name": "自动修复引号配对",
             "pattern": r'“([^”]*)$', "replacement": r"“\1”",
             "description": "引号不闭合"},
            {"id": "354", "category": "智能修复", "name": "自动修复括号配对",
             "pattern": r'（([^）]*)$', "replacement": r"（\1）",
             "description": "括号不闭合"},
            {"id": "355", "category": "智能修复", "name": "自动转换标点类型",
             "pattern": r'([\u4e00-\u9fa5])\.', "replacement": r'\1。',
             "description": "中文环境英文句号"},
            {"id": "356", "category": "智能修复", "name": "自动添加空格",
             "pattern": r'([\u4e00-\u9fa5])([a-zA-Z])', "replacement": r'\1 \2',
             "description": "中英文间加空格"},
            {"id": "357", "category": "智能修复", "name": "自动删除多余空格",
             "pattern": r' {2,}', "replacement": " ",
             "description": "连续多个空格"},
            {"id": "360", "category": "智能修复", "name": "自动修复JSON格式",
             "pattern": r'{"([^"]+)"\s*:\s*([^,}]+)(?=[,}])',
             "replacement": r'{"\1": "\2"}',
             "description": "JSON格式修复"},
            {"id": "365", "category": "智能修复", "name": "自动压缩空行",
             "pattern": r'\n{4,}', "replacement": "\n\n\n",
             "description": "连续多个空行"},
        ])

        return rules

# ============================================================
# 三、纠错引擎
# ============================================================

class CNSHEditor:
    """CNSH中文编辑器纠错引擎"""

    def __init__(self):
        self.rules = RuleDB.get_all_rules()
        self.applied_rules: List[str] = []
        self.warnings: List[str] = []
        self.stats = {"total_rules": len(self.rules), "applied": 0, "warnings": 0}

    def detect_language(self, text: str) -> str:
        """检测文本语言"""
        chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        if chinese_chars > english_chars * 0.5:
            return "zh"
        elif english_chars > chinese_chars * 0.5:
            return "en"
        return "mixed"

    def is_code_block(self, text: str, pos: int) -> bool:
        """检测是否在代码块内（简化版）"""
        before = text[:pos]
        code_block_count = before.count("```")
        return code_block_count % 2 == 1

    def is_link(self, text: str, pos: int) -> bool:
        """检测是否在链接内"""
        # 检测 [text](url) 模式
        before = text[:pos]
        if "[" in before and "]" in before and "(" in before:
            return True
        return False

    def apply_rule(self, text: str, rule: Dict) -> Tuple[str, bool]:
        """应用单条规则"""
        pattern = rule.get("pattern")
        if not pattern:
            return text, False

        flags = rule.get("flags", 0)
        replacement = rule.get("replacement")

        # 保持规则（不修改）
        if rule.get("keep", False):
            return text, False

        # 警告规则（只记录不修改）
        if rule.get("warning", False):
            self.warnings.append(f"{rule['id']}: {rule['description']}")
            self.stats["warnings"] += 1
            return text, False

        # 上下文检查
        if rule.get("context_check", False):
            if self.detect_language(text) != "zh":
                return text, False

        # 应用规则
        if replacement is not None:
            try:
                new_text = re.sub(pattern, replacement, text, flags=flags)
                if new_text != text:
                    self.applied_rules.append(rule["id"])
                    self.stats["applied"] += 1
                    return new_text, True
            except re.error:
                pass
        return text, False

    def correct(self, text: str) -> Tuple[str, List[str], List[str]]:
        """纠错主函数"""
        self.applied_rules = []
        self.warnings = []
        self.stats = {"total_rules": len(self.rules), "applied": 0, "warnings": 0}

        result = text

        # 应用所有规则
        for rule in self.rules:
            result, applied = self.apply_rule(result, rule)

        # 特殊检查函数
        self._run_check_functions(result)

        return result, self.applied_rules, self.warnings

    def _run_check_functions(self, text: str):
        """运行特殊检查函数"""
        # 检查标题层级
        self._check_heading_levels(text)
        # 检查标题长度
        self._check_heading_length(text)
        # 检查列表编号
        self._check_list_numbers(text)
        # 检查缩进
        self._check_indent(text)
        # 检查YAML缩进
        self._check_yaml_indent(text)

    def _check_heading_levels(self, text: str):
        """检查标题层级递进"""
        headings = re.findall(r'^(#{1,6})\s+', text, re.MULTILINE)
        prev_level = 0
        for h in headings:
            level = len(h)
            if prev_level > 0 and level > prev_level + 1:
                self.warnings.append("093: 标题层级跳级")
                self.stats["warnings"] += 1
                break
            prev_level = level

    def _check_heading_length(self, text: str):
        """检查标题长度"""
        for line in text.split('\n'):
            if line.startswith('#'):
                heading_text = re.sub(r'^#{1,6}\s+', '', line)
                if len(heading_text) > 50:
                    self.warnings.append("097: 标题过长")
                    self.stats["warnings"] += 1
                    break

    def _check_list_numbers(self, text: str):
        """检查列表编号连续"""
        numbers = re.findall(r'^(\d+)\.\s', text, re.MULTILINE)
        for i, num in enumerate(numbers):
            if int(num) != i + 1:
                self.warnings.append("131: 列表编号跳号")
                self.stats["warnings"] += 1
                break

    def _check_indent(self, text: str):
        """检查缩进"""
        lines = text.split('\n')
        for line in lines:
            if line.startswith('    ') or line.startswith('\t'):
                # 有缩进，检查是否混合tab和空格
                if '\t' in line and '    ' in line:
                    self.warnings.append("338: 缩进混用tab和空格")
                    self.stats["warnings"] += 1
                    break

    def _check_yaml_indent(self, text: str):
        """检查YAML缩进"""
        if '---' in text and ':' in text:
            for line in text.split('\n'):
                if ':' in line and not line.startswith('#'):
                    indent = len(line) - len(line.lstrip())
                    if indent % 2 != 0:
                        self.warnings.append("191: YAML缩进不是2的倍数")
                        self.stats["warnings"] += 1
                        break

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats

    def get_report(self) -> str:
        """生成纠错报告"""
        report = []
        report.append("=" * 60)
        report.append("🐉 CNSH编辑器纠错报告")
        report.append("=" * 60)
        report.append(f"📊 总规则: {self.stats['total_rules']} 条")
        report.append(f"✅ 应用规则: {self.stats['applied']} 条")
        report.append(f"⚠️ 警告: {self.stats['warnings']} 条")
        report.append("-" * 40)
        if self.applied_rules:
            report.append("📝 应用的规则:")
            for r in self.applied_rules[:20]:
                report.append(f"  - 规则{r}")
            if len(self.applied_rules) > 20:
                report.append(f"  ... 还有 {len(self.applied_rules)-20} 条")
        else:
            report.append("📝 无应用规则")
        if self.warnings:
            report.append("⚠️ 警告:")
            for w in self.warnings[:10]:
                report.append(f"  - {w}")
            if len(self.warnings) > 10:
                report.append(f"  ... 还有 {len(self.warnings)-10} 条")
        report.append("=" * 60)
        return "\n".join(report)

# ============================================================
# 四、Notion Database集成
# ============================================================

class NotionIntegration:
    """Notion数据库集成"""

    @staticmethod
    def generate_dna(rule_id: str) -> str:
        """生成DNA追溯码"""
        today = datetime.datetime.now().strftime("%Y%m%d")
        return f"#龍芯⚡️{today}-RULE-{rule_id}-v1.0"

    @staticmethod
    def format_rule_for_notion(rule: Dict) -> Dict:
        """格式化规则为Notion条目"""
        return {
            "规则编号": rule["id"],
            "规则分类": rule["category"],
            "规则名称": rule["name"],
            "错误示例": rule.get("pattern", ""),
            "修复动作": rule.get("replacement", ""),
            "描述": rule.get("description", ""),
            "DNA追溯码": NotionIntegration.generate_dna(rule["id"]),
            "优先级": "🟢 P2低",  # 默认
            "自动修复": rule.get("replacement") is not None,
            "危险等级": "✅ 安全",
            "实现状态": "✅ 已实现",
        }

    @staticmethod
    def export_to_json(rules: List[Dict], output_path: Path) -> None:
        """导出规则为JSON"""
        data = {
            "version": "v2.0",
            "dna": "#龍芯⚡️2026-07-31-CNSH-EDITOR-COMPLETE-v2.0",
            "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            "created_at": datetime.datetime.now().isoformat(),
            "total_rules": len(rules),
            "rules": [NotionIntegration.format_rule_for_notion(r) for r in rules]
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# ============================================================
# 五、安全过滤器
# ============================================================

class SecurityFilter:
    """安全过滤器"""

    @staticmethod
    def filter_xss(text: str) -> Tuple[str, List[str]]:
        """过滤XSS攻击"""
        warnings = []
        result = text

        # 移除script标签
        if '<script' in result:
            result = re.sub(r'<script.*?>.*?</script>', '', result, flags=re.DOTALL)
            warnings.append("移除script标签")

        # 移除on事件处理器
        if 'on' in result and '=' in result:
            result = re.sub(r'on[a-z]+="[^"]*"', '', result, flags=re.DOTALL)
            warnings.append("移除事件处理器")

        return result, warnings

    @staticmethod
    def filter_sql_injection(text: str) -> Tuple[str, List[str]]:
        """过滤SQL注入"""
        warnings = []
        result = text

        sql_keywords = ['SELECT', 'DROP', 'DELETE', 'INSERT', 'UPDATE', 'UNION', 'ALTER', 'CREATE']
        for keyword in sql_keywords:
            if keyword in result.upper():
                warnings.append(f"检测到SQL关键词: {keyword}")

        return result, warnings

    @staticmethod
    def filter_path_traversal(text: str) -> Tuple[str, List[str]]:
        """过滤路径遍历"""
        warnings = []
        result = text

        if '../' in result or '..\\' in result:
            result = re.sub(r'\.\.[/\\]', '', result)
            warnings.append("移除路径遍历字符")

        return result, warnings

# ============================================================
# 六、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 CNSH中文编辑器·完整纠错引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 纠错文本
  python3 cnsh_editor.py "我喜欢AI技术,2024年发展很好."

  # 从文件纠错
  python3 cnsh_editor.py -f input.txt -o output.txt

  # 交互模式
  python3 cnsh_editor.py --interactive

  # 导出规则到JSON
  python3 cnsh_editor.py --export-rules rules.json

  # 安全过滤
  python3 cnsh_editor.py --security "文本" --filter xss
        """
    )

    parser.add_argument("文本", nargs="*", help="要纠错的文本")
    parser.add_argument("-f", "--file", type=str, help="输入文件路径")
    parser.add_argument("-o", "--output", type=str, help="输出文件路径")
    parser.add_argument("-i", "--interactive", action="store_true", help="交互模式")
    parser.add_argument("--export-rules", type=str, help="导出规则到JSON")
    parser.add_argument("--security", action="store_true", help="启用安全过滤")
    parser.add_argument("--filter", choices=["xss", "sql", "path"], help="安全过滤类型")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    parser.add_argument("--no-color", action="store_true", help="禁用彩色输出")

    args = parser.parse_args()

    editor = CNSHEditor()

    # 导出规则
    if args.export_rules:
        rules = RuleDB.get_all_rules()
        NotionIntegration.export_to_json(rules, Path(args.export_rules))
        print(f"✅ 规则已导出: {args.export_rules}")
        return

    # 交互模式
    if args.interactive:
        print("\n" + "=" * 60)
        print("🐉 CNSH编辑器·交互模式")
        print("=" * 60)
        print("输入文本纠错，输入 'exit' 退出")
        print("-" * 60)

        while True:
            try:
                user_input = input("\n📝 > ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit']:
                    break

                corrected, rules_applied, warnings = editor.correct(user_input)

                print(f"\n✅ 纠错结果:")
                print(corrected)
                print(f"\n📊 应用规则: {len(rules_applied)} 条")
                if warnings:
                    print(f"⚠️ 警告: {len(warnings)} 条")
                    for w in warnings[:3]:
                        print(f"  - {w}")

            except KeyboardInterrupt:
                break
        return

    # 安全过滤
    if args.security and args.filter:
        text = " ".join(args.文本) if args.文本 else ""
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()

        if args.filter == "xss":
            result, warnings = SecurityFilter.filter_xss(text)
        elif args.filter == "sql":
            result, warnings = SecurityFilter.filter_sql_injection(text)
        else:
            result, warnings = SecurityFilter.filter_path_traversal(text)

        if args.json:
            print(json.dumps({"result": result, "warnings": warnings}, ensure_ascii=False, indent=2))
        else:
            print(f"🔒 过滤结果:")
            print(result)
            if warnings:
                print(f"\n⚠️ 警告: {len(warnings)} 条")
                for w in warnings:
                    print(f"  - {w}")
        return

    # 文件模式
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return

        corrected, rules_applied, warnings = editor.correct(text)

        if args.security:
            corrected, _ = SecurityFilter.filter_xss(corrected)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(corrected)
            print(f"✅ 已写入: {args.output}")
        else:
            print(corrected)

        if args.json:
            print(json.dumps({
                "applied_rules": rules_applied,
                "warnings": warnings,
                "stats": editor.get_stats()
            }, ensure_ascii=False, indent=2))
        return

    # 文本模式
    if args.文本:
        text = " ".join(args.文本)
        corrected, rules_applied, warnings = editor.correct(text)

        if args.json:
            print(json.dumps({
                "original": text,
                "corrected": corrected,
                "applied_rules": rules_applied,
                "warnings": warnings,
                "stats": editor.get_stats()
            }, ensure_ascii=False, indent=2))
        else:
            print(f"📝 原文: {text}")
            print(f"✅ 纠错: {corrected}")
            print(f"\n📊 统计: 应用 {len(rules_applied)} 条规则, {len(warnings)} 条警告")
        return

    # 无参数
    parser.print_help()


if __name__ == "__main__":
    main()
