#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂系统 · 关联矩阵扫描器
Longhun Relation Matrix Scanner v1.0

功能：
- 扫描指定目录所有文件
- 提取DNA追溯码、类型标记、版本号
- 自动建立文件间关联（同DNA、同类型、版本依赖、关键词匹配）
- 输出可视化JSON（力导向图格式）
- 标记孤立文件（无关联>30天）
- 支持增量扫描（断点续传）
- 多线程处理（默认4线程）
- 完整日志追踪

DNA格式支持：
- #龍芯⚡️YYYY-MM-DD-项目-版本
- #龍魂⚡️YYYY-MM-DD-项目-版本
- #CONFIRM🌌9622-ONLY-ONCE🧬XXXX-XXXX

作者：龍芯北辰·UID9622
协议：龍魂开源公约 v2.0
"""

import os
import re
import json
import hashlib
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any
import logging

# ═══════════════════════════════════════════════════════════
# 配置区
# ═══════════════════════════════════════════════════════════

CONFIG = {
    "scan_root": "~/longhun-system",  # 修改为你的实际路径
    "output_dir": "~/longhun-system/.matrix",
    "checkpoint_file": "~/.longhun_matrix_checkpoint.json",
    "log_file": "~/.longhun_matrix_scan.log",
    "max_workers": 4,
    "batch_size": 1000,
    "isolation_threshold_days": 30,
    "dna_patterns": [
        r"#龍芯⚡️(\d{4}-\d{2}-\d{2})-([^-]+)-v([\d.]+)",
        r"#龍魂⚡️(\d{4}-\d{2}-\d{2})-([^-]+)-v([\d.]+)",
        r"#CONFIRM🌌9622-ONLY-ONCE🧬([A-Z0-9-]+)",
    ],
    "type_markers": ["文", "规", "设", "资", "图", "录", "锚", "核"],
    "relation_rules": {
        "same_dna": {"weight": 1.0, "color": "#FF0000"},      # 同DNA强关联
        "same_type": {"weight": 0.3, "color": "#00FF00"},     # 同类型弱关联
        "version_dep": {"weight": 0.8, "color": "#0000FF"},   # 版本依赖
        "keyword_match": {"weight": 0.2, "color": "#FFFF00"}, # 关键词匹配
        "temporal": {"weight": 0.4, "color": "#FF00FF"},      # 时间邻近
    }
}

# ═══════════════════════════════════════════════════════════
# 日志配置
# ═══════════════════════════════════════════════════════════

def setup_logging():
    log_path = os.path.expanduser(CONFIG["log_file"])
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("LonghunMatrix")

logger = setup_logging()

# ═══════════════════════════════════════════════════════════
# DNA提取器
# ═══════════════════════════════════════════════════════════

class DNAExtractor:
    def __init__(self):
        self.patterns = [re.compile(p) for p in CONFIG["dna_patterns"]]

    def extract(self, content: str, filename: str) -> Dict[str, Any]:
        """从文件内容和文件名提取DNA信息"""
        result = {
            "filename": filename,
            "dna_codes": [],
            "type_marker": None,
            "version": None,
            "date": None,
            "project": None,
            "confirm_code": None,
            "is_valid": False
        }

        # 从内容提取
        for pattern in self.patterns:
            matches = pattern.findall(content)
            for match in matches:
                if isinstance(match, tuple):
                    if len(match) == 3:  # DNA追溯码
                        date_str, project, version = match
                        result["dna_codes"].append({
                            "type": "dna_trace",
                            "date": date_str,
                            "project": project,
                            "version": version,
                            "raw": f"#龍芯⚡️{date_str}-{project}-v{version}"
                        })
                        result["date"] = date_str
                        result["project"] = project
                        result["version"] = version
                        result["is_valid"] = True
                    elif len(match) == 1:  # CONFIRM码
                        result["confirm_code"] = match[0]
                else:
                    result["confirm_code"] = match

        # 从文件名提取类型标记
        for marker in CONFIG["type_markers"]:
            if marker in filename:
                result["type_marker"] = marker
                break

        # 从文件名提取版本号
        version_match = re.search(r'v([\d.]+)', filename)
        if version_match:
            result["version"] = version_match.group(1)

        return result

# ═══════════════════════════════════════════════════════════
# 文件扫描器
# ═══════════════════════════════════════════════════════════

class FileScanner:
    def __init__(self, root_path: str):
        self.root = Path(os.path.expanduser(root_path))
        self.extractor = DNAExtractor()
        self.checkpoint = self._load_checkpoint()
        self.scanned_files: Set[str] = set(self.checkpoint.get("scanned", []))
        self.results: List[Dict] = self.checkpoint.get("results", [])

    def _load_checkpoint(self) -> Dict[str, Any]:
        cp_path = os.path.expanduser(CONFIG["checkpoint_file"])
        if os.path.exists(cp_path):
            try:
                with open(cp_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"检查点加载失败: {e}，重新开始")
        return {"scanned": [], "results": [], "last_scan": None}

    def _save_checkpoint(self):
        cp_path = os.path.expanduser(CONFIG["checkpoint_file"])
        os.makedirs(os.path.dirname(cp_path), exist_ok=True)
        with open(cp_path, 'w', encoding='utf-8') as f:
            json.dump({
                "scanned": list(self.scanned_files),
                "results": self.results,
                "last_scan": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        logger.info(f"检查点已保存: {len(self.scanned_files)} 文件")

    def _scan_single_file(self, file_path: Path) -> Optional[Dict]:
        """扫描单个文件"""
        try:
            # 跳过二进制文件和大文件
            if file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB
                return None

            # 读取前1000行或前100KB
            content = ""
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f):
                    if i >= 1000:
                        break
                    content += line
                    if len(content) > 100 * 1024:
                        break

            dna_info = self.extractor.extract(content, str(file_path.relative_to(self.root)))
            dna_info["file_size"] = file_path.stat().st_size
            dna_info["modified_time"] = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            dna_info["file_hash"] = hashlib.md5(str(file_path).encode()).hexdigest()[:8]

            return dna_info

        except Exception as e:
            logger.debug(f"扫描失败 {file_path}: {e}")
            return None

    def scan(self, incremental: bool = True) -> List[Dict]:
        """执行扫描"""
        logger.info(f"开始扫描: {self.root}")

        # 收集所有文件
        all_files = []
        for ext in ['.md', '.py', '.js', '.html', '.sh', '.txt', '.json', '.yaml', '.yml']:
            all_files.extend(self.root.rglob(f'*{ext}'))

        logger.info(f"发现 {len(all_files)} 个候选文件")

        # 过滤已扫描（增量模式）
        if incremental:
            new_files = [f for f in all_files if str(f) not in self.scanned_files]
            logger.info(f"增量模式: {len(new_files)} 个新文件待扫描")
        else:
            new_files = all_files
            self.scanned_files.clear()
            self.results.clear()

        # 多线程扫描
        batch_size = CONFIG["batch_size"]
        total_batches = (len(new_files) + batch_size - 1) // batch_size

        for batch_idx in range(total_batches):
            batch = new_files[batch_idx * batch_size : (batch_idx + 1) * batch_size]
            logger.info(f"处理批次 {batch_idx + 1}/{total_batches}: {len(batch)} 文件")

            with ThreadPoolExecutor(max_workers=CONFIG["max_workers"]) as executor:
                futures = {executor.submit(self._scan_single_file, f): f for f in batch}

                for future in as_completed(futures):
                    file_path = futures[future]
                    self.scanned_files.add(str(file_path))

                    try:
                        result = future.result()
                        if result:
                            self.results.append(result)
                    except Exception as e:
                        logger.error(f"处理失败 {file_path}: {e}")

            # 每批次保存检查点
            self._save_checkpoint()

        logger.info(f"扫描完成: {len(self.results)} 个有效文件")
        return self.results

# ═══════════════════════════════════════════════════════════
# 关联矩阵构建器
# ═══════════════════════════════════════════════════════════

class RelationMatrix:
    def __init__(self, nodes: List[Dict]):
        self.nodes = nodes
        self.edges: List[Dict] = []
        self.isolated: List[Dict] = []

    def build(self) -> Dict[str, Any]:
        """构建关联矩阵"""
        logger.info("构建关联矩阵...")

        # 建立索引
        dna_index: Dict[str, List[int]] = {}  # DNA -> 节点索引列表
        type_index: Dict[str, List[int]] = {}  # 类型 -> 节点索引列表
        project_index: Dict[str, List[int]] = {}  # 项目 -> 节点索引列表

        for i, node in enumerate(self.nodes):
            for dna in node.get("dna_codes", []):
                dna_key = dna.get("raw", "")
                if dna_key:
                    dna_index.setdefault(dna_key, []).append(i)

            type_marker = node.get("type_marker")
            if type_marker:
                type_index.setdefault(type_marker, []).append(i)

            project = node.get("project")
            if project:
                project_index.setdefault(project, []).append(i)

        # 生成边
        edge_set: Set[Tuple[int, int, str]] = set()

        # 1. 同DNA关联（最强）
        for dna_key, indices in dna_index.items():
            if len(indices) > 1:
                for i in range(len(indices)):
                    for j in range(i + 1, len(indices)):
                        a, b = indices[i], indices[j]
                        if (a, b, "same_dna") not in edge_set and (b, a, "same_dna") not in edge_set:
                            self.edges.append({
                                "source": a,
                                "target": b,
                                "relation": "same_dna",
                                "weight": CONFIG["relation_rules"]["same_dna"]["weight"],
                                "color": CONFIG["relation_rules"]["same_dna"]["color"],
                                "label": f"同DNA: {dna_key[:20]}..."
                            })
                            edge_set.add((a, b, "same_dna"))

        # 2. 同类型关联
        for type_marker, indices in type_index.items():
            if len(indices) > 1:
                for i in range(len(indices)):
                    for j in range(i + 1, len(indices)):
                        a, b = indices[i], indices[j]
                        if (a, b, "same_type") not in edge_set and (b, a, "same_type") not in edge_set:
                            self.edges.append({
                                "source": a,
                                "target": b,
                                "relation": "same_type",
                                "weight": CONFIG["relation_rules"]["same_type"]["weight"],
                                "color": CONFIG["relation_rules"]["same_type"]["color"],
                                "label": f"同类型: {type_marker}"
                            })
                            edge_set.add((a, b, "same_type"))

        # 3. 同项目关联
        for project, indices in project_index.items():
            if len(indices) > 1:
                for i in range(len(indices)):
                    for j in range(i + 1, len(indices)):
                        a, b = indices[i], indices[j]
                        if (a, b, "same_project") not in edge_set and (b, a, "same_project") not in edge_set:
                            # 检查版本依赖
                            ver_a = self.nodes[a].get("version")
                            ver_b = self.nodes[b].get("version")
                            if ver_a and ver_b:
                                relation = "version_dep" if self._is_version_related(ver_a, ver_b) else "keyword_match"
                            else:
                                relation = "keyword_match"

                            self.edges.append({
                                "source": a,
                                "target": b,
                                "relation": relation,
                                "weight": CONFIG["relation_rules"][relation]["weight"],
                                "color": CONFIG["relation_rules"][relation]["color"],
                                "label": f"同项目: {project}"
                            })
                            edge_set.add((a, b, relation))

        # 4. 时间邻近关联
        for i, node_a in enumerate(self.nodes):
            date_a = node_a.get("date")
            if not date_a:
                continue
            for j, node_b in enumerate(self.nodes[i+1:], i+1):
                date_b = node_b.get("date")
                if not date_b:
                    continue
                try:
                    da = datetime.strptime(date_a, "%Y-%m-%d")
                    db = datetime.strptime(date_b, "%Y-%m-%d")
                    if abs((da - db).days) <= 7:  # 7天内
                        if (i, j, "temporal") not in edge_set and (j, i, "temporal") not in edge_set:
                            self.edges.append({
                                "source": i,
                                "target": j,
                                "relation": "temporal",
                                "weight": CONFIG["relation_rules"]["temporal"]["weight"],
                                "color": CONFIG["relation_rules"]["temporal"]["color"],
                                "label": f"时间邻近: {date_a} ~ {date_b}"
                            })
                            edge_set.add((i, j, "temporal"))
                except:
                    pass

        # 标记孤立文件
        connected = set()
        for edge in self.edges:
            connected.add(edge["source"])
            connected.add(edge["target"])

        for i, node in enumerate(self.nodes):
            if i not in connected:
                node["is_isolated"] = True
                node["isolation_days"] = self._calc_isolation_days(node)
                self.isolated.append(node)
            else:
                node["is_isolated"] = False
                node["connection_count"] = sum(1 for e in self.edges if e["source"] == i or e["target"] == i)

        logger.info(f"关联矩阵构建完成: {len(self.nodes)} 节点, {len(self.edges)} 边, {len(self.isolated)} 孤立")

        return {
            "nodes": self.nodes,
            "edges": self.edges,
            "isolated": self.isolated,
            "stats": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "isolated_count": len(self.isolated),
                "relation_types": {r: sum(1 for e in self.edges if e["relation"] == r) for r in CONFIG["relation_rules"].keys()}
            }
        }

    def _is_version_related(self, v1: str, v2: str) -> bool:
        """判断版本是否相关（如v1.0和v2.0）"""
        try:
            parts1 = [int(x) for x in v1.split('.')]
            parts2 = [int(x) for x in v2.split('.')]
            # 主版本相同或相差1
            return abs(parts1[0] - parts2[0]) <= 1
        except:
            return False

    def _calc_isolation_days(self, node: Dict[str, Any]) -> int:
        """计算孤立天数"""
        modified = node.get("modified_time")
        if modified:
            try:
                mod_time = datetime.fromisoformat(modified)
                return (datetime.now() - mod_time).days
            except:
                pass
        return 999  # 未知

# ═══════════════════════════════════════════════════════════
# 可视化输出器
# ═══════════════════════════════════════════════════════════

class Visualizer:
    def __init__(self, matrix_data: Dict[str, Any]):
        self.data = matrix_data

    def to_force_graph_json(self) -> Dict[str, Any]:
        """输出力导向图格式（兼容D3.js/ECharts）"""
        nodes = []
        for i, node in enumerate(self.data["nodes"]):
            nodes.append({
                "id": i,
                "name": node["filename"],
                "value": node.get("file_size", 0),
                "category": node.get("type_marker", "未知"),
                "symbolSize": max(10, min(50, node.get("file_size", 0) / 1024)),
                "label": {
                    "show": True,
                    "formatter": node.get("project", node["filename"])[:20]
                },
                "itemStyle": {
                    "color": "#FF0000" if node.get("is_isolated") else "#00FF00"
                },
                "dna": node.get("dna_codes", []),
                "isolated": node.get("is_isolated", False),
                "isolation_days": node.get("isolation_days", 0)
            })

        edges = []
        for edge in self.data["edges"]:
            edges.append({
                "source": edge["source"],
                "target": edge["target"],
                "value": edge["weight"],
                "lineStyle": {
                    "color": edge["color"],
                    "width": edge["weight"] * 3
                },
                "label": {
                    "show": True,
                    "formatter": edge["label"]
                }
            })

        return {
            "nodes": nodes,
            "edges": edges,
            "categories": [{"name": t} for t in CONFIG["type_markers"]],
            "stats": self.data["stats"]
        }

    def save(self, output_dir: str):
        """保存所有输出文件"""
        out_path = Path(os.path.expanduser(output_dir))
        out_path.mkdir(parents=True, exist_ok=True)

        # 1. 力导向图JSON
        force_graph = self.to_force_graph_json()
        with open(out_path / "force_graph.json", 'w', encoding='utf-8') as f:
            json.dump(force_graph, f, ensure_ascii=False, indent=2)

        # 2. 完整矩阵数据
        with open(out_path / "matrix_full.json", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        # 3. 孤立文件报告
        isolated = self.data.get("isolated", [])
        with open(out_path / "isolated_files.md", 'w', encoding='utf-8') as f:
            f.write("# 龍魂系统 · 孤立文件报告\n\n")
            f.write(f"> 生成时间: {datetime.now().isoformat()}\n")
            f.write(f"> 孤立文件数: {len(isolated)}\n\n")

            for node in sorted(isolated, key=lambda x: x.get("isolation_days", 0), reverse=True):
                f.write(f"## {node['filename']}\n\n")
                f.write(f"- 类型标记: {node.get('type_marker', '无')}\n")
                f.write(f"- 版本: {node.get('version', '无')}\n")
                f.write(f"- 修改时间: {node.get('modified_time', '未知')}\n")
                f.write(f"- 孤立天数: {node.get('isolation_days', '未知')}\n")
                f.write(f"- 文件大小: {node.get('file_size', 0)} bytes\n")
                if node.get("dna_codes"):
                    f.write(f"- DNA: {node['dna_codes'][0].get('raw', '无')}\n")
                f.write("\n---\n\n")

        # 4. 统计摘要
        stats = self.data["stats"]
        with open(out_path / "summary.md", 'w', encoding='utf-8') as f:
            f.write("# 龍魂系统 · 关联矩阵摘要\n\n")
            f.write(f"- 总节点: {stats['total_nodes']}\n")
            f.write(f"- 总关联: {stats['total_edges']}\n")
            f.write(f"- 孤立文件: {stats['isolated_count']}\n")
            f.write("\n## 关联类型分布\n\n")
            for rel_type, count in stats["relation_types"].items():
                f.write(f"- {rel_type}: {count}\n")

        logger.info(f"输出已保存: {out_path}")

# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════

def main():
    logger.info("=" * 60)
    logger.info("龍魂系统 · 关联矩阵扫描器 v1.0")
    logger.info("DNA: #龍芯⚡️2026-07-01-RELATION-MATRIX-v1.0")
    logger.info("=" * 60)

    # 扫描
    scanner = FileScanner(CONFIG["scan_root"])
    nodes = scanner.scan(incremental=True)

    # 构建矩阵
    matrix = RelationMatrix(nodes)
    data = matrix.build()

    # 可视化输出
    viz = Visualizer(data)
    viz.save(CONFIG["output_dir"])

    logger.info("全部完成！")
    logger.info(f"查看结果: {os.path.expanduser(CONFIG['output_dir'])}")

if __name__ == "__main__":
    main()
