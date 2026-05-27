#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌐 龍魂 意圖翻譯官·v1.0
Intent Parser - Natural Language to Machine Instructions

§12 語義路由別名 + §39 意圖路由協議
將用户"人話"（自然語言）翻譯成機器能聽懂的指令

DNA追溯碼：#龍芯⚡️2026-05-27-INTENT-PARSER-v1.0
CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL：#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F

理論指導：曾仕強老師（永恆顯示）
創建者：UID9622 諸葛鑫
獻禮：龍魂系統·中華文化傳承

§12 語義別名（中文原生·不翻譯）：
┌─────────────────────────────────────────────────────────┐
│ 補全 (Fulfill)      →    完成未完成的數據·填補空缺     │
│ 歸檔 (Archive)      →    標記為已完成·不再活躍         │
│ 熔斷 (Fuse)         →    因違規阻斷·進度凍結          │
│ 恢復 (Recover)      →    解除凍結·恢復執行            │
│ 審視 (Audit)        →    詳細檢查·生成審計報告        │
│ 發佈 (Release)      →    向外界公開·開放訪問          │
│ 封存 (Seal)         →    永久鎖定·不可再改            │
│ 見證 (Witness)      →    邀請第三方見證·強化信度      │
└─────────────────────────────────────────────────────────┘
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


# ============================================================================
# 意圖定義·中文原生語義
# ============================================================================

class Intent(Enum):
    """意圖類型（§12 語義別名）"""
    FULFILL = "補全"        # 完成未完成的數據
    ARCHIVE = "歸檔"        # 標記為已完成
    FUSE = "熔斷"           # 因違規阻斷
    RECOVER = "恢復"        # 解除凍結
    AUDIT = "審視"          # 詳細檢查
    RELEASE = "發佈"        # 向外界公開
    SEAL = "封存"           # 永久鎖定
    WITNESS = "見證"        # 邀請第三方見證
    TRANSLATE = "翻譯"      # 翻譯文本
    QUERY = "查詢"          # 查詢信息
    CREATE = "創建"         # 創建新數據
    UPDATE = "更新"         # 更新現有數據
    DELETE = "刪除"         # 刪除數據
    EXPORT = "導出"         # 導出數據
    IMPORT = "導入"         # 導入數據
    UNKNOWN = "未知"        # 無法識別


# ============================================================================
# 解析結果結構
# ============================================================================

@dataclass
class IntentParseResult:
    """意圖解析結果"""
    intent: str              # 識別的意圖
    confidence: float        # 置信度 (0.0-1.0)
    keywords: List[str]      # 提取的關鍵詞
    parameters: Dict         # 參數字典
    raw_input: str           # 原始輸入
    is_valid: bool          # 是否有效
    message: str            # 說明信息
    aliases: List[str]      # 匹配的別名


# ============================================================================
# 語義別名與規則定義
# ============================================================================

