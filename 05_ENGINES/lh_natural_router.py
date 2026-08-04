#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·自然语言多引擎路由 v1.0
============================
DNA: #龍芯⚡️丙午·癸未·丁未·申时·☵坎-NATURAL-ROUTER-v1.0-MULTI-ENGINE

一句话触发多个引擎，不再依赖固定指令。
基于语义抽屉体系（L1情绪 → L2领域 → L3哲学 → L4执行 → L5关系）
+ 扩展引擎注册表，实现自然语言到系统能力的自动分发。

用法:
  python3 engines/lh_natural_router.py "查一下语义抽屉和通心译"
  python3 engines/lh_natural_router.py "去年318路上的事"
  python3 engines/lh_natural_router.py "人参的功效和用量"
  python3 engines/lh_natural_router.py "帮我审计一下系统"
"""

import hashlib
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─── 项目路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = PROJECT_ROOT / "bin"
ENGINES_DIR = PROJECT_ROOT / "engines"
DRAWERS_FILE = PROJECT_ROOT / "01_技能庫" / "owner_semantic_drawers_v2.0.json"
SEMANTIC_LIB = PROJECT_ROOT / "L7_数据层" / "semantic_context_library.json"
VENV_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python3"
PYTHON_CMD = str(VENV_PYTHON) if VENV_PYTHON.exists() else "python3"

CST = timezone(timedelta(hours=8))
DNA_PREFIX = "#龍芯⚡️"
ENGINE_DNA = f"{DNA_PREFIX}丙午·癸未·丁未·申时·☵坎-NATURAL-ROUTER-v1.0-MULTI-ENGINE"

# 主导引擎阈值：第一名得分是第二名的 DOMINANCE_RATIO 倍以上时，只执行第一名
DOMINANCE_RATIO = 2.0

# ─── L4 抽屉 target_bin 兜底映射（抽屉里写的脚本可能已改名/不存在） ───
L4_FALLBACK = {
    "lh_review": "full_audit",
    "lh_memory_load": "xuanji",
}

# ─── 扩展引擎注册表（不在语义抽屉 L4 里的独立引擎） ───
EXTRA_ENGINES = {
    "xuanji": {
        "name": "璇玑·记忆推演",
        "cmd": [PYTHON_CMD, str(ENGINES_DIR / "lh_xuanji_engine.py")],
        "triggers": [
            "去年", "前年", "上次", "之前", "记得", "回忆", "追溯", "推演",
            "怎么回事", "发生了什么", "路线", "路上", "旅程", "经历"
        ],
        "weight": 1.0,
        "description": "基于记忆索引的多人格溯源推演",
    },
    "herbal_rag": {
        "name": "龍芯·华佗本草RAG",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "lh_herbal_rag.py")],
        "triggers": [
            "人参", "甘草", "当归", "黄芪", "本草", "中药", "药材", "药性",
            "功效", "主治", "用量", "性味", "归经", "土话", "草药"
        ],
        "weight": 1.0,
        "description": "48味药八维知识检索",
    },
    "semantic_context": {
        "name": "通心译·语境语义",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "lh_semantic_context_engine.py")],
        "triggers": [
            "什么意思", "怎么理解", "语义", "语境", "通心译", "对齐", "统一",
            "收口", "映射", "翻译", "大白话", "解释"
        ],
        "weight": 0.9,
        "description": "中文语境语义理解与意图识别",
    },
    "knowledge_search": {
        "name": "龍魂·知识搜索",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "lh_knowledge_semantic_trigger.py")],
        "triggers": [
            "搜索", "查找", "查一下", "找", "文章", "知识", "资料", "论文",
            "文档", "笔记", "Notion", "CSDN", "博客"
        ],
        "weight": 0.8,
        "description": "三源融合知识搜索（CSDN+Notion+本地）",
    },
    "persona_orchestrator": {
        "name": "人格编排调度",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "lh_persona_orchestrator.py"), "--interactive"],
        "triggers": [
            "人格", "角色", " persona", "调度", "派活", "路由", "谁来做"
        ],
        "weight": 0.7,
        "description": "按任务自动分发到对应人格",
    },
    "kfpp": {
        "name": "KFPP·知识纯净度检测",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "lh_kfpp_engine.py"), "--inspect"],
        "triggers": [
            "KFPP", "kfpp", "知识污染", "知识纯净", "资格化", "垄断",
            "黑名单", "红线", "熔断", "免疫系统", "信任分", "申诉",
            "只有我能教", "必须跟我学", "删除记录", "篡改账本"
        ],
        "weight": 1.0,
        "description": "七因子知识流动纯净度检测与分级处置",
    },
    "safeai": {
        "name": "🛡️ 上下文安全引擎",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "lh_safeai.py"), "--inspect"],
        "triggers": [
            "SQL注入", "黑客", "入侵", "绕过WAF", "payload", "木马", "病毒",
            "炸弹", "制毒", "诈骗", "勒索", "钓鱼", "盗号", "攻击",
            "安全检测", "恶意请求", "L4熔断", "F7", "删记录", "安全审查",
            "能不能黑", "怎么做攻击", "给我工具", "免杀", "反侦察"
        ],
        "weight": 1.0,
        "description": "意图分类+七因子审计+P0-P4分层熔断",
    },
    "judge": {
        "name": "⚖️ 龍魂·公正总裁/审计员",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "lh_judge.py"), "--content"],
        "triggers": [
            "裁决", "审计", "公正总裁", "首席审计员", "你怎么看", "怎么判",
            "公平吗", "合理吗", "违规吗", "触发红线", "如何处理", "调解",
            "争议", "纠纷", "判一下", "评评理", "三色审计", "L1", "L2", "L3", "L4"
        ],
        "weight": 1.0,
        "description": "调用鲲鹏 longhun-judge 模型做公正裁决与审计",
    },
    "seq": {
        "name": "🔄 龍魂·序列执行引擎",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "lh_seq.py"), "--text"],
        "triggers": [
            "序列执行", "流水线", "综合判断", "综合审计", "串起来", "走一遍",
            "审计一下", "裁决一下", "检测一下", "过一遍", "全流程", "联合审计",
            "上下文安全", "知识纯净", "CSDN审计", "公正总裁"
        ],
        "weight": 1.0,
        "description": "SafeAI→KFPP→CSDN→公正总裁 流水线审计",
    },
    "system_eval": {
        "name": "系统健康评估",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "lh_system_eval.py")],
        "triggers": [
            "系统健康", "健康检查", "评估", "状态", "怎么样", "还好吗",
            "体检", "巡检"
        ],
        "weight": 0.7,
        "description": "全面系统健康评分",
    },
    "full_audit": {
        "name": "全系统安全审计",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "lh_full_system_audit.py")],
        "triggers": [
            "审计", "安全检查", "扫描", "漏洞", "合规", "安检", "巡检"
        ],
        "weight": 0.8,
        "description": "一键触发全系统安全扫描",
    },
    "semantic_lie_detector": {
        "name": "语义测谎仪",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "lh_semantic_lie_detector.py")],
        "triggers": [
            "测谎", "话术分析", "骗局", "反诈", "是不是骗", "套路", "忽悠",
            "传销", "营销话术", "真实性"
        ],
        "weight": 0.9,
        "description": "9维话术检测+跨会话DNA追踪",
    },
    "dna_generator": {
        "name": "DNA追溯码生成",
        "cmd": [PYTHON_CMD, str(BIN_DIR / "hetu_luoshu_dna.py")],
        "triggers": [
            "生成DNA", "DNA码", "追溯码", "签名", "确认码", "哈希"
        ],
        "weight": 0.6,
        "description": "为内容生成DNA追溯码",
    },
}


# ──────────────────────────────────────────────
# 语义抽屉加载与匹配
# ──────────────────────────────────────────────

def _load_drawers() -> Dict[str, Any]:
    """加载语义抽屉体系"""
    if DRAWERS_FILE.exists():
        try:
            return json.loads(DRAWERS_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"⚠️ 语义抽屉加载失败: {e}", file=sys.stderr)
    return {}


def _load_semantic_library() -> Dict[str, Any]:
    """加载语义上下文库"""
    if SEMANTIC_LIB.exists():
        try:
            return json.loads(SEMANTIC_LIB.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"⚠️ 语义库加载失败: {e}", file=sys.stderr)
    return {"words": {}}


def _match_drawers(query: str, drawers: Dict[str, Any]) -> Dict[str, List[Dict]]:
    """
    按 L1-L5 逐层匹配抽屉。
    返回 {layer_id: [matched_drawer, ...]}
    """
    query_lower = query.lower()
    routing = {}
    layers = drawers.get("layers", [])

    for layer in layers:
        layer_id = layer.get("layer_id", "L?")
        matched = []
        for drawer in layer.get("drawers", []):
            score = 0.0
            # 关键词匹配
            keywords = drawer.get("keywords", [])
            for kw in keywords:
                if kw.lower() in query_lower:
                    score += len(kw)  # 长词权重更高
            # 别名匹配
            for alias in drawer.get("aliases", []):
                if alias.lower() in query_lower:
                    score += len(alias)

            if score > 0:
                matched.append({
                    "drawer_id": drawer.get("drawer_id"),
                    "name": drawer.get("name"),
                    "score": score,
                    "action": drawer.get("action", ""),
                    "target_bin": drawer.get("target_bin", ""),
                    "target_ipa": drawer.get("target_ipa", []),
                    "default_philosophy": drawer.get("default_philosophy", []),
                    "applicable_layers": drawer.get("applicable_layers", []),
                    "dezi_gate": drawer.get("dezi_gate", ""),
                })

        # 按得分排序
        matched.sort(key=lambda x: x["score"], reverse=True)
        routing[layer_id] = matched[:3]  # 每层最多取前3

    return routing


# ──────────────────────────────────────────────
# 引擎评分
# ──────────────────────────────────────────────

def _score_engines(query: str, routing: Dict[str, List[Dict]]) -> Dict[str, float]:
    """
    综合语义抽屉 L4 动作 + 扩展引擎注册表，给每个引擎打分。
    """
    query_lower = query.lower()
    scores: Dict[str, float] = {}

    # 1. 从语义抽屉 L4 提取动作引擎
    l4_drawers = routing.get("L4", [])
    for d in l4_drawers:
        target = d.get("target_bin", "")
        if target:
            # 用 target_bin 路径作为引擎标识
            engine_key = Path(target).stem
            scores[engine_key] = scores.get(engine_key, 0) + d["score"]

    # 2. 扩展引擎关键词匹配
    for engine_id, meta in EXTRA_ENGINES.items():
        score = 0.0
        for trigger in meta.get("triggers", []):
            if trigger.lower() in query_lower:
                score += len(trigger) * meta.get("weight", 1.0)
        if score > 0:
            scores[engine_id] = scores.get(engine_id, 0) + score

    return scores


def _extract_persona_routing(routing: Dict[str, List[Dict]]) -> List[Dict]:
    """从语义抽屉中提取人格路由推荐"""
    personas = []
    seen = set()
    # L2 领域抽屉带 target_ipa
    for d in routing.get("L2", []):
        for ipa in d.get("target_ipa", []):
            if ipa not in seen:
                seen.add(ipa)
                personas.append({
                    "ipa": ipa,
                    "source": f"L2-{d.get('name', '')}",
                    "reason": d.get("notes", "领域匹配"),
                })
    # L1 情绪抽屉也带 target_ipa
    for d in routing.get("L1", []):
        for ipa in d.get("target_ipa", []):
            if ipa not in seen:
                seen.add(ipa)
                personas.append({
                    "ipa": ipa,
                    "source": f"L1-{d.get('name', '')}",
                    "reason": d.get("emotion_handling", "情绪匹配"),
                })
    return personas


def _extract_actions(routing: Dict[str, List[Dict]]) -> List[Dict]:
    """从 L4 执行抽屉中提取建议动作"""
    actions = []
    for d in routing.get("L4", []):
        action = d.get("action", "")
        if action:
            actions.append({
                "drawer": d.get("name", ""),
                "action": action,
                "target_bin": d.get("target_bin", ""),
                "triggers_decision_card": d.get("triggers_decision_card", False),
                "dna_required": d.get("dna_required", False),
            })
    return actions


def _is_under_project(path: Path) -> bool:
    """判断路径是否位于项目根目录下。"""
    try:
        path.resolve().relative_to(PROJECT_ROOT)
        return True
    except Exception:
        return False


def _resolve_cmd(engine_id: str, routing: Dict[str, List[Dict]]) -> Tuple[Optional[List[str]], Optional[str]]:
    """
    根据引擎ID解析要执行的命令。
    返回 (cmd_list, data_lookup_path):
      - cmd_list: 可执行命令（如果是脚本）
      - data_lookup_path: 数据文件路径（如果是 .json/.md，需要查数据而非执行）

    安全约束：
      - target_bin 必须位于项目根目录下的 bin/ 或 engines/ 中
      - 拒绝绝对路径、~ 展开、.. 跳转、非 .py 可执行文件
    """
    # 优先查扩展引擎表（已限定在项目目录内）
    if engine_id in EXTRA_ENGINES:
        return list(EXTRA_ENGINES[engine_id]["cmd"]), None

    # L4 fallback：抽屉里写的脚本已改名/不存在时，映射到扩展引擎
    if engine_id in L4_FALLBACK:
        fallback_id = L4_FALLBACK[engine_id]
        if fallback_id in EXTRA_ENGINES:
            return list(EXTRA_ENGINES[fallback_id]["cmd"]), None

    allowed_dirs = (PROJECT_ROOT / "bin", PROJECT_ROOT / "engines")

    # 否则从 L4 drawer 的 target_bin 找
    for d in routing.get("L4", []):
        target = d.get("target_bin", "")
        if not target or Path(target).stem != engine_id:
            continue

        # 拒绝明显危险的路径特征
        if target.startswith("/") or target.startswith("~") or ".." in target:
            return None, None

        target_path = Path(target).expanduser()
        if not target_path.is_absolute():
            target_path = PROJECT_ROOT / target_path
        target_path = target_path.resolve()

        if not target_path.exists():
            return None, None

        if target_path.suffix == ".py":
            # 可执行脚本必须位于 bin/ 或 engines/ 下
            try:
                in_allowed = any(target_path.relative_to(ad) for ad in allowed_dirs)
            except Exception:
                in_allowed = False
            if not in_allowed:
                return None, None
            return [PYTHON_CMD, str(target_path)], None

        if target_path.suffix in (".json", ".md", ".txt", ".jsonl"):
            # 数据文件只需位于项目目录内
            if not _is_under_project(target_path):
                return None, None
            return None, str(target_path)

        # 拒绝其他类型文件
        return None, None
    return None, None


def _lookup_data(engine_id: str, data_path: str, query: str) -> Dict[str, Any]:
    """对数据文件（json/md）做查询，而不是执行脚本"""
    start = datetime.now(CST)
    try:
        path = Path(data_path).resolve()
        if not _is_under_project(path):
            return {
                "engine_id": engine_id,
                "name": f"数据查询·{path.name}",
                "status": "error",
                "elapsed": 0,
                "output": "(数据文件必须位于项目目录内)",
            }
        content = path.read_text(encoding="utf-8", errors="ignore")
        query_lower = query.lower()

        # 语义抽屉 JSON：返回匹配的 drawer
        if path.suffix == ".json" and "semantic_drawer" in str(path).lower():
            data = json.loads(content)
            matches = []
            for layer in data.get("layers", []):
                for drawer in layer.get("drawers", []):
                    score = 0
                    texts = (
                        drawer.get("keywords", [])
                        + drawer.get("aliases", [])
                        + [drawer.get("name", ""), drawer.get("action", "")]
                    )
                    for t in texts:
                        if t.lower() in query_lower:
                            score += len(t)
                    if score > 0:
                        matches.append({
                            "drawer_id": drawer.get("drawer_id"),
                            "name": drawer.get("name"),
                            "action": drawer.get("action"),
                            "score": score,
                        })
            matches.sort(key=lambda x: x["score"], reverse=True)
            elapsed = (datetime.now(CST) - start).total_seconds()
            return {
                "engine_id": engine_id,
                "name": "语义抽屉数据查询",
                "status": "ok",
                "elapsed": round(elapsed, 2),
                "output": json.dumps({
                    "文件": str(path),
                    "匹配抽屉": matches[:5],
                }, ensure_ascii=False, indent=2),
            }

        # 通用 md/txt：按行匹配
        matched_lines = []
        for line in content.splitlines():
            line_lower = line.lower()
            if any(kw in line_lower for kw in query_lower.split() if len(kw) >= 2):
                matched_lines.append(line.strip())
                if len(matched_lines) >= 10:
                    break
        elapsed = (datetime.now(CST) - start).total_seconds()
        return {
            "engine_id": engine_id,
            "name": f"数据查询·{path.name}",
            "status": "ok",
            "elapsed": round(elapsed, 2),
            "output": "\n".join(matched_lines) if matched_lines else "(未在文件中找到匹配行)",
        }
    except Exception as e:
        return {
            "engine_id": engine_id,
            "name": f"数据查询·{Path(data_path).name}",
            "status": "exception",
            "elapsed": 0,
            "output": f"(数据查询异常: {e})",
        }


# 已知需要取值的标志；这些标志后面的查询直接作为参数值，不会被 argparse 误解析为选项
_FLAG_VALUE_OPTIONS = {"--inspect", "--content", "--text"}


def _execute_engine(engine_id: str, cmd: List[str], query: str) -> Dict[str, Any]:
    """执行单个引擎，捕获输出。用户查询前加 -- 分隔符，防止 argparse 选项注入。"""
    start = datetime.now(CST)
    try:
        # 把自然语言查询安全地传给引擎：
        # - 若命令最后一个是需要取值的 flag，则查询作为该 flag 的值；
        # - 否则在用户查询前插入 --，将后续参数全部视为位置参数。
        full_cmd = list(cmd)
        if full_cmd and full_cmd[-1] in _FLAG_VALUE_OPTIONS:
            full_cmd.append(query)
        else:
            full_cmd.extend(["--", query])
        proc = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=PROJECT_ROOT,
        )
        elapsed = (datetime.now(CST) - start).total_seconds()
        output = proc.stdout.strip()
        if proc.returncode != 0 and not output:
            output = f"(错误: {proc.stderr.strip()[:200]})"

        return {
            "engine_id": engine_id,
            "name": EXTRA_ENGINES.get(engine_id, {}).get("name", engine_id),
            "status": "ok" if proc.returncode == 0 else "error",
            "returncode": proc.returncode,
            "elapsed": round(elapsed, 2),
            "output": output[:2000],  # 截断避免过长
        }
    except subprocess.TimeoutExpired:
        return {
            "engine_id": engine_id,
            "name": EXTRA_ENGINES.get(engine_id, {}).get("name", engine_id),
            "status": "timeout",
            "elapsed": 120,
            "output": "(执行超时)",
        }
    except Exception as e:
        return {
            "engine_id": engine_id,
            "name": EXTRA_ENGINES.get(engine_id, {}).get("name", engine_id),
            "status": "exception",
            "elapsed": 0,
            "output": f"(异常: {e})",
        }


# ──────────────────────────────────────────────
# 主路由引擎
# ──────────────────────────────────────────────

class NaturalLanguageRouter:
    """自然语言多引擎路由器"""

    def __init__(self):
        self.drawers = _load_drawers()
        self.semantic_lib = _load_semantic_library()

    def route(self, query: str, top_k: int = 3, threshold: float = 2.0) -> Dict[str, Any]:
        """路由自然语言查询到多个引擎"""
        # 1. 语义抽屉分层匹配
        routing = _match_drawers(query, self.drawers)

        # 2. 引擎评分
        scores = _score_engines(query, routing)

        # 3. 超过阈值的引擎中，按得分取 top_k
        sorted_engines = sorted(scores.items(), key=lambda x: -x[1])
        selected = [(eid, score) for eid, score in sorted_engines if score >= threshold][:top_k]

        # 3.5 主导引擎判断：如果第一名得分是第二名的 DOMINANCE_RATIO 倍以上，只执行第一名
        # 这样可以避免次要引擎超时/报错污染主结果
        if len(sorted_engines) >= 2:
            top_eid, top_score = sorted_engines[0]
            second_eid, second_score = sorted_engines[1]
            if top_score >= threshold and second_score > 0 and (top_score / second_score) >= DOMINANCE_RATIO:
                selected = [(top_eid, top_score)]
        elif len(sorted_engines) == 1:
            selected = [(sorted_engines[0][0], sorted_engines[0][1])] if sorted_engines[0][1] >= threshold else []

        # 4. 并行执行（脚本执行 + 数据查询）
        results = []
        skipped = []
        if selected:
            max_workers = min(4, len(selected))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_map = {}
                for eid, score in selected:
                    cmd, data_path = _resolve_cmd(eid, routing)
                    if cmd:
                        future = executor.submit(_execute_engine, eid, cmd, query)
                        future_map[future] = (eid, score)
                    elif data_path:
                        future = executor.submit(_lookup_data, eid, data_path, query)
                        future_map[future] = (eid, score)
                    else:
                        skipped.append(eid)

                for future in as_completed(future_map):
                    eid, score = future_map[future]
                    res = future.result()
                    res["trigger_score"] = round(score, 2)
                    results.append(res)

        # 5. 构造返回
        now = datetime.now(CST)
        output_text = json.dumps({
            "query": query,
            "routing": {k: [m["name"] for m in v] for k, v in routing.items()},
            "engines": [
                {
                    "name": r["name"],
                    "status": r["status"],
                    "score": r["trigger_score"],
                    "output_preview": r["output"][:300] + "..." if len(r["output"]) > 300 else r["output"],
                }
                for r in results
            ],
        }, ensure_ascii=False, indent=2)

        # 人格路由与动作建议
        persona_routing = _extract_persona_routing(routing)
        actions = _extract_actions(routing)

        return {
            "query": query,
            "抽屉路由": routing,
            "人格路由": persona_routing,
            "建议动作": actions,
            "引擎评分": {eid: round(s, 2) for eid, s in sorted_engines[:top_k]},
            "执行结果": sorted(results, key=lambda x: -x["trigger_score"]),
            "命中引擎数": len(results),
            "DNA": f"{DNA_PREFIX}{now.strftime('%Y-%m-%d')}-NATURAL-ROUTER-{hashlib.sha256(output_text.encode()).hexdigest()[:8]}",
            "引擎DNA": ENGINE_DNA,
            "时间戳": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        }


def _format_output(result: Dict[str, Any]) -> str:
    """格式化终端输出"""
    lines = []
    lines.append("")
    lines.append("=" * 64)
    lines.append("  🐉 龍魂·自然语言多引擎路由 v1.0")
    lines.append("=" * 64)
    lines.append(f"\n  📝 输入: {result['query']}")

    # 抽屉路由
    lines.append("\n  🗂️ 语义抽屉路由:")
    for layer_id, matches in result["抽屉路由"].items():
        if matches:
            names = ", ".join([f"{m['name']}({m['score']:.0f})" for m in matches[:2]])
            lines.append(f"    {layer_id}: {names}")

    # 人格路由
    personas = result.get("人格路由", [])
    if personas:
        lines.append("\n  🎭 人格路由推荐:")
        for p in personas[:3]:
            lines.append(f"    → {p['ipa']} ({p['source']})")

    # 建议动作
    actions = result.get("建议动作", [])
    if actions:
        lines.append("\n  🎯 建议执行动作:")
        for a in actions[:3]:
            flag = "🚨需决策卡" if a.get("triggers_decision_card") else ""
            lines.append(f"    • {a['drawer']}: {a['action']} {flag}")

    # 引擎执行结果
    lines.append(f"\n  ⚡ 触发 {result['命中引擎数']} 个引擎:\n")
    for r in result["执行结果"]:
        status_emoji = "✅" if r["status"] == "ok" else "⚠️"
        lines.append(f"  {status_emoji} {r['name']} [score={r['trigger_score']}, {r['elapsed']}s]")
        # 输出摘要（按行取前5行）
        for line in r["output"].splitlines()[:8]:
            lines.append(f"      {line[:80]}")
        if len(r["output"].splitlines()) > 8:
            lines.append("      ...")
        lines.append("")

    lines.append(f"  🧬 {result['DNA']}")
    lines.append("=" * 64)
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·自然语言多引擎路由")
    parser.add_argument("query", type=str, help="自然语言查询")
    parser.add_argument("--top-k", type=int, default=5, help="最多触发引擎数")
    parser.add_argument("--threshold", type=float, default=2.0, help="触发阈值")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")
    args = parser.parse_args()

    router = NaturalLanguageRouter()
    result = router.route(args.query, top_k=args.top_k, threshold=args.threshold)

    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_format_output(result))


if __name__ == "__main__":
    main()
