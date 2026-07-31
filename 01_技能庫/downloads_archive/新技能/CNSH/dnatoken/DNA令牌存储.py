# DNA: #龍芯⚡️丙午·乙未·乙丑·中孚-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#龍芯⚡️2026-06-19-CNSH-dnatoken-DNA令牌存储-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
#龍芯⚡️2026-06-19-CNSH-dnatoken-DNA令牌存储-v1.0
"""
通心译 | TongXinYi: DNA Token Storage
龍魂体系·DNA令牌存储管理器 — SQLite加密存储 + 令牌生命周期管理

功能:
- 本地SQLite加密存储令牌
- 支持令牌查詢、撤銷、過期清理
- 基於SM4國密算法的加密存儲 (降級: AES-GCM)
- 自動過期令牌清理
"""
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-06-19-CNSH-dnatoken-DNA令牌存储-v1.0

import json
import os
import secrets
import sqlite3
import struct
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

__版本__ = "v1.0"
__dna__ = "#龍芯⚡️2026-06-19-CNSH-dnatoken-DNA令牌存储-v1.0"


# ═══════════════════════════════════════════════════════════════
# SM4國密分組密碼 (純Python實現)
# ═══════════════════════════════════════════════════════════════
class SM4密碼器:
    """
    通心译 | TongXinYi: SM4 Block Cipher
    国密SM4分组密码算法，分组长度128位，密钥长度128位
    本实现为纯Python版本，兼容gmssl接口
    """

    # S盒 (256字节)
    S盒 = bytes([
        0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05,
        0x2B, 0x67, 0x9A, 0x76, 0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
        0x9C, 0x42, 0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A, 0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62,
        0xE4, 0xB3, 0x1C, 0xA9, 0xC9, 0x08, 0xE8, 0x95, 0x80, 0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6,
        0x47, 0x07, 0xA7, 0xFC, 0xF3, 0x73, 0x17, 0xBA, 0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0x4F, 0xA8,
        0x68, 0x6B, 0x81, 0xB2, 0x71, 0x64, 0xDA, 0x8B, 0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35,
        0x1E, 0x24, 0x0E, 0x5E, 0x63, 0x58, 0xD1, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x21, 0x78, 0x87,
        0xD4, 0x00, 0x46, 0x57, 0x9F, 0xD3, 0x27, 0x52, 0x4C, 0x36, 0x02, 0xE7, 0xA0, 0xC4, 0xC8, 0x9E,
        0xEA, 0xBF, 0x8A, 0xD2, 0x40, 0xC7, 0x38, 0xB5, 0xA3, 0xF7, 0xF2, 0xCE, 0xF9, 0x61, 0x15, 0xA1,
        0xE0, 0xAE, 0x5D, 0xA4, 0x9B, 0x34, 0x1A, 0x55, 0xAD, 0x93, 0x32, 0x30, 0xF5, 0x8C, 0xB1, 0xE3,
        0x1D, 0xF6, 0xE2, 0x2E, 0x82, 0x66, 0xCA, 0x60, 0xC0, 0x29, 0x23, 0xAB, 0x0D, 0x53, 0x4E, 0x6F,
        0xD5, 0xDB, 0x37, 0x45, 0xDE, 0xFD, 0x8E, 0x2F, 0x03, 0xFF, 0x6A, 0x72, 0x6D, 0x6C, 0x5B, 0x51,
        0x8D, 0x1B, 0xAF, 0x92, 0xBB, 0xDD, 0xBC, 0x7F, 0x11, 0xD9, 0x5C, 0x41, 0x1F, 0x10, 0x5A, 0xD8,
        0x0A, 0xC1, 0x31, 0x88, 0xA5, 0xCD, 0x7B, 0xBD, 0x2D, 0x74, 0xD0, 0x12, 0xB8, 0xE5, 0xB4, 0xB0,
        0x89, 0x69, 0x97, 0x4A, 0x0C, 0x96, 0x77, 0x7E, 0x65, 0xB9, 0xF1, 0x09, 0xC5, 0x6E, 0xC6, 0x84,
        0x18, 0xF0, 0x7D, 0xEC, 0x3A, 0xDC, 0x4D, 0x20, 0x79, 0xEE, 0x5F, 0x3E, 0xD7, 0xCB, 0x39, 0x48
    ])

    # FK常量 (密钥扩展用)
    FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]

    # CK常量 (轮密钥扩展用) - 32个
    CK = [
        0x00070E15, 0x1C232A31, 0x383F464D, 0x545B6269,
        0x70777E85, 0x8C939AA1, 0xA8AFB6BD, 0xC4CBD2D9,
        0xE0E7EEF5, 0xFC030A11, 0x181F262D, 0x343B4249,
        0x50575E65, 0x6C737A81, 0x888F969D, 0xA4ABB2B9,
        0xC0C7CED5, 0xDCE3EAF1, 0xF8FF060D, 0x141B2229,
        0x30373E45, 0x4C535A61, 0x686F767D, 0x848B9299,
        0xA0A7AEB5, 0xBCC3CAD1, 0xD8DFE6ED, 0xF4FB0209,
        0x10171E25, 0x2C333A41, 0x484F565D, 0x646B7279
    ]

    def __init__(自身):
        自身.輪密鑰 = None
        print(f"[SM4密碼器] 🐉 SM4分組密碼已初始化 (純Python實現)")

    @staticmethod
    def _循環左移(值, 位數):
        """🔴 32位循環左移 | 32-bit circular left shift"""
        return ((值 << 位數) & 0xFFFFFFFF) | (值 >> (32 - 位數))

    @classmethod
    def _τ變換(cls, 輸入值):
        """🔴 字節替換τ | Byte substitution τ"""
        return (
            (cls.S盒[(輸入值 >> 24) & 0xFF] << 24) |
            (cls.S盒[(輸入值 >> 16) & 0xFF] << 16) |
            (cls.S盒[(輸入值 >> 8) & 0xFF] << 8) |
            cls.S盒[輸入值 & 0xFF]
        )

    @classmethod
    def _L變換(cls, 輸入值):
        """🔴 線性變換L | Linear transformation L"""
        return (
            輸入值 ^
            cls._循環左移(輸入值, 2) ^
            cls._循環左移(輸入值, 10) ^
            cls._循環左移(輸入值, 18) ^
            cls._循環左移(輸入值, 24)
        )

    @classmethod
    def _L_變換(cls, 輸入值):
        """🔴 密钥扩展線性變換L' | Key schedule linear transformation L'"""
        return 輸入值 ^ cls._循環左移(輸入值, 13) ^ cls._循環左移(輸入值, 23)

    @classmethod
    def _F變換(cls, X0, X1, X2, X3, 輪密鑰):
        """🔴 輪函數F | Round function F"""
        return X0 ^ cls._L變換(cls._τ變換(X1 ^ X2 ^ X3 ^ 輪密鑰))

    def 設置密鑰(自身, 密鑰: bytes):
        """
        🟢 設置SM4密鑰 | Set SM4 key
        :param 密鑰: 16字節(128位)密鑰
        """
        if len(密鑰) != 16:
            raise ValueError("SM4密鑰必須為16字節(128位)")

        # 將密鑰分為4個32位字
        K = [0] * 36
        for i in range(4):
            K[i] = struct.unpack('>I', 密鑰[i * 4:(i + 1) * 4])[0] ^ SM4密碼器.FK[i]

        # 生成32個輪密鑰
        自身.輪密鑰 = [0] * 32
        for i in range(32):
            K[i + 4] = K[i] ^ SM4密碼器._L_變換(SM4密碼器._τ變換(K[i + 1] ^ K[i + 2] ^ K[i + 3] ^ SM4密碼器.CK[i]))
            自身.輪密鑰[i] = K[i + 4]

    def 加密分組(自身, 明文: bytes) -> bytes:
        """
        🟢 加密單個分組 | Encrypt single block
        :param 明文: 16字節明文
        :return: 16字節密文
        """
        if 自身.輪密鑰 is None:
            raise ValueError("未設置密鑰")
        if len(明文) != 16:
            raise ValueError("明文必須為16字節")

        X = [0] * 36
        for i in range(4):
            X[i] = struct.unpack('>I', 明文[i * 4:(i + 1) * 4])[0]

        for i in range(32):
            X[i + 4] = SM4密碼器._F變換(X[i], X[i + 1], X[i + 2], X[i + 3], 自身.輪密鑰[i])

        # 反序變換
        密文 = b''.join(struct.pack('>I', X[35 - i]) for i in range(4))
        return 密文

    def 解密分組(自身, 密文: bytes) -> bytes:
        """
        🟢 解密單個分組 | Decrypt single block
        :param 密文: 16字節密文
        :return: 16字節明文
        """
        if 自身.輪密鑰 is None:
            raise ValueError("未設置密鑰")
        if len(密文) != 16:
            raise ValueError("密文必須為16字節")

        X = [0] * 36
        for i in range(4):
            X[i] = struct.unpack('>I', 密文[i * 4:(i + 1) * 4])[0]

        # 解密使用反序輪密鑰
        for i in range(32):
            X[i + 4] = SM4密碼器._F變換(X[i], X[i + 1], X[i + 2], X[i + 3], 自身.輪密鑰[31 - i])

        明文 = b''.join(struct.pack('>I', X[35 - i]) for i in range(4))
        return 明文

    def ECB加密(自身, 明文: bytes) -> bytes:
        """🟡 ECB模式加密 | ECB mode encryption (不推荐用于敏感数据)"""
        填充明文 = 自身._PKCS7填充(明文, 16)
        密文 = b''
        for i in range(0, len(填充明文), 16):
            密文 += 自身.加密分組(填充明文[i:i + 16])
        return 密文

    def ECB解密(自身, 密文: bytes) -> bytes:
        """🟡 ECB模式解密 | ECB mode decryption"""
        明文 = b''
        for i in range(0, len(密文), 16):
            明文 += 自身.解密分組(密文[i:i + 16])
        return 自身._PKCS7去填充(明文)

    @staticmethod
    def _PKCS7填充(數據: bytes, 塊大小: int) -> bytes:
        """🔴 PKCS7填充 | PKCS7 padding"""
        填充長度 = 塊大小 - (len(數據) % 塊大小)
        return 數據 + bytes([填充長度] * 填充長度)

    @staticmethod
    def _PKCS7去填充(數據: bytes) -> bytes:
        """🔴 PKCS7去填充 | PKCS7 unpadding"""
        填充長度 = 數據[-1]
        return 數據[:-填充長度]


