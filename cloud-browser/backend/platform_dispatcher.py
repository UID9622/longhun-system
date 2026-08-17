# -*- coding: utf-8 -*-
"""
🐉 龍魂·云浏览器 平台调度器 v2.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时-☰乾-PLATFORM-DISPATCHER-v2.0-BUILD
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2

功能: 把自然语言指令解析为「平台 × 动作 × 目标」计划
  - parse_platforms("在CSDN发布文章") → ["csdn"]
  - parse_action → "publish"
  - dispatch → [PlatformAction(...)]
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

try:
    import yaml
except ImportError:  # 缺 yaml 时降级空配置（服务不崩）
    yaml = None


@dataclass
class PlatformAction:
    """平台动作"""
    platform: str
    platform_name: str
    action: str
    target: str
    url: str
    params: Dict[str, Any] = field(default_factory=dict)


class PlatformDispatcher:
    """平台指令调度器"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or str(Path(__file__).parent / "platforms.yaml")
        self.platforms = self._load_config()
        self._build_routing_table()
        self._build_action_map()

    def _load_config(self) -> Dict[str, Any]:
        if yaml is None or not os.path.exists(self.config_path):
            return {"platforms": {}}
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {"platforms": {}}

    def _build_routing_table(self):
        """关键词路由表：平台名 + 别名 + 描述词"""
        self.routing_table: Dict[str, Dict[str, Any]] = {}
        self.platform_list: List[str] = []
        for key, platform in self.platforms.get("platforms", {}).items():
            keywords = [platform.get("name", "").lower()]
            for alias in platform.get("aliases", []):
                keywords.append(str(alias).lower())
            for word in str(platform.get("description", "")).split():
                if len(word) > 2:
                    keywords.append(word.lower())
            self.routing_table[key] = {
                "keywords": keywords,
                "platform": key,
                "name": platform.get("name", key),
                "url": platform.get("url", ""),
                "category": platform.get("category", "other"),
                "actions": platform.get("actions", []),
                "login_required": platform.get("login_required", True),
            }
            self.platform_list.append(key)

    def _build_action_map(self):
        self.action_map = {
            "发布": "publish", "群发": "mass_send", "同步": "sync",
            "推送": "push", "提交": "submit", "管理": "manage",
            "查看": "view", "查询": "query", "搜索": "search",
            "发送": "send", "创建": "create", "编辑": "edit",
            "删除": "delete", "调用": "call", "触发": "trigger",
            "监控": "monitor", "上传": "upload", "下载": "download",
            "评论": "comment", "转发": "repost", "收藏": "collect",
            "点赞": "like", "关注": "follow", "登录": "login",
            "开通": "open_service", "充值": "recharge",
        }

    def parse_platforms(self, command: str) -> List[str]:
        """从指令中解析目标平台（长关键词优先消歧：『微信公众号』优先于『微信』）"""
        cmd = command.lower()
        hits = []  # (平台key, 关键词, 关键词长度)
        for key, info in self.routing_table.items():
            for kw in info["keywords"]:
                if kw and kw in cmd:
                    hits.append((key, kw))
        hits.sort(key=lambda h: len(h[1]), reverse=True)
        matched: List[str] = []
        for key, kw in hits:
            if key in matched:
                continue
            # 短关键词已被已入选平台的更长关键词包含 → 泛化命中，跳过
            owned = {h[1] for h in hits if h[0] in matched}
            if any(kw in hk and kw != hk for hk in owned):
                continue
            matched.append(key)
        return matched

    def parse_action(self, command: str) -> str:
        cmd = command.lower()
        for key, value in self.action_map.items():
            if key in cmd:
                return value
        return "view"  # 默认查看

    def extract_target(self, command: str) -> str:
        """提取目标内容：优先引号内，其次『这个/那个』后，最后整句截断"""
        m = re.search(r'["\'\u201c\u201d]([^"\'\u201c\u201d]+)["\'\u201c\u201d]', command)
        if m:
            return m.group(1).strip()
        m = re.search(r"(这个|那个|以下|如下|内容)[：:]?\s*(.+)", command)
        if m:
            return m.group(2).strip()[:200]
        return command[:200]

    def dispatch(self, command: str) -> List[PlatformAction]:
        """解析指令 → 平台动作计划"""
        platforms = self.parse_platforms(command)
        if not platforms:
            # 无平台关键词：含搜索意图 → 百度；否则视为通用浏览
            if any(k in command for k in ["搜索", "查一下", "搜一下", "找一下", "帮我查"]):
                platforms = ["baidu"]
            else:
                platforms = []

        action_type = self.parse_action(command)
        target = self.extract_target(command)

        actions = []
        for key in platforms:
            info = self.routing_table.get(key, {})
            actions.append(PlatformAction(
                platform=key,
                platform_name=info.get("name", key),
                action=action_type,
                target=target,
                url=info.get("url", ""),
                params={"full_command": command},
            ))
        return actions

    def list_platforms(self) -> List[Dict[str, Any]]:
        result = []
        for key, info in self.routing_table.items():
            result.append({
                "id": key,
                "name": info["name"],
                "category": info.get("category", "other"),
                "url": info["url"],
                "actions": info.get("actions", []),
                "login_required": info.get("login_required", True),
            })
        return sorted(result, key=lambda x: (x["category"], x["name"]))

    def get_platform(self, platform_id: str) -> Optional[Dict[str, Any]]:
        info = self.routing_table.get(platform_id)
        if info:
            return {
                "id": platform_id,
                "name": info["name"],
                "url": info["url"],
                "category": info.get("category", "other"),
                "actions": info.get("actions", []),
            }
        return None


if __name__ == "__main__":
    d = PlatformDispatcher()
    print(f"平台总数: {len(d.list_platforms())}")
    for c in ["在CSDN发布文章", "同步代码到GitHub和Gitee", "查一下华为云服务器状态",
              "帮我在微信公众号发一篇文章", "搜索 龍魂系统", "打开阿里云开通短信服务"]:
        acts = d.dispatch(c)
        print(f"\n指令: {c}")
        for a in acts:
            print(f"  → {a.platform_name} [{a.action}] 目标: {a.target[:30]} url: {a.url}")
