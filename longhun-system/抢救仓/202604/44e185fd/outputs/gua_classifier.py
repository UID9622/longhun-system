#!/usr/bin/env python3
"""
龍魂卦分类器 · Trainable Hexagram Classifier v1.0
================================================
UID9622 原创 · 三才算法驱动

将任意文本/意图映射到易经64卦体系。
支持：自定义训练、增量学习、模型导出/加载。

核心思路（三才映射）：
  天（输入层）→ 文本特征提取
  地（处理层）→ 分类模型推理
  人（决策层）→ 卦象解读 + 行动建议

用法：
  # 训练
  python gua_classifier.py train --data training_data.json --output model.pkl

  # 预测
  python gua_classifier.py predict --model model.pkl --text "我想学AI但不知道从哪开始"

  # 增量训练
  python gua_classifier.py retrain --model model.pkl --data new_data.json
"""

import json
import hashlib
import pickle
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder


# ============================================================
# 一、64卦定义（核心兵种表）
# ============================================================

GUA_64 = {
    1: {"name": "乾", "symbol": "☰☰", "nature": "天行健", "action": "自强不息，全力推进"},
    2: {"name": "坤", "symbol": "☷☷", "nature": "地势坤", "action": "厚德载物，稳扎稳打"},
    3: {"name": "屯", "symbol": "☵☳", "nature": "万物初生", "action": "艰难起步，不急不躁"},
    4: {"name": "蒙", "symbol": "☶☵", "nature": "启蒙求知", "action": "虚心学习，找到导师"},
    5: {"name": "需", "symbol": "☵☰", "nature": "等待时机", "action": "耐心准备，蓄势待发"},
    6: {"name": "讼", "symbol": "☰☵", "nature": "争端冲突", "action": "避免争执，求同存异"},
    7: {"name": "师", "symbol": "☷☵", "nature": "统帅之道", "action": "组织协调，纪律先行"},
    8: {"name": "比", "symbol": "☵☷", "nature": "亲和团结", "action": "寻找盟友，合作共赢"},
    9: {"name": "小畜", "symbol": "☴☰", "nature": "小有积蓄", "action": "积少成多，持续积累"},
    10: {"name": "履", "symbol": "☰☱", "nature": "谨慎行走", "action": "小心实践，步步为营"},
    11: {"name": "泰", "symbol": "☷☰", "nature": "天地交泰", "action": "顺势而为，大胆推进"},
    12: {"name": "否", "symbol": "☰☷", "nature": "天地不交", "action": "韬光养晦，等待转机"},
    13: {"name": "同人", "symbol": "☰☲", "nature": "志同道合", "action": "团结协作，开放分享"},
    14: {"name": "大有", "symbol": "☲☰", "nature": "大有收获", "action": "乘胜追击，扩大成果"},
    15: {"name": "谦", "symbol": "☷☶", "nature": "谦虚低调", "action": "保持谦逊，稳步前行"},
    16: {"name": "豫", "symbol": "☳☷", "nature": "喜悦准备", "action": "做好规划，享受过程"},
    17: {"name": "随", "symbol": "☱☳", "nature": "顺时而动", "action": "灵活应变，跟随趋势"},
    18: {"name": "蛊", "symbol": "☶☴", "nature": "整治腐败", "action": "清理遗留问题，重构系统"},
    19: {"name": "临", "symbol": "☷☱", "nature": "居高临下", "action": "以身作则，引领方向"},
    20: {"name": "观", "symbol": "☴☷", "nature": "观察全局", "action": "先看后做，全面分析"},
    21: {"name": "噬嗑", "symbol": "☲☳", "nature": "果断处理", "action": "当断则断，清除障碍"},
    22: {"name": "贲", "symbol": "☶☲", "nature": "文饰修养", "action": "注重细节，美化输出"},
    23: {"name": "剥", "symbol": "☶☷", "nature": "剥落衰退", "action": "收缩防守，保存实力"},
    24: {"name": "复", "symbol": "☷☳", "nature": "一阳来复", "action": "重新出发，小步试探"},
    25: {"name": "无妄", "symbol": "☰☳", "nature": "纯真无妄", "action": "遵循本心，不投机取巧"},
    26: {"name": "大畜", "symbol": "☶☰", "nature": "大量积蓄", "action": "大量输入，深度积累"},
    27: {"name": "颐", "symbol": "☶☳", "nature": "养育滋养", "action": "充电休息，养精蓄锐"},
    28: {"name": "大过", "symbol": "☱☴", "nature": "超越极限", "action": "大胆突破，但注意风险"},
    29: {"name": "坎", "symbol": "☵☵", "nature": "重重困难", "action": "坚持不放弃，穿越困境"},
    30: {"name": "离", "symbol": "☲☲", "nature": "光明依附", "action": "借助外力，照亮方向"},
    31: {"name": "咸", "symbol": "☱☶", "nature": "感应相通", "action": "用心感受，建立连接"},
    32: {"name": "恒", "symbol": "☳☴", "nature": "持之以恒", "action": "坚持长期主义，不动摇"},
    33: {"name": "遁", "symbol": "☰☶", "nature": "战略撤退", "action": "暂时后退，保全大局"},
    34: {"name": "大壮", "symbol": "☳☰", "nature": "力量壮大", "action": "以强击弱，但不可鲁莽"},
    35: {"name": "晋", "symbol": "☲☷", "nature": "晋升前进", "action": "稳步上升，展示实力"},
    36: {"name": "明夷", "symbol": "☷☲", "nature": "光明受损", "action": "隐藏实力，暗中积蓄"},
    37: {"name": "家人", "symbol": "☴☲", "nature": "家庭和睦", "action": "先治内再治外，基础先行"},
    38: {"name": "睽", "symbol": "☲☱", "nature": "背离分歧", "action": "求同存异，找到共识"},
    39: {"name": "蹇", "symbol": "☵☶", "nature": "行路艰难", "action": "迂回前进，借力突围"},
    40: {"name": "解", "symbol": "☳☵", "nature": "化解困局", "action": "抓住机会，快速解决"},
    41: {"name": "损", "symbol": "☶☱", "nature": "减损节制", "action": "精简聚焦，断舍离"},
    42: {"name": "益", "symbol": "☴☳", "nature": "增益补充", "action": "抓住增长机会，扩大投入"},
    43: {"name": "夬", "symbol": "☱☰", "nature": "决断突破", "action": "下定决心，果断行动"},
    44: {"name": "姤", "symbol": "☰☴", "nature": "偶然相遇", "action": "警惕诱惑，保持清醒"},
    45: {"name": "萃", "symbol": "☱☷", "nature": "聚集汇合", "action": "整合资源，集中力量"},
    46: {"name": "升", "symbol": "☷☴", "nature": "持续上升", "action": "稳步攀升，不骄不躁"},
    47: {"name": "困", "symbol": "☱☵", "nature": "困境受限", "action": "保持乐观，寻找出路"},
    48: {"name": "井", "symbol": "☵☴", "nature": "源源不断", "action": "深挖根基，持续供给"},
    49: {"name": "革", "symbol": "☱☲", "nature": "变革创新", "action": "大胆改革，破旧立新"},
    50: {"name": "鼎", "symbol": "☲☴", "nature": "革新承载", "action": "建立新系统，承载未来"},
    51: {"name": "震", "symbol": "☳☳", "nature": "震动觉醒", "action": "从冲击中学习，保持警觉"},
    52: {"name": "艮", "symbol": "☶☶", "nature": "止步思考", "action": "停下来想清楚，再出发"},
    53: {"name": "渐", "symbol": "☴☶", "nature": "循序渐进", "action": "一步一步来，不跳步"},
    54: {"name": "归妹", "symbol": "☳☱", "nature": "有所归属", "action": "找到定位，安心发展"},
    55: {"name": "丰", "symbol": "☳☲", "nature": "丰盛鼎盛", "action": "趁势扩张，但防盛极必衰"},
    56: {"name": "旅", "symbol": "☲☶", "nature": "旅途探索", "action": "保持开放，探索新领域"},
    57: {"name": "巽", "symbol": "☴☴", "nature": "柔顺渗透", "action": "温和推进，润物细无声"},
    58: {"name": "兑", "symbol": "☱☱", "nature": "喜悦交流", "action": "分享传播，以教促学"},
    59: {"name": "涣", "symbol": "☴☵", "nature": "散开扩展", "action": "打破边界，跨领域融合"},
    60: {"name": "节", "symbol": "☵☱", "nature": "节制有度", "action": "设定边界，适度投入"},
    61: {"name": "中孚", "symbol": "☴☱", "nature": "诚信中正", "action": "以诚为本，言行一致"},
    62: {"name": "小过", "symbol": "☳☶", "nature": "小有过越", "action": "小步试错，快速迭代"},
    63: {"name": "既济", "symbol": "☵☲", "nature": "已经完成", "action": "巩固成果，防止退步"},
    64: {"name": "未济", "symbol": "☲☵", "nature": "尚未完成", "action": "继续前进，终点即起点"},
}


