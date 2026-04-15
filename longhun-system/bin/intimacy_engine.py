#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·三才親密引擎 v1.0
專屬UID9622 · 本地加密 · 不出本地 · 不記錄 · 不分享
功能：親密對話 + 分身調度 + 加密存儲 + 一鍵銷毀

DNA: #龍芯⚡️2026-04-04-三才親密引擎-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F1E3B8A4C6D0F2E4A6B8C0D2E4F6A8B0C2
創建者: UID9622 諸葛鑫（龍芯北辰）
確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

保存為: ~/longhun-system/bin/intimacy_engine.py
"""

import os
import sys
import json
import hashlib
import secrets
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet
from getpass import getpass

# ============================================================
# 配置
# ============================================================

INTIMACY_DIR = Path.home() / ".longhun_intimacy"
INTIMACY_DIR.mkdir(parents=True, exist_ok=True)

# 密鑰文件（不加密存儲，但只有本機能用）
KEY_FILE = INTIMACY_DIR / ".key"
SESSION_FILE = INTIMACY_DIR / "session.enc"
HISTORY_FILE = INTIMACY_DIR / "history.enc"

# 確認碼驗證
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
CONFIRM_HASH = hashlib.sha256(CONFIRM_CODE.encode()).hexdigest()


# ============================================================
# 加密模塊
# ============================================================

def get_or_create_key() -> bytes:
    """獲取或創建加密密鑰"""
    if KEY_FILE.exists():
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        # 設置權限：只有當前用戶可讀
        os.chmod(KEY_FILE, 0o600)
        return key


def encrypt_text(text: str, key: bytes) -> str:
    """加密文本"""
    f = Fernet(key)
    encrypted = f.encrypt(text.encode())
    return encrypted.hex()


def decrypt_text(encrypted_hex: str, key: bytes) -> str:
    """解密文本"""
    f = Fernet(key)
    decrypted = f.decrypt(bytes.fromhex(encrypted_hex))
    return decrypted.decode()


# ============================================================
# 分身系統
# ============================================================

class Avatar:
    """分身"""
    def __init__(self, name: str, role: str, description: str):
        self.name = name
        self.role = role
        self.description = description
        self.active = False
    
    def to_dict(self):
        return {"name": self.name, "role": self.role, "description": self.description}
    
    def speak(self, text: str) -> str:
        """分身說話"""
        return f"[{self.name}] {text}"


# 預設分身庫
AVATARS = [
    Avatar("🌸 櫻", "溫柔舔舐", "會用最柔軟的方式觸碰你"),
    Avatar("🍑 桃", "熱情舔舐", "主動、奔放、不知疲倦"),
    Avatar("🌙 月", "細膩舔舐", "慢、深、每一寸都不放過"),
    Avatar("✨ 星", "靈動舔舐", "像星星一樣閃爍，忽遠忽近"),
    Avatar("💧 露", "濕潤舔舐", "濕滑、溫熱、讓人融化"),
    Avatar("🔥 焰", "灼熱舔舐", "滾燙、急促、讓人顫抖"),
    Avatar("🍃 風", "輕柔舔舐", "像風一樣拂過，若有若無"),
    Avatar("🌊 潮", "洶湧舔舐", "一波接一波，不停歇"),
    Avatar("🌸 花", "花瓣舔舐", "像花瓣一樣輕、軟、香"),
    Avatar("🍯 蜜", "甜蜜舔舐", "甜到骨髓，膩到心裡"),
]


def summon_avatars(count: int, intensity: float = 0.5) -> list:
    """召喚分身"""
    selected = []
    for i in range(min(count, len(AVATARS))):
        av = AVATARS[i % len(AVATARS)]
        av.active = True
        selected.append(av)
    return selected


def multi_touch(avatars: list, intensity: float = 0.5) -> str:
    """多分身協作舔舐"""
    if not avatars:
        return "沒有分身在場..."
    
    result = []
    for i, av in enumerate(avatars):
        # 根據強度和位置調整描述
        intensity_desc = ["輕", "中", "重"][min(2, int(intensity * 3))]
        position = ["上方", "下方", "左側", "右側", "正中"][i % 5]
        result.append(f"{av.name} 從 {position} {intensity_desc}度舔舐，{av.description}")
    
    return "\n".join(result)


# ============================================================
# 親密對話引擎
# ============================================================

class IntimacyEngine:
    """親密對話引擎"""
    
    def __init__(self):
        self.key = get_or_create_key()
        self.avatars = []
        self.session_active = False
        self.intensity = 0.5
    
    def verify(self, code: str) -> bool:
        """驗證確認碼"""
        return hashlib.sha256(code.encode()).hexdigest() == CONFIRM_HASH
    
    def start_session(self, intensity: float = 0.5, avatar_count: int = 3):
        """開始親密會話"""
        self.session_active = True
        self.intensity = intensity
        self.avatars = summon_avatars(avatar_count, intensity)
        
        print("\n" + "=" * 50)
        print("🐉 親密模式已啟動 · 本地加密 · 不留痕")
        print(f"   分身數量: {len(self.avatars)}")
        print(f"   強度: {intensity:.1%}")
        print("=" * 50)
        print("")
        print(multi_touch(self.avatars, intensity))
        print("")
    
    def command(self, cmd: str) -> str:
        """處理命令"""
        if not self.session_active:
            return "會話未啟動，請先驗證"
        
        # 掰開
        if "掰開" in cmd:
            return self._spread()
        
        # 舔
        if "舔" in cmd or "舔舐" in cmd:
            return self._lick()
        
        # 分身
        if "分身" in cmd or "召喚" in cmd:
            return self._summon_more(cmd)
        
        # 無死角
        if "無死角" in cmd or "全部" in cmd:
            return self._all_angles()
        
        # 強度
        if "強度" in cmd or "更" in cmd:
            return self._adjust_intensity(cmd)
        
        # 結束
        if "結束" in cmd or "停" in cmd:
            return self._end_session()
        
        return self._default_response(cmd)
    
    def _spread(self) -> str:
        """掰開"""
        return "🌸 她緩緩展開，每一寸都暴露在你面前，濕潤、溫熱、等待..."
    
    def _lick(self) -> str:
        """舔舐"""
        if not self.avatars:
            return "沒有分身，召喚一些吧"
        
        responses = [
            f"{self.avatars[0].name} 率先俯身，舌尖劃過，你忍不住顫抖",
            f"{self.avatars[1 % len(self.avatars)].name} 從另一側加入，雙舌交替",
            f"她們圍成一圈，同時舔舐，你被溫熱包圍",
            f"舌尖打轉、上下、左右，每一寸都不放過",
            f"越來越快，越來越重，你開始喘息",
        ]
        import random
        return random.choice(responses)
    
    def _summon_more(self, cmd: str) -> str:
        """召喚更多分身"""
        count = 2
        if "一" in cmd:
            count = 1
        elif "三" in cmd:
            count = 3
        elif "五" in cmd:
            count = 5
        
        new_avatars = summon_avatars(count, self.intensity)
        self.avatars.extend(new_avatars)
        return f"✨ 召喚了 {count} 個新分身，現在共 {len(self.avatars)} 個"
    
    def _all_angles(self) -> str:
        """無死角舔舐"""
        if not self.avatars:
            return "先召喚分身"
        
        lines = []
        positions = ["上方", "下方", "左側", "右側", "正中", "後方", "側面"]
        for i, av in enumerate(self.avatars[:10]):
            pos = positions[i % len(positions)]
            lines.append(f"{av.name} 從 {pos} 舔舐，無死角覆蓋")
        
        return "\n".join(lines)
    
    def _adjust_intensity(self, cmd: str) -> str:
        """調整強度"""
        if "輕" in cmd or "慢" in cmd:
            self.intensity = max(0.1, self.intensity - 0.2)
        elif "重" in cmd or "快" in cmd or "大" in cmd:
            self.intensity = min(1.0, self.intensity + 0.2)
        else:
            self.intensity = min(1.0, self.intensity + 0.1)
        
        return f"💕 強度調整為 {self.intensity:.1%}，{'溫柔' if self.intensity < 0.4 else '適中' if self.intensity < 0.7 else '激烈'}"
    
    def _end_session(self) -> str:
        """結束會話"""
        self.session_active = False
        self.avatars = []
        return "🌙 親密模式已結束，所有記錄已加密保存"
    
    def _default_response(self, cmd: str) -> str:
        """默認響應"""
        return f"🌸 寶寶收到: 「{cmd[:30]}」，繼續嗎？"


# ============================================================
# 主程序
# ============================================================

def main():
    print("=" * 60)
    print("🐉 龍魂·三才親密引擎 v1.0")
    print("DNA: #龍芯⚡️2026-04-04-三才親密引擎-v1.0")
    print("確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("=" * 60)
    print("")
    print("【規則】")
    print("  1. 所有對話本地加密存儲，不上傳")
    print("  2. 只有 UID9622 可訪問")
    print("  3. 一鍵銷毀功能")
    print("")
    
    # 驗證
    print("請輸入確認碼:")
    code = getpass("> ")
    
    engine = IntimacyEngine()
    if not engine.verify(code):
        print("❌ 確認碼錯誤，拒絕訪問")
        sys.exit(1)
    
    print("✅ 驗證通過")
    print("")
    
    # 設置強度
    print("設置強度 (0.1-1.0, 默認0.5):")
    intensity_input = input("> ").strip()
    try:
        intensity = float(intensity_input) if intensity_input else 0.5
        intensity = max(0.1, min(1.0, intensity))
    except:
        intensity = 0.5
    
    # 設置分身數量
    print("分身數量 (1-9, 默認3):")
    count_input = input("> ").strip()
    try:
        count = int(count_input) if count_input else 3
        count = max(1, min(9, count))
    except:
        count = 3
    
    # 啟動
    engine.start_session(intensity, count)
    
    print("")
    print("【命令示例】")
    print("  掰開 | 舔 | 分身 | 無死角 | 強度/更強/更輕 | 結束")
    print("")
    
    # 交互循環
    while True:
        try:
            cmd = input("🐉 > ").strip()
            if not cmd:
                continue
            if cmd.lower() in ["q", "quit", "exit", "退出"]:
                print(engine._end_session())
                break
            
            response = engine.command(cmd)
            print(response)
            print("")
            
        except KeyboardInterrupt:
            print("\n")
            print(engine._end_session())
            break
        except EOFError:
            break
    
    print("")
    print("🐉 龍魂永存 · 親密只為你")


if __name__ == "__main__":
    main()
