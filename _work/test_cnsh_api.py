#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂 CNSH FastAPI 接口测试脚本
Test script for CNSH FastAPI Task Submission Interface

使用 curl 或此脚本测试 /submit_task 接口

运行：
  python3 test_cnsh_api.py
"""

import json
import requests
from datetime import datetime

# API 基础地址
BASE_URL = "http://localhost:8000"
TIMEOUT = 10

print("\n" + "=" * 80)
print("🐉 龍魂 CNSH FastAPI 接口测试")
print("=" * 80)
print(f"API 地址: {BASE_URL}")
print(f"测试时间: {datetime.now().isoformat()}\n")

# ============================================================================
# 测试 1: 健康检查
# ============================================================================

print("【测试 1】健康检查")
print("-" * 80)

try:
    response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
    print(f"✅ 状态码: {response.status_code}")
    print(f"✅ 响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}\n")
except Exception as e:
    print(f"❌ 错误: {e}\n")
    print("⚠️  确保 FastAPI 服务已启动:")
    print("   python3 cnsh_fastapi_interface.py\n")
    exit(1)


# ============================================================================
# 测试 2: 获取 API 主页
# ============================================================================

print("【测试 2】API 主页")
print("-" * 80)

try:
    response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
    data = response.json()
    print(f"✅ 标题: {data.get('title')}")
    print(f"✅ 版本: {data.get('version')}")
    print(f"✅ 系统状态: {data.get('system_status')}")
    print(f"✅ 可用端点:")
    for endpoint, description in data.get('endpoints', {}).items():
        print(f"   - {endpoint}: {description}")
    print()
except Exception as e:
    print(f"❌ 错误: {e}\n")


# ============================================================================
# 测试 3: 提交任务 1 (中文 → 英文)
# ============================================================================

print("【测试 3】提交任务 (中文 → 英文)")
print("-" * 80)

task1_data = {
    "source_text": "你好，这是一个来自 FastAPI 接口的翻译任务",
    "source_language": "中文",
    "target_language": "英文",
    "priority": 10,
    "notes": "来自测试脚本的任务"
}

try:
    response = requests.post(
        f"{BASE_URL}/submit_task",
        json=task1_data,
        timeout=TIMEOUT
    )
    result = response.json()
    task1_id = result.get('task_id')

    print(f"✅ 状态码: {response.status_code}")
    print(f"✅ 消息: {result.get('message')}")
    print(f"✅ 任务 ID: {task1_id}")
    print(f"✅ 队列长度: {result.get('queue_length')}")
    print()
except Exception as e:
    print(f"❌ 错误: {e}\n")
    task1_id = None


# ============================================================================
# 测试 4: 提交任务 2 (英文 → 中文)
# ============================================================================

print("【测试 4】提交任务 (英文 → 中文)")
print("-" * 80)

task2_data = {
    "source_text": "Hello, this is a translation task from FastAPI",
    "source_language": "英文",
    "target_language": "中文",
    "priority": 5,
    "notes": "优先级较高的任务"
}

try:
    response = requests.post(
        f"{BASE_URL}/submit_task",
        json=task2_data,
        timeout=TIMEOUT
    )
    result = response.json()
    task2_id = result.get('task_id')

    print(f"✅ 状态码: {response.status_code}")
    print(f"✅ 消息: {result.get('message')}")
    print(f"✅ 任务 ID: {task2_id}")
    print(f"✅ 队列长度: {result.get('queue_length')}")
    print()
except Exception as e:
    print(f"❌ 错误: {e}\n")
    task2_id = None


# ============================================================================
# 测试 5: 提交任务 3 (中文 → 日文)
# ============================================================================

print("【测试 5】提交任务 (中文 → 日文)")
print("-" * 80)

task3_data = {
    "source_text": "龍魂系統完全就緒",
    "source_language": "中文",
    "target_language": "日文",
    "priority": 15,
    "notes": "系统验证任务"
}

try:
    response = requests.post(
        f"{BASE_URL}/submit_task",
        json=task3_data,
        timeout=TIMEOUT
    )
    result = response.json()
    task3_id = result.get('task_id')

    print(f"✅ 状态码: {response.status_code}")
    print(f"✅ 消息: {result.get('message')}")
    print(f"✅ 任务 ID: {task3_id}")
    print(f"✅ 队列长度: {result.get('queue_length')}")
    print()
except Exception as e:
    print(f"❌ 错误: {e}\n")
    task3_id = None


# ============================================================================
# 测试 6: 获取队列统计
# ============================================================================

print("【测试 6】获取队列统计")
print("-" * 80)

try:
    response = requests.get(f"{BASE_URL}/stats", timeout=TIMEOUT)
    stats = response.json()

    print(f"✅ 统计时间: {stats.get('timestamp')}")
    print(f"✅ 总任务数: {stats.get('total_tasks')}")
    print(f"✅ 待处理: {stats.get('pending')}")
    print(f"✅ 处理中: {stats.get('processing')}")
    print(f"✅ 校对中: {stats.get('reviewing')}")
    print(f"✅ 已完成: {stats.get('completed')}")
    print(f"✅ 失败: {stats.get('failed')}")
    print(f"✅ 当前队列长度: {stats.get('queue_length')}")
    print(f"✅ 平均质量评分: {stats.get('average_quality_score'):.1f}")
    print()
except Exception as e:
    print(f"❌ 错误: {e}\n")


# ============================================================================
# 测试 7: 查询任务状态
# ============================================================================

if task1_id:
    print(f"【测试 7】查询任务状态 ({task1_id})")
    print("-" * 80)

    try:
        response = requests.get(f"{BASE_URL}/task/{task1_id}", timeout=TIMEOUT)
        task = response.json()

        print(f"✅ 任务 ID: {task.get('task_id')}")
        print(f"✅ 状态: {task.get('status')}")
        print(f"✅ 源语言: {task.get('source_language')} → {task.get('target_language')}")
        print(f"✅ 源文本: {task.get('source_text')}")
        print(f"✅ 翻译结果: {task.get('translated_text')}")
        print(f"✅ 质量评分: {task.get('quality_score')}")
        print(f"✅ 创建时间: {task.get('created_at')}")
        print(f"✅ 完成时间: {task.get('completed_at')}")
        print(f"✅ 词数: {task.get('word_count')}")
        print(f"✅ 备注: {task.get('notes')}")
        print()
    except Exception as e:
        print(f"❌ 错误: {e}\n")


# ============================================================================
# 测试 8: 错误处理 - 相同的源和目标语言
# ============================================================================

print("【测试 8】错误处理 - 相同的源和目标语言")
print("-" * 80)

bad_data = {
    "source_text": "这会失败",
    "source_language": "中文",
    "target_language": "中文",  # ❌ 错误：源和目标相同
    "priority": 10
}

try:
    response = requests.post(
        f"{BASE_URL}/submit_task",
        json=bad_data,
        timeout=TIMEOUT
    )

    if response.status_code == 400:
        print(f"✅ 正确捕获错误:")
        print(f"   状态码: {response.status_code}")
        print(f"   错误: {response.json().get('detail')}")
    else:
        print(f"❌ 意外的状态码: {response.status_code}")
    print()
except Exception as e:
    print(f"❌ 错误: {e}\n")


# ============================================================================
# 总结
# ============================================================================

print("=" * 80)
print("✅ 测试完成")
print("=" * 80)

print("\n📋 API 端点总结:")
print("   POST /submit_task    - 提交新任务到队列")
print("   GET  /task/{task_id} - 查询任务状态")
print("   GET  /stats          - 获取队列统计信息")
print("   GET  /health         - 健康检查")
print("   GET  /reset          - 重置系统 (清空所有任务)")

print("\n📚 完整文档:")
print("   http://localhost:8000/docs (Swagger UI)")
print("   http://localhost:8000/redoc (ReDoc)")

print("\n💡 使用 curl 示例:")
print("""
# 提交任务
curl -X POST http://localhost:8000/submit_task \\
  -H 'Content-Type: application/json' \\
  -d '{
    "source_text": "你好",
    "source_language": "中文",
    "target_language": "英文",
    "priority": 10,
    "notes": "测试任务"
  }'

# 查询任务
curl http://localhost:8000/task/TRANS-000001

# 获取统计
curl http://localhost:8000/stats
""")

print()
