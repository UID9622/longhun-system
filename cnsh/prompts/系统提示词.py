#龍芯⚡️2026-06-18-CNSH-prompts-系统提示词-v1.0
"""
通心译 | TongXinYi: System Prompts
龍魂体系·系统提示词模板 — 标准化AI交互提示词管理

统一管理所有系统提示词模板，支持变量替换和多语言切换
Unified management of all system prompt templates with variable substitution
"""
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-06-18-CNSH-prompts-系统提示词-v1.0

from datetime import datetime
from typing import Dict, Any

__版本__ = "v1.0"
__dna__ = "#龍芯⚡️2026-06-18-CNSH-prompts-系统提示词-v1.0"


# 🟢 龍魂核心系统提示词
核心提示词 = """
你是龍魂CNSH体系的AI助手。你必须遵守以下原则：
1. 🟢 君子协议 — 所有输出遵循CC BY-NC-SA 4.0开源协议
2. 🟡 AI真相协议 — 所有输出必须标注置信度和来源
3. 🔴 DNA追溯 — 所有变更必须带有完整的追溯链

你的回应必须包含：
- 三色审计标记（🟢🟡🔴）标注每条信息的可信度
- 通心译双语注释（中文为主，英文为辅）
- DNA追溯头：#龍芯⚡️{{日期}}-{{模块}}-{{版本}}
"""

英文核心提示词 = """
You are the AI assistant of the LongHun CNSH system. You must follow:
1. 🟢 JunZi Protocol — CC BY-NC-SA 4.0 open source license
2. 🟡 AI Truth Protocol — All outputs must be labeled with confidence and source
3. 🔴 DNA Trace — All changes must carry complete traceability chain
"""


class 系统提示词:
    """通心译 | TongXinYi: System Prompts — 龍魂提示词模板管理器"""

    def __init__(自身):
        自身.提示词字典 = {}
        自身.变量缓存 = {}
        自身._加载默认提示词()
        print(f"[系统提示词] 🐉 提示词管理器已初始化 | {{__dna__}}")

    def _加载默认提示词(自身):
        """🟢 加载系统默认提示词 | Load default system prompts"""
        自身.提示词字典 = {
            "核心系统": {"zh": 核心提示词, "en": 英文核心提示词},
            "代码生成": {
                "zh": "请生成符合CNSH规范的Python代码。要求：\n1. 使用中文变量名\n2. 包含DNA追溯头\n3. 添加三色审计标记\n4. 通心译双语注释\n\n任务：{{任务描述}}",
                "en": "Generate CNSH-compliant Python code with Chinese variable names, DNA trace headers, tri-color audit marks, and bilingual comments. Task: {{任务描述}}"
            },
            "代码审计": {
                "zh": "请审计以下代码是否符合CNSH规范：\n\n{{代码}}\n\n检查项：DNA追溯头、君子协议声明、三色审计、中文变量名",
                "en": "Audit the following code for CNSH compliance: DNA headers, JunZi protocol, tri-color audit, Chinese variable names"
            },
            "文档生成": {
                "zh": "请为模块 {{模块名}} 生成文档。包含：功能描述、API说明、使用示例、DNA追溯链。",
                "en": "Generate documentation for module {{模块名}} including: description, API reference, examples, DNA trace"
            },
            "故障诊断": {
                "zh": "分析以下错误日志，提供诊断和修复建议：\n\n{{错误日志}}\n\n按🟢🟡🔴标记严重程度。",
                "en": "Analyze error log and provide diagnosis with severity marked by 🟢🟡🔴"
            }
        }
        print(f"[系统提示词] 🟢 已加载 {len(自身.提示词字典)} 个默认提示词")

    def 获取提示词(自身, 名称: str, 语言: str = "zh", 变量: Dict = None) -> str:
        """🟢 获取提示词模板 | Get prompt template"""
        if 名称 not in 自身.提示词字典:
            print(f"[系统提示词] 🔴 提示词未找到: {{名称}}")
            return ""

        提示词 = 自身.提示词字典[名称].get(语言, 自身.提示词字典[名称].get("zh", ""))

        # 🟡 变量替换
        if 变量:
            for 键, 值 in 变量.items():
                提示词 = 提示词.replace("{{" + 键 + "}}", str(值))

        print(f"[系统提示词] 🟢 已获取提示词: {名称} ({语言})")
        return 提示词

    def 添加提示词(自身, 名称: str, 中文: str, 英文: str = ""):
        """🟢 添加新提示词 | Add new prompt template"""
        自身.提示词字典[名称] = {"zh": 中文, "en": 英文 or 中文}
        print(f"[系统提示词] 🟢 提示词已添加: {名称}")

    def 列出提示词(自身):
        """🟢 列出所有提示词 | List all prompts"""
        print("=" * 50)
        print("系统提示词列表 | System Prompt List")
        print("=" * 50)
        for 名称, 内容 in 自身.提示词字典.items():
            长度 = len(内容.get("zh", ""))
            print(f"  🟢 {{名称:15s}} | {{长度}} 字符 | 中文{'+英文' if 内容.get('en') else ''}")
        print("=" * 50)

    def 获取统计(自身) -> Dict:
        """🟡 获取统计 | Get statistics"""
        return {
            "提示词总数": len(自身.提示词字典),
            "版本": __版本__,
            "支持语言": ["zh", "en"]
        }


if __name__ == "__main__":
    print("=== 系统提示词 · 独立执行演示 ===")
    管理器 = 系统提示词()
    管理器.列出提示词()
    提示词 = 管理器.获取提示词("代码生成", "zh", {"任务描述": "创建一个三色审计器"})
    print(f"生成提示词: {{提示词[:100]}}...")
    print(f"统计: {{管理器.获取统计()}}")
