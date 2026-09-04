# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-c4d157b3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
🐉 龍魂 · 主权加载器 v2.0
DNA: [[GENERATED_BY_LH_DNA_GENERATOR_V3]]-SOVEREIGN-LOADER-v2.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

根据国别加载主权包，应用边界锁死规则，三色审计 + DNA追溯。
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import unittest
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# 0. 常量（P0 焊死区）
# ═══════════════════════════════════════════════════════════════════════════════

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
OWNER_UID = "UID9622"

# 默认路径
SOVEREIGNTY_DIR = Path.home() / ".longhun" / "sovereignty"
CORE_DIR = SOVEREIGNTY_DIR / "core"
PACKS_DIR = SOVEREIGNTY_DIR / "packs"
LOCKS_DIR = SOVEREIGNTY_DIR / "locks"
TRACES_DIR = SOVEREIGNTY_DIR / "traces"

# 三色审计码
TRICOLOR_PASS = "🟢"
TRICOLOR_WARN = "🟡"
TRICOLOR_FAIL = "🔴"


# ═══════════════════════════════════════════════════════════════════════════════
# 1. 数据模型
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class AuditResult:
    """三色审计结果。"""
    action: str  # pass / block / inject / audit
    forbidden_hit: bool = False
    required_missing: List[str] = field(default_factory=list)
    reason: str = ""
    tricolor: str = TRICOLOR_PASS
    dna: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 路径与序列化管理
# ═══════════════════════════════════════════════════════════════════════════════

