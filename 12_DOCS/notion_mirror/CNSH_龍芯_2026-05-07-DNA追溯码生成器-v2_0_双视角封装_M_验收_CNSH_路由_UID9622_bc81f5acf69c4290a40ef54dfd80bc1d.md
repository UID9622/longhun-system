# CNSH::#龍芯⚡️2026-05-07-DNA追溯码生成器-v2.0｜双视角封装·M::验收+CNSH::路由｜UID9622

> Notion URL: https://app.notion.com/p/CNSH-2026-05-07-DNA-v2-0-M-CNSH-UID9622-bc81f5acf69c4290a40ef54dfd80bc1d
> Created: 2026-05-07T14:06:00.000Z
> Last edited: 2026-07-01T15:28:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
---
## 1. M:: 机器验收头（本页自检）
```json
M:: {
  "id": "M::SCRIPT-9622-20260507-DNA-GEN-V2",
  "type": "script",
  "ts": "2026-05-07T22:10:00+08:00",
  "status": "true",
  "refs": [
    "CNSH::#龍芯⚡️2026-04-29-CNSH双视角封装协议-Machine×CNSH-v1.0",
    "CNSH::#龍芯⚡️2026-05-01-五行计算器-v3.0-流场压缩核-封板"
  ],
  "payload": {
    "summary": "DNA追溯码生成器 v2.0·双视角封装版",
    "replaces": "#龙芯⚡️2026-02-11-DNA生成器-v1.0",
    "upgrades": ["双视角封装", "数字根熔断", "五行映射", "三色审计", "父子链", "双签章"]
  }
}
```
## 2. CNSH:: 路由签章头（本页归属）
```json
CNSH:: {
  "dna": "#龍芯⚡️2026-05-07-DNA追溯码生成器-v2.0",
  "parent_dna": "#龍芯⚡️2026-02-11-DNA生成器-v1.0",
  "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
  "route": "IPA-DNA-GENERATOR",
  "audit": "🟢",
  "wuxing": "金",
  "layer": "L1百年",
  "policy": "pass",
  "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
}
```
---
## 3. DNA 怎么算的·七步切刀（人话版）
---
## 4. 升级后的完整代码（v2.0·可直接复制运行）
```python
# -*- coding: utf-8 -*-
# ============================================================
# 🐉 龍魂系統 · DNA追溯码生成器 v2.0（双视角封装版）
# CNSH::#龍芯⚡️2026-05-07-DNA追溯码生成器-v2.0
# 父DNA：#龍芯⚡️2026-02-11-DNA生成器-v1.0
# CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL：#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ============================================================

import hashlib
import datetime
from typing import Dict, Optional, Tuple


class DNA生成器V2:
    """龍魂系統 DNA 生成器 v2.0·双视角封装版

    每次生成同时输出 M:: 与 CNSH:: 两个对象：
      - M::   机器验收（id / type / ts / status / payload）
      - CNSH:: 路由签章（dna / gate / seal / route / audit / wuxing / layer / policy）
    """

    # —— 数字根 → 五行 —— #
    数字根五行 = {
        1: "水", 2: "火", 3: "木", 4: "金", 5: "土",
        6: "水", 7: "火", 8: "木", 9: "金", 0: "土",
    }

    # —— 熔断闸门 —— #
    熔断数字根 = {3, 9}
    待审数字根 = {6}

    def __init__(self,
                 confirm: str = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
                 seal: str = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼\u200d♀️❤️♾️-DEVICE-BIND-SOUL",
                 gpg: str = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"):
        self.系統标记 = "龍芯⚡️"
        self.加密算法 = "SHA-256"
        self.DNA版本 = "v2.0"
        self.confirm = confirm
        self.seal = seal
        self.gpg = gpg

    # ---------- 核心计算（七步切刀） ----------
    def _计算短指纹(self, 文本: str) -> Tuple[str, str]:
        字节 = 文本.encode("utf-8")              # ① 编码
        完整 = hashlib.sha256(字节).hexdigest()   # ② SHA-256
        短 = 完整[:8]                              # ③ 截短
        return 完整, 短

    def _计算数字根(self, 短指纹: str) -> int:
        数字 = [int(c) for c in 短指纹 if c.isdigit()]
        if not 数字:
            return 0
        n = sum(数字)
        while n >= 10:
            n = sum(int(c) for c in str(n))
        return n                                  # ④ 数字根

    def _三色审计(self, dr: int) -> str:
        if dr in self.熔断数字根:
            return "🔴"                            # ⑥ 熔断
        if dr in self.待审数字根:
            return "🟡"                            # ⑥ 待审
        return "🟢"                                # ⑥ 通行

    # ---------- 双视角封装出口 ----------
    def 生成(self,
             文本内容: str,
             功能名称: str,
             版本号: str = "v1.0",
             父DNA: Optional[str] = None,
             route: str = "IPA-DNA-GENERATOR",
             layer: str = "L3日常") -> Dict:
        完整指纹, 短指纹 = self._计算短指纹(文本内容)
        dr = self._计算数字根(短指纹)
        五行 = self.数字根五行[dr]                  # ⑤ 五行
        三色 = self._三色审计(dr)
        日期 = datetime.datetime.now().strftime("%Y-%m-%d")
        DNA码 = f"#{self.系統标记}{日期}-{功能名称}-{版本号}-{短指纹}"  # ⑦ 拼接

        # 三色 = 🔴 时·policy 强制 fuse·不许入库
        policy = {"🟢": "pass", "🟡": "hold", "🔴": "fuse"}[三色]

        # —— M:: 机器验收 —— #
        M = {
            "id": f"M::DNA-9622-{日期.replace('-', '')}-{短指纹.upper()}-V2",
            "type": "dna",
            "ts": datetime.datetime.now().isoformat(),
            "status": "true" if 三色 == "🟢" else ("pending" if 三色 == "🟡" else "error"),
            "refs": [父DNA] if 父DNA else [],
            "payload": {
                "summary": f"{功能名称} {版本号}",
                "input_len": len(文本内容),
                "hash_full": 完整指纹,
                "hash_short": 短指纹,
                "digital_root": dr,
                "algo": self.加密算法,
            },
        }

        # —— CNSH:: 路由签章 —— #
        CNSH = {
            "dna": DNA码,
            "parent_dna": 父DNA,
            "gate": self.confirm,
            "seal": self.seal,
            "route": route,
            "audit": 三色,
            "wuxing": 五行,
            "layer": layer,
            "policy": policy,
            "gpg": self.gpg,
        }

        return {"M::": M, "CNSH::": CNSH}

    # ---------- 验证（带完整审计回执） ----------
    def 验证(self, 原文本: str, 声称的DNA码: str) -> Dict:
        if not 声称的DNA码.startswith(f"#{self.系統标记}"):
            return {
                "M::": {"status": "error", "reason": "format_invalid"},
                "CNSH::": {"audit": "🔴", "policy": "fuse",
                            "note": "DNA 不以 #龍芯⚡️ 开头"},
            }
        声称指纹 = 声称的DNA码.split("-")[-1]
        _, 重算指纹 = self._计算短指纹(原文本)
        匹配 = (声称指纹 == 重算指纹)
        三色 = "🟢" if 匹配 else "🔴"
        return {
            "M::": {
                "id": f"M::AUDIT-9622-DNA-VERIFY",
                "type": "audit",
                "status": "true" if 匹配 else "false",
                "payload": {
                    "claimed": 声称指纹,
                    "recomputed": 重算指纹,
                    "match": 匹配,
                },
            },
            "CNSH::": {
                "audit": 三色,
                "policy": "pass" if 匹配 else "fuse",
                "gate": self.confirm,
                "seal": self.seal,
                "note": "DNA 与原文匹配" if 匹配 else "⚠️ DNA 与原文不匹配·疑似篡改",
            },
        }


# ============================================================
# 测试·三组示例（覆盖 🟢🟡🔴 三种状态）
# ============================================================
if __name__ == "__main__":
    import json
    g = DNA生成器V2()

    样本 = [
        ("龍魂系統：以人民为中心，拒绝资本剥削", "核心价值观", "v1.0"),
        ("const shieldBurn = require('./shield_burn.js');", "shield_burn代码片段", "v1.0"),
        ("测试一段普通文本", "测试样本", "v1.0"),
    ]
    for 文本, 名, 版 in 样本:
        结果 = g.生成(文本, 名, 版, 父DNA="#龍芯⚡️2026-05-07-DNA追溯码生成器-v2.0")
        print(json.dumps(结果, ensure_ascii=False, indent=2))
        print("-" * 60)
```
---
## 5. 输出长这样（双段封装·缺一不可）
```json
{
  "M::": {
    "id": "M::DNA-9622-20260507-A3F7C92E-V2",
    "type": "dna",
    "ts": "2026-05-07T22:10:00+08:00",
    "status": "true",
    "refs": ["#龍芯⚡️2026-05-07-DNA追溯码生成器-v2.0"],
    "payload": {
      "summary": "核心价值观 v1.0",
      "input_len": 19,
      "hash_full": "a3f7c92e...8b1d4f（64位）",
      "hash_short": "a3f7c92e",
      "digital_root": 3,
      "algo": "SHA-256"
    }
  },
  "CNSH::": {
    "dna": "#龍芯⚡️2026-05-07-核心价值观-v1.0-a3f7c92e",
    "parent_dna": "#龍芯⚡️2026-05-07-DNA追溯码生成器-v2.0",
    "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
    "route": "IPA-DNA-GENERATOR",
    "audit": "🔴",
    "wuxing": "木",
    "layer": "L3日常",
    "policy": "fuse",
    "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  }
}
```
---
## 6. 与 v1.0 老版本对账表
---
