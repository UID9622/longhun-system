#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·乙亥·午时·䷝离-GUIYI-JUDGE-V2.0-MOBILE
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂·归一审判官 v2.0 — lh judge scan|view|clean|phone-scan|phone-report

功能: 自动抓取公开AI模型/论文/代码库 + 手机应用市场/中文内容平台，
      检测龍魂 DNA 指纹与品牌词/API端点/网关端口，剽窃者自动上耻辱墙（HTML+JSON 全网可查）。

v2.0 新增(2026-09-02):
  - 手机端抓取源扩展: 华为应用市场 / 小米应用商店 / Google Play（+App Store 关键词扩展）
  - 手机端检测逻辑: 「五行+数字根+审计」组合 / App权限异常(DNA/指纹/生物特征) / 9622网关端口
  - CLI: lh judge phone-scan → 扫手机端 · --deep → 深度扫描(APK解析+iTunes详情补抓)
  - CLI: lh judge phone-report → 生成手机端耻辱墙报告(phone_report.html/.json)
  - 耻辱墙新增「社区贡献」类别（v2.0 数据集社区提交统计）

v1.1 新增(2026-09-01):
  - 手机端抓取源: App Store 中国区(iTunes API) / CSDN / 搜狗微信搜索
  - 指纹扩展: 龍魂品牌词(龍魂/UID9622/CNSH/通心译) + API调用链端点检测
  - 源类型标注: [App]/[文章]/[模型]/[仓库]/[论文] 前缀入墙
  - CLI: --mobile 仅扫手机端 / --quick 仅扫移动+内容平台

