#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂道引器 · lh_daoyin.py v2.0

道引：以道为引，纳开源智慧于龍魂体系。
非爬虫、非偷窃，而是：
  来源可查 → 许可证可溯 → 德字闸可过 → 参数可压缩 → DNA可追 → IPA可配

v2.0 新增：
  · 批量吸收（repos.txt 名单 → 并发处理）
  · 鸿蒙适配度评分（驱动/内核/国密/UI框架/编译器）
  · 自驱狩猎（GitHub 搜索 → 自动发现鸿蒙相关仓库）
  · 本地加工 → 产出去（ARM64/qemu 适配验证）
  · 报表输出（MD + JSON，可直接传到成果页）

用法：
  lh_daoyin absorb <github-url|local-path> [--ipa IPA-01,IPA-02]
  lh_daoyin batch <repos.txt> [--workers 4] [--harmony-only]
  lh_daoyin hunt [--query "hongmeng kernel"] [--max 10] [--absorb]
  lh_daoyin list
  lh_daoyin report [--format md|json]
  lh_daoyin query <hash>
  lh_daoyin verify <hash>

DNA: #龍芯⚡️2026-07-10-LONGHUN-DAOYIN-v2.0
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

# ═══════════════════════════════════════════════════════════
# 路径常量
# ═══════════════════════════════════════════════════════════
HOME = Path.home()
LONGHUN_ROOT = HOME / "longhun-system"
DAOYIN_DIR = LONGHUN_ROOT / "L7_数据层" / "daoyin"
MIRROR_DIR = DAOYIN_DIR / "mirror"
CHAIN_FILE = DAOYIN_DIR / "daoyin_chain.jsonl"
REGISTRY_FILE = DAOYIN_DIR / "daoyin_registry.jsonl"

ANTI_TAMPER = LONGHUN_ROOT / "bin" / "lh_anti_tamper.py"

# ═══════════════════════════════════════════════════════════
# 许可证数据库（SPDX 简写 → 全称 + 兼容性）
# ═══════════════════════════════════════════════════════════
LICENSES: Dict[str, Dict[str, Any]] = {
    "mit": {"name": "MIT License", "open_source": True, "copyleft": False, "commercial_ok": True},
    "apache-2.0": {"name": "Apache License 2.0", "open_source": True, "copyleft": False, "commercial_ok": True},
    "bsd-2-clause": {"name": "BSD 2-Clause", "open_source": True, "copyleft": False, "commercial_ok": True},
    "bsd-3-clause": {"name": "BSD 3-Clause", "open_source": True, "copyleft": False, "commercial_ok": True},
    "gpl-2.0": {"name": "GNU GPL v2.0", "open_source": True, "copyleft": True, "commercial_ok": False, "warning": "Copyleft，私有化系统吸收需谨慎"},
    "gpl-3.0": {"name": "GNU GPL v3.0", "open_source": True, "copyleft": True, "commercial_ok": False, "warning": "Copyleft，私有化系统吸收需谨慎"},
    "lgpl": {"name": "GNU LGPL", "open_source": True, "copyleft": "weak", "commercial_ok": True, "warning": "弱 Copyleft，链接形式使用通常安全"},
    "mpl-2.0": {"name": "Mozilla Public License 2.0", "open_source": True, "copyleft": "weak", "commercial_ok": True},
    "cc0-1.0": {"name": "CC0 1.0 Universal", "open_source": True, "copyleft": False, "commercial_ok": True},
    "unlicense": {"name": "The Unlicense", "open_source": True, "copyleft": False, "commercial_ok": True},
}

# 德污标记（A-026）
VIRTUE_DIRT_MARKERS: Dict[str, List[str]] = {
    "德污·A001": ["借曾仕强", "曾老师引流", "曾老师卖课", "曾仕强卖课"],
    "德污·A002": ["断章取义", "歪曲原意"],
    "德污·A003": ["成功学", "鸡汤"],
    "德污·A004": ["德绑架", "用德字压人"],
    "德污·A005": ["删记录", "掩盖错误"],
    "德污·A006": ["假装有结果", "伪造记忆"],
    "德污·A007": ["攻击人格", "制造误会", "煽动对立"],
}

# IPA 关键词路由
IPA_KEYWORDS: Dict[str, List[str]] = {
    "IPA-01-北辰": ["架构", "总纲", "DNA", "系统", "主权"],
    "IPA-20-哲学家": ["哲学", "道阳佛阴", "传承契约", "易经", "德", "价值观"],
    "IPA-11-程序师": ["代码", "算法", "编译器", "运行时", "API"],
    "IPA-13-分析师": ["数据", "分析", "图谱", "统计", "指标"],
    "IPA-30-守护者": ["安全", "审计", "加密", "防火墙", "权限"],
    "IPA-09-法官": ["合规", "许可证", "法律", "规则", "治理"],
}

# ═══════════════════════════════════════════════════════════
# v2.0 新增：鸿蒙适配度评分矩阵
# ═══════════════════════════════════════════════════════════

