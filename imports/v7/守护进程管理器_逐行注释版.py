#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【第1行】指定用python3解释器执行此脚本
# 【第2行】声明文件编码为UTF-8，支持中文

# 【第3-14行】模块文档字符串，说明本文件的功能和元信息
"""
================================================================================
【龍魂守護進程管理器】
================================================================================
· 功能：安裝 / 啟動 / 停止 / 重啟龍魂系統守護進程
· 架構：systemd / launchd 雙模式適配
· 規範：CNSH中文編程規範 v5.2
· 君子協議：未經授權不得修改核心進程參數
================================================================================
· DNA:#龍芯⚡️2026-06-19-LONGHUN-DAEMON-v5.2
================================================================================
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 第一區：DNA追溯與全域常數（全局配置，所有函数共享）
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
# 第一區：DNA追溯與全域常數（续）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第36行】定义全局DNA追溯码字符串，标识此文件的版本和归属
龍魂DNA追溯碼 = "#龍芯⚡️2026-06-19-LONGHUN-DAEMON-v5.2"
# 【第37行】定义版本号字符串，用于状态看板显示
龍魂版本號 = "v5.2.0"
# 【第38行】定义编译日期标记，用于追踪构建时间
龍魂編譯標記 = "2026-06-19"

# ═══════════════════════════════════════════════════════════════════════════════
# 三色審計級別定義（龍魂体系核心：🟢綠/🟡黃/🔴紅）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第41行】定义红色审计级别常量 = "紅"，表示致命错误，需立即告警
審計級別_紅 = "紅"      # 致命錯誤 → 立即告警，服务必须停止
# 【第42行】定义黄色审计级别常量 = "黃"，表示警告异常，需记录追踪
審計級別_黃 = "黃"      # 警告異常 → 記錄追蹤，需人工复核
# 【第43行】定义绿色审计级别常量 = "綠"，表示正常运行，常规记录
審計級別_綠 = "綠"      # 正常運行 → 常規記錄，通过检查

# ═══════════════════════════════════════════════════════════════════════════════
# 服務註冊表（定义所有龍魂服务的配置参数）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第46行】定义全局字典：服务注册表，key是服务名，value是配置字典
服務註冊表 = {
    # 【第47-56行】龍魂操作台：Web UI主界面，对外提供HTTP服务
    "龍魂操作台": {
        "端口": 8443,                              # HTTP服务监听端口
        "路徑": "/",                               # URL根路径
        "進程標識": "longhun-console",             # 进程名称标识
        "啟動指令": ["python3", "-m", "http.server", "8443"],  # 启动命令数组
        "健康檢查路徑": "/health",                  # HTTP健康检查端点
        "依賴服務": [],                            # 此服务无前置依赖
        "超時秒數": 30,                           # 启动最多等30秒
        "自動重啟": True,                         # 崩溃后自动重启
        "最大重試次數": 5,                        # 最多重试5次
    },
    # 【第58-68行】MCP服务：Model Context Protocol协议服务
    "MCP服務": {
        "端口": 8443,                              # 复用操作台端口
        "路徑": "/mcp",                            # MCP专用路径
        "進程標識": "longhun-mcp",                 # 进程标识
        "啟動指令": ["python3", "-m", "mcp.server"],  # MCP启动命令
        "健康檢查路徑": "/mcp/health",              # 健康检查端点
        "依賴服務": ["龍魂操作台"],                 # 必须先启动操作台
        "超時秒數": 30,
        "自動重啟": True,
        "最大重試次數": 3,
    },
    # 【第69-79行】Kimi集成：连接Kimi AI的桥接服务
    "Kimi集成": {
        "端口": 8443,
        "路徑": "/kimi",
        "進程標識": "longhun-kimi",
        "啟動指令": ["python3", "-m", "longhun.kimi_bridge"],
        "健康檢查路徑": "/kimi/health",
        "依賴服務": ["龍魂操作台", "MCP服務"],       # 依赖操作台和MCP
        "超時秒數": 30,
        "自動重啟": True,
        "最大重試次數": 3,
    },
    # 【第80-91行】Notion同步：与Notion的双向数据同步服务
    "Notion同步": {
        "端口": 0,                                 # 0表示不监听端口（后台任务）
        "路徑": "",
        "進程標識": "longhun-notion-sync",         # 进程标识
        "啟動指令": ["python3", "-m", "longhun.notion_sync"],
        "健康檢查路徑": "",                       # 无HTTP健康检查
        "依賴服務": ["龍魂操作台"],
        "超時秒數": 60,                           # 同步可能需要较长时间
        "自動重啟": False,                        # 定时任务不自动重启
        "最大重試次數": 2,
        "定時觸發": "*/5 * * * *",                # Cron表达式：每5分钟触发
    },
    # 【第92-103行】自动化评估：6维度系统日评估
    "自動化評估": {
        "端口": 0,
        "路徑": "",
        "進程標識": "longhun-auto-eval",
        "啟動指令": ["python3", "-m", "longhun.auto_evaluation"],
        "健康檢查路徑": "",
        "依賴服務": ["龍魂操作台", "MCP服務"],
        "超時秒數": 120,                          # 评估可能需要2分钟
        "自動重啟": False,
        "最大重試次數": 1,
        "定時觸發": "30 22 * * *",                # 每天22:30触发
    },
    # 【第104-115行】复盘引擎：每日复盘报告生成
    "復盤引擎": {
        "端口": 0,
        "路徑": "",
        "進程標識": "longhun-review-engine",
        "啟動指令": ["python3", "-m", "longhun.review_engine"],
        "健康檢查路徑": "",
        "依賴服務": ["龍魂操作台", "自動化評估"],
        "超時秒數": 180,                          # 复盘可能需要3分钟
        "自動重啟": False,
        "最大重試次數": 1,
        "定時觸發": "0 23 * * *",                 # 每天23:00触发
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# 第二區：審計日誌系統（所有操作留痕，三色审计可追溯）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第122行】定义审计日志器类，负责所有日志的写入和分级显示
class 審計日誌器:
    # 【第123行】类文档字符串，说明此类的用途
    """三色審計日誌系統 — 所有操作留痕可追溯"""

    # 【第125行】构造方法（初始化），接收日志目录路径参数
    def __init__(self, 日誌目錄: str = ""):
        # 【第126行】如果调用者没有指定日志目录
        if not 日誌目錄:
            # 【第127行】自动设置为脚本所在目录的上一层下的logs文件夹
            日誌目錄 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
        # 【第128行】将日志目录字符串转为Path对象，并解析为绝对路径
        self.日誌目錄 = Path(日誌目錄).resolve()
        # 【第129行】如果日志目录不存在，自动创建（包括父目录）
        self.日誌目錄.mkdir(parents=True, exist_ok=True)

        # 【第131行】构造今天的审计日志文件路径，格式：daemon_audit_2026-06-20.log
        self.日誌文件路徑 = self.日誌目錄 / f"daemon_audit_{datetime.date.today().isoformat()}.log"
        # 【第132行】标准输出日志路径（对应launchd的stdout）
        self.運行日誌路徑 = self.日誌目錄 / "launchd.out.log"
        # 【第133行】标准错误日志路径（对应launchd的stderr）
        self.錯誤日誌路徑 = self.日誌目錄 / "launchd.err.log"

    # 【第135行】核心方法：写入一条审计日志（私有方法，外部通过红/黄/绿调用）
    def 記錄(self, 級別: str, 模塊: str, 訊息: str, 元數據: dict = None):
        # 【第136行】方法文档字符串
        """寫入審計日誌"""
        # 【第137行】获取当前时间的ISO格式字符串作为时间戳
        時間戳 = datetime.datetime.now().isoformat()
        # 【第138行】计算"龍印"指纹：对时间戳+模块名+消息+DNA码做SHA256哈希，取前12位
        龍印 = hashlib.sha256(f"{時間戳}{模塊}{訊息}{龍魂DNA追溯碼}".encode()).hexdigest()[:12]
        # 【第139行】拼接日志行：时间戳 + 龍印 + 级别 + 模块 + 消息
        記錄行 = f"[{時間戳}] [龍印:{龍印}] [{級別}] [{模塊}] {訊息}"
        # 【第140行】如果调用者提供了额外元数据
        if 元數據:
            # 【第141行】将元数据转为JSON字符串，追加到日志行
            記錄行 += f" | 元數據:{json.dumps(元數據, ensure_ascii=False)}"
        # 【第142行】在日志行末尾追加DNA追溯码，确保每条日志都可追溯
        記錄行 += f" | DNA:{龍魂DNA追溯碼}\n"

        # 【第144行】尝试将日志写入文件（try防止写文件异常导致程序崩溃）
        try:
            # 【第145行】以追加模式（"a"）打开日志文件，编码UTF-8
            with open(self.日誌文件路徑, "a", encoding="utf-8") as 檔:
                # 【第146行】将拼接好的日志行写入文件
                檔.write(記錄行)
        # 【第147行】如果写文件出错（如磁盘满、权限不足）
        except Exception as 異常:
            # 【第148行】将错误信息输出到标准错误流（stderr），不中断程序
            print(f"[審計日誌錯誤] {異常}", file=sys.stderr)

        # 【第150行】根据审计级别，在控制台输出带颜色的日志
        if 級別 == 審計級別_紅:
            # 【第151行】红色ANSI转义码 \033[91m = 红色文字，\033[0m = 恢复默认
            print(f"\033[91m{記錄行.strip()}\033[0m", file=sys.stderr)
        elif 級別 == 審計級別_黃:
            # 【第153行】黄色ANSI转义码 \033[93m = 黄色文字
            print(f"\033[93m{記錄行.strip()}\033[0m")
        else:
            # 【第155行】绿色ANSI转义码 \033[92m = 绿色文字
            print(f"\033[92m{記錄行.strip()}\033[0m")

    # 【第158行】便捷方法：记录红色（致命）级别日志
    def 紅(self, 模塊: str, 訊息: str, 元數據: dict = None):
        self.記錄(審計級別_紅, 模塊, 訊息, 元數據)  # 委托给核心記錄方法

    # 【第161行】便捷方法：记录黄色（警告）级别日志
    def 黃(self, 模塊: str, 訊息: str, 元數據: dict = None):
        self.記錄(審計級別_黃, 模塊, 訊息, 元數據)

    # 【第164行】便捷方法：记录绿色（正常）级别日志
    def 綠(self, 模塊: str, 訊息: str, 元數據: dict = None):
        self.記錄(審計級別_綠, 模塊, 訊息, 元數據)

    # 【第167行】方法：写入标准输出日志文件
    def 輸出標準(self, 訊息: str):
        """寫入stdout日誌"""
        # 【第169行】以追加模式打开stdout日志文件
        with open(self.運行日誌路徑, "a", encoding="utf-8") as 檔:
            # 【第170行】写入带时间戳的日志行
            檔.write(f"[{datetime.datetime.now().isoformat()}] {訊息}\n")

    # 【第172行】方法：写入标准错误日志文件
    def 輸出錯誤(self, 訊息: str):
        """寫入stderr日誌"""
        # 【第174行】以追加模式打开stderr日志文件
        with open(self.錯誤日誌路徑, "a", encoding="utf-8") as 檔:
            檔.write(f"[{datetime.datetime.now().isoformat()}] {訊息}\n")


# 【第178行】创建全局审计日志器实例（单例模式，整个模块共享）
日誌 = 審計日誌器()


# ═══════════════════════════════════════════════════════════════════════════════
# 第三區：進程狀態數據結構（用dataclass定义，简洁高效）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第186行】@dataclass装饰器：自动生成__init__、__repr__等方法
@dataclass
class 進程狀態:
    """進程狀態數據結構 — 记录一个服务的运行状态"""
    # 【第189行】服务名称（如"龍魂操作台"）
    服務名稱: str = ""
    # 【第190行】操作系统进程ID（PID），0表示未启动
    進程ID: int = 0
    # 【第191行】状态字符串：未啟動/運行中/已停止/異常/重啟中
    狀態: str = "未啟動"
    # 【第192行】ISO格式启动时间字符串
    啟動時間: str = ""
    # 【第193行】ISO格式最后一次心跳检测时间
    最後心跳: str = ""
    # 【第194行】连续重试次数（用于自恢复限制）
    重試計數: int = 0
    # 【第195行】历史总重启次数（累计值）
    總重啟次數: int = 0
    # 【第196行】占用的网络端口号（0表示不占用端口）
    端口佔用: int = 0
    # 【第197行】内存使用量，单位MB
    內存使用MB: float = 0.0
    # 【第198行】CPU使用率百分比
    CPU使用率: float = 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# 第三區：守護進程管理器（核心类，管理所有服务的生命周期）
# ═══════════════════════════════════════════════════════════════════════════════

class 守護進程管理器:
    """
    龍魂守護進程管理器 — 核心类
    · 管理所有龍魂服務的生命週期（啟動→運行→停止→重啟）
    · 支持 systemd (Linux) 和 launchd (macOS) 双模式
    · 自恢復機制：服務崩潰後自動重啟（最多重試N次）
    """

    def __init__(self):
        # 【第210行】检测当前操作系统类型：linux/darwin/windows
        self.系統類型 = platform.system().lower()
        # 【第211行】初始化进程表字典：key=服务名，value=進程狀態对象
        self.進程表: Dict[str, 進程狀態] = {}
        # 【第212行】运行标志位：True表示守护循环在运行
        self.運行中 = False
        # 【第213行】配置目录：脚本所在目录的上一层下的config文件夹
        self.配置目錄 = Path(__file__).parent.parent / "config"
        # 【第214行】如果配置目录不存在则自动创建
        self.配置目錄.mkdir(parents=True, exist_ok=True)
        # 【第215行】状态文件路径：用于进程崩溃后恢复状态
        self.狀態文件 = self.配置目錄 / "daemon_state.json"
        # 【第216行】从状态文件加载之前的进程状态（恢复机制）
        self._加載狀態()
        # 【第217行】记录绿色日志：管理器初始化完成
        日誌.綠("守護進程管理器", f"初始化完成 | 系統:{self.系統類型} | DNA:{龍魂DNA追溯碼}")

    def _加載狀態(self):
        """從持久化文件加載進程狀態（崩溃恢复时调用）"""
        # 【第221行】如果之前保存的状态文件存在
        if self.狀態文件.exists():
            try:
                # 【第223行】以只读模式打开状态文件
                with open(self.狀態文件, "r", encoding="utf-8") as 檔:
                    # 【第224行】将JSON内容解析为Python字典
                    數據 = json.load(檔)
                # 【第225行】遍历状态数据，恢复每个服务的状态
                for 名稱, 狀態數據 in 數據.items():
                    # 【第226行】将字典数据解压为進程狀態对象
                    self.進程表[名稱] = 進程狀態(**狀態數據)
                # 【第227行】记录绿色日志：成功恢复N个服务状态
                日誌.綠("狀態加載", f"已恢復 {len(self.進程表)} 個服務狀態")
            except Exception as 異常:
                # 【第229行】如果状态文件损坏，记录黄色警告，使用默认状态
                日誌.黃("狀態加載", f"加載失敗，使用默認狀態: {異常}")

    def _保存狀態(self):
        """將當前進程狀態持久化到文件（供崩溃后恢复使用）"""
        try:
            # 【第234行】创建空字典，准备序列化
            數據 = {}
            # 【第235行】遍历当前所有服务的进程状态
            for 名稱, 狀態 in self.進程表.items():
                # 【第236行】将進程狀態对象转为普通字典（JSON可序列化）
                數據[名稱] = {
                    "服務名稱": 狀態.服務名稱,
                    "進程ID": 狀態.進程ID,
                    "狀態": 狀態.狀態,
                    "啟動時間": 狀態.啟動時間,
                    "最後心跳": 狀態.最後心跳,
                    "重試計數": 狀態.重試計數,
                    "總重啟次數": 狀態.總重啟次數,
                    "端口佔用": 狀態.端口佔用,
                    "內存使用MB": 狀態.內存使用MB,
                    "CPU使用率": 狀態.CPU使用率,
                }
            # 【第248行】以写入模式（"w"）打开状态文件，覆盖旧内容
            with open(self.狀態文件, "w", encoding="utf-8") as 檔:
                # 【第249行】将字典序列化为JSON，缩进2空格，保留中文
                json.dump(數據, 檔, ensure_ascii=False, indent=2)
        except Exception as 異常:
            # 【第251行】如果保存失败，记录红色错误日志
            日誌.紅("狀態保存", f"持久化失敗: {異常}")

    # ─────────────────────────────────────────
    # 端口檢測工具方法
    # ─────────────────────────────────────────
    def 檢測端口佔用(self, 端口: int) -> bool:
        """檢查指定TCP端口是否已被其他进程佔用"""
        try:
            # 【第259行】创建一个IPv4 TCP套接字（AF_INET=IPv4，SOCK_STREAM=TCP）
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as 探測:
                # 【第260行】设置超时时间为1秒，防止阻塞
                探測.settimeout(1)
                # 【第261行】尝试连接本地指定端口，connect_ex返回0表示连接成功（端口被占用）
                結果 = 探測.connect_ex(("127.0.0.1", 端口))
                # 【第262行】返回True表示端口已被占用，False表示空闲
                return 結果 == 0
        except Exception:
            # 【第263行】如果检测出错（如权限不足），保守地返回False（认为端口空闲）
            return False

    def 查找進程佔用端口(self, 端口: int) -> int:
        """查找佔用指定端口的进程ID（PID）"""
        try:
            # 【第269行】判断当前系统类型是否为Linux
            if self.系統類型 == "linux":
                # 【第270行】执行lsof命令查找占用端口的进程
                結果 = subprocess.run(
                    ["lsof", "-ti", f":{端口}"],   # -t=只输出PID，-i=网络文件
                    capture_output=True,             # 捕获标准输出
                    text=True,                       # 以文本模式返回
                    timeout=5                        # 最多等5秒
                )
                # 【第274行】如果命令有输出（stdout非空），解析第一行得到PID
                if 結果.stdout.strip():
                    return int(結果.stdout.strip().split("\n")[0])
            # 【第276行】判断当前系统是否为macOS（darwin是macOS的内核名）
            elif self.系統類型 == "darwin":
                # 【第277行】macOS也使用lsof命令（同Linux）
                結果 = subprocess.run(
                    ["lsof", "-ti", f":{端口}"],
                    capture_output=True, text=True, timeout=5
                )
                if 結果.stdout.strip():
                    return int(結果.stdout.strip().split("\n")[0])
            # 【第283行】判断是否为Windows
            elif self.系統類型 == "windows":
                # 【第284行】Windows使用netstat命令查找端口占用
                結果 = subprocess.run(
                    ["netstat", "-ano", "|", "findstr", f":{端口}"],
                    capture_output=True, text=True, timeout=5, shell=True
                )
                # 【第288行】Windows的netstat输出解析较复杂，此处简化处理
        except Exception as 異常:
            # 【第290行】如果查找失败，记录黄色警告，返回0
            日誌.黃("端口檢測", f"查找進程失敗: {異常}")
        # 【第291行】返回0表示未找到占用进程（或查找失败）
        return 0

    # ─────────────────────────────────────────
    # 進程操作核心方法（啟動 / 停止 / 重啟）
    # ─────────────────────────────────────────
    def 獲取進程狀態(self, 進程ID: int) -> str:
        """檢查指定PID的進程是否仍然存活"""
        # 【第298行】如果PID小于等于0，说明进程未启动
        if 進程ID <= 0:
            return "未啟動"
        try:
            # 【第301行】向进程发送信号0（空信号，不执行任何操作，仅检测进程是否存在）
            os.kill(進程ID, 0)
            # 【第302行】如果os.kill没有抛出异常，说明进程存在且存活
            return "運行中"
        except OSError:
            # 【第304行】如果抛出OSError，说明进程不存在或无权访问
            return "已停止"

    def 啟動服務(self, 服務名稱: str) -> bool:
        """啟動指定名稱的服務（包含依賴檢查、端口衝突處理、進程啟動）"""
        # 【第308行】检查要启动的服务是否在注册表中存在
        if 服務名稱 not in 服務註冊表:
            日誌.紅("啟動服務", f"未知服務: {服務名稱}")
            return False

        # 【第312行】从注册表中获取此服务的配置字典
        配置 = 服務註冊表[服務名稱]
        # 【第313行】记录绿色日志：开始启动服务
        日誌.綠("啟動服務", f"正在啟動 [{服務名稱}]...")

        # ── 第1步：檢查依賴服務是否已運行 ──
        # 【第316行】遍历此服务依赖的所有前置服务
        for 依賴名稱 in 配置.get("依賴服務", []):
            # 【第317行】检查依赖服务是否已在进程表中
            if 依賴名稱 in self.進程表:
                # 【第318行】获取依赖服务的当前状态
                依賴狀態 = self.進程表[依賴名稱]
                # 【第319行】如果依赖服务未在运行中
                if 依賴狀態.狀態 != "運行中":
                    # 【第320行】记录黄色日志：依赖未就绪，需要先启动依赖
                    日誌.黃("依賴檢查", f"依賴服務 [{依賴名稱}] 未運行，先啟動依賴")
                    # 【第321行】递归调用自身，先启动依赖服务
                    if not self.啟動服務(依賴名稱):
                        # 【第322行】如果依赖启动失败，记录红色错误
                        日誌.紅("依賴失敗", f"無法啟動依賴 [{依賴名稱}]")
                        return False

        # ── 第2步：檢查端口是否被佔用 ──
        # 【第326行】获取此服务配置的端口号（0表示不需要端口）
        端口 = 配置.get("端口", 0)
        # 【第327行】如果配置了端口且端口已被占用
        if 端口 > 0 and self.檢測端口佔用(端口):
            # 【第328行】查找占用此端口的进程PID
            佔用進程 = self.查找進程佔用端口(端口)
            # 【第329行】记录黄色警告：端口被占用
            日誌.黃("端口檢查", f"端口 {端口} 已被進程 {佔用進程} 佔用")
            # 【第330行】检查占用进程是否不是本服务的进程（确实是其他进程抢占了端口）
            if 配置.get("進程標識") not in str(佔用進程):
                # 【第331行】尝试释放端口：向占用进程发送SIGTERM（优雅终止信号）
                try:
                    os.kill(佔用進程, signal.SIGTERM)
                    time.sleep(1)  # 等待1秒让进程退出
                except Exception:
                    pass  # 如果终止失败，继续尝试启动

        # ── 第3步：啟動進程 ──
        try:
            # 【第340行】复制当前环境变量，避免污染系统环境
            環境變量 = os.environ.copy()
            # 【第341行】设置龍魂守护进程标志，告知子进程它在守护环境下运行
            環境變量["LONGHUN_DAEMON"] = "1"
            # 【第342行】将DNA追溯码传入子进程环境，确保全链路可追溯
            環境變量["LONGHUN_DNA"] = 龍魂DNA追溯碼
            # 【第343行】设置服务名称环境变量，子进程可识别自身身份
            環境變量["LONGHUN_SERVICE"] = 服務名稱

            # 【第345行】使用subprocess.Popen启动子进程（非阻塞，立即返回）
            進程 = subprocess.Popen(
                配置["啟動指令"],       # 启动命令数组（如["python3","-m","http.server","8443"]）
                stdout=subprocess.PIPE,  # 捕获标准输出
                stderr=subprocess.PIPE,  # 捕获标准错误
                env=環境變量,             # 传入自定义环境变量
                cwd=str(Path(__file__).parent.parent.parent),  # 设置工作目录为项目根
            )

            # ── 第4步：等待服務就緒（健康檢查）──
            # 【第353行】初始化等待计时器
            等待時間 = 0
            # 【第354行】获取配置的超时时间（默认30秒）
            超時 = 配置.get("超時秒數", 30)
            # 【第355行】循环等待，直到服务就绪或超时
            while 等待時間 < 超時:
                # 【第356行】poll()检查子进程是否已退出（返回None表示仍在运行）
                返回碼 = 進程.poll()
                # 【第357行】如果poll()返回非None，说明子进程过早退出（启动失败）
                if 返回碼 is not None:
                    日誌.紅("啟動失敗", f"[{服務名稱}] 進程過早退出，返回碼: {返回碼}")
                    return False
                # 【第360行】如果配置了端口且端口已被监听（服务已就绪）
                if 端口 > 0 and self.檢測端口佔用(端口):
                    break  # 服务已就绪，跳出等待循环
                # 【第362行】等待0.5秒后再次检查
                time.sleep(0.5)
                # 【第363行】累计等待时间
                等待時間 += 0.5

            # ── 第5步：記錄進程狀態 ──
            # 【第366行】创建進程狀態对象，记录新启动服务的信息
            狀態 = 進程狀態(
                服務名稱=服務名稱,                          # 服务名称
                進程ID=進程.pid,                            # 操作系统分配的PID
                狀態="運行中",                              # 状态设为运行中
                啟動時間=datetime.datetime.now().isoformat(),  # 当前时间作为启动时间
                最後心跳=datetime.datetime.now().isoformat(),  # 当前时间作为心跳时间
                端口佔用=端口,                             # 记录占用的端口号
                重試計數=0,                                # 重置重试计数
            )
            # 【第375行】将新状态存入进程表（key=服务名，value=状态对象）
            self.進程表[服務名稱] = 狀態
            # 【第376行】立即将状态持久化到文件（崩溃后可恢复）
            self._保存狀態()

            # 【第378行】记录绿色日志：启动成功
            日誌.綠("啟動成功", f"[{服務名稱}] PID={進程.pid} 端口={端口}")
            return True

        except Exception as 異常:
            # 【第381行】如果启动过程中发生任何异常，记录红色错误+完整堆栈
            日誌.紅("啟動異常", f"[{服務名稱}] {traceback.format_exc()}")
            return False

    def 停止服務(self, 服務名稱: str, 強制: bool = False) -> bool:
        """停止指定服務（先SIGTERM优雅终止，超时后SIGKILL强制终止）"""
        # 【第387行】检查服务是否在进程表中
        if 服務名稱 not in self.進程表:
            日誌.黃("停止服務", f"[{服務名稱}] 未在進程表中")
            return True

        # 【第391行】获取服务当前的状态对象
        狀態 = self.進程表[服務名稱]
        # 【第392行】获取进程的PID
        進程ID = 狀態.進程ID

        # 【第394行】如果PID无效或进程已不在运行中
        if 進程ID <= 0 or self.獲取進程狀態(進程ID) != "運行中":
            狀態.狀態 = "已停止"   # 将状态标记为已停止
            狀態.進程ID = 0       # 清空PID
            self._保存狀態()      # 持久化新状态
            return True

        # 【第400行】记录绿色日志：开始停止服务
        日誌.綠("停止服務", f"正在停止 [{服務名稱}] PID={進程ID}")

        try:
            # 【第402行】如果调用者要求强制停止
            if 強制:
                # 【第403行】发送SIGKILL信号（强制终止，进程无法拦截）
                os.kill(進程ID, signal.SIGKILL)
            else:
                # 【第405行】发送SIGTERM信号（优雅终止，允许进程清理资源）
                os.kill(進程ID, signal.SIGTERM)
                # 【第407行】初始化等待计数器
                等待 = 0
                # 【第408行】最多等待5秒（10次×0.5秒）让进程优雅退出
                while 等待 < 10 and self.獲取進程狀態(進程ID) == "運行中":
                    time.sleep(0.5)   # 等0.5秒
                    等待 += 0.5       # 累计等待时间
                # 【第412行】如果5秒后进程还在运行，强制终止
                if self.獲取進程狀態(進程ID) == "運行中":
                    os.kill(進程ID, signal.SIGKILL)

            # 【第415行】更新状态为已停止
            狀態.狀態 = "已停止"
            狀態.進程ID = 0
            self._保存狀態()
            日誌.綠("停止完成", f"[{服務名稱}] 已停止")
            return True

        except ProcessLookupError:
            # 【第421行】如果进程已经不存在（其他原因退出了）
            狀態.狀態 = "已停止"
            狀態.進程ID = 0
            self._保存狀態()
            return True
        except Exception as 異常:
            # 【第426行】其他异常情况，记录红色错误
            日誌.紅("停止異常", f"[{服務名稱}] {異常}")
            return False

    def 重啟服務(self, 服務名稱: str) -> bool:
        """重啟指定服務（先停止，等1秒，再啟動）"""
        日誌.綠("重啟服務", f"正在重啟 [{服務名稱}]...")
        self.停止服務(服務名稱)   # 第1步：停止
        time.sleep(1)             # 第2步：等待1秒确保端口释放
        return self.啟動服務(服務名稱)  # 第3步：重新啟動

    # ─────────────────────────────────────────
    # 批量操作方法（啟動全部 / 停止全部）
    # ─────────────────────────────────────────
    def 啟動全部服務(self) -> Dict[str, bool]:
        """按拓撲排序順序啟動所有服務（確保依賴先啟動）"""
        日誌.綠("批量啟動", "開始啟動全部龍魂服務...")
        結果 = {}  # 记录每个服务的启动结果

        # 【第446行】调用拓扑排序，确保依赖服务先启动
        已排序 = self._拓撲排序服務()

        # 【第448行】按排序后的顺序逐个启动服务
        for 服務名稱 in 已排序:
            成功 = self.啟動服務(服務名稱)
            結果[服務名稱] = 成功
            if not 成功:
                日誌.紅("批量啟動", f"[{服務名稱}] 啟動失敗，後續依賴服務可能受影響")

        # 【第454行】统计成功数量
        成功數 = sum(1 for v in 結果.values() if v)
        日誌.綠("批量啟動", f"完成: {成功數}/{len(結果)} 個服務啟動成功")
        return 結果

    def 停止全部服務(self) -> Dict[str, bool]:
        """反向停止所有服務（先停後置服務，再停依賴服務）"""
        日誌.綠("批量停止", "正在停止全部服務...")
        結果 = {}

        # 【第464行】反向遍历进程表（先停止最后被依赖的服务）
        for 服務名稱 in reversed(list(self.進程表.keys())):
            結果[服務名稱] = self.停止服務(服務名稱)

        日誌.綠("批量停止", f"完成: {sum(1 for v in 結果.values() if v)}/{len(結果)} 個服務已停止")
        return 結果

    def _拓撲排序服務(self) -> List[str]:
        """拓撲排序：根據服務間的依賴關係計算啟動順序（Kahn算法）"""
        # 【第472行】初始化入度字典：每个服务的依赖数量（默认0）
        入度 = {名稱: 0 for 名稱 in 服務註冊表}
        # 【第473行】初始化鄰接表：每个服务被哪些服务依赖
        鄰接表 = {名稱: [] for 名稱 in 服務註冊表}

        # 【第475行】遍历服务注册表，构建依赖图
        for 名稱, 配置 in 服務註冊表.items():
            # 【第476行】获取此服务的依赖列表
            for 依賴 in 配置.get("依賴服務", []):
                # 【第477行】如果依赖也在注册表中（防止配置错误引用不存在的服务）
                if 依賴 in 服務註冊表:
                    # 【第478行】鄰接表：依赖 → 被依赖者（反向索引）
                    鄰接表[依賴].append(名稱)
                    # 【第479行】被依赖者的入度+1
                    入度[名稱] += 1

        # 【第481行】将所有入度为0的服务加入队列（这些服务没有依赖，可以先启动）
        隊列 = [名稱 for 名稱, 度 in 入度.items() if 度 == 0]
        結果 = []  # 存储排序后的结果

        # 【第484行】Kahn算法主循环
        while 隊列:
            當前 = 隊列.pop(0)    # 【第485行】从队头取出一个入度为0的服务
            結果.append(當前)     # 【第486行】将其加入结果列表
            # 【第487行】遍历所有依赖当前服务的邻居
            for 鄰居 in 鄰接表[當前]:
                入度[鄰居] -= 1    # 【第488行】邻居的入度-1（因为一个依赖已解决）
                if 入度[鄰居] == 0:  # 【第489行】如果邻居入度变为0
                    隊列.append(鄰居)  # 【第490行】将其加入队列，准备启动

        return 結果

    # ─────────────────────────────────────────
    # 系統服務安裝（systemd for Linux / launchd for macOS）
    # ─────────────────────────────────────────
    def 安裝系統服務(self) -> bool:
        """安裝為系統服務（開機自啟動）"""
        # 【第499行】根据操作系统类型选择安装方式
        if self.系統類型 == "linux":
            return self._安裝_systemd()   # Linux用systemd
        elif self.系統類型 == "darwin":
            return self._安裝_launchd()  # macOS用launchd
        else:
            日誌.黃("系統服務", f"不支持的操作系統: {self.系統類型}")
            return False

    def _安裝_systemd(self) -> bool:
        """安裝 systemd 服務單元文件（Linux專用）"""
        # 【第509行】构造systemd服务单元文件的INI格式内容
        服務文件內容 = f"""[Unit]
