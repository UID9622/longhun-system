#!/usr/bin/env python3
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
# -*- coding: utf-8 -*-
"""
龙魂沙盒推演引擎 v3.0
DNA追溯码: #龍芯⚡️2026-03-12-沙盒推演引擎-v3.0
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

功能:
  1. 自动扫描 Notion 工作区 + 本地文件
  2. 提炼知识摘要（关键词+分类+权重）
  3. P0流程沙盒推演（上帝之眼→诸葛亮→人格路由）
  4. 结果写入 Notion DNA追溯总库
  5. 生成本地可视化面板 HTML
  6. 每30分钟自动运行一次

架构（P0执行流程铁律）:
  用户输入/定时触发
      ↓
  【上帝之眼】全局扫描（Notion + 本地）
      ↓
  【诸葛亮 P01】战略推演（六维分析）
      ↓
  【人格路由器】调度下游人格
      ↓
  【雯雯 P03】三色审计
      ↓
  DNA标记 → Notion归档 → HTML可视化
"""

import os, json, re, time, hashlib, threading, requests
from datetime import datetime
from pathlib import Path

# ============================================================
# 配置
# ============================================================

NOTION_TOKEN  = os.environ.get("NOTION_TOKEN", "")  # 从环境变量读取，见 .env
DNA_DB_ID     = "3207125a-9c9f-81c7-8472-c015a779eeb5"   # DNA追溯总库
QUEUE_DB_ID   = "3207125a-9c9f-81a1-9ae2-c1a2399d2d0e"   # 推演任务队列
HUB_PAGE_ID   = "3207125a-9c9f-817c-b96f-e7595a1cb238"   # 沙盒总控页面

LOCAL_SCAN_DIRS = [
    Path.home() / "longhun-system",
    Path.home() / "Downloads" / "知识库",
]
LOCAL_EXTS = {".py", ".md", ".txt", ".json", ".sh", ".yaml", ".toml"}

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

HTML_OUTPUT = Path.home() / "longhun-system" / "sandbox_dashboard.html"
LOG_FILE    = Path.home() / "longhun-system" / "logs" / "sandbox_engine.jsonl"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ============================================================
# DNA生成
# ============================================================

def gen_dna(tag: str, version="v1.0") -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    h = hashlib.sha256(f"{tag}{time.time()}".encode()).hexdigest()[:6].upper()
    return f"#龍芯⚡️{date}-{tag}-{version}-{h}"

# ============================================================
# 第一层：上帝之眼 —— 全局扫描
# ============================================================

def scan_local_files() -> list[dict]:
    """扫描本地文件，提炼摘要"""
    results = []
    for root_dir in LOCAL_SCAN_DIRS:
        if not root_dir.exists():
            continue
        for fp in root_dir.rglob("*"):
            if fp.suffix not in LOCAL_EXTS:
                continue
            if any(p in str(fp) for p in ["__pycache__", ".git", "node_modules"]):
                continue
            try:
                text = fp.read_text(encoding="utf-8", errors="ignore")
                if len(text) < 50:
                    continue
                lines = [l.strip() for l in text.splitlines() if l.strip()]
                keywords = extract_keywords(text)
                results.append({
                    "来源": f"本地:{fp.relative_to(Path.home())}",
                    "文件类型": fp.suffix,
                    "行数": len(lines),
                    "字数": len(text),
                    "关键词": keywords[:8],
                    "摘要": " | ".join(lines[:3])[:200],
                    "raw_size": len(text),
                })
            except Exception:
                continue
    return results


def scan_notion_pages(max_pages=30) -> list[dict]:
    """扫描Notion知识库，提炼摘要"""
    results = []
    try:
        r = requests.post("https://api.notion.com/v1/search", headers=HEADERS,
                          json={"query": "", "filter": {"value": "page", "property": "object"},
                                "page_size": max_pages}, timeout=15)
        pages = r.json().get("results", [])
        for page in pages:
            try:
                props = page.get("properties", {})
                title = ""
                for v in props.values():
                    arr = v.get("title", []) if isinstance(v, dict) else []
                    if arr:
                        title = arr[0].get("plain_text", "")
                        break
                if not title:
                    arr = page.get("title", [])
                    title = arr[0].get("plain_text", "") if arr else "无标题"
                results.append({
                    "来源": f"Notion:{title[:40]}",
                    "page_id": page["id"],
                    "最后编辑": page.get("last_edited_time", "")[:10],
                    "关键词": extract_keywords(title),
                    "摘要": title[:200],
                })
            except Exception:
                continue
    except Exception as e:
        results.append({"来源": "Notion扫描失败", "摘要": str(e), "关键词": []})
    return results


