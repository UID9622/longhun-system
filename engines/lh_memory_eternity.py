#!/usr/bin/env python3
#龍芯⚡️2026-07-25-MEMORY-ETERNITY-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂体系 | 记忆永存引擎 v1.0
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️2026-07-25-MEMORY-ETERNITY-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: UID9622（诸葛鑫·Lucky）
# 三色审计: 🟢 通过
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ═══════════════════════════════════════════
# 存储层: 记忆永生管道第三环
# 多格式快照·跨平台同步·跨模型适配·时间锚定·恢复验证
# 确保记忆不因模型升级/平台迁移/时间流逝而丢失
#
# 上游: engines/lh_exobrain_compressor.py (压缩层)
# 配合: bin/lh_memory_api.py (记忆API)
#        bin/lh_memory_load.py (记忆加载器)
#
# 用法:
#   python3 engines/lh_memory_eternity.py snapshot                    # 生成三格式快照
#   python3 engines/lh_memory_eternity.py sync                        # 跨平台同步
#   python3 engines/lh_memory_eternity.py verify                      # 完整性验证
#   python3 engines/lh_memory_eternity.py recover --from <快照路径>    # 从快照恢复
#   python3 engines/lh_memory_eternity.py status                      # 系统状态
#   python3 engines/lh_memory_eternity.py health                      # 健康检查
# ═══════════════════════════════════════════
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─── 项目路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MEMORY_DIR = PROJECT_ROOT / ".codebuddy" / "memory"
SNAPSHOT_DIR = PROJECT_ROOT / "state" / "eternity" / "snapshots"
BACKUP_DIR = PROJECT_ROOT / "state" / "eternity" / "backups"
STATE_FILE = PROJECT_ROOT / "state" / "eternity" / "eternity_state.json"
SYNC_LOG = PROJECT_ROOT / "state" / "eternity" / "sync_log.jsonl"

for d in [SNAPSHOT_DIR, BACKUP_DIR, STATE_FILE.parent, SYNC_LOG.parent]:
    d.mkdir(parents=True, exist_ok=True)

# ─── 同步目标配置 ───
KUNPENG_HOST = os.environ.get("LH_KUNPENG_HOST", "119.13.90.27")
KUNPENG_USER = os.environ.get("LH_KUNPENG_USER", "root")
SSH_KEY = os.environ.get("LH_SSH_KEY", os.path.expanduser("~/.ssh/longhun_kunpeng_ed25519"))
KUNPENG_MEMORY_PATH = "/root/longhun-system/.codebuddy/memory/"


def _is_local_target() -> bool:
    """检测当前机器是否就是同步目标（鲲鹏本机执行时直接本地拷贝）。"""
    if KUNPENG_HOST in ("127.0.0.1", "localhost", "::1"):
        return True
    try:
        # 如果能直接写入目标路径，说明在本地
        target = Path(KUNPENG_MEMORY_PATH)
        target.mkdir(parents=True, exist_ok=True)
        test_file = target / ".sync_write_test"
        test_file.write_text("ok")
        test_file.unlink()
        return True
    except Exception:
        return False


def _copy_local(src: Path, dst_dir: Path) -> Dict[str, Any]:
    """本地拷贝文件，替代 rsync+ssh。"""
    import shutil
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    try:
        shutil.copy2(str(src), str(dst))
        return {"状态": "🟢"}
    except Exception as e:
        return {"状态": "🔴", "错误": str(e)}

# 三份快照格式
SNAPSHOT_FORMATS = ["json", "markdown", "raw"]