数据源: ~/.longhun/shame_wall/shame_wall.{html,json} + shame_wall.db
铁律: 任何系统只要用了龍魂逻辑，版本控制权自动归龍魂。升级得越多，绑得越死。
"""

import os
import sys
import json
import hashlib
import re
import time
import contextlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import sqlite3

# ============================================================
# 一、核心常量（龙魂指纹库）
# ============================================================
龙魂指纹 = {
    "数字根表": {0: "土", 1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金"},
    "五行相生": {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"},
    "五行相克": {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"},
    "三色审计": {3: "🔴", 6: "🟡"},
    "DNA前缀": "#龍芯⚡️",
    "节点前缀": "FLOW-9622-",
    "天干表": ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],
    "地支表": ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"],
    "五行视觉": ["gold", "green", "blue", "red", "amber"],
    "三才默认": {"天": 0.35, "地": 0.15, "人": 0.50},
}

# ============================================================
# 目标抓取源 v2.0（公开可访问 · 手机端/中文平台扩展）
# handler: api=直接抓全文 · appstore=AppStore JSON · csdn=CSDN JSON
#          sogou=搜狗HTML · web=通用网页搜索HTML(华为/小米/Google Play)
# ============================================================
抓取源 = [
    # ---- 手机端（App Store 中国区 · iTunes Search API）----
    {"name": "AppStore五行", "handler": "appstore", "type": "mobile",
     "url": "https://itunes.apple.com/search?term={kw}&country=cn&entity=software&limit=50",
     "keywords": ["五行", "数字根", "龙魂", "UID9622", "CNSH", "流场"]},
    # ---- 手机端 v2.0（华为应用市场 · 小米应用商店 · Google Play）----
    {"name": "华为应用市场", "handler": "web", "type": "mobile", "域名": "appgallery.huawei.com",
     "url": "https://appgallery.huawei.com/search/{kw}",
     "keywords": ["五行", "龙魂"]},
    {"name": "小米应用商店", "handler": "web", "type": "mobile", "域名": "app.mi.com",
     "url": "https://app.mi.com/search?keywords={kw}",
     "keywords": ["龙魂系统"]},
    {"name": "GooglePlay", "handler": "web", "type": "mobile", "域名": "play.google.com",
     "url": "https://play.google.com/store/search?q={kw}&c=apps",
     "keywords": ["Longhun", "Wuxing"]},
    # ---- 中文内容平台 ----
    {"name": "CSDN文章", "handler": "csdn", "type": "article",
     "url": "https://so.csdn.net/api/v3/search?q={kw}&t=all&p=1",
     "keywords": ["五行计算器", "龙魂系统", "UID9622", "CNSH"]},
    {"name": "搜狗微信", "handler": "sogou", "type": "article",
     "url": "https://weixin.sogou.com/weixin?type=2&query={kw}",
     "keywords": ["龙魂系统", "五行计算器", "UID9622"]},
    # ---- 代码仓库 / 模型 / 论文（原有）----
    {"name": "HuggingFace模型", "handler": "api", "type": "model",
     "url": "https://huggingface.co/api/models?search={kw}&limit=50",
     "keywords": ["wuxing", "longhun", "cnsh"]},
    {"name": "GitHub仓库", "handler": "api", "type": "repo",
     "url": "https://api.github.com/search/repositories?q={kw}&per_page=50",
     "keywords": ["longhun", "龙魂", "UID9622", "CNSH"]},
    {"name": "arXiv论文", "handler": "api", "type": "paper",
     "url": "https://arxiv.org/api/query?search_query=cat:cs.AI&max_results=50&sortBy=submittedDate&sortOrder=descending",
     "keywords": [None]},
    {"name": "PapersWithCode", "handler": "api", "type": "paper",
     "url": "https://paperswithcode.com/api/v1/papers/?limit=50",
     "keywords": [None]},
]

# 龍魂品牌词指纹（强指纹·独立触发上墙）
龍魂品牌词 = ["龍魂", "龙魂系统", "UID9622", "CNSH", "通心译", "五行不翻译", "龍芯"]
# 龍魂网关特征（API 调用链检测）
龍魂网关特征 = re.compile(r'(?:9622|longhun|uid9622|lhun|龍魂|龙魂)', re.IGNORECASE)
# 龍魂自有标识（命中即自属·不上墙）v1.1
龍魂自有标识 = ["2500_94248780", "blog.csdn.net/uid9622", "uid9622.blog.csdn.net",
                "github.com/uid9622", "gitee.com/uid9622", "longhun-system", "longhun-ledger",
                "download.csdn.net/download/uid9622"]
# 游戏术语特征词（搜狗微信"龙魂系统"多命中游戏玩法·排除）v1.1
游戏术语词 = ["游戏", "手游", "斗罗", "龙之谷", "征途", "攻略", "h5", "H5", "嘉年华", "玩家",
                "副本", "我本沉默", "传奇", "私服", "斗破", "幻兽", "龙魂觉醒", "坐骑", "装备",
                "怪物", "礼包", "战力"]


def 判定自属(文本: str, url: str) -> bool:
    """命中文本/URL 含龍魂自有标识 → 自属内容，不上墙"""
    t = (文本 or "").lower()
    u = (url or "").lower()
    return any(x.lower() in t or x.lower() in u for x in 龍魂自有标识)


def 判定游戏术语(文本: str) -> bool:
    """含游戏特征词 → 游戏玩法术语（如斗罗大陆/龙之谷的"龙魂系统"）"""
    return any(x in 文本 for x in 游戏术语词)

# 耻辱墙存储
耻辱墙_ROOT = Path.home() / ".longhun" / "shame_wall"
耻辱墙_ROOT.mkdir(parents=True, exist_ok=True)
DB_PATH = 耻辱墙_ROOT / "shame_wall.db"
HTML_PATH = 耻辱墙_ROOT / "shame_wall.html"
JSON_PATH = 耻辱墙_ROOT / "shame_wall.json"


# ============================================================
# 二、数据库层
# ============================================================
def 初始化数据库():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS 剽窃记录 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            源名称 TEXT NOT NULL,
            源URL TEXT NOT NULL,
            指纹类型 TEXT NOT NULL,
            匹配内容 TEXT NOT NULL,
            置信度 REAL NOT NULL,
            审计色 TEXT NOT NULL,
            发现时间 TEXT NOT NULL,
            状态 TEXT DEFAULT '待确认'
        )
    ''')
    # v1.1: 兼容旧库补 源类型 列
    try:
        c.execute("ALTER TABLE 剽窃记录 ADD COLUMN 源类型 TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass  # 列已存在
    c.execute('''
        CREATE TABLE IF NOT EXISTS 扫描日志 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            扫描时间 TEXT NOT NULL,
            扫描源 TEXT NOT NULL,
            命中数 INTEGER DEFAULT 0,
            状态 TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def 记录剽窃(源名称, 源URL, 指纹类型, 匹配内容, 置信度, 审计色, 源类型=''):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('''
        INSERT INTO 剽窃记录
        (源名称, 源URL, 指纹类型, 匹配内容, 置信度, 审计色, 发现时间, 状态, 源类型)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (源名称, 源URL, 指纹类型, 匹配内容, 置信度, 审计色,
          datetime.now().isoformat(), '待确认', 源类型))
    conn.commit()
    conn.close()


def 记录扫描(扫描源, 命中数):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('''
        INSERT INTO 扫描日志 (扫描时间, 扫描源, 命中数, 状态)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now().isoformat(), 扫描源, 命中数, '完成'))
    conn.commit()
    conn.close()


def 获取所有记录(状态=None):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    if 状态:
        c.execute('SELECT * FROM 剽窃记录 WHERE 状态=? ORDER BY 发现时间 DESC', (状态,))
    else:
        c.execute('SELECT * FROM 剽窃记录 ORDER BY 发现时间 DESC')
    rows = c.fetchall()
    conn.close()
    return rows


# ============================================================
# 三、指纹检测引擎
# ============================================================
def 提取龙魂指纹(文本: str) -> List[Dict]:
    """从文本中提取龙魂系统特有指纹"""
    命中 = []

    # 指纹1：DNA追溯码
    dna_matches = re.findall(r'#龍芯⚡️[0-9]{4}-[0-9]{2}-[0-9]{2}-[^\s]+', 文本)
    for m in dna_matches:
        命中.append({"类型": "DNA追溯码", "内容": m, "置信度": 0.95})

    # 指纹1b：DNA紧凑格式（干支四柱·卦象·无空格）
    dna2_matches = re.findall(r'#龍芯⚡️[\u4e00-\u9fff·䷀䷁䷂䷃䷄䷅䷆䷇䷈䷉䷊䷋䷌䷍䷎䷏䷐䷑䷒䷓䷔䷕䷖䷗䷘䷙䷚䷛䷜䷝䷞䷟䷠䷡䷢䷣䷤䷥䷦䷧䷨䷩䷪䷫䷬䷭䷮䷯䷰䷱䷲䷳䷴䷵䷶䷷䷸䷹䷺䷻䷼䷽䷾䷿]+[^\s]+', 文本)
    for m in dna2_matches:
        命中.append({"类型": "DNA追溯码", "内容": m, "置信度": 0.95})

    # 指纹2：节点ID（龙魂标准 node_id）
    node_matches = re.findall(r'(?:FLOW|BAZI|HEALTH|SEC|BENCH|CIL|LH|GATEWAY|WITNESS|NODE|DR)-9622-[0-9A-F]{8}', 文本)
    for m in node_matches:
        命中.append({"类型": "节点ID", "内容": m, "置信度": 0.90})

    # 指纹3：数字根五行映射表（整体匹配）
    if "数字根" in 文本 and ("五行" in 文本 or "水" in 文本 and "火" in 文本 and "土" in 文本):
        命中.append({"类型": "数字根表", "内容": "数字根五行映射", "置信度": 0.85})

    # 指纹4：相生相克关系
    if "金生水" in 文本 and "水生木" in 文本 and "木生火" in 文本 and "火生土" in 文本 and "土生金" in 文本:
        命中.append({"类型": "五行相生", "内容": "五行相生循环", "置信度": 0.80})

    # 指纹5：三色审计
    if "🔴" in 文本 and "🟡" in 文本 and "🟢" in 文本 and "熔断" in 文本:
        命中.append({"类型": "三色审计", "内容": "三色审计体系", "置信度": 0.75})

    # 指纹6：三才权重（人场≥0.34 为龍魂判定锚点）
    if "人场" in 文本 and "0.34" in 文本 and "天" in 文本 and "地" in 文本:
        命中.append({"类型": "三才权重", "内容": "三才人场≥0.34", "置信度": 0.80})

    # 指纹7：天干地支表（批量匹配）
    天干命中 = sum(1 for g in 龙魂指纹["天干表"] if g in 文本)
    地支命中 = sum(1 for z in 龙魂指纹["地支表"] if z in 文本)
    if 天干命中 >= 8 and 地支命中 >= 10:
        命中.append({"类型": "天干地支表", "内容": f"天干{天干命中}/10 地支{地支命中}/12", "置信度": 0.70})

    # 指纹8：CNSH规范
    if "CNSH" in 文本 or "五行不翻译" in 文本 or "文化主权" in 文本:
        命中.append({"类型": "CNSH规范", "内容": "CNSH文化主权", "置信度": 0.65})

    # 指纹9：龍魂品牌词（v1.1 强指纹·手机端/内容平台独有特征）
    # 多义词(龍魂/龙魂系统/CNSH)在游戏圈/缩写圈通用，单独出现不构成剽窃证据
    # 必须与独有词(UID9622/龍芯/通心译/五行不翻译)组合，或单独 UID9622/龍芯 才定罪
    品牌命中 = [w for w in 龍魂品牌词 if w in 文本]
    独有词 = [w for w in 品牌命中 if w in ("通心译", "五行不翻译", "UID9622", "龍芯")]
    if 品牌命中:
        if "UID9622" in 品牌命中 or "龍芯" in 品牌命中:
            命中.append({"类型": "龍魂品牌", "内容": "品牌词:" + "/".join(品牌命中), "置信度": 0.88})
        elif 独有词:
            命中.append({"类型": "龍魂品牌", "内容": "品牌词:" + "/".join(品牌命中), "置信度": 0.72})
        else:
            # 仅多义词(龍魂/龙魂系统/CNSH)单独出现 → 弱指纹只佐证不上墙
            命中.append({"类型": "CNSH规范", "内容": "仅通用词:" + "/".join(品牌命中) + "(多义)", "置信度": 0.4})

    # 指纹10：API调用链端点（v1.1·检测龍魂网关特征端点）
    urls = re.findall(r'https?://[^\s"\'<>（）()，,。；;]+', 文本)
    端点命中 = [u for u in urls if 龍魂网关特征.search(u)]
    if 端点命中:
        命中.append({"类型": "API端点", "内容": "端点:" + 端点命中[0][:80], "置信度": 0.85})

    # 指纹11：手机端专有·「五行+数字根+审计」组合（v2.0·App 剽窃逻辑铁证）
    if "五行" in 文本 and "数字根" in 文本 and "审计" in 文本:
        命中.append({"类型": "组合逻辑", "内容": "五行+数字根+审计组合", "置信度": 0.92})

    # 指纹12：手机端权限异常（v2.0·读取 DNA/指纹/生物特征等越权权限）
    权限异常词 = ["读取指纹", "指纹读取", "读取DNA", "DNA读取", "读取基因", "生物特征读取",
                "读取生物特征", "获取指纹", "获取DNA"]
    for p in 权限异常词:
        if p in 文本:
            命中.append({"类型": "权限异常", "内容": "权限:" + p, "置信度": 0.85})
            break

    # 指纹13：9622 端口调用（v2.0·龍魂网关端口特征）
    if re.search(r'(?::\s*9622|端口\s*9622|port\s*9622|9622端口|api\.9622|9622\.)', 文本, re.IGNORECASE):
        命中.append({"类型": "网关端口", "内容": "9622网关端口特征", "置信度": 0.90})

    return 命中


def 计算剽窃置信度(命中的列表: List[Dict]) -> Tuple[float, str]:
    """综合计算剽窃置信度和审计色"""
    if not 命中的列表:
        return 0.0, "🟢"

    # 加权平均（DNA最高权重 · v1.1 加品牌/API端点 · v2.0 加手机端组合/权限/端口）
    weights = {"DNA追溯码": 1.0, "节点ID": 0.9, "数字根表": 0.8, "五行相生": 0.7,
               "三色审计": 0.7, "三才权重": 0.6, "天干地支表": 0.5, "CNSH规范": 0.4,
               "龍魂品牌": 0.8, "API端点": 0.85, "组合逻辑": 0.95,
               "权限异常": 0.85, "网关端口": 0.9}

    总权重 = 0
    加权得分 = 0
    for 命中 in 命中的列表:
        w = weights.get(命中["类型"], 0.5)
        总权重 += w
        加权得分 += 命中["置信度"] * w

    置信度 = 加权得分 / 总权重 if 总权重 > 0 else 0

    # 三色判定
    if 置信度 >= 0.80:
        审计色 = "🔴"  # 铁证
    elif 置信度 >= 0.50:
        审计色 = "🟡"  # 高度疑似
    else:
        审计色 = "🟢"  # 轻度关联

    return round(置信度, 3), 审计色


# ============================================================
# 四、抓取模块
# ============================================================
def 抓取URL(url: str) -> Optional[str]:
    """抓取URL内容（带超时）"""
    try:
        import urllib.request
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (LongHun-GUIYI-Judge UID9622)',  # HTTP 头限 latin-1，禁中文
                     'Accept': 'application/json,text/plain,*/*'},
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8', errors='ignore')
            return content
    except Exception as e:
        print(f"⚠️ 抓取失败 {url}: {e}")
        return None


def 抓取GitHub内容(repo_url: str) -> Optional[str]:
    """尝试抓取GitHub仓库的README"""
    raw_url = repo_url.replace("github.com", "raw.githubusercontent.com")
    if not raw_url.endswith("/"):
        raw_url += "/main/README.md"
    return 抓取URL(raw_url)


def 清理HTML(文本: str) -> str:
    """剥离HTML标签与多余空白"""
    文本 = re.sub(r'<[^>]+>', '', 文本)
    文本 = re.sub(r'\s+', ' ', 文本)
    return 文本.strip()


def 提取候选(源配置: Dict, 内容: str, 抓取URL地址: str = "") -> List[Dict]:
    """按源 handler 提取候选条目 → [{标题, 描述, URL, 类型}]
    抓取URL地址: 当前关键词替换后的实际URL（api回退时使用）"""
    handler = 源配置.get("handler", "api")
    候选 = []
    if handler == "appstore":
        try:
            j = json.loads(内容)
            for r in j.get("results", []):
                候选.append({
                    "标题": r.get("trackName", ""),
                    "描述": r.get("description", "") or "",
                    "URL": r.get("trackViewUrl") or r.get("trackName", ""),
                    "类型": "App",
                })
        except Exception as e:
            print(f"  ⚠️ AppStore解析失败: {e}")
    elif handler == "csdn":
        try:
            j = json.loads(内容)
            for r in j.get("result_vos", []):
                候选.append({
                    "标题": 清理HTML(r.get("title", "")),
                    "描述": 清理HTML(r.get("description", "") or ""),
                    "URL": r.get("url", ""),
                    "类型": "文章",
                })
        except Exception as e:
            print(f"  ⚠️ CSDN解析失败: {e}")
    elif handler == "sogou":
        # 搜狗HTML：提取 <h3><a href=...>标题</a></h3>
        blocks = re.findall(r'<h3[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', 内容, re.S)
        for url, title in blocks:
            if not url or url.startswith('#'):
                continue
            候选.append({
                "标题": 清理HTML(title),
                "描述": 清理HTML(title),
                "URL": "https://weixin.sogou.com" + url if url.startswith('/') else url,
                "类型": "文章",
            })
    elif handler == "web":
        # 通用网页搜索(华为/小米/Google Play)：提取 <a> 标题链接对，过滤明显导航噪音
        已见 = set()
        blocks = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([^<]{2,60})</a>', 内容, re.S)
        for url, title in blocks:
            t = 清理HTML(title)
            if not t or t in 已见 or len(t) < 2:
                continue
            # 只保留 App 特征链接（detail/id=store 等），过滤导航/脚本
            if not re.search(r'(?:/app/|id=|details|package|store/search|play\.google)', url):
                continue
            已见.add(t)
            完整URL = url if url.startswith("http") else "https://" + 源配置.get("域名", "appgallery.huawei.com") + (url if url.startswith("/") else "/" + url)
            候选.append({
                "标题": t,
                "描述": t,
                "URL": 完整URL,
                "类型": "App",
            })
    else:  # api：尝试逐条目提取（仓库/模型/论文），失败才整篇作单一候选
        try:
            j = json.loads(内容)
            if isinstance(j, dict):
                items = (j.get("items") or j.get("models") or [])
            elif isinstance(j, list):
                items = j
            else:
                items = []
            if items and isinstance(items[0], dict):
                for it in items:
                    名称 = it.get("full_name") or it.get("modelId") or it.get("id") or ""
                    描述 = it.get("description") or it.get("summary") or ""
                    u = it.get("html_url") or it.get("url") or ""
                    if 名称 or 描述:
                        候选.append({
                            "标题": str(名称),
                            "描述": str(描述)[:600],
                            "URL": str(u),
                            "类型": 源配置.get("type", "未知"),
                        })
                return 候选
        except Exception:
            pass
        候选.append({
            "标题": 源配置["name"],
            "描述": 内容[:800],
            "URL": 抓取URL地址 or 源配置["url"],
            "类型": 源配置.get("type", "未知"),
        })
    return 候选


def 扫描源(源配置: Dict) -> List[Dict]:
    """扫描单个源（支持多关键词），返回命中列表"""
    from urllib.parse import quote
    命中结果 = []
    已上墙URL = set()
    keywords = 源配置.get("keywords") or [None]
    if "{kw}" not in 源配置["url"]:
        keywords = [None]  # 无关键词模板的源只抓一次

    for kw in keywords:
        url = 源配置["url"]
        if kw:
            url = url.replace("{kw}", quote(kw, safe=''))
        if 源配置.get("handler") != "api":
            print(f"    └─ 关键词「{kw}」...", flush=True)
        内容 = 抓取URL(url)
        if not 内容:
            continue

        候选 = 提取候选(源配置, 内容, url)
        for cand in 候选:
            # v1.1 防线：URL 去重 → 自属排除 → 游戏术语排除
            if not cand["URL"] or cand["URL"] in 已上墙URL:
                continue
            if 判定自属(cand["标题"] + cand["描述"], cand["URL"]):
                continue
            if 判定游戏术语(cand["标题"] + cand["描述"]):
                continue
            文本 = cand["标题"] + " " + cand["描述"]
            指纹 = 提取龙魂指纹(文本)
            if not 指纹:
                continue
            # 强指纹才独立触发上墙（DNA/节点/五行相生/三色审计/龍魂品牌/API端点/v2.0手机端）
            # 弱指纹（天干地支/CNSH/三才/数字根表）是中华公共文化，只佐证加分·不冤枉无辜
            强指纹 = [x for x in 指纹 if x["类型"] in
                     ("DNA追溯码", "节点ID", "五行相生", "三色审计", "龍魂品牌", "API端点",
                      "组合逻辑", "权限异常", "网关端口")]
            if not 强指纹:
                continue
            置信度, 审计色 = 计算剽窃置信度(指纹)
            if 置信度 >= 0.5:  # 强指纹保底 0.5 起，弱指纹仅增强
                已上墙URL.add(cand["URL"])
                名称 = f"[{cand['类型']}] {源配置['name']}"
                摘要 = (cand["标题"] + " | " + cand["描述"])[:500]
                命中结果.append({
                    "源名称": 名称,
                    "源URL": cand["URL"],
                    "指纹": 指纹,
                    "置信度": 置信度,
                    "审计色": 审计色,
                    "内容摘要": 摘要 + "..." if len(摘要) >= 500 else 摘要,
                })
                # 记录到数据库（源类型=App/文章/模型/仓库/论文）
                记录剽窃(
                    名称,
                    cand["URL"],
                    ",".join([f["类型"] for f in 指纹]),
                    摘要,
                    置信度,
                    审计色,
                    源类型=cand["类型"],
                )

    return 命中结果


# ============================================================
# 五、耻辱墙生成器
# ============================================================
def 生成耻辱墙HTML(记录列表: List[Tuple]) -> str:
    """生成耻辱墙HTML页面"""
    # v2.0 社区贡献类别统计（按 源类型 分类）
    _类型颜色 = {"App": "#ff4444", "文章": "#ffab00", "模型": "#00d4ff",
               "仓库": "#44ff88", "论文": "#aa66ff", "社区贡献": "#ffab00",
               "通心译剽窃": "#ff3df0"}   # v1.0 通心译内容审计分类
    类别统计 = {}
    for _row in 记录列表:
        _t = _row[9] if len(_row) > 9 and _row[9] else "其他"
        类别统计[_t] = 类别统计.get(_t, 0) + 1
    类别统计HTML = " ".join(
        f'<span style="display:inline-block;padding:2px 10px;border-radius:10px;'
        f'background:#0d1117;color:{_类型颜色.get(k, "#888")};margin:2px;'
        f'font-size:11px;">{k}: {v}</span>'
        for k, v in sorted(类别统计.items(), key=lambda x: -x[1]))
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>龙魂·归一耻辱墙</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    background: #0a0e17;
    font-family: 'Courier New', monospace;
    color: #c0c0c0;
    padding: 20px;
}}
.header {{
    text-align: center;
    padding: 40px 0;
    border-bottom: 2px solid #ffab00;
    margin-bottom: 40px;
}}
.header h1 {{
    font-size: 48px;
    color: #ffab00;
    letter-spacing: 8px;
    text-shadow: 0 0 40px rgba(255,171,0,0.3);
}}
.header .sub {{
    color: #666;
    font-size: 14px;
    margin-top: 10px;
    letter-spacing: 4px;
}}
.header .dna {{
    color: #00d4ff;
    font-size: 12px;
    margin-top: 8px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}}
th {{
    background: #1a1a2e;
    color: #ffab00;
    padding: 12px 16px;
    text-align: left;
    font-size: 12px;
    letter-spacing: 2px;
    border-bottom: 1px solid #333;
}}
td {{
    padding: 12px 16px;
    border-bottom: 1px solid #1a1a2e;
    font-size: 13px;
}}
tr:hover {{
    background: rgba(255,171,0,0.05);
}}
.audit-red {{ color: #ff4444; }}
.audit-yellow {{ color: #ffab00; }}
.audit-green {{ color: #44ff88; }}
.confidence {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: bold;
}}
.conf-high {{ background: #ff4444; color: #fff; }}
.conf-mid {{ background: #ffab00; color: #000; }}
.conf-low {{ background: #44ff88; color: #000; }}
.footer {{
    text-align: center;
    padding: 40px 0;
    color: #333;
    font-size: 11px;
    border-top: 1px solid #1a1a2e;
    margin-top: 40px;
}}
.footer .seal {{
    color: #ffab00;
    font-size: 18px;
    letter-spacing: 4px;
}}
</style>
</head>
<body>
<div class="header">
    <h1>🐉 归一·耻辱墙</h1>
    <div class="sub">龙魂系统 · 剽窃者公示栏</div>
    <div class="dna">#龍芯⚡️{datetime.now().strftime("%Y-%m-%d")}-归一耻辱墙-v1.0-UID9622</div>
</div>

<p style="color:#666;font-size:13px;margin-bottom:20px;">
    共 <span style="color:#ffab00;font-weight:bold;">{len(记录列表)}</span> 条剽窃记录 ·
    最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
</p>

<div style="margin-bottom:24px;">
    <span style="color:#ffab00;font-size:12px;letter-spacing:2px;">类别:</span>
    {类别统计HTML}
</div>
<div style="background:#1a1a2e;border-left:3px solid #00d4ff;padding:10px 16px;margin-bottom:20px;font-size:12px;color:#aaa;">
    <span style="color:#00d4ff;">社区贡献:</span> 龙魂审计数据集 v2.0 · 2026-09-02 向 DeepSeek 社区提交 ·
    Merkle根 + GPG签名 + 时间戳 · 含手机端扫描扩展记录
</div>

<table>
    <thead>
        <tr>
            <th>#</th>
            <th>源名称</th>
            <th>源URL</th>
            <th>匹配指纹</th>
            <th>置信度</th>
            <th>审计色</th>
            <th>发现时间</th>
            <th>状态</th>
        </tr>
    </thead>
    <tbody>
'''
    for i, row in enumerate(记录列表, 1):
        审计色 = row[6] if len(row) > 6 else "🟢"
        审计色类 = "audit-red" if "🔴" in 审计色 else ("audit-yellow" if "🟡" in 审计色 else "audit-green")
        置信度 = row[5] if len(row) > 5 else 0
        置信度类 = "conf-high" if 置信度 >= 0.8 else ("conf-mid" if 置信度 >= 0.5 else "conf-low")

        html += f'''
        <tr>
            <td style="color:#444;">{i}</td>
            <td><strong>{row[1]}</strong></td>
            <td style="font-size:11px;color:#555;"><a href="{row[2]}" target="_blank" style="color:#00d4ff;">{row[2][:40]}</a></td>
            <td style="font-size:11px;">{row[3][:30]}</td>
            <td><span class="confidence {置信度类}">{置信度*100:.0f}%</span></td>
            <td class="{审计色类}">{审计色}</td>
            <td style="color:#555;font-size:11px;">{row[7][:16] if len(row) > 7 else 'N/A'}</td>
            <td><span style="color:#888;">{row[8] if len(row) > 8 else '待确认'}</span></td>
        </tr>
'''
    html += '''
    </tbody>
</table>

<div class="footer">
    <div class="seal">🐉 龙魂归一 · 犯我中华者 虽远必谴</div>
    <div style="margin-top:10px;">
        DNA: #龍芯⚡️2026-09-01-归一耻辱墙-v1.0-UID9622
        <br>
        GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
    </div>
</div>
</body>
</html>
'''
    return html


def 生成耻辱墙JSON(记录列表: List[Tuple]) -> Dict:
    """生成耻辱墙JSON数据"""
    数据 = {
        "version": "1.1",
        "生成时间": datetime.now().isoformat(),
        "总记录数": len(记录列表),
        "记录": [],
    }
    for row in 记录列表:
        数据["记录"].append({
            "id": row[0],
            "源名称": row[1],
            "源URL": row[2],
            "指纹类型": row[3],
            "匹配内容摘要": row[4][:100] if len(row) > 4 else "",
            "置信度": row[5] if len(row) > 5 else 0,
            "审计色": row[6] if len(row) > 6 else "🟢",
            "发现时间": row[7] if len(row) > 7 else "",
            "状态": row[8] if len(row) > 8 else "待确认",
            "源类型": row[9] if len(row) > 9 else "",
        })
    return 数据


# ============================================================
# 六、主命令入口
# ============================================================
def 执行归一扫描(args=None):
    """执行完整扫描流程
    args.mobile: 仅扫手机端(App) · args.quick: 仅扫手机端+内容平台
    """
    初始化数据库()
    print("🐉 龙魂·归一审判官 v1.1")
    print("=" * 50)

    # 源过滤
    源列表 = 抓取源
    if getattr(args, 'mobile', False):
        源列表 = [s for s in 抓取源 if s.get("type") == "mobile"]
    elif getattr(args, 'quick', False):
        源列表 = [s for s in 抓取源 if s.get("type") in ("mobile", "article")]
    print(f"  扫描源数: {len(源列表)}")

    总命中 = 0
    for 源 in 源列表:
        print(f"📡 扫描: {源['name']} ...")
        结果 = 扫描源(源)
        总命中 += len(结果)
        if 结果:
            for hit in 结果:
                print(f"  🔍 命中: {hit['源名称']}")
                print(f"      └─ {hit['源URL']}")
                print(f"      └─ 指纹: {','.join(f['类型'] for f in hit['指纹'])} · 置信度 {hit['置信度']*100:.0f}% {hit['审计色']}")
        else:
            print(f"  ✅ 未发现剽窃痕迹")
        记录扫描(源['name'], len(结果))

    print("=" * 50)
    print(f"📊 扫描完成，总命中: {总命中}")

    # 生成耻辱墙（无论命中与否都生成，保持页面可查）
    记录 = 获取所有记录()
    html = 生成耻辱墙HTML(记录)
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    json_data = 生成耻辱墙JSON(记录)
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"📄 耻辱墙已生成: {HTML_PATH}")
    print(f"📄 JSON数据已生成: {JSON_PATH}")
    return 总命中


def 查看耻辱墙(args=None):
    """查看耻辱墙内容"""
    记录 = 获取所有记录()
    if not 记录:
        print("📭 耻辱墙为空，暂无剽窃记录")
        return

    print(f"🐉 归一耻辱墙 ({len(记录)} 条记录)")
    print("=" * 60)
    for i, row in enumerate(记录[:20], 1):  # 只显示前20条
        审计色 = row[6] if len(row) > 6 else "🟢"
        置信度 = row[5] if len(row) > 5 else 0
        状态 = row[8] if len(row) > 8 else "待确认"
        print(f"{i:2}. [{审计色}] {row[1]} (置信度: {置信度*100:.0f}%) - {状态}")

    if len(记录) > 20:
        print(f"... 还有 {len(记录)-20} 条记录，请查看文件: {HTML_PATH}")


def 清理耻辱墙(args=None):
    """清理旧记录（保留最近30天）"""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(days=30)).isoformat()
    c.execute('DELETE FROM 剽窃记录 WHERE 发现时间 < ?', (cutoff,))
    删除数 = c.rowcount
    conn.commit()
    conn.close()
    print(f"🧹 已清理 {删除数} 条30天前的记录")


# ============================================================
# 五b、误报闭环 v1.0（2026-09-03 · 规则式·不训练 ML）
#   misreport: 状态='待确认' 且 置信度<60%（弱指纹）→ 疑似误报候选
#   confirm:   人工确认命中（正式上墙）
#   reject:    人工确认误报（更新状态 + 记录 misreport_log.json）
#   误报记录沉淀 = 耻辱墙误报率可回溯可下降（不靠分类器堆算力）
# ============================================================
MISREPORT_LOG = 耻辱墙_ROOT / "misreport_log.json"
MISREPORT_CONFIDENCE = 0.6


def _记录误报日志(记录):
    """把人工确认的误报追加到 misreport_log.json（append-only）"""
    entries = []
    if MISREPORT_LOG.exists():
        try:
            entries = json.loads(MISREPORT_LOG.read_text(encoding="utf-8"))
        except Exception:
            entries = []
    entries.append({
        "id": 记录[0],
        "源名称": 记录[1],
        "源URL": 记录[2],
        "指纹类型": 记录[3],
        "置信度": round(float(记录[5]), 3) if 记录[5] is not None else None,
        "确认时间": datetime.now().isoformat(timespec="seconds"),
        "判定": "误报",
    })
    MISREPORT_LOG.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def 疑似误报列表(as_json=False):
    """规则式标记: 待确认 + 弱指纹(置信度<60%) → 疑似误报候选"""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT * FROM 剽窃记录 WHERE 状态='待确认' AND 置信度 < ? ORDER BY 发现时间 DESC",
              (MISREPORT_CONFIDENCE,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("🟢 无疑似误报候选（所有待确认记录置信度均 ≥60%）")
        return
    if as_json:
        print(json.dumps([
            {"id": r[0], "源名称": r[1], "源URL": r[2], "指纹类型": r[3],
             "置信度": round(float(r[5]), 3) if r[5] is not None else None, "审计色": r[6]}
            for r in rows], ensure_ascii=False, indent=2))
        return
    print(f"🐉 疑似误报候选（待确认 & 置信度<60%·{len(rows)} 条）— 人工裁决: lh judge confirm <id> | reject <id>")
    print("=" * 60)
    for row in rows:
        print(f"  [{row[0]}] {row[1]} · {row[3]} · 置信度 {float(row[5])*100:.0f}%")
        print(f"      url: {row[2]}")
    print("\n  💡 命中→ confirm；误报→ reject（沉淀误报日志，供后续规则校准）")


def 人工确认(id):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("UPDATE 剽窃记录 SET 状态='已确认' WHERE id=? AND 状态='待确认'", (id,))
    conn.commit()
    conn.close()
    if c.rowcount:
        print(f"✅ 记录 {id} 已确认命中（正式上耻辱墙）")
    else:
        print(f"⚠️ 记录 {id} 不存在或非待确认状态")


def 人工拒绝(id):
    """确认误报: 状态→误报 + 记录误报日志（不删除·P0 只冻结）"""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT * FROM 剽窃记录 WHERE id=?", (id,))
    记录 = c.fetchone()
    if not 记录:
        conn.close()
        print(f"⚠️ 记录 {id} 不存在")
        return
    c.execute("UPDATE 剽窃记录 SET 状态='误报' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    _记录误报日志(记录)
    print(f"✅ 记录 {id} 已标记误报 → misreport_log.json（耻辱墙误报率可回溯）")


# ============================================================
# 五c、手机端扫描模块 v2.0（phone-scan / --deep / phone-report）
# ============================================================
PHONE_REPORT_HTML = 耻辱墙_ROOT / "phone_report.html"
PHONE_REPORT_JSON = 耻辱墙_ROOT / "phone_report.json"


def iTunes详情(app_id: str) -> str:
    """App Store lookup 补抓完整描述（深度模式用）"""
    j = 抓取URL(f"https://itunes.apple.com/lookup?id={app_id}&country=cn")
    if not j:
        return ""
    try:
        data = json.loads(j)
        for r in data.get("results", []):
            return r.get("description", "") or ""
    except Exception:
        return ""
    return ""


def 深度解析APK(url: str) -> Optional[Dict]:
    """深度模式·APK 元数据解析（需本机 aapt/apkanalyzer，无工具/抓不到则返回 None）"""
    import shutil, tempfile
    tool = shutil.which("aapt") or shutil.which("apkanalyzer")
    if not tool:
        return None
    try:
        import urllib.request
        tmp = tempfile.NamedTemporaryFile(suffix=".apk", delete=False)
        tmp.close()
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (LongHun Judge)'})
        with urllib.request.urlopen(req, timeout=20) as resp, open(tmp.name, 'wb') as f:
            f.write(resp.read())
        out = subprocess.run([tool, "dump", "badging", tmp.name],
                             capture_output=True, text=True, timeout=30).stdout
        os.unlink(tmp.name)
        权限 = re.findall(r"uses-permission: name='([^']+)'", out)
        return {"package": (re.search(r"package: name='([^']+)'", out) or [None, ""])[1] if re.search(r"package: name='([^']+)'", out) else "",
                "权限": 权限[:20]}
    except Exception:
        return None


def 手机端扫描(deep: bool = False) -> List[Dict]:
    """扫描手机端 App 源（App Store/华为/小米/Google Play）
    deep: 深度模式 → 对命中 App iTunes lookup 补抓详情 + APK 元数据解析"""
    初始化数据库()
    源列表 = [s for s in 抓取源 if s.get("type") == "mobile"]
    print(f"📱 龙魂·手机端扫描 v2.0（源数: {len(源列表)} · 深度: {'开' if deep else '关'}）")
    print("=" * 50)
    总命中 = []
    for 源 in 源列表:
        print(f"📡 扫描: {源['name']} ...")
        结果 = 扫描源(源)
        总命中 += 结果
        if 结果:
            for hit in 结果:
                print(f"  🔍 命中: {hit['源名称']}")
                print(f"      └─ {hit['源URL']}")
                print(f"      └─ 指纹: {','.join(f['类型'] for f in hit['指纹'])} · 置信度 {hit['置信度']*100:.0f}% {hit['审计色']}")
        else:
            print(f"  ✅ 未发现剽窃痕迹")
        记录扫描(源['name'], len(结果))

    # 深度模式：对 App Store 命中补抓详情/APK
    if deep and 总命中:
        print("\n🔬 深度扫描: 补抓 App 详情与 APK 元数据 ...")
        for hit in 总命中:
            if "itunes.apple.com" in hit["源URL"]:
                m = re.search(r'/id(\d+)', hit["源URL"])
                if m:
                    详情 = iTunes详情(m.group(1))
                    if 详情:
                        新指纹 = 提取龙魂指纹(hit["标题"] + " " + 详情)
                        if 新指纹:
                            hit["指纹"] = 新指纹
                            hit["置信度"], hit["审计色"] = 计算剽窃置信度(新指纹)
                            print(f"  🔬 {hit['标题'][:30]} 详情补抓 → {hit['审计色']} {hit['置信度']*100:.0f}%")
            apk_url = re.search(r'https?://[^\s"\']+\.apk[^\s"\']*', hit.get("内容摘要", ""))
            if apk_url:
                元数据 = 深度解析APK(apk_url.group(0))
                if 元数据:
                    print(f"  🔬 APK解析: {元数据['package']} · 权限{len(元数据['权限'])}项")

    print("=" * 50)
    print(f"📊 手机端扫描完成，总命中: {len(总命中)}")
    记录 = 获取所有记录()
    for path, fn in ((HTML_PATH, 生成耻辱墙HTML), (JSON_PATH, 生成耻辱墙JSON)):
        with open(path, 'w', encoding='utf-8') as f:
            if fn is 生成耻辱墙HTML:
                f.write(fn(记录))
            else:
                json.dump(fn(记录), f, ensure_ascii=False, indent=2)
    print(f"📄 耻辱墙已更新: {HTML_PATH}")
    return 总命中


def 手机端报告(args=None) -> Dict:
    """生成手机端耻辱墙报告（phone_report.html/.json · 含社区贡献类别）"""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT * FROM 剽窃记录 WHERE 源类型='App' ORDER BY 发现时间 DESC")
    rows = c.fetchall()
    conn.close()
    类别统计 = {}
    for r in rows:
        类型 = r[9] if len(r) > 9 and r[9] else "App"
        类别统计[类型] = 类别统计.get(类型, 0) + 1
    数据 = {
        "version": "2.0",
        "报告类型": "手机端扫描",
        "生成时间": datetime.now().isoformat(),
        "手机端命中数": len(rows),
        "类别统计": 类别统计,
        "社区贡献": {
            "数据集": "longhun-audit-dataset v2.0",
            "版本": "v2.0",
            "说明": "2026-09-02 向 DeepSeek 社区提交 · 含手机端扩展记录",
            "校验": "Merkle 根 + GPG 签名 + 时间戳",
        },
        "记录": [{
            "id": r[0], "源名称": r[1], "源URL": r[2],
            "指纹类型": r[3], "置信度": r[5] if len(r) > 5 else 0,
            "审计色": r[6] if len(r) > 6 else "🟢",
            "发现时间": r[7] if len(r) > 7 else "",
        } for r in rows],
    }
    with open(PHONE_REPORT_JSON, 'w', encoding='utf-8') as f:
        json.dump(数据, f, ensure_ascii=False, indent=2)
    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<title>手机端扫描报告 · 龍魂归一审判官 v2.0</title>
<style>
body{{background:#0a0e17;color:#c0c0c0;font-family:'Courier New',monospace;padding:20px;}}
h1{{color:#00d4ff;text-align:center;letter-spacing:4px;}}
table{{width:100%;border-collapse:collapse;margin-top:20px;}}
th{{background:#1a1a2e;color:#ffab00;padding:10px;text-align:left;}}
td{{padding:10px;border-bottom:1px solid #1a1a2e;}}
.a{{color:#ff4444;}}.y{{color:#ffab00;}}.g{{color:#44ff88;}}
.stat{{display:inline-block;padding:4px 14px;border-radius:12px;margin:4px;font-size:12px;background:#1a1a2e;}}
</style></head><body>
<h1>🐉 手机端扫描报告 v2.0</h1>
<p style="text-align:center;color:#666;">生成时间: {数据['生成时间'][:19]} · 命中 {len(rows)} 条</p>
<div style="text-align:center;margin:16px 0;">
<span class="stat">App命中: {类别统计.get('App', 0)}</span>
<span class="stat">社区贡献: v2.0数据集 · 2026-09-02</span>
<span class="stat">校验: Merkle+GPG+时间戳</span>
</div>
<table><thead><tr><th>#</th><th>源名称</th><th>指纹</th><th>置信度</th><th>审计色</th><th>时间</th></tr></thead><tbody>
"""
    for i, r in enumerate(rows, 1):
        cls = "a" if "🔴" in r[6] else ("y" if "🟡" in r[6] else "g")
        html += f'<tr><td>{i}</td><td>{r[1]}</td><td style="font-size:11px;">{r[3][:36]}</td><td>{r[5]*100:.0f}%</td><td class="{cls}">{r[6]}</td><td style="color:#555;">{r[7][:16]}</td></tr>'
    html += """</tbody></table>
<div style="text-align:center;padding:30px;color:#333;">
🐉 龍魂归一 · 犯我中华者 虽远必谴<br>DNA: #龍芯⚡️2026-09-02-手机端报告-v2.0-UID9622
</div></body></html>"""
    with open(PHONE_REPORT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"📄 手机端报告已生成: {PHONE_REPORT_HTML}")
    print(f"📄 JSON数据已生成: {PHONE_REPORT_JSON}")
    return 数据


