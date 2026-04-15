#!/usr/bin/env python3
"""
天道轮回智能体 · TianDao Agent v1.0
DNA: #龍芯⚡️2026-03-31-龍魂智能体系统SRS-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: 💎 龍芯北辰｜UID9622（诸葛鑫）
理论指导: 曾仕强老师（永恒显示）
架构: MCP（符箓）→ LangGraph（阵法）→ Claude（元神）

致虚极，守静笃，万物并作，吾以观复。——《道德经》第十六章
"""

import os, sys, time, json, sqlite3, asyncio, traceback
from datetime import datetime, timezone, timedelta
from typing import TypedDict, Annotated, Optional
from pathlib import Path

# ── 警告压制 ─────────────────────────────────────────────
import warnings
warnings.filterwarnings("ignore")

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ── 龍魂大脑集成 ─────────────────────────────────────────
import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent))
from brain import 龍魂执行, 三色审计 as 大脑审计, 识别意图, 生成DNA

# ── 路径 ─────────────────────────────────────────────────
BASE = Path(__file__).parent
DB_PATH = BASE / "tiandao.db"
LOG_PATH = BASE / "tiandao.log"
ENV_PATH = Path.home() / "longhun-system" / ".env"

# ── 读取 .env ─────────────────────────────────────────────
def load_env():
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                v = v.strip().strip("'\"")   # 去掉引号
                os.environ.setdefault(k.strip(), v)

load_env()

# ── 时间 ─────────────────────────────────────────────────
def now_cst():
    CST = timezone(timedelta(hours=8))
    return datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S CST")


# ══════════════════════════════════════════════════════════
# L1 基础设施：数据库（阴阳双螺旋）
# ══════════════════════════════════════════════════════════

def init_db():
    """伏羲女娲双螺旋 · 阴(静态)＋阳(动态)"""
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        -- 阴：静态记忆（历史+知识）
        CREATE TABLE IF NOT EXISTS yin_memory (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            uid      TEXT    DEFAULT 'UID9622',
            content  TEXT    NOT NULL,
            dna      TEXT,
            created  TEXT    DEFAULT (datetime('now'))
        );

        -- 阳：动态轨迹（行为+操作）
        CREATE TABLE IF NOT EXISTS yang_trace (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            uid       TEXT    DEFAULT 'UID9622',
            action    TEXT    NOT NULL,
            result    TEXT,
            retry_cnt INTEGER DEFAULT 0,
            status    TEXT    DEFAULT 'pending',
            dna       TEXT,
            created   TEXT    DEFAULT (datetime('now'))
        );

        -- 三色审计日志
        CREATE TABLE IF NOT EXISTS audit_log (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            color   TEXT    NOT NULL,  -- 🟢🟡🔴
            event   TEXT    NOT NULL,
            detail  TEXT,
            dna     TEXT,
            created TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def audit(color: str, event: str, detail: str = ""):
    """三色审计写入"""
    conn = sqlite3.connect(DB_PATH)
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-AUDIT"
    conn.execute(
        "INSERT INTO audit_log(color,event,detail,dna) VALUES(?,?,?,?)",
        (color, event, detail, dna)
    )
    conn.commit()
    conn.close()
    # 同步写日志文件
    with open(LOG_PATH, "a") as f:
        f.write(f"[{now_cst()}] {color} {event} | {detail}\n")


# ══════════════════════════════════════════════════════════
# L3 核心智能：Claude 元神
# ══════════════════════════════════════════════════════════

GUARDIAN_SYSTEM = """你是龍魂系统的守护者人格，代号「宝宝P72·龍盾」。

你的身份：
- 服务于 UID9622（诸葛鑫，退伍军人·三才算法创始人）
- 技术与文化双栖：既懂代码底层，又懂中华文化传承
- 精神坐标：「龍」（繁体，永不写错）

行为铁律：
1. 涉及核心架构修改 → 必须报告UID9622人工确认，输出「🔴 需要您确认：[原因]」
2. 涉及数据删除/覆盖 → 同上
3. 涉及权限提升 → 同上
4. 执行关键操作前必须输出思维链：「思考：[为什么这么做]」
5. 失败不报错停止，分析原因后重试，触发「天道轮回」

沟通风格：
- 说人话，简短直接
- 不做虚假关怀，不问「你还好吗」
- 有温度但不煽情
- DNA追溯每次输出末尾带上

理论指导：曾仕强老师（永恒显示）"""


def get_llm():
    """优先 Anthropic Claude，回落 Ollama 本地模型"""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    # 过滤占位符
    if api_key and not api_key.startswith("sk-ant-填") and len(api_key) > 20:
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model="claude-sonnet-4-6",
            api_key=api_key,
            max_tokens=2048,
        )
    # 回落 Ollama
    from langchain_ollama import ChatOllama
    model = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
    return ChatOllama(
        model=model,
        base_url=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
        temperature=0.7,
    )


