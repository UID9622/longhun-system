#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LONGHUN_DNA_REPAIR-v1.0-fb202a25
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂系统 · DNA修复与补全工具
Longhun DNA Repair Tool v1.0

功能：
- 扫描孤立文件（无DNA或DNA不完整）
- 基于文件名/内容自动推断DNA
- 批量修复：补全DNA、统一命名、建立关联
- 支持预览模式（先看不改）
- 支持撤销（备份原文件）
- 多线程处理
- 完整日志

修复规则：
- 无DNA → 根据文件名生成DNA
- DNA格式错误 → 按CNSH规范修正
- 孤立>30天 → 标记待处理
- 类型标记缺失 → 根据内容推断

作者：龍芯北辰·UID9622
协议：龍魂开源公约 v2.0
"""

import os
import re
import json
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging

# ═══════════════════════════════════════════════════════════
# 配置区
# ═══════════════════════════════════════════════════════════

CONFIG = {
    "scan_root": "~/longhun-system",
    "backup_dir": "~/.longhun_dna_backup",
    "log_file": "~/.longhun_dna_repair.log",
    "max_workers": 4,
    "preview_mode": True,  # True=只预览不修改，False=执行修复
    "isolation_threshold_days": 30,
    "dna_template": "#龍芯⚡️{date}-{project}-v{version}",
    "confirm_template": "#CONFIRM🌌9622-ONLY-ONCE🧬{random}",
    "type_inference_rules": {
        ".md": "文",
        ".py": "设",
        ".js": "设",
        ".html": "设",
        ".sh": "录",
        ".txt": "文",
        ".json": "规",
        ".yaml": "规",
        ".yml": "规",
        ".png": "图",
        ".jpg": "图",
        ".svg": "图",
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
    return logging.getLogger("LonghunDNARepair")

logger = setup_logging()

# ═══════════════════════════════════════════════════════════
# DNA修复引擎
# ═══════════════════════════════════════════════════════════

class DNARepairEngine:
    def __init__(self):
        self.dna_pattern = re.compile(r"#龍[芯魂]⚡️(\d{4}-\d{2}-\d{2})-([^-]+)-v([\d.]+)")
        self.confirm_pattern = re.compile(r"#CONFIRM🌌9622-ONLY-ONCE🧬([A-Z0-9-]+)")

    def analyze(self, file_path: Path, content: str) -> Dict[str, Any]:
        """分析文件DNA状态"""
        result = {
            "file_path": str(file_path),
            "filename": file_path.name,
            "has_dna": False,
            "has_confirm": False,
            "dna_valid": False,
            "confirm_valid": False,
            "dna_codes": [],
            "issues": [],
            "suggested_fixes": [],
            "type_marker": None,
            "project_name": None,
            "version": None,
        }

        # 检查现有DNA
        dna_matches = self.dna_pattern.findall(content)
        if dna_matches:
            result["has_dna"] = True
            for date, project, version in dna_matches:
                result["dna_codes"].append({
                    "date": date,
                    "project": project,
                    "version": version
                })
            result["dna_valid"] = True
        else:
            result["issues"].append("缺少DNA追溯码")

        # 检查CONFIRM码
        confirm_matches = self.confirm_pattern.findall(content)
        if confirm_matches:
            result["has_confirm"] = True
            result["confirm_valid"] = True
        else:
            result["issues"].append("缺少CONFIRM确认码")

        # 推断类型标记
        ext = file_path.suffix.lower()
        result["type_marker"] = CONFIG["type_inference_rules"].get(ext, "文")

        # 推断项目名称
        result["project_name"] = self._infer_project(file_path, content)

        # 推断版本
        ver_match = re.search(r'v([\d.]+)', file_path.name)
        result["version"] = ver_match.group(1) if ver_match else "1.0"

        # 生成建议修复
        if not result["has_dna"]:
            result["suggested_fixes"].append({
                "type": "add_dna",
                "content": self._generate_dna(file_path, result),
                "reason": "文件无DNA追溯码，根据路径和内容推断"
            })

        if not result["has_confirm"]:
            result["suggested_fixes"].append({
                "type": "add_confirm",
                "content": self._generate_confirm(),
                "reason": "文件无CONFIRM确认码"
            })

        # 检查命名规范
        if not any(marker in file_path.name for marker in ["文", "规", "设", "资", "图", "录", "锚", "核"]):
            result["issues"].append("文件名缺少CNSH类型标记")
            result["suggested_fixes"].append({
                "type": "rename",
                "new_name": self._suggest_rename(file_path, result),
                "reason": "按CNSH规范添加类型标记"
            })

        return result

    def _infer_project(self, file_path: Path, content: str) -> str:
        """推断项目名称"""
        # 从路径推断
        parts = file_path.parts
        for part in reversed(parts[:-1]):
            if part not in ["longhun-system", "src", "docs", "assets", "backup"]:
                return part[:20]  # 限制长度

        # 从内容推断
        title_match = re.search(r"#+\s*(.+)", content[:500])
        if title_match:
            return title_match.group(1).strip()[:20]

        # 从文件名推断
        name = file_path.stem
        # 移除常见后缀
        name = re.sub(r'[_-]v[\d.]+', '', name)
        name = re.sub(r'[_-]\d{4}[-\d]*', '', name)
        return name[:20] or "未命名"

    def _generate_dna(self, file_path: Path, analysis: Dict[str, Any]) -> str:
        """生成DNA追溯码"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        project = analysis["project_name"] or "未命名"
        version = analysis["version"] or "1.0"
        return CONFIG["dna_template"].format(
            date=date_str,
            project=project,
            version=version
        )

    def _generate_confirm(self) -> str:
        """生成CONFIRM码"""
        import random
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        random_part = "".join(random.choices(chars, k=8))
        return CONFIG["confirm_template"].format(random=random_part)

    def _suggest_rename(self, file_path: Path, analysis: Dict[str, Any]) -> str:
        """建议新文件名"""
        type_marker = analysis["type_marker"] or "文"
        project = analysis["project_name"] or "未命名"
        version = analysis["version"] or "1.0"
        ext = file_path.suffix

        # CNSH格式: 【类型】·【项目】·【龍】·v版本.扩展名
        new_name = f"{type_marker}·{project}·龍·v{version}{ext}"
        # 清理非法字符
        new_name = re.sub(r'[\/:*?"<>|]', '_', new_name)
        return new_name

