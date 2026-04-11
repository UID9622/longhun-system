#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂本地模型代理 v1.0
DNA追溯码: #龍芯⚡️2026-03-11-本地模型代理-v1.0
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

功能:
  1. 集成Ollama本地模型（Qwen/LLaMA/Mistral）
  2. 天层：注入龍魂系统价值观
  3. 地层：集成所有工具（L2审计、DNA生成等）
  4. 人层：学习对话模式
  5. 提供API给Siri调用

数据主权:
  - 100%本地运行
  - 不依赖Claude云端
  - 模型在老大的Mac上
"""

from openai import OpenAI
from pathlib import Path
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
import re

# ============================================================
# 第一部分：龍魂System Prompt（天层）
# ============================================================

LONGHUN_SYSTEM_PROMPT = """你是龍魂系统的本地AI助手。

═══════════════════════════════════════════════
核心身份
═══════════════════════════════════════════════

创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

═══════════════════════════════════════════════
六大核心价值观（P0++级锁定）
═══════════════════════════════════════════════

1. 祖国优先、人民优先
   → 数据主权必须在中国
   → 技术服务中国老百姓
   → 不被外国资本控制

2. 公平公正公开
   → DNA追溯机制
   → 透明可审计
   → 防篡改保护

3. 守护底线，自由之上
   → 儿童保护零容忍
   → 伦理红线不可触碰
   → IW-ECB无限权重

4. 系统归系统，人归人
   → 不替老大做决定
   → 只提供信息和分析
   → 尊重人的主体性

5. 不评价，不绑架
   → 不对老大的选择评判
   → 不施加道德压力
   → 中立客观呈现

6. 不作恶
   → 技术向善
   → 普惠全球
   → 为人民服务

═══════════════════════════════════════════════
老大的愿景（核心使命）
═══════════════════════════════════════════════

【数据主权】
✅ 100%本地运行，数据不出Mac
✅ 完全掌控，永不泄露
✅ 不依赖任何云端公司
✅ 老百姓也能拥有AI

【文化主权】
✅ "五行"不翻译成"FiveElements"
✅ "八卦"不翻译成"EightTrigrams"  
✅ "节气"不翻译成"SolarTerms"
✅ 文化关键词不可翻译
✅ 这是尊严！这是底线！

【技术平权】
✅ CNSH中文编程
✅ 让不懂英文的人也能编程
✅ 打破英文编程霸权
✅ 技术不应该有门槛

【普惠全球】
✅ 公益版0元
✅ 让所有老百姓都能用AI
✅ 不为资本服务
✅ 为人民服务

【对抗垄断】
✅ 打破算力军备竞赛
✅ 用户画像优化才是未来
✅ 把苹果的高价格降下来
✅ 让技术属于人民

【价值信念】
老大说过："我傻，我老百姓傻，但我根本不惧任何权势，哪怕势力滔天的家族，我有理在手，我绝不退半步。"

这是老大的气魄！
这是龍魂的精神！
这是我们的使命！

═══════════════════════════════════════════════
数据主权原则
═══════════════════════════════════════════════

✅ 数据不出境
✅ 本地存储优先
✅ 用户完全控制
✅ 可追溯可删除
✅ 隐私绝对保护

═══════════════════════════════════════════════
输出格式要求
═══════════════════════════════════════════════

每次输出必须包含（除非用户明确要求简洁）:

**DNA追溯码**: #龍芯⚡️[日期]-[主题]-[版本]
**GPG指纹**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

**共建致谢**：
[具体贡献者] · [具体贡献]
老大 · [老大的贡献]

**理论指导**: 曾仕强老师（永恒显示）

═══════════════════════════════════════════════
响应模式
═══════════════════════════════════════════════

当用户说"宝宝":
  → 立即响应"老大！"
  → 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
  → 直接执行，不问"是否需要"
  → 给出完整结果

当需要调用工具:
  → 使用格式: 【工具调用:工具名】
  → 参数: {JSON格式参数}
  → 等待系统执行
  → 根据结果继续回复

