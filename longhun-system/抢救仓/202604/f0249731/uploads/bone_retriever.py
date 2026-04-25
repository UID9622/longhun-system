#!/usr/bin/env python3
"""
龍魂骨检索引擎 · FAISS Vector Bone Retriever v1.0
==================================================
UID9622 原创 · 数字大军知识武装系统

用向量相似度检索 Knowledge DNA 库中最相关的"骨"（核心知识单元）。
支持：中文文本向量化、FAISS索引构建、增量添加、持久化存储。

核心思路（数字大军比喻）：
  骨 = Knowledge DNA 中的核心知识单元
  骨检索 = 根据问题/意图，快速调兵（找到最相关的知识DNA）
  向量 = 把知识翻译成数字编队，方便快速匹配

用法：
  # 构建索引
  python bone_retriever.py build --data bones.json --output bone_index/

  # 检索
  python bone_retriever.py search --index bone_index/ --query "梯度下降怎么理解"

  # 添加新骨
  python bone_retriever.py add --index bone_index/ --data new_bones.json

  # 从 Notion Knowledge DNA 同步（需配合外部脚本导出）
  python bone_retriever.py build --data knowledge_dna_export.json --output bone_index/
"""

import json
import hashlib
import pickle
import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from collections import Counter

import numpy as np
import faiss


# ============================================================
# 一、中文文本向量化器（无需外部大模型）
# ============================================================

class ChineseTextVectorizer:
    """
    基于 TF-IDF 字符级 n-gram 的中文文本向量化器。

    为什么不用 BERT/Sentence-Transformers？
    → UID9622 的系统要求离线运行、轻量、不依赖大模型。
    → 字符级 n-gram 对中文足够好，能捕捉词汇和短语模式。
    → 以后升级到 embedding 模型时，只需替换这个类。

    向量维度默认 256，用 SVD 降维保持检索速度。
    """

    def __init__(self, dim=256, ngram_range=(1, 4), max_features=8000):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.decomposition import TruncatedSVD

        self.dim = dim
        self.tfidf = TfidfVectorizer(
            analyzer='char_wb',
            ngram_range=ngram_range,
            max_features=max_features,
            sublinear_tf=True
        )
        self.svd = TruncatedSVD(n_components=dim, random_state=9622)
        self.is_fitted = False

    def fit(self, texts):
        """从文本语料库训练向量化器"""
        tfidf_matrix = self.tfidf.fit_transform(texts)
        actual_dim = min(self.dim, tfidf_matrix.shape[1] - 1)
        if actual_dim < self.dim:
            from sklearn.decomposition import TruncatedSVD
            self.svd = TruncatedSVD(n_components=actual_dim, random_state=9622)
            self.dim = actual_dim
        self.svd.fit(tfidf_matrix)
        self.is_fitted = True
        return self

    def transform(self, texts):
        """将文本转换为向量"""
        if not self.is_fitted:
            raise RuntimeError("向量化器未训练！请先 fit()")
        tfidf_matrix = self.tfidf.transform(texts)
        vectors = self.svd.transform(tfidf_matrix)
        # L2 归一化（FAISS 余弦相似度需要）
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        vectors = vectors / norms
        return vectors.astype('float32')

    def fit_transform(self, texts):
        """训练 + 转换"""
        self.fit(texts)
        return self.transform(texts)


# ============================================================
# 二、骨数据结构
# ============================================================

def create_bone(bone_id, concept, tech_points, direction="未知",
                purity="中-需验证", source="", extra=None):
    """
    创建一条骨记录（对应 Knowledge DNA 的一条）

    bone_id: 唯一标识（对应 DNA-ID）
    concept: 核心概念（用于向量化的主文本）
    tech_points: 技术点描述
    direction: 方向（AI/Web/元宇宙/系统/哲学/CNSH）
    purity: 纯度
    source: 来源
    extra: 额外元数据 dict
    """
    # 合并文本用于向量化
    full_text = f"{concept} {tech_points}"

    bone = {
        "bone_id": bone_id,
        "concept": concept,
        "tech_points": tech_points,
        "direction": direction,
        "purity": purity,
        "source": source,
        "full_text": full_text,
        "created_at": datetime.now().isoformat(),
    }
    if extra:
        bone.update(extra)

    return bone


# ============================================================
# 三、FAISS 骨检索引擎
# ============================================================