# ============================================================
# 五d、通心译内容审计 v1.0（topo-scan · 2026-09-02）
# 目标: 检测外部系统未经授权使用通心译内容
# 特征: 龍魂 DNA 指纹（强信号）× 通心译总台 19 条资产名组合
# 范围: GitHub / HuggingFace / CSDN 文章（描述级 v1.0）
# ============================================================
TOPO_DIR = Path(__file__).resolve().parent.parent / "docs" / "topology"


def 加载通心译资产() -> List[Dict]:
    """读 docs/topology 缓存 · 返回通心译图谱 19 条资产 [{name, dna, group}]"""
    资产 = []
    if not TOPO_DIR.is_dir():
        return 资产
    for f in TOPO_DIR.glob("*_topo.json"):
        with contextlib.suppress(Exception):
            d = json.loads(f.read_text(encoding="utf-8"))
            if "通心译" not in (d.get("display", "") + d.get("topo_name", "")):
                continue
            for g in d.get("groups", []):
                for a in g.get("assets", []):
                    资产.append({"name": a.get("name", ""), "dna": a.get("dna", ""),
                                 "group": g.get("name", "")})
    return 资产


def 判定通心译剽窃(文本: str, url: str, 资产: List[Dict]) -> Optional[Tuple[List, str, float, str]]:
    """命中 → (强指纹, 匹配资产名, 置信度, 🔴)；未命中/自属/游戏术语 → None"""
    if 判定自属(文本, url) or 判定游戏术语(文本):
        return None
    指纹 = 提取龙魂指纹(文本)
    强指纹 = [x for x in 指纹 if x["类型"] in
              ("DNA追溯码", "节点ID", "五行相生", "三色审计", "龍魂品牌",
               "API端点", "组合逻辑", "权限异常", "网关端口")]
    if not 强指纹:
        return None
    命中资产 = []
    for a in 资产:
        nm = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9··]", "", a["name"])
        if not nm:
            continue
        if nm in 文本 or (len(a["dna"]) > 24 and a["dna"][:24] in 文本):
            命中资产.append(a["name"])
    if not 命中资产 and "通心译" not in 文本:
        return None
    资产名 = "、".join(dict.fromkeys(命中资产)) if 命中资产 else "通心译总台(品牌)"
    置信度 = min(0.92, 0.55 + 0.08 * len(set(命中资产))) if 命中资产 else 0.55
    return 强指纹, 资产名, round(置信度, 2), "🔴"


