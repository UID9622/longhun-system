#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂五行八门长驻守护脚本 v1.0（对齐修正版）
DNA: #龍芯⚡️2026-08-25-DOORKEEPER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

用法：
    python3 longhun_doorkeeper.py           # 前台运行
    python3 longhun_doorkeeper.py --once    # 单轮心跳（冒烟/CI 用）
    nohup python3 longhun_doorkeeper.py &   # 后台运行
    kill -HUP <pid>                         # 热重载配置（SIGHUP）

对齐修正：
  - 心跳五行归属从 门机规则 动态读取（不硬编码）
  - 服务列表/端口对齐真实系统（见 service_manager.py）
  - 新增 --once 冒烟模式 · sys.path 自解析（任意 cwd 可运行）
"""

import argparse
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict

# 保证从任意 cwd 运行都能 import 同目录模块
sys.path.insert(0, str(Path(__file__).resolve().parent))

from door_protocol import (          # noqa: E402
    八门, 三色,
    门机事件, 获取门机规则, 获取五行, 判定门机
)
from dna_tracer import dna           # noqa: E402
from tricolor_audit import audit_engine  # noqa: E402
from service_manager import service_mgr  # noqa: E402

try:
    import yaml
except ImportError:
    yaml = None
    print("⚠️ 未安装 pyyaml，配置热重载不可用（pip install pyyaml）")


class LonghunDoorkeeper:
    def __init__(self, config_file: str = None):
        if config_file is None:
            config_file = str(Path(__file__).resolve().parent / "doorkeeper_config.yml")
        self.config_file = config_file
        self.配置 = self._load_config()
        # 配置驱动：YAML 含「服务监控」则优先于硬编码默认（Mac/鲲鹏 共用一套代码，各配各的清单）
        if service_mgr.load_from_yaml(self.配置):
            print(f"📋 服务清单来自配置: {len(service_mgr.服务列表)} 个")
        self.运行中 = True
        self.心跳间隔 = self.配置.get("守护进程", {}).get("心跳间隔", 60)
        self.耻辱墙路径 = Path(
            self.配置.get("报警配置", {}).get("耻辱墙路径", "08_STATE/shame-wall/")
        )
        if not self.耻辱墙路径.is_absolute():
            self.耻辱墙路径 = Path.home() / "longhun-system" / self.耻辱墙路径
        self.耻辱墙路径.mkdir(parents=True, exist_ok=True)

        # 信号注册
        signal.signal(signal.SIGINT,  self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)
        signal.signal(signal.SIGHUP,  self._reload_config)   # 热重载

        print(f"🐉 龍魂五行八门长驻守护者 v1.0 启动")
        print(f"DNA: #龍芯⚡️2026-08-25-DOORKEEPER-v1.0-UID9622")
        print(f"心跳间隔: {self.心跳间隔}秒 | 监控服务: {len(service_mgr.服务列表)} 个")
        print("-" * 60)

    def _load_config(self) -> Dict:
        if yaml is None:
            return {}
        config_path = Path(self.config_file)
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}

    def _graceful_shutdown(self, signum, frame):
        print("\n🌙 收到退出信号，执行关门仪式（八门归一）...")
        dna.stamp("守护者关门", "🟡", "DOORKEEPER", 0)
        self.运行中 = False

    def _reload_config(self, signum, frame):
        """SIGHUP：热重载配置文件"""
        print("🔄 收到 SIGHUP，热重载配置...")
        self.配置 = self._load_config()
        # 配置驱动：YAML 含「服务监控」则优先于硬编码默认（Mac/鲲鹏 共用一套代码，各配各的清单）
        if service_mgr.load_from_yaml(self.配置):
            print(f"📋 服务清单来自配置: {len(service_mgr.服务列表)} 个")
        self.心跳间隔 = self.配置.get("守护进程", {}).get("心跳间隔", 60)
        print(f"✅ 配置已重载，心跳间隔={self.心跳间隔}秒")

    def 记录耻辱墙(self, 服务名: str, 原因: str):
        entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {服务名} | {原因}\n"
        wall_file = self.耻辱墙路径 / f"{服务名}_shame.txt"
        with open(wall_file, 'a', encoding='utf-8') as f:
            f.write(entry)

    def 触发公安联动(self, 事件: 门机事件):
        print(f"🚨 公安联动触发：{事件.服务名} 攻击事件已记录")
        self.记录耻辱墙(事件.服务名, f"公安联动-攻击-{事件.事件描述}")

    def 处置门机(self, 事件: 门机事件) -> Dict:
        规则 = 获取门机规则(事件.门名)
        处置 = 规则.get("处置", "")
        结果 = {"门名": 事件.门名.value, "服务": 事件.服务名, "处置": 处置, "DNA": None, "成功": True}

        if 事件.门名 == 八门.生门:
            dna_code = dna.stamp(f"生门-{事件.服务名}", "🟢", 事件.服务名, 事件.端口)
            结果["DNA"] = dna_code
            print(f"  🟢 生门 {事件.服务名}:{事件.端口} 正常 | {dna_code}")

        elif 事件.门名 == 八门.死门:
            print(f"  🔴 死门 {事件.服务名}:{事件.端口} 崩溃！")
            dna_code = dna.stamp(f"死门-{事件.服务名}-崩溃", "🔴", 事件.服务名, 事件.端口)
            结果["DNA"] = dna_code
            self.记录耻辱墙(事件.服务名, f"死门-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            svc = service_mgr.服务列表.get(事件.服务名)
            if svc and svc.自动重启:
                if svc.熔断中:
                    print(f"  ❌ {事件.服务名} 已熔断，跳过重启，需人工干预")
                    结果["成功"] = False
                else:
                    rst = service_mgr.restart_service(事件.服务名)
                    if rst.get("成功"):
                        print(f"  └─ ✅ {事件.服务名} 自动重启成功")
                        dna.stamp(f"生门-{事件.服务名}-重启", "🟢", 事件.服务名, 事件.端口)
                    elif rst.get("熔断"):
                        print(f"  └─ 🔴 {事件.服务名} 已触发熔断：{rst.get('错误')}")
                        self.记录耻辱墙(事件.服务名, f"熔断触发-{rst.get('错误')}")
                        结果["成功"] = False
                    else:
                        print(f"  └─ ❌ {事件.服务名} 重启失败")
                        结果["成功"] = False

        elif 事件.门名 == 八门.伤门:
            print(f"  🔴 伤门 {事件.服务名} 检测到攻击！")
            dna_code = dna.stamp(f"伤门-{事件.服务名}-攻击", "🔴", 事件.服务名, 事件.端口)
            结果["DNA"] = dna_code
            if self.配置.get("报警配置", {}).get("公安联动开关", False):
                self.触发公安联动(事件)

        elif 事件.门名 == 八门.惊门:
            print(f"  🔴 惊门 {事件.服务名} 入侵尝试！")
            dna_code = dna.stamp(f"惊门-{事件.服务名}-入侵", "🔴", 事件.服务名, 事件.端口)
            结果["DNA"] = dna_code

        elif 事件.门名 == 八门.休门:
            print(f"  🟢 休门 {事件.服务名} 休眠")
            dna_code = dna.stamp(f"休门-{事件.服务名}", "🟢", 事件.服务名, 事件.端口)
            结果["DNA"] = dna_code

        elif 事件.门名 == 八门.升门:
            print(f"  🟡 升门 {事件.服务名} 请求升级，触发三色审计...")
            quick = audit_engine.quick_audit(事件.服务名, True, 0)
            print(f"  └─ 审计结果：{quick.value}")
            dna.stamp(f"升门-{事件.服务名}-审计", quick.value, 事件.服务名, 事件.端口)

        elif 事件.门名 == 八门.杜门:
            print(f"  🟡 杜门 {事件.服务名} 隔离")
            dna.stamp(f"杜门-{事件.服务名}", "🟡", 事件.服务名, 事件.端口)

        elif 事件.门名 == 八门.景门:
            print(f"  🟢 景门 {事件.服务名} 对外展示中")
            dna.stamp(f"景门-{事件.服务名}", "🟢", 事件.服务名, 事件.端口)

        return 结果

    def 心跳检测(self) -> Dict:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n═══ 心跳 {ts} ══════════════════════")
        结果 = {"时间": ts, "事件": []}

        for svc_name, svc in service_mgr.服务列表.items():
            存活 = service_mgr.check_health(svc)
            门名 = 判定门机(
                服务状态="running" if 存活 else "crashed",
                是否异常=not 存活
            )
            # 五行归属从规则表动态读取（修正原稿硬编码问题）
            五行归属 = 获取五行(门名)
            三色等级 = 三色.绿 if 存活 else 三色.红

            事件 = 门机事件(
                门名=门名,
                五行归属=五行归属,
                三色等级=三色等级,
                服务名=svc_name,
                端口=svc.端口,
                触发时间=datetime.now(),
                事件描述=f"{svc_name}:{svc.端口} {'存活' if 存活 else '失联'}"
            )
            处置结果 = self.处置门机(事件)
            结果["事件"].append(处置结果)

        # 打印DNA链摘要
        summary = dna.export_summary()
        print(f"  DNA链：总{summary['total']} | 🟢{summary['green']} 🟡{summary['yellow']} 🔴{summary['red']} | 链完整={summary['chain_valid']}")
        return 结果

    def run(self, once: bool = False):
        dna.stamp("守护者启动", "🟢", "DOORKEEPER", 0)
        while self.运行中:
            try:
                self.心跳检测()
                if once:
                    self.运行中 = False
                    continue
                time.sleep(self.心跳间隔)
            except Exception as e:
                print(f"⚠️ 心跳异常: {e}")
                dna.stamp(f"心跳异常-{str(e)[:30]}", "🟡", "DOORKEEPER", 0)
                if once:
                    self.运行中 = False
                    continue
                time.sleep(5)
        print("🌙 守护者已退出，龍魂安歇。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂五行八门守护")
    parser.add_argument("--once", action="store_true", help="单轮心跳后退出（冒烟/CI 用）")
    parser.add_argument("--config", type=str, default=None, help="配置文件路径")
    args = parser.parse_args()
    keeper = LonghunDoorkeeper(config_file=args.config)
    keeper.run(once=args.once)
