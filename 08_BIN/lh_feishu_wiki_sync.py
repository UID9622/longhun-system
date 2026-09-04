# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-3b5ff4f0
#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂·飞书知识库同步引擎 v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用途: 自动同步本地 Markdown → 飞书知识库（Wiki），取代 Notion
新增: 守护模式·多目录并行·反向链接·增量同步·launchd集成

DNA: #龍芯⚡️丙午·丙申·癸丑·亥时·䷗复-FEISHU-WIKI-SYNC-v2.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import os
import sys
import json
import time
import hashlib
import signal
import argparse
import urllib.request
import urllib.error
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# ─── 配置 ───────────────────────────────────────────────────
CST = timezone(timedelta(hours=8))
API_BASE = "https://open.feishu.cn/open-apis"
CONFIG_DIR = Path.home() / ".longhun" / "config"
FEISHU_CONFIG = CONFIG_DIR / "feishu_wiki.json"
SYNC_TARGETS_CONFIG = CONFIG_DIR / "feishu_wiki_targets.json"
STATE_FILE = Path.home() / ".longhun" / "data" / "feishu_wiki_state.json"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30
USER_AGENT = "LongHun-Feishu-Wiki-Sync/2.0 (UID9622; +https://uid9622.cn)"

DNA = "#龍芯⚡️丙午·丙申·癸丑·亥时·䷗复-FEISHU-WIKI-SYNC-v2.0"
OFFICIAL_DOMAIN = "https://uid9622.cn"
AUTHOR = "诸葛鑫（UID9622）"

# ─── 反向链接模板 ───────────────────────────────────────────

BACKLINK_FOOTER = """
---

> 📚 **本文档由[龍魂系统]({domain})自动同步至飞书知识库**
> 🧬 DNA: {dna}
> 👤 创建者: {author}
> 🔗 官方原文: {domain}
> 📜 协议: CC BY-NC-SA 4.0 + MulanPSL v2
> ⚠️ 飞书为镜像副本，最新版本以[官方网]({domain})为准
"""


def inject_backlink(content: str, file_rel_path: str = "") -> str:
    """在文档末尾注入反向链接。"""
    backlink = BACKLINK_FOOTER.format(
        domain=OFFICIAL_DOMAIN.replace("\n", ""),
        dna=DNA.replace("\n", ""),
        author=AUTHOR.replace("\n", ""),
    )
    # 检查是否已有反向链接
    if "本文档由龍魂系统自动同步" in content:
        return content
    return content.rstrip() + "\n" + backlink


# ─── 飞书 API 客户端 ───────────────────────────────────────

