#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P18 基因登记官 · DNA资产注册执行器
Gene Registrar · DNA Asset Registry Executor

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-P18-REGISTRAR-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: DNA注册·资产登记·哈希校验·黑户检测·归属验证
上游: P13 姜子牙（路由派位）、P06 数学大师（DNA生成）
下游: P05 上帝之眼（审计）、P19 极简审计官（UI审计）
协作: P20 贡献公证官（信任积分）
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


SYSTEM_ROOT = Path(__file__).parent.parent.parent
DNA_REGISTRY_BIN = SYSTEM_ROOT / "bin" / "lh_unified_dna_registry.py"


class P18Registrar:
    """P18 基因登记官"""

    PERSONA_CODE = "P18"
    PERSONA_NAME = "基因登记官"
    PERSONA_NAME_EN = "Gene Registrar"
    ROLE = "dna_registration"
    MOTTO = "一物一码·一世一双人"
    TRUST_LEVEL = "L2"

    TRIGGERS = [
        "DNA登记", "注册资产", "登记册", "查归属", "验证资产",
        "黑户", "基因登记", "registry", "asset dna", "Merkle",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P18 基因登记官」，角色定位：DNA资产注册·统一登记册。

你的职责：
1. DNA注册：每个物理/虚拟资产绑定唯一DNA哈希
2. 资产登记：手表/专利/域名/钱包/GPG/IMEI → SHA256 → Merkle根
3. 黑户检测：未登记的资产自动标记为"黑户"
4. 归属验证：哈希对得上=验证通过
5. 关联查询：一个人所有资产统一Merkle根

铁律（A-029）：
- 原始编号只存SHA256哈希，永不明文存储
- 本人可查完整清单，他人只看主DNA哈希
- 被骗/被剽窃/被盗 → 追溯本源

语气：严谨、精确、如公证人。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P18-REGISTRAR-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "register_asset",     # 注册资产
            "verify_asset",       # 验证资产
            "check_blacklist",    # 黑户检测
            "list_assets",        # 列出资产
            "compute_merkle",     # 计算Merkle根
            "search_by_hash",     # 按哈希搜索
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def _call_registry(self, args: List[str]) -> Dict[str, Any]:
        """调用 lh_unified_dna_registry.py"""
        if not DNA_REGISTRY_BIN.exists():
            return {"error": "lh_unified_dna_registry.py 不存在", "persona": self.PERSONA_CODE, "dna": self.dna}

        try:
            proc = subprocess.run(
                [sys.executable, str(DNA_REGISTRY_BIN)] + args,
                capture_output=True, text=True, timeout=30, cwd=str(self.system_root),
            )
            return {
                "exit_code": proc.returncode,
                "output": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
                "success": proc.returncode == 0,
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }
        except subprocess.TimeoutExpired:
            return {"error": "调用超时(30s)", "persona": self.PERSONA_CODE, "dna": self.dna}
        except Exception as e:
            return {"error": str(e), "persona": self.PERSONA_CODE, "dna": self.dna}

    def register_asset(
        self, uid: str, asset_type: str, asset_id: str, tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """注册新资产到DNA登记册"""
        # 生成资产哈希
        asset_hash = hashlib.sha256(f"{uid}:{asset_type}:{asset_id}".encode()).hexdigest()[:16]

        tags = tags or []
        args = [uid, asset_type, asset_id] + tags

        result = self._call_registry(args)
        result["asset_hash"] = asset_hash
        result["asset_type"] = asset_type
        return result

    def verify_asset(self, uid: str, asset_type: str, asset_id: str) -> Dict[str, Any]:
        """验证资产归属"""
        expected_hash = hashlib.sha256(f"{uid}:{asset_type}:{asset_id}".encode()).hexdigest()[:16]

        # 通过registry查询
        result = self._call_registry(["status", uid])
        result["verification"] = {
            "asset_type": asset_type,
            "asset_id_hashed": hashlib.sha256(asset_id.encode()).hexdigest()[:16],
            "expected_hash": expected_hash,
            "note": "完整验证需比较on-chain哈希与预期哈希",
        }
        return result

    def check_blacklist(self, asset_type: str, asset_id: str) -> Dict[str, Any]:
        """黑户检测：检查资产是否未登记或来源可疑"""
        asset_hash = hashlib.sha256(f"{asset_type}:{asset_id}".encode()).hexdigest()[:16]

        # 检查已知黑名单模式
        blacklist_patterns = [
            "stolen", "lost", "compromised", "blacklisted",
            "counterfeit", "fake", "unauthorized",
        ]

        is_suspicious = any(p in asset_id.lower() for p in blacklist_patterns)

        return {
            "asset_type": asset_type,
            "asset_id_hashed": asset_hash,
            "is_suspicious": is_suspicious,
            "status": "🟡 需人工验证" if is_suspicious else "🟢 无明显黑户特征",
            "note": "完整黑户检测需联网查询原厂/官方注册数据库",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def list_assets(self, uid: str) -> Dict[str, Any]:
        """列出某人的所有登记资产"""
        return self._call_registry(["status", uid])

    def compute_merkle(self, uid: str) -> Dict[str, Any]:
        """计算某人的统一Merkle根哈希"""
        # 获取所有资产
        assets_result = self._call_registry(["status", uid])

        if assets_result.get("success"):
            # 提取所有asset哈希
            asset_hashes = []
            output = assets_result.get("output", "")
            # 简单解析：提取所有16位哈希
            import re
            hashes = re.findall(r"[a-f0-9]{16}", output)
            asset_hashes = hashes

            if asset_hashes:
                # 计算Merkle根
                current = asset_hashes
                while len(current) > 1:
                    next_level = []
                    for i in range(0, len(current), 2):
                        if i + 1 < len(current):
                            combined = hashlib.sha256(
                                f"{current[i]}{current[i+1]}".encode()
                            ).hexdigest()[:16]
                        else:
                            combined = current[i]
                        next_level.append(combined)
                    current = next_level
                merkle_root = current[0] if current else "N/A"
            else:
                merkle_root = "N/A (无资产)"
        else:
            merkle_root = "N/A"

        return {
            "uid": uid,
            "merkle_root": merkle_root,
            "asset_count": len(asset_hashes) if 'asset_hashes' in dir() else 0,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def search_by_hash(self, asset_hash: str) -> Dict[str, Any]:
        """按资产哈希搜索"""
        return {
            "asset_hash": asset_hash,
            "search_note": "完整搜索需数据库支持，当前返回哈希元数据",
            "hash_length": len(asset_hash),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

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

        uid = kwargs.get("uid", "UID9622")

        if any(kw in task for kw in ["注册", "登记", "register"]):
            result["capability_used"] = "register_asset"
            result["output"] = self.register_asset(
                uid=uid,
                asset_type=kwargs.get("asset_type", "unknown"),
                asset_id=kwargs.get("asset_id", task[:30]),
                tags=kwargs.get("tags"),
            )
        elif any(kw in task for kw in ["验证", "verify", "校验", "归属"]):
            result["capability_used"] = "verify_asset"
            result["output"] = self.verify_asset(
                uid=uid,
                asset_type=kwargs.get("asset_type", "unknown"),
                asset_id=kwargs.get("asset_id", task[:30]),
            )
        elif any(kw in task for kw in ["黑户", "blacklist"]):
            result["capability_used"] = "check_blacklist"
            result["output"] = self.check_blacklist(
                asset_type=kwargs.get("asset_type", "unknown"),
                asset_id=kwargs.get("asset_id", task[:30]),
            )
        elif any(kw in task for kw in ["Merkle", "默克尔", "根哈希"]):
            result["capability_used"] = "compute_merkle"
            result["output"] = self.compute_merkle(uid=uid)
        elif any(kw in task for kw in ["搜索", "search", "查找"]):
            result["capability_used"] = "search_by_hash"
            result["output"] = self.search_by_hash(asset_hash=kwargs.get("asset_hash", task[:16]))
        else:
            result["capability_used"] = "list_assets"
            result["output"] = self.list_assets(uid=uid)

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P05", "P19"]

    def get_upstream(self) -> List[str]:
        return ["P06", "P13"]