def _sha256_file(path: Path) -> str:
    """计算文件SHA256"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        return json.loads(open(STATE_FILE, "r", encoding="utf-8").read())
    return {
        "快照": [],
        "同步记录": [],
        "验证记录": [],
        "创建时间": datetime.now(timezone.utc).isoformat(),
    }


def _save_state(state: Dict[str, Any]):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _append_sync_log(entry: Dict[str, Any]):
    with open(SYNC_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ═══════════════════════════════════════════
# 1. 多格式快照
# ═══════════════════════════════════════════

class MemorySnapshotter:
    """生成三份格式快照: JSON(机器可读)·Markdown(人类可读)·原始数据(完整备份)"""

    DNA = "#龍芯⚡️2026-07-25-MEMORY-SNAPSHOTTER-v1.0"

    def __init__(self):
        self.state = _load_state()

    def create_snapshot(self, trigger: str = "manual") -> Dict[str, Any]:
        """创建完整快照"""
        now = datetime.now(timezone.utc)
        now_str = now.strftime("%Y%m%d_%H%M%S")
        gan_str = self._ganzhi_timestamp(now)
        snapshot_id = f"snapshot_{now_str}"

        snapshot_path = SNAPSHOT_DIR / snapshot_id
        snapshot_path.mkdir(parents=True, exist_ok=True)

        # 收集所有记忆数据
        memory_data = self._collect_all_memory()

        # 1. JSON快照（机器可读）
        json_path = snapshot_path / f"memory_{snapshot_id}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=2)

        # 2. Markdown快照（人类可读）
        md_path = snapshot_path / f"memory_{snapshot_id}.md"
        md_content = self._to_markdown(memory_data)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # 3. 原始数据备份（完整tar.gz）
        raw_path = snapshot_path / f"memory_raw_{snapshot_id}.tar.gz"
        self._create_raw_backup(raw_path)

        # 计算哈希
        json_hash = _sha256_file(json_path)
        md_hash = _sha256_file(md_path)
        raw_hash = _sha256_file(raw_path)

        snapshot_record = {
            "快照ID": snapshot_id,
            "干支时间": gan_str,
            "ISO时间": now.isoformat(),
            "触发原因": trigger,
            "JSON哈希": json_hash,
            "Markdown哈希": md_hash,
            "原始备份哈希": raw_hash,
            "JSON大小": json_path.stat().st_size,
            "MD大小": md_path.stat().st_size,
            "原始备份大小": raw_path.stat().st_size,
            "记忆条目数": len(memory_data.get("结构化日志", [])),
            "DNA": self._generate_snapshot_dna(snapshot_id, json_hash),
        }

        self.state["快照"].append(snapshot_record)
        _save_state(self.state)

        return snapshot_record

    def _collect_all_memory(self) -> Dict[str, Any]:
        """收集所有记忆数据"""
        data = {
            "快照时间": datetime.now(timezone.utc).isoformat(),
            "MEMORY.md": "",
            "结构化日志": [],
            "日记忆文件": {},
            "文件清单": [],
        }

        # MEMORY.md
        memory_md = MEMORY_DIR / "MEMORY.md"
        if memory_md.exists():
            data["MEMORY.md"] = memory_md.read_text(encoding="utf-8")

        # 结构化日志
        daily_db = MEMORY_DIR / "daily_log_structured.jsonl"
        if daily_db.exists():
            with open(daily_db, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data["结构化日志"].append(json.loads(line))
                        except json.JSONDecodeError:
                            pass

        # 日记忆文件
        for md_file in sorted(MEMORY_DIR.glob("????-??-??.md")):
            stem = md_file.stem
            data["日记忆文件"][stem] = md_file.read_text(encoding="utf-8")

        # 文件清单
        for f in sorted(MEMORY_DIR.rglob("*")):
            if f.is_file():
                data["文件清单"].append({
                    "路径": str(f.relative_to(MEMORY_DIR)),
                    "大小": f.stat().st_size,
                    "修改时间": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                    "SHA256": _sha256_file(f),
                })

        return data

    def _to_markdown(self, data: Dict[str, Any]) -> str:
        """将记忆数据转为Markdown"""
        lines = [
            "# 龍魂记忆快照",
            "",
            f"快照时间: {data['快照时间']}",
            f"条目数: {len(data.get('结构化日志', []))}",
            f"日记忆文件: {len(data.get('日记忆文件', {}))}",
            "",
            "---",
            "",
            "## MEMORY.md",
            "```",
            data.get("MEMORY.md", "(空)"),
            "```",
            "",
            "---",
            "",
            "## 结构化日志",
            "",
        ]

        for entry in data.get("结构化日志", []):
            lines.append(f"### {entry.get('类型标签', '')} | {entry.get('时间', '')}")
            lines.append(f"- {entry.get('内容', '')}")
            extra = entry.get("扩展", {})
            for k, v in extra.items():
                lines.append(f"  - {k}: {v}")
            lines.append(f"  - DNA: `{entry.get('DNA', '')}`")
            lines.append("")

        return "\n".join(lines)

    def _create_raw_backup(self, output_path: Path):
        """创建原始数据tar.gz备份"""
        import tarfile
        with tarfile.open(output_path, "w:gz") as tar:
            for f in MEMORY_DIR.rglob("*"):
                if f.is_file():
                    arcname = str(f.relative_to(PROJECT_ROOT))
                    tar.add(f, arcname=arcname)

    def _ganzhi_timestamp(self, dt: datetime) -> str:
        """生成简化的干支时间戳"""
        tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        y = tiangan[(dt.year - 4) % 10] + dizhi[(dt.year - 4) % 12]
        m = tiangan[((dt.year - 4) * 12 + dt.month + 1) % 10] + dizhi[(dt.month + 1) % 12]
        d = tiangan[((dt.year - 4) * 365 + dt.timetuple().tm_yday + 4) % 10] + dizhi[(dt.timetuple().tm_yday + 4) % 12]
        return f"{y}·{m}·{d}"

    def _generate_snapshot_dna(self, snapshot_id: str, json_hash: str) -> str:
        now_str = datetime.now().strftime("%Y%m%d")
        return f"#龍芯⚡️{now_str}-MEMORY-SNAPSHOT-{json_hash[:8]}"

    def list_snapshots(self) -> List[Dict]:
        """列出所有快照"""
        return self.state.get("快照", [])

    def recover_from(self, snapshot_id: str) -> Dict[str, Any]:
        """从快照恢复记忆"""
        snapshot_path = SNAPSHOT_DIR / snapshot_id
        if not snapshot_path.exists():
            return {"状态": "🔴", "错误": f"快照 {snapshot_id} 不存在"}

        # 从原始备份恢复
        raw_path = snapshot_path / f"memory_raw_{snapshot_id}.tar.gz"
        if raw_path.exists():
            import tarfile
            with tarfile.open(raw_path, "r:gz") as tar:
                # 只恢复到临时目录，不直接覆盖
                temp_dir = MEMORY_DIR.parent / "_memory_recover_temp"
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
                temp_dir.mkdir(parents=True, exist_ok=True)
                tar.extractall(temp_dir)

            return {
                "状态": "🟢",
                "快照ID": snapshot_id,
                "恢复目标": str(temp_dir),
                "说明": "原始备份已解压到临时目录，请人工确认后覆盖",
            }

        return {"状态": "🔴", "错误": "快照中无原始备份文件"}


# ═══════════════════════════════════════════
# 2. 跨平台同步
# ═══════════════════════════════════════════

class CrossPlatformSyncer:
    """三地冗余: Mac本地 → 鲲鹏 → 香港备份"""

    DNA = "#龍芯⚡️2026-07-25-CROSS-PLATFORM-SYNCER-v1.0"

    def __init__(self):
        self.state = _load_state()

    def sync_to_kunpeng(self) -> Dict[str, Any]:
        """同步记忆到鲲鹏服务器。若当前就在鲲鹏上，则直接本地拷贝。"""
        now = datetime.now(timezone.utc).isoformat()
        is_local = _is_local_target()
        result = {
            "时间": now,
            "目标": f"{KUNPENG_USER}@{KUNPENG_HOST}:{KUNPENG_MEMORY_PATH}",
            "模式": "本地拷贝" if is_local else "SSH+rsync",
            "步骤": [],
        }

        if not is_local:
            # 检查SSH连通性
            try:
                ssh_test = subprocess.run(
                    ["ssh", "-i", SSH_KEY, "-o", "ConnectTimeout=5",
                     "-o", "BatchMode=yes", f"{KUNPENG_USER}@{KUNPENG_HOST}", "echo ok"],
                    capture_output=True, text=True, timeout=10
                )
                if ssh_test.returncode != 0:
                    result["状态"] = "🔴"
                    result["错误"] = f"SSH连接失败: {ssh_test.stderr.strip()}"
                    return result
            except Exception as e:
                result["状态"] = "🔴"
                result["错误"] = f"SSH异常: {e}"
                return result

        target_dir = Path(KUNPENG_MEMORY_PATH) if is_local else None

        def _transfer(src: Path):
            if is_local:
                return _copy_local(src, target_dir)
            try:
                r = subprocess.run(
                    ["rsync", "-avz", "-e", f"ssh -i {SSH_KEY}",
                     str(src), f"{KUNPENG_USER}@{KUNPENG_HOST}:{KUNPENG_MEMORY_PATH}"],
                    capture_output=True, text=True, timeout=30
                )
                return {"状态": "🟢" if r.returncode == 0 else "🔴", "错误": r.stderr.strip() if r.returncode != 0 else None}
            except Exception as e:
                return {"状态": "🔴", "错误": str(e)}

        # MEMORY.md
        mem_file = MEMORY_DIR / "MEMORY.md"
        if mem_file.exists():
            res = _transfer(mem_file)
            result["步骤"].append({"文件": "MEMORY.md", **res})

        # 结构化日志
        daily_db = MEMORY_DIR / "daily_log_structured.jsonl"
        if daily_db.exists():
            res = _transfer(daily_db)
            result["步骤"].append({"文件": "daily_log_structured.jsonl", **res})

        # 每日日志
        for daily_md in MEMORY_DIR.glob("????-??-??.md"):
            res = _transfer(daily_md)
            result["步骤"].append({"文件": daily_md.name, **res})

        all_ok = all(s.get("状态") == "🟢" for s in result["步骤"])
        result["状态"] = "🟢" if all_ok else "🟡"
        result["同步文件数"] = len(result["步骤"])

        # 记录同步日志
        _append_sync_log(result)
        self.state["同步记录"].append({
            "时间": now,
            "目标": "鲲鹏",
            "状态": result["状态"],
            "文件数": result["同步文件数"],
        })
        _save_state(self.state)

        return result

    def sync_all(self) -> Dict[str, Any]:
        """全量同步（鲲鹏 + 本地备份）"""
        results = {"时间": datetime.now(timezone.utc).isoformat(), "目标": []}

        # 1. 鲲鹏同步
        kunpeng_result = self.sync_to_kunpeng()
        results["目标"].append({"名称": "鲲鹏", **kunpeng_result})

        # 2. 本地备份（如果配置了外部磁盘或网络位置）
        local_backup_path = os.environ.get("LH_BACKUP_PATH")
        if local_backup_path:
            bp = Path(local_backup_path)
            if bp.exists():
                try:
                    for f in MEMORY_DIR.rglob("*"):
                        if f.is_file():
                            dest = bp / f.relative_to(PROJECT_ROOT)
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(f, dest)
                    results["目标"].append({"名称": "本地备份", "状态": "🟢"})
                except Exception as e:
                    results["目标"].append({"名称": "本地备份", "状态": "🔴", "错误": str(e)})

        all_ok = all(t.get("状态") in ["🟢", None] for t in results["目标"])
        results["总体状态"] = "🟢" if all_ok else "🟡"
        return results


# ═══════════════════════════════════════════
# 3. 完整性验证
# ═══════════════════════════════════════════

class IntegrityVerifier:
    """定期自动验证记忆完整性"""

    DNA = "#龍芯⚡️2026-07-25-INTEGRITY-VERIFIER-v1.0"

    def __init__(self):
        self.state = _load_state()

    def verify(self) -> Dict[str, Any]:
        """验证记忆完整性"""
        now = datetime.now(timezone.utc).isoformat()
        issues = []

        # 1. MEMORY.md存在且可读
        mem_file = MEMORY_DIR / "MEMORY.md"
        if not mem_file.exists():
            issues.append({"级别": "🔴", "问题": "MEMORY.md 不存在"})
        else:
            try:
                content = mem_file.read_text(encoding="utf-8")
                if len(content) < 100:
                    issues.append({"级别": "🔴", "问题": "MEMORY.md 内容异常短"})
                # 检查关键字段
                required_fields = ["UID9622", "诸葛鑫", "GPG", "DNA", "369"]
                for field in required_fields:
                    if field not in content:
                        issues.append({"级别": "🟡", "问题": f"MEMORY.md 缺少关键字段: {field}"})
            except Exception as e:
                issues.append({"级别": "🔴", "问题": f"MEMORY.md 无法读取: {e}"})

        # 2. 结构化日志完整性
        daily_db = MEMORY_DIR / "daily_log_structured.jsonl"
        if daily_db.exists():
            try:
                entries = []
                broken_lines = 0
                with open(daily_db, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            broken_lines += 1

                if broken_lines > 0:
                    issues.append({"级别": "🟡", "问题": f"结构化日志有 {broken_lines} 行损坏"})

                # 检查DNA重复
                dnas = [e.get("DNA") for e in entries if e.get("DNA")]
                if len(dnas) != len(set(dnas)):
                    issues.append({"级别": "🟡", "问题": "存在重复DNA"})

            except Exception as e:
                issues.append({"级别": "🔴", "问题": f"结构化日志读取异常: {e}"})

        # 3. 快照校验
        last_snapshot = None
        if self.state.get("快照"):
            last_snapshot = self.state["快照"][-1]
            snap_id = last_snapshot.get("快照ID")
            snap_dir = SNAPSHOT_DIR / snap_id
            if snap_dir.exists():
                # 验证JSON哈希
                json_file = snap_dir / f"memory_{snap_id}.json"
                if json_file.exists():
                    actual_hash = _sha256_file(json_file)
                    expected_hash = last_snapshot.get("JSON哈希", "")
                    if actual_hash != expected_hash:
                        issues.append({"级别": "🔴", "问题": "快照JSON哈希不匹配-快照已损坏"})
            else:
                issues.append({"级别": "🟡", "问题": f"最后快照 {snap_id} 目录不存在"})

        # 4. 每日日志文件日期连续性检查
        daily_files = sorted(MEMORY_DIR.glob("????-??-??.md"))
        if daily_files:
            dates = [f.stem for f in daily_files]
            if len(dates) > 3:
                for i in range(1, len(dates)):
                    from datetime import date
                    try:
                        d1 = date.fromisoformat(dates[i - 1])
                        d2 = date.fromisoformat(dates[i])
                        gap = (d2 - d1).days
                        if gap > 3:
                            issues.append({"级别": "🟡", "问题": f"日期断档: {dates[i-1]} → {dates[i]} (相隔{gap}天)"})
                    except ValueError:
                        pass

        report = {
            "验证时间": now,
            "记忆条目数": len(issues),
            "问题列表": issues,
            "总体判定": "🟢" if len(issues) == 0 else ("🔴" if any(i["级别"] == "🔴" for i in issues) else "🟡"),
            "MEMORY.md存在": MEMORY_DIR.joinpath("MEMORY.md").exists(),
            "结构化日志存在": daily_db.exists(),
            "快照数量": len(self.state.get("快照", [])),
            "最后快照": last_snapshot.get("快照ID") if last_snapshot else "无",
        }

        self.state["验证记录"].append({
            "时间": now,
            "判定": report["总体判定"],
            "问题数": len(issues),
        })
        _save_state(self.state)

        return report


# ═══════════════════════════════════════════
# 4. 跨模型适配
# ═══════════════════════════════════════════

class CrossModelAdapter:
    """记忆格式与模型无关——任何模型都能直接读取"""

    DNA = "#龍芯⚡️2026-07-25-CROSS-MODEL-ADAPTER-v1.0"

    @staticmethod
    def export_for_model(format: str = "system_prompt") -> str:
        """
        导出适合AI模型直接读取的记忆格式
        format: system_prompt | context | json
        """
        mem_file = MEMORY_DIR / "MEMORY.md"
        if not mem_file.exists():
            return "# 无记忆数据"

        content = mem_file.read_text(encoding="utf-8")

        if format == "system_prompt":
            # 转为系统提示词格式
            return f"""<longhun_memory>
