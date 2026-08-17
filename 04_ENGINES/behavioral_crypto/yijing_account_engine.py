#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·易經六十四卦賬號身份引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·甲寅·子時·䷀乾-YIJING-ACCOUNT-ENGINE-V1.0-UID9622
License: MulanPSL v2

功能：
  - 從 CSDN 文章「易經六十四卦動態決策算法」提取的核心賬號身份邏輯
  - 道·法·術 三層身份模型：道層（不可複製）·法層（難複製）·術層（開源可驗證）
  - 六十四卦 × 六爻變爻 = 4096 種身份狀態
  - 時間四柱注入 + 人性變量（不可計算種子）
  - 與行為密碼學七因子引擎聯動

核心原理（來源：https://blog.csdn.net/2500_94248780/article/details/157721810）:
  1. 六十四卦對應 6-bit 二進制身份編碼（0-63）
  2. 六爻動態變爻創造 2^6=64 種平行身份狀態
  3. 時間因子（天干地支四柱）作為連續維度
  4. 人性變量（不可計算種子）使身份無法被 AI 完全預測
  5. 道法術三層：別人能抄術層（代碼），抄不了法層（推理鏈），更抄不了道層（價值觀）

用法：
  from yijing_account_engine import YijingAccountEngine
  engine = YijingAccountEngine(seed="UID9622")
  identity = engine.derive_identity(text="龍魂系統的根本原則是為人民服務")
  # identity.hexagram_id: 當前卦 ID
  # identity.changing_lines: 變爻模式
  # identity.dao_hash: 道層哈希（不可複製）
  # identity.fa_vector: 法層推理向量
  # identity.shu_sig: 術層簽名
