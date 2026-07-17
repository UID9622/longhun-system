# -*- coding: utf-8 -*-
"""
#龍芯⚡️2026-06-18-CNSH-TRANSLATOR-v5.0
# 🟢 审计通过: 通心译翻译器完整实现
# 🔒 AI Truth Protocol: 所有声明均为真实
# 🤝 君子协议: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

通心译翻译器 - 24核心AI术语双向映射
中英实时翻译 · 批量转换 · 中央藏经阁集成
"""

import re
import json
import hashlib
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime


# ========== 24核心AI术语双向映射 ==========
TERM_MAP: Dict[str, str] = {
    "Prompt": "道令",
    "Agent": "灵使",
    "RAG": "博古通今",
    "LLM": "大语言模型",
    "Token": "字元",
    "Embedding": "嵌入向量",
    "Vector": "向量",
    "Cluster": "聚类",
    "Fine-tune": "精调",
    "Inference": "推理",
    "Training": "训练",
    "Dataset": "数据集",
    "Checkpoint": "检查点",
    "Epoch": "轮次",
    "Batch": "批次",
    "Learning Rate": "学习率",
    "Loss": "损失",
    "Gradient": "梯度",
    "Backpropagation": "反向传播",
    "Attention": "注意力",
    "Transformer": "变换器",
    "Convolution": "卷积",
    "Pooling": "池化",
    "Regularization": "正则化"
}

# 反向映射：中文 → 英文
REVERSE_MAP: Dict[str, str] = {v: k for k, v in TERM_MAP.items()}

# 排序术语（长词优先匹配）
SORTED_EN_TERMS = sorted(TERM_MAP.keys(), key=len, reverse=True)
SORTED_CN_TERMS = sorted(REVERSE_MAP.keys(), key=len, reverse=True)

# 术语分类
术语分类: Dict[str, List[str]] = {
    "基础概念": ["Prompt", "Agent", "RAG", "LLM", "Token"],
    "数据结构": ["Embedding", "Vector", "Cluster", "Dataset"],
    "训练过程": ["Training", "Fine-tune", "Epoch", "Batch", "Learning Rate"],
    "数学概念": ["Loss", "Gradient", "Backpropagation"],
    "模型架构": ["Attention", "Transformer", "Convolution", "Pooling", "Regularization"],
    "模型管理": ["Inference", "Checkpoint"]
}


@dataclass
class 翻译结果:
    """翻译结果数据结构"""
    原文: str
    译文: str
    术语映射: Dict[str, str]
    翻译方向: str  # "英到中" 或 "中到英"
    时间戳: str
    DNA追溯: str

    def 转字典(self) -> Dict[str, Any]:
        return asdict(self)

    def __repr__(self):
        return f"翻译结果({self.翻译方向}: '{self.原文}' → '{self.译文}')"