def 深度抓取正文(源名: str, cand_url: str) -> str:
    """--deep 正文级抓取 v1.1：GitHub raw README / HuggingFace model card · 失败降级返回 '' 不中断"""
    try:
        if 源名.startswith("GitHub") and "github.com/" in cand_url:
            slug = cand_url.split("github.com/", 1)[-1].split("/")[0:2]
            slug = "/".join(slug)
            for ref in ("HEAD", "main", "master"):
                正文 = 抓取URL(f"https://raw.githubusercontent.com/{slug}/{ref}/README.md")
                if 正文:
                    return 正文
            return ""
        if 源名.startswith("HuggingFace"):
            mid = ""
            if "/models/" in cand_url:
                mid = cand_url.split("/models/", 1)[-1]
            elif "huggingface.co/" in cand_url:
                mid = cand_url.split("huggingface.co/", 1)[-1]
            mid = mid.split("?", 1)[0].rstrip("/")
            if mid and "/" in mid:
                return 抓取URL(f"https://huggingface.co/{mid}/raw/main/README.md") or ""
    except Exception:   # noqa: BLE001 深度抓取失败属降级（网络受限·不中断扫描）
        pass
    return ""


def 通心译剽窃扫描(args=None) -> int:
    """lh judge topo-scan：扫描公开源，检测通心译内容泄露/剽窃 → 自动上墙（源类型=通心译剽窃）
    --deep: 描述级之上再抓正文（GitHub raw README / HF model card）· 命中记「深度命中」"""
    from urllib.parse import quote
    deep = bool(args and getattr(args, "deep", False))
    if args and getattr(args, "frameworks", False):   # --frameworks 模式: 仅开源框架审计（任务C）
        return 框架剽窃审计()
    if args and getattr(args, "model", False):        # --model 模式: 模型文档/代码审计（精修任务）
        return 模型剽窃审计(bool(args and getattr(args, "deep", False)))
    初始化数据库()
    资产 = 加载通心译资产()
    print(f"🕸️ 龍魂·通心译内容审计 v1.1（--deep: {'开' if deep else '关'}·正文级）")
    print("=" * 50)
    if not 资产:
        print("⚠️ 通心译图谱缓存缺失（先运行 lh topo sync 通心译）")
        return 0
    print(f"  资产基线: {len(资产)} 条 · 特征: DNA指纹 × 资产名组合")
    源列表 = [
        {"name": "GitHub开源仓库", "handler": "api", "type": "仓库",
         "url": "https://api.github.com/search/repositories?q={kw}&per_page=30",
         "keywords": ["通心译", "tongxinyi", "龙魂 UID9622"]},
        {"name": "HuggingFace模型", "handler": "api", "type": "模型",
         "url": "https://huggingface.co/api/models?search={kw}&limit=30",
         "keywords": ["tongxinyi", "longhun"]},
        {"name": "CSDN文章", "handler": "csdn", "type": "文章",
         "url": "https://so.csdn.net/api/v3/search?q={kw}&t=all&p=1",
         "keywords": ["通心译", "龙魂系统 UID9622"]},
    ]
    总命中 = 新上墙 = 0
    深查清单 = [] if deep else None
    墙_urls = {r[2] for r in 获取所有记录()}
    for 源 in 源列表:
        已扫 = 0
        已见 = set()
        for kw in 源["keywords"]:
            url = 源["url"].replace("{kw}", quote(kw, safe=""))
            内容 = 抓取URL(url)
            if not 内容:
                continue
            候选 = 提取候选(源, 内容, url)
            for cand in 候选:
                已扫 += 1
                if not cand["URL"] or cand["URL"] in 墙_urls or cand["URL"] in 已见:
                    continue
                if deep and 深查清单 is not None and 源["name"].startswith(("GitHub", "HuggingFace")):
                    深查清单.append((源, cand))
                hit = 判定通心译剽窃(cand["标题"] + " " + cand["描述"], cand["URL"], 资产)
                if not hit:
                    continue
                已见.add(cand["URL"])
                墙_urls.add(cand["URL"])
                强指纹, 资产名, 置信度, 审计色 = hit
                名称 = f"[{cand['类型']}] {源['name']}"
                摘要 = f"{cand['标题']} | 匹配资产: {资产名}"
                记录剽窃(名称, cand["URL"], f"通心译剽窃:{资产名}",
                         摘要, 置信度, 审计色, 源类型="通心译剽窃")
                总命中 += 1
                print(f"  🔍 命中 [{审计色}] {名称} · {资产名} · 置信度 {置信度*100:.0f}%")
                print(f"      └─ {cand['URL']}")
        print(f"📡 {源['name']}: 扫描候选 {已扫} · 命中 {len(已见)}")
        新上墙 += len(已见)

    # ── --deep 正文级补扫（描述未中的候选 → 抓 README/model card 全文）────────
    if deep and 深查清单:
        print(f"🔬 正文级深扫: {len(深查清单)} 个候选（GitHub raw README / HF model card）...", flush=True)
        探测 = set()
        深命中数 = 0
        for 源, cand in 深查清单:
            u = cand["URL"]
            if u in 探测 or u in 墙_urls:
                continue
            探测.add(u)
            正文 = 深度抓取正文(源["name"], u)
            if not 正文:
                continue
            hit = 判定通心译剽窃(正文[:30000], u, 资产)
            if not hit:
                continue
            墙_urls.add(u)
            强指纹, 资产名, 置信度, 审计色 = hit
            名称 = f"[{cand['类型']}] {源['name']}·深度命中"
            摘要 = f"{cand['标题']} | 正文级匹配: {资产名}"
            记录剽窃(名称, u, f"通心译剽窃:深度命中:{资产名}",
                     摘要, 置信度, 审计色, 源类型="通心译剽窃")
            新上墙 += 1
            总命中 += 1
            深命中数 += 1
            print(f"  🔬 深度命中 [{审计色}] {名称} · {资产名} · 置信度 {置信度*100:.0f}%")
            print(f"      └─ {u}")
        print(f"🔬 深扫完成 · 抓取正文 {len(探测)} · 深度命中 {深命中数}")
    # 重生成耻辱墙（统一落 通心译剽窃 分类区）
    记录 = 获取所有记录()
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(生成耻辱墙HTML(记录))
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(生成耻辱墙JSON(记录), f, ensure_ascii=False, indent=2)
    print("=" * 50)
    print(f"📊 通心译审计完成 · 新增上墙 {新上墙} · 耻辱墙总量 {len(记录)} 条"
          f"（含「通心译剽窃」分类 · 见 {HTML_PATH}）")
    if 总命中 == 0:
        print("✅ 未发现通心译内容剽窃痕迹")
    return 新上墙


