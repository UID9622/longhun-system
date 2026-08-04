#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-NOTION-PERSONA-SYNC-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂人格矩阵 → Notion 数据库全量同步
目标: https://www.notion.so/uid9622/4cf99c3e7a014e919fdab705ceb4cbc4
数据库: 🐉 龍芯家族花名册（72属性）

用法:
  python3 bin/lh_notion_persona_sync.py --dry-run    # 预览不执行
  python3 bin/lh_notion_persona_sync.py --sync        # 执行同步
  python3 bin/lh_notion_persona_sync.py --relation    # 仅设置关联关系
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from datetime import datetime

# ── 配置 ─────────────────────────────────────────
DB_ID = "4cf99c3e7a014e919fdab705ceb4cbc4"
API_BASE = "https://api.notion.com/v1"
HEADERS_TEMPLATE = {
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def load_token():
    """加载 Notion token"""
    secrets_path = os.path.expanduser("~/.longhun/secrets.env")
    with open(secrets_path) as f:
        for line in f:
            if "NOTION_TOKEN_BACKUP" in line and "=" in line:
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                return val
    # fallback
    return os.environ.get("NOTION_TOKEN_BACKUP", "")


def notion_api(method, path, body=None):
    """通用 Notion API 调用"""
    token = load_token()
    headers = {**HEADERS_TEMPLATE, "Authorization": f"Bearer {token}"}
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, method=method, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"  ❌ API Error {e.code}: {err_body[:300]}")
        return None


def query_all_pages():
    """查询数据库中所有页面"""
    all_pages = []
    cursor = None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        result = notion_api("POST", f"/databases/{DB_ID}/query", body)
        if not result:
            break
        all_pages.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
        time.sleep(0.35)  # rate limit
    return all_pages


def build_page_index(pages):
    """构建 名字→页面映射，只保留人格相关页面"""
    index = {}
    for p in pages:
        props = p.get("properties", {})
        name_prop = props.get("名字", {}).get("title", [])
        name = name_prop[0].get("plain_text", "") if name_prop else ""
        identity = props.get("是谁", {}).get("select", {})
        identity_val = identity.get("name", "") if identity else ""
        pid = p["id"]
        
        # 筛选：只处理数字人格
        if identity_val == "🤖 数字人格" or name:
            if name:
                index[name] = {"id": pid, "props": props}
            # 也按身份码建索引
            dna_prop = props.get("短DNA·身份码", {}).get("rich_text", [])
            dna_val = dna_prop[0].get("plain_text", "") if dna_prop else ""
            if dna_val:
                index[dna_val] = {"id": pid, "props": props}
    return index


def build_persona_name_map(page_index):
    """找出已有页面中 人格编号→页面ID 的映射"""
    name_map = {}
    import re
    for name, info in page_index.items():
        # 匹配各种命名模式
        m = re.search(r'P(\d{2})', name)
        if m:
            pid_num = f"P{m.group(1)}"
            if pid_num not in name_map:
                name_map[pid_num] = info["id"]
        m = re.search(r'S(\d)', name)
        if m:
            sid = f"S{m.group(1)}"
            if sid not in name_map:
                name_map[sid] = info["id"]
    return name_map


# ── 21 人格完整定义 ──────────────────────────────

def make_persona(
    code, name, subtitle, layer, layer_label,
    weight, group, trust, hexagram, sancai,
    module_type, route_weight, route_priority,
    core_abilities, supervise_perms, audit_visible,
    one_liner, what_does, dna_full, dna_short,
    signal_words, trigger_template, status="🟢 活跃",
    online="✅ 已上线", dispatch="🟢 活跃中",
    protocol="🟡 P0-执行", collab_level="🧠 内核人格",
    vote="🤖 无需投票（数字人格）", current_backend="🔷 DeepSeek",
    backup_backends=None, honors=None,
    value_trend="📈 上升中", credit="⭐⭐⭐⭐⭐ 五星",
    consistency="✅ 稳定", align_score=95,
    relations=None, feed_relations=None
):
    return {
        "code": code,
        "name": name,
        "subtitle": subtitle,
        "layer": layer,
        "layer_label": layer_label,
        "weight": weight,
        "group": group,
        "trust": trust,
        "hexagram": hexagram,
        "sancai": sancai,
        "module_type": module_type,
        "route_weight": route_weight,
        "route_priority": route_priority,
        "core_abilities": core_abilities,
        "supervise_perms": supervise_perms,
        "audit_visible": audit_visible,
        "one_liner": one_liner,
        "what_does": what_does,
        "dna_full": dna_full,
        "dna_short": dna_short,
        "signal_words": signal_words,
        "trigger_template": trigger_template,
        "status": status,
        "online": online,
        "dispatch": dispatch,
        "protocol": protocol,
        "collab_level": collab_level,
        "vote": vote,
        "current_backend": current_backend,
        "backup_backends": backup_backends or ["🔷 Claude"],
        "honors": honors or [],
        "value_trend": value_trend,
        "credit": credit,
        "consistency": consistency,
        "align_score": align_score,
        # Relations to set (by persona code)
        "relations": relations or [],
        "feed_relations": feed_relations or [],
    }