class 通心译翻译器:
    """
    通心译翻译器 - 核心翻译引擎
    支持实时翻译、批量转换、术语高亮
    """

    DNA追溯 = "#龍芯⚡️2026-06-18-CNSH-TRANSLATOR-v5.0"

    def __init__(self, 启用藏经阁: bool = True):
        self.术语映射 = TERM_MAP.copy()
        self.反向映射 = REVERSE_MAP.copy()
        self.审计日志: List[Dict] = []
        self.翻译历史: List[翻译结果] = []
        self.启用藏经阁 = 启用藏经阁
        self.藏经阁 = None

        if 启用藏经阁:
            try:
                from .terminology_bank import 中央藏经阁
                self.藏经阁 = 中央藏经阁()
                self.藏经阁.批量导入(self.术语映射)
                self.记录("成功", "中央藏经阁连接成功")
            except Exception as e:
                self.记录("警告", f"中央藏经阁连接失败: {e}")

    def 记录(self, 级别: str, 消息: str) -> None:
        """记录审计日志"""
        self.审计日志.append({
            "级别": 级别,
            "消息": 消息,
            "时间": datetime.now().isoformat(),
            "颜色": {"成功": "🟢", "警告": "🟡", "错误": "🔴"}.get(级别, "⚪")
        })

    # ========== 核心翻译方法 ==========

    def 英文到中文(self, 文本: str) -> str:
        """
        英文术语翻译为中文
        支持整句中的术语替换
        """
        替换记录 = {}
        结果 = 文本

        for 英文术语 in SORTED_EN_TERMS:
            if 英文术语 in 结果:
                中文术语 = self.术语映射[英文术语]
                结果 = 结果.replace(英文术语, 中文术语)
                替换记录[英文术语] = 中文术语

        self.记录("成功", f"英→中翻译完成，替换 {len(替换记录)} 个术语")

        # 保存翻译记录
        if 替换记录:
            翻译记录 = 翻译结果(
                原文=文本,
                译文=结果,
                术语映射=替换记录,
                翻译方向="英到中",
                时间戳=datetime.now().isoformat(),
                DNA追溯=f"{self.DNA追溯}-{hashlib.sha256(文本.encode()).hexdigest()[:8]}"
            )
            self.翻译历史.append(翻译记录)

        return 结果

    def 中文到英文(self, 文本: str) -> str:
        """
        中文术语翻译为英文
        支持整句中的术语替换
        """
        替换记录 = {}
        结果 = 文本

        for 中文术语 in SORTED_CN_TERMS:
            if 中文术语 in 结果:
                英文术语 = self.反向映射[中文术语]
                结果 = 结果.replace(中文术语, 英文术语)
                替换记录[中文术语] = 英文术语

        self.记录("成功", f"中→英翻译完成，替换 {len(替换记录)} 个术语")

        if 替换记录:
            翻译记录 = 翻译结果(
                原文=文本,
                译文=结果,
                术语映射=替换记录,
                翻译方向="中到英",
                时间戳=datetime.now().isoformat(),
                DNA追溯=f"{self.DNA追溯}-{hashlib.sha256(文本.encode()).hexdigest()[:8]}"
            )
            self.翻译历史.append(翻译记录)

        return 结果

    def 智能翻译(self, 文本: str) -> str:
        """
        智能方向检测翻译
        自动判断文本主要语言并进行对应翻译
        """
        中文比重 = self.计算中文比重(文本)

        if 中文比重 > 0.5:
            return self.中文到英文(文本)
        else:
            return self.英文到中文(文本)

    def 计算中文比重(self, 文本: str) -> float:
        """计算文本中中文字符比重"""
        if not 文本:
            return 0.0

        中文字符数 = sum(1 for c in 文本 if '\u4e00' <= c <= '\u9fff')
        return 中文字符数 / len(文本)

    # ========== 批量转换 ==========

    def 批量转换(self, 文本列表: List[str], 方向: str = "auto") -> List[str]:
        """
        批量转换文本列表
        方向: "en2cn" | "cn2en" | "auto"
        """
        结果列表 = []
        for 文本 in 文本列表:
            if 方向 == "en2cn":
                结果列表.append(self.英文到中文(文本))
            elif 方向 == "cn2en":
                结果列表.append(self.中文到英文(文本))
            else:
                结果列表.append(self.智能翻译(文本))
        return 结果列表

    def 转换文件(self, 文件内容: str, 方向: str = "auto") -> Tuple[str, Dict]:
        """
        转换整个文件内容
        返回: (转换后内容, 统计信息)
        """
        原始行数 = 文件内容.count('\n') + 1

        if 方向 == "en2cn":
            结果 = self.英文到中文(文件内容)
        elif 方向 == "cn2en":
            结果 = self.中文到英文(文件内容)
        else:
            结果 = self.智能翻译(文件内容)

        替换数 = sum(1 for 原, 译 in zip(文件内容, 结果) if 原 != 译)

        统计 = {
            "原始行数": 原始行数,
            "替换数": 替换数,
            "方向": 方向,
            "术语命中": len(self.翻译历史[-1].术语映射) if self.翻译历史 else 0
        }

        return 结果, 统计

    # ========== 实时翻译辅助 ==========

    def 获取术语提示(self, 前缀: str) -> List[Dict[str, str]]:
        """
        根据输入前缀获取术语补全提示
        用于编辑器自动补全
        """
        前缀小写 = 前缀.lower()
        提示列表 = []

        # 英文前缀匹配
        for 英文, 中文 in self.术语映射.items():
            if 英文.lower().startswith(前缀小写):
                提示列表.append({
                    "英文": 英文,
                    "中文": 中文,
                    "显示": f"{英文} → {中文}",
                    "类型": "术语"
                })

        # 中文前缀匹配
        for 中文, 英文 in self.反向映射.items():
            if 中文.startswith(前缀):
                提示列表.append({
                    "英文": 英文,
                    "中文": 中文,
                    "显示": f"{中文} ← {英文}",
                    "类型": "术语"
                })

        return 提示列表[:10]  # 最多返回10条

    def 高亮术语(self, 文本: str) -> List[Dict]:
        """
        识别文本中的术语并返回高亮信息
        返回: [{"术语", "位置", "长度", "类型", "翻译"}]
        """
        高亮信息 = []

        for 英文术语 in SORTED_EN_TERMS:
            for match in re.finditer(re.escape(英文术语), 文本):
                高亮信息.append({
                    "术语": 英文术语,
                    "位置": match.start(),
                    "长度": len(英文术语),
                    "类型": "英文术语",
                    "翻译": self.术语映射[英文术语]
                })

        for 中文术语 in SORTED_CN_TERMS:
            for match in re.finditer(re.escape(中文术语), 文本):
                高亮信息.append({
                    "术语": 中文术语,
                    "位置": match.start(),
                    "长度": len(中文术语),
                    "类型": "中文术语",
                    "翻译": self.反向映射[中文术语]
                })

        # 按位置排序
        高亮信息.sort(key=lambda x: x["位置"])
        return 高亮信息

    def 解释术语(self, 术语: str) -> Optional[Dict]:
        """
        获取术语的详细解释
        返回完整术语信息
        """
        英文 = 术语
        中文 = None

        if 术语 in self.术语映射:
            中文 = self.术语映射[术语]
        elif 术语 in self.反向映射:
            英文 = self.反向映射[术语]
            中文 = 术语
        else:
            return None

        # 查找分类
        分类 = "未分类"
        for cat, terms in 术语分类.items():
            if 英文 in terms:
                分类 = cat
                break

        return {
            "英文": 英文,
            "中文": 中文,
            "分类": 分类,
            "说明": self.生成术语说明(英文),
            "相关术语": self.查找相关术语(英文)
        }

    def 生成术语说明(self, 英文术语: str) -> str:
        """生成术语简要说明"""
        说明映射 = {
            "Prompt": "向AI模型发出的指令或问题，引导模型生成期望的输出",
            "Agent": "能够自主感知环境并执行任务的智能体",
            "RAG": "检索增强生成，结合外部知识库提升AI回答质量",
            "LLM": "具有大量参数、能理解生成自然语言的深度学习模型",
            "Token": "文本处理的最小单位，可以是字、词或子词",
            "Embedding": "将高维离散数据映射到低维连续向量空间的技术",
            "Vector": "具有大小和方向的数学对象，AI中表示数据的数值形式",
            "Cluster": "将数据按相似性分组的无监督学习方法",
            "Fine-tune": "在预训练模型基础上针对特定任务的进一步训练",
            "Inference": "使用训练好的模型进行预测或生成的过程",
            "Training": "通过数据调整模型参数以学习模式的过程",
            "Dataset": "用于训练或测试模型的结构化数据集合",
            "Checkpoint": "训练过程中保存的模型状态快照",
            "Epoch": "完整遍历训练数据集一次的迭代周期",
            "Batch": "一次前向/反向传播处理的样本集合",
            "Learning Rate": "控制模型参数更新步幅的超参数",
            "Loss": "衡量模型预测与真实值差距的指标",
            "Gradient": "损失函数对参数的导数，指导参数更新方向",
            "Backpropagation": "从输出层向输入层逐层计算梯度的算法",
            "Attention": "让模型聚焦输入序列重要部分的机制",
            "Transformer": "基于自注意力机制的深度学习架构",
            "Convolution": "通过滑动窗口提取局部特征的运算",
            "Pooling": "降低特征图维度的下采样操作",
            "Regularization": "防止模型过拟合的技术手段"
        }
        return 说明映射.get(英文术语, "暂无说明")

    def 查找相关术语(self, 术语: str, 数量: int = 3) -> List[str]:
        """查找同一分类下的相关术语"""
        英文 = 术语 if 术语 in self.术语映射 else self.反向映射.get(术语, 术语)

        for cat, terms in 术语分类.items():
            if 英文 in terms:
                相关 = [t for t in terms if t != 英文][:数量]
                return [f"{t}→{self.术语映射[t]}" for t in 相关]

        return []

    # ========== 藏经阁集成 ==========

    def 藏经阁查询(self, 查询: str) -> List[Dict]:
        """查询中央藏经阁"""
        if self.藏经阁:
            return self.藏经阁.查询术语(查询)
        return []

    def 藏经阁存储(self, 英文: str, 中文: str, 上下文: str = "") -> bool:
        """向中央藏经阁存储术语"""
        if self.藏经阁:
            try:
                self.藏经阁.存储术语(英文, 中文, 上下文)
                return True
            except Exception as e:
                self.记录("错误", f"藏经阁存储失败: {e}")
        return False

    # ========== 工具方法 ==========

    def 获取全部术语(self) -> Dict[str, str]:
        """获取全部术语映射"""
        return self.术语映射.copy()

    def 获取术语数(self) -> int:
        """获取术语总数"""
        return len(self.术语映射)

    def 获取审计结果(self) -> Dict[str, Any]:
        """获取审计结果"""
        错误数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "错误")
        警告数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "警告")
        成功数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "成功")

        return {
            "DNA追溯": self.DNA追溯,
            "错误数": 错误数,
            "警告数": 警告数,
            "成功数": 成功数,
            "术语总数": self.获取术语数(),
            "翻译历史数": len(self.翻译历史),
            "日志": self.审计日志,
            "状态": "🔴 失败" if 错误数 > 0 else ("🟡 警告" if 警告数 > 0 else "🟢 通过")
        }

    def 导出术语表(self, 格式: str = "json") -> str:
        """导出术语表"""
        if 格式 == "json":
            return json.dumps(self.术语映射, ensure_ascii=False, indent=2)
        elif 格式 == "markdown":
            行 = ["| 英文术语 | 中文术语 | 分类 |", "|---------|---------|------|"]
            for en, cn in sorted(self.术语映射.items()):
                cat = "未分类"
                for c, terms in 术语分类.items():
                    if en in terms:
                        cat = c
                        break
                行.append(f"| {en} | {cn} | {cat} |")
            return "\n".join(行)
        return ""


# ========== 便捷函数 ==========

def 快速翻译(文本: str, 方向: str = "auto") -> str:
    """快速翻译入口"""
    翻译器 = 通心译翻译器()
    if 方向 == "en2cn":
        return 翻译器.英文到中文(文本)
    elif 方向 == "cn2en":
        return 翻译器.中文到英文(文本)
    return 翻译器.智能翻译(文本)


# 自检
if __name__ == "__main__":
    翻译器 = 通心译翻译器(启用藏经阁=False)

    # 测试翻译
    测试文本 = "The Transformer model uses Attention mechanism for Inference with a specific Learning Rate."
    print(f"原文: {测试文本}")
    print(f"译文: {翻译器.英文到中文(测试文本)}")
    print()

    # 测试反向翻译
    中文文本 = "变换器模型使用注意力机制进行推理，并设置特定的学习率。"
    print(f"中文: {中文文本}")
    print(f"英文: {翻译器.中文到英文(中文文本)}")
    print()

    # 术语查询
    print("术语解释:")
    print(json.dumps(翻译器.解释术语("Attention"), ensure_ascii=False, indent=2))
