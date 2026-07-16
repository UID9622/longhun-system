#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂Notion双向同步守护 v4.0
守护五层目录 ↔ Notion五层数据库

DNA: #龍芯⚡️2026-06-09-LONGHUN-SYNC-v4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅

依赖: watchdog, requests, python-dotenv
    pip3 install watchdog requests python-dotenv

使用方法:
    # 启动全部五层监听
    python3 longhun_sync.py

    # 只监听指定层（如L3公开层）
    python3 longhun_sync.py --layer L3

    # 全量扫描一次后退出
    python3 longhun_sync.py --once

    # 指定层全量同步一次
    python3 longhun_sync.py --once --layer L0
"""

import os
import sys
import json
import hashlib
import time
import platform
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

# ───────────────────────────────────────────────────────────────
# 0. DNA签名常量
# ───────────────────────────────────────────────────────────────
DNA签名 = "#龍芯⚡️2026-06-09-LONGHUN-SYNC-v4.0"
确认码 = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅"
封印码 = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅"
NOTION_API基础URL = "https://api.notion.com/v1"
NOTION版本 = "2022-06-28"
脚本版本 = "4.0.0"

# ───────────────────────────────────────────────────────────────
# 1. 环境变量读取（修复：从~/.longhun/secrets.env读取，不写死DATABASE_ID）
# ───────────────────────────────────────────────────────────────

secrets路径 = os.path.expanduser("~/.longhun/secrets.env")
if os.path.exists(secrets路径):
    load_dotenv(secrets路径)
else:
    # 尝试从当前目录加载
    load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")

五层数据库 = {
    'L0': os.getenv("DB_LU"),      # 干·主权层·龍露
    'L1': os.getenv("DB_JQ"),      # 离·继承层·佳琪
    'L2': os.getenv("DB_AL"),      # 震·战友层·阿龙
    'L3': os.getenv("DB_PUB"),     # 巽·公开层
    'L4': os.getenv("DB_CLOUD"),   # 坎·云端层
}

五层目录 = {
    'L0': os.path.expanduser("~/longhun-lu/"),
    'L1': os.path.expanduser("~/longhun-jq/"),
    'L2': os.path.expanduser("~/longhun-al/"),
    'L3': os.path.expanduser("~/longhun-pub/"),
    'L4': os.path.expanduser("~/longhun-cloud/"),
}

五层名称 = {
    'L0': '干·主权层·龍露',
    'L1': '离·继承层·佳琪',
    'L2': '震·战友层·阿龙',
    'L3': '巽·公开层',
    'L4': '坎·云端层',
}

# ───────────────────────────────────────────────────────────────
# 2. 五大人格v4.0（修复：guardian→p72）
# ───────────────────────────────────────────────────────────────

人格映射 = {
    'wenwen': '雯雯P03·技术整理师',
    'p72': '宝宝P72·龍盾',        # ← 修复：原guardian已修正为p72
    'scout': '侦察兵',
    'architect': '架构师',
    'syncer': '同步官',
}

层默认人格 = {
    'L0': 'wenwen',
    'L1': 'p72',                  # ← 修复：原guardian已修正为p72
    'L2': 'syncer',
    'L3': 'scout',
    'L4': 'architect',
}

# ───────────────────────────────────────────────────────────────
# 3. 彩色日志输出
# ───────────────────────────────────────────────────────────────

颜色码 = {
    '绿': '\033[92m',      # 成功
    '黄': '\033[93m',      # 警告
    '红': '\033[91m',      # 错误
    '蓝': '\033[94m',      # 信息
    '青': '\033[96m',      # 强调
    '灰': '\033[90m',      # 调试
    '重置': '\033[0m',
}


def 日志(级别, 消息):
    """输出彩色日志到控制台"""
    颜色 = {
        '成功': '绿',
        '警告': '黄',
        '错误': '红',
        '信息': '蓝',
        '调试': '灰',
        '强调': '青',
    }.get(级别, '重置')
    前缀 = {
        '成功': '[✅]',
        '警告': '[⚠️]',
        '错误': '[❌]',
        '信息': '[ℹ️]',
        '调试': '[🔍]',
        '强调': '[⚡]',
    }.get(级别, '[?]')
    时间戳 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{颜色码[颜色]}{前缀} [{时间戳}] {消息}{颜色码['重置']}")


# ───────────────────────────────────────────────────────────────
# 4. HTTP请求工具（带3次重试机制）
# ───────────────────────────────────────────────────────────────


def notion请求(方法, 路径, json数据=None, 重试次数=3):
    """发送Notion API请求，带自动重试机制"""
    头信息 = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION版本,
    }
    url = f"{NOTION_API基础URL}{路径}"

    for 尝试 in range(重试次数):
        try:
            if 方法.upper() == "GET":
                响应 = requests.get(url, headers=头信息, timeout=30)
            elif 方法.upper() == "POST":
                响应 = requests.post(url, headers=头信息, json=json数据, timeout=30)
            elif 方法.upper() == "PATCH":
                响应 = requests.patch(url, headers=头信息, json=json数据, timeout=30)
            else:
                日志('错误', f'不支持的HTTP方法: {方法}')
                return None

            if 响应.status_code in (200, 201):
                return 响应.json()
            elif 响应.status_code == 429:  # 限流
                等待 = (尝试 + 1) * 2
                日志('警告', f'Notion API限流，等待{等待}秒后重试...')
                time.sleep(等待)
            else:
                日志('错误', f'HTTP {响应.status_code}: {响应.text[:200]}')
                if 尝试 < 重试次数 - 1:
                    time.sleep(1)
        except requests.exceptions.RequestException as e:
            日志('错误', f'请求异常(尝试{尝试+1}/{重试次数}): {e}')
            if 尝试 < 重试次数 - 1:
                time.sleep(2)

    日志('错误', f'请求失败，已重试{重试次数}次: {url}')
    return None


# ───────────────────────────────────────────────────────────────
# 5. 系统信息（修复：使用platform自动读取，不再写死）
# ───────────────────────────────────────────────────────────────


def 获取系统信息():
    """自动检测系统信息（修复：使用platform模块动态获取）"""
    try:
        系统 = platform.system() or "Unknown"
        版本 = platform.release() or "Unknown"
        节点 = platform.node() or "Unknown"
        架构 = platform.machine() or "Unknown"
        处理器 = platform.processor() or "Unknown"
    except Exception as e:
        日志('警告', f'获取系统信息失败: {e}')
        系统, 版本, 节点, 架构, 处理器 = "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"

    return {
        '主机名': 节点,
        '操作系统': 系统,
        '系统版本': 版本,
        '架构': 架构,
        '处理器': 处理器,
        'Python版本': platform.python_version(),
    }


SYSTEM_INFO = 获取系统信息()


# ───────────────────────────────────────────────────────────────
# 6. 核心功能函数
# ───────────────────────────────────────────────────────────────


def 获取层目录(层键):
    """返回该层对应的本地目录路径"""
    return 五层目录.get(层键)


def 获取层数据库(层键):
    """返回该层对应的Notion数据库ID"""
    return 五层数据库.get(层键)


def 计算文件哈希(文件路径):
    """计算文件的SHA256哈希（修复：hashlib.sha256()要带括号）"""
    try:
        h = hashlib.sha256()  # ← 修复：原hashlib.sha256缺括号
        with open(文件路径, 'rb') as f:
            while True:
                块 = f.read(8192)
                if not 块:
                    break
                h.update(块)
        return h.hexdigest()[:16]  # ← 修复：原h.hexdigest[:16]缺括号
    except Exception as e:
        日志('错误', f'计算哈希失败 {文件路径}: {e}')
        return None


def 获取文件元信息(文件路径):
    """获取文件的完整元信息"""
    try:
        路径对象 = Path(文件路径)
        状态 = 路径对象.stat()
        return {
            '文件名': 路径对象.name,
            '大小': 状态.st_size,
            '修改时间': datetime.fromtimestamp(状态.st_mtime).isoformat(),
            '创建时间': datetime.fromtimestamp(状态.st_ctime).isoformat(),
            '后缀': 路径对象.suffix.lower(),
            '目录': str(路径对象.parent),
        }
    except Exception as e:
        日志('错误', f'获取元信息失败 {文件路径}: {e}')
        return {}


# ───────────────────────────────────────────────────────────────
# 7. Notion数据库操作
# ───────────────────────────────────────────────────────────────


def 创建Notion页面(层键, 文件路径, 文件哈希):
    """将文件信息写入Notion数据库（修复：URL不能空）"""
    数据库ID = 获取层数据库(层键)
    if not 数据库ID:
        日志('错误', f'层 {层键} 没有配置数据库ID')
        return None

    元信息 = 获取文件元信息(文件路径)
    文件名 = 元信息.get('文件名', os.path.basename(文件路径))
    层名 = 五层名称.get(层键, 层键)
    人格键 = 层默认人格.get(层键, 'wenwen')
    人格名 = 人格映射.get(人格键, '未知')
    层名人格 = f"{层名} | {人格名}"
    文件大小 = 元信息.get('大小', 0)
    文件大小可读 = f"{文件大小} 字节" if 文件大小 < 1024 else f"{文件大小/1024:.1f} KB" if 文件大小 < 1048576 else f"{文件大小/1048576:.1f} MB"

    # 构建Notion页面属性
    属性 = {
        "标题": {
            "title": [{"text": {"content": 文件名}}]
        },
        "文件名": {
            "rich_text": [{"text": {"content": 文件名}}]
        },
        "文件哈希": {
            "rich_text": [{"text": {"content": 文件哈希}}]
        },
        "文件路径": {
            "rich_text": [{"text": {"content": str(文件路径)}}]
        },
        "同步时间": {
            "rich_text": [{"text": {"content": datetime.now().isoformat()}}]  # ← 修复：原datetime.now.isoformat缺括号
        },
        "层": {
            "select": {"name": 层名}
        },
        "人格": {
            "rich_text": [{"text": {"content": 层名人格}}]
        },
        "文件大小": {
            "rich_text": [{"text": {"content": 文件大小可读}}]
        },
        "状态": {
            "select": {"name": "已同步"}
        },
        "DNA": {
            "rich_text": [{"text": {"content": DNA签名}}]
        },
    }

    请求体 = {
        "parent": {"database_id": 数据库ID},
        "properties": 属性,
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": f"同步记录 by {SYSTEM_INFO['主机名']}"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": f"{DNA签名}\n{确认码}\n{封印码}"}}],
                    "icon": {"emoji": "🐉"}
                }
            }
        ]
    }

    # ← 修复：原requests.post("", ...)空URL，现使用正确URL
    结果 = notion请求("POST", "/pages", 请求体)

    if 结果:
        页面ID = 结果.get('id', 'unknown')
        日志('成功', f'创建页面 [{层键}] {文件名} → {页面ID[:12]}...')
        return 页面ID
    else:
        日志('错误', f'创建页面失败 [{层键}] {文件名}')
        return None


def 更新Notion页面(页面ID, 文件哈希):
    """更新已有Notion页面的文件哈希"""
    if not 页面ID:
        return None

    请求体 = {
        "properties": {
            "文件哈希": {
                "rich_text": [{"text": {"content": 文件哈希}}]
            },
            "同步时间": {
                "rich_text": [{"text": {"content": datetime.now().isoformat()}}]  # ← 修复：原datetime.now.isoformat缺括号
            },
            "状态": {
                "select": {"name": "已更新"}
            },
            "DNA": {
                "rich_text": [{"text": {"content": DNA签名}}]
            },
        }
    }

    结果 = notion请求("PATCH", f"/pages/{页面ID}", 请求体)

    if 结果:
        日志('成功', f'更新页面 {页面ID[:12]}... 新哈希={文件哈希}')
        return 结果.get('id')
    else:
        日志('错误', f'更新页面失败 {页面ID[:12]}...')
        return None


def 查询Notion页面(层键, 文件名):
    """查询数据库中是否已有该文件"""
    数据库ID = 获取层数据库(层键)
    if not 数据库ID:
        return None

    请求体 = {
        "filter": {
            "and": [
                {
                    "property": "文件名",
                    "rich_text": {
                        "equals": 文件名
                    }
                }
            ]
        },
        "page_size": 10
    }

    结果 = notion请求("POST", f"/databases/{数据库ID}/query", 请求体)

    if 结果 and 结果.get('results'):
        页面 = 结果['results'][0]
        return {
            'id': 页面['id'],
            'hash': 页面.get('properties', {})
            .get('文件哈希', {})
            .get('rich_text', [{}])[0]
            .get('text', {})
            .get('content', '') if 页面.get('properties', {}).get('文件哈希', {}).get('rich_text') else '',
        }
    return None


def 归档Notion页面(页面ID, 文件名):
    """标记页面为已归档（文件被删除时）"""
    if not 页面ID:
        return None

    请求体 = {
        "properties": {
            "状态": {
                "select": {"name": "已归档"}
            },
            "同步时间": {
                "rich_text": [{"text": {"content": datetime.now().isoformat()}}]  # ← 修复：原datetime.now.isoformat缺括号
            },
        },
        "archived": True
    }

    结果 = notion请求("PATCH", f"/pages/{页面ID}", 请求体)

    if 结果:
        日志('信息', f'归档页面 {页面ID[:12]}... 文件={文件名}')
        return 结果.get('id')
    else:
        日志('错误', f'归档页面失败 {页面ID[:12]}...')
        return None


def 更新文件路径(页面ID, 新路径):
    """更新Notion页面中的文件路径（文件移动时）"""
    if not 页面ID:
        return None

    请求体 = {
        "properties": {
            "文件路径": {
                "rich_text": [{"text": {"content": str(新路径)}}]
            },
            "同步时间": {
                "rich_text": [{"text": {"content": datetime.now().isoformat()}}]  # ← 修复：原datetime.now.isoformat缺括号
            },
            "状态": {
                "select": {"name": "已移动"}
            },
        }
    }

    结果 = notion请求("PATCH", f"/pages/{页面ID}", 请求体)

    if 结果:
        日志('成功', f'更新路径 {页面ID[:12]}... → {新路径}')
        return 结果.get('id')
    else:
        日志('错误', f'更新路径失败 {页面ID[:12]}...')
        return None


# ───────────────────────────────────────────────────────────────
# 8. 同步功能
# ───────────────────────────────────────────────────────────────


def 同步文件到Notion(层键, 文件路径):
    """单向同步（本地→Notion）：创建或更新"""
    if not os.path.isfile(文件路径):
        日志('警告', f'文件不存在，跳过: {文件路径}')
        return None

    # 忽略隐藏文件和临时文件
    文件名 = os.path.basename(文件路径)
    if 文件名.startswith('.') or 文件名.endswith('~') or 文件名.endswith('.tmp'):
        日志('调试', f'忽略隐藏/临时文件: {文件名}')
        return None

    # 忽略Python缓存文件
    if '__pycache__' in str(文件路径) or 文件名.endswith('.pyc'):
        return None

    文件哈希 = 计算文件哈希(文件路径)
    if not 文件哈希:
        return None

    # 查询是否已存在
    现有页面 = 查询Notion页面(层键, 文件名)

    if 现有页面:
        现有哈希 = 现有页面.get('hash', '')
        if 现有哈希 == 文件哈希:
            日志('调试', f'哈希未变，跳过: {文件名}')
            return 现有页面['id']
        # 哈希变化，更新
        return 更新Notion页面(现有页面['id'], 文件哈希)
    else:
        # 新文件，创建
        return 创建Notion页面(层键, 文件路径, 文件哈希)


def 全量扫描同步(层键):
    """扫描整个层的目录，全量同步"""
    目录 = 获取层目录(层键)
    if not 目录 or not os.path.isdir(目录):
        日志('错误', f'层 {层键} 目录不存在: {目录}')
        return 0

    日志('强调', f'开始全量扫描 [{层键}] {五层名称.get(层键)} → {目录}')
    同步计数 = 0
    错误计数 = 0

    for 根路径, 子目录, 文件列表 in os.walk(目录):
        # 跳过隐藏目录
        子目录[:] = [d for d in 子目录 if not d.startswith('.')]

        for 文件名 in 文件列表:
            if 文件名.startswith('.') or 文件名.endswith('.tmp'):
                continue

            完整路径 = os.path.join(根路径, 文件名)
            try:
                页面ID = 同步文件到Notion(层键, 完整路径)
                if 页面ID:
                    同步计数 += 1
            except Exception as e:
                日志('错误', f'同步失败 {完整路径}: {e}')
                错误计数 += 1

    日志('成功', f'全量扫描完成 [{层键}] 同步={同步计数} 错误={错误计数}')
    return 同步计数


# ───────────────────────────────────────────────────────────────
# 9. 文件系统事件处理器（修复：on_moved完整实现）
# ───────────────────────────────────────────────────────────────


class 同步处理器(FileSystemEventHandler):
    """Watchdog事件处理器：完整处理文件变更事件"""

    def __init__(self, 层键):
        self.层键 = 层键
        self.层名 = 五层名称.get(层键, 层键)
        日志('信息', f'初始化处理器 [{层键}] {self.层名}')

    def on_created(self, event):
        """文件/目录被创建时触发"""
        if event.is_directory:
            return
        文件路径 = event.src_path
        文件名 = os.path.basename(文件路径)
        日志('信息', f'[{self.层键}] 文件创建: {文件名}')
        try:
            同步文件到Notion(self.层键, 文件路径)
        except Exception as e:
            日志('错误', f'处理创建事件失败: {e}')

    def on_modified(self, event):
        """文件被修改时触发"""
        if event.is_directory:
            return
        文件路径 = event.src_path
        文件名 = os.path.basename(文件路径)
        日志('信息', f'[{self.层键}] 文件修改: {文件名}')
        try:
            同步文件到Notion(self.层键, 文件路径)
        except Exception as e:
            日志('错误', f'处理修改事件失败: {e}')

    def on_moved(self, event):
        """文件被移动/重命名时触发（修复：之前被截断，现已补全）"""
        if event.is_directory:
            return
        旧路径 = event.src_path
        新路径 = event.dest_path
        旧名 = os.path.basename(旧路径)
        新名 = os.path.basename(新路径)
        日志('信息', f'[{self.层键}] 文件移动: {旧名} → {新名}')

        try:
            # 先查找旧文件对应的Notion页面
            现有页面 = 查询Notion页面(self.层键, 旧名)
            if 现有页面:
                # 更新路径和文件名
                更新文件路径(现有页面['id'], 新路径)
                # 如果文件名变了，需要更新标题
                if 旧名 != 新名:
                    请求体 = {
                        "properties": {
                            "标题": {
                                "title": [{"text": {"content": 新名}}]
                            },
                            "文件名": {
                                "rich_text": [{"text": {"content": 新名}}]
                            },
                        }
                    }
                    notion请求("PATCH", f"/pages/{现有页面['id']}", 请求体)
                    日志('成功', f'更新文件名: {旧名} → {新名}')
            else:
                # 旧文件没在Notion中，当作新文件处理
                日志('警告', f'旧文件未找到Notion记录，按新文件处理: {旧名}')
                同步文件到Notion(self.层键, 新路径)
        except Exception as e:
            日志('错误', f'处理移动事件失败: {e}')

    def on_deleted(self, event):
        """文件被删除时触发：标记归档"""
        if event.is_directory:
            return
        文件路径 = event.src_path
        文件名 = os.path.basename(文件路径)
        日志('警告', f'[{self.层键}] 文件删除: {文件名}')

        try:
            现有页面 = 查询Notion页面(self.层键, 文件名)
            if 现有页面:
                归档Notion页面(现有页面['id'], 文件名)
            else:
                日志('调试', f'删除的文件未在Notion中记录: {文件名}')
        except Exception as e:
            日志('错误', f'处理删除事件失败: {e}')


# ───────────────────────────────────────────────────────────────
# 10. 监听启动
# ───────────────────────────────────────────────────────────────


def 启动层监听(层键):
    """为指定层启动watchdog监听"""
    目录 = 获取层目录(层键)
    数据库ID = 获取层数据库(层键)

    if not 目录 or not os.path.isdir(目录):
        日志('错误', f'层 {层键} 目录不存在，无法启动监听: {目录}')
        return None

    if not 数据库ID:
        日志('警告', f'层 {层键} 未配置数据库ID，跳过监听')
        return None

    # 确保目录存在
    os.makedirs(目录, exist_ok=True)

    处理器 = 同步处理器(层键)
    观测器 = Observer()
    观测器.schedule(处理器, 目录, recursive=True)
    观测器.start()

    日志('成功', f'已启动监听 [{层键}] {五层名称.get(层键)} → {目录}')
    return 观测器


def 启动全部监听():
    """启动所有5层的watchdog监听"""
    观测器列表 = []
    日志('强调', f'=== 龍魂Notion同步守护 v{脚本版本} 启动 ===')
    日志('信息', f'主机: {SYSTEM_INFO["主机名"]} | 系统: {SYSTEM_INFO["操作系统"]} {SYSTEM_INFO["系统版本"]}')

    for 层键 in ['L0', 'L1', 'L2', 'L3', 'L4']:
        观测器 = 启动层监听(层键)
        if 观测器:
            观测器列表.append((层键, 观测器))

    日志('成功', f'共启动 {len(观测器列表)} 层监听')
    return 观测器列表


# ───────────────────────────────────────────────────────────────
# 11. 主入口（修复：之前缺失if __name__ == "__main__"）
# ───────────────────────────────────────────────────────────────


def 打印启动画面():
    """打印龍魂启动画面"""
    print(f"""
{颜色码['青']}
  🐉 ╔══════════════════════════════════════════════════╗
  🐉 ║      龍魂 Notion 双向同步守护 v{脚本版本}             ║
  🐉 ║  五层目录 ↔ Notion五层数据库 实时守护            ║
  🐉 ╚══════════════════════════════════════════════════╝
{颜色码['重置']}
    {DNA签名}
    {确认码}
    {封印码}
    """)


def 检查环境():
    """检查运行环境是否满足要求"""
    通过 = True

    # 检查NOTION_TOKEN
    if not NOTION_TOKEN:
        日志('错误', '未找到NOTION_TOKEN环境变量！')
        日志('信息', f'请在 {secrets路径} 中设置:')
        日志('信息', '  NOTION_TOKEN=你的集成令牌')
        日志('信息', '  DB_LU=你的L0层数据库ID')
        日志('信息', '  DB_JQ=你的L1层数据库ID')
        日志('信息', '  DB_AL=你的L2层数据库ID')
        日志('信息', '  DB_PUB=你的L3层数据库ID')
        日志('信息', '  DB_CLOUD=你的L4层数据库ID')
        日志('信息', 'mkdir -p ~/.longhun && touch ~/.longhun/secrets.env')
        通过 = False
    else:
        日志('成功', f'NOTION_TOKEN 已配置 ({NOTION_TOKEN[:8]}...)')

    # 检查各层数据库配置
    for 层键, 层名 in 五层名称.items():
        数据库ID = 五层数据库.get(层键)
        if 数据库ID:
            日志('成功', f'[{层键}] {层名} → 数据库已配置 ({数据库ID[:8]}...)')
        else:
            日志('警告', f'[{层键}] {层名} → 数据库未配置')

    # 检查依赖
    try:
        import watchdog  # noqa: F811
        日志('成功', 'watchdog 已安装')
    except ImportError:
        日志('错误', 'watchdog 未安装，请运行: pip3 install watchdog')
        通过 = False

    try:
        import requests  # noqa: F811
        日志('成功', 'requests 已安装')
    except ImportError:
        日志('错误', 'requests 未安装，请运行: pip3 install requests')
        通过 = False

    try:
        import dotenv  # noqa: F811
        日志('成功', 'python-dotenv 已安装')
    except ImportError:
        日志('错误', 'python-dotenv 未安装，请运行: pip3 install python-dotenv')
        通过 = False

    return 通过


if __name__ == "__main__":  # ← 修复：原脚本缺失主入口
    打印启动画面()

    # 命令行参数解析
    参数解析器 = argparse.ArgumentParser(
        description='龍魂Notion双向同步守护 v4.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 longhun_sync.py                    # 启动全部监听
  python3 longhun_sync.py --layer L3         # 只监听公开层
  python3 longhun_sync.py --once             # 全量扫描一次后退出
  python3 longhun_sync.py --once --layer L0  # 只同步主权层一次
        """
    )
    参数解析器.add_argument(
        '--layer',
        choices=['L0', 'L1', 'L2', 'L3', 'L4'],
        help='只监听指定层 (L0=干·主权层, L1=离·继承层, L2=震·战友层, L3=巽·公开层, L4=坎·云端层)'
    )
    参数解析器.add_argument(
        '--once',
        action='store_true',
        help='全量扫描一次后退出（不启动持续监听）'
    )

    参数 = 参数解析器.parse_args()

    # 检查环境
    if not 检查环境():
        日志('错误', '环境检查未通过，请修复后重试')
        sys.exit(1)

    # --once 模式：全量扫描一次
    if 参数.once:
        if 参数.layer:
            全量扫描同步(参数.layer)
        else:
            for 层键 in ['L0', 'L1', 'L2', 'L3', 'L4']:
                全量扫描同步(层键)
        日志('强调', '全量扫描完成，退出')
        sys.exit(0)

    # 正常模式：启动监听
    观测器列表 = []
    if 参数.layer:
        # 只监听指定层
        观测器 = 启动层监听(参数.layer)
        if 观测器:
            观测器列表.append((参数.layer, 观测器))
    else:
        # 启动全部监听
        观测器列表 = 启动全部监听()

    if not 观测器列表:
        日志('错误', '没有成功启动任何监听，退出')
        sys.exit(1)

    日志('强调', '=== 龍魂同步守护运行中，按 Ctrl+C 停止 ===')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        日志('警告', '\n收到停止信号，正在关闭...')
        for 层键, 观测器 in 观测器列表:
            观测器.stop()
            日志('信息', f'已停止 [{层键}]')
        for 层键, 观测器 in 观测器列表:
            观测器.join()
        日志('成功', '龍魂同步守护已安全退出')
        sys.exit(0)
