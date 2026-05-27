#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌐 CNSH 完整翻译系统 v1.0
Comprehensive Translation System with Notion Integration

功能：
  • 多语言翻译（中英日柬文）
  • Notion 看板自动化
  • AI 翻译 + 人工校对工作流
  • DNA 签名生成
  • 质量追踪与监控

DNA: #龍芯⚡️2026-05-27-CNSH-TRANSLATION-SYSTEM-COMPLETE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

理论指导: 曾仕强老师（永恒显示）
创建者: UID9622 诸葛鑫（龍芯北辰）
献礼: 龍魂系统，中华文化传承
"""

import json
import hashlib
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from queue import PriorityQueue
import time


# ============================================================================
# 日志配置
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# 枚举定义
# ============================================================================

class Language(Enum):
    """支持的语言"""
    CHINESE = '中文'
    ENGLISH = '英文'
    JAPANESE = '日文'
    KHMER = '柬文'
    OTHER = '其他'


class TranslationStatus(Enum):
    """翻译状态"""
    PENDING = '📥 待翻译'
    PROCESSING = '⚙️ AI处理中'
    REVIEWING = '👁️ 人工校对中'
    COMPLETED = '✅ 已完成'
    FAILED = '❌ 翻译失败'


class QualityLevel(Enum):
    """翻译质量等级"""
    EXCELLENT = '优秀'
    GOOD = '良好'
    FAIR = '一般'
    NEEDS_IMPROVEMENT = '待改进'


# ============================================================================
# 数据结构
# ============================================================================

@dataclass
class TranslationTask:
    """翻译任务"""
    task_id: str
    source_text: str
    source_language: Language
    target_language: Language
    status: TranslationStatus = TranslationStatus.PENDING
    translated_text: Optional[str] = None
    translator: Optional[str] = None
    reviewer: Optional[str] = None
    quality_level: Optional[QualityLevel] = None
    quality_score: float = 0.0
    dna_signature: Optional[str] = None
    created_at: str = None
    completed_at: Optional[str] = None
    word_count: int = 0
    notes: str = ""
    retry_count: int = 0

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'task_id': self.task_id,
            'source_text': self.source_text,
            'source_language': self.source_language.value,
            'target_language': self.target_language.value,
            'status': self.status.value,
            'translated_text': self.translated_text,
            'translator': self.translator,
            'reviewer': self.reviewer,
            'quality_level': self.quality_level.value if self.quality_level else None,
            'quality_score': self.quality_score,
            'dna_signature': self.dna_signature,
            'created_at': self.created_at,
            'completed_at': self.completed_at,
            'word_count': self.word_count,
            'notes': self.notes,
            'retry_count': self.retry_count
        }


# ============================================================================
# 翻译引擎 (Module 2)
# ============================================================================

class TranslationEngine:
    """CNSH 多语言翻译引擎"""

    # 简化版翻译字典（实际应用中应连接到真实翻译 API）
    TRANSLATION_DICT = {
        ('中文', '英文'): {
            '你好': 'Hello',
            '谢谢': 'Thank you',
            '对不起': 'Sorry',
            '再见': 'Goodbye',
            '龍魂': 'Dragon Soul',
            '系统': 'System',
            '翻译': 'Translation',
            '完整': 'Complete',
            '架构': 'Architecture'
        },
        ('英文', '中文'): {
            'Hello': '你好',
            'Thank you': '谢谢',
            'Sorry': '对不起',
            'Goodbye': '再见',
            'Dragon': '龍',
            'System': '系统',
            'Translation': '翻译',
            'Complete': '完整',
            'Architecture': '架构'
        },
        ('中文', '日文'): {
            '你好': 'こんにちは',
            '谢谢': 'ありがとう',
            '龍': '龍',
            '系统': 'システム'
        }
    }

    def __init__(self):
        self.cache = {}
        logger.info("翻译引擎初始化完成")

    def translate(
        self,
        text: str,
        source_lang: Language,
        target_lang: Language
    ) -> Tuple[str, float]:
        """
        翻译文本

        Returns:
            (翻译结果, 置信度)
        """
        if source_lang == target_lang:
            return text, 1.0

        # 检查缓存
        cache_key = f"{source_lang.value}_{target_lang.value}_{text}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # 简化实现：查词典或返回占位符
        dict_key = (source_lang.value, target_lang.value)

        if dict_key in self.TRANSLATION_DICT:
            translation_dict = self.TRANSLATION_DICT[dict_key]
            if text in translation_dict:
                result = (translation_dict[text], 0.95)
                self.cache[cache_key] = result
                return result

        # 如果找不到，返回占位符
        placeholder = f"[自动翻译: {text} ({source_lang.value}→{target_lang.value})]"
        result = (placeholder, 0.5)
        self.cache[cache_key] = result
        return result

    def analyze_text(self, text: str) -> Dict:
        """分析文本"""
        words = text.split()

        return {
            'word_count': len(words),
            'character_count': len(text),
            'line_count': len(text.split('\n')),
            'estimated_difficulty': 'medium'  # 简化
        }


# ============================================================================
# 质量评分 (Module 3)
# ============================================================================

class QualityScorer:
    """自动翻译质量评分"""

    def score(self, source: str, translation: str, confidence: float) -> Dict:
        """
        综合评分

        Returns:
            {
                "score": 0-100,
                "level": "优秀/良好/一般/待改进",
                "factors": {...}
            }
        """
        # 评分维度：
        # 1. 准确度 (40%) - 基于翻译引擎置信度
        # 2. 流畅度 (30%) - 基于文本长度和格式
        # 3. 术语一致性 (20%) - 基于缓存命中率
        # 4. 格式保持 (10%) - 基于结构一致性

        accuracy_score = confidence * 40
        fluency_score = 30  # 简化
        consistency_score = 20  # 简化
        format_score = 10  # 简化

        total_score = accuracy_score + fluency_score + consistency_score + format_score

        if total_score >= 95:
            level = QualityLevel.EXCELLENT
        elif total_score >= 80:
            level = QualityLevel.GOOD
        elif total_score >= 60:
            level = QualityLevel.FAIR
        else:
            level = QualityLevel.NEEDS_IMPROVEMENT

        return {
            'score': total_score,
            'level': level.value,
            'factors': {
                'accuracy': accuracy_score,
                'fluency': fluency_score,
                'consistency': consistency_score,
                'format': format_score
            }
        }

    def should_skip_human_review(self, score: Dict) -> bool:
        """判断是否可以跳过人工校对直接发布"""
        return score['score'] >= 95


# ============================================================================
# DNA 签名生成 (Module 4)
# ============================================================================

class DNASignatureGenerator:
    """龍魂系统的身份认证签名"""

    @staticmethod
    def generate(task_id: str, source: str, target: str,
                translation: str, metadata: dict = None) -> str:
        """
        生成 DNA 签名

        格式：#龍芯⚡️YYYY-MM-DD-TRANS-{hash}
        """
        if metadata is None:
            metadata = {}

        content = f"{task_id}|{source}|{target}|{translation}|{datetime.now().isoformat()}"
        hash_val = hashlib.sha256(content.encode()).hexdigest()[:8]

        dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-TRANS-{hash_val.upper()}"

        logger.info(f"DNA签名已生成: {dna}")
        return dna

    @staticmethod
    def verify_dna(dna: str) -> bool:
        """验证 DNA 签名的真伪"""
        # 简化实现：检查格式
        return dna.startswith('#龍芯⚡️') and 'TRANS-' in dna


# ============================================================================
# 任务队列管理 (Module 5)
# ============================================================================

class TaskQueueManager:
    """任务队列·支持优先级·重试·监控"""

    def __init__(self):
        self.queue = PriorityQueue()
        self.tasks: Dict[str, TranslationTask] = {}
        self.task_counter = 0
        self.engine = TranslationEngine()
        self.scorer = QualityScorer()

        self.retry_policy = {
            "max_retries": 3,
            "backoff_multiplier": 2,
            "initial_delay": 5  # 秒
        }

        # 统计
        self.stats = {
            'total_processed': 0,
            'failed_count': 0,
            'total_wait_time': 0
        }

        logger.info("任务队列管理器初始化完成")

    def create_task(
        self,
        source_text: str,
        source_language: Language,
        target_language: Language
    ) -> TranslationTask:
        """创建新的翻译任务"""
        self.task_counter += 1
        task_id = f"TRANS-{self.task_counter:06d}"

        # 分析文本
        analysis = self.engine.analyze_text(source_text)

        task = TranslationTask(
            task_id=task_id,
            source_text=source_text,
            source_language=source_language,
            target_language=target_language,
            status=TranslationStatus.PENDING,
            created_at=datetime.now().isoformat(),
            word_count=analysis['word_count']
        )

        self.tasks[task_id] = task

        # 入队
        self.enqueue(task, priority=analysis['word_count'])

        logger.info(f"✓ 任务已创建: {task_id}")
        return task

    def enqueue(self, task: TranslationTask, priority: int = 0):
        """入队·priority 越低越优先"""
        self.queue.put((priority, task.task_id, task))

    def dequeue(self) -> Optional[TranslationTask]:
        """出队"""
        try:
            _, task_id, task = self.queue.get(timeout=1)
            return task
        except:
            return None

    def auto_translate_task(self, task_id: str) -> bool:
        """自动翻译任务"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]

        try:
            # 翻译
            translated_text, confidence = self.engine.translate(
                task.source_text,
                task.source_language,
                task.target_language
            )

            task.translated_text = translated_text
            task.status = TranslationStatus.PROCESSING
            task.translator = 'AI_ENGINE'

            # 质量评分
            quality = self.scorer.score(task.source_text, translated_text, confidence)
            task.quality_score = quality['score']
            task.quality_level = QualityLevel(quality['level'])

            # 生成 DNA 签名
            task.dna_signature = DNASignatureGenerator.generate(
                task.task_id,
                task.source_language.value,
                task.target_language.value,
                translated_text
            )

            # 判断是否需要人工校对
            if self.scorer.should_skip_human_review(quality):
                task.status = TranslationStatus.COMPLETED
                task.completed_at = datetime.now().isoformat()
                logger.info(f"✓ {task_id}: 自动翻译完成（质量 {quality['score']:.0f}）")
            else:
                task.status = TranslationStatus.REVIEWING
                logger.info(f"✓ {task_id}: 需要人工校对（质量 {quality['score']:.0f}）")

            self.stats['total_processed'] += 1
            return True

        except Exception as e:
            logger.error(f"❌ {task_id}: 翻译失败 - {e}")
            task.status = TranslationStatus.FAILED
            self.mark_failed(task)
            return False

    def mark_failed(self, task: TranslationTask) -> bool:
        """标记失败·尝试重试"""
        if task.retry_count < self.retry_policy["max_retries"]:
            task.retry_count += 1
            delay = self.retry_policy["initial_delay"] * (
                self.retry_policy["backoff_multiplier"] ** (task.retry_count - 1)
            )
            logger.warning(f"⚠️ {task.task_id}: 将在 {delay} 秒后重试 (重试次数: {task.retry_count})")
            # 延迟后重新入队
            time.sleep(min(delay, 10))  # 最多等待 10 秒
            self.enqueue(task, priority=0)
            return True
        else:
            # 超过重试次数·标记为失败
            task.status = TranslationStatus.FAILED
            self.stats['failed_count'] += 1
            logger.error(f"❌ {task.task_id}: 超过最大重试次数·标记为失败")
            return False

    def assign_reviewer(self, task_id: str, reviewer: str) -> bool:
        """分配校对者"""
        if task_id not in self.tasks:
            return False

        self.tasks[task_id].reviewer = reviewer
        self.tasks[task_id].status = TranslationStatus.REVIEWING
        logger.info(f"✓ {task_id}: 分配给校对者 {reviewer}")
        return True

    def complete_task(
        self,
        task_id: str,
        quality_level: QualityLevel,
        notes: str = ""
    ) -> bool:
        """完成任务"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        task.status = TranslationStatus.COMPLETED
        task.quality_level = quality_level
        task.completed_at = datetime.now().isoformat()
        task.notes = notes

        logger.info(f"✅ {task_id}: 任务已完成（质量：{quality_level.value}）")
        return True

    def get_pending_tasks(self) -> List[TranslationTask]:
        """获取待翻译任务"""
        return [t for t in self.tasks.values()
                if t.status == TranslationStatus.PENDING]

    def get_processing_tasks(self) -> List[TranslationTask]:
        """获取处理中的任务"""
        return [t for t in self.tasks.values()
                if t.status == TranslationStatus.PROCESSING]

    def get_reviewing_tasks(self) -> List[TranslationTask]:
        """获取校对中的任务"""
        return [t for t in self.tasks.values()
                if t.status == TranslationStatus.REVIEWING]

    def get_completed_tasks(self) -> List[TranslationTask]:
        """获取已完成的任务"""
        return [t for t in self.tasks.values()
                if t.status == TranslationStatus.COMPLETED]

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        total = len(self.tasks)
        completed = len(self.get_completed_tasks())

        return {
            'total_tasks': total,
            'pending': len(self.get_pending_tasks()),
            'processing': len(self.get_processing_tasks()),
            'reviewing': len(self.get_reviewing_tasks()),
            'completed': completed,
            'failed': self.stats['failed_count'],
            'total_words': sum(t.word_count for t in self.tasks.values()),
            'completion_rate': (completed / total * 100) if total > 0 else 0,
            'total_processed': self.stats['total_processed']
        }

    def get_queue_length(self) -> int:
        """获取队列长度"""
        return self.queue.qsize()


# ============================================================================
# Notion 集成 (Module 1)
# ============================================================================

class NotionTranslationIntegration:
    """Notion 看板集成"""

    def __init__(self, manager: TaskQueueManager, notion_db_id: str = None):
        self.manager = manager
        self.notion_db_id = notion_db_id or "local_db"

        # 属性映射
        self.property_mapping = {
            'task_id': '任务编号',
            'status': '状态',
            'source_text': '源文本',
            'source_language': '源语言',
            'target_language': '目标语言',
            'translated_text': '翻译结果',
            'translator': '翻译者',
            'reviewer': '校对者',
            'quality_level': '翻译质量',
            'quality_score': '质量分数',
            'dna_signature': 'DNA签名',
            'created_at': '创建时间',
            'completed_at': '完成时间',
            'word_count': '字数',
            'notes': '备注'
        }

        logger.info("Notion 集成初始化完成")

    def sync_to_notion(self, task: TranslationTask) -> Dict:
        """同步任务到 Notion"""
        # 这是一个示意实现
        # 实际应该调用 Notion API

        logger.info(f"📤 同步任务到 Notion: {task.task_id}")

        return {
            'status': 'synced',
            'task_id': task.task_id,
            'notion_properties': {
                '任务编号': task.task_id,
                '状态': task.status.value,
                '源文本': task.source_text[:100] if task.source_text else '',
                '源语言': task.source_language.value,
                '目标语言': task.target_language.value,
                '翻译结果': task.translated_text or '',
                '翻译者': task.translator or '',
                '校对者': task.reviewer or '',
                '翻译质量': task.quality_level.value if task.quality_level else '',
                '质量分数': task.quality_score,
                'DNA签名': task.dna_signature or '',
                '字数': task.word_count,
                '备注': task.notes
            }
        }

    def auto_sync_workflow(self) -> Dict:
        """自动同步工作流"""
        stats = {
            'synced_pending': 0,
            'synced_processing': 0,
            'synced_reviewing': 0,
            'synced_completed': 0
        }

        logger.info("🔄 开始自动同步工作流...")

        # 同步待翻译任务
        for task in self.manager.get_pending_tasks():
            self.sync_to_notion(task)
            stats['synced_pending'] += 1

        # 同步处理中的任务
        for task in self.manager.get_processing_tasks():
            self.sync_to_notion(task)
            stats['synced_processing'] += 1

        # 同步审核中的任务
        for task in self.manager.get_reviewing_tasks():
            self.sync_to_notion(task)
            stats['synced_reviewing'] += 1

        # 同步已完成的任务
        for task in self.manager.get_completed_tasks():
            self.sync_to_notion(task)
            stats['synced_completed'] += 1

        logger.info(f"✅ 同步完成: {sum(stats.values())} 个任务")
        return stats


# ============================================================================
# 主系统类
# ============================================================================

class CNSHTranslationSystem:
    """CNSH 完整翻译系统"""

    def __init__(self, notion_db_id: str = None):
        self.manager = TaskQueueManager()
        self.notion = NotionTranslationIntegration(self.manager, notion_db_id)
        self.running = False

        logger.info("=" * 80)
        logger.info("🌐 CNSH 完整翻译系统 v1.0")
        logger.info("=" * 80)

    def process_queue(self) -> None:
        """处理队列中的任务"""
        logger.info("🚀 开始处理任务队列...")

        while True:
            task = self.manager.dequeue()

            if task is None:
                # 没有待处理的任务
                pending = self.manager.get_pending_tasks()
                if pending:
                    # 有待翻译的任务
                    logger.info(f"⏳ 队列中有 {len(pending)} 个待翻译任务")
                    for task in pending:
                        logger.info(f"  - {task.task_id}: {task.source_text[:30]}...")
                        self.manager.auto_translate_task(task.task_id)
                        self.notion.sync_to_notion(task)

                # 显示统计
                stats = self.manager.get_statistics()
                logger.info(f"\n📊 实时统计:")
                logger.info(f"  总任务数: {stats['total_tasks']}")
                logger.info(f"  待翻译: {stats['pending']}")
                logger.info(f"  AI处理中: {stats['processing']}")
                logger.info(f"  人工校对中: {stats['reviewing']}")
                logger.info(f"  已完成: {stats['completed']}")
                logger.info(f"  失败: {stats['failed']}")
                logger.info(f"  完成率: {stats['completion_rate']:.1f}%")
                logger.info(f"  总字数: {stats['total_words']}\n")

                break

            # 处理任务
            self.manager.auto_translate_task(task.task_id)
            self.notion.sync_to_notion(task)

    def interactive_mode(self) -> None:
        """交互模式"""
        logger.info("\n🎯 进入交互模式")
        logger.info("命令: create, list, translate, complete, stats, exit\n")

        while True:
            try:
                cmd = input("cnsh> ").strip()

                if cmd == 'exit':
                    break
                elif cmd == 'create':
                    self._cmd_create_task()
                elif cmd == 'list':
                    self._cmd_list_tasks()
                elif cmd == 'translate':
                    self._cmd_translate()
                elif cmd == 'complete':
                    self._cmd_complete()
                elif cmd == 'stats':
                    self._cmd_stats()
                else:
                    logger.info("未知命令")
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"错误: {e}")

    def _cmd_create_task(self) -> None:
        """创建任务"""
        source_text = input("源文本: ").strip()
        source_lang = input("源语言 (中/英/日): ").strip()
        target_lang = input("目标语言 (中/英/日): ").strip()

        lang_map = {'中': Language.CHINESE, '英': Language.ENGLISH, '日': Language.JAPANESE}

        if source_lang not in lang_map or target_lang not in lang_map:
            logger.error("不支持的语言")
            return

        task = self.manager.create_task(
            source_text,
            lang_map[source_lang],
            lang_map[target_lang]
        )
        logger.info(f"✓ 任务创建成功: {task.task_id}")

    def _cmd_list_tasks(self) -> None:
        """列出任务"""
        pending = self.manager.get_pending_tasks()
        processing = self.manager.get_processing_tasks()
        reviewing = self.manager.get_reviewing_tasks()
        completed = self.manager.get_completed_tasks()

        logger.info(f"\n📋 待翻译 ({len(pending)}):")
        for t in pending[:5]:
            logger.info(f"  {t.task_id}: {t.source_text[:40]}...")

        logger.info(f"\n⚙️ AI处理中 ({len(processing)}):")
        for t in processing[:5]:
            logger.info(f"  {t.task_id}: {t.source_text[:40]}...")

        logger.info(f"\n👁️ 人工校对中 ({len(reviewing)}):")
        for t in reviewing[:5]:
            logger.info(f"  {t.task_id}: {t.source_text[:40]}...")

        logger.info(f"\n✅ 已完成 ({len(completed)}):")
        for t in completed[:5]:
            logger.info(f"  {t.task_id}: {t.source_text[:40]}...")

    def _cmd_translate(self) -> None:
        """翻译任务"""
        task_id = input("任务ID: ").strip()

        if task_id not in self.manager.tasks:
            logger.error("任务不存在")
            return

        if self.manager.auto_translate_task(task_id):
            logger.info(f"✓ {task_id}: 翻译完成")
        else:
            logger.error(f"❌ {task_id}: 翻译失败")

    def _cmd_complete(self) -> None:
        """完成任务"""
        task_id = input("任务ID: ").strip()
        quality = input("质量等级 (优秀/良好/一般/待改进): ").strip()

        quality_map = {
            '优秀': QualityLevel.EXCELLENT,
            '良好': QualityLevel.GOOD,
            '一般': QualityLevel.FAIR,
            '待改进': QualityLevel.NEEDS_IMPROVEMENT
        }

        if quality not in quality_map:
            logger.error("无效的质量等级")
            return

        if self.manager.complete_task(task_id, quality_map[quality]):
            logger.info(f"✓ {task_id}: 已标记为完成")
        else:
            logger.error(f"❌ {task_id}: 操作失败")

    def _cmd_stats(self) -> None:
        """显示统计"""
        stats = self.manager.get_statistics()
        logger.info(f"\n📊 统计信息:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")


# ============================================================================
# 演示和测试
# ============================================================================

def demo():
    """演示模式·单次运行"""

    system = CNSHTranslationSystem()

    # 创建示例任务
    logger.info("\n📝 创建翻译任务...")

    test_cases = [
        ("龍魂系统是一个完整的通心译框架", Language.CHINESE, Language.ENGLISH),
        ("This is a translation test", Language.ENGLISH, Language.CHINESE),
        ("你好，世界", Language.CHINESE, Language.ENGLISH),
    ]

    for source_text, source_lang, target_lang in test_cases:
        task = system.manager.create_task(source_text, source_lang, target_lang)
        logger.info(f"✓ {task.task_id}: {source_text}")

    logger.info("\n")

    # 自动处理队列
    system.process_queue()

    logger.info("\n" + "=" * 80)
    logger.info("✅ 演示完成")
    logger.info("=" * 80)


def run_forever():
    """生产模式·无限循环自运行

    系统启动后：
    1. 初始化完成
    2. 进入无限循环
    3. 定期扫描任务队列
    4. 自动处理新任务
    5. 支持热重启和迭代升级
    """

    system = CNSHTranslationSystem()

    logger.info("\n" + "=" * 80)
    logger.info("🚀 CNSH 翻译系统启动（无限循环模式）")
    logger.info("=" * 80)
    logger.info("✓ 系统已初始化")
    logger.info("✓ 任务队列管理器就绪")
    logger.info("✓ Notion 集成已激活")
    logger.info("✓ DNA 签名生成器启动")
    logger.info("\n进入主循环·监听任务队列...\n")

    # 无限循环运行
    loop_count = 0
    while True:
        try:
            loop_count += 1

            # 每100循环输出一次心跳信号（防止日志过多）
            if loop_count % 100 == 0:
                stats = system.manager.get_statistics()
                logger.info(f"💓 [心跳 #{loop_count}] 队列状态: "
                           f"待处理={stats['pending']}, "
                           f"校对中={stats['reviewing']}, "
                           f"已完成={stats['completed']}")

            # 处理队列中的任务
            if system.manager.get_queue_length() > 0:
                system.process_queue()

            # 等待0.5秒后继续（避免CPU占用过高）
            time.sleep(0.5)

        except KeyboardInterrupt:
            logger.info("\n\n" + "=" * 80)
            logger.info("🛑 收到停止信号，系统优雅关闭中...")
            logger.info("=" * 80)
            stats = system.manager.get_statistics()
            logger.info(f"📊 最终统计:")
            logger.info(f"   总任务数: {stats['total_tasks']}")
            logger.info(f"   已完成: {stats['completed']}")
            logger.info(f"   校对中: {stats['reviewing']}")
            logger.info(f"   待处理: {stats['pending']}")
            logger.info("✅ 系统已关闭\n")
            break
        except Exception as e:
            logger.error(f"❌ 处理过程中发生错误: {e}")
            logger.info("⚠ 系统继续运行，2秒后重试...")
            time.sleep(2)


if __name__ == '__main__':
    import sys

    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        # 演示模式：运行一次就退出
        demo()
    else:
        # 生产模式：无限循环（默认）
        run_forever()
