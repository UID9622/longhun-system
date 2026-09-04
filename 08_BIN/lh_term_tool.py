#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂系统 · 术语大白话查询工具
DNA: #龍芯⚡️丙午·癸未·丙戌·甲午·䷀乾-TERM-TOOL-V1.2-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
分层许可: 工程层 MulanPSL v2
描述: 查询龍魂+鸿蒙术语的中文大白话解释
用法:
    lh term <术语>           # 查询单个术语
    lh term --list           # 列出所有术语
    lh term --scan <文件>     # 扫描文件中的术语
    lh term --enforce <路径>  # 白话执法扫描器·检查未白话化术语
    lh term --help           # 查看帮助
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
TERM_DB_FILE = ROOT / "01_protocols" / "term_db.json"

# ============================================================
# 术语库（焊死·从协议v1.2提取·龍魂+鸿蒙共生体）
# ============================================================

TERM_DB = {
    # === 端口 ===
    "localhost:8765": {
        "term": "localhost:8765",
        "plain": "本地通讯端口8765",
        "meaning": "你家书房的电脑地址，用来跑龍魂系统核心服务",
        "category": "端口"
    },
    "localhost:9622": {
        "term": "localhost:9622",
        "plain": "本地通讯端口9622",
        "meaning": "专门留给 lh 命令用的，用来执行龍魂系统里的各种指令",
        "category": "端口"
    },
    "localhost:8501": {
        "term": "localhost:8501",
        "plain": "本地通讯端口8501",
        "meaning": "给 Streamlit 这类可视化工具用的，用来展示我们的数据和图表",
        "category": "端口"
    },
    "localhost:8080": {
        "term": "localhost:8080",
        "plain": "本地通讯端口8080",
        "meaning": "常用的网页测试服务器端口，让你在浏览器里预览效果",
        "category": "端口"
    },
    "localhost:11434": {
        "term": "localhost:11434",
        "plain": "本地通讯端口11434",
        "meaning": "给 Ollama 本地大模型用的端口，用来跑 AI 对话",
        "category": "端口"
    },
    "8765": {
        "term": "8765",
        "plain": "龍魂核心服务端口",
        "meaning": "龍魂系统的主服务，用来处理各种核心功能",
        "category": "端口"
    },
    "9622": {
        "term": "9622",
        "plain": "CNSH网关端口",
        "meaning": "专门处理中文编程指令的入口",
        "category": "端口"
    },
    "8501": {
        "term": "8501",
        "plain": "流场可视化端口",
        "meaning": "显示龍魂系统的流场和粒子动画",
        "category": "端口"
    },
    "11434": {
        "term": "11434",
        "plain": "本地大模型端口",
        "meaning": "跑本地AI模型（比如Ollama）用的",
        "category": "端口"
    },

    # === 目录 ===
    "portal": {
        "term": "portal",
        "plain": "门户目录",
        "meaning": "存放系统首页和入口页面的地方，相当于龍魂的'大门'",
        "category": "目录"
    },
    "_work/repos": {
        "term": "_work/repos",
        "plain": "工作代码库目录",
        "meaning": "专门用来存放工作的代码仓库，就像你的工作台",
        "category": "目录"
    },
    "service": {
        "term": "service",
        "plain": "服务层",
        "meaning": "系统里承担不同功能的服务模块所在位置",
        "category": "目录"
    },
    "bin": {
        "term": "bin",
        "plain": "可执行命令目录",
        "meaning": "存放龍魂系统各种命令的地方（比如 lh 命令就在这儿）",
        "category": "目录"
    },
    "config": {
        "term": "config",
        "plain": "配置文件目录",
        "meaning": "存放龍魂系统各种设置文件的地方",
        "category": "目录"
    },
    "logs": {
        "term": "logs",
        "plain": "日志目录",
        "meaning": "存放系统运行记录的地方，出问题时能查这里",
        "category": "目录"
    },
    "data": {
        "term": "data",
        "plain": "数据目录",
        "meaning": "存放系统数据的地方，比如记忆、知识库等",
        "category": "目录"
    },
    "backup": {
        "term": "backup",
        "plain": "备份目录",
        "meaning": "存放系统备份文件的地方",
        "category": "目录"
    },
    "docs": {
        "term": "docs",
        "plain": "文档目录",
        "meaning": "存放系统各种说明文档的地方",
        "category": "目录"
    },
    "scripts": {
        "term": "scripts",
        "plain": "脚本目录",
        "meaning": "存放各种自动化脚本的地方",
        "category": "目录"
    },
    "01_protocols": {
        "term": "01_protocols",
        "plain": "协议归档目录",
        "meaning": "存放龍魂系统所有协议文档的地方，系统规则都在这里",
        "category": "目录"
    },
    "02_SKILLS": {
        "term": "02_SKILLS",
        "plain": "技能库目录",
        "meaning": "存放龍魂系统所有AI技能的目录，每个技能一个文件夹",
        "category": "目录"
    },

    # === 版本 ===
    "v1.0": {
        "term": "v1.0",
        "plain": "版本1.0",
        "meaning": "系统的第一个正式版本，表示功能已经基本稳定",
        "category": "版本"
    },
    "v2.0-beta": {
        "term": "v2.0-beta",
        "plain": "版本2.0测试版",
        "meaning": "新功能的测试版本，可能会有一些BUG，邀请大家一起测试",
        "category": "版本"
    },
    "L1": {
        "term": "L1",
        "plain": "第一层",
        "meaning": "在架构图中，从下往上数的第一层，通常是基础层",
        "category": "版本"
    },
    "P0": {
        "term": "P0",
        "plain": "最高优先级",
        "meaning": "系统里最重要的事，不能改动、不能绕过、不能降级",
        "category": "版本"
    },
    "P1": {
        "term": "P1",
        "plain": "高优先级",
        "meaning": "系统里很重要的事，优先级仅次于P0",
        "category": "版本"
    },
    "P2": {
        "term": "P2",
        "plain": "中优先级",
        "meaning": "系统里一般重要的事，可以按计划推进",
        "category": "版本"
    },

    # === 命令 ===
    "lh deploy": {
        "term": "lh deploy",
        "plain": "执行部署",
        "meaning": "把当前龍魂系统的修改推送到鲲鹏服务器上",
        "category": "命令"
    },
    "lh status": {
        "term": "lh status",
        "plain": "查看系统状态",
        "meaning": "看看龍魂系统现在运行得怎么样，有没有出问题",
        "category": "命令"
    },
    "lh audit": {
        "term": "lh audit",
        "plain": "执行审计",
        "meaning": "对系统进行一次三色审计检查，看看有没有违规的地方",
        "category": "命令"
    },
    "lh dna": {
        "term": "lh dna",
        "plain": "生成DNA追溯码",
        "meaning": "生成一条新的DNA追溯码，用来标记某条数据或某次操作",
        "category": "命令"
    },
    "lh help": {
        "term": "lh help",
        "plain": "查看帮助",
        "meaning": "看看 lh 命令都能干什么，都有哪些子命令可用",
        "category": "命令"
    },
    "lh term": {
        "term": "lh term",
        "plain": "查询术语",
        "meaning": "查询龍魂系统里某个术语的中文大白话解释",
        "category": "命令"
    },
    "deploy": {
        "term": "deploy",
        "plain": "部署",
        "meaning": "把代码/文件推送到服务器上让它们跑起来",
        "category": "命令"
    },

    # === 缩写 ===
    "CNSH": {
        "term": "CNSH",
        "plain": "中文编程语法",
        "meaning": "Chinese Syntax 的缩写——用中文写代码的语法规范",
        "category": "缩写"
    },
    "DNA": {
        "term": "DNA",
        "plain": "追溯码",
        "meaning": "Deoxyribonucleic Acid 的借用——每条数据或操作的唯一身份标识",
        "category": "缩写"
    },
    "GPG": {
        "term": "GPG",
        "plain": "数字签名",
        "meaning": "GNU Privacy Guard 的缩写——给文件或数据签名的工具",
        "category": "缩写"
    },
    "UID": {
        "term": "UID",
        "plain": "用户唯一标识",
        "meaning": "Unique ID 的缩写——龍魂系统里每个用户的唯一编号",
        "category": "缩写"
    },
    "REST": {
        "term": "REST",
        "plain": "接口风格",
        "meaning": "Representational State Transfer 的缩写——一种设计网络接口的方式",
        "category": "缩写"
    },
    "API": {
        "term": "API",
        "plain": "编程接口",
        "meaning": "Application Programming Interface 的缩写——程序之间互相通信的规则",
        "category": "缩写"
    },
    "CLI": {
        "term": "CLI",
        "plain": "命令行工具",
        "meaning": "Command Line Interface 的缩写——在黑色终端窗口里敲命令操作的工具",
        "category": "缩写"
    },
    "JSON": {
        "term": "JSON",
        "plain": "数据格式",
        "meaning": "JavaScript Object Notation 的缩写——一种人和机器都能读懂的数据格式",
        "category": "缩写"
    },
    "SSH": {
        "term": "SSH",
        "plain": "安全远程连接",
        "meaning": "Secure Shell 的缩写——安全地远程登录到另一台电脑的方式",
        "category": "缩写"
    },
    "HTTP": {
        "term": "HTTP",
        "plain": "网页传输协议",
        "meaning": "HyperText Transfer Protocol 的缩写——浏览器和网站之间传数据的规则",
        "category": "缩写"
    },
    "HTTPS": {
        "term": "HTTPS",
        "plain": "加密网页传输",
        "meaning": "HTTP 的加密版本，传输数据时加了锁，别人看不到",
        "category": "缩写"
    },
    "MCP": {
        "term": "MCP",
        "plain": "模型上下文协议",
        "meaning": "Model Context Protocol 的缩写——让AI工具之间互相通信的标准协议",
        "category": "缩写"
    },

    # === 组件 ===
    "三色审计": {
        "term": "三色审计",
        "plain": "三种颜色的检查",
        "meaning": "用🟢🟡🔴三种颜色给系统行为打标签，方便管理",
        "category": "组件"
    },
    "DNA追溯": {
        "term": "DNA追溯",
        "plain": "身份追踪",
        "meaning": "给每条数据、每次操作都打上一个独一无二的'身份证号'",
        "category": "组件"
    },
    "六维对齐": {
        "term": "六维对齐",
        "plain": "六个维度的对齐检查",
        "meaning": "从数据、协议、行为、价值、时间、空间六个维度检查系统是否对齐",
        "category": "组件"
    },
    "CNSH语法": {
        "term": "CNSH语法",
        "plain": "中文编程语法",
        "meaning": "用中文写代码，而不是用英文",
        "category": "组件"
    },
    "四级熔断": {
        "term": "四级熔断",
        "plain": "四级安全保护",
        "meaning": "L0伦理→L1数据→L2人格→L3行为，四个级别自动停止危险操作",
        "category": "组件"
    },
    "通心译": {
        "term": "通心译",
        "plain": "智能翻译",
        "meaning": "龍魂系统里把英文术语翻译成中文+大白话的功能",
        "category": "组件"
    },
    "鲲鹏": {
        "term": "鲲鹏",
        "plain": "华为云服务器",
        "meaning": "龍魂系统部署在华为云上的服务器（IP: 119.13.90.27）",
        "category": "组件"
    },
    "洛书369": {
        "term": "洛书369",
        "plain": "数学不动点",
        "meaning": "龍魂系统核心算法的数学底座，sn=369，不能变动",
        "category": "组件"
    },
    "三才算法": {
        "term": "三才算法",
        "plain": "天地人三层计算",
        "meaning": "龍魂系统核心算法，天·地·人三个维度的计算引擎",
        "category": "组件"
    },
    "龍魂守卫": {
        "term": "龍魂守卫",
        "plain": "自动化守护流程",
        "meaning": "代码进去→主权注入→安全审查→GPG签名→全绿才报，常驻不歇",
        "category": "组件"
    },
    "localhost": {
        "term": "localhost",
        "plain": "本地电脑",
        "meaning": "指你正在用的这台电脑，不是远程的、不是别人的，就是自己的",
        "category": "端口"
    },
    "端口": {
        "term": "端口",
        "plain": "通讯端口",
        "meaning": "就像你家的门牌号，不同的号码通往不同的房间（服务）",
        "category": "端口"
    },
    "IP": {
        "term": "IP",
        "plain": "网络地址",
        "meaning": "Internet Protocol 的缩写——就像你家的邮政地址，网上每台电脑都有一个",
        "category": "缩写"
    },
    "python3": {
        "term": "python3",
        "plain": "Python编程语言",
        "meaning": "一种容易上手的编程语言，龍魂系统主要用它来写",
        "category": "缩写"
    },
    "Ollama": {
        "term": "Ollama",
        "plain": "本地AI运行工具",
        "meaning": "让你在自己电脑上跑AI大模型（不用联网）的工具",
        "category": "组件"
    },

    # === 龍魂核心工作流（v1.2新增） ===
    "lh-station": {
        "term": "lh-station",
        "plain": "代码中转站",
        "meaning": "代码进去 → 过一道龍魂流水线 → 带着主权标识出来",
        "category": "工作流"
    },
    "八步管道": {
        "term": "八步管道",
        "plain": "八道工序",
        "meaning": "检测→注入→编译→安全审查→成本分析→签名→打包→封印",
        "category": "工作流"
    },
    "主权注入": {
        "term": "主权注入",
        "plain": "盖章",
        "meaning": "给代码盖上'中国身份章'，证明它属于中国主权",
        "category": "工作流"
    },
    "交叉编译": {
        "term": "交叉编译",
        "plain": "代编译",
        "meaning": "在一种电脑上编译，给另一种芯片用",
        "category": "工作流"
    },
    "记忆封印": {
        "term": "记忆封印",
        "plain": "加密存档",
        "meaning": "把每次操作记录加密存进记忆库，防篡改",
        "category": "工作流"
    },
    "君子协议": {
        "term": "君子协议",
        "plain": "两套许可",
        "meaning": "思想层CC版权、工程层Mulan开源，说好的规矩",
        "category": "工作流"
    },
    "双轨加密": {
        "term": "双轨加密",
        "plain": "两条加密路",
        "meaning": "国产SM2/SM4国密 + 国际TLS/AES两套标准",
        "category": "工作流"
    },

    # === 鸿蒙共生体（v1.2新增） ===
    "HarmonyOS": {
        "term": "HarmonyOS",
        "plain": "鸿蒙系统",
        "meaning": "华为的操作系统，装在手机、平板、车机、手表上的中国系统",
        "category": "鸿蒙"
    },
    "鸿蒙": {
        "term": "鸿蒙",
        "plain": "华为的操作系统",
        "meaning": "装在手机、平板、车机、手表上的中国自研系统，龍魂的共生体",
        "category": "鸿蒙"
    },
    "共生体": {
        "term": "共生体",
        "plain": "你中有我",
        "meaning": "龍魂给鸿蒙'灵魂'，鸿蒙给龍魂'载体'，谁也离不开谁",
        "category": "鸿蒙"
    },
    "ArkTS": {
        "term": "ArkTS",
        "plain": "鸿蒙的普通话",
        "meaning": "用类似网页脚本的方式写鸿蒙应用，中国系统说中国话",
        "category": "鸿蒙"
    },
    "Hvigor": {
        "term": "Hvigor",
        "plain": "鸿蒙的工头",
        "meaning": "负责把代码打包、优化、编译成可运行的应用",
        "category": "鸿蒙"
    },
    "元服务": {
        "term": "元服务",
        "plain": "免安装小应用",
        "meaning": "不用下载安装、点开就能用的轻量服务",
        "category": "鸿蒙"
    },
    "分布式软总线": {
        "term": "分布式软总线",
        "plain": "设备间的隐形网线",
        "meaning": "让手机、平板、电脑之间数据自动互通",
        "category": "鸿蒙"
    },
    "HiLog": {
        "term": "HiLog",
        "plain": "鸿蒙的记事本",
        "meaning": "记录鸿蒙应用运行日志，出问题能查",
        "category": "鸿蒙"
    },
    "鸿蒙适配器": {
        "term": "鸿蒙适配器",
        "plain": "翻译官",
        "meaning": "让龍魂代码在鸿蒙上跑起来的连接模块",
        "category": "鸿蒙"
    },
    "Ability": {
        "term": "Ability",
        "plain": "能力单元",
        "meaning": "鸿蒙应用里的一个功能模块，相当于一个'房间'",
        "category": "鸿蒙"
    },
    "原子化服务": {
        "term": "原子化服务",
        "plain": "精简小服务",
        "meaning": "只做一件事的服务，用完即走",
        "category": "鸿蒙"
    },
    "DevEco Studio": {
        "term": "DevEco Studio",
        "plain": "鸿蒙开发台",
        "meaning": "华为官方写鸿蒙代码的IDE工具",
        "category": "鸿蒙"
    },
    "鸿蒙四大组件": {
        "term": "鸿蒙四大组件",
        "plain": "四个零件",
        "meaning": "Page/Ability/Service/Data四类基础模块，拼装成应用",
        "category": "鸿蒙"
    },

    # === 芯片适配（v1.2新增） ===
    "昇腾": {
        "term": "昇腾",
        "plain": "华为AI芯片",
        "meaning": "专门用来跑AI计算的国产芯片",
        "category": "芯片"
    },
    "飞腾": {
        "term": "飞腾",
        "plain": "国产服务器芯片",
        "meaning": "国产CPU，兼容ARM指令",
        "category": "芯片"
    },
    "龍芯": {
        "term": "龍芯",
        "plain": "国产芯片",
        "meaning": "完全自主指令集的国产CPU",
        "category": "芯片"
    },
    "申威": {
        "term": "申威",
        "plain": "国产超算芯片",
        "meaning": "用在'神威·太湖之光'超算上的国产芯片",
        "category": "芯片"
    },
    "aarch64": {
        "term": "aarch64",
        "plain": "ARM64位架构",
        "meaning": "一款芯片的'内部方言'，鲲鹏/飞腾都用它",
        "category": "芯片"
    },
}