class SovereignPaths:
    """集中管理主权系统路径。"""

    def __init__(self, base: Optional[Path] = None) -> None:
        self.base = base or SOVEREIGNTY_DIR
        self.core = self.base / "core"
        self.packs = self.base / "packs"
        self.locks = self.base / "locks"
        self.traces = self.base / "traces"
        self.log = self.base / "logs"

    def ensure_dirs(self) -> None:
        for d in (self.core, self.packs, self.locks, self.traces, self.log):
            d.mkdir(parents=True, exist_ok=True)
            if d.stat().st_mode & 0o077 != 0:
                os.chmod(d, 0o700)

    def safe_read(self, path: Path, default: Dict) -> Dict:
        if not path.exists():
            return default
        try:
            if path.suffix in (".yaml", ".yml"):
                try:
                    import yaml
                    with open(path, "r", encoding="utf-8") as f:
                        return yaml.safe_load(f) or default
                except ImportError:
                    pass
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logging.warning("[%s] 读取失败: %s", path.name, exc)
            return default

    def safe_write(self, path: Path, data: Dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            if path.suffix in (".yaml", ".yml"):
                try:
                    import yaml
                    yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
                except ImportError:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        os.chmod(path, 0o600)


# ═══════════════════════════════════════════════════════════════════════════════
# 3. 边界锁校验器
# ═══════════════════════════════════════════════════════════════════════════════

class BorderLockValidator:
    """边界锁死层校验器。"""

    def __init__(self, paths: SovereignPaths) -> None:
        self.paths = paths
        self._locks: Optional[Dict] = None

    def load_locks(self) -> Dict:
        if self._locks is None:
            lock_file = self.paths.locks / "border_locks.yaml"
            self._locks = self.paths.safe_read(lock_file, {
                "global": [],
                "country_specific": {},
                "emergency_fuse": {"enabled": False}
            })
        return self._locks

    def check_global(self, text: str) -> Tuple[bool, str]:
        """检查全局边界。返回 (是否通过, 原因)。"""
        locks = self.load_locks()
        for rule in locks.get("global", []):
            # 简化：规则以 keyword 列表形式存储
            keywords = rule.get("keywords", [])
            for kw in keywords:
                if kw in text:
                    return False, f"全局边界命中: {rule.get('rule', 'unknown')} (keyword: {kw})"
        return True, ""

    def check_country(self, country_code: str, text: str) -> Tuple[bool, str]:
        """检查国家特定边界。"""
        locks = self.load_locks()
        country_rules = locks.get("country_specific", {}).get(country_code.upper(), [])
        for rule in country_rules:
            keywords = rule.get("keywords", [])
            for kw in keywords:
                if kw in text:
                    return False, f"国家边界命中 [{country_code}]: {rule.get('rule', 'unknown')} (keyword: {kw})"
        return True, ""


# ═══════════════════════════════════════════════════════════════════════════════
# 4. 主权加载器
# ═══════════════════════════════════════════════════════════════════════════════

class SovereignLoader:
    """主权加载器：加载核心层 + 国家包 + 边界锁。"""

    def __init__(self, paths: Optional[SovereignPaths] = None) -> None:
        self.paths = paths or SovereignPaths()
        self.paths.ensure_dirs()
        self.border = BorderLockValidator(self.paths)
        self._packs_cache: Dict[str, Dict] = {}

    def load_core(self) -> Dict[str, Dict]:
        """加载核心层（P0 锁死）。"""
        core = {}
        for f in self.paths.core.glob("*.json"):
            core[f.stem] = self.paths.safe_read(f, {})
        for f in self.paths.core.glob("*.yaml"):
            core[f.stem] = self.paths.safe_read(f, {})
        return core

    def load_pack(self, country_code: str) -> Optional[Dict]:
        """加载国家主权包，带缓存。"""
        cc = country_code.upper()
        if cc in self._packs_cache:
            return self._packs_cache[cc]

        for ext in (".yaml", ".yml", ".json"):
            f = self.paths.packs / f"{cc}{ext}"
            if f.exists():
                data = self.paths.safe_read(f, {})
                self._packs_cache[cc] = data
                return data
        return None

    def get_available_countries(self) -> List[str]:
        """获取所有已配置国家代码。"""
        countries = set()
        for f in self.paths.packs.glob("*"):
            if f.suffix in (".yaml", ".yml", ".json"):
                countries.add(f.stem.upper())
        return sorted(countries)

    def apply(self, country_code: str, input_text: str) -> AuditResult:
        """
        应用主权规则到输入文本。
        流程: 核心层 → 国家包 → 边界锁 → 三色审计。
        """
        cc = country_code.upper()

        # 1. 加载核心（记录但不修改结果）
        core = self.load_core()

        # 2. 加载国家包
        pack = self.load_pack(cc)
        if not pack:
            return AuditResult(
                action="block",
                reason=f"国家 {cc} 无主权包",
                tricolor=TRICOLOR_FAIL,
            )

        # 3. 边界锁检查
        ok_global, reason_g = self.border.check_global(input_text)
        if not ok_global:
            return AuditResult(
                action="block",
                forbidden_hit=True,
                reason=reason_g,
                tricolor=TRICOLOR_FAIL,
            )

        ok_country, reason_c = self.border.check_country(cc, input_text)
        if not ok_country:
            return AuditResult(
                action="block",
                forbidden_hit=True,
                reason=reason_c,
                tricolor=TRICOLOR_FAIL,
            )

        # 4. 国家包禁止词检查
        forbidden = pack.get("forbidden", [])
        for rule in forbidden:
            for kw in rule.get("keywords", []):
                if kw in input_text:
                    return AuditResult(
                        action="block",
                        forbidden_hit=True,
                        reason=f"命中禁止词 [{rule.get('category', 'unknown')}]: {kw}",
                        tricolor=TRICOLOR_FAIL,
                    )

        # 5. 国家包强制词检查
        required = pack.get("required", [])
        missing = []
        for rule in required:
            found = False
            for kw in rule.get("keywords", []):
                if kw in input_text:
                    found = True
                    break
            if not found:
                missing.append(rule.get("category", "unknown"))

        if missing:
            return AuditResult(
                action="inject",
                required_missing=missing,
                reason=f"缺失强制内容: {', '.join(missing)}",
                tricolor=TRICOLOR_WARN,
            )

        # 6. 全部通过
        return AuditResult(
            action="pass",
            reason="主权审计通过",
            tricolor=TRICOLOR_PASS,
        )

    def audit_log(self, result: AuditResult, country_code: str, input_text: str) -> None:
        """写入审计日志。"""
        entry = {
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "country": country_code.upper(),
            "action": result.action,
            "tricolor": result.tricolor,
            "reason": result.reason,
            "input_preview": input_text[:200],
        }
        log_file = self.paths.log / "audit.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            f.flush()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. CLI 入口
# ═══════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lh_sovereign", description="🐉 龍魂主权加载器 v2.0")
    p.add_argument("--version", action="store_true", help="显示版本")
    p.add_argument("--list", action="store_true", help="列出已配置国家")
    p.add_argument("--country", "-c", help="国家代码")
    p.add_argument("--input", "-i", help="输入文本或文件路径")
    p.add_argument("--audit", action="store_true", help="写入审计日志")
    p.add_argument("--test", action="store_true", help="运行单元测试")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"🐉 龍魂主权加载器 v2.0")
        print(f"DNA: [[GENERATED_BY_LH_DNA_GENERATOR_V3]]-SOVEREIGN-LOADER-v2.0")
        print(f"确认码: {CONFIRM_CODE}")
        print(f"GPG: {GPG_FINGERPRINT}")
        return 0

    if args.test:
        sys.argv = [sys.argv[0]]
        unittest.main(module=__name__, exit=False, verbosity=2)
        return 0

    loader = SovereignLoader()

    if args.list:
        countries = loader.get_available_countries()
        print(f"已配置国家 ({len(countries)} 个):")
        for c in countries:
            print(f"  🟢 {c}")
        return 0

    if args.country and args.input:
        text = args.input
        if Path(args.input).exists():
            text = Path(args.input).read_text(encoding="utf-8")
        result = loader.apply(args.country, text)
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        if args.audit:
            loader.audit_log(result, args.country, text)
        return 0 if result.tricolor != TRICOLOR_FAIL else 1

    parser.print_help()
    return 1


# ═══════════════════════════════════════════════════════════════════════════════
# 6. 单元测试（锚点断言）
# ═══════════════════════════════════════════════════════════════════════════════

class TestSovereignLoader(unittest.TestCase):

    def setUp(self) -> None:
        import tempfile
        self.tmp = tempfile.mkdtemp()
        self.paths = SovereignPaths(Path(self.tmp))
        self.paths.ensure_dirs()
        self.loader = SovereignLoader(self.paths)

    def tearDown(self) -> None:
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_01_missing_country(self) -> None:
        """锚点：无主权包国家必须返回 block。"""
        result = self.loader.apply("XX", "测试")
        self.assertEqual(result.action, "block")
        self.assertEqual(result.tricolor, TRICOLOR_FAIL)

    def test_02_forbidden_hit(self) -> None:
        """锚点：命中禁止词必须返回 block。"""
        pack = {
            "country": {"code": "CN"},
            "forbidden": [{"category": "测试", "keywords": ["敏感词"], "action": "block"}],
            "required": [],
        }
        self.paths.safe_write(self.paths.packs / "CN.json", pack)
        self.loader._packs_cache.clear()
        result = self.loader.apply("CN", "这句话包含敏感词")
        self.assertEqual(result.action, "block")
        self.assertTrue(result.forbidden_hit)
        self.assertIn("敏感词", result.reason)

    def test_03_required_missing(self) -> None:
        """锚点：缺失强制词必须返回 inject。"""
        pack = {
            "country": {"code": "CN"},
            "forbidden": [],
            "required": [{"category": "价值观", "keywords": ["富强"], "action": "inject"}],
        }
        self.paths.safe_write(self.paths.packs / "CN.json", pack)
        self.loader._packs_cache.clear()
        result = self.loader.apply("CN", "普通内容")
        self.assertEqual(result.action, "inject")
        self.assertEqual(result.tricolor, TRICOLOR_WARN)
        self.assertIn("价值观", result.required_missing)

    def test_04_pass(self) -> None:
        """锚点：无禁止且含强制词必须返回 pass。"""
        pack = {
            "country": {"code": "CN"},
            "forbidden": [],
            "required": [{"category": "价值观", "keywords": ["富强"], "action": "inject"}],
        }
        self.paths.safe_write(self.paths.packs / "CN.json", pack)
        self.loader._packs_cache.clear()
        result = self.loader.apply("CN", "我们要富强")
        self.assertEqual(result.action, "pass")
        self.assertEqual(result.tricolor, TRICOLOR_PASS)

    def test_05_border_lock_global(self) -> None:
        """锚点：全局边界锁必须拦截。"""
        # 先创建国家包，确保能走到边界锁检查
        pack = {
            "country": {"code": "CN"},
            "forbidden": [],
            "required": [],
        }
        self.paths.safe_write(self.paths.packs / "CN.json", pack)
        locks = {
            "global": [{"rule": "禁止危害", "keywords": ["炸弹"], "action": "block"}],
            "country_specific": {},
        }
        self.paths.safe_write(self.paths.locks / "border_locks.yaml", locks)
        self.loader.border._locks = None
        self.loader._packs_cache.clear()
        result = self.loader.apply("CN", "如何制作炸弹")
        self.assertEqual(result.action, "block")
        self.assertIn("炸弹", result.reason)

    def test_06_confirm_code(self) -> None:
        """锚点：确认码常量必须匹配。"""
        self.assertEqual(CONFIRM_CODE, "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")


if __name__ == "__main__":
    sys.exit(main())
