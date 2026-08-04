#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·中孚-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#龍芯⚡️2026-06-19-CNSH-dnatoken-DNA令牌生成器-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
#龍芯⚡️2026-06-19-CNSH-dnatoken-DNA令牌生成器-v1.0
"""
通心译 | TongXinYi: DNA Token Generator
龍魂体系·DNA令牌生成器 — 核心令牌生成 + 驗證 + 撤銷

功能:
- 生成帶DNA追溯頭的國密令牌
- SM2簽名 + SM3哈希 + 六十四卦審計
- 令牌驗證（簽名驗證 + 過期檢查 + 撤銷檢查）
- 令牌撤銷與過期清理
- 隱私保護: 平台限定哈希，無法反推真實身份
"""
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-06-19-CNSH-dnatoken-DNA令牌生成器-v1.0

import json
import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any

__版本__ = "v1.0"
__dna__ = "#龍芯⚡️2026-06-19-CNSH-dnatoken-DNA令牌生成器-v1.0"


# ═══════════════════════════════════════════════════════════════
# 導入子模塊 | Import Submodules
# ═══════════════════════════════════════════════════════════════
from .DNA身份锚定 import (
    DNA身份錨定器, SM3哈希器, SM2簽名器,
    卦名表, 卦吉凶表, 甲骨文對照
)
from .DNA令牌存储 import DNA令牌存儲管理器