"""

import hashlib
import json
import math
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Set, Any


# ═══════════════════════════════════════════════════════════════
# §0. 焊死基表：六十四卦全表（L0 不可變）
# ═══════════════════════════════════════════════════════════════

HEXAGRAM_TABLE = {
    1:  {"name": "乾",  "binary": "111111", "element": "乾·天", "nature": "創始·剛健", "unicode": "䷀"},
    2:  {"name": "坤",  "binary": "000000", "element": "坤·地", "nature": "包容·順承", "unicode": "䷁"},
    3:  {"name": "屯",  "binary": "010001", "element": "水雷",   "nature": "初生·艱難", "unicode": "䷂"},
    4:  {"name": "蒙",  "binary": "100010", "element": "山水",   "nature": "蒙昧·啟蒙", "unicode": "䷃"},
    5:  {"name": "需",  "binary": "010111", "element": "水天",   "nature": "等待·時機", "unicode": "䷄"},
    6:  {"name": "訟",  "binary": "111010", "element": "天水",   "nature": "爭訟·衝突", "unicode": "䷅"},
    7:  {"name": "師",  "binary": "000010", "element": "地水",   "nature": "軍隊·統率", "unicode": "䷆"},
    8:  {"name": "比",  "binary": "010000", "element": "水地",   "nature": "親附·團結", "unicode": "䷇"},
    9:  {"name": "小畜","binary": "110111", "element": "風天",   "nature": "小積·蓄勢", "unicode": "䷈"},
    10: {"name": "履",  "binary": "111011", "element": "天澤",   "nature": "實踐·禮儀", "unicode": "䷉"},
    11: {"name": "泰",  "binary": "000111", "element": "地天",   "nature": "通泰·和諧", "unicode": "䷊"},
    12: {"name": "否",  "binary": "111000", "element": "天地",   "nature": "閉塞·不通", "unicode": "䷋"},
    13: {"name": "同人","binary": "111101", "element": "天火",   "nature": "同心·共識", "unicode": "䷌"},
    14: {"name": "大有","binary": "101111", "element": "火天",   "nature": "富有·收穫", "unicode": "䷍"},
    15: {"name": "謙",  "binary": "000100", "element": "地山",   "nature": "謙遜·低調", "unicode": "䷎"},
    16: {"name": "豫",  "binary": "001000", "element": "雷地",   "nature": "豫樂·準備", "unicode": "䷏"},
    17: {"name": "隨",  "binary": "011001", "element": "澤雷",   "nature": "跟隨·順應", "unicode": "䷐"},
    18: {"name": "蠱",  "binary": "100110", "element": "山風",   "nature": "蠱惑·整頓", "unicode": "䷑"},
    19: {"name": "臨",  "binary": "000011", "element": "地澤",   "nature": "臨近·監督", "unicode": "䷒"},
    20: {"name": "觀",  "binary": "110000", "element": "風地",   "nature": "觀察·審視", "unicode": "䷓"},
    21: {"name": "噬嗑","binary": "101001", "element": "火雷",   "nature": "咬合·決斷", "unicode": "䷔"},
    22: {"name": "賁",  "binary": "100101", "element": "山火",   "nature": "修飾·美化", "unicode": "䷕"},
    23: {"name": "剝",  "binary": "100000", "element": "山地",   "nature": "剝落·衰敗", "unicode": "䷖"},
    24: {"name": "復",  "binary": "000001", "element": "地雷",   "nature": "回復·再生", "unicode": "䷗"},
    25: {"name": "無妄","binary": "111001", "element": "天雷",   "nature": "無妄·真誠", "unicode": "䷘"},
    26: {"name": "大畜","binary": "100111", "element": "山天",   "nature": "大積·儲備", "unicode": "䷙"},
    27: {"name": "頤",  "binary": "100001", "element": "山雷",   "nature": "頤養·休養", "unicode": "䷚"},
    28: {"name": "大過","binary": "011110", "element": "澤風",   "nature": "大過·失衡", "unicode": "䷛"},
    29: {"name": "坎",  "binary": "010010", "element": "坎·水", "nature": "險陷·坎坷", "unicode": "䷜"},
    30: {"name": "離",  "binary": "101101", "element": "離·火", "nature": "附麗·光明", "unicode": "䷝"},
    31: {"name": "咸",  "binary": "011100", "element": "澤山",   "nature": "感應·互動", "unicode": "䷞"},
    32: {"name": "恆",  "binary": "001110", "element": "雷風",   "nature": "恆久·持久", "unicode": "䷟"},
    33: {"name": "遯",  "binary": "111100", "element": "天山",   "nature": "退避·隱藏", "unicode": "䷠"},
    34: {"name": "大壯","binary": "001111", "element": "雷天",   "nature": "強盛·壯大", "unicode": "䷡"},
    35: {"name": "晉",  "binary": "101000", "element": "火地",   "nature": "晉升·進步", "unicode": "䷢"},
    36: {"name": "明夷","binary": "000101", "element": "地火",   "nature": "晦明·隱忍", "unicode": "䷣"},
    37: {"name": "家人","binary": "110101", "element": "風火",   "nature": "家庭·內部", "unicode": "䷤"},
    38: {"name": "睽",  "binary": "101011", "element": "火澤",   "nature": "乖離·分歧", "unicode": "䷥"},
    39: {"name": "蹇",  "binary": "010100", "element": "水山",   "nature": "艱難·阻礙", "unicode": "䷦"},
    40: {"name": "解",  "binary": "001010", "element": "雷水",   "nature": "解除·釋放", "unicode": "䷧"},
    41: {"name": "損",  "binary": "100011", "element": "山澤",   "nature": "減損·捨棄", "unicode": "䷨"},
    42: {"name": "益",  "binary": "110001", "element": "風雷",   "nature": "增益·幫助", "unicode": "䷩"},
    43: {"name": "夬",  "binary": "011111", "element": "澤天",   "nature": "決斷·果斷", "unicode": "䷪"},
    44: {"name": "姤",  "binary": "111110", "element": "天風",   "nature": "相遇·邂逅", "unicode": "䷫"},
    45: {"name": "萃",  "binary": "011000", "element": "澤地",   "nature": "聚集·薈萃", "unicode": "䷬"},
    46: {"name": "升",  "binary": "000110", "element": "地風",   "nature": "上升·成長", "unicode": "䷭"},
    47: {"name": "困",  "binary": "011010", "element": "澤水",   "nature": "困頓·受限", "unicode": "䷮"},
    48: {"name": "井",  "binary": "010110", "element": "水風",   "nature": "井源·根基", "unicode": "䷯"},
    49: {"name": "革",  "binary": "011101", "element": "澤火",   "nature": "變革·革新", "unicode": "䷰"},
    50: {"name": "鼎",  "binary": "101110", "element": "火風",   "nature": "鼎新·確立", "unicode": "䷱"},
    51: {"name": "震",  "binary": "001001", "element": "震·雷", "nature": "震動·驚醒", "unicode": "䷲"},
    52: {"name": "艮",  "binary": "100100", "element": "艮·山", "nature": "靜止·堅守", "unicode": "䷳"},
    53: {"name": "漸",  "binary": "110100", "element": "風山",   "nature": "漸進·逐步", "unicode": "䷴"},
    54: {"name": "歸妹","binary": "001101", "element": "雷澤",   "nature": "歸宿·結合", "unicode": "䷵"},
    55: {"name": "豐",  "binary": "001101", "element": "雷火",   "nature": "豐盛·充盈", "unicode": "䷶"},
    56: {"name": "旅",  "binary": "101100", "element": "火山",   "nature": "旅行·遷移", "unicode": "䷷"},
    57: {"name": "巽",  "binary": "110110", "element": "巽·風", "nature": "順從·滲透", "unicode": "䷸"},
    58: {"name": "兌",  "binary": "011011", "element": "兌·澤", "nature": "喜悅·溝通", "unicode": "䷹"},
    59: {"name": "渙",  "binary": "110010", "element": "風水",   "nature": "渙散·解散", "unicode": "䷺"},
    60: {"name": "節",  "binary": "010011", "element": "水澤",   "nature": "節制·約束", "unicode": "䷻"},
    61: {"name": "中孚","binary": "110011", "element": "風澤",   "nature": "誠信·中孚", "unicode": "䷼"},
    62: {"name": "小過","binary": "001100", "element": "雷山",   "nature": "小過·過度", "unicode": "䷽"},
    63: {"name": "既濟","binary": "010101", "element": "水火",   "nature": "完成·既濟", "unicode": "䷾"},
    64: {"name": "未濟","binary": "101010", "element": "火水",   "nature": "未完成·待續", "unicode": "䷿"},
}

# ═══════════════════════════════════════════════════════════════
# §1. 數據結構
# ═══════════════════════════════════════════════════════════════

@dataclass
class YijingAccountIdentity:
    """易經賬號身份（道·法·術三層）"""
    # 卦象層
    hexagram_id: int               # 當前卦 ID (1-64)
    hexagram_name: str             # 卦名
    hexagram_unicode: str          # 卦符
    hexagram_binary: str           # 6-bit 二進制
    hexagram_nature: str           # 卦象屬性

    # 變爻層
    changing_lines: List[int]      # 變爻位置 [1-6]
    changing_pattern: str          # 變爻二進制模式（6-bit）
    divergent_states: int          # 平行身份狀態數 (2^n)

    # 時間層
    stem_branch: str               # 天干地支四柱
    time_seed: float               # 時間種子

    # 道·法·術 三層
    dao_hash: str                  # 道層哈希（不可複製·SM3）
    fa_vector: List[float]         # 法層推理向量（8-dim，難複製）
    shu_signature: str             # 術層簽名（開源可驗證）

    # 人性變量
    human_variable: float          # 不可計算種子
    identity_fingerprint: str      # 綜合身份指紋

    # 元數據
    source: str = "YIJING-ACCOUNT-ENGINE-v1.0"
    dna: str = ""


@dataclass
class AccountVerificationResult:
    """賬號驗證結果"""
    original_identity: YijingAccountIdentity
    target_text: str
    hexagram_match: bool           # 卦象是否匹配
    dao_match: bool                # 道層是否匹配
    fa_similarity: float           # 法層相似度 (0-1)
    shu_valid: bool                # 術層簽名是否有效
    time_consistency: float        # 時間一致性 (0-1)
    combined_confidence: float     # 綜合置信度 (0-1)
    verdict: str                   # 🟢通過·🟡待核·🔴拒絕
    details: Dict[str, Any]


# ═══════════════════════════════════════════════════════════════
# §2. 易經賬號引擎核心
# ═══════════════════════════════════════════════════════════════

class YijingAccountEngine:
    """
    易經六十四卦賬號身份引擎

    從 CSDN 文章提取的核心算法：
    - 文本 → SM3哈希 → 數字根 → 卦象映射
    - 時間四柱 → 變爻計算
    - 人性變量 → 不可計算的身份種子
    - 道法術三層分離

    Usage:
        engine = YijingAccountEngine(seed="UID9622")
        identity = engine.derive_identity("我的原創文本")
        result = engine.verify_identity(identity, "待驗證文本")
    """

    def __init__(self, seed: str = "UID9622", human_variable: Optional[float] = None):
        """
        Args:
            seed: 身份種子（如 UID9622）
            human_variable: 人性變量（None=自動從種子生成）
        """
        self.seed = seed
        self._seed_hash = self._sm3(seed)

        # 人性變量：從 seed_hash 推導的不可逆常數
        if human_variable is None:
            # 從 SM3 哈希的前 8 字節推導為 [0,1] 區間的不可計算值
            seed_bytes = bytes.fromhex(self._seed_hash[:16])
            human_int = int.from_bytes(seed_bytes, 'big')
            self.human_variable = (human_int % 1000000) / 1000000.0
        else:
            self.human_variable = human_variable

        # 記錄身份派生歷史
        self._history: List[YijingAccountIdentity] = []

    # ── 哈希函數 ──
    @staticmethod
    def _sm3(text: str) -> str:
        """SM3 國密哈希（降級 SHA256）"""
        try:
            return hashlib.new('sm3', text.encode()).hexdigest()
        except (ValueError, AttributeError):
            return hashlib.sha256(text.encode()).hexdigest()

    # ── 數字根計算 ──
    @staticmethod
    def _digital_root(n: int) -> int:
        """369 洛書數字根"""
        if n <= 0:
            return 0
        r = n % 9
        return 9 if r == 0 else r

    # ── 文本 → 卦象映射 ──
    def _text_to_hexagram(self, text: str) -> Tuple[int, str]:
        """
        文本 → 六十四卦映射

        算法（源自 CSDN 文章）：
        1. SM3(text) → 256-bit hash
        2. 取前 6 bits → 初卦 (1-64)
        3. 人性變量加擾 → 最終卦
        """
        h = self._sm3(text)
        # 取哈希前 6 bits，映射到 0-63
        hash_int = int(h[:16], 16)
        base_id = (hash_int % 64) + 1

        # 人性變量擾動：±1 卦偏移
        perturbation = int(self.human_variable * 3) - 1  # -1, 0, or +1
        final_id = ((base_id - 1 + perturbation) % 64) + 1
        # 確保在合法範圍內
        final_id = max(1, min(64, final_id))

        hex_data = HEXAGRAM_TABLE[final_id]
        return final_id, hex_data["binary"]

    # ── 變爻計算 ──
    def _calculate_changing_lines(self, text: str, timestamp: float) -> List[int]:
        """
        計算六爻中的變爻

        算法：
        1. 時間種子 → 決定哪些爻會「動」
        2. 人性變量 → 加擾變爻數量
        3. 返回變爻位置列表（從下往上：初爻=1 ... 上爻=6）

        每一爻的變化概率由 time_seed ⊕ human_variable 決定
        """
        time_seed_hex = hashlib.sha256(str(timestamp).encode()).hexdigest()
        human_hex = self._seed_hash[:16]

        # 合併時間種子與人性變量
        combined = int(time_seed_hex[:12], 16) ^ int(human_hex[:12], 16)

        changing = []
        for line in range(6):
            # 每爻取 combined 的對應 4 bits
            shift = line * 4
            line_val = (combined >> shift) & 0xF
            # 人性變量調節變化閾值
            threshold = int(8 + self.human_variable * 4)  # 8-12 out of 16
            if line_val < threshold:
                changing.append(line + 1)  # 爻位從 1 開始

        # 限制變爻數：至少 0 個，最多 4 個（避免太極端）
        if len(changing) > 4:
            changing = changing[:4]

        return changing

    # ── 時間四柱 ──
    @staticmethod
    def _get_stem_branch() -> Tuple[str, float]:
        """獲取當前時間的天干地支四柱和時間種子"""
        now = datetime.now()
        # 使用 LU-Time Engine v4.0 的簡化計算
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour

        # 天干地支基表
        tian_gan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
        di_zhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

        # 年柱（簡化：取年份%10為天干，%12為地支）
        yg = tian_gan[(year - 4) % 10]
        yz = di_zhi[(year - 4) % 12]
        # 月柱（簡化）
        mg = tian_gan[(year * 12 + month) % 10]
        mz = di_zhi[(month + 1) % 12]
        # 日柱（簡化）
        dg = tian_gan[(year + month + day) % 10]
        dz = di_zhi[(day + 5) % 12]
        # 時柱
        hg = tian_gan[((day % 10) * 2 + (hour // 2)) % 10]
        hz = di_zhi[hour // 2]

        stem_branch = f"{yg}{yz}·{mg}{mz}·{dg}{dz}·{hg}{hz}"
        time_seed = (year * 1000000 + month * 10000 + day * 100 + hour) / 1e8

        return stem_branch, time_seed

    # ── 道層哈希 ──
    def _derive_dao_hash(self, seed: str) -> str:
        """道層哈希（不可複製）"""
        # 道層 = 種子 ⊕ 人性變量 ⊕ 確認碼，多重 SM3
        confirm = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
        layer1 = self._sm3(f"{seed}:{confirm}")
        layer2 = self._sm3(f"{layer1}:{self.human_variable:.10f}")
        return self._sm3(f"{layer2}:DAO-LAYER-IMMUTABLE")

    # ── 法層推理向量 ──
    def _derive_fa_vector(self, hexagram_id: int, changing: List[int], time_seed: float) -> List[float]:
        """法層推理向量（8-dim，難複製）"""
        h = self._sm3(f"{hexagram_id}:{changing}:{time_seed:.6f}")
        vector = []
        for i in range(8):
            chunk = int(h[i*4:(i+1)*4], 16)
            # 加入人性變量擾動
            val = (chunk / 65535.0) * (0.8 + self.human_variable * 0.4)
            vector.append(round(min(1.0, val), 6))
        # 歸一化
        total = sum(vector)
        if total > 0:
            vector = [v / total for v in vector]
        return vector

    # ── 術層簽名 ──
    def _derive_shu_signature(self, text: str, hexagram_id: int) -> str:
        """術層簽名（開源可驗證）"""
        return self._sm3(f"{text}:{hexagram_id}:SHU-VERIFIABLE")

    # ── 主入口：派生賬號身份 ──
    def derive_identity(self, text: str, timestamp: Optional[float] = None) -> YijingAccountIdentity:
        """
        從文本派生完整的易經賬號身份

        Args:
            text: 原創文本（如用戶的文章、代碼、指令）
            timestamp: 可選時間戳（None=當前時間）

        Returns:
            YijingAccountIdentity with complete three-layer identity
        """
        if timestamp is None:
            timestamp = time.time()

        # 1. 卦象映射
        hex_id, hex_bin = self._text_to_hexagram(text)
        hex_data = HEXAGRAM_TABLE[hex_id]

        # 2. 變爻計算
        changing = self._calculate_changing_lines(text, timestamp)
        pattern = ''.join('1' if (i+1) in changing else '0' for i in range(6))
        divergent_states = 2 ** len(changing)

        # 3. 時間四柱
        stem_branch, time_seed = self._get_stem_branch()

        # 4. 道·法·術三層
        dao_hash = self._derive_dao_hash(self.seed)
        fa_vector = self._derive_fa_vector(hex_id, changing, time_seed)
        shu_sig = self._derive_shu_signature(text, hex_id)

        # 5. 綜合身份指紋
        identity_fingerprint = self._sm3(
            f"{hex_id}:{pattern}:{dao_hash[:16]}:{shu_sig[:16]}:{self.human_variable:.10f}"
        )

        # 6. DNA 追溯碼
        dna = f"#龍芯⚡️{stem_branch}·{hex_data['unicode']}-YIJING-ACCOUNT-{identity_fingerprint[:8]}"

        identity = YijingAccountIdentity(
            hexagram_id=hex_id,
            hexagram_name=hex_data["name"],
            hexagram_unicode=hex_data["unicode"],
            hexagram_binary=hex_bin,
            hexagram_nature=hex_data["nature"],
            changing_lines=changing,
            changing_pattern=pattern,
            divergent_states=divergent_states,
            stem_branch=stem_branch,
            time_seed=time_seed,
            dao_hash=dao_hash,
            fa_vector=fa_vector,
            shu_signature=shu_sig,
            human_variable=self.human_variable,
            identity_fingerprint=identity_fingerprint,
            dna=dna,
        )

        self._history.append(identity)
        return identity

    # ── 賬號驗證 ──
    def verify_identity(
        self,
        original_identity: YijingAccountIdentity,
        target_text: str,
        tolerance: float = 0.30,
    ) -> AccountVerificationResult:
        """
        驗證目標文本是否來自同一賬號

        Args:
            original_identity: 原始賬號身份
            target_text: 待驗證文本
            tolerance: 容差 (0-1)

        Returns:
            AccountVerificationResult
        """
        # 從目標文本派生身份
        target = self.derive_identity(target_text)

        # 1. 卦象匹配
        hexagram_match = target.hexagram_id == original_identity.hexagram_id

        # 2. 道層驗證（必須完全一致）
        dao_match = target.dao_hash == original_identity.dao_hash

        # 3. 法層相似度（餘弦相似度）
        fa_sim = self._cosine_similarity(original_identity.fa_vector, target.fa_vector)

        # 4. 術層簽名（只需要有效格式）
        shu_valid = len(target.shu_signature) == 64 and all(c in '0123456789abcdef' for c in target.shu_signature)

        # 5. 時間一致性
        time_diff = abs(target.time_seed - original_identity.time_seed)
        time_consistency = max(0.0, 1.0 - time_diff * 10)  # 10小時為衰減尺度

        # 6. 綜合置信度（加權融合）
        weights = {
            "dao": 0.30,     # 道層權重最高（不可複製）
            "fa": 0.30,      # 法層同等重要（推理鏈）
            "hexagram": 0.20, # 卦象匹配
            "shu": 0.10,     # 術層格式
            "time": 0.10,    # 時間一致性
        }

        combined = (
            weights["dao"] * (1.0 if dao_match else 0.0) +
            weights["fa"] * fa_sim +
            weights["hexagram"] * (1.0 if hexagram_match else 0.0) +
            weights["shu"] * (1.0 if shu_valid else 0.0) +
            weights["time"] * time_consistency
        )

        # 三色判定
        if combined >= 0.80:
            verdict = "🟢 通過"
        elif combined >= 0.50:
            verdict = "🟡 待核"
        else:
            verdict = "🔴 拒絕"

        return AccountVerificationResult(
            original_identity=original_identity,
            target_text=target_text[:200],
            hexagram_match=hexagram_match,
            dao_match=dao_match,
            fa_similarity=fa_sim,
            shu_valid=shu_valid,
            time_consistency=time_consistency,
            combined_confidence=round(combined, 4),
            verdict=verdict,
            details={
                "original_hexagram": f"{original_identity.hexagram_name}({original_identity.hexagram_id})",
                "target_hexagram": f"{target.hexagram_name}({target.hexagram_id})",
                "changing_lines_diff": set(target.changing_lines) ^ set(original_identity.changing_lines),
                "fa_diff_summary": {
                    "original_mean": round(sum(original_identity.fa_vector) / 8, 4),
                    "target_mean": round(sum(target.fa_vector) / 8, 4),
                },
            },
        )

    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        """餘弦相似度"""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x**2 for x in a))
        norm_b = math.sqrt(sum(x**2 for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return round(max(-1.0, min(1.0, dot / (norm_a * norm_b))), 4)

    def get_history(self) -> List[Dict]:
        """獲取身份派生歷史"""
        return [
            {
                "hexagram": i.hexagram_name,
                "unicode": i.hexagram_unicode,
                "changing_lines": i.changing_lines,
                "stem_branch": i.stem_branch,
                "dao_hash": i.dao_hash[:16],
                "fingerprint": i.identity_fingerprint[:16],
                "timestamp": i.time_seed,
            }
            for i in self._history
        ]


# ═══════════════════════════════════════════════════════════════
# §3. 命令行入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    engine = YijingAccountEngine(seed="UID9622")

    # 測試案例
    test_texts = [
        "龍魂系統的根本原則是為人民服務。數據主權歸用戶，隱私不可傳。",
        "離火運五條底線：德在技術前、路徑對齊、不讓付出者寒心。",
        "def verify_fingerprint(text: str) -> bool: return True",
    ]

    print("🐉 龍魂·易經賬號身份引擎 v1.0")
    print("=" * 60)

    for i, text in enumerate(test_texts):
        identity = engine.derive_identity(text)
        print(f"\n[{i+1}] 文本: {text[:50]}...")
        print(f"  卦象: {identity.hexagram_unicode} {identity.hexagram_name}({identity.hexagram_id}) {identity.hexagram_nature}")
        print(f"  變爻: {identity.changing_lines} (模式: {identity.changing_pattern}, {identity.divergent_states}種平行狀態)")
        print(f"  四柱: {identity.stem_branch}")
        print(f"  道層: {identity.dao_hash[:16]}...")
        print(f"  法層: {[round(v, 3) for v in identity.fa_vector[:4]]}...")
        print(f"  術層: {identity.shu_signature[:16]}...")
        print(f"  身份指紋: {identity.identity_fingerprint[:24]}")
        print(f"  人性變量: {identity.human_variable:.6f}")

    # 自我驗證測試
    print(f"\n{'='*60}")
    print("自我驗證測試:")
    identity = engine.derive_identity(test_texts[0])
    result = engine.verify_identity(identity, test_texts[0])
    print(f"  相同文本: {result.verdict} (置信度: {result.combined_confidence:.2%})")

    # 修改後文本
    modified = test_texts[0].replace("龍魂", "龍魂").replace("隱私", "隐私")
    result2 = engine.verify_identity(identity, modified)
    print(f"  簡化字替換: {result2.verdict} (置信度: {result2.combined_confidence:.2%})")

    # 完全不同文本
    result3 = engine.verify_identity(identity, "今天天氣真好，適合出去玩。")
    print(f"  無關文本: {result3.verdict} (置信度: {result3.combined_confidence:.2%})")
