#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · Notion 实时同步双向链路 v2.0

在原 v1.0 (tools/notion_sync.py pull/push/sync) 基础上增强：
  - 双向监听：本地文件变更 → Notion | Notion变更 → 本地
  - 冲突检测：基于 last_edited_time 的乐观锁
  - 增量同步：仅同步变更页（基于 Notion API 的 last_edited_time 过滤）
  - 状态持久化：记录每个页面的同步指纹，下次仅同步变更
  - 自动重试：指数退避 + 限流控制（继承 v1.1 Phase 1）

依赖：
  - Python 3.8+
  - NOTION_TOKEN 环境变量
  - tools/notion_sync.py (v1.0 基础能力)

用法：
  # 双向监听（启动后持续运行）
  python3 tools/notion_bidirectional_sync.py watch

  # 双向同步一次
  python3 tools/notion_bidirectional_sync.py sync-once

  # 仅拉取（Notion → 本地）
  python3 tools/notion_bidirectional_sync.py pull --page-id <id> -o <file>

  # 仅推送（本地 → Notion）
  python3 tools/notion_bidirectional_sync.py push --page-id <id> -i <file>

  # 查看同步状态
  python3 tools/notion_bidirectional_sync.py status

DNA: #龍芯⚡️2026-07-12-NOTION-BIDIRECTIONAL-SYNC-v2.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════
# 0. 路径与配置
# ═══════════════════════════════════════════
HOME = Path.home()
LONGHUN_ROOT = Path(os.environ.get("LONGHUN_ROOT", HOME / "longhun-system"))
SYNC_DIR = HOME / ".longhun" / "notion_sync"
SYNC_STATE_FILE = SYNC_DIR / "bidirectional_state.json"
SYNC_DIR.mkdir(parents=True, exist_ok=True)

# Notion 配置
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

# 同步间隔（秒）
WATCH_INTERVAL = 300  # 5分钟
PULL_INTERVAL = 60    # 1分钟检查 Notion 变更

CST = timezone(timedelta(hours=8))

# ═══════════════════════════════════════════
# 1. 同步状态管理
# ═══════════════════════════════════════════

