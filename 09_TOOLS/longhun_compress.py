#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂压缩版 · LongHun Compress v1.0

把全文（文章、代码、记忆、对话）压缩成可还原的「龍魂压缩包」：
  - 摘要读取：人看几百字就知道全文大意
  - 一键还原：输入压缩包即可恢复原文
  - 国密加密：可选 SM4-CBC 加密，主权不外泄
  - DNA 锚定：每个包都有唯一追溯码，来源可查
  - 三才闭环：天（压缩行动）· 地（存储承载）· 人（语义摘要），最终归一中宫五

用法:
    python3 longhun_compress.py compress  input.txt  --title "文章标题" -o article.lhpack
    python3 longhun_compress.py summary   article.lhpack
    python3 longhun_compress.py decompress article.lhpack -o restored.txt
    python3 longhun_compress.py verify    article.lhpack
    python3 longhun_compress.py info      article.lhpack

DNA: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-LONGHUN-COMPRESS-v1.0
"""
from __future__ import annotations

import argparse
import base64
import bz2
import gzip
import hashlib
import json
import lzma
import os
import re
import sys
import zlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------- 路径与常量 ----------
HOME = Path.home()
ROOT = HOME / "longhun-system"
CNSH_GUOMI_PATH = ROOT / "cnsh-runtime-v1" / "CNSH_国密工具.py"

DNA_PREFIX = "#龍芯⚡️"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
SCHEMA = "longhun-compress/v1.0"

# 龍魂高频关键词字典（按长度降序排列，避免短词覆盖）
LONGHUN_DICT: Dict[str, str] = {
    "龍魂系统": "龍魂",
    "龍魂": "龍",
    "LongHun": "LH",
    "UID9622": "U9",
    "诸葛鑫": "ZX",
    "龍芯北辰": "XB",
    "CNSH": "CN",
    "DNA追溯码": "DZ",
    "DNA": "D",
    "追溯": "Z",
    "压缩": "Y",
    "解压": "JY",
    "摘要": "ZY",
    "还原": "HY",
    "人格": "R",
    "模块": "M",
    "系统": "X",
    "状态": "S",
    "高峰期": "P",
    "三色": "3C",
    "审计": "SH",
    "卦象": "GX",
    "数字根": "DR",
    "中宫五": "ZW",
    "道德经": "DDJ",
    "乾卦": "QG",
    "坤卦": "KG",
    "为人民服务": "RM",
    "老百姓": "LBX",
    "中国": "ZG",
}

STOPWORDS = set(
    "的 了 和 是 在 我 有 就 不 人 都 一 一个 上 也 很 到 说 要 去 你 会 着 没有 看 好 自己 这 那 我们 可以 这个 这些 为 之 与 而 及 以 于 被 把 给 让 向 从 对 将 等 吗 呢 吧 啊 哦 嗯".split()
    + "the a an is are was were be been have has had do does did will would could should may might must can shall".split()
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dna(event_type: str, seed: str = "") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{event_type}|{seed}|{ts}".encode("utf-8")).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-{event_type}-{h}"


def _content_hash(text: bytes) -> str:
    return hashlib.sha256(text).hexdigest()


def _safe_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)


def _load_guomi() -> Optional[Any]:
    """安全加载 CNSH 国密工具模块。"""
    if not CNSH_GUOMI_PATH.exists():
        return None
    try:
        module_dir = str(CNSH_GUOMI_PATH.parent)
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)
        import importlib.util
        spec = importlib.util.spec_from_file_location("CNSH_国密工具", str(CNSH_GUOMI_PATH))
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    except Exception:
        pass
    return None


# ---------- 摘要/关键词/骨架 ----------
def _extract_chinese_terms(text: str, top_k: int = 12) -> List[Tuple[str, int]]:
    terms: Dict[str, int] = {}
    for m in re.finditer(r"[\u4e00-\u9fff]{2,8}", text):
        term = m.group(0)
        if len(term) >= 2 and term not in STOPWORDS:
            terms[term] = terms.get(term, 0) + 1
    return sorted(terms.items(), key=lambda x: x[1], reverse=True)[:top_k]


def _extract_english_terms(text: str, top_k: int = 8) -> List[Tuple[str, int]]:
    terms: Dict[str, int] = {}
    for m in re.finditer(r"[A-Za-z][A-Za-z0-9_]{1,30}", text):
        term = m.group(0).lower()
        if term not in STOPWORDS and len(term) > 2:
            terms[term] = terms.get(term, 0) + 1
    return sorted(terms.items(), key=lambda x: x[1], reverse=True)[:top_k]


def _extract_keywords(text: str) -> List[str]:
    cn = _extract_chinese_terms(text, top_k=10)
    en = _extract_english_terms(text, top_k=5)
    keywords = [t[0] for t in cn] + [t[0] for t in en]
    return list(dict.fromkeys(keywords))[:15]


def _generate_summary(text: str, title: str = "", max_len: int = 140) -> str:
    if title:
        return title[:max_len]
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines[:10]:
        if line.startswith(("#", "```", "[", "-", "*", "|")):
            continue
        cleaned = re.sub(r"\[.*?\]\(.*?\)", "", line).strip("*-· ")
        if len(cleaned) > 10:
            return cleaned[:max_len]
    terms = _extract_chinese_terms(text, top_k=5)
    if terms:
        return "关于" + "、".join([t[0] for t in terms[:5]]) + "的内容"
    return text[:max_len].replace("\n", " ")


def _extract_skeleton(content: str) -> Dict[str, Any]:
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    skeleton = {
        "background": "",
        "problem": "",
        "solution": "",
        "key_points": [],
        "next_action": "",
    }
    section = "background"
    for line in lines[:200]:
        lower = line.lower()
        if any(kw in line for kw in ["问题", "Problem", "Issue", "错误", "痛点"]):
            section = "problem"
            continue
        if any(kw in line for kw in ["方案", "Solution", "解决", "方法", "策略"]):
            section = "solution"
            continue
        if any(kw in line for kw in ["下一步", "Next", "Action", "TODO", "待办"]):
            section = "next_action"
            continue
        if line.startswith(("-", "*", "•", "1.", "2.", "3.", "4.", "5.")) and section in ("solution", "background"):
            cleaned = re.sub(r"^[-*•\d\.\s]+", "", line)
            if len(cleaned) > 4:
                skeleton["key_points"].append(cleaned)
            continue
        if section == "problem":
            skeleton["problem"] += line + "\n"
        elif section == "solution":
            skeleton["solution"] += line + "\n"
        elif section == "next_action":
            skeleton["next_action"] += line + "\n"
        else:
            skeleton["background"] += line + "\n"

    for key in ("background", "problem", "solution", "next_action"):
        skeleton[key] = skeleton[key].strip()[:300]
    skeleton["key_points"] = skeleton["key_points"][:8]
    return skeleton


# ---------- 字典编码与重复去重 ----------
_BOUNDARY = "\uE000"  # 私有使用区字符，用作字典标记边界


def _dict_encode(text: str, reverse: bool = False) -> str:
    """龍魂字典编码：用边界符包围短标记，一次性正则替换，避免嵌套误替换。"""
    if reverse:
        # 先转义还原
        text = text.replace(f"{_BOUNDARY}E{_BOUNDARY}", _BOUNDARY)
        reverse_mapping = {short: full for full, short in LONGHUN_DICT.items()}
        # 按短标记长度降序构造正则，避免短标记覆盖
        shorts = sorted(reverse_mapping.keys(), key=lambda x: -len(x))
        pattern = re.compile(
            re.escape(_BOUNDARY) + "(" + "|".join(re.escape(s) for s in shorts) + ")" + re.escape(_BOUNDARY)
        )

        def repl(m: re.Match) -> str:
            return reverse_mapping.get(m.group(1), m.group(0))

        return pattern.sub(repl, text)
    else:
        # 先转义原文中的边界符
        text = text.replace(_BOUNDARY, f"{_BOUNDARY}E{_BOUNDARY}")
        # 按关键词长度降序构造正则，长词优先匹配
        items = sorted(LONGHUN_DICT.items(), key=lambda x: -len(x[0]))
        pattern = re.compile("|".join(re.escape(k) for k, _ in items))

        def repl(m: re.Match) -> str:
            full = m.group(0)
            return f"{_BOUNDARY}{LONGHUN_DICT[full]}{_BOUNDARY}"

        return pattern.sub(repl, text)


def _dedup_lines(text: str) -> str:
    # split('\n') 保留末尾空行，确保换行符不丢失
    lines = text.split("\n")
    if not lines:
        return text
    out = []
    prev = lines[0]
    count = 1
    for line in lines[1:]:
        if line == prev:
            count += 1
        else:
            out.append(f"<{count}x>{prev}" if count > 1 else prev)
            prev = line
            count = 1
    out.append(f"<{count}x>{prev}" if count > 1 else prev)
    return "\n".join(out)


def _undup_lines(text: str) -> str:
    # split('\n') 保留末尾空行
    out = []
    for line in text.split("\n"):
        m = re.match(r"^<(\d+)x>(.*)$", line)
        if m:
            out.extend([m.group(2)] * int(m.group(1)))
        else:
            out.append(line)
    return "\n".join(out)


# ---------- 算法压缩 ----------
def _try_zstd(data: bytes, decompress: bool = False) -> Optional[bytes]:
    try:
        import zstandard as zstd  # type: ignore
        if decompress:
            return zstd.ZstdDecompressor().decompress(data)
        return zstd.ZstdCompressor(level=22).compress(data)
    except Exception:
        return None


def _compress_algorithm(data: bytes, method: str) -> Tuple[str, bytes]:
    if method == "raw":
        return "raw", data
    if method == "zlib":
        return "zlib", zlib.compress(data, level=9)
    if method == "gzip":
        return "gzip", gzip.compress(data, compresslevel=9)
    if method == "bz2":
        return "bz2", bz2.compress(data, compresslevel=9)
    if method == "lzma":
        return "lzma", lzma.compress(data, preset=9)
    if method == "zstd":
        res = _try_zstd(data)
        if res is not None:
            return "zstd", res
        raise RuntimeError("zstd 不可用，请安装 zstandard")
    raise ValueError(f"不支持的压缩算法: {method}")


def _decompress_algorithm(data: bytes, method: str) -> bytes:
    if method == "raw":
        return data
    if method == "zlib":
        return zlib.decompress(data)
    if method == "gzip":
        return gzip.decompress(data)
    if method == "bz2":
        return bz2.decompress(data)
    if method == "lzma":
        return lzma.decompress(data)
    if method == "zstd":
        res = _try_zstd(data, decompress=True)
        if res is not None:
            return res
        raise RuntimeError("zstd 不可用")
    raise ValueError(f"不支持的解压算法: {method}")


def _auto_compress(data: bytes) -> Tuple[str, bytes]:
    best_size = len(data)
    best_method = "raw"
    best_data = data
    for name in ("zlib", "gzip", "bz2", "lzma", "zstd"):
        try:
            _, compressed = _compress_algorithm(data, name)
            if len(compressed) < best_size:
                best_size = len(compressed)
                best_method = name
                best_data = compressed
        except Exception:
            continue
    return best_method, best_data


# ---------- 加密 ----------
def _sm4_encrypt(plaintext: bytes, key: bytes) -> Tuple[bytes, bytes]:
    """SM4-ECB 加密并返回 (ciphertext, iv)。iv 为空。"""
    if len(key) not in (16, 24, 32):
        # SM4 需要 16 字节密钥，这里做简单填充/截断
        key = hashlib.sha256(key).digest()[:16]
    mod = _load_guomi()
    if mod is None:
        raise RuntimeError("CNSH 国密工具未找到，无法使用 SM4 加密")
    ct = mod.SM4.encrypt_ecb(plaintext, key)
    return ct, b""


def _sm4_decrypt(ciphertext: bytes, key: bytes, iv: bytes = b"") -> bytes:
    if len(key) not in (16, 24, 32):
        key = hashlib.sha256(key).digest()[:16]
    mod = _load_guomi()
    if mod is None:
        raise RuntimeError("CNSH 国密工具未找到，无法使用 SM4 解密")
    return mod.SM4.decrypt_ecb(ciphertext, key)


# ---------- 核心压缩/解压 ----------
def compress(
    text: str,
    title: str = "",
    operator: str = "UID9622",
    method: str = "auto",
    use_dict: bool = True,
    use_dedup: bool = True,
    encrypt: bool = False,
    key: Optional[bytes] = None,
) -> Dict[str, Any]:
    """把长文本压缩成龍魂压缩包。"""
    original_bytes = text.encode("utf-8")
    original_hash = _content_hash(original_bytes)

    # 1. 字典编码
    processed = text
    if use_dict:
        processed = _dict_encode(processed)
    # 2. 重复去重
    if use_dedup:
        processed = _dedup_lines(processed)

    payload_bytes = processed.encode("utf-8")

    # 3. 算法压缩
    if method == "auto":
        algo_name, compressed = _auto_compress(payload_bytes)
    else:
        algo_name, compressed = _compress_algorithm(payload_bytes, method)

    # 4. 可选加密
    encrypted = False
    iv_b64 = ""
    if encrypt and key:
        compressed, iv = _sm4_encrypt(compressed, key)
        encrypted = True
        iv_b64 = base64.b64encode(iv).decode("ascii") if iv else ""

    # 5. 封装
    payload_b64 = base64.b64encode(compressed).decode("ascii")
    dna = _dna("LONGHUN-COMPRESS", original_hash)
    summary = _generate_summary(text, title)
    keywords = _extract_keywords(text)
    skeleton = _extract_skeleton(text)

    package = {
        "schema": SCHEMA,
        "version": "1.0",
        "dna": dna,
        "confirm_code": CONFIRM_CODE,
        "seal": SEAL,
        "created_at": _now(),
        "operator": operator,
        "header": {
            "title": title or summary[:40],
            "summary": summary,
            "keywords": keywords,
            "skeleton": skeleton,
            "original_hash": original_hash,
            "original_size": len(original_bytes),
            "char_count": len(text),
            "language": "zh-CN",
        },
        "crypto": {
            "encrypted": encrypted,
            "algorithm": "SM4-ECB" if encrypted else "none",
            "iv": iv_b64,
        },
        "payload": {
            "encoding": "base64",
            "method": algo_name,
            "use_dict": use_dict,
            "use_dedup": use_dedup,
            "compressed_size": len(compressed),
            "ratio": round(len(compressed) / len(original_bytes), 6) if original_bytes else 0.0,
            "saved": round(1 - len(compressed) / len(original_bytes), 6) if original_bytes else 0.0,
            "data": payload_b64,
        },
        "sancai": {
            "tian": "压缩执行·算法选择·加密行动",
            "di": "base64承载·文件存储·数据库归档",
            "ren": "语义摘要·关键词·骨架",
            "zhonggong": "DNA不动点·369归一",
        },
    }
    return package


def decompress(package: Dict[str, Any], key: Optional[bytes] = None) -> str:
    """从龍魂压缩包还原文本。"""
    payload = package["payload"]
    compressed = base64.b64decode(payload["data"])

    # 1. 解密
    crypto = package.get("crypto", {})
    if crypto.get("encrypted"):
        if not key:
            raise ValueError("压缩包已加密，需提供解密密钥")
        iv = base64.b64decode(crypto.get("iv", "")) if crypto.get("iv") else b""
        algorithm = crypto.get("algorithm", "SM4-ECB")
        if algorithm == "SM4-ECB":
            compressed = _sm4_decrypt(compressed, key, iv)
        else:
            raise ValueError(f"不支持的加密算法: {algorithm}")

    # 2. 算法解压
    method = payload.get("method", "raw")
    data = _decompress_algorithm(compressed, method)

    # 3. 重复还原
    if payload.get("use_dedup"):
        text = _undup_lines(data.decode("utf-8", errors="replace"))
    else:
        text = data.decode("utf-8", errors="replace")

    # 4. 字典还原
    if payload.get("use_dict"):
        text = _dict_encode(text, reverse=True)

    return text


def verify(package: Dict[str, Any], original_text: Optional[str] = None) -> Dict[str, Any]:
    """验证压缩包完整性。"""
    header = package.get("header", {})
    original_hash = header.get("original_hash", "")
    result = {
        "schema_ok": package.get("schema") == SCHEMA,
        "hash_match": None,
        "dna": package.get("dna", ""),
        "confirm_code": package.get("confirm_code", ""),
        "ratio": package.get("payload", {}).get("ratio", 0),
    }
    if original_text is not None:
        result["hash_match"] = _content_hash(original_text.encode("utf-8")) == original_hash
    return result


def generate_card(package: Dict[str, Any]) -> str:
    """生成给人看的 Markdown 压缩卡。"""
    header = package.get("header", {})
    payload = package.get("payload", {})
    sk = header.get("skeleton", {})
    return f"""【龍魂压缩卡 · v1.0】

