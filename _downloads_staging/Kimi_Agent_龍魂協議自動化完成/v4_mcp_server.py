#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂MCP标准电话线 v4.0
让AI客户端接到本地工具/数据/模型

DNA: #龍芯⚡️2026-06-09-MCP-SERVER-v4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
"""

from mcp.server.fastmcp import FastMCP
import json
import os
import hashlib
import copy
from datetime import datetime
from typing import Optional, Dict, Any

# ═══════════════════════════════════════════
# 全局配置与常量
# ═══════════════════════════════════════════

VERSION = "4.0.0"
持久化目录 = os.path.expanduser("~/.longhun")
持久化文件 = os.path.join(持久化目录, "flow_field.json")
审计日志文件 = os.path.join(持久化目录, "audit_log.jsonl")


def 确保目录():
    """确保持久化目录存在"""
    if not os.path.exists(持久化目录):
        os.makedirs(持久化目录, mode=0o700, exist_ok=True)


def 生成dna时间戳() -> str:
    """生成龍魂DNA时间戳签名"""
    当前时间 = datetime.now()
    时间字符串 = 当前时间.strftime("%Y%m%d%H%M%S%f")
    哈希 = hashlib.sha256(f"龍魂{时间字符串}UID9622".encode()).hexdigest()[:8]
    return f"#{时间字符串}-{哈希}"


def 生成审计哈希(操作者: str, 字段路径: str, 旧值, 新值) -> str:
    """生成审计记录的唯一哈希"""
    内容 = f"{操作者}:{字段路径}:{旧值}:{新值}:{datetime.now().isoformat()}"
    return hashlib.sha256(内容.encode()).hexdigest()[:16]


# ═══════════════════════════════════════════
# 五大人格v4.0 定义
# ═══════════════════════════════════════════

五大人格 = {
    'wenwen': {
        '姓名': '雯雯P03·技术整理师',
        '职能': '归档·整理·索引',
        '状态': '待机',
        '激活条件': '收到整理/归档/索引请求时自动激活',
        '宫格': 3,
        '五行': '木'
    },
    'p72': {
        '姓名': '宝宝P72·龍盾',
        '职能': '熔断守门·宫格5不动点锚',
        '状态': '始终激活',
        '激活条件': '系统启动即激活，不可关闭',
        '宫格': 5,
        '五行': '土'
    },
    'scout': {
        '姓名': '侦察兵',
        '职能': '信息收集·外部感知',
        '状态': '待机',
        '激活条件': '需要外部信息/侦察任务时激活',
        '宫格': 1,
        '五行': '水'
    },
    'architect': {
        '姓名': '架构师',
        '职能': '系统设计·逻辑构建',
        '状态': '待机',
        '激活条件': '需要架构设计/系统规划时激活',
        '宫格': 9,
        '五行': '火'
    },
    'syncer': {
        '姓名': '同步官',
        '职能': '状态同步·一致性维护',
        '状态': '待机',
        '激活条件': '检测到状态不一致/需要同步时激活',
        '宫格': 7,
        '五行': '金'
    },
}

# ═══════════════════════════════════════════
# 五层设备语法 路由表
# ═══════════════════════════════════════════

五层路由 = {
    'L0': {
        '名': '干·主权层',
        '目录': '~/longhun-lu/',
        '数据库': 'DB_LU',
        '人格': 'wenwen',
        '权限': '完全控制',
        '加密': 'AES-256-GCM',
        '状态': '在线'
    },
    'L1': {
        '名': '离·继承层',
        '目录': '~/longhun-jq/',
        '数据库': 'DB_JQ',
        '人格': 'p72',
        '权限': '读取+熔断',
        '加密': 'AES-256-GCM',
        '状态': '在线'
    },
    'L2': {
        '名': '震·战友层',
        '目录': '~/longhun-al/',
        '数据库': 'DB_AL',
        '人格': 'syncer',
        '权限': '读写同步',
        '加密': 'AES-256-CBC',
        '状态': '在线'
    },
    'L3': {
        '名': '巽·公开层',
        '目录': '~/longhun-pub/',
        '数据库': 'DB_PUB',
        '人格': 'scout',
        '权限': '只读公开',
        '加密': '无',
        '状态': '在线'
    },
    'L4': {
        '名': '坎·云端层',
        '目录': '~/longhun-cloud/',
        '数据库': 'DB_CLOUD',
        '人格': 'architect',
        '权限': '云端同步',
        '加密': 'TLS-1.3',
        '状态': '在线'
    },
}

# ═══════════════════════════════════════════
# 流场状态初始化与持久化
# ═══════════════════════════════════════════

默认流场状态: Dict[str, Any] = {
    'merkleDensity': {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5, 5: 1.0, 6: 0.5, 7: 0.5, 8: 0.5, 9: 0.5},
    'auditField': {'平衡': '🟢', '相克': '🟢', '三才': '🟢', '置信': '🟢', '整体': '🟢'},
    'personas': 五大人格,
    'dragonPulse': {
        'heartbeat': datetime.now().isoformat(),
        'stability': 1.0,
        'lastCorrection': None,
        'anchor': 5,
        'pulseCount': 0,
        'version': VERSION,
    },
    'routingTable': 五层路由,
    'metadata': {
        'created': datetime.now().isoformat(),
        'owner': 'UID9622-龍芯北辰·诸葛鑫',
        'dna': '#龍芯⚡️2026-06-09-MCP-SERVER-v4.0',
        'confirm': '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅',
        'seal': '#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅',
    }
}

流场状态: Dict[str, Any] = {}


def 加载流场状态() -> Dict[str, Any]:
    """从持久化文件加载流场状态，不存在则初始化"""
    global 流场状态
    确保目录()
    try:
        if os.path.exists(持久化文件):
            with open(持久化文件, 'r', encoding='utf-8') as f:
                已保存 = json.load(f)
            # 合并已保存状态和默认值（防止新增字段缺失）
            流场状态 = copy.deepcopy(默认流场状态)
            深度合并(流场状态, 已保存)
            流场状态['dragonPulse']['heartbeat'] = datetime.now().isoformat()
            流场状态['dragonPulse']['pulseCount'] = (
                流场状态['dragonPulse'].get('pulseCount', 0) + 1
            )
            保存流场状态()
            return 流场状态
    except Exception as e:
        print(f"[警告] 加载流场状态失败，使用默认值: {e}")
    流场状态 = copy.deepcopy(默认流场状态)
    保存流场状态()
    return 流场状态


def 深度合并(基础: dict, 覆盖: dict):
    """递归合并两个字典"""
    for 键, 值 in 覆盖.items():
        if 键 in 基础 and isinstance(基础[键], dict) and isinstance(值, dict):
            深度合并(基础[键], 值)
        else:
            基础[键] = 值


def 保存流场状态():
    """将流场状态持久化到JSON文件"""
    确保目录()
    try:
        # 更新心跳
        if 'dragonPulse' in 流场状态:
            流场状态['dragonPulse']['heartbeat'] = datetime.now().isoformat()
        with open(持久化文件, 'w', encoding='utf-8') as f:
            json.dump(流场状态, f, ensure_ascii=False, indent=2, default=str)
    except Exception as e:
        print(f"[错误] 流场状态持久化失败: {e}")


def 记录审计日志(操作者: str, 操作类型: str, 字段路径: str, 旧值, 新值) -> str:
    """记录审计日志到JSONL文件，返回审计哈希"""
    确保目录()
    审计哈希 = 生成审计哈希(操作者, 字段路径, 旧值, 新值)
    审计记录 = {
        'timestamp': datetime.now().isoformat(),
        'dnaStamp': 生成dna时间戳(),
        'operator': 操作者,
        'action': 操作类型,
        'fieldPath': 字段路径,
        'oldValue': str(旧值) if 旧值 is not None else None,
        'newValue': str(新值) if 新值 is not None else None,
        'auditHash': 审计哈希,
        'version': VERSION,
    }
    try:
        with open(审计日志文件, 'a', encoding='utf-8') as f:
            f.write(json.dumps(审计记录, ensure_ascii=False, default=str) + '\n')
    except Exception as e:
        print(f"[错误] 审计日志写入失败: {e}")
    return 审计哈希


def 读取审计日志(最近条数: int = 50) -> list:
    """读取最近的审计日志条目"""
    日志 = []
    try:
        if os.path.exists(审计日志文件):
            with open(审计日志文件, 'r', encoding='utf-8') as f:
                for 行 in f:
                    行 = 行.strip()
                    if 行:
                        try:
                            日志.append(json.loads(行))
                        except json.JSONDecodeError:
                            continue
    except Exception:
        pass
    return 日志[-最近条数:] if 日志 else []


# ═══════════════════════════════════════════
# 字段路径解析器
# ═══════════════════════════════════════════

def 解析字段路径(路径: str, 数据: dict):
    """
    解析点号分隔的字段路径，返回 (父对象, 最终键, 当前值)
    例如: "merkleDensity.5" -> (merkleDensity字典, "5", 当前值)
    """
    部分们 = 路径.split('.')
    当前 = 数据
    for i, 部分 in enumerate(部分们[:-1]):
        # 尝试作为整数索引（用于宫格数字键）
        键 = int(部分) if 部分.isdigit() else 部分
        if isinstance(当前, dict) and 键 in 当前:
            当前 = 当前[键]
        elif isinstance(当前, dict) and str(键) in 当前:
            当前 = 当前[str(键)]
        else:
            raise KeyError(f"路径 '{路径}' 在第 '{部分}' 段不存在")
    最终键 = 部分们[-1]
    最终键 = int(最终键) if 最终键.isdigit() else 最终键
    if isinstance(当前, dict):
        查找键 = 最终键 if 最终键 in 当前 else str(最终键)
        当前值 = 当前.get(查找键)
        return 当前, 查找键, 当前值
    else:
        raise TypeError(f"路径 '{路径}' 的父级不是字典类型")


def 设置字段值(路径: str, 新值, 数据: dict):
    """设置指定路径的字段值"""
    父对象, 最终键, _ = 解析字段路径(路径, 数据)
    旧值 = 父对象.get(最终键)
    # 尝试类型转换
    if isinstance(旧值, (int, float)):
        try:
            if isinstance(旧值, int):
                新值 = int(新值)
            else:
                新值 = float(新值)
        except ValueError:
            pass  # 保持字符串
    elif isinstance(旧值, bool):
        新值 = str(新值).lower() in ('true', '1', 'yes', '是', 'on')
    父对象[最终键] = 新值
    return 旧值, 新值


# ═══════════════════════════════════════════
# MCP 服务器初始化
# ═══════════════════════════════════════════

mcp = FastMCP("龍魂三才流场")

# ═══════════════════════════════════════════
# 工具一: flow_query - 查询三才流场完整状态
# ═══════════════════════════════════════════

@mcp.tool()
def flow_query(查询类型: str = "完整") -> str:
    """查询三才流场完整状态

    参数:
        查询类型: "完整" | "天场" | "地场" | "人场" | "脉冲" | "路由" | "审计"

    返回:
        JSON格式的查询结果字符串
    """
    try:
        dna = 生成dna时间戳()
        状态 = 加载流场状态()

        if 查询类型 == "完整":
            结果 = {
                "查询类型": "完整流场状态",
                "DNA时间戳": dna,
                "merkleDensity": 状态.get("merkleDensity", {}),
                "auditField": 状态.get("auditField", {}),
                "dragonPulse": 状态.get("dragonPulse", {}),
                "personas": {
                    键: {"状态": 值.get("状态"), "职能": 值.get("职能")}
                    for 键, 值 in 状态.get("personas", {}).items()
                },
                "routingTable": {
                    键: {"名": 值.get("名"), "状态": 值.get("状态")}
                    for 键, 值 in 状态.get("routingTable", {}).items()
                },
                "metadata": 状态.get("metadata", {}),
            }

        elif 查询类型 == "天场":
            密度 = 状态.get("merkleDensity", {})
            审计 = 状态.get("auditField", {})
            结果 = {
                "查询类型": "天场·九宫密度与审计",
                "DNA时间戳": dna,
                "merkleDensity": 密度,
                "auditField": 审计,
                "天场解读": {
                    "中心锚定": "宫格5不动点密度=1.0（龍盾P72守护）",
                    "八宫环绕": "宫格1-4,6-9密度0.5（待激活）",
                    "审计状态": "五维绿灯全通" if all(v == '🟢' for v in 审计.values()) else "存在异常信号",
                }
            }

        elif 查询类型 == "地场":
            结果 = {
                "查询类型": "地场·五层设备路由",
                "DNA时间戳": dna,
                "routingTable": 状态.get("routingTable", {}),
                "地场解读": {
                    "L0干层": "主权核心·完全控制·雯雯管理",
                    "L1离层": "继承守护·熔断机制·龍盾P72",
                    "L2震层": "战友协同·状态同步·同步官",
                    "L3巽层": "公开透明·只读访问·侦察兵",
                    "L4坎层": "云端备份·TLS加密·架构师",
                }
            }

        elif 查询类型 == "人场":
            人格们 = 状态.get("personas", {})
            激活数 = sum(1 for p in 人格们.values() if p.get("状态") != "待机")
            结果 = {
                "查询类型": "人场·五大人格状态",
                "DNA时间戳": dna,
                "personas": 人格们,
                "人场统计": {
                    "总人数": len(人格们),
                    "激活数": 激活数,
                    "待机数": len(人格们) - 激活数,
                }
            }

        elif 查询类型 == "脉冲":
            脉冲 = 状态.get("dragonPulse", {})
            结果 = {
                "查询类型": "脉冲·龍魂心跳",
                "DNA时间戳": dna,
                "dragonPulse": 脉冲,
                "脉冲解读": {
                    "状态": "稳定" if 脉冲.get("stability", 0) >= 0.9 else "需校正",
                    "锚点": f"宫格{脉冲.get('anchor', 5)}（不动点）",
                    "心跳": 脉冲.get("heartbeat"),
                    "版本": 脉冲.get("version"),
                }
            }

        elif 查询类型 == "路由":
            路由 = 状态.get("routingTable", {})
            结果 = {
                "查询类型": "路由·五层详细信息",
                "DNA时间戳": dna,
                "layers": {
                    层键: {
                        "层级": 层键,
                        "名称": 层值.get("名"),
                        "目录": 层值.get("目录"),
                        "数据库": 层值.get("数据库"),
                        "负责人格": 层值.get("人格"),
                        "权限": 层值.get("权限"),
                        "加密": 层值.get("加密"),
                        "状态": 层值.get("状态"),
                    }
                    for 层键, 层值 in 路由.items()
                }
            }

        elif 查询类型 == "审计":
            日志 = 读取审计日志(100)
            结果 = {
                "查询类型": "审计日志",
                "DNA时间戳": dna,
                "总条目": len(日志),
                "recentLogs": 日志[-20:] if 日志 else [],
            }

        else:
            return json.dumps({
                "错误": f"未知查询类型 '{查询类型}'",
                "有效选项": ["完整", "天场", "地场", "人场", "脉冲", "路由", "审计"],
                "DNA时间戳": dna,
            }, ensure_ascii=False, indent=2)

        return json.dumps(结果, ensure_ascii=False, indent=2, default=str)

    except Exception as e:
        return json.dumps({
            "错误": f"查询执行失败: {str(e)}",
            "查询类型": 查询类型,
            "DNA时间戳": 生成dna时间戳(),
        }, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════
# 工具二: flow_mutate - 修改流场状态（需审计）
# ═══════════════════════════════════════════

@mcp.tool()
def flow_mutate(字段路径: str, 新值: str, 操作者: str) -> str:
    """修改流场状态（需审计日志）

    参数:
        字段路径: 如 "merkleDensity.5" 或 "auditField.整体" 或 "personas.wenwen.状态"
        新值: 新值（字符串形式，会自动转换类型）
        操作者: 操作者DNA签名

    返回:
        JSON格式的操作结果，包含审计哈希
    """
    try:
        dna = 生成dna时间戳()
        状态 = 加载流场状态()

        # 验证操作者签名
        if not 操作者 or len(操作者.strip()) < 4:
            return json.dumps({
                "错误": "操作者DNA签名无效（至少4个字符）",
                "DNA时间戳": dna,
            }, ensure_ascii=False, indent=2)

        # 验证字段路径安全性
        禁止路径 = ["metadata", "dragonPulse.version"]
        for 禁止 in 禁止路径:
            if 字段路径.startswith(禁止):
                return json.dumps({
                    "错误": f"字段路径 '{字段路径}' 为受保护区域，禁止修改",
                    "受保护路径": 禁止路径,
                    "DNA时间戳": dna,
                }, ensure_ascii=False, indent=2)

        # 获取旧值并设置新值
        try:
            旧值, 实际新值 = 设置字段值(字段路径, 新值, 状态)
        except (KeyError, TypeError) as e:
            return json.dumps({
                "错误": f"字段路径解析失败: {str(e)}",
                "字段路径": 字段路径,
                "DNA时间戳": dna,
            }, ensure_ascii=False, indent=2)

        # 记录审计日志
        审计哈希 = 记录审计日志(
            操作者=操作者,
            操作类型="mutate",
            字段路径=字段路径,
            旧值=旧值,
            新值=实际新值,
        )

        # 更新dragonPulse
        状态['dragonPulse']['lastCorrection'] = {
            'field': 字段路径,
            'old': str(旧值) if 旧值 is not None else None,
            'new': str(实际新值),
            'operator': 操作者[:20],  # 截断显示
            'timestamp': datetime.now().isoformat(),
        }
        状态['dragonPulse']['stability'] = min(
            1.0,
            状态['dragonPulse'].get('stability', 1.0) + 0.01
        )

        # 持久化
        保存流场状态()

        结果 = {
            "操作": "流场状态修改成功",
            "DNA时间戳": dna,
            "字段路径": 字段路径,
            "旧值": str(旧值) if 旧值 is not None else None,
            "新值": str(实际新值),
            "操作者": 操作者[:20],
            "审计哈希": 审计哈希,
            "稳定性": 状态['dragonPulse']['stability'],
        }
        return json.dumps(结果, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "错误": f"修改操作失败: {str(e)}",
            "字段路径": 字段路径,
            "DNA时间戳": 生成dna时间戳(),
        }, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════
# 工具三: persona_status - 查询五大人格当前状态
# ═══════════════════════════════════════════

@mcp.tool()
def persona_status(人格键: str = "全部") -> str:
    """查询五大人格当前状态

    参数:
        人格键: "全部" | "wenwen" | "p72" | "scout" | "architect" | "syncer"

    返回:
        JSON格式的人格状态
    """
    try:
        dna = 生成dna时间戳()
        状态 = 加载流场状态()
        人格们 = 状态.get("personas", {})

        有效键们 = list(五大人格.keys())

        if 人格键 == "全部":
            # 返回所有人格概览
            概览 = {}
            for 键, 信息 in 人格们.items():
                概览[键] = {
                    "姓名": 信息.get("姓名"),
                    "职能": 信息.get("职能"),
                    "状态": 信息.get("状态"),
                    "五行": 信息.get("五行"),
                    "宫格": 信息.get("宫格"),
                    "激活条件": 信息.get("激活条件"),
                }
            激活数 = sum(1 for p in 概览.values() if p["状态"] != "待机")
            结果 = {
                "查询类型": "五大人格全景",
                "DNA时间戳": dna,
                "人格列表": 概览,
                "系统状态": {
                    "总人数": len(概览),
                    "激活数": 激活数,
                    "待机数": len(概览) - 激活数,
                    "守护状态": "龍盾P72在线" if 概览.get("p72", {}).get("状态") == "始终激活" else "⚠️ 龍盾异常",
                }
            }

        elif 人格键 in 有效键们:
            信息 = 人格们.get(人格键, {})
            结果 = {
                "查询类型": f"单人格详情: {人格键}",
                "DNA时间戳": dna,
                "人格": {
                    "键名": 人格键,
                    "姓名": 信息.get("姓名"),
                    "职能": 信息.get("职能"),
                    "状态": 信息.get("状态"),
                    "五行": 信息.get("五行"),
                    "宫格": 信息.get("宫格"),
                    "激活条件": 信息.get("激活条件"),
                },
                "关联路由": 五层路由.get(f"L{list(五大人格.keys()).index(人格键)}", {}),
            }

        else:
            return json.dumps({
                "错误": f"未知人格键 '{人格键}'",
                "有效选项": ["全部"] + 有效键们,
                "DNA时间戳": dna,
            }, ensure_ascii=False, indent=2)

        return json.dumps(结果, ensure_ascii=False, indent=2, default=str)

    except Exception as e:
        return json.dumps({
            "错误": f"人格查询失败: {str(e)}",
            "人格键": 人格键,
            "DNA时间戳": 生成dna时间戳(),
        }, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("🐉 龍魂MCP标准电话线 v4.0")
    print("=" * 60)
    print(f"📡 服务器: 龍魂三才流场")
    print(f"🔧 版本: {VERSION}")
    print(f"👤 所有者: UID9622-龍芯北辰·诸葛鑫")
    print(f"🧬 DNA: #龍芯⚡️2026-06-09-MCP-SERVER-v4.0")
    print("-" * 60)
    print("🛠️ 三种工具:")
    print("   1️⃣ flow_query - 查询三才流场完整状态")
    print("      参数: 查询类型=[完整|天场|地场|人场|脉冲|路由|审计]")
    print("   2️⃣ flow_mutate - 修改流场状态（需审计）")
    print("      参数: 字段路径, 新值, 操作者")
    print("   3️⃣ persona_status - 查询五大人格当前状态")
    print("      参数: 人格键=[全部|wenwen|p72|scout|architect|syncer]")
    print("-" * 60)
    print(f"💾 持久化: {持久化文件}")
    print(f"📋 审计日志: {审计日志文件}")
    print("=" * 60)

    # 初始化流场状态
    加载流场状态()
    print("[✅] 流场状态已加载")
    print("[🚀] 启动MCP服务器传输层 (stdio)...")
    print()

    mcp.run(transport='stdio')