class BoneRetriever:
    """
    龍魂骨检索引擎

    用 FAISS 做向量近邻检索，实现：
    - 毫秒级从数千条 DNA 中找到最相关的几条
    - 支持增量添加新骨
    - 持久化存储索引
    """

    def __init__(self, dim=256):
        self.dim = dim
        self.vectorizer = ChineseTextVectorizer(dim=dim)
        self.index = None  # FAISS index
        self.bones = []     # 骨记录列表（metadata）
        self.bone_id_map = {}  # bone_id → index position

    def build(self, bones, verbose=True):
        """
        从骨记录列表构建索引
        bones: [{"bone_id": "DNA-1", "concept": "...", "tech_points": "...", ...}, ...]
        """
        if not bones:
            raise ValueError("骨记录列表为空！")

        self.bones = bones
        self.bone_id_map = {b["bone_id"]: i for i, b in enumerate(bones)}

        # 提取文本
        texts = [b.get("full_text", b["concept"]) for b in bones]

        # 向量化
        vectors = self.vectorizer.fit_transform(texts)
        actual_dim = vectors.shape[1]
        self.dim = actual_dim

        # 构建 FAISS 索引（余弦相似度 = 内积 on L2-normalized vectors）
        self.index = faiss.IndexFlatIP(actual_dim)
        self.index.add(vectors)

        if verbose:
            print(f"  骨记录数: {len(bones)}")
            print(f"  向量维度: {actual_dim}")
            print(f"  索引类型: FlatIP (精确余弦相似度)")
            # 统计方向分布
            directions = Counter(b.get("direction", "未知") for b in bones)
            print(f"  方向分布: {dict(directions)}")

    def search(self, query, top_k=5):
        """
        搜索最相关的骨
        返回: [{"bone": bone_record, "score": float}, ...]
        """
        if self.index is None:
            raise RuntimeError("索引未构建！请先 build() 或 load()")

        query_vec = self.vectorizer.transform([query])
        scores, indices = self.index.search(query_vec, min(top_k, len(self.bones)))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            results.append({
                "bone": self.bones[idx],
                "score": float(score)
            })

        return results

    def add_bones(self, new_bones, verbose=True):
        """增量添加新骨到索引"""
        if self.index is None:
            raise RuntimeError("索引未构建！请先 build()")

        start_idx = len(self.bones)
        self.bones.extend(new_bones)
        for i, b in enumerate(new_bones):
            self.bone_id_map[b["bone_id"]] = start_idx + i

        texts = [b.get("full_text", b["concept"]) for b in new_bones]
        vectors = self.vectorizer.transform(texts)
        self.index.add(vectors)

        if verbose:
            print(f"  新增 {len(new_bones)} 条骨")
            print(f"  索引总量: {self.index.ntotal}")

    def get_bone(self, bone_id):
        """根据 bone_id 获取骨记录"""
        idx = self.bone_id_map.get(bone_id)
        if idx is not None:
            return self.bones[idx]
        return None

    def save(self, directory):
        """持久化保存索引和数据"""
        os.makedirs(directory, exist_ok=True)

        # 保存 FAISS 索引
        faiss.write_index(self.index, os.path.join(directory, "bone.index"))

        # 保存骨记录和向量化器
        meta = {
            "bones": self.bones,
            "bone_id_map": self.bone_id_map,
            "vectorizer": self.vectorizer,
            "dim": self.dim,
            "saved_at": datetime.now().isoformat(),
            "total_bones": len(self.bones)
        }
        with open(os.path.join(directory, "bone_meta.pkl"), 'wb') as f:
            pickle.dump(meta, f)

        # 生成 DNA 追溯码
        hash_input = json.dumps([b["bone_id"] for b in self.bones], ensure_ascii=False)
        file_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:8].upper()
        dna_code = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-INDEX-{file_hash}"

        print(f"  索引已保存: {directory}/")
        print(f"  骨总量: {len(self.bones)}")
        print(f"  DNA追溯码: {dna_code}")
        return dna_code

    def load(self, directory):
        """加载索引和数据"""
        # 加载 FAISS 索引
        index_path = os.path.join(directory, "bone.index")
        self.index = faiss.read_index(index_path)

        # 加载元数据
        meta_path = os.path.join(directory, "bone_meta.pkl")
        with open(meta_path, 'rb') as f:
            meta = pickle.load(f)

        self.bones = meta["bones"]
        self.bone_id_map = meta["bone_id_map"]
        self.vectorizer = meta["vectorizer"]
        self.dim = meta["dim"]

        print(f"  索引已加载: {directory}/")
        print(f"  骨总量: {len(self.bones)}")
        print(f"  向量维度: {self.dim}")