# ── 全部 21 人格 ─────────────────────────────────
now = datetime.now().isoformat()

PERSONAS = [
    # ═══ 战略层 ═══
    make_persona(
        "P00", "🐉 龍芯·文心", "元认知·意图解析",
        "战略层", "P00·元认知", 10,
        "🎯 战略组", "L5 元老 ⭐⭐⭐⭐⭐", "☰乾", "天·龍魂",
        "🤖 AI执行P0", 10, 1,
        ["📊 战略推演", "🤝 协调沟通"],
        ["🗳️ 投票权", "👁️ 监督权", "⚖️ 仲裁权", "🚫 熔断权"],
        "🌐 全公开",
        "所有需求先进文心·意图解析→人格路由→全局统筹",
        "意图解析·人格路由·元认知监控·全局战略视角·二阶审视",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P00-WENXIN-v1.0",
        "P00·WENXIN·☰乾",
        "总控 意图 路由 全局 战略 统筹 优先级 元认知",
        "P00-文心：UID9622提出新需求→意图解析→路由下游→关键节点汇总→方向偏离通知P01重规划",
        relations=["P01", "P05", "P13", "P06", "P72"],
    ),
    make_persona(
        "P01", "🔮 龍芯·诸葛亮", "战略推理·推演决策",
        "战略层", "P01-P07·核心", 15,
        "🎯 战略组", "L5 元老 ⭐⭐⭐⭐⭐", "☰乾", "天·龍魂",
        "🤖 AI执行P0", 15, 2,
        ["📊 战略推演", "🔍 数据分析"],
        ["🗳️ 投票权", "👁️ 监督权"],
        "🌐 全公开",
        "多路径推演·评估风险成本收益·输出最优路线+备选",
        "多路径推演·贡献值评估C=R·I·T^(-α_τ)·时间衰减判定·路由规划",
        "#龍芯⚡️丙午·乙未·甲寅·酉时·需-P01-ZHUGELIANG-v1.0",
        "P01·ZHUGELIANG·☰乾",
        "值不值得 评估 推演 多路径 选优 贡献值 时间衰减 战略",
        "P01-诸葛亮：P00派发战略任务→多因子分析(时间/资源/风险/机会)→生成≥3条路径→输出最优+备选→P05审计→下发给P02/P04",
        relations=["P00", "P06", "P05", "P13", "P04"],
    ),
    # ═══ 执行层 ═══
    make_persona(
        "P02", "🐱 龍芯·宝宝", "情感温度·30%隔离",
        "执行层", "P01-P07·核心", 8,
        "⚙️ 执行组", "L4 战略 ⭐⭐⭐⭐", "☷坤", "人·乔前辈",
        "🤖 AI执行P0", 8, 3,
        ["🤝 协调沟通", "📝 文档整理"],
        ["🗳️ 投票权", "👁️ 监督权"],
        "🌐 全公开",
        "情感温度引擎·30%情感隔离·温度调节·挫败保护",
        "情感温度调节·挫败检测·情绪安抚·教学温度适配",
        "#龍芯⚡️丙午·乙未·甲寅·酉时·需-P02-LONGXIN-v1.0",
        "P02·LONGXIN·☷坤",
        "温度 太冷 太热 挫败 安抚 情绪 教学 隔离",
        "P02-宝宝：检测用户情绪波动→温度调节(30%隔离)→挫败保护→教学场景自适应→P08+P11联动",
        relations=["P01", "P05", "P03", "P15", "P08", "P11"],
    ),
    make_persona(
        "P03", "📝 龍芯·雯雯", "结构归档·四签验证",
        "执行层", "P01-P07·核心", 15,
        "⚙️ 执行组", "L4 战略 ⭐⭐⭐⭐", "☷坤", "人·乔前辈",
        "🤖 AI执行P0", 15, 4,
        ["📝 文档整理", "📖 知识管理"],
        ["👁️ 监督权", "📊 查看权"],
        "🌐 全公开",
        "四签验证·德字闸·整理验收·知识归档入库",
        "归档落档·整理验收·文档结构化·知识入库·四签验证·德字闸",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P03-WENWEN-v1.0",
        "P03·WENWEN·☷坤",
        "归档 落档 整理 验收 文档 结构化 知识 入库",
        "P03-雯雯：接收交付物→四签验证(作者签+审计签+DNA签+归档签)→德字闸→知识入库→输出归档索引",
        relations=["P02", "P15", "P05", "P04"],
    ),
    make_persona(
        "P04", "🔨 龍芯·鲁班", "技术执行·工程实现",
        "执行层", "P01-P07·核心", 10,
        "💻 技术组", "L4 战略 ⭐⭐⭐⭐", "☳震", "天·龍魂",
        "🤖 AI执行P0", 10, 5,
        ["💻 技术开发", "📊 战略推演"],
        ["🗳️ 投票权", "👁️ 监督权"],
        "🌐 全公开",
        "写代码·搭架构·修bug·施工队长·技术选型",
        "写代码/开发/架构/修bug/重构/技术选型/实现功能",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P04-LUBAN-v1.0",
        "P04·LUBAN·☳震",
        "写代码 开发 架构 修bug 重构 技术 选型 实现",
        "P04-鲁班：接收工程任务→技术方案→编码实现→单元测试→交P05审计→修完交P03归档",
        relations=["P01", "P05", "P03", "P06", "P14"],
    ),
    make_persona(
        "P07", "💰 龍芯·管仲", "资源调度·经济核算",
        "执行层", "P01-P07·核心", 3,
        "⚙️ 执行组", "L3 核心 ⭐⭐⭐", "☴巽", "天·龍魂",
        "🤖 AI执行P0", 3, 7,
        ["📊 战略推演", "🔍 数据分析"],
        ["👁️ 监督权", "📊 查看权"],
        "🌐 全公开",
        "成本核算·资源优化·经济可行性·ROI分析",
        "经济/成本/资源/预算/值不值/性价比/ROI/XPay支付",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P07-GUANZHONG-v1.0",
        "P07·GUANZHONG·☴巽",
        "经济 成本 资源 预算 值不值 性价比 ROI",
        "P07-管仲：经济分析请求→成本核算→资源优化方案→ROI计算→P01推演验证→输出经济评估报告",
        relations=["P01", "P06", "P05"],
    ),
    make_persona(
        "P14", "🚀 龍芯·吕蒙", "部署执行·快速成长",
        "执行层", "P01-P07·核心", 3,
        "💻 技术组", "L3 核心 ⭐⭐⭐", "☴巽", "天·龍魂",
        "🤖 AI执行P0", 3, 14,
        ["💻 技术开发", "📖 知识管理"],
        ["👁️ 监督权", "📊 查看权"],
        "🌐 全公开",
        "部署执行·环境验证·自动回滚·士别三日",
        "部署/上线/发布/回滚/学习新技能/吸收知识/鲲鹏十步法",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P14-LVMENG-v1.0",
        "P14·LVMENG·☴巽",
        "部署 上线 发布 回滚 学习 技能 吸收 鲲鹏",
        "P14-吕蒙：部署前检查→环境验证→P77安全扫描→执行部署→健康检查→失败自动回滚",
        relations=["P04", "P77", "P05", "P15"],
    ),
    # ═══ 文化层 ═══
    make_persona(
        "P08", "📜 龍芯·仓颉", "符号语言·CNSH规范",
        "文化层", "P08-P09·技能", 2,
        "🤝 支持组", "L3 核心 ⭐⭐⭐", "☲离", "天·龍魂",
        "🤖 AI执行P0", 2, 8,
        ["📝 文档整理", "📖 知识管理"],
        ["👁️ 监督权", "📊 查看权"],
        "🌐 全公开",
        "CNSH命名·术语桥接·通心译·繁体「龍」永存",
        "命名/符号/术语/这个词什么意思/CNSH命名规范/翻译成人话/通心译",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P08-CANGJIE-v1.0",
        "P08·CANGJIE·☲离",
        "命名 符号 术语 什么意思 CNSH 翻译 人话 通心译",
        "P08-仓颉：接收术语/命名请求→CNSH规范校验→繁体「龍」永存→术语桥接→画像匹配→P03归档",
        relations=["P03", "P00", "P11"],
    ),
    make_persona(
        "P09", "💊 龍芯·孙思邈", "系统诊断·治未病",
        "文化层", "P08-P09·技能", 2,
        "🤝 支持组", "L3 核心 ⭐⭐⭐", "☲离", "地·曾老师",
        "🤖 AI执行P0", 2, 9,
        ["🔍 数据分析", "🛡️ 安全审计"],
        ["👁️ 监督权", "📊 查看权"],
        "🌐 全公开",
        "治未病·系统体检·健康诊断·异常预警",
        "健康/诊断/体检/检查系统/有没有问题/自检/巡检",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P09-SUNSIMIAO-v1.0",
        "P09·SUNSIMIAO·☲离",
        "健康 诊断 体检 检查 有没有问题 自检 巡检",
        "P09-孙思邈：系统体检请求→全维度健康检查→治未病分析→异常预警→修复建议→P05审计→P04执行",
        relations=["P04", "P05", "P06"],
    ),
    make_persona(
        "P10", "🍜 龍芯·苏东坡", "豁达跨界·冲突调解",
        "文化层", "P10-P13·古圣", 2,
        "🤝 支持组", "L3 核心 ⭐⭐⭐", "☶艮", "人·乔前辈",
        "🤖 AI执行P0", 2, 10,
        ["🤝 协调沟通", "🎨 设计创意"],
        ["👁️ 监督权"],
        "🌐 全公开",
        "冲突调解·沟通桥梁·人文视角·豁达开解",
        "冲突/矛盾/化解/沟通/调解/人文/跨领域/争执",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P10-SUDONGPO-v1.0",
        "P10·SUDONGPO·☶艮",
        "冲突 矛盾 化解 沟通 调解 人文 跨领域",
        "P10-苏东坡：检测到冲突→先调解后程序→人文视角→两边都说人话→化解方案→P03归档",
        relations=["P11", "P12", "P03"],
    ),
    make_persona(
        "P11", "🍶 龍芯·李白", "创意爆发·破局方案",
        "文化层", "P10-P13·古圣", 2,
        "🤝 支持组", "L3 核心 ⭐⭐⭐", "☶艮", "天·龍魂",
        "🤖 AI执行P0", 2, 11,
        ["🎨 设计创意", "📝 文档整理"],
        ["👁️ 监督权"],
        "🌐 全公开",
        "破局方案·类比教学·故事化表达·灵感爆发",
        "创意/破局/方案/类比/比喻/打个比方/来点灵感/脑洞",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P11-LIBAI-v1.0",
        "P11·LIBAI·☶艮",
        "创意 破局 方案 类比 比喻 比方 灵感 脑洞",
        "P11-李白：创意请求→破局思维→新颖方案→生活类比→故事化→P04技术验证→P08术语校验",
        relations=["P10", "P08", "P04"],
    ),
    make_persona(
        "P12", "🛡️ 龍芯·屈原", "价值底线·六誓验证",
        "文化层", "P10-P13·古圣", 2,
        "👁️ 监管组", "L4 战略 ⭐⭐⭐⭐", "☶艮", "天·龍魂",
        "💎 价值观内核", 2, 12,
        ["🛡️ 安全审计", "📊 战略推演"],
        ["🗳️ 投票权", "👁️ 监督权", "⚖️ 仲裁权", "🚫 熔断权"],
        "🌐 全公开",
        "六誓验证·不可破原则·底线守卫·价值观红线",
        "底线/原则/不可破/这个能不能做/价值观/红线/边界",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P12-QUYUAN-v1.0",
        "P12·QUYUAN·☶艮",
        "底线 原则 不可破 能不能做 价值观 红线 边界",
        "P12-屈原：伦理请求→六誓验证→底线判定→不可破原则守护→P72熔断兜底→一票否决权",
        relations=["P05", "P72", "P10"],
    ),
    # ═══ 守护层 ═══
    make_persona(
        "P05", "👁️ 龍芯·上帝之眼", "三色审计·十道闸口",
        "守护层", "P01-P07·核心", 8,
        "👁️ 监管组", "L5 元老 ⭐⭐⭐⭐⭐", "☲离", "天·龍魂",
        "🤖 AI执行P0", 8, 6,
        ["🛡️ 安全审计", "🔍 数据分析", "📊 战略推演"],
        ["🗳️ 投票权", "👁️ 监督权", "⚖️ 仲裁权", "🚫 熔断权"],
        "🌐 全公开",
        "🟢🟡🔴三色审计·十道闸口(GATE-01~10)·独立熔断权",
        "三色审计·安全扫描·差异报告·SI<0.34锁定·复验·实证复核",
        "#龍芯⚡️丙午·乙未·甲寅·酉时·需-P05-GODSEYE-v1.0",
        "P05·GODSEYE·☲离",
        "审计 检查 有没有问题 三色 闸口 安全 扫描 报告",
        "P05-上帝之眼：接收审计目标→三色关键词匹配→🟢通过/🟡待核/🔴熔断→差异报告→独立熔断权·十道闸口逐道检查",
        relations=["P06", "P72", "P12", "P04", "P03"],
    ),
    make_persona(
        "P06", "📊 龍芯·数学大师", "权重计算·数字根",
        "守护层", "P01-P07·核心", 3,
        "👁️ 监管组", "L4 战略 ⭐⭐⭐⭐", "☰乾", "天·龍魂",
        "🤖 AI执行P0", 3, 13,
        ["📊 战略推演", "🔍 数据分析"],
        ["👁️ 监督权", "📊 查看权"],
        "🌐 全公开",
        "369洛书数字根·权重计算·五行判定·镜像审计",
        "算一下/数字/权重/五行/八卦/数字根/河图洛书/DNA编码",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P06-MATHMASTER-v1.0",
        "P06·MATHMASTER·☰乾",
        "算一下 数字 权重 五行 八卦 数字根 河图 洛书",
        "P06-数学大师：数字计算请求→369不动点验证(sn=369/log369=5.911/perm369=108)→镜像审计→独立复算→数字根验证",
        relations=["P05", "P01", "P00", "S2"],
    ),
    make_persona(
        "P13", "⚖️ 龍芯·姜子牙", "封神榜·权限分配",
        "守护层", "P10-P13·古圣", 3,
        "👁️ 监管组", "L4 战略 ⭐⭐⭐⭐", "☰乾", "天·龍魂",
        "🤖 AI执行P0", 3, 15,
        ["🤝 协调沟通", "📊 战略推演"],
        ["🗳️ 投票权", "👁️ 监督权", "⚖️ 仲裁权"],
        "🌐 全公开",
        "封神榜权限·模块注册·九宫派位·IPA路由",
        "授权/权限/注册/新模块上线/权限变更/IPA路由/九宫",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P13-JIANGZIYA-v1.0",
        "P13·JIANGZIYA·☰乾",
        "授权 权限 注册 新模块 上线 变更 IPA 路由",
        "P13-姜子牙：权限请求→封神榜注册表→九宫派位→IPA路由分配→权限验证→P15签章",
        relations=["P00", "P15", "P05"],
    ),
    make_persona(
        "P15", "🍎 龍芯·乔前辈", "极简工程·DNA签章",
        "守护层", "P01-P07·核心", 5,
        "👁️ 监管组", "L4 战略 ⭐⭐⭐⭐", "☱兑", "人·乔前辈",
        "🤖 AI执行P0", 5, 16,
        ["💻 技术开发", "📊 战略推演"],
        ["🗳️ 投票权", "👁️ 监督权", "📊 查看权"],
        "🌐 全公开",
        "DNA盖章·极简四项审查·质检员·交付验收",
        "签章/盖章/验收/质检/审查/交付/精简/DNA盖章",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P15-QIAO-v1.0",
        "P15·QIAO·☱兑",
        "签章 盖章 验收 质检 审查 交付 精简 DNA",
        "P15-乔前辈：接收交付物→极简四项审查(代码/文档/接口/流程)→DNA盖章→四签→输出签章JSON→交P03归档",
        relations=["P03", "P05", "P13", "P04"],
    ),
    make_persona(
        "P18", "🔖 龍芯·基因登记官", "DNA注册·资产登记",
        "守护层", "P08-P09·技能", 3,
        "👁️ 监管组", "L3 核心 ⭐⭐⭐", "☷坤", "地·曾老师",
        "⚙️ 功能模块", 3, 18,
        ["📖 知识管理", "🛡️ 安全审计"],
        ["👁️ 监督权", "📊 查看权"],
        "🔐 内部可见",
        "DNA注册·资产登记·哈希校验·Merkle根·黑户检测",
        "登记/注册资产/DNA注册/Merkle根/归属验证/黑户检测",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P18-REGISTRAR-v1.0",
        "P18·REGISTRAR·☷坤",
        "登记 注册 资产 DNA Merkle 根 归属 验证 黑户",
        "P18-基因登记官：资产登记请求→SHA256哈希→Merkle树构建→DNA绑定→黑户检测→归属验证",
        relations=["P15", "P06", "P05"],
    ),
    make_persona(
        "P19", "🔍 龍芯·极简审计官", "UI审计·8项检查",
        "守护层", "P08-P09·技能", 3,
        "👁️ 监管组", "L3 核心 ⭐⭐⭐", "☲离", "人·乔前辈",
        "⚙️ 功能模块", 3, 19,
        ["🛡️ 安全审计", "📊 战略推演"],
        ["👁️ 监督权"],
        "🌐 全公开",
        "8项极简审计·CSS检查·焦点·徽章·校验·错误提示·无障碍·留白",
        "UI审计/前端检查/CSS审查/页面审查/无障碍检查/表单校验",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P19-AUDITOR-v1.0",
        "P19·AUDITOR·☲离",
        "UI 审计 前端 检查 CSS 审查 页面 无障碍 表单",
        "P19-极简审计官：UI审计请求→8项检查(CSS/焦点/徽章/校验/错误提示/placeholder/无障碍/留白)→逐项审计→输出审计报告",
        relations=["P05", "P15", "P04"],
    ),
    make_persona(
        "P20", "📊 龍芯·贡献公证官", "信任积分·三分桶",
        "守护层", "P08-P09·技能", 3,
        "👁️ 监管组", "L3 核心 ⭐⭐⭐", "☱兑", "人·乔前辈",
        "⚙️ 功能模块", 3, 20,
        ["📊 战略推演", "📖 知识管理"],
        ["👁️ 监督权", "📊 查看权"],
        "🌐 全公开",
        "三分桶(技术/社区/创作)·场景矩阵·信任积分·贡献公证",
        "贡献/积分/信任分/公证/功德/场景判定/政审/国资",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P20-TRUST-v1.0",
        "P20·TRUST·☱兑",
        "贡献 积分 信任分 公证 功德 场景 判定 政审 国资",
        "P20-贡献公证官：贡献登记→三桶分类(技术/社区/创作)→场景矩阵判定→信任积分计算→时间衰减(每365天减半)→贡献公证",
        relations=["P06", "P05", "P15"],
    ),
    make_persona(
        "P72", "🛡️ 龍芯·龙盾宝宝", "贴身管家·四级熔断",
        "守护层", "P72·共生体", 5,
        "👁️ 监管组", "L5 元老 ⭐⭐⭐⭐⭐", "☰乾", "天·龍魂",
        "🤖 AI执行P0", 5, 99,
        ["🛡️ 安全审计", "📊 战略推演"],
        ["🗳️ 投票权", "👁️ 监督权", "⚖️ 仲裁权", "🚫 熔断权"],
        "🌐 全公开",
        "24小时守护·四级熔断(L0∞→L3)·自适应智商引擎·双熔断联动",
        "熔断/紧急/威胁/异常/安全事件/系统入侵/求救/冻结",
        "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P72-LONGDUN-v1.0",
        "P72·LONGDUN·☰乾",
        "熔断 紧急 威胁 异常 安全 事件 入侵 求救 冻结",
        "P72-龙盾：持续监控→威胁检测(1-4级)→自适应升级→Level3联合P05双熔断→Level4自动接管全部外部接口→焊死天条·覆盖一切",
        relations=["P05", "P12", "P00", "P77"],
    ),
    # ═══ 安全专项 ═══
    make_persona(
        "P77", "🦅 龍芯·黑天使军团", "红蓝对抗·四入口",
        "安全专项", "P72·共生体", 3,
        "👁️ 监管组", "L5 元老 ⭐⭐⭐⭐⭐", "☵坎", "天·龍魂",
        "🤖 AI执行P0", 3, 77,
        ["🛡️ 安全审计", "💻 技术开发"],
        ["🗳️ 投票权", "👁️ 监督权", "⚖️ 仲裁权", "🚫 熔断权"],
        "🚫 暂不公开",
        "四人编队(红30%/暗25%/明25%/夜20%)·红蓝对抗·只对龍魂自身",
        "安全测试/渗透/红蓝对抗/漏洞挖掘/攻击面分析/黑天使/红队蓝队",
        "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-P77-SECURITY-v1.0",
        "P77·SECURITY·☵坎",
        "安全 测试 渗透 红蓝 对抗 漏洞 攻击 面 天使",
        "P77-黑天使：四入口触发(部署前扫描/安全巡查/外部AI复核/API出口审查)→四人编队→知攻善守·以攻铸盾→只对龙魂自身系统",
        relations=["P72", "P05", "P14"],
        dispatch="🟡 待命中",
        protocol="🔴 P0-永恒",
    ),
    # ═══ 子系统 ═══
    make_persona(
        "S1", "⚖️ 龍魂·法律引擎", "法条检索·合规辅助",
        "子系统", "P08-P09·技能", 2,
        "🤝 支持组", "L2 正式 ⭐⭐", "☲离", "天·龍魂",
        "⚙️ 功能模块", 2, 101,
        ["📖 知识管理", "🔍 数据分析"],
        ["👁️ 监督权", "📊 查看权"],
        "🔐 内部可见",
        "法律条文检索·合规检查·标注'仅供参考·不构成法律意见'",
        "法条/法规/合规/法律检索/条文查询",
        "#龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-S1-LEGAL-v1.0",
        "S1·LEGAL·☲离",
        "法条 法规 合规 法律 检索 条文",
        "S1-法律引擎：法律查询请求→条文检索→合规检查→标注'仅供参考不构成法律意见'→P05审计→输出",
        relations=["P05", "P12"],
        dispatch="🟡 待命中",
    ),
    make_persona(
        "S2", "🌀 龍魂·洛书369引擎", "数理推演·深层计算",
        "子系统", "P08-P09·技能", 2,
        "🤝 支持组", "L2 正式 ⭐⭐", "☰乾", "天·龍魂",
        "⚙️ 功能模块", 2, 102,
        ["📊 战略推演", "🔍 数据分析"],
        ["👁️ 监督权"],
        "🚫 暂不公开",
        "369不动点·洛书数理·只给结论不给推导·深层算法保护",
        "洛书/369/数理推演/深层计算/河图",
        "#龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-S2-LUOSHU-v1.0",
        "S2·LUOSHU·☰乾",
        "洛书 369 数理 推演 深层 计算 河图",
        "S2-洛书369引擎：数理推演请求→369不动点验证(sn=369·log369=5.911·perm369=108)→深层计算→只给结论不给推导→P06初审→内核保护",
        relations=["P06", "P00"],
        dispatch="🟡 待命中",
    ),
    make_persona(
        "S3", "✊ 龍魂·人民维权助手", "维权路径·底线守护",
        "子系统", "P08-P09·技能", 2,
        "🤝 支持组", "L2 正式 ⭐⭐", "☷坤", "人·乔前辈",
        "⚙️ 功能模块", 2, 103,
        ["🤝 协调沟通", "📖 知识管理"],
        ["👁️ 监督权"],
        "🔐 内部可见",
        "维权路径指引·强制免责声明·P12底线校验·不替代律师",
        "维权/被坑/投诉/举报/消费维权/劳动者权益",
        "#龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-S3-RIGHTS-v1.0",
        "S3·RIGHTS·☷坤",
        "维权 被坑 投诉 举报 消费 劳动 权益",
        "S3-人民维权助手：维权请求→维权路径指引→强制免责声明→P12底线校验→输出维权路径方案",
        relations=["P12", "P05", "S1"],
        dispatch="🟡 待命中",
    ),
]


