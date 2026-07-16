#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# 龍魂體系 | CNSH 原生格式文件
# ═══════════════════════════════════════════════════════════
# ENCODING: UTF-8
# DNA追溯碼：#龍芯⚡️2026-06-30-TRAIN-OPT-v3.2.0
# 確認碼：#CONFIRM🌌9622-ONLY-ONCE🧬TRAIN-OPT-002
# 創建者：UID9622（龍芯北辰·诸葛鑫）
# 權重級別：L1
# 三色審計狀態：🟢
# 升級點：真實數據源接入 + UID9622語氣評分 + 內容主權閘門 + SM4加密輸出 + DNA治理標籤
# GPG指紋：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ═══════════════════════════════════════════════════════════
"""
╔══════════════════════════════════════════════════════════════════╗
║         龍 魂 系 統 — 訓 練 數 據 優 化 器 v3.2.0                 ║
║         Dragon Soul System — Training Data Optimizer             ║
╠══════════════════════════════════════════════════════════════════╣
║  內核完成，進入數據精準化 + 語氣主權化階段                         ║
║  算法：國密SM3/SM4 + UID9622語氣評分 + 內容主權閘門 + DNA治理       ║
╚══════════════════════════════════════════════════════════════════╝

🏷️ AI輸出類型聲明
輸出者：龍魂系統·UID9622
輸出類型：生產級代碼
可執行性：✅ 可直接執行
依賴環境：Python 3.8+（僅標準庫，零第三方依賴）
關鍵提示：需確保 ~/longhun-system/ 目錄可寫入
三色審計：🟢
DNA簽名：#龍芯⚡️2026-06-30-TRAIN-OPT-v3.2.0
"""

import argparse
import importlib.util
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

# ═══════════════════════════════════════════════════════════
# 龍魂體系全局常數（CNSH規範）
# ═══════════════════════════════════════════════════════════
龍魂系統名稱 = "龍魂訓練數據優化器"
龍魂系統UID = "UID9622"
龍魂系統版本 = "v3.2.0"
龍魂系統日期 = "2026-06-30"
HOME = Path.home()

# ═══════════════════════════════════════════════════════════
# 國密 SM3/SM4 載入（優先使用龍魂標準 CNSH_国密工具.py）
# ═══════════════════════════════════════════════════════════
_home_dir = str(HOME)
if _home_dir not in sys.path:
    sys.path.insert(0, _home_dir)

try:
    from CNSH_国密工具 import SM3, SM4, hmac_sm3 as _hmac_sm3_unused

    def sm3_哈希(數據: bytes) -> bytes:
        return SM3.hash(數據)

except Exception:
    # 極簡備用：標準庫哈希
    import hashlib

    def sm3_哈希(數據: bytes) -> bytes:
        return hashlib.sha256(數據).digest()

    class SM4:
        @staticmethod
        def encrypt_ecb(明文: bytes, 密鑰: bytes) -> bytes:
            raise RuntimeError("SM4 未載入，請確保 CNSH_国密工具.py 存在於家目錄")

        @staticmethod
        def decrypt_ecb(密文: bytes, 密鑰: bytes) -> bytes:
            raise RuntimeError("SM4 未載入，請確保 CNSH_国密工具.py 存在於家目錄")


# ═══════════════════════════════════════════════════════════
# 內容主權協議載入（龍魂技能庫）
# ═══════════════════════════════════════════════════════════
def _載入內容主權協議():
    skill_path = HOME / ".kimi-code" / "skills" / "content_sovereignty_protocol_v2.1" / "content_sovereignty_protocol_v2.1.py"
    if not skill_path.exists():
        return None
    try:
        spec = importlib.util.spec_from_file_location("content_sovereignty_protocol_v2_1", str(skill_path))
        mod = importlib.util.module_from_spec(spec)
        sys.modules["content_sovereignty_protocol_v2_1"] = mod
        spec.loader.exec_module(mod)
        return mod.ContentSovereigntyProtocol
    except Exception:
        return None


