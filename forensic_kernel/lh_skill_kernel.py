#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 技能内核 v1.0

统一发现、注册、路由、评分、自优化龍魂生态里的所有技能。

能力：
  1. 发现技能：扫描 .kimi-code/skills、.agents/skills、longhun-system/skills
  2. 注册：读取 SKILL.md 元数据，生成 DNA
  3. 路由：根据用户输入匹配最合适的技能
  4. 回调：执行 Python 技能的 CLI 入口，或返回 Skill.md 调用说明
  5. 评分：成功率 + 使用频次 + 主权审计 + 用户反馈
  6. 自优化：定时/手动重算评分，优胜劣汰，输出优化建议

DNA: #龍芯⚡️2026-07-01-LONGHUN-SKILL-KERNEL-v1.0
"""

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_HOME = Path.home()

# 技能搜索路径
SKILL_SEARCH_PATHS = [
    _HOME / ".kimi-code" / "skills",
    _HOME / ".agents" / "skills",
    _HOME / "longhun-system" / "skills",
]

REGISTRY_PATH = _HOME / "longhun-system" / "data" / "forensic_kernel" / "skill_kernel_registry.json"
EXECUTION_LOG_PATH = _HOME / "longhun-system" / "data" / "forensic_kernel" / "skill_execution_log.jsonl"

sys.path.insert(0, str(_HOME / "longhun-system" / "龍魂取证内核"))
from 龍魂技能收集器 import 收集技能 as _从留证收集技能


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dna(主题: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    short = hashlib.sha256(f"{主题}:{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts[:8]}-{ts[9:]}-{主题}-v1.0-{short}"


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class 龍魂技能内核:
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}
        self.execution_log: List[Dict[str, Any]] = []
        self.load()

    # ========== 1. 发现与注册 ==========
    def 发现技能(self) -> "龍魂技能内核":
        """扫描所有技能目录，读取 SKILL.md 元数据。"""
        found: Dict[str, Dict[str, Any]] = {}
        skill_id = 0

        for base in SKILL_SEARCH_PATHS:
            if not base.exists():
                continue
            for entry in base.iterdir():
                skill_file = entry if entry.is_file() and entry.suffix == ".md" else entry / "SKILL.md"
                if not skill_file.exists():
                    continue
                meta = self._解析SKILL(skill_file)
                sid = f"SKILL-{skill_id:04d}"
                skill_id += 1
                found[sid] = {
                    "id": sid,
                    "技能名": meta.get("技能名") or entry.stem,
                    "路径": str(skill_file),
                    "作用域": meta.get("作用域", "未知"),
                    "版本": meta.get("版本", "v1.0"),
                    "描述": meta.get("描述", ""),
                    "DNA": _dna(meta.get("技能名") or entry.stem),
                    "来源": str(base.name),
                    "关键词": meta.get("关键词", []),
                    "入口": meta.get("入口", ""),
                    "优先级": meta.get("优先级", 50),
                    "状态": "已注册",
                    "评分": 50.0,
                    "使用次数": 0,
                    "成功次数": 0,
                    "失败次数": 0,
                    "审计状态": "未审计",
                    "注册时间": _now(),
                }

        # 同时把 Claude 留证里识别出的技能也注册为“候选技能”
        try:
            留证技能 = _从留证收集技能()
            for item in 留证技能.get("技能清单", []):
                sid = f"SKILL-{skill_id:04d}"
                skill_id += 1
                found[sid] = {
                    "id": sid,
                    "技能名": item["技能名"],
                    "路径": "",
                    "作用域": "留证识别",
                    "版本": "v1.0",
                    "描述": f"来自 Claude 留证，关键词：{', '.join(item['关键词'])}",
                    "DNA": _dna(item["技能名"]),
                    "来源": "Claude留证",
                    "关键词": item["关键词"],
                    "入口": "",
                    "状态": item.get("状态", "候选"),
                    "评分": 30.0 if item.get("状态") == "候选" else 60.0,
                    "使用次数": 0,
                    "成功次数": 0,
                    "失败次数": 0,
                    "审计状态": "未审计",
                    "注册时间": _now(),
                    "提及次数": item.get("提及次数", 0),
                    "来源文件": item.get("来源文件", []),
                }
        except Exception as e:
            print(f"🟡 留证技能收集失败: {e}")

        self.registry.update(found)
        return self

    def _解析SKILL(self, path: Path) -> Dict[str, Any]:
        text = path.read_text(encoding="utf-8", errors="ignore")
        meta: Dict[str, Any] = {}

        # 1. 尝试解析 YAML frontmatter
        if text.startswith("---"):
            try:
                import yaml
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    front = yaml.safe_load(parts[1]) or {}
                    if isinstance(front, dict):
                        meta["技能名"] = front.get("name") or front.get("title")
                        meta["描述"] = front.get("description", "")
                        meta["版本"] = front.get("metadata", {}).get("version", "v1.0")
                        meta["DNA"] = front.get("metadata", {}).get("dna", "")
                        # 触发条件：优先取 metadata.trigger.keywords，其次从 description/WHEN 提取
                        triggers: List[str] = []
                        md = front.get("metadata") or {}
                        if isinstance(md, dict):
                            trigger = md.get("trigger") or {}
                            if isinstance(trigger, dict):
                                triggers.extend(trigger.get("keywords", []))
                                meta["优先级"] = trigger.get("priority", 50)
                        desc = str(front.get("description", ""))
                        when = front.get("when") or ""
                        triggers.extend(re.findall(r"['\"]([^'\"]+)['\"]", when + " " + desc))
                        meta["关键词"] = [t.strip() for t in triggers if len(t.strip()) > 1]
                        # 入口命令：优先 metadata.entry，其次从 description 提取 .py 路径
                        entry = md.get("entry")
                        if entry and isinstance(entry, str):
                            meta["入口"] = entry
                        else:
                            cmd_match = re.search(r"([~/][^\s\"]+\.py)", desc)
                            if cmd_match:
                                meta["入口"] = f"python3 {cmd_match.group(1)}"
            except Exception:
                pass

        # 2. 兜底：Markdown 标题
        if not meta.get("技能名"):
            title_match = re.search(r"^#\s*(.+)", text, re.MULTILINE)
            if title_match:
                meta["技能名"] = title_match.group(1).strip()

        # 3. 兜底：WHEN / Path 字段
        if not meta.get("关键词"):
            when_match = re.search(r"WHEN:\s*(.+)", text, re.IGNORECASE)
            if when_match:
                meta["关键词"] = [k.strip() for k in when_match.group(1).split(",") if k.strip()]

        if not meta.get("描述"):
            meta["描述"] = text[:500].replace("#", "").strip()

        if not meta.get("版本"):
            ver_match = re.search(r"v\d+\.\d+", text)
            if ver_match:
                meta["版本"] = ver_match.group(0)

        return meta

    # ========== 2. 路由 ==========
    def 路由(self, 输入: str) -> Optional[Dict[str, Any]]:
        """根据输入文本匹配最合适的技能。"""
        lower = 输入.lower()
        candidates: List[Tuple[float, Dict[str, Any]]] = []
        for skill in self.registry.values():
            score = 0.0
            关键词 = skill.get("关键词", [])
            if not 关键词 and skill.get("描述"):
                关键词 = re.findall(r"[\w\-]+", skill["描述"].lower())
            for kw in 关键词:
                kw_lower = kw.lower()
                if kw_lower in lower:
                    score += 1.0
                    # 完整词匹配加分
                    if re.search(rf"\b{re.escape(kw_lower)}\b", lower):
                        score += 0.5
            if score > 0:
                # 加上技能本身评分作为质量权重
                score += skill.get("评分", 50.0) / 100.0
                # 加上 YAML 中声明的优先级（高优先级技能优先）
                score += skill.get("优先级", 50) / 1000.0
                candidates.append((score, skill))
        if not candidates:
            return None

        def _version_value(skill: Dict[str, Any]) -> float:
            m = re.search(r"v?(\d+)\.(\d+)(?:\.(\d+))?", str(skill.get("版本", "v1.0")))
            if not m:
                return 1.0
            major, minor, patch = m.groups()
            patch = patch or "0"
            return float(f"{major}.{minor}{patch.zfill(3)}")

        # 按分数降序；分数相同按版本号降序、优先级降序
        candidates.sort(
            key=lambda x: (x[0], _version_value(x[1]), x[1].get("优先级", 50)),
            reverse=True,
        )
        return candidates[0][1]

    # ========== 3. 回调执行 ==========
    def 执行回调(self, 技能ID: str, 参数: str = "") -> Dict[str, Any]:
        """
        执行技能回调。
        - 如果 SKILL.md 写了入口命令，尝试直接执行
        - 否则返回调用说明
        """
        skill = self.registry.get(技能ID)
        if not skill:
            return {"成功": False, "输出": f"🔴 技能不存在: {技能ID}", "返回码": -1}

        入口 = skill.get("入口", "")
        if not 入口 and skill.get("路径", "").endswith(".py"):
            入口 = f"python3 {skill['路径']}"

        start = time.time()
        if 入口:
            try:
                import sys as _sys
                _sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'bin'))
                from lh_secure_subprocess import safe_shell_cmd
                cmd = f"{入口} {参数}".strip()
                result = safe_shell_cmd(cmd, caller='skill_kernel', timeout=60)
                success = result.returncode == 0
                output = result.stdout if success else result.stderr
            except Exception as e:
                success = False
                output = str(e)
        else:
            success = True
            output = f"🟡 技能 '{skill['技能名']}' 无可执行入口，调用说明：\n{skill.get('描述', '')}"

        elapsed = time.time() - start
        self._记录执行(技能ID, 参数, success, output, elapsed)
        self._更新技能统计(技能ID, success)
        return {"成功": success, "输出": output, "技能": skill["技能名"], "耗时": elapsed}

    def _记录执行(self, 技能ID: str, 参数: str, 成功: bool, 输出: str, 耗时: float):
        record = {
            "时间": _now(),
            "技能ID": 技能ID,
            "参数": 参数,
            "成功": 成功,
            "输出": 输出[:500],
            "耗时": round(耗时, 3),
            "DNA": _dna("EXEC"),
        }
        EXECUTION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(EXECUTION_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _更新技能统计(self, 技能ID: str, 成功: bool):
        skill = self.registry.get(技能ID)
        if not skill:
            return
        skill["使用次数"] = skill.get("使用次数", 0) + 1
        if 成功:
            skill["成功次数"] = skill.get("成功次数", 0) + 1
        else:
            skill["失败次数"] = skill.get("失败次数", 0) + 1
        self._重算单技能评分(skill)
        self.save()

    # ========== 4. 评分机制 ==========
    def _重算单技能评分(self, skill: Dict[str, Any]):
        """
        评分公式（可替换为完整龍魂公式）：
          基础分 50
          + 成功率 × 40
          + log(使用次数+1) × 5
          + 审计奖励/惩罚 ±10
          - 失败次数 × 2
        """
        使用 = skill.get("使用次数", 0)
        成功 = skill.get("成功次数", 0)
        失败 = skill.get("失败次数", 0)
        成功率 = 成功 / 使用 if 使用 > 0 else 0.5

        audit_bonus = 0
        audit = skill.get("审计状态", "未审计")
        if audit == "通过":
            audit_bonus = 10
        elif audit == "警告":
            audit_bonus = -5
        elif audit == "熔断":
            audit_bonus = -20

        score = 50 + 成功率 * 40 + math.log(使用 + 1) * 5 + audit_bonus - 失败 * 2
        # 候选技能初始分低一点，但可以用
        if skill.get("状态") == "候选":
            score = min(score, 45)
        skill["评分"] = round(max(0, min(100, score)), 2)

    def 运行主权审计(self, 技能ID: str) -> str:
        """对技能描述/路径做简单内容主权审查。"""
        skill = self.registry.get(技能ID)
        if not skill:
            return "未找到"
        text = f"{skill.get('技能名', '')} {skill.get('描述', '')}"
        熔断词 = ["诈骗", "骗子", "洗脑", "操纵", "虚假"]
        警告词 = ["愤怒", "崩溃", "失望", "对抗"]
        if any(w in text for w in 熔断词):
            skill["审计状态"] = "熔断"
        elif any(w in text for w in 警告词):
            skill["审计状态"] = "警告"
        else:
            skill["审计状态"] = "通过"
        self._重算单技能评分(skill)
        self.save()
        return skill["审计状态"]

    # ========== 5. 自优化 ==========
    def 自优化(self) -> Dict[str, Any]:
        """
        自动优化循环：
          1. 对所有技能运行主权审计
          2. 重算评分
          3. 优胜劣汰：评分 < 20 标记废弃，> 80 标记核心
          4. 输出优化建议
        """
        for skill in self.registry.values():
            self.运行主权审计(skill["id"])
            self._重算单技能评分(skill)

        核心 = [s for s in self.registry.values() if s["评分"] >= 80]
        废弃 = [s for s in self.registry.values() if s["评分"] < 20]
        候选 = [s for s in self.registry.values() if s.get("状态") == "候选" and s["评分"] >= 60]

        for s in 核心:
            s["状态"] = "核心"
        for s in 废弃:
            s["状态"] = "废弃"
        for s in 候选:
            s["状态"] = "已转正"

        suggestions = []
        for s in sorted(self.registry.values(), key=lambda x: x["评分"]):
            if s["评分"] < 40:
                suggestions.append(f"🔴 建议废弃/重审：{s['技能名']}（评分 {s['评分']}）")
            elif 40 <= s["评分"] < 60:
                suggestions.append(f"🟡 建议改进：{s['技能名']}（评分 {s['评分']}）")

        report = {
            "时间": _now(),
            "技能总数": len(self.registry),
            "核心数": len(核心),
            "废弃数": len(废弃),
            "平均分": round(sum(s["评分"] for s in self.registry.values()) / len(self.registry), 2) if self.registry else 0,
            "优化建议": suggestions,
            "DNA": _dna("SKILL-OPT"),
        }
        self.save()
        return report

    # ========== 6. 持久化 ==========
    def load(self):
        self.registry = _load_json(REGISTRY_PATH, {})
        if EXECUTION_LOG_PATH.exists():
            self.execution_log = [json.loads(line) for line in open(EXECUTION_LOG_PATH, encoding="utf-8") if line.strip()]
        else:
            self.execution_log = []

    def save(self):
        _save_json(REGISTRY_PATH, self.registry)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "系统DNA": "#龍芯⚡️2026-07-01-LONGHUN-SKILL-KERNEL-v1.0",
            "生成时间": _now(),
            "技能总数": len(self.registry),
            "技能列表": list(self.registry.values()),
            "执行日志数": len(self.execution_log),
        }


# ========== 7. API 服务 ==========
def _build_app(内核: 龍魂技能内核):
    from flask import Flask, jsonify, request, Response
    app = Flask(__name__)

    @app.route("/")
    def 首页():
        v = 内核.to_dict()
        rows = ""
        for s in sorted(v["技能列表"], key=lambda x: x.get("评分", 0), reverse=True):
            status_color = {"核心": "green", "已注册": "blue", "候选": "orange", "废弃": "red", "已转正": "purple"}.get(s["状态"], "black")
            rows += f"""
            <tr>
              <td><strong>{s['技能名']}</strong></td>
              <td><span style="color:{status_color}">{s['状态']}</span></td>
              <td>{s.get('评分', 0)}</td>
              <td>{s.get('使用次数', 0)} / {s.get('成功次数', 0)} / {s.get('失败次数', 0)}</td>
              <td>{s.get('审计状态', '-')}</td>
              <td>{s.get('来源', '')}</td>
            </tr>
            """
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>龍魂技能内核</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 40px; background: #f7f7f7; }}
  .container {{ max-width: 1200px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 12px; }}
  h1 {{ color: #b91c1c; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
  th, td {{ text-align: left; padding: 10px; border-bottom: 1px solid #eee; font-size: 14px; }}
  th {{ background: #f0f0f0; }}
</style></head>
<body>
<div class="container">
  <h1>🐉 龍魂技能内核 · 统一注册表</h1>
  <p><strong>系统 DNA:</strong> <code>{v['系统DNA']}</code></p>
  <p><strong>技能总数:</strong> {v['技能总数']} | <strong>执行日志:</strong> {v['执行日志数']}</p>
  <table>
    <tr><th>技能名</th><th>状态</th><th>评分</th><th>使用/成功/失败</th><th>审计</th><th>来源</th></tr>
    {rows}
  </table>
</div>
</body></html>"""
        return Response(html, mimetype="text/html")

    @app.route("/api/skills")
    def API技能列表():
        return jsonify(内核.to_dict())

    @app.route("/api/route", methods=["POST"])
    def API路由():
        data = request.get_json() or {}
        text = str(data.get("text", ""))
        skill = 内核.路由(text)
        return jsonify({"输入": text, "匹配技能": skill})

    @app.route("/api/execute", methods=["POST"])
    def API执行():
        data = request.get_json() or {}
        skill_id = str(data.get("id", ""))
        args = str(data.get("args", ""))
        result = 内核.执行回调(skill_id, args)
        return jsonify(result)

    @app.route("/api/optimize", methods=["POST"])
    def API自优化():
        return jsonify(内核.自优化())

    return app


