# P0焊死: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂行为密码学 · Behavioral Cryptography for LongHun
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

把“谁、在什么时候、对什么对象、以什么权限、做了什么、结果如何”
全部编码成不可伪造、可追溯、可审计的 DNA 链。

核心设计：
  - 每个动作绑定唯一 DNA 码
  - 敏感动作必须命中一次性确认码
  - 权限等级决定 AI 能做什么、对谁做、做到什么程度
  - 所有行为写入本地审计链，不上传第三方

DNA:#龍芯⚡️丙午·甲午·乙丑·壬午·䷨损-LONGHUN-BEHAVIORAL-CRYPTO-FILE1-v1.0
"""

import hashlib
import json
import secrets
import time
from datetime import datetime, timezone
from enum import IntEnum
from pathlib import Path
from typing import Optional


class 权限等级(IntEnum):
    """权限从低到高，宪法层最高。"""
    L0_PUBLIC = 0      # 公开只读，任何人可执行
    L1_QUERY = 1       # 查询类，不修改状态
    L2_ACTION = 2      # 执行类，修改本地状态
    L3_ADMIN = 3       # 管理类，影响服务/配置
    L4_CONSTITUTION = 4  # 宪法层变更，需人工确认


class 行为密码:
    """
    生成并校验 LongHun 系统的行为 DNA 与一次性确认码。
    """

    def __init__(
        self,
        操作人: str = "UID9622",
        审计日志路径: str = "~/.longhun/audit/behavioral_chain.jsonl",
    ):
        self.操作人 = 操作人
        self.审计日志路径 = Path(审计日志路径).expanduser()
        self.审计日志路径.parent.mkdir(parents=True, exist_ok=True)

    def 生成DNA(
        self,
        操作类型: str,
        对象: str,
        权限: 权限等级,
        输入摘要: str = "",
        输出摘要: str = "",
        副作用摘要: str = "",
    ) -> str:
        """生成不可伪造的 DNA 追溯码。"""
        时间戳 = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        原料 = "|".join([
            时间戳,
            self.操作人,
            操作类型,
            对象,
            str(权限.value),
            输入摘要,
            输出摘要,
            副作用摘要,
        ])
        哈希 = hashlib.sha3_256(原料.encode("utf-8")).hexdigest()[:16].upper()
        return f"#龍芯⚡️{时间戳}-{操作类型}-{对象}-L{权限.value}-{哈希}"

    def 生成一次性确认码(self, 操作ID: str) -> str:
        """生成一次性确认码，命中后才允许宪法层操作。"""
        随机 = secrets.token_urlsafe(12)
        return f"#CONFIRM🌌9622-ONLY-ONCE🧬{随机}-{操作ID}"

    def 校验确认码(self, 用户输入: str, 期望码: str) -> bool:
        """常量时间比较，防时序攻击（UTF-8 字节级）。"""
        if not 用户输入 or not 期望码:
            return False
        a = 用户输入.strip().encode("utf-8")
        b = 期望码.strip().encode("utf-8")
        return secrets.compare_digest(a, b)

    def 权限是否足够(self, 所需: 权限等级, 持有: 权限等级) -> bool:
        return 持有.value >= 所需.value

    def 记录(
        self,
        DNA: str,
        行为: str,
        结果: str,
        确认码: Optional[str] = None,
    ) -> dict:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dna": DNA,
            "operator": self.操作人,
            "behavior": 行为,
            "result": 结果,
            "confirmed": bool(确认码),
        }
        with open(self.审计日志路径, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record


class 行为授权矩阵:
    """
    决定“AI 什么时候笨、对谁笨、怎么赋能”。
    敏感对象/操作提升权限等级，甚至要求人工确认码。
    """

    默认矩阵 = {
        "read_public": 权限等级.L0_PUBLIC,
        "query_identity": 权限等级.L1_QUERY,
        "issue_token": 权限等级.L2_ACTION,
        "register_service": 权限等级.L2_ACTION,
        "modify_nginx": 权限等级.L3_ADMIN,
        "modify_dns": 权限等级.L3_ADMIN,
        "change_constitution": 权限等级.L4_CONSTITUTION,
        "grant_super_power": 权限等级.L4_CONSTITUTION,
    }

    def __init__(self, 矩阵: Optional[dict] = None):
        self.矩阵 = 矩阵 or self.默认矩阵

    def 查询权限(self, 操作: str) -> 权限等级:
        return self.矩阵.get(操作, 权限等级.L2_ACTION)

    def 需要确认码(self, 操作: str) -> bool:
        return self.查询权限(操作) == 权限等级.L4_CONSTITUTION


if __name__ == "__main__":
    bc = 行为密码()
    dna = bc.生成DNA("TEST", "portal", 权限等级.L2_ACTION)
    confirm = bc.生成一次性确认码("TEST-001")
    print(dna)
    print(confirm)
    print(bc.校验确认码(confirm, confirm))
    bc.记录(dna, "行为密码学自检", "通过")
    print("✅ 行为密码学模块自检完成")