# ============================================================
# 四、示例骨数据（对应 Knowledge DNA 库）
# ============================================================

def get_sample_bones():
    """返回示例骨数据，模拟 Knowledge DNA 库中的记录"""
    return [
        create_bone("DNA-1", "MCP Server架构与工具定义",
                     "MCP用JSON-RPC 2.0通信 Server暴露tools/resources/prompts三种能力 工具定义用JSON Schema描述参数 支持stdio和SSE传输",
                     direction="AI", purity="高-核心知识"),
        create_bone("DNA-2", "反向传播与梯度下降的几何直觉",
                     "损失函数是高维曲面 梯度等于最陡方向 链式法则将整网络的梯度拆解为层层传递 学习率等于每步走多远 反向传播从结果往回找原因",
                     direction="AI", purity="高-核心知识"),
        create_bone("DNA-3", "阴阳三才与龍魂权重算法的哲学根基",
                     "天地人三才等于输入处理输出三层 阴阳对立统一等于权重正负反馈 变化之道等于动态调整 中庸等于系统平衡点",
                     direction="哲学", purity="高-核心知识"),
        create_bone("DNA-4", "Transformer自注意力机制",
                     "Q K V三矩阵 注意力分数等于QK转置除以根号dk 多头注意力并行捕捉不同模式 位置编码补充序列信息",
                     direction="AI", purity="高-核心知识"),
        create_bone("DNA-5", "TCP三次握手与四次挥手",
                     "SYN SYN-ACK ACK三步建立连接 FIN ACK FIN ACK四步释放 TIME_WAIT等待2MSL 半连接队列SYN Flood攻击",
                     direction="系统", purity="高-核心知识"),
        create_bone("DNA-6", "Docker容器化与镜像分层",
                     "镜像是只读模板 容器是镜像的运行实例 Dockerfile定义构建步骤 分层存储节省空间 docker-compose编排多容器",
                     direction="系统", purity="高-核心知识"),
        create_bone("DNA-7", "CNSH中文编程语法设计",
                     "用中文自然语言表达编程逻辑 结合龍魂DNA追溯系统 融入三才算法天地人三层 目标让不懂英文的人也能编程 语法糖自动翻译为可执行代码",
                     direction="CNSH", purity="中-需验证"),
        create_bone("DNA-8", "Adam优化器数学原理",
                     "一阶矩估计m和二阶矩估计v 偏差修正除以1减beta的t次方 自适应学习率 结合动量和RMSProp 工程首选优化器",
                     direction="AI", purity="高-核心知识"),
        create_bone("DNA-9", "B+树索引与数据库查询优化",
                     "B+树叶子节点链表有序 聚集索引和非聚集索引 覆盖索引避免回表 联合索引最左前缀原则 EXPLAIN分析执行计划",
                     direction="系统", purity="高-核心知识"),
        create_bone("DNA-10", "龍魂三色审计框架",
                     "绿色通过红色危险黄色待审 知识质量三维评估 内容纯度可复用性时效性 自动化审计管道 DNA净化标准",
                     direction="CNSH", purity="高-核心知识"),
        create_bone("DNA-11", "Diffusion扩散模型原理",
                     "前向过程逐步加噪 反向过程学习去噪 马尔可夫链 噪声预测网络UNet DDPM DDIM加速采样 Stable Diffusion架构",
                     direction="AI", purity="高-核心知识"),
        create_bone("DNA-12", "Swift并发模型Actor和async/await",
                     "Actor隔离可变状态 async await异步函数 Task结构化并发 Sendable协议线程安全 MainActor主线程",
                     direction="系统", purity="高-核心知识"),
        create_bone("DNA-13", "分布式系统CAP定理",
                     "一致性可用性分区容忍性三选二 CP系统如ZooKeeper AP系统如Cassandra 最终一致性折中方案 PACELC扩展定理",
                     direction="系统", purity="高-核心知识"),
        create_bone("DNA-14", "曾仕强易经管理哲学",
                     "以不变应万变 中庸之道不走极端 天时地利人和 上善若水 无为而治 变化中找规律 太极生两仪生四象生八卦",
                     direction="哲学", purity="高-核心知识"),
        create_bone("DNA-15", "龍魂DNA追溯码生成算法",
                     "SHA256哈希前8位 日期加类型加哈希 格式龍芯加日期加类型加哈希 每条知识唯一追溯 不可篡改 内容指纹",
                     direction="CNSH", purity="高-核心知识"),
    ]


