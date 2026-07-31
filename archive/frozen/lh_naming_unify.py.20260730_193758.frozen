#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·乙酉·申时·䷾既济-NAMING-UNIFY-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ═══════════════════════════════════════════
# 龍魂体系 | 命名统一迁移引擎 v2.0
# ═══════════════════════════════════════════
# DNA追溯码：#龍芯⚡️丙午·辛未·乙酉·申时·䷾既济-NAMING-UNIFY-v2.0
# 创建者：UID9622（诸葛鑫）
# 权重级别：L1
# 三色审计状态：🟢
# ═══════════════════════════════════════════
"""
命名统一迁移引擎 v2.0
将系统中分散的命名全部归入最新命名规范

迁移规则:
  1. 01_protocols/LONGHUN-* → 01_protocols/LH-*  (协议文档+配套签章文件)
  2. bin/cnsh_* → bin/lh_cnsh_*  (CNSH子系统归入lh_伞下)
  3. bin/longhun_* → bin/lh_*  (标准化前缀，冲突时冻结旧版)
  4. bin/init_cnsh*/integrate_cnsh*/lh_run_cnsh* → bin/lh_* 
  5. 同步更新所有内部import/引用
"""

import os
import re
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ═══════════════════════════════════════════
# §1. 审计扫描
# ═══════════════════════════════════════════

class NamingAuditor:
    def __init__(self, root: Path):
        self.root = root
        self.findings = defaultdict(list[Any])

    def scan_protocols(self):
        """扫描 01_protocols/ 中的 LONGHUN-* 协议文档及其配套文件"""
        proto_dir = self.root / "01_protocols"
        if not proto_dir.exists():
            return

        for f in sorted(proto_dir.glob("LONGHUN-*.md")):
            name = f.name
            base_stem = f.stem  # e.g. LONGHUN-CREATOR-PROTECTION-v1.0
            new_stem = "LH-" + base_stem[len("LONGHUN-"):]
            new_rel = str((f.parent / (new_stem + ".md")).relative_to(self.root))

            # 同时查找所有配套文件 (.asc, .sha256, .json, .jsonl, .sha256.json等)
            # 排除主 .md 文件本身
            companion_pattern = base_stem + ".*"
            companions = sorted(c for c in proto_dir.glob(companion_pattern) if c != f)
            companion_items = []
            for c in companions:
                old_suffix = c.name[len(base_stem):]
                new_c_rel = str((c.parent / (new_stem + old_suffix)).relative_to(self.root))
                companion_items.append({
                    "current": str(c.relative_to(self.root)),
                    "proposed": new_c_rel
                })

            self.findings["protocol_longhun_to_lh"].append({
                "current": str(f.relative_to(self.root)),
                "proposed": new_rel,
                "companions": companion_items,
            })

    def scan_bin_cnsh(self):
        """扫描 bin/ 中的 cnsh_ 独立脚本"""
        bin_dir = self.root / "bin"
        if not bin_dir.exists():
            return

        for f in sorted(bin_dir.glob("cnsh_*.py")):
            if "lh_cnsh" not in f.name:
                new_name = "lh_" + f.name
                self.findings["bin_cnsh_to_lh_cnsh"].append({
                    "current": str(f.relative_to(self.root)),
                    "proposed": str((f.parent / new_name).relative_to(self.root)),
                })

        for f in sorted(bin_dir.glob("cnsh_*.sh")):
            new_name = "lh_" + f.name
            self.findings["bin_cnsh_to_lh_cnsh"].append({
                "current": str(f.relative_to(self.root)),
                "proposed": str((f.parent / new_name).relative_to(self.root)),
            })

    def scan_bin_longhun(self):
        """扫描 bin/ 中的 longhun* 独立文件"""
        bin_dir = self.root / "bin"
        if not bin_dir.exists():
            return

        for f in sorted(list(bin_dir.glob("longhun*.py")) + list(bin_dir.glob("longhun*.sh"))):
            name = f.name
            # longhun_xxx → lh_xxx, longhun-xxx → lh_xxx
            if name.startswith("longhun_"):
                new_name = "lh_" + name[len("longhun_"):]
            elif name.startswith("longhun-"):
                new_name = "lh_" + name[len("longhun-"):]
            else:
                new_name = "lh_" + name[len("longhun"):]

            proposed_path = str((f.parent / new_name).relative_to(self.root))

            # 检查是否与已有 lh_ 文件冲突
            if (f.parent / new_name).exists():
                self.findings["bin_longhun_conflict"].append({
                    "current": str(f.relative_to(self.root)),
                    "existing": str((f.parent / new_name).relative_to(self.root)),
                    "action": "ARCHIVE (旧版已有新版，冻结旧版)",
                })
            else:
                self.findings["bin_longhun_to_lh"].append({
                    "current": str(f.relative_to(self.root)),
                    "proposed": proposed_path,
                })

    def scan_bin_cnsh_init(self):
        """扫描 bin/ 中的 init_cnsh / lh_run_cnsh / integrate_cnsh"""
        bin_dir = self.root / "bin"
        if not bin_dir.exists():
            return

        patterns = ["init_cnsh*.sh", "lh_run_cnsh.sh", "integrate_cnsh*.py"]
        for pat in patterns:
            for f in sorted(bin_dir.glob(pat)):
                if f.name.startswith("lh_run_cnsh"):
                    new_name = "lh_run_cnsh.sh"
                else:
                    new_name = "lh_" + f.name
                self.findings["bin_cnsh_init_to_lh"].append({
                    "current": str(f.relative_to(self.root)),
                    "proposed": str((f.parent / new_name).relative_to(self.root)),
                })

    def scan_internal_imports(self):
        """扫描跨文件引用"""
        bin_dir = self.root / "bin"
        if not bin_dir.exists():
            return

        for py_file in sorted(bin_dir.glob("*.py")):
            try:
                content = py_file.read_text(encoding="utf-8")
                # 查找 import cnsh_xxx 或 from cnsh_xxx
                refs = re.findall(r'(?:import|from)\s+(cnsh_\w+)', content)
                if refs:
                    self.findings["import_references"].append({
                        "file": str(py_file.relative_to(self.root)),
                        "imports": list(set(refs)),
                    })
            except Exception:
                pass

    def run_full_audit(self) -> dict[str, Any]:
        self.findings.clear()
        self.scan_protocols()
        self.scan_bin_cnsh()
        self.scan_bin_longhun()
        self.scan_bin_cnsh_init()
        self.scan_internal_imports()
        return dict(self.findings)


