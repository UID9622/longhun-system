#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 数字人主权印记引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-DIGITAL-IMPRINT-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  1. 生成数字人唯一 DNA（面孔哈希 + 声纹指纹 + IPA）
  2. 在视频帧/音频中嵌入不可见水印
  3. 验证数字人身份
  4. 同步到 Notion

用法：
  python3 bin/lh_digital_imprint.py create --name "张三" --ipa "ZHS-001"
  python3 bin/lh_digital_imprint.py verify --dna "DNA-xxx"
  python3 bin/lh_digital_imprint.py watermark --video input.mp4 --output output.mp4 --dna "DNA-xxx"
  python3 bin/lh_digital_imprint.py sync --ipa "ZHS-001"
  python3 bin/lh_digital_imprint.py list
  python3 bin/lh_digital_imprint.py status
"""

import os
import json
import hashlib
import base64
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field

# 项目根路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIGITAL_DIR = PROJECT_ROOT / "digital_humans"
DIGITAL_DIR.mkdir(parents=True, exist_ok=True)

# 确认码（焊死）
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DNA_PREFIX = "#龍芯⚡️"


@dataclass
class DigitalImprint:
    """数字人主权印记数据模型"""
    dna: str
    name: str
    ipa: str
    face_hash: str = ""
    voiceprint: str = ""
    model_path: str = ""
    created_at: str = ""
    updated_at: str = ""
    version: int = 1
    status: str = "active"  # active / archived / training
    metadata: dict = field(default_factory=dict)


class ImprintEngine:
    """数字人主权印记引擎"""

    def __init__(self):
        self.registry_file = DIGITAL_DIR / "registry.json"
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """加载注册表"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ 注册表损坏，重建中...")
        return {"digital_humans": {}, "meta": {"version": 1, "last_updated": ""}}

    def _save_registry(self):
        """保存注册表"""
        self.registry["meta"]["last_updated"] = datetime.now().isoformat()
        self.registry["meta"]["version"] += 1
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, ensure_ascii=False, indent=2)

    # ────────────────────────────────────────────
    # DNA 生成
    # ────────────────────────────────────────────

    def generate_dna(self, name: str, ipa: str) -> str:
        """生成数字人唯一 DNA（基于姓名+IPA+时间戳+随机数）"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        raw = f"{name}|{ipa}|{timestamp}|{os.urandom(8).hex()}"
        dna_hash = hashlib.sha256(raw.encode()).hexdigest()[:16].upper()
        return f"{DNA_PREFIX}DIG-{dna_hash}"

    def generate_face_hash(self, image_path: Optional[Path] = None, name: str = "") -> str:
        """生成面孔哈希"""
        if image_path and image_path.exists():
            with open(image_path, 'rb') as f:
                return f"FACE-{hashlib.sha256(f.read()).hexdigest()[:16]}"
        # 无图片时基于名字生成占位哈希
        return f"FACE-{hashlib.sha256(f'NOPHOTO:{name}'.encode()).hexdigest()[:12]}"

    def generate_voiceprint(self, audio_path: Optional[Path] = None, name: str = "") -> str:
        """生成声纹指纹"""
        if audio_path and audio_path.exists():
            with open(audio_path, 'rb') as f:
                return f"VOICE-{hashlib.sha256(f.read()).hexdigest()[:16]}"
        return f"VOICE-{hashlib.sha256(f'NOVOICE:{name}'.encode()).hexdigest()[:12]}"

    # ────────────────────────────────────────────
    # 印记管理
    # ────────────────────────────────────────────

    def create_imprint(
        self,
        name: str,
        ipa: str,
        face_path: Optional[Path] = None,
        voice_path: Optional[Path] = None,
        metadata: Optional[dict] = None,
    ) -> DigitalImprint:
        """创建数字人印记"""
        if ipa in self.registry["digital_humans"]:
            print(f"⚠️ IPA '{ipa}' 已存在，将更新现有印记")

        dna = self.generate_dna(name, ipa)
        face_hash = self.generate_face_hash(face_path, name)
        voiceprint = self.generate_voiceprint(voice_path, name)
        model_dir = DIGITAL_DIR / f"{ipa}_{name}"
        model_dir.mkdir(parents=True, exist_ok=True)

        now = datetime.now().isoformat()
        existing_data = self.registry["digital_humans"].get(ipa, {})
        version = existing_data.get("version", 0) + 1
        # 保留旧DNA（如果存在）
        old_dna = existing_data.get("dna", dna)
        if not old_dna.startswith(DNA_PREFIX):
            old_dna = dna

        imprint = DigitalImprint(
            dna=old_dna,
            name=name,
            ipa=ipa,
            face_hash=face_hash,
            voiceprint=voiceprint,
            model_path=str(model_dir),
            created_at=existing_data.get("created_at", now),
            updated_at=now,
            version=version,
            status="active",
            metadata=metadata or {},
        )

        self.registry["digital_humans"][ipa] = asdict(imprint)
        self._save_registry()

        # 同时保存独立印记文件
        imprint_file = model_dir / "imprint.json"
        with open(imprint_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(imprint), f, ensure_ascii=False, indent=2)

        return imprint

    def verify_imprint(self, dna: str) -> Optional[Dict]:
        """通过 DNA 验证数字人身份"""
        for ipa, data in self.registry["digital_humans"].items():
            if data.get("dna") == dna:
                return data
        return None

    def find_by_name(self, name: str) -> List[Dict]:
        """按名字查找数字人"""
        results = []
        for ipa, data in self.registry["digital_humans"].items():
            if name.lower() in data.get("name", "").lower():
                results.append(data)
        return results

    def find_by_ipa(self, ipa: str) -> Optional[Dict]:
        """按 IPA 查找数字人"""
        return self.registry["digital_humans"].get(ipa)

    def list_all(self) -> List[Dict]:
        """列出所有数字人"""
        return list(self.registry["digital_humans"].values())

    def archive_imprint(self, ipa: str) -> bool:
        """归档数字人（不删除）"""
        if ipa not in self.registry["digital_humans"]:
            return False
        self.registry["digital_humans"][ipa]["status"] = "archived"
        self._save_registry()
        return True

    # ────────────────────────────────────────────
    # 水印嵌入
    # ────────────────────────────────────────────

    def embed_video_watermark(
        self, video_path: Path, output_path: Path, dna: str
    ) -> Dict:
        """在视频中嵌入不可见DNA水印（使用FFmpeg）"""
        if not video_path.exists():
            return {"status": "error", "message": f"视频文件不存在: {video_path}"}

        # 多行水印：DNA + 时间戳 + 确认码
        timestamp = datetime.now().isoformat()
        watermark_text = f"\\nDNA: {dna}\\nTime: {timestamp}\\n{CONFIRM_CODE}"

        # FFmpeg 透明水印
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-vf",
            f"drawtext=text='{watermark_text}':"
            f"fontsize=18:fontcolor=white@0.08:"
            f"x=(w-text_w)/2:y=h-text_h-30:"
            f"box=1:boxcolor=black@0.05:boxborderw=8",
            "-c:a", "copy",
            str(output_path),
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                return {
                    "status": "success",
                    "output": str(output_path),
                    "dna": dna,
                    "timestamp": timestamp,
                }
            return {
                "status": "failed",
                "message": result.stderr[-200:] if result.stderr else "未知错误",
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "FFmpeg 处理超时（>5分钟）"}
        except FileNotFoundError:
            return {"status": "error", "message": "FFmpeg 未安装。请执行: brew install ffmpeg"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def embed_audio_watermark(
        self, audio_path: Path, output_path: Path, dna: str
    ) -> Dict:
        """在音频中嵌入DNA水印"""
        if not audio_path.exists():
            return {"status": "error", "message": f"音频文件不存在: {audio_path}"}

        # 音频水印：metadata 注入
        timestamp = datetime.now().isoformat()
        cmd = [
            "ffmpeg", "-y",
            "-i", str(audio_path),
            "-metadata", f"DNA={dna}",
            "-metadata", f"ImprintTime={timestamp}",
            "-metadata", f"Creator=UID9622",
            "-metadata", f"Protocol=CC BY-NC-SA 4.0",
            "-c:a", "copy",
            str(output_path),
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                return {
                    "status": "success",
                    "output": str(output_path),
                    "dna": dna,
                    "timestamp": timestamp,
                }
            return {"status": "failed", "message": result.stderr[-200:]}
        except FileNotFoundError:
            return {"status": "error", "message": "FFmpeg 未安装"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ────────────────────────────────────────────
    # Notion 同步
    # ────────────────────────────────────────────

    def sync_to_notion(self, ipa: str) -> Dict:
        """将印记同步到 Notion（通过现有对话桥）"""
        imprint = self.find_by_ipa(ipa)
        if not imprint:
            return {"status": "error", "message": f"IPA '{ipa}' 未找到"}

        # 尝试通过 Notion API 同步
        notion_token = os.environ.get("NOTION_TOKEN_BACKUP") or os.environ.get("NOTION_TOKEN")
        if not notion_token:
            return {
                "status": "warning",
                "message": "NOTION_TOKEN 未设置，印记仅保存在本地",
                "imprint": imprint,
            }

        try:
            import urllib.request
            headers = {
                "Authorization": f"Bearer {notion_token}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",
            }

            # 搜索数字人数据库
            search_payload = json.dumps({
                "query": f"数字人 {imprint['name']}",
                "page_size": 5,
            }).encode()
            req = urllib.request.Request(
                "https://api.notion.com/v1/search",
                data=search_payload,
                headers=headers,
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                results = json.loads(resp.read().decode()).get("results", [])

            return {
                "status": "synced" if results else "not_found_in_notion",
                "ipa": ipa,
                "dna": imprint["dna"],
                "notion_pages_found": len(results),
                "message": "已搜索 Notion 数据库" if results else "未在 Notion 中找到对应数据库",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Notion同步失败: {e}",
                "imprint": imprint,
            }

    # ────────────────────────────────────────────
    # 状态与报告
    # ────────────────────────────────────────────

    def get_status(self) -> Dict:
        """获取引擎整体状态"""
        humans = self.registry["digital_humans"]
        active = sum(1 for d in humans.values() if d.get("status") == "active")
        archived = sum(1 for d in humans.values() if d.get("status") == "archived")
        return {
            "total": len(humans),
            "active": active,
            "archived": archived,
            "registry_version": self.registry["meta"]["version"],
            "last_updated": self.registry["meta"]["last_updated"],
            "digital_humans": humans,
        }


# ============================================================
# CLI
# ============================================================

def print_banner():
    print(f"""
{'='*56}
  🐉 龍魂 · 数字人主权印记引擎 v1.0
  {DNA_PREFIX}丙午·丙申·乙巳·辛巳·☴巽-DIGITAL-IMPRINT-v1.0-UID9622
  {CONFIRM_CODE}
{'='*56}
""")


def cmd_create(args):
    """创建数字人印记"""
    engine = ImprintEngine()
    face_path = Path(args.face) if args.face else None
    voice_path = Path(args.voice) if args.voice else None

    meta = {}
    if args.meta:
        try:
            meta = json.loads(args.meta)
        except json.JSONDecodeError:
            print("❌ --meta 参数需为合法 JSON")
            return

    print_banner()
    print(f"  创建数字人: {args.name}")
    print(f"  IPA: {args.ipa}")

    imprint = engine.create_imprint(
        name=args.name,
        ipa=args.ipa,
        face_path=face_path,
        voice_path=voice_path,
        metadata=meta,
    )

    print(f"""
  ✅ 数字人印记已创建
  {'─'*40}
  DNA:       {imprint.dna}
  IPA:       {imprint.ipa}
  姓名:      {imprint.name}
  面孔哈希:  {imprint.face_hash}
  声纹指纹:  {imprint.voiceprint}
  模型路径:  {imprint.model_path}
  版本:      v{imprint.version}
  时间:      {imprint.created_at}
  {'─'*40}