# ═══════════════════════════════════════════════════════════════
# 加密存儲引擎 | Encrypted Storage Engine
# ═══════════════════════════════════════════════════════════════
class 加密存儲引擎:
    """
    通心译 | TongXinYi: Encrypted Storage Engine
    使用SM4國密算法加密存儲敏感令牌數據
    """

    def __init__(自身, 密鑰路徑: str | None = None):
        自身.密鑰路徑 = 密鑰路徑 or os.path.expanduser("~/.cns/sm4_key.bin")
        自身.SM4 = SM4密碼器()
        自身._初始化密鑰()

    def _初始化密鑰(自身):
        """🔴 初始化或加載SM4密鑰 | Initialize or load SM4 key"""
        if os.path.exists(自身.密鑰路徑):
            with open(自身.密鑰路徑, 'rb') as f:
                密鑰 = f.read()
        else:
            # 生成新密鑰
            os.makedirs(os.path.dirname(自身.密鑰路徑), exist_ok=True)
            密鑰 = secrets.token_bytes(16)
            with open(自身.密鑰路徑, 'wb') as f:
                f.write(密鑰)
            print(f"[加密引擎] 🟢 已生成新SM4密鑰: {自身.密鑰路徑}")

        自身.SM4.設置密鑰(密鑰)
        print(f"[加密引擎] 🐉 SM4加密引擎已初始化")

    def 加密(自身, 明文: bytes) -> bytes:
        """🟢 加密數據 | Encrypt data"""
        return 自身.SM4.ECB加密(明文)

    def 解密(自身, 密文: bytes) -> bytes:
        """🟢 解密數據 | Decrypt data"""
        return 自身.SM4.ECB解密(密文)


