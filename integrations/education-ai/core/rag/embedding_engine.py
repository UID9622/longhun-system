#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# core/rag/embedding_engine.py
# 龍魂 · 向量嵌入引擎 · 语义检索

import numpy as np
from typing import List, Dict, Tuple, Optional
import hashlib
from dataclasses import dataclass
import json

# === DNA常量 ===
MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"
MASTER_UID = "9622"

@dataclass
class SearchResult:
    """检索结果"""
    chunk_id: str
    content: str
    score: float                    # 相似度分数
    source: str
    page: int
    metadata: Dict
    dna_signature: str


class EmbeddingEngine:
    """向量嵌入引擎"""
    
    def __init__(self, model_name: str = "BAAI/bge-large-zh", 
                 vector_dim: int = 1024,
                 device: str = "cpu"):
        self.model_name = model_name
        self.vector_dim = vector_dim
        self.device = device
        self.model = None
        self.vector_store = None
        
        # 初始化模型
        self._load_model()
    
    def _load_model(self):
        """加载嵌入模型"""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name, device=self.device)
            print(f"[龍魂] 嵌入模型加载完成: {self.model_name}")
        except ImportError:
            print("[龍魂] 警告: sentence-transformers未安装，使用模拟嵌入")
            self.model = None
    
    def embed(self, texts: List[str]) -> np.ndarray:
        """生成嵌入向量"""
        if self.model:
            embeddings = self.model.encode(texts, convert_to_numpy=True, 
                                          normalize_embeddings=True)
            return embeddings
        
        # 模拟嵌入（fallback）
        return self._mock_embed(texts)
    
    def _mock_embed(self, texts: List[str]) -> np.ndarray:
        """模拟嵌入（用于测试）"""
        np.random.seed(42)
        embeddings = []
        for text in texts:
            # 基于文本哈希生成确定性向量
            hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
            np.random.seed(hash_val % 2**32)
            vec = np.random.randn(self.vector_dim).astype(np.float32)
            vec = vec / np.linalg.norm(vec)  # 归一化
            embeddings.append(vec)
        return np.array(embeddings)
    
    def similarity(self, query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """计算余弦相似度"""
        return np.dot(doc_vecs, query_vec)
    
    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """语义检索"""
        if not self.vector_store:
            raise ValueError("向量库未初始化，请先调用build_index()")
        
        # 编码查询
        query_vec = self.embed([query])[0]
        
        # 检索
        results = self.vector_store.search(query_vec, top_k)
        
        return results
    
    def build_index(self, chunks: List):
        """构建索引"""
        if not chunks:
            return
        
        # 提取文本
        texts = [chunk.content for chunk in chunks]
        
        # 生成嵌入
        embeddings = self.embed(texts)
        
        # 存储到向量库
        for i, chunk in enumerate(chunks):
            chunk.embedding = embeddings[i].tolist()
        
        # 初始化向量存储
        self.vector_store = VectorStore(self.vector_dim)
        self.vector_store.add(chunks, embeddings)
        
        print(f"[龍魂] 索引构建完成: {len(chunks)} 个向量")
    
    def add_documents(self, chunks: List):
        """增量添加文档"""
        if not self.vector_store:
            self.build_index(chunks)
            return
        
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embed(texts)
        
        for i, chunk in enumerate(chunks):
            chunk.embedding = embeddings[i].tolist()
        
        self.vector_store.add(chunks, embeddings)


class VectorStore:
    """向量存储（基于Faiss简化版）"""
    
    def __init__(self, dim: int):
        self.dim = dim
        self.chunks = []
        self.vectors = None
        
        try:
            import faiss
            self.index = faiss.IndexFlatIP(dim)  # 内积 = 余弦相似度（已归一化）
            self.use_faiss = True
        except ImportError:
            print("[龍魂] 警告: Faiss未安装，使用暴力搜索")
            self.index = None
            self.use_faiss = False
    
    def add(self, chunks: List, embeddings: np.ndarray):
        """添加向量"""
        self.chunks.extend(chunks)
        
        if self.vectors is None:
            self.vectors = embeddings
        else:
            self.vectors = np.vstack([self.vectors, embeddings])
        
        if self.use_faiss:
            self.index.add(embeddings.astype(np.float32))
    
    def search(self, query_vec: np.ndarray, top_k: int) -> List[SearchResult]:
        """检索"""
        if self.use_faiss:
            query_vec = query_vec.reshape(1, -1).astype(np.float32)
            scores, indices = self.index.search(query_vec, top_k)
            
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < 0 or idx >= len(self.chunks):
                    continue
                chunk = self.chunks[idx]
                results.append(SearchResult(
                    chunk_id=chunk.id,
                    content=chunk.content,
                    score=float(score),
                    source=chunk.source,
                    page=chunk.page,
                    metadata=chunk.metadata,
                    dna_signature=chunk.dna_signature
                ))
            return results
        
        # 暴力搜索（fallback）
        similarities = np.dot(self.vectors, query_vec)
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            chunk = self.chunks[idx]
            results.append(SearchResult(
                chunk_id=chunk.id,
                content=chunk.content,
                score=float(similarities[idx]),
                source=chunk.source,
                page=chunk.page,
                metadata=chunk.metadata,
                dna_signature=chunk.dna_signature
            ))
        
        return results


# === 使用示例 ===
if __name__ == "__main__":
    engine = EmbeddingEngine()
    
    # 模拟数据
    from document_parser import DocumentParser, DocumentChunk
    parser = DocumentParser()
    
    # 构建索引
    chunks = parser.parse_file("data/教材.pdf")
    engine.build_index(chunks)
    
    # 检索
    results = engine.search("二次函数的定义是什么？", top_k=3)
    for r in results:
        print(f"\n[得分: {r.score:.4f}] {r.content[:100]}...")