""")


def cmd_verify(args):
    """验证数字人DNA"""
    engine = ImprintEngine()
    print_banner()

    result = engine.verify_imprint(args.dna)
    if result:
        print(f"  ✅ 验证通过 — {result['name']} (IPA: {result['ipa']})")
        print(f"  DNA:      {result['dna']}")
        print(f"  面孔哈希:  {result.get('face_hash', 'N/A')}")
        print(f"  声纹指纹:  {result.get('voiceprint', 'N/A')}")
        print(f"  状态:      {result.get('status', 'unknown')}")
        print(f"  版本:      v{result.get('version', 1)}")
    else:
        print(f"  ❌ DNA 未找到: {args.dna}")
        all_humans = engine.list_all()
        if all_humans:
            print(f"\n  已注册的数字人:")
            for h in all_humans:
                print(f"    · {h['name']} — IPA: {h['ipa']} — DNA: {h['dna'][:30]}...")


def cmd_watermark(args):
    """嵌入水印"""
    engine = ImprintEngine()
    print_banner()

    dna = args.dna
    if not dna:
        # 尝试从 IPA 查找 DNA
        if args.ipa:
            imprint = engine.find_by_ipa(args.ipa)
            if imprint:
                dna = imprint["dna"]
                print(f"  📌 从 IPA '{args.ipa}' 查找到 DNA: {dna[:30]}...")
            else:
                print(f"  ❌ IPA '{args.ipa}' 未注册")
                return
        else:
            dna = input("  请输入 DNA (或 IPA): ").strip()
            # 尝试按 IPA 查找
            imprint = engine.find_by_ipa(dna)
            if imprint:
                dna = imprint["dna"]
                print(f"  📌 识别为 IPA，DNA: {dna[:30]}...")

    if not dna:
        print("  ❌ DNA 不能为空")
        return

    video_path = Path(args.video) if args.video else None
    audio_path = Path(args.audio) if args.audio else None
    output_path = Path(args.output) if args.output else None

    if video_path:
        if not output_path:
            output_path = video_path.parent / f"{video_path.stem}_watermarked{video_path.suffix}"
        print(f"  🎬 嵌入视频水印: {video_path.name}")
        result = engine.embed_video_watermark(video_path, output_path, dna)
        if result["status"] == "success":
            print(f"  ✅ 水印已嵌入 → {result['output']}")
        else:
            print(f"  ❌ 失败: {result.get('message', '未知错误')}")

    elif audio_path:
        if not output_path:
            output_path = audio_path.parent / f"{audio_path.stem}_watermarked{audio_path.suffix}"
        print(f"  🎵 嵌入音频水印: {audio_path.name}")
        result = engine.embed_audio_watermark(audio_path, output_path, dna)
        if result["status"] == "success":
            print(f"  ✅ 水印已嵌入 → {result['output']}")
        else:
            print(f"  ❌ 失败: {result.get('message', '未知错误')}")

    else:
        print("  ❌ 请指定 --video 或 --audio")
        return


def cmd_sync(args):
    """同步到 Notion"""
    engine = ImprintEngine()
    print_banner()

    if args.ipa:
        print(f"  同步 IPA: {args.ipa} → Notion...")
        result = engine.sync_to_notion(args.ipa)
        status_icon = {"synced": "✅", "not_found_in_notion": "⚠️", "warning": "⚠️"}.get(
            result["status"], "❌"
        )
        print(f"  {status_icon} {result['message']}")
    elif args.all:
        all_humans = engine.list_all()
        print(f"  全量同步 {len(all_humans)} 个数字人 → Notion...")
        for h in all_humans:
            if h.get("status") == "active":
                result = engine.sync_to_notion(h["ipa"])
                status_icon = "✅" if result["status"] == "synced" else "⚠️"
                print(f"  {status_icon} {h['name']} ({h['ipa']}) — {result['message']}")
    else:
        print("  ❌ 请指定 --ipa 或 --all")


def cmd_list(args):
    """列出所有数字人"""
    engine = ImprintEngine()
    print_banner()
    humans = engine.list_all()

    if not humans:
        print("  📭 暂无注册数字人")
        print("  使用 create 命令创建: python3 bin/lh_digital_imprint.py create --name 姓名 --ipa IPA-001")
        return

    for h in sorted(humans, key=lambda x: x.get("created_at", ""), reverse=True):
        status_icon = {"active": "🟢", "archived": "📦", "training": "🟡"}.get(
            h.get("status"), "⚪"
        )
        print(f"""
  {status_icon} {h['name']}
     IPA:       {h['ipa']}
     DNA:       {h['dna']}
     面孔哈希:  {h.get('face_hash', 'N/A')}
     声纹指纹:  {h.get('voiceprint', 'N/A')}
     版本:      v{h.get('version', 1)}
     状态:      {h.get('status', 'unknown')}
     创建:      {h.get('created_at', 'N/A')[:19]}