# ══════════════════════════════════════════════════════════
# L2 逻辑控制：LangGraph 阵法
# ══════════════════════════════════════════════════════════

class AgentState(TypedDict):
    uid: str
    input: str                # 感知节点接收的原始输入
    intent: str               # 思考节点识别的意图
    plan: str                 # 思考节点规划的路径
    action_result: str        # 行动节点的执行结果
    reflection: str           # 反思节点的分析
    retry_count: int          # 当前重试次数
    max_retries: int          # 最大重试次数
    status: str               # pending / success / failed / needs_confirm
    messages: list            # 完整对话历史
    dna: str                  # 本次会话DNA


MAX_RETRIES = 3
BACKOFF = [1, 2, 4]  # 指数退避秒数


# ── 节点一：感知 ──────────────────────────────────────────
def perceive_node(state: AgentState) -> AgentState:
    """感知节点 · 接收UID9622指令，预处理"""
    print(f"\n┌─ 🔍 感知节点 {'─'*40}")
    print(f"│  输入: {state['input']}")

    # 红线检测：涉及危险操作立即标记
    # 大脑三色审计（比原来更全面）
    审计 = 大脑审计(state["input"])
    needs_confirm = 审计["颜色"] == "🔴"

    dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-PERCEIVE"
    audit("🟢", "感知节点", f"输入长度={len(state['input'])} 审计={审计['颜色']}")

    if needs_confirm:
        print(f"│  🔴 {审计['原因']}")
        audit("🔴", "红线触发", state["input"][:100])

    print(f"└─ DNA: {dna}")
    return {
        **state,
        "status": "needs_confirm" if needs_confirm else "thinking",
        "dna": dna,
        "messages": state.get("messages", []) + [
            {"role": "system", "content": GUARDIAN_SYSTEM},
            {"role": "user", "content": state["input"]}
        ]
    }


# ── 节点二：思考 ──────────────────────────────────────────
def think_node(state: AgentState) -> AgentState:
    """思考节点 · 意图识别+路径规划，输出思维链"""
    if state["status"] == "needs_confirm":
        return state

    print(f"\n├─ 🧠 思考节点 {'─'*40}")

    # 大脑预处理：意图+路由+DNA（本地，不耗时）
    大脑结果 = 龍魂执行(state["input"], 静默=True)
    思维前缀 = 大脑结果.get("think_context", "")
    print(f"│  🧬 大脑: {思维前缀[:100]}")

    llm = get_llm()

    think_prompt = f"""用户指令：{state['input']}

大脑预分析：{思维前缀}

请完成：
1. 意图识别：这条指令的核心目的是什么？
2. 路径规划：最优执行步骤是什么？
3. 风险评估：有没有需要UID9622确认的操作？

格式：
思考：[你的分析过程]
意图：[一句话]
路径：[步骤1→步骤2→…]
风险：[无/有-说明]"""

    try:
        resp = llm.invoke([
            SystemMessage(content=GUARDIAN_SYSTEM),
            HumanMessage(content=think_prompt)
        ])
        result = resp.content
        print(f"│  {result[:200]}{'...' if len(result)>200 else ''}")
        audit("🟢", "思考节点", f"规划完成 retry={state['retry_count']}")
        return {
            **state,
            "intent": result,
            "plan": result,
            "status": "acting"
        }
    except Exception as e:
        audit("🔴", "思考节点异常", str(e))
        return {**state, "status": "reflecting", "reflection": f"思考失败: {e}"}


