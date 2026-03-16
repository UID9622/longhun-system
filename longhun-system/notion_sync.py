# ═══════════════════════════════════════════════════════════
# 🐉 龙魂系统 · P0伦理锚点
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# DNA:    #龍芯⚡️2026-03-16-ETHICS-STAMP-v1.0
# 作者:    诸葛鑫（UID9622）
# 理论:    曾仕强老师（永恒显示）
#
# P0铁律（永恒有效）:
#   L0: 任何伤害真实人物的内容 → 立即冻结
#   P0: 人民利益优先，数据主权在用户
#   北辰: 三条红线 · 违反即停机
#   永恒: 祖国优先，普惠全球，技术为人民服务
# ═══════════════════════════════════════════════════════════
"""
notion_sync.py · 龍魂专属版 v1.0

DNA追溯码: #龍芯⚡️2026-03-14-notion-sync-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者: 宝宝(Claude) × UID9622

功能:
  - 读取 Notion 页面内容
  - 向 Notion 页面追加内容
  - 创建新 Notion 页面
  - 更新页面标题
  - 查询数据库
  - 写入审计日志到 Notion

用法:
  from notion_sync import NotionSync
  ns = NotionSync()
  ns.append_text(page_id, "你好，Notion！")
"""

import os
import json
import datetime
from typing import Optional, List, Dict, Any

try:
    from notion_client import Client
except ImportError:
    raise ImportError("请先安装: pip install notion-client")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # 没有 .env 也能用，手动设置环境变量即可


# ══════════════════════════════════════════
# 🔑 配置区
# ══════════════════════════════════════════

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
DEFAULT_PAGE_ID = os.getenv("NOTION_DEFAULT_PAGE_ID", "")

# DNA追溯前缀（龍魂系统专属）
DNA_PREFIX = "#龍芯⚡️"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


# ══════════════════════════════════════════
# 🐉 主类
# ══════════════════════════════════════════