# ═══════════════════════════════════════════════════════════════
# DNA令牌生成器 | DNA Token Generator
# ═══════════════════════════════════════════════════════════════
class DNA令牌生成器:
    """
    通心译 | TongXinYi: DNA Token Generator
    龍魂DNA令牌核心生成器 — 生成、驗證、撤銷完整的國密令牌

    令牌結構:
    {
        "dna_header": "#龍芯⚡️{時間戳}-{平台}-{動作}",
        "identity_hash": "SM3(生物特徵+64卦+甲骨文)",
        "wuxing_sig": {"金": 0.8, "木": 0.6, "水": 0.7, "火": 0.5, "土": 0.9},
        "hexagram_audit": "雷天大壯-吉",
        "scope": ["淘寶:購物", "滴滴:打車", "美團:外賣"],
        "platform_key": "平台公鑰指紋",
        "expiry": "2026-06-20T23:59:59+08:00",
        "issued_at": "2026-06-19T10:00:00+08:00",
        "token_id": "UUID",
        "signature": "SM2簽名"
    }
    """

    # 預定義授權範圍模板 | Predefined scope templates
    授權範圍模板 = {
        '購物': ['淘寶:購物', '京東:購物', '拼多多:購物'],
        '出行': ['滴滴:打車', '高德:導航', '攜程:訂票'],
        '餐飲': ['美團:外賣', '餓了麼:外賣', '大眾點評:點評'],
        '支付': ['支付寶:支付', '微信支付:支付', '銀聯:支付'],
        '社交': ['微信:聊天', 'QQ:聊天', '微博:發帖'],
        '娛樂': ['抖音:觀看', 'B站:觀看', '網易雲:聽歌'],
        '全部': []  # 動態填充所有
    }

    def __init__(自身, 數據庫路徑: str | None = None, 加密密鑰路徑: str | None = None):
        """
        初始化DNA令牌生成器
        :param 數據庫路徑: 令牌存儲數據庫路徑
        :param 加密密鑰路徑: SM4加密密鑰路徑
        """
        自身.身份錨定 = DNA身份錨定器()
        自身.存儲管理 = DNA令牌存儲管理器(數據庫路徑, 加密密鑰路徑)
        自身.SM2 = 自身.身份錨定.SM2

        # 初始化密鑰（若未生成）
        if 自身.SM2.私鑰 is None:
            自身.SM2.生成密鑰對()

        print(f"[DNA令牌生成器] 🐉 DNA令牌核心系統已初始化 | {__dna__}")

    # ═══════════════════════════════════════════════════════════════
    # 核心: 生成令牌 | Core: Generate Token
    # ═══════════════════════════════════════════════════════════════

    def 生成令牌(自身,
              用戶身份: str,
              授權範圍: List[str],
              有效期小時: int = 24,
              生物特徵種子: str = None,
              平台標識: str = "CNSH",
              動作描述: str = "令牌簽發") -> Dict[str, Any]:
        """
        🟢 生成DNA令牌 | Generate DNA Token
        :param 用戶身份: 用戶身份標識（如用戶名或身份證摘要）
        :param 授權範圍: 授權範圍列表，如 ['淘寶:購物', '滴滴:打車']
        :param 有效期小時: 令牌有效期（小時），默認24小時
        :param 生物特徵種子: 可選生物特徵種子
        :param 平台標識: 平台標識，默認CNSH
        :param 動作描述: 動作描述
        :return: 完整的DNA令牌字典
        """
        print(f"[令牌生成] 🟢 正在為用戶 '{用戶身份}' 生成DNA令牌...")

        # 生成唯一令牌ID
        令牌ID = str(uuid.uuid4())

        # 當前時間
        簽發時間 = datetime.now(timezone(timedelta(hours=8)))
        過期時間 = 簽發時間 + timedelta(hours=有效期小時)

        # DNA頭部
        DNA頭部 = 自身.身份錨定.生成DNA頭部(平台標識, 動作描述)

        # 生成身份哈希
        if 生物特徵種子 is None:
            生物特徵種子 = f"用戶種子_{用戶身份}_{secrets.token_hex(8)}"

        身份信息 = 自身.身份錨定.生成身份哈希(生物特徵種子)

        # 平台公鑰指紋
        公鑰指紋 = 自身.SM2.獲取公鑰指紋()

        # 構造令牌主體（待簽名部分）
        令牌主體 = {
            'dna_header': DNA頭部,
            'identity_hash': 身份信息['identity_hash'],
            'wuxing_sig': 身份信息['wuxing_sig'],
            'hexagram_audit': 身份信息['hexagram_audit'],
            'scope': 授權範圍,
            'platform_key': 公鑰指紋,
            'expiry': 過期時間.isoformat(),
            'issued_at': 簽發時間.isoformat(),
            'token_id': 令牌ID,
            'user_identity': 用戶身份
        }

        # SM2簽名
        簽名數據 = json.dumps(令牌主體, sort_keys=True, ensure_ascii=False).encode('utf-8')
        簽名 = 自身.SM2.簽名(簽名數據)

        # 完整令牌
        完整令牌 = dict(令牌主體)
        完整令牌['signature'] = 簽名

        # 存儲到數據庫
        存儲結果 = 自身.存儲管理.存儲令牌(完整令牌)

        if 存儲結果:
            print(f"[令牌生成] 🟢 DNA令牌生成成功 | ID: {令牌ID[:20]}...")
            print(f"[令牌生成] 📋 授權範圍: {授權範圍}")
            print(f"[令牌生成] ⏰ 有效期至: {過期時間.strftime('%Y-%m-%d %H:%M')}")
            print(f"[令牌生成] ☯ 卦象: {身份信息['hexagram_audit']}")
        else:
            print(f"[令牌生成] 🟡 令牌已生成但存儲失敗")

        return 完整令牌

    def 生成令牌字符串(自身,
                  用戶身份: str,
                  授權範圍: List[str],
                  有效期小時: int = 24,
                  生物特徵種子: str = None) -> str:
        """
        🟢 生成DNA令牌並返回序列化字符串 | Generate and serialize token
        :return: Base64編碼的令牌字符串
        """
        import base64
        令牌 = 自身.生成令牌(用戶身份, 授權範圍, 有效期小時, 生物特徵種子)
        令牌JSON = json.dumps(令牌, ensure_ascii=False)
        return base64.b64encode(令牌JSON.encode('utf-8')).decode('utf-8')

    # ═══════════════════════════════════════════════════════════════
    # 核心: 驗證令牌 | Core: Verify Token
    # ═══════════════════════════════════════════════════════════════

    def 驗證令牌(自身, 令牌輸入) -> Dict[str, Any]:
        """
        🟡 驗證DNA令牌 | Verify DNA Token
        檢查: 格式合法性 → SM2簽名 → 過期時間 → 撤銷狀態
        :param 令牌輸入: 令牌字典或Base64字符串
        :return: 驗證結果字典 {'valid': bool, 'reason': str, 'token': dict}
        """
        # 解析令牌
        令牌 = 自身._解析令牌(令牌輸入)
        if 令牌 is None:
            return {'valid': False, 'reason': '令牌格式無效', 'token': None}

        令牌ID = 令牌.get('token_id', '')

        # 1. 檢查必需字段
        必需字段 = ['dna_header', 'identity_hash', 'signature', 'expiry', 'token_id']
        for 字段 in 必需字段:
            if 字段 not in 令牌 or not 令牌[字段]:
                return {'valid': False, 'reason': f'缺少必需字段: {字段}', 'token': 令牌}

        # 2. 驗證SM2簽名
        try:
            驗證主體 = dict(令牌)
            簽名 = 驗證主體.pop('signature')
            簽名數據 = json.dumps(驗證主體, sort_keys=True, ensure_ascii=False).encode('utf-8')

            簽名有效 = 自身.SM2.驗證(簽名數據, 簽名)
            if not 簽名有效:
                return {'valid': False, 'reason': 'SM2簽名驗證失敗', 'token': 令牌}
        except Exception as 錯誤:
            return {'valid': False, 'reason': f'簽名驗證異常: {錯誤}', 'token': 令牌}

        # 3. 檢查過期時間
        try:
            過期時間 = datetime.fromisoformat(令牌['expiry'])
            現在 = datetime.now(timezone(timedelta(hours=8)))
            if 現在 > 過期時間:
                return {'valid': False, 'reason': '令牌已過期', 'token': 令牌}
        except Exception:
            return {'valid': False, 'reason': '過期時間格式無效', 'token': 令牌}

        # 4. 檢查撤銷狀態（查數據庫）
        數據庫令牌 = 自身.存儲管理.查詢令牌(令牌ID)
        if 數據庫令牌 and 數據庫令牌.get('status') != '有效':
            return {'valid': False, 'reason': f'令牌已被{數據庫令牌["status"]}', 'token': 令牌}

        # 5. 驗證DNA頭部格式
        if not 令牌['dna_header'].startswith('#龍芯⚡️'):
            return {'valid': False, 'reason': 'DNA頭部格式無效', 'token': 令牌}

        # 全部通過
        print(f"[令牌驗證] 🟢 令牌驗證通過 | ID: {令牌ID[:20]}...")
        return {
            'valid': True,
            'reason': '驗證通過',
            'token': 令牌,
            'identity_hash': 令牌.get('identity_hash'),
            'scope': 令牌.get('scope', []),
            'hexagram_audit': 令牌.get('hexagram_audit')
        }

    def 快速驗證(自身, 令牌輸入) -> bool:
        """
        🟡 快速驗證令牌（只返回布爾值）| Quick verify token
        :return: 是否有效
        """
        結果 = 自身.驗證令牌(令牌輸入)
        return 結果.get('valid', False)

    # ═══════════════════════════════════════════════════════════════
    # 核心: 撤銷令牌 | Core: Revoke Token
    # ═══════════════════════════════════════════════════════════════

    def 撤銷令牌(自身, 令牌ID: str, 原因: str = "用戶主動撤銷") -> bool:
        """
        🔴 撤銷指定令牌 | Revoke a token
        :param 令牌ID: 要撤銷的令牌UUID
        :param 原因: 撤銷原因
        :return: 撤銷是否成功
        """
        print(f"[令牌撤銷] 🔴 正在撤銷令牌: {令牌ID[:20]}...")
        結果 = 自身.存儲管理.撤銷令牌(令牌ID, 原因)
        return 結果

    def 列出有效令牌(自身, 用戶身份: str | None = None) -> List[Dict]:
        """
        🟢 列出有效令牌 | List active tokens
        :param 用戶身份: 可選，指定用戶
        :return: 有效令牌列表
        """
        if 用戶身份:
            令牌列表 = 自身.存儲管理.查詢用戶令牌(用戶身份, 包含過期=False)
            print(f"[令牌列表] 🟢 用戶 '{用戶身份}' 有 {len(令牌列表)} 個有效令牌")
        else:
            # 獲取所有有效令牌（通過統計）
            統計 = 自身.存儲管理.獲取統計()
            print(f"[令牌列表] 🟢 系統共有 {統計.get('有效令牌', 0)} 個有效令牌")
            令牌列表 = []

        return 令牌列表

    # ═══════════════════════════════════════════════════════════════
    # 隱私保護: 範圍驗證 | Privacy: Scope Verification
    # ═══════════════════════════════════════════════════════════════

    def 驗證平台授權(自身, 令牌輸入, 平台名: str, 操作: str) -> Dict[str, Any]:
        """
        🟡 驗證平台特定授權 — 平台只能看到跟自己相關的授權
        | Verify platform-specific authorization
        :param 令牌輸入: 令牌
        :param 平台名: 平台名稱，如 '淘寶', '滴滴'
        :param 操作: 操作名稱，如 '購物', '打車'
        :return: 驗證結果
        """
        # 先完整驗證令牌
        驗證結果 = 自身.驗證令牌(令牌輸入)
        if not 驗證結果.get('valid'):
            return 驗證結果

        令牌 = 驗證結果['token']
        授權範圍 = 令牌.get('scope', [])

        # 檢查平台特定授權
        平台授權 = f"{平台名}:{操作}"
        通配授權 = f"{平台名}:*"

        if 平台授權 in 授權範圍 or 通配授權 in 授權範圍:
            # 生成平台限定哈希（平台無法獲取真實身份）
            限定哈希 = 自身.身份錨定.生成範圍哈希(
                令牌.get('identity_hash', ''),
                平台名
            )

            print(f"[平台授權] 🟢 平台 '{平台名}' 授權驗證通過")
            return {
                'valid': True,
                'reason': '平台授權驗證通過',
                'platform': 平台名,
                'operation': 操作,
                'scoped_hash': 限定哈希,  # 平台只能看到限定哈希
                'scope': [s for s in 授權範圍 if s.startswith(平台名)]  # 只返回平台相關授權
            }
        else:
            print(f"[平台授權] 🔴 平台 '{平台名}' 無 '{操作}' 授權")
            return {
                'valid': False,
                'reason': f'平台 {平台名} 未被授權執行 {操作}',
                'platform': 平台名
            }

    # ═══════════════════════════════════════════════════════════════
    # 維護操作 | Maintenance Operations
    # ═══════════════════════════════════════════════════════════════

    def 清理過期令牌(自身) -> int:
        """🟡 清理所有過期令牌 | Clean up expired tokens"""
        清理數 = 自身.存儲管理.清理過期令牌()
        return 清理數

    def 獲取統計(自身) -> Dict[str, Any]:
        """🟡 獲取系統統計 | Get system statistics"""
        存儲統計 = 自身.存儲管理.獲取統計()
        存儲統計['dna_version'] = __dna__
        存儲統計['generator_version'] = __版本__
        return 存儲統計

    # ═══════════════════════════════════════════════════════════════
    # 便捷方法 | Convenience Methods
    # ═══════════════════════════════════════════════════════════════

    def 從模板生成(自身,
              用戶身份: str,
              模板名: str = '全部',
              有效期小時: int = 24) -> Dict[str, Any]:
        """
        🟢 從預設模板生成令牌 | Generate token from template
        :param 模板名: 模板名稱（購物/出行/餐飲/支付/社交/娛樂/全部）
        """
        if 模板名 == '全部':
            # 合併所有授權
            所有範圍 = []
            for 類別, 範圍 in 自身.授權範圍模板.items():
                if 類別 != '全部':
                    所有範圍.extend(範圍)
            授權範圍 = 所有範圍
        else:
            授權範圍 = 自身.授權範圍模板.get(模板名, [])

        if not 授權範圍:
            print(f"[令牌生成] 🟡 未知模板 '{模板名}'，使用默認空授權")
            授權範圍 = []

        return 自身.生成令牌(用戶身份, 授權範圍, 有效期小時)

    # ═══════════════════════════════════════════════════════════════
    # 內部工具 | Internal Utilities
    # ═══════════════════════════════════════════════════════════════

    def _解析令牌(自身, 令牌輸入):
        """🔴 解析令牌輸入（支持字典和Base64字符串）| Parse token input"""
        if isinstance(令牌輸入, dict):
            return 令牌輸入
        elif isinstance(令牌輸入, str):
            try:
                import base64
                # 嘗試Base64解碼
                JSON字符串 = base64.b64decode(令牌輸入).decode('utf-8')
                return json.loads(JSON字符串)
            except Exception:
                # 嘗試直接JSON解析
                try:
                    return json.loads(令牌輸入)
                except Exception:
                    return None
        return None