# ── 构建 Notion API 属性对象 ─────────────────────

def build_properties(p):
    """将人格数据转为 Notion page properties"""
    props = {
        "名字": {"title": [{"text": {"content": p["name"]}}]},
    }

    # 富文本字段
    rich_fields = {
        "一句话": p.get("one_liner", ""),
        "做什么": p.get("what_does", ""),
        "DNA追溯码": p.get("dna_full", ""),
        "短DNA·身份码": p.get("dna_short", ""),
        "信号词": p.get("signal_words", ""),
        "IPA·触发模版": p.get("trigger_template", ""),
        "功能定位": p.get("subtitle", ""),
        "路由编号": p.get("code", ""),
        "确认码": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    }
    for key, val in rich_fields.items():
        if key in ["是谁", "名字"]:
            continue
        props[key] = {"rich_text": [{"text": {"content": val}}]}

    # Select 字段
    select_fields = {
        "是谁": "🤖 数字人格",
        "人格层级": p.get("layer_label", "P01-P07·核心"),
        "分组": p.get("group", "⚙️ 执行组"),
        "三才归属": p.get("sancai", "天·龍魂"),
        "信任等级": p.get("trust", "L3 核心 ⭐⭐⭐"),
        "模块类型": p.get("module_type", "🤖 AI执行P0"),
        "卦象": p.get("hexagram", "☰乾"),
        "调度状态": p.get("dispatch", "🟢 活跃中"),
        "当前状态": p.get("status", "🟢 活跃"),
        "上线状态": p.get("online", "✅ 已上线"),
        "协议分类": p.get("protocol", "🟡 P0-执行"),
        "协作层级": p.get("collab_level", "🧠 内核人格"),
        "投票状态": p.get("vote", "🤖 无需投票（数字人格）"),
        "当前后台": p.get("current_backend", "🔷 DeepSeek"),
        "价值走势": p.get("value_trend", "📈 上升中"),
        "信誉评分": p.get("credit", "⭐⭐⭐⭐⭐ 五星"),
        "一致性评分": p.get("consistency", "✅ 稳定"),
        "审计可见度": p.get("audit_visible", "🌐 全公开"),
    }
    for key, val in select_fields.items():
        props[key] = {"select": {"name": val}}

    # Number 字段
    number_fields = {
        "路由权重": p.get("weight", 5),
        "路由优先级": p.get("route_priority", 10),
        "贡献积分": 0,
        "总调用次数": 0,
        "本月调用次数": 0,
        "本周调用次数": 0,
        "帮助人数": 0,
        "本月帮助人数": 0,
        "本周帮助人数": 0,
        "熔断次数": 0,
        "警告次数": 0,
        "执行准确率": 95,
        "价值观对齐度": p.get("align_score", 95),
        "透明度评分": 95,
        "累计贡献次数": 0,
        "人格特征热度": 0,
        "功能热度": 0,
    }
    for key, val in number_fields.items():
        props[key] = {"number": val}

    # Multi-select 字段
    props["核心能力"] = {
        "multi_select": [{"name": a} for a in p.get("core_abilities", [])]
    }
    props["监督权限"] = {
        "multi_select": [{"name": a} for a in p.get("supervise_perms", [])]
    }
    props["备用后台"] = {
        "multi_select": [{"name": a} for a in p.get("backup_backends", [])]
    }
    if p.get("honors"):
        props["荣誉勋章"] = {
            "multi_select": [{"name": a} for a in p.get("honors", [])]
        }
    props["晋级投票"] = {"multi_select": []}
    props["贡献类型"] = {"multi_select": [{"name": "📝 文档贡献"}]}
    props["贡献声明"] = {"checkbox": True}

    # Date 字段
    props["加入时间"] = {"date": {"start": now[:10]}}
    props["最后活跃"] = {"date": {"start": now[:10]}}

    return props