Description=龍魂系統守護進程 v5.2
Documentation=https://longhun.dev/docs
After=network.target

[Service]
Type=simple
User={os.environ.get('USER', 'root')}
WorkingDirectory={Path(__file__).parent.parent}
ExecStart={sys.executable} {Path(__file__).parent}/一鍵啟動器.py --daemon
ExecStop={sys.executable} {Path(__file__)}/守護進程管理器.py --stop-all
Restart=on-failure
RestartSec=5
StandardOutput=append:{日誌.運行日誌路徑}
StandardError=append:{日誌.錯誤日誌路徑}
Environment="LONGHUN_DAEMON=1"
Environment="LONGHUN_DNA={龍魂DNA追溯碼}"

[Install]
WantedBy=multi-user.target
"""
        try:
            # 【第531行】systemd服务文件的标准路径
            服務路徑 = Path("/etc/systemd/system/longhun-daemon.service")
            # 【第533行】先写入临时文件（避免直接写/etc需要权限的问题）
            臨時文件 = Path("/tmp/longhun-daemon.service")
            with open(臨時文件, "w", encoding="utf-8") as 檔:
                檔.write(服務文件內容)  # 【第535行】写入服务文件内容
            # 【第536行】用sudo复制到systemd目录
            subprocess.run(["sudo", "cp", str(臨時文件), str(服務路徑)], check=True)
            # 【第537行】重载systemd配置
            subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
            # 【第538行】设置为开机自启动
            subprocess.run(["sudo", "systemctl", "enable", "longhun-daemon"], check=True)
            日誌.綠("systemd", "服務安裝成功: longhun-daemon.service")
            return True
        except Exception as 異常:
            日誌.紅("systemd", f"安裝失敗: {異常}")
            return False

    def _安裝_launchd(self) -> bool:
        """安裝 launchd plist 文件（macOS專用）"""
        # 【第547行】构造macOS launchd的plist XML内容
        plist內容 = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>dev.longhun.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{Path(__file__).parent}/一鍵啟動器.py</string>
        <string>--daemon</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{Path(__file__).parent.parent}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>LONGHUN_DAEMON</key>
        <string>1</string>
        <key>LONGHUN_DNA</key>
        <string>{龍魂DNA追溯碼}</string>
    </dict>
    <key>StandardOutPath</key>
    <string>{日誌.運行日誌路徑}</string>
    <key>StandardErrorPath</key>
    <string>{日誌.錯誤日誌路徑}</string>
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
            launchd目錄 = Path.home() / "Library/LaunchAgents"
            launchd目錄.mkdir(parents=True, exist_ok=True)
            # 【第587行】plist文件路径
            plist路徑 = launchd目錄 / "dev.longhun.daemon.plist"
            with open(plist路徑, "w", encoding="utf-8") as 檔:
                檔.write(plist內容)
            # 【第590行】加载plist到launchd
            subprocess.run(["launchctl", "load", str(plist路徑)], check=True)
            日誌.綠("launchd", f"服務安裝成功: {plist路徑}")
            return True
        except Exception as 異常:
            日誌.紅("launchd", f"安裝失敗: {異常}")
            return False

    def 卸載系統服務(self) -> bool:
        """卸載系統服務（清理systemd或launchd配置）"""
        try:
            if self.系統類型 == "linux":
                # 【第601行】停止服务
                subprocess.run(["sudo", "systemctl", "stop", "longhun-daemon"], check=False)
                # 【第602行】禁用开机自启
                subprocess.run(["sudo", "systemctl", "disable", "longhun-daemon"], check=False)
                # 【第603行】删除服务文件
                subprocess.run(["sudo", "rm", "-f", "/etc/systemd/system/longhun-daemon.service"], check=False)
                # 【第604行】重载systemd
                subprocess.run(["sudo", "systemctl", "daemon-reload"], check=False)
            elif self.系統類型 == "darwin":
                # 【第606行】macOS：unload plist
                plist路徑 = Path.home() / "Library/LaunchAgents/dev.longhun.daemon.plist"
                subprocess.run(["launchctl", "unload", str(plist路徑)], check=False)
                # 【第608行】删除plist文件（missing_ok=True表示文件不存在不报错）
                plist路徑.unlink(missing_ok=True)
            日誌.綠("卸載服務", "系統服務已卸載")
            return True
        except Exception as 異常:
            日誌.紅("卸載服務", f"卸載失敗: {異常}")
            return False

    # ─────────────────────────────────────────
    # 狀態監控與看板
    # ─────────────────────────────────────────
    def 獲取全部狀態(self) -> Dict[str, dict]:
        """獲取所有服務的當前狀態（會刷新實際進程狀態）"""
        結果 = {}
        # 【第621行】遍历注册表中所有服务
        for 服務名稱 in 服務註冊表:
            if 服務名稱 in self.進程表:
                狀態 = self.進程表[服務名稱]
                # 【第625行】刷新实际进程状态（检测进程是否还活着）
                實際狀態 = self.獲取進程狀態(狀態.進程ID)
                # 【第626行】如果实际状态与记录不一致，更新记录
                if 狀態.狀態 != 實際狀態:
                    狀態.狀態 = 實際狀態
                # 【第628行】将状态对象转为字典，加入结果
                結果[服務名稱] = {
                    "進程ID": 狀態.進程ID,
                    "狀態": 狀態.狀態,
                    "啟動時間": 狀態.啟動時間,
                    "最後心跳": 狀態.最後心跳,
                    "重試計數": 狀態.重試計數,
                    "總重啟次數": 狀態.總重啟次數,
                    "端口佔用": 狀態.端口佔用,
                }
            else:
                # 【第638行】如果服务从未启动过
                結果[服務名稱] = {"狀態": "未註冊"}
        return 結果

    def 打印狀態看板(self):
        """在控制台打印ASCII格式的狀態看板（類似top命令）"""
        print("\n" + "=" * 80)
        print(f"  🐉 龍魂守護進程狀態看板  |  {龍魂版本號}  |  {datetime.datetime.now().isoformat()}")
        print("=" * 80)
        狀態表 = self.獲取全部狀態()
        # 【第647行】遍历每个服务，打印状态行
        for 服務名稱, 狀態 in 狀態表.items():
            # 【第648行】根据状态选择对应的emoji图标
            狀態圖標 = {
                "運行中": "🟢",
                "已停止": "🔴",
                "未啟動": "⚪",
                "異常": "🟠",
                "重啟中": "🟡",
                "未註冊": "⚫",
            }.get(狀態.get("狀態", "未知"), "❓")
            # 【第656行】获取服务配置（用于显示端口信息）
            配置 = 服務註冊表.get(服務名稱, {})
            # 【第657行】构造端口显示字符串
            端口信息 = f":{狀態.get('端口佔用', 配置.get('端口', 0))}" if 配置.get("端口") else ""
            # 【第658行】打印格式化状态行
            print(f"  {狀態圖標} {服務名稱:<12} {狀態.get('狀態', '未知'):<6} "
                  f"PID={狀態.get('進程ID', 0):<8} {端口信息:<8} "
                  f"重啟={狀態.get('總重啟次數', 0)}次")
        print("=" * 80 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# 第四區：命令行接口（CLI入口，支持各種命令參數）
# ═══════════════════════════════════════════════════════════════════════════════

def 主函數():
    """命令行入口函數 — 解析參數並執行對應操作"""
    # 【第670行】创建参数解析器
    解析器 = argparse.ArgumentParser(
        description="龍魂守護進程管理器",           # 程序描述
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 守護進程管理器.py --start-all          啟動全部服務
  python3 守護進程管理器.py --stop 龍魂操作台    停止指定服務
  python3 守護進程管理器.py --restart MCP服務    重啟指定服務
  python3 守護進程管理器.py --status             查看狀態看板
  python3 守護進程管理器.py --install            安裝系統服務
  python3 守護進程管理器.py --uninstall          卸載系統服務
        """  # 【第673-681行】使用示例
    )
    # 【第683行】定义--start参数：启动指定服务
    解析器.add_argument("--start", help="啟動指定服務")
    # 【第684行】定义--stop参数：停止指定服务
    解析器.add_argument("--stop", help="停止指定服務")
    # 【第685行】定义--restart参数：重启指定服务
    解析器.add_argument("--restart", help="重啟指定服務")
    # 【第686行】定义--start-all参数：启动所有服务（action=store_true表示不用传值）
    解析器.add_argument("--start-all", action="store_true", help="啟動全部服務")
    # 【第687行】定义--stop-all参数：停止所有服务
    解析器.add_argument("--stop-all", action="store_true", help="停止全部服務")
    # 【第688行】定义--status参数：查看状态看板
    解析器.add_argument("--status", action="store_true", help="查看狀態看板")
    # 【第689行】定义--install参数：安装为系统服务
    解析器.add_argument("--install", action="store_true", help="安裝為系統服務")
    # 【第690行】定义--uninstall参数：卸载系统服务
    解析器.add_argument("--uninstall", action="store_true", help="卸載系統服務")
    # 【第691行】定义--daemon参数：守护进程模式（持续运行）
    解析器.add_argument("--daemon", action="store_true", help="守護進程模式")

    # 【第693行】解析命令行传入的参数
    參數 = 解析器.parse_args()
    # 【第694行】创建守護進程管理器实例（初始化）
    管理器 = 守護進程管理器()

    # 【第696行】根据解析到的参数执行对应操作
    if 參數.start:
        管理器.啟動服務(參數.start)           # 【第697行】啟動指定服務
    elif 參數.stop:
        管理器.停止服務(參數.stop)            # 【第699行】停止指定服務
    elif 參數.restart:
        管理器.重啟服務(參數.restart)         # 【第701行】重啟指定服務
    elif 參數.start_all:
        管理器.啟動全部服務()                 # 【第703行】啟動全部服務
    elif 參數.stop_all:
        管理器.停止全部服務()                 # 【第705行】停止全部服務
    elif 參數.status:
        管理器.打印狀態看板()                 # 【第707行】打印狀態看板
    elif 參數.install:
        管理器.安裝系統服務()                 # 【第709行】安裝為系統服務
    elif 參數.uninstall:
        管理器.卸載系統服務()                 # 【第711行】卸載系統服務
    elif 參數.daemon:
        # ── 守護進程模式（持續運行，自恢復循環）──
        日誌.綠("守護模式", "進入守護進程循環...")
        管理器.運行中 = True
        # 【第715行】主循环：持续运行直到收到退出信号
        while 管理器.運行中:
            try:
                # 【第718行】遍历所有已注册的服务
                for 服務名稱 in 服務註冊表:
                    # 【第719行】如果服务不在进程表中，跳过
                    if 服務名稱 not in 管理器.進程表:
                        continue
                    # 【第721行】获取服务的当前状态
                    狀態 = 管理器.進程表[服務名稱]
                    # 【第722行】获取服务的配置
                    配置 = 服務註冊表[服務名稱]
                    # 【第723行】如果配置了自动重启且服务不在运行中（崩溃了）
                    if 配置.get("自動重啟") and 狀態.狀態 != "運行中":
                        # 【第724行】检查重试次数是否未超过上限
                        if 狀態.重試計數 < 配置.get("最大重試次數", 3):
                            # 【第725行】记录黄色日志：检测到异常，正在自动重启
                            日誌.黃("自恢復", f"[{服務名稱}] 檢測到異常，自動重啟 (第{狀態.重試計數 + 1}次)")
                            # 【第726行】执行重启
                            管理器.重啟服務(服務名稱)
                            # 【第727行】重试计数+1
                            管理器.進程表[服務名稱].重試計數 += 1
                            # 【第728行】总重启次数+1（累计值）
                            管理器.進程表[服務名稱].總重啟次數 += 1
                        else:
                            # 【第730行】如果超过最大重试次数，停止自动恢复
                            日誌.紅("自恢復", f"[{服務名稱}] 重試次數超限，停止自動恢復")
                # 【第731行】每次循环结束后休眠10秒（避免CPU空转）
                time.sleep(10)
            except KeyboardInterrupt:
                # 【第733行】收到Ctrl+C信号，记录退出日志
                日誌.綠("守護模式", "收到退出信號")
                管理器.運行中 = False
            except Exception as 異常:
                # 【第736行】其他异常（如磁盘满、权限变更），记录错误后继续运行
                日誌.紅("守護循環", f"異常: {異常}")
                time.sleep(30)  # 异常后等30秒再试
    else:
        # 【第739行】如果没有传任何参数，默认显示状态看板
        管理器.打印狀態看板()


# ═══════════════════════════════════════════════════════════════════════════════
# 程序入口（Python惯用法：只有直接运行此文件时才执行主函数）
# ═══════════════════════════════════════════════════════════════════════════════

# 【第742行】判断是否是直接运行此文件（而非作为模块被import）
if __name__ == "__main__":
    # 【第743行】调用主函数，开始执行
    主函數()
