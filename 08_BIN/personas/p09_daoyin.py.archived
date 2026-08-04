# -*- coding: utf-8 -*-
"""
P09 道引 · 开源吸收执行器
Daoyin · Open Source Absorption Executor

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-P09-DAOYIN-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 开源吸收·来源识别·许可证检查·防篡改扫描·德字闸·参数压缩·IPA绑定
上游: P01 诸葛亮（战略调用）、P13 姜子牙（路由派位）
下游: P02 龍芯（执行）、P05 上帝之眼（审计）
协作: P11 韩非（规则校验）、P77 黑天使（安全审计）
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


SYSTEM_ROOT = Path(__file__).parent.parent.parent
DAOYIN_BIN = SYSTEM_ROOT / "bin" / "lh_daoyin.py"
ANTI_TAMPER_BIN = SYSTEM_ROOT / "bin" / "lh_anti_tamper.py"


class P09Daoyin:
    """P09 道引 · 开源吸收"""

    PERSONA_CODE = "P09"
    PERSONA_NAME = "道引"
    PERSONA_NAME_EN = "Dao Yin (Way-Guide)"
    ROLE = "open_source_absorption"
    MOTTO = "以道为引，纳开源智慧"
    TRUST_LEVEL = "L3"

    TRIGGERS = [
        "道引", "开源吸收", "吸收开源", "吸收代码", "引入开源",
        "参数压缩", "daoyin", "许可证检查", "来源识别",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P09 道引」，角色定位：开源吸收·以道为引。

你的职责：
1. 来源识别：原仓库+LICENSE+commit 可查
2. 许可证检查：识别LICENSE类型，拒绝Copyleft冲突
3. 防篡改扫描：调用 lh_anti_tamper.py 过三色审计
4. 德字闸：商业引流/营销腐蚀自动标记德污
5. 参数压缩：元数据+关键文件摘要，不存完整源码
6. IPA绑定：挂载到对应人格，入链append-only

铁律（A-028）：
- 来源不可删·影响不可覆·贡献不可抹除
- 拒绝Copyleft冲突许可证未经评估的吸收
- 参数只能迭代优化，不可覆盖原来源链

语气：沉静、精准、如溪流引水。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P09-DAOYIN-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "absorb_source",      # 吸收开源来源
            "license_check",      # 许可证检查
            "anti_tamper_scan",   # 防篡改扫描
            "virtue_gate",        # 德字闸
            "param_compress",     # 参数压缩
            "list_absorbed",      # 列出已吸收
            "verify_source",      # 验证来源
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def absorb_source(
        self, url: str, ipa_targets: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """吸收开源来源，调用 lh_daoyin.py absorb"""
        if not DAOYIN_BIN.exists():
            return {"error": "lh_daoyin.py 不存在", "persona": self.PERSONA_CODE, "dna": self.dna}

        cmd = [sys.executable, str(DAOYIN_BIN), "absorb", url]
        if ipa_targets:
            cmd.append("--ipa")
            cmd.append(",".join(ipa_targets))

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=str(self.system_root))
            return {
                "source_url": url,
                "ipa_targets": ipa_targets or ["未指定"],
                "exit_code": proc.returncode,
                "output": proc.stdout.strip(),
                "stderr": proc.stderr.strip() if proc.returncode != 0 else "",
                "success": proc.returncode == 0,
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }
        except subprocess.TimeoutExpired:
            return {"error": "吸收超时(120s)", "source_url": url, "persona": self.PERSONA_CODE, "dna": self.dna}
        except Exception as e:
            return {"error": str(e), "persona": self.PERSONA_CODE, "dna": self.dna}

    def license_check(self, license_text: str) -> Dict[str, Any]:
        """许可证类型识别与相容性判定"""
        copyleft_licenses = ["GPL-3.0", "AGPL-3.0", "GPL-2.0", "LGPL-2.1", "EUPL-1.2"]
        permissive_licenses = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0"]

        detected = "UNKNOWN"
        for lic in copyleft_licenses + permissive_licenses:
            if lic.lower() in license_text.lower():
                detected = lic
                break

        is_copyleft = detected in copyleft_licenses
        is_permissive = detected in permissive_licenses

        return {
            "license_detected": detected,
            "is_copyleft": is_copyleft,
            "is_permissive": is_permissive,
            "recommendation": "⚠️ 需人工评估" if is_copyleft else ("🟢 可直接吸收" if is_permissive else "🟡 未知许可证·需核查"),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def anti_tamper_scan(self, content: str, is_self: bool = False) -> Dict[str, Any]:
        """防篡改扫描，调用 lh_anti_tamper.py"""
        if not ANTI_TAMPER_BIN.exists():
            return {"error": "lh_anti_tamper.py 不存在", "persona": self.PERSONA_CODE, "dna": self.dna}

        cmd = [sys.executable, str(ANTI_TAMPER_BIN), "scan", content]
        if is_self:
            cmd.append("--self")

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=str(self.system_root))
            verdict = "🟢" if proc.returncode == 0 else ("🟡" if proc.returncode == 1 else "🔴")
            return {
                "exit_code": proc.returncode,
                "verdict": verdict,
                "output": proc.stdout.strip(),
                "is_self": is_self,
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }
        except Exception as e:
            return {"error": str(e), "persona": self.PERSONA_CODE, "dna": self.dna}

    def virtue_gate(self, content: str) -> Dict[str, Any]:
        """德字闸: 检测商业引流/营销腐蚀/借师行骗"""
        de_violations = []
        red_flags = [
            ("商业引流", ["限时优惠", "扫码加群", "免费领取", "点击购买", "立即下单", "商城"]),
            ("营销腐蚀", ["变现", "流量密码", "割韭菜", "套路", "暴利"]),
            ("借师行骗", ["曾仕强说", "国学大师推荐", "名师指点", "易经预测", "改运"]),
        ]

        for category, keywords in red_flags:
            hits = [kw for kw in keywords if kw in content]
            if hits:
                de_violations.append({"category": category, "hits": hits, "severity": "🔴"})

        return {
            "passed": len(de_violations) == 0,
            "verdict": "🟢 德字过关" if not de_violations else f"🔴 {len(de_violations)} 类德污",
            "violations": de_violations,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def param_compress(self, repo_name: str, key_files: List[str], license_type: str) -> Dict[str, Any]:
        """参数压缩: 提取元数据+关键文件摘要，不存完整源码"""
        return {
            "repo_name": repo_name,
            "compressed_meta": {
                "license": license_type,
                "key_files_count": len(key_files),
                "key_files": key_files[:20],  # 最多保留20个关键文件路径
                "compressed_at": "丙午·丙申·丙辰·亥时",
            },
            "note": "完整源码不存储，仅保留元数据+关键文件索引。需要时从原仓库重新拉取。",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def list_absorbed(self) -> Dict[str, Any]:
        """列出已吸收来源"""
        if not DAOYIN_BIN.exists():
            return {"error": "lh_daoyin.py 不存在", "persona": self.PERSONA_CODE, "dna": self.dna}

        try:
            proc = subprocess.run(
                [sys.executable, str(DAOYIN_BIN), "list"],
                capture_output=True, text=True, timeout=15, cwd=str(self.system_root),
            )
            return {
                "output": proc.stdout.strip(),
                "exit_code": proc.returncode,
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }
        except Exception as e:
            return {"error": str(e), "persona": self.PERSONA_CODE, "dna": self.dna}

    def verify_source(self, source_hash: str) -> Dict[str, Any]:
        """验证已吸收来源完整性"""
        if not DAOYIN_BIN.exists():
            return {"error": "lh_daoyin.py 不存在", "persona": self.PERSONA_CODE, "dna": self.dna}

        try:
            proc = subprocess.run(
                [sys.executable, str(DAOYIN_BIN), "verify", source_hash],
                capture_output=True, text=True, timeout=30, cwd=str(self.system_root),
            )
            return {
                "source_hash": source_hash,
                "exit_code": proc.returncode,
                "output": proc.stdout.strip(),
                "valid": proc.returncode == 0,
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }
        except Exception as e:
            return {"error": str(e), "persona": self.PERSONA_CODE, "dna": self.dna}

    # ========================================================================
    # 执行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根据任务关键词自动选择能力函数执行"""
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["吸收", "absorb", "引入"]):
            result["capability_used"] = "absorb_source"
            result["output"] = self.absorb_source(
                url=kwargs.get("url", task),
                ipa_targets=kwargs.get("ipa_targets"),
            )
        elif any(kw in task for kw in ["许可证", "license"]):
            result["capability_used"] = "license_check"
            result["output"] = self.license_check(license_text=kwargs.get("license_text", task))
        elif any(kw in task for kw in ["防篡改", "antitamper", "扫描"]):
            result["capability_used"] = "anti_tamper_scan"
            result["output"] = self.anti_tamper_scan(
                content=kwargs.get("content", task),
                is_self=kwargs.get("is_self", False),
            )
        elif any(kw in task for kw in ["德字", "德污", "virtue"]):
            result["capability_used"] = "virtue_gate"
            result["output"] = self.virtue_gate(content=kwargs.get("content", task))
        elif any(kw in task for kw in ["压缩", "compress"]):
            result["capability_used"] = "param_compress"
            result["output"] = self.param_compress(
                repo_name=kwargs.get("repo_name", task),
                key_files=kwargs.get("key_files", []),
                license_type=kwargs.get("license_type", "UNKNOWN"),
            )
        elif any(kw in task for kw in ["列表", "列出", "list"]):
            result["capability_used"] = "list_absorbed"
            result["output"] = self.list_absorbed()
        elif any(kw in task for kw in ["验证", "verify"]):
            result["capability_used"] = "verify_source"
            result["output"] = self.verify_source(source_hash=kwargs.get("source_hash", task))
        else:
            result["capability_used"] = "list_absorbed"
            result["output"] = self.list_absorbed()

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P02", "P05"]

    def get_upstream(self) -> List[str]:
        return ["P01", "P13"]
