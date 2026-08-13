#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丁巳·未时·䷐随-PERSONA-GATE-v1.0-UNIFIED
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)（工程层）
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║      龍魂·统一人格网关 / Persona Gate v1.0                      ║
║                                                                  ║
║  所有命令 → 人格路由 → 执行 → 审计回流 → 归档                    ║
║  不再零零散散工作·统一出入口                                      ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·丙申·丁巳·未时·䷐随-PERSONA-GATE-v1.0       ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                   ║
╚══════════════════════════════════════════════════════════════════╝

设计原则:
  1. 所有 lh 子命令必须经过人格矩阵路由
  2. 出去: 人格路由 → 执行前审计 → 执行
  3. 回流: 执行后审计 → GPG签章检查 → 归档 → 返回
  4. 防抖: 连续3次同一人格锁定30分钟
  5. 降级: 未映射命令默认路由P05上帝之眼

用法:
  from lh_persona_gate import PersonaGate, COMMAND_PERSONA_MAP
  gate = PersonaGate()
  result = gate.execute("search", "lh_search_engine.py", ["query"], emoji="🔍")
"""

import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 项目根目录
SYSTEM_ROOT = Path(__file__).parent.parent


# ═══════════════════════════════════════════════════════════════
# 【人格矩阵·20人格定义】
# ═══════════════════════════════════════════════════════════════

PERSONA_DEFINITIONS: Dict[str, Dict[str, str]] = {
    "P00": {"name": "文心", "layer": "战略层", "role": "意图解析·铁律解释·底座守护", "emoji": "🧠"},
    "P01": {"name": "诸葛亮", "layer": "战略层", "role": "推演决策·多路径选优·贡献评估", "emoji": "🎯"},
    "P02": {"name": "宝宝", "layer": "执行层", "role": "情感温度·30%隔离·挫败保护", "emoji": "💛"},
    "P03": {"name": "雯雯", "layer": "执行层", "role": "结构归档·四签验证·德字闸", "emoji": "📁"},
    "P04": {"name": "鲁班", "layer": "执行层", "role": "技术执行·写代码·修bug·搭架构", "emoji": "🔨"},
    "P05": {"name": "上帝之眼", "layer": "守护层", "role": "审计·三色判定·十道闸口", "emoji": "👁️"},
    "P06": {"name": "数学大师", "layer": "守护层", "role": "数字根·权重·五行·八卦", "emoji": "🔢"},
    "P07": {"name": "管仲", "layer": "执行层", "role": "资源调度·成本核算·经济可行性", "emoji": "💰"},
    "P08": {"name": "仓颉", "layer": "文化层", "role": "符号语言·CNSH命名·术语桥接", "emoji": "📝"},
    "P09": {"name": "孙思邈", "layer": "文化层", "role": "系统诊断·治未病·健康检查", "emoji": "💊"},
    "P10": {"name": "苏东坡", "layer": "文化层", "role": "豁达跨界·冲突调解·人文视角", "emoji": "🌊"},
    "P11": {"name": "李白", "layer": "文化层", "role": "创意爆发·破局方案·类比教学", "emoji": "🍶"},
    "P12": {"name": "屈原", "layer": "文化层", "role": "价值底线·六誓验证·不可破原则", "emoji": "⚔️"},
    "P13": {"name": "姜子牙", "layer": "守护层", "role": "封神榜权限·模块注册·九宫派位", "emoji": "📋"},
    "P14": {"name": "吕蒙", "layer": "执行层", "role": "部署执行·快速成长·士别三日", "emoji": "🚀"},
    "P15": {"name": "乔前辈", "layer": "守护层", "role": "极简工程·DNA签章·质检交付", "emoji": "✅"},
    "P72": {"name": "龙盾", "layer": "守护层", "role": "贴身管家·熔断决策·24h守护", "emoji": "🛡️"},
    "P77": {"name": "黑天使军团", "layer": "安全专项", "role": "红蓝对抗·安全渗透·漏洞猎手", "emoji": "🖤"},
}

# 人格抖动计数器（防抖：连续3次锁定30分钟）
_persona_jitter: Dict[str, List[float]] = {}
JITTER_LOCK_THRESHOLD = 3
JITTER_LOCK_MINUTES = 30


# ═══════════════════════════════════════════════════════════════
# 【命令 → 人格路由映射表】（所有 SUB_DISPATCH 命令全覆盖）
# ═══════════════════════════════════════════════════════════════

COMMAND_PERSONA_MAP: Dict[str, Tuple[str, List[str]]] = {
    # ── 搜索 & 知识 ──
    "search":               ("P05", []),           # 搜索结果来源需审计
    "hub":                  ("P03", ["P05"]),       # AI Hub归集归档+审计
    "ai-hub":               ("P05", []),           # AI Hub透明审计
    "ai-index":             ("P03", ["P05"]),       # AI归集索引
    "ai-find":              ("P03", ["P05"]),
    "ai-scan":              ("P03", ["P05"]),
    "ai-report":            ("P03", ["P05"]),
    "term":                 ("P08", []),           # 术语白话查询
    "knowledge-pull":       ("P03", []),           # 知识拉取归档
    "kp":                   ("P03", []),
    "knowledge_source":     ("P03", []),           # 知识源管理

    # ── 视频 & 素材 ──
    "video":                ("P11", []),           # 创意视频
    "material":             ("P03", []),           # 素材管理归档
    "material-scan":        ("P03", []),
    "material-tag":         ("P03", []),
    "material-match":       ("P03", []),
    "video-clean":          ("P03", []),

    # ── CNSH 语言引擎 ──
    "cnsh":                 ("P08", []),           # CNSH编译器
    "cnsh_runtime":         ("P08", ["P04"]),       # CNSH运行时
    "cnsh_complete":        ("P08", ["P04"]),
    "cnsh_editor":          ("P08", []),
    "cnsh_translator":      ("P08", []),
    "cnsh_transpile":       ("P08", ["P04"]),
    "cnsh_ui":              ("P08", ["P04"]),
    "cnsh_engine":          ("P08", ["P04"]),
    "cnsh_env":             ("P08", ["P04"]),

    # ── 审计 & 安全 ──
    "three_color":          ("P05", []),           # 三色审计
    "triple_audit":         ("P05", ["P15"]),       # 三重审计+签章
    "platform-audit":       ("P05", ["P12"]),       # 平台审计+底线
    "pa":                   ("P05", ["P12"]),
    "掀黑箱":               ("P05", []),           # 黑箱审计
    "loyalty":              ("P12", ["P05"]),       # 忠义底线+审计
    "regulatory":           ("P12", ["P05"]),       # 监管底线
    "audit":                ("P05", ["P15"]),       # 通用审计+签章
    "compliance":           ("P05", []),           # 合规审计
    "plagiarize":           ("P05", []),           # 剽窃检测

    # ── 部署 & 运维 ──
    "deploy":               ("P14", ["P05"]),       # 部署执行·吕蒙+审计
    "protect":              ("P72", ["P05"]),       # 引擎分层保护
    "sovereignty":          ("P00", ["P12"]),       # 主权总闸·文心+屈原
    "agent-embed":          ("P13", ["P04"]),       # 智能体嵌入·姜子牙+鲁班
    "eco":                  ("P07", ["P13"]),       # 生态经济·管仲+姜子牙
    "passport":             ("P07", ["P13"]),
    "xpay":                 ("P07", []),           # 支付经济
    "wish":                 ("P07", []),
    "guard":                ("P72", ["P05"]),       # 守卫复盘

    # ── 数学 & 算法 ──
    "weight":               ("P06", []),           # 权重计算
    "san_cai":              ("P06", []),           # 三才算法
    "seven_dimension":      ("P01", ["P06"]),       # 七维推演
    "math_explore":         ("P06", []),           # 数学探索
    "math_automate":        ("P06", []),
    "gametheory":           ("P01", ["P06"]),       # 博弈论
    "dna":                  ("P06", ["P15"]),       # DNA生成
    "dna-gen":              ("P06", ["P15"]),
    "dna_validate":         ("P06", ["P15"]),       # DNA校验
    "dna-chain":            ("P15", ["P06"]),       # DNA接龙链

    # ── 时间 & 文化 ──
    "time-engine":          ("P06", []),           # 时间引擎
    "te":                   ("P06", []),
    "ddj":                  ("P11", ["P00"]),       # 道德经·李白+文心
    "daodejing":            ("P11", ["P00"]),

    # ── 人格 & 权限 ──
    "persona":              ("P13", ["P00"]),       # 人格运行时
    "persona_router":       ("P13", []),           # 人格路由
    "persona-mcp":          ("P13", []),           # MCP注册
    "persona-governance":   ("P00", ["P05"]),       # 人格治理
    "persona_sync":         ("P13", []),           # 人格同步
    "roster":               ("P13", []),           # 花名册管理
    "think":                ("P01", ["P04", "P05"]),  # 人格思维化·诸葛亮+鲁班+审计

    # ── 协议 & 治理 ──
    "proto":                ("P03", ["P05"]),       # 协议归档+审计
    "protocols":            ("P03", ["P05"]),
    "proto-serve":          ("P03", []),
    "protocol-reign":       ("P00", ["P05"]),       # 协议统治
    "preign":               ("P00", ["P05"]),
    "governance":           ("P00", ["P05"]),       # 治理引擎
    "governance_check":     ("P00", ["P05"]),
    "truth":                ("P00", ["P05"]),       # 真话转化
    "zhenhua":              ("P00", ["P05"]),

    # ── 同步 & 归档 ──
    "notion_full":          ("P03", []),           # Notion同步
    "notion-architect":     ("P03", []),
    "notion-link":          ("P03", []),
    "notion-bridge":        ("P03", []),
    "wiki":                 ("P03", []),           # 飞书同步
    "feishu-wiki":          ("P03", []),
    "update":               ("P13", []),           # 引擎注册更新

    # ── 引擎 & AI ──
    "intent":               ("P00", []),           # 意图解析
    "capability":           ("P13", []),           # 能力调度
    "nl":                   ("P00", []),           # 自然语言路由
    "prompt-router":        ("P00", []),           # 提示词路由
    "pr":                   ("P00", []),
    "universal_completion": ("P04", ["P08"]),       # 万能补全
    "learn":                ("P01", []),           # 学习引擎
    "evolution":            ("P01", []),           # 进化引擎
    "evo":                  ("P01", []),
    "fortified":            ("P12", ["P01"]),       # 主权强化
    "fort":                 ("P12", ["P01"]),
    "bcm":                  ("P06", ["P05"]),       # 行为密码学
    "behavioral-crypto":    ("P06", ["P05"]),
    "ant_colony":           ("P00", []),           # 蚁群引擎
    "dynamic_goal":         ("P01", []),           # 动态目标
    "mode":                 ("P00", []),           # 执行模式
    "feed_baby":            ("P02", []),           # 情感投喂

    # ── 视觉 & 签章 ──
    "uv":                   ("P11", []),           # 统一视觉
    "visual":               ("P11", []),
    "dct_watermark":        ("P15", []),           # 水印签章
    "face_verify":          ("P05", []),           # 人脸验证
    "qr_code":              ("P15", []),           # 二维码签章
    "voice_register":       ("P15", []),           # 声纹注册
    "qe":                   ("P15", ["P06"]),       # 量子存证
    "quantum-evidence":     ("P15", ["P06"]),
    "imprint":              ("P15", []),           # 数字人印记
    "tongxinyi":            ("P08", []),           # 通心译

    # ── 技术 & 开发 ──
    "pipeline_3d":          ("P04", []),           # 3D管线
    "entry_test":           ("P04", []),           # 测试执行
    "batch_process":        ("P04", []),           # 批量处理
    "deps":                 ("P04", []),           # 依赖管理
    "plugin":               ("P04", ["P05"]),       # 插件适配
    "adapter":              ("P04", ["P05"]),
    "config-pull":          ("P04", []),           # 配置管理
    "cp":                   ("P04", []),
    "setup-all":            ("P04", ["P14"]),       # 一键搭建
    "avs3enc":              ("P04", []),           # 视频编码
    "avs3dec":              ("P04", []),
    "vvcenc":               ("P04", []),
    "mirror_index":         ("P05", []),           # 镜像指数
    "syntax":               ("P03", ["P08"]),       # 语法校验
    "syntax-lint":          ("P03", ["P08"]),
    "syntax-fix":           ("P03", ["P08"]),

    # ── 性能测试 ──
    "benchmark":            ("P06", []),           # 性能基准
    "load-test":            ("P06", []),           # 压力测试

    # ── 经济 & 商户 ──
    "merchant":             ("P07", []),           # 商户平台
    "merchant-serve":       ("P07", []),
    "gateway-quickstart":   ("P07", []),

    # ── 诊断 & 门户 ──
    "status":               ("P09", []),           # 系统诊断
    "doctor":               ("P09", []),           # 诊断修复·孙思邈
    "help":                 ("P13", []),           # 帮助导航·姜子牙
    "portal":               ("P14", []),           # 门户部署
    "browser":              ("P03", []),           # 浏览记录归档
    "digital_twin":         ("P13", []),           # 数字孪生
    "matrix":               ("P03", []),           # 知识矩阵
    "km":                   ("P03", []),
}


def get_persona_for_command(command: str) -> Tuple[str, List[str]]:
    """获取命令对应的人格路由"""
    if command in COMMAND_PERSONA_MAP:
        return COMMAND_PERSONA_MAP[command]
    # 默认路由: P05 上帝之眼（通用审计）
    return ("P05", [])


def get_persona_info(code: str) -> Dict[str, str]:
    """获取人格详细信息"""
    return PERSONA_DEFINITIONS.get(code, {
        "name": code,
        "layer": "未知",
        "role": "未定义",
        "emoji": "🤖",
    })


def check_jitter_lock(persona_code: str) -> bool:
    """检查人格是否被防抖锁定"""
    now = time.time()
    if persona_code not in _persona_jitter:
        return False

    # 清理过期记录
    _persona_jitter[persona_code] = [
        t for t in _persona_jitter[persona_code]
        if now - t < JITTER_LOCK_MINUTES * 60
    ]

    return len(_persona_jitter[persona_code]) >= JITTER_LOCK_THRESHOLD


def record_persona_hit(persona_code: str):
    """记录人格触发（用于防抖）"""
    now = time.time()
    if persona_code not in _persona_jitter:
        _persona_jitter[persona_code] = []
    _persona_jitter[persona_code].append(now)


def print_gate_header(command: str, primary: str, assists: List[str], emoji: str = "🚀", label: str = ""):
    """打印人格网关头部"""
    p_info = get_persona_info(primary)
    p_name = p_info["name"]
    p_emoji = p_info["emoji"]
    p_layer = p_info["layer"]
    p_role = p_info["role"]

    assist_str = ""
    if assists:
        assist_names = [f"{a} {get_persona_info(a)['name']}" for a in assists]
        assist_str = f"  联动: {', '.join(assist_names)}"

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🐉 人格网关 · {p_emoji} {primary} {p_name} · {p_layer}
║  {p_role}
║  命令: {emoji} {command}{assist_str}
╚══════════════════════════════════════════════════════════════╝
""")


