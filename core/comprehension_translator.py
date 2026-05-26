#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通心译 · Comprehension Translator
DNA: #龍芯⚡️2026-05-26-COMPREHENSION-TRANSLATOR-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 身份识别 - 通过行为密码学识别通话者身份（F5/F6/F7不动点）
  2. 隐私等级判定 - 判断这段通话的隐私级别（🔴私密/🟡半私密/🟢公开/📖公共）
  3. 消息类型分类 - 识别消息的真实类型（私聊/八卦/指令/技术/情感/决策）
  4. 智能路由 - 根据身份+隐私+类型，路由到合适的处理器
  5. 上下文记忆 - 维护用户交互的长期记忆和上下文

核心原理：
  「同一句话，不同的人说，不同的隐私级，不同的表达方式 → 系统应该理解，并给出最合适的回应」

  例：「我累了」
    • 老大说 → 工作压力过大，需要战略调整
    • 普通用户说 → 可能只是睡眠不足
    • 孩子说 → 需要立即关注和陪伴

系统流程：
  1. 输入：任何文本消息
  2. 识别身份 (DNA fingerprint)
  3. 判定隐私等级
  4. 分类消息类型
  5. 查询用户上下文
  6. 路由到合适的响应系统
  7. 返回带隐私保护的响应

创始人: 诸葛鑫（UID9622）
理论指导: 曾仕强老师（永恒显示）