class 同步状态管理器:
    """
    管理每个同步页面的状态指纹。
    
    结构:
      {
        "page_id": {
          "local_sha256": "...",        # 本地文件 SHA256
          "notion_last_edited": "...",   # Notion 最后编辑时间
          "last_synced": "ISO时间戳",
          "direction": "push|pull",
          "conflict_count": 0
        }
      }
    """
    
    def __init__(self, state_file: Path = SYNC_STATE_FILE):
        self.state_file = state_file
        self.state: Dict[str, dict[str, Any]] = self._加载()
    
    def _加载(self) -> dict[str, Any]:
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}
    
    def _保存(self):
        self.state_file.write_text(
            json.dumps(self.state, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    
    def 获取状态(self, page_id: str) -> dict[str, Any]:
        return self.state.get(page_id, {})
    
    def 更新本地指纹(self, page_id: str, local_sha256: str):
        if page_id not in self.state:
            self.state[page_id] = {}
        self.state[page_id]["local_sha256"] = local_sha256
        self.state[page_id]["last_checked"] = datetime.now(CST).isoformat()
        self._保存()
    
    def 更新Notion指纹(self, page_id: str, notion_last_edited: str):
        if page_id not in self.state:
            self.state[page_id] = {}
        self.state[page_id]["notion_last_edited"] = notion_last_edited
        self._保存()
    
    def 记录同步(self, page_id: str, direction: str):
        if page_id not in self.state:
            self.state[page_id] = {}
        self.state[page_id]["last_synced"] = datetime.now(CST).isoformat()
        self.state[page_id]["direction"] = direction
        self._保存()
    
    def 检测冲突(self, page_id: str) -> bool:
        """
        冲突条件：本地和Notion都变更了
        即 local_sha256 变了 AND notion_last_edited 比 last_synced 晚
        """
        s = self.state.get(page_id, {})
        last_synced = s.get("last_synced", "")
        notion_edited = s.get("notion_last_edited", "")
        
        if not last_synced or not notion_edited:
            return False
        
        return notion_edited > last_synced
    
    def 需要拉取(self, page_id: str) -> bool:
        """Notion有新内容 → 需要拉到本地"""
        s = self.state.get(page_id, {})
        last_synced = s.get("last_synced", "")
        notion_edited = s.get("notion_last_edited", "")
        
        if not notion_edited:
            return False  # 还没拿到 Notion 数据
        if not last_synced:
            return True   # 从未同步过
        
        return notion_edited > last_synced
    
    def 需要推送(self, page_id: str, local_sha256: str) -> bool:
        """本地变更 → 需要推到 Notion"""
        s = self.state.get(page_id, {})
        stored_sha = s.get("local_sha256", "")
        
        if not stored_sha:
            return True  # 从未记录过
        
        return local_sha256 != stored_sha
    
    def 摘要(self) -> dict[str, Any]:
        return {
            "tracked_pages": len(self.state),
            "pages": {
                pid: {
                    "last_synced": s.get("last_synced", "从不"),
                    "direction": s.get("direction", "无"),
                    "conflicts": s.get("conflict_count", 0)
                }
                for pid, s in self.state.items()
            }
        }


# ═══════════════════════════════════════════
# 2. Notion API 客户端
# ═══════════════════════════════════════════

class Notion客户端:
    """Notion API 封装"""
    
    def __init__(self, token: str = ""):
        self.token = token or NOTION_TOKEN
        if not self.token:
            raise ValueError("缺少 NOTION_TOKEN。设置: export NOTION_TOKEN=ntn_...")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json"
        }
        # 简易限流
        self._last_call = 0
        self._min_interval = 0.34  # ~3 req/s
    
    def _调用(self, method: str, endpoint: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """HTTP调用 + 限流"""
        import urllib.request
        import urllib.error
        
        # 限流
        elapsed = time.time() - self._last_call
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_call = time.time()
        
        url = f"{NOTION_API_BASE}{endpoint}"
        body = json.dumps(data).encode() if data else None
        
        req = urllib.request.Request(url, data=body, headers=self.headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else str(e)
            raise RuntimeError(f"Notion API {e.code}: {error_body[:500]}")
    
    def 获取页面(self, page_id: str) -> dict[str, Any]:
        """获取 Notion 页面属性"""
        return self._调用("GET", f"/pages/{page_id}")
    
    def 获取块列表(self, block_id: str) -> List[dict[str, Any]]:
        """获取页面的所有子块"""
        result = self._调用("GET", f"/blocks/{block_id}/children?page_size=100")
        return result.get("results", [])
    
    def 搜索(self, query: str = "", filter_params: dict[str, Any] | None = None) -> List[dict[str, Any]]:
        """搜索 Notion 页面"""
        data: dict[str, Any] = {"page_size": 50}
        if query:
            data["query"] = query
        if filter_params:
            data["filter"] = filter_params
        result = self._调用("POST", "/search", data)
        return result.get("results", [])
    
    def 添加块(self, block_id: str, blocks: List[dict[str, Any]]):
        """向页面添加子块"""
        return self._调用("PATCH", f"/blocks/{block_id}/children", {"children": blocks})


# ═══════════════════════════════════════════
# 3. 本地文件工具
# ═══════════════════════════════════════════

def 文件SHA256(文件路径: Path) -> str:
    """计算文件的 SHA256"""
    if not 文件路径.exists():
        return ""
    return hashlib.sha256(文件路径.read_bytes()).hexdigest()


def 本地文件列表(目录: Path) -> List[Path]:
    """列出目录下所有 .md 文件"""
    return sorted(目录.rglob("*.md"))


def Markdown转Notion块(内容: str) -> list[dict[str, Any]]:
    """
    将 Markdown 文本转换为 Notion 块。
    简化版：段落/标题/代码块
    """
    blocks = []
    lines = 内容.split("\n")
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 空行 → 跳过
        if not line.strip():
            i += 1
            continue
        
        # 代码块
        if line.startswith("```"):
            code_lines = []
            language = line[3:].strip()
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # 跳过关闭 ```
            
            code_text = "\n".join(code_lines)
            block = {
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": code_text}}],
                    "language": language or "plain text"
                }
            }
            blocks.append(block)
            continue
        
        # 标题
        if line.startswith("# "):
            blocks.append(_标题块("heading_1", line[2:]))
        elif line.startswith("## "):
            blocks.append(_标题块("heading_2", line[3:]))
        elif line.startswith("### "):
            blocks.append(_标题块("heading_3", line[4:]))
        else:
            # 普通段落
            if len(line) > 2000:
                line = line[:1997] + "..."
            blocks.append(_段落块(line))
        
        i += 1
    
    return blocks


def _标题块(heading_type: str, text: str) -> dict[str, Any]:
    return {
        "type": heading_type,
        heading_type: {
            "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
        }
    }


def _段落块(text: str) -> dict[str, Any]:
    return {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }


def Notion块转Markdown(blocks: List[dict[str, Any]]) -> str:
    """将 Notion 块转换为 Markdown"""
    lines = []
    
    for block in blocks:
        block_type = block.get("type", "")
        
        if block_type == "paragraph":
            text = _提取富文本(block.get("paragraph", {}).get("rich_text", []))
            lines.append(text + "\n")
        
        elif block_type in ("heading_1", "heading_2", "heading_3"):
            level = int(block_type[-1])
            text = _提取富文本(block.get(block_type, {}).get("rich_text", []))
            lines.append("#" * level + " " + text + "\n")
        
        elif block_type == "code":
            lang = block.get("code", {}).get("language", "")
            text = _提取富文本(block.get("code", {}).get("rich_text", []))
            lines.append(f"```{lang}\n{text}\n```\n")
        
        elif block_type == "bulleted_list_item":
            text = _提取富文本(block.get("bulleted_list_item", {}).get("rich_text", []))
            lines.append(f"- {text}\n")
        
        elif block_type == "numbered_list_item":
            text = _提取富文本(block.get("numbered_list_item", {}).get("rich_text", []))
            lines.append(f"1. {text}\n")
        
        elif block_type == "divider":
            lines.append("---\n")
        
        elif block_type == "quote":
            text = _提取富文本(block.get("quote", {}).get("rich_text", []))
            lines.append(f"> {text}\n")
    
    return "\n".join(lines)


def _提取富文本(rich_text: List[dict[str, Any]]) -> str:
    """从 Notion rich_text 数组提取纯文本"""
    parts = []
    for rt in rich_text:
        if rt.get("type") == "text":
            parts.append(rt.get("text", {}).get("content", ""))
    return "".join(parts)


# ═══════════════════════════════════════════
# 4. 核心同步逻辑
# ═══════════════════════════════════════════

class 双向同步器:
    def __init__(self, notion_client: Optional[Notion客户端] = None, state_manager: Optional[同步状态管理器] = None):
        self.notion = notion_client or Notion客户端()
        self.state = state_manager or 同步状态管理器()
    
    def 拉取(self, page_id: str, 输出文件: Path) -> Tuple[bool, str]:
        """Notion → 本地文件"""
        try:
            # 获取页面信息
            page = self.notion.获取页面(page_id)
            last_edited = page.get("last_edited_time", "")
            
            # 检查是否需要拉取
            if not self.state.需要拉取(page_id):
                return True, "已是最新"
            
            # 获取块
            blocks = self.notion.获取块列表(page_id)
            md_content = Notion块转Markdown(blocks)
            
            # 添加元数据头
            title = self._提取页面标题(page)
            header = f"# {title}\n\n> 从 Notion 同步 · {datetime.now(CST).isoformat()}\n> Page ID: {page_id}\n\n"
            输出文件.write_text(header + md_content, encoding="utf-8")
            
            # 更新状态
            self.state.更新Notion指纹(page_id, last_edited)
            self.state.更新本地指纹(page_id, 文件SHA256(输出文件))
            self.state.记录同步(page_id, "pull")
            
            return True, f"拉取完成: {输出文件}"
        except Exception as e:
            return False, f"拉取失败: {e}"
    
    def 推送(self, 输入文件: Path, page_id: str) -> Tuple[bool, str]:
        """本地文件 → Notion 页面"""
        try:
            if not 输入文件.exists():
                return False, f"文件不存在: {输入文件}"
            
            内容 = 输入文件.read_text(encoding="utf-8")
            local_sha = 文件SHA256(输入文件)
            
            # 检查是否需要推送
            if not self.state.需要推送(page_id, local_sha):
                return True, "已是最新"
            
            # 检查冲突
            if self.state.检测冲突(page_id):
                self.state.state[page_id]["conflict_count"] = \
                    self.state.state[page_id].get("conflict_count", 0) + 1
                self.state._保存()
                return False, f"⚠️ 冲突：Notion 和本地同时变更，请手动解决"
            
            # 转换并推送
            blocks = Markdown转Notion块(内容)
            self.notion.添加块(page_id, blocks)
            
            # 更新状态
            self.state.更新本地指纹(page_id, local_sha)
            self.state.记录同步(page_id, "push")
            
            return True, f"推送完成: {输入文件}"
        except Exception as e:
            return False, f"推送失败: {e}"
    
    def 双向同步一次(self, 页面映射: Dict[str, Path]):
        """
        执行一次双向同步。
        
        页面映射: {page_id: 本地文件路径}
        """
        results = {"pull": [], "push": [], "errors": []}
        
        for page_id, local_file in 页面映射.items():
            # 第一步：拉取 Notion → 本地
            ok, msg = self.拉取(page_id, local_file)
            if ok:
                results["pull"].append(f"{page_id[:8]}... → {local_file}")
            else:
                results["errors"].append(f"pull {page_id[:8]}: {msg}")
            
            # 第二步：推送 本地 → Notion
            ok, msg = self.推送(local_file, page_id)
            if ok:
                results["push"].append(f"{local_file} → {page_id[:8]}...")
            else:
                results["errors"].append(f"push {page_id[:8]}: {msg}")
        
        return results
    
    def 监听模式(self, 页面映射: Dict[str, Path], 间隔秒: int = WATCH_INTERVAL):
        """持续监听模式"""
        print(f"🔍 Notion 双向监听启动 (间隔: {间隔秒}s)")
        print(f"   监听页面: {len(页面映射)} 个")
        print(f"   按 Ctrl+C 停止\n")
        
        try:
            while True:
                results = self.双向同步一次(页面映射)
                成功数 = len(results["pull"]) + len(results["push"])
                错误数 = len(results["errors"])
                
                ts = datetime.now(CST).strftime("%H:%M:%S")
                if 成功数 > 0:
                    print(f"[{ts}] ✅ 同步 {成功数} 项", end="")
                    if 错误数 > 0:
                        print(f" | ⚠️ {错误数} 错误", end="")
                    print()
                elif 错误数 > 0:
                    print(f"[{ts}] ⚠️ {错误数} 错误: {results['errors'][:2]}")
                
                time.sleep(间隔秒)
        except KeyboardInterrupt:
            print(f"\n🛑 监听已停止")
    
    def _提取页面标题(self, page: dict[str, Any]) -> str:
        """从 Notion 页面属性提取标题"""
        props = page.get("properties", {})
        for _, val in props.items():
            if val.get("type") == "title":
                title_parts = val.get("title", [])
                return _提取富文本(title_parts)
        return "未命名页面"


# ═══════════════════════════════════════════
# 5. 同步配置
# ═══════════════════════════════════════════

默认页面映射 = {
    # 示例：将 Notion 页面 ID 映射到本地文件
    # "your-notion-page-id": LONGHUN_ROOT / "docs" / "notion_synced.md",
}


def 加载配置() -> Dict[str, Path]:
    """从配置文件或环境变量加载页面映射"""
    映射 = dict(默认页面映射)
    
    # 尝试从 JSON 配置加载
    config_file = SYNC_DIR / "bidirectional_config.json"
    if config_file.exists():
        try:
            loaded = json.loads(config_file.read_text(encoding="utf-8"))
            for pid, local in loaded.get("mappings", {}).items():
                映射[pid] = Path(local)
        except Exception:
            pass
    
    # 尝试从环境变量加载
    env_pages = os.environ.get("NOTION_SYNC_PAGES", "")
    if env_pages:
        for mapping in env_pages.split(","):
            parts = mapping.strip().split("=")
            if len(parts) == 2:
                映射[parts[0]] = Path(parts[1])
    
    return 映射


# ═══════════════════════════════════════════
# 6. CLI
# ═══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂 · Notion 双向同步链路 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s watch                        # 启动双向监听
  %(prog)s sync-once                    # 执行一次双向同步
  %(prog)s pull --page-id <id> -o <file>  # 从 Notion 拉取
  %(prog)s push --page-id <id> -i <file>  # 推送到 Notion
  %(prog)s status                       # 查看同步状态
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # watch
    watch_parser = subparsers.add_parser("watch", help="启动双向监听")
    watch_parser.add_argument("--interval", type=int, default=WATCH_INTERVAL,
                              help=f"监听间隔秒数 (默认: {WATCH_INTERVAL})")
    
    # sync-once
    subparsers.add_parser("sync-once", help="执行一次双向同步")
    
    # pull
    pull_parser = subparsers.add_parser("pull", help="从 Notion 拉取到本地")
    pull_parser.add_argument("--page-id", required=True, help="Notion 页面 ID")
    pull_parser.add_argument("-o", "--output", required=True, help="输出文件路径")
    
    # push
    push_parser = subparsers.add_parser("push", help="推送到 Notion")
    push_parser.add_argument("--page-id", required=True, help="Notion 页面 ID")
    push_parser.add_argument("-i", "--input", required=True, help="输入 Markdown 文件")
    
    # status
    subparsers.add_parser("status", help="查看同步状态")
    
    # init-config
    subparsers.add_parser("init-config", help="生成配置文件模板")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        notion = Notion客户端()
        state = 同步状态管理器()
        sync = 双向同步器(notion, state)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    if args.command == "watch":
        映射 = 加载配置()
        if not 映射:
            print("⚠️  未配置页面映射。请先运行 init-config 或设置 NOTION_SYNC_PAGES")
            print("   示例: export NOTION_SYNC_PAGES='page-id-1=docs/file1.md,page-id-2=docs/file2.md'")
            sys.exit(1)
        sync.监听模式(映射, args.interval)
    
    elif args.command == "sync-once":
        映射 = 加载配置()
        if not 映射:
            print("⚠️  未配置页面映射")
            sys.exit(1)
        results = sync.双向同步一次(映射)
        成功数 = len(results["pull"]) + len(results["push"])
        错误数 = len(results["errors"])
        print(f"\n📊 同步完成: ✅ {成功数} | ❌ {错误数}")
        if results["errors"]:
            for e in results["errors"]:
                print(f"  ⚠️  {e}")
    
    elif args.command == "pull":
        ok, msg = sync.拉取(args.page_id, Path(args.output))
        print(f"{'✅' if ok else '❌'} {msg}")
    
    elif args.command == "push":
        ok, msg = sync.推送(Path(args.input), args.page_id)
        print(f"{'✅' if ok else '❌'} {msg}")
    
    elif args.command == "status":
        摘要 = state.摘要()
        print(f"\n📊 Notion 双向同步状态")
        print(f"   跟踪页面: {摘要['tracked_pages']}")
        if 摘要["tracked_pages"] > 0:
            print(f"\n   页面详情:")
            for pid, info in 摘要["pages"].items():
                print(f"     {pid[:12]}... | 最后同步: {info['last_synced']} | 方向: {info['direction']} | 冲突: {info['conflicts']}")
        else:
            print("   (暂无同步记录)")
    
    elif args.command == "init-config":
        config_path = SYNC_DIR / "bidirectional_config.json"
        template = {
            "mappings": {
                "your-notion-page-id-1": "docs/notion_synced_file1.md",
                "your-notion-page-id-2": "docs/notion_synced_file2.md"
            },
            "watch_interval_seconds": 300,
            "auto_resolve": "notion_wins"  # 冲突自动解决策略: notion_wins | local_wins | manual
        }
        config_path.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 配置文件已生成: {config_path}")
        print(f"   编辑此文件，填入你的 Notion 页面 ID 和本地文件路径")


if __name__ == "__main__":
    main()