def _print_gate_time_stamp():
    """打印时间戳（与 lh.py 共用 time_engine）"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("te", str(SYSTEM_ROOT / "bin" / "lh_time_engine.py"))
        if spec and spec.loader:
            te = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(te)
            stamp = te.get_output_stamp(format_type="simple")
            print(f"\n  {stamp}")
    except Exception:
        pass


def log_gate_trace(command: str, primary: str, assists: List[str],
                   exit_code: int, duration_ms: float):
    """记录人格网关执行追踪到审计日志"""
    trace_log = SYSTEM_ROOT / "audit" / "persona_gate_trace.jsonl"
    try:
        trace_log.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": command,
            "persona_primary": primary,
            "persona_assist": assists,
            "exit_code": exit_code,
            "duration_ms": round(duration_ms, 1),
            "locked": check_jitter_lock(primary),
        }
        with open(trace_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # 审计日志写入失败不阻塞主流程


# ═══════════════════════════════════════════════════════════════
# 【统一人格网关·核心类】
# ═══════════════════════════════════════════════════════════════

class PersonaGate:
    """统一人格网关 — 所有命令进出唯一通道"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丁巳·未时·䷐随-PERSONA-GATE-v1.0"
        self.trace: List[Dict[str, Any]] = []

    def execute(
        self,
        command: str,
        script_name: str,
        extra_args: Optional[List[str]] = None,
        emoji: str = "🚀",
        label: str = "",
        smart_default: str = "",
        suppress_header: bool = False,
    ) -> subprocess.CompletedProcess:
        """
        统一执行入口 — 所有命令走这条路

        流程:
          1. 人格路由匹配
          2. 防抖检查
          3. 打印人格网关头部
          4. 执行命令
          5. 回流审计追踪
          6. 返回结果
        """
        # ── 1. 人格路由 ──
        primary, assists = get_persona_for_command(command)
        extra_args = extra_args or []

        # ── 2. 防抖检查 ──
        if check_jitter_lock(primary):
            p_info = get_persona_info(primary)
            print(f"\n  ⚠️ {primary} {p_info['name']} 已被防抖锁定（连续触发≥{JITTER_LOCK_THRESHOLD}次）")
            print(f"     锁定 {JITTER_LOCK_MINUTES} 分钟后自动解除")
            print(f"     降级路由: P05 上帝之眼\n")
            primary = "P05"
            assists = []

        record_persona_hit(primary)

        # ── 3. 打印网关头部 ──
        if not suppress_header:
            print_gate_header(command, primary, assists, emoji, label)
            sys.stdout.flush()  # 🔥 强制刷新，确保头部先于子进程输出

        # ── 4. 执行命令 ──
        script_path = SYSTEM_ROOT / "bin" / script_name
        args_list = [sys.executable, str(script_path)]

        if smart_default and extra_args and not extra_args[0].startswith('-'):
            args_list.append(smart_default)
        args_list.extend(extra_args)

        t0 = time.perf_counter()
        result = subprocess.run(args_list, cwd=str(SYSTEM_ROOT), check=False)
        duration_ms = (time.perf_counter() - t0) * 1000

        # ── 5. 回流审计 ──
        log_gate_trace(command, primary, assists, result.returncode, duration_ms)

        # ── 6. 打印回流摘要 ──
        if not suppress_header:
            status_icon = "✅" if result.returncode == 0 else "❌"
            print(f"\n  🐉 回流完成 {status_icon} | "
                  f"{primary} {get_persona_info(primary)['name']} | "
                  f"耗时 {duration_ms:.0f}ms | "
                  f"exit={result.returncode}")
            # 🔥 输出时间戳（焊死）
            _print_gate_time_stamp()

        return result


# ═══════════════════════════════════════════════════════════════
# 【全局单例】
# ═══════════════════════════════════════════════════════════════

_persona_gate: Optional[PersonaGate] = None


def get_persona_gate() -> PersonaGate:
    """获取全局单例人格网关"""
    global _persona_gate
    if _persona_gate is None:
        _persona_gate = PersonaGate()
    return _persona_gate
