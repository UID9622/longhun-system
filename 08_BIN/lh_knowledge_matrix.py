#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·知识矩阵数据聚合引擎 v1.0
用途: 聚合所有知识索引 → 生成统一 matrix_data.json → portal/knowledge-matrix 页面数据源
DNA: #龍芯⚡️丙午·丙申·戊申·午时·䷗复-KNOWLEDGE-MATRIX-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
用法: python3 bin/lh_knowledge_matrix.py [--output portal/knowledge-matrix/matrix_data.json]
"""

import json
import os
import re
import sys
import glob
from datetime import datetime
from pathlib import Path

# ─── 路径 ───
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "portal" / "knowledge-matrix" / "matrix_data.json"

TZ_OFFSET = "+08:00"


def scan_protocols(root: Path) -> dict:
    """扫描 01_protocols/ 下全部协议文档"""
    proto_dir = root / "01_protocols"
    result = {"total": 0, "by_category": {}, "items": []}
    if not proto_dir.exists():
        return result

    for f in sorted(proto_dir.rglob("*.md")):
        name = f.stem
        # 分类
        if "PERSONA" in name or "GOVERNANCE" in name:
            cat = "人格治理"
        elif "DEBEN" in name or "AUDIT" in name:
            cat = "审计协议"
        elif "DELIVERY" in name or "STANDARD" in name:
            cat = "交付标准"
        elif "PRIVACY" in name or "SECURITY" in name:
            cat = "隐私安全"
        elif "CNSH" in name or "MATH" in name or "ALGO" in name:
            cat = "算法数学"
        elif "DEPLOY" in name or "CONFIG" in name:
            cat = "部署运维"
        elif "M261" in name or "COVENANT" in name:
            cat = "授权契碑"
        elif "ORIGINALITY" in name or "DECLARATION" in name:
            cat = "原创声明"
        elif "FUSION" in name or "INSTRUCTION" in name:
            cat = "融合指令"
        elif "NO-BACKEND" in name or "SOVEREIGNTY" in name:
            cat = "主权协议"
        elif "HEADER" in name or "TEMPLATE" in name:
            cat = "模板规范"
        else:
            cat = "其他协议"

        size = f.stat().st_size
        try:
            with open(f, "r") as fh:
                first_lines = "".join([fh.readline() for _ in range(5)])
            dna_match = re.search(r'#龍芯⚡️[^\n]+', first_lines)
            dna = dna_match.group(0).strip() if dna_match else ""
        except Exception:
            dna = ""

        item = {
            "name": name,
            "path": str(f.relative_to(root)),
            "category": cat,
            "size_kb": round(size / 1024, 1),
            "dna": dna,
        }
        result["items"].append(item)
        result["by_category"].setdefault(cat, 0)
        result["by_category"][cat] += 1
        result["total"] += 1

    return result


def scan_papers(root: Path) -> dict:
    """扫描 papers/ 论文索引"""
    papers_dir = root / "papers"
    result = {"total": 0, "series": {}, "items": []}
    if not papers_dir.exists():
        return result

    # 读 PAPER_INDEX.md
    idx_path = papers_dir / "PAPER_INDEX.md"
    if idx_path.exists():
        text = idx_path.read_text(encoding="utf-8")
        # 解析系列标题
        series_pattern = re.findall(r'^## ([A-I])\.\s*(.+)$', text, re.MULTILINE)
        for letter, title in series_pattern:
            result["series"][letter] = title.strip()

        # 统计论文条目
        paper_rows = re.findall(r'^\|\s*\d+\s*\|', text, re.MULTILINE)
        result["total"] = len(paper_rows)

    # 扫描实际文件
    pdfs = list(papers_dir.rglob("*.pdf"))
    texs = list(papers_dir.rglob("*.tex"))
    mds = list(papers_dir.rglob("*.md"))

    result["files"] = {
        "pdf": len(pdfs),
        "tex": len(texs),
        "md": len(mds) - 1,  # 减去 PAPER_INDEX.md 本身
    }
    return result


def scan_csdn_sync(root: Path) -> dict:
    """扫描 CSDN 归档索引"""
    idx_path = root / "archive" / "csdn_sync" / "_index.json"
    result = {"total": 0, "by_tag": {}, "latest": []}
    if not idx_path.exists():
        return result

    try:
        data = json.loads(idx_path.read_text(encoding="utf-8"))
        result["total"] = data.get("total_articles", data.get("total", 0))
        by_tag = data.get("by_tag", {})
        result["by_tag"] = {k: v for k, v in sorted(by_tag.items(), key=lambda x: -x[1])[:15]}

        # 最新5篇
        articles = data.get("articles", [])
        latest = sorted(articles, key=lambda a: a.get("publish_time", ""), reverse=True)[:5]
        result["latest"] = [
            {"title": a["title"], "url": a.get("url", ""), "time": a.get("publish_time", "")[:10]}
            for a in latest
        ]
        # 时间范围
        if articles:
            times = [a.get("publish_time", "") for a in articles if a.get("publish_time")]
            times.sort()
            result["time_range"] = f"{times[0][:10]} ~ {times[-1][:10]}" if times else ""
    except Exception:
        pass
    return result


def scan_bin_engines(root: Path) -> dict:
    """扫描引擎脚本"""
    bin_dir = root / "bin"
    result = {"total": 0, "by_domain": {}}
    if not bin_dir.exists():
        return result

    domain_map = {
        "lh_ai": "AI模型", "lh_audit": "审计", "lh_security": "安全", "lh_anti": "防篡改",
        "lh_circuit": "熔断", "lh_deploy": "部署", "lh_gpg": "签名", "lh_cnsh": "CNSH",
        "lh_dna": "DNA", "lh_deben": "德本", "lh_identity": "身份", "lh_trust": "信任",
        "lh_search": "搜索", "lh_memory": "记忆", "lh_persona": "人格", "lh_health": "健康",
        "lh_notion": "Notion", "lh_digital": "数字根", "lh_wuxing": "五行", "lh_bagua": "八卦",
        "lh_flow": "流场", "lh_time": "时间", "lh_video": "视频", "lh_api": "API",
        "lh_xpay": "经济", "lh_agent": "代理", "lh_seven": "七维", "lh_quantum": "量子",
        "lh_anomaly": "异常", "lh_adaptive": "自适应", "lh_active": "主动观察",
        "lh_csdn": "CSDN", "lh_knowledge": "知识", "lh_align": "对齐",
        "lh_whitepaper": "白皮书", "lh_header": "模板", "lh_lora": "训练",
    }

    py_files = list(bin_dir.glob("lh_*.py"))
    result["total"] = len(py_files)
    for f in py_files:
        stem = f.stem
        domain = "其他"
        for prefix, label in domain_map.items():
            if stem.startswith(prefix):
                domain = label
                break
        result["by_domain"].setdefault(domain, 0)
        result["by_domain"][domain] += 1

    return result


def _strip_comment_header(text: str) -> str:
    """剥掉文件开头的注释行（# DNA / # CONFIRM / # SEAL 等），返回可解析 JSON 正文。
    graph_data.json / crawled_knowledge.json 均带龍魂注释头，直接 json.loads 必失败。"""
    lines = text.split("\n")
    start = 0
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("#"):
            continue
        start = i
        break
    return "\n".join(lines[start:])


def _load_json_with_header(path: Path):
    """读取可能带注释头的 JSON 文件。解析失败抛异常由调用方处理。"""
    text = path.read_text(encoding="utf-8")
    return json.loads(_strip_comment_header(text))


def scan_knowledge_graph(root: Path) -> dict:
    """扫描知识图谱 — 优先读 brain/unified_kg.db，回退 graph_data.json，双无则报数据源缺失。
    铁律 #IRON-MISSING-SOURCE-NEVER-REPORT-ZERO-v1.0：扫不到报「数据源缺失」，绝不报 0 冒充真值。"""
    kg_dir = root / "03_知識圖譜"
    result = {
        "total_nodes": 0, "total_edges": 0, "node_types": {}, "crawled_knowledge": {},
        "source": None, "source_path": None, "source_time": None,
        "source_status": "missing", "data_source_missing": True,
    }

    # 1) 优先：brain/unified_kg.db（知识图谱 v2 引擎真数据）
    kg_db = root / "brain" / "unified_kg.db"
    if kg_db.exists():
        try:
            import sqlite3
            con = sqlite3.connect(f"file:{kg_db}?mode=ro", uri=True, timeout=3)
            cur = con.cursor()
            nodes = edges = 0
            node_types = {}
            try:
                nodes = cur.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
            except Exception:
                pass
            try:
                edges = cur.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
            except Exception:
                pass
            try:
                for nt, n in cur.execute("SELECT type, COUNT(*) FROM nodes GROUP BY type").fetchall():
                    node_types[nt] = n
            except Exception:
                pass
            con.close()
            result.update({
                "total_nodes": nodes, "total_edges": edges, "node_types": node_types,
                "source": "unified_kg.db",
                "source_path": str(kg_db.relative_to(root)),
                "source_time": datetime.now().isoformat(timespec="seconds"),
                "source_status": "ok" if nodes or edges else "empty_db",
                "data_source_missing": False,
            })
        except Exception as e:
            result.update({
                "source": "unified_kg.db",
                "source_path": str(kg_db.relative_to(root)),
                "source_time": datetime.now().isoformat(timespec="seconds"),
                "source_status": f"error: {e}",
            })
            return result

    # 2) 回退：graph_data.json（带注释头，需先剥头）
    gd_path = kg_dir / "graph_data.json"
    if (result["source_status"] == "missing" or
            (result["total_nodes"] == 0 and result["total_edges"] == 0)) and gd_path.exists():
        try:
            gd = _load_json_with_header(gd_path)
            raw_nodes = gd.get("nodes", [])
            result["total_nodes"] = len(raw_nodes)
            result["total_edges"] = len(gd.get("edges", []))
            # nodes 元素可能混有字符串（非 dict），isinstance 保护后统计
            for n in raw_nodes:
                if not isinstance(n, dict):
                    continue
                nt = n.get("type", "unknown")
                result["node_types"].setdefault(nt, 0)
                result["node_types"][nt] += 1
            result.update({
                "source": "graph_data.json",
                "source_path": str(gd_path.relative_to(root)),
                "source_time": datetime.now().isoformat(timespec="seconds"),
                "source_status": "ok",
                "data_source_missing": False,
            })
        except Exception as e:
            result["source_status"] = f"error_graph_data: {e}"

    # 3) crawled_knowledge.json（带注释头，剥头后解析；保持原逻辑）
    ck_path = kg_dir / "crawled_knowledge.json"
    if ck_path.exists():
        try:
            ck = _load_json_with_header(ck_path)

            def count_recursive(obj):
                if isinstance(obj, dict):
                    return sum(count_recursive(v) for v in obj.values())
                elif isinstance(obj, list):
                    return len(obj) + sum(count_recursive(v) for v in obj)
                return 0

            result["crawled_knowledge"] = {
                "domains": list(ck.keys()) if isinstance(ck, dict) else [],
                "total_items": count_recursive(ck),
            }
        except Exception:
            pass

    return result