def main():
    parser = argparse.ArgumentParser(description="龍魂技能内核")
    parser.add_argument("--discover", action="store_true", help="重新扫描并注册所有技能")
    parser.add_argument("--start", action="store_true", help="启动 API 服务")
    parser.add_argument("--route", type=str, help="测试路由，例如：--route '跑训练优化'")
    parser.add_argument("--execute", nargs=2, metavar=("ID", "ARGS"), help="执行技能回调")
    parser.add_argument("--optimize", action="store_true", help="运行自优化")
    parser.add_argument("--port", type=int, default=8844, help="服务端口（默认 8844）")
    args = parser.parse_args()

    内核 = 龍魂技能内核()
    if args.discover or not 内核.registry:
        内核.发现技能()
        内核.save()
        print(f"🐉 技能发现完成，共注册 {len(内核.registry)} 个技能")

    if args.route:
        skill = 内核.路由(args.route)
        print(json.dumps(skill, ensure_ascii=False, indent=2))
        return

    if args.execute:
        result = 内核.执行回调(args.execute[0], args.execute[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.optimize:
        report = 内核.自优化()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    if args.start:
        app = _build_app(内核)
        print(f"🐉 龍魂技能内核已启动")
        print(f"   面板: http://127.0.0.1:{args.port}/")
        print(f"   API:  http://127.0.0.1:{args.port}/api/skills")
        app.run(host="127.0.0.1", port=args.port, threaded=True)
        return

    # 默认：显示注册表摘要
    print("🐉 龍魂技能内核")
    print(f"   已注册技能: {len(内核.registry)}")
    print(f"   执行日志:   {len(内核.execution_log)}")
    print(f"   注册表:     {REGISTRY_PATH}")
    print(f"\n常用命令:")
    print(f"   重新发现: python3 {__file__} --discover")
    print(f"   启动服务: python3 {__file__} --start")
    print(f"   路由测试: python3 {__file__} --route '跑训练优化'")
    print(f"   自优化:   python3 {__file__} --optimize")


if __name__ == "__main__":
    main()