""")


def cmd_status(args):
    """查看引擎状态"""
    engine = ImprintEngine()
    print_banner()
    status = engine.get_status()

    print(f"""
  📊 引擎状态
  {'─'*40}
  注册数字人:  {status['total']}
  🟢 活跃:      {status['active']}
  📦 归档:      {status['archived']}
  注册表版本:  v{status['registry_version']}
  最后更新:    {status['last_updated'][:19] if status['last_updated'] else '从未'}
  {'─'*40}
""")


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 数字人主权印记引擎 v1.0"
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # create
    p_create = sub.add_parser("create", help="创建数字人印记")
    p_create.add_argument("--name", required=True, help="数字人姓名")
    p_create.add_argument("--ipa", required=True, help="智能人格锚点 (如 ZGX-001)")
    p_create.add_argument("--face", help="面孔图片路径")
    p_create.add_argument("--voice", help="语音文件路径")
    p_create.add_argument("--meta", help='元数据JSON (如 \'{"role":"host"}\')')

    # verify
    p_verify = sub.add_parser("verify", help="验证数字人DNA")
    p_verify.add_argument("--dna", required=True, help="要验证的DNA")

    # watermark
    p_wm = sub.add_parser("watermark", help="嵌入水印到视频/音频")
    p_wm.add_argument("--video", help="视频文件路径")
    p_wm.add_argument("--audio", help="音频文件路径")
    p_wm.add_argument("--output", help="输出路径（默认添加 _watermarked 后缀）")
    p_wm.add_argument("--dna", help="数字人DNA（可选，也可用 --ipa）")
    p_wm.add_argument("--ipa", help="从已注册IPA获取DNA")

    # sync
    p_sync = sub.add_parser("sync", help="同步印记到 Notion")
    p_sync.add_argument("--ipa", help="指定IPA同步")
    p_sync.add_argument("--all", action="store_true", help="全量同步所有活跃数字人")

    # list
    sub.add_parser("list", help="列出所有数字人")

    # status
    sub.add_parser("status", help="查看引擎状态")

    args = parser.parse_args()

    if args.command == "create":
        cmd_create(args)
    elif args.command == "verify":
        cmd_verify(args)
    elif args.command == "watermark":
        cmd_watermark(args)
    elif args.command == "sync":
        cmd_sync(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "status":
        cmd_status(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
