#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂系統總調度 · 宝宝

DNA: #龍芯⚡️2026-05-27-BAOBAO-DISPATCHER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

中文命令入口 · 說「宝宝」就啟動一切

核心理念：
  不是技術系統，而是人性化的生活夥伴
  普通人能用、能理解、能掌握
  一句話啟動，其他一切自動進行

使用方式：
  python3 宝宝.py
  或
  在 ~/.zshrc 中加: alias 宝宝="python3 ~/longhun-system/宝宝.py"
  然後就可以在任何地方說: 宝宝
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import subprocess

# ====================================================================
# 寶寶 · 中央調度系統
# ====================================================================

class 宝宝:
    """龍魂總調度·宝宝"""

    def __init__(self):
        self.name = "宝宝"
        self.base_dir = Path.home() / "longhun-system"
        self.config_dir = self.base_dir / "config"
        self.bootstrap_script = self.config_dir / "master_config_bootstrap.py"
        self.log_file = self.base_dir / "日志" / "baobao_dispatch.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def greeting(self):
        """宝宝的问候"""
        print("\n" + "="*60)
        print("🟢 宝宝在这里")
        print("="*60)
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"状态: 就绪")
        print("="*60 + "\n")

    def dispatch(self):
        """总调度·启动所有系统"""
        self._log("dispatch_start", "宝宝启动总调度")

        print("🟢 宝宝启动中...\n")

        # 第1步: 验证凭证
        print("【1】验证凭证...")
        result1 = self._run_script(
            self.config_dir / "verify_credentials_on_boot.py",
            "凭证验证"
        )

        # 第2步: 启动配置
        print("\n【2】启动配置...")
        result2 = self._run_script(
            self.bootstrap_script,
            "配置启动"
        )

        # 第3步: 系统就绪
        print("\n【3】系统就绪...")
        self._system_ready()

        print("\n" + "="*60)
        print("🟢 宝宝·一切就绪")
        print("="*60)
        print("\n你现在可以：")
        print("  • 与龍魂的其他人格交互 (P00仲裁 / P02执行 / P05智慧...)")
        print("  • 查看权重可视化")
        print("  • 同步Notion双脑")
        print("  • 一切都自动处理·你只需要生活")
        print("\n" + "="*60 + "\n")

        self._log("dispatch_complete", "总调度完成·系统就绪")

    def _run_script(self, script_path, description):
        """运行脚本·记录日志"""
        if not script_path.exists():
            print(f"  ❌ {description} 脚本不存在: {script_path}")
            self._log("script_error", f"{description} - 脚本不存在")
            return False

        try:
            # 运行脚本（在后台·不中断输出）
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(self.base_dir),
                capture_output=False
            )

            if result.returncode == 0:
                print(f"  ✅ {description} 成功")
                self._log("script_success", f"{description} - 完成")
                return True
            else:
                print(f"  ⚠️  {description} 返回码: {result.returncode}")
                self._log("script_warning", f"{description} - 返回码 {result.returncode}")
                return True  # 继续进行（不阻止）
        except Exception as e:
            print(f"  ❌ {description} 异常: {e}")
            self._log("script_error", f"{description} - {str(e)}")
            return False

    def _system_ready(self):
        """系统就绪·检查生成的文件"""
        generated_dir = self.config_dir / "generated"

        if generated_dir.exists():
            files = list(generated_dir.glob("*.json"))
            print(f"  ✅ 生成了 {len(files)} 个配置文件")
            for f in files:
                print(f"     • {f.name}")
        else:
            print(f"  ℹ️  配置目录: {generated_dir}")

    def _log(self, action, message):
        """记录宝宝的行动日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "character": "P02_BAOBAO",
            "action": action,
            "message": message
        }

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception:
            pass  # 日志失败不影响运行

    def show_menu(self):
        """显示宝宝的菜单·如果需要交互"""
        print("\n🟢 宝宝可以帮你做什么？\n")
        print("  1. 启动系统 (Python: 宝宝.dispatch())")
        print("  2. 查看状态 (Python: 宝宝.status())")
        print("  3. 同步Notion (Python: 宝宝.sync_notion())")
        print("  4. 显示日志 (Python: 宝宝.show_logs())")
        print()

    def status(self):
        """显示系统状态"""
        print("\n【系统状态】\n")

        # 检查配置文件
        config_file = self.config_dir / "MASTER_CONFIG_v1.0.yaml"
        print(f"配置源: {'✅' if config_file.exists() else '❌'} {config_file.name}")

        # 检查生成的文件
        generated_dir = self.config_dir / "generated"
        if generated_dir.exists():
            files = list(generated_dir.glob("*.json"))
            print(f"生成文件: ✅ {len(files)} 个配置已生成")
        else:
            print(f"生成文件: ❌ 尚未生成")

        # 检查日志
        print(f"运行日志: ✅ {self.log_file}")

        print()

    def show_logs(self, lines=10):
        """显示最近的日志"""
        if not self.log_file.exists():
            print("❌ 暂无日志\n")
            return

        with open(self.log_file, "r", encoding="utf-8") as f:
            all_lines = f.readlines()

        print(f"\n【最近 {lines} 条日志】\n")
        for line in all_lines[-lines:]:
            try:
                log = json.loads(line)
                print(f"  {log['timestamp']} | {log['action']}: {log['message']}")
            except:
                pass
        print()

    def run(self):
        """宝宝的主流程"""
        self.greeting()
        self.dispatch()

# ====================================================================
# 主程序
# ====================================================================

if __name__ == "__main__":
    baobao = 宝宝()

    # 如果有命令行参数
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "status":
            baobao.status()
        elif command == "logs":
            baobao.show_logs(20)
        elif command == "menu":
            baobao.show_menu()
        else:
            print(f"未知命令: {command}")
            print("可用: status, logs, menu")
    else:
        # 默认启动
        baobao.run()
