#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Notion API 统一客户端 v1.0

DNA: #龍芯⚇️2026-06-01-NOTION-CLIENT-v1.0
UID: 9622
Purpose: 提供统一的 Notion API 接口，包含错误处理、重试和速率限制

Features:
  - 统一的 API 调用接口
  - 自动重试和指数退避
  - 速率限制和请求排队
  - 完整的错误处理和日志
  - 支持批量操作
  - CRUD 操作抽象
  - 实时请求追踪（DNA 签名）
"""

import urllib.request
import urllib.error
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import hashlib
import sys

# Handle both relative and absolute imports
try:
    from .notion_config import NotionConfig, NotionConfigManager
except ImportError:
    from notion_config import NotionConfig, NotionConfigManager


class NotionAPIError(Exception):
    """Notion API 错误基类"""
    pass


class NotionAuthError(NotionAPIError):
    """认证错误"""
    pass


class NotionRateLimitError(NotionAPIError):
    """速率限制错误"""
    pass


class NotionClient:
    """统一的 Notion API 客户端"""

    def __init__(self, config: Optional[NotionConfig] = None):
        if not config:
            manager = NotionConfigManager()
            config = manager.load()

        self.config = config
        self.headers = {
            "Authorization": f"Bearer {config.api_token}",
            "Notion-Version": config.api_version,
            "Content-Type": "application/json",
        }

        # 速率限制器
        self.rate_limit_per_second = config.rate_limit
        self.last_request_time = 0
        self.request_count = 0

        # 审计日志
        self.audit_log_file = Path.home() / ".龍魂" / "notion_api_audit.jsonl"
        self.audit_log_file.parent.mkdir(parents=True, exist_ok=True)

    def _apply_rate_limit(self):
        """应用速率限制"""
        now = time.time()
        time_since_last = now - self.last_request_time

        min_interval = 1.0 / self.rate_limit_per_second
        if time_since_last < min_interval:
            sleep_time = min_interval - time_since_last
            time.sleep(sleep_time)

        self.last_request_time = time.time()
        self.request_count += 1

    def _log_audit(
        self,
        method: str,
        endpoint: str,
        status: str,
        payload: Optional[Dict] = None,
        response: Optional[Dict] = None,
        error: Optional[str] = None,
    ):
        """记录 API 调用到审计日志"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "endpoint": endpoint,
            "status": status,
            "request_hash": hashlib.md5(
                json.dumps(payload, sort_keys=True, default=str).encode()
            ).hexdigest()[:8] if payload else None,
            "response_hash": hashlib.md5(
                json.dumps(response, sort_keys=True, default=str).encode()
            ).hexdigest()[:8] if response else None,
            "error": error,
            "dna": f"#龍芯⚇️{datetime.now().strftime('%Y%m%d')}-API-{method}",
        }

        with open(self.audit_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    def _request(
        self,
        method: str,
        endpoint: str,
        payload: Optional[Dict] = None,
        retry_count: int = 0,
    ) -> Tuple[Dict, bool]:
        """执行 HTTP 请求（带重试机制）"""
        self._apply_rate_limit()

        url = f"{self.config.base_url}{endpoint}"

        try:
            data = None
            if payload:
                data = json.dumps(payload, ensure_ascii=False).encode('utf-8')

            req = urllib.request.Request(
                url,
                data=data,
                headers=self.headers,
                method=method,
            )

            with urllib.request.urlopen(req, timeout=self.config.timeout) as resp:
                response = json.loads(resp.read().decode('utf-8'))
                self._log_audit(method, endpoint, "success", payload, response)
                return response, True

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            error_data = json.loads(error_body) if error_body else {}

            # 处理速率限制
            if e.code == 429:
                if retry_count < self.config.retry_count:
                    wait_time = 2 ** retry_count  # 指数退避
                    print(f"⏳ 速率限制，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    return self._request(method, endpoint, payload, retry_count + 1)
                else:
                    self._log_audit(method, endpoint, "rate_limit_exceeded", payload, error=error_data.get('message'))
                    raise NotionRateLimitError(f"超过速率限制: {error_data.get('message')}")

            # 处理认证错误
            if e.code in (401, 403):
                self._log_audit(method, endpoint, "auth_error", payload, error=error_data.get('message'))
                raise NotionAuthError(f"认证失败: {error_data.get('message')}")

            # 其他可重试的错误
            if e.code >= 500 and retry_count < self.config.retry_count:
                wait_time = 2 ** retry_count
                print(f"⚠️  服务器错误 ({e.code})，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
                return self._request(method, endpoint, payload, retry_count + 1)

            self._log_audit(method, endpoint, "error", payload, error=error_data.get('message'))
            raise NotionAPIError(
                f"Notion API 错误 ({e.code}): {error_data.get('message', str(e))}"
            )

        except Exception as e:
            self._log_audit(method, endpoint, "exception", payload, error=str(e))
            raise NotionAPIError(f"请求失败: {str(e)}")

    def create_page(self, database_id: str, properties: Dict) -> Dict:
        """在数据库中创建页面"""
        payload = {
            "parent": {"database_id": database_id},
            "properties": properties,
        }

        response, _ = self._request("POST", "/pages", payload)
        return response

    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """更新页面属性"""
        payload = {"properties": properties}
        response, _ = self._request("PATCH", f"/pages/{page_id}", payload)
        return response

    def query_database(
        self,
        database_id: str,
        filter: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        page_size: int = 100,
    ) -> Dict:
        """查询数据库"""
        payload = {
            "page_size": min(page_size, 100),
        }

        if filter:
            payload["filter"] = filter

        if sorts:
            payload["sorts"] = sorts

        response, _ = self._request("POST", f"/databases/{database_id}/query", payload)
        return response

    def get_page(self, page_id: str) -> Dict:
        """获取页面详情"""
        response, _ = self._request("GET", f"/pages/{page_id}")
        return response

    def delete_page(self, page_id: str) -> Dict:
        """删除页面"""
        payload = {"archived": True}
        response, _ = self._request("PATCH", f"/pages/{page_id}", payload)
        return response

    def get_database(self, database_id: str) -> Dict:
        """获取数据库详情"""
        response, _ = self._request("GET", f"/databases/{database_id}")
        return response

    def list_databases(self) -> Dict:
        """列出所有数据库（需要工作区 ID）"""
        response, _ = self._request("GET", "/databases")
        return response

    def append_block_children(self, page_id: str, children: List[Dict]) -> Dict:
        """为页面添加块元素"""
        payload = {"children": children}
        response, _ = self._request("PATCH", f"/blocks/{page_id}/children", payload)
        return response

    def create_database(
        self,
        parent_id: str,
        title: str,
        properties: Dict,
        is_page_parent: bool = False,
    ) -> Dict:
        """创建新数据库"""
        payload = {
            "parent": {
                "page_id" if is_page_parent else "database_id": parent_id
            },
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties,
        }

        response, _ = self._request("POST", "/databases", payload)
        return response

    def batch_create_pages(self, database_id: str, pages: List[Dict]) -> List[Dict]:
        """批量创建页面"""
        results = []

        for i, page_props in enumerate(pages):
            try:
                result = self.create_page(database_id, page_props)
                results.append({"status": "success", "page_id": result.get('id')})
                print(f"  ✅ 页面 {i+1}/{len(pages)}")
            except NotionAPIError as e:
                results.append({"status": "error", "error": str(e)})
                print(f"  ❌ 页面 {i+1}/{len(pages)}: {str(e)}")

        return results

    def test_connection(self) -> bool:
        """测试 API 连接"""
        try:
            print("🔍 测试 Notion API 连接...")
            response, _ = self._request("GET", "/users/me")
            print(f"✅ 连接成功！用户: {response.get('name', 'Unknown')}")
            return True
        except NotionAuthError:
            print("❌ 认证失败，请检查 NOTION_TOKEN")
            return False
        except NotionAPIError as e:
            print(f"❌ 连接失败: {e}")
            return False

    def print_audit_summary(self):
        """打印审计日志摘要"""
        if not self.audit_log_file.exists():
            print("📊 未发现审计日志")
            return

        stats = {"success": 0, "error": 0, "rate_limit": 0}
        methods = {}

        try:
            with open(self.audit_log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    record = json.loads(line)
                    status = record.get('status', '')

                    if status == "success":
                        stats["success"] += 1
                    elif status == "rate_limit_exceeded":
                        stats["rate_limit"] += 1
                    else:
                        stats["error"] += 1

                    method = record.get('method', 'unknown')
                    methods[method] = methods.get(method, 0) + 1

            print("\n📊 API 调用统计")
            print("=" * 60)
            print(f"总调用: {sum(stats.values())}")
            print(f"  ✅ 成功: {stats['success']}")
            print(f"  ⚠️  错误: {stats['error']}")
            print(f"  🚫 速率限制: {stats['rate_limit']}")
            print(f"\n方法统计:")
            for method, count in sorted(methods.items()):
                print(f"  {method}: {count}")
            print("=" * 60)
        except Exception as e:
            print(f"⚠️  无法读取审计日志: {e}")


if __name__ == "__main__":
    # 测试客户端
    try:
        client = NotionClient()
        if client.test_connection():
            client.print_audit_summary()
    except Exception as e:
        print(f"❌ 错误: {e}")
