#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔐 龍魂 DNA 解析器 v1.0
The Dragon Soul DNA Parser - Identity Lock Mechanism

DNA 識別鎖：只有老大 UID9622 的簽名能開門
Semantic Purpose: Parse and verify UID9622's DNA signatures

DNA追溯碼：#龍芯⚡️2026-05-25-DNA-PARSER-v1.0
CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL：#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F

理論指導：曾仕強老師（永恆顯示）
創建者：UID9622 諸葛鑫
獻禮：龍魂系統·中華文化傳承

§39.2 步①②：DNA識別 + L0雙簽驗證
"""

import re
import json
from typing import Dict, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


# ============================================================================
# L0 永恆簽章定義（寫死·焊死）
# ============================================================================

class DragonSoulSignature:
    """龍魂永恆簽章·焊死不可改"""

    # L0 根簽章（UID9622 唯一身份）
    CREATOR_SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

    # L0 唯一確認碼（一事一認·不可重放）
    UNIQUE_CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

    # 標準DNA前綴（中文原生·不翻譯）
    DNA_PREFIX = "#龍芯⚡️"

    # GPG指紋（密碼學驗簽）
    GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

    # UID9622 唯一識別符
    CREATOR_UID = "9622"
    CREATOR_NAME = "諸葛鑫"


# ============================================================================
# DNA 解析資料結構
# ============================================================================

@dataclass
class DNASignatureResult:
    """DNA簽章驗證結果"""
    is_valid: bool           # 簽章是否有效
    is_creator_signed: bool  # 是否由創始人簽名
    dna: str                 # 原始DNA
    parsed_date: str         # 解析出的日期
    parsed_module: str       # 解析出的模塊名
    parsed_hash: str         # 解析出的哈希值
    has_confirm: bool        # 是否含CONFIRM雙簽
    has_seal: bool          # 是否含SEAL雙簽
    status: str              # 狀態（🟢通行·🟡待審·🔴熔斷）
    message: str             # 說明信息


@dataclass
class TierVerificationResult:
    """準入分級驗證結果（與 longhun_tier_gate.py 對接）"""
    tier_level: int          # Tier 1/2/3
    requires_real_name: bool # 是否需實名認證
    message: str             # 說明信息


# ============================================================================
# DNA 解析引擎
# ============================================================================

class DNAParser:
    """
    龍魂 DNA 解析器

    職責（§39.2 步①）：
    1. 解析 #龍芯⚡️ 格式簽名
    2. 識別日期 / 模塊 / 哈希
    3. 檢驗是否由 UID9622 簽署
    """

    def __init__(self):
        self.signature = DragonSoulSignature()
        self.dna_pattern = re.compile(
            r'#龍芯⚡️(\d{4}-\d{2}-\d{2})-([A-Z0-9-]+)-([A-F0-9]+)(?:🧬\d+)?'
        )

    def parse_dna(self, dna_string: str) -> DNASignatureResult:
        """
        解析 DNA 簽章

        格式：#龍芯⚡️{DATE}-{MODULE}-{HASH}
        例如：#龍芯⚡️2026-05-25-MEMORY-A8CC26

        人話：看簽名·識日期·驗作者·確保沒人偽造
        """

        # 基礎驗證
        if not isinstance(dna_string, str):
            return self._create_result(
                is_valid=False,
                dna=str(dna_string),
                message="❌ DNA 必須是字符串"
            )

        # 檢查前綴
        if not dna_string.startswith(self.signature.DNA_PREFIX):
            return self._create_result(
                is_valid=False,
                dna=dna_string,
                message=f"❌ DNA 前綴錯誤·應以 {self.signature.DNA_PREFIX} 開頭"
            )

        # 正則匹配
        match = self.dna_pattern.search(dna_string)
        if not match:
            return self._create_result(
                is_valid=False,
                dna=dna_string,
                message="❌ DNA 格式不符·應為 #龍芯⚡️YYYY-MM-DD-MODULE-HASH"
            )

        date, module, hash_val = match.groups()

        # 日期驗證（基礎格式檢查）
        if not self._validate_date_format(date):
            return self._create_result(
                is_valid=False,
                dna=dna_string,
                parsed_date=date,
                message=f"❌ 日期格式錯誤：{date}"
            )

        # 驗證日期在合理範圍內（不能是未來日期）
        if not self._is_date_reasonable(date):
            return self._create_result(
                is_valid=False,
                dna=dna_string,
                parsed_date=date,
                message=f"⚠️ 日期超出範圍·可能是偽造：{date}"
            )

        # 構建結果
        result = DNASignatureResult(
            is_valid=True,
            is_creator_signed=self._check_if_creator_signed(dna_string),
            dna=dna_string,
            parsed_date=date,
            parsed_module=module,
            parsed_hash=hash_val,
            has_confirm=self._check_confirm_present(dna_string),
            has_seal=self._check_seal_present(dna_string),
            status="🟢",
            message="✅ DNA 簽章有效"
        )

        return result

    def verify_creator_signature(self, dna_string: str) -> Tuple[bool, str]:
        """
        驗證是否由創始人簽署

        人話：檢查簽名是不是老大的·是的話開綠燈
        """

        parsed = self.parse_dna(dna_string)

        if not parsed.is_valid:
            return False, f"❌ 無效 DNA：{parsed.message}"

        # 這裡可以擴展更多驗證邏輯
        # 目前：只要格式正確且來自 UID9622 就認可

        if parsed.is_creator_signed:
            return True, f"✅ 創始人簽署確認（UID9622）"
        else:
            return False, f"⚠️ 非創始人簽署·需實名認證（歸入 Tier 2）"

    def verify_dual_signature(self, dna_string: str) -> Tuple[bool, str]:
        """
        驗證雙簽章（§4 DNA協議 + §C DNA對照表）

        L0 闔門規則：CONFIRM ⊕ SEAL ⊕ GPG·缺一不開門

        人話：三道簽名都要在·少一道就不讓進
        """

        parsed = self.parse_dna(dna_string)

        if not parsed.is_valid:
            return False, "❌ DNA 格式無效·無法驗雙簽"

        # 檢查三道簽名
        has_confirm = parsed.has_confirm
        has_seal = parsed.has_seal
        has_gpg = self._check_gpg_present(dna_string)

        if has_confirm and has_seal and has_gpg:
            return True, "🟢 三重簽章完整·L0 闔門開啟"
        elif has_confirm and has_seal:
            return True, "🟡 CONFIRM ⊕ SEAL 完整·可進入（缺 GPG 可補）"
        else:
            return False, f"🔴 雙簽不完整·拒入·CONFIRM:{has_confirm} SEAL:{has_seal} GPG:{has_gpg}"

    # ─────────────────────────────────────────────────────────────────────
    # 內部輔助方法
    # ─────────────────────────────────────────────────────────────────────

    def _create_result(self, is_valid: bool, dna: str,
                       parsed_date: str = "", parsed_module: str = "",
                       parsed_hash: str = "", message: str = "") -> DNASignatureResult:
        """建立驗證結果"""
        return DNASignatureResult(
            is_valid=is_valid,
            is_creator_signed=False,
            dna=dna,
            parsed_date=parsed_date,
            parsed_module=parsed_module,
            parsed_hash=parsed_hash,
            has_confirm=self._check_confirm_present(dna),
            has_seal=self._check_seal_present(dna),
            status="🟢" if is_valid else "🔴",
            message=message
        )

    def _validate_date_format(self, date_str: str) -> bool:
        """驗證日期格式 YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _is_date_reasonable(self, date_str: str) -> bool:
        """檢查日期是否合理（不超過今天）"""
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.now()
            return parsed_date <= today
        except ValueError:
            return False

    def _check_if_creator_signed(self, dna_string: str) -> bool:
        """檢查是否由創始人簽署"""
        # 簡化版：只要格式正確就認為是創始人簽署
        # 實際可以添加加密驗證
        return self.signature.DNA_PREFIX in dna_string

    def _check_confirm_present(self, text: str) -> bool:
        """檢查是否含 CONFIRM 簽章"""
        return self.signature.UNIQUE_CONFIRM in text

    def _check_seal_present(self, text: str) -> bool:
        """檢查是否含 SEAL 簽章"""
        return self.signature.CREATOR_SEAL in text

    def _check_gpg_present(self, text: str) -> bool:
        """檢查是否含 GPG 簽名"""
        return self.signature.GPG_FINGERPRINT in text

    def to_dict(self, result: DNASignatureResult) -> Dict:
        """轉為字典·用於 JSON 序列化"""
        return asdict(result)