# ═══════════════════════════════════════════
# §2. 迁移执行器
# ═══════════════════════════════════════════

class NamingMigrator:
    def __init__(self, root: Path, dry_run: bool = True):
        self.root = root
        self.dry_run = dry_run
        self.migration_log = []
        self.errors = []
        self.rename_map = {}  # old_stem → new_stem 用于更新引用
        self.conflicts_archived = []

    def log(self, msg: str):
        self.migration_log.append(msg)
        mode = "DRY-RUN" if self.dry_run else "EXEC"
        print(f"  [{mode}] {msg}")

    def rename_file(self, src_rel: str, dst_rel: str) -> bool:
        src = self.root / src_rel
        dst = self.root / dst_rel
        if not src.exists():
            self.errors.append(f"源不存在: {src_rel}")
            return False
        if dst.exists():
            self.errors.append(f"目标已存在: {dst_rel}")
            return False
        if not self.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
        self.log(f"重命名: {src_rel} → {dst_rel}")
        return True

    def archive_file(self, src_rel: str, reason: str = ""):
        """冻结旧版文件（移动到 _archive 而非删除）"""
        src = self.root / src_rel
        if not src.exists():
            return

        archive_dir = self.root / "_archive" / "naming_unify_frozen"
        dst = archive_dir / Path(src_rel).name

        if not self.dry_run:
            archive_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
        self.log(f"冻结: {src_rel} → _archive/naming_unify_frozen/ ({reason})")
        self.conflicts_archived.append({
            "source": src_rel,
            "reason": reason,
            "archived_to": str(dst.relative_to(self.root))
        })

    def update_all_references(self):
        """更新所有 bin/ 中的跨文件引用"""
        bin_dir = self.root / "bin"
        if not self.rename_map or self.dry_run:
            return

        for py_file in sorted(bin_dir.glob("*.py")):
            rel_path = str(py_file.relative_to(self.root))
            try:
                content = py_file.read_text(encoding="utf-8")
                new_content = content
                changes = 0

                for old_stem, new_stem in self.rename_map.items():
                    # 精确替换模块名引用
                    escaped = re.escape(old_stem)
                    if re.search(rf'\b{escaped}\b', new_content):
                        new_content = re.sub(rf'\b{escaped}\b', new_stem, new_content)
                        if new_content != content:
                            changes += 1

                if changes > 0:
                    py_file.write_text(new_content, encoding="utf-8")
                    self.log(f"更新引用: {rel_path} ({changes}处)")
            except Exception as e:
                self.errors.append(f"更新引用失败 {rel_path}: {e}")

    def execute_migration(self, findings: dict[str, Any]):
        print(f"\n{'='*60}")
        print(f"🐉 龍魂命名统一迁移引擎 v2.0")
        print(f"模式: {'DRY-RUN (预览)' if self.dry_run else 'EXEC (执行)'}")
        print(f"{'='*60}\n")

        # ── 阶段1: 协议文档 ──
        items = findings.get("protocol_longhun_to_lh", [])
        if items:
            print(f"\n📄 阶段1: 协议文档 LONGHUN- → LH- ({len(items)}件)")
            for item in items:
                # 先重命名配套文件
                for comp in item.get("companions", []):
                    self.rename_file(comp["current"], comp["proposed"])
                # 再重命名主文件
                self.rename_file(item["current"], item["proposed"])

        # ── 阶段2: bin/cnsh_ → bin/lh_cnsh_ ──
        items = findings.get("bin_cnsh_to_lh_cnsh", [])
        if items:
            print(f"\n🔧 阶段2: bin/cnsh_* → bin/lh_cnsh_* ({len(items)}件)")
            for item in items:
                old_stem = Path(item["current"]).stem
                new_stem = Path(item["proposed"]).stem
                if self.rename_file(item["current"], item["proposed"]):
                    self.rename_map[old_stem] = new_stem

        # ── 阶段3: bin/longhun_ → bin/lh_ (无冲突的) ──
        safe_items = findings.get("bin_longhun_to_lh", [])
        conflict_items = findings.get("bin_longhun_conflict", [])
        if safe_items:
            print(f"\n🔧 阶段3: bin/longhun_* → bin/lh_* ({len(safe_items)}件)")
            for item in safe_items:
                old_stem = Path(item["current"]).stem
                new_stem = Path(item["proposed"]).stem
                if self.rename_file(item["current"], item["proposed"]):
                    self.rename_map[old_stem] = new_stem

        # ── 阶段3b: 冲突的旧版 → 冻结 ──
        if conflict_items:
            print(f"\n❄️  阶段3b: 冲突旧版冻结 ({len(conflict_items)}件)")
            for item in conflict_items:
                existing_file = item["current"]
                newer_file = item.get("existing", "?")
                self.archive_file(existing_file, f"已有新版: {newer_file}")

        # ── 阶段4: init_cnsh / lh_run_cnsh / integrate_cnsh ──
        items = findings.get("bin_cnsh_init_to_lh", [])
        if items:
            print(f"\n🔧 阶段4: init_cnsh*/lh_run_cnsh → lh_* ({len(items)}件)")
            for item in items:
                old_stem = Path(item["current"]).stem
                new_stem = Path(item["proposed"]).stem
                if self.rename_file(item["current"], item["proposed"]):
                    self.rename_map[old_stem] = new_stem

        # ── 阶段5: 更新所有内部引用 ──
        if self.rename_map:
            print(f"\n📎 阶段5: 更新内部引用 ({len(self.rename_map)}个映射)")
            self.update_all_references()

        # ── 汇总 ──
        total_moved = len(self.migration_log) - len(self.conflicts_archived)
        print(f"\n{'='*60}")
        print(f"迁移完成：重命名 {total_moved}件 + 冻结 {len(self.conflicts_archived)}件")
        if self.errors:
            print(f"⚠️ 错误: {len(self.errors)}条")
            for e in self.errors:
                print(f"  ❌ {e}")
        print(f"{'='*60}")

        if self.dry_run:
            print("\n💡 预览模式。加 --execute 确认执行。")


