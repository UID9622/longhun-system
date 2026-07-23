#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂嘿咕仓 · iPhone录音自动同步管道 v1.0
LongHun HumHa-Ku · iPhone Voice Memo Auto-Sync Pipeline

功能：
  1. 监听指定目录（iPhone同步目录/手动传入）的新增 .m4a/.wav/.mp3 文件
  2. 自动将录音文件归档到 voice-twin/raw/ 目录
  3. 自动调用 Whisper 转写，生成 .txt 文件
  4. 更新 VOICE-MEMOS-INDEX-v1.0.md 索引
  5. 生成 DNA 追溯码，绑定声纹锚定

DNA: #龍芯⚡️丙午·乙未·甲寅·亥时-HUMHA-KU-SYNC-37357AB4
创始人: UID9622 · 龍芯北辰 · 诸葛鑫
"""

import os
import sys
import json
import hashlib
import shutil
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


# ══════════════════════════════════════════════════════
# 配置常量
# ══════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "voice-twin" / "raw"
INDEX_PATH = ROOT / "voice-twin" / "VOICE-MEMOS-INDEX-v1.0.md"
MANIFEST_PATH = ROOT / "voice-twin" / "humha_sync_manifest.json"

# iPhone 语音备忘录常见同步路径
IPHONE_SYNC_PATHS = [
    Path.home() / "Music" / "iTunes" / "iTunes Media" / "Voice Memos",
    Path.home() / "Downloads",
    Path.home() / "Desktop",
]

SUPPORTED_FORMATS = {".m4a", ".wav", ".mp3", ".aac", ".ogg", ".flac"}


# ══════════════════════════════════════════════════════
# 数据结构
# ══════════════════════════════════════════════════════

class SyncStatus(Enum):
    NEW = "new"
    COPIED = "copied"
    TRANSCRIBED = "transcribed"
    INDEXED = "indexed"
    ERROR = "error"


@dataclass
class VoiceMemoRecord:
    """语音备忘录记录"""
    filename: str
    original_path: str
    archived_path: str
    file_size: int
    duration_seconds: float = 0.0
    transcribed_text: str = ""
    transcribed_path: str = ""
    word_count: int = 0
    sync_status: SyncStatus = SyncStatus.NEW
    dna: str = ""
    synced_at: str = ""
    error_message: str = ""
    tags: List[str] = field(default_factory=list)


# ══════════════════════════════════════════════════════
# 核心同步器
# ══════════════════════════════════════════════════════

class HumHaKuSync:
    """嘿咕仓同步器 · iPhone录音→本地归档→Whisper转写→索引更新"""

    def __init__(self, source_dir: Optional[str] = None, auto_transcribe: bool = True):
        self.source_dir = Path(source_dir) if source_dir else None
        self.auto_transcribe = auto_transcribe
        self.raw_dir = RAW_DIR
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.records: List[VoiceMemoRecord] = []
        self.manifest = self._load_manifest()

    # ── 清单管理 ──

    def _load_manifest(self) -> dict[str, Any]:
        """加载同步清单"""
        if MANIFEST_PATH.exists():
            try:
                return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"records": [], "last_sync": None, "dna": ""}

    def _save_manifest(self):
        """保存同步清单"""
        self.manifest["last_sync"] = datetime.now().isoformat()
        self.manifest["records"] = [
            {
                "filename": r.filename,
                "original_path": r.original_path,
                "archived_path": r.archived_path,
                "file_size": r.file_size,
                "duration_seconds": r.duration_seconds,
                "word_count": r.word_count,
                "sync_status": r.sync_status.value,
                "dna": r.dna,
                "synced_at": r.synced_at,
                "tags": r.tags,
            }
            for r in self.records
        ]
        MANIFEST_PATH.write_text(
            json.dumps(self.manifest, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    # ── DNA 追溯码 ──

    def _gen_dna(self, filename: str) -> str:
        """生成 DNA 追溯码"""
        file_hash = hashlib.md5(filename.encode()).hexdigest()[:8].upper()
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"#龍芯⚡️{ts}-HUMHA-KU-{file_hash}"

    # ── 文件扫描 ──

    def scan_source(self, path: Optional[str] = None) -> List[Path]:
        """
        扫描源目录中新增的音频文件。
        搜索模式：递归查找所有 .m4a/.wav/.mp3 文件。
        """
        search_path = Path(path) if path else self.source_dir
        if not search_path or not search_path.exists():
            # 自动探测 iPhone 同步目录
            for p in IPHONE_SYNC_PATHS:
                if p.exists():
                    search_path = p
                    print(f"🔍 自动探测到音频源目录: {search_path}")
                    break
            else:
                print("⚠️ 未找到音频源目录，请手动指定路径")
                return []

        audio_files = []
        for ext in SUPPORTED_FORMATS:
            audio_files.extend(search_path.rglob(f"*{ext}"))

        print(f"📁 扫描到 {len(audio_files)} 个音频文件")
        return sorted(audio_files, key=lambda f: f.stat().st_mtime, reverse=True)

    # ── 文件归档 ──

    def archive_recording(self, source_path: Path) -> Optional[VoiceMemoRecord]:
        """
        将录音文件复制到 voice-twin/raw/ 归档。
        如果已存在同名文件，跳过。
        """
        filename = source_path.name

        # 检查是否已归档
        existing = [r for r in self.records if r.filename == filename]
        if existing and existing[0].sync_status != SyncStatus.ERROR:
            print(f"  ⏭️ 跳过（已归档）: {filename}")
            return None

        # 复制文件
        dest_path = self.raw_dir / filename
        try:
            shutil.copy2(source_path, dest_path)
            file_size = dest_path.stat().st_size
        except Exception as e:
            print(f"  ❌ 复制失败: {filename} — {e}")
            return None

        # 获取音频时长
        duration = self._get_audio_duration(dest_path)

        record = VoiceMemoRecord(
            filename=filename,
            original_path=str(source_path),
            archived_path=str(dest_path),
            file_size=file_size,
            duration_seconds=duration,
            sync_status=SyncStatus.COPIED,
            dna=self._gen_dna(filename),
            synced_at=datetime.now().isoformat(),
        )
        self.records.append(record)
        print(f"  ✅ 归档完成: {filename} ({file_size / 1024:.0f}KB, {duration:.0f}s)")

        return record

    # ── 音频时长获取 ──

    def _get_audio_duration(self, path: Path) -> float:
        """获取音频时长（秒）"""
        try:
            import soundfile as sf
            info = sf.info(str(path))
            return info.duration
        except Exception:
            pass

        # ffprobe 降级
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                capture_output=True, text=True, timeout=10,
            )
            return float(result.stdout.strip())
        except Exception:
            return 0.0

    # ── Whisper 转写 ──

    def transcribe_recording(self, record: VoiceMemoRecord) -> Optional[VoiceMemoRecord]:
        """
        使用 Whisper 转写录音，生成 .txt 文件。
        """
        audio_path = Path(record.archived_path)
        if not audio_path.exists():
            record.error_message = "音频文件不存在"
            record.sync_status = SyncStatus.ERROR
            return None

        txt_path = audio_path.with_suffix(audio_path.suffix + ".txt")
        if txt_path.exists():
            existing_text = txt_path.read_text(encoding="utf-8")
            if len(existing_text.strip()) > 10:
                record.transcribed_text = existing_text
                record.transcribed_path = str(txt_path)
                record.word_count = len(existing_text)
                record.sync_status = SyncStatus.TRANSCRIBED
                print(f"  📝 转写已存在: {txt_path.name} ({record.word_count}字)")
                return record

        if not self.auto_transcribe:
            record.sync_status = SyncStatus.COPIED
            return record

        print(f"  🎙️ 开始转写: {audio_path.name} ...")
        try:
            # 优先使用龍魂语音识别器
            sys.path.insert(0, str(ROOT / "cnsh" / "terminal" / "modules" / "multimodal"))
            from 龍魂语音识别器 import 龍魂语音识别器

            recognizer = 龍魂语音识别器(模型名称="base", 设备="cpu", 启用审计=False)
            result = recognizer.语音转文字(str(audio_path), 语言="zh")

            text = result.文本
            if text:
                txt_path.write_text(text, encoding="utf-8")
                record.transcribed_text = text
                record.transcribed_path = str(txt_path)
                record.word_count = len(text)
                record.sync_status = SyncStatus.TRANSCRIBED
                print(f"  ✅ 转写完成: {record.word_count}字, 置信度={result.置信度:.2f}")
                return record
        except ImportError:
            print("  ⚠️ Whisper 未安装，跳过转写")
            record.sync_status = SyncStatus.COPIED
            return record
        except Exception as e:
            print(f"  ⚠️ 转写失败: {e}")
            record.error_message = str(e)
            record.sync_status = SyncStatus.ERROR
            return None

    # ── 索引更新 ──

    def update_index(self):
        """
        更新 VOICE-MEMOS-INDEX-v1.0.md 索引文件。
        追加新增录音的转写内容。
        """
        transcribed = [r for r in self.records if r.sync_status == SyncStatus.TRANSCRIBED]
        if not transcribed:
            print("📋 无新增转写内容，索引无需更新")
            return

        # 读取现有索引
        existing_content = ""
        if INDEX_PATH.exists():
            existing_content = INDEX_PATH.read_text(encoding="utf-8")

        # 获取当前录音总数
        existing_m4a = list(self.raw_dir.glob("*.m4a"))
        new_entries = []

        for i, record in enumerate(transcribed, start=1):
            entry = f"""