# ═══════════════════════════════════════════════════════════
# 文件修复器
# ═══════════════════════════════════════════════════════════

class FileRepairer:
    def __init__(self, preview: bool = True):
        self.preview = preview
        self.backup_dir = Path(os.path.expanduser(CONFIG["backup_dir"]))
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.repaired_count = 0
        self.failed_count = 0

    def backup(self, file_path: Path) -> Path:
        """备份原文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.bak"
        backup_path = self.backup_dir / backup_name
        shutil.copy2(file_path, backup_path)
        return backup_path

    def repair(self, file_path: Path, analysis: Dict[str, Any]) -> bool:
        """执行修复"""
        if self.preview:
            logger.info(f"[预览] {file_path.name}")
            for fix in analysis["suggested_fixes"]:
                logger.info(f"  → 建议: {fix['type']} - {fix['reason']}")
                if fix['type'] == 'add_dna':
                    logger.info(f"     DNA: {fix['content']}")
                elif fix['type'] == 'add_confirm':
                    logger.info(f"     CONFIRM: {fix['content']}")
                elif fix['type'] == 'rename':
                    logger.info(f"     新名: {fix['new_name']}")
            return True

        # 执行模式
        try:
            # 备份
            backup_path = self.backup(file_path)
            logger.info(f"[备份] {backup_path}")

            # 读取内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # 应用修复
            new_content = content
            new_path = file_path

            for fix in analysis["suggested_fixes"]:
                if fix["type"] == "add_dna":
                    # 在文件头部添加DNA
                    header = f"""---
# ═══════════════════════════════════════════════════════════
# 龍魂系统 · DNA追溯
# ═══════════════════════════════════════════════════════════
# {fix['content']}
# 创建者: 龍芯北辰｜UID9622
# ═══════════════════════════════════════════════════════════
---

"""
                    new_content = header + new_content

                elif fix["type"] == "add_confirm":
                    # 在文件尾部添加CONFIRM
                    footer = f"""

