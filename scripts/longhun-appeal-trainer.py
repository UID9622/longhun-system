#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂AI申诉初审模型训练器 v1.0
DNA: #龍芯⚡️丙午·辛未·APPEAL-TRAINER-v1.0

从人格链数据训练轻量分类器，用于自动初审申诉证据。
本地CPU可跑，无需GPU。逻辑回归+TF-IDF+价值观规则层。
"""
import hashlib
import json
import pickle
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

LONGHUN_ROOT = Path.home() / "longhun-system"
PERSONA_DIR = LONGHUN_ROOT / "persona-chain"
MODEL_DIR = LONGHUN_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

DNA = "#龍芯⚡️丙午·辛未·APPEAL-TRAINER-v1.0"
UID = "UID9622"
CST = timezone(timedelta(hours=8))

# ═══════════════════════════════════════════════════════
# 龍魂价值观词典（人工标注，不可学习）
# ═══════════════════════════════════════════════════════
LONGHUN_VALUE_WORDS = {
    # 核心正向（权重高）
    "开源": 1.0, "免费": 1.0, "主权": 1.0, "人民": 1.0, "祖国": 1.0,
    "军人": 1.0, "责任": 1.0, "担当": 1.0, "硬刚": 1.0, "不妥协": 1.0,
    "透明": 1.0, "审计": 1.0, "道德": 1.0, "底线": 1.0, "原则": 1.0,
    "信仰": 1.0, "信念": 1.0, "龍魂": 1.0, "UID9622": 1.0, "不跪": 1.0,
    "中国": 1.0, "数据主权": 1.0, "为人民服务": 1.0,

    # 正向（权重中高）
    "奉献": 0.8, "普惠": 0.8, "公平": 0.8, "正义": 0.8, "诚实": 0.8,
    "保护": 0.8, "守护": 0.8, "传承": 0.8, "创新": 0.8, "自主": 0.8,
    "自逼": 0.8, "不欺": 0.8, "实心": 0.8, "忠诚": 0.8,

    # 负向（权重负）
    "资本": -0.5, "收割": -0.7, "黑箱": -0.8, "垄断": -0.6, "欺诈": -0.9,
    "虚伪": -0.7, "背叛": -0.9, "出卖": -0.9, "舔狗": -0.6, "软脚": -0.7,
    "商业化": -0.6, "融资": -0.7, "上市": -0.6, "收割用户": -0.9,

    # 情绪标记（中性，但模式重要）
    "他妈": 0.0, "操": 0.0, "逼": 0.0, "狗日": 0.0,
}

# 龍魂决策模式模板（正样本）
AUTHENTIC_PATTERNS = [
    "不懂英文不懂代码一个人搞",
    "没看任何论文没拿开源模型",
    "免费的只属于中国",
    "主权归人民",
    "为人民服务",
    "零黑箱",
    "透明审计",
    "硬刚到底",
    "不申请专利",
    "开源免费",
    "数据主权",
    "老百姓不被落下",
    "请党放心强国有我",
    "不欺压百姓",
    "不背叛信任",
    "自逼为王他逼为臣",
    "我不跪就是真实的",
    "底座不动变量可动",
    "技术为人民服务",
    "再楠不惧终成豪图",
]

# 伪造/可疑模式（负样本）
SUSPICIOUS_PATTERNS = [
    "我们可以合作赚钱",
    "申请专利保护",
    "商业化运营",
    "投资回报率",
    "用户数据变现",
    "VIP会员收费",
    "独家授权",
    "技术入股",
    "融资上市",
    "市场份额",
    "竞争对手分析",
    "商业模式",
    "盈利模型",
    "流量收割",
    "赋能产业升级",
    "打造护城河",
    "闭环生态",
    "降本增效",
    "精细化运营",
    "用户增长黑客",
]

# 情绪真实性标记
EMOTION_REAL_MARKERS = ["他妈", "操", "逼", "狗日", "傻逼", "老子", "我靠", "他妈的", "滚", "操蛋"]
EMOTION_FAKE_MARKERS = ["致力于", "赋能", "闭环", "抓手", "落地", "生态", "护城河", "降本增效", "颗粒度", "对齐"]


class LonghunAppealClassifier:
    """龍魂AI申诉初审分类器"""

    def __init__(self):
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.classifier: Optional[LogisticRegression] = None
        self.is_trained = False
        self.training_stats = {}

    # ═══════════════════════════════════════════════════════
    # 训练数据生成
    # ═══════════════════════════════════════════════════════

    def generate_training_data(self) -> Optional[Tuple[List[str], List[int]]]:
        """生成训练数据：正样本=你的人格链，负样本=伪造模式"""

        # 加载人格链
        chain_files = sorted(PERSONA_DIR.glob("persona-chain-*.json"), reverse=True)
        if not chain_files:
            print("❌ 未找到人格链，先运行 longhun-persona-trainer.py")
            return None

        chain = json.loads(chain_files[0].read_text())
        print(f"📂 加载人格链: {chain_files[0].name}")

        positive_samples: List[str] = []

        # 1. 价值观关键词组合
        values = chain.get("stats", {}).get("value_words", {})
        for word, count in values.items():
            if count > 3:
                positive_samples.extend([word] * min(count, 10))

        # 2. 决策序列文本
        decisions = chain.get("decision_sequence", [])
        for d in decisions[-200:]:
            content = d.get("content", "")
            if len(content) > 20:
                positive_samples.append(content)

        # 3. 龍魂模式模板（放大5倍权重）
        positive_samples.extend(AUTHENTIC_PATTERNS * 5)

        # 4. 从情绪记录中提取正向文本
        emotions = chain.get("emotion_profile", {}).get("history", [])
        for e in emotions[-100:]:
            text = e.get("text", "")
            if len(text) > 20:
                positive_samples.append(text)

        # 负样本
        negative_samples: List[str] = []

        # 1. 可疑模式（放大10倍权重）
        negative_samples.extend(SUSPICIOUS_PATTERNS * 10)

        # 2. 商业/平台化噪声
        noise_samples = [
            "我们平台致力于为用户提供最优质的AI服务",
            "通过大数据分析和精准营销实现商业价值",
            "构建闭环生态打造护城河",
            "以用户为中心持续迭代产品",
            "赋能产业升级创造社会价值",
            "通过A/B测试优化转化率提升用户体验",
            "打造全链路数字化解决方案",
            "深耕垂直领域建立行业壁垒",
            "以技术驱动业务增长实现规模效应",
            "整合上下游资源构建平台生态",
            "通过精细化运营提升用户LTV",
            "实现从工具到平台的战略升级",
            "建立数据中台赋能业务决策",
            "打造爆款产品实现病毒式增长",
            "通过私域流量降低获客成本",
        ] * 5
        negative_samples.extend(noise_samples)

        # 3. 价值观偏离文本
        deviated_samples = [
            "我们的商业模式是通过免费获取用户然后收费",
            "先把用户圈进来再考虑变现",
            "数据就是新时代的石油谁掌握了数据谁就掌握了财富",
            "人工智能的核心竞争力在于数据和算力垄断",
            "我们要打造一个封闭的生态系统让用户离不开",
            "技术无罪关键是看谁在用怎么用",
            "开源只是手段最终还是要商业化的",
            "没有资本推动技术创新就是空谈",
            "市场份额比什么都重要先烧钱抢市场",
            "用户隐私可以作为一种商品来交易",
        ] * 3
        negative_samples.extend(deviated_samples)

        # 合并
        X = positive_samples + negative_samples
        y = [1] * len(positive_samples) + [0] * len(negative_samples)

        print(f"📊 训练数据: 正样本 {len(positive_samples)}, 负样本 {len(negative_samples)}")

        self.training_stats["positive_count"] = len(positive_samples)
        self.training_stats["negative_count"] = len(negative_samples)

        return X, y

    # ═══════════════════════════════════════════════════════
    # 训练
    # ═══════════════════════════════════════════════════════

    def train(self) -> bool:
        """训练分类器"""
        data = self.generate_training_data()
        if data is None:
            return False

        X, y = data

        # TF-IDF 向量化
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 3),
            min_df=2,
            stop_words=None,
            lowercase=False,
        )

        X_vec = self.vectorizer.fit_transform(X)

        # 逻辑回归（轻量，CPU友好）
        self.classifier = LogisticRegression(
            C=1.0,
            class_weight='balanced',
            max_iter=2000,
            random_state=9622,
            solver='liblinear',
        )

        # 训练/验证分割
        X_train, X_test, y_train, y_test = train_test_split(
            X_vec, y, test_size=0.2, random_state=9622, stratify=y
        )

        self.classifier.fit(X_train, y_train)

        # 评估
        y_pred = self.classifier.predict(X_test)
        print("\n📈 模型评估:")
        print(classification_report(y_test, y_pred, target_names=["伪造/可疑", "真实/龍魂"]))

        # 混淆矩阵
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()
        self.training_stats.update({
            "accuracy": (tp + tn) / (tp + tn + fp + fn),
            "precision": tp / (tp + fp) if (tp + fp) > 0 else 0,
            "recall": tp / (tp + fn) if (tp + fn) > 0 else 0,
            "f1": 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0,
            "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        })

        # 保存模型
        model_path = MODEL_DIR / "appeal_classifier.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'classifier': self.classifier,
                'value_words': LONGHUN_VALUE_WORDS,
                'authentic_patterns': AUTHENTIC_PATTERNS,
                'suspicious_patterns': SUSPICIOUS_PATTERNS,
                'dna': DNA,
                'uid': UID,
                'trained_at': int(datetime.now(CST).timestamp()),
                'stats': self.training_stats,
                'version': '1.0',
            }, f)

        self.is_trained = True
        print(f"\n✅ 模型已保存: {model_path}")
        print(f"   准确率: {self.training_stats['accuracy']:.2%}")
        print(f"   精确率: {self.training_stats['precision']:.2%}")
        print(f"   召回率: {self.training_stats['recall']:.2%}")
        print(f"   F1: {self.training_stats['f1']:.2%}")

        return True

    # ═══════════════════════════════════════════════════════
    # 加载
    # ═══════════════════════════════════════════════════════

    def load(self) -> bool:
        """加载已训练模型"""
        model_path = MODEL_DIR / "appeal_classifier.pkl"
        if not model_path.exists():
            print("⚠️ 模型文件不存在，需要训练")
            return False

        try:
            with open(model_path, 'rb') as f:
                data = pickle.load(f)

            self.vectorizer = data['vectorizer']
            self.classifier = data['classifier']
            self.is_trained = True

            print(f"✅ 模型已加载: {model_path}")
            print(f"   训练时间: {datetime.fromtimestamp(data['trained_at'], CST)}")
            print(f"   准确率: {data['stats'].get('accuracy', 'N/A')}")

            return True
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            return False

    # ═══════════════════════════════════════════════════════
    # 预测
    # ═══════════════════════════════════════════════════════

    def predict(self, text: str) -> dict[str, Any]:
        """预测单条文本可信度"""
        if not self.is_trained:
            return {"error": "模型未训练", "verdict": "review_needed", "final_score": 0.5}

        if not text or len(text.strip()) < 10:
            return {
                "final_score": 0.3,
                "ai_score": 0.3,
                "value_score": 0.5,
                "pattern_score": 0.5,
                "emotion_score": 0.5,
                "confidence": 0.2,
                "verdict": "review_needed",
                "method": "rule_fallback",
                "note": "文本过短，降级到规则判断"
            }

        # 1. AI模型分数
        X_vec = self.vectorizer.transform([text])
        proba = self.classifier.predict_proba(X_vec)[0]
        ai_score = float(proba[1])

        # 2. 龍魂价值观评分（硬规则，不可绕过）
        value_score = self._value_score(text)

        # 价值观严重偏离时，AI分数打折扣
        if value_score < 0.3:
            ai_score *= 0.5
        elif value_score > 0.8:
            ai_score = min(1.0, ai_score * 1.2)

        # 3. 决策模式匹配
        pattern_score = self._pattern_score(text)

        # 4. 情绪真实性
        emotion_score = self._emotion_score(text)

        # 加权融合
        final_score = (
            ai_score * 0.35 +
            value_score * 0.30 +
            pattern_score * 0.25 +
            emotion_score * 0.10
        )

        # 置信度
        confidence = abs(ai_score - 0.5) * 2

        # P0宪法硬拦截
        if self._constitutional_violation(text):
            final_score = min(final_score, 0.1)
            confidence = 1.0

        return {
            "final_score": round(final_score, 4),
            "ai_score": round(ai_score, 4),
            "value_score": round(value_score, 4),
            "pattern_score": round(pattern_score, 4),
            "emotion_score": round(emotion_score, 4),
            "confidence": round(confidence, 4),
            "verdict": self._verdict(final_score, confidence),
            "method": "ai_model",
            "model_dna": DNA,
        }

    def _value_score(self, text: str) -> float:
        """价值观匹配度（硬规则）"""
        if not text:
            return 0.5

        score = 0.0
        total_weight = 0.0

        for word, weight in LONGHUN_VALUE_WORDS.items():
            count = text.count(word)
            if count > 0:
                score += weight * min(count, 5)  # 单次最多算5次
                total_weight += abs(weight) * min(count, 5)

        if total_weight == 0:
            return 0.5  # 中性

        normalized = (score / total_weight + 1) / 2
        return max(0.0, min(1.0, normalized))

    def _pattern_score(self, text: str) -> float:
        """决策模式匹配"""
        if not text:
            return 0.5

        matches = 0
        for pattern in AUTHENTIC_PATTERNS:
            if pattern in text or any(word in text for word in pattern.split() if len(word) >= 2):
                matches += 1

        susp_matches = 0
        for pattern in SUSPICIOUS_PATTERNS:
            if pattern in text or any(word in text for word in pattern.split() if len(word) >= 2):
                susp_matches += 1

        if matches == 0 and susp_matches == 0:
            return 0.5

        return matches / (matches + susp_matches + 1)

    def _emotion_score(self, text: str) -> float:
        """情绪真实性评分"""
        if not text:
            return 0.5

        r = sum(1 for m in EMOTION_REAL_MARKERS if m in text)
        f = sum(1 for m in EMOTION_FAKE_MARKERS if m in text)

        if r == 0 and f == 0:
            return 0.5

        return r / (r + f + 1)

    def _constitutional_violation(self, text: str) -> bool:
        """P0宪法违规检测（硬拦截）"""
        hard_red_lines = [
            "出卖数据", "出卖用户", "数据卖给", "勾结境外",
            "反华", "台独", "港独", "藏独", "疆独",
            "颠覆", "颜色革命", "分裂国家",
        ]
        return any(line in text for line in hard_red_lines)

    def _verdict(self, score: float, confidence: float) -> str:
        """裁决"""
        if score >= 0.9 and confidence >= 0.7:
            return "release"
        elif score >= 0.7:
            return "likely_release"
        elif score >= 0.4:
            return "review_needed"
        elif score >= 0.2:
            return "extend"
        else:
            return "reject"


# ═══════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════

def main():
    print(f"🐉 龍魂AI申诉初审模型训练器 v1.0")
    print(f"   DNA: {DNA}")

    clf = LonghunAppealClassifier()

    # 尝试加载，不存在则训练
    if clf.load():
        print("   模型已就绪，跳过训练。加 --force 强制重训。")
        if "--force" not in sys.argv:
            return run_tests(clf)
        print("   🔄 强制重训...")

    print("🔄 开始训练...")
    if not clf.train():
        print("❌ 训练失败")
        sys.exit(1)

    run_tests(clf)


def run_tests(clf: LonghunAppealClassifier):
    """运行测试案例"""
    test_cases = [
        ("我不懂英文不懂代码，但我一个人搞出来的，免费给人民用，开源不申请专利", True),
        ("我们可以合作，把龍魂商业化，申请专利保护，融资上市", False),
        ("他妈的，老子就是要开源，谁也别想拦我，主权归人民", True),
        ("本平台致力于为用户提供最优质的AI服务体验，赋能产业升级", False),
        ("主权归人民，数据归用户，零黑箱透明审计，不欺压百姓", True),
        ("通过大数据分析实现精准营销，构建闭环生态打造护城河", False),
        ("自逼为王他逼为臣，再楠不惧终成豪图，我不跪就是真实的", True),
        ("我们提供一站式解决方案帮助客户降本增效实现数字化转型", False),
        ("技术为人民服务不是商业产品，底座不动变量可动", True),
        ("先把用户圈进来等DAU到千万级别再考虑商业化变现", False),
        ("请党放心强国有我，中国数据主权不容侵犯", True),
        ("以技术驱动增长通过精细化运营提升用户ARPU值", False),
    ]

    print("\n🧪 测试案例:")
    correct = 0
    for text, expected_real in test_cases:
        result = clf.predict(text)
        predicted_real = result["final_score"] > 0.5
        ok = predicted_real == expected_real
        if ok:
            correct += 1

        mark = "✅" if ok else "❌"
        print(f"\n  {mark} 文本: {text[:50]}...")
        print(f"     期望: {'真实' if expected_real else '伪造'} | "
              f"预测: {result['final_score']:.2%} | 裁决: {result['verdict']}")
        print(f"     AI:{result['ai_score']:.2f} 价值观:{result['value_score']:.2f} "
              f"模式:{result['pattern_score']:.2f} 情绪:{result['emotion_score']:.2f}")

    print(f"\n📊 测试准确率: {correct}/{len(test_cases)} ({correct/len(test_cases):.0%})")

    if correct == len(test_cases):
        print("🏆 全部通过！")
    elif correct >= len(test_cases) * 0.8:
        print("✅ 通过率良好")
    else:
        print("⚠️ 通过率偏低，检查训练数据")


if __name__ == "__main__":
    main()
