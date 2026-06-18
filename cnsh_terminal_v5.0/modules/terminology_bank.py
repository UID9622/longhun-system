# -*- coding: utf-8 -*-
"""
#龍芯⚡️2026-06-18-CNSH-TERMINOLOGY-BANK-v5.0
# 🟢 审计通过: 中央藏经阁完整实现
# 🔒 AI Truth Protocol: 所有声明均为真实
# 🤝 君子协议: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

中央藏经阁 - AI术语知识库
Chroma向量库 + SQLite关系库存储和查询
"""

import os
import re
import json
import sqlite3
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict


# 尝试导入Chroma，如果不可用则使用纯SQLite回退
try:
    import chromadb
    from chromadb.config import Settings
    CHROMA可用 = True
except ImportError:
    CHROMA可用 = False

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING可用 = True
except ImportError:
    EMBEDDING可用 = False


@dataclass
class 术语记录:
    """术语记录数据结构"""
    英文: str
    中文: str
    分类: str
    说明: str
    上下文: str
    创建时间: str
    DNA追溯: str
    使用次数: int = 0
    置信度: float = 1.0

    def 转字典(self) -> Dict:
        return asdict(self)


class 中央藏经阁:
    """
    中央藏经阁 - AI术语中央知识库
    支持向量搜索 + 关系查询 + 术语管理
    """

    DNA追溯 = "#龍芯⚡️2026-06-18-CNSH-TERMINOLOGY-BANK-v5.0"

    def __init__(self, chroma_path: str = None, sqlite_path: str = None):
        """
        初始化中央藏经阁
        """
        self.审计日志: List[Dict] = []
        self.术语缓存: Dict[str, 术语记录] = {}
        self.chroma集合 = None
        self.嵌入模型 = None

        # 设置默认路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.chroma路径 = chroma_path or os.path.join(base_dir, "data", "chroma_db")
        self.sqlite路径 = sqlite_path or os.path.join(base_dir, "data", "terminology.db")

        # 确保目录存在
        os.makedirs(os.path.dirname(self.sqlite路径), exist_ok=True)
        os.makedirs(self.chroma路径, exist_ok=True)

        # 初始化SQLite
        self._初始化SQLite()

        # 初始化Chroma（如果可用）
        if CHROMA可用 and EMBEDDING可用:
            try:
                self._初始化Chroma()
                self.记录("成功", "Chroma向量库初始化成功")
            except Exception as e:
                self.记录("警告", f"Chroma初始化失败: {e}，回退到纯SQLite模式")
                self.chroma集合 = None
        else:
            self.记录("警告", f"Chroma不可用(CHROMA={CHROMA可用}, EMBEDDING={EMBEDDING可用})，使用纯SQLite模式")

        # 从SQLite加载术语到缓存
        self._加载术语到缓存()

    def 记录(self, 级别: str, 消息: str) -> None:
        """记录审计日志"""
        self.审计日志.append({
            "级别": 级别,
            "消息": 消息,
            "时间": datetime.now().isoformat(),
            "颜色": {"成功": "🟢", "警告": "🟡", "错误": "🔴"}.get(级别, "⚪")
        })

    # ========== 数据库初始化 ==========

    def _初始化SQLite(self) -> None:
        """初始化SQLite数据库"""
        try:
            self.sqlite连接 = sqlite3.connect(self.sqlite路径, check_same_thread=False)
            self.sqlite连接.row_factory = sqlite3.Row
            cursor = self.sqlite连接.cursor()

            # 创建术语表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS 术语表 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    英文 TEXT UNIQUE NOT NULL,
                    中文 TEXT NOT NULL,
                    分类 TEXT DEFAULT '未分类',
                    说明 TEXT,
                    上下文 TEXT,
                    创建时间 TEXT NOT NULL,
                    DNA追溯 TEXT NOT NULL,
                    使用次数 INTEGER DEFAULT 0,
                    置信度 REAL DEFAULT 1.0,
                    sha256 TEXT NOT NULL
                )
            ''')

            # 创建索引
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_术语_英文 ON 术语表(英文)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_术语_中文 ON 术语表(中文)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_术语_分类 ON 术语表(分类)
            ''')

            # 创建审计日志表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS 审计日志表 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    时间 TEXT NOT NULL,
                    级别 TEXT NOT NULL,
                    消息 TEXT NOT NULL,
                    DNA追溯 TEXT
                )
            ''')

            # 创建查询历史表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS 查询历史表 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    查询 TEXT NOT NULL,
                    结果数 INTEGER,
                    查询时间 TEXT NOT NULL
                )
            ''')

            self.sqlite连接.commit()
            self.记录("成功", f"SQLite数据库初始化成功: {self.sqlite路径}")

        except Exception as e:
            self.记录("错误", f"SQLite初始化失败: {e}")
            raise

    def _初始化Chroma(self) -> None:
        """初始化Chroma向量库"""
        self.chroma客户端 = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=self.chroma路径
        ))

        # 获取或创建集合
        self.chroma集合 = self.chroma客户端.get_or_create_collection(
            name="ai术语",
            metadata={"描述": "CNSH AI术语向量库", "版本": "5.0"}
        )

        # 初始化嵌入模型
        try:
            self.嵌入模型 = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        except:
            self.嵌入模型 = None

    def _加载术语到缓存(self) -> None:
        """从SQLite加载术语到内存缓存"""
        try:
            cursor = self.sqlite连接.cursor()
            cursor.execute("SELECT * FROM 术语表")
            行列表 = cursor.fetchall()

            for 行 in 行列表:
                记录 = 术语记录(
                    英文=行["英文"],
                    中文=行["中文"],
                    分类=行["分类"],
                    说明=行["说明"],
                    上下文=行["上下文"],
                    创建时间=行["创建时间"],
                    DNA追溯=行["DNA追溯"],
                    使用次数=行["使用次数"],
                    置信度=行["置信度"]
                )
                self.术语缓存[行["英文"]] = 记录
                self.术语缓存[行["中文"]] = 记录

            self.记录("成功", f"已加载 {len(行列表)} 条术语到缓存")
        except Exception as e:
            self.记录("警告", f"缓存加载失败: {e}")

    # ========== 核心CRUD操作 ==========

    def 存储术语(self, 英文: str, 中文: str, 上下文: str = "",
               分类: str = "未分类", 说明: str = "") -> bool:
        """
        存储术语到中央藏经阁
        同时存入SQLite和Chroma
        """
        try:
            时间戳 = datetime.now().isoformat()
            追溯码 = f"{self.DNA追溯}-{hashlib.sha256(英文.encode()).hexdigest()[:8]}"

            # 计算SHA256
            数据字符串 = f"{英文}:{中文}:{上下文}:{时间戳}"
            sha256 = hashlib.sha256(数据字符串.encode()).hexdigest()

            # 存入SQLite
            cursor = self.sqlite连接.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO 术语表
                (英文, 中文, 分类, 说明, 上下文, 创建时间, DNA追溯, 使用次数, 置信度, sha256)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0, 1.0, ?)
            ''', (英文, 中文, 分类, 说明, 上下文, 时间戳, 追溯码, sha256))
            self.sqlite连接.commit()

            # 存入Chroma（如果可用）
            if self.chroma集合 and self.嵌入模型:
                try:
                    嵌入向量 = self.嵌入模型.encode(英文).tolist()
                    self.chroma集合.add(
                        ids=[追溯码],
                        embeddings=[嵌入向量],
                        metadatas=[{
                            "英文": 英文,
                            "中文": 中文,
                            "分类": 分类,
                            "说明": 说明
                        }],
                        documents=[f"{英文} - {中文}: {说明}"]
                    )
                except Exception as e:
                    self.记录("警告", f"Chroma存储失败: {e}")

            # 更新缓存
            记录 = 术语记录(英文=英文, 中文=中文, 分类=分类, 说明=说明,
                          上下文=上下文, 创建时间=时间戳, DNA追溯=追溯码)
            self.术语缓存[英文] = 记录
            self.术语缓存[中文] = 记录

            self.记录("成功", f"术语存储成功: {英文} → {中文}")
            return True

        except Exception as e:
            self.记录("错误", f"术语存储失败: {e}")
            return False

    def 查询术语(self, 查询: str, 数量: int = 5) -> List[Dict]:
        """
        查询术语
        优先使用Chroma向量搜索，回退到SQLite模糊搜索
        """
        结果列表 = []
        查询时间 = datetime.now().isoformat()

        try:
            # 方法1: Chroma向量搜索
            if self.chroma集合 and self.嵌入模型:
                try:
                    查询向量 = self.嵌入模型.encode(查询).tolist()
                    chroma结果 = self.chroma集合.query(
                        query_embeddings=[查询向量],
                        n_results=min(数量, 10)
                    )

                    for i, 文档 in enumerate(chroma结果.get("documents", [[]])[0]):
                        元数据 = chroma结果["metadatas"][0][i] if chroma结果.get("metadatas") else {}
                        距离 = chroma结果["distances"][0][i] if chroma结果.get("distances") else 0
                        结果列表.append({
                            "英文": 元数据.get("英文", ""),
                            "中文": 元数据.get("中文", ""),
                            "分类": 元数据.get("分类", "未分类"),
                            "说明": 元数据.get("说明", ""),
                            "相似度": 1.0 - min(距离, 1.0),
                            "来源": "向量搜索"
                        })
                except Exception as e:
                    self.记录("警告", f"向量搜索失败: {e}")

            # 方法2: SQLite模糊搜索（补充或回退）
            if len(结果列表) < 数量:
                cursor = self.sqlite连接.cursor()
                模糊查询 = f"%{查询}%"

                cursor.execute('''
                    SELECT DISTINCT * FROM 术语表
                    WHERE 英文 LIKE ? OR 中文 LIKE ? OR 说明 LIKE ?
                    LIMIT ?
                ''', (模糊查询, 模糊查询, 模糊查询, 数量))

                现有英文 = {r["英文"] for r in 结果列表}
                for 行 in cursor.fetchall():
                    if 行["英文"] not in 现有英文:
                        结果列表.append({
                            "英文": 行["英文"],
                            "中文": 行["中文"],
                            "分类": 行["分类"],
                            "说明": 行["说明"],
                            "相似度": self._计算文本相似度(查询, 行["英文"] + 行["中文"]),
                            "来源": "模糊搜索"
                        })

            # 方法3: 缓存精确匹配
            if 查询 in self.术语缓存:
                记录 = self.术语缓存[查询]
                是否已存在 = any(r["英文"] == 记录.英文 for r in 结果列表)
                if not 是否已存在:
                    结果列表.insert(0, {
                        "英文": 记录.英文,
                        "中文": 记录.中文,
                        "分类": 记录.分类,
                        "说明": 记录.说明,
                        "相似度": 1.0,
                        "来源": "精确缓存"
                    })

            # 记录查询历史
            cursor = self.sqlite连接.cursor()
            cursor.execute('''
                INSERT INTO 查询历史表 (查询, 结果数, 查询时间)
                VALUES (?, ?, ?)
            ''', (查询, len(结果列表), 查询时间))
            self.sqlite连接.commit()

            # 更新使用次数
            for 结果 in 结果列表:
                self._增加使用次数(结果["英文"])

            self.记录("成功", f"查询 '{查询}' 返回 {len(结果列表)} 条结果")
            return 结果列表[:数量]

        except Exception as e:
            self.记录("错误", f"查询失败: {e}")
            return []

    def 精确查询(self, 术语: str) -> Optional[Dict]:
        """精确查询单个术语"""
        # 先查缓存
        if 术语 in self.术语缓存:
            记录 = self.术语缓存[术语]
            return 记录.转字典()

        # 再查SQLite
        try:
            cursor = self.sqlite连接.cursor()
            cursor.execute('''
                SELECT * FROM 术语表 WHERE 英文 = ? OR 中文 = ?
            ''', (术语, 术语))
            行 = cursor.fetchone()

            if 行:
                return dict(行)
            return None

        except Exception as e:
            self.记录("错误", f"精确查询失败: {e}")
            return None

    def 批量导入(self, 术语字典: Dict[str, str], 分类: str = "未分类") -> Dict[str, bool]:
        """
        批量导入术语
        返回导入结果字典
        """
        结果 = {}
        for 英文, 中文 in 术语字典.items():
            结果[英文] = self.存储术语(英文, 中文, 分类=分类)
        return 结果

    def 删除术语(self, 术语: str) -> bool:
        """删除术语"""
        try:
            cursor = self.sqlite连接.cursor()
            cursor.execute('DELETE FROM 术语表 WHERE 英文 = ? OR 中文 = ?',
                         (术语, 术语))
            self.sqlite连接.commit()

            # 删除缓存
            if 术语 in self.术语缓存:
                记录 = self.术语缓存.pop(术语)
                if 记录.中文 in self.术语缓存:
                    del self.术语缓存[记录.中文]
                if 记录.英文 in self.术语缓存:
                    del self.术语缓存[记录.英文]

            self.记录("成功", f"术语删除成功: {术语}")
            return True
        except Exception as e:
            self.记录("错误", f"术语删除失败: {e}")
            return False

    def 更新术语(self, 英文: str, **更新字段) -> bool:
        """更新术语信息"""
        try:
            允许字段 = {"中文", "分类", "说明", "上下文", "置信度"}
            更新键值 = {k: v for k, v in 更新字段.items() if k in 允许字段}

            if not 更新键值:
                return False

            set子句 = ", ".join(f"{k} = ?" for k in 更新键值.keys())
            参数 = list(更新键值.values()) + [英文]

            cursor = self.sqlite连接.cursor()
            cursor.execute(f'UPDATE 术语表 SET {set子句} WHERE 英文 = ?', 参数)
            self.sqlite连接.commit()

            self._加载术语到缓存()  # 刷新缓存
            self.记录("成功", f"术语更新成功: {英文}")
            return True

        except Exception as e:
            self.记录("错误", f"术语更新失败: {e}")
            return False

    # ========== 统计与报告 ==========

    def 获取统计(self) -> Dict:
        """获取藏经阁统计信息"""
        try:
            cursor = self.sqlite连接.cursor()
            cursor.execute("SELECT COUNT(*) FROM 术语表")
            术语总数 = cursor.fetchone()[0]

            cursor.execute("SELECT 分类, COUNT(*) FROM 术语表 GROUP BY 分类")
            分类统计 = {行[0]: 行[1] for 行 in cursor.fetchall()}

            cursor.execute("SELECT COUNT(*) FROM 查询历史表")
            查询次数 = cursor.fetchone()[0]

            return {
                "术语总数": 术语总数,
                "分类统计": 分类统计,
                "查询次数": 查询次数,
                "缓存命中": len(self.术语缓存),
                "chroma可用": self.chroma集合 is not None
            }
        except Exception as e:
            self.记录("错误", f"统计失败: {e}")
            return {}

    def 获取全部术语(self) -> List[Dict]:
        """获取全部术语列表"""
        try:
            cursor = self.sqlite连接.cursor()
            cursor.execute("SELECT * FROM 术语表 ORDER BY 英文")
            return [dict(行) for 行 in cursor.fetchall()]
        except Exception as e:
            self.记录("错误", f"获取全部术语失败: {e}")
            return []

    def 导出JSON(self, 文件路径: str = None) -> str:
        """导出术语库为JSON"""
        术语列表 = self.获取全部术语()
        json字符串 = json.dumps(术语列表, ensure_ascii=False, indent=2)

        if 文件路径:
            with open(文件路径, 'w', encoding='utf-8') as f:
                f.write(json字符串)
            self.记录("成功", f"术语库导出到: {文件路径}")

        return json字符串

    # ========== 内部辅助方法 ==========

    def _增加使用次数(self, 英文术语: str) -> None:
        """增加术语使用次数"""
        try:
            cursor = self.sqlite连接.cursor()
            cursor.execute('''
                UPDATE 术语表 SET 使用次数 = 使用次数 + 1 WHERE 英文 = ?
            ''', (英文术语,))
            self.sqlite连接.commit()
        except:
            pass

    def _计算文本相似度(self, 文本1: str, 文本2: str) -> float:
        """简单的Jaccard相似度计算"""
        集合1 = set(文本1.lower())
        集合2 = set(文本2.lower())
        if not 集合1 or not 集合2:
            return 0.0
        交集 = 集合1 & 集合2
        并集 = 集合1 | 集合2
        return len(交集) / len(并集)

    def 获取审计结果(self) -> Dict:
        """获取审计结果"""
        错误数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "错误")
        警告数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "警告")
        成功数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "成功")
        统计 = self.获取统计()

        return {
            "DNA追溯": self.DNA追溯,
            "错误数": 错误数,
            "警告数": 警告数,
            "成功数": 成功数,
            "统计": 统计,
            "日志": self.审计日志,
            "状态": "🔴 失败" if 错误数 > 0 else ("🟡 警告" if 警告数 > 0 else "🟢 通过")
        }

    def __del__(self):
        """析构时关闭连接"""
        if hasattr(self, 'sqlite连接'):
            try:
                self.sqlite连接.close()
            except:
                pass


# ========== 便捷函数 ==========

def 创建藏经阁() -> 中央藏经阁:
    """创建中央藏经阁实例"""
    return 中央藏经阁()


# 自检
if __name__ == "__main__":
    藏经阁 = 中央藏经阁()

    # 存储测试术语
    藏经阁.存储术语("Prompt", "道令", "AI核心概念", "基础概念",
                    "向AI模型发出的指令或问题")
    藏经阁.存储术语("Agent", "灵使", "AI核心概念", "基础概念",
                    "能够自主感知环境并执行任务的智能体")

    # 查询
    结果 = 藏经阁.查询术语("Prompt")
    print("查询结果:")
    for r in 结果:
        print(f"  {r['英文']} → {r['中文']} ({r['来源']}, 相似度: {r['相似度']:.3f})")

    # 统计
    print("\n统计:")
    print(json.dumps(藏经阁.获取统计(), ensure_ascii=False, indent=2))