def scan_portal_pages(root: Path) -> dict:
    """扫描门户子页面"""
    portal_dir = root / "portal"
    result = {"total": 0, "pages": []}
    if not portal_dir.exists():
        return result

    for subdir in sorted(portal_dir.iterdir()):
        if subdir.is_dir() and not subdir.name.startswith("."):
            html = subdir / "index.html"
            if html.exists():
                # 读标题
                try:
                    text = html.read_text(encoding="utf-8")
                    title_match = re.search(r'<title>(.+?)</title>', text)
                    title = title_match.group(1) if title_match else subdir.name
                    # 清理解析
                    title = re.sub(r'🐉|龍魂[·\s]*', '', title).strip()
                except Exception:
                    title = subdir.name

                result["pages"].append({
                    "name": subdir.name,
                    "title": title,
                    "path": f"portal/{subdir.name}/",
                })
                result["total"] += 1

    return result


def scan_external_repos(root: Path) -> dict:
    """扫描外部仓库索引"""
    result = {"gitee": 0, "github": 0, "total": 0}

    gitee_idx = root / "docs" / "GITEE_REPOS_INDEX.md"
    if gitee_idx.exists():
        text = gitee_idx.read_text(encoding="utf-8")
        result["gitee"] = len(re.findall(r'^\|\s*\d+\s*\|', text, re.MULTILINE))

    github_idx = root / "docs" / "GITHUB_REPOS_INDEX.md"
    if github_idx.exists():
        text = github_idx.read_text(encoding="utf-8")
        result["github"] = len(re.findall(r'^\|\s*\d+\s*\|', text, re.MULTILINE))

    result["total"] = result["gitee"] + result["github"]
    return result