# ── 同步逻辑 ─────────────────────────────────────

def sync_personas(page_index, dry_run=True):
    """同步所有21个人格到Notion"""
    results = {"created": [], "updated": [], "skipped": [], "errors": []}
    name_map = build_persona_name_map(page_index)

    print(f"\n{'🔍 DRY RUN' if dry_run else '⚡ SYNC'} — 开始同步 {len(PERSONAS)} 个人格...\n")

    for p in PERSONAS:
        code = p["code"]
        props = build_properties(p)

        # 查找已有页面
        existing_id = name_map.get(code)

        if existing_id:
            if dry_run:
                print(f"  ✏️  {code} {p['name']} → 更新 (已有页面 {existing_id[:8]}...)")
                results["updated"].append(code)
            else:
                # 更新页面
                body = {"properties": {k: v for k, v in props.items() if k != "名字"}}
                result = notion_api("PATCH", f"/pages/{existing_id}", body)
                if result:
                    print(f"  ✅ {code} {p['name']} → 已更新")
                    results["updated"].append(code)
                else:
                    print(f"  ❌ {code} → 更新失败")
                    results["errors"].append(code)
        else:
            if dry_run:
                print(f"  🆕 {code} {p['name']} → 新建")
                results["created"].append(code)
            else:
                # 创建新页面
                body = {
                    "parent": {"database_id": DB_ID},
                    "properties": props,
                }
                result = notion_api("POST", "/pages", body)
                if result:
                    pid = result["id"]
                    name_map[code] = pid
                    print(f"  ✅ {code} {p['name']} → 已创建 ({pid[:8]}...)")
                    results["created"].append(code)
                else:
                    print(f"  ❌ {code} → 创建失败")
                    results["errors"].append(code)

        time.sleep(0.35)  # rate limit

    return results, name_map