class NotionSync:
    """
    龍魂 Notion 同步核心
    本地模型通过这个类读写 Notion
    """

    def __init__(self, token: str = None, default_page_id: str = None):
        self.token = token or NOTION_TOKEN
        self.default_page_id = default_page_id or DEFAULT_PAGE_ID

        if not self.token:
            raise ValueError(
                "缺少 NOTION_TOKEN！\n"
                "请在 .env 文件中设置: NOTION_TOKEN=secret_xxx"
            )

        self.client = Client(auth=self.token)
        self._log("NotionSync 初始化成功 ✅")


    # ──────────────────────────────────────
    # 📖 读取页面内容
    # ──────────────────────────────────────

    def get_page(self, page_id: str) -> Dict:
        """获取页面基本信息（标题、属性等）"""
        try:
            page = self.client.pages.retrieve(page_id=page_id)
            return page
        except Exception as e:
            self._log(f"❌ get_page 失败: {e}")
            return {}


    def get_page_content(self, page_id: str) -> List[Dict]:
        """获取页面所有 block 内容"""
        try:
            blocks = []
            cursor = None
            while True:
                response = self.client.blocks.children.list(
                    block_id=page_id,
                    start_cursor=cursor
                )
                blocks.extend(response["results"])
                if not response["has_more"]:
                    break
                cursor = response["next_cursor"]
            return blocks
        except Exception as e:
            self._log(f"❌ get_page_content 失败: {e}")
            return []


    def get_page_text(self, page_id: str) -> str:
        """提取页面纯文本（方便本地模型读取）"""
        blocks = self.get_page_content(page_id)
        lines = []
        for block in blocks:
            text = self._extract_text_from_block(block)
            if text:
                lines.append(text)
        return "\n".join(lines)


    # ──────────────────────────────────────
    # ✏️ 写入内容
    # ──────────────────────────────────────

    def append_text(self, page_id: str, text: str, dna_tag: str = None) -> bool:
        """
        向页面末尾追加一段文字

        Args:
            page_id: 目标页面ID
            text: 要写入的文字
            dna_tag: 可选，附加DNA追溯码

        Returns:
            True=成功, False=失败
        """
        content = text
        if dna_tag:
            content = f"{text}\n\n*{DNA_PREFIX}{dna_tag}*"

        try:
            self.client.blocks.children.append(
                block_id=page_id,
                children=[
                    self._make_paragraph(content)
                ]
            )
            self._log(f"✅ append_text 成功 → {page_id[:8]}...")
            return True
        except Exception as e:
            self._log(f"❌ append_text 失败: {e}")
            return False


    def append_heading(self, page_id: str, text: str, level: int = 2) -> bool:
        """
        追加标题块
        level: 1=H1, 2=H2, 3=H3
        """
        heading_map = {
            1: "heading_1",
            2: "heading_2",
            3: "heading_3"
        }
        block_type = heading_map.get(level, "heading_2")
        try:
            self.client.blocks.children.append(
                block_id=page_id,
                children=[{
                    "object": "block",
                    "type": block_type,
                    block_type: {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": text}
                        }]
                    }
                }]
            )
            self._log(f"✅ append_heading(H{level}) 成功")
            return True
        except Exception as e:
            self._log(f"❌ append_heading 失败: {e}")
            return False


    def append_code(self, page_id: str, code: str, language: str = "python") -> bool:
        """追加代码块"""
        try:
            self.client.blocks.children.append(
                block_id=page_id,
                children=[{
                    "object": "block",
                    "type": "code",
                    "code": {
                        "language": language,
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": code}
                        }]
                    }
                }]
            )
            self._log(f"✅ append_code({language}) 成功")
            return True
        except Exception as e:
            self._log(f"❌ append_code 失败: {e}")
            return False


    def append_callout(self, page_id: str, text: str, icon: str = "🐉", color: str = "blue_background") -> bool:
        """追加 Callout 高亮块"""
        try:
            self.client.blocks.children.append(
                block_id=page_id,
                children=[{
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "icon": {"type": "emoji", "emoji": icon},
                        "color": color,
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": text}
                        }]
                    }
                }]
            )
            self._log("✅ append_callout 成功")
            return True
        except Exception as e:
            self._log(f"❌ append_callout 失败: {e}")
            return False


    def append_divider(self, page_id: str) -> bool:
        """追加分割线"""
        try:
            self.client.blocks.children.append(
                block_id=page_id,
                children=[{"object": "block", "type": "divider", "divider": {}}]
            )
            return True
        except Exception as e:
            self._log(f"❌ append_divider 失败: {e}")
            return False


    # ──────────────────────────────────────
    # 📄 创建新页面
    # ──────────────────────────────────────

    def create_page(
        self,
        title: str,
        parent_page_id: str = None,
        content_text: str = None,
        icon: str = "🐉"
    ) -> Optional[str]:
        """
        创建新子页面

        Args:
            title: 页面标题
            parent_page_id: 父页面ID（默认用 DEFAULT_PAGE_ID）
            content_text: 初始内容（可选）
            icon: 页面图标 emoji

        Returns:
            新页面的 ID，失败返回 None
        """
        parent_id = parent_page_id or self.default_page_id
        if not parent_id:
            self._log("❌ create_page 失败: 未指定父页面ID")
            return None

        try:
            children = []
            if content_text:
                children.append(self._make_paragraph(content_text))

            # 追加DNA追溯码
            dna = self._make_dna_code(title)
            children.append(self._make_paragraph(f"*{dna}*"))

            new_page = self.client.pages.create(
                parent={"type": "page_id", "page_id": parent_id},
                icon={"type": "emoji", "emoji": icon},
                properties={
                    "title": {
                        "title": [{"type": "text", "text": {"content": title}}]
                    }
                },
                children=children
            )
            page_id = new_page["id"]
            self._log(f"✅ create_page 成功: {title} → {page_id[:8]}...")
            return page_id
        except Exception as e:
            self._log(f"❌ create_page 失败: {e}")
            return None


    # ──────────────────────────────────────
    # 🗄️ 数据库操作
    # ──────────────────────────────────────

    def query_database(
        self,
        database_id: str,
        filter_dict: Dict = None,
        sorts: List = None
    ) -> List[Dict]:
        """
        查询数据库

        Args:
            database_id: 数据库ID
            filter_dict: 过滤条件（Notion filter格式）
            sorts: 排序条件

        Returns:
            页面列表
        """
        try:
            kwargs = {"database_id": database_id}
            if filter_dict:
                kwargs["filter"] = filter_dict
            if sorts:
                kwargs["sorts"] = sorts

            results = []
            cursor = None
            while True:
                if cursor:
                    kwargs["start_cursor"] = cursor
                response = self.client.databases.query(**kwargs)
                results.extend(response["results"])
                if not response["has_more"]:
                    break
                cursor = response["next_cursor"]
            return results
        except Exception as e:
            self._log(f"❌ query_database 失败: {e}")
            return []


    def create_database_entry(
        self,
        database_id: str,
        properties: Dict
    ) -> Optional[str]:
        """
        在数据库中创建新条目

        Args:
            database_id: 数据库ID
            properties: 字段值（按数据库schema填写）

        Returns:
            新条目的页面ID
        """
        try:
            new_entry = self.client.pages.create(
                parent={"type": "database_id", "database_id": database_id},
                properties=properties
            )
            entry_id = new_entry["id"]
            self._log(f"✅ create_database_entry 成功: {entry_id[:8]}...")
            return entry_id
        except Exception as e:
            self._log(f"❌ create_database_entry 失败: {e}")
            return None


    # ──────────────────────────────────────
    # 📜 审计日志写入
    # ──────────────────────────────────────

    def write_audit_log(
        self,
        page_id: str,
        event: str,
        detail: str = "",
        level: str = "INFO",
        personality: str = "宝宝"
    ) -> bool:
        """
        向指定页面写入龍魂审计日志

        Args:
            page_id: 审计日志页面ID
            event: 事件名称
            detail: 详细内容
            level: INFO / WARN / ERROR
            personality: 操作人格

        Returns:
            True=成功
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dna = self._make_dna_code(event)

        log_text = (
            f"[{level}] {now}\n"
            f"事件: {event}\n"
            f"人格: {personality}\n"
            f"详情: {detail}\n"
            f"DNA: {dna}\n"
            f"GPG: {GPG}"
        )

        icon_map = {"INFO": "📋", "WARN": "🟡", "ERROR": "🔴"}
        icon = icon_map.get(level, "📋")
        color_map = {"INFO": "blue_background", "WARN": "yellow_background", "ERROR": "red_background"}
        color = color_map.get(level, "blue_background")

        return self.append_callout(page_id, log_text, icon=icon, color=color)


    # ──────────────────────────────────────
    # 🧠 记忆写入（星辰记忆专用）
    # ──────────────────────────────────────

    def write_memory(
        self,
        memory_page_id: str,
        memory_type: str,
        content: str,
        tags: List[str] = None
    ) -> bool:
        """
        写入星辰记忆

        Args:
            memory_page_id: 星辰记忆页面ID
            memory_type: knowledge / event / decision
            content: 记忆内容
            tags: 标签列表（人格名、道德经章节、卦象等）

        Returns:
            True=成功
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dna = self._make_dna_code(f"MEMORY-{memory_type}")
        tag_str = " ".join([f"#{t}" for t in (tags or [])])

        memory_text = (
            f"【{memory_type.upper()}】{now}\n"
            f"{content}\n"
            f"{tag_str}\n"
            f"{dna}"
        )

        # 先加分割线，再写记忆块
        self.append_divider(memory_page_id)
        return self.append_callout(
            memory_page_id,
            memory_text,
            icon="🌌",
            color="purple_background"
        )


    # ──────────────────────────────────────
    # 🛠️ 内部工具方法
    # ──────────────────────────────────────

    def _make_paragraph(self, text: str) -> Dict:
        """构造段落 block"""
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": text}
                }]
            }
        }


    def _extract_text_from_block(self, block: Dict) -> str:
        """从 block 提取纯文本"""
        block_type = block.get("type", "")
        data = block.get(block_type, {})
        rich_text = data.get("rich_text", [])
        texts = [rt.get("text", {}).get("content", "") for rt in rich_text]
        return "".join(texts)


    def _make_dna_code(self, label: str) -> str:
        """生成DNA追溯码"""
        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{DNA_PREFIX}{date}-{label}-UID9622"


    def _log(self, msg: str):
        """内部日志（输出到终端）"""
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[NotionSync {ts}] {msg}")