# 尝试从外部 JSON 文件合并术语库
if TERM_DB_FILE.exists():
    try:
        with open(TERM_DB_FILE, "r", encoding="utf-8") as f:
            external_db = json.load(f)
        TERM_DB.update(external_db)
    except Exception:
        pass


# ============================================================
# 核心功能
# ============================================================

def lookup_term(term: str) -> Optional[dict]:
    """查询术语"""
    if term in TERM_DB:
        return TERM_DB[term]

    # 模糊匹配（小写、去除斜杠等）
    normalized = term.lower().replace("/", "").replace(":", "_").replace("-", "_")
    for key, value in TERM_DB.items():
        key_norm = key.lower().replace("/", "").replace(":", "_").replace("-", "_")
        if key_norm == normalized:
            return value

    return None


def format_output(term: str, data: dict) -> str:
    """格式化单个术语输出"""
    category_emoji = {
        "端口": "🔌", "目录": "📁", "版本": "🏷️",
        "命令": "⚡", "缩写": "🔤", "组件": "🧩",
        "工作流": "⚙️", "鸿蒙": "🧬", "芯片": "💎"
    }
    emoji = category_emoji.get(data.get("category", ""), "📖")
    return f"""
{emoji} 术语: {data['term']}
📝 白话: {data['plain']}
💡 解释: {data['meaning']}"""


