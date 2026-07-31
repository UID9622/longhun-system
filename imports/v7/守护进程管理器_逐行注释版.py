# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【第1行】指定用python3解释器执行此脚本
# 【第2行】声明文件编码为UTF-8，支持中文

# 【第3-14行】模块文档字符串，说明本文件的功能和元信息
"""
================================================================================
【龍魂守护进程管理器】
================================================================================
· 功能：安装 / 启动 / 停止 / 重启龍魂系统守护进程
· 架构：systemd / launchd 双模式适配
· 规范：CNSH中文编程规范 v5.2
· 君子协议：未经授权不得修改核心进程参数
================================================================================
· DNA:#龍芯⚡️2026-06-19-LONGHUN-DAEMON-v5.2
================================================================================
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 第一区：DNA追溯与全域常数（全局配置，所有函数共享）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第16行】导入操作系统接口模块，用于进程管理、环境变量等
import os
# 【第17行】导入系统相关功能，如命令行参数、标准输入输出
import sys
# 【第18行】导入JSON处理模块，用于配置文件的读写
import json
# 【第19行】导入时间模块，用于延时、超时控制
import time
# 【第20行】导入文件操作工具，用于日志归档等
import shutil
# 【第21行】导入信号处理模块，用于优雅停止进程（SIGTERM等）
import signal
# 【第22行】导入网络套接字模块，用于检测端口占用
import socket
# 【第23行】导入哈希算法模块，用于生成审计日志的"龍印"指纹
import hashlib
# 【第24行】导入命令行参数解析模块，支持--start/--stop等命令
import argparse
# 【第25行】导入平台检测模块，自动判断Linux/macOS/Windows
import platform
# 【第26行】导入日期时间模块，用于日志时间戳和令牌倒计时
import datetime
# 【第27行】导入异常堆栈跟踪模块，出错时打印详细调用链
import traceback
# 【第28行】导入子进程管理模块，用于启动/停止其他服务进程
import subprocess
# 【第29行】导入面向对象的路径操作类，替代字符串拼接路径
from pathlib import Path
# 【第30行】从dataclasses导入装饰器和字段工具，用于定义进程状态数据结构
from dataclasses import dataclass, field
# 【第31行】从typing导入类型提示工具，增强代码可读性和IDE提示
from typing import Dict, List, Optional, Callable

# ═══════════════════════════════════════════════════════════════════════════════
# 第一区：DNA追溯与全域常数（续）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第36行】定义全局DNA追溯码字符串，标识此文件的版本和归属
龍魂DNA追溯码 = "#龍芯⚡️2026-06-19-LONGHUN-DAEMON-v5.2"
# 【第37行】定义版本号字符串，用于状态看板显示
龍魂版本号 = "v5.2.0"
# 【第38行】定义编译日期标记，用于追踪构建时间
龍魂编译标记 = "2026-06-19"

# ═══════════════════════════════════════════════════════════════════════════════
# 三色审计级别定义（龍魂体系核心：🟢绿/🟡黄/🔴红）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第41行】定义红色审计级别常量 = "红"，表示致命错误，需立即告警
审计级别_红 = "红"      # 致命错误 → 立即告警，服务必须停止
# 【第42行】定义黄色审计级别常量 = "黄"，表示警告异常，需记录追踪
审计级别_黄 = "黄"      # 警告异常 → 记录追踪，需人工复核
# 【第43行】定义绿色审计级别常量 = "绿"，表示正常运行，常规记录
审计级别_绿 = "绿"      # 正常运行 → 常规记录，通过检查

# ═══════════════════════════════════════════════════════════════════════════════
# 服务注册表（定义所有龍魂服务的配置参数）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第46行】定义全局字典：服务注册表，key是服务名，value是配置字典
服务注册表 = {
    # 【第47-56行】龍魂操作台：Web UI主界面，对外提供HTTP服务
    "龍魂操作台": {
        "端口": 8443,                              # HTTP服务监听端口
        "路径": "/",                               # URL根路径
        "进程标识": "longhun-console",             # 进程名称标识
        "启动指令": ["python3", "-m", "http.server", "8443"],  # 启动命令数组
        "健康检查路径": "/health",                  # HTTP健康检查端点
        "依赖服务": [],                            # 此服务无前置依赖
        "超时秒数": 30,                           # 启动最多等30秒
        "自动重启": True,                         # 崩溃后自动重启
        "最大重试次数": 5,                        # 最多重试5次
    },
    # 【第58-68行】MCP服务：Model Context Protocol协议服务
    "MCP服务": {
        "端口": 8443,                              # 复用操作台端口
        "路径": "/mcp",                            # MCP专用路径
        "进程标识": "longhun-mcp",                 # 进程标识
        "启动指令": ["python3", "-m", "mcp.server"],  # MCP启动命令
        "健康检查路径": "/mcp/health",              # 健康检查端点
        "依赖服务": ["龍魂操作台"],                 # 必须先启动操作台
        "超时秒数": 30,
        "自动重启": True,
        "最大重试次数": 3,
    },
    # 【第69-79行】Kimi集成：连接Kimi AI的桥接服务
    "Kimi集成": {
        "端口": 8443,
        "路径": "/kimi",
        "进程标识": "longhun-kimi",
        "启动指令": ["python3", "-m", "longhun.kimi_bridge"],
        "健康检查路径": "/kimi/health",
        "依赖服务": ["龍魂操作台", "MCP服务"],       # 依赖操作台和MCP
        "超时秒数": 30,
        "自动重启": True,
        "最大重试次数": 3,
    },
    # 【第80-91行】Notion同步：与Notion的双向数据同步服务
    "Notion同步": {
        "端口": 0,                                 # 0表示不监听端口（后台任务）
        "路径": "",
        "进程标识": "longhun-notion-sync",         # 进程标识
        "启动指令": ["python3", "-m", "longhun.notion_sync"],
        "健康检查路径": "",                       # 无HTTP健康检查
        "依赖服务": ["龍魂操作台"],
        "超时秒数": 60,                           # 同步可能需要较长时间
        "自动重启": False,                        # 定时任务不自动重启
        "最大重试次数": 2,
        "定时触发": "*/5 * * * *",                # Cron表达式：每5分钟触发
    },
    # 【第92-103行】自动化评估：6维度系统日评估
    "自动化评估": {
        "端口": 0,
        "路径": "",
        "进程标识": "longhun-auto-eval",
        "启动指令": ["python3", "-m", "longhun.auto_evaluation"],
        "健康检查路径": "",
        "依赖服务": ["龍魂操作台", "MCP服务"],
        "超时秒数": 120,                          # 评估可能需要2分钟
        "自动重启": False,
        "最大重试次数": 1,
        "定时触发": "30 22 * * *",                # 每天22:30触发
    },
    # 【第104-115行】复盘引擎：每日复盘报告生成
    "复盘引擎": {
        "端口": 0,
        "路径": "",
        "进程标识": "longhun-review-engine",
        "启动指令": ["python3", "-m", "longhun.review_engine"],
        "健康检查路径": "",
        "依赖服务": ["龍魂操作台", "自动化评估"],
        "超时秒数": 180,                          # 复盘可能需要3分钟
        "自动重启": False,
        "最大重试次数": 1,
        "定时触发": "0 23 * * *",                 # 每天23:00触发
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# 第二区：审计日志系统（所有操作留痕，三色审计可追溯）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第122行】定义审计日志器类，负责所有日志的写入和分级显示
class 审计日志器:
    # 【第123行】类文档字符串，说明此类的用途
    """三色审计日志系统 — 所有操作留痕可追溯"""

    # 【第125行】构造方法（初始化），接收日志目录路径参数
    def __init__(self, 日志目录: str = ""):
        # 【第126行】如果调用者没有指定日志目录
        if not 日志目录:
            # 【第127行】自动设置为脚本所在目录的上一层下的logs文件夹
            日志目录 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
        # 【第128行】将日志目录字符串转为Path对象，并解析为绝对路径
        self.日志目录 = Path(日志目录).resolve()
        # 【第129行】如果日志目录不存在，自动创建（包括父目录）
        self.日志目录.mkdir(parents=True, exist_ok=True)

        # 【第131行】构造今天的审计日志文件路径，格式：daemon_audit_2026-06-20.log
        self.日志文件路径 = self.日志目录 / f"daemon_audit_{datetime.date.today().isoformat()}.log"
        # 【第132行】标准输出日志路径（对应launchd的stdout）
        self.运行日志路径 = self.日志目录 / "launchd.out.log"
        # 【第133行】标准错误日志路径（对应launchd的stderr）
        self.错误日志路径 = self.日志目录 / "launchd.err.log"

    # 【第135行】核心方法：写入一条审计日志（私有方法，外部通过红/黄/绿调用）
    def 记录(self, 级别: str, 模块: str, 讯息: str, 元数据: dict = None):
        # 【第136行】方法文档字符串
        """写入审计日志"""
        # 【第137行】获取当前时间的ISO格式字符串作为时间戳
        时间戳 = datetime.datetime.now().isoformat()
        # 【第138行】计算"龍印"指纹：对时间戳+模块名+消息+DNA码做SHA256哈希，取前12位
        龍印 = hashlib.sha256(f"{时间戳}{模块}{讯息}{龍魂DNA追溯码}".encode()).hexdigest()[:12]
        # 【第139行】拼接日志行：时间戳 + 龍印 + 级别 + 模块 + 消息
        记录行 = f"[{时间戳}] [龍印:{龍印}] [{级别}] [{模块}] {讯息}"
        # 【第140行】如果调用者提供了额外元数据
        if 元数据:
            # 【第141行】将元数据转为JSON字符串，追加到日志行
            记录行 += f" | 元数据:{json.dumps(元数据, ensure_ascii=False)}"
        # 【第142行】在日志行末尾追加DNA追溯码，确保每条日志都可追溯
        记录行 += f" | DNA:{龍魂DNA追溯码}\n"

        # 【第144行】尝试将日志写入文件（try防止写文件异常导致程序崩溃）
        try:
            # 【第145行】以追加模式（"a"）打开日志文件，编码UTF-8
            with open(self.日志文件路径, "a", encoding="utf-8") as 档:
                # 【第146行】将拼接好的日志行写入文件
                档.write(记录行)
        # 【第147行】如果写文件出错（如磁盘满、权限不足）
        except Exception as 异常:
            # 【第148行】将错误信息输出到标准错误流（stderr），不中断程序
            print(f"[审计日志错误] {异常}", file=sys.stderr)

        # 【第150行】根据审计级别，在控制台输出带颜色的日志
        if 级别 == 审计级别_红:
            # 【第151行】红色ANSI转义码 \033[91m = 红色文字，\033[0m = 恢复默认
            print(f"\033[91m{记录行.strip()}\033[0m", file=sys.stderr)
        elif 级别 == 审计级别_黄:
            # 【第153行】黄色ANSI转义码 \033[93m = 黄色文字
            print(f"\033[93m{记录行.strip()}\033[0m")
        else:
            # 【第155行】绿色ANSI转义码 \033[92m = 绿色文字
            print(f"\033[92m{记录行.strip()}\033[0m")

    # 【第158行】便捷方法：记录红色（致命）级别日志
    def 红(self, 模块: str, 讯息: str, 元数据: dict = None):
        self.记录(审计级别_红, 模块, 讯息, 元数据)  # 委托给核心记录方法

    # 【第161行】便捷方法：记录黄色（警告）级别日志
    def 黄(self, 模块: str, 讯息: str, 元数据: dict = None):
        self.记录(审计级别_黄, 模块, 讯息, 元数据)

    # 【第164行】便捷方法：记录绿色（正常）级别日志
    def 绿(self, 模块: str, 讯息: str, 元数据: dict = None):
        self.记录(审计级别_绿, 模块, 讯息, 元数据)

    # 【第167行】方法：写入标准输出日志文件
    def 输出标准(self, 讯息: str):
        """写入stdout日志"""
        # 【第169行】以追加模式打开stdout日志文件
        with open(self.运行日志路径, "a", encoding="utf-8") as 档:
            # 【第170行】写入带时间戳的日志行
            档.write(f"[{datetime.datetime.now().isoformat()}] {讯息}\n")

    # 【第172行】方法：写入标准错误日志文件
    def 输出错误(self, 讯息: str):
        """写入stderr日志"""
        # 【第174行】以追加模式打开stderr日志文件
        with open(self.错误日志路径, "a", encoding="utf-8") as 档:
            档.write(f"[{datetime.datetime.now().isoformat()}] {讯息}\n")


# 【第178行】创建全局审计日志器实例（单例模式，整个模块共享）
日志 = 审计日志器()


# ═══════════════════════════════════════════════════════════════════════════════
# 第三区：进程状态数据结构（用dataclass定义，简洁高效）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第186行】@dataclass装饰器：自动生成__init__、__repr__等方法
@dataclass
class 进程状态:
    """进程状态数据结构 — 记录一个服务的运行状态"""
    # 【第189行】服务名称（如"龍魂操作台"）
    服务名称: str = ""
    # 【第190行】操作系统进程ID（PID），0表示未启动
    进程ID: int = 0
    # 【第191行】状态字符串：未启动/运行中/已停止/异常/重启中
    状态: str = "未启动"
    # 【第192行】ISO格式启动时间字符串
    启动时间: str = ""
    # 【第193行】ISO格式最后一次心跳检测时间
    最后心跳: str = ""
    # 【第194行】连续重试次数（用于自恢复限制）
    重试计数: int = 0
    # 【第195行】历史总重启次数（累计值）
    总重启次数: int = 0
    # 【第196行】占用的网络端口号（0表示不占用端口）
    端口占用: int = 0
    # 【第197行】内存使用量，单位MB
    内存使用MB: float = 0.0
    # 【第198行】CPU使用率百分比
    CPU使用率: float = 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# 第三区：守护进程管理器（核心类，管理所有服务的生命周期）
# ═══════════════════════════════════════════════════════════════════════════════

class 守护进程管理器:
    """
    龍魂守护进程管理器 — 核心类
    · 管理所有龍魂服务的生命周期（启动→运行→停止→重启）
    · 支持 systemd (Linux) 和 launchd (macOS) 双模式
    · 自恢复机制：服务崩溃后自动重启（最多重试N次）
    """

    def __init__(self):
        # 【第210行】检测当前操作系统类型：linux/darwin/windows
        self.系统类型 = platform.system().lower()
        # 【第211行】初始化进程表字典：key=服务名，value=进程状态对象
        self.进程表: Dict[str, 进程状态] = {}
        # 【第212行】运行标志位：True表示守护循环在运行
        self.运行中 = False
        # 【第213行】配置目录：脚本所在目录的上一层下的config文件夹
        self.配置目录 = Path(__file__).parent.parent / "config"
        # 【第214行】如果配置目录不存在则自动创建
        self.配置目录.mkdir(parents=True, exist_ok=True)
        # 【第215行】状态文件路径：用于进程崩溃后恢复状态
        self.状态文件 = self.配置目录 / "daemon_state.json"
        # 【第216行】从状态文件加载之前的进程状态（恢复机制）
        self._加载状态()
        # 【第217行】记录绿色日志：管理器初始化完成
        日志.绿("守护进程管理器", f"初始化完成 | 系统:{self.系统类型} | DNA:{龍魂DNA追溯码}")

    def _加载状态(self):
        """从持久化文件加载进程状态（崩溃恢复时调用）"""
        # 【第221行】如果之前保存的状态文件存在
        if self.状态文件.exists():
            try:
                # 【第223行】以只读模式打开状态文件
                with open(self.状态文件, "r", encoding="utf-8") as 档:
                    # 【第224行】将JSON内容解析为Python字典
                    数据 = json.load(档)
                # 【第225行】遍历状态数据，恢复每个服务的状态
                for 名称, 状态数据 in 数据.items():
                    # 【第226行】将字典数据解压为进程状态对象
                    self.进程表[名称] = 进程状态(**状态数据)
                # 【第227行】记录绿色日志：成功恢复N个服务状态
                日志.绿("状态加载", f"已恢复 {len(self.进程表)} 个服务状态")
            except Exception as 异常:
                # 【第229行】如果状态文件损坏，记录黄色警告，使用默认状态
                日志.黄("状态加载", f"加载失败，使用默认状态: {异常}")

    def _保存状态(self):
        """将当前进程状态持久化到文件（供崩溃后恢复使用）"""
        try:
            # 【第234行】创建空字典，准备序列化
            数据 = {}
            # 【第235行】遍历当前所有服务的进程状态
            for 名称, 状态 in self.进程表.items():
                # 【第236行】将进程状态对象转为普通字典（JSON可序列化）
                数据[名称] = {
                    "服务名称": 状态.服务名称,
                    "进程ID": 状态.进程ID,
                    "状态": 状态.状态,
                    "启动时间": 状态.启动时间,
                    "最后心跳": 状态.最后心跳,
                    "重试计数": 状态.重试计数,
                    "总重启次数": 状态.总重启次数,
                    "端口占用": 状态.端口占用,
                    "内存使用MB": 状态.内存使用MB,
                    "CPU使用率": 状态.CPU使用率,
                }
            # 【第248行】以写入模式（"w"）打开状态文件，覆盖旧内容
            with open(self.状态文件, "w", encoding="utf-8") as 档:
                # 【第249行】将字典序列化为JSON，缩进2空格，保留中文
                json.dump(数据, 档, ensure_ascii=False, indent=2)
        except Exception as 异常:
            # 【第251行】如果保存失败，记录红色错误日志
            日志.红("状态保存", f"持久化失败: {异常}")

    # ─────────────────────────────────────────
    # 端口检测工具方法
    # ─────────────────────────────────────────
    def 检测端口占用(self, 端口: int) -> bool:
        """检查指定TCP端口是否已被其他进程占用"""
        try:
            # 【第259行】创建一个IPv4 TCP套接字（AF_INET=IPv4，SOCK_STREAM=TCP）
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as 探测:
                # 【第260行】设置超时时间为1秒，防止阻塞
                探测.settimeout(1)
                # 【第261行】尝试连接本地指定端口，connect_ex返回0表示连接成功（端口被占用）
                结果 = 探测.connect_ex(("127.0.0.1", 端口))
                # 【第262行】返回True表示端口已被占用，False表示空闲
                return 结果 == 0
        except Exception:
            # 【第263行】如果检测出错（如权限不足），保守地返回False（认为端口空闲）
            return False

    def 查找进程占用端口(self, 端口: int) -> int:
        """查找占用指定端口的进程ID（PID）"""
        try:
            # 【第269行】判断当前系统类型是否为Linux
            if self.系统类型 == "linux":
                # 【第270行】执行lsof命令查找占用端口的进程
                结果 = subprocess.run(
                    ["lsof", "-ti", f":{端口}"],   # -t=只输出PID，-i=网络文件
                    capture_output=True,             # 捕获标准输出
                    text=True,                       # 以文本模式返回
                    timeout=5                        # 最多等5秒
                )
                # 【第274行】如果命令有输出（stdout非空），解析第一行得到PID
                if 结果.stdout.strip():
                    return int(结果.stdout.strip().split("\n")[0])
            # 【第276行】判断当前系统是否为macOS（darwin是macOS的内核名）
            elif self.系统类型 == "darwin":
                # 【第277行】macOS也使用lsof命令（同Linux）
                结果 = subprocess.run(
                    ["lsof", "-ti", f":{端口}"],
                    capture_output=True, text=True, timeout=5
                )
                if 结果.stdout.strip():
                    return int(结果.stdout.strip().split("\n")[0])
            # 【第283行】判断是否为Windows
            elif self.系统类型 == "windows":
                # 【第284行】Windows使用netstat命令查找端口占用
                结果 = subprocess.run(
                    ["netstat", "-ano", "|", "findstr", f":{端口}"],
                    capture_output=True, text=True, timeout=5, shell=True
                )
                # 【第288行】Windows的netstat输出解析较复杂，此处简化处理
        except Exception as 异常:
            # 【第290行】如果查找失败，记录黄色警告，返回0
            日志.黄("端口检测", f"查找进程失败: {异常}")
        # 【第291行】返回0表示未找到占用进程（或查找失败）
        return 0

    # ─────────────────────────────────────────
    # 进程操作核心方法（启动 / 停止 / 重启）
    # ─────────────────────────────────────────
    def 获取进程状态(self, 进程ID: int) -> str:
        """检查指定PID的进程是否仍然存活"""
        # 【第298行】如果PID小于等于0，说明进程未启动
        if 进程ID <= 0:
            return "未启动"
        try:
            # 【第301行】向进程发送信号0（空信号，不执行任何操作，仅检测进程是否存在）
            os.kill(进程ID, 0)
            # 【第302行】如果os.kill没有抛出异常，说明进程存在且存活
            return "运行中"
        except OSError:
            # 【第304行】如果抛出OSError，说明进程不存在或无权访问
            return "已停止"

    def 启动服务(self, 服务名称: str) -> bool:
        """启动指定名称的服务（包含依赖检查、端口冲突处理、进程启动）"""
        # 【第308行】检查要启动的服务是否在注册表中存在
        if 服务名称 not in 服务注册表:
            日志.红("启动服务", f"未知服务: {服务名称}")
            return False

        # 【第312行】从注册表中获取此服务的配置字典
        配置 = 服务注册表[服务名称]
        # 【第313行】记录绿色日志：开始启动服务
        日志.绿("启动服务", f"正在启动 [{服务名称}]...")

        # ── 第1步：检查依赖服务是否已运行 ──
        # 【第316行】遍历此服务依赖的所有前置服务
        for 依赖名称 in 配置.get("依赖服务", []):
            # 【第317行】检查依赖服务是否已在进程表中
            if 依赖名称 in self.进程表:
                # 【第318行】获取依赖服务的当前状态
                依赖状态 = self.进程表[依赖名称]
                # 【第319行】如果依赖服务未在运行中
                if 依赖状态.状态 != "运行中":
                    # 【第320行】记录黄色日志：依赖未就绪，需要先启动依赖
                    日志.黄("依赖检查", f"依赖服务 [{依赖名称}] 未运行，先启动依赖")
                    # 【第321行】递归调用自身，先启动依赖服务
                    if not self.启动服务(依赖名称):
                        # 【第322行】如果依赖启动失败，记录红色错误
                        日志.红("依赖失败", f"无法启动依赖 [{依赖名称}]")
                        return False

        # ── 第2步：检查端口是否被占用 ──
        # 【第326行】获取此服务配置的端口号（0表示不需要端口）
        端口 = 配置.get("端口", 0)
        # 【第327行】如果配置了端口且端口已被占用
        if 端口 > 0 and self.检测端口占用(端口):
            # 【第328行】查找占用此端口的进程PID
            占用进程 = self.查找进程占用端口(端口)
            # 【第329行】记录黄色警告：端口被占用
            日志.黄("端口检查", f"端口 {端口} 已被进程 {占用进程} 占用")
            # 【第330行】检查占用进程是否不是本服务的进程（确实是其他进程抢占了端口）
            if 配置.get("进程标识") not in str(占用进程):
                # 【第331行】尝试释放端口：向占用进程发送SIGTERM（优雅终止信号）
                try:
                    os.kill(占用进程, signal.SIGTERM)
                    time.sleep(1)  # 等待1秒让进程退出
                except Exception:
                    pass  # 如果终止失败，继续尝试启动

        # ── 第3步：启动进程 ──
        try:
            # 【第340行】复制当前环境变量，避免污染系统环境
            环境变量 = os.environ.copy()
            # 【第341行】设置龍魂守护进程标志，告知子进程它在守护环境下运行
            环境变量["LONGHUN_DAEMON"] = "1"
            # 【第342行】将DNA追溯码传入子进程环境，确保全链路可追溯
            环境变量["LONGHUN_DNA"] = 龍魂DNA追溯码
            # 【第343行】设置服务名称环境变量，子进程可识别自身身份
            环境变量["LONGHUN_SERVICE"] = 服务名称

            # 【第345行】使用subprocess.Popen启动子进程（非阻塞，立即返回）
            进程 = subprocess.Popen(
                配置["启动指令"],       # 启动命令数组（如["python3","-m","http.server","8443"]）
                stdout=subprocess.PIPE,  # 捕获标准输出
                stderr=subprocess.PIPE,  # 捕获标准错误
                env=环境变量,             # 传入自定义环境变量
                cwd=str(Path(__file__).parent.parent.parent),  # 设置工作目录为项目根
            )

            # ── 第4步：等待服务就绪（健康检查）──
            # 【第353行】初始化等待计时器
            等待时间 = 0
            # 【第354行】获取配置的超时时间（默认30秒）
            超时 = 配置.get("超时秒数", 30)
            # 【第355行】循环等待，直到服务就绪或超时
            while 等待时间 < 超时:
                # 【第356行】poll()检查子进程是否已退出（返回None表示仍在运行）
                返回码 = 进程.poll()
                # 【第357行】如果poll()返回非None，说明子进程过早退出（启动失败）
                if 返回码 is not None:
                    日志.红("启动失败", f"[{服务名称}] 进程过早退出，返回码: {返回码}")
                    return False
                # 【第360行】如果配置了端口且端口已被监听（服务已就绪）
                if 端口 > 0 and self.检测端口占用(端口):
                    break  # 服务已就绪，跳出等待循环
                # 【第362行】等待0.5秒后再次检查
                time.sleep(0.5)
                # 【第363行】累计等待时间
                等待时间 += 0.5

            # ── 第5步：记录进程状态 ──
            # 【第366行】创建进程状态对象，记录新启动服务的信息
            状态 = 进程状态(
                服务名称=服务名称,                          # 服务名称
                进程ID=进程.pid,                            # 操作系统分配的PID
                状态="运行中",                              # 状态设为运行中
                启动时间=datetime.datetime.now().isoformat(),  # 当前时间作为启动时间
                最后心跳=datetime.datetime.now().isoformat(),  # 当前时间作为心跳时间
                端口占用=端口,                             # 记录占用的端口号
                重试计数=0,                                # 重置重试计数
            )
            # 【第375行】将新状态存入进程表（key=服务名，value=状态对象）
            self.进程表[服务名称] = 状态
            # 【第376行】立即将状态持久化到文件（崩溃后可恢复）
            self._保存状态()

            # 【第378行】记录绿色日志：启动成功
            日志.绿("启动成功", f"[{服务名称}] PID={进程.pid} 端口={端口}")
            return True

        except Exception as 异常:
            # 【第381行】如果启动过程中发生任何异常，记录红色错误+完整堆栈
            日志.红("启动异常", f"[{服务名称}] {traceback.format_exc()}")
            return False

    def 停止服务(self, 服务名称: str, 强制: bool = False) -> bool:
        """停止指定服务（先SIGTERM优雅终止，超时后SIGKILL强制终止）"""
        # 【第387行】检查服务是否在进程表中
        if 服务名称 not in self.进程表:
            日志.黄("停止服务", f"[{服务名称}] 未在进程表中")
            return True

        # 【第391行】获取服务当前的状态对象
        状态 = self.进程表[服务名称]
        # 【第392行】获取进程的PID
        进程ID = 状态.进程ID

        # 【第394行】如果PID无效或进程已不在运行中
        if 进程ID <= 0 or self.获取进程状态(进程ID) != "运行中":
            状态.状态 = "已停止"   # 将状态标记为已停止
            状态.进程ID = 0       # 清空PID
            self._保存状态()      # 持久化新状态
            return True

        # 【第400行】记录绿色日志：开始停止服务
        日志.绿("停止服务", f"正在停止 [{服务名称}] PID={进程ID}")

        try:
            # 【第402行】如果调用者要求强制停止
            if 强制:
                # 【第403行】发送SIGKILL信号（强制终止，进程无法拦截）
                os.kill(进程ID, signal.SIGKILL)
            else:
                # 【第405行】发送SIGTERM信号（优雅终止，允许进程清理资源）
                os.kill(进程ID, signal.SIGTERM)
                # 【第407行】初始化等待计数器
                等待 = 0
                # 【第408行】最多等待5秒（10次×0.5秒）让进程优雅退出
                while 等待 < 10 and self.获取进程状态(进程ID) == "运行中":
                    time.sleep(0.5)   # 等0.5秒
                    等待 += 0.5       # 累计等待时间
                # 【第412行】如果5秒后进程还在运行，强制终止
                if self.获取进程状态(进程ID) == "运行中":
                    os.kill(进程ID, signal.SIGKILL)

            # 【第415行】更新状态为已停止
            状态.状态 = "已停止"
            状态.进程ID = 0
            self._保存状态()
            日志.绿("停止完成", f"[{服务名称}] 已停止")
            return True

        except ProcessLookupError:
            # 【第421行】如果进程已经不存在（其他原因退出了）
            状态.状态 = "已停止"
            状态.进程ID = 0
            self._保存状态()
            return True
        except Exception as 异常:
            # 【第426行】其他异常情况，记录红色错误
            日志.红("停止异常", f"[{服务名称}] {异常}")
            return False

    def 重启服务(self, 服务名称: str) -> bool:
        """重启指定服务（先停止，等1秒，再启动）"""
        日志.绿("重启服务", f"正在重启 [{服务名称}]...")
        self.停止服务(服务名称)   # 第1步：停止
        time.sleep(1)             # 第2步：等待1秒确保端口释放
        return self.启动服务(服务名称)  # 第3步：重新启动

    # ─────────────────────────────────────────
    # 批量操作方法（启动全部 / 停止全部）
    # ─────────────────────────────────────────
    def 启动全部服务(self) -> Dict[str, bool]:
        """按拓扑排序顺序启动所有服务（确保依赖先启动）"""
        日志.绿("批量启动", "开始启动全部龍魂服务...")
        结果 = {}  # 记录每个服务的启动结果

        # 【第446行】调用拓扑排序，确保依赖服务先启动
        已排序 = self._拓扑排序服务()

        # 【第448行】按排序后的顺序逐个启动服务
        for 服务名称 in 已排序:
            成功 = self.启动服务(服务名称)
            结果[服务名称] = 成功
            if not 成功:
                日志.红("批量启动", f"[{服务名称}] 启动失败，后续依赖服务可能受影响")

        # 【第454行】统计成功数量
        成功数 = sum(1 for v in 结果.values() if v)
        日志.绿("批量启动", f"完成: {成功数}/{len(结果)} 个服务启动成功")
        return 结果

    def 停止全部服务(self) -> Dict[str, bool]:
        """反向停止所有服务（先停后置服务，再停依赖服务）"""
        日志.绿("批量停止", "正在停止全部服务...")
        结果 = {}

        # 【第464行】反向遍历进程表（先停止最后被依赖的服务）
        for 服务名称 in reversed(list(self.进程表.keys())):
            结果[服务名称] = self.停止服务(服务名称)

        日志.绿("批量停止", f"完成: {sum(1 for v in 结果.values() if v)}/{len(结果)} 个服务已停止")
        return 结果

    def _拓扑排序服务(self) -> List[str]:
        """拓扑排序：根据服务间的依赖关系计算启动顺序（Kahn算法）"""
        # 【第472行】初始化入度字典：每个服务的依赖数量（默认0）
        入度 = {名称: 0 for 名称 in 服务注册表}
        # 【第473行】初始化邻接表：每个服务被哪些服务依赖
        邻接表 = {名称: [] for 名称 in 服务注册表}

        # 【第475行】遍历服务注册表，构建依赖图
        for 名称, 配置 in 服务注册表.items():
            # 【第476行】获取此服务的依赖列表
            for 依赖 in 配置.get("依赖服务", []):
                # 【第477行】如果依赖也在注册表中（防止配置错误引用不存在的服务）
                if 依赖 in 服务注册表:
                    # 【第478行】邻接表：依赖 → 被依赖者（反向索引）
                    邻接表[依赖].append(名称)
                    # 【第479行】被依赖者的入度+1
                    入度[名称] += 1

        # 【第481行】将所有入度为0的服务加入队列（这些服务没有依赖，可以先启动）
        队列 = [名称 for 名称, 度 in 入度.items() if 度 == 0]
        结果 = []  # 存储排序后的结果

        # 【第484行】Kahn算法主循环
        while 队列:
            当前 = 队列.pop(0)    # 【第485行】从队头取出一个入度为0的服务
            结果.append(当前)     # 【第486行】将其加入结果列表
            # 【第487行】遍历所有依赖当前服务的邻居
            for 邻居 in 邻接表[当前]:
                入度[邻居] -= 1    # 【第488行】邻居的入度-1（因为一个依赖已解决）
                if 入度[邻居] == 0:  # 【第489行】如果邻居入度变为0
                    队列.append(邻居)  # 【第490行】将其加入队列，准备启动

        return 结果

    # ─────────────────────────────────────────
    # 系统服务安装（systemd for Linux / launchd for macOS）
    # ─────────────────────────────────────────
    def 安装系统服务(self) -> bool:
        """安装为系统服务（开机自启动）"""
        # 【第499行】根据操作系统类型选择安装方式
        if self.系统类型 == "linux":
            return self._安装_systemd()   # Linux用systemd
        elif self.系统类型 == "darwin":
            return self._安装_launchd()  # macOS用launchd
        else:
            日志.黄("系统服务", f"不支持的操作系统: {self.系统类型}")
            return False

    def _安装_systemd(self) -> bool:
        """安装 systemd 服务单元文件（Linux专用）"""
        # 【第509行】构造systemd服务单元文件的INI格式内容
        服务文件内容 = f"""[Unit]