# ============================================================
# 二、默认训练数据（种子数据 · 可扩展）
# ============================================================

def get_seed_training_data():
    """返回种子训练数据，覆盖常见意图场景"""
    data = [
        # 乾卦 - 全力推进
        {"text": "我要全力以赴把这个项目做完", "gua": 1},
        {"text": "现在状态很好，要趁势冲刺", "gua": 1},
        {"text": "不要犹豫了，直接干", "gua": 1},
        {"text": "这个方向是对的，加速推进", "gua": 1},

        # 蒙卦 - 启蒙学习
        {"text": "我想学AI但不知道从哪开始", "gua": 4},
        {"text": "这个概念完全看不懂", "gua": 4},
        {"text": "有没有入门教程推荐", "gua": 4},
        {"text": "我是零基础的小白", "gua": 4},

        # 需卦 - 等待时机
        {"text": "现在不是做这件事的好时候", "gua": 5},
        {"text": "再等等看情况", "gua": 5},
        {"text": "条件还不成熟", "gua": 5},
        {"text": "先准备好再说", "gua": 5},

        # 师卦 - 组织协调
        {"text": "怎么管理这个团队", "gua": 7},
        {"text": "数字大军怎么组建", "gua": 7},
        {"text": "需要一个清晰的组织架构", "gua": 7},
        {"text": "人多了就要有纪律", "gua": 7},

        # 小畜 - 持续积累
        {"text": "每天学一点点", "gua": 9},
        {"text": "积少成多慢慢来", "gua": 9},
        {"text": "先把基础打好", "gua": 9},
        {"text": "不贪多，稳扎稳打", "gua": 9},

        # 泰卦 - 顺势而为
        {"text": "一切都很顺利，继续", "gua": 11},
        {"text": "天时地利人和", "gua": 11},
        {"text": "项目进展超预期", "gua": 11},
        {"text": "现在是最好的时机", "gua": 11},

        # 否卦 - 韬光养晦
        {"text": "现在做什么都不顺", "gua": 12},
        {"text": "环境不好，先忍忍", "gua": 12},
        {"text": "资源不足，不能硬拼", "gua": 12},
        {"text": "退一步海阔天空", "gua": 12},

        # 谦卦 - 保持谦逊
        {"text": "不要太张扬", "gua": 15},
        {"text": "做出成绩也要低调", "gua": 15},
        {"text": "跟别人学习他们的长处", "gua": 15},
        {"text": "承认自己还有很多不足", "gua": 15},

        # 蛊卦 - 整治重构
        {"text": "代码太乱了需要重构", "gua": 18},
        {"text": "系统有很多历史遗留问题", "gua": 18},
        {"text": "这个项目需要清理", "gua": 18},
        {"text": "之前的设计有问题要改", "gua": 18},

        # 观卦 - 观察分析
        {"text": "先看看别人怎么做的", "gua": 20},
        {"text": "我要研究一下市场", "gua": 20},
        {"text": "先分析问题再动手", "gua": 20},
        {"text": "观察一下趋势走向", "gua": 20},

        # 大畜 - 大量积累
        {"text": "我要大量阅读论文", "gua": 26},
        {"text": "疯狂学习阶段", "gua": 26},
        {"text": "把所有相关资料都收集起来", "gua": 26},
        {"text": "深度积累期不着急输出", "gua": 26},

        # 坎卦 - 穿越困境
        {"text": "遇到了很大的困难", "gua": 29},
        {"text": "怎么都解决不了这个bug", "gua": 29},
        {"text": "感觉很迷茫不知道方向", "gua": 29},
        {"text": "接连失败了好几次", "gua": 29},

        # 恒卦 - 坚持长期
        {"text": "这件事要坚持做下去", "gua": 32},
        {"text": "长期主义", "gua": 32},
        {"text": "每天坚持不间断", "gua": 32},
        {"text": "持之以恒才能看到结果", "gua": 32},

        # 损卦 - 精简断舍离
        {"text": "功能太多了要砍掉一些", "gua": 41},
        {"text": "聚焦核心不要贪多", "gua": 41},
        {"text": "减少不必要的学习任务", "gua": 41},
        {"text": "做减法比做加法更难", "gua": 41},

        # 革卦 - 变革创新
        {"text": "现有的方式不行了要改革", "gua": 49},
        {"text": "需要全新的思路", "gua": 49},
        {"text": "打破传统做法", "gua": 49},
        {"text": "创新是唯一的出路", "gua": 49},

        # 鼎卦 - 建立新系统
        {"text": "要搭建一个全新的架构", "gua": 50},
        {"text": "从零开始设计系统", "gua": 50},
        {"text": "龍魂系统需要升级换代", "gua": 50},
        {"text": "建立新的知识管理体系", "gua": 50},

        # 渐卦 - 循序渐进
        {"text": "一步一步来不要急", "gua": 53},
        {"text": "按照计划逐步推进", "gua": 53},
        {"text": "不能跳步骤", "gua": 53},
        {"text": "稳步前进", "gua": 53},

        # 未济 - 尚未完成
        {"text": "还没做完继续加油", "gua": 64},
        {"text": "任务还在进行中", "gua": 64},
        {"text": "完成了80%还差一点", "gua": 64},
        {"text": "终点就是新的起点", "gua": 64},
    ]
    return data