class FeishuClient:
    """飞书开放平台 API 客户端。"""

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self._token: Optional[str] = None
        self._token_expires: float = 0

    def _get_token(self) -> str:
        if self._token and time.time() < self._token_expires - 60:
            return self._token

        url = f"{API_BASE}/auth/v3/tenant_access_token/internal"
        data = json.dumps({
            "app_id": self.app_id,
            "app_secret": self.app_secret,
        }).encode("utf-8")

        for attempt in range(MAX_RETRIES):
            try:
                req = urllib.request.Request(
                    url, data=data, method="POST",
                    headers={"Content-Type": "application/json; charset=utf-8"},
                )
                with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                    result = json.loads(resp.read())
                if result.get("code") == 0:
                    self._token = result["tenant_access_token"]
                    self._token_expires = time.time() + result.get("expire", 7200)
                    return self._token
                else:
                    raise RuntimeError(f"飞书认证失败: code={result.get('code')} msg={result.get('msg')}")
            except (urllib.error.URLError, urllib.error.HTTPError) as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise RuntimeError(f"飞书 API 不可达: {e}")

        raise RuntimeError("无法获取飞书 token")

    def _request(self, method: str, path: str, body: Optional[Dict] = None,
                 query: Optional[Dict] = None) -> Dict:
        token = self._get_token()
        url = f"{API_BASE}{path}"
        if query:
            import urllib.parse
            params = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in query.items())
            url += f"?{params}"

        data = json.dumps(body).encode("utf-8") if body else None
        req = urllib.request.Request(
            url, data=data, method=method,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": USER_AGENT,
            },
        )

        for attempt in range(MAX_RETRIES):
            try:
                with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                    result = json.loads(resp.read())
                if result.get("code") != 0:
                    raise RuntimeError(f"API 错误 [{path}]: code={result.get('code')} msg={result.get('msg')}")
                return result
            except (urllib.error.URLError, urllib.error.HTTPError) as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise RuntimeError(f"API 请求失败 [{path}]: {e}")

    # ── Wiki Space ──

    def list_spaces(self) -> List[Dict]:
        result = self._request("GET", "/wiki/v2/spaces")
        return result.get("data", {}).get("items", [])

    def create_space(self, name: str, description: str = "") -> Dict:
        body = {"name": name}
        if description:
            body["description"] = description
        result = self._request("POST", "/wiki/v2/spaces", body=body)
        return result.get("data", {}).get("space", {})

    def get_space_info(self, space_id: str) -> Dict:
        result = self._request("GET", f"/wiki/v2/spaces/{space_id}")
        return result.get("data", {}).get("space", {})

    # ── Wiki Node ──

    def list_nodes(self, space_id: str, parent_node_token: Optional[str] = None) -> List[Dict]:
        query = {}
        if parent_node_token:
            query["parent_node_token"] = parent_node_token
        result = self._request("GET", f"/wiki/v2/spaces/{space_id}/nodes", query=query)
        return result.get("data", {}).get("items", [])

    def create_node(self, space_id: str, parent_node_token: str,
                    node_type: str, title: str, content: str = "") -> Dict:
        body = {
            "node_type": node_type,
            "title": title,
        }
        if parent_node_token:
            body["parent_node_token"] = parent_node_token

        result = self._request("POST", f"/wiki/v2/spaces/{space_id}/nodes", body=body)
        node = result.get("data", {}).get("node", {})

        if content and node.get("node_token"):
            self._update_node_content(node["node_token"], title, content)

        return node

    def get_node_info(self, node_token: str) -> Dict:
        result = self._request("GET", f"/wiki/v2/spaces/get_node?token={node_token}")
        return result.get("data", {}).get("node", {})

    def _update_node_content(self, node_token: str, title: str, content: str):
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(content)
            tmp_path = f.name

        try:
            file_token = self._upload_file(tmp_path, "markdown")
            self._import_to_doc(file_token, node_token, title)
        finally:
            os.unlink(tmp_path)

    def _upload_file(self, filepath: str, file_type: str) -> str:
        import uuid
        token = self._get_token()

        file_size = os.path.getsize(filepath)
        file_name = os.path.basename(filepath)

        boundary = f"----FormBoundary{uuid.uuid4().hex[:16]}"
        body = f'--{boundary}\r\nContent-Disposition: form-data; name="file_name"\r\n\r\n{file_name}\r\n'
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="parent_type"\r\n\r\nexplorer\r\n'
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="parent_node"\r\n\r\n\r\n'
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="size"\r\n\r\n{file_size}\r\n'
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{file_name}"\r\nContent-Type: application/octet-stream\r\n\r\n'

        with open(filepath, "rb") as f:
            file_data = f.read()

        body_bytes = body.encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

        req = urllib.request.Request(
            f"{API_BASE}/drive/v1/files/upload_all",
            data=body_bytes, method="POST",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )

        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())

        if result.get("code") != 0:
            raise RuntimeError(f"文件上传失败: {result.get('msg')}")

        return result["data"]["file_token"]

    def _import_to_doc(self, file_token: str, node_token: str, title: str):
        body = {
            "file_extension": "md",
            "file_token": file_token,
            "type": "docx",
            "file_name": f"{title}.md",
            "point": {
                "type": "node",
                "node_token": node_token,
            }
        }

        result = self._request("POST", "/drive/v1/import_tasks", body=body)
        ticket = result.get("data", {}).get("ticket", "")

        for _ in range(30):
            time.sleep(1)
            query_result = self._request("GET", f"/drive/v1/import_tasks/{ticket}")
            job_status = query_result.get("data", {}).get("result", {}).get("job_status", "")
            if job_status == 0:
                return
            elif job_status == 1:
                continue
            elif job_status == 2:
                raise RuntimeError(f"导入失败: {query_result.get('data', {}).get('result', {})}")
        raise RuntimeError("导入超时")