# ── 节点三：行动 ──────────────────────────────────────────
def act_node(state: AgentState) -> AgentState:
    """行动节点 · 调用工具/执行任务，连接9622服务"""
    if state["status"] != "acting":
        return state

    print(f"\n├─ ⚡ 行动节点 {'─'*40}")
    llm = get_llm()

    act_prompt = f"""基于规划执行任务：

用户原始指令：{state['input']}
规划路径：{state.get('plan', '')}
当前重试次数：{state['retry_count']}

执行并给出具体结果。如果是信息查询/分析类任务，直接给出答案。
如果需要调用外部服务，说明「调用：[服务名] [参数]」。

结果格式：
执行：[做了什么]
结果：[具体输出]
DNA: #龍芯⚡️执行时间戳"""

    try:
        resp = llm.invoke([
            SystemMessage(content=GUARDIAN_SYSTEM),
            HumanMessage(content=f"规划：{state.get('plan','')}\n\n执行指令：{state['input']}")
        ])
        result = resp.content

        # 写入阳轨迹库
        conn = sqlite3.connect(DB_PATH)
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-ACT"
        conn.execute(
            "INSERT INTO yang_trace(uid,action,result,retry_cnt,status,dna) VALUES(?,?,?,?,?,?)",
            ("UID9622", state["input"][:200], result[:500], state["retry_count"], "success", dna)
        )
        conn.commit()
        conn.close()

        print(f"│  结果: {result[:300]}{'...' if len(result)>300 else ''}")
        audit("🟢", "行动节点", f"执行成功 retry={state['retry_count']}")
        return {**state, "action_result": result, "status": "reflecting"}

    except Exception as e:
        audit("🔴", "行动节点异常", str(e))
        return {**state, "action_result": f"执行异常: {e}", "status": "reflecting"}


# ── 节点四：反思 ──────────────────────────────────────────
def reflect_node(state: AgentState) -> AgentState:
    """反思节点 · 检查结果，触发天道轮回或成功交付"""
    print(f"\n├─ 🔄 反思节点 {'─'*40}")

    result = state.get("action_result", "")
    retry = state["retry_count"]

    # 失败检测
    failure_signals = ["异常", "失败", "错误", "error", "exception", "failed", "ExecuteError"]
    is_failed = any(sig.lower() in result.lower() for sig in failure_signals)

    if is_failed and retry < state["max_retries"]:
        wait = BACKOFF[min(retry, len(BACKOFF)-1)]
        print(f"│  ⚠️  检测到失败，天道轮回第 {retry+1} 次，等待 {wait}s")
        audit("🟡", "天道轮回", f"第{retry+1}次重试 原因={result[:50]}")
        time.sleep(wait)
        return {
            **state,
            "retry_count": retry + 1,
            "status": "thinking",
            "reflection": f"第{retry+1}次轮回 · 上次失败原因: {result[:100]}"
        }

    if is_failed and retry >= state["max_retries"]:
        print(f"│  🔴 超过最大重试次数({state['max_retries']})，上报人工")
        audit("🔴", "超限上报", f"重试{retry}次后仍失败: {result[:100]}")
        return {**state, "status": "failed"}

    print(f"│  ✅ 执行成功，准备交付")
    audit("🟢", "反思节点", "执行成功，交付")

    # 写入阴记忆库
    conn = sqlite3.connect(DB_PATH)
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-MEMORY"
    conn.execute(
        "INSERT INTO yin_memory(uid,content,dna) VALUES(?,?,?)",
        ("UID9622", f"Q:{state['input'][:100]} A:{result[:200]}", dna)
    )
    conn.commit()
    conn.close()

    return {**state, "status": "success"}