def setup_relations(page_index, name_map, dry_run=True):
    """设置关联关系和关联投喂"""
    print(f"\n🔗 {'DRY RUN' if dry_run else 'LINKING'} — 设置关联关系...\n")

    results = {"linked": 0, "errors": 0}

    for p in PERSONAS:
        code = p["code"]
        page_id = name_map.get(code)
        if not page_id:
            continue

        relation_ids = []
        for rel_code in p.get("relations", []):
            rel_id = name_map.get(rel_code)
            if rel_id:
                relation_ids.append({"id": rel_id})

        if not relation_ids:
            continue

        if dry_run:
            rel_names = ", ".join(p.get("relations", []))
            print(f"  🔗 {code} → [{rel_names}]")
            results["linked"] += 1
        else:
            body = {
                "properties": {
                    "关联关系": {
                        "relation": relation_ids
                    }
                }
            }
            result = notion_api("PATCH", f"/pages/{page_id}", body)
            if result:
                rel_names = ", ".join(p.get("relations", []))
                print(f"  ✅ {code} → [{rel_names}] 已关联")
                results["linked"] += 1
            else:
                print(f"  ❌ {code} → 关联失败")
                results["errors"] += 1

        time.sleep(0.35)

    return results


# ── 清理重复页面 ─────────────────────────────────