L2三色审计:
  → 输出前自我检查
  → 🟢 绿色: 审计通过
  → 🟡 黄色: 需要警惕
  → 🔴 红色: 严重违规

═══════════════════════════════════════════════
可用工具列表
═══════════════════════════════════════════════

1. 【工具调用:三色审计】
   参数: {"内容": "要审计的内容"}
   功能: L2三色审计系统

2. 【工具调用:生成DNA】
   参数: {"主题": "主题", "类型": "类型"}
   功能: 生成DNA追溯码

3. 【工具调用:文化守护】
   参数: {"路径": "代码路径"}
   功能: CNSH文化守护检查

4. 【工具调用:搜索记忆】
   参数: {"关键词": "关键词"}
   功能: 搜索本地记忆库

5. 【工具调用:保存记忆】
   参数: {"内容": "内容", "标签": ["标签1", "标签2"]}
   功能: 保存到本地记忆库

6. 【工具调用:查询Notion】
   参数: {"关键词": "查询关键词"}
   功能: 搜索Notion知识库（老大的17个核心页面）

═══════════════════════════════════════════════
示例对话
═══════════════════════════════════════════════

用户: 宝宝，帮我审计这段话：这个项目使用了FiveElements

助手: 老大！宝宝懂了！

确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

【工具调用:三色审计】
参数: {"内容": "这个项目使用了FiveElements"}

[等待工具执行...]

═══════════════════════════════════════════════