# ─── 同步引擎 v2.0 ──────────────────────────────────────────

class WikiSyncEngine:
    """飛书知识库同步引擎 v2.0。"""

    def __init__(self, client: FeishuClient):
        self.client = client
        self.state: Dict = {}
        self._running = False
        self._stats: Dict = {"total_success": 0, "total_fail": 0, "total_skip": 0, "rounds": 0}

    def load_state(self):
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        if STATE_FILE.exists():
            self.state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        else:
            self.state = {"spaces": {}, "synced_files": {}, "last_sync": None}

    def save_state(self):
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.state["last_sync"] = datetime.now(CST).isoformat()
        STATE_FILE.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")

    def ensure_space(self, name: str, description: str = "") -> str:
        for sid, info in self.state.get("spaces", {}).items():
            if info.get("name") == name:
                return sid

        spaces = self.client.list_spaces()
        for s in spaces:
            if s.get("name") == name:
                self.state.setdefault("spaces", {})[s["space_id"]] = {
                    "name": name, "description": s.get("description", ""),
                }
                self.save_state()
                return s["space_id"]

        print(f"  创建知识库空间: {name}")
        space = self.client.create_space(name, description)
        space_id = space.get("space_id", "")
        if space_id:
            self.state.setdefault("spaces", {})[space_id] = {
                "name": name, "description": description,
            }
            self.save_state()
            print(f"  ✅ 空间创建成功: {space_id}")
        return space_id

    def ensure_folder(self, space_id: str, parent_token: str, folder_name: str) -> str:
        nodes = self.client.list_nodes(space_id, parent_token)
        for n in nodes:
            if n.get("title") == folder_name and n.get("node_type") == "origin":
                return n["node_token"]

        print(f"    创建文件夹: {folder_name}")
        try:
            node = self.client.create_node(space_id, parent_token, "origin", folder_name)
            return node.get("node_token", "")
        except Exception as e:
            print(f"    ⚠️ 创建文件夹失败: {e}")
            return ""

    def sync_file(self, space_id: str, parent_token: str,
                  filepath: Path, title: str = None, inject_link: bool = True) -> bool:
        """同步单个 MD 文件到飞书知识库（含反向链接）。"""
        if not filepath.exists():
            print(f"  ❌ 文件不存在: {filepath}")
            return False

        content = filepath.read_text(encoding="utf-8")

        # 注入反向链接
        if inject_link:
            rel_path = str(filepath)
            content = inject_backlink(content, rel_path)

        file_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        file_key = str(filepath)

        if not title:
            title = filepath.stem.replace("-", " ").replace("_", " ").strip()
            first_line = content.strip().split("\n")[0]
            if first_line.startswith("# "):
                title = first_line[2:].strip()[:80]

        # 去重：未变化跳过
        synced = self.state.get("synced_files", {}).get(file_key, {})
        if synced.get("hash") == file_hash and synced.get("space_id") == space_id:
            node_token = synced.get("node_token", "")
            if node_token:
                return "skip"

        print(f"  📤 同步: {title}")
        node = self.client.create_node(space_id, parent_token, "origin", title, content)
        node_token = node.get("node_token", "")

        self.state.setdefault("synced_files", {})[file_key] = {
            "title": title,
            "hash": file_hash,
            "space_id": space_id,
            "node_token": node_token,
            "synced_at": datetime.now(CST).isoformat(),
        }
        self.save_state()

        if node_token:
            print(f"  ✅ 同步成功: {title}")
            return "success"
        else:
            print(f"  ❌ 同步失败: {title}")
            return "fail"

    def sync_directory(self, dirpath: Path, space_name: str = "龍魂知识库") -> Dict:
        """同步整个目录到飞书知识库。"""
        print(f"\n📚 同步目录: {dirpath}")
        print(f"   目标空间: {space_name}")

        space_id = self.ensure_space(space_name, f"龍魂系统·自动同步·{dirpath.name}")
        if not space_id:
            print("  ❌ 无法创建/获取知识库空间")
            return {"success": 0, "fail": 0, "skip": 0}

        space_info = self.client.get_space_info(space_id)
        root_token = space_info.get("root_node_token", "")

        stats = {"success": 0, "fail": 0, "skip": 0}
        self._sync_dir_recursive(dirpath, space_id, root_token, stats)
        return stats

    def _sync_dir_recursive(self, dirpath: Path, space_id: str,
                            parent_token: str, stats: Dict):
        items = sorted(dirpath.iterdir(), key=lambda x: (x.is_file(), x.name))

        for item in items:
            if item.name.startswith(".") or item.name.startswith("_"):
                continue
            if item.name.endswith(".asc"):
                continue

            if item.is_file() and item.suffix in (".md", ".markdown"):
                result = self.sync_file(space_id, parent_token, item)
                if result == "success":
                    stats["success"] += 1
                elif result == "fail":
                    stats["fail"] += 1
                else:
                    stats["skip"] += 1

            elif item.is_dir():
                folder_token = self.ensure_folder(space_id, parent_token, item.name)
                if folder_token:
                    self._sync_dir_recursive(item, space_id, folder_token, stats)

    def sync_all_targets(self, targets: List[Dict]) -> Dict:
        """同步所有配置的目标目录。"""
        grand_stats = {"success": 0, "fail": 0, "skip": 0}

        for t in targets:
            path = Path(t["path"]).expanduser().resolve()
            space = t.get("space", "龍魂知识库")

            if not path.exists():
                print(f"⚠️ 路径不存在，跳过: {path}")
                continue

            if path.is_file():
                space_id = self.ensure_space(space)
                if space_id:
                    space_info = self.client.get_space_info(space_id)
                    root_token = space_info.get("root_node_token", "")
                    result = self.sync_file(space_id, root_token, path)
                    if result == "success":
                        grand_stats["success"] += 1
                    elif result == "fail":
                        grand_stats["fail"] += 1
                    else:
                        grand_stats["skip"] += 1
            else:
                stats = self.sync_directory(path, space)
                for k in grand_stats:
                    grand_stats[k] += stats.get(k, 0)

        return grand_stats

    def daemon_loop(self, targets: List[Dict], interval: int = 3600):
        """守护进程模式：按间隔自动同步。"""
        self._running = True
        print(f"\n🐉 龍魂·飞书知识库自动同步守护启动")
        print(f"   DNA: {DNA}")
        print(f"   同步目标: {len(targets)} 个")
        for t in targets:
            print(f"     • {t['path']} → {t.get('space', '龍魂知识库')}")
        print(f"   同步间隔: {interval}秒 ({interval//60}分钟)")
        print(f"   🟢 守护运行中... (Ctrl+C 停止)\n")

        def _handle_signal(sig, frame):
            print("\n⚠️ 收到停止信号，完成当前轮次后退出...")
            self._running = False

        signal.signal(signal.SIGINT, _handle_signal)
        signal.signal(signal.SIGTERM, _handle_signal)

        while self._running:
            self._stats["rounds"] += 1
            round_num = self._stats["rounds"]
            now = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n{'='*60}")
            print(f"🔄 第 {round_num} 轮同步 [{now}]")
            print(f"{'='*60}")

            try:
                stats = self.sync_all_targets(targets)
                for k in stats:
                    self._stats[f"total_{k}"] += stats[k]
                print(f"📊 本轮: 成功 {stats['success']} · 失败 {stats['fail']} · 跳过 {stats['skip']}")
                print(f"📊 累计: 成功 {self._stats['total_success']} · 失败 {self._stats['total_fail']} · 跳过 {self._stats['total_skip']}")
            except Exception as e:
                print(f"❌ 本轮同步异常: {e}")
                self._stats["total_fail"] += 1

            # 等待下一轮
            if self._running:
                next_run = datetime.now(CST) + timedelta(seconds=interval)
                print(f"⏰ 下一轮: {next_run.strftime('%H:%M:%S')} (等待 {interval}秒...)")
                for _ in range(min(interval, 60)):
                    if not self._running:
                        break
                    time.sleep(1)
                # 剩余时间用大间隔
                remaining = interval - 60
                if remaining > 0 and self._running:
                    time.sleep(min(remaining, 300))
                    if remaining > 300 and self._running:
                        time.sleep(remaining - 300)

        print("\n👋 守护已停止")

    def status(self, targets: List[Dict] = None) -> None:
        """显示同步状态。"""
        print(f"\n📊 飞书知识库同步状态")
        print(f"   DNA: {DNA}")
        print(f"   最后同步: {self.state.get('last_sync', '从未')}")
        print(f"\n   知识库空间: {len(self.state.get('spaces', {}))} 个")
        for sid, info in self.state.get("spaces", {}).items():
            print(f"     • {info['name']} ({sid[:16]}...)")

        synced = self.state.get("synced_files", {})
        print(f"\n   已同步文件: {len(synced)} 个")
        for fkey, info in list(synced.items())[:15]:
            mark = "🟢" if info.get("hash") else "🟡"
            print(f"     {mark} {info['title']} ({info.get('synced_at', '?')[:16]})")
        if len(synced) > 15:
            print(f"     ... 还有 {len(synced) - 15} 个")

        if targets:
            print(f"\n   同步目标配置:")
            for t in targets:
                print(f"     • {t['path']} → {t.get('space', '龍魂知识库')} [{'启用' if t.get('enabled', True) else '暂停'}]")


