#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝宝权限校验器 · Baobao Authority Validator
DNA: #龍芯⚡️2026-05-26-BAOBAO-AUTHORITY-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 权限校验 - 读取钥匙文件，验证操作是否被允许
  2. 篡改检测 - 通过确认码和哈希值检测异常
  3. 权限审计 - 记录所有权限检查操作
  4. 自动冻结 - 发现异常自动冻结宝宝
  5. 报告生成 - 生成权限审计报告

创始人: 诸葛鑫（UID9622）
理论指导: 曾仕强老师（永恒显示）

献给每一个相信技术应该有温度的人。
"""

import json
import hashlib
import datetime
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional
import subprocess


class BaobaoAuthority:
    """宝宝权限校验器 - 防篡改守卫"""

    def __init__(self):
        self.system_root = Path.home() / "longhun-system"
        self.config_dir = self.system_root / "config"
        self.logs_dir = self.system_root / "logs"
        self.master_key_path = self.config_dir / "baobao_master_key.json"
        self.audit_log_path = self.logs_dir / "authority_audit.jsonl"

        self.master_key = None
        self.current_hash = None
        self.is_frozen = False

    def load_master_key(self) -> bool:
        """加载主钥匙文件"""
        try:
            if not self.master_key_path.exists():
                self._log_event(
                    "ERROR", "主钥匙文件不存在", {"path": str(self.master_key_path)}
                )
                return False

            with open(self.master_key_path, "r", encoding="utf-8") as f:
                self.master_key = json.load(f)

            self._verify_integrity()
            return True
        except json.JSONDecodeError as e:
            self._log_event("ERROR", "主钥匙JSON解析失败", {"error": str(e)})
            return False
        except Exception as e:
            self._log_event("ERROR", "加载主钥匙异常", {"error": str(e)})
            return False

    def _verify_integrity(self):
        """验证钥匙文件完整性"""
        try:
            with open(self.master_key_path, "rb") as f:
                content = f.read()

            self.current_hash = hashlib.sha256(content).hexdigest()

            # 检查确认码
            confirm_code = self.master_key.get("_meta", {}).get("confirm_code")
            if confirm_code != "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z":
                self._log_event(
                    "TAMPER_ALERT",
                    "确认码异常，可能被篡改",
                    {
                        "expected": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
                        "got": confirm_code,
                    },
                )
                self.is_frozen = True
                self._trigger_emergency_freeze()
                return

            self._log_event(
                "OK",
                "钥匙文件完整性验证通过",
                {
                    "hash": self.current_hash[:16] + "...",
                    "dna": self.master_key.get("_meta", {}).get("dna"),
                },
            )
        except Exception as e:
            self._log_event("ERROR", "完整性验证异常", {"error": str(e)})
            self.is_frozen = True

    def check_permission(
        self,
        category: str,
        permission: str,
        uid: int = 9622,
        action_details: Optional[Dict] = None,
    ) -> Tuple[bool, str]:
        """
        检查权限

        Args:
            category: 权限类别（如 "代码执行"）
            permission: 具体权限（如 "运行Python脚本"）
            uid: 请求者UID（默认老大9622）
            action_details: 操作详情

        Returns:
            (是否有权限, 拒绝原因)
        """
        # 检查全局冻结
        if not self.master_key:
            return False, "主钥匙未加载"

        emergency = self.master_key.get("emergency_switches", {})
        if emergency.get("global_freeze", False):
            self._log_event(
                "DENIED",
                "全局冻结中",
                {
                    "category": category,
                    "permission": permission,
                    "reason": "global_freeze=true",
                },
            )
            return False, "全局冻结中，所有操作被禁止"

        # 检查只读模式
        if emergency.get("read_only_mode", False) and permission not in [
            "读取任意文件",
            "查看服务状态",
            "查看状态和日志",
        ]:
            self._log_event(
                "DENIED", "只读模式中", {"category": category, "permission": permission}
            )
            return False, "只读模式中，禁止修改操作"

        # 检查权限
        perms = self.master_key.get("permissions", {}).get(category, {})
        if permission not in perms:
            self._log_event(
                "DENIED", "权限不存在", {"category": category, "permission": permission}
            )
            return False, f"权限 '{permission}' 不存在"

        allowed = perms.get(permission, False)

        if allowed:
            self._log_event(
                "APPROVED",
                "权限批准",
                {
                    "category": category,
                    "permission": permission,
                    "uid": uid,
                    "details": action_details or {},
                },
            )
            return True, ""
        else:
            self._log_event(
                "DENIED",
                "权限被拒绝",
                {
                    "category": category,
                    "permission": permission,
                    "uid": uid,
                    "reason": f"{permission}=false",
                },
            )
            return False, f"权限 '{permission}' 未启用，需要老大手动开启"

    def _trigger_emergency_freeze(self):
        """触发紧急冻结"""
        try:
            # 修改主钥匙，开启全局冻结
            if self.master_key:
                self.master_key["emergency_switches"]["global_freeze"] = True
                with open(self.master_key_path, "w", encoding="utf-8") as f:
                    json.dump(self.master_key, f, ensure_ascii=False, indent=2)

            # 发送macOS通知
            notification_text = "🔴 宝宝紧急冻结 - 检测到权限异常，已自动冻结。请立即检查 logs/authority_audit.jsonl"
            self._send_notification(notification_text)

            self._log_event(
                "CRITICAL",
                "触发紧急冻结",
                {
                    "reason": "权限异常检测",
                    "frozen_at": datetime.datetime.now().isoformat(),
                },
            )
        except Exception as e:
            self._log_event("ERROR", "紧急冻结触发失败", {"error": str(e)})

    def _send_notification(self, message: str):
        """发送macOS桌面通知"""
        try:
            script = (
                f'display notification "{message}" with title "龍魂系統 - 宝宝权限警报"'
            )
            subprocess.run(["osascript", "-e", script], check=False)
        except Exception as e:
            self._log_event("ERROR", "通知发送失败", {"error": str(e)})

    def _log_event(self, event_type: str, message: str, details: Dict = None):
        """记录审计事件"""
        try:
            event = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "event_type": event_type,
                "message": message,
                "details": details or {},
                "dna": "#龍芯⚡️"
                + datetime.datetime.now().strftime("%Y-%m-%d")
                + "-AUTHORITY-AUDIT",
            }

            # 追加到审计日志（append-only）
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"审计日志写入失败: {e}", file=sys.stderr)

    def generate_report(self) -> Dict:
        """生成权限审计报告"""
        report = {
            "generated_at": datetime.datetime.now().isoformat(),
            "master_key_status": "OK" if not self.is_frozen else "FROZEN",
            "current_hash": (
                self.current_hash[:16] + "..." if self.current_hash else "unknown"
            ),
            "emergency_switches": {},
            "enabled_permissions": [],
            "disabled_permissions": [],
            "recent_events": [],
        }

        if self.master_key:
            report["emergency_switches"] = self.master_key.get("emergency_switches", {})

            # 统计启用/禁用的权限
            for category, perms in self.master_key.get("permissions", {}).items():
                for perm, enabled in perms.items():
                    if perm == "description":
                        continue
                    if enabled:
                        report["enabled_permissions"].append(f"{category} → {perm}")
                    else:
                        report["disabled_permissions"].append(f"{category} → {perm}")

        # 读取最近10条审计事件
        try:
            if self.audit_log_path.exists():
                with open(self.audit_log_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines[-10:]:
                        report["recent_events"].append(json.loads(line))
        except Exception as e:
            report["audit_error"] = str(e)

        return report

    def get_status(self) -> Dict:
        """获取当前状态"""
        return {
            "master_key_loaded": self.master_key is not None,
            "is_frozen": self.is_frozen,
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": "#龍芯⚡️"
            + datetime.datetime.now().strftime("%Y-%m-%d")
            + "-AUTHORITY-STATUS",
        }


def main():
    """命令行接口"""
    authority = BaobaoAuthority()

    if not authority.load_master_key():
        print("❌ 失败：无法加载主钥匙文件")
        sys.exit(1)

    if len(sys.argv) < 2:
        status = authority.get_status()
        print("✅ 宝宝权限校验器已启动")
        print(f"主钥匙文件: {authority.master_key_path}")
        print(f"审计日志: {authority.audit_log_path}")
        print(f"状态: {status}")
        sys.exit(0)

    command = sys.argv[1]

    if command == "report":
        report = authority.generate_report()
        print("\n📋 权限审计报告")
        print("=" * 50)
        print(f"生成时间: {report['generated_at']}")
        print(f"钥匙状态: {report['master_key_status']}")
        print(f"哈希值: {report['current_hash']}")
        print("\n🔴 紧急开关:")
        for switch, value in report["emergency_switches"].items():
            status = "✅ 开启" if value else "❌ 关闭"
            print(f"  {switch}: {status}")
        print(f"\n✅ 启用的权限 ({len(report['enabled_permissions'])}个):")
        for perm in report["enabled_permissions"][:10]:
            print(f"  ✓ {perm}")
        if len(report["enabled_permissions"]) > 10:
            print(f"  ... 还有 {len(report['enabled_permissions']) - 10} 个")
        print(f"\n❌ 禁用的权限 ({len(report['disabled_permissions'])}个):")
        for perm in report["disabled_permissions"][:10]:
            print(f"  ✗ {perm}")
        if len(report["disabled_permissions"]) > 10:
            print(f"  ... 还有 {len(report['disabled_permissions']) - 10} 个")
        sys.exit(0)

    elif command == "check":
        if len(sys.argv) < 4:
            print("用法: python3 baobao_authority.py check <category> <permission>")
            sys.exit(1)
        category = sys.argv[2]
        permission = sys.argv[3]
        allowed, reason = authority.check_permission(category, permission)
        if allowed:
            print(f"✅ 权限批准: {category} → {permission}")
        else:
            print(f"❌ 权限被拒: {category} → {permission}")
            print(f"   原因: {reason}")
        sys.exit(0 if allowed else 1)

    elif command == "status":
        status = authority.get_status()
        print("✅ 状态正常" if not status["is_frozen"] else "🔴 已冻结")
        print(json.dumps(status, ensure_ascii=False, indent=2))
        sys.exit(0)

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