class SemanticAliasRegistry:
    """語義別名註冊表（§12 中文原生）"""

    def __init__(self):
        # 意圖 → 別名列表（從簡單到複雜）
        self.aliases = {
            Intent.FULFILL.value: [
                "補全", "完成", "填補", "補足", "補充",
                "把這個做完", "幫我填完", "補齊缺失的"
            ],
            Intent.ARCHIVE.value: [
                "歸檔", "存檔", "標記完成", "歸類",
                "把這個存了", "已經完成", "標記為已做"
            ],
            Intent.FUSE.value: [
                "熔斷", "阻斷", "凍結", "禁用", "封禁",
                "給他熔斷", "這條熔掉", "因為違規我熔了"
            ],
            Intent.RECOVER.value: [
                "恢復", "解凍", "解除", "重新開放",
                "幫我恢復", "解除凍結", "再開一下"
            ],
            Intent.AUDIT.value: [
                "審視", "審計", "檢查", "詳細查看", "複審",
                "幫我檢查一下", "審計一下這條", "給我看審計報告"
            ],
            Intent.RELEASE.value: [
                "發佈", "公開", "發送", "推送", "上線",
                "幫我發佈", "公開這條", "發送給大家"
            ],
            Intent.SEAL.value: [
                "封存", "鎖定", "永久存檔", "永不改動",
                "把這個永久鎖了", "封存這條", "不再改"
            ],
            Intent.WITNESS.value: [
                "見證", "邀請見證", "請第三方確認", "公證",
                "請他見證", "讓別人看著", "邀請見證人"
            ],
            Intent.TRANSLATE.value: [
                "翻譯", "轉譯", "把這個翻成", "譯成",
                "幫我翻譯", "翻成中文", "翻成英文"
            ],
            Intent.QUERY.value: [
                "查詢", "查看", "看看", "給我看", "有沒有",
                "查一下", "找找", "幫我查", "搜一下"
            ],
            Intent.CREATE.value: [
                "創建", "新建", "添加", "新增", "做一個",
                "給我建個", "新建一個", "添加到"
            ],
            Intent.UPDATE.value: [
                "更新", "修改", "改", "重新做", "改一下",
                "把這個改成", "更新一下", "重新設定"
            ],
            Intent.DELETE.value: [
                "刪除", "刪掉", "移除", "去掉", "搞掉",
                "幫我刪了", "刪掉這個", "移除這條"
            ],
            Intent.EXPORT.value: [
                "導出", "匯出", "備份", "下載", "保存",
                "給我導出", "導出成", "備份一份"
            ],
            Intent.IMPORT.value: [
                "導入", "匯入", "上傳", "導進來", "加載",
                "幫我導入", "導進去", "上傳一份"
            ]
        }

    def find_intent_for_alias(self, text: str) -> Tuple[str, float]:
        """
        根據用户文本查找意圖

        人話：看你說什麼·猜你想幹什麼

        Returns:
            (intent_name, confidence)
        """
        text_lower = text.lower()

        # 優先級 1：精確匹配（最高置信度）
        for intent, alias_list in self.aliases.items():
            for alias in alias_list:
                if alias.lower() == text_lower:
                    return intent, 1.0

        # 優先級 2：前綴匹配（高置信度）
        for intent, alias_list in self.aliases.items():
            for alias in alias_list:
                if text_lower.startswith(alias.lower()):
                    return intent, 0.9

        # 優先級 3：包含匹配（中等置信度）
        for intent, alias_list in self.aliases.items():
            for alias in alias_list:
                if alias.lower() in text_lower:
                    return intent, 0.7

        # 未找到
        return Intent.UNKNOWN.value, 0.0

    def get_aliases_for_intent(self, intent: str) -> List[str]:
        """獲取某個意圖的所有別名"""
        return self.aliases.get(intent, [])


# ============================================================================
# 參數提取引擎
# ============================================================================

class ParameterExtractor:
    """從用户輸入中提取參數"""

    def __init__(self):
        # 參數提取規則（正則表達式）
        self.patterns = {
            "language": r"(成|为|到)?(中文|英文|日文|韓文|法文|德文|俄文|西班牙文|意大利文)",
            "target_id": r"(ID|编号|代码|号码)[:：\s]+([A-Z0-9\-]+)",
            "count": r"(\d+)\s*(个|條|份|次|遍)",
            "time": r"(现在|今天|明天|周|月|年|小时|分钟)",
            "person": r"(給|给|发给|分享给)?\s*([^\s]+?)(?:\.|\s|$)",
            "scope": r"(全部|所有|這個|那個|他們|我們|你們)",
        }

    def extract_parameters(self, text: str, intent: str) -> Dict:
        """提取參數"""
        params = {
            "intent": intent,
            "raw_text": text,
            "timestamp": datetime.now().isoformat(),
        }

        # 動態提取
        for param_name, pattern in self.patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    params[param_name] = matches[0][-1]  # 取最後一個group
                else:
                    params[param_name] = matches[0]

        return params