以下为龍魂系统的跨会话持久化记忆。所有AI必须在启动时加载并遵循。
{content}
</longhun_memory>"""

        elif format == "context":
            # 转为对话上下文格式
            return f"[龍魂记忆上下文]\n{content[:3000]}..."

        elif format == "json":
            # 转为结构化JSON
            sections = {}
            current_section = "header"
            current_content = []
            for line in content.split("\n"):
                if line.startswith("## "):
                    if current_content:
                        sections[current_section] = "\n".join(current_content)
                    current_section = line[3:].strip()
                    current_content = []
                else:
                    current_content.append(line)
            if current_content:
                sections[current_section] = "\n".join(current_content)
            return json.dumps(sections, ensure_ascii=False, indent=2)

        return content


# ═══════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("用法: python3 engines/lh_memory_eternity.py <命令>")
        print("命令: snapshot|sync|verify|recover|status|health|export")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "snapshot":
        trigger = sys.argv[2] if len(sys.argv) > 2 else "manual"
        snapshotter = MemorySnapshotter()
        result = snapshotter.create_snapshot(trigger)
        print("=" * 50)
        print(f"  📸 记忆快照已生成")
        print(f"  快照ID: {result['快照ID']}")
        print(f"  时间: {result['干支时间']}")
        print(f"  条目数: {result['记忆条目数']}")
        print(f"  JSON: {result['JSON哈希'][:16]}... ({result['JSON大小']/1024:.1f}KB)")
        print(f"  MD:   {result['Markdown哈希'][:16]}... ({result['MD大小']/1024:.1f}KB)")
        print(f"  RAW:  {result['原始备份哈希'][:16]}... ({result['原始备份大小']/1024:.1f}KB)")
        print(f"  DNA:  {result['DNA']}")
        print("=" * 50)

    elif cmd == "sync":
        syncer = CrossPlatformSyncer()
        result = syncer.sync_all()
        print("=" * 50)
        print(f"  🔄 跨平台同步 {result['总体状态']}")
        for target in result.get("目标", []):
            name = target.get("名称", "")
            status = target.get("状态", "?")
            files = target.get("同步文件数", target.get("错误", ""))
            print(f"  {status} {name}: {files}")
        print("=" * 50)

    elif cmd == "verify":
        verifier = IntegrityVerifier()
        report = verifier.verify()
        print("=" * 50)
        print(f"  ✅ 记忆完整性验证 {report['总体判定']}")
        print(f"  MEMORY.md: {'存在' if report['MEMORY.md存在'] else '🔴缺失'}")
        print(f"  结构化日志: {'存在' if report['结构化日志存在'] else '🔴缺失'}")
        print(f"  快照数: {report['快照数量']}")
        for issue in report.get("问题列表", []):
            print(f"  {issue['级别']} {issue['问题']}")
        print("=" * 50)

    elif cmd == "recover":
        if len(sys.argv) < 4 or sys.argv[2] != "--from":
            print("用法: python3 engines/lh_memory_eternity.py recover --from <快照ID>")
            sys.exit(1)
        snapshotter = MemorySnapshotter()
        result = snapshotter.recover_from(sys.argv[3])
        print(f"{result['状态']} {result.get('说明', result.get('错误', ''))}")

    elif cmd == "status":
        state = _load_state()
        print("=" * 50)
        print("  📊 记忆永存引擎状态")
        print("=" * 50)
        print(f"  快照数: {len(state.get('快照', []))}")
        print(f"  同步记录: {len(state.get('同步记录', []))}")
        print(f"  验证记录: {len(state.get('验证记录', []))}")

        mem_file = MEMORY_DIR / "MEMORY.md"
        if mem_file.exists():
            size = mem_file.stat().st_size
            print(f"  MEMORY.md: {size / 1024:.1f}KB")

        daily_db = MEMORY_DIR / "daily_log_structured.jsonl"
        if daily_db.exists():
            entries = sum(1 for _ in open(daily_db, "r"))
            print(f"  结构化日志: {entries}条")

        snapshots = sorted(SNAPSHOT_DIR.glob("snapshot_*"))
        if snapshots:
            print(f"  快照目录: {len(snapshots)}个")
            print(f"  最新: {snapshots[-1].name}")
        print("=" * 50)

    elif cmd == "health":
        verifier = IntegrityVerifier()
        report = verifier.verify()
        syncer = CrossPlatformSyncer()
        state = _load_state()

        last_sync = state.get("同步记录", [])
        last_sync_time = last_sync[-1]["时间"] if last_sync else "从未同步"
        last_sync_status = last_sync[-1]["状态"] if last_sync else "?"

        print("=" * 50)
        print("  🏥 记忆永存系统健康检查")
        print("=" * 50)
        print(f"  完整性: {report['总体判定']}")
        print(f"  最后同步: {last_sync_time[:19]} ({last_sync_status})")
        print(f"  快照: {len(state.get('快照', []))}个")
        print(f"  问题: {len(report.get('问题列表', []))}个")
        print("=" * 50)

    elif cmd == "export":
        fmt = sys.argv[2] if len(sys.argv) > 2 else "system_prompt"
        adapter = CrossModelAdapter()
        output = adapter.export_for_model(fmt)
        print(output)

    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