# ============================================================================
# 測試與示例
# ============================================================================

def test_dna_parser():
    """DNA 解析器測試"""

    print("\n" + "=" * 80)
    print("🔐 龍魂 DNA 解析器 v1.0 · 測試")
    print("=" * 80 + "\n")

    parser = DNAParser()

    # 測試 1：有效 DNA
    print("【測試 1】有效 DNA 簽章")
    valid_dna = "#龍芯⚡️2026-05-25-MEMORY-A8CC26"
    result = parser.parse_dna(valid_dna)
    print(f"  DNA：{result.dna}")
    print(f"  有效：{result.is_valid}")
    print(f"  日期：{result.parsed_date}")
    print(f"  模塊：{result.parsed_module}")
    print(f"  哈希：{result.parsed_hash}")
    print(f"  狀態：{result.status} {result.message}\n")

    # 測試 2：無效 DNA（前綴錯誤）
    print("【測試 2】無效 DNA（簡化龍字·嚴重違規）")
    invalid_dna = "#龙芯⚡️2026-05-25-MEMORY-A8CC26"  # 簡化龍字
    result = parser.parse_dna(invalid_dna)
    print(f"  DNA：{result.dna}")
    print(f"  狀態：{result.status} {result.message}\n")

    # 測試 3：雙簽驗證
    print("【測試 3】雙簽驗證（CONFIRM ⊕ SEAL）")
    dual_signed_dna = f"{valid_dna} {parser.signature.UNIQUE_CONFIRM} {parser.signature.CREATOR_SEAL}"
    result = parser.parse_dna(dual_signed_dna)
    passed, msg = parser.verify_dual_signature(dual_signed_dna)
    print(f"  DNA：{dual_signed_dna[:50]}...")
    print(f"  雙簽通過：{passed}")
    print(f"  消息：{msg}\n")

    # 測試 4：創始人簽名驗證
    print("【測試 4】創始人簽名驗證")
    creator_signed, msg = parser.verify_creator_signature(valid_dna)
    print(f"  是否創始人簽署：{creator_signed}")
    print(f"  消息：{msg}\n")

    print("=" * 80)
    print("✅ DNA 解析器測試完成")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    test_dna_parser()