### 录音 {i + len(existing_m4a) - len(transcribed)}: {record.filename}

- **时长**: {record.duration_seconds:.0f}分{record.duration_seconds % 60:.0f}秒
- **原文件**: `voice-twin/raw/{record.filename}`
- **转写文件**: `voice-twin/raw/{record.filename}.txt`
- **DNA**: `{record.dna}`

**转写内容**:

```
{record.transcribed_text[:2000]}{'...' if len(record.transcribed_text) > 2000 else ''}
```

---
"""
            new_entries.append(entry)
            record.sync_status = SyncStatus.INDEXED

        # 追加到索引文件
        if new_entries:
            appendix = "\n".join(new_entries)
            if "## 录音清单" in existing_content:
                # 插入到主题标签之后
                idx = existing_content.find("## 主题标签")
                if idx > 0:
                    # 找下一个 ---
                    insert_idx = existing_content.find("---", idx)
                    if insert_idx > 0:
                        insert_idx = existing_content.find("\n", insert_idx) + 1
                        updated = existing_content[:insert_idx] + "\n" + appendix + existing_content[insert_idx:]
                    else:
                        updated = existing_content + "\n" + appendix
                else:
                    updated = existing_content + "\n" + appendix
            else:
                updated = existing_content + "\n" + appendix

            # 更新录音总数
            updated = updated.replace(
                "总录音数: ",
                f"总录音数: {len(existing_m4a)} ",
            )
            INDEX_PATH.write_text(updated, encoding="utf-8")
            print(f"📋 索引已更新: 新增 {len(new_entries)} 条录音")

    # ── 主流程 ──

    def run(self, source_path: Optional[str] = None) -> Dict[str, Any]:
        """
        主同步流程：
        1. 扫描源目录
        2. 归档新增文件
        3. Whisper 转写
        4. 更新索引
        5. 保存清单
        """
        print("=" * 60)
        print("  🐉 嘿咕仓 · 录音同步管道 v1.0")
        print("  HumHa-Ku · Voice Memo Sync Pipeline")
        print("=" * 60)

        if source_path:
            self.source_dir = Path(source_path)

        # Step 1: 扫描
        files = self.scan_source()
        if not files:
            print("\n📭 未发现新增音频文件")
            return {"status": "no_new_files", "count": 0}

        # Step 2: 归档
        print(f"\n📦 Step 1/3: 归档新增文件 ({len(files)} 个)")
        archived = []
        for f in files:
            record = self.archive_recording(f)
            if record:
                archived.append(record)
        print(f"  归档完成: {len(archived)} 个新文件")

        # Step 3: 转写
        if self.auto_transcribe and archived:
            print(f"\n🎙️ Step 2/3: Whisper 转写 ({len(archived)} 个)")
            for record in archived:
                self.transcribe_recording(record)

        # Step 4: 更新索引
        print(f"\n📋 Step 3/3: 更新索引")
        self.update_index()

        # Step 5: 保存清单
        self._save_manifest()

        # 统计
        stats = {
            "status": "complete",
            "total_scanned": len(files),
            "new_archived": len(archived),
            "transcribed": len([r for r in self.records if r.sync_status in (SyncStatus.TRANSCRIBED, SyncStatus.INDEXED)]),
            "errors": len([r for r in self.records if r.sync_status == SyncStatus.ERROR]),
            "dna": self._gen_dna("batch_sync"),
        }

        print("\n" + "=" * 60)
        print(f"  ✅ 同步完成")
        print(f"  扫描: {stats['total_scanned']} | 归档: {stats['new_archived']} | 转写: {stats['transcribed']} | 错误: {stats['errors']}")
        print(f"  DNA: {stats['dna']}")
        print("=" * 60)

        return stats


# ══════════════════════════════════════════════════════
# 监听模式（持续运行）
# ══════════════════════════════════════════════════════

def watch_mode(source_dir: str, interval: int = 60):
    """
    监听模式：每 N 秒检查一次新文件。
    适合作为后台守护进程运行。
    """
    print(f"👁️ 嘿咕仓监听模式启动 | 目录={source_dir} | 间隔={interval}s")
    print("  按 Ctrl+C 停止\n")

    syncer = HumHaKuSync(source_dir, auto_transcribe=True)
    syncer.run()

    try:
        while True:
            time.sleep(interval)
            files = syncer.scan_source()
            new_files = [f for f in files if f.stat().st_mtime > time.time() - interval * 2]
            if new_files:
                print(f"\n🆕 发现 {len(new_files)} 个新录音文件")
                syncer.run()
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 等待新录音...")
    except KeyboardInterrupt:
        print("\n👋 嘿咕仓监听已停止")


# ══════════════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="龍魂嘿咕仓 · iPhone录音同步管道",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_humha_ku_sync.py                          # 自动扫描同步
  python3 bin/lh_humha_ku_sync.py --source ~/Downloads     # 指定源目录
  python3 bin/lh_humha_ku_sync.py --watch ~/Downloads      # 监听模式
  python3 bin/lh_humha_ku_sync.py --no-transcribe          # 只归档不转写
        """,
    )

    parser.add_argument("--source", "-s", type=str, help="音频源目录路径")
    parser.add_argument("--watch", "-w", type=str, help="监听目录（持续运行）")
    parser.add_argument("--no-transcribe", action="store_true", help="跳过Whisper转写")
    parser.add_argument("--interval", "-i", type=int, default=60, help="监听间隔（秒，默认60）")

    args = parser.parse_args()

    if args.watch:
        watch_mode(args.watch, args.interval)
    else:
        syncer = HumHaKuSync(
            source_dir=args.source,
            auto_transcribe=not args.no_transcribe,
        )
        result = syncer.run(args.source)
        sys.exit(0 if result["status"] == "complete" or result["status"] == "no_new_files" else 1)
