# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# core/rag/rag_service.py
# 龍魂 · RAG检索服务 · 检索增强生成

from typing import List, Dict, Optional
from dataclasses import dataclass
import json
import hashlib
from datetime import datetime

from document_parser import DocumentParser, DocumentChunk
from embedding_engine import EmbeddingEngine, SearchResult

# === DNA常量 ===
MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"
MASTER_UID = "9622"

@dataclass
class RAGResponse:
    """RAG响应"""
    answer: str
    sources: List[SearchResult]
    confidence: float              # 置信度
    processing_time: float         # 处理时间
    model_used: str
    dna_signature: str
    
    def __post_init__(self):
        if not self.dna_signature:
            self.dna_signature = self._sign_data()
    
    def _sign_data(self) -> str:
        payload = f"{self.answer[:50]}-{self.confidence}-{datetime.now().timestamp()}"
        return f"SM3-{hashlib.sha256(payload.encode()).hexdigest()[:16]}"


class RAGService:
    """RAG检索服务"""
    
    def __init__(self, 
                 embedding_model: str = "BAAI/bge-large-zh",
                 llm_model: str = "deepseek-chat",
                 top_k: int = 5,
                 rerank: bool = True):
        self.embedding_engine = EmbeddingEngine(embedding_model)
        self.llm_model = llm_model
        self.top_k = top_k
        self.rerank = rerank
        self.parser = DocumentParser()
        
        # 重排序器
        self.reranker = None
        if rerank:
            self._init_reranker()
    
    def _init_reranker(self):
        """初始化重排序器"""
        try:
            from sentence_transformers import CrossEncoder
            self.reranker = CrossEncoder('BAAI/bge-reranker-large')
            print("[龍魂] 重排序器加载完成")
        except ImportError:
            print("[龍魂] 警告: 重排序器未加载")
    
    def ingest_documents(self, file_paths: List[str]):
        """批量导入文档"""
        all_chunks = []
        for path in file_paths:
            try:
                chunks = self.parser.parse_file(path)
                all_chunks.extend(chunks)
                print(f"[龍魂] 导入: {path} -> {len(chunks)} 块")
            except Exception as e:
                print(f"[龍魂] 导入失败: {path} - {e}")
        
        self.embedding_engine.build_index(all_chunks)
        print(f"[龍魂] 共导入 {len(all_chunks)} 个分块")
    
    def query(self, question: str, context_filter: Optional[Dict] = None) -> RAGResponse:
        """RAG查询"""
        import time
        start_time = time.time()
        
        # 1. 检索相关文档
        results = self.embedding_engine.search(question, top_k=self.top_k * 2)
        
        # 2. 重排序（如果启用）
        if self.reranker and len(results) > 0:
            results = self._rerank(question, results)
            results = results[:self.top_k]
        
        # 3. 构建上下文
        context = self._build_context(results)
        
        # 4. 生成答案（调用LLM）
        answer = self._generate_answer(question, context)
        
        # 5. 计算置信度
        confidence = self._calculate_confidence(results, answer)
        
        processing_time = time.time() - start_time
        
        return RAGResponse(
            answer=answer,
            sources=results,
            confidence=confidence,
            processing_time=processing_time,
            model_used=self.llm_model
        )
    
    def _rerank(self, query: str, results: List[SearchResult]) -> List[SearchResult]:
        """重排序"""
        if not self.reranker:
            return results
        
        pairs = [[query, r.content] for r in results]
        scores = self.reranker.predict(pairs)
        
        # 按重排序分数排序
        scored_results = list(zip(results, scores))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        return [r for r, _ in scored_results]
    
    def _build_context(self, results: List[SearchResult]) -> str:
        """构建上下文"""
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[文档{i}] 来源: {result.source} 第{result.page}页\n"
                f"{result.content}\n"
            )
        return "\n".join(context_parts)
    
    def _generate_answer(self, question: str, context: str) -> str:
        """生成答案（调用LLM - 实际接入DeepSeek等）"""
        prompt = self._build_prompt(question, context)
        
        # 模拟响应（实际: response = self.llm_client.chat.completions.create(...)）
        answer = self._mock_generate(prompt)
        return answer
    
    def _build_prompt(self, question: str, context: str) -> str:
        """构建提示词"""
        return f"""你是一个专业的教育AI助手。请基于以下参考资料回答问题。

参考资料：
{context}

用户问题：{question}

请用中文回答，要求：
1. 基于提供的参考资料回答
2. 如果资料不足，明确说明
3. 回答简洁准确，适合学生理解
4. 必要时给出示例

回答："""
    
    def _mock_generate(self, prompt: str) -> str:
        """模拟生成（实际接入LLM API）"""
        return "[模拟回答] 基于检索到的资料，二次函数的一般形式是 y = ax² + bx + c (a≠0)，其中a、b、c为常数..."
    
    def _calculate_confidence(self, results: List[SearchResult], answer: str) -> float:
        """计算置信度"""
        if not results:
            return 0.0
        
        avg_score = sum(r.score for r in results) / len(results)
        confidence = min(avg_score * 0.8 + 0.2, 1.0)
        return round(confidence, 3)


# === 使用示例 ===
if __name__ == "__main__":
    rag = RAGService()
    
    # 导入教材
    rag.ingest_documents([
        "data/数学教材.pdf",
        "data/物理笔记.md",
        "data/英语词汇.txt"
    ])
    
    # 查询
    response = rag.query("什么是牛顿第二定律？")
    print(f"\n回答: {response.answer}")
    print(f"置信度: {response.confidence}")
    print(f"处理时间: {response.processing_time:.2f}s")
    print(f"引用来源: {len(response.sources)} 个")
    print(f"签名: {response.dna_signature}")
