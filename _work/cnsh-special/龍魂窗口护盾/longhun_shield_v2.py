#!/usr/bin/env python3
"""
龍盾 v2.0 · 粘贴板智能中转站
====================================
DNA: #龍芯⚡️2026-05-21-LONGHUN-SHIELD-V2.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
1. 粘贴板监控 - 复制即转换，不需要其他工具
2. AI通用格式 - 输出YAML+正文，任何AI都能解析
3. Notion回写 - 自动分类到指定数据库
4. 数字根审计 - 继承v1.0的三色熔断

用法：
  # 启动监控（后台运行）
  python longhun_shield_v2.py watch

  # 手动转换粘贴板内容
  python longhun_shield_v2.py convert

  # 转换并推送到Notion
  python longhun_shield_v2.py push

  # 查看当前粘贴板结构
  python longhun_shield_v2.py peek

UID9622 原创 · 龍魂系统
"""

import re
import json
import hashlib
import argparse
import subprocess
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse

# ============================================================
# 一、配置
# ============================================================

class Config:
    """龍盾配置"""
    # Notion数据库ID（收集箱）
    NOTION_INBOX_DB = os.environ.get("NOTION_INBOX_DB", "")
    NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")

    # 数字根三色分区
    DR_GREEN = {1, 2, 4, 5, 7, 8}
    DR_YELLOW = {6}
    DR_RED = {3, 9}

    # AI通用格式模板
    FORMAT_VERSION = "longhun-shield-v2.0"


# ============================================================
# 二、粘贴板操作（macOS原生，不依赖外部库）
# ============================================================

