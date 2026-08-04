#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 全设备知识孤儿收割机 v1.0
扫描 /Users 下所有用户目录，识别并归集 UID9622 的知识/代码/笔记文件。
DNA: #龍芯⚡️2026-06-26-DEVICE-HARVESTER-v1.0
"""

import hashlib
import json
import os
import re
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, Set, Tuple, Any

HOME = Path.home()
DB_PATH = HOME / "_work" / "dragon_knowledge.db"
SCAN_ROOT = Path("/Users")
WORK_DIR = Path("/tmp") / "longhun_device_harvester"
WORK_DIR.mkdir(parents=True, exist_ok=True)

CST = timezone(timedelta(hours=8))
DNA_SIGNATURE = "#龍芯⚡️2026-06-26-DEVICE-HARVESTER-v1.0"

# 允许的文件扩展名
ALLOWED_EXTS = {
    '.py', '.md', '.json', '.yaml', '.yml', '.txt', '.skill',
    '.sh', '.swift', '.m', '.h', '.cpp', '.hpp', '.c', '.mm',
    '.js', '.ts', '.jsx', '.tsx', '.vue', '.html', '.css',
    '.toml', '.ini', '.cfg', '.conf', '.sql', '.log',
}

# 忽略的目录
IGNORE_DIRS = {
    '__pycache__', 'node_modules', '.git', '.svn', '.hg',
    '.venv', 'venv', 'env', '.tox', '.pytest_cache', '.mypy_cache',
    'dist', 'build', 'target', '.idea', '.vscode', '.DS_Store',
    'Pods', 'Carthage', '.build', '.gradle', 'bin', 'obj',
    'Caches', 'Cache', 'tmp', 'temp', 'logs', 'log',
    '.npm', '.yarn', '.pnpm', '.cargo', '.rustup', '.gradle',
    'site-packages', 'lib', 'lib64', 'include', 'share',
    'Applications', 'Library', 'Pictures', 'Movies', 'Music',
    'Public', 'Movies', 'Desktop',
    'Epic Games', 'UnrealEngine', 'UE_5.7', 'Previously Relocated Items',
    'Relocated Items', 'DTCloudPrinter', 'SC Info',
}

# 敏感文件模式
SENSITIVE_PATTERNS = [
    r'\.env', r'\.envrc', r'\.bashrc', r'\.zshrc', r'\.profile',
    r'\.ssh', r'\.gnupg', r'\.aws', r'\.kube', r'\.docker',
    r'id_rsa', r'id_ed25519', r'id_dsa', r'\.pem', r'\.p12',
    r'\.key', r'\.crt', r'\.cer', r'keystore', r'truststore',
    r'password', r'secret', r'token', r'api_key', r'apikey',
    r'credentials', r'cookie', r'session',
]
SENSITIVE_RE = re.compile('|'.join(SENSITIVE_PATTERNS), re.I)

# 血脉标记
STRONG_MARKERS = [
    "龍魂", "龍芯", "CNSH", "UID9622", "君子协议", "DNA", "河图洛书",
    "易经", "太极", "五行", "八卦", "六十四卦", "洛书", "通心译",
    "longhun", "dragon soul", "德者永生殿", "铁律", "主权",
    "魂灵", "星闪", "鸿蒙", "北斗", "龍芯", "数字人", "曾老师",
    "Zhuge Xin", "诸葛鑫", "龍芯北辰",
]
WEAK_MARKERS = [
    "python", "script", "module", "skill", "知识库", "协议", "规范",
    "审计", "追溯", "检查", "引擎", "计算", "公式", "算法",
    "架构", "设计", "实现", "部署", "测试", "笔记", "文档",
]

SENSITIVE_DOMAINS = {
    "github.com", "gitlab.com", "bitbucket.org",
    "huggingface.co", "openai.com", "anthropic.com",
    "google.com", "microsoft.com", "amazon.com",
    "twitter.com", "x.com", "facebook.com", "meta.com",
}


def now_iso():
    return datetime.now(CST).isoformat()


def sha256_short(text: str, length=16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def sha256_full(data) -> str:
    if isinstance(data, bytes):
        return hashlib.sha256(data).hexdigest()
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def is_sensitive_file(path: Path) -> bool:
    """判断是否为敏感文件"""
    name = path.name.lower()
    parts = [p.lower() for p in path.parts]
    
    # 路径或文件名匹配敏感模式
    if SENSITIVE_RE.search(str(path)):
        return True
    
    # 隐藏目录中的文件（除了 .kimi-code/skills 等明确白名单）
    for part in parts:
        if part.startswith('.') and part not in {'.kimi-code', '.longhun', '.cnsh', '.claude'}:
            if part in {'.ssh', '.gnupg', '.aws', '.kube', '.docker', '.npm', '.yarn'}:
                return True
    
    return False


def is_ignored_dir(path: Path) -> bool:
    """判断是否应跳过的目录"""
    for part in path.parts:
        if part in IGNORE_DIRS:
            return True
    return False


def compute_bloodline_score(text: str) -> int:
    score = 0
    text_lower = text.lower()
    for m in STRONG_MARKERS:
        if m.lower() in text_lower:
            score += 3
    for m in WEAK_MARKERS:
        if m.lower() in text_lower:
            score += 1
    return score


def extract_meta(text: str, filename: str) -> Dict[str, Any]:
    meta = {
        "dna": "",
        "version": "",
        "description": "",
        "author": "",
        "title": filename,
    }
    dna_match = re.search(r'#龍芯[⚡️][^\s\n]+', text)
    if dna_match:
        meta["dna"] = dna_match.group(0)
    ver_match = re.search(r'v(\d+\.\d+(?:\.\d+)?)', text[:2000])
    if ver_match:
        meta["version"] = ver_match.group(1)
    if "UID9622" in text:
        meta["author"] = "UID9622"
    
    # 描述
    lines = []
    for line in text.split('\n')[:30]:
        line = line.strip()
        if line.startswith('#') or line.startswith('//'):
            cleaned = line.lstrip('#').lstrip('/').strip()
            if cleaned and len(cleaned) > 5:
                lines.append(cleaned)
        elif line and not line.startswith('```') and len(lines) < 3:
            if len(line) > 10:
                lines.append(line)
    if lines:
        meta["description"] = " | ".join(lines[:3])[:200]
    return meta


def scan_files(output_json: Path, max_files: int = 100000, max_size: int = 5*1024*1024) -> int:
    """扫描文件并保存清单"""
    found = []
    count = 0
    
    for user_dir in SCAN_ROOT.iterdir():
        if not user_dir.is_dir():
            continue
        print(f"扫描用户目录: {user_dir}")
        
        try:
            for root, dirs, files in os.walk(user_dir, topdown=True):
                root_path = Path(root)
                
                # 过滤目录
                dirs[:] = [d for d in dirs if not is_ignored_dir(root_path / d) and not d.startswith('.')]
                
                for file in files:
                    if count >= max_files:
                        break
                    
                    file_path = root_path / file
                    
                    # 扩展名检查
                    if file_path.suffix.lower() not in ALLOWED_EXTS:
                        continue
                    
                    # 大小检查
                    try:
                        size = file_path.stat().st_size
                        if size == 0 or size > max_size:
                            continue
                    except (PermissionError, OSError):
                        continue
                    
                    # 敏感文件检查
                    if is_sensitive_file(file_path):
                        continue
                    
                    found.append({
                        "path": str(file_path),
                        "rel_path": str(file_path.relative_to(SCAN_ROOT)) if SCAN_ROOT in file_path.parents else str(file_path),
                        "size": size,
                        "ext": file_path.suffix.lower(),
                    })
                    count += 1
                    
                    if count % 1000 == 0:
                        print(f"  已发现 {count} 个候选文件...")
        except PermissionError:
            print(f"  无权限访问 {user_dir}，跳过")
        except Exception as e:
            print(f"  扫描 {user_dir} 出错: {e}")
    
    output_json.write_text(json.dumps(found, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n扫描完成，共发现 {count} 个候选文件，清单保存到 {output_json}")
    return count


def analyze_bloodline(input_json: Path, output_json: Path):
    """对候选文件做血脉识别"""
    candidates = json.loads(input_json.read_text(encoding="utf-8"))
    results = []
    
    for item in candidates:
        path = Path(item["path"])
        try:
            content = path.read_bytes()
            text = content.decode('utf-8', errors='ignore')
        except Exception:
            continue
        
        file_hash = sha256_full(content)
        bloodline = compute_bloodline_score(text)
        meta = extract_meta(text, path.name)
        
        # 检查外网敏感域名
        sensitive_urls = [d for d in SENSITIVE_DOMAINS if d in text]
        
        # 判定
        if sensitive_urls and bloodline < 6:
            level = "RED"
            passed = False
        elif bloodline < 2:
            level = "RED"
            passed = False
        elif bloodline >= 6 and not sensitive_urls and meta["dna"] and meta["author"]:
            level = "GREEN"
            passed = True
        else:
            level = "YELLOW"
            passed = True
        
        results.append({
            **item,
            "file_hash": file_hash,
            "bloodline": bloodline,
            "dna": meta["dna"],
            "version": meta["version"],
            "title": meta["title"],
            "description": meta["description"],
            "author": meta["author"],
            "shield_level": level,
            "shield_passed": passed,
            "sensitive_urls": sensitive_urls,
            "snippet": text[:500].replace('\x00', ''),
        })
        
        if len(results) % 500 == 0:
            print(f"  已分析 {len(results)} 个文件...")
    
    output_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n血脉分析完成，共 {len(results)} 个文件，结果保存到 {output_json}")
    return results


def main():
    print("🐉 龍魂 · 全设备知识孤儿收割机 v1.0\n")
    print(f"扫描根目录: {SCAN_ROOT}")
    print(f"数据库: {DB_PATH}")
    print(f"DNA: {DNA_SIGNATURE}\n")
    
    candidates_json = WORK_DIR / "candidates.json"
    analyzed_json = WORK_DIR / "analyzed.json"
    
    # 阶段1：扫描
    count = scan_files(candidates_json)
    if count == 0:
        print("未发现候选文件")
        return
    
    # 阶段2：血脉识别
    results = analyze_bloodline(candidates_json, analyzed_json)
    
    # 统计
    total = len(results)
    passed = sum(1 for r in results if r["shield_passed"])
    green = sum(1 for r in results if r["shield_level"] == "GREEN")
    yellow = sum(1 for r in results if r["shield_level"] == "YELLOW")
    red = sum(1 for r in results if r["shield_level"] == "RED")
    
    print(f"\n=== 扫描统计 ===")
    print(f"候选文件总数: {total}")
    print(f"通过导入: {passed}")
    print(f"  🟢 GREEN: {green}")
    print(f"  🟡 YELLOW: {yellow}")
    print(f"  🔴 RED: {red}")
    print(f"\n详细结果: {analyzed_json}")


if __name__ == "__main__":
    main()