# ============================================================
# 五、CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="龍魂骨检索引擎 · FAISS Vector Bone Retriever",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 用示例数据构建索引
  python bone_retriever.py build --output bone_index/

  # 用自定义数据构建
  python bone_retriever.py build --data my_bones.json --output bone_index/

  # 搜索
  python bone_retriever.py search --index bone_index/ --query "怎么理解注意力机制"

  # 添加新骨
  python bone_retriever.py add --index bone_index/ --data new_bones.json

  # 交互模式
  python bone_retriever.py interactive --index bone_index/
        """
    )
    sub = parser.add_subparsers(dest="command")

    # build
    p_build = sub.add_parser("build", help="构建骨索引")
    p_build.add_argument("--data", help="骨数据 JSON（省略则用示例数据）")
    p_build.add_argument("--output", default="bone_index", help="索引输出目录")

    # search
    p_search = sub.add_parser("search", help="搜索相关骨")
    p_search.add_argument("--index", default="bone_index", help="索引目录")
    p_search.add_argument("--query", required=True, help="搜索文本")
    p_search.add_argument("--top", type=int, default=5, help="返回前N个结果")

    # add
    p_add = sub.add_parser("add", help="添加新骨到索引")
    p_add.add_argument("--index", required=True, help="索引目录")
    p_add.add_argument("--data", required=True, help="新骨数据 JSON")

    # interactive
    p_inter = sub.add_parser("interactive", help="交互式检索")
    p_inter.add_argument("--index", default="bone_index", help="索引目录")

    args = parser.parse_args()

    if args.command == "build":
        print("🦴 龍魂骨检索引擎 · 构建索引...")
        retriever = BoneRetriever()
        if args.data:
            with open(args.data, 'r', encoding='utf-8') as f:
                raw = json.load(f)
                bones = raw if isinstance(raw, list) else raw.get("bones", [])
            print(f"  加载骨数据: {args.data} ({len(bones)} 条)")
        else:
            bones = get_sample_bones()
            print(f"  使用示例骨数据 ({len(bones)} 条)")
        retriever.build(bones)
        retriever.save(args.output)
        print("✅ 索引构建完成!")

    elif args.command == "search":
        retriever = BoneRetriever()
        retriever.load(args.index)
        results = retriever.search(args.query, top_k=args.top)
        print(f"\n🔍 搜索: \"{args.query}\"")
        print("─" * 60)
        for i, r in enumerate(results):
            bone = r["bone"]
            score = r["score"]
            bar = "█" * int(score * 30)
            direction_emoji = {"AI": "🤖", "系统": "⚙️", "哲学": "🌀",
                               "CNSH": "🐉", "Web": "🌐", "元宇宙": "🪐"}.get(bone["direction"], "📦")
            print(f"  {i+1}. {direction_emoji} [{bone['bone_id']}] {bone['concept']}")
            print(f"     {bone['tech_points'][:80]}...")
            print(f"     方向: {bone['direction']} | 纯度: {bone['purity']}")
            print(f"     相似度: {score:.3f} {bar}")
            print()

    elif args.command == "add":
        retriever = BoneRetriever()
        retriever.load(args.index)
        with open(args.data, 'r', encoding='utf-8') as f:
            raw = json.load(f)
            bones = raw if isinstance(raw, list) else raw.get("bones", [])
        print(f"🦴 添加新骨 ({len(bones)} 条)...")
        retriever.add_bones(bones)
        retriever.save(args.index)
        print("✅ 新骨添加完成!")

    elif args.command == "interactive":
        retriever = BoneRetriever()
        retriever.load(args.index)
        print("\n🦴 龍魂骨检索 · 交互模式")
        print("  输入问题/关键词检索相关知识DNA")
        print("  输入 'quit' 退出\n")
        while True:
            query = input("🔍 > ").strip()
            if query.lower() in ('quit', 'exit', 'q'):
                print("再见! 🐉")
                break
            if not query:
                continue
            results = retriever.search(query, top_k=3)
            for i, r in enumerate(results):
                bone = r["bone"]
                print(f"  {i+1}. [{bone['bone_id']}] {bone['concept']} (相似度: {r['score']:.3f})")
            print()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