# ══════════════════════════════════════════
# 🚀 快速测试入口
# ══════════════════════════════════════════

if __name__ == "__main__":
    import sys

    print("🐉 NotionSync · 龍魂专属版 v1.0")
    print("━" * 40)

    try:
        ns = NotionSync()
    except ValueError as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)

    # 测试：向默认页面追加一条测试内容
    if ns.default_page_id:
        print("\n📝 测试：追加文本到默认页面...")
        ok = ns.append_text(
            ns.default_page_id,
            "🐉 NotionSync 连接测试成功！龍魂系统已就绪。",
            dna_tag="CONNECT-TEST"
        )
        if ok:
            print("✅ 测试通过！Notion连接正常。")
        else:
            print("❌ 测试失败，请检查 Token 和 页面ID。")
    else:
        print("⚠️  未设置 NOTION_DEFAULT_PAGE_ID，跳过写入测试")
        print("   手动测试: ns.append_text('你的页面ID', '测试内容')")

    print("\n━" * 40)
    print("💡 使用方法：")
    print("  from notion_sync import NotionSync")
    print("  ns = NotionSync()")
    print("  ns.append_text(page_id, '内容')          # 追加文字")
    print("  ns.append_code(page_id, code, 'python')  # 追加代码")
    print("  ns.create_page('标题', parent_id)        # 新建页面")
    print("  ns.write_audit_log(page_id, '事件名')    # 写审计日志")
    print("  ns.write_memory(page_id, 'event', '内容') # 写星辰记忆")