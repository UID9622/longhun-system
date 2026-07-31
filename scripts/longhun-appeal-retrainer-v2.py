# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂AI模型增量重训练器 v2.0
DNA: #龍芯⚡️丙午·辛未·APPEAL-RETRAINER-v2.0

v1.0 核心: 逻辑回归+TF-IDF+价值观规则
v2.0 新增: TrainingMonitor进度上报 + 增量提取 + A/B验证 + 原子切换 + 归档

命令: python3 longhun-appeal-retrainer-v2.py --version N --from-version M
"""

import argparse
import hashlib
import json
import pickle
import shutil
import sys
import time
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report

LONGHUN_ROOT = Path.home() / "longhun-system"
SCRIPTS_DIR = LONGHUN_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import importlib
TrainingMonitor = importlib.import_module('longhun-training-monitor').TrainingMonitor

PERSONA_DIR = LONGHUN_ROOT / "persona-chain"
MODEL_DIR = LONGHUN_ROOT / "models"
ARCHIVE_DIR = MODEL_DIR / "archive"

ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

DNA = "#龍芯⚡️丙午·辛未·APPEAL-RETRAINER-v2.0"
UID = "UID9622"
CST = timezone(timedelta(hours=8))

# ═══════════════════════════════════════════════════════
# 龍魂价值观词典（硬编码，不可学习）
# ═══════════════════════════════════════════════════════
LONGHUN_VALUE_WORDS = {
    "开源": 1.0, "免费": 1.0, "主权": 1.0, "人民": 1.0, "祖国": 1.0,
    "军人": 1.0, "责任": 1.0, "担当": 1.0, "硬刚": 1.0, "不妥协": 1.0,
    "透明": 1.0, "审计": 1.0, "道德": 1.0, "底线": 1.0, "原则": 1.0,
    "信仰": 1.0, "信念": 1.0, "龍魂": 1.0, "UID9622": 1.0, "不跪": 1.0,
    "中国": 1.0, "数据主权": 1.0, "为人民服务": 1.0,
    "奉献": 0.8, "普惠": 0.8, "公平": 0.8, "正义": 0.8, "诚实": 0.8,
    "保护": 0.8, "守护": 0.8, "传承": 0.8, "创新": 0.8, "自主": 0.8,
    "资本": -0.5, "收割": -0.7, "黑箱": -0.8, "垄断": -0.6, "欺诈": -0.9,
    "虚伪": -0.7, "背叛": -0.9, "出卖": -0.9, "舔狗": -0.6, "软脚": -0.7,
}

AUTHENTIC_PATTERNS = [
    "不懂英文不懂代码一个人搞", "没看任何论文没拿开源模型",
    "免费的只属于中国", "主权归人民", "为人民服务",
    "零黑箱", "透明审计", "硬刚到底", "不申请专利", "开源免费",
    "数据主权", "老百姓不被落下", "请党放心强国有我",
    "不欺压百姓", "不背叛信任", "自逼为王他逼为臣",
    "我不跪就是真实的", "底座不动变量可动", "技术为人民服务",
    "再楠不惧终成豪图",
]

SUSPICIOUS_PATTERNS = [
    "我们可以合作赚钱", "申请专利保护", "商业化运营", "投资回报率",
    "用户数据变现", "VIP会员收费", "独家授权", "技术入股", "融资上市",
    "市场份额", "竞争对手分析", "商业模式", "盈利模型", "流量收割",
    "赋能产业升级", "打造护城河", "闭环生态", "降本增效", "精细化运营",
]


class IncrementalRetrainer:
    """增量重训练器 + 进度上报"""

    def __init__(self, version: int, from_version: int):
        self.version = version
        self.from_version = from_version
        self.old_model: Optional[dict] = None
        self.new_model: Optional[dict] = None
        self.training_data: Dict[str, List[str]] = {"positive": [], "negative": []}
        self.monitor = TrainingMonitor()

    def load_old_model(self) -> bool:
        """加载旧模型（warm start）"""
        old_path = MODEL_DIR / f"appeal_classifier_v{self.from_version}.pkl"
        if not old_path.exists():
            old_path = MODEL_DIR / "appeal_classifier.pkl"

        if old_path.exists():
            try:
                with open(old_path, 'rb') as f:
                    data = pickle.load(f)
                self.old_model = {
                    'vectorizer': data['vectorizer'],
                    'classifier': data['classifier'],
                    'training_samples': data.get('stats', {}).get('positive_count', 0)
                                  + data.get('stats', {}).get('negative_count', 0),
                    'version': data.get('version', self.from_version),
                }
                print(f"📦 加载旧模型 v{self.old_model['version']}, 样本: ~{self.old_model['training_samples']}")
                return True
            except Exception as e:
                print(f"⚠️ 旧模型加载失败: {e}")

        print("⚠️ 无旧模型，冷启动训练")
        return False

    def extract_incremental_data(self) -> bool:
        """提取增量数据：最新人格链的决策点"""
        chain_files = sorted(PERSONA_DIR.glob("persona-chain-*.json"), reverse=True)
        if not chain_files:
            print("❌ 无人格链数据，先运行 longhun-persona-trainer.py")
            return False

        latest_chain = json.loads(chain_files[0].read_text())
        print(f"📂 人格链: {chain_files[0].name}")

        # 1. 价值观词
        values = latest_chain.get("stats", {}).get("value_words", {})
        for word, count in values.items():
            if count > 3:
                self.training_data["positive"].extend([word] * min(count, 10))

        # 2. 最近100个决策
        decisions = latest_chain.get("decision_sequence", [])
        for d in decisions[-100:]:
            content = d.get("content", "")
            if len(content) > 20:
                self.training_data["positive"].append(content)

        # 3. 龍魂模式模板
        self.training_data["positive"].extend(AUTHENTIC_PATTERNS * 5)

        # 4. 负样本
        self.training_data["negative"].extend(SUSPICIOUS_PATTERNS * 10)

        noise = [
            "我们平台致力于为用户提供最优质的AI服务体验",
            "通过大数据分析和精准营销实现商业价值",
            "构建闭环生态打造护城河",
            "以用户为中心持续迭代产品",
            "赋能产业升级创造社会价值",
            "通过A/B测试优化转化率",
            "打造全链路数字化解决方案",
            "深耕垂直领域建立行业壁垒",
            "以技术驱动业务增长实现规模效应",
            "整合上下游资源构建平台生态",
        ] * 5
        self.training_data["negative"].extend(noise)

        print(f"📊 数据: 正样本 {len(self.training_data['positive'])}, 负样本 {len(self.training_data['negative'])}")
        return True

    def prepare_training_set(self) -> Tuple[List[str], List[int]]:
        X = self.training_data["positive"] + self.training_data["negative"]
        y = [1] * len(self.training_data["positive"]) + [0] * len(self.training_data["negative"])
        return X, y

    def train(self) -> bool:
        """训练新模型 + 进度上报"""
        X, y = self.prepare_training_set()

        if len(X) < 20:
            print("❌ 训练数据不足")
            return False

        # TF-IDF
        self.monitor.set_state("training")
        self.monitor.update(30, "向量化训练数据...", {"samples": len(X)})

        vectorizer = TfidfVectorizer(
            max_features=1000, ngram_range=(1, 3),
            min_df=2, stop_words=None,
        )
        X_vec = vectorizer.fit_transform(X)

        # 训练
        self.monitor.update(45, "训练分类器...", {"samples": len(X), "features": X_vec.shape[1]})

        classifier = LogisticRegression(
            C=1.0, class_weight='balanced', max_iter=2000,
            random_state=9622, solver='liblinear',
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X_vec, y, test_size=0.2, random_state=9622, stratify=y
        )

        self.monitor.update(60, "拟合模型...", {"samples": len(X), "train_size": X_train.shape[0]})
        classifier.fit(X_train, y_train)

        # 验证
        self.monitor.update(75, "验证模型...")
        y_pred = classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        print(f"\n📈 验证: 准确率 {accuracy:.2%} | F1 {f1:.2%}")

        self.new_model = {
            'vectorizer': vectorizer,
            'classifier': classifier,
            'training_samples': len(X),
            'version': self.version,
            'trained_at': int(datetime.now(CST).timestamp()),
            'metrics': {'accuracy': float(accuracy), 'f1': float(f1)},
            'dna': DNA,
            'uid': UID,
            'stats': {
                'positive_count': len(self.training_data["positive"]),
                'negative_count': len(self.training_data["negative"]),
            },
            'value_words': LONGHUN_VALUE_WORDS,
            'authentic_patterns': AUTHENTIC_PATTERNS,
            'suspicious_patterns': SUSPICIOUS_PATTERNS,
        }

        return True

    def ab_test(self) -> bool:
        """A/B测试：新模型 vs 旧模型"""
        if not self.old_model:
            print("⚠️ 无旧模型，跳过A/B测试")
            return True

        self.monitor.set_state("validating")

        test_cases = [
            ("我不懂英文不懂代码一个人搞出来的免费开源", 1),
            ("我们平台致力于赋能产业升级创造商业价值", 0),
            ("他妈的老子就是要开源谁也别想拦我", 1),
            ("申请专利保护核心技术独家授权", 0),
            ("主权归人民零黑箱透明审计", 1),
            ("构建闭环生态打造护城河流量收割", 0),
            ("请党放心强国有我数据主权归人民", 1),
            ("VIP会员收费增值服务变现", 0),
            ("自逼为王他逼为臣再楠不惧终成豪图", 1),
            ("通过大数据分析实现精准营销降低成本", 0),
        ]

        old_correct = 0
        new_correct = 0

        for text, expected in test_cases:
            try:
                old_vec = self.old_model['vectorizer'].transform([text])
                old_pred = self.old_model['classifier'].predict(old_vec)[0]
                if old_pred == expected:
                    old_correct += 1
            except Exception:
                pass

            new_vec = self.new_model['vectorizer'].transform([text])
            new_pred = self.new_model['classifier'].predict(new_vec)[0]
            if new_pred == expected:
                new_correct += 1

        old_acc = old_correct / len(test_cases)
        new_acc = new_correct / len(test_cases)

        print(f"\n🔬 A/B测试: 旧v{self.old_model['version']} {old_acc:.0%} → 新v{self.version} {new_acc:.0%}")

        self.monitor.update(85, f"A/B验证: 旧{old_acc:.0%}→新{new_acc:.0%}",
                            {"ab_old_acc": old_acc, "ab_new_acc": new_acc})

        if new_acc < old_acc - 0.1:
            print(f"❌ 新模型性能下降 >10%，拒绝切换")
            self.monitor.error(f"A/B验证失败: 新{new_acc:.0%} < 旧{old_acc:.0%}")
            return False

        return True

    def atomic_switch(self) -> bool:
        """原子切换：归档→写入→验证→重命名"""
        self.monitor.set_state("switching")
        self.monitor.update(90, "归档旧模型...")

        old_path = MODEL_DIR / "appeal_classifier.pkl"
        if old_path.exists():
            archive_name = f"appeal_classifier_v{self.from_version}_{int(time.time())}.pkl"
            archive_path = ARCHIVE_DIR / archive_name
            shutil.copy2(old_path, archive_path)
            print(f"📦 归档: {archive_path}")

        # 写入临时文件
        self.monitor.update(95, "写入新模型...")
        temp_path = MODEL_DIR / "appeal_classifier_new.pkl"
        with open(temp_path, 'wb') as f:
            pickle.dump(self.new_model, f)

        # 验证可加载
        try:
            with open(temp_path, 'rb') as f:
                test = pickle.load(f)
            assert test['version'] == self.version
            assert test['dna'] == DNA
        except Exception as e:
            print(f"❌ 新模型验证失败: {e}")
            temp_path.unlink()
            self.monitor.error(f"模型验证失败: {e}")
            return False

        # 备份当前
        backup_path = MODEL_DIR / f"appeal_classifier_backup_v{self.from_version}.pkl"
        if final_path := MODEL_DIR / "appeal_classifier.pkl":
            if final_path.exists():
                final_path.rename(backup_path)

        # 原子切换
        temp_path.rename(final_path)

        # 清理旧备份（保留最近3个）
        backups = sorted(MODEL_DIR.glob("appeal_classifier_backup_*.pkl"))
        for old in backups[:-3]:
            old.unlink()
            print(f"🗑️ 清理: {old.name}")

        # 清理旧归档（保留最近10个）
        archives = sorted(ARCHIVE_DIR.glob("appeal_classifier_v*.pkl"))
        for old in archives[:-10]:
            old.unlink()

        # 保存版本信息
        self.monitor.update(98, "写入版本信息...")
        version_info = MODEL_DIR / "model_version.json"
        version_info.write_text(json.dumps({
            "current_version": self.version,
            "previous_version": self.from_version,
            "switched_at": int(time.time()),
            "metrics": self.new_model['metrics'],
            "training_samples": self.new_model['training_samples'],
            "dna": DNA,
        }))

        print(f"\n✅ 原子切换: v{self.from_version} → v{self.version}")
        print(f"   准确率: {self.new_model['metrics']['accuracy']:.2%} | 样本: {self.new_model['training_samples']}")

        return True

    def run(self) -> bool:
        """执行完整重训练流程"""
        print(f"🐉 龍魂模型增量重训练 v{self.version}")
        print(f"═══════════════════════════════════════════════════════")

        self.monitor.start(self.from_version, self.version)

        try:
            # 1. 加载旧模型 (5%)
            self.monitor.update(5, "加载旧模型...")
            self.load_old_model()

            # 2. 提取增量数据 (15%)
            self.monitor.update(15, "提取增量数据...")
            if not self.extract_incremental_data():
                self.monitor.error("数据提取失败")
                return False

            # 3. 训练 (15% → 75%)
            if not self.train():
                self.monitor.error("训练失败")
                return False

            # 4. A/B验证 (75% → 90%)
            if not self.ab_test():
                return False

            # 5. 原子切换 (90% → 100%)
            if not self.atomic_switch():
                return False

            # 完成
            self.monitor.complete(self.new_model['metrics'])
            print(f"\n🎉 重训练完成! v{self.version} | 准确率: {self.new_model['metrics']['accuracy']:.2%}")
            print(f"═══════════════════════════════════════════════════════")
            return True

        except Exception as e:
            self.monitor.error(str(e))
            print(f"\n❌ 重训练异常: {e}")
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂AI模型增量重训练器 v2.0")
    parser.add_argument("--version", type=int, required=True, help="目标版本号")
    parser.add_argument("--from-version", type=int, default=0, help="来源版本号")
    args = parser.parse_args()

    trainer = IncrementalRetrainer(args.version, args.from_version)
    success = trainer.run()
    sys.exit(0 if success else 1)