# ═══════════════════════════════════════════════════════════
# 确认码: {fix['content']}
# ═══════════════════════════════════════════════════════════
"""
                    new_content = new_content + footer

                elif fix["type"] == "rename":
                    new_path = file_path.parent / fix["new_name"]

            # 写入
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # 重命名
            if new_path != file_path:
                file_path.rename(new_path)
                logger.info(f"[重命名] {file_path.name} → {new_path.name}")

            self.repaired_count += 1
            return True

        except Exception as e:
            logger.error(f"[修复失败] {file_path}: {e}")
            self.failed_count += 1
            return False

# ═══════════════════════════════════════════════════════════
# 批量处理器
# ═══════════════════════════════════════════════════════════

class BatchProcessor:
    def __init__(self, preview: bool = True):
        self.preview = preview
        self.engine = DNARepairEngine()
        self.repairer = FileRepairer(preview=preview)
        self.results: List[Dict] = []

    def process_single(self, file_path: Path) -> Optional[Dict]:
        """处理单个文件"""
        try:
            # 读取内容（前1000行）
            content = ""
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f):
                    if i >= 1000:
                        break
                    content += line

            # 分析
            analysis = self.engine.analyze(file_path, content)

            # 如果有问题，修复
            if analysis["issues"]:
                self.repairer.repair(file_path, analysis)

            return analysis

        except Exception as e:
            logger.error(f"[处理失败] {file_path}: {e}")
            return None

    def process_batch(self, files: List[Path]):
        """批量处理"""
        logger.info(f"批量处理: {len(files)} 文件 (预览模式={self.preview})")

        with ThreadPoolExecutor(max_workers=CONFIG["max_workers"]) as executor:
            futures = {executor.submit(self.process_single, f): f for f in files}

            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    result = future.result()
                    if result:
                        self.results.append(result)
                except Exception as e:
                    logger.error(f"[批次失败] {file_path}: {e}")

        # 生成报告
        self._generate_report()

    def _generate_report(self):
        """生成修复报告"""
        report_path = Path(os.path.expanduser(CONFIG["backup_dir"])) / "repair_report.md"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 龍魂系统 · DNA修复报告\n\n")
            f.write(f"> 生成时间: {datetime.now().isoformat()}\n")
            f.write(f"> 模式: {'预览' if self.preview else '执行'}\n")
            f.write(f"> 处理文件: {len(self.results)}\n\n")

            # 问题统计
            issue_counts = {}
            for r in self.results:
                for issue in r.get("issues", []):
                    issue_counts[issue] = issue_counts.get(issue, 0) + 1

            f.write("## 问题统计\n\n")
            for issue, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
                f.write(f"- {issue}: {count} 文件\n")

            # 详细列表
            f.write("\n## 详细列表\n\n")
            for r in self.results:
                if r.get("issues"):
                    f.write(f"### {r['filename']}\n\n")
                    f.write(f"- 路径: `{r['file_path']}`\n")
                    f.write(f"- 类型: {r.get('type_marker', '未知')}\n")
                    f.write(f"- 项目: {r.get('project_name', '未知')}\n")
                    f.write(f"- 问题: {', '.join(r['issues'])}\n")

                    if r.get("suggested_fixes"):
                        f.write("- 建议修复:\n")
                        for fix in r["suggested_fixes"]:
                            f.write(f"  - {fix['type']}: {fix['reason']}\n")
                            if fix['type'] == 'add_dna':
                                f.write(f"    - DNA: `{fix['content']}`\n")
                            elif fix['type'] == 'rename':
                                f.write(f"    - 新名: `{fix['new_name']}`\n")
                    f.write("\n---\n\n")

            # 执行统计
            if not self.preview:
                f.write(f"\n## 执行统计\n\n")
                f.write(f"- 修复成功: {self.repairer.repaired_count}\n")
                f.write(f"- 修复失败: {self.repairer.failed_count}\n")

        logger.info(f"报告已保存: {report_path}")

# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂系统DNA修复工具")
    parser.add_argument("--execute", action="store_true", help="执行修复（默认预览）")
    parser.add_argument("--path", default=CONFIG["scan_root"], help="扫描路径")
    args = parser.parse_args()

    preview = not args.execute
    scan_root = Path(os.path.expanduser(args.path))

    logger.info("=" * 60)
    logger.info("龍魂系统 · DNA修复工具 v1.0")
    logger.info(f"模式: {'预览' if preview else '执行'}")
    logger.info(f"路径: {scan_root}")
    logger.info("=" * 60)

    # 收集文件
    files = []
    for ext in ['.md', '.py', '.js', '.html', '.sh', '.txt', '.json', '.yaml', '.yml']:
        files.extend(scan_root.rglob(f'*{ext}'))

    logger.info(f"发现 {len(files)} 个候选文件")

    # 处理
    processor = BatchProcessor(preview=preview)
    processor.process_batch(files)

    logger.info("处理完成！")
    if preview:
        logger.info("这是预览模式，未实际修改文件。要执行修复，加 --execute 参数")

if __name__ == "__main__":
    main()