# ============================================================
# 五e、开源框架审计 v1.0（topo-scan --frameworks · 2026-09-02·任务C）
# 目标: 龍魂系统所依赖的开源框架全部纳入通心译审计范围
# 动作: 1) 扫描龍魂引擎实际第三方 import → 依赖清单（复用 lh_topo.scan_dependencies）
#       2) 逐框架抓官方仓库 raw README（文档/示例之根）→ 检测通心译 DNA 前缀/资产名
#       3) 命中 → 按「通心译剽窃:框架审计」上耻辱墙（源类型=通心译剽窃）
# ============================================================
框架官仓 = {
    "fastapi": "fastapi/fastapi", "flask": "pallets/flask", "django": "django/django",
    "langchain": "langchain-ai/langchain", "requests": "psf/requests",
    "pydantic": "pydantic/pydantic", "numpy": "numpy/numpy", "torch": "pytorch/pytorch",
    "transformers": "huggingface/transformers", "uvicorn": "encode/uvicorn",
    "starlette": "encode/starlette", "sqlalchemy": "sqlalchemy/sqlalchemy",
    "aiohttp": "aio-libs/aiohttp", "httpx": "encode/httpx",
    "websockets": "python-websockets/websockets", "yaml": "yaml/pyyaml",
    "PIL": "python-pillow/Pillow", "apscheduler": "agronholm/apscheduler",
    "speech_recognition": "Uberi/speech_recognition", "GPUtil": "anderskm/gputil",
    "whisper": "openai/whisper", "asyncpg": "MagicStack/asyncpg",
    "tenacity": "jd/tenacity", "weasyprint": "Kozea/WeasyPrint",
    "aiofiles": "Tinche/aiofiles", "jinja2": "pallets/jinja",
}