def list_all_terms() -> str:
    """列出所有术语"""
    lines = ["📋 龍魂系统术语表\n", "=" * 60]
    by_category = {}
    for data in TERM_DB.values():
        cat = data.get("category", "其他")
        by_category.setdefault(cat, []).append(data)

    for cat in ["端口", "目录", "版本", "命令", "缩写", "组件", "工作流", "鸿蒙", "芯片", "其他"]:
        if cat in by_category:
            lines.append(f"\n🏷️  {cat}类:")
            for data in sorted(by_category[cat], key=lambda x: x["term"]):
                lines.append(f"  {data['term']:24s} → {data['plain']}")
    return "\n".join(lines)


def list_all_json() -> str:
    """列出所有术语（JSON格式）"""
    return json.dumps(list(TERM_DB.values()), ensure_ascii=False, indent=2)


def scan_file_for_terms(filepath: str) -> list:
    """扫描文件，找出其中出现的龍魂术语"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ 文件不存在: {filepath}")
        return []
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return []

    found = []
    for term in TERM_DB:
        if term in content:
            found.append(term)

    return sorted(set(found), key=lambda t: TERM_DB[t].get("category", "") + t)


# ============================================================
# 白话执法扫描器（v1.2新增·--enforce）
# ============================================================

# 常见技术黑话模式（不在术语库中的潜在未白话化词汇）
TECH_JARGON_PATTERNS = [
    r'\bdeploy\b', r'\bserialize\b', r'\bdeserialize\b', r'\brepository\b',
    r'\bendpoint\b', r'\bmiddleware\b', r'\bbackend\b', r'\bfrontend\b',
    r'\bcontainer\b', r'\bdocker\b', r'\bkubernetes\b', r'\bnamespace\b',
    r'\bartifact\b', r'\bartifact\b', r'\borchestrator\b', r'\bprovision\b',
    r'\bload.?balanc', r'\bfailover\b', r'\brollback\b', r'\bscalability\b',
    r'\bthroughput\b', r'\blatency\b', r'\bcache\b', r'\bproxy\b',
    r'\bgateway\b', r'\brouter\b', r'\bdispatcher\b', r'\bworker\b',
    r'\bqueue\b', r'\bpub.?sub\b', r'\bstream\b', r'\bbatch\b',
    r'\bshard\b', r'\bpartition\b', r'\breplica\b', r'\bsnapshot\b',
    r'\brecovery\b', r'\bintegrity\b', r'\bconsistency\b',
]


def enforce_scan_path(scan_path: str) -> tuple:
    """白话执法扫描器：检查路径下的文件，找出未白话化的术语"""
    sp = Path(scan_path)
    if not sp.exists():
        print(f"❌ 路径不存在: {scan_path}")
        return [], []

    # 收集所有文本文件
    text_extensions = {'.py', '.js', '.ts', '.html', '.css', '.md', '.rs',
                       '.json', '.yaml', '.yml', '.toml', '.sh', '.txt',
                       '.java', '.kt', '.swift', '.c', '.cpp', '.h', '.hpp'}
    files_to_scan = []
    if sp.is_file():
        if sp.suffix in text_extensions:
            files_to_scan = [sp]
    else:
        for ext in text_extensions:
            files_to_scan.extend(sp.rglob(f"*{ext}"))
        # 跳过隐藏目录和常见的非源码目录
        files_to_scan = [f for f in files_to_scan
                         if not any(p.startswith('.') or p in {'node_modules', '__pycache__',
                                    '.git', 'dist', 'build', 'target', 'venv', '.venv',
                                    'eggs', '.eggs', '.tox', '.mypy_cache', '.pytest_cache'}
                                    for p in f.parts)]

    violations = []  # 文件中有但不在术语库的技术黑话
    found_terms = []  # 文件中在术语库的术语

    for fp in files_to_scan:
        try:
            content = fp.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        file_black = set()
        for pattern in TECH_JARGON_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for m in matches:
                # 排除已在术语库中的
                if m not in TERM_DB and m.lower() not in [t.lower() for t in TERM_DB]:
                    file_black.add(m)

        file_good = set()
        for term in TERM_DB:
            if term in content:
                file_good.add(term)

        if file_black:
            violations.append((str(fp), sorted(file_black)))
        if file_good:
            found_terms.append((str(fp), sorted(file_good)))

    return violations, found_terms


def print_enforce_report(violations: list, found_terms: list, scan_path: str):
    """打印白话执法报告"""
    total_v = sum(len(v) for _, v in violations)
    total_f = sum(len(v) for _, v in found_terms)

    print(f"\n{'='*60}")
    print(f"🐉 龍魂 · 白话执法扫描报告")
    print(f"{'='*60}")
    print(f"📂 扫描路径: {scan_path}")
    print(f"📊 已白话化: {total_f} 处 · 未白话化: {total_v} 处")

    if violations:
        print(f"\n🔴 未白话化技术黑话（需补大白话解释）:")
        print(f"{'-'*60}")
        for filepath, terms in violations:
            short_path = str(filepath).replace(str(ROOT) + "/", "")
            print(f"\n  📄 {short_path}:")
            for t in terms:
                print(f"     🔴 {t}")
        print(f"\n💡 建议: 每个术语必须配一句中文大白话（参考 lh term --list）")
    else:
        print(f"\n🟢 全部通过！所有技术术语均已白话化。")

    if found_terms:
        print(f"\n🟢 已白话化术语 ({total_f}处):")
        print(f"{'-'*60}")
        for filepath, terms in found_terms[:5]:  # 最多展示5个文件
            short_path = str(filepath).replace(str(ROOT) + "/", "")
            print(f"  📄 {short_path}: {', '.join(terms[:8])}{'...' if len(terms)>8 else ''}")
        if len(found_terms) > 5:
            print(f"  ... 还有 {len(found_terms)-5} 个文件")

    print(f"\n{'='*60}")


def print_time_stamp():
    """输出时间戳"""
    try:
        from lh_time_engine import get_output_stamp
        ts = get_output_stamp()
        if ts:
            print(f"\n{ts}")
    except ImportError:
        pass


# ============================================================
# 命令行入口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂系统 · 术语大白话查询工具（v1.2·龍魂+鸿蒙共生体）",
        epilog="示例: lh term localhost:8765  |  lh term --list  |  lh term --scan README.md  |  lh term --enforce src/",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("term", nargs="?", help="要查询的术语")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有术语")
    parser.add_argument("--json", "-j", action="store_true", help="以JSON格式输出")
    parser.add_argument("--scan", "-s", help="扫描文件中的术语")
    parser.add_argument("--enforce", "-e", help="白话执法扫描器·检查路径下未白话化的技术黑话")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")

    args = parser.parse_args()

    if args.list:
        if args.json:
            print(list_all_json())
        else:
            print(list_all_terms())
        print_time_stamp()
        sys.exit(0)

    if args.scan:
        found = scan_file_for_terms(args.scan)
        if found:
            print(f"📄 文件 {args.scan} 中的术语 ({len(found)}个):\n")
            for t in found:
                data = lookup_term(t)
                if data:
                    if args.verbose:
                        print(format_output(t, data))
                        print()
                    else:
                        print(f"  {t:24s} → {data['plain']}")
        else:
            print(f"📄 文件 {args.scan} 中未发现龍魂术语")
        print_time_stamp()
        sys.exit(0)

    if args.enforce:
        violations, found_terms = enforce_scan_path(args.enforce)
        print_enforce_report(violations, found_terms, args.enforce)
        print_time_stamp()
        sys.exit(0 if len(violations) == 0 else 1)

    if args.term:
        data = lookup_term(args.term)
        if data:
            print(format_output(args.term, data))
        else:
            print(f"❌ 未找到术语: {args.term}")
            print("💡 提示: 使用 'lh term --list' 查看所有术语")

        print_time_stamp()
        sys.exit(0)

    parser.print_help()


if __name__ == "__main__":
    main()