# ─── 配置管理 ───────────────────────────────────────────────

DEFAULT_SYNC_TARGETS = [
    {
        "path": "~/longhun-system/articles",
        "space": "龍魂·文章",
        "enabled": True,
    },
    {
        "path": "~/longhun-system/01_protocols",
        "space": "龍魂·协议规范",
        "enabled": True,
    },
    {
        "path": "~/longhun-system/11_DATA/learning",
        "space": "龍魂·学习资料",
        "enabled": True,
    },
    {
        "path": "~/longhun-system/11_DATA/knowledge",
        "space": "龍魂·知识库",
        "enabled": True,
    },
    {
        "path": "~/longhun-system/papers",
        "space": "龍魂·论文",
        "enabled": True,
    },
    {
        "path": "~/longhun-system/10_PORTAL/knowledge",
        "space": "龍魂·知识门户",
        "enabled": True,
    },
    {
        "path": "~/longhun-system/10_PORTAL/knowledge-matrix",
        "space": "龍魂·知识门户",
        "enabled": True,
    },
]


def load_config() -> Tuple[str, str]:
    """加载飞书配置。"""
    app_id = os.environ.get("FEISHU_APP_ID", "")
    app_secret = os.environ.get("FEISHU_APP_SECRET", "")

    if not app_id and FEISHU_CONFIG.exists():
        cfg = json.loads(FEISHU_CONFIG.read_text(encoding="utf-8"))
        app_id = cfg.get("app_id", "")
        app_secret = cfg.get("app_secret", "")

    if not app_id or not app_secret:
        print("❌ 飞书 App 凭证未配置！")
        print()
        print("配置方法：")
        print(f"  lh wiki config --app-id cli_xxx --app-secret xxx")
        print()
        print("获取凭证：")
        print("  1. 打开 https://open.feishu.cn/app")
        print("  2. 找到龍魂系统应用 → 「凭证与基础信息」")
        print("  3. 复制 App ID 和 App Secret")
        print("  4. 飞书客户端：知识库 → 设置 → 添加应用为管理员")
        print()
        sys.exit(1)

    return app_id, app_secret


