#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂服务管理器 v1.0（对齐修正版）
DNA: #龍芯⚡️2026-08-25-SERVICE-MANAGER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

对齐修正（vs M77 原稿）：
  - 服务列表全部替换为 longhun-system 真实存在的服务（原稿 hash_api.py /
    longhun_backup.py / api_gateway.py 均不存在）
  - :8766 实为「主权网关」（非渲染）· 渲染真身 :8972（lh_render.py server）
  - :9623 实为「注册中心 registry_server」（非龍魂备控）
  - launchd 托管服务用 launchctl kickstart 重启（不抢守护职责·避免重复守护打架）
  - 新增熔断：重启超上限 → 不再重启，耻辱墙记录
"""

import os
import signal
import socket
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

# longhun-system 仓库根目录（自动解析）
_REPO_ROOT = str(Path.home() / "longhun-system")
_BIN_DIR   = f"{_REPO_ROOT}/08_BIN"
_UID       = os.getuid()


@dataclass
class 服务配置:
    名称: str
    端口: int
    重启命令: str                 # 真实启动/重启命令（launchctl kickstart 或 python3 ...）
    健康路径: str = "/"           # 端口探测以外的可选 HTTP 健康检查路径
    自动重启: bool = True
    最大重启次数: int = 3
    当前重启次数: int = field(default=0, compare=False)
    熔断中: bool = field(default=False, compare=False)  # 新增：超上限后熔断


class ServiceManager:
    def __init__(self):
        self.服务列表: Dict[str, 服务配置] = {}
        self._init_default_services()

    def _init_default_services(self):
        """默认服务列表 · 全部真实存在于 longhun-system（2026-08-25 实测）"""
        defaults = [
            服务配置(
                名称="龍魂API网关",
                端口=9622,
                重启命令=f"launchctl kickstart -k gui/{_UID}/com.longhun.internal-net",
                健康路径="/health",
            ),
            服务配置(
                名称="主权网关",
                端口=8766,
                重启命令=f"python3 {_BIN_DIR}/lh_sovereign_gateway.py",
            ),
            服务配置(
                名称="渲染服务M75",
                端口=8972,
                重启命令=f"python3 {_BIN_DIR}/lh_render.py server",
                健康路径="/render/health",
            ),
            服务配置(
                名称="Ollama模型",
                端口=11434,
                重启命令=f"launchctl kickstart -k gui/{_UID}/homebrew.mxcl.ollama",
                健康路径="/api/version",
            ),
            服务配置(
                名称="注册中心",
                端口=9623,
                重启命令=f"python3 {_REPO_ROOT}/deploy/longhun-registry/registry_server.py --host 127.0.0.1 --port 9623",
            ),
            服务配置(
                名称="Ollama反代",
                端口=11435,
                重启命令=f"launchctl kickstart -k gui/{_UID}/com.uid9622.ollama-host-proxy",
            ),
        ]
        for svc in defaults:
            self.服务列表[svc.名称] = svc

    def load_from_yaml(self, config: Dict) -> bool:
        """从 YAML 配置的「服务监控」列表加载服务（配置优先，硬编码默认兜底）。

        支持 Mac/鲲鹏 共用同一套代码：各平台只需维护自己的 doorkeeper_config.yml。
        无「服务监控」或列表为空 → 返回 False，继续使用默认硬编码列表。
        """
        items = (config or {}).get("服务监控")
        if not items:
            return False
        self.服务列表 = {}
        for it in items:
            name = it.get("名称")
            if not name:
                continue
            self.服务列表[name] = 服务配置(
                名称=name,
                端口=int(it.get("端口", 0)),
                重启命令=it.get("重启命令", ""),
                健康路径=it.get("健康路径", "/"),
                自动重启=bool(it.get("自动重启", True)),
                最大重启次数=int(it.get("最大重启次数", 3)),
            )
        return True

    def check_port(self, port: int, host: str = '127.0.0.1', timeout: int = 2) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def check_health(self, svc: 服务配置) -> bool:
        """端口存活 + 可选 HTTP 健康路径双重校验（避免"端口开但服务废"假阳性）"""
        if not self.check_port(svc.端口):
            return False
        if svc.健康路径 == "/":
            return True
        try:
            import urllib.request
            req = urllib.request.Request(
                f"http://127.0.0.1:{svc.端口}{svc.健康路径}",
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=2) as resp:
                return 200 <= resp.status < 500   # 404 视为存活但无该路由（registry/审计类服务常见）
        except Exception:
            return False

    def get_service_status(self, 服务名: str) -> Dict:
        svc = self.服务列表.get(服务名)
        if not svc:
            return {"错误": "服务不存在"}
        存活 = self.check_health(svc)
        return {
            "服务名":     svc.名称,
            "端口":       svc.端口,
            "健康路径":   svc.健康路径,
            "端口存活":   存活,
            "运行状态":   "running" if 存活 else "stopped",
            "自动重启":   svc.自动重启,
            "重启次数":   svc.当前重启次数,
            "最大重启":   svc.最大重启次数,
            "熔断中":     svc.熔断中,
        }

    def get_all_services_status(self) -> List[Dict]:
        return [self.get_service_status(name) for name in self.服务列表]

    def _run_restart_command(self, svc: 服务配置) -> bool:
        """launchctl 命令用 run（等待完成），普通进程用 Popen（后台常驻）"""
        try:
            if svc.重启命令.startswith("launchctl"):
                subprocess.run(svc.重启命令, shell=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               timeout=10)
            else:
                subprocess.Popen(
                    svc.重启命令, shell=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
            time.sleep(3)
            return self.check_health(svc)
        except Exception:
            return False

    def start_service(self, 服务名: str) -> Dict:
        svc = self.服务列表.get(服务名)
        if not svc:
            return {"成功": False, "错误": "服务不存在"}
        if svc.熔断中:
            return {"成功": False, "错误": f"{服务名} 已熔断，需人工干预后 reset_fuse"}
        if self.check_health(svc):
            return {"成功": True, "消息": f"{服务名} 已在运行"}
        ok = self._run_restart_command(svc)
        if ok:
            svc.当前重启次数 = 0
            return {"成功": True, "消息": f"{服务名} 启动成功"}
        return {"成功": False, "错误": f"{服务名} 启动超时，端口未开"}

    def stop_service(self, 服务名: str) -> Dict:
        """按端口停止占用进程（注意：launchd 托管服务会被自动拉起）"""
        svc = self.服务列表.get(服务名)
        if not svc:
            return {"成功": False, "错误": "服务不存在"}
        try:
            result = subprocess.run(
                f"lsof -ti:{svc.端口}",
                shell=True, capture_output=True, text=True
            )
            if result.stdout.strip():
                for pid in result.stdout.strip().split('\n'):
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                return {"成功": True, "消息": f"{服务名} 已停止"}
            return {"成功": True, "消息": f"{服务名} 未运行"}
        except Exception as e:
            return {"成功": False, "错误": str(e)}

    def restart_service(self, 服务名: str) -> Dict:
        """含熔断逻辑：超过最大重启次数则熔断，不再重启"""
        svc = self.服务列表.get(服务名)
        if not svc:
            return {"成功": False, "错误": "服务不存在"}
        if svc.熔断中:
            return {"成功": False, "错误": f"{服务名} 已熔断，需人工干预"}
        if svc.当前重启次数 >= svc.最大重启次数:
            svc.熔断中 = True
            return {
                "成功": False,
                "熔断": True,
                "错误": f"{服务名} 重启 {svc.当前重启次数} 次已达上限，触发熔断"
            }
        self.stop_service(服务名)
        time.sleep(2)
        result = self.start_service(服务名)
        if result.get("成功"):
            svc.当前重启次数 = 0
        else:
            svc.当前重启次数 += 1
        return result

    def reset_fuse(self, 服务名: str) -> Dict:
        """人工重置熔断（需人工干预后调用）"""
        svc = self.服务列表.get(服务名)
        if not svc:
            return {"成功": False, "错误": "服务不存在"}
        svc.熔断中 = False
        svc.当前重启次数 = 0
        return {"成功": True, "消息": f"{服务名} 熔断已重置"}


# 全局服务管理器单例
service_mgr = ServiceManager()
