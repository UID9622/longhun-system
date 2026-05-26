#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂主干配置启动脚本 v1.0

DNA: #龍芯⚡️2026-05-26-MASTER-CONFIG-BOOTSTRAP-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

目的：
  从单一真实源头 (MASTER_CONFIG_v1.0.yaml) 启动
  自动生成所有衍生配置文件
  确保系统启动时所有文件一致

使用：
  python3 master_config_bootstrap.py
  └─ 启动时自动运行（可加入 .zshrc 或系统启动脚本）
"""

import yaml
import json
import hashlib
from pathlib import Path
from datetime import datetime


class MasterConfigBootstrap:
    """从主干配置启动系统"""

    def __init__(self, config_path: str = "MASTER_CONFIG_v1.0.yaml"):
        self.config_path = Path(config_path)
        self.config = None
        self.generated_dir = Path("./generated")
        self.generated_dir.mkdir(exist_ok=True)

        self.log_file = self.generated_dir / "bootstrap.log"
        self._log("\n{'='*60}")
        self._log("龍魂主干配置启动 | {datetime.now().isoformat()}")
        self._log("{'='*60}")

    def _log(self, message: str):
        """记录启动日志"""
        print(message)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def load_master_config(self) -> bool:
        """加载主干配置"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
            self._log("✓ 主干配置已加载: {self.config_path}")
            return True
        except Exception as e:
            self._log("✗ 加载主干配置失败: {e}")
            return False

    def validate_config(self) -> bool:
        """验证配置完整性"""
        required_sections = [
            "behavioral_cryptography",
            "five_color_audit",
            "weight_formulas",
            "multi_persona_system",
            "dna_signature_system",
            "metadata",
        ]

        missing = [s for s in required_sections if s not in self.config]

        if missing:
            self._log("⚠️  缺失部分: {', '.join(missing)}")
        else:
            self._log("✓ 配置完整性检查通过")
        return len(missing) == 0

    def generate_behavioral_profiles(self):
        """生成 behavioral_profiles.json"""
        self._log("\n【生成】behavioral_profiles.json")

        profiles = {
            "registry_metadata": {
                "name": "行为密码学·身份特征库",
                "dna": self.config["metadata"]["dna"],
                "timestamp": datetime.now().isoformat(),
                "version": "{self.config['metadata']['versioning']['major']}.{self.config['metadata']['versioning']['minor']}",
                "status": "🟢 ACTIVE",
                "description": "通过F5/F6/F7不动点，存储已知用户的行为特征，用于身份识别",
            }
        }

        # 从主干配置提取 F5/F6/F7
        if "behavioral_cryptography" in self.config:
            bc = self.config["behavioral_cryptography"]

            # 建构 UID9622
            profiles["UID9622"] = {
                "name": "诸葛鑫（老大）",
                "role": "龍魂系統創始人",
                "status": "verified",
                "verification_date": datetime.now().strftime("%Y-%m-%d"),
                "confirmation_code": self.config["metadata"]["confirm"],
                "gpg_fingerprint": self.config["metadata"]["gpg_fingerprint"],
                "identity_confidence_threshold": 0.75,
                "features": {
                    "F5_vocabulary": bc["F5_vocabulary"]
                    .get("master_profile", {})
                    .get("UID9622", {}),
                    "F6_rhythm": bc["F6_rhythm"].get("UID9622", {}),
                    "F7_punctuation": bc["F7_punctuation"].get("UID9622", {}),
                    "immovable_points": bc["immovable_points"].get("UID9622", []),
                },
            }

            # 建构其他人格
            for person in ["P02_BAOBAO", "P00_CHIEF_JUSTICE", "P05_DAODE_SAGE"]:
                if person in bc["F5_vocabulary"]:
                    profiles[person] = {
                        "name": bc["F5_vocabulary"][person].get("name"),
                        "role": bc["F5_vocabulary"][person].get("name"),
                        "type": "persona",
                        "status": "verified",
                        "features": {
                            "F5_vocabulary": bc["F5_vocabulary"].get(person, {}),
                            "F6_rhythm": bc["F6_rhythm"].get(person, {}),
                            "F7_punctuation": bc["F7_punctuation"].get(person, {}),
                        },
                    }

        output_file = self.generated_dir / "behavioral_profiles.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(profiles, f, ensure_ascii=False, indent=2)
        self._log("  → {output_file}")

    def generate_weight_color_mapping(self):
        """生成 weight_color_mapping.json"""
        self._log("\n【生成】weight_color_mapping.json")

        mapping = {
            "metadata": {
                "name": "龍魂權重·色彩映射統一配置表",
                "dna": self.config["metadata"]["dna"],
                "timestamp": datetime.now().isoformat(),
                "version": "{self.config['metadata']['versioning']['major']}.{self.config['metadata']['versioning']['minor']}",
                "status": "🟢 ACTIVE",
            },
            "five_color_system": self.config.get("five_color_audit", {}),
            "weight_factors_seven_dimensional": self.config.get("weight_formulas", {})
            .get("responsibility_coefficient_r", {})
            .get("factors", {}),
            "responsibility_coefficient_r_formula": self.config.get(
                "weight_formulas", {}
            ).get("responsibility_coefficient_r", {}),
            "three_talent_weights": self.config.get("weight_formulas", {}).get(
                "three_talent_system", {}
            ),
        }

        output_file = self.generated_dir / "weight_color_mapping.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
        self._log("  → {output_file}")

    def generate_multi_persona_definitions(self):
        """生成多人格定义 JSON"""
        self._log("\n【生成】multi_persona_definitions.json")

        personas = {
            "metadata": {
                "name": "龍魂15人格·完整定義",
                "dna": self.config["metadata"]["dna"],
                "timestamp": datetime.now().isoformat(),
                "total_personas": self.config["multi_persona_system"]["total_personas"],
            },
            "personas": self.config["multi_persona_system"]["personas"],
        }

        output_file = self.generated_dir / "multi_persona_definitions.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(personas, f, ensure_ascii=False, indent=2)
        self._log("  → {output_file}")

    def compute_integrity_hash(self) -> str:
        """计算配置完整性哈希"""
        config_str = json.dumps(self.config, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(config_str.encode()).hexdigest()[:16]

    def generate_startup_report(self):
        """生成启动报告"""
        self._log("\n【启动报告】")

        report = {
            "timestamp": datetime.now().isoformat(),
            "status": "🟢 SUCCESS",
            "files_generated": [
                "behavioral_profiles.json",
                "weight_color_mapping.json",
                "multi_persona_definitions.json",
                "startup_report.json",
            ],
            "integrity_hash": self.compute_integrity_hash(),
            "dna": self.config["metadata"]["dna"],
            "next_sync": "on-boot",
            "notes": "所有配置文件从 MASTER_CONFIG_v1.0.yaml 一致生成·无人工修改",
        }

        output_file = self.generated_dir / "startup_report.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        self._log("✓ 启动完成")
        self._log("  完整性哈希: {report['integrity_hash']}")
        self._log("  DNA: {report['dna']}")
        self._log("  生成文件数: {len(report['files_generated'])}")

        return report

    def run(self):
        """执行完整启动流程"""
        if not self.load_master_config():
            return False

        if not self.validate_config():
            self._log("⚠️  配置不完整，但继续启动...")

        self.generate_behavioral_profiles()
        self.generate_weight_color_mapping()
        self.generate_multi_persona_definitions()
        report = self.generate_startup_report()

        self._log("\n{'='*60}")
        self._log("启动完成 | 所有文件已生成到 ./generated/")
        self._log("{'='*60}\n")

        return True


def ensure_master_config_exists():
    """确保主干配置文件存在"""
    master_config_path = Path("MASTER_CONFIG_v1.0.yaml")
    if not master_config_path.exists():
        print("✗ 找不到主干配置文件: {master_config_path}")
        print("  请先创建 MASTER_CONFIG_v1.0.yaml")
        return False
    return True


if __name__ == "__main__":
    if not ensure_master_config_exists():
        exit(1)

    bootstrap = MasterConfigBootstrap()
    success = bootstrap.run()

    if success:
        print("\n✓ 系统启动成功·所有文件已同步")
        print("  你可以安全地使用 generated/ 目录下的文件")
        print("  或将其链接到项目根目录")
    else:
        print("\n✗ 启动失败·请检查配置")
        exit(1)