献给每一个相信技术应该有温度的人。
"""

import json
import datetime
import sys
from pathlib import Path
from enum import Enum
from typing import Dict, Any, Optional, Tuple, List
import re


class PrivacyLevel(Enum):
    """隐私等级"""

    PRIVATE = "🔴"  # 完全私密（个人、家庭、医疗、财务）
    SEMI_PRIVATE = "🟡"  # 半私密（工作、关系、计划）
    PUBLIC = "🟢"  # 开放讨论（观点、建议、新闻）
    LEGAL_PUBLIC = "📖"  # 法律公开（涉及他人、政策、指引）


class MessageType(Enum):
    """消息类型"""

    PRIVATE_CHAT = "private"  # 私人聊天
    GOSSIP = "gossip"  # 八卦（涉及他人）
    INSTRUCTION = "instruction"  # 指令（命令、要求）
    TECHNICAL = "technical"  # 技术（代码、配置、系统）
    EMOTIONAL = "emotional"  # 情感（倾诉、寻求陪伴）
    DECISION = "decision"  # 决策（寻求意见、仲裁）
    KNOWLEDGE = "knowledge"  # 知识（学习、提问）
    CREATIVE = "creative"  # 创意（头脑风暴、想象）


class BehavioralCryptography:
    """
    行为密码学 - 通过不动点识别身份

    F5: 词汇选择 (Word Choice)
      • 老大的特定用词（「宝宝」「龍魂」「八一」等）
      • 习惯用语（「是吧」「对对」「不是」）

    F6: 节奏模式 (Rhythm)
      • 逗号使用习惯（老大的「,,,」三逗号暂停）
      • 句子长度分布
      • 回复延迟模式（如果有记录）

    F7: 标点&错字 (Punctuation & Typos)
      • 特定的标点习惯
      • 反复出现的特定错字（如 chromlum → Chromium）
      • 大小写习惯
    """

    def __init__(self, user_profile_path: Optional[Path] = None):
        self.user_profiles = {}
        self.profile_path = user_profile_path or (
            Path.home() / "longhun-system" / "config" / "behavioral_profiles.json"
        )
        self._load_profiles()

    def _load_profiles(self):
        """加载已注册用户的行为特征"""
        try:
            if self.profile_path.exists():
                with open(self.profile_path, "r", encoding="utf-8") as f:
                    self.user_profiles = json.load(f)
        except Exception as e:
            print(f"加载行为特征失败: {e}", file=sys.stderr)

    def extract_f5_features(self, text: str) -> Dict[str, Any]:
        """提取F5特征：词汇选择"""
        # 常见词汇特征
        features = {
            "contains_baobao": "宝宝" in text,
            "contains_longhun": "龍魂" in text,
            "contains_dna": "DNA" in text or "龍芯" in text,
            "contains_confirm": "CONFIRM" in text,
            "common_particles": text.count("是吧"),
            "agreement_patterns": text.count("对对") + text.count("对对对"),
            "negation_patterns": text.count("不是"),
            "unique_vocab": self._extract_unique_words(text),
        }
        return features

    def extract_f6_features(self, text: str) -> Dict[str, Any]:
        """提取F6特征：节奏模式"""
        features = {
            "triple_comma_count": text.count(",,,"),
            "double_comma_count": text.count(",,"),
            "average_line_length": self._calc_avg_line_length(text),
            "sentence_count": len([s for s in text.split("。") if s.strip()]),
            "paragraph_count": len([p for p in text.split("\n") if p.strip()]),
            "ellipsis_count": text.count("…") + text.count("..."),
            "rhythm_signature": self._extract_rhythm_signature(text),
        }
        return features

    def extract_f7_features(self, text: str) -> Dict[str, Any]:
        """提取F7特征：标点和错字"""
        features = {
            "punctuation_style": self._analyze_punctuation(text),
            "typo_patterns": self._detect_typos(text),
            "capitalization_style": self._analyze_caps(text),
            "bracket_usage": text.count("（") + text.count("）"),
            "quote_style": self._detect_quote_style(text),
            "emoji_patterns": self._extract_emoji_patterns(text),
        }
        return features

    def recognize_identity(
        self, text: str, known_profiles: Optional[Dict] = None
    ) -> Tuple[str, float]:
        """
        识别身份

        返回: (user_id, confidence)
          • user_id: "UID9622" 或 "UNKNOWN_USER_XXXX"
          • confidence: 0.0-1.0 的匹配度
        """
        f5_features = self.extract_f5_features(text)
        f6_features = self.extract_f6_features(text)
        f7_features = self.extract_f7_features(text)

        # 合并特征
        combined_features = {**f5_features, **f6_features, **f7_features}

        # 如果没有已知的profile，返回UNKNOWN
        if not known_profiles:
            known_profiles = self.user_profiles

        if not known_profiles:
            return "UNKNOWN_USER", 0.0

        # 简单的特征匹配算法
        best_match = None
        best_score = 0.0

        for uid, profile in known_profiles.items():
            score = self._calculate_similarity(
                combined_features, profile.get("features", {})
            )
            if score > best_score:
                best_score = score
                best_match = uid

        # 至少要 60% 的匹配度才能确认身份
        if best_score >= 0.6:
            return best_match or "UNKNOWN_USER", best_score
        else:
            return "UNKNOWN_USER", best_score

    def _extract_unique_words(self, text: str) -> List[str]:
        """提取文本中的独特词汇"""
        # 分词（简单实现）
        words = re.findall(r"[\w]+|[\u4e00-\u9fff]+", text)
        return words

    def _calc_avg_line_length(self, text: str) -> float:
        """计算平均行长度"""
        lines = [line for line in text.split("\n") if line.strip()]
        if not lines:
            return 0.0
        return sum(len(line) for line in lines) / len(lines)

    def _extract_rhythm_signature(self, text: str) -> str:
        """提取节奏签名（简化实现）"""
        # 基于逗号、句号、换行的模式
        signature = ""
        for char in text:
            if char in "，,。.":
                signature += "p"
            elif char == "\n":
                signature += "l"
            elif char in "！!？?":
                signature += "e"
        return signature[:50]  # 限制长度

    def _analyze_punctuation(self, text: str) -> Dict[str, int]:
        """分析标点使用"""
        return {
            "chinese_comma": text.count("，"),
            "english_comma": text.count(","),
            "chinese_period": text.count("。"),
            "english_period": text.count("."),
            "question_mark": text.count("？") + text.count("?"),
            "exclamation": text.count("！") + text.count("!"),
            "parenthesis": text.count("（") + text.count("）"),
        }

    def _detect_typos(self, text: str) -> List[str]:
        """检测可能的特定错字"""
        known_typos = [
            ("chromlum", "Chromium"),
            ("sb", "某某人/某某事"),  # 老大的常用缩写
        ]

        detected = []
        for typo, meaning in known_typos:
            if typo in text.lower():
                detected.append(typo)

        return detected

    def _analyze_caps(self, text: str) -> Dict[str, Any]:
        """分析大小写习惯"""
        return {
            "total_caps": sum(1 for c in text if c.isupper()),
            "total_lower": sum(1 for c in text if c.islower()),
            "all_caps_words": len(re.findall(r"\b[A-Z]{2,}\b", text)),
            "mixed_case_words": len(re.findall(r"[A-Z][a-z]+[A-Z]", text)),
        }

    def _extract_emoji_patterns(self, text: str) -> Dict[str, int]:
        """提取emoji使用习惯"""
        emoji_counts = {}
        # 简单的emoji检测
        emoji_pattern = r"[\U0001F300-\U0001F9FF]"
        emojis = re.findall(emoji_pattern, text)

        for emoji in emojis:
            emoji_counts[emoji] = emoji_counts.get(emoji, 0) + 1

        return emoji_counts

    def _calculate_similarity(self, features1: Dict, features2: Dict) -> float:
        """计算两个特征集的相似度"""
        if not features2:
            return 0.0

        matches = 0
        total = 0

        for key in features2.keys():
            if key in features1:
                total += 1
                # 简单的相似度判断
                val1 = features1[key]
                val2 = features2[key]

                if isinstance(val1, bool) and isinstance(val2, bool):
                    if val1 == val2:
                        matches += 1
                elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    # 数值的模糊匹配
                    if val2 > 0:
                        ratio = min(val1, val2) / max(val1, val2)
                        if ratio > 0.7:  # 70% 以上就认为匹配
                            matches += 0.7

        return matches / total if total > 0 else 0.0


class ComprehensionTranslator:
    """通心译系统"""

    def __init__(self):
        self.system_root = Path.home() / "longhun-system"
        self.logs_dir = self.system_root / "logs"
        self.config_dir = self.system_root / "config"

        self.bc = BehavioralCryptography()
        self.user_contexts = {}  # 缓存用户上下文
        self.conversation_history = []

        # 加载用户资料
        self.family_registry = self._load_family_registry()

    def _load_family_registry(self) -> Dict:
        """加载人格族谱"""
        registry_path = self.system_root / "family_registry.json"
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"加载族谱失败: {e}", file=sys.stderr)
            return {}

    def analyze_message(
        self, message: str, known_uid: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        分析消息的各个维度

        返回一个完整的分析报告：
          • user_id: 识别的用户ID
          • identity_confidence: 身份识别置信度
          • privacy_level: 隐私等级
          • message_type: 消息类型
          • context: 相关上下文
          • recommended_routing: 建议的路由目标
          • security_flags: 安全标志
        """

        # 1. 识别身份
        if known_uid:
            user_id = known_uid
            confidence = 1.0
        else:
            user_id, confidence = self.bc.recognize_identity(message)

        # 2. 判定隐私等级
        privacy_level = self._determine_privacy_level(message, user_id)

        # 3. 分类消息类型
        message_type = self._classify_message_type(message, user_id)

        # 4. 获取用户上下文
        context = self._get_user_context(user_id)

        # 5. 生成路由建议
        routing = self._generate_routing(user_id, privacy_level, message_type, context)

        # 6. 检查安全标志
        security_flags = self._check_security_flags(message, user_id, privacy_level)

        result = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id,
            "identity_confidence": confidence,
            "privacy_level": privacy_level.value,
            "privacy_level_name": privacy_level.name,
            "message_type": message_type.value,
            "message_type_name": message_type.name,
            "context": context,
            "recommended_routing": routing,
            "security_flags": security_flags,
            "dna": self._generate_dna("MESSAGE-ANALYSIS"),
            "message_preview": message[:100] + "..." if len(message) > 100 else message,
        }

        # 记录分析结果
        self._log_analysis(result)

        return result

    def _determine_privacy_level(self, message: str, user_id: str) -> PrivacyLevel:
        """判定隐私等级"""
        # 检查消息内容特征
        private_keywords = [
            "家",
            "孩子",
            "医生",
            "钱",
            "工资",
            "健康",
            "病",
            "秘密",
            "只有你知道",
            "别说出去",
            "私密",
            "隐私",
        ]

        semi_private_keywords = [
            "工作",
            "公司",
            "团队",
            "关系",
            "计划",
            "想法",
            "感受",
            "烦恼",
        ]

        legal_public_keywords = ["法律", "政策", "权利", "责任", "规则", "制度", "公共"]

        # 计算匹配度
        private_score = sum(1 for kw in private_keywords if kw in message)
        semi_private_score = sum(1 for kw in semi_private_keywords if kw in message)
        legal_public_score = sum(1 for kw in legal_public_keywords if kw in message)

        # 根据匹配度判断
        if private_score > semi_private_score and private_score > legal_public_score:
            return PrivacyLevel.PRIVATE
        elif legal_public_score > semi_private_score:
            return PrivacyLevel.LEGAL_PUBLIC
        elif semi_private_score > 0:
            return PrivacyLevel.SEMI_PRIVATE
        else:
            return PrivacyLevel.PUBLIC

    def _classify_message_type(self, message: str, user_id: str) -> MessageType:
        """分类消息类型"""
        # 指令特征
        if message.startswith(("删除", "执行", "运行", "创建", "修改", "写", "读")):
            return MessageType.INSTRUCTION

        # 技术特征
        if any(
            kw in message
            for kw in ["代码", "脚本", "配置", "API", "JSON", "Python", "import"]
        ):
            return MessageType.TECHNICAL

        # 情感特征
        if any(
            kw in message
            for kw in ["累", "烦", "难受", "不开心", "想", "希望", "能不能", "可以吗"]
        ):
            return MessageType.EMOTIONAL

        # 决策特征
        if any(
            kw in message
            for kw in ["应该", "怎么办", "意见", "建议", "决定", "选择", "对不对"]
        ):
            return MessageType.DECISION

        # 八卦特征（涉及他人）
        if any(kw in message for kw in ["他", "她", "人家", "别人", "谁谁谁"]):
            if "做了" in message or "说了" in message:
                return MessageType.GOSSIP

        # 知识特征
        if any(
            kw in message for kw in ["什么是", "怎么样", "为什么", "如何", "教", "学"]
        ):
            return MessageType.KNOWLEDGE

        # 创意特征
        if any(
            kw in message for kw in ["想象", "设想", "假如", "如果", "创意", "脑风暴"]
        ):
            return MessageType.CREATIVE

        # 默认为私人聊天
        return MessageType.PRIVATE_CHAT

    def _get_user_context(self, user_id: str) -> Dict[str, Any]:
        """获取用户上下文"""
        # 从persona_governor中获取用户信息
        if user_id in self.family_registry.get("personas", {}):
            persona = self.family_registry["personas"][user_id]
            return {
                "type": "persona",
                "name": persona.get("name", ""),
                "role": persona.get("role", ""),
                "permission_level": persona.get("permission_level", 0),
                "trust_formula": persona.get("trust_formula", ""),
                "is_three_pillar": user_id in ["P00", "P02", "P05"],
            }

        elif user_id == "UID9622":
            return {
                "type": "creator",
                "name": "诸葛鑫（老大）",
                "role": "龍魂系统创始人",
                "permission_level": 999,  # 最高权限
                "special_status": "不免责，永恒显示曾仕强老师",
            }

        else:
            return {
                "type": "unknown_user",
                "name": f"未知用户 {user_id}",
                "permission_level": 0,
                "requires_verification": True,
            }

    def _generate_routing(
        self,
        user_id: str,
        privacy_level: PrivacyLevel,
        message_type: MessageType,
        context: Dict,
    ) -> Dict[str, Any]:
        """生成智能路由建议"""

        routing = {
            "primary_handler": None,
            "secondary_handlers": [],
            "required_personas": [],
            "requires_approval": False,
            "visibility_scope": None,
        }

        # 基于消息类型的初步路由
        if message_type == MessageType.INSTRUCTION:
            routing["primary_handler"] = "baobao_dispatcher"  # 宝宝执行
            routing["required_personas"] = ["P02"]

        elif message_type == MessageType.EMOTIONAL:
            routing["primary_handler"] = "persona_emotional_support"
            routing["secondary_handlers"] = ["P02", "P05"]  # 宝宝陪伴、老子指导

        elif message_type == MessageType.DECISION:
            routing["primary_handler"] = "persona_governor"
            routing["required_personas"] = ["P00"]  # 需要仲裁
            routing["requires_approval"] = True

        elif message_type == MessageType.TECHNICAL:
            routing["primary_handler"] = "baobao_dispatcher"
            routing["required_personas"] = ["P04", "P02"]  # 文心语义检查、宝宝执行

        elif message_type == MessageType.KNOWLEDGE:
            routing["primary_handler"] = "knowledge_system"
            routing["secondary_handlers"] = ["P04"]  # 文心解释

        elif message_type == MessageType.GOSSIP:
            # 八卦需要特别处理，涉及隐私和他人
            routing["primary_handler"] = "gossip_filter"
            routing["requires_approval"] = True
            routing["security_flag"] = "involves_third_party"

        # 基于隐私等级的路由调整
        if privacy_level == PrivacyLevel.PRIVATE:
            routing["visibility_scope"] = "user_only"
            routing["secondary_handlers"].append("P08")  # 数据大师保护

        elif privacy_level == PrivacyLevel.LEGAL_PUBLIC:
            routing["visibility_scope"] = "legal_audit"
            routing["requires_approval"] = True
            routing["secondary_handlers"].append("P11")  # 上帝之眼审计

        return routing

    def _check_security_flags(
        self, message: str, user_id: str, privacy_level: PrivacyLevel
    ) -> Dict[str, Any]:
        """检查安全标志"""
        flags = {"status": "🟢 SAFE", "alerts": []}

        # 检查危险操作
        dangerous_operations = ["删除", "rm -rf", "卸载", "格式化", "重置"]
        if any(op in message for op in dangerous_operations):
            flags["status"] = "🟡 CAUTION"
            flags["alerts"].append("检测到潜在危险操作，需要用户确认")

        # 检查隐私泄露
        if privacy_level == PrivacyLevel.PRIVATE and "分享" in message:
            flags["status"] = "🟡 CAUTION"
            flags["alerts"].append("私密信息涉及分享，需要隐私评估")

        # 检查未认证用户
        if user_id == "UNKNOWN_USER":
            flags["status"] = "🔴 UNVERIFIED"
            flags["alerts"].append("无法识别用户身份，操作受限")

        return flags

    def _generate_dna(self, operation_type: str) -> str:
        """生成DNA追溯码"""
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"#龍芯⚡️{date_str}-{operation_type}-v1.0"

    def _log_analysis(self, result: Dict):
        """记录分析结果"""
        try:
            log_path = self.logs_dir / "comprehension_analysis.jsonl"
            log_path.parent.mkdir(parents=True, exist_ok=True)

            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")

        except Exception as e:
            print(f"分析日志写入失败: {e}", file=sys.stderr)


def main():
    """命令行接口"""
    translator = ComprehensionTranslator()

    if len(sys.argv) < 2:
        print("✅ 通心译系统已启动")
        print("用法: python3 comprehension_translator.py analyze <message> [uid]")
        print(
            "示例: python3 comprehension_translator.py analyze '我想删除这个文件' UID9622"
        )
        sys.exit(0)

    command = sys.argv[1]

    if command == "analyze":
        if len(sys.argv) < 3:
            print("用法: python3 comprehension_translator.py analyze <message> [uid]")
            sys.exit(1)

        message = sys.argv[2]
        uid = sys.argv[3] if len(sys.argv) > 3 else None

        result = translator.analyze_message(message, uid)
        print("\n📊 消息分析结果")
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