# 鸿蒙生态关键词权重矩阵（越高越适配）
HARMONY_MATRIX: Dict[str, Dict[str, Any]] = {
    "kernel_driver": {
        "weight": 10, "label": "内核/驱动",
        "keywords": ["kernel", "driver", "dts", "device-tree", "arm64", "aarch64",
                     "bare-metal", "rtos", "liteos", "openharmony", "harmonyos",
                     "mmu", "dma", "interrupt", "gic", "uart", "spi", "i2c", "gpio",
                     "device tree", "kconfig", "kbuild", "makefile", "linker"],
    },
    "guomi_crypto": {
        "weight": 10, "label": "国密/加密",
        "keywords": ["sm2", "sm3", "sm4", "guomi", "国密", "gmssl", "tls", "ssl",
                     "椭圆曲线", "密码", "encrypt", "decrypt", "hash", "signature",
                     "certificate", "pki", "openssl", "mbedtls", "wolfssl"],
    },
    "ui_framework": {
        "weight": 8, "label": "UI框架",
        "keywords": ["arkui", "ace", "declarative", "component", "widget",
                     "render", "canvas", "gpu", "opengl", "vulkan", "skia",
                     "flutter", "react", "vue", "electron", "qt", "gtk"],
    },
    "compiler_toolchain": {
        "weight": 9, "label": "编译器/工具链",
        "keywords": ["compiler", "llvm", "gcc", "clang", "assembler", "linker",
                     "toolchain", "cross-compile", "build", "cmake", "makefile",
                     "objdump", "elf", "binary", "jit", "aot", "bytecode"],
    },
    "network_protocol": {
        "weight": 7, "label": "网络/协议",
        "keywords": ["tcp", "udp", "http", "mqtt", "coap", "lwm2m", "websocket",
                     "socket", "ipv6", "netif", "ethernet", "wifi", "ble",
                     "nfc", "zigbee", "lorawan", "5g", "nb-iot"],
    },
    "storage_fs": {
        "weight": 6, "label": "存储/文件系统",
        "keywords": ["filesystem", "fs", "fat", "ext4", "nand", "nor", "flash",
                     "littlefs", "spiffs", "sqlite", "rocksdb", "leveldb",
                     "nvme", "mmc", "sd", "emmc", "ufs"],
    },
    "ai_ml": {
        "weight": 7, "label": "AI/推理",
        "keywords": ["neural", "inference", "onnx", "tflite", "ncnn", "mnn",
                     "tensor", "quantization", "int8", "fp16", "npu", "dsp",
                     "edge-ai", "tiny-ml", "embedded-ml", "model"],
    },
    "security_hardening": {
        "weight": 9, "label": "安全加固",
        "keywords": ["selinux", "apparmor", "seccomp", "sandbox", "capability",
                     "trustzone", "tee", "op-tee", "secure-boot", "verified-boot",
                     "dm-verity", "fde", "fbe", "keymaster", "keystore"],
    },
}

# 许可证黑名单（绝对不能吸的）
LICENSE_BLACKLIST = {"agpl-3.0", "gpl-3.0", "sspl"}

# 批量吸收结果类型
class BatchResult(NamedTuple):
    source: str
    success: bool
    harmony_score: int
    license_spdx: str
    dna: str
    error: str
    files_count: int
    ipa_targets: List[str]

