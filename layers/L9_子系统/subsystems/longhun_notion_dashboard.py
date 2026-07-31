# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Notion 公开仪表盘 v1.0

在 Notion 公开页下自动创建/维护：
- 龍魂公开仪表盘（子页面）
- 攻击地图数据库
- 审计登记数据库

DNA: #龍芯⚡️2026-06-29-LONGHUN-NOTION-DASHBOARD-v1-UID9622
"""
from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DNA = "#龍芯⚡️2026-06-29-LONGHUN-NOTION-DASHBOARD-v1-UID9622"

HOME = Path.home()
STATE_PATH = HOME / ".longhun" / "notion_dashboard.json"
NOTION_VERSION = "2022-06-28"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_state() -> Dict[str, Any]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save_state(state: Dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _api(token: str, method: str, endpoint: str, payload: Optional[Dict] = None) -> Dict[str, Any]:
    """通过 curl 调用 Notion API，避免 Python urllib 对 Notion 的超时/连接问题。"""
    url = f"https://api.notion.com/v1/{endpoint}"
    args = [
        "curl", "-s", "-S", "-L", "--max-time", "30",
        "-X", method,
        "-H", f"Authorization: Bearer {token}",
        "-H", "Content-Type: application/json",
        "-H", f"Notion-Version: {NOTION_VERSION}",
    ]
    data_file = None
    try:
        if payload is not None:
            data_file = Path(f"/tmp/.longhun_notion_{os.getpid()}.json")
            data_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            args += ["-d", f"@{data_file}"]
        args.append(url)
        proc = subprocess.run(args, capture_output=True, timeout=35)
        text = proc.stdout.decode("utf-8", errors="replace")
        if proc.returncode != 0:
            return {"ok": False, "error": proc.stderr.decode("utf-8", errors="replace")[:500]}
        resp = json.loads(text)
        if "status" in resp and resp.get("status") >= 400:
            return {"ok": False, "status": resp["status"], "error": resp.get("message", text[:500])}
        return {"ok": True, "status": proc.returncode, "data": resp}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "curl timeout"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        if data_file and data_file.exists():
            data_file.unlink()


class LongHunNotionDashboard:
    """龍魂 Notion 公开仪表盘管理器"""

    def __init__(self, token: Optional[str] = None, parent_page_id: Optional[str] = None):
        self.token = token or os.environ.get("NOTION_TOKEN") or os.environ.get("LONGHUN_NOTION_TOKEN")
        self.parent_page_id = parent_page_id or os.environ.get("LONGHUN_NOTION_PARENT_PAGE")
        self.state = _load_state()

    def ready(self) -> bool:
        return bool(self.token and self.parent_page_id)

    def init_dashboard(self) -> Dict[str, Any]:
        if not self.ready():
            return {"ok": False, "reason": "缺少 NOTION_TOKEN 或 LONGHUN_NOTION_PARENT_PAGE"}

        # 创建仪表盘页面
        if not self.state.get("dashboard_page_id"):
            page = _api(
                self.token, "POST", "pages",
                {
                    "parent": {"page_id": self.parent_page_id},
                    "properties": {
                        "title": {"title": [{"text": {"content": "龍魂公开仪表盘"}}]}
                    },
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [
                                    {"type": "text", "text": {"content": "技术为人民服务 · 数据主权不可侵犯 · 祖国优先 · 龍魂公开透明窗口"}}
                                ]
                            },
                        },
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [
                                    {"type": "text", "text": {"content": f"DNA: {DNA}"}}
                                ]
                            },
                        },
                    ],
                },
            )
            if not page["ok"]:
                return page
            self.state["dashboard_page_id"] = page["data"]["id"]
            _save_state(self.state)

        dashboard_id = self.state["dashboard_page_id"]

        # 创建攻击地图数据库
        if not self.state.get("attack_db_id"):
            db = _api(
                self.token, "POST", "databases",
                {
                    "parent": {"page_id": dashboard_id},
                    "title": [{"type": "text", "text": {"content": "攻击地图"}}],
                    "properties": {
                        "事件": {"title": {}},
                        "时间": {"date": {}},
                        "类型": {"select": {"options": [
                            {"name": "下载威胁", "color": "red"},
                            {"name": "AI输出风险", "color": "orange"},
                            {"name": "权限异常", "color": "yellow"},
                            {"name": "系统审计", "color": "blue"},
                        ]}},
                        "来源": {"rich_text": {}},
                        "严重级别": {"select": {"options": [
                            {"name": "🔴", "color": "red"},
                            {"name": "🟡", "color": "yellow"},
                            {"name": "🟢", "color": "green"},
                        ]}},
                        "详情": {"rich_text": {}},
                        "DNA": {"rich_text": {}},
                    },
                },
            )
            if not db["ok"]:
                return db
            self.state["attack_db_id"] = db["data"]["id"]
            _save_state(self.state)

        # 创建审计登记数据库
        if not self.state.get("audit_db_id"):
            db = _api(
                self.token, "POST", "databases",
                {
                    "parent": {"page_id": dashboard_id},
                    "title": [{"type": "text", "text": {"content": "审计登记"}}],
                    "properties": {
                        "条目": {"title": {}},
                        "时间": {"date": {}},
                        "模块": {"select": {"options": [
                            {"name": "CNSH代码审计", "color": "purple"},
                            {"name": "龍魂护盾", "color": "red"},
                            {"name": "下载守卫", "color": "orange"},
                            {"name": "编辑器记忆", "color": "blue"},
                            {"name": "语法引擎", "color": "green"},
                        ]}},
                        "三色": {"select": {"options": [
                            {"name": "🟢", "color": "green"},
                            {"name": "🟡", "color": "yellow"},
                            {"name": "🔴", "color": "red"},
                        ]}},
                        "红灯": {"number": {}},
                        "黄灯": {"number": {}},
                        "绿灯": {"number": {}},
                        "摘要": {"rich_text": {}},
                        "DNA": {"rich_text": {}},
                    },
                },
            )
            if not db["ok"]:
                return db
            self.state["audit_db_id"] = db["data"]["id"]
            _save_state(self.state)

        # 创建 Timeline 数据库
        if not self.state.get("timeline_db_id"):
            db = _api(
                self.token, "POST", "databases",
                {
                    "parent": {"page_id": dashboard_id},
                    "title": [{"type": "text", "text": {"content": "Timeline"}}],
                    "properties": {
                        "事件": {"title": {}},
                        "时间": {"date": {}},
                        "窗口ID": {"rich_text": {}},
                        "DNA": {"rich_text": {}},
                        "输入摘要": {"rich_text": {}},
                        "输出摘要": {"rich_text": {}},
                    },
                },
            )
            if not db["ok"]:
                return db
            self.state["timeline_db_id"] = db["data"]["id"]
            _save_state(self.state)

        # 创建 LU 公开档案数据库（本地 → Notion → GitHub 的 Notion 层）
        if not self.state.get("lu_archive_db_id"):
            db = _api(
                self.token, "POST", "databases",
                {
                    "parent": {"page_id": dashboard_id},
                    "title": [{"type": "text", "text": {"content": "LU 公开档案"}}],
                    "properties": {
                        "标题": {"title": {}},
                        "DNA": {"rich_text": {}},
                        "标签": {"multi_select": {}},
                        "路径": {"rich_text": {}},
                        "来源": {"select": {"options": [
                            {"name": "CNSH卡片", "color": "purple"},
                            {"name": "审计报告", "color": "blue"},
                        ]}},
                        "同步时间": {"date": {}},
                    },
                },
            )
            if not db["ok"]:
                return db
            self.state["lu_archive_db_id"] = db["data"]["id"]
            _save_state(self.state)

        return {"ok": True, "state": self.state}

    def add_attack_event(
        self,
        title: str,
        event_type: str,
        source: str,
        severity: str,
        detail: str,
        dna: str = DNA,
    ) -> Dict[str, Any]:
        db_id = self.state.get("attack_db_id")
        if not self.ready() or not db_id:
            return {"ok": False, "reason": "仪表盘未初始化"}
        return _api(
            self.token, "POST", "pages",
            {
                "parent": {"database_id": db_id},
                "properties": {
                    "事件": {"title": [{"text": {"content": title}}]},
                    "时间": {"date": {"start": _now_iso()}},
                    "类型": {"select": {"name": event_type}},
                    "来源": {"rich_text": [{"text": {"content": source}}]},
                    "严重级别": {"select": {"name": severity}},
                    "详情": {"rich_text": [{"text": {"content": detail[:2000]}}]},
                    "DNA": {"rich_text": [{"text": {"content": dna}}]},
                },
            },
        )

    def add_audit_record(
        self,
        title: str,
        module: str,
        score: str,
        red: int,
        yellow: int,
        green: int,
        summary: str,
        dna: str = DNA,
    ) -> Dict[str, Any]:
        db_id = self.state.get("audit_db_id")
        if not self.ready() or not db_id:
            return {"ok": False, "reason": "仪表盘未初始化"}
        return _api(
            self.token, "POST", "pages",
            {
                "parent": {"database_id": db_id},
                "properties": {
                    "条目": {"title": [{"text": {"content": title}}]},
                    "时间": {"date": {"start": _now_iso()}},
                    "模块": {"select": {"name": module}},
                    "三色": {"select": {"name": score}},
                    "红灯": {"number": red},
                    "黄灯": {"number": yellow},
                    "绿灯": {"number": green},
                    "摘要": {"rich_text": [{"text": {"content": summary[:2000]}}]},
                    "DNA": {"rich_text": [{"text": {"content": dna}}]},
                },
            },
        )

    def add_timeline_event(
        self,
        window_id: str,
        title: str,
        input_summary: str,
        output_summary: str,
        dna: str = DNA,
    ) -> Dict[str, Any]:
        db_id = self.state.get("timeline_db_id")
        if not self.ready() or not db_id:
            return {"ok": False, "reason": "仪表盘未初始化"}
        return _api(
            self.token, "POST", "pages",
            {
                "parent": {"database_id": db_id},
                "properties": {
                    "事件": {"title": [{"text": {"content": title}}]},
                    "时间": {"date": {"start": _now_iso()}},
                    "窗口ID": {"rich_text": [{"text": {"content": window_id}}]},
                    "DNA": {"rich_text": [{"text": {"content": dna}}]},
                    "输入摘要": {"rich_text": [{"text": {"content": input_summary[:2000]}}]},
                    "输出摘要": {"rich_text": [{"text": {"content": output_summary[:2000]}}]},
                },
            },
        )

    def _query_database(self, db_id: str, property_name: str, value: str) -> List[Dict[str, Any]]:
        """按 rich_text 属性精确查询数据库中的页面。"""
        resp = _api(
            self.token, "POST", f"databases/{db_id}/query",
            {
                "filter": {
                    "property": property_name,
                    "rich_text": {"equals": value},
                },
                "page_size": 10,
            },
        )
        if not resp.get("ok"):
            return []
        return resp.get("data", {}).get("results", [])

    def add_or_update_page(
        self,
        title: str,
        dna: str,
        tags: List[str],
        path: str,
        source: str,
    ) -> Dict[str, Any]:
        """
        把本地 Markdown 档案同步到 Notion 的 LU 公开档案数据库。
        按 DNA 去重：已存在则更新，不存在则创建。
        """
        db_id = self.state.get("lu_archive_db_id")
        if not self.ready() or not db_id:
            return {"ok": False, "reason": "仪表盘未初始化"}

        existing = self._query_database(db_id, "DNA", dna)
        payload = {
            "parent": {"database_id": db_id},
            "properties": {
                "标题": {"title": [{"text": {"content": title}}]},
                "DNA": {"rich_text": [{"text": {"content": dna}}]},
                "标签": {"multi_select": [{"name": t} for t in tags]},
                "路径": {"rich_text": [{"text": {"content": path}}]},
                "来源": {"select": {"name": source}},
                "同步时间": {"date": {"start": _now_iso()}},
            },
        }

        if existing:
            page_id = existing[0]["id"]
            return _api(self.token, "PATCH", f"pages/{page_id}", payload)
        return _api(self.token, "POST", "pages", payload)


def main() -> int:
    dashboard = LongHunNotionDashboard()
    if not dashboard.ready():
        print("未配置 NOTION_TOKEN / LONGHUN_NOTION_PARENT_PAGE，跳过仪表盘初始化")
        print("示例：")
        print("  export NOTION_TOKEN=secret_xxx")
        print("  export LONGHUN_NOTION_PARENT_PAGE=6c03f9ad-afd9-4ce8-bf98-f8439eb9dbbf")
        return 0
    result = dashboard.init_dashboard()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
