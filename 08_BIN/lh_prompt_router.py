#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂提示词路由器 v1.0
动态路由 · 自我迭代 · 鲲鹏同步

DNA: #龍芯⚡️丙午·癸未·庚辰·壬午·䷑蛊-ROUTER-ENGINE-v1.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  1. 多路由配置管理 (YAML)
  2. 关键词/正则匹配
  3. 动态加载对应 System Prompt
  4. 自我学习：未匹配时记录，人工审核后自动添加新路由
  5. 与鲲鹏服务器双向同步
  6. 版本控制 + 回滚
  7. 完整日志和错误处理

用法:
  python lh_prompt_router.py --serve         # 启动API服务 (:9630)
  python lh_prompt_router.py --route "审计"   # 命令行路由测试
  python lh_prompt_router.py --sync          # 手动同步到鲲鹏
  python lh_prompt_router.py --learn         # 处理待学习记录
  python lh_prompt_router.py --status        # 查看状态
"""

import os, sys, json, re, hashlib, time, shutil, subprocess, argparse
import logging, threading
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field, asdict

# ============================================================
# 固定锚点
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
ROUTER_DIR = ROOT / "config" / "prompt_router"
CONFIG_FILE = ROUTER_DIR / "routes.yaml"
LEARN_FILE = ROUTER_DIR / "learn_queue.yaml"
BACKUP_DIR = ROUTER_DIR / "backups"
LOG_DIR = ROUTER_DIR / "logs"
SYNC_LOG = ROUTER_DIR / "sync_history.json"
ROUTER_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

KUNPENG_HOST = os.environ.get("KUNPENG_HOST", "119.13.90.27")
KUNPENG_USER = os.environ.get("KUNPENG_USER", "root")
KUNPENG_PATH = os.environ.get("KUNPENG_PATH", "/opt/longhun-system/config/prompt_router/")
KUNPENG_SSH_KEY = os.environ.get("KUNPENG_SSH_KEY", str(Path.home() / ".ssh" / "longhun_kunpeng_ed25519"))

DNA = "#龍芯⚡️丙午·癸未·庚辰·壬午·䷑蛊-ROUTER-ENGINE-v1.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
VERSION = "1.0.0"

# ============================================================
# 日志系统
# ============================================================

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / f"router_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("prompt_router")

logger = setup_logging()

# ============================================================
# 核心数据结构
# ============================================================

@dataclass
class Route:
    name: str
    triggers: list[str]
    patterns: list[str] = field(default_factory=list)
    system_prompt: str = ""
    tools: list[str] = field(default_factory=list)
    priority: int = 0
    enabled: bool = True
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Route":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class RouterConfig:
    version: str = VERSION
    default_prompt: str = "你是龍魂助手，处理通用问题。"
    routes: list = field(default_factory=list)
    learn_threshold: int = 3
    sync_interval: int = 3600

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "default_prompt": self.default_prompt,
            "routes": [r.to_dict() if isinstance(r, Route) else r for r in self.routes],
            "learn_threshold": self.learn_threshold,
            "sync_interval": self.sync_interval
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RouterConfig":
        config = cls(
            version=data.get("version", VERSION),
            default_prompt=data.get("default_prompt", "你是龍魂助手，处理通用问题。"),
            learn_threshold=data.get("learn_threshold", 3),
            sync_interval=data.get("sync_interval", 3600)
        )
        for r in data.get("routes", []):
            config.routes.append(Route.from_dict(r))
        return config

# ============================================================
# 配置管理器
# ============================================================

class ConfigManager:
    def __init__(self, config_path: Path = CONFIG_FILE):
        self.config_path = config_path
        self.config: Optional[RouterConfig] = None
        self._load()

    def _load(self):
        if not self.config_path.exists():
            self.config = RouterConfig()
            self._save()
            logger.info("✅ 创建默认配置文件")
        else:
            try:
                import yaml
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
                self.config = RouterConfig.from_dict(data)
                logger.info(f"✅ 加载配置: {len(self.config.routes)} 条路由")
            except Exception as e:
                logger.error(f"❌ 配置文件损坏: {e}")
                self.config = RouterConfig()
                self._save()

    def _save(self):
        import yaml
        self._backup()
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config.to_dict(), f, allow_unicode=True, default_flow_style=False)
        logger.info("💾 配置已保存")

    def _backup(self):
        if self.config_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = BACKUP_DIR / f"routes_{timestamp}.yaml"
            shutil.copy(self.config_path, backup_file)
            backups = sorted(BACKUP_DIR.glob("routes_*.yaml"))
            if len(backups) > 30:
                for old in backups[:-30]:
                    old.unlink()

    def reload(self):
        self._load()

    def get_route_by_name(self, name: str) -> Optional[Route]:
        for r in self.config.routes:
            if isinstance(r, Route) and r.name == name:
                return r
        return None

    def add_route(self, route: Route):
        existing = self.get_route_by_name(route.name)
        if existing:
            existing.triggers = route.triggers
            existing.patterns = route.patterns
            existing.system_prompt = route.system_prompt
            existing.tools = route.tools
            existing.priority = route.priority
            existing.enabled = route.enabled
            existing.updated_at = datetime.now().isoformat()
        else:
            self.config.routes.append(route)
        self._save()

    def remove_route(self, name: str):
        self.config.routes = [r for r in self.config.routes if (isinstance(r, Route) and r.name != name)]
        self._save()

    def enable_route(self, name: str, enable: bool = True):
        route = self.get_route_by_name(name)
        if route:
            route.enabled = enable
            route.updated_at = datetime.now().isoformat()
            self._save()

    def rollback(self, version: str | None = None):
        if version:
            backup_file = BACKUP_DIR / f"routes_{version}.yaml"
        else:
            backups = sorted(BACKUP_DIR.glob("routes_*.yaml"))
            if len(backups) < 2:
                logger.warning("没有可回滚的备份")
                return
            backup_file = backups[-2]
        if backup_file.exists():
            shutil.copy(backup_file, self.config_path)
            self._load()
            logger.info(f"⏪ 已回滚到: {backup_file.name}")

    def get_history(self) -> list[dict]:
        backups = sorted(BACKUP_DIR.glob("routes_*.yaml"))
        history = []
        for b in backups:
            stat = b.stat()
            history.append({
                "file": b.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        return history

# ============================================================
# 学习队列管理器
# ============================================================

class LearnManager:
    def __init__(self, learn_file: Path = LEARN_FILE):
        self.learn_file = learn_file
        self.queue = self._load()

    def _load(self) -> list[dict]:
        import yaml
        if not self.learn_file.exists():
            return []
        try:
            with open(self.learn_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or []
        except:
            return []

    def _save(self):
        import yaml
        with open(self.learn_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.queue, f, allow_unicode=True, default_flow_style=False)

    def record_unmatched(self, user_input: str, context: dict | None = None):
        entry = {
            "input": user_input,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "count": 1,
            "resolved": False
        }
        for item in self.queue:
            if item["input"] == user_input and not item.get("resolved", False):
                item["count"] += 1
                item["timestamp"] = datetime.now().isoformat()
                self._save()
                return
        self.queue.append(entry)
        self._save()

    def get_pending(self) -> list[dict]:
        pending = [item for item in self.queue if not item.get("resolved", False)]
        return sorted(pending, key=lambda x: x["count"], reverse=True)

    def mark_resolved(self, input_text: str, route_name: str):
        for item in self.queue:
            if item["input"] == input_text:
                item["resolved"] = True
                item["resolved_at"] = datetime.now().isoformat()
                item["route_name"] = route_name
                self._save()
                return

    def suggest_new_routes(self, threshold: int = 3) -> list[dict]:
        pending = self.get_pending()
        suggestions = []
        for item in pending:
            if item["count"] >= threshold:
                suggestions.append({
                    "input": item["input"],
                    "count": item["count"],
                    "suggested_triggers": self._extract_keywords(item["input"]),
                    "suggested_name": self._generate_name(item["input"])
                })
        return suggestions

    def _extract_keywords(self, text: str) -> list[str]:
        words = re.findall(r'[\u4e00-\u9fa5a-zA-Z]+', text)
        stopwords = {'的', '了', '是', '我', '你', '他', '她', '它', '们', '和', '与', '或', '但', '而', '因', '为', '以', '于'}
        return [w for w in words if len(w) >= 2 and w not in stopwords][:5]

    def _generate_name(self, text: str) -> str:
        keywords = self._extract_keywords(text)
        if keywords:
            return "_".join(keywords[:2]).lower()
        return "route_" + hashlib.md5(text.encode()).hexdigest()[:8]

# ============================================================
# 路由引擎核心
# ============================================================

class RouterEngine:
    def __init__(self, config_manager: ConfigManager, learn_manager: LearnManager):
        self.config_mgr = config_manager
        self.learn_mgr = learn_manager
        self.match_cache: dict[str, tuple[str, Optional[Route]]] = {}

    def route(self, user_input: str, context: dict | None = None) -> tuple[str, Optional[Route]]:
        context = context or {}
        cache_key = hashlib.md5((user_input + str(context)).encode()).hexdigest()
        if cache_key in self.match_cache:
            return self.match_cache[cache_key]

        sorted_routes = sorted(
            [r for r in self.config_mgr.config.routes if isinstance(r, Route) and r.enabled],
            key=lambda x: x.priority, reverse=True
        )

        matched_route = None
        for route in sorted_routes:
            for trigger in route.triggers:
                if trigger in user_input:
                    matched_route = route
                    break
            if matched_route:
                break
            for pattern in route.patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    matched_route = route
                    break
            if matched_route:
                break

        if not matched_route:
            self.learn_mgr.record_unmatched(user_input, context)
            result = (self.config_mgr.config.default_prompt, None)
        else:
            result = (matched_route.system_prompt, matched_route)

        self.match_cache[cache_key] = result
        return result

    def clear_cache(self):
        self.match_cache.clear()

    def get_route_names(self) -> list[str]:
        return [r.name for r in self.config_mgr.config.routes if isinstance(r, Route)]

    def stats(self) -> dict:
        routes = [r for r in self.config_mgr.config.routes if isinstance(r, Route)]
        enabled = sum(1 for r in routes if r.enabled)
        pending = len(self.learn_mgr.get_pending())
        return {
            "total_routes": len(routes),
            "enabled_routes": enabled,
            "pending_learn": pending,
            "cache_size": len(self.match_cache)
        }

# ============================================================
# 同步管理器
# ============================================================

class SyncManager:
    def __init__(self, local_dir: Path = ROUTER_DIR):
        self.local_dir = local_dir
        self.host = KUNPENG_HOST
        self.user = KUNPENG_USER
        self.remote_path = KUNPENG_PATH
        self.ssh_key = KUNPENG_SSH_KEY
        self.history_file = SYNC_LOG
        self._load_history()

    def _load_history(self):
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        else:
            self.history = []

    def _save_history(self, entry: dict):
        self.history.append(entry)
        if len(self.history) > 100:
            self.history = self.history[-100:]
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def sync_to_kunpeng(self) -> bool:
        try:
            result = subprocess.run([
                "rsync", "-avz", "-e", f"ssh -i {self.ssh_key}", "--delete",
                str(self.local_dir) + "/",
                f"{self.user}@{self.host}:{self.remote_path}"
            ], capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                logger.info(f"✅ 同步成功到鲲鹏: {self.host}:{self.remote_path}")
                self._save_history({"time": datetime.now().isoformat(), "status": "success", "host": self.host})
                return True
            else:
                logger.error(f"❌ 同步失败: {result.stderr}")
                self._save_history({"time": datetime.now().isoformat(), "status": "failed", "error": result.stderr[:200]})
                return False
        except Exception as e:
            logger.error(f"❌ 同步异常: {e}")
            return False

    def sync_from_kunpeng(self) -> bool:
        try:
            result = subprocess.run([
                "rsync", "-avz", "-e", f"ssh -i {self.ssh_key}", "--delete",
                f"{self.user}@{self.host}:{self.remote_path}/",
                str(self.local_dir) + "/"
            ], capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                logger.info(f"✅ 从鲲鹏拉取成功: {self.host}")
                return True
            else:
                logger.error(f"❌ 拉取失败: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ 拉取异常: {e}")
            return False

    def get_history(self) -> list[dict]:
        return self.history

# ============================================================
# 路由器服务
# ============================================================

class RouterService:
    def __init__(self):
        self.config_mgr = ConfigManager()
        self.learn_mgr = LearnManager()
        self.engine = RouterEngine(self.config_mgr, self.learn_mgr)
        self.sync_mgr = SyncManager()
        self.running = False
        self.auto_sync_thread: threading.Thread | None = None

    def route(self, user_input: str, context: dict | None = None) -> dict:
        prompt, route = self.engine.route(user_input, context)
        return {
            "system_prompt": prompt,
            "route": route.to_dict() if route else None,
            "matched": route is not None,
            "timestamp": datetime.now().isoformat()
        }

    def add_route(self, name: str, triggers: list[str], system_prompt: str,
                  patterns: list[str] | None = None, tools: list[str] | None = None,
                  priority: int = 0) -> dict:
        route = Route(
            name=name, triggers=triggers,
            patterns=patterns or [], system_prompt=system_prompt,
            tools=tools or [], priority=priority, enabled=True
        )
        self.config_mgr.add_route(route)
        self.engine.clear_cache()
        return {"status": "success", "name": name}

    def remove_route(self, name: str) -> dict:
        self.config_mgr.remove_route(name)
        self.engine.clear_cache()
        return {"status": "success", "name": name}

    def learn_suggestions(self, threshold: int | None = None) -> list[dict]:
        threshold = threshold or self.config_mgr.config.learn_threshold
        return self.learn_mgr.suggest_new_routes(threshold)

    def apply_suggestion(self, suggestion: dict) -> dict:
        name = suggestion.get("suggested_name", "")
        triggers = suggestion.get("suggested_triggers", [])
        input_text = suggestion.get("input", "")
        prompt = f"你是龍魂助手，专门处理『{input_text}』相关的问题。请根据用户输入提供专业、清晰的回答。"
        self.add_route(name=name, triggers=triggers, system_prompt=prompt, priority=5)
        self.learn_mgr.mark_resolved(input_text, name)
        return {"status": "success", "name": name, "triggers": triggers}

    def sync(self, direction: str = "to") -> bool:
        if direction == "to":
            return self.sync_mgr.sync_to_kunpeng()
        else:
            return self.sync_mgr.sync_from_kunpeng()

    def start_auto_sync(self, interval: int = 3600):
        if self.running:
            logger.warning("服务已在运行")
            return
        self.running = True
        def sync_loop():
            while self.running:
                time.sleep(interval)
                if self.running:
                    logger.info("⏰ 自动同步触发")
                    self.sync(direction="to")
        self.auto_sync_thread = threading.Thread(target=sync_loop, daemon=True)
        self.auto_sync_thread.start()
        logger.info(f"🔄 自动同步已启动 (间隔 {interval}秒)")

    def stop(self):
        self.running = False
        if self.auto_sync_thread:
            self.auto_sync_thread.join(timeout=5)

    def stats(self) -> dict:
        return {
            "router": self.engine.stats(),
            "config_version": self.config_mgr.config.version,
            "sync_history": self.sync_mgr.get_history()[-5:],
            "backups": len(list(BACKUP_DIR.glob("routes_*.yaml")))
        }

# ============================================================
# API服务
# ============================================================

def run_api_server(port: int = 9630, host: str = "0.0.0.0"):
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel
        import uvicorn
    except ImportError:
        logger.error("请安装 fastapi 和 uvicorn: pip install fastapi uvicorn")
        return

    app = FastAPI(title="龍魂提示词路由器", version=VERSION)
    service = RouterService()

    class RouteRequest(BaseModel):
        input: str
        context: dict | None = None

    class AddRouteRequest(BaseModel):
        name: str
        triggers: list[str]
        system_prompt: str
        patterns: list[str] | None = []
        tools: list[str] | None = []
        priority: int = 0

    @app.get("/health")
    def health():
        return {"status": "ok", "version": VERSION, "dna": DNA}

    @app.post("/route")
    def route(req: RouteRequest):
        return {"code": 0, "data": service.route(req.input, req.context)}

    @app.post("/route/add")
    def add_route(req: AddRouteRequest):
        result = service.add_route(req.name, req.triggers, req.system_prompt, req.patterns, req.tools, req.priority)
        return {"code": 0, "data": result}

    @app.delete("/route/{name}")
    def delete_route(name: str):
        return {"code": 0, "data": service.remove_route(name)}

    @app.get("/learn/suggestions")
    def get_suggestions():
        return {"code": 0, "data": service.learn_suggestions()}

    @app.post("/learn/apply")
    def apply_suggestion(suggestion: dict):
        return {"code": 0, "data": service.apply_suggestion(suggestion)}

    @app.post("/sync/to")
    def sync_to():
        ok = service.sync(direction="to")
        return {"code": 0 if ok else 1, "data": {"success": ok}}

    @app.post("/sync/from")
    def sync_from():
        ok = service.sync(direction="from")
        return {"code": 0 if ok else 1, "data": {"success": ok}}

    @app.get("/stats")
    def get_stats():
        return {"code": 0, "data": service.stats()}

    @app.get("/backups")
    def get_backups():
        return {"code": 0, "data": service.config_mgr.get_history()}

    logger.info(f"🚀 API服务启动: http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

# ============================================================
# 命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂提示词路由器 v1.0",
        epilog="示例: lh --prompt-router --route '审计'"
    )
    parser.add_argument("--route", type=str, help="测试路由匹配（输入文本）")
    parser.add_argument("--context", type=str, help="上下文JSON（可选）")
    parser.add_argument("--serve", action="store_true", help="启动API服务")
    parser.add_argument("--port", type=int, default=9630, help="API端口")
    parser.add_argument("--sync", action="store_true", help="同步到鲲鹏")
    parser.add_argument("--sync-from", action="store_true", help="从鲲鹏拉取")
    parser.add_argument("--learn", action="store_true", help="查看学习建议")
    parser.add_argument("--apply-learn", type=str, help="应用学习建议")
    parser.add_argument("--add-route", action="store_true", help="交互式添加路由")
    parser.add_argument("--list", action="store_true", help="列出所有路由")
    parser.add_argument("--status", action="store_true", help="显示状态")
    parser.add_argument("--rollback", type=str, help="回滚到指定备份")
    parser.add_argument("--info", action="store_true", help="显示版本信息")

    args = parser.parse_args()

    if args.info:
        print(f"""