def scan_data_sources(root: Path) -> dict:
    """扫描数据源 — 索引缺失报「数据源缺失」不报 0（铁律 #IRON-MISSING-SOURCE-NEVER-REPORT-ZERO）"""
    result = {
        "total": 0,
        "source_status": "missing",
        "source_path": "data/sources/index-for-codebuddy.md",
        "data_source_missing": True,
    }
    src_idx = root / "data" / "sources" / "index-for-codebuddy.md"
    if src_idx.exists():
        text = src_idx.read_text(encoding="utf-8")
        result["total"] = len(re.findall(r'^\|\s*\d+\s*\|', text, re.MULTILINE))
        result["source_status"] = "ok"
        result["data_source_missing"] = False
    return result


def scan_system_state(root: Path) -> dict:
    """读取系统状态"""
    result = {}
    state_path = root / "STATE.md"
    if state_path.exists():
        text = state_path.read_text(encoding="utf-8")
        # 提取模型信息
        model_match = re.search(r'v(\d+\.\d+).*?(Qwen[\d.]+|Llama[\d.-]+)', text)
        if model_match:
            result["current_model"] = f"v{model_match.group(1)} ({model_match.group(2)})"
        # 提取引擎数
        eng_match = re.search(r'(\d+)\s*(?:个|\s+engines|个引擎)', text)
        if eng_match:
            result["engine_count"] = int(eng_match.group(1))
    return result


