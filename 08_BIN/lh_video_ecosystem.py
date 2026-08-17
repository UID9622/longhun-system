#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 视频生态主控制器 v1.0
DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-VIDEO-ECOSYSTEM-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过

功能:
  1. 内容索引 → 素材检索
  2. 智能体创作 → 解说稿/分镜/剪辑方案
  3. 视频工具集成 → 对接外部视频生成/剪辑工具
  4. 审计发布 → 三色审计 + DNA追溯
"""

import json
import hashlib
import time
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 引入同级目录与 engines 目录
_LONGHUN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_LONGHUN_ROOT / "08_BIN"))
sys.path.insert(0, str(_LONGHUN_ROOT / "05_ENGINES"))

from lh_video_knowledge import VideoKnowledgeIndex, VideoMaterial
from lh_video_agent import VideoAgent, Script, Storyboard
from lh_video_tools import VideoTools


# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def generate_dna(suffix: str = "VIDEO-ECOSYSTEM") -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    rand = hashlib.sha256(f"{suffix}{timestamp}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{timestamp}-{suffix}-{rand}-{UID}"


# ============================================================
# 视频生态主控制器
# ============================================================

class VideoEcosystem:
    """视频生态主控制器"""

    def __init__(self):
        self.knowledge = VideoKnowledgeIndex()
        self.agent = VideoAgent()
        self.tools = VideoTools()
        self.history: List[Dict] = []

    def add_material(self, title: str, category: str, era: str,
                     description: str, keywords: List[str], source: str = "") -> VideoMaterial:
        """添加素材"""
        return self.knowledge.add_material(
            title=title, category=category, era=era,
            description=description, keywords=keywords, source=source
        )

    def create_video(self, topic: str, category: str = "文化",
                     style: str = "解说", tool_id: str = None) -> Dict:
        """创建视频：完整流程"""
        dna = generate_dna("VIDEO-CREATE")
        result = {"dna": dna, "topic": topic, "steps": {}}

        # Step 1: 检索素材（先按主题+分类，未命中则按分类兜底）
        print("📚 ① 检索素材...")
        materials = self.knowledge.search(topic, category)
        if not materials and category:
            materials = self.knowledge.search("", category)
        result["steps"]["search"] = {
            "found": len(materials),
            "materials": [{"id": m.id, "title": m.title, "era": m.era,
                           "tiancai": m.tiancai, "wuxing": m.wuxing}
                          for m in materials[:5]]
        }
        print(f"   ✅ 找到 {len(materials)} 条素材")

        # Step 2: 生成解说稿
        print("✍️  ② 编剧Agent生成解说稿...")
        script = self.agent.write_script(topic, [m.to_dict() for m in materials], style)
        result["steps"]["script"] = {
            "title": script.title,
            "style": script.style,
            "scenes": len(script.scenes),
            "duration": sum(s.get("duration", 30) for s in script.scenes),
            "dna": script.dna,
        }
        print(f"   ✅ 解说稿已生成: {len(script.scenes)} 场景")

        # Step 3: 规划分镜
        print("🎬 ③ 导演Agent规划分镜...")
        storyboard = self.agent.plan_storyboard(script)
        result["steps"]["storyboard"] = {
            "scenes": len(storyboard.scenes),
            "total_duration": storyboard.total_duration,
            "dna": storyboard.dna,
        }
        print(f"   ✅ 分镜已规划: {storyboard.total_duration}s")

        # Step 4: 剪辑方案
        print("✂️  ④ 剪辑Agent规划剪辑...")
        edit_plan = self.agent.plan_edit(storyboard)
        result["steps"]["edit_plan"] = {
            "clips": len(edit_plan.clips),
            "music": edit_plan.music,
            "dna": edit_plan.dna,
        }
        print(f"   ✅ 剪辑方案已生成: {len(edit_plan.clips)} 个镜头")

        # Step 5: 三色审计
        print("⚖️  ⑤ 审核Agent三色审计...")
        audit = self.agent.audit_script(script)
        result["steps"]["audit"] = audit
        print(f"   {audit['tricolor']} 审计得分: {audit['score']}")

        # Step 6: 推荐/调用外部工具
        print("🛠️  ⑥ 视频工具集成...")
        selected_tool = tool_id or self.tools.auto_select(style)
        tool_result = self.tools.run_tool(
            selected_tool,
            input_path=None,
            output_dir=str(Path.home() / ".longhun" / "video_output"),
            params={"topic": topic, "style": style, "scenes": len(script.scenes)}
        )
        result["steps"]["tool"] = tool_result
        print(f"   ✅ 工具调用: {tool_result['tool']} ({tool_result['status']})")

        self.history.append(result)
        return result

    def search_material(self, query: str, category: str = None) -> List[Dict]:
        """搜索素材"""
        results = self.knowledge.search(query, category)
        return [m.to_dict() for m in results]

    def get_status(self) -> Dict:
        return {
            "total_materials": len(self.knowledge.materials),
            "total_videos": len(self.history),
            "data_dir": str(self.knowledge.data_dir),
            "dna": generate_dna("ECOSYSTEM-STATUS"),
        }


# ============================================================
# 命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 视频生态主控制器")
    parser.add_argument("--add-material", action="store_true", help="添加素材")
    parser.add_argument("--title", type=str, help="素材标题")
    parser.add_argument("--category", type=str, default=None, choices=["历史", "抗战", "教育", "文化"], help="分类（默认：添加素材时为文化，搜索/创建时不限制）")
    parser.add_argument("--era", type=str, default="未知", help="年代")
    parser.add_argument("--description", type=str, default="", help="描述")
    parser.add_argument("--keywords", type=str, default="", help="关键词，逗号分隔")
    parser.add_argument("--source", type=str, default="", help="来源")

    parser.add_argument("--create", type=str, help="创建视频主题")
    parser.add_argument("--style", type=str, default="解说", choices=["解说", "短剧", "教育"], help="风格")
    parser.add_argument("--tool", type=str, help="指定外部工具")

    parser.add_argument("--search", type=str, help="搜索素材")
    parser.add_argument("--status", action="store_true", help="查看生态状态")
    parser.add_argument("--tools", action="store_true", help="列出集成工具")

    args = parser.parse_args()
    eco = VideoEcosystem()

    if args.add_material:
        if not args.title:
            print("❌ 请提供 --title")
            return
        keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else []
        material = eco.add_material(
            title=args.title,
            category=args.category or "文化",
            era=args.era,
            description=args.description,
            keywords=keywords,
            source=args.source,
        )
        print("✅ 素材已添加")
        print(json.dumps(material.to_dict(), indent=2, ensure_ascii=False))
        return

    if args.create:
        result = eco.create_video(args.create, args.category, args.style, args.tool)
        print("\n🐉 视频创建结果")
        print("=" * 50)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.search:
        results = eco.search_material(args.search, args.category)
        print(f"🔍 找到 {len(results)} 条素材")
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    if args.status:
        print(json.dumps(eco.get_status(), indent=2, ensure_ascii=False))
        return

    if args.tools:
        print(json.dumps(VideoTools.list_tools(), indent=2, ensure_ascii=False))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
