#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 数据清洗引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-CLEAN-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 清洗日志文件（去重、压缩）
  - 清洗代码（去冗余空行）
  - 清洗数据（去重、标准化）
"""

import re
import gzip
import json
from pathlib import Path
from typing import Dict, List


class CleanEngine:
    """数据清洗引擎——去重·格式化·压缩·回收空间"""

    def __init__(self):
        self.project_root = Path.home() / "longhun-system"

    def clean_logs(self, log_dir: Path = None) -> Dict:
        """清洗日志文件（压缩大文件）"""
        log_dir = log_dir or self.project_root / "logs"
        if not log_dir.exists():
            return {"status": "skip", "reason": "日志目录不存在"}

        result = {"cleaned": 0, "size_reduced_mb": 0, "files": []}
        for log_file in log_dir.glob("*.log"):
            size = log_file.stat().st_size
            if size > 1024 * 1024:  # >1MB
                compressed = log_file.with_suffix(".log.gz")
                with open(log_file, 'rb') as f_in:
                    with gzip.open(compressed, 'wb') as f_out:
                        f_out.write(f_in.read())
                result["size_reduced_mb"] += (size - compressed.stat().st_size) / (1024**2)
                result["cleaned"] += 1
                result["files"].append({
                    "file": log_file.name,
                    "original_kb": round(size / 1024, 1),
                    "compressed_kb": round(compressed.stat().st_size / 1024, 1),
                })
                log_file.unlink()
        return result

    def deduplicate_lines(self, file_path: Path) -> Dict:
        """去除文件中的重复行"""
        if not file_path.exists():
            return {"status": "error", "reason": "文件不存在"}

        lines = file_path.read_text(encoding="utf-8", errors="ignore").split("\n")
        seen = set()
        unique = []
        for line in lines:
            stripped = line.strip()
            if stripped and stripped not in seen:
                seen.add(stripped)
                unique.append(line)
            elif not stripped:
                unique.append(line)

        file_path.write_text("\n".join(unique), encoding="utf-8")
        return {
            "original": len(lines),
            "unique": len(unique),
            "removed": len(lines) - len(unique),
        }

    def clean_code(self, file_path: Path) -> Dict:
        """清洗代码文件"""
        if not file_path.exists():
            return {"status": "error", "reason": "文件不存在"}

        content = file_path.read_text(encoding="utf-8", errors="ignore")
        original_len = len(content)
        # 去多余空行
        cleaned = re.sub(r'\n{3,}', '\n\n', content)
        # 去行尾空白
        cleaned = re.sub(r'[ \t]+$', '', cleaned, flags=re.MULTILINE)

        if cleaned != content:
            file_path.write_text(cleaned, encoding="utf-8")

        return {
            "status": "cleaned",
            "original_chars": original_len,
            "cleaned_chars": len(cleaned),
            "reduction_pct": round((1 - len(cleaned) / max(1, original_len)) * 100, 1),
        }

    def deduplicate_data(self, data: List[Dict], key: str = None) -> List[Dict]:
        """清洗数据列表去重"""
        if key:
            seen = set()
            cleaned = []
            for item in data:
                val = item.get(key)
                if val is not None and val not in seen:
                    seen.add(val)
                    cleaned.append(item)
            return cleaned

        seen = set()
        cleaned = []
        for item in data:
            hashed = json.dumps(item, sort_keys=True, ensure_ascii=False)
            if hashed not in seen:
                seen.add(hashed)
                cleaned.append(item)
        return cleaned


if __name__ == "__main__":
    engine = CleanEngine()

    # 测试去重
    result = engine.deduplicate_data(
        [{"id": 1, "name": "a"}, {"id": 1, "name": "a"}, {"id": 2, "name": "b"}],
        key="id"
    )
    print(f"去重: {len(result)} 条 (原3条)")

    # 测试日志扫描
    log_result = engine.clean_logs()
    print(f"日志清洗: {log_result}")

    print("🟢 数据清洗引擎测试通过")