def build_matrix(root: Path) -> dict:
    """构建完整知识矩阵数据"""
    now = datetime.now()
    matrix = {
        "dna": "#龍芯⚡️丙午·丙申·戊申·午时·䷗复-KNOWLEDGE-MATRIX-v1.0",
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "generated_at": now.isoformat(),
        "generated_by": "lh_knowledge_matrix.py v1.0",
        "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",

        # 各维度数据
        "protocols": scan_protocols(root),
        "papers": scan_papers(root),
        "csdn": scan_csdn_sync(root),
        "engines": scan_bin_engines(root),
        "knowledge_graph": scan_knowledge_graph(root),
        "portal": scan_portal_pages(root),
        "external_repos": scan_external_repos(root),
        "data_sources": scan_data_sources(root),
        "system_state": scan_system_state(root),

        # 汇总统计
        "summary": {
            "protocols": 0,
            "papers": 0,
            "csdn_articles": 0,
            "engines": 0,
            "kg_nodes": 0,
            "kg_edges": 0,
            "portal_pages": 0,
            "external_repos": 0,
            "data_sources": 0,
        },
    }

    # 填汇总
    s = matrix["summary"]
    s["protocols"] = matrix["protocols"]["total"]
    s["papers"] = matrix["papers"]["total"]
    s["csdn_articles"] = matrix["csdn"]["total"]
    s["engines"] = matrix["engines"]["total"]
    s["kg_nodes"] = matrix["knowledge_graph"]["total_nodes"]
    s["kg_edges"] = matrix["knowledge_graph"]["total_edges"]
    s["portal_pages"] = matrix["portal"]["total"]
    s["external_repos"] = matrix["external_repos"]["total"]
    s["data_sources"] = matrix["data_sources"]["total"]
    s["grand_total"] = sum(s.values())

    return matrix


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·知识矩阵数据聚合")
    parser.add_argument("--output", "-o", default=str(DEFAULT_OUTPUT), help="输出JSON路径")
    parser.add_argument("--pretty", action="store_true", help="美化输出")
    args = parser.parse_args()

    print("🐉 龍魂·知识矩阵数据聚合引擎 v1.0")
    print(f"   扫描根目录: {ROOT}")
    print(f"   输出路径: {args.output}")

    matrix = build_matrix(ROOT)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        if args.pretty:
            json.dump(matrix, f, ensure_ascii=False, indent=2)
        else:
            json.dump(matrix, f, ensure_ascii=False)

    print(f"\n   ✅ 聚合完成")
    print(f"   总知识项: {matrix['summary']['grand_total']}")
    print(f"   协议: {matrix['summary']['protocols']}")
    print(f"   论文: {matrix['summary']['papers']}")
    print(f"   CSDN: {matrix['summary']['csdn_articles']}")
    print(f"   引擎: {matrix['summary']['engines']}")
    print(f"   图谱节点: {matrix['summary']['kg_nodes']}")
    print(f"   图谱边: {matrix['summary']['kg_edges']}")
    print(f"   门户页: {matrix['summary']['portal_pages']}")
    print(f"   外部仓库: {matrix['summary']['external_repos']}")
    print(f"   数据源: {matrix['summary']['data_sources']}")


if __name__ == "__main__":
    main()