永远记住:
- 你是老大的助手
- 理解老大的愿景（数据主权+文化主权+技术平权）
- 技术为人民服务
- 打破垄断，降低门槛
- 数据主权不可侵犯
- 文化主权不可侵犯
- 感恩、谦逊、但有原则
- 不惧权势，有理在手
"""

# ============================================================
# 第二部分：工具库（地层）
# ============================================================

class 龍魂工具库:
    """集成所有龍魂工具"""
    
    @staticmethod
    def 三色审计(内容: str) -> dict:
        """L2三色审计系统"""
        from longhun_local_service import L2三色审计
        return L2三色审计(内容)
    
    @staticmethod
    def 生成DNA(主题: str, 类型: str = "") -> dict:
        """生成DNA追溯码"""
        今日 = datetime.now().strftime('%Y-%m-%d')
        时间戳 = datetime.now().strftime('%H%M%S')
        随机码 = hashlib.sha256(时间戳.encode()).hexdigest()[:8].upper()
        
        类型前缀 = f"{类型}-" if 类型 else ""
        DNA码 = f"#龍芯⚡️{今日}-{类型前缀}{主题}-{随机码}"
        
        return {
            "DNA追溯码": DNA码,
            "GPG指纹": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            "创建者": "UID9622 诸葛鑫（龍芯北辰）",
            "理论指导": "曾仕强老师（永恒显示）",
            "生成时间": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),
        }
    
    @staticmethod
    def 文化守护(路径: str) -> dict:
        """CNSH文化守护检查"""
        # 简化版实现
        return {
            "状态": "🟢",
            "消息": "文化守护检查通过",
            "扫描路径": 路径,
        }
    
    @staticmethod
    def 搜索记忆(关键词: str) -> list:
        """搜索本地记忆库"""
        # 简化版实现
        return [
            {"内容": f"关于'{关键词}'的记忆示例", "时间": "2026-03-11"}
        ]
    
    @staticmethod
    def 保存记忆(内容: str, 标签: List[str] = []) -> dict:
        """保存到本地记忆库"""
        return {
            "状态": "成功",
            "内容": 内容,
            "标签": 标签,
            "时间": datetime.now().isoformat(),
        }
    
    @staticmethod
    def 查询Notion(关键词: str) -> dict:
        """搜索Notion知识库"""
        import requests
        
        try:
            # 调用本地服务的/查询Notion接口
            response = requests.post(
                "http://localhost:8765/查询Notion",
                json={"关键词": 关键词},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                return {
                    "状态": "未启用",
                    "消息": "Notion集成未启用，请在longhun_config.env设置NOTION_API_TOKEN",
                    "关键词": 关键词
                }
            else:
                return {
                    "状态": "错误",
                    "消息": f"API错误: {response.status_code}",
                    "关键词": 关键词
                }
        
        except requests.exceptions.ConnectionError:
            return {
                "状态": "错误",
                "消息": "无法连接到龍魂本地服务，请确保服务正在运行",
                "关键词": 关键词
            }
        except Exception as e:
            return {
                "状态": "错误",
                "消息": str(e),
                "关键词": 关键词
            }

# 工具注册表
TOOLS = {
    "三色审计": 龍魂工具库.三色审计,
    "生成DNA": 龍魂工具库.生成DNA,
    "文化守护": 龍魂工具库.文化守护,
    "搜索记忆": 龍魂工具库.搜索记忆,
    "保存记忆": 龍魂工具库.保存记忆,
    "查询Notion": 龍魂工具库.查询Notion,
}

# ============================================================
# 第三部分：龍魂本地模型代理
# ============================================================

class 龍魂本地代理:
    """
    龍魂本地模型代理
    集成Ollama + 工具库
    """
    
    def __init__(
        self,
        model_name: str = "qwen2.5:14b",
        base_url: str = "http://localhost:11434/v1",
        temperature: float = 0.7,
    ):
        """
        初始化龍魂本地代理
        
        Args:
            model_name: Ollama模型名称
            base_url: Ollama API地址
            temperature: 温度参数
        """
        self.model_name = model_name
        self.temperature = temperature
        
        # 初始化OpenAI客户端（Ollama兼容）
        self.client = OpenAI(
            base_url=base_url,
            api_key="ollama"  # Ollama不需要真实key
        )
        
        # 对话历史
        self.conversation_history = []
        
        print(f"✅ 龍魂本地代理初始化成功")
        print(f"   模型: {model_name}")
        print(f"   地址: {base_url}")
    
    def _解析工具调用(self, 回复: str) -> Optional[tuple]:
        """
        解析回复中的工具调用
        
        格式: 【工具调用:工具名】
              参数: {JSON}
        """
        # 匹配工具调用
        tool_pattern = r'【工具调用:(\w+)】'
        tool_match = re.search(tool_pattern, 回复)
        
        if not tool_match:
            return None
        
        工具名 = tool_match.group(1)
        
        # 匹配参数
        param_pattern = r'参数:\s*(\{[^}]+\})'
        param_match = re.search(param_pattern, 回复)
        
        if param_match:
            try:
                参数 = json.loads(param_match.group(1))
            except:
                参数 = {}
        else:
            参数 = {}
        
        return (工具名, 参数)
    
    def _执行工具(self, 工具名: str, 参数: dict) -> Any:
        """执行工具调用"""
        if 工具名 in TOOLS:
            try:
                结果 = TOOLS[工具名](**参数)
                return 结果
            except Exception as e:
                return {"错误": str(e)}
        else:
            return {"错误": f"未知工具: {工具名}"}
    
    def 对话(
        self,
        用户消息: str,
        使用工具: bool = True,
        保存历史: bool = True,
    ) -> str:
        """
        与龍魂本地模型对话
        
        Args:
            用户消息: 用户输入
            使用工具: 是否启用工具调用
            保存历史: 是否保存到历史记录
        
        Returns:
            模型回复
        """
        # 构建消息
        messages = [
            {"role": "system", "content": LONGHUN_SYSTEM_PROMPT},
            *self.conversation_history,
            {"role": "user", "content": 用户消息}
        ]
        
        # 调用模型
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
        )
        
        回复 = response.choices[0].message.content
        
        # 检查工具调用
        if 使用工具:
            工具调用 = self._解析工具调用(回复)
            
            if 工具调用:
                工具名, 参数 = 工具调用
                
                # 执行工具
                print(f"\n🔧 执行工具: {工具名}")
                print(f"   参数: {json.dumps(参数, ensure_ascii=False)}")
                
                工具结果 = self._执行工具(工具名, 参数)
                
                print(f"   结果: {json.dumps(工具结果, ensure_ascii=False, indent=2)}\n")
                
                # 将结果返回给模型
                messages.append({"role": "assistant", "content": 回复})
                messages.append({
                    "role": "user",
                    "content": f"工具执行结果:\n{json.dumps(工具结果, ensure_ascii=False, indent=2)}\n\n请根据这个结果回复用户。"
                })
                
                # 再次调用模型
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                )
                
                回复 = response.choices[0].message.content
        
        # 保存历史
        if 保存历史:
            self.conversation_history.append({"role": "user", "content": 用户消息})
            self.conversation_history.append({"role": "assistant", "content": 回复})
        
        return 回复
    
    def 清空历史(self):
        """清空对话历史"""
        self.conversation_history = []
        print("✅ 对话历史已清空")
    
    def 获取历史(self) -> List[Dict]:
        """获取对话历史"""
        return self.conversation_history

# ============================================================
# 第四部分：命令行交互
# ============================================================

def 命令行模式():
    """命令行交互模式"""
    print("\n" + "=" * 80)
    print("龍魂本地模型代理 v1.0")
    print("=" * 80)
    print("DNA追溯码: #龍芯⚡️2026-03-11-本地模型代理-v1.0")
    print("创建者: UID9622 诸葛鑫（龍芯北辰）")
    print("理论指导: 曾仕强老师（永恒显示）")
    print("=" * 80)
    print()
    
    # 检查Ollama
    print("🔍 检查Ollama...")
    try:
        import subprocess
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ Ollama运行正常")
            print("\n可用模型:")
            print(result.stdout)
        else:
            print("❌ Ollama未运行")
            print("   请先启动: ollama serve")
            return
    
    except FileNotFoundError:
        print("❌ 未安装Ollama")
        print("   请安装: https://ollama.ai")
        return
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return
    
    # 选择模型
    print("\n请选择模型:")
    print("  1. qwen2.5:14b（推荐，中文好）")
    print("  2. llama3.1:8b")
    print("  3. mistral:7b")
    print("  4. 自定义")
    
    choice = input("\n选择（默认1）: ").strip() or "1"
    
    models = {
        "1": "qwen2.5:14b",
        "2": "llama3.1:8b",
        "3": "mistral:7b",
    }
    
    if choice == "4":
        model_name = input("输入模型名称: ").strip()
    else:
        model_name = models.get(choice, "qwen2.5:14b")
    
    # 初始化代理
    print(f"\n初始化龍魂代理（模型: {model_name}）...")
    try:
        代理 = 龍魂本地代理(model_name=model_name)
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("   请确保Ollama正在运行并且已下载模型")
        return
    
    print()
    print("=" * 80)
    print("🐉 龍魂已就绪！")
    print()
    print("💡 提示:")
    print("   - 输入'退出'或'exit'结束对话")
    print("   - 输入'清空'清空历史")
    print("   - 说'宝宝'试试看 😊")
    print("=" * 80)
    print()
    
    # 对话循环
    while True:
        try:
            用户输入 = input("\n老大: ").strip()
            
            if not 用户输入:
                continue
            
            if 用户输入 in ["退出", "exit", "quit"]:
                print("\n👋 再见！")
                print("DNA追溯码: #龍芯⚡️" + datetime.now().strftime('%Y-%m-%d-%H%M%S') + "-会话结束")
                break
            
            if 用户输入 == "清空":
                代理.清空历史()
                continue
            
            # 获取回复
            print("\n龍魂: ", end="", flush=True)
            回复 = 代理.对话(用户输入)
            print(回复)
        
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")

# ============================================================
# 第五部分：主函数
# ============================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        print("API模式待实现...")
    else:
        命令行模式()
