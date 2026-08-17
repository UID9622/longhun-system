#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 统一门户 API v2.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-PORTAL-API-v2.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  1. 静态门户服务 (portal/index.html)
  2. 人格矩阵 API (/api/persona/*)
  3. 知识库搜索 API (/api/search)
  4. 服务生态 API (/api/services/*)
  5. 数字人印记 API (/api/imprint/*)
  6. 健康检查 API (/api/health)

用法:
  lh portal [--port 8778] [--host 127.0.0.1]
  python3 bin/lh_portal_api.py --port 8778
"""

import os
import sys
import json
import time
import sqlite3
import urllib.request
import urllib.error
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# 项目根
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    print("⚠️ 请安装: pip install fastapi uvicorn pydantic")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# 日志
# ═══════════════════════════════════════════════════════════════
logging.basicConfig(level=logging.INFO, format="%(asctime)s | PORTAL-API | %(message)s")
logger = logging.getLogger(__name__)

DNA = "#龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-PORTAL-API-v2.0"

# ═══════════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════════
DATA_DIR = PROJECT_ROOT / "data"
PORTAL_DIR = PROJECT_ROOT / "portal"
SYNC_DB = DATA_DIR / "notion_sync.db"
NOTION_TOKEN = os.environ.get("NOTION_API_KEY", "")
NOTION_VERSION = "2022-06-28"

# ═══════════════════════════════════════════════════════════════
# 人格矩阵（扩增字段：ipa·expertise·ipa_phonetic）
# ═══════════════════════════════════════════════════════════════
PERSONA_MATRIX = {
    "P00": {
        "name": "文心", "role": "意图解析", "expertise": "自然语言理解·用户意图识别·语义路由",
        "layer": "strategic", "motto": "大音希声", "ipa": "P00", "ipa_phonetic": "wén xīn"
    },
    "P01": {
        "name": "诸葛亮", "role": "战略推演", "expertise": "多路径推演·决策分析·风险评估·战场沙盘",
        "layer": "strategic", "motto": "运筹帷幄", "ipa": "P01", "ipa_phonetic": "zhū gě liàng"
    },
    "P02": {
        "name": "宝宝", "role": "情感温度", "expertise": "情感温度引擎·30%情感隔离·挫败保护·教学场景温度调节",
        "layer": "executive", "motto": "赤子之心", "ipa": "P02", "ipa_phonetic": "bǎo bǎo"
    },
    "P03": {
        "name": "雯雯", "role": "结构归档", "expertise": "四签验证·德字闸·整理验收·文档结构化·知识入库",
        "layer": "executive", "motto": "井井有条", "ipa": "P03", "ipa_phonetic": "wén wén"
    },
    "P04": {
        "name": "鲁班", "role": "技术执行", "expertise": "代码编写·架构设计·bug修复·施工队长·技术选型",
        "layer": "executive", "motto": "匠心独运", "ipa": "P04", "ipa_phonetic": "lǔ bān"
    },
    "P05": {
        "name": "上帝之眼", "role": "审计监察", "expertise": "三色审计·十道闸口·加权多因子评分·独立否决权",
        "layer": "guardian", "motto": "明察秋毫", "ipa": "P05", "ipa_phonetic": "shàng dì zhī yǎn"
    },
    "P06": {
        "name": "数学大师", "role": "权重计算", "expertise": "数字根·五行判定·八卦映射·镜像审计·369不动点",
        "layer": "guardian", "motto": "天数有定", "ipa": "P06", "ipa_phonetic": "shù xué dà shī"
    },
    "P07": {
        "name": "管仲", "role": "资源调度", "expertise": "成本核算·经济可行性·ROI分析·预算规划·资源优化",
        "layer": "executive", "motto": "通货积财", "ipa": "P07", "ipa_phonetic": "guǎn zhòng"
    },
    "P08": {
        "name": "仓颉", "role": "符号命名", "expertise": "CNSH命名规范·术语桥接·通心译·概念翻译",
        "layer": "cultural", "motto": "造字正名", "ipa": "P08", "ipa_phonetic": "cāng jié"
    },
    "P09": {
        "name": "孙思邈", "role": "系统诊断", "expertise": "治未病·健康检查·系统体检·巡检·异常预警",
        "layer": "cultural", "motto": "治未病", "ipa": "P09", "ipa_phonetic": "sūn sī miǎo"
    },
    "P10": {
        "name": "苏东坡", "role": "沟通调解", "expertise": "冲突调解·沟通桥梁·人文视角·跨领域沟通",
        "layer": "cultural", "motto": "清风徐来", "ipa": "P10", "ipa_phonetic": "sū dōng pō"
    },
    "P11": {
        "name": "李白", "role": "创意爆发", "expertise": "破局方案·类比教学·故事化表达·创意生成",
        "layer": "cultural", "motto": "天生我材", "ipa": "P11", "ipa_phonetic": "lǐ bái"
    },
    "P12": {
        "name": "屈原", "role": "价值底线", "expertise": "六誓验证·不可破原则·底线守卫·红线判定",
        "layer": "cultural", "motto": "九死不悔", "ipa": "P12", "ipa_phonetic": "qū yuán"
    },
    "P13": {
        "name": "姜子牙", "role": "权限调度", "expertise": "封神榜权限分配·模块注册·IPA路由·权限变更",
        "layer": "guardian", "motto": "封神授权", "ipa": "P13", "ipa_phonetic": "jiāng zǐ yá"
    },
    "P14": {
        "name": "吕蒙", "role": "部署执行", "expertise": "部署上线·发布·回滚·鲲鹏同步·健康检查",
        "layer": "executive", "motto": "刮目相看", "ipa": "P14", "ipa_phonetic": "lǚ méng"
    },
    "P15": {
        "name": "乔前辈", "role": "签章质检", "expertise": "DNA盖章·交付验收·极简工程·四签验证",
        "layer": "guardian", "motto": "一签定乾坤", "ipa": "P15", "ipa_phonetic": "qiáo qián bèi"
    },
    "P18": {
        "name": "基因登记官", "role": "DNA注册", "expertise": "资产登记·哈希校验·黑户检测·Merkle根·归属验证",
        "layer": "executive", "motto": "锚定本源", "ipa": "P18", "ipa_phonetic": "jī yīn dēng jì guān"
    },
    "P19": {
        "name": "极简审计官", "role": "UI审计", "expertise": "CSS检查·8项极简审计·前端质量·无障碍检查·表单校验",
        "layer": "guardian", "motto": "少即是多", "ipa": "P19", "ipa_phonetic": "jí jiǎn shěn jì guān"
    },
    "P20": {
        "name": "贡献公证官", "role": "信任积分", "expertise": "三分桶·贡献公证·场景矩阵·政审·国资判定",
        "layer": "guardian", "motto": "公正无私", "ipa": "P20", "ipa_phonetic": "gòng xiàn gōng zhèng guān"
    },
    "P72": {
        "name": "龍盾", "role": "熔断守护", "expertise": "四级熔断·24小时守护·双熔断联动·例外豁免",
        "layer": "guardian", "motto": "熔断守底", "ipa": "P72", "ipa_phonetic": "lóng dùn"
    },
    "P77": {
        "name": "黑天使军团", "role": "红蓝对抗", "expertise": "漏洞猎手·渗透专家·代码审计·威胁情报·四天使编队",
        "layer": "special", "motto": "知攻善守", "ipa": "P77", "ipa_phonetic": "hēi tiān shǐ jūn tuán"
    },
    "S1": {
        "name": "法律引擎", "role": "合规审查", "expertise": "条文检索·合规分析·知识产权·法律边界（仅供参考）",
        "layer": "subsystem", "motto": "法度森严", "ipa": "S1", "ipa_phonetic": "fǎ lǜ yǐn qíng"
    },
    "S2": {
        "name": "洛书369", "role": "数理推演", "expertise": "洛书九宫·369不动点·深层数理（只给结论不给推导）",
        "layer": "subsystem", "motto": "数理深藏", "ipa": "S2", "ipa_phonetic": "luò shū sān liù jiǔ"
    },
    "S3": {
        "name": "人民维权助手", "role": "维权指引", "expertise": "维权路径指引·民生守护（强制免责声明）",
        "layer": "subsystem", "motto": "为人民服务", "ipa": "S3", "ipa_phonetic": "rén mín wéi quán zhù shǒu"
    },
}

# ═══════════════════════════════════════════════════════════════
# 服务生态注册表
# ═══════════════════════════════════════════════════════════════
SERVICES_REGISTRY = [
    {"name": "门户官网", "port": 8778, "icon": "🌐", "status": "online",
     "desc": "统一门户·人格矩阵·知识库搜索·数字人印记"},
    {"name": "人格路由 API", "port": 8779, "icon": "🧠", "status": "online",
     "desc": "22人格路由·意图分发·人格执行·降级兜底"},
    {"name": "Notion 对话桥", "port": 8779, "icon": "💬", "status": "online",
     "desc": "Notion RAG检索·人格联动·导航意图·记忆共享"},
    {"name": "知识中枢", "port": 8766, "icon": "🧠", "status": "online",
     "desc": "统一知识检索·AI摘要·向量搜索"},
    {"name": "统一记忆", "port": 8771, "icon": "📝", "status": "online",
     "desc": "跨会话持久化·焊死记忆·FTS5全文索引"},
    {"name": "搜索引擎", "port": 9631, "icon": "🔍", "status": "online",
     "desc": "Bing多源搜索·深度页面提取·结果缓存·P05审计"},
    {"name": "省电 API", "port": 8700, "icon": "⚡", "status": "online",
     "desc": "全球AI模型调用·Ollama+混元+DeepSeek·智能路由·省电率99.98%"},
    {"name": "量子卦象 API", "port": 9000, "icon": "☯️", "status": "online",
     "desc": "64卦希尔伯特空间·太极生两仪·卦象路由"},
    {"name": "DCT 水印", "port": "—", "icon": "🔏", "status": "online",
     "desc": "不可见水印·来源标记·防AI洗稿"},
    {"name": "声纹注册库", "port": 8774, "icon": "🎙️", "status": "online",
     "desc": "声纹注册·验证·匹配·身份核验"},
    {"name": "五行判定", "port": "—", "icon": "☯️", "status": "online",
     "desc": "五行属性判定·生克关系·能量流向·干支纳音"},
    {"name": "数字根引擎", "port": "—", "icon": "🔢", "status": "online",
     "desc": "369洛书数字根·三六九不动点·权重计算"},
]

# ═══════════════════════════════════════════════════════════════
# 数字人印记
# ═══════════════════════════════════════════════════════════════
IMPRINTS = [
    {"name": "诸葛鑫", "code": "ZGX-001", "icon": "👤",
     "desc": "龍魂系统创始人 · 数字人原型 · DNA 已锚定 · 退役老兵",
     "meta": "GPG: A2D0092C... · 声纹已注册 · 面孔已绑定 · UID9622"},
    {"name": "AI 代理", "code": "ASI-001", "icon": "🤖",
     "desc": "自主执行引擎 · 22人格联动 · 192引擎 · 多模型路由",
     "meta": "Ollama + 混元 + DeepSeek · 透明审计 · 熔断守护"},
    {"name": "鲲鹏执行器", "code": "KUNP-001", "icon": "⚡",
     "desc": "华为云服务器 · 119.13.90.27 · 11 systemd · 公网入口",
     "meta": "Nginx反向代理 · Let's Encrypt · 境内部署"},
]

# ═══════════════════════════════════════════════════════════════
# FastAPI 应用
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title="龍魂系统 · 统一门户 API",
    version="2.0.0",
    description="主权级 AI 执行骨架 · 人格矩阵 · 数字人 · 知识图谱",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JSON 序列化
class SearchRequest(BaseModel):
    query: str
    limit: int = 10


# ═══════════════════════════════════════════════════════════════
# 首页
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def serve_index():
    """门户首页"""
    index_path = PORTAL_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h2>portal/index.html 未找到</h2>", status_code=404)


# ═══════════════════════════════════════════════════════════════
# API: 健康检查
# ═══════════════════════════════════════════════════════════════

@app.get("/health")
def health_root():
    """健康检查（根路径兼容）"""
    return {"status": "ok", "service": "portal-api", "port": 8778, "dna": DNA}

@app.get("/api/health")
def health():
    """统一健康检查"""
    # 人格引擎状态
    persona_ok = False
    persona_count = 0
    try:
        import engines.lh_persona_runner
        persona_ok = True
        persona_count = len(PERSONA_MATRIX)
    except Exception:
        pass

    # Notion 状态
    notion_ok = bool(NOTION_TOKEN)
    notion_count = 0
    if notion_ok and SYNC_DB.exists():
        try:
            conn = sqlite3.connect(str(SYNC_DB))
            cnt = conn.execute("SELECT COUNT(*) FROM pages").fetchone()
            notion_count = cnt[0] if cnt else 0
            conn.close()
        except Exception:
            notion_count = 0

    # 鲲鹏检测（简单尝试）
    kunpeng_ok = False
    try:
        req = urllib.request.Request("https://uid9622.cn/api/onboarding/bootstrap",
                                      headers={"User-Agent": "LongHun-Portal/2.0"})
        urllib.request.urlopen(req, timeout=3)
        kunpeng_ok = True
    except Exception:
        pass

    return {
        "status": "ok",
        "dna": DNA,
        "persona": persona_ok,
        "persona_count": persona_count,
        "notion": notion_ok,
        "notion_count": notion_count,
        "imprint": True,
        "kunpeng": kunpeng_ok,
        "timestamp": datetime.now().isoformat(),
    }


# ═══════════════════════════════════════════════════════════════
# API: 人格矩阵
# ═══════════════════════════════════════════════════════════════

@app.get("/api/persona/list")
def list_personas():
    """列出所有22人格 + 详细信息"""
    result = []
    for pid, meta in PERSONA_MATRIX.items():
        result.append({
            "id": pid,
            "name": meta["name"],
            "role": meta["role"],
            "expertise": meta.get("expertise", ""),
            "layer": meta["layer"],
            "motto": meta["motto"],
            "ipa": pid,
            "ipa_phonetic": meta.get("ipa_phonetic", ""),
            "online": True,
        })
    # 按层级排序
    layer_order = {"strategic": 0, "executive": 1, "cultural": 2, "guardian": 3, "special": 4, "subsystem": 5}
    result.sort(key=lambda p: layer_order.get(p["layer"], 99))
    return {"personas": result, "total": len(result), "online": len(result),
            "dna": DNA, "timestamp": datetime.now().isoformat()}


@app.get("/api/persona/{persona_id}")
def get_persona(persona_id: str):
    """获取单个人格详情"""
    meta = PERSONA_MATRIX.get(persona_id.upper())
    if not meta:
        raise HTTPException(status_code=404, detail=f"未知人格: {persona_id}")
    return {
        "id": persona_id.upper(),
        "name": meta["name"],
        "role": meta["role"],
        "expertise": meta.get("expertise", ""),
        "layer": meta["layer"],
        "motto": meta["motto"],
        "ipa": persona_id.upper(),
        "ipa_phonetic": meta.get("ipa_phonetic", ""),
        "online": True,
        "dna": DNA,
    }


# ═══════════════════════════════════════════════════════════════
# API: 知识库搜索
# ═══════════════════════════════════════════════════════════════

def search_local(query: str, limit: int = 10) -> List[Dict]:
    """本地 FTS5 全文搜索"""
    results = []
    if not SYNC_DB.exists():
        return results
    try:
        conn = sqlite3.connect(str(SYNC_DB))
        conn.row_factory = sqlite3.Row
        # 尝试 FTS5 搜索
        rows = conn.execute(
            "SELECT id, title, content, url, updated_at FROM pages "
            "WHERE title LIKE ? OR content LIKE ? "
            "ORDER BY updated_at DESC LIMIT ?",
            (f"%{query}%", f"%{query}%", limit)
        ).fetchall()
        for row in rows:
            d = dict(row)
            # 截断内容
            content = d.get("content", "")
            if len(content) > 300:
                content = content[:300] + "..."
            results.append({
                "title": d.get("title", "未命名"),
                "snippet": content,
                "url": d.get("url", ""),
                "source": d.get("id", "")[:20],
                "updated": d.get("updated_at", ""),
            })
        conn.close()
    except Exception as e:
        logger.warning(f"本地搜索失败: {e}")
    return results


def search_notion(query: str, limit: int = 10) -> List[Dict]:
    """Notion API 全文搜索"""
    if not NOTION_TOKEN:
        return []
    results = []
    try:
        payload = json.dumps({"query": query, "page_size": limit}).encode('utf-8')
        req = urllib.request.Request(
            "https://api.notion.com/v1/search",
            method="POST",
            data=payload,
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        for item in data.get("results", []):
            title = ""
            props = item.get("properties", {})
            for p in props.values():
                if p.get("type") == "title":
                    title = "".join([t.get("plain_text", "") for t in p.get("title", [])])
                    break
            results.append({
                "title": title or "未命名",
                "snippet": f"[Notion: {item.get('object', 'page')}]",
                "url": item.get("url", ""),
                "source": item.get("id", "")[:20],
            })
    except Exception as e:
        logger.warning(f"Notion API 搜索失败: {e}")
    return results


@app.post("/api/search")
def search(req: SearchRequest):
    """知识库搜索（本地FTS5优先 → Notion API兜底）"""
    start = time.time()

    # 本地搜索
    local_results = search_local(req.query, req.limit)

    # Notion 补充
    if len(local_results) < req.limit:
        remote = search_notion(req.query, req.limit - len(local_results))
        seen = {r.get("source", "") for r in local_results}
        for r in remote:
            if r.get("source") not in seen:
                local_results.append(r)

    return {
        "query": req.query,
        "results": local_results[:req.limit],
        "total": len(local_results),
        "duration_ms": round((time.time() - start) * 1000, 2),
        "sources": ["local", "notion"] if NOTION_TOKEN else ["local"],
        "timestamp": datetime.now().isoformat(),
    }


# ═══════════════════════════════════════════════════════════════
# API: 服务生态
# ═══════════════════════════════════════════════════════════════

@app.get("/api/services/list")
def list_services():
    """列出所有注册服务"""
    return {
        "services": SERVICES_REGISTRY,
        "total": len(SERVICES_REGISTRY),
        "online": sum(1 for s in SERVICES_REGISTRY if s.get("status") == "online"),
        "dna": DNA,
        "timestamp": datetime.now().isoformat(),
    }


# ═══════════════════════════════════════════════════════════════
# API: 数字人印记
# ═══════════════════════════════════════════════════════════════

@app.get("/api/imprint/list")
def list_imprints():
    """数字人印记列表"""
    return {
        "imprints": IMPRINTS,
        "total": len(IMPRINTS),
        "dna": DNA,
        "timestamp": datetime.now().isoformat(),
    }


# ═══════════════════════════════════════════════════════════════
# API: 全体状态（聚合）
# ═══════════════════════════════════════════════════════════════

@app.get("/api/status")
def full_status():
    """聚合全部状态：健康·人格·服务·印记·搜索"""
    return {
        "health": health() if hasattr(health, '__call__') else {},
        "personas": list_personas(),
        "services": list_services(),
        "imprints": list_imprints(),
        "dna": DNA,
        "timestamp": datetime.now().isoformat(),
    }


# ═══════════════════════════════════════════════════════════════
# 静态文件兜底路由（必须在所有API路由之后）
# ═══════════════════════════════════════════════════════════════

@app.get("/{filename:path}")
async def serve_static(filename: str):
    """静态文件服务（CSS/JS/字体等）—— 兜底：所有API不匹配时触发"""
    file_path = PORTAL_DIR / filename
    if file_path.is_file():
        return FileResponse(str(file_path))
    # 兜底到 index.html (SPA)
    index_path = PORTAL_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding='utf-8'))
    raise HTTPException(status_code=404, detail="Not found")


# ═══════════════════════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    ap = argparse.ArgumentParser(description="龍魂统一门户 API v2.0")
    ap.add_argument("--host", default="127.0.0.1", help="监听地址 (默认: 127.0.0.1)")
    ap.add_argument("--port", type=int, default=8778, help="监听端口")
    ap.add_argument("--reload", action="store_true", help="热重载模式")
    args = ap.parse_args()

    logger.info(f"🚀 龍魂统一门户 v2.0 启动 | {DNA}")
    logger.info(f"   📡 {args.host}:{args.port}")
    logger.info(f"   🌐 http://localhost:{args.port}")
    logger.info(f"   🧠 {len(PERSONA_MATRIX)} 人格已注册")
    logger.info(f"   🔌 {len(SERVICES_REGISTRY)} 服务已注册")
    logger.info(f"   🧬 {len(IMPRINTS)} 数字人印记")
    logger.info(f"   📚 Notion: {'已配置' if NOTION_TOKEN else '未配置'}")

    uvicorn.run(app, host=args.host, port=args.port, log_level="warning",
                reload=args.reload)


if __name__ == "__main__":
    main()