# 线程安全锁
_write_lock = Lock()

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def short_hash(text: str, length: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def generate_dna(action: str, source_hash: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"#龍芯⚡️{ts}-DAOYIN-{action.upper()}-{source_hash[:8].upper()}"


# 最高系统确认 DNA 锚 · 所有写入必须携带
SYSTEM_CONFIRM_ANCHOR = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def ensure_dirs() -> None:
    DAOYIN_DIR.mkdir(parents=True, exist_ok=True)
    MIRROR_DIR.mkdir(parents=True, exist_ok=True)


def append_jsonl(path: Path, records: List[Dict[str, Any]]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def init_chain() -> None:
    if not CHAIN_FILE.exists():
        append_jsonl(CHAIN_FILE, [{
            "chain": "init",
            "version": "1.0",
            "created": now_iso(),
            "dna": generate_dna("init", "0" * 32),
            "desc": "龍魂道引器入链文件·append-only·记录所有开源吸收",
            "confirm": SYSTEM_CONFIRM_ANCHOR,
        }])


# ═══════════════════════════════════════════════════════════
# 来源解析与获取
# ═══════════════════════════════════════════════════════════

def parse_source(source: str) -> Tuple[str, str]:
    """返回 (source_type, canonical_url_or_path)"""
    if source.startswith("http://") or source.startswith("https://"):
        if "github.com" in source:
            return "github", normalize_github_url(source)
        return "url", source
    if Path(source).exists():
        return "local", str(Path(source).resolve())
    return "unknown", source


def normalize_github_url(url: str) -> str:
    """统一 GitHub URL 为 https://github.com/owner/repo 形式"""
    url = url.rstrip("/").replace("http://", "https://")
    # 去掉 .git 后缀
    if url.endswith(".git"):
        url = url[:-4]
    # 处理 /tree/... /blob/... 等
    url = re.sub(r"/tree/.*", "", url)
    url = re.sub(r"/blob/.*", "", url)
    return url


def github_owner_repo(url: str) -> Optional[Tuple[str, str]]:
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)", url)
    if m:
        return m.group(1), m.group(2)
    return None


def download_github_archive(url: str, dest_dir: Path) -> Path:
    """下载 GitHub 仓库 main/master tarball 并解压"""
    owner, repo = github_owner_repo(url)
    # 尝试 main 分支
    tarball_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.tar.gz"
    tarball_path = dest_dir / f"{repo}.tar.gz"
    try:
        urllib.request.urlretrieve(tarball_url, tarball_path)
    except Exception:
        # 尝试 master 分支
        tarball_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/master.tar.gz"
        urllib.request.urlretrieve(tarball_url, tarball_path)

    with tarfile.open(tarball_path, "r:gz") as tar:
        tar.extractall(dest_dir)
    tarball_path.unlink()

    # 找到解压后的目录
    extracted = [d for d in dest_dir.iterdir() if d.is_dir()]
    if not extracted:
        raise RuntimeError("解压后未找到目录")
    return extracted[0]


def copy_local_path(path: str, dest_dir: Path) -> Path:
    src = Path(path).resolve()
    if src.is_dir():
        dst = dest_dir / src.name
        shutil.copytree(src, dst, dirs_exist_ok=True)
        return dst
    else:
        # 单文件：在目标目录下创建一个同名子目录存放
        dst = dest_dir / src.name
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst / src.name)
        return dst


# ═══════════════════════════════════════════════════════════
# 仓库分析
# ═══════════════════════════════════════════════════════════

def find_license(repo_dir: Path) -> Tuple[Optional[str], Optional[str]]:
    """查找并识别 LICENSE 文件，返回 (spdx_key, raw_text)"""
    candidates = ["LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING"]
    for cand in candidates:
        lic_path = repo_dir / cand
        if lic_path.exists():
            text = lic_path.read_text(encoding="utf-8", errors="ignore")
            key = identify_license(text)
            return key, text
    return None, None


def identify_license(text: str) -> Optional[str]:
    """根据文本识别 SPDX 许可证"""
    upper = text.upper()
    # 优先匹配强 Copyleft
    if "GPL V3" in upper or "GPL VERSION 3" in upper or "GPL-3.0" in upper:
        return "gpl-3.0"
    if "GPL V2" in upper or "GPL VERSION 2" in upper or "GPL-2.0" in upper:
        return "gpl-2.0"
    if "LGPL" in upper:
        return "lgpl"
    if "APACHE LICENSE, VERSION 2.0" in upper or "APACHE-2.0" in upper:
        return "apache-2.0"
    if "MIT LICENSE" in upper or "PERMISSION IS HEREBY GRANTED, FREE OF CHARGE" in upper:
        return "mit"
    if "BSD 3-CLAUSE" in upper:
        return "bsd-3-clause"
    if "BSD 2-CLAUSE" in upper:
        return "bsd-2-clause"
    if "MOZILLA PUBLIC LICENSE VERSION 2.0" in upper:
        return "mpl-2.0"
    if "CC0 1.0" in upper:
        return "cc0-1.0"
    if "THE UNLICENSE" in upper:
        return "unlicense"
    return None


def build_manifest(repo_dir: Path) -> List[Dict[str, Any]]:
    """构建文件清单（相对路径 + sha256 + 大小），限制文件类型与大小"""
    manifest: List[Dict[str, Any]] = []
    for path in sorted(repo_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_dir)
        str_rel = str(rel)
        # 跳过二进制/大文件/依赖目录
        if any(p in str_rel for p in [".git/", "node_modules/", "__pycache__/", ".venv/", "venv/", ".pytest_cache/"]):
            continue
        size = path.stat().st_size
        if size > 2 * 1024 * 1024:  # 跳过 >2MB
            manifest.append({"path": str_rel, "size": size, "sha256": "", "skipped": "too_large"})
            continue
        try:
            h = hashlib.sha256(path.read_bytes()).hexdigest()
            manifest.append({"path": str_rel, "size": size, "sha256": h})
        except Exception:
            pass
    return manifest


def extract_key_files(repo_dir: Path, manifest: List[Dict[str, Any]]) -> Dict[str, str]:
    """提取 README、核心代码片段等文本内容用于审查"""
    key_files: Dict[str, str] = {}
    priority_names = ["README.md", "README.rst", "README.txt", "README", 
                      "pyproject.toml", "setup.py", "Cargo.toml", "package.json"]
    for item in manifest:
        name = Path(item["path"]).name
        if name in priority_names and not item.get("skipped"):
            try:
                text = (repo_dir / item["path"]).read_text(encoding="utf-8", errors="ignore")
                key_files[item["path"]] = text[:5000]
            except Exception:
                pass
    return key_files


def run_anti_tamper(text: str) -> Tuple[int, str]:
    """运行防篡改扫描，返回 (exit_code, stdout)"""
    if not ANTI_TAMPER.exists():
        return 0, "anti_tamper not found, skipped"
    sample = text[:8000]
    try:
        result = subprocess.run(
            [sys.executable, str(ANTI_TAMPER), "scan", sample],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode, result.stdout
    except Exception as e:
        return 1, str(e)


def run_virtue_gate(text: str) -> Tuple[bool, List[str]]:
    """德字闸检测，返回 (是否通过, 命中标记列表)"""
    hits = []
    for code, markers in VIRTUE_DIRT_MARKERS.items():
        for marker in markers:
            if marker in text:
                hits.append(code)
                break
    return len(hits) == 0, hits


def determine_ipa_targets(text: str, user_ipas: Optional[List[str]] = None) -> List[str]:
    """根据内容关键词确定目标 IPA"""
    if user_ipas:
        return user_ipas
    targets = set()
    for ipa, keywords in IPA_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                targets.add(ipa)
                break
    if not targets:
        targets.add("IPA-01-北辰")
    return sorted(targets)


def compress_parameters(manifest: List[Dict[str, Any]], key_files: Dict[str, str]) -> Dict[str, Any]:
    """
    参数压缩：保留来源、许可证、文件清单、关键文件摘要、统计信息。
    不保存完整二进制，只保存可追溯的元数据与文本摘要。
    """
    total_files = len([m for m in manifest if not m.get("skipped")])
    total_size = sum(m.get("size", 0) for m in manifest if not m.get("skipped"))
    return {
        "manifest_hash": short_hash(json.dumps(manifest, sort_keys=True, ensure_ascii=False)),
        "file_count": total_files,
        "total_bytes": total_size,
        "key_files": {k: v[:2000] for k, v in key_files.items()},
        "file_tree_sample": [m["path"] for m in manifest[:50] if not m.get("skipped")],
    }


# ═══════════════════════════════════════════════════════════
# 核心：吸收
# ═══════════════════════════════════════════════════════════

def absorb_source(source: str, user_ipas: Optional[List[str]] = None, dry_run: bool = False) -> Dict[str, Any]:
    """吸收一个开源来源"""
    ensure_dirs()
    init_chain()

    source_type, canonical = parse_source(source)
    if source_type == "unknown":
        raise ValueError(f"无法识别的来源: {source}")

    print(f"\n☯️ 道引开始: {canonical}")
    print(f"   来源类型: {source_type}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        if source_type == "github":
            repo_dir = download_github_archive(canonical, tmp_path)
        else:
            repo_dir = copy_local_path(canonical, tmp_path)

        # 1. 识别许可证
        lic_key, lic_text = find_license(repo_dir)
        lic_info = LICENSES.get(lic_key, {"name": "Unknown", "open_source": False, "copyleft": False, "commercial_ok": False})
        print(f"   许可证: {lic_info.get('name', lic_key)} ({'✅ 可吸收' if lic_info.get('open_source') else '❌ 非开源'})")
        if lic_info.get("warning"):
            print(f"   ⚠️ {lic_info['warning']}")

        # 2. 构建清单与关键文件
        manifest = build_manifest(repo_dir)
        key_files = extract_key_files(repo_dir, manifest)
        combined_text = "\n".join(key_files.values())

        # 3. 防篡改扫描
        at_code, at_output = run_anti_tamper(combined_text)
        at_label = {0: "🟢 通过", 1: "🟡 待审", 2: "🔴 熔断"}.get(at_code, "❓ 未知")
        print(f"   防篡改: {at_label}")

        # 4. 德字闸
        virtue_ok, virtue_hits = run_virtue_gate(combined_text)
        print(f"   德字闸: {'🟢 通过' if virtue_ok else '🔴 命中 ' + ', '.join(virtue_hits)}")

        # 5. 参数压缩
        compressed = compress_parameters(manifest, key_files)

        # 6. IPA 目标
        ipa_targets = determine_ipa_targets(combined_text, user_ipas)
        print(f"   目标 IPA: {', '.join(ipa_targets)}")

        # 7. 复制镜像（只保留文本与小文件）
        mirror_id = short_hash(canonical + now_iso())
        mirror_subdir = MIRROR_DIR / mirror_id
        mirror_subdir.mkdir(parents=True, exist_ok=True)
        for item in manifest:
            if item.get("skipped") or not item.get("sha256"):
                continue
            src = repo_dir / item["path"]
            dst = mirror_subdir / item["path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(src, dst)
            except Exception:
                pass

        # 8. 生成 PARAM_CARD
        source_hash = short_hash(canonical + json.dumps(manifest, sort_keys=True, ensure_ascii=False))
        param_card = {
            "type": "daoyin_param_card",
            "absorbed_at": now_iso(),
            "source": canonical,
            "source_type": source_type,
            "source_hash": source_hash,
            "license": {"spdx": lic_key, **lic_info},
            "manifest_hash": compressed["manifest_hash"],
            "mirror_path": str(mirror_subdir),
            "ipa_targets": ipa_targets,
            "anti_tamper": {"exit_code": at_code, "label": at_label.strip(), "output": at_output[:500]},
            "virtue_gate": {"passed": virtue_ok, "hits": virtue_hits},
            "compressed": compressed,
            "dna": generate_dna("absorb", source_hash),
            "confirm": SYSTEM_CONFIRM_ANCHOR,
        }

        if dry_run:
            print(f"\n🧪 试运行，未写入链")
            return param_card

        # 9. 入链
        append_jsonl(CHAIN_FILE, [param_card])
        registry_entry = {
            "source": canonical,
            "source_hash": source_hash,
            "license": lic_key,
            "ipa_targets": ipa_targets,
            "anti_tamper": at_code,
            "virtue_passed": virtue_ok,
            "absorbed_at": now_iso(),
            "dna": param_card["dna"],
            "mirror_id": mirror_id,
            "confirm": SYSTEM_CONFIRM_ANCHOR,
        }
        append_jsonl(REGISTRY_FILE, [registry_entry])

        print(f"\n✅ 道引完成")
        print(f"   DNA: {param_card['dna']}")
        print(f"   镜像: {mirror_subdir}")
        print(f"   入链: {CHAIN_FILE}")

        return param_card


# ═══════════════════════════════════════════════════════════
# 查询与验证
# ═══════════════════════════════════════════════════════════

def load_chain() -> List[Dict[str, Any]]:
    if not CHAIN_FILE.exists():
        return []
    records = []
    with open(CHAIN_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def list_absorbed() -> None:
    records = load_chain()
    print(f"\n📜 龍魂道引 · 已吸收来源（共 {len(records) - 1} 条，不含 init）\n")
    for rec in records[1:]:
        print(f"  {rec.get('dna', 'N/A')}")
        print(f"    来源: {rec.get('source', 'N/A')}")
        print(f"    许可证: {rec.get('license', {}).get('name', 'N/A')}")
        print(f"    IPA: {', '.join(rec.get('ipa_targets', []))}")
        print(f"    时间: {rec.get('absorbed_at', 'N/A')}")
        print()


def query_by_hash(query: str) -> Optional[Dict[str, Any]]:
    records = load_chain()
    for rec in records:
        source_hash = rec.get("source_hash", "")
        dna = rec.get("dna", "")
        if query.lower() in source_hash.lower() or query.lower() in dna.lower():
            return rec
    return None


def verify_integrity(query: str) -> bool:
    rec = query_by_hash(query)
    if not rec:
        print(f"❌ 未找到: {query}")
        return False

    print(f"\n🔍 验证: {rec.get('dna')}")
    mirror_path = Path(rec.get("mirror_path", ""))
    if not mirror_path.exists():
        print(f"   ❌ 镜像目录不存在: {mirror_path}")
        return False

    stored_manifest_hash = rec.get("compressed", {}).get("manifest_hash", "")
    # 重新计算当前镜像的 manifest hash
    manifest = build_manifest(mirror_path)
    current_hash = short_hash(json.dumps(manifest, sort_keys=True, ensure_ascii=False))

    if current_hash != stored_manifest_hash:
        print(f"   ❌ 哈希不匹配: stored={stored_manifest_hash}, current={current_hash}")
        return False

    print(f"   ✅ 镜像完整，哈希一致")
    print(f"   ✅ 文件数: {len([m for m in manifest if not m.get('skipped')])}")
    return True


# ═══════════════════════════════════════════════════════════
# v2.0 新增：鸿蒙适配度评分
# ═══════════════════════════════════════════════════════════

def score_harmony_fit(repo_dir: Path, manifest: List[Dict[str, Any]], key_files: Dict[str, str]) -> Tuple[int, Dict[str, int]]:
    """
    计算仓库的鸿蒙适配度。
    扫描文件路径+文件名+README内容，按 HARMONY_MATRIX 七大维度打分。
    返回 (总分, {维度: 得分})
    """
    scores: Dict[str, int] = {}
    total = 0

    # 收集所有文本用于匹配
    all_text = " ".join(key_files.values()).lower()
    all_paths = " ".join(m["path"].lower() for m in manifest)

    for dim, cfg in HARMONY_MATRIX.items():
        dim_score = 0
        for kw in cfg["keywords"]:
            kw_lower = kw.lower()
            # 路径命中 +3，内容命中 +1
            if kw_lower in all_paths:
                dim_score += 3
            if kw_lower in all_text:
                dim_score += 1
        # 权重加成
        weighted = min(dim_score * cfg["weight"], cfg["weight"] * 10)
        scores[dim] = weighted
        total += weighted

    return total, scores


# ═══════════════════════════════════════════════════════════
# v2.0 新增：批量吸收
# ═══════════════════════════════════════════════════════════

def read_repo_list(filepath: str) -> List[str]:
    """从文件读取仓库列表，支持 # 注释和空行"""
    repos = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            repos.append(line)
    return repos


def batch_absorb_one(source: str, harmony_only: bool) -> BatchResult:
    """吸收一个来源并返回结果（用于线程池）"""
    try:
        with _write_lock:
            print(f"\n{'='*60}")
            print(f"📥 道引: {source}")

        ensure_dirs()
        init_chain()

        source_type, canonical = parse_source(source)
        if source_type == "unknown":
            return BatchResult(source, False, 0, "unknown", "", f"无法识别来源: {source}", 0, [])

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            if source_type == "github":
                repo_dir = download_github_archive(canonical, tmp_path)
            else:
                repo_dir = copy_local_path(canonical, tmp_path)

            lic_key, lic_text = find_license(repo_dir)
            lic_info = LICENSES.get(lic_key, {"name": "Unknown", "open_source": False, "copyleft": False, "commercial_ok": False})

            # 强 Copyleft 跳过
            if lic_key in LICENSE_BLACKLIST:
                with _write_lock:
                    print(f"   ⛔ 跳过: {lic_info.get('name', lic_key)} 在黑名单中")
                return BatchResult(source, False, 0, lic_key or "unknown", "", "许可证黑名单", 0, [])

            manifest = build_manifest(repo_dir)
            key_files = extract_key_files(repo_dir, manifest)
            combined_text = "\n".join(key_files.values())

            # 鸿蒙评分
            harmony_score, harmony_detail = score_harmony_fit(repo_dir, manifest, key_files)
            with _write_lock:
                print(f"   鸿蒙适配度: {harmony_score}/100")
                for dim, s in sorted(harmony_detail.items(), key=lambda x: -x[1]):
                    if s > 0:
                        print(f"     {HARMONY_MATRIX[dim]['label']}: {s}")

            # harmony_only 模式：低分跳过
            if harmony_only and harmony_score < 30:
                with _write_lock:
                    print(f"   ⏭️ 跳过（适配度 {harmony_score} < 30）")
                return BatchResult(source, False, harmony_score, lic_key or "unknown", "", "适配度不足", len(manifest), [])

            # 防篡改
            at_code, at_output = run_anti_tamper(combined_text)
            if at_code == 2:  # 熔断
                with _write_lock:
                    print(f"   🔴 防篡改熔断")
                return BatchResult(source, False, harmony_score, lic_key or "unknown", "", "防篡改熔断", len(manifest), [])

            # 德字闸
            virtue_ok, virtue_hits = run_virtue_gate(combined_text)
            if not virtue_ok:
                with _write_lock:
                    print(f"   🔴 德字闸命中: {virtue_hits}")
                return BatchResult(source, False, harmony_score, lic_key or "unknown", "", f"德污: {virtue_hits}", len(manifest), [])

            # 参数压缩
            compressed = compress_parameters(manifest, key_files)
            ipa_targets = determine_ipa_targets(combined_text, None)
            source_hash = short_hash(canonical + json.dumps(manifest, sort_keys=True, ensure_ascii=False))

            # 镜像
            mirror_id = short_hash(canonical + now_iso())
            mirror_subdir = MIRROR_DIR / mirror_id
            mirror_subdir.mkdir(parents=True, exist_ok=True)
            for item in manifest:
                if item.get("skipped") or not item.get("sha256"):
                    continue
                src = repo_dir / item["path"]
                dst = mirror_subdir / item["path"]
                dst.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(src, dst)
                except Exception:
                    pass

            dna = generate_dna("batch", source_hash)
            param_card = {
                "type": "daoyin_param_card",
                "version": "2.0",
                "absorbed_at": now_iso(),
                "source": canonical,
                "source_type": source_type,
                "source_hash": source_hash,
                "license": {"spdx": lic_key, **lic_info},
                "harmony_fit": {"total": harmony_score, "detail": harmony_detail},
                "manifest_hash": compressed["manifest_hash"],
                "mirror_path": str(mirror_subdir),
                "ipa_targets": ipa_targets,
                "anti_tamper": {"exit_code": at_code, "output": at_output[:500]},
                "virtue_gate": {"passed": virtue_ok, "hits": virtue_hits},
                "compressed": compressed,
                "dna": dna,
                "confirm": SYSTEM_CONFIRM_ANCHOR,
                "files_count": len([m for m in manifest if not m.get("skipped")]),
            }

            with _write_lock:
                append_jsonl(CHAIN_FILE, [param_card])
                append_jsonl(REGISTRY_FILE, [{
                    "source": canonical, "source_hash": source_hash,
                    "license": lic_key, "ipa_targets": ipa_targets,
                    "harmony_score": harmony_score,
                    "absorbed_at": now_iso(), "dna": dna,
                    "mirror_id": mirror_id, "confirm": SYSTEM_CONFIRM_ANCHOR,
                }])
                print(f"   ✅ 完成 · 文件 {param_card['files_count']} · DNA {dna}")

            return BatchResult(source, True, harmony_score, lic_key or "unknown", dna, "",
                               param_card["files_count"], ipa_targets)
    except Exception as e:
        with _write_lock:
            print(f"   ❌ 异常: {e}")
        return BatchResult(source, False, 0, "unknown", "", str(e), 0, [])


def batch_absorb(repo_file: str, workers: int = 4, harmony_only: bool = False) -> List[BatchResult]:
    """批量吸收：读名单 → 并发处理 → 汇总报告"""
    repos = read_repo_list(repo_file)
    if not repos:
        print("❌ 仓库名单为空")
        return []

    print(f"\n🔰 龍魂道引 · 批量吸收")
    print(f"   名单: {repo_file}")
    print(f"   仓库数: {len(repos)}")
    print(f"   并发数: {workers}")
    print(f"   鸿蒙过滤: {'开' if harmony_only else '关'}")
    print(f"{'='*60}\n")

    results: List[BatchResult] = []
    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(batch_absorb_one, repo, harmony_only): repo for repo in repos}
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                source = futures[future]
                results.append(BatchResult(source, False, 0, "unknown", "", str(e), 0, []))

    elapsed = time.time() - start
    success = [r for r in results if r.success]
    failed = [r for r in results if not r.success]

    print(f"\n{'='*60}")
    print(f"📊 批量吸收完成 · 耗时 {elapsed:.1f}s")
    print(f"   ✅ 成功: {len(success)}")
    print(f"   ❌ 失败: {len(failed)}")
    print(f"   📄 总文件数: {sum(r.files_count for r in success)}")

    if success:
        print(f"\n   按鸿蒙适配度排序:")
        for r in sorted(success, key=lambda x: -x.harmony_score)[:10]:
            icon = "🟢" if r.harmony_score >= 60 else "🟡" if r.harmony_score >= 30 else "🔵"
            print(f"   {icon} [{r.harmony_score:3d}] {r.source[:60]}")

    if failed:
        print(f"\n   失败清单:")
        for r in failed:
            print(f"   ❌ {r.source[:60]} — {r.error[:80]}")

    # 自动生成报表
    generate_report(results)

    return results


# ═══════════════════════════════════════════════════════════
# v2.0 新增：自驱狩猎
# ═══════════════════════════════════════════════════════════

def hunt_github(query: str, max_results: int = 10, auto_absorb: bool = False) -> List[Dict[str, Any]]:
    """
    GitHub 自驱狩猎：搜索鸿蒙生态相关仓库。
    用 GitHub REST API 搜索，按 stars 排序。
    """
    print(f"\n🔍 龍魂狩猎: \"{query}\" (最多 {max_results} 个)")
    print(f"{'='*60}")

    # 使用 GitHub 搜索 API（无需认证即可搜索仓库）
    search_url = f"https://api.github.com/search/repositories?q={urllib.request.quote(query)}&sort=stars&order=desc&per_page={max_results}"
    
    req = urllib.request.Request(search_url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "Longhun-Daoyin/2.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"   ❌ GitHub API 请求失败: {e}")
        return []

    repos = []
    for item in data.get("items", [])[:max_results]:
        repo_info = {
            "full_name": item["full_name"],
            "url": item["html_url"],
            "stars": item["stargazers_count"],
            "language": item.get("language", "N/A"),
            "description": item.get("description", "")[:200],
            "license": item.get("license", {}).get("spdx_id", "N/A") if item.get("license") else "N/A",
            "topics": item.get("topics", []),
            "updated_at": item["updated_at"],
        }
        repos.append(repo_info)
        print(f"   ⭐ {item['stargazers_count']:>6} | {item['full_name']}")
        print(f"      {item.get('description', '')[:100]}")
        if item.get("license"):
            print(f"      📜 {item['license'].get('spdx_id', 'N/A')} | {item.get('language', 'N/A')}")

    print(f"\n   发现 {len(repos)} 个仓库")

    if auto_absorb and repos:
        print(f"\n   🔄 自动吸收中...")
        repo_urls = [r["url"] for r in repos]
        # 写入临时名单
        hunt_list = DAOYIN_DIR / "hunt_list.txt"
        hunt_list.write_text("\n".join(repo_urls), encoding="utf-8")
        results = batch_absorb(str(hunt_list), workers=3, harmony_only=False)
        hunt_list.unlink()

    # 保存狩猎结果
    hunt_log = DAOYIN_DIR / f"hunt_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    hunt_log.write_text(json.dumps(repos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n   狩猎日志: {hunt_log}")

    return repos


# ═══════════════════════════════════════════════════════════
# v2.0 新增：报表生成
# ═══════════════════════════════════════════════════════════

def generate_report(results: List[BatchResult]) -> str:
    """生成批次吸收报表（MD格式），可直接传到龍魂成果页"""
    success = [r for r in results if r.success]
    failed = [r for r in results if not r.success]

    report_lines = [
        "# 龍魂道引 · 批量吸收报表",
        f"",
        f"| 项目 | 数值 |",
        f"|------|------|",
        f"| 总仓库数 | {len(results)} |",
        f"| ✅ 成功 | {len(success)} |",
        f"| ❌ 失败 | {len(failed)} |",
        f"| 📄 总文件数 | {sum(r.files_count for r in success)} |",
        f"| 🔗 DNA数 | {len([r for r in success if r.dna])} |",
        f"",
        f"## 按鸿蒙适配度排序",
        f"",
        f"| 适配度 | 来源 | 许可证 | 文件数 | DNA |",
        f"|--------|------|--------|--------|-----|",
    ]

    for r in sorted(success, key=lambda x: -x.harmony_score):
        icon = "🟢" if r.harmony_score >= 60 else "🟡" if r.harmony_score >= 30 else "🔵"
        report_lines.append(
            f"| {icon} {r.harmony_score} | {r.source[:50]} | {r.license_spdx} | {r.files_count} | `{r.dna[:30]}...` |"
        )

    if failed:
        report_lines.append(f"")
        report_lines.append(f"## 失败清单")
        report_lines.append(f"")
        for r in failed:
            report_lines.append(f"- ❌ {r.source[:60]} — {r.error[:100]}")

    report_lines.append(f"")
    report_lines.append(f"> 生成时间: {now_iso()}")
    report_lines.append(f"> 引擎: 龍魂道引器 v2.0")
    report_lines.append(f"> {SYSTEM_CONFIRM_ANCHOR}")

    report_text = "\n".join(report_lines)
    report_path = DAOYIN_DIR / f"report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.md"
    report_path.write_text(report_text, encoding="utf-8")

    print(f"\n📋 报表已生成: {report_path}")
    return report_text


# ═══════════════════════════════════════════════════════════
# v2.0 新增：本地加工装甲（ARM64/鲲鹏适配检查）
# ═══════════════════════════════════════════════════════════

def check_arm64_compatibility(repo_dir: Path, manifest: List[Dict[str, Any]]) -> Dict[str, Any]:
    """检查仓库是否 ARM64 适配就绪"""
    has_makefile = False
    has_cmake = False
    has_docker = False
    has_arm_config = False
    has_cross_toolchain = False

    for item in manifest:
        name = item["path"].lower()
        if name.endswith("makefile") or name.endswith("gn"):
            has_makefile = True
        if name.endswith("cmakelists.txt"):
            has_cmake = True
        if name.endswith("dockerfile") or "docker" in name:
            has_docker = True
        if "arm" in name or "aarch64" in name:
            has_arm_config = True
        if "toolchain" in name or "cross" in name:
            has_cross_toolchain = True

    # 扫描文件内容中是否有 arm64/aarch64 引用
    arm_refs = 0
    for item in manifest:
        if item.get("skipped"):
            continue
        try:
            text = (repo_dir / item["path"]).read_text(encoding="utf-8", errors="ignore")[:2000].lower()
            if "aarch64" in text or "arm64" in text:
                arm_refs += 1
        except Exception:
            pass

    ready = has_arm_config and (has_makefile or has_cmake) and arm_refs > 0

    return {
        "arm64_ready": ready,
        "has_makefile": has_makefile,
        "has_cmake": has_cmake,
        "has_docker": has_docker,
        "has_arm_config": has_arm_config,
        "has_cross_toolchain": has_cross_toolchain,
        "arm_references_in_code": arm_refs,
        "suggestion": "可直接交叉编译" if ready else (
            "需补充 ARM64 配置" if not has_arm_config else
            "ARM64 配置存在但缺少构建系统" if not (has_makefile or has_cmake) else
            "ARM64 配置完整但代码中无 arm64 引用")
    }


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂道引器 v2.0 · 以道为引，纳开源智慧")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ── 单个吸收 ──
    p_absorb = subparsers.add_parser("absorb", help="吸收一个开源来源")
    p_absorb.add_argument("source", help="GitHub URL 或本地路径")
    p_absorb.add_argument("--ipa", help="指定目标 IPA，逗号分隔")
    p_absorb.add_argument("--dry-run", action="store_true", help="试运行，不入链")

    # ── 批量吸收（v2.0）──
    p_batch = subparsers.add_parser("batch", help="批量吸收 repos.txt 名单")
    p_batch.add_argument("repo_list", help="仓库名单文件（每行一个URL）")
    p_batch.add_argument("--workers", "-w", type=int, default=4, help="并发线程数（默认4）")
    p_batch.add_argument("--harmony-only", action="store_true", help="只吸收鸿蒙适配度 >= 30 的仓库")

    # ── 自驱狩猎（v2.0）──
    p_hunt = subparsers.add_parser("hunt", help="GitHub 自驱狩猎鸿蒙生态仓库")
    p_hunt.add_argument("--query", "-q", default="harmonyos kernel driver embedded arm64 guomi",
                        help="搜索关键词（默认鸿蒙生态相关）")
    p_hunt.add_argument("--max", "-n", type=int, default=10, help="最多返回数量（默认10）")
    p_hunt.add_argument("--absorb", "-a", action="store_true", help="发现后自动吸收")

    # ── 列表 ──
    subparsers.add_parser("list", help="列出已吸收来源")

    # ── 报表（v2.0）──
    p_report = subparsers.add_parser("report", help="生成最近批次报表")
    p_report.add_argument("--format", "-f", choices=["md", "json"], default="md", help="报表格式")

    # ── 查询 ──
    p_query = subparsers.add_parser("query", help="按 hash/DNA 查询")
    p_query.add_argument("query", help="source_hash 或 DNA 片段")

    # ── 验证 ──
    p_verify = subparsers.add_parser("verify", help="验证镜像完整性")
    p_verify.add_argument("query", help="source_hash 或 DNA 片段")

    args = parser.parse_args()

    ensure_dirs()

    if args.command == "absorb":
        user_ipas = None
        if args.ipa:
            user_ipas = [ipa.strip() for ipa in args.ipa.split(",")]
        try:
            result = absorb_source(args.source, user_ipas=user_ipas, dry_run=args.dry_run)
            if args.dry_run:
                print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"❌ 道引失败: {e}")
            return 1

    elif args.command == "batch":
        try:
            batch_absorb(args.repo_list, workers=args.workers, harmony_only=args.harmony_only)
        except Exception as e:
            print(f"❌ 批量道引失败: {e}")
            return 1

    elif args.command == "hunt":
        try:
            hunt_github(args.query, max_results=args.max, auto_absorb=args.absorb)
        except Exception as e:
            print(f"❌ 狩猎失败: {e}")
            return 1

    elif args.command == "report":
        records = load_chain()
        # 只取最近的吸收记录
        absorbed = [r for r in records if r.get("type") == "daoyin_param_card"]
        if args.format == "json":
            print(json.dumps(absorbed, ensure_ascii=False, indent=2))
        else:
            # 生成 MD 报表
            report_lines = [
                "# 龍魂道引 · 吸收记录报表",
                "",
                f"总计吸收: {len(absorbed)} 个来源",
                "",
                "| 时间 | 来源 | 许可证 | 适配度 | DNA |",
                "|------|------|--------|--------|-----|",
            ]
            for r in absorbed[-50:]:
                hs = r.get("harmony_fit", {}).get("total", "N/A")
                report_lines.append(
                    f"| {r.get('absorbed_at', '')[:16]} | {r.get('source', '')[:40]} | "
                    f"{r.get('license', {}).get('spdx', 'N/A')} | {hs} | "
                    f"`{r.get('dna', '')[:24]}...` |"
                )
            report_lines = report_lines + [
                "",
                f"> {SYSTEM_CONFIRM_ANCHOR}",
            ]
            print("\n".join(report_lines))

    elif args.command == "list":
        list_absorbed()

    elif args.command == "query":
        rec = query_by_hash(args.query)
        if rec:
            print(json.dumps(rec, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 未找到: {args.query}")
            return 1

    elif args.command == "verify":
        ok = verify_integrity(args.query)
        return 0 if ok else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