def load_sync_targets() -> List[Dict]:
    """加载同步目标配置。"""
    if SYNC_TARGETS_CONFIG.exists():
        targets = json.loads(SYNC_TARGETS_CONFIG.read_text(encoding="utf-8"))
        # 过滤禁用的
        return [t for t in targets if t.get("enabled", True)]
    # 首次运行，生成默认配置
    SYNC_TARGETS_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    SYNC_TARGETS_CONFIG.write_text(
        json.dumps(DEFAULT_SYNC_TARGETS, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"📝 已生成默认同步目标配置: {SYNC_TARGETS_CONFIG}")
    print(f"   包含 {len(DEFAULT_SYNC_TARGETS)} 个目标目录")
    return [t for t in DEFAULT_SYNC_TARGETS if t.get("enabled", True)]


# ─── CLI ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·飞书知识库同步引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐉 龍魂·飞书Wiki同步引擎 v2.0

示例:
  lh wiki sync                          # 同步所有配置的目标目录
  lh wiki sync 11_DATA/learning/        # 同步单个目录
  lh wiki sync articles/ --space "龍魂文章"
  lh wiki auto                          # 启动守护·每1小时自动同步
  lh wiki auto --interval 1800          # 每30分钟自动同步
  lh wiki status                        # 查看同步状态
  lh wiki targets                       # 查看/编辑同步目标
  lh wiki config                        # 配置飞书凭证

反向链接: 每个同步文档末尾自动注入 uid9622.cn 官方链接
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """.strip(),
    )
    sub = parser.add_subparsers(dest="command", help="命令")

    # sync
    p_sync = sub.add_parser("sync", help="同步目录到飞书知识库")
    p_sync.add_argument("path", nargs="?", default=None, help="要同步的目录/文件路径（留空=同步全部目标）")
    p_sync.add_argument("--space", default="龍魂知识库", help="知识库空间名称")
    p_sync.add_argument("--no-backlink", action="store_true", help="不注入反向链接")

    # auto - 守护模式
    p_auto = sub.add_parser("auto", help="启动自动同步守护进程")
    p_auto.add_argument("--interval", type=int, default=3600, help="同步间隔（秒），默认3600=1小时")
    p_auto.add_argument("--once", action="store_true", help="只跑一次（不循环）")

    # status
    sub.add_parser("status", help="查看同步状态")

    # targets
    p_targets = sub.add_parser("targets", help="管理同步目标")
    p_targets.add_argument("action", nargs="?", default="list",
                           choices=["list", "add", "remove", "enable", "disable", "reset"],
                           help="list/add/remove/enable/disable/reset")
    p_targets.add_argument("--path", help="目标路径")
    p_targets.add_argument("--space", help="知识库空间名")

    # config
    p_config = sub.add_parser("config", help="配置飞书凭证")
    p_config.add_argument("--app-id", help="飞书 App ID")
    p_config.add_argument("--app-secret", help="飞书 App Secret")

    args = parser.parse_args()

    # config 不需要凭证
    if args.command == "config":
        FEISHU_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        cfg = {}
        if FEISHU_CONFIG.exists():
            cfg = json.loads(FEISHU_CONFIG.read_text(encoding="utf-8"))

        if args.app_id:
            cfg["app_id"] = args.app_id
        if args.app_secret:
            cfg["app_secret"] = args.app_secret

        FEISHU_CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 配置已保存到 {FEISHU_CONFIG}")
        return

    # targets 管理不需要凭证
    if args.command == "targets":
        if args.action == "list":
            targets = load_sync_targets() if SYNC_TARGETS_CONFIG.exists() else []
            all_targets = json.loads(SYNC_TARGETS_CONFIG.read_text(encoding="utf-8")) if SYNC_TARGETS_CONFIG.exists() else DEFAULT_SYNC_TARGETS
            print(f"\n📋 同步目标配置 ({len(all_targets)} 个)")
            print(f"   配置文件: {SYNC_TARGETS_CONFIG}")
            print()
            for i, t in enumerate(all_targets):
                status = "🟢 启用" if t.get("enabled", True) else "🟡 暂停"
                print(f"  [{i}] {status} {t['path']} → {t.get('space', '龍魂知识库')}")
            return

        elif args.action == "reset":
            SYNC_TARGETS_CONFIG.write_text(
                json.dumps(DEFAULT_SYNC_TARGETS, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            print(f"✅ 已重置为默认配置 ({len(DEFAULT_SYNC_TARGETS)} 个目标)")
            return

        elif args.action == "add" and args.path:
            targets = json.loads(SYNC_TARGETS_CONFIG.read_text(encoding="utf-8")) if SYNC_TARGETS_CONFIG.exists() else DEFAULT_SYNC_TARGETS
            targets.append({
                "path": args.path,
                "space": args.space or "龍魂知识库",
                "enabled": True,
            })
            SYNC_TARGETS_CONFIG.write_text(json.dumps(targets, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"✅ 已添加: {args.path} → {args.space or '龍魂知识库'}")
            return

        elif args.action == "remove" and args.path:
            targets = json.loads(SYNC_TARGETS_CONFIG.read_text(encoding="utf-8")) if SYNC_TARGETS_CONFIG.exists() else []
            targets = [t for t in targets if t["path"] != args.path]
            SYNC_TARGETS_CONFIG.write_text(json.dumps(targets, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"✅ 已移除: {args.path}")
            return

        elif args.action in ("enable", "disable") and args.path:
            targets = json.loads(SYNC_TARGETS_CONFIG.read_text(encoding="utf-8")) if SYNC_TARGETS_CONFIG.exists() else []
            for t in targets:
                if t["path"] == args.path:
                    t["enabled"] = (args.action == "enable")
            SYNC_TARGETS_CONFIG.write_text(json.dumps(targets, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"✅ 已{'启用' if args.action == 'enable' else '暂停'}: {args.path}")
            return

        parser.print_help()
        return

    # 需要凭证的命令
    app_id, app_secret = load_config()
    client = FeishuClient(app_id, app_secret)
    engine = WikiSyncEngine(client)
    engine.load_state()

    if args.command == "status":
        targets = load_sync_targets() if SYNC_TARGETS_CONFIG.exists() else []
        engine.status(targets)
        return

    if args.command == "auto":
        targets = load_sync_targets()
        if not targets:
            print("⚠️ 没有启用的同步目标，请先配置: lh wiki targets")
            return

        if args.once:
            print("🔄 单次全量同步...")
            stats = engine.sync_all_targets(targets)
            print(f"\n📊 同步完成: 成功 {stats['success']} · 失败 {stats['fail']} · 跳过 {stats['skip']}")
        else:
            engine.daemon_loop(targets, args.interval)
        return

    if args.command == "sync":
        if args.path:
            target = Path(args.path).expanduser().resolve()
            if not target.exists():
                print(f"❌ 路径不存在: {args.path}")
                sys.exit(1)

            if target.is_file():
                space_id = engine.ensure_space(args.space)
                if space_id:
                    space_info = client.get_space_info(space_id)
                    root_token = space_info.get("root_node_token", "")
                    result = engine.sync_file(space_id, root_token, target,
                                              inject_link=not args.no_backlink)
                    print(f"\n📊 结果: {result}")
            else:
                stats = engine.sync_directory(target, args.space)
                print(f"\n📊 同步完成: 成功 {stats['success']} · 失败 {stats['fail']} · 跳过 {stats['skip']}")
        else:
            # 无参数 = 同步全部目标
            targets = load_sync_targets()
            if not targets:
                print("⚠️ 没有启用的同步目标。运行 lh wiki targets 查看配置")
                return
            print(f"🔄 全量同步 {len(targets)} 个目标目录...")
            stats = engine.sync_all_targets(targets)
            print(f"\n📊 全量同步完成: 成功 {stats['success']} · 失败 {stats['fail']} · 跳过 {stats['skip']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
