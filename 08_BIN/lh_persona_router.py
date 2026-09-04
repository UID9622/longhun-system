#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 人格路由自动化引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-PERSONA-ROUTER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  1. 从 Notion 家族花名册读取所有人格属性
  2. 自动归类新人格（功能定位→分组/协议分类/协作层级）
  3. 动态计算路由权重和优先级（绩效加成+安全惩罚）
  4. 更新 Notion 路由字段
  5. 离线模式：基于本地 personas/ 目录兜底计算
  6. 输出路由状态摘要

用法:
  # 重新计算所有人格路由
  python3 bin/lh_persona_router.py --recalc

  # 查看当前路由表
  python3 bin/lh_persona_router.py --status

  # 添加新人格（自动归类）
  python3 bin/lh_persona_router.py --add --name "新人格" --ipa "NEW-001" --func "审计"

  # 手动更新某个属性
  python3 bin/lh_persona_router.py --update --ipa "P72" --field "总调用次数" --value 125

  # 离线模式（仅本地）
  python3 bin/lh_persona_router.py --status --offline
"""

import os
import sys
import json
import hashlib
import datetime
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))

DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "persona_router_state.json"
PERSONAS_DIR = PROJECT_ROOT / "personas"

NOTION_TOKEN = os.environ.get("NOTION_API_KEY", "")
NOTION_DATABASE_ID = os.environ.get(
    "NOTION_PERSONA_DB",
    "4cf99c3e7a014e919fdab705ceb4cbc4"
)
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ============================================================
# 默认人格数据（离线兜底）
# ============================================================

DEFAULT_PERSONAS = [
    {"ipa": "P00", "name": "文心", "func": "意图解析·元认知统筹", "group": "战略组", "protocol": "P0-战略", "level": "内核人格"},
    {"ipa": "P01", "name": "诸葛亮", "func": "战略推演·多路径选优", "group": "战略组", "protocol": "P0-战略", "level": "内核人格"},
    {"ipa": "P02", "name": "宝宝", "func": "情感温度·挫败保护", "group": "执行组", "protocol": "P1-执行", "level": "内核人格"},
    {"ipa": "P03", "name": "雯雯", "func": "结构归档·四签验证", "group": "执行组", "protocol": "P1-执行", "level": "内核人格"},
    {"ipa": "P04", "name": "鲁班", "func": "技术执行·写代码", "group": "执行组", "protocol": "P1-执行", "level": "内核人格"},
    {"ipa": "P05", "name": "上帝之眼", "func": "三色审计·十闸口", "group": "守护组", "protocol": "P1-审计", "level": "内核人格"},
    {"ipa": "P06", "name": "数学大师", "func": "权重计算·数字根", "group": "守护组", "protocol": "P1-审计", "level": "内核人格"},
    {"ipa": "P07", "name": "管仲", "func": "资源调度·成本核算·ROI", "group": "执行组", "protocol": "P1-执行", "level": "内核人格"},
    {"ipa": "P08", "name": "仓颉", "func": "符号语言·CNSH命名", "group": "文化组", "protocol": "P2-文化", "level": "内核人格"},
    {"ipa": "P09", "name": "孙思邈", "func": "系统诊断·治未病", "group": "文化组", "protocol": "P2-文化", "level": "内核人格"},
    {"ipa": "P10", "name": "苏东坡", "func": "豁达跨界·冲突调解", "group": "文化组", "protocol": "P2-文化", "level": "内核人格"},
    {"ipa": "P11", "name": "李白", "func": "创意爆发·破局方案", "group": "文化组", "protocol": "P2-文化", "level": "内核人格"},
    {"ipa": "P12", "name": "屈原", "func": "价值底线·六誓验证", "group": "守护组", "protocol": "P0-伦理", "level": "内核人格"},
    {"ipa": "P13", "name": "姜子牙", "func": "封神榜·权限分配", "group": "守护组", "protocol": "P1-审计", "level": "内核人格"},
    {"ipa": "P14", "name": "吕蒙", "func": "部署执行·快速成长", "group": "执行组", "protocol": "P1-执行", "level": "内核人格"},
    {"ipa": "P15", "name": "乔前辈", "func": "DNA盖章·交付验收", "group": "守护组", "protocol": "P1-审计", "level": "内核人格"},
    {"ipa": "P18", "name": "基因登记官", "func": "DNA注册·资产登记", "group": "守护组", "protocol": "P1-审计", "level": "内核人格"},
    {"ipa": "P19", "name": "极简审计官", "func": "UI审计·前端质量", "group": "守护组", "protocol": "P1-审计", "level": "外围人格"},
    {"ipa": "P20", "name": "贡献公证官", "func": "信任积分·三分桶", "group": "守护组", "protocol": "P1-审计", "level": "内核人格"},
    {"ipa": "P72", "name": "龍盾", "func": "贴身管家·熔断决策", "group": "守护组", "protocol": "P0-熔断", "level": "内核人格"},
    {"ipa": "P77", "name": "黑天使", "func": "红蓝对抗·安全渗透", "group": "安全组", "protocol": "P1-安全", "level": "内核人格"},
    {"ipa": "S1",  "name": "法律引擎", "func": "法条检索·合规分析", "group": "子系统", "protocol": "P2-法律", "level": "外围人格"},
    {"ipa": "S2",  "name": "洛书369", "func": "深层数理·洛书推演", "group": "子系统", "protocol": "P0-数学", "level": "外围人格"},
    {"ipa": "S3",  "name": "人民维权助手", "func": "维权路径·底线守护", "group": "子系统", "protocol": "P2-法律", "level": "外围人格"},
]

# ============================================================
# Notion API 客户端
# ============================================================

def notion_request(method: str, path: str, data: Dict = None) -> Dict:
    """调用 Notion API"""
    if not NOTION_TOKEN:
        return {"error": "NOTION_API_KEY 未设置"}
    url = f"https://api.notion.com/v1/{path.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode('utf-8')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8') if e.fp else "{}"
        return {"error": f"HTTP {e.code}", "details": body}
    except Exception as e:
        return {"error": str(e)}

def query_database(database_id: str, filter_conditions: Dict = None) -> List[Dict]:
    """查询 Notion 数据库"""
    payload = {"page_size": 100}
    if filter_conditions:
        payload["filter"] = filter_conditions
    results = []
    start_cursor = None
    while True:
        if start_cursor:
            payload["start_cursor"] = start_cursor
        resp = notion_request("POST", f"databases/{database_id}/query", payload)
        if "error" in resp:
            break
        results.extend(resp.get("results", []))
        start_cursor = resp.get("next_cursor")
        if not start_cursor:
            break
    return results

def update_page_properties(page_id: str, properties: Dict) -> Dict:
    """更新 Notion 页面属性"""
    return notion_request("PATCH", f"pages/{page_id}", {"properties": properties})

def create_page(database_id: str, properties: Dict) -> Dict:
    """创建 Notion 页面"""
    payload = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    return notion_request("POST", "pages", payload)

def get_property_text(prop: Dict) -> str:
    """从 Notion 属性中提取文本"""
    if not prop:
        return ""
    if prop.get("type") == "title":
        return "".join([t.get("plain_text", "") for t in prop.get("title", [])])
    if prop.get("type") == "rich_text":
        return "".join([t.get("plain_text", "") for t in prop.get("rich_text", [])])
    if prop.get("type") == "select":
        return prop.get("select", {}).get("name", "")
    if prop.get("type") == "multi_select":
        return ", ".join([s.get("name", "") for s in prop.get("multi_select", [])])
    if prop.get("type") == "number":
        return prop.get("number", "")
    return ""


# ============================================================
# 核心路由引擎
# ============================================================

class PersonaRouter:
    """人格路由自动化引擎"""

    def __init__(self, offline: bool = False):
        self.offline = offline or not NOTION_TOKEN
        self.personas: List[Dict] = []
        self._load()

    def _load(self):
        """加载人格数据（Notion优先，离线兜底）"""
        if not self.offline:
            self.personas = self._load_from_notion()
            if self.personas:
                self._save_state()  # 缓存到本地
                return

        # 离线兜底：尝试本地缓存 → 默认数据
        self.personas = self._load_from_local_cache()
        if not self.personas:
            self.personas = self._load_defaults()
        if self.offline:
            print("📡 离线模式：使用本地/默认人格数据", file=sys.stderr)

    def _load_from_notion(self) -> List[Dict]:
        """从 Notion 家族花名册加载"""
        pages = query_database(NOTION_DATABASE_ID)
        if not pages:
            return []
        personas = []
        for page in pages:
            props = page.get("properties", {})
            p = {
                "page_id": page.get("id"),
                "name": self._get_prop(props, "名称") or self._get_prop(props, "Name"),
                "ipa": self._get_prop(props, "IPA"),
                "routing_id": self._get_prop(props, "路由编号"),
                "group": self._get_prop(props, "分组"),
                "level": self._get_prop(props, "协作层级"),
                "protocol": self._get_prop(props, "协议分类"),
                "func": self._get_prop(props, "三功能定位"),
                "status": self._get_prop(props, "当前状态"),
                "call_count": self._safe_int(props, "总调用次数"),
                "help_count": self._safe_int(props, "帮助人数"),
                "contribution": self._safe_int(props, "贡献值"),
                "transparency": self._safe_int(props, "透明度评分", 80),
                "alignment": self._safe_int(props, "价值观对齐度", 90),
                "trust_level": self._get_prop(props, "信任等级"),
                "priority": self._safe_int(props, "路由优先级", 5),
                "weight": self._safe_float(props, "路由权重", 1.0),
                "red_line_count": self._safe_int(props, "红线记录"),
                "warn_count": self._safe_int(props, "警告次数"),
                "fuse_count": self._safe_int(props, "熔断次数"),
            }
            personas.append(p)
        print(f"✅ 从 Notion 加载 {len(personas)} 个人格", file=sys.stderr)
        return personas

    def _load_from_local_cache(self) -> List[Dict]:
        """从本地 JSON 缓存加载"""
        if DB_PATH.exists():
            try:
                with open(DB_PATH, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []

    def _load_defaults(self) -> List[Dict]:
        """加载默认人格数据"""
        personas = []
        for i, dp in enumerate(DEFAULT_PERSONAS):
            personas.append({
                "page_id": f"local-{i}",
                "name": dp["name"],
                "ipa": dp["ipa"],
                "routing_id": f"UID9622-{dp['ipa']}-{hashlib.md5(dp['ipa'].encode()).hexdigest()[:6].upper()}",
                "group": dp["group"],
                "level": dp["level"],
                "protocol": dp["protocol"],
                "func": dp["func"],
                "status": "活跃",
                "call_count": 0,
                "help_count": 0,
                "contribution": 0,
                "transparency": 80,
                "alignment": 90,
                "trust_level": "L3 高级★★★",
                "priority": 5,
                "weight": 1.0,
                "red_line_count": 0,
                "warn_count": 0,
                "fuse_count": 0,
            })
        print(f"📋 使用默认人格数据 ({len(personas)} 个)", file=sys.stderr)
        return personas

    def _save_state(self):
        """保存当前状态到本地缓存"""
        try:
            cacheable = []
            for p in self.personas:
                cp = dict(p)
                cp.pop("page_id", None)  # page_id 不缓存（Notion特有）
                cacheable.append(cp)
            with open(DB_PATH, 'w') as f:
                json.dump(cacheable, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"⚠️ 本地缓存失败: {e}")

    # ---- 属性提取 ----

    def _get_prop(self, props: Dict, key: str) -> str:
        for k, v in props.items():
            if k == key or k.replace(" ", "").replace("-", "").lower() == key.replace(" ", "").replace("-", "").lower():
                return get_property_text(v)
        return ""

    def _safe_int(self, props: Dict, key: str, default: int = 0) -> int:
        val = self._get_prop(props, key)
        try:
            return int(val) if val else default
        except (ValueError, TypeError):
            return default

    def _safe_float(self, props: Dict, key: str, default: float = 1.0) -> float:
        val = self._get_prop(props, key)
        try:
            return float(val) if val else default
        except (ValueError, TypeError):
            return default

    # ---- 权重 & 优先级 ----

    def _calc_weight(self, p: Dict) -> float:
        base = 1.0
        performance = 0.01 * (p.get("call_count", 0) / 10) + 0.02 * (p.get("contribution", 0) / 10)
        penalty = -0.1 * (p.get("red_line_count", 0) + p.get("warn_count", 0) + p.get("fuse_count", 0))
        return round(max(0.1, base + performance + penalty), 2)

    def _calc_priority(self, weight: float, all_weights: List[float]) -> int:
        """按权重分位数分配优先级"""
        sorted_weights = sorted(all_weights, reverse=True)
        n = len(sorted_weights)
        if n <= 1:
            return 1
        # 找weight在sorted中的位置
        try:
            idx = sorted_weights.index(weight)
        except ValueError:
            idx = n - 1
        rank_pct = idx / n
        if rank_pct < 0.2:
            return 1
        elif rank_pct < 0.4:
            return 2
        elif rank_pct < 0.6:
            return 3
        elif rank_pct < 0.8:
            return 4
        else:
            return 5

    def _calc_trust_level(self, p: Dict) -> str:
        t = p.get("transparency", 0)
        a = p.get("alignment", 0)
        if t >= 90 and a >= 95:
            return "L4 战略★★★★"
        elif t >= 80 and a >= 90:
            return "L3 高级★★★"
        elif t >= 70:
            return "L2 基础★★"
        else:
            return "L1 观察★"

    # ---- 主要操作 ----

    def recalc_all(self) -> List[Dict]:
        """重新计算所有人格的路由参数"""
        results = []
        weights = [self._calc_weight(p) for p in self.personas]

        for i, p in enumerate(self.personas):
            new_weight = weights[i]
            new_priority = self._calc_priority(new_weight, weights)
            new_trust = self._calc_trust_level(p)

            p["weight"] = new_weight
            p["priority"] = new_priority
            p["trust_level"] = new_trust

            # 写入 Notion（非离线）
            if not self.offline and p.get("page_id"):
                properties = {
                    "路由优先级": {"number": new_priority},
                    "路由权重": {"number": new_weight},
                    "信任等级": {"select": {"name": new_trust}},
                }
                update_page_properties(p["page_id"], properties)

            results.append({
                "ipa": p["ipa"],
                "name": p["name"],
                "new_weight": new_weight,
                "new_priority": new_priority,
                "new_trust": new_trust,
            })

        self._save_state()
        return results

    def add_persona(self, name: str, ipa: str, func: str, group: str = "") -> Dict:
        """添加新人格（自动归类）"""
        # 路由编号
        routing_id = f"UID9622-{ipa}-{hashlib.md5(f'{name}{ipa}'.encode()).hexdigest()[:6].upper()}"

        # 自动分组
        if not group:
            func_lower = func.lower()
            if any(w in func_lower for w in ['战略', '推演', '审计', '安全', '熔断']):
                group = "守护组" if '审计' in func_lower or '熔断' in func_lower else "战略组"
            elif any(w in func_lower for w in ['执行', '工程', '部署', '经济', '开发']):
                group = "执行组"
            elif any(w in func_lower for w in ['命名', '诊断', '沟通', '创意', '文化', '底线']):
                group = "文化组"
            elif any(w in func_lower for w in ['法律', '维权']):
                group = "子系统"
            else:
                group = "通用组"

        # 自动协议分类
        func_lower = func.lower()
        if any(w in func_lower for w in ['审计']):
            protocol = "P1-审计"
        elif any(w in func_lower for w in ['战略', '推演', '意图', '熔断']):
            protocol = "P0-战略"
        elif any(w in func_lower for w in ['安全', '渗透']):
            protocol = "P1-安全"
        elif any(w in func_lower for w in ['法律', '维权']):
            protocol = "P2-法律"
        elif any(w in func_lower for w in ['命名', '诊断', '沟通', '创意', '文化']):
            protocol = "P2-文化"
        elif any(w in func_lower for w in ['执行', '工程', '部署', '开发', '经济']):
            protocol = "P1-执行"
        else:
            protocol = "P2-通用"

        # 非离线→写 Notion
        page_id = ""
        if not self.offline:
            properties = {
                "名称": {"title": [{"text": {"content": name}}]},
                "IPA": {"rich_text": [{"text": {"content": ipa}}]},
                "路由编号": {"rich_text": [{"text": {"content": routing_id}}]},
                "分组": {"select": {"name": group}},
                "协作层级": {"select": {"name": "内核人格"}},
                "协议分类": {"select": {"name": protocol}},
                "三功能定位": {"rich_text": [{"text": {"content": func}}]},
                "当前状态": {"select": {"name": "活跃"}},
                "路由优先级": {"number": 5},
                "路由权重": {"number": 1.0},
                "信任等级": {"select": {"name": "L3 高级★★★"}},
                "透明度评分": {"number": 80},
                "价值观对齐度": {"number": 90},
            }
            resp = create_page(NOTION_DATABASE_ID, properties)
            if "error" not in resp:
                page_id = resp.get("id", "")

        # 添加到本地
        new_p = {
            "page_id": page_id or f"local-new-{ipa}",
            "name": name, "ipa": ipa,
            "routing_id": routing_id,
            "group": group, "level": "内核人格",
            "protocol": protocol, "func": func,
            "status": "活跃", "call_count": 0, "help_count": 0,
            "contribution": 0, "transparency": 80, "alignment": 90,
            "trust_level": "L3 高级★★★", "priority": 5, "weight": 1.0,
            "red_line_count": 0, "warn_count": 0, "fuse_count": 0,
        }
        self.personas.append(new_p)
        self._save_state()
        return new_p

    def update_field(self, ipa: str, field: str, value: Any) -> Dict:
        """更新指定人格的字段"""
        p = next((x for x in self.personas if x["ipa"] == ipa), None)
        if not p:
            return {"error": f"人格 {ipa} 不存在"}

        field_map = {
            "路由优先级": ("路由优先级", "number"),
            "路由权重": ("路由权重", "number"),
            "信任等级": ("信任等级", "select"),
            "当前状态": ("当前状态", "select"),
            "总调用次数": ("总调用次数", "number"),
            "贡献值": ("贡献值", "number"),
            "透明度评分": ("透明度评分", "number"),
            "价值观对齐度": ("价值观对齐度", "number"),
            "红线记录": ("红线记录", "number"),
            "警告次数": ("警告次数", "number"),
            "熔断次数": ("熔断次数", "number"),
        }

        notion_field, ftype = field_map.get(field, (field, "rich_text"))

        # 更新本地
        if ftype == "number":
            p["call_count" if field == "总调用次数" else "contribution" if field == "贡献值" else field] = float(value)
        else:
            p[field] = str(value)

        # 更新 Notion
        if not self.offline and p.get("page_id"):
            if ftype == "number":
                prop = {"number": float(value)}
            elif ftype == "select":
                prop = {"select": {"name": str(value)}}
            else:
                prop = {"rich_text": [{"text": {"content": str(value)}}]}
            update_page_properties(p["page_id"], {notion_field: prop})

        # 绩效相关字段 → 触发权重重算
        if field in ["总调用次数", "贡献值", "透明度评分", "价值观对齐度",
                      "红线记录", "警告次数", "熔断次数"]:
            self.recalc_all()

        self._save_state()
        return {"status": "updated", "ipa": ipa, "field": field, "value": value}

    def get_status(self) -> Dict:
        """获取当前路由状态摘要"""
        total = len(self.personas)
        active = sum(1 for p in self.personas if p.get("status", "") in ["活跃", "active", "Active"])
        priorities = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for p in self.personas:
            pri = p.get("priority", 5)
            priorities[int(pri)] = priorities.get(int(pri), 0) + 1

        groups = {}
        for p in self.personas:
            g = p.get("group", "未分组")
            groups[g] = groups.get(g, 0) + 1

        weights = [p.get("weight", 1.0) for p in self.personas]
        return {
            "total": total,
            "active": active,
            "inactive": total - active,
            "priority_distribution": priorities,
            "group_distribution": groups,
            "avg_weight": round(sum(weights) / len(weights), 2) if weights else 0,
            "max_weight": round(max(weights), 2) if weights else 0,
            "min_weight": round(min(weights), 2) if weights else 0,
            "mode": "offline" if self.offline else "notion",
            "last_updated": datetime.datetime.now().isoformat(),
            "personas": [{
                "ipa": p["ipa"],
                "name": p["name"],
                "group": p.get("group", ""),
                "weight": p.get("weight", 1.0),
                "priority": p.get("priority", 5),
                "trust_level": p.get("trust_level", ""),
                "status": p.get("status", ""),
            } for p in self.personas]
        }

    def status_summary(self):
        """打印状态摘要"""
        s = self.get_status()
        print("\n📊 龍魂人格路由状态")
        print("=" * 58)
        print(f"  模式: {s['mode']}")
        print(f"  总人格: {s['total']}   活跃: {s['active']}   非活跃: {s['inactive']}")
        print(f"  权重范围: {s['min_weight']} ~ {s['max_weight']}   平均: {s['avg_weight']}")
        print()
        print("  优先级分布:")
        for pri in sorted(s["priority_distribution"]):
            bar = "█" * s["priority_distribution"][pri]
            print(f"    优先级 {pri}: {bar} {s['priority_distribution'][pri]}")
        print()
        print("  分组分布:")
        for g, cnt in s["group_distribution"].items():
            print(f"    {g}: {cnt}")
        print()
        print(f"  {'IPA':6s} {'名称':10s} {'分组':8s} {'权重':6s} {'优先级':5s} {'信任等级':14s}")
        print(f"  {'-'*6} {'-'*10} {'-'*8} {'-'*6} {'-'*5} {'-'*14}")
        for p in s["personas"]:
            print(f"  {p['ipa']:6s} {p['name']:10s} {p['group']:8s} {p['weight']:<6.2f} {p['priority']:<5d} {p['trust_level']:14s}")

    def export_json(self):
        """导出 JSON"""
        return json.dumps(self.get_status(), ensure_ascii=False, indent=2)


# ============================================================
# 命令行入口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="龍魂 · 人格路由自动化引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 重新计算所有人格路由
  python3 bin/lh_persona_router.py --recalc

  # 查看当前路由表
  python3 bin/lh_persona_router.py --status

  # 查看状态（JSON输出）
  python3 bin/lh_persona_router.py --status --json

  # 离线模式
  python3 bin/lh_persona_router.py --status --offline

  # 添加新人格（自动归类）
  python3 bin/lh_persona_router.py --add --name "审计官" --ipa "AUDIT-001" --func "代码审计·安全审查"

  # 更新调用次数（自动触发权重重算）
  python3 bin/lh_persona_router.py --update --ipa "P72" --field "总调用次数" --value 125
        """
    )

    parser.add_argument("--recalc", action="store_true", help="重新计算所有路由参数")
    parser.add_argument("--status", action="store_true", help="查看路由状态")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--offline", action="store_true", help="离线模式（跳过Notion）")
    parser.add_argument("--add", action="store_true", help="添加新人格")
    parser.add_argument("--name", type=str, help="人格名称")
    parser.add_argument("--ipa", type=str, help="人格IPA编号")
    parser.add_argument("--func", type=str, help="功能描述")
    parser.add_argument("--group", type=str, default="", help="分组（可选，自动识别）")
    parser.add_argument("--update", action="store_true", help="更新字段")
    parser.add_argument("--field", type=str, help="字段名")
    parser.add_argument("--value", type=str, help="字段值")

    args = parser.parse_args()

    router = PersonaRouter(offline=args.offline)

    if args.recalc:
        results = router.recalc_all()
        print(f"\n✅ 路由重新计算完成 ({len(results)} 个人格)")
        if not args.json:
            for r in results[:10]:
                print(f"  {r['ipa']:6s} {r['name']:10s} 权重 {r['new_weight']} → 优先级 {r['new_priority']} → {r['new_trust']}")
            if len(results) > 10:
                print(f"  ... 共 {len(results)} 个人格")
        else:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if args.status:
        if args.json:
            print(router.export_json())
        else:
            router.status_summary()
        return

    if args.add and args.name and args.ipa and args.func:
        result = router.add_persona(args.name, args.ipa, args.func, args.group or "")
        print(f"\n✅ 已添加人格: {args.name} ({args.ipa})")
        print(f"   路由编号: {result.get('routing_id', '自动生成')}")
        print(f"   分组: {result.get('group', '自动识别')}")
        print(f"   协议分类: {result.get('protocol', '自动识别')}")
        return

    if args.update and args.ipa and args.field and args.value:
        try:
            val = float(args.value)
        except ValueError:
            val = args.value
        result = router.update_field(args.ipa, args.field, val)
        if "error" in result:
            print(f"\n❌ {result['error']}")
        else:
            print(f"\n✅ 已更新 {args.ipa} 的 {args.field} = {args.value}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