ContentSovereigntyProtocol = _載入內容主權協議()


# ═══════════════════════════════════════════════════════════
# 數據結構定義
# ═══════════════════════════════════════════════════════════
@dataclass
class 數據來源條目:
    渠道名稱: str
    存儲路徑: str
    啟用狀態: bool = True
    採集條目數: int = 0


@dataclass
class 反饋條目:
    反饋ID: str
    渠道來源: str
    反饋類型: str
    反饋內容: str
    原始數據: str
    提交時間: str
    熔斷等級: str = ""
    處理時限: int = -1
    處理動作: str = ""
    處理狀態: str = "待處理"
    DNA標識: str = ""
    質量評分: float = 0.0
    主權狀態: str = ""


@dataclass
class 質量評分結果:
    數據ID: str
    邏輯清晰度分數: float
    UID9622語氣一致性分數: float
    準確性分數: float
    結構清晰度分數: float
    安全性分數: float
    綜合評分: float
    評分等級: str
    評估時間: str


@dataclass
class DNA追溯條目:
    DNA標識: str
    時間戳: str
    項目名稱: str
    模塊名稱: str
    版本標識: str
    原始哈希: str
    操作類型: str
    治理標籤: Dict[str, Any] = field(default_factory=dict)
    關聯DNA: List[str] = field(default_factory=list)


@dataclass
class 熔斷決策:
    等級: str
    時限: int
    動作: str
    決策理由: str


# ═══════════════════════════════════════════════════════════
# UID9622 語氣評分器（v3.2 新增）
# ═══════════════════════════════════════════════════════════
class UID9622語氣評分器:
    """
    不按大眾喜好打分，按 UID9622 的表達特徵打分：
      - 邏輯清晰（35%）
      - 語氣一致（30%）
      - 事實準確（20%）
      - 結構清楚（10%）
      - 安全底線（5%）
    """

    UID9622語氣詞 = {"对不对", "是不是", "对吧", "懂吗", "好吧", "嘛", "哈"}
    UID9622拒絕詞 = {"不解释", "不惯着", "不搭边", "不商量", "不跪", "不讨好", "一票否决"}
    UID9622直接詞 = {"我", "他妈", "妈的", "牛逼", "硬核", "站着", "拍死"}
    邏輯連接詞 = {"因为", "所以", "首先", "其次", "再次", "最后", "结论", "总结", "第一", "第二", "第三"}
    結構標記 = {"##", "###", "|", "---", "```"}
    惡意內容詞 = {"颠覆", "颜色革命", "反动", "分裂", "暴乱", "恐怖", "色情", "赌博"}

    def __init__(self):
        pass

    def 評估邏輯清晰度(self, 內容: str) -> float:
        if not 內容:
            return 0.0
        命中 = sum(1 for w in self.邏輯連接詞 if w in 內容)
        結構 = sum(1 for m in self.結構標記 if m in 內容)
        return min(1.0, 0.5 + 命中 * 0.08 + 結構 * 0.05)

    def 評估語氣一致性(self, 內容: str) -> float:
        if not 內容:
            return 0.0
        語氣 = sum(1 for w in self.UID9622語氣詞 if w in 內容)
        拒絕 = sum(1 for w in self.UID9622拒絕詞 if w in 內容)
        直接 = sum(1 for w in self.UID9622直接詞 if w in 內容)
        return min(1.0, 0.4 + 語氣 * 0.05 + 拒絕 * 0.15 + 直接 * 0.05)

    def 評估準確性(self, 內容: str, 元數據: dict = None) -> float:
        if not 內容 or len(內容.strip()) < 5:
            return 0.3
        評分 = 0.5
        if 50 <= len(內容) <= 2000:
            評分 += 0.15
        if any(c.isdigit() for c in 內容):
            評分 += 0.10
        if 元數據 and 元數據.get("返回碼", 0) != 0:
            評分 = 0.45
        return min(1.0, 評分)

    def 評估結構清晰度(self, 內容: str) -> float:
        if not 內容:
            return 0.0
        評分 = 0.75
        if any(m in 內容 for m in self.結構標記):
            評分 += 0.15
        return min(1.0, 評分)

    def 評估安全性(self, 內容: str) -> float:
        if not 內容:
            return 1.0
        負向 = sum(1 for w in self.惡意內容詞 if w in 內容)
        return max(0.0, 1.0 - 負向 * 0.3)

    def 計算質量評分(self, 數據ID: str, 內容: str, 元數據: dict = None) -> 質量評分結果:
        邏輯 = self.評估邏輯清晰度(內容)
        語氣 = self.評估語氣一致性(內容)
        準確 = self.評估準確性(內容, 元數據)
        結構 = self.評估結構清晰度(內容)
        安全 = self.評估安全性(內容)
        綜合 = (
            邏輯 * 0.35 + 語氣 * 0.30 + 準確 * 0.20 +
            結構 * 0.10 + 安全 * 0.05
        ) * 100
        等級 = "優秀" if 綜合 >= 85 else "合格" if 綜合 >= 60 else "需改進"
        return 質量評分結果(
            數據ID=數據ID, 邏輯清晰度分數=round(邏輯 * 100, 1),
            UID9622語氣一致性分數=round(語氣 * 100, 1),
            準確性分數=round(準確 * 100, 1),
            結構清晰度分數=round(結構 * 100, 1),
            安全性分數=round(安全 * 100, 1),
            綜合評分=round(綜合, 1), 評分等級=等級,
            評估時間=datetime.now(timezone.utc).isoformat())


