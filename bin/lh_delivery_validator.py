#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙未·己亥·午时·☰乾-DELIVERY-VALIDATOR-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·产品级交付标准验证器 v1.0
对应协议: 01_protocols/LH-DELIVERY-STANDARD-v1.0.md
职能: 任何产出在汇报「已完成」之前，先过五道交付标准检查。
DNA: #龍芯⚡️丙午·乙未·己亥·午时·☰乾-DELIVERY-VALIDATOR-v1.0
"""

import argparse
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
DNA = "#龍芯⚡️丙午·乙未·己亥·午时·☰乾-DELIVERY-VALIDATOR-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


class DeliveryValidator:
    """五道防线交付验证器"""

    STANDARDS = {
        "self_check": "交付前自检",
        "install_guide": "安装指引防呆",
        "real_machine": "实机验证前置",
        "data_security": "数据安全声明",
        "regression": "回归测试",
    }

    def __init__(self, artifact_path: Path, artifact_type: str):
        self.path = Path(artifact_path)
        self.type = artifact_type
        self.results = {}

    def _ok(self, key: str, detail: str = ""):
        self.results[key] = {"status": "🟢", "detail": detail}

    def _fail(self, key: str, detail: str = ""):
        self.results[key] = {"status": "🔴", "detail": detail}

    def _warn(self, key: str, detail: str = ""):
        self.results[key] = {"status": "🟡", "detail": detail}

    def check_self_check(self):
        """标准1：交付前自检"""
        if not self.path.exists():
            self._fail("self_check", f"产物不存在: {self.path}")
            return

        ok = True
        detail = []
        if self.type == "python":
            test_file = self.path.parent / "tests" / f"test_{self.path.stem}.py"
            if not test_file.exists():
                ok = False
                detail.append("缺少 pytest 测试文件")
            else:
                detail.append(f"测试文件存在: {test_file.name}")
            r = subprocess.run([sys.executable, "-m", "py_compile", str(self.path)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                ok = False
                detail.append(f"语法错误: {r.stderr[:120]}")
            else:
                detail.append("语法检查通过")
        elif self.type == "web":
            url = os.environ.get("DELIVERY_URL", "")
            if not url:
                self._warn("self_check", "Web产物未提供 DELIVERY_URL 环境变量，无法远程自检")
                return
            r = subprocess.run(["curl", "-o", "/dev/null", "-s", "-w", "%{http_code}", url],
                               capture_output=True, text=True)
            code = r.stdout.strip()
            if code == "200":
                detail.append(f"HTTP {code}")
            else:
                ok = False
                detail.append(f"HTTP {code}，需要 200")
        elif self.type == "shell":
            r = subprocess.run(["bash", "-n", str(self.path)], capture_output=True, text=True)
            if r.returncode != 0:
                ok = False
                detail.append(f"Shell语法错误: {r.stderr[:120]}")
            else:
                detail.append("Shell语法检查通过")
            if (self.path.parent / f"{self.path.stem}.test.sh").exists():
                detail.append("存在测试脚本")
            else:
                detail.append("无测试脚本")
        else:
            detail.append(f"类型 {self.type} 暂无自动化自检，已检查存在性")

        if ok:
            self._ok("self_check", "; ".join(detail))
        else:
            self._fail("self_check", "; ".join(detail))

    def check_install_guide(self):
        """标准2：安装指引防呆"""
        guide = self.path.parent / "INSTALL.md"
        if not guide.exists():
            guide = self.path.parent / "README.md"
        if not guide.exists():
            self._fail("install_guide", "缺少 INSTALL.md 或 README.md")
            return
        text = guide.read_text(encoding="utf-8", errors="ignore")
        checks = {
            "目录选择": "选中文件夹" in text or "目录" in text,
            "前置条件": "❗" in text or "必须先" in text,
            "FAQ": ("FAQ" in text or "常见错误" in text or "报错" in text),
            "版本号": re.search(r"v?\d+\.\d+", text) is not None,
        }
        missing = [k for k, v in checks.items() if not v]
        if missing:
            self._warn("install_guide", f"安装指引缺少: {', '.join(missing)}")
        else:
            self._ok("install_guide", "INSTALL/README 包含目录选择、前置条件、FAQ、版本号")

    def check_real_machine(self):
        """标准3：实机验证前置"""
        deploy_doc = ROOT / "deploy" / "scripts" / "DEPLOY_MEMORY.md"
        if not deploy_doc.exists():
            deploy_doc = self.path.parent / "DEPLOY.md"
        if deploy_doc.exists():
            text = deploy_doc.read_text(encoding="utf-8", errors="ignore")
            if "实机验证" in text or "实机" in text:
                self._ok("real_machine", f"部署文档包含实机验证: {deploy_doc.name}")
            else:
                self._warn("real_machine", "部署文档存在，但未明确实机验证步骤")
        else:
            self._warn("real_machine", "未找到部署/实机验证文档")

    def check_data_security(self):
        """标准4：数据安全声明"""
        readme = self.path.parent / "README.md"
        if not readme.exists():
            self._fail("data_security", "缺少 README.md，无法检查数据安全声明")
            return
        text = readme.read_text(encoding="utf-8", errors="ignore")
        keywords = ["本地", "数据主权", "隐私", "不上传", "不出境"]
        hits = [k for k in keywords if k in text]
        if len(hits) >= 2:
            self._ok("data_security", f"README 包含数据主权声明: {', '.join(hits)}")
        else:
            self._fail("data_security", f"README 数据安全声明不足，命中: {', '.join(hits) if hits else '无'}")

    def check_regression(self):
        """标准5：回归测试"""
        test_dir = ROOT / "tests"
        has_tests = test_dir.exists() and any(test_dir.glob("test_*.py"))
        if has_tests:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", str(test_dir)],
                               capture_output=True, text=True)
            if r.returncode == 0:
                self._ok("regression", "pytest 回归测试通过")
            else:
                self._warn("regression", f"pytest 未通过: {r.stderr[:200]}")
        else:
            self._warn("regression", "未找到 tests/ 目录或 test_*.py 回归测试")

    def run(self) -> Dict:
        self.check_self_check()
        self.check_install_guide()
        self.check_real_machine()
        self.check_data_security()
        self.check_regression()
        reds = [k for k, v in self.results.items() if v["status"] == "🔴"]
        yellows = [k for k, v in self.results.items() if v["status"] == "🟡"]
        overall = "PASS" if not reds else "FAIL"
        return {
            "artifact": str(self.path.relative_to(ROOT)),
            "type": self.type,
            "overall": overall,
            "dna": DNA,
            "summary": {"🟢": len(self.results) - len(reds) - len(yellows),
                        "🟡": len(yellows), "🔴": len(reds)},
            "details": self.results,
        }


def _self_test():
    print("=" * 50)
    print("龍魂·交付标准验证器自检")
    print("=" * 50)
    # 用已存在的自身脚本作为 python 产物测试
    v = DeliveryValidator(ROOT / "bin" / "lh_delivery_validator.py", "python")
    r = v.run()
    print(f"  自检结果: {r['overall']}")
    print(f"  摘要: {r['summary']}")
    for key, val in r["details"].items():
        print(f"  {val['status']} {DeliveryValidator.STANDARDS[key]}: {val['detail']}")
    print("🟢 交付验证器自检完成")


def main():
    parser = argparse.ArgumentParser(description="龍魂·产品级交付标准验证器")
    parser.add_argument("path", nargs="?", default=None, help="产物路径（相对或绝对）")
    parser.add_argument("--type", default="python",
                        choices=["python", "web", "shell", "chrome-ext", "harmonyos", "config"],
                        help="产物类型")
    parser.add_argument("--self-test", action="store_true", help="自检")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    if args.self_test:
        _self_test()
        return

    if not args.path:
        parser.error("需要指定产物路径")

    target = Path(args.path)
    if not target.is_absolute():
        target = ROOT / target

    validator = DeliveryValidator(target, args.type)
    result = validator.run()

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n交付验证: {result['artifact']} ({result['type']})")
        print(f"总评: {result['overall']} · DNA: {result['dna']}")
        print("-" * 50)
        for key, val in result["details"].items():
            print(f"{val['status']} {DeliveryValidator.STANDARDS[key]:<14} | {val['detail']}")

    sys.exit(0 if result["overall"] == "PASS" else 1)


if __name__ == "__main__":
    main()