🐉 龍魂提示词路由器 v{VERSION}
DNA: {DNA}
CONFIRM: {CONFIRM}
配置: {CONFIG_FILE}
用法:
  lh --prompt-router --route "审计协议"
  lh --prompt-router --serve --port 9630
  lh --prompt-router --sync
  lh --prompt-router --learn
  lh --prompt-router --status
""")
        return

    service = RouterService()

    if args.serve:
        run_api_server(port=args.port)
        return

    if args.sync:
        ok = service.sync(direction="to")
        print("✅ 同步成功" if ok else "❌ 同步失败")
        return

    if args.sync_from:
        ok = service.sync(direction="from")
        print("✅ 拉取成功" if ok else "❌ 拉取失败")
        return

    if args.learn:
        suggestions = service.learn_suggestions()
        if suggestions:
            print("\n📚 学习建议 (高频未匹配输入):")
            for s in suggestions:
                print(f"  - '{s['input']}' (出现{s['count']}次) → 建议路由名: {s['suggested_name']}")
                print(f"    候选触发词: {', '.join(s['suggested_triggers'])}")
        else:
            print("✅ 暂无学习建议")
        return

    if args.apply_learn:
        suggestions = service.learn_suggestions()
        for s in suggestions:
            if s["input"] == args.apply_learn:
                result = service.apply_suggestion(s)
                print(f"✅ 已应用: {result['name']}")
                return
        print("❌ 未找到匹配的待处理记录")
        return

    if args.add_route:
        print("🐉 交互式添加路由")
        name = input("路由名称: ").strip()
        triggers = [t.strip() for t in input("触发词（逗号分隔）: ").split(",") if t.strip()]
        system_prompt = input("System Prompt: ").strip()
        priority = int(input("优先级 (0-10): ").strip() or "0")
        result = service.add_route(name, triggers, system_prompt, priority=priority)
        print(f"✅ 添加成功: {result['name']}")
        return

    if args.list:
        routes = [r for r in service.config_mgr.config.routes if isinstance(r, Route)]
        print(f"\n📋 当前路由列表 ({len(routes)}条):")
        for r in routes:
            status = "✅" if r.enabled else "⛔"
            print(f"  {status} {r.name} (优先级{r.priority}) -> {r.triggers[:3]}")
        return

    if args.rollback:
        service.config_mgr.rollback(args.rollback)
        print(f"⏪ 已回滚到: {args.rollback}")
        return

    if args.status:
        stats = service.stats()
        print("\n📊 路由器状态:")
        print(f"  总路由数: {stats['router']['total_routes']}")
        print(f"  已启用: {stats['router']['enabled_routes']}")
        print(f"  待学习记录: {stats['router']['pending_learn']}")
        print(f"  缓存大小: {stats['router']['cache_size']}")
        print(f"  配置版本: {stats['config_version']}")
        print(f"  备份数量: {stats['backups']}")
        if stats['sync_history']:
            last_sync = stats['sync_history'][-1]
            print(f"  最近同步: {last_sync['time']} ({last_sync['status']})")
        return

    if args.route:
        context = json.loads(args.context) if args.context else {}
        result = service.route(args.route, context)
        print("\n🐉 路由结果:")
        print(f"  输入: {args.route}")
        print(f"  匹配: {'✅' if result['matched'] else '❌'}")
        if result['route']:
            print(f"  路由: {result['route']['name']}")
            print(f"  触发词: {', '.join(result['route']['triggers'])}")
        print(f"  System Prompt:\n{result['system_prompt'][:200]}...")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