# ============================================================
# 三、卦分类器核心（可训练 Pipeline）
# ============================================================

class GuaClassifier:
    """
    龍魂卦分类器 · 可训练版

    内部用 TF-IDF + SGD 分类器，支持：
    - 从种子数据训练
    - 从自定义数据训练
    - 增量学习（partial_fit）
    - 模型导出/加载
    - 预测 + 卦象解读
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            analyzer='char_wb',  # 字符级n-gram，对中文更友好
            ngram_range=(1, 4),
            max_features=5000,
            sublinear_tf=True
        )
        self.classifier = SGDClassifier(
            loss='modified_huber',  # 输出概率
            alpha=1e-4,
            max_iter=1000,
            random_state=9622,  # UID9622 专属种子
            class_weight='balanced'
        )
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        self.training_count = 0
        self.version = "1.0.0"
        self.created_at = datetime.now().isoformat()

    def train(self, data, verbose=True):
        """
        从数据训练模型
        data: [{"text": "...", "gua": int}, ...]
        """
        texts = [d["text"] for d in data]
        labels = [d["gua"] for d in data]

        # 编码标签
        encoded_labels = self.label_encoder.fit_transform(labels)

        # 特征提取
        X = self.vectorizer.fit_transform(texts)

        # 训练分类器
        self.classifier.fit(X, encoded_labels)

        self.is_trained = True
        self.training_count = len(data)

        if verbose:
            # 交叉验证评估
            if len(set(labels)) >= 2 and len(data) >= 10:
                n_splits = min(5, min(np.bincount(encoded_labels)))
                if n_splits >= 2:
                    scores = cross_val_score(
                        self.classifier, X, encoded_labels,
                        cv=n_splits, scoring='accuracy'
                    )
                    print(f"  交叉验证准确率: {scores.mean():.2%} (±{scores.std():.2%})")

            print(f"  训练样本数: {len(data)}")
            print(f"  卦象类别数: {len(set(labels))}")
            print(f"  特征维度: {X.shape[1]}")

    def predict(self, text, top_k=3):
        """
        预测文本对应的卦象
        返回 top_k 个最可能的卦象及概率
        """
        if not self.is_trained:
            raise RuntimeError("模型未训练！请先 train() 或 load()")

        X = self.vectorizer.transform([text])
        probs = self.classifier.predict_proba(X)[0]

        # 获取 top_k 结果
        top_indices = np.argsort(probs)[::-1][:top_k]
        results = []
        for idx in top_indices:
            gua_num = self.label_encoder.inverse_transform([idx])[0]
            gua_info = GUA_64.get(gua_num, {"name": "未知", "nature": "未知", "action": "未知"})
            results.append({
                "gua_number": int(gua_num),
                "gua_name": gua_info["name"],
                "symbol": gua_info.get("symbol", ""),
                "nature": gua_info["nature"],
                "action": gua_info["action"],
                "confidence": float(probs[idx])
            })

        return results

    def retrain(self, new_data, verbose=True):
        """
        增量训练（在现有模型基础上追加数据）
        """
        if not self.is_trained:
            print("⚠️ 模型未训练，将执行完整训练...")
            self.train(new_data, verbose)
            return

        texts = [d["text"] for d in new_data]
        labels = [d["gua"] for d in new_data]

        # 需要确保所有新标签都在 encoder 中
        all_known = set(self.label_encoder.classes_)
        new_labels = set(labels) - all_known
        if new_labels:
            # 重新 fit encoder 包含新标签
            all_labels = list(all_known) + list(new_labels)
            self.label_encoder.fit(all_labels)
            if verbose:
                print(f"  新增卦象类别: {new_labels}")

        encoded_labels = self.label_encoder.transform(labels)
        X = self.vectorizer.transform(texts)

        # partial_fit 增量学习
        self.classifier.partial_fit(X, encoded_labels)
        self.training_count += len(new_data)

        if verbose:
            print(f"  增量训练样本: {len(new_data)}")
            print(f"  累计训练样本: {self.training_count}")

    def save(self, path):
        """导出模型"""
        model_data = {
            "vectorizer": self.vectorizer,
            "classifier": self.classifier,
            "label_encoder": self.label_encoder,
            "is_trained": self.is_trained,
            "training_count": self.training_count,
            "version": self.version,
            "created_at": self.created_at,
            "saved_at": datetime.now().isoformat()
        }
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
        # 生成 DNA 追溯码
        with open(path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()[:8].upper()
        dna_code = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-MODEL-{file_hash}"
        print(f"  模型已保存: {path}")
        print(f"  DNA追溯码: {dna_code}")
        return dna_code

    def load(self, path):
        """加载模型"""
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        self.vectorizer = model_data["vectorizer"]
        self.classifier = model_data["classifier"]
        self.label_encoder = model_data["label_encoder"]
        self.is_trained = model_data["is_trained"]
        self.training_count = model_data["training_count"]
        self.version = model_data.get("version", "1.0.0")
        self.created_at = model_data.get("created_at", "unknown")
        print(f"  模型已加载: {path}")
        print(f"  训练样本数: {self.training_count}")
        print(f"  版本: {self.version}")

    def export_training_template(self, path):
        """导出训练数据模板 JSON"""
        template = {
            "_说明": "在 data 数组中添加训练样本，text=文本，gua=卦号(1-64)",
            "_卦号参考": {str(k): v["name"] + " · " + v["nature"] for k, v in GUA_64.items()},
            "data": [
                {"text": "示例文本1", "gua": 1},
                {"text": "示例文本2", "gua": 4}
            ]
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        print(f"  训练模板已导出: {path}")


# ============================================================
# 四、CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="龍魂卦分类器 · Trainable Hexagram Classifier",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 用种子数据训练并保存
  python gua_classifier.py train --output gua_model.pkl

  # 用自定义数据训练
  python gua_classifier.py train --data my_training.json --output gua_model.pkl

  # 预测
  python gua_classifier.py predict --model gua_model.pkl --text "我遇到了很大困难"

  # 增量训练
  python gua_classifier.py retrain --model gua_model.pkl --data new_data.json

  # 导出训练模板
  python gua_classifier.py template --output training_template.json
        """
    )
    sub = parser.add_subparsers(dest="command")

    # train
    p_train = sub.add_parser("train", help="训练模型")
    p_train.add_argument("--data", help="训练数据 JSON 文件（省略则用种子数据）")
    p_train.add_argument("--output", default="gua_model.pkl", help="模型输出路径")

    # predict
    p_pred = sub.add_parser("predict", help="预测卦象")
    p_pred.add_argument("--model", default="gua_model.pkl", help="模型路径")
    p_pred.add_argument("--text", required=True, help="要预测的文本")
    p_pred.add_argument("--top", type=int, default=3, help="返回前N个结果")

    # retrain
    p_retrain = sub.add_parser("retrain", help="增量训练")
    p_retrain.add_argument("--model", required=True, help="已有模型路径")
    p_retrain.add_argument("--data", required=True, help="新训练数据 JSON")

    # template
    p_template = sub.add_parser("template", help="导出训练数据模板")
    p_template.add_argument("--output", default="training_template.json", help="模板输出路径")

    args = parser.parse_args()

    if args.command == "train":
        print("🧬 龍魂卦分类器 · 训练中...")
        clf = GuaClassifier()
        if args.data:
            with open(args.data, 'r', encoding='utf-8') as f:
                raw = json.load(f)
                data = raw if isinstance(raw, list) else raw.get("data", [])
            print(f"  加载训练数据: {args.data} ({len(data)} 条)")
        else:
            data = get_seed_training_data()
            print(f"  使用种子数据 ({len(data)} 条)")
        clf.train(data)
        clf.save(args.output)
        print("✅ 训练完成!")

    elif args.command == "predict":
        clf = GuaClassifier()
        clf.load(args.model)
        results = clf.predict(args.text, top_k=args.top)
        print(f"\n🔮 输入: \"{args.text}\"")
        print("─" * 50)
        for i, r in enumerate(results):
            bar = "█" * int(r['confidence'] * 30)
            print(f"  {'🥇' if i==0 else '🥈' if i==1 else '🥉'} 第{r['gua_number']}卦 · {r['gua_name']} {r['symbol']}")
            print(f"     {r['nature']} → {r['action']}")
            print(f"     置信度: {r['confidence']:.1%} {bar}")
            print()

    elif args.command == "retrain":
        clf = GuaClassifier()
        clf.load(args.model)
        with open(args.data, 'r', encoding='utf-8') as f:
            raw = json.load(f)
            data = raw if isinstance(raw, list) else raw.get("data", [])
        print(f"🔄 增量训练 ({len(data)} 条新数据)...")
        clf.retrain(data)
        clf.save(args.model)
        print("✅ 增量训练完成!")

    elif args.command == "template":
        clf = GuaClassifier()
        clf.export_training_template(args.output)
        print("✅ 模板导出完成!")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