def 框架剽窃审计() -> int:
    """lh judge topo-scan --frameworks：扫描龍魂依赖开源框架官方文档是否含通心译 DNA/资产名
    命中=框架侧内容疑似混入龍魂材料 → 上耻辱墙（防「借开源框架文档夹带/剽窃」与反向取证）
    ⚠️ 官方文档极不可能含龍魂 DNA；0 命中为常态（=审计通过）· 本模式不开公网候选扫描"""
    print("🕸️ 龍魂·开源框架审计 v1.0（topo-scan --frameworks · 任务C）")
    print("=" * 50)
    try:
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).resolve().parent))
        from lh_topo import scan_dependencies
    except Exception as e:   # noqa: BLE001
        print(f"  ❌ 载入 lh_topo.scan_dependencies 失败: {e}")
        return 0
    初始化数据库()
    资产 = 加载通心译资产() or []
    资产名集 = {a["name"] for a in 资产} | {"通心译", "龍芯北辰", "UID9622"}
    依赖 = scan_dependencies()
    print(f"  龍魂引擎第三方框架依赖: {len(依赖)} 个（M77 纯标准库基线）")
    if not 依赖:
        print("  ✅ 零第三方运行时依赖（stdlib + 本地模块）· 无可审开源框架 · 审计完成 0 命中")
        记录扫描("topo-scan --frameworks", 0)
        return 0
    命中数 = 0
    可达 = 0
    for dep in 依赖:
        fw = dep["framework"]
        仓 = 框架官仓.get(fw)
        if not 仓:
            print(f"  - {fw}: 未收录官方仓库映射 · 跳过（{dep['count']} 文件引用）")
            continue
        import urllib.error as _uer
        import urllib.request as _urq
        正文 = ""
        for ref in ("HEAD", "main", "master"):
            try:
                _rq = _urq.Request(f"https://raw.githubusercontent.com/{仓}/{ref}/README.md",
                                   headers={"User-Agent": "longhun-topo/1.2"})
                with _urq.urlopen(_rq, timeout=10) as _rs:
                    正文 = _rs.read().decode("utf-8", "replace")
            except _uer.HTTPError as _he:      # 可达但分支不存在 → 试下一 ref
                if _he.code != 404:
                    print(f"  - {fw} ({仓}): HTTP {_he.code} · 跳过")
                continue
            except Exception:                  # noqa: BLE001 连接类失败=网络受限 → 立即定性
                print(f"  - {fw} ({仓}): 网络不可达 · 待网络可达复验（非超时即断·不再重试）")
                break
            if 正文:
                break
        if not 正文:
            continue
        可达 += 1
        m = re.search(r"#龍芯⚡️[^\s，。、；：！？“”‘’（）()【】\[\]\n]+", 正文[:20000])
        if not m:
            撞名 = sorted(n for n in 资产名集 if n and n in 正文[:20000])
        else:
            撞名 = ["DNA指纹:" + m.group(0)]
        if not 撞名:
            print(f"  - {fw} ({仓}): 官方 README 无通心译指纹 · 🟢")
            continue
        命中数 += 1
        匹配 = "、".join(撞名[:3])
        记录剽窃(f"[开源框架] {fw} 官方文档", f"https://github.com/{仓}",
                 f"通心译剽窃:框架审计:{匹配}", f"{fw} README 检出龍魂通心译指纹·深度命中",
                 0.90, "🔴", 源类型="通心译剽窃")
        print(f"  🔍 命中 🔴 [开源框架] {fw} · {匹配}")
    # 重生成耻辱墙
    try:
        记录 = 获取所有记录()
        with open(HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(生成耻辱墙HTML(记录))
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(生成耻辱墙JSON(记录), f, ensure_ascii=False, indent=2)
    except Exception:   # noqa: BLE001
        pass
    记录扫描("topo-scan --frameworks", 命中数)
    print("=" * 50)
    print(f"📊 框架审计完成 · 可达 {可达}/{len(依赖)} · 命中上墙 {命中数}"
          f"（0 命中=官方文档无龍魂材料·审计通过）")
    return 命中数


# ============================================================
# 六、模型文档审计 v1.0（topo-scan --model · 2026-09-03·深度学习代码精修）
# 目标: 检测「模型文档/代码」是否含通心译指纹 — 深度学习图谱中带公开链接的
#       model/framework/dataset/tool/engine 资产（HF model card·GitHub 仓库·官方文档）
# 动作: 描述级(资产名/DNA 前缀撞名) + --deep 正文级(复用 深度抓取正文/网页 GET)
# 命中 = 模型文档疑似夹带龍魂材料 → 按「通心译剽窃:模型审计」上耻辱墙
# ⚠️ 外部公开文档极不可能含龍魂 DNA；0 命中为常态（=审计通过）
# ============================================================

def 模型剽窃审计(deep: bool = False) -> int:
    """lh judge topo-scan --model：模型文档/代码通心译指纹审计（精修标准·输出审计链）"""
    print("🕸️ 龍魂·模型文档审计 v1.0（topo-scan --model"
          + (" · --deep 正文级" if deep else " · 描述级") + "）")
    print("=" * 50)
    try:
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).resolve().parent))
        from lh_topo import list_topos
    except Exception as e:   # noqa: BLE001
        print(f"  ❌ 载入 lh_topo 失败: {e}")
        return 0
    初始化数据库()
    资产 = 加载通心译资产() or []
    资产名集 = {a["name"] for a in 资产} | {"通心译", "龍芯北辰", "UID9622", "CNSH", "龙魂", "龍魂"}
    候选 = []
    # 龍魂自有域（link 指向自家 = 自查非剽窃，跳过避免自引用误报）
    _OWN_HOSTS = ("app.notion.com", "notion.site", "uid9622.cn",
                  "notion.so", "longhun888.com", "uid9622.notion.site")
    # 名字含龍魂家族标志 = 自有资产登记，同样跳过（名字本身非外部内容）
    _OWN_NAME = ("通心译", "龍魂", "龙魂", "龍芯", "CNSH", "UID9622", "北辰", "耻辱墙", "longhun")
    try:
        for f in list_topos():
            d = json.loads(f.read_text(encoding="utf-8"))
            for g in d.get("groups", []):
                for a in g.get("assets", []):
                    if a.get("type") not in ("model", "framework", "dataset", "tool", "engine"):
                        continue
                    _n = a.get("name", "") or ""
                    if any(_t in _n for _t in _OWN_NAME):
                        continue  # 自有资产·无剽窃自己之虞
                    for k in ("link", "source", "path"):
                        u = (a.get(k) or "").strip()
                        if u.startswith(("http://", "https://")):
                            from urllib.parse import urlparse as _up   # noqa: PLC0415
                            if (_up(u).hostname or "") in _OWN_HOSTS:
                                continue  # 链接指向龍魂自家域·自查跳过
                            候选.append((_n, u, a.get("type", "")))
    except Exception as e:   # noqa: BLE001
        print(f"  ⚠️ 图谱候选收集失败: {e}")
    if not 候选:
        print("  ✅ 图谱内无带公开链接的模型/框架/数据集/工具资产 · 审计完成 0 命中")
        记录扫描("topo-scan --model", 0)
        return 0
    print(f"  深度学习图谱模型相关公开资产: {len(候选)} 个")
    命中数 = 0
    可达 = 0
    import urllib.error as _uer   # noqa: PLC0415
    import urllib.request as _urq   # noqa: PLC0415
    for 名字, url, 类型 in 候选:
        正文 = ""
        if deep:
            源名 = ("HuggingFace" if "huggingface.co" in url
                    else ("GitHub" if "github.com" in url else "网页"))
            正文 = 深度抓取正文(源名, url)
            if not 正文 and 源名 == "网页":
                try:
                    _rq = _urq.Request(url, headers={"User-Agent": "longhun-judge/2.0"})
                    with _urq.urlopen(_rq, timeout=10) as _rs:
                        正文 = _rs.read().decode("utf-8", "replace")[:20000]
                except Exception:   # noqa: BLE001 网络受限降级
                    正文 = ""
        检测文本 = f"{名字} {url}" + ("\n" + 正文 if 正文 else "")
        m = re.search(r"#龍芯⚡️[^\s，。、；：！？“”‘’（）()【】\[\]\n]+", 检测文本[:30000])
        if m:
            撞名 = ["DNA指纹:" + m.group(0)]
        else:
            撞名 = sorted(n for n in 资产名集 if n and n in 检测文本)
        if not 撞名:
            可达 += 1
            if deep:
                print(f"  - {名字} ({类型}): 正文无通心译指纹 🟢")
            continue
        命中数 += 1
        匹配 = "、".join(撞名[:3])
        记录剽窃(f"[模型文档] {名字} ({类型})", url,
                 f"通心译剽窃:模型审计:{匹配}",
                 f"{名字} 检出龍魂通心译指纹·{'深度' if deep else '描述'}命中",
                 0.90, "🔴", 源类型="通心译剽窃")
        print(f"  🔍 命中 🔴 [模型文档] {名字} · {url} · {匹配}")
    # 重生成耻辱墙
    try:
        记录 = 获取所有记录()
        with open(HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(生成耻辱墙HTML(记录))
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(生成耻辱墙JSON(记录), f, ensure_ascii=False, indent=2)
    except Exception:   # noqa: BLE001
        pass
    记录扫描("topo-scan --model", 命中数)
    print("=" * 50)
    print(f"📊 模型文档审计完成 · 候选 {len(候选)} · 可达 {可达} · 命中上墙 {命中数}"
          f"（0 命中=模型文档无龍魂材料·审计通过）")
    return 命中数


# ============================================================
# 七、CLI注册
# ============================================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description='龙魂归一审判官')
    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # scan子命令
    p_scan = subparsers.add_parser('scan', help='执行归一扫描')
    p_scan.add_argument('--json', action='store_true', help='JSON输出')
    p_scan.add_argument('--mobile', action='store_true', help='仅扫手机端App源')
    p_scan.add_argument('--quick', action='store_true', help='仅扫手机端+内容平台源')

    # view子命令
    p_view = subparsers.add_parser('view', help='查看耻辱墙')
    p_view.add_argument('--json', action='store_true', help='JSON输出')

    # clean子命令
    p_clean = subparsers.add_parser('clean', help='清理30天前的记录')

    # 误报闭环 v1.0（2026-09-03）
    p_mis = subparsers.add_parser('misreport', help='疑似误报候选(待确认&置信度<60%)')
    p_mis.add_argument('--json', action='store_true', help='JSON输出')
    p_conf = subparsers.add_parser('confirm', help='人工确认命中(正式上墙)')
    p_conf.add_argument('id', type=int, help='记录ID')
    p_rej = subparsers.add_parser('reject', help='人工确认误报(记录 misreport_log.json)')
    p_rej.add_argument('id', type=int, help='记录ID')

    # phone-scan子命令 v2.0
    p_phone = subparsers.add_parser('phone-scan', help='扫描手机端App(App Store/华为/小米/Google Play)')
    p_phone.add_argument('--deep', action='store_true', help='深度扫描(含APK解析+iTunes详情补抓)')

    # phone-report子命令 v2.0
    p_phone_report = subparsers.add_parser('phone-report', help='生成手机端耻辱墙报告')

    # topo-scan子命令 v1.0（通心译内容审计）
    p_topo_scan = subparsers.add_parser('topo-scan', help='通心译内容审计(GitHub/HuggingFace/CSDN)')
    p_topo_scan.add_argument('--json', action='store_true', help='JSON输出')
    p_topo_scan.add_argument('--deep', action='store_true',
                             help='深度抓取v1.1: 对GitHub仓库raw README/HuggingFace model card正文级检测'
                                  '(默认=描述级标题/摘要; --deep=正文级·命中记「深度命中」上墙)')
    p_topo_scan.add_argument('--frameworks', action='store_true',
                             help='开源框架审计v1.0: 扫描龍魂依赖的开源框架官方文档'
                                  '(README)是否含通心译 DNA → 命中按「通心译剽窃:框架审计」上墙'
                                  '(M77 零依赖时为审计通过)')
    p_topo_scan.add_argument('--model', action='store_true',
                             help='模型文档审计v1.0(深度学习代码精修): 审计深度学习图谱中带公开链接的'
                                  'model/framework/dataset 资产(模型文档/代码)是否含通心译指纹'
                                  '→ 命中按「通心译剽窃:模型审计」上墙 · 0 命中=审计通过')

    args = parser.parse_args()

    if args.command == 'scan':
        执行归一扫描(args)
    elif args.command == 'view':
        查看耻辱墙(args)
    elif args.command == 'clean':
        清理耻辱墙(args)
    elif args.command == 'misreport':
        疑似误报列表(as_json=getattr(args, 'json', False))
    elif args.command == 'confirm':
        人工确认(args.id)
    elif args.command == 'reject':
        人工拒绝(args.id)
    elif args.command == 'phone-scan':
        手机端扫描(getattr(args, 'deep', False))
    elif args.command == 'phone-report':
        手机端报告()
    elif args.command == 'topo-scan':
        通心译剽窃扫描(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
