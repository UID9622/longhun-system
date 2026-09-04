#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂本地训练引擎 · 自动语料收集器
DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-TRAIN-COLLECT-v1.0

自动扫描项目内的协议、论文、技能、记忆等目录，把 .md/.txt 收集到训练目录。
跳过密钥、.env、私密文件、二进制、重复文件。
"""
import hashlib
from pathlib import Path
from datetime import datetime

from tqdm import tqdm


class CorpusCollector:
    """自动语料收集器。"""

    def __init__(self, sources, output_dir, exclude_patterns=None, max_file_size=5 * 1024 * 1024,
                 max_files=None, max_total_mb=None):
        self.sources = [Path(s).expanduser().resolve() for s in sources]
        self.output_dir = Path(output_dir).expanduser().resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.exclude_patterns = exclude_patterns or []
        self.max_file_size = max_file_size
        self.max_files = max_files
        self.max_total_bytes = (max_total_mb * 1024 * 1024) if max_total_mb else None
        self.dna = "#龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-TRAIN-COLLECT-v1.0"

    def _should_skip(self, path):
        """判断文件是否跳过。"""
        name = path.name.lower()
        # 跳过隐藏文件
        if name.startswith("."):
            return True
        # 跳过密钥/私密/环境文件
        sensitive = [
            ".env", ".env.", "private", "secret", "key", "password", "token",
            "credentials", "api_key", "ssh", "gpg", "id_rsa", "id_ed25519",
            "wallet", "seed", "mnemonic",
        ]
        if any(s in name for s in sensitive):
            return True
        # 跳过匹配模式
        for pattern in self.exclude_patterns:
            if path.match(pattern):
                return True
        # 跳过过大文件
        try:
            if path.stat().st_size > self.max_file_size:
                return True
        except Exception:
            return True
        return False

    def _file_hash(self, path):
        """计算文件内容哈希，用于去重。"""
        h = hashlib.blake2b(digest_size=16)
        try:
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception:
            return None

    def collect(self):
        """执行收集，返回收集到的文件列表。"""
        collected = []
        seen_hashes = set()
        total_bytes = 0

        # 先枚举所有候选文件
        candidates = []
        for source in self.sources:
            if not source.exists():
                print(f"⚠️ 目录不存在，跳过: {source}")
                continue
            for ext in ("*.md", "*.txt"):
                candidates.extend(source.rglob(ext))

        pbar = tqdm(candidates, desc="📚 自动收集语料")
        for file in pbar:
            if self.max_files and len(collected) >= self.max_files:
                print(f"   已达 max_files 上限 ({self.max_files})，停止收集。")
                break

            if self._should_skip(file):
                continue

            fh = self._file_hash(file)
            if not fh or fh in seen_hashes:
                continue
            seen_hashes.add(fh)

            try:
                size = file.stat().st_size
                if self.max_total_bytes and total_bytes + size > self.max_total_bytes:
                    continue
                text = file.read_text(encoding="utf-8")
            except Exception as e:
                print(f"⚠️ 读取失败 {file}: {e}")
                continue

            # 输出文件名带上相对路径，避免冲突
            source = next((s for s in self.sources if file.is_relative_to(s)), self.sources[0])
            rel = file.relative_to(source)
            safe_name = str(rel).replace("/", "__").replace("\\", "__")
            out_path = self.output_dir / safe_name

            try:
                out_path.write_text(text, encoding="utf-8")
                collected.append(out_path)
                total_bytes += size
                pbar.set_postfix({"files": len(collected), "MB": f"{total_bytes / 1e6:.1f}"})
            except Exception as e:
                print(f"⚠️ 复制失败 {file}: {e}")

        return collected

    def report(self):
        """生成收集报告。"""
        files = list(self.output_dir.glob("*.md")) + list(self.output_dir.glob("*.txt"))
        total_size = sum(f.stat().st_size for f in files if f.exists())
        return {
            "dna": self.dna,
            "timestamp": datetime.now().isoformat(),
            "output_dir": str(self.output_dir),
            "file_count": len(files),
            "total_bytes": total_size,
        }


def default_collector(project_root):
    """基于项目根目录创建默认收集器。"""
    sources = [
        project_root / "01_protocols",
        project_root / "papers",
        project_root / "docs",
        project_root / "memory-universe",
        project_root / "skills",
        project_root / "06_技術文檔",
        project_root / "voice-twin",
    ]
    output_dir = project_root / "train" / "data" / "processed" / "auto_corpus"
    exclude_patterns = [
        "*.bak",
        "*.tmp",
        "*.log",
        "*/node_modules/*",
        "*/.venv/*",
        "*/__pycache__/*",
        "*/.git/*",
    ]
    return CorpusCollector(sources, output_dir, exclude_patterns=exclude_patterns)