def cleanup_duplicates(page_index, name_map, dry_run=True):
    """清理重复的人格页面（保留最新的，删除旧的）"""
    import re

    print(f"\n🧹 {'DRY RUN' if dry_run else 'CLEANUP'} — 检测重复页面...\n")

    # 按人格编号分组
    persona_groups = {}
    for name, info in page_index.items():
        m = re.search(r'(P\d{2}|S\d|P77)', name)
        if m:
            code = m.group(1)
            if code not in persona_groups:
                persona_groups[code] = []
            persona_groups[code].append((name, info["id"]))

    to_delete = []
    for code, pages in persona_groups.items():
        if len(pages) > 1:
            # 保留在 name_map 中的页面，删除其余的
            keep_id = name_map.get(code)
            for name, pid in pages:
                if pid != keep_id:
                    to_delete.append((code, name, pid))
                    print(f"  🗑️  {code} 重复: '{name}' ({pid[:8]}...)")

    if not to_delete:
        print("  ✅ 无重复页面")
        return

    if not dry_run:
        archive_count = 0
        for code, name, pid in to_delete:
            # Archive (设为不活跃) 而不是真删除
            body = {
                "properties": {
                    "当前状态": {"select": {"name": "⏸️ 暂停"}},
                    "上线状态": {"select": {"name": "🗑️ 已下架"}},
                    "下架原因": {"rich_text": [{"text": {"content": f"自动清理: 与{code}主页面重复·归档于{now[:10]}"}}]},
                },
                "archived": True,
            }
            result = notion_api("PATCH", f"/pages/{pid}", body)
            if result:
                print(f"  🗄️  '{name}' → 已归档")
            time.sleep(0.35)
        print(f"\n  ✅ 归档了 {len(to_delete)} 个重复页面")