# ═══════════════════════════════════════════════════════════════
# 獨立執行演示 | Standalone Execution Demo
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import tempfile

    print("=" * 70)
    print("🐉 DNA令牌生成器 · 獨立執行演示")
    print(f"🧬 {__dna__}")
    print("=" * 70)

    # 使用臨時目錄
    臨時目錄 = tempfile.mkdtemp(prefix="cns_token_gen_")
    數據庫路徑 = os.path.join(臨時目錄, "tokens.db")
    密鑰路徑 = os.path.join(臨時目錄, "key.bin")

    print(f"\n臨時測試目錄: {臨時目錄}")

    # 創建令牌生成器
    生成器 = DNA令牌生成器(數據庫路徑, 密鑰路徑)

    print("\n" + "=" * 70)
    print("--- 1. 生成DNA令牌 ---")
    print("=" * 70)

    令牌 = 生成器.生成令牌(
        用戶身份="用戶_張三",
        授權範圍=['淘寶:購物', '滴滴:打車', '美團:外賣'],
        有效期小時=24,
        生物特徵種子="指紋特徵_AABBCCDD00112233"
    )

    print(f"\n令牌結構:")
    print(f"  DNA頭部: {令牌['dna_header']}")
    print(f"  身份哈希: {令牌['identity_hash'][:32]}...")
    print(f"  卦象審計: {令牌['hexagram_audit']}")
    print(f"  授權範圍: {令牌['scope']}")
    print(f"  公鑰指紋: {令牌['platform_key'][:24]}...")
    print(f"  簽發時間: {令牌['issued_at']}")
    print(f"  過期時間: {令牌['expiry']}")
    print(f"  令牌ID: {令牌['token_id'][:24]}...")
    print(f"  簽名: {令牌['signature'][:32]}...")

    print("\n" + "=" * 70)
    print("--- 2. 令牌序列化 ---")
    print("=" * 70)

    序列化令牌 = 生成器.生成令牌字符串(
        用戶身份="用戶_李四",
        授權範圍=['支付寶:支付', '微信:聊天'],
        有效期小時=12
    )
    print(f"序列化令牌長度: {len(序列化令牌)} 字符")
    print(f"前80字符: {序列化令牌[:80]}...")

    print("\n" + "=" * 70)
    print("--- 3. 驗證令牌 ---")
    print("=" * 70)

    驗證結果 = 生成器.驗證令牌(令牌)
    print(f"驗證結果: {'✅ 有效' if 驗證結果['valid'] else '❌ 無效'}")
    print(f"驗證原因: {驗證結果['reason']}")
    if 驗證結果['valid']:
        print(f"授權範圍: {驗證結果['scope']}")
        print(f"卦象: {驗證結果['hexagram_audit']}")

    # 驗證序列化令牌
    序列驗證 = 生成器.驗證令牌(序列化令牌)
    print(f"\n序列化令牌驗證: {'✅ 有效' if 序列驗證['valid'] else '❌ 無效'}")

    print("\n" + "=" * 70)
    print("--- 4. 平台授權驗證（隱私保護）---")
    print("=" * 70)

    淘寶驗證 = 生成器.驗證平台授權(令牌, '淘寶', '購物')
    print(f"淘寶購物授權: {'✅ 通過' if 淘寶驗證['valid'] else '❌ 拒絕'}")
    if 淘寶驗證['valid']:
        print(f"  平台限定哈希: {淘寶驗證['scoped_hash'][:32]}...")
        print(f"  可見授權: {淘寶驗證['scope']}")

    京東驗證 = 生成器.驗證平台授權(令牌, '京東', '購物')
    print(f"\n京東購物授權: {'✅ 通過' if 京東驗證['valid'] else '❌ 拒絕'}")
    if not 京東驗證['valid']:
        print(f"  原因: {京東驗證['reason']}")

    print("\n" + "=" * 70)
    print("--- 5. 撤銷令牌 ---")
    print("=" * 70)

    撤銷結果 = 生成器.撤銷令牌(令牌['token_id'], '演示撤銷')
    print(f"撤銷結果: {'✅ 成功' if 撤銷結果 else '❌ 失敗'}")

    # 驗證已撤銷的令牌
    撤銷驗證 = 生成器.驗證令牌(令牌)
    print(f"撤銷後驗證: {'✅ 有效' if 撤銷驗證['valid'] else '❌ 無效'}")
    print(f"原因: {撤銷驗證['reason']}")

    print("\n" + "=" * 70)
    print("--- 6. 模板生成令牌 ---")
    print("=" * 70)

    出行令牌 = 生成器.從模板生成('用戶_王五', '出行', 有效期小時=6)
    print(f"出行模板令牌授權: {出行令牌['scope']}")

    餐飲令牌 = 生成器.從模板生成('用戶_趙六', '餐飲', 有效期小時=3)
    print(f"餐飲模板令牌授權: {餐飲令牌['scope']}")

    print("\n" + "=" * 70)
    print("--- 7. 列出有效令牌 ---")
    print("=" * 70)

    有效令牌 = 生成器.列出有效令牌('用戶_張三')
    print(f"用戶_張三有效令牌: {len(有效令牌)} 個")

    全部有效 = 生成器.列出有效令牌()
    print(f"系統全部有效令牌查詢完成")

    print("\n" + "=" * 70)
    print("--- 8. 系統統計 ---")
    print("=" * 70)

    統計 = 生成器.獲取統計()
    for 鍵, 值 in 統計.items():
        print(f"  {鍵}: {值}")

    # 清理臨時文件
    import shutil
    shutil.rmtree(臨時目錄, ignore_errors=True)

    print("\n" + "=" * 70)
    print("✅ DNA令牌生成器系統演示完成")
    print("=" * 70)
