#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·DNA验证工具 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-DNA-VERIFIER-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

验证AI内容的DNA完整性和真实性。任何人都可以用它验证任何AI内容。

用法:
  python3 bin/lh_dna_verifier.py verify --text "一段文本"
  python3 bin/lh_dna_verifier.py verify --file article.md
  python3 bin/lh_dna_verifier.py verify --url https://xxx.com/article
  python3 bin/lh_dna_verifier.py trace --dna "#龍芯⚡️..."
  python3 bin/lh_dna_verifier.py stats
"""

import hashlib
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from engines.lh_dual_labeler import get_labeler, ZWSP, ZWNJ, ZWJ

VERIFIER_DIR = SYSTEM_ROOT / "data" / "dna_verify"
VERIFIER_DIR.mkdir(parents=True, exist_ok=True)


class DNAVerifier:
    """DNA验证器"""

    def __init__(self):
        self.labeler = get_labeler()
        self._verify_log: List[Dict[str, Any]] = []
        self._load_log()

    def _load_log(self):
        lf = VERIFIER_DIR / "verify_log.jsonl"
        if lf.exists():
            try:
                for line in lf.read_text().splitlines():
                    if line.strip():
                        self._verify_log.append(json.loads(line))
            except Exception:
                pass

    def _save_log(self, entry: Dict[str, Any]):
        self._verify_log.append(entry)
        with open(VERIFIER_DIR / "verify_log.jsonl", "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def verify_text(self, text: str, source: str = "manual") -> Dict[str, Any]:
        """验证文本中的DNA"""
        result = self.labeler.verify(text)

        # 额外检查内容哈希一致性
        clean = text
        for c in [ZWSP, ZWNJ, ZWJ]:
            clean = clean.replace(c, "")
        result["text_length"] = len(clean)

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": source,
            "status": result.get("status", "未知"),
            **result,
        }
        self._save_log(entry)
        return entry

    def verify_file(self, filepath: str) -> Dict[str, Any]:
        """验证文件中的DNA"""
        path = Path(filepath)
        if not path.exists():
            return {"error": f"文件不存在: {filepath}"}

        text = path.read_text(encoding="utf-8", errors="ignore")
        return self.verify_text(text, source=f"file:{path.name}")

    def verify_url(self, url: str) -> Dict[str, Any]:
        """验证在线内容的DNA"""
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Longhun-DNA-Verifier/1.0"
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                # 只读前500KB
                text = resp.read(500000).decode("utf-8", errors="ignore")
        except Exception as e:
            return {"error": f"无法获取URL: {e}", "url": url}

        # 尝试从HTML提取正文
        from html.parser import HTMLParser

        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.skip_tags = {"script", "style", "noscript", "meta", "link"}
                self.current = ""

            def handle_data(self, data):
                self.current += data

            def handle_endtag(self, tag):
                if tag not in self.skip_tags:
                    t = self.current.strip()
                    if t:
                        self.text.append(t)
                self.current = ""

        extractor = TextExtractor()
        try:
            extractor.feed(text)
        except Exception:
            pass
        plain_text = "\n".join(extractor.text)

        # 如果HTML没有DNA标签，直接用原始文本
        result = self.labeler.verify(plain_text)
        if not result["has_visible_label"]:
            result = self.labeler.verify(text)  # 尝试原始text

        return self.verify_text(
            plain_text if result.get("has_visible_label") else text,
            source=f"url:{url}",
        )

    def trace(self, dna_code: str) -> Dict[str, Any]:
        """追溯DNA生成链路"""
        # 清理输入
        dna_code = dna_code.strip()

        # 解析DNA格式
        info = self._parse_dna(dna_code)

        # 搜索相关验证记录
        related = []
        for entry in self._verify_log:
            if dna_code in json.dumps(entry, ensure_ascii=False):
                related.append({
                    "timestamp": entry.get("timestamp", ""),
                    "status": entry.get("status", ""),
                    "source": entry.get("source", ""),
                })

        return {
            "dna": dna_code,
            "parsed": info,
            "related_verifications": related[-10:],
            "traced_at": datetime.now(timezone.utc).isoformat(),
        }

    def _parse_dna(self, dna_code: str) -> Dict[str, str]:
        """解析DNA结构"""
        info = {
            "format": "unknown",
        }

        # #龍芯⚡️丙午·乙未·丁酉-DeepSeek-v3.1-GENERATE-a1b2c3d4
        pattern = r'#龍芯⚡️(\S+)'
        m = re.search(pattern, dna_code)
        if m:
            info["format"] = "龍芯v∞"
            parts = dna_code.replace("#龍芯⚡️", "").split("-")
            if len(parts) >= 3:
                info["timestamp"] = parts[0]
                info["model"] = parts[1] if len(parts) > 1 else ""
                info["action"] = parts[2] if len(parts) > 2 else ""
                info["hash"] = parts[-1] if len(parts) > 3 else ""

        # #七因⚡️202607251900-a1b2c3d4
        pattern2 = r'#七因⚡️(\S+)'
        m2 = re.search(pattern2, dna_code)
        if m2:
            info["format"] = "七因子"
            info["timestamp"] = m2.group(1)

        return info

    def stats(self) -> Dict[str, Any]:
        """验证统计"""
        total = len(self._verify_log)
        verified = sum(1 for e in self._verify_log if e.get("status") == "🟢 完整可信")
        tampered = sum(1 for e in self._verify_log if e.get("status") == "🔴 已被篡改")
        unlabeled = sum(1 for e in self._verify_log if "🟡" in e.get("status", ""))

        return {
            "total_verifications": total,
            "verified_authentic": verified,
            "tampered_detected": tampered,
            "unlabeled_or_partial": unlabeled,
            "authenticity_rate": f"{verified / max(1, total) * 100:.1f}%",
            "source_distribution": self._source_distribution(),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _source_distribution(self) -> Dict[str, int]:
        dist: Dict[str, int] = {}
        for e in self._verify_log:
            src = e.get("source", "unknown")
            dist[src] = dist.get(src, 0) + 1
        return dict(sorted(dist.items(), key=lambda x: x[1], reverse=True)[:10])


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def format_result(result: Dict[str, Any]) -> str:
    """格式化输出"""
    lines = []
    lines.append("=" * 50)
    lines.append(f"   状态: {result.get('status', '未知')}")
    lines.append("=" * 50)

    if "error" in result:
        lines.append(f"  ❌ 错误: {result['error']}")
        return "\n".join(lines)

    lines.append(f"  显式标识: {'✅' if result.get('has_visible_label') else '❌'}")
    if result.get('visible_dna'):
        lines.append(f"  显式DNA: {result['visible_dna']}")

    lines.append(f"  隐式标识: {'✅' if result.get('has_invisible_label') else '❌'}")
    if result.get('invisible_meta'):
        lines.append(f"  隐式元数据: {json.dumps(result['invisible_meta'], ensure_ascii=False)}")

    lines.append(f"  内容哈希: {result.get('content_hash', 'N/A')}")
    lines.append(f"  篡改: {'🔴 是' if result.get('tampered') else '🟢 否'}")
    if result.get('mismatch_detail'):
        lines.append(f"  不匹配: {result['mismatch_detail']}")

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·DNA验证工具")
    sub = parser.add_subparsers(dest="cmd")

    p_verify = sub.add_parser("verify", help="验证DNA")
    p_verify.add_argument("--text", help="直接验证文本")
    p_verify.add_argument("--file", help="验证文件")
    p_verify.add_argument("--url", help="验证在线内容")

    p_trace = sub.add_parser("trace", help="追溯DNA链路")
    p_trace.add_argument("--dna", required=True, help="DNA追溯码")

    sub.add_parser("stats", help="验证统计")

    args = parser.parse_args()
    verifier = DNAVerifier()

    if args.cmd == "verify":
        if args.text:
            result = verifier.verify_text(args.text)
            print(format_result(result))
        elif args.file:
            result = verifier.verify_file(args.file)
            print(format_result(result))
        elif args.url:
            result = verifier.verify_url(args.url)
            print(format_result(result))
        else:
            print("请指定 --text / --file / --url")
            sys.exit(1)

    elif args.cmd == "trace":
        result = verifier.trace(args.dna)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == "stats":
        print(json.dumps(verifier.stats(), ensure_ascii=False, indent=2))

    else:
        parser.print_help()
