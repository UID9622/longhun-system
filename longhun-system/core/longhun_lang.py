#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║  龍魂语言解释器 · LongHun Language Interpreter            ║
║  DNA: #龍芯⚡️2026-04-12-LONGHUN-LANG-v1.0               ║
║  创始人: 诸葛鑫（UID9622）                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
║  理论指导: 曾仕强老师（永恒显示）                          ║
║  协议: CC BY-NC-ND                                       ║
║  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z             ║
╚══════════════════════════════════════════════════════════╝

老大的歪歪话 → 龍魂语言 → 执行指令

老大不需要：
  ❌ 写PPT
  ❌ 整理逻辑
  ❌ 学编程术语
  ❌ 记命令

老大只需要：
  ✅ 说人话（哪怕歪的、骚的、带脏字的）
  ✅ 宝宝自动翻译成可执行的龍魂语言
  ✅ Notion宝宝和本地宝宝都能读懂

三层翻译管道：
  老大口语 → 通心译提取意境 → 龍魂指令 → 分发执行

献给每一个相信技术应该有温度的人。
"""

import re
import json
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

SYSTEM_ROOT = Path.home() / "longhun-system"


# ═══════════════════════════════════════════
# 龍魂语言词典
# 老大说的 → 系统听到的
# ═══════════════════════════════════════════

LONGHUN_DICT = {
    # ── 动作词 ──
    "搞": "execute",       # 搞一下 = 执行
    "干": "execute",       # 干就完了
    "弄": "execute",       # 帮我弄一下
    "搞定": "complete",    # 搞定了
    "拉": "start",         # 拉起来
    "停": "stop",          # 停掉
    "杀": "kill",          # 杀掉进程
    "查": "query",         # 查一下
    "看": "read",          # 看一下
    "存": "save",          # 存起来
    "记住": "memorize",    # 记住这个
    "落页": "write_notion", # 落到Notion
    "推": "push",          # 推到GitHub
    "拉回来": "pull",      # 拉回来
    "扫": "scan",          # 扫一下
    "审": "audit",         # 审计一下
    "签": "stamp",         # 签到
    "整理": "organize",    # 整理一下
    "串": "connect",       # 串起来
    "融": "merge",         # 融合
    "拆": "split",         # 拆开
    "补": "patch",         # 补一下
    "删": "delete",        # 删掉（需要权限）
    "冻": "freeze",        # 冻结
    "解冻": "unfreeze",    # 解冻

    # ── 对象词 ──
    "宝宝": "baobao",      # 宝宝 = AI助手
    "服务": "service",     # 本地服务
    "页面": "notion_page",
    "代码": "code",
    "脚本": "script",
    "记忆": "memory",
    "知识库": "knowledge",
    "数据库": "database",
    "钥匙": "master_key",
    "权限": "permission",
    "桌面": "desktop",
    "文件": "file",
    "日志": "log",

    # ── 状态词 ──
    "挂了": "down",
    "活着": "alive",
    "骚": "powerful",      # Xcode最骚 = Xcode最强
    "牛逼": "excellent",
    "歪": "creative",      # 歪歪的 = 有创意的
    "飘": "unstable",      # 飘了 = 不稳定
    "扎住": "stable",      # 扎住了 = 稳了
    "倒霉": "risk",        # 被盯上的倒霉 = 有风险
    "吹牛逼": "unverified", # 没落页 = 吹牛逼

    # ── 龍魂专属词（不翻译·直接传）──
    "龍": "龍",
    "龍魂": "龍魂",
    "通心译": "通心译",
    "三才": "三才",
    "数根": "数根",
    "不动点": "不动点",
    "初心": "初心",
    "DNA": "DNA",
    "卦象": "卦象",
    "三色审计": "三色审计",
}


# ═══════════════════════════════════════════
# 意图模式库
# 老大的句式 → 系统意图
# ═══════════════════════════════════════════

INTENT_PATTERNS = [
    # 格式: (正则, 意图, 参数提取)
    (r"帮我(.+?)落[到页]", "write_notion", "content"),
    (r"把(.+?)存[起到住]", "save", "content"),
    (r"(.+?)挂了", "service_check", "target"),
    (r"拉起(.+)", "service_start", "target"),
    (r"停掉?(.+)", "service_stop", "target"),
    (r"查[一下看]*(.+)", "query", "target"),
    (r"扫[一下]*(.+)", "scan", "target"),
    (r"审计[一下]*(.+?)", "audit", "target"),
    (r"签到[一下]*", "stamp_check", None),
    (r"钥匙[状态怎么样]*", "key_status", None),
    (r"服务[状态怎么样]*", "service_status", None),
    (r"整理[一下]*(.+)", "organize", "target"),
    (r"推[到上]*[Gg]it", "git_push", None),
    (r"提交[一下代码]*", "git_commit", None),
    (r"打开(.+)", "open_app", "target"),
    (r"(.+?)是什么", "explain", "target"),
    (r"记住(.+)", "memorize", "content"),
    (r"删[掉除]*(.+)", "delete", "target"),
    (r"冻结", "freeze", None),
    (r"解冻", "unfreeze", None),
]


class LongHunLang:
    """
    龍魂语言解释器

    老大说人话 → 解释器翻译 → 输出可执行的龍魂指令

    三层管道:
      1. 口语清洗（去口水词·保留语气）
      2. 意境提取（通心译·抓核心意图）
      3. 指令生成（龍魂语言·可执行）
    """

    def __init__(self):
        self.dna = f"#龍芯⚡️{datetime.date.today()}-LANG"
        self.history: List[Dict] = []

    # ═══════════════════════════════════════════
    # 第一层：口语清洗
    # ═══════════════════════════════════════════

    def clean(self, raw: str) -> str:
        """
        去口水·保语气·留干货

        老大的话可能是：
        "嗯那个就是说帮我把这个搞一下落到Notion上面去嘿嘿"
        清洗后：
        "帮我搞一下落到Notion"
        """
        # 去口水填充词
        fillers = [
            "嗯嗯", "嗯", "啊", "那个", "就是说", "就是就是",
            "然后呢", "对吧", "你知道吗", "我跟你说",
            "其实呢", "怎么说呢", "反正就是", "差不多就是",
            "嘿嘿", "哈哈哈", "哈哈", "我操", "我靠",
            "是吧", "对不对", "呃", "额", "哦",
            "上面去", "一下下", "好不好",
        ]
        text = raw
        for filler in sorted(fillers, key=len, reverse=True):
            text = text.replace(filler, "")

        # 去多余标点和逗号
        text = re.sub(r'[,，]{2,}', '，', text)
        text = re.sub(r'[.。]{2,}', '。', text)
        text = re.sub(r'\s{2,}', ' ', text)
        text = text.strip()

        return text

    # ═══════════════════════════════════════════
    # 第二层：意境提取
    # ═══════════════════════════════════════════

    def extract_intent(self, cleaned: str) -> Dict:
        """
        通心译意境提取

        从清洗后的文本中抓出：
        - 意图（干什么）
        - 对象（对谁干）
        - 参数（怎么干）
        """
        # 先试模式匹配
        for pattern, intent, param_name in INTENT_PATTERNS:
            match = re.search(pattern, cleaned)
            if match:
                param = match.group(1).strip() if match.lastindex and match.lastindex >= 1 else ""
                return {
                    "意图": intent,
                    "参数": {param_name: param} if param_name and param else {},
                    "原文": cleaned,
                    "置信度": 0.9,
                }

        # 没匹配到 → 用关键词猜
        for word, meaning in LONGHUN_DICT.items():
            if word in cleaned:
                return {
                    "意图": meaning,
                    "参数": {"原文": cleaned},
                    "原文": cleaned,
                    "置信度": 0.5,
                }

        # 完全没概念 → 聊天
        return {
            "意图": "chat",
            "参数": {"原文": cleaned},
            "原文": cleaned,
            "置信度": 0.1,
        }

    # ═══════════════════════════════════════════
    # 第三层：指令生成
    # ═══════════════════════════════════════════

    def to_command(self, intent_result: Dict) -> Dict:
        """
        把意图翻译成可执行的龍魂指令

        输出格式（Notion宝宝和本地宝宝都能读）：
        {
            "龍魂指令": "write_notion",
            "参数": {"content": "..."},
            "DNA": "...",
            "时间": "...",
            "执行者": "baobao_dispatcher" / "notion_mcp",
            "权限": "已检查" / "需确认"
        }
        """
        intent = intent_result["意图"]

        # 执行者路由
        notion_intents = {"write_notion", "query_notion", "notion_page"}
        local_intents = {"execute", "service_start", "service_stop", "service_check",
                         "service_status", "scan", "audit", "stamp_check",
                         "key_status", "git_push", "git_commit", "open_app",
                         "organize", "script", "kill"}
        memory_intents = {"save", "memorize", "memory"}

        if intent in notion_intents:
            executor = "notion_mcp"
        elif intent in local_intents:
            executor = "baobao_dispatcher"
        elif intent in memory_intents:
            executor = "baobao_dispatcher.memory"
        else:
            executor = "chat"

        # 权限检查（敏感操作）
        sensitive = {"delete", "freeze", "unfreeze", "git_push", "kill"}
        permission = "需要老大确认" if intent in sensitive else "已授权"

        # DNA生成
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        dna_hash = hashlib.sha256(
            f"{intent}{ts}{intent_result.get('原文', '')}".encode()
        ).hexdigest()[:8]

        command = {
            "龍魂指令": intent,
            "参数": intent_result.get("参数", {}),
            "DNA": f"#龍芯⚡️{ts}-CMD-{dna_hash}",
            "时间": datetime.datetime.now().isoformat(),
            "执行者": executor,
            "权限": permission,
            "置信度": intent_result.get("置信度", 0),
            "原文": intent_result.get("原文", ""),
        }

        self.history.append(command)
        return command

    # ═══════════════════════════════════════════
    # 一键翻译：老大说话 → 龍魂指令
    # ═══════════════════════════════════════════

    def translate(self, raw_input: str) -> Dict:
        """
        完整翻译管道

        老大说: "帮我把今天聊的核心落到Notion上面去嘿嘿"
        输出: {"龍魂指令": "write_notion", "参数": {"content": "今天聊的核心"}, ...}
        """
        # 第一层：清洗
        cleaned = self.clean(raw_input)

        # 第二层：意境提取
        intent = self.extract_intent(cleaned)

        # 第三层：指令生成
        command = self.to_command(intent)

        return command

    def translate_batch(self, raw_inputs: List[str]) -> List[Dict]:
        """批量翻译·多句话一起处理"""
        return [self.translate(r) for r in raw_inputs]

    def format_command(self, cmd: Dict) -> str:
        """格式化指令·给人看的版本"""
        lines = [
            f"🐉 龍魂指令: {cmd['龍魂指令']}",
            f"📦 参数: {json.dumps(cmd['参数'], ensure_ascii=False)}",
            f"🎯 执行者: {cmd['执行者']}",
            f"🔐 权限: {cmd['权限']}",
            f"📊 置信度: {cmd['置信度']:.0%}",
            f"🔏 DNA: {cmd['DNA']}",
        ]
        return "\n".join(lines)

    # ═══════════════════════════════════════════
    # Notion同步格式（Notion宝宝能读的）
    # ═══════════════════════════════════════════

    def to_notion_block(self, cmd: Dict) -> Dict:
        """
        把龍魂指令转成Notion块格式

        Notion宝宝收到这个 → 知道干什么
        """
        return {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "🐉"},
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": (
                            f"龍魂指令: {cmd['龍魂指令']}\n"
                            f"参数: {json.dumps(cmd['参数'], ensure_ascii=False)}\n"
                            f"执行者: {cmd['执行者']}\n"
                            f"DNA: {cmd['DNA']}"
                        )
                    }
                }]
            }
        }

    def export_history(self, filepath: str = None) -> str:
        """导出指令历史"""
        path = Path(filepath) if filepath else SYSTEM_ROOT / "logs" / "longhun_lang_history.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            for cmd in self.history:
                f.write(json.dumps(cmd, ensure_ascii=False) + "\n")
        return f"✅ 已导出 {len(self.history)} 条指令到 {path}"


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import sys

    lang = LongHunLang()

    if len(sys.argv) < 2:
        print("🐉 龍魂语言解释器 v1.0")
        print()
        print("用法:")
        print("  python3 longhun_lang.py '老大说的话'     # 翻译一句")
        print("  python3 longhun_lang.py demo              # 演示效果")
        print()
        print("示例:")
        print("  python3 longhun_lang.py '帮我把今天聊的落到Notion'")
        print("  python3 longhun_lang.py '服务挂了帮我看一下'")
        print("  python3 longhun_lang.py '嗯那个就是审计一下代码嘿嘿'")
        sys.exit(0)

    if sys.argv[1] == "demo":
        test_inputs = [
            "嗯那个就是说帮我把这个搞一下落到Notion上面去嘿嘿",
            "服务挂了帮我看一下",
            "宝宝帮我审计一下代码",
            "记住这个：通心译是龍魂体系的核心产品",
            "帮我把今天聊的核心存起来",
            "签到一下看看",
            "钥匙状态怎么样",
            "帮我整理一下桌面",
            "推到GitHub上去",
            "Xcode是什么",
            "我想吃火锅嘿嘿",
        ]
        print("🐉 龍魂语言解释器 · 演示\n")
        print("═" * 50)
        for raw in test_inputs:
            print(f"\n老大说: 「{raw}」")
            cmd = lang.translate(raw)
            print(lang.format_command(cmd))
            print("─" * 50)
    else:
        raw = " ".join(sys.argv[1:])
        cmd = lang.translate(raw)
        print(f"老大说: 「{raw}」\n")
        print(lang.format_command(cmd))