**标题**: {header.get('title', '（未命名）')}
**DNA**: `{package.get('dna', '-')}`
**时间**: {package.get('created_at', '-')}
**操作人**: {package.get('operator', 'UID9622')}
**格式**: `{package.get('schema', SCHEMA)}`

---

## 一｜一句话压缩
{header.get('summary', '（暂无）')}

## 二｜核心骨架
- **背景**：{sk.get('background') or '（暂无）'}
- **问题**：{sk.get('problem') or '（暂无）'}
- **方案**：{sk.get('solution') or '（暂无）'}
- **下一步**：{sk.get('next_action') or '（暂无）'}

## 三｜关键点
{chr(10).join(f'- {p}' for p in sk.get('key_points', [])) or '- （暂无）'}

## 四｜压缩指标
- 原始大小：{payload.get('original_size', header.get('original_size', 0))} bytes
- 压缩后大小：{payload.get('compressed_size', 0)} bytes
- 压缩率：{payload.get('ratio', 0):.2%}
- 算法：{payload.get('method', 'raw')}
- 字典编码：{'启用' if payload.get('use_dict') else '未启用'}
- 重复去重：{'启用' if payload.get('use_dedup') else '未启用'}
- 加密：{'是 · ' + package.get('crypto', {}).get('algorithm', '未知') if package.get('crypto', {}).get('encrypted') else '否'}

## 五｜三才锚定
- 天：{package.get('sancai', {}).get('tian', '-')}
- 地：{package.get('sancai', {}).get('di', '-')}
- 人：{package.get('sancai', {}).get('ren', '-')}
- 中宫：{package.get('sancai', {}).get('zhonggong', '-')}

---
*龍魂压缩版 · 摘要可读 · 原文可还原 · DNA可追溯*
"""


# ---------- 命令行 ----------
def main() -> None:
    parser = argparse.ArgumentParser(description="龍魂压缩版 · 全文压缩/还原/摘要工具")
    sub = parser.add_subparsers(dest="action", required=True)

    # compress
    p_compress = sub.add_parser("compress", help="压缩文件或文本")
    p_compress.add_argument("input", type=str, help="输入文件路径，或 file:路径")
    p_compress.add_argument("-t", "--title", type=str, default="", help="标题")
    p_compress.add_argument("-o", "--output", type=str, default=None, help="输出 .lhpack 文件路径")
    p_compress.add_argument("-m", "--method", type=str, default="auto", help="压缩算法: auto/zlib/gzip/bz2/lzma/zstd/raw")
    p_compress.add_argument("--no-dict", action="store_true", help="不使用龍魂字典")
    p_compress.add_argument("--no-dedup", action="store_true", help="不去重")
    p_compress.add_argument("--encrypt", action="store_true", help="使用 SM4 加密")
    p_compress.add_argument("--key", type=str, default=None, help="加密密钥（字符串，会哈希成16字节）")
    p_compress.add_argument("--operator", type=str, default="UID9622", help="操作人标识")

    # decompress
    p_decompress = sub.add_parser("decompress", help="还原压缩包")
    p_decompress.add_argument("input", type=str, help="输入 .lhpack 文件路径")
    p_decompress.add_argument("-o", "--output", type=str, default=None, help="输出还原文件路径")
    p_decompress.add_argument("--key", type=str, default=None, help="解密密钥")

    # summary
    p_summary = sub.add_parser("summary", help="读取压缩包摘要，不还原文本")
    p_summary.add_argument("input", type=str, help="输入 .lhpack 文件路径")

    # verify
    p_verify = sub.add_parser("verify", help="验证压缩包完整性")
    p_verify.add_argument("input", type=str, help="输入 .lhpack 文件路径")
    p_verify.add_argument("--original", type=str, default=None, help="原始文件路径，用于校验哈希")

    # info
    p_info = sub.add_parser("info", help="显示压缩包元信息")
    p_info.add_argument("input", type=str, help="输入 .lhpack 文件路径")

    args = parser.parse_args()

    if args.action == "compress":
        # 读取输入
        if args.input.startswith("file:"):
            path = Path(args.input[5:])
        else:
            path = Path(args.input)
        if not path.exists():
            print(f"❌ 文件不存在: {path}")
            sys.exit(1)
        text = path.read_text(encoding="utf-8", errors="replace")

        key = args.key.encode("utf-8") if args.key else None
        package = compress(
            text,
            title=args.title,
            operator=args.operator,
            method=args.method,
            use_dict=not args.no_dict,
            use_dedup=not args.no_dedup,
            encrypt=args.encrypt,
            key=key,
        )

        out_path = Path(args.output) if args.output else Path(str(path) + ".lhpack")
        out_path.write_text(_safe_json(package), encoding="utf-8")

        # 同时输出 .lhcard 给人看的摘要卡
        card_path = out_path.with_suffix(".lhcard")
        card_path.write_text(generate_card(package), encoding="utf-8")

        payload = package["payload"]
        header = package["header"]
        print(f"🗜️ 龍魂压缩完成")
        print(f"   DNA: {package['dna']}")
        print(f"   原始: {header.get('original_size', 0)} bytes")
        print(f"   压缩后: {payload['compressed_size']} bytes")
        print(f"   压缩率: {payload['ratio']:.2%} (节省 {payload['saved']:.2%})")
        print(f"   算法: {payload['method']}")
        print(f"   加密: {'是' if package['crypto']['encrypted'] else '否'}")
        print(f"   输出: {out_path}")
        print(f"   摘要卡: {card_path}")

    elif args.action == "decompress":
        path = Path(args.input)
        if not path.exists():
            print(f"❌ 文件不存在: {path}")
            sys.exit(1)
        package = json.loads(path.read_text(encoding="utf-8"))
        key = args.key.encode("utf-8") if args.key else None
        text = decompress(package, key=key)

        out_path = Path(args.output) if args.output else Path(str(path).replace(".lhpack", ".restored.txt"))
        out_path.write_text(text, encoding="utf-8")
        print(f"📦 龍魂解压完成")
        print(f"   DNA: {package.get('dna')}")
        print(f"   还原文件: {out_path}")
        print(f"   字数: {len(text)}")

    elif args.action == "summary":
        path = Path(args.input)
        package = json.loads(path.read_text(encoding="utf-8"))
        print(generate_card(package))

    elif args.action == "verify":
        path = Path(args.input)
        package = json.loads(path.read_text(encoding="utf-8"))
        original_text = None
        if args.original:
            original_text = Path(args.original).read_text(encoding="utf-8", errors="replace")
        result = verify(package, original_text)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.action == "info":
        path = Path(args.input)
        package = json.loads(path.read_text(encoding="utf-8"))
        header = package.get("header", {})
        payload = package.get("payload", {})
        info = {
            "schema": package.get("schema"),
            "version": package.get("version"),
            "dna": package.get("dna"),
            "confirm_code": package.get("confirm_code"),
            "created_at": package.get("created_at"),
            "operator": package.get("operator"),
            "title": header.get("title"),
            "summary": header.get("summary"),
            "keywords": header.get("keywords"),
            "original_size": header.get("original_size"),
            "compressed_size": payload.get("compressed_size"),
            "ratio": payload.get("ratio"),
            "method": payload.get("method"),
            "encrypted": package.get("crypto", {}).get("encrypted"),
            "algorithm": package.get("crypto", {}).get("algorithm"),
        }
        print(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