# ============================================================================
# 關鍵詞提取引擎
# ============================================================================

class KeywordExtractor:
    """從用户輸入中提取關鍵詞"""

    def __init__(self):
        # 中文停用詞
        self.stopwords = {
            "的", "了", "是", "在", "有", "个", "一", "等", "以",
            "我", "你", "他", "她", "它", "我们", "你们", "他们",
            "呢", "吗", "啊", "哦", "嗯", "吧", "嘛", "啦"
        }
        # 高價值詞彙（給更高權重）
        self.high_value_terms = {
            "龍魂", "DNA", "簽章", "認證", "驗證", "翻譯",
            "數據", "隱私", "主權", "安全", "生態"
        }

    def extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """
        提取關鍵詞

        人話：從句子裡抽出最重要的詞
        """
        # 分詞（簡化版：按照標點和空格）
        words = re.findall(r"[\w\u4e00-\u9fff]+", text)

        # 過濾停用詞
        keywords = [w for w in words if w not in self.stopwords]

        # 按權重排序（高價值詞彙優先）
        keywords.sort(
            key=lambda w: (w in self.high_value_terms, len(w)),
            reverse=True
        )

        return keywords[:max_keywords]


# ============================================================================
# 意圖解析器·核心引擎
# ============================================================================

class IntentParser:
    """
    意圖翻譯官 - 把"人話"翻譯成"機器話"

    職責（§12 + §39 步③④）：
    1. 識別用户意圖（別名匹配）
    2. 提取參數和關鍵詞
    3. 驗證意圖有效性
    4. 輸出機器可執行的指令結構
    """

    def __init__(self):
        self.alias_registry = SemanticAliasRegistry()
        self.param_extractor = ParameterExtractor()
        self.keyword_extractor = KeywordExtractor()

    def parse_intent(self, user_input: str) -> IntentParseResult:
        """
        解析用户意圖

        人話：看你說的話·理解你想幹什麼·告訴機器

        Args:
            user_input: 用户的自然語言輸入

        Returns:
            IntentParseResult
        """

        if not user_input or not isinstance(user_input, str):
            return IntentParseResult(
                intent=Intent.UNKNOWN.value,
                confidence=0.0,
                keywords=[],
                parameters={},
                raw_input=user_input,
                is_valid=False,
                message="❌ 輸入無效·必須為非空字符串",
                aliases=[]
            )

        # ════════════════════════════════════════════════════════════════
        # 步驟 1：意圖識別（§12 別名匹配）
        # ════════════════════════════════════════════════════════════════

        intent, confidence = self.alias_registry.find_intent_for_alias(user_input)

        # ════════════════════════════════════════════════════════════════
        # 步驟 2：參數提取
        # ════════════════════════════════════════════════════════════════

        parameters = self.param_extractor.extract_parameters(user_input, intent)

        # ════════════════════════════════════════════════════════════════
        # 步驟 3：關鍵詞提取
        # ════════════════════════════════════════════════════════════════

        keywords = self.keyword_extractor.extract_keywords(user_input)

        # ════════════════════════════════════════════════════════════════
        # 步驟 4：置信度驗證
        # ════════════════════════════════════════════════════════════════

        is_valid = confidence >= 0.5  # 置信度閾值

        # ════════════════════════════════════════════════════════════════
        # 步驟 5：生成結果
        # ════════════════════════════════════════════════════════════════

        # 查找匹配的別名
        matched_aliases = []
        if intent != Intent.UNKNOWN.value:
            for alias in self.alias_registry.get_aliases_for_intent(intent):
                if alias.lower() in user_input.lower():
                    matched_aliases.append(alias)

        message = self._generate_message(intent, confidence, is_valid)

        return IntentParseResult(
            intent=intent,
            confidence=confidence,
            keywords=keywords,
            parameters=parameters,
            raw_input=user_input,
            is_valid=is_valid,
            message=message,
            aliases=matched_aliases
        )

    def _generate_message(self, intent: str, confidence: float, is_valid: bool) -> str:
        """生成說明信息"""
        if not is_valid:
            return "⚠️ 意圖不清楚·置信度太低·請重新表述"

        if confidence == 1.0:
            return f"✅ 意圖識別完美·{intent}（置信度 100%）"
        elif confidence >= 0.9:
            return f"✅ 意圖識別高可信·{intent}（置信度 {int(confidence*100)}%）"
        else:
            return f"🟡 意圖識別中等可信·{intent}（置信度 {int(confidence*100)}%）"

    def to_machine_instruction(self, parse_result: IntentParseResult) -> Dict:
        """
        將解析結果轉換為機器可執行的指令

        人話：給機器一份它能聽懂的清單
        """
        return {
            "instruction": {
                "intent": parse_result.intent,
                "confidence": parse_result.confidence,
                "timestamp": datetime.now().isoformat(),
                "status": "ready_to_execute" if parse_result.is_valid else "pending_review"
            },
            "parameters": parse_result.parameters,
            "keywords": parse_result.keywords,
            "metadata": {
                "raw_input": parse_result.raw_input,
                "matched_aliases": parse_result.aliases,
                "requires_confirmation": parse_result.confidence < 0.9
            }
        }

    def get_intent_help(self, intent: str = None) -> str:
        """獲取意圖幫助信息"""
        if intent and intent in [i.value for i in Intent]:
            aliases = self.alias_registry.get_aliases_for_intent(intent)
            return f"""
意圖：{intent}
別名：{', '.join(aliases[:3])} 等
例句：
  • "幫我{aliases[0]}"
  • "{aliases[1]}這個"
  • "我想{aliases[2]}"
"""
        else:
            help_text = "🌐 龍魂意圖翻譯官·支持的意圖列表：\n\n"
            for intent_enum in Intent:
                if intent_enum.value != "未知":
                    aliases = self.alias_registry.get_aliases_for_intent(intent_enum.value)
                    help_text += f"  {intent_enum.value:6} → {', '.join(aliases[:3])}\n"
            return help_text


