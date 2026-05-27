#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂 · CNSH FastAPI 任务提交接口 v1.0
CNSH Translation System - FastAPI Task Submission Interface

DNA追溯碼：#龍芯⚡️2026-05-27-CNSH-FASTAPI-INTERFACE-v1.0
CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 提供 FastAPI REST API 接口
  2. 接收外部 JSON 任务请求
  3. 验证任务数据并放入优先级队列
  4. 返回任务 ID 和提交确认消息
  5. 支持查询任务状态和队列统计

安装与运行：
  pip install fastapi uvicorn python-dotenv
  python3 cnsh_fastapi_interface.py

访问：
  API 主页: http://localhost:8000
  API 文档: http://localhost:8000/docs
  提交任务: POST http://localhost:8000/submit_task
  任务状态: GET http://localhost:8000/task/{task_id}
  队列统计: GET http://localhost:8000/stats
"""

import sys
import json
import logging
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from enum import Enum

# 导入 FastAPI 和 CORS
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    from uvicorn import run
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("⚠️  警告: FastAPI 和 Uvicorn 未安装")
    print("   请运行: pip install fastapi uvicorn pydantic")

# 导入配置管理器
sys.path.insert(0, str(Path(__file__).parent))

try:
    from 配置读取器 import CONFIG
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    print("⚠️  警告: 配置读取器不可用，使用默认端口")

# 导入 CNSH 系统
try:
    from cnsh_translator_complete import (
        CNSHTranslationSystem,
        Language,
        TranslationStatus,
        TranslationTask
    )
    CNSH_AVAILABLE = True
except ImportError as e:
    CNSH_AVAILABLE = False
    print(f"⚠️  警告: CNSH 系统导入失败: {e}")

# ============================================================================
# 日志配置
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# FastAPI 应用初始化
# ============================================================================

if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="🐉 龍魂 CNSH 任务提交接口",
        description="CNSH 翻译系统 - 外部任务提交 API",
        version="1.0.0"
    )

    # CORS 中间件 - 允许跨域请求
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ============================================================================
# 数据模型
# ============================================================================

class LanguageEnum(str, Enum):
    """支持的语言"""
    CHINESE = "中文"
    ENGLISH = "英文"
    JAPANESE = "日文"
    KHMER = "柬文"
    OTHER = "其他"


class TaskSubmissionRequest(BaseModel):
    """任务提交请求"""
    source_text: str = Field(..., min_length=1, max_length=10000,
                             description="源文本")
    source_language: LanguageEnum = Field(...,
                                         description="源语言")
    target_language: LanguageEnum = Field(...,
                                         description="目标语言")
    priority: int = Field(default=0, ge=0, le=100,
                         description="优先级 (0-100, 越小越优先)")
    notes: str = Field(default="", max_length=500,
                      description="任务备注")

    class Config:
        example = {
            "source_text": "你好，这是一个翻译任务",
            "source_language": "中文",
            "target_language": "英文",
            "priority": 10,
            "notes": "来自外部系统的任务"
        }


class TaskSubmissionResponse(BaseModel):
    """任务提交响应"""
    success: bool = Field(..., description="是否提交成功")
    message: str = Field(..., description="状态消息")
    task_id: Optional[str] = Field(default=None, description="任务 ID")
    timestamp: str = Field(..., description="提交时间")
    queue_length: int = Field(..., description="当前队列长度")

    class Config:
        example = {
            "success": True,
            "message": "✅ 任务已接收并放入队列",
            "task_id": "TRANS-000001",
            "timestamp": "2026-05-27T23:30:00",
            "queue_length": 5
        }


class TaskStatusResponse(BaseModel):
    """任务状态响应"""
    task_id: str = Field(..., description="任务 ID")
    status: str = Field(..., description="任务状态")
    source_text: str = Field(..., description="源文本")
    source_language: str = Field(..., description="源语言")
    target_language: str = Field(..., description="目标语言")
    translated_text: Optional[str] = Field(default=None, description="翻译结果")
    quality_score: float = Field(..., description="质量评分 (0-100)")
    created_at: str = Field(..., description="创建时间")
    completed_at: Optional[str] = Field(default=None, description="完成时间")
    word_count: int = Field(..., description="词数")
    notes: str = Field(..., description="备注")


class QueueStatsResponse(BaseModel):
    """队列统计响应"""
    timestamp: str = Field(..., description="统计时间")
    total_tasks: int = Field(..., description="总任务数")
    pending: int = Field(..., description="待处理")
    processing: int = Field(..., description="处理中")
    reviewing: int = Field(..., description="校对中")
    completed: int = Field(..., description="已完成")
    failed: int = Field(..., description="失败")
    queue_length: int = Field(..., description="当前队列长度")
    average_quality_score: float = Field(..., description="平均质量评分")


# ============================================================================
# 全局 CNSH 系统实例
# ============================================================================

cnsh_system: Optional[CNSHTranslationSystem] = None
system_initialized = False


def initialize_system():
    """初始化 CNSH 系统"""
    global cnsh_system, system_initialized

    if not CNSH_AVAILABLE:
        logger.error("CNSH 系统不可用")
        return False

    try:
        cnsh_system = CNSHTranslationSystem()
        system_initialized = True
        logger.info("✅ CNSH 系统初始化成功")
        return True
    except Exception as e:
        logger.error(f"❌ CNSH 系统初始化失败: {e}")
        return False


def run_system_background():
    """在后台线程运行 CNSH 系统的无限循环"""
    if not system_initialized or cnsh_system is None:
        logger.warning("⚠️  CNSH 系统未初始化，无法启动后台监听")
        return

    logger.info("🚀 启动 CNSH 任务队列监听线程...")

    def background_loop():
        loop_count = 0
        while True:
            try:
                loop_count += 1

                # 每 100 循环输出一次心跳
                if loop_count % 100 == 0:
                    stats = cnsh_system.manager.get_statistics()
                    logger.info(f"💓 [后台监听 #{loop_count}] 队列: "
                              f"待处理={stats['pending']}, "
                              f"处理中={stats['processing']}, "
                              f"已完成={stats['completed']}")

                # 处理队列中的任务
                if cnsh_system.manager.get_queue_length() > 0:
                    cnsh_system.process_queue()

                # 等待 0.5 秒
                time.sleep(0.5)

            except KeyboardInterrupt:
                logger.info("🛑 后台监听线程收到停止信号")
                break
            except Exception as e:
                logger.error(f"❌ 后台处理错误: {e}")
                time.sleep(2)

    # 创建后台线程
    thread = threading.Thread(target=background_loop, daemon=True)
    thread.start()
    logger.info("✅ 后台监听线程已启动")


# ============================================================================
# API 路由
# ============================================================================

if FASTAPI_AVAILABLE:

    @app.on_event("startup")
    async def startup_event():
        """应用启动事件"""
        logger.info("=" * 80)
        logger.info("🐉 龍魂 CNSH FastAPI 接口启动")
        logger.info("=" * 80)

        # 初始化系统
        if initialize_system():
            # 启动后台任务队列监听
            run_system_background()
        else:
            logger.warning("⚠️  CNSH 系统初始化失败，API 仅支持任务提交")


    @app.get("/", tags=["主页"])
    async def read_root():
        """API 主页"""
        return {
            "title": "🐉 龍魂 CNSH 任务提交接口",
            "version": "1.0.0",
            "dna": "#龍芯⚡️2026-05-27-CNSH-FASTAPI-INTERFACE-v1.0",
            "endpoints": {
                "POST /submit_task": "提交新的翻译任务",
                "GET /task/{task_id}": "查询任务状态",
                "GET /stats": "获取队列统计信息",
                "GET /docs": "API 文档 (Swagger UI)",
                "GET /redoc": "API 文档 (ReDoc)"
            },
            "system_status": "initialized" if system_initialized else "not_initialized",
            "timestamp": datetime.now().isoformat()
        }


    @app.post("/submit_task", response_model=TaskSubmissionResponse,
              tags=["任务提交"])
    async def submit_task(request: TaskSubmissionRequest):
        """
        提交新的翻译任务到队列

        接收 JSON 格式的任务请求，验证数据后放入优先级队列。

        **请求体示例**:
        ```json
        {
          "source_text": "你好，这是一个翻译任务",
          "source_language": "中文",
          "target_language": "英文",
          "priority": 10,
          "notes": "来自外部系统的任务"
        }
        ```

        **返回**:
        - success: 是否提交成功
        - message: 状态消息
        - task_id: 任务 ID (用于后续查询)
        - timestamp: 提交时间戳
        - queue_length: 当前队列长度
        """

        if not system_initialized or cnsh_system is None:
            logger.warning("⚠️  系统未初始化，拒绝任务提交")
            raise HTTPException(
                status_code=503,
                detail="系统未初始化，请稍后重试"
            )

        try:
            # 将语言字符串转换为 Language 枚举
            source_lang = Language(request.source_language.value)
            target_lang = Language(request.target_language.value)

            # 验证：源语言和目标语言不能相同
            if source_lang == target_lang:
                raise HTTPException(
                    status_code=400,
                    detail="源语言和目标语言不能相同"
                )

            # 创建任务
            task = cnsh_system.manager.create_task(
                source_text=request.source_text,
                source_language=source_lang,
                target_language=target_lang
            )

            # 设置备注
            if request.notes:
                task.notes = request.notes

            # 更新任务的优先级（重新入队）
            cnsh_system.manager.enqueue(task, priority=request.priority)

            # 记录提交
            logger.info(f"✅ 外部任务已提交: {task.task_id} "
                       f"({source_lang.value} → {target_lang.value})")

            # 返回响应
            return TaskSubmissionResponse(
                success=True,
                message="✅ 任务已接收并放入队列",
                task_id=task.task_id,
                timestamp=datetime.now().isoformat(),
                queue_length=cnsh_system.manager.get_queue_length()
            )

        except ValueError as e:
            logger.error(f"❌ 语言参数错误: {e}")
            raise HTTPException(status_code=400, detail="不支持的语言类型")
        except Exception as e:
            logger.error(f"❌ 任务提交失败: {e}")
            raise HTTPException(status_code=500, detail="任务提交失败")


    @app.get("/task/{task_id}", response_model=TaskStatusResponse,
            tags=["任务查询"])
    async def get_task_status(task_id: str):
        """
        查询任务状态

        通过任务 ID 获取任务的详细状态信息。

        **参数**:
        - task_id: 任务 ID (例如: TRANS-000001)

        **返回**:
        - task_id: 任务 ID
        - status: 任务状态 (待翻译/处理中/校对中/已完成/失败)
        - translated_text: 翻译结果 (若已完成)
        - quality_score: 质量评分 (0-100)
        - 其他详细信息
        """

        if not system_initialized or cnsh_system is None:
            raise HTTPException(status_code=503, detail="系统未初始化")

        # 查找任务
        if task_id not in cnsh_system.manager.tasks:
            logger.warning(f"⚠️  任务不存在: {task_id}")
            raise HTTPException(status_code=404, detail="任务不存在")

        task = cnsh_system.manager.tasks[task_id]

        logger.info(f"📋 查询任务状态: {task_id} - {task.status.value}")

        return TaskStatusResponse(
            task_id=task.task_id,
            status=task.status.value,
            source_text=task.source_text,
            source_language=task.source_language.value,
            target_language=task.target_language.value,
            translated_text=task.translated_text,
            quality_score=task.quality_score,
            created_at=task.created_at,
            completed_at=task.completed_at,
            word_count=task.word_count,
            notes=task.notes
        )


    @app.get("/stats", response_model=QueueStatsResponse, tags=["统计信息"])
    async def get_queue_stats():
        """
        获取队列统计信息

        返回当前任务队列的全体统计数据。

        **返回**:
        - total_tasks: 总任务数
        - pending: 待处理任务数
        - processing: 处理中任务数
        - reviewing: 校对中任务数
        - completed: 已完成任务数
        - failed: 失败任务数
        - queue_length: 当前队列长度
        - average_quality_score: 平均质量评分
        """

        if not system_initialized or cnsh_system is None:
            raise HTTPException(status_code=503, detail="系统未初始化")

        stats = cnsh_system.manager.get_statistics()
        queue_length = cnsh_system.manager.get_queue_length()

        # 计算平均质量评分
        completed_tasks = [t for t in cnsh_system.manager.tasks.values()
                          if t.status == TranslationStatus.COMPLETED]
        avg_quality = sum(t.quality_score for t in completed_tasks) / len(completed_tasks) \
                     if completed_tasks else 0.0

        logger.info(f"📊 队列统计: 总任务={stats['total_tasks']}, "
                   f"待处理={stats['pending']}, "
                   f"已完成={stats['completed']}")

        return QueueStatsResponse(
            timestamp=datetime.now().isoformat(),
            total_tasks=stats['total_tasks'],
            pending=stats['pending'],
            processing=stats['processing'],
            reviewing=stats['reviewing'],
            completed=stats['completed'],
            failed=stats['failed'],
            queue_length=queue_length,
            average_quality_score=avg_quality
        )


    @app.get("/health", tags=["系统监控"])
    async def health_check():
        """健康检查"""
        return {
            "status": "healthy",
            "system_initialized": system_initialized,
            "timestamp": datetime.now().isoformat()
        }


    @app.get("/reset", tags=["管理员"])
    async def reset_system():
        """重置系统（清空所有任务）"""
        global cnsh_system, system_initialized

        if not system_initialized:
            raise HTTPException(status_code=503, detail="系统未初始化")

        try:
            # 创建新的系统实例
            cnsh_system = CNSHTranslationSystem()
            logger.warning("🔄 系统已重置，所有任务已清除")

            return {
                "success": True,
                "message": "系统已重置",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ 重置失败: {e}")
            raise HTTPException(status_code=500, detail="重置失败")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    if not FASTAPI_AVAILABLE:
        print("\n❌ 错误: FastAPI 和 Uvicorn 未安装")
        print("请运行以下命令安装依赖:")
        print("  pip install fastapi uvicorn pydantic")
        sys.exit(1)

    # 从统一配置读取端口
    if CONFIG_AVAILABLE:
        host = CONFIG.get('MAIN_API_HOST', '0.0.0.0')
        port = CONFIG.get('CNSH_FASTAPI_PORT', 8000)
    else:
        host = "0.0.0.0"
        port = 8000

    print("\n" + "=" * 80)
    print("🐉 龍魂 CNSH FastAPI 任务提交接口")
    print("=" * 80)
    print(f"DNA: #龍芯⚡️2026-05-27-CNSH-FASTAPI-INTERFACE-v1.0")
    print(f"启动时间: {datetime.now().isoformat()}\n")

    print("📱 API 访问地址:")
    print(f"   - 主页: http://localhost:{port}")
    print(f"   - 文档: http://localhost:{port}/docs (Swagger UI)")
    print(f"   - ReDoc: http://localhost:{port}/redoc\n")

    print("📋 快速开始:")
    print("   1. 提交任务:")
    print(f"      curl -X POST http://localhost:{port}/submit_task \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{")
    print('          "source_text": "你好",')
    print('          "source_language": "中文",')
    print('          "target_language": "英文",')
    print('          "priority": 10')
    print("        }'\n")

    print("   2. 查询任务状态:")
    print(f"      curl http://localhost:{port}/task/TRANS-000001\n")

    print("   3. 获取队列统计:")
    print(f"      curl http://localhost:{port}/stats\n")

    print("⌨️  按 Ctrl+C 停止服务器\n")

    # 启动 FastAPI 应用
    run(app, host=host, port=port, reload=False)


if __name__ == "__main__":
    if FASTAPI_AVAILABLE:
        main()
    else:
        print("\n❌ FastAPI 不可用")
        print("请运行: pip install fastapi uvicorn pydantic")