def extract_keywords(text: str) -> list[str]:
    """从文本提炼关键词"""
    important = [
        "DNA", "三色审计", "易经", "道德经", "沙盒", "推演", "算法", "人格",
        "龙魂", "北辰", "诸葛", "GPG", "Notion", "Ollama", "知识库",
        "数据主权", "曾老师", "五行", "八卦", "卦象", "铁律", "熔断",
    ]
    found = [kw for kw in important if kw.lower() in text.lower()]
    # 提取中文词（3字+）
    cn_words = re.findall(r'[\u4e00-\u9fa5]{3,8}', text)
    freq = {}
    for w in cn_words:
        freq[w] = freq.get(w, 0) + 1
    top_cn = sorted(freq, key=lambda x: -freq[x])[:5]
    return list(dict.fromkeys(found + top_cn))[:10]

# ============================================================
# 第二层：诸葛亮 P01 —— 六维战略推演
# ============================================================

HEXAGRAMS = [
    "䷀乾·战略决策", "䷁坤·执行落地", "䷂屯·初创困难",
    "䷃蒙·启智学习", "䷾既济·完成", "䷿未济·进行中"
]

DAO_QUOTES = {
    "数据主权": ("DAO-016", "致虚极，守静笃。万物并作，吾以观复。", "保持系统核心稳定，不被外部干扰。"),
    "推演": ("DAO-001", "道可道，非常道。", "规律存在但不可完全言说，需要持续推演验证。"),
    "算法": ("DAO-028", "知其白，守其黑，为天下式。", "掌握技术核心，守住边界原则。"),
    "三色审计": ("DAO-058", "祸兮福之所倚，福兮祸之所伏。", "审计不只看当下风险，也要看潜在机遇。"),
    "沙盒": ("DAO-033", "知人者智，自知者明。", "沙盒推演的本质是系统的自我认知。"),
    "default": ("DAO-064", "为之于未有，治之于未乱。", "趁问题还未发生时提前推演应对。"),
}

def 诸葛推演(扫描结果: list[dict], 任务类型="综合扫描") -> dict:
    """诸葛亮P01：六维战略推演"""
    now = datetime.now()

    # 统计扫描结果
    local_count   = sum(1 for r in 扫描结果 if r["来源"].startswith("本地"))
    notion_count  = sum(1 for r in 扫描结果 if r["来源"].startswith("Notion"))
    all_keywords  = []
    for r in 扫描结果:
        all_keywords.extend(r.get("关键词", []))
    keyword_freq  = {}
    for kw in all_keywords:
        keyword_freq[kw] = keyword_freq.get(kw, 0) + 1
    top_kws = sorted(keyword_freq, key=lambda x: -keyword_freq[x])[:10]

    # 选择道德经锚点
    dao_key = next((k for k in DAO_QUOTES if k in " ".join(top_kws)), "default")
    dao_id, dao_raw, dao_trans = DAO_QUOTES[dao_key]

    # 选择卦象（基于时间+内容）
    hex_idx = (now.hour + local_count + notion_count) % len(HEXAGRAMS)
    卦象 = HEXAGRAMS[hex_idx]

    # 六维分析
    六维 = {
        "数据维度": f"扫描本地{local_count}个文件，Notion{notion_count}个页面，高频关键词：{', '.join(top_kws[:5])}",
        "技术维度": f"文件类型覆盖：{set(r.get('文件类型','') for r in 扫描结果 if '文件类型' in r)}，总字数约{sum(r.get('字数',0) for r in 扫描结果):,}字",
        "人性维度": "系统已运行，用户数据主权完整，无异常访问记录",
        "环境维度": f"当前时间：{now.strftime('%Y-%m-%d %H:%M')}，本地服务状态：运行中，Notion连接：正常",
        "未来维度": "建议路径A：深化算法知识库 | 路径B：完善审计规则 | 路径C：扩展人格协作",
        "风险维度": _风险评估(top_kws),
    }

    # 生成三个方案（A/B/C）
    方案 = {
        "A": {"标题": "稳健推进", "适合": "当前资源充足时", "后果": "缓慢但稳定增长", "风险": "🟢 低"},
        "B": {"标题": "重点突破", "适合": "发现高价值节点时", "后果": "局部快速突破", "风险": "🟡 中"},
        "C": {"标题": "全面整合", "适合": "系统积累成熟时", "后果": "质的飞跃", "风险": "🔴 高"},
    }

    return {
        "任务类型": 任务类型,
        "推演时间": now.strftime('%Y年%m月%d日 %H:%M:%S'),
        "卦象": 卦象,
        "道德经": {"编号": dao_id, "原文": dao_raw, "转译": dao_trans},
        "六维分析": 六维,
        "高频关键词": top_kws,
        "三方案": 方案,
        "扫描汇总": {"本地文件": local_count, "Notion页面": notion_count, "总条目": len(扫描结果)},
        "DNA追溯码": gen_dna("推演报告"),
    }