# ============================================================================
# 測試與示例
# ============================================================================

def test_intent_parser():
    """意圖翻譯官·測試"""

    print("\n" + "=" * 80)
    print("🌐 龍魂 意圖翻譯官 v1.0 · 測試")
    print("=" * 80 + "\n")

    parser = IntentParser()

    # 測試用例
    test_cases = [
        "幫我翻譯",
        "把這個翻成英文",
        "查詢 ID:001 的信息",
        "歸檔",
        "標記為已完成",
        "熔斷這個用户",
        "恢復訪問權限",
        "給我看審計報告",
        "發佈到外面",
        "封存這條記錄",
        "邀請見證人",
        "導出所有數據",
        "??不懂??",
        ""
    ]

    for user_input in test_cases:
        if user_input == "":
            continue

        result = parser.parse_intent(user_input)

        print(f"【輸入】{user_input}")
        print(f"  意圖：{result.intent}")
        print(f"  置信度：{int(result.confidence*100)}%")
        print(f"  有效：{'✅' if result.is_valid else '❌'}")
        print(f"  說明：{result.message}")

        if result.keywords:
            print(f"  關鍵詞：{', '.join(result.keywords)}")

        if result.aliases:
            print(f"  匹配別名：{', '.join(result.aliases)}")

        if result.is_valid:
            instruction = parser.to_machine_instruction(result)
            print(f"  機器指令狀態：{instruction['instruction']['status']}")

        print()

    # 幫助信息
    print("=" * 80)
    print(parser.get_intent_help())
    print("=" * 80 + "\n")


if __name__ == "__main__":
    test_intent_parser()
