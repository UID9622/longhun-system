#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂系统启动·凭证完整性验证脚本

DNA: #龍芯⚡️2026-05-27-VERIFY-CREDENTIALS-ON-BOOT-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

目的：
  系统每次启动时·自动验证所有凭证的完整性
  生成启动验证报告
  发现缺失凭证时发出警告

使用：
  1. 手动运行: python3 verify_credentials_on_boot.py
  2. 在 .zshrc 中添加: python3 ~/longhun-system/config/verify_credentials_on_boot.py
"""

# 献礼: 向曾仕强老师致敬 · 龍魂系統 · UID9622·龍芯北辰

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# 导入凭证管理器
import importlib.util

spec = importlib.util.spec_from_file_location(
    "credential_manager", Path(__file__).parent / "credential_manager_v1.0.py"
)
credential_manager = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(credential_manager)
    CredentialManager = credential_manager.CredentialManager
    CredentialTier = credential_manager.CredentialTier
except Exception as e:
    print(f"❌ 导入凭证管理器失败: {e}")
    print("   请确保 credential_manager_v1.0.py 与本脚本在同一目录")
    sys.exit(1)


class CredentialBootVerifier:
    """系统启动时的凭证验证器"""

    def __init__(self):
        self.mgr = CredentialManager(uid="9622")
        self.report_path = Path(
            "~/longhun-system/日志/credentials_verified_on_boot.jsonl"
        ).expanduser()
        self.report_path.parent.mkdir(parents=True, exist_ok=True)
        self.results = []

    def verify_all(self) -> Tuple[bool, Dict]:
        """验证所有凭证"""
        print("\n" + "=" * 60)
        print("龍魂系统启动·凭证完整性验证")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # 关键凭证（必须存在）
        critical = [
            "notion_api_key",
            "gpg_master_key",
        ]

        # 可选凭证（能找到最好）
        optional = [
            "deepseek_api_key",
            "github_token",
            "huawei_cloud_credentials",
            "cloudflare_token",
        ]

        critical_ok = self._verify_credentials(critical, is_critical=True)
        optional_ok = self._verify_credentials(optional, is_critical=False)

        success = critical_ok

        # 生成报告
        report = self._generate_report(critical_ok, optional_ok)
        self._write_report(report)

        print("\n" + "=" * 60)
        if success:
            print("✅ 所有关键凭证已验证·系统可以启动")
        else:
            print("⚠️  缺失关键凭证·请检查凭证配置")
        print("=" * 60 + "\n")

        return success, report

    def _verify_credentials(
        self, cred_list: List[str], is_critical: bool = False
    ) -> bool:
        """验证一组凭证"""
        cred_type = "【关键凭证】" if is_critical else "【可选凭证】"
        print(f"\n{cred_type}")

        all_found = True
        for cred_name in cred_list:
            # 尝试获取凭证（不需要确认）
            value = self.mgr.get(cred_name, require_confirmation=False)

            if value:
                masked = self.mgr.get_masked(cred_name)
                config = credential_manager.CREDENTIAL_REGISTRY.get(cred_name, {})
                tier = config.get("tier", "UNKNOWN").name

                status = "✅"
                print(f"  {status} {cred_name:<30} | {masked:<20} | {tier}")

                self.results.append(
                    {
                        "credential": cred_name,
                        "status": "FOUND",
                        "tier": tier,
                        "masked": masked,
                    }
                )
            else:
                status = "❌" if is_critical else "⚠️"
                print(f"  {status} {cred_name:<30} | 未找到")

                self.results.append(
                    {
                        "credential": cred_name,
                        "status": "NOT_FOUND",
                        "is_critical": is_critical,
                    }
                )

                if is_critical:
                    all_found = False

        return all_found

    def _generate_report(self, critical_ok: bool, optional_ok: bool) -> Dict:
        """生成验证报告"""
        return {
            "timestamp": datetime.now().isoformat(),
            "system": "longhun",
            "version": "1.0",
            "status": "SUCCESS" if critical_ok else "PARTIAL",
            "critical_verified": critical_ok,
            "optional_verified": optional_ok,
            "details": self.results,
            "summary": {
                "total_checked": len(self.results),
                "found": sum(1 for r in self.results if r["status"] == "FOUND"),
                "not_found": sum(1 for r in self.results if r["status"] == "NOT_FOUND"),
            },
            "next_action": (
                "系统可以启动" if critical_ok else "请补充缺失的关键凭证后再启动"
            ),
        }

    def _write_report(self, report: Dict):
        """写入报告到JSONL日志"""
        try:
            with open(self.report_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(report, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"⚠️  报告写入失败: {e}")


# ====================================================================
# 主函数
# ====================================================================

if __name__ == "__main__":
    verifier = CredentialBootVerifier()
    success, report = verifier.verify_all()

    # 返回系统状态码
    sys.exit(0 if success else 1)