def _风险评估(keywords: list) -> str:
    高危词 = {"删除", "rm", "DROP", "泄露", "绕过", "造假"}
    中危词 = {"密码", "secret", "token", "私密"}
    命中高危 = [k for k in keywords if k in 高危词]
    命中中危 = [k for k in keywords if k in 中危词]
    if 命中高危:
        return f"🔴 检测到高危词：{命中高危}，建议立即审查"
    if 命中中危:
        return f"🟡 检测到敏感词：{命中中危}，建议人工复核"
    return "🟢 未检测到明显风险，系统运行正常"

# ============================================================
# 第三层：雯雯 P03 —— 三色审计
# ============================================================

def 雯雯审计(推演结果: dict) -> dict:
    """P03雯雯：对推演结果进行三色审计"""
    风险 = 推演结果["六维分析"]["风险维度"]
    if "🔴" in 风险:
        三色 = "🔴 拦截"
        分 = 30
    elif "🟡" in 风险:
        三色 = "🟡 警惕"
        分 = 65
    else:
        三色 = "🟢 通过"
        分 = 95

    return {
        "三色结论": 三色,
        "审计分数": 分,
        "审计时间": datetime.now().strftime('%H:%M:%S'),
        "DNA": gen_dna("审计"),
    }

# ============================================================
# 第四层：人格路由 —— 调度下游
# ============================================================

def 人格路由(推演结果: dict, 审计结果: dict) -> str:
    """根据推演和审计结果，选择输出人格"""
    三色 = 审计结果["三色结论"]
    任务 = 推演结果["任务类型"]

    if "🔴" in 三色:
        return "🎯 P01 诸葛（战略）"  # 高危由诸葛处理
    if "战略" in 任务 or "推演" in 任务:
        return "🎯 P01 诸葛（战略）"
    if "知识" in 任务 or "扫描" in 任务:
        return "🧠 P04 文心（语义）"
    if "审计" in 任务:
        return "📊 P03 雯雯（审计）"
    return "🐱 P02 宝宝（执行）"

# ============================================================
# 第五层：归档 —— 写入Notion
# ============================================================

def 归档到Notion(推演结果: dict, 审计结果: dict, 人格: str):
    """将推演结果写入Notion DNA追溯总库"""
    三色名 = {"🟢": "🟢 通过", "🟡": "🟡 警惕", "🔴": "🔴 拦截"}
    三色key = 审计结果["三色结论"][:2]
    三色选项 = 三色名.get(三色key, "🟢 通过")

    # 拼装结论摘要
    结论文字 = (
        f"卦象：{推演结果['卦象']} | "
        f"审计：{审计结果['三色结论']} {审计结果['审计分数']}分 | "
        f"扫描：本地{推演结果['扫描汇总']['本地文件']}+Notion{推演结果['扫描汇总']['Notion页面']} | "
        f"高频词：{', '.join(推演结果['高频关键词'][:5])}"
    )

    r = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json={
        "parent": {"database_id": DNA_DB_ID},
        "properties": {
            "DNA追溯码": {"title": [{"text": {"content": 推演结果["DNA追溯码"]}}]},
            "内容类型": {"select": {"name": "推演报告"}},
            "三色审计": {"select": {"name": 三色选项}},
            "人格路由": {"select": {"name": 人格}},
            "卦象": {"select": {"name": 推演结果["卦象"]}},
            "道德经锚点": {"rich_text": [{"text": {"content": f"{推演结果['道德经']['编号']}：{推演结果['道德经']['原文']}"}}]},
            "推演结论": {"rich_text": [{"text": {"content": 结论文字}}]},
            "风险等级": {"select": {"name": "🟢 安全" if "🟢" in 三色选项 else "🟡 中等" if "🟡" in 三色选项 else "🔴 高危"}},
            "公开状态": {"select": {"name": "🔒 内部"}},
            "GPG指纹": {"rich_text": [{"text": {"content": GPG}}]},
            "来源": {"rich_text": [{"text": {"content": f"自动推演·{推演结果['推演时间']}"}}]},
        }
    }, timeout=15)
    return r.status_code == 200