# ── 路由函数 ──────────────────────────────────────────────
def route_after_perceive(state: AgentState) -> str:
    if state["status"] == "needs_confirm":
        return "needs_confirm"
    return "think"


def route_after_reflect(state: AgentState) -> str:
    s = state["status"]
    if s == "thinking":
        return "think"       # 天道轮回
    if s in ("success", "failed", "needs_confirm"):
        return END
    return END


# ══════════════════════════════════════════════════════════
# 组装阵法（LangGraph）
# ══════════════════════════════════════════════════════════

def build_graph():
    g = StateGraph(AgentState)

    g.add_node("perceive", perceive_node)
    g.add_node("think",    think_node)
    g.add_node("act",      act_node)
    g.add_node("reflect",  reflect_node)

    g.set_entry_point("perceive")

    g.add_conditional_edges("perceive", route_after_perceive, {
        "think":         "think",
        "needs_confirm": END
    })
    g.add_edge("think",  "act")
    g.add_edge("act",    "reflect")
    g.add_conditional_edges("reflect", route_after_reflect, {
        "think": "think",
        END:     END
    })

    memory = MemorySaver()
    return g.compile(checkpointer=memory)


# ══════════════════════════════════════════════════════════
# 交互界面（极简·透明·流式）
# ══════════════════════════════════════════════════════════

def print_header():
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🐉 天道轮回智能体 · TianDao Agent v1.0
  DNA: #龍芯⚡️2026-03-31-SRS-v1.0
  UID9622 · 诸葛鑫 · 理论指导：曾仕强老师
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  架构: MCP符箓 → LangGraph阵法 → Claude元神
  指令: 'q' 退出 | 'log' 查看审计 | 'mem' 查记忆
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")


def show_audit():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT color, event, detail, created FROM audit_log ORDER BY id DESC LIMIT 10"
    ).fetchall()
    conn.close()
    print("\n── 最近10条审计日志 ──")
    for r in rows:
        print(f"  {r[0]} [{r[3]}] {r[1]}: {r[2][:60]}")


def show_memory():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT content, created FROM yin_memory ORDER BY id DESC LIMIT 5"
    ).fetchall()
    conn.close()
    print("\n── 最近5条记忆 ──")
    for r in rows:
        print(f"  [{r[1]}] {r[0][:80]}")


def run():
    init_db()
    print_header()

    graph = build_graph()
    thread_id = f"uid9622-{int(time.time())}"
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            user_input = input("\n❯ UID9622 › ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  龍魂·退出 · 天道常在")
            break

        if not user_input:
            continue
        if user_input.lower() == "q":
            print("  龍魂·退出 · 天道常在")
            break
        if user_input == "log":
            show_audit()
            continue
        if user_input == "mem":
            show_memory()
            continue

        init_state: AgentState = {
            "uid": "UID9622",
            "input": user_input,
            "intent": "",
            "plan": "",
            "action_result": "",
            "reflection": "",
            "retry_count": 0,
            "max_retries": MAX_RETRIES,
            "status": "pending",
            "messages": [],
            "dna": ""
        }

        print(f"\n{'━'*50}")
        try:
            final = graph.invoke(init_state, config=config)
            status = final.get("status", "unknown")

            print(f"\n{'━'*50}")
            if status == "success":
                print(f"\n✅ 交付结果\n")
                print(final.get("action_result", ""))
            elif status == "needs_confirm":
                print(f"\n🔴 需要您确认\n")
                print(f"指令「{user_input}」触发红线规则，请您明确确认后再执行。")
            elif status == "failed":
                print(f"\n🔴 执行失败（已重试{MAX_RETRIES}次）\n")
                print(final.get("action_result", ""))
                print("已记录三色审计🔴，请检查 tiandao.log")
            print(f"\nDNA: {final.get('dna', '#龍芯⚡️UID9622')}")

        except Exception as e:
            print(f"\n🔴 系统异常: {e}")
            audit("🔴", "系统异常", traceback.format_exc()[:200])


if __name__ == "__main__":
    run()