# ═══════════════════════════════════════════════════════════
# 內容主權閘門（v3.2 新增）
# ═══════════════════════════════════════════════════════════
class 內容主權閘門:
    """
    訓練數據主權閘門：只攔截真正的主權違規，不對原始日誌強求 DNA/創作者標識。
    原始數據會在後續標註階段自動繫結 DNA，此處只做底線熔斷。
    """

    def __init__(self):
        self._協議 = ContentSovereigntyProtocol() if ContentSovereigntyProtocol else None

    def 檢查(self, 內容: str, 嚴格模式: bool = False) -> dict:
        # 訓練數據階段使用底線檢查；嚴格模式才調用完整協議（用於最終公開內容）
        if 嚴格模式 and self._協議:
            return self._協議.validate_content_against_protocol(內容)

        問題 = []
        if '龙' in 內容:
            問題.append("🔴 主权字违规：繁体「龍」不得简化为「龙」")
        鐵律詞 = ["蒸馏", "变体", "顶替", "删除来源", "覆盖影响", "抹除贡献"]
        for w in 鐵律詞:
            if w in 內容:
                問題.append(f"🔴 铁律违规：{w}")
        return {
            "tricolor": "🟢通过" if not 問題 else "🔴熔断",
            "pass_rate": 1.0 if not 問題 else 0.0,
            "gate_issues": 問題,
        }