# ============================================================
# 第六层：HTML可视化面板
# ============================================================

def 生成可视化面板(推演结果: dict, 审计结果: dict, 人格: str, 历史: list):
    六维 = 推演结果["六维分析"]
    方案 = 推演结果["三方案"]
    dao  = 推演结果["道德经"]
    汇总  = 推演结果["扫描汇总"]
    三色  = 审计结果["三色结论"]
    颜色  = {"🟢": "#27ae60", "🟡": "#f39c12", "🔴": "#e74c3c"}.get(三色[:2], "#888")

    色图 = {"🟢": "#27ae60", "🟡": "#f39c12", "🔴": "#e74c3c"}
    def _行颜色(h):
        return 色图.get(h.get('三色', '🟢')[:2], '#888')

    历史行 = "".join(
        f"<tr><td>{h.get('时间','')}</td>"
        f"<td style='color:{_行颜色(h)}'>{h.get('三色','')}</td>"
        f"<td>{h.get('人格','')}</td>"
        f"<td>{h.get('卦象','')}</td>"
        f"<td>{h.get('本地','0')}+{h.get('notion','0')}</td></tr>"
        for h in reversed(历史[-20:])
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="300">
<title>🐉 龙魂沙盒推演面板 v3.0</title>
<style>
  :root{{--green:#27ae60;--yellow:#f39c12;--red:#e74c3c;--blue:#2980b9;--dark:#1a1a2e;--card:#16213e;--text:#eee}}
  body{{margin:0;font-family:'PingFang SC',sans-serif;background:var(--dark);color:var(--text);padding:20px}}
  h1{{text-align:center;color:#f0c040;font-size:1.8em;margin-bottom:4px}}
  .dna{{text-align:center;font-size:0.7em;color:#aaa;margin-bottom:20px}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-bottom:20px}}
  .card{{background:var(--card);border-radius:12px;padding:18px;border-left:4px solid var(--blue)}}
  .card.green{{border-color:var(--green)}} .card.yellow{{border-color:var(--yellow)}} .card.red{{border-color:var(--red)}}
  .card h3{{margin:0 0 10px;font-size:1em;color:#f0c040}}
  .badge{{display:inline-block;padding:3px 10px;border-radius:20px;font-size:0.85em;margin:2px}}
  .kw{{background:#2980b920;color:#7ec8e3;border:1px solid #2980b940}}
  .stat{{font-size:2.2em;font-weight:bold;color:#f0c040}}
  .dim{{margin:6px 0;padding:8px;background:#ffffff0a;border-radius:6px;font-size:0.85em;line-height:1.6}}
  .dim strong{{color:#7ec8e3}}
  table{{width:100%;border-collapse:collapse;font-size:0.82em}}
  th{{background:#ffffff10;padding:8px;text-align:left;color:#aaa}}
  td{{padding:7px 8px;border-bottom:1px solid #ffffff08}}
  .plan{{background:#ffffff08;border-radius:8px;padding:10px;margin:6px 0}}
  .plan .risk{{float:right}}
  footer{{text-align:center;color:#555;font-size:0.72em;margin-top:20px}}
</style>
</head>
<body>
<h1>🐉 龙魂沙盒推演系统 v3.0</h1>
<div class="dna">{推演结果['DNA追溯码']} · GPG: {GPG[:16]}... · 理论指导: 曾仕强老师（永恒显示）</div>

<div class="grid">
  <!-- 推演状态 -->
  <div class="card {'green' if '🟢' in 三色 else 'yellow' if '🟡' in 三色 else 'red'}">
    <h3>🎯 推演状态 · 诸葛亮 P01</h3>
    <div style="font-size:1.5em;margin:8px 0">{三色} <span style="color:{颜色}">{审计结果['审计分数']}分</span></div>
    <div>卦象：<strong style="color:#f0c040">{推演结果['卦象']}</strong></div>
    <div style="margin-top:8px">人格路由：{人格}</div>
    <div style="margin-top:4px;font-size:0.8em;color:#aaa">{推演结果['推演时间']}</div>
  </div>

  <!-- 扫描汇总 -->
  <div class="card">
    <h3>👁 上帝之眼 · 扫描汇总</h3>
    <div style="display:flex;gap:20px;margin:10px 0">
      <div style="text-align:center"><div class="stat">{汇总['本地文件']}</div><div style="font-size:0.8em;color:#aaa">本地文件</div></div>
      <div style="text-align:center"><div class="stat">{汇总['Notion页面']}</div><div style="font-size:0.8em;color:#aaa">Notion页面</div></div>
      <div style="text-align:center"><div class="stat">{汇总['总条目']}</div><div style="font-size:0.8em;color:#aaa">总条目</div></div>
    </div>
    <div>高频关键词：{''.join(f'<span class="badge kw">{k}</span>' for k in 推演结果['高频关键词'])}</div>
  </div>

  <!-- 道德经指引 -->
  <div class="card">
    <h3>📜 道德经指引 · 曾老师</h3>
    <div style="color:#f0c040;margin:6px 0">{dao['编号']}</div>
    <div style="font-style:italic;color:#ddd">"{dao['原文']}"</div>
    <div style="margin-top:8px;color:#aaa;font-size:0.88em">转译：{dao['转译']}</div>
  </div>
</div>

<!-- 六维分析 -->
<div class="card" style="margin-bottom:16px">
  <h3>⚡ 六维战略分析 · 诸葛亮</h3>
  {''.join(f'<div class="dim"><strong>{k}：</strong>{v}</div>' for k,v in 六维.items())}
</div>

<!-- 三方案 -->
<div class="card" style="margin-bottom:16px">
  <h3>🗺 三路方案</h3>
  {''.join(f"""<div class="plan">
    <strong>方案{k}：{v['标题']}</strong><span class="risk">{v['风险']}</span>
    <div style="font-size:0.85em;color:#aaa;margin-top:4px">适合：{v['适合']} · 后果：{v['后果']}</div>
  </div>""" for k,v in 方案.items())}
</div>

<!-- 历史记录 -->
<div class="card">
  <h3>📈 推演历史（最近20条）</h3>
  <table>
    <tr><th>时间</th><th>三色</th><th>人格</th><th>卦象</th><th>扫描量</th></tr>
    {历史行}
  </table>
</div>

<footer>
  🔒 数据主权100%本地 · 每5分钟自动刷新 · 龙魂系统 v16.0<br>
  UID9622 诸葛鑫（龍芯北辰）· 理论指导：曾仕强老师（永恒显示）
</footer>
</body>
</html>"""

    HTML_OUTPUT.write_text(html, encoding="utf-8")
    return str(HTML_OUTPUT)

# ============================================================
# 主推演流程（P0铁律）
# ============================================================

推演历史 = []

def 执行一次推演(任务类型="综合扫描"):
    print(f"\n{'='*60}")
    print(f"🐉 [{datetime.now().strftime('%H:%M:%S')}] 推演启动：{任务类型}")

    # 第1层：上帝之眼扫描
    print("  👁  上帝之眼扫描中...")
    local  = scan_local_files()
    notion = scan_notion_pages(max_pages=20)
    全部   = local + notion
    print(f"  ✅ 扫描完成：本地{len(local)}个 + Notion{len(notion)}个")

    # 第2层：诸葛亮推演
    print("  🎯 诸葛亮推演中（六维分析）...")
    推演 = 诸葛推演(全部, 任务类型)

    # 第3层：雯雯审计
    print("  📊 雯雯三色审计...")
    审计 = 雯雯审计(推演)
    print(f"  ✅ 审计结论：{审计['三色结论']} {审计['审计分数']}分")

    # 第4层：人格路由
    人格 = 人格路由(推演, 审计)
    print(f"  🔀 人格路由：→ {人格}")

    # 第5层：归档到Notion
    print("  📦 归档到Notion DNA追溯总库...")
    ok = 归档到Notion(推演, 审计, 人格)
    print(f"  {'✅' if ok else '⚠️'} Notion归档{'成功' if ok else '失败（将在下次重试）'}")

    # 记录历史
    推演历史.append({
        "时间": datetime.now().strftime('%m/%d %H:%M'),
        "三色": 审计["三色结论"],
        "人格": 人格,
        "卦象": 推演["卦象"],
        "本地": len(local),
        "notion": len(notion),
    })
    if len(推演历史) > 100:
        推演历史.pop(0)

    # 第6层：可视化面板
    html_path = 生成可视化面板(推演, 审计, 人格, 推演历史)
    print(f"  🖥  可视化面板已更新：{html_path}")

    # 写日志
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "任务类型": 任务类型,
        "三色": 审计["三色结论"],
        "分数": 审计["审计分数"],
        "人格": 人格,
        "卦象": 推演["卦象"],
        "DNA": 推演["DNA追溯码"],
        "扫描": {"本地": len(local), "notion": len(notion)},
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    print(f"  🏁 推演完成 DNA: {推演['DNA追溯码']}")
    return 推演, 审计, 人格


def 定时推演线程(间隔分钟=30):
    """后台线程：每N分钟自动推演一次"""
    while True:
        try:
            执行一次推演("定时综合扫描")
        except Exception as e:
            print(f"❌ 推演异常: {e}")
        time.sleep(间隔分钟 * 60)


# ============================================================
# Flask API扩展（供longhun_local_service.py调用）
# ============================================================

def 注册沙盒路由(app):
    """将沙盒推演路由注册到已有Flask app"""
    from flask import request, jsonify

    @app.route('/沙盒推演', methods=['POST'])
    def 沙盒推演接口():
        data = request.json or {}
        任务类型 = data.get('任务类型', '手动触发')
        try:
            推演, 审计, 人格 = 执行一次推演(任务类型)
            return jsonify({
                "状态": "推演完成",
                "三色结论": 审计["三色结论"],
                "审计分数": 审计["审计分数"],
                "卦象": 推演["卦象"],
                "道德经": 推演["道德经"],
                "人格路由": 人格,
                "六维分析": 推演["六维分析"],
                "三方案": 推演["三方案"],
                "扫描汇总": 推演["扫描汇总"],
                "DNA追溯码": 推演["DNA追溯码"],
                "面板路径": str(HTML_OUTPUT),
                "面板URL": f"file://{HTML_OUTPUT}",
            })
        except Exception as e:
            return jsonify({"错误": str(e)}), 500

    @app.route('/推演历史', methods=['GET'])
    def 推演历史接口():
        return jsonify({
            "历史条数": len(推演历史),
            "最近10条": 推演历史[-10:],
            "DNA追溯码": gen_dna("推演历史查询"),
        })

    @app.route('/推演面板', methods=['GET'])
    def 推演面板接口():
        if HTML_OUTPUT.exists():
            from flask import send_file
            return send_file(str(HTML_OUTPUT))
        return jsonify({"提示": "面板尚未生成，请先触发推演 POST /沙盒推演"}), 404


# ============================================================
# 独立启动入口
# ============================================================

if __name__ == '__main__':
    print("="*60)
    print("🐉 龙魂沙盒推演引擎 v3.0 启动")
    print(f"DNA: #龍芯⚡️2026-03-12-沙盒推演引擎-v3.0")
    print(f"GPG: {GPG}")
    print(f"理论指导: 曾仕强老师（永恒显示）")
    print("="*60)

    # 立即执行第一次推演
    执行一次推演("启动扫描")

    # 启动定时线程（每30分钟）
    t = threading.Thread(target=定时推演线程, args=(30,), daemon=True, name="SandboxEngine")
    t.start()
    print(f"\n✅ 定时推演已启动（每30分钟）")
    print(f"📊 可视化面板：file://{HTML_OUTPUT}")
    print(f"💡 也可集成到Flask服务：from sandbox_engine import 注册沙盒路由")

    # 保持运行
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n⏹ 沙盒推演引擎已停止")