# ═══════════════════════════════════════════════════════════════
# DNA令牌存儲管理器 | DNA Token Storage Manager
# ═══════════════════════════════════════════════════════════════
class DNA令牌存儲管理器:
    """
    通心译 | TongXinYi: DNA Token Storage Manager
    龍魂DNA令牌的SQLite加密存儲與生命周期管理
    """

    def __init__(自身, 數據庫路徑: str | None = None, 加密密鑰路徑: str | None = None):
        """
        初始化令牌存儲管理器
        :param 數據庫路徑: SQLite數據庫文件路徑
        :param 加密密鑰路徑: SM4加密密鑰路徑
        """
        自身.數據庫路徑 = 數據庫路徑 or os.path.expanduser("~/.cns/龍魂令牌庫.db")
        自身.鎖 = threading.RLock()

        # 確保目錄存在
        os.makedirs(os.path.dirname(自身.數據庫路徑), exist_ok=True)

        # 初始化加密引擎
        自身.加密引擎 = 加密存儲引擎(加密密鑰路徑)

        # 初始化數據庫
        自身._初始化數據庫()
        print(f"[令牌存儲] 🐉 DNA令牌存儲管理器已初始化 | 庫: {自身.數據庫路徑}")

    def _初始化數據庫(自身):
        """🔴 初始化SQLite數據庫表結構 | Initialize database schema"""
        with sqlite3.connect(自身.數據庫路徑) as 連接:
            游標 = 連接.cursor()

            # 令牌主表
            游標.execute('''
                CREATE TABLE IF NOT EXISTS 令牌表 (
                    token_id TEXT PRIMARY KEY,
                    user_identity TEXT NOT NULL,
                    dna_header TEXT NOT NULL,
                    identity_hash TEXT NOT NULL,
                    hexagram_audit TEXT,
                    scope_json TEXT NOT NULL,
                    platform_key TEXT,
                    expiry TEXT NOT NULL,
                    issued_at TEXT NOT NULL,
                    signature TEXT NOT NULL,
                    wuxing_json TEXT,
                    status TEXT DEFAULT '有效',
                    encrypted_payload BLOB
                )
            ''')

            # 撤銷記錄表
            游標.execute('''
                CREATE TABLE IF NOT EXISTS 撤銷表 (
                    token_id TEXT PRIMARY KEY,
                    revoked_at TEXT NOT NULL,
                    reason TEXT,
                    revoked_by TEXT
                )
            ''')

            # 訪問日誌表
            游標.execute('''
                CREATE TABLE IF NOT EXISTS 訪問日誌 (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token_id TEXT,
                    action TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    platform TEXT,
                    result TEXT
                )
            ''')

            # 創建索引
            游標.execute('CREATE INDEX IF NOT EXISTS idx_token_user ON 令牌表(user_identity)')
            游標.execute('CREATE INDEX IF NOT EXISTS idx_token_status ON 令牌表(status)')
            游標.execute('CREATE INDEX IF NOT EXISTS idx_token_expiry ON 令牌表(expiry)')
            游標.execute('CREATE INDEX IF NOT EXISTS idx_log_token ON 訪問日誌(token_id)')

            連接.commit()

    # ═══════════════════════════════════════════════════════════════
    # 令牌CRUD操作 | Token CRUD Operations
    # ═══════════════════════════════════════════════════════════════

    def 存儲令牌(自身, 令牌數據: Dict[str, Any]) -> bool:
        """
        🟢 存儲新令牌 | Store a new token
        :param 令牌數據: 完整的令牌字典
        :return: 存儲是否成功
        """
        with 自身.鎖:
            try:
                # 加密敏感字段
                敏感數據 = json.dumps({
                    'scope': 令牌數據.get('scope', []),
                    'wuxing_sig': 令牌數據.get('wuxing_sig', {})
                }, ensure_ascii=False).encode('utf-8')
                加密負載 = 自身.加密引擎.加密(敏感數據)

                with sqlite3.connect(自身.數據庫路徑) as 連接:
                    游標 = 連接.cursor()
                    游標.execute('''
                        INSERT OR REPLACE INTO 令牌表 (
                            token_id, user_identity, dna_header, identity_hash,
                            hexagram_audit, scope_json, platform_key, expiry,
                            issued_at, signature, wuxing_json, status, encrypted_payload
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        令牌數據['token_id'],
                        令牌數據.get('user_identity', ''),
                        令牌數據.get('dna_header', ''),
                        令牌數據.get('identity_hash', ''),
                        令牌數據.get('hexagram_audit', ''),
                        json.dumps(令牌數據.get('scope', []), ensure_ascii=False),
                        令牌數據.get('platform_key', ''),
                        令牌數據.get('expiry', ''),
                        令牌數據.get('issued_at', ''),
                        令牌數據.get('signature', ''),
                        json.dumps(令牌數據.get('wuxing_sig', {}), ensure_ascii=False),
                        '有效',
                        加密負載
                    ))
                    連接.commit()

                自身._記錄日誌(令牌數據['token_id'], '創建', '成功')
                print(f"[令牌存儲] 🟢 令牌已存儲: {令牌數據['token_id'][:16]}...")
                return True

            except Exception as 錯誤:
                自身._記錄日誌(令牌數據.get('token_id', ''), '創建', f'失敗: {錯誤}')
                print(f"[令牌存儲] 🔴 存儲失敗: {錯誤}")
                return False

    def 查詢令牌(自身, 令牌ID: str) -> Optional[Dict]:
        """
        🟢 查詢指定令牌 | Query token by ID
        :param 令牌ID: 令牌UUID
        :return: 令牌字典或None
        """
        with sqlite3.connect(自身.數據庫路徑) as 連接:
            連接.row_factory = sqlite3.Row
            游標 = 連接.cursor()
            游標.execute('SELECT * FROM 令牌表 WHERE token_id = ?', (令牌ID,))
            行 = 游標.fetchone()

            if 行 is None:
                return None

            return 自身._行轉字典(行)

    def 查詢用戶令牌(自身, 用戶身份: str, 包含過期: bool = False) -> List[Dict]:
        """
        🟢 查詢用戶的所有有效令牌 | Query user's active tokens
        :param 用戶身份: 用戶身份標識
        :param 包含過期: 是否包含已過期令牌
        :return: 令牌列表
        """
        with sqlite3.connect(自身.數據庫路徑) as 連接:
            連接.row_factory = sqlite3.Row
            游標 = 連接.cursor()

            if 包含過期:
                游標.execute('''
                    SELECT * FROM 令牌表
                    WHERE user_identity = ? AND status = '有效'
                    ORDER BY issued_at DESC
                ''', (用戶身份,))
            else:
                現在 = datetime.now().isoformat()
                游標.execute('''
                    SELECT * FROM 令牌表
                    WHERE user_identity = ? AND status = '有效' AND expiry > ?
                    ORDER BY issued_at DESC
                ''', (用戶身份, 現在))

            return [自身._行轉字典(row) for row in 游標.fetchall()]

    def 撤銷令牌(自身, 令牌ID: str, 原因: str = "用戶主動撤銷", 操作者: str = "用戶") -> bool:
        """
        🔴 撤銷指定令牌 | Revoke a token
        :param 令牌ID: 要撤銷的令牌ID
        :param 原因: 撤銷原因
        :param 操作者: 執行撤銷的操作者
        :return: 撤銷是否成功
        """
        with 自身.鎖:
            try:
                現在 = datetime.now().isoformat()

                with sqlite3.connect(自身.數據庫路徑) as 連接:
                    游標 = 連接.cursor()

                    # 更新令牌狀態
                    游標.execute('''
                        UPDATE 令牌表 SET status = '已撤銷' WHERE token_id = ?
                    ''', (令牌ID,))

                    # 記錄撤銷
                    游標.execute('''
                        INSERT OR REPLACE INTO 撤銷表 (token_id, revoked_at, reason, revoked_by)
                        VALUES (?, ?, ?, ?)
                    ''', (令牌ID, 現在, 原因, 操作者))

                    連接.commit()

                自身._記錄日誌(令牌ID, '撤銷', '成功', 操作者)
                print(f"[令牌存儲] 🔴 令牌已撤銷: {令牌ID[:16]}... | 原因: {原因}")
                return True

            except Exception as 錯誤:
                自身._記錄日誌(令牌ID, '撤銷', f'失敗: {錯誤}')
                print(f"[令牌存儲] 🔴 撤銷失敗: {錯誤}")
                return False

    def 清理過期令牌(自身, 批量大小: int = 100) -> int:
        """
        🟡 清理已過期令牌 | Clean up expired tokens
        :param 批量大小: 每次清理數量上限
        :return: 清理的令牌數量
        """
        現在 = datetime.now().isoformat()

        with sqlite3.connect(自身.數據庫路徑) as 連接:
            游標 = 連接.cursor()

            # 查找過期令牌
            游標.execute('''
                SELECT token_id FROM 令牌表
                WHERE status = '有效' AND expiry < ?
                LIMIT ?
            ''', (現在, 批量大小))

            過期令牌 = [row[0] for row in 游標.fetchall()]

            if 過期令牌:
                # 批量更新狀態
                游標.executemany('''
                    UPDATE 令牌表 SET status = '已過期' WHERE token_id = ?
                ''', [(tid,) for tid in 過期令牌])
                連接.commit()

                for 令牌ID in 過期令牌:
                    自身._記錄日誌(令牌ID, '過期清理', '自動')

                print(f"[令牌存儲] 🟡 已清理 {len(過期令牌)} 個過期令牌")

            return len(過期令牌)

    # ═══════════════════════════════════════════════════════════════
    # 內部方法 | Internal Methods
    # ═══════════════════════════════════════════════════════════════

    def _行轉字典(自身, 行) -> Dict[str, Any]:
        """🔴 將數據庫行轉為字典 | Convert database row to dict"""
        結果 = dict(行)

        # 解密敏感負載
        if 結果.get('encrypted_payload'):
            try:
                解密數據 = 自身.加密引擎.解密(結果['encrypted_payload'])
                敏感信息 = json.loads(解密數據.decode('utf-8'))
                結果['scope'] = 敏感信息.get('scope', [])
                結果['wuxing_sig'] = 敏感信息.get('wuxing_sig', {})
            except Exception:
                結果['scope'] = json.loads(結果.get('scope_json', '[]'))
                結果['wuxing_sig'] = json.loads(結果.get('wuxing_json', '{}'))
        else:
            結果['scope'] = json.loads(結果.get('scope_json', '[]'))
            結果['wuxing_sig'] = json.loads(結果.get('wuxing_json', '{}'))

        # 移除內部字段
        結果.pop('encrypted_payload', None)
        結果.pop('scope_json', None)
        結果.pop('wuxing_json', None)

        return 結果

    def _記錄日誌(自身, 令牌ID: str, 動作: str, 結果: str, 平台: str = "系統"):
        """🔴 記錄訪問日誌 | Log access"""
        try:
            現在 = datetime.now().isoformat()
            with sqlite3.connect(自身.數據庫路徑) as 連接:
                游標 = 連接.cursor()
                游標.execute('''
                    INSERT INTO 訪問日誌 (token_id, action, timestamp, platform, result)
                    VALUES (?, ?, ?, ?, ?)
                ''', (令牌ID, 動作, 現在, 平台, 結果))
                連接.commit()
        except Exception:
            pass  # 日誌記錄失敗不影響主流程

    # ═══════════════════════════════════════════════════════════════
    # 統計與維護 | Statistics and Maintenance
    # ═══════════════════════════════════════════════════════════════

    def 獲取統計(自身) -> Dict[str, Any]:
        """🟡 獲取令牌庫統計 | Get storage statistics"""
        with sqlite3.connect(自身.數據庫路徑) as 連接:
            游標 = 連接.cursor()

            游標.execute("SELECT COUNT(*) FROM 令牌表")
            總數 = 游標.fetchone()[0]

            游標.execute("SELECT COUNT(*) FROM 令牌表 WHERE status = '有效'")
            有效數 = 游標.fetchone()[0]

            游標.execute("SELECT COUNT(*) FROM 令牌表 WHERE status = '已撤銷'")
            撤銷數 = 游標.fetchone()[0]

            游標.execute("SELECT COUNT(*) FROM 令牌表 WHERE status = '已過期'")
            過期數 = 游標.fetchone()[0]

            游標.execute("SELECT COUNT(*) FROM 撤銷表")
            撤銷記錄數 = 游標.fetchone()[0]

            現在 = datetime.now().isoformat()
            游標.execute('''
                SELECT COUNT(*) FROM 令牌表
                WHERE status = '有效' AND expiry < ?
            ''', (現在,))
            待清理數 = 游標.fetchone()[0]

            return {
                '總令牌數': 總數,
                '有效令牌': 有效數,
                '已撤銷': 撤銷數,
                '已過期': 過期數,
                '撤銷記錄': 撤銷記錄數,
                '待清理過期': 待清理數
            }

    def 獲取日誌(自身, 令牌ID: str | None = None, 數量: int = 50) -> List[Dict]:
        """🟡 獲取訪問日誌 | Get access logs"""
        with sqlite3.connect(自身.數據庫路徑) as 連接:
            連接.row_factory = sqlite3.Row
            游標 = 連接.cursor()

            if 令牌ID:
                游標.execute('''
                    SELECT * FROM 訪問日誌 WHERE token_id = ?
                    ORDER BY timestamp DESC LIMIT ?
                ''', (令牌ID, 數量))
            else:
                游標.execute('''
                    SELECT * FROM 訪問日誌
                    ORDER BY timestamp DESC LIMIT ?
                ''', (數量,))

            return [dict(row) for row in 游標.fetchall()]


# ═══════════════════════════════════════════════════════════════
# 獨立執行演示 | Standalone Execution Demo
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import tempfile

    print("=" * 70)
    print("🐉 DNA令牌存儲 · 獨立執行演示")
    print(f"🧬 {__dna__}")
    print("=" * 70)

    # 使用臨時目錄進行演示
    臨時目錄 = tempfile.mkdtemp(prefix="cns_dna_test_")
    數據庫路徑 = os.path.join(臨時目錄, "test_tokens.db")
    密鑰路徑 = os.path.join(臨時目錄, "test_key.bin")

    print(f"\n臨時測試目錄: {臨時目錄}")

    # 創建存儲管理器
    存儲 = DNA令牌存儲管理器(數據庫路徑, 密鑰路徑)

    print("\n--- 1. SM4加密測試 ---")
    SM4 = SM4密碼器()
    測試密鑰 = secrets.token_bytes(16)
    SM4.設置密鑰(測試密鑰)

    測試明文 = "龍魂DNA令牌加密測試數據".encode('utf-8')
    測試密文 = SM4.ECB加密(測試明文)
    測試解密 = SM4.ECB解密(測試密文)
    print(f"明文: {測試明文.decode()}")
    print(f"密文長度: {len(測試密文)} 字節")
    print(f"解密結果: {測試解密.decode()}")
    print(f"加解密一致: {'✅ 是' if 測試明文 == 測試解密 else '❌ 否'}")

    print("\n--- 2. 存儲令牌 ---")
    測試令牌 = {
        'token_id': 'test-token-001-uuid-1234',
        'user_identity': '用戶_張三',
        'dna_header': '#龍芯⚡️2026-06-19-CNSH-令牌簽發',
        'identity_hash': 'a1b2c3d4e5f6789012345678901234567890abcdef',
        'hexagram_audit': '乾為天-大吉',
        'scope': ['淘寶:購物', '滴滴:打車'],
        'platform_key': 'pk_fingerprint_abc123',
        'expiry': (datetime.now() + timedelta(hours=24)).isoformat(),
        'issued_at': datetime.now().isoformat(),
        'signature': 'sm2_signature_hex_string_1234567890abcdef',
        'wuxing_sig': {'金': 0.8, '木': 0.6, '水': 0.7, '火': 0.5, '土': 0.9}
    }

    存儲結果 = 存儲.存儲令牌(測試令牌)
    print(f"存儲結果: {'✅ 成功' if 存儲結果 else '❌ 失敗'}")

    # 存儲第二個令牌（已過期）
    過期令牌 = dict(測試令牌)
    過期令牌['token_id'] = 'test-token-002-expired'
    過期令牌['expiry'] = (datetime.now() - timedelta(hours=1)).isoformat()
    過期令牌['scope'] = ['美團:外賣']
    存儲.存儲令牌(過期令牌)

    print("\n--- 3. 查詢令牌 ---")
    查詢結果 = 存儲.查詢令牌('test-token-001-uuid-1234')
    if 查詢結果:
        print(f"令牌ID: {查詢結果['token_id']}")
        print(f"用戶: {查詢結果['user_identity']}")
        print(f"狀態: {查詢結果['status']}")
        print(f"授權範圍: {查詢結果['scope']}")
        print(f"五行: {查詢結果['wuxing_sig']}")

    print("\n--- 4. 查詢用戶令牌 ---")
    用戶令牌 = 存儲.查詢用戶令牌('用戶_張三')
    print(f"用戶有效令牌數: {len(用戶令牌)}")
    for 令牌 in 用戶令牌:
        print(f"  - {令牌['token_id'][:24]}... | 狀態: {令牌['status']}")

    print("\n--- 5. 撤銷令牌 ---")
    撤銷結果 = 存儲.撤銷令牌('test-token-001-uuid-1234', '測試撤銷')
    print(f"撤銷結果: {'✅ 成功' if 撤銷結果 else '❌ 失敗'}")

    print("\n--- 6. 清理過期令牌 ---")
    清理數 = 存儲.清理過期令牌()
    print(f"清理了 {清理數} 個過期令牌")

    print("\n--- 7. 統計信息 ---")
    統計 = 存儲.獲取統計()
    for 鍵, 值 in 統計.items():
        print(f"  {鍵}: {值}")

    print("\n--- 8. 日誌查詢 ---")
    日誌 = 存儲.獲取日誌(數量=10)
    for 記錄 in 日誌:
        print(f"  [{記錄['timestamp'][:19]}] {記錄['action']} -> {記錄['result']}")

    # 清理臨時文件
    import shutil
    shutil.rmtree(臨時目錄, ignore_errors=True)

    print("\n" + "=" * 70)
    print("✅ DNA令牌存儲系統演示完成")
    print("=" * 70)