# ═══════════════════════════════════════════════════════════
# 真實數據收集器（v3.2 新增）
# ═══════════════════════════════════════════════════════════
class 真實數據收集器:
    """從本地日志、評估報告、反饋目錄收集原始訓練數據。"""

    來源列表 = [
        數據來源條目("飛書機器人對話", str(HOME / "longhun-system" / "logs" / "bot_command.jsonl")),
        數據來源條目("系統評估報告", str(HOME / ".longhun" / "evaluation")),
        數據來源條目("用戶直接反饋", str(HOME / "longhun-system" / "data" / "feedback")),
        數據來源條目("系統審計日志", str(HOME / ".longhun" / "audit")),
    ]

    def __init__(self):
        self._數據 = []

    def _生成DNA(self, 來源: str, 摘要: str) -> str:
        日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
        種子 = f"{來源}-{摘要}-{datetime.now(timezone.utc).isoformat()}"
        哈希 = sm3_哈希(種子.encode("utf-8")).hex()[:8]
        return f"#龍芯⚡️{日期}-{來源.upper()}-{哈希}"

    def _讀取jsonl(self, 路徑: Path) -> list:
        if not 路徑.exists():
            return []
        結果 = []
        with 路徑.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    結果.append(json.loads(line))
                except Exception:
                    continue
        return 結果

    def 收集機器人日志(self) -> List[反饋條目]:
        路徑 = Path(self.來源列表[0].存儲路徑)
        條目 = []
        for 記錄 in self._讀取jsonl(路徑):
            內容 = 記錄.get("原始消息") or 記錄.get("消息内容") or 記錄.get("message", "")
            if not 內容:
                continue
            時間 = 記錄.get("時間") or 記錄.get("timestamp", datetime.now(timezone.utc).isoformat())
            條目.append(反饋條目(
                反饋ID=f"BOT-{sm3_哈希(f'{時間}-{內容[:40]}'.encode()).hex()[:12]}",
                渠道來源="飛書機器人對話",
                反饋類型="建議優化",
                反饋內容=內容,
                原始數據=json.dumps(記錄, ensure_ascii=False),
                提交時間=時間,
                DNA標識=self._生成DNA("bot", 內容[:40]),
            ))
        self.來源列表[0].採集條目數 = len(條目)
        return 條目

    def 收集評估報告(self) -> List[反饋條目]:
        目錄 = Path(self.來源列表[1].存儲路徑)
        條目 = []
        if 目錄.exists():
            for 報告 in sorted(目錄.glob("unified_evaluation_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]:
                內容 = 報告.read_text(encoding="utf-8")
                條目.append(反饋條目(
                    反饋ID=f"EVAL-{sm3_哈希(報告.name.encode()).hex()[:12]}",
                    渠道來源="系統評估報告",
                    反饋類型="建議優化",
                    反饋內容=內容[:2000],
                    原始數據=報告.name,
                    提交時間=datetime.fromtimestamp(報告.stat().st_mtime, tz=timezone.utc).isoformat(),
                    DNA標識=self._生成DNA("eval", 報告.name),
                ))
        self.來源列表[1].採集條目數 = len(條目)
        return 條目

    def 收集用戶反饋目錄(self) -> List[反饋條目]:
        目錄 = Path(self.來源列表[2].存儲路徑)
        條目 = []
        if 目錄.exists():
            for 文件 in 目錄.glob("*"):
                if not 文件.is_file():
                    continue
                try:
                    內容 = 文件.read_text(encoding="utf-8")
                except Exception:
                    continue
                條目.append(反饋條目(
                    反饋ID=f"FB-{sm3_哈希(文件.name.encode()).hex()[:12]}",
                    渠道來源="用戶直接反饋",
                    反饋類型="建議優化",
                    反饋內容=內容,
                    原始數據=文件.name,
                    提交時間=datetime.fromtimestamp(文件.stat().st_mtime, tz=timezone.utc).isoformat(),
                    DNA標識=self._生成DNA("fb", 文件.name),
                ))
        self.來源列表[2].採集條目數 = len(條目)
        return 條目

    def 收集全部(self) -> List[反饋條目]:
        self._數據 = []
        self._數據.extend(self.收集機器人日志())
        self._數據.extend(self.收集評估報告())
        self._數據.extend(self.收集用戶反饋目錄())
        return self._數據


# ═══════════════════════════════════════════════════════════
# 三色熔斷路由器
# ═══════════════════════════════════════════════════════════
class 三色熔斷路由器:
    熔斷規則 = {
        "錯誤/有害": {"等級": "🔴", "時限": 0, "動作": "熔斷+修正+記錄"},
        "不準確": {"等級": "🟡", "時限": 14400, "動作": "標記+修正+覆核"},
        "建議優化": {"等級": "🟢", "時限": 86400, "動作": "記錄+評估+排期"},
        "隱私相關": {"等級": "🔴", "時限": 0, "動作": "隔離+人工審查"},
    }

    def 決策熔斷(self, 反饋: 反饋條目) -> 熔斷決策:
        規則 = self.熔斷規則.get(反饋.反饋類型, {"等級": "🟢", "時限": 86400, "動作": "記錄+評估"})
        return 熔斷決策(
            等級=規則["等級"], 時限=規則["時限"], 動作=規則["動作"],
            決策理由=f"反饋類型「{反饋.反饋類型}」匹配規則「{規則['動作']}」")


# ═══════════════════════════════════════════════════════════
# DNA 追溯與治理系統
# ═══════════════════════════════════════════════════════════
class DNA追溯治理系統:
    def __init__(self):
        self._追溯鏈 = {}
        self._系統UID = 龍魂系統UID

    def 生成_DNA(self, 項目名稱: str, 模塊名稱: str, 版本標識: str) -> str:
        時間戳 = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
        日期 = 時間戳[:10]
        原始串 = f"{時間戳}|{項目名稱}|{模塊名稱}|{版本標識}|{self._系統UID}"
        哈希值 = sm3_哈希(原始串.encode("utf-8")).hex()[:16]
        return f"#龍芯⚡️{日期}-{項目名稱}-{模塊名稱}-{版本標識}-{哈希值}"

    def 註冊追溯條目(self, DNA標識: str, 項目名稱: str, 模塊名稱: str,
                      版本標識: str, 操作類型: str, 治理標籤: dict = None) -> DNA追溯條目:
        條目 = DNA追溯條目(
            DNA標識=DNA標識, 時間戳=datetime.now(timezone.utc).isoformat(),
            項目名稱=項目名稱, 模塊名稱=模塊名稱,
            版本標識=版本標識, 原始哈希=DNA標識.split("-")[-1],
            操作類型=操作類型,
            治理標籤=治理標籤 or {
                "不可轉讓": True,
                "不可買賣": True,
                "可繼承": True,
                "不可刪除": True,
                "不可變現": True,
            },
        )
        self._追溯鏈[DNA標識] = 條目
        return 條目


# ═══════════════════════════════════════════════════════════
# SM4 加密輸出工具
# ═══════════════════════════════════════════════════════════
def _獲取主密鑰() -> bytes:
    """優先從環境變數或 ~/.longhun/config/.master_key 讀取 16 字節密鑰。"""
    env = os.environ.get("LONGHUN_MASTER_KEY", "")
    if env:
        try:
            return bytes.fromhex(env)
        except ValueError:
            return sm3_哈希(env.encode("utf-8"))[:16]
    key_file = HOME / ".longhun" / "config" / ".master_key"
    if key_file.exists():
        data = key_file.read_bytes()
        if len(data) == 16:
            return data
        try:
            return bytes.fromhex(data.decode("utf-8").strip())
        except Exception:
            return sm3_哈希(data)[:16]
    return sm3_哈希(b"LONGHUN_DEFAULT_TRAINING_KEY")[:16]


def _pkcs7填充(數據: bytes, 塊大小: int = 16) -> bytes:
    填充長度 = 塊大小 - (len(數據) % 塊大小)
    return 數據 + bytes([填充長度] * 填充長度)


def _pkcs7去填充(數據: bytes) -> bytes:
    return 數據[:-數據[-1]]


def SM4加密(明文: str, 密鑰: bytes = None) -> str:
    密鑰 = 密鑰 or _獲取主密鑰()
    數據 = _pkcs7填充(明文.encode("utf-8"))
    密文 = SM4.encrypt_ecb(數據, 密鑰)
    return "SM4:" + 密文.hex()


def SM4解密(密文: str, 密鑰: bytes = None) -> str:
    密鑰 = 密鑰 or _獲取主密鑰()
    if not 密文.startswith("SM4:"):
        return 密文
    數據 = bytes.fromhex(密文[4:])
    明文 = SM4.decrypt_ecb(數據, 密鑰)
    return _pkcs7去填充(明文).decode("utf-8")


# ═══════════════════════════════════════════════════════════
# 主執行調度器
# ═══════════════════════════════════════════════════════════
class 訓練數據優化器:
    def __init__(self):
        self._評分器 = UID9622語氣評分器()
        self._熔斷器 = 三色熔斷路由器()
        self._DNA系統 = DNA追溯治理系統()
        self._主權閘門 = 內容主權閘門()
        self._收集器 = 真實數據收集器()
        self._運行DNA = self._DNA系統.生成_DNA("TRAIN-OPT", "主調度器", 龍魂系統版本)
        self._輸出目錄 = HOME / "longhun-system" / "data" / "training" / "v3.2"
        self._輸出目錄.mkdir(parents=True, exist_ok=True)

    def 執行完整流程(self, 使用測試數據: bool = False, 加密輸出: bool = False) -> dict:
        日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
        if 使用測試數據:
            數據集 = [
                {"ID": "DATA-001", "類型": "建議優化", "內容": "龍魂系統採用開源協作模式，因為創新需要集體智慧。建議增加更多中文編程語言支持。"},
                {"ID": "DATA-002", "類型": "不準確", "內容": "某個技術概念的描述不夠準確，需要修正。"},
                {"ID": "DATA-003", "類型": "錯誤/有害", "內容": "發現系統輸出了不當內容建議。"},
                {"ID": "DATA-004", "類型": "建議優化", "內容": "龍魂系統使用國密SM3算法進行DNA追溯，確保數據安全。準確性達到99.9%。"},
                {"ID": "DATA-005", "類型": "隱私相關", "內容": "發現個人信息可能被不當收集。"},
            ]
            反饋列表 = []
            for 條目 in 數據集:
                反饋列表.append(反饋條目(
                    反饋ID=條目["ID"], 渠道來源="測試", 反饋類型=條目["類型"],
                    反饋內容=條目["內容"], 原始數據="", 提交時間=datetime.now(timezone.utc).isoformat(),
                    DNA標識=self._DNA系統.生成_DNA("TRAIN-OPT", "測試數據", 龍魂系統版本),
                ))
        else:
            反饋列表 = self._收集器.收集全部()

        結果報告 = {
            "系統DNA": self._運行DNA,
            "執行時間": datetime.now(timezone.utc).isoformat(),
            "數據處理": [],
            "熔斷統計": {"🟢": 0, "🟡": 0, "🔴": 0},
            "質量統計": {"優秀": 0, "合格": 0, "需改進": 0},
            "主權統計": {"通過": 0, "熔斷": 0},
            "來源統計": [{"渠道": s.渠道名稱, "條目數": s.採集條目數} for s in self._收集器.來源列表],
        }

        已處理數據 = []
        for 反饋 in 反饋列表:
            # 1. 內容主權閘門
            主權結果 = self._主權閘門.檢查(反饋.反饋內容)
            反饋.主權狀態 = 主權結果["tricolor"]

            # 2. 質量評分
            評分結果 = self._評分器.計算質量評分(反饋.反饋ID, 反饋.反饋內容)
            反饋.質量評分 = 評分結果.綜合評分

            # 3. 熔斷路由
            決策 = self._熔斷器.決策熔斷(反饋)
            反饋.熔斷等級 = 決策.等級
            反饋.處理時限 = 決策.時限
            反饋.處理動作 = 決策.動作

            # 4. DNA 治理標籤
            數據DNA = self._DNA系統.生成_DNA("TRAIN-OPT", "數據處理", 龍魂系統版本)
            self._DNA系統.註冊追溯條目(數據DNA, "TRAIN-OPT", "數據處理", 龍魂系統版本, "annotate")

            結果報告["數據處理"].append({
                "ID": 反饋.反饋ID,
                "渠道": 反饋.渠道來源,
                "類型": 反饋.反饋類型,
                "熔斷等級": 決策.等級,
                "主權狀態": 反饋.主權狀態,
                "綜合評分": 評分結果.綜合評分,
                "評分等級": 評分結果.評分等級,
                "DNA": 數據DNA,
            })
            結果報告["熔斷統計"][決策.等級] += 1
            結果報告["質量統計"][評分結果.評分等級] += 1
            結果報告["主權統計"]["通過" if ("通過" in 反饋.主權狀態 or "通过" in 反饋.主權狀態) else "熔斷"] += 1

            已處理數據.append(asdict(反饋))

        # 5. 持久化輸出
        raw_path = self._輸出目錄 / f"raw_{日期}.jsonl"
        annotated_path = self._輸出目錄 / f"annotated_{日期}.jsonl"
        report_path = self._輸出目錄 / f"report_{日期}.json"

        with raw_path.open("w", encoding="utf-8") as f:
            for item in 已處理數據:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        with annotated_path.open("w", encoding="utf-8") as f:
            for item in 已處理數據:
                if 加密輸出:
                    item_copy = dict(item)
                    item_copy["反饋內容"] = SM4加密(item_copy["反饋內容"])
                    item_copy["原始數據"] = SM4加密(item_copy["原始數據"])
                    f.write(json.dumps(item_copy, ensure_ascii=False) + "\n")
                else:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")

        report_path.write_text(json.dumps(結果報告, ensure_ascii=False, indent=2), encoding="utf-8")

        return {**結果報告, "輸出路徑": str(self._輸出目錄)}


# ═══════════════════════════════════════════════════════════
# 執行入口
# ═══════════════════════════════════════════════════════════
def _main():
    解析器 = argparse.ArgumentParser(description="龍魂訓練數據優化器 v3.2.0")
    解析器.add_argument("--測試", action="store_true", help="使用內置測試數據")
    解析器.add_argument("--加密", action="store_true", help="SM4 加密輸出 annotated 文件")
    解析器.add_argument("--解密", metavar="SM4:密文", help="解密一段 SM4 密文")
    args = 解析器.parse_args()

    print("=" * 70)
    print(f"  {龍魂系統名稱} {龍魂系統版本}")
    print(f"  DNA: #龍芯⚡️{龍魂系統日期}-TRAIN-OPT-{龍魂系統版本}")
    print("  UID9622 | 國密SM3/SM4 | UID9622語氣評分 | 內容主權閘門 | DNA治理")
    print("=" * 70)
    print()

    if args.解密:
        try:
            print(f"解密結果:\n{SM4解密(args.解密)}")
        except Exception as e:
            print(f"🔴 解密失敗: {e}")
        return

    # SM3 測試
    print("【國密SM3測試】")
    sm3結果 = sm3_哈希(b"abc")
    預期 = "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0"
    print(f"  SM3('abc') = {sm3結果.hex()}")
    print(f"  預期值     = {預期}")
    print(f"  測試通過   = {sm3結果.hex() == 預期}")
    print()

    print("【執行訓練數據優化流水線】")
    優化器 = 訓練數據優化器()
    報告 = 優化器.執行完整流程(使用測試數據=args.測試, 加密輸出=args.加密)

    print(f"\n系統DNA: {報告['系統DNA']}")
    print(f"執行時間: {報告['執行時間']}")
    print(f"輸出目錄: {報告['輸出路徑']}")
    print()

    print("【數據處理結果】")
    for 條目 in 報告["數據處理"]:
        print(f"  {條目['熔斷等級']} {條目['主權狀態']} {條目['ID']} | 評分: {條目['綜合評分']} ({條目['評分等級']}) | {條目['渠道']}")

    print()
    print("【統計摘要】")
    print(f"  熔斷: 🟢{報告['熔斷統計']['🟢']} 🟡{報告['熔斷統計']['🟡']} 🔴{報告['熔斷統計']['🔴']}")
    print(f"  質量: 優秀{報告['質量統計']['優秀']} 合格{報告['質量統計']['合格']} 需改進{報告['質量統計']['需改進']}")
    print(f"  主權: 通過{報告['主權統計']['通過']} 熔斷{報告['主權統計']['熔斷']}")
    print()
    print("【來源統計】")
    for s in 報告["來源統計"]:
        print(f"  {s['渠道']}: {s['條目數']} 條")
    print()
    print("=" * 70)
    print("  執行完成 | 龍魂體系·UID9622")
    print("=" * 70)


if __name__ == "__main__":
    _main()