class Clipboard:
    """macOS粘贴板操作"""

    @staticmethod
    def get() -> str:
        """获取粘贴板内容"""
        try:
            result = subprocess.run(
                ["pbpaste"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout
        except Exception as e:
            return f"[粘贴板读取失败: {e}]"

    @staticmethod
    def set(content: str) -> bool:
        """设置粘贴板内容"""
        try:
            process = subprocess.Popen(
                ["pbcopy"],
                stdin=subprocess.PIPE
            )
            process.communicate(content.encode("utf-8"))
            return process.returncode == 0
        except Exception as e:
            print(f"[粘贴板写入失败: {e}]")
            return False


# ============================================================
# 三、数字根引擎（继承v1.0）
# ============================================================

class DigitalRoot:
    """数字根计算与三色判定"""

    @staticmethod
    def extract_numbers(text: str) -> List[int]:
        """提取文本中所有数字"""
        return [int(d) for d in re.findall(r'\d', text)]

    @staticmethod
    def calculate(n: int) -> int:
        """计算数字根 dr(n) = 1 + ((n-1) mod 9)"""
        if n == 0:
            return 0
        return 1 + ((n - 1) % 9)

    @classmethod
    def analyze(cls, text: str) -> Dict[str, Any]:
        """分析文本的数字根"""
        digits = cls.extract_numbers(text)

        if not digits:
            return {
                "dr": 0,
                "color": "gray",
                "emoji": "⬜",
                "action": "pass",
                "reason": "无数字内容"
            }

        digit_sum = sum(digits)
        dr = cls.calculate(digit_sum)

        if dr in Config.DR_GREEN:
            return {
                "dr": dr,
                "color": "green",
                "emoji": "🟢",
                "action": "pass",
                "reason": f"dr={dr} 绿色通行"
            }
        elif dr in Config.DR_YELLOW:
            return {
                "dr": dr,
                "color": "yellow",
                "emoji": "🟡",
                "action": "review",
                "reason": f"dr={dr} 黄色待审"
            }
        else:  # RED
            return {
                "dr": dr,
                "color": "red",
                "emoji": "🔴",
                "action": "fuse",
                "reason": f"dr={dr} 红色熔断"
            }


# ============================================================
# 四、内容智能分类器
# ============================================================

class ContentClassifier:
    """内容类型自动识别"""

    # 类型关键词
    TYPE_PATTERNS = {
        "website": {
            "keywords": ["http", "https", "www", ".com", ".io", ".org", "网站", "官网", "链接"],
            "emoji": "🌐"
        },
        "paper": {
            "keywords": ["论文", "paper", "arxiv", "研究", "实验", "结论", "摘要", "abstract", "doi"],
            "emoji": "📄"
        },
        "video": {
            "keywords": ["视频", "video", "youtube", "bilibili", "b站", "抖音", "看了", "讲了"],
            "emoji": "🎬"
        },
        "code": {
            "keywords": ["代码", "code", "github", "仓库", "repo", "函数", "class ", "def ", "import ", "```"],
            "emoji": "💻"
        },
        "idea": {
            "keywords": ["想法", "灵感", "突然想到", "如果", "能不能", "我觉得", "试试", "方案"],
            "emoji": "💡"
        },
        "quote": {
            "keywords": ["说", "曾说", "名言", "语录", """, """, "「", "」", "——"],
            "emoji": "💬"
        },
        "trend": {
            "keywords": ["趋势", "未来", "风口", "赛道", "方向", "发展", "行业", "预测"],
            "emoji": "📈"
        },
        "task": {
            "keywords": ["TODO", "待办", "要做", "记得", "别忘", "提醒", "任务"],
            "emoji": "✅"
        }
    }

    @classmethod
    def classify(cls, text: str, url: Optional[str] = None) -> Dict[str, Any]:
        """自动分类内容"""
        combined = text + (f" {url}" if url else "")
        combined_lower = combined.lower()

        scores = {}
        for type_name, config in cls.TYPE_PATTERNS.items():
            score = sum(1 for kw in config["keywords"] if kw.lower() in combined_lower)
            scores[type_name] = score

        if not any(scores.values()):
            return {"type": "note", "emoji": "📝", "confidence": 0}

        best_type = max(scores, key=scores.get)
        return {
            "type": best_type,
            "emoji": cls.TYPE_PATTERNS[best_type]["emoji"],
            "confidence": scores[best_type]
        }

    @classmethod
    def extract_url(cls, text: str) -> Optional[str]:
        """从文本提取URL"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        matches = re.findall(url_pattern, text)
        return matches[0] if matches else None

    @classmethod
    def extract_title(cls, text: str) -> str:
        """智能提取标题"""
        lines = text.strip().split('\n')

        # 第一行如果够短，就是标题
        if lines and len(lines[0]) < 100:
            return lines[0].strip()

        # 否则取前50字
        return text[:50].replace('\n', ' ').strip() + "..."

    @classmethod
    def extract_tags(cls, text: str) -> List[str]:
        """提取标签"""
        tags = []

        # 提取 #标签
        hashtags = re.findall(r'#(\w+)', text)
        tags.extend(hashtags[:5])

        # 基于内容类型加标签
        classification = cls.classify(text)
        tags.append(classification["type"])

        return list(set(tags))[:5]


# ============================================================
# 五、AI通用格式生成器
# ============================================================

class UniversalFormat:
    """
    生成任何AI都能读懂的通用格式

    格式：YAML头 + 正文 + 尾部DNA
    任何LLM（ChatGPT/Claude/Cursor/Copilot）都认YAML
    """

    @staticmethod
    def generate(text: str, url: Optional[str] = None) -> str:
        """生成AI通用格式"""

        # 1. 分类
        classification = ContentClassifier.classify(text, url)
        extracted_url = url or ContentClassifier.extract_url(text)
        title = ContentClassifier.extract_title(text)
        tags = ContentClassifier.extract_tags(text)

        # 2. 数字根分析
        dr_result = DigitalRoot.analyze(text)

        # 3. 生成DNA
        content_hash = hashlib.sha256(text.encode()).hexdigest()[:8].upper()
        timestamp = datetime.now()
        dna = f"#龍芯⚡️{timestamp.strftime('%Y-%m-%d')}-SHIELD-{content_hash}"

        # 4. 构建YAML头
        yaml_header = f"""---
format: {Config.FORMAT_VERSION}
type: {classification['type']}
emoji: {classification['emoji']}
title: "{title.replace('"', "'")}"
source: {extracted_url or "clipboard"}
tags: [{', '.join(tags)}]
dr: {dr_result['dr']}
color: {dr_result['emoji']} {dr_result['color']}
action: {dr_result['action']}
timestamp: {timestamp.isoformat()}
dna: {dna}
---"""

        # 5. 清理正文（去掉URL如果已提取）
        body = text
        if extracted_url and extracted_url in body:
            body = body.replace(extracted_url, "").strip()

        # 6. 组装完整输出
        output = f"""{yaml_header}

{body}

---
{dr_result['emoji']} dr={dr_result['dr']} | {classification['emoji']} {classification['type']} | {dna}
"""
        return output

    @staticmethod
    def parse(formatted_text: str) -> Dict[str, Any]:
        """解析AI通用格式回结构体"""
        result = {
            "valid": False,
            "metadata": {},
            "body": ""
        }

        # 检查是否是龍盾格式
        if not formatted_text.startswith("---"):
            return result

        parts = formatted_text.split("---")
        if len(parts) < 3:
            return result

        # 解析YAML头（简单解析，不依赖yaml库）
        yaml_part = parts[1].strip()
        metadata = {}
        for line in yaml_part.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"')

        result["valid"] = True
        result["metadata"] = metadata
        result["body"] = parts[2].strip() if len(parts) > 2 else ""

        return result


# ============================================================
# 六、Notion回写器
# ============================================================

class NotionPusher:
    """推送到Notion收集箱"""

    def __init__(self):
        self.token = Config.NOTION_TOKEN
        self.database_id = Config.NOTION_INBOX_DB

    def can_push(self) -> bool:
        """检查是否可以推送"""
        return bool(self.token and self.database_id)

    def push(self, formatted_text: str) -> Dict[str, Any]:
        """推送到Notion"""
        if not self.can_push():
            return {
                "success": False,
                "error": "NOTION_TOKEN 或 NOTION_INBOX_DB 未配置",
                "help": "请在 ~/.longhun/secrets.env 配置"
            }

        # 解析格式化内容
        parsed = UniversalFormat.parse(formatted_text)
        if not parsed["valid"]:
            return {
                "success": False,
                "error": "内容不是有效的龍盾格式"
            }

        meta = parsed["metadata"]

        # 构建Notion页面数据
        # 这里用curl调用，不依赖requests库
        page_data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": meta.get("title", "未命名")[:100]}}]
                },
                "Type": {
                    "select": {"name": meta.get("type", "note")}
                },
                "Source": {
                    "url": meta.get("source") if meta.get("source", "").startswith("http") else None
                },
                "Tags": {
                    "multi_select": [{"name": t} for t in meta.get("tags", "").split(", ")[:5] if t]
                },
                "DR": {
                    "number": int(meta.get("dr", 0))
                },
                "DNA": {
                    "rich_text": [{"text": {"content": meta.get("dna", "")}}]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": parsed["body"][:2000]}}]
                    }
                }
            ]
        }

        # 写入临时文件
        tmp_file = Path("/tmp/longhun_shield_push.json")
        tmp_file.write_text(json.dumps(page_data, ensure_ascii=False))

        # 用curl推送
        try:
            result = subprocess.run([
                "curl", "-s", "-X", "POST",
                "https://api.notion.com/v1/pages",
                "-H", f"Authorization: Bearer {self.token}",
                "-H", "Content-Type: application/json",
                "-H", "Notion-Version: 2022-06-28",
                "-d", f"@{tmp_file}"
            ], capture_output=True, text=True, timeout=30)

            response = json.loads(result.stdout)

            if "id" in response:
                return {
                    "success": True,
                    "page_id": response["id"],
                    "url": response.get("url", "")
                }
            else:
                return {
                    "success": False,
                    "error": response.get("message", "未知错误"),
                    "code": response.get("code", "")
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            tmp_file.unlink(missing_ok=True)


# ============================================================
# 七、龍盾主控制器
# ============================================================

class LonghunShield:
    """龍盾v2.0主控制器"""

    def __init__(self):
        self.clipboard = Clipboard()
        self.pusher = NotionPusher()

    def convert(self, auto_copy: bool = True) -> str:
        """转换粘贴板内容为AI通用格式"""
        # 获取粘贴板
        raw = self.clipboard.get()

        if not raw or raw.startswith("[粘贴板"):
            print("❌ 粘贴板为空或读取失败")
            return ""

        # 生成通用格式
        formatted = UniversalFormat.generate(raw)

        # 写回粘贴板
        if auto_copy:
            self.clipboard.set(formatted)
            print("✅ 已转换并写回粘贴板")

        return formatted

    def peek(self) -> None:
        """预览粘贴板内容（不修改）"""
        raw = self.clipboard.get()

        if not raw:
            print("❌ 粘贴板为空")
            return

        print("📋 当前粘贴板内容：")
        print("─" * 50)
        print(raw[:500] + ("..." if len(raw) > 500 else ""))
        print("─" * 50)

        # 分析
        classification = ContentClassifier.classify(raw)
        dr_result = DigitalRoot.analyze(raw)
        url = ContentClassifier.extract_url(raw)

        print(f"\n📊 分析结果：")
        print(f"  类型: {classification['emoji']} {classification['type']}")
        print(f"  数字根: {dr_result['emoji']} dr={dr_result['dr']} ({dr_result['reason']})")
        print(f"  URL: {url or '无'}")
        print(f"  长度: {len(raw)} 字符")

    def push(self) -> None:
        """转换并推送到Notion"""
        # 先转换
        formatted = self.convert(auto_copy=False)

        if not formatted:
            return

        print("\n📤 推送到Notion...")
        result = self.pusher.push(formatted)

        if result["success"]:
            print(f"✅ 推送成功！")
            print(f"   Page ID: {result['page_id']}")
            if result.get("url"):
                print(f"   URL: {result['url']}")

            # 写回粘贴板（带Notion链接）
            formatted_with_link = formatted + f"\nNotion: {result.get('url', '')}"
            self.clipboard.set(formatted_with_link)
        else:
            print(f"❌ 推送失败: {result['error']}")
            if "help" in result:
                print(f"   帮助: {result['help']}")

    def watch(self, interval: int = 2) -> None:
        """监控粘贴板变化（持续运行）"""
        import time

        print("🛡️ 龍盾v2.0 粘贴板监控已启动")
        print("   复制内容后自动转换为AI通用格式")
        print("   按 Ctrl+C 退出")
        print("─" * 50)

        last_content = ""

        try:
            while True:
                current = self.clipboard.get()

                # 检测变化（且不是龍盾格式）
                if current != last_content and not current.startswith("---\nformat: longhun"):
                    if current and len(current) > 10:
                        print(f"\n📥 检测到新内容 ({len(current)} 字符)")

                        # 自动转换
                        formatted = UniversalFormat.generate(current)
                        self.clipboard.set(formatted)

                        # 显示摘要
                        classification = ContentClassifier.classify(current)
                        dr_result = DigitalRoot.analyze(current)
                        print(f"   ✅ 已转换: {classification['emoji']} {classification['type']} | {dr_result['emoji']} dr={dr_result['dr']}")

                        last_content = formatted
                    else:
                        last_content = current

                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n👋 龍盾监控已退出")


# ============================================================
# 八、CLI入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="龍盾v2.0 · 粘贴板智能中转站",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 转换粘贴板内容（最常用）
  python longhun_shield_v2.py convert

  # 预览分析（不修改粘贴板）
  python longhun_shield_v2.py peek

  # 转换并推送到Notion
  python longhun_shield_v2.py push

  # 启动监控模式
  python longhun_shield_v2.py watch

DNA: #龍芯⚡️2026-05-21-LONGHUN-SHIELD-V2.0
UID9622 · 龍魂系统
        """
    )

    sub = parser.add_subparsers(dest="command")

    # convert
    p_convert = sub.add_parser("convert", help="转换粘贴板内容为AI通用格式")
    p_convert.add_argument("--no-copy", action="store_true", help="不写回粘贴板，只打印")

    # peek
    sub.add_parser("peek", help="预览粘贴板内容（不修改）")

    # push
    sub.add_parser("push", help="转换并推送到Notion")

    # watch
    p_watch = sub.add_parser("watch", help="启动粘贴板监控")
    p_watch.add_argument("--interval", type=int, default=2, help="检测间隔（秒）")

    args = parser.parse_args()
    shield = LonghunShield()

    if args.command == "convert":
        result = shield.convert(auto_copy=not getattr(args, "no_copy", False))
        if getattr(args, "no_copy", False):
            print(result)

    elif args.command == "peek":
        shield.peek()

    elif args.command == "push":
        shield.push()

    elif args.command == "watch":
        shield.watch(interval=args.interval)

    else:
        # 默认行为：转换
        if len(sys.argv) == 1:
            result = shield.convert()
            print("\n📋 转换结果：")
            print(result)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