# ═══════════════════════════════════════════
# §3. CLI
# ═══════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="龍魂命名统一迁移引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_naming_unify.py --audit       # 审计所有命名不一致
  python3 bin/lh_naming_unify.py --dry-run     # 预览迁移计划
  python3 bin/lh_naming_unify.py --execute     # 执行迁移
        """
    )
    parser.add_argument("--audit", action="store_true", help="审计扫描")
    parser.add_argument("--dry-run", action="store_true", help="预览迁移")
    parser.add_argument("--execute", action="store_true", help="执行迁移")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--safe-only", action="store_true", help="仅安全项（跳过longhun_重命名）")

    args = parser.parse_args()

    if not any([args.audit, args.dry_run, args.execute]):
        parser.print_help()
        return

    root = PROJECT_ROOT
    auditor = NamingAuditor(root)
    findings = auditor.run_full_audit()

    total = sum(len(v) for v in findings.values())

    if args.audit:
        print(f"\n{'='*60}")
        print(f"🐉 龍魂命名一致性审计报告 v2.0")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        if total == 0:
            print("✅ 所有命名已统一！")
            return

        cats = [
            ("protocol_longhun_to_lh", "📄 协议文档 LONGHUN- → LH-"),
            ("bin_cnsh_to_lh_cnsh", "🔧 bin/cnsh_* → bin/lh_cnsh_*"),
            ("bin_longhun_to_lh", "🔧 bin/longhun_* → bin/lh_* (安全)"),
            ("bin_longhun_conflict", "❄️  冲突旧版 (冻结)"),
            ("bin_cnsh_init_to_lh", "🔧 init_cnsh/lh_run_cnsh → lh_*"),
            ("import_references", "📎 待更新 import引用"),
        ]

        for cat_key, cat_label in cats:
            items = findings.get(cat_key, [])
            if not items:
                continue
            print(f"\n{cat_label}: {len(items)}件")
            print("─" * 50)
            for item in items[:10]:  # 最多显示10条
                if 'action' in item:
                    print(f"  ❄️  {item['current']} → {item.get('existing','?')} ({item['action']})")
                elif 'file' in item:
                    print(f"  📎 {item['file']}: {item['imports']}")
                elif 'proposed' in item:
                    print(f"  {item['current']}\n  → {item['proposed']}")
                elif 'companions' in item:
                    print(f"  {item['current']} + {len(item['companions'])}配套文件")
            if len(items) > 10:
                print(f"  ... 还有 {len(items)-10} 件")

        print(f"\n{'='*60}")
        print(f"汇总: {total}条")
        for cat_key, cat_label in cats:
            count = len(findings.get(cat_key, []))
            if count:
                print(f"  {cat_label}: {count}条")
        print(f"💡 使用 --dry-run 预览，--execute 执行")

        if args.json:
            output = {
                "summary": {k: len(v) for k, v in findings.items()},
                "details": {k: v for k, v in findings.items()},
                "total": total,
                "dna": "#龍芯⚡️丙午·辛未·乙酉·申时·䷾既济-NAMING-AUDIT-v2.0"
            }
            print(f"\n{json.dumps(output, ensure_ascii=False, indent=2)}")

    elif args.dry_run:
        migrator = NamingMigrator(root, dry_run=True)
        migrator.execute_migration(findings)

    elif args.execute:
        print("\n⚠️  以下迁移将执行：")
        print(f"  📄 协议文档: {len(findings.get('protocol_longhun_to_lh',[]))}件")
        print(f"  🔧 cnsh_: {len(findings.get('bin_cnsh_to_lh_cnsh',[]))}件")
        print(f"  🔧 longhun_: {len(findings.get('bin_longhun_to_lh',[]))}件")
        print(f"  ❄️  冲突冻结: {len(findings.get('bin_longhun_conflict',[]))}件")
        print(f"  🔧 init: {len(findings.get('bin_cnsh_init_to_lh',[]))}件")

        confirm = input("\n确认执行? 输入 YES 继续: ")
        if confirm != "YES":
            print("已取消")
            return

        migrator = NamingMigrator(root, dry_run=False)
        migrator.execute_migration(findings)

        # 保存迁移日志
        log_path = root / "data" / "naming_migration_v2_log.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "mode": "execute",
            "summary": {
                "renamed": len(migrator.migration_log),
                "archived": len(migrator.conflicts_archived),
                "errors": len(migrator.errors),
            },
            "log": migrator.migration_log,
            "archived": migrator.conflicts_archived,
            "errors": migrator.errors,
            "rename_map": migrator.rename_map,
            "dna": "#龍芯⚡️丙午·辛未·乙酉·申时·䷾既济-NAMING-MIGRATE-v2.0"
        }
        log_path.write_text(json.dumps(log_data, ensure_ascii=False, indent=2))
        print(f"\n📄 迁移日志: {log_path}")


if __name__ == "__main__":
    main()