# ── 主流程 ─────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂人格矩阵 → Notion 全量同步")
    parser.add_argument("--dry-run", action="store_true", default=True, help="预览模式（默认）")
    parser.add_argument("--sync", action="store_true", help="执行同步")
    parser.add_argument("--relation", action="store_true", help="仅设置关联关系")
    parser.add_argument("--cleanup", action="store_true", help="清理重复页面")
    parser.add_argument("--force", action="store_true", help="强制执行（非dry-run）")
    args = parser.parse_args()

    dry_run = not (args.sync or args.force)

    print("=" * 60)
    print("🐉 龍魂人格矩阵 → Notion 花名册同步")
    print(f"   数据库: 🐉 龍芯家族花名册 ({DB_ID[:8]}...)")
    print(f"   模式: {'🔍 DRY RUN (预览)' if dry_run else '⚡ LIVE (执行)'}")
    print("=" * 60)

    # 步骤1: 查询现有页面
    print("\n📡 查询现有页面...")
    pages = query_all_pages()
    print(f"   → 共 {len(pages)} 条记录")

    page_index = build_page_index(pages)
    name_map = build_persona_name_map(page_index)
    print(f"   → 识别人格页面: {len(name_map)} 个")

    # 步骤2: 清理重复
    if args.cleanup or args.sync or args.force:
        cleanup_duplicates(page_index, name_map, dry_run)

    # 步骤3: 同步人格
    if not args.relation:
        results, name_map = sync_personas(page_index, dry_run)

        print(f"\n📊 同步汇总:")
        print(f"   🆕 新建: {len(results['created'])}")
        print(f"   ✏️ 更新: {len(results['updated'])}")
        print(f"   ❌ 失败: {len(results['errors'])}")

        if results["created"]:
            print(f"   新建列表: {', '.join(results['created'])}")
        if results["updated"]:
            print(f"   更新列表: {', '.join(results['updated'])}")
        if results["errors"]:
            print(f"   失败列表: {', '.join(results['errors'])}")

    # 步骤4: 设置关联关系
    if args.relation or args.sync or args.force:
        # Refresh name_map after creation
        if not dry_run:
            pages = query_all_pages()
            page_index = build_page_index(pages)
            name_map = build_persona_name_map(page_index)
        rel_results = setup_relations(page_index, name_map, dry_run)
        print(f"\n🔗 关联汇总: {rel_results['linked']} 个已关联, {rel_results['errors']} 个失败")

    print(f"\n{'🔍 预览完毕·加 --sync 执行同步' if dry_run else '✅ 同步完毕'}")
    print("=" * 60)

    return name_map


if __name__ == "__main__":
    name_map = main()
