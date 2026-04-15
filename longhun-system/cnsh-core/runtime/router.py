"""
CNSH Command Router — 执行分发层
解析完的 CNSHCommand → 路由到对应业务模块

规则：
  CALENDAR → dna_calendar 模块
  DNA      → dna_ledger 模块
  RISK     → risk_engine
  ETHICS   → ethics_engine
  AUDIT    → decision_engine
  ALGO/AI/PLUGIN → L3 extension_registry（真实查找）
  REGISTRY → registry 操作
  DARE     → 四敢品质系统
  SHIELD   → LocalShield 三层防御
  SYSTEM   → system ops

Author: 诸葛鑫 (UID9622)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime
from typing import Any
from .command import CNSHCommand


class CNSHRouter:

    def dispatch(self, cmd: CNSHCommand) -> Any:
        """
        根据 domain:verb 分发到对应处理器
        返回执行结果（dict）
        """
        domain = cmd.domain
        verb   = cmd.verb

        handler_map = {
            "CALENDAR":   self._handle_calendar,
            "DNA":        self._handle_dna,
            "RISK":       self._handle_risk,
            "ETHICS":     self._handle_ethics,
            "AUDIT":      self._handle_audit,
            "REGISTRY":   self._handle_registry,
            "PROJECTION": self._handle_projection,
            "DARE":       self._handle_dare,
            "SHIELD":     self._handle_shield,
            "SYSTEM":     self._handle_system,
        }

        handler = handler_map.get(domain)
        if handler:
            return handler(cmd)

        # 未知域 → L3 扩展注册表真实查找
        return self._handle_extension(cmd)

    # ── CALENDAR 处理器 ───────────────────────────────────────────

    def _handle_calendar(self, cmd: CNSHCommand) -> dict:
        import requests
        api = "http://127.0.0.1:9622"
        p = cmd.params

        if cmd.verb == "ADD":
            payload = {
                "title":         p.get("title", "(CNSH事件)"),
                "user_id":       cmd.user_id,
                "mood":          p.get("mood", ""),
                "notes":         p.get("notes", ""),
                "tags":          [t.strip() for t in str(p.get("tags","")).split(",") if t.strip()],
                "lat":           float(p.get("lat", 0)),
                "lng":           float(p.get("lng", 0)),
                "city":          p.get("city", ""),
                "fetch_weather": bool(p.get("weather", True)),
            }
            r = requests.post(f"{api}/calendar/event", json=payload, timeout=10)
            r.raise_for_status()
            return {"status": "ok", **r.json()}

        if cmd.verb == "LIST":
            date = p.get("date")
            limit = int(p.get("limit", 20))
            url = f"{api}/calendar/events/{cmd.user_id}?limit={limit}"
            if date: url += f"&date={date}"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb == "REFLOW":
            dna = p.get("dna") or p.get("dna_trace")
            date = p.get("date")
            if dna:
                import urllib.parse
                r = requests.get(f"{api}/calendar/reflow/dna/{urllib.parse.quote(dna)}", timeout=10)
                r.raise_for_status()
                return r.json()
            if date:
                r = requests.get(f"{api}/calendar/reflow/date/{cmd.user_id}/{date}", timeout=10)
                r.raise_for_status()
                return r.json()
            return {"error": "REFLOW 需要 PARAMS{dna=...} 或 PARAMS{date=YYYY-MM-DD}"}

        if cmd.verb == "VERIFY":
            r = requests.get(f"{api}/calendar/verify/{cmd.user_id}", timeout=10)
            r.raise_for_status()
            return r.json()

        return {"error": f"CALENDAR:{cmd.verb} 未实现"}

    # ── DNA 处理器 ────────────────────────────────────────────────

    def _handle_dna(self, cmd: CNSHCommand) -> dict:
        import requests
        api = "http://127.0.0.1:9622"
        p = cmd.params

        if cmd.verb == "QUERY":
            uid = p.get("user", cmd.user_id)
            limit = int(p.get("limit", 10))
            r = requests.get(f"{api}/dna/{uid}?limit={limit}", timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb == "VERIFY":
            r = requests.get(f"{api}/ledger/verify", timeout=10)
            r.raise_for_status()
            return r.json()

        return {"error": f"DNA:{cmd.verb} 未实现"}

    # ── RISK 处理器 ───────────────────────────────────────────────

    def _handle_risk(self, cmd: CNSHCommand) -> dict:
        import requests
        p = cmd.params
        payload = {
            "R": float(p.get("R", 0.5)),
            "U": float(p.get("U", 0.3)),
            "I": float(p.get("I", 0.2)),
        }
        r = requests.post("http://127.0.0.1:9622/risk", json=payload, timeout=10)
        r.raise_for_status()
        return r.json()

    # ── ETHICS 处理器 ─────────────────────────────────────────────

    def _handle_ethics(self, cmd: CNSHCommand) -> dict:
        import requests
        if cmd.verb == "RULES":
            r = requests.get("http://127.0.0.1:9622/ethics/rules", timeout=10)
            r.raise_for_status()
            return r.json()
        return {"error": f"ETHICS:{cmd.verb} 未实现"}

    # ── AUDIT 处理器 ──────────────────────────────────────────────

    def _handle_audit(self, cmd: CNSHCommand) -> dict:
        import requests
        p = cmd.params
        # 支持 PARAMS{scores=85,90,78,82,88,76,91,80} 格式
        scores_raw = str(p.get("scores", "80,80,80,80,80,80,80,80"))
        try:
            scores = [float(s.strip()) for s in scores_raw.split(",")]
        except Exception:
            scores = [80.0] * 8

        payload = {
            "content": p.get("content", "audit request"),
            "user_id": cmd.user_id,
            "metadata": {"audit_scores": scores}
        }
        r = requests.post("http://127.0.0.1:9622/event", json=payload, timeout=10)
        r.raise_for_status()
        return r.json()

    # ── REGISTRY 处理器 ───────────────────────────────────────────

    def _handle_registry(self, cmd: CNSHCommand) -> dict:
        import requests
        api = "http://127.0.0.1:9622"
        p   = cmd.params

        if cmd.verb == "REGISTER":
            payload = {
                "content":      p.get("content", cmd.raw),
                "scope":        p.get("scope", "PUBLIC"),
                "ext_id":       p.get("ext_id", cmd.ext_id or ""),
                "ext_type":     p.get("ext_type", ""),
                "handler_path": p.get("handler", ""),
                "description":  p.get("desc", ""),
                "version":      p.get("version", "1.0.0"),
            }
            r = requests.post(f"{api}/registry/register", json=payload, timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb == "LOOKUP":
            ext_id = p.get("ext_id") or cmd.ext_id
            if not ext_id:
                return {"error": "LOOKUP 需要 PARAMS{ext_id=xxx} 或 EXT[xxx]"}
            r = requests.get(f"{api}/registry/lookup/ext/{ext_id}", timeout=10)
            if r.status_code == 404:
                return {"found": False, "ext_id": ext_id}
            r.raise_for_status()
            return r.json()

        if cmd.verb == "VERIFY":
            r = requests.get(f"{api}/registry/verify", timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb == "LIST":
            r = requests.get(f"{api}/registry/extensions", timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb == "BOUNDARY":
            dna = p.get("dna") or cmd.ext_id
            if not dna:
                return {"error": "BOUNDARY 需要 PARAMS{dna=...}"}
            import urllib.parse
            r = requests.get(f"{api}/registry/boundary/{urllib.parse.quote(dna)}", timeout=10)
            r.raise_for_status()
            return r.json()

        return {"error": f"REGISTRY:{cmd.verb} 未实现，支持 REGISTER · LOOKUP · VERIFY · LIST · BOUNDARY"}

    # ── PROJECTION 处理器 ─────────────────────────────────────────

    def _handle_projection(self, cmd: CNSHCommand) -> dict:
        import requests
        api = "http://127.0.0.1:9622"
        p   = cmd.params

        if cmd.verb in ("NODES", "LIST"):
            limit = int(p.get("limit", 200))
            r = requests.get(f"{api}/projection/nodes?limit={limit}", timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb == "STATS":
            r = requests.get(f"{api}/projection/stats", timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb == "GLOBE":
            return {
                "status":  "ok",
                "message": "打开浏览器访问地球仪",
                "url":     "http://127.0.0.1:9622/ui/globe.html",
            }

        if cmd.verb == "GEOJSON":
            limit = int(p.get("limit", 200))
            r = requests.get(f"{api}/projection/nodes.geojson?limit={limit}", timeout=10)
            r.raise_for_status()
            return r.json()

        return {"error": f"PROJECTION:{cmd.verb} 未实现，支持 NODES · STATS · GLOBE · GEOJSON"}

    # ── DARE 处理器（四敢品质）────────────────────────────────────

    def _handle_dare(self, cmd: CNSHCommand) -> dict:
        import requests
        api = "http://127.0.0.1:9622"
        p   = cmd.params
        uid = p.get("user", cmd.user_id or "uid9622")

        if cmd.verb in ("SCORE", "GET", "STATUS"):
            r = requests.get(f"{api}/dare/score/{uid}", timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb == "YAO":
            r = requests.get(f"{api}/dare/yao/{uid}", timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb == "RECORD":
            atype = p.get("type", p.get("action_type", ""))
            if not atype:
                return {"error": "RECORD 需要 PARAMS{type=TRUST-INIT|SACRIFICE|DISSENT|AUDIT-OPEN}"}
            payload = {
                "action_type": atype,
                "weight":  float(p.get("weight", 1.0)),
                "context": p.get("context", ""),
                "user_id": uid,
            }
            r = requests.post(f"{api}/dare/record", json=payload, timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb in ("EASTER", "EGG", "EGGS"):
            r = requests.get(f"{api}/dare/easter-eggs", timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb == "CATALOG":
            r = requests.get(f"{api}/dare/catalog", timeout=10)
            r.raise_for_status()
            return r.json()

        return {"error": f"DARE:{cmd.verb} 未实现，支持 SCORE · YAO · RECORD · EASTER · CATALOG"}

    # ── SHIELD 处理器（三层防御）──────────────────────────────────

    def _handle_shield(self, cmd: CNSHCommand) -> dict:
        import requests
        api = "http://127.0.0.1:9622"
        p   = cmd.params

        if cmd.verb in ("PROCESS", "RUN", "CHECK"):
            content = p.get("content", cmd.raw or "")
            action  = p.get("action", "PROCESS")
            r = requests.post(f"{api}/shield/process",
                              json={"content": content, "action": action}, timeout=10)
            r.raise_for_status()
            return r.json()

        if cmd.verb in ("STATUS", "INFO"):
            r = requests.get(f"{api}/shield/status", timeout=10)
            r.raise_for_status()
            return r.json()

        return {"error": f"SHIELD:{cmd.verb} 未实现，支持 PROCESS · STATUS"}

    # ── 扩展注册表分发（L3 真实查找）─────────────────────────────

    def _handle_extension(self, cmd: CNSHCommand) -> dict:
        """
        通过 L3 注册表查找扩展处理器。
        EXT[algo.fractal] → 注册表查 handler_path → 分发执行
        """
        ext_id = cmd.ext_id
        if not ext_id:
            return {
                "status":  "unknown_domain",
                "domain":  cmd.domain,
                "verb":    cmd.verb,
                "message": f"域 [{cmd.domain}] 未内置，且未提供 EXT[...] 扩展ID",
                "hint":    "请用 EXT[ext.id] 指定处理器，或先通过 @REGISTRY:REGISTER 注册",
            }

        # 查 L3 注册表
        try:
            import requests
            r = requests.get(
                f"http://127.0.0.1:9622/registry/lookup/ext/{ext_id}",
                timeout=5,
            )
            if r.status_code == 404:
                return {
                    "status":  "ext_not_found",
                    "ext_id":  ext_id,
                    "domain":  cmd.domain,
                    "message": f"扩展 [{ext_id}] 未在 L3 注册表中注册",
                    "hint":    f"@REGISTRY:REGISTER PARAMS{{content=..., ext_id={ext_id}, handler=http://...}}",
                }
            r.raise_for_status()
            data  = r.json()
            entry = data.get("entry", {})

            return {
                "status":       "ext_found",
                "ext_id":       ext_id,
                "domain":       cmd.domain,
                "verb":         cmd.verb,
                "handler_path": entry.get("handler_path", ""),
                "scope":        entry.get("scope", ""),
                "version":      entry.get("version", ""),
                "dna_code":     entry.get("dna_code", ""),
                "note":         f"扩展已注册，handler: {entry.get('handler_path', '（未配置）')}",
            }

        except Exception as e:
            return {
                "status":  "registry_error",
                "ext_id":  ext_id,
                "error":   str(e),
                "message": "L3注册表查询失败，请确认服务在 9622 端口运行",
            }

    # ── SYSTEM 处理器 ─────────────────────────────────────────────

    def _handle_system(self, cmd: CNSHCommand) -> dict:
        if cmd.verb == "STATUS":
            import requests
            r = requests.get("http://127.0.0.1:9622/", timeout=5)
            return r.json()

        if cmd.verb == "HELP":
            return {
                "syntax": "@DOMAIN:VERB  PARAMS{k=v}  FLAG[f]  EXT[ext.id]",
                "layers": {
                    "L1-L2": "CNSH语法层 + 命令解析（已上线）",
                    "L3":    "扩展注册表 · 私域/公域边界（已上线）",
                    "L4":    "伦理熔断 + 风险引擎（已上线）",
                    "L5-L6": "日历时空胶囊 · 时光回流（基础版）",
                },
                "domains": {
                    "CALENDAR":   "ADD · LIST · REFLOW · VERIFY",
                    "DNA":        "QUERY · VERIFY",
                    "RISK":       "ASSESS  PARAMS{R=0~1, U=0~1, I=0~1}",
                    "ETHICS":     "RULES",
                    "AUDIT":      "RUN  PARAMS{scores=85,90,78,...}",
                    "REGISTRY":   "REGISTER · LOOKUP · VERIFY · LIST · BOUNDARY",
                    "PROJECTION": "NODES · STATS · GLOBE · GEOJSON",
                    "DARE":       "SCORE · YAO · RECORD · EASTER · CATALOG",
                    "SHIELD":     "PROCESS · STATUS",
                    "SYSTEM":     "STATUS · HELP",
                    "ALGO":       "任意VERB  EXT[algo.xxx]",
                    "AI":         "任意VERB  EXT[ai.xxx]",
                    "PLUGIN":     "任意VERB  EXT[plugin.xxx]",
                },
                "examples": [
                    "@CALENDAR:ADD  PARAMS{title=今天的会议, mood=专注, city=北京}",
                    "@CALENDAR:REFLOW  PARAMS{date=2026-03-23}",
                    "@DNA:VERIFY",
                    "@RISK:ASSESS  PARAMS{R=0.7, U=0.4, I=0.3}",
                    "@REGISTRY:REGISTER  PARAMS{content=算法扩展, ext_id=algo.fractal, handler=http://127.0.0.1:9700/run, scope=PUBLIC}",
                    "@REGISTRY:LOOKUP  EXT[algo.fractal]",
                    "@REGISTRY:VERIFY",
                    "@ALGO:RUN  PARAMS{name=fractal}  EXT[algo.fractal]",
                    "@SYSTEM:STATUS",
                ]
            }

        return {"error": f"SYSTEM:{cmd.verb} 未实现"}


# 单例
_router = CNSHRouter()

def dispatch(cmd: CNSHCommand) -> Any:
    return _router.dispatch(cmd)