Description=龍魂系统守护进程 v5.2
Documentation=https://longhun.dev/docs
After=network.target

[Service]
Type=simple
User={os.environ.get('USER', 'root')}
WorkingDirectory={Path(__file__).parent.parent}
ExecStart={sys.executable} {Path(__file__).parent}/一键启动器.py --daemon
ExecStop={sys.executable} {Path(__file__)}/守护进程管理器.py --stop-all
Restart=on-failure
RestartSec=5
StandardOutput=append:{日志.运行日志路径}
StandardError=append:{日志.错误日志路径}
Environment="LONGHUN_DAEMON=1"
Environment="LONGHUN_DNA={龍魂DNA追溯码}"

[Install]
WantedBy=multi-user.target
"""
        try:
            # 【第531行】systemd服务文件的标准路径
            服务路径 = Path("/etc/systemd/system/longhun-daemon.service")
            # 【第533行】先写入临时文件（避免直接写/etc需要权限的问题）
            临时文件 = Path("/tmp/longhun-daemon.service")
            with open(临时文件, "w", encoding="utf-8") as 档:
                档.write(服务文件内容)  # 【第535行】写入服务文件内容
            # 【第536行】用sudo复制到systemd目录
            subprocess.run(["sudo", "cp", str(临时文件), str(服务路径)], check=True)
            # 【第537行】重载systemd配置
            subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
            # 【第538行】设置为开机自启动
            subprocess.run(["sudo", "systemctl", "enable", "longhun-daemon"], check=True)
            日志.绿("systemd", "服务安装成功: longhun-daemon.service")
            return True
        except Exception as 异常:
            日志.红("systemd", f"安装失败: {异常}")
            return False

    def _安装_launchd(self) -> bool:
        """安装 launchd plist 文件（macOS专用）"""
        # 【第547行】构造macOS launchd的plist XML内容
        plist内容 = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>dev.longhun.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{Path(__file__).parent}/一键启动器.py</string>
        <string>--daemon</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{Path(__file__).parent.parent}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>LONGHUN_DAEMON</key>
        <string>1</string>
        <key>LONGHUN_DNA</key>
        <string>{龍魂DNA追溯码}</string>
    </dict>
    <key>StandardOutPath</key>
    <string>{日志.运行日志路径}</string>
    <key>StandardErrorPath</key>
    <string>{日志.错误日志路径}</string>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>ThrottleInterval</key>
    <integer>30</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
        try:
            # 【第585行】launchd用户级服务目录
            launchd目录 = Path.home() / "Library/LaunchAgents"
            launchd目录.mkdir(parents=True, exist_ok=True)
            # 【第587行】plist文件路径
            plist路径 = launchd目录 / "dev.longhun.daemon.plist"
            with open(plist路径, "w", encoding="utf-8") as 档:
                档.write(plist内容)
            # 【第590行】加载plist到launchd
            subprocess.run(["launchctl", "load", str(plist路径)], check=True)
            日志.绿("launchd", f"服务安装成功: {plist路径}")
            return True
        except Exception as 异常:
            日志.红("launchd", f"安装失败: {异常}")
            return False

    def 卸载系统服务(self) -> bool:
        """卸载系统服务（清理systemd或launchd配置）"""
        try:
            if self.系统类型 == "linux":
                # 【第601行】停止服务
                subprocess.run(["sudo", "systemctl", "stop", "longhun-daemon"], check=False)
                # 【第602行】禁用开机自启
                subprocess.run(["sudo", "systemctl", "disable", "longhun-daemon"], check=False)
                # 【第603行】删除服务文件
                subprocess.run(["sudo", "rm", "-f", "/etc/systemd/system/longhun-daemon.service"], check=False)
                # 【第604行】重载systemd
                subprocess.run(["sudo", "systemctl", "daemon-reload"], check=False)
            elif self.系统类型 == "darwin":
                # 【第606行】macOS：unload plist
                plist路径 = Path.home() / "Library/LaunchAgents/dev.longhun.daemon.plist"
                subprocess.run(["launchctl", "unload", str(plist路径)], check=False)
                # 【第608行】删除plist文件（missing_ok=True表示文件不存在不报错）
                plist路径.unlink(missing_ok=True)
            日志.绿("卸载服务", "系统服务已卸载")
            return True
        except Exception as 异常:
            日志.红("卸载服务", f"卸载失败: {异常}")
            return False

    # ─────────────────────────────────────────
    # 状态监控与看板
    # ─────────────────────────────────────────
    def 获取全部状态(self) -> Dict[str, dict]:
        """获取所有服务的当前状态（会刷新实际进程状态）"""
        结果 = {}
        # 【第621行】遍历注册表中所有服务
        for 服务名称 in 服务注册表:
            if 服务名称 in self.进程表:
                状态 = self.进程表[服务名称]
                # 【第625行】刷新实际进程状态（检测进程是否还活着）
                实际状态 = self.获取进程状态(状态.进程ID)
                # 【第626行】如果实际状态与记录不一致，更新记录
                if 状态.状态 != 实际状态:
                    状态.状态 = 实际状态
                # 【第628行】将状态对象转为字典，加入结果
                结果[服务名称] = {
                    "进程ID": 状态.进程ID,
                    "状态": 状态.状态,
                    "启动时间": 状态.启动时间,
                    "最后心跳": 状态.最后心跳,
                    "重试计数": 状态.重试计数,
                    "总重启次数": 状态.总重启次数,
                    "端口占用": 状态.端口占用,
                }
            else:
                # 【第638行】如果服务从未启动过
                结果[服务名称] = {"状态": "未注册"}
        return 结果

    def 打印状态看板(self):
        """在控制台打印ASCII格式的状态看板（类似top命令）"""
        print("\n" + "=" * 80)
        print(f"  🐉 龍魂守护进程状态看板  |  {龍魂版本号}  |  {datetime.datetime.now().isoformat()}")
        print("=" * 80)
        状态表 = self.获取全部状态()
        # 【第647行】遍历每个服务，打印状态行
        for 服务名称, 状态 in 状态表.items():
            # 【第648行】根据状态选择对应的emoji图标
            状态图标 = {
                "运行中": "🟢",
                "已停止": "🔴",
                "未启动": "⚪",
                "异常": "🟠",
                "重启中": "🟡",
                "未注册": "⚫",
            }.get(状态.get("状态", "未知"), "❓")
            # 【第656行】获取服务配置（用于显示端口信息）
            配置 = 服务注册表.get(服务名称, {})
            # 【第657行】构造端口显示字符串
            端口信息 = f":{状态.get('端口占用', 配置.get('端口', 0))}" if 配置.get("端口") else ""
            # 【第658行】打印格式化状态行
            print(f"  {状态图标} {服务名称:<12} {状态.get('状态', '未知'):<6} "
                  f"PID={状态.get('进程ID', 0):<8} {端口信息:<8} "
                  f"重启={状态.get('总重启次数', 0)}次")
        print("=" * 80 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# 第四区：命令行接口（CLI入口，支持各种命令参数）
# ═══════════════════════════════════════════════════════════════════════════════

def 主函数():
    """命令行入口函数 — 解析参数并执行对应操作"""
    # 【第670行】创建参数解析器
    解析器 = argparse.ArgumentParser(
        description="龍魂守护进程管理器",           # 程序描述
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 守护进程管理器.py --start-all          启动全部服务
  python3 守护进程管理器.py --stop 龍魂操作台    停止指定服务
  python3 守护进程管理器.py --restart MCP服务    重启指定服务
  python3 守护进程管理器.py --status             查看状态看板
  python3 守护进程管理器.py --install            安装系统服务
  python3 守护进程管理器.py --uninstall          卸载系统服务
        """  # 【第673-681行】使用示例
    )
    # 【第683行】定义--start参数：启动指定服务
    解析器.add_argument("--start", help="启动指定服务")
    # 【第684行】定义--stop参数：停止指定服务
    解析器.add_argument("--stop", help="停止指定服务")
    # 【第685行】定义--restart参数：重启指定服务
    解析器.add_argument("--restart", help="重启指定服务")
    # 【第686行】定义--start-all参数：启动所有服务（action=store_true表示不用传值）
    解析器.add_argument("--start-all", action="store_true", help="启动全部服务")
    # 【第687行】定义--stop-all参数：停止所有服务
    解析器.add_argument("--stop-all", action="store_true", help="停止全部服务")
    # 【第688行】定义--status参数：查看状态看板
    解析器.add_argument("--status", action="store_true", help="查看状态看板")
    # 【第689行】定义--install参数：安装为系统服务
    解析器.add_argument("--install", action="store_true", help="安装为系统服务")
    # 【第690行】定义--uninstall参数：卸载系统服务
    解析器.add_argument("--uninstall", action="store_true", help="卸载系统服务")
    # 【第691行】定义--daemon参数：守护进程模式（持续运行）
    解析器.add_argument("--daemon", action="store_true", help="守护进程模式")

    # 【第693行】解析命令行传入的参数
    参数 = 解析器.parse_args()
    # 【第694行】创建守护进程管理器实例（初始化）
    管理器 = 守护进程管理器()

    # 【第696行】根据解析到的参数执行对应操作
    if 参数.start:
        管理器.启动服务(参数.start)           # 【第697行】启动指定服务
    elif 参数.stop:
        管理器.停止服务(参数.stop)            # 【第699行】停止指定服务
    elif 参数.restart:
        管理器.重启服务(参数.restart)         # 【第701行】重启指定服务
    elif 参数.start_all:
        管理器.启动全部服务()                 # 【第703行】启动全部服务
    elif 参数.stop_all:
        管理器.停止全部服务()                 # 【第705行】停止全部服务
    elif 参数.status:
        管理器.打印状态看板()                 # 【第707行】打印状态看板
    elif 参数.install:
        管理器.安装系统服务()                 # 【第709行】安装为系统服务
    elif 参数.uninstall:
        管理器.卸载系统服务()                 # 【第711行】卸载系统服务
    elif 参数.daemon:
        # ── 守护进程模式（持续运行，自恢复循环）──
        日志.绿("守护模式", "进入守护进程循环...")
        管理器.运行中 = True
        # 【第715行】主循环：持续运行直到收到退出信号
        while 管理器.运行中:
            try:
                # 【第718行】遍历所有已注册的服务
                for 服务名称 in 服务注册表:
                    # 【第719行】如果服务不在进程表中，跳过
                    if 服务名称 not in 管理器.进程表:
                        continue
                    # 【第721行】获取服务的当前状态
                    状态 = 管理器.进程表[服务名称]
                    # 【第722行】获取服务的配置
                    配置 = 服务注册表[服务名称]
                    # 【第723行】如果配置了自动重启且服务不在运行中（崩溃了）
                    if 配置.get("自动重启") and 状态.状态 != "运行中":
                        # 【第724行】检查重试次数是否未超过上限
                        if 状态.重试计数 < 配置.get("最大重试次数", 3):
                            # 【第725行】记录黄色日志：检测到异常，正在自动重启
                            日志.黄("自恢复", f"[{服务名称}] 检测到异常，自动重启 (第{状态.重试计数 + 1}次)")
                            # 【第726行】执行重启
                            管理器.重启服务(服务名称)
                            # 【第727行】重试计数+1
                            管理器.进程表[服务名称].重试计数 += 1
                            # 【第728行】总重启次数+1（累计值）
                            管理器.进程表[服务名称].总重启次数 += 1
                        else:
                            # 【第730行】如果超过最大重试次数，停止自动恢复
                            日志.红("自恢复", f"[{服务名称}] 重试次数超限，停止自动恢复")
                # 【第731行】每次循环结束后休眠10秒（避免CPU空转）
                time.sleep(10)
            except KeyboardInterrupt:
                # 【第733行】收到Ctrl+C信号，记录退出日志
                日志.绿("守护模式", "收到退出信号")
                管理器.运行中 = False
            except Exception as 异常:
                # 【第736行】其他异常（如磁盘满、权限变更），记录错误后继续运行
                日志.红("守护循环", f"异常: {异常}")
                time.sleep(30)  # 异常后等30秒再试
    else:
        # 【第739行】如果没有传任何参数，默认显示状态看板
        管理器.打印状态看板()


# ═══════════════════════════════════════════════════════════════════════════════
# 程序入口（Python惯用法：只有直接运行此文件时才执行主函数）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第742行】判断是否是直接运行此文件（而非作为模块被import）
if __name__ == "__main__":
    # 【第743行】调用主函数，开始执行
    主函数()
