#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · Notion 空壳填充执行引擎 v1.0
用法: python3 bin/lh_notion_fill_executor.py --dry-run
      python3 bin/lh_notion_fill_executor.py --execute
DNA: #龍芯⚡️2026-07-14-NOTION-FILL-v1.0
"""
import json, os, subprocess, sys, time, argparse
from pathlib import Path

HOME = Path.home()
ROOT = HOME / "longhun-system"
DATA_DIR = ROOT / "data" / "notion_scan" / "deep_scan_3dbs"
SCAN_FILE = DATA_DIR / "deep_scan_result.json"
PLAN_FILE = DATA_DIR / "fill_plan.json"

sys.path.insert(0, str(ROOT / "bin"))
from lh_secrets_loader import load_all
from lh_knowledge_algo_db import LONGHUN_ALGORITHMS, ML_ALGORITHMS, RENDER_KNOWLEDGE, CS_BASICS, ARTICLE_LOGIC, EXTRA_ALGOS

load_all(export_to_os=True)
TOKEN = os.environ.get("NOTION_TOKEN", "")

ALL_ALGOS = {**LONGHUN_ALGORITHMS, **ML_ALGORITHMS, **RENDER_KNOWLEDGE, **CS_BASICS, **EXTRA_ALGOS}

def notion_api(endpoint, method="GET", payload=None):
    url = f"https://api.notion.com/v1{endpoint}"
    cmd = [
        "curl", "-s", "-S", "--max-time", "30",
        "-H", f"Authorization: Bearer {TOKEN}",
        "-H", "Notion-Version: 2022-06-28",
        "-H", "Content-Type: application/json",
    ]
    if method != "GET": cmd.extend(["-X", method])
    if payload: cmd.extend(["-d", json.dumps(payload, ensure_ascii=False)])
    cmd.extend(["-w", r"\nHTTP_CODE:%{http_code}", url])
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=35)
        out = proc.stdout.decode("utf-8", errors="replace")
        if "HTTP_CODE:" not in out: return None
        body, code = out.rsplit("HTTP_CODE:", 1)
        code = int(code.strip())
        if code >= 400:
            if code == 429: time.sleep(3); return notion_api(endpoint, method, payload)
            print(f"  API{code}: {body[:100]}", file=sys.stderr); return None
        return json.loads(body.strip()) if body.strip() else {}
    except: return None

def update_page(page_id, properties):
    return notion_api(f"/pages/{page_id}", "PATCH", {"properties": properties})

def rt(content):
    """rich_text"""
    if not content: return {"rich_text": []}
    return {"rich_text": [{"type": "text", "text": {"content": str(content)}}]}

def sel(name):
    """select"""
    if not name: return {"select": None}
    return {"select": {"name": str(name)}}

def msel(names):
    """multi_select"""
    if not names: return {"multi_select": []}
    if isinstance(names, str): names = [n.strip() for n in names.split("·")]
    return {"multi_select": [{"name": str(n)[:100]} for n in names if n.strip()]}

def find_algo(title):
    """匹配算法"""
    tl = title.lower()
    kmap = {
        "数字根": "数字根", "三才": "三才算法", "五行": "五行生克",
        "三色审计": "三色审计", "梦幻": "梦幻度评分", "贡献": "贡献值算法",
        "信息熵": "信息熵", "熵": "信息熵",
        "洛书": "洛书九宫矩阵", "九宫": "洛书九宫矩阵",
        "f(x)=x": "f(x)=x原点定理", "原点": "f(x)=x原点定理", "不动点定理": "f(x)=x原点定理",
        "太极": "太极递归算法", "64卦": "64卦有限状态自动机", "六十四": "64卦有限状态自动机",
        "水军": "水军行为识别", "路由": "CNSH路由公式",
        "三才校验": "三才校验公式", "人格路由": "人格路由规则",
        "记忆压缩": "记忆压缩引擎", "不动点网络": "不动点网络",
        "六维路径": "六维路径编码", "16588800": "六维路径编码",
        "原点能量": "CNSH原点能量场", "能量场": "CNSH原点能量场",
        "时间压缩": "时间压缩算法", "bra.ket": "量子Bra-Ket人格协作", "量子": "量子Bra-Ket人格协作",
        "perlin": "Perlin噪声", "三才向量": "三才向量合成",
        "七维": "七维伦理权重", "伦理权重": "七维伦理权重", "伦理": "七维伦理权重",
        "涌现": "涌现质量公式", "逻辑漂移": "逻辑漂移侦测器",
        "线性回归": "线性回归", "逻辑回归": "逻辑回归",
        "决策树": "决策树", "svm": "SVM", "随机森林": "随机森林",
        "xgboost": "XGBoost", "朴素贝叶斯": "朴素贝叶斯", "pca": "PCA",
        "k-means": "K-Means", "knn": "KNN", "k-nn": "KNN",
        "mlp": "MLP", "多层感知": "MLP", "cnn": "CNN", "卷积": "CNN",
        "rnn": "RNN/LSTM", "lstm": "RNN/LSTM",
        "transformer": "Transformer", "注意力": "Transformer",
        "bert": "BERT", "gpt": "GPT", "生成式": "GPT",
        "扩散": "扩散模型", "gan": "GAN", "生成对抗": "GAN",
        "梯度下降": "梯度下降", "adam": "Adam优化器",
        "强化学习": "强化学习", "迁移学习": "迁移学习",
        "贝叶斯优化": "贝叶斯优化", "遗传算法": "遗传算法",
        "光线追踪": "光线追踪", "光栅化": "光栅化",
        "pbr": "PBR", "基于物理": "PBR", "全局光照": "全局光照",
        "材质": "材质", "渲染": "渲染", "贴图": "材质",
        "建模": "材质", "灯光": "渲染", "漫反射": "渲染",
        "焦散": "光线追踪", "抗锯齿": "渲染", "采样率": "光栅化",
        "lod": "光栅化", "acid": "数据库 ACID", "事务": "数据库 ACID",
        "tcp": "TCP三次握手", "三次握手": "TCP三次握手",
        "进程": "进程线程协程", "线程": "进程线程协程", "协程": "进程线程协程",
        "大o": "大O表示法", "时间复杂度": "大O表示法",
        "内存模型": "内存模型", "堆": "内存模型", "栈": "内存模型",
        "cnsh渲染": "光栅化", "SwiftUI": "光栅化", "星空": "Perlin噪声",
        "公司根": "f(x)=x原点定理", "三才流場": "三才算法",
        "龍魂印记": "数字根", "伦理沙盒": "七维伦理权重",
        "自愈健康": "五行生克", "mcp": "CNSH路由公式", "sse": "CNSH路由公式",
        "dna日历": "记忆压缩引擎", "dna加密": "数字根",
        "铜墙铁壁": "三色审计", "统一引擎": "涌现质量公式",
        "小妖": "量子Bra-Ket人格协作", "arkit": "三才向量合成",
        "ai跨会话": "记忆压缩引擎", "量子计算": "量子Bra-Ket人格协作",
        "通心译": "CNSH路由公式", "天干地支": "六维路径编码",
        "龍芯家族花名册": "人格路由规则", "龍魂暗语": "数字根",
        "星辰记忆": "记忆压缩引擎", "龍魂本地引擎": "涌现质量公式",
        "龍魂指挥塔": "人格路由规则", "沙盒推演": "涌现质量公式",
        "质检机器人": "三色审计", "数据": "数据库 ACID",
        "计算": "TCP三次握手", "网络": "TCP三次握手",
        "python": "内存模型", "数论": "数字根", "概率": "信息熵",
        "线性代数": "PCA", "离散数学": "大O表示法",
        "数据结构": "大O表示法", "操作系统": "进程线程协程",
        "渲染器": "光栅化", "采样": "光栅化",
        "傅里叶": "傅里叶变换", "fourier": "傅里叶变换",
        "自动微分": "梯度下降", "数值方法": "梯度下降",
        "渲染几何": "光栅化", "信息论": "信息熵",
        "龍魂龍醒": "涌现质量公式", "龍魂本地": "涌现质量公式",
        "五层时间": "时间压缩算法", "河洛图": "洛书九宫矩阵",
        "八卦维度": "CNSH路由公式", "河图维度": "洛书九宫矩阵",
        "cnsh中文": "CNSH路由公式", "cnsh网关": "CNSH路由公式",
        "ai-dna": "涌现质量公式", "dna思考": "涌现质量公式",
        "三路只读": "三才校验公式", "双脑同步": "记忆压缩引擎",
        "规则库": "人格路由规则", "swift": "内存模型",
        "数据库理论": "数据库 ACID", "计算机网络": "TCP三次握手",
        "操作系统原理": "进程线程协程", "计算理论": "大O表示法",
        "数据结构与算法": "大O表示法", "数据库：事务": "数据库 ACID",
        "计算机网络：tcp": "TCP三次握手", "操作系统：进程": "进程线程协程",
        "内存模型：": "内存模型", "算法复杂度": "大O表示法",
        "cnsh渲染": "光栅化", "渲染格式": "光栅化",
        "渲染器": "光栅化", "抗锯齿": "光栅化",
        "漫反射": "渲染", "灯光": "渲染", "渲染几何": "光栅化",
        "渲染": "光栅化", "renderer": "光栅化",
        "龍魂龍醒": "涌现质量公式", "龍魂本地引擎": "涌现质量公式",
        "龍魂指挥塔": "人格路由规则", "龍魂本地服务": "涌现质量公式",
    }
    for kw, aname in kmap.items():
        if kw in tl:
            return ALL_ALGOS.get(aname), aname
    return None, None

def find_article(title):
    if not title: return None
    tl = title.lower()
    # 精确匹配映射
    amap = {
        "cns·协议层文明": "CNSH·协议层文明论",
        "cns·协议层": "CNSH·协议层文明论",
        "洛书 369": "洛书369与AI决策不变量",
        "洛书369": "洛书369与AI决策不变量",
        "通心译": "通心译×SAST",
        "道德经底层引擎": "道德经底层引擎",
        "道德经": "道德经底层引擎",
        "dna 永生记忆": "DNA永生记忆系统",
        "dna永生": "DNA永生记忆系统",
        "统一压缩科学护城河": "统一压缩科学护城河",
        "统一压缩": "统一压缩科学护城河",
        "三才流场 mcp": "三才流场 MCP",
        "三才流場": "三才流场 MCP",
        "行为密码学": "行为密码学",
        "伦理计算框架": "龍魂伦理计算框架",
        "倫理計算": "龍魂伦理计算框架",
        "文化卖国": "文化卖国罪",
        "家法": "文化卖国罪",
        "自主创新驱动": "自主创新AI落地",
        "人工智能+": "自主创新AI落地",
        "倾听中国科技": "科技创新总结2025",
        "科技事业奋进": "科技创新总结2025",
        "加快高水平科技": "科技自立自强",
        "科技自立自强之路": "科技自立自强",
        "智能经济支撑": "智能经济GDP",
        "智能经济": "智能经济GDP",
        "加强科技创新": "科技自立自强",
        "人民": "科技自立自强",
        "抢救仓": "通心译验证清单",
        "video_gen": "通心译验证清单",
        "禪宗": "禪宗水墨音效",
        "水墨": "禪宗水墨音效",
        "知识库批量抓取": "知识库抓取系统",
        "知識庫": "知识库抓取系统",
        "textrank": "知识库抓取系统",
        "嫦娥": "嫦娥七号",
        "月球": "嫦娥七号",
        "光刻机": "光刻机28nm",
        "上海微电子": "光刻机28nm",
        "麒麟 9020": "麒麟9020",
        "麒麟9020": "麒麟9020",
        "华为": "麒麟9020",
        "cns-64": "CNSH-64形式化",
        "cns-64": "CNSH-64形式化",
        "dual-state": "CNSH-64形式化",
        "以人为本的ai治理": "CNSH以人为本",
        "中国人自己的": "CNSH以人为本",
        "中国科技自主创新": "中国科技总览",
        "关键核心技术突破": "中国科技总览",
        "总览": "中国科技总览",
    }
    # 先检查映射
    for kw, aname in amap.items():
        if kw in tl:
            return ARTICLE_LOGIC.get(aname)
    # 再检查ARTICLE_LOGIC中的关键词
    for art_name, data in ARTICLE_LOGIC.items():
        # 提取关键片段匹配
        key_parts = art_name.split("·")
        for part in key_parts:
            if len(part) >= 3 and part.lower() in tl:
                return data
    return None

def fill_db1(scan, args):
    """填充DB1知识图谱"""
    db1 = scan["databases"][0]
    print(f"\n{'='*60}")
    print(f"🐉 DB1 知识图谱 ({len(db1['entries'])}条)")
    print(f"{'='*60}")

    fills = []
    filled = skipped = not_matched = 0

    for entry in db1["entries"]:
        title = entry["title"]
        algo_data, algo_name = find_algo(title)
        if not algo_data:
            not_matched += 1
            continue

        empty_set = set(entry.get("empty_fields", []))
        props = {}

        field_map = {
            "算法公式": "算法公式", "核心公式": "核心公式",
            "描述": "描述", "常见误区": "常见误区",
            "关联知识点": "关联知识点", "dr·五行·宫位": "dr·五行·宫位",
        }
        for empty_f, data_k in field_map.items():
            if empty_f in empty_set and data_k in algo_data:
                props[empty_f] = rt(algo_data[data_k])

        # multi_select 字段
        msel_fields = {"应用场景": "应用场景", "人格路由": "人格路由"}
        for empty_f, data_k in msel_fields.items():
            if empty_f in empty_set and data_k in algo_data:
                props[empty_f] = msel(algo_data[data_k])

        select_fields = {
            "学习优先级": "学习优先级",
            "掌握程度": "掌握程度", "是否核心": "是否核心",
            "难度等级": "难度等级",
        }
        for empty_f, data_k in select_fields.items():
            if empty_f in empty_set and data_k in algo_data:
                props[empty_f] = sel(algo_data[data_k])

        if not props:
            skipped += 1
            continue

        filled += 1
        fills.append({"id": entry["id"], "title": title, "algo": algo_name, "n": len(props)})

        if args.execute:
            result = update_page(entry["id"], props)
            s = "✅" if result else "❌"
            print(f"  {s} {title[:55]} → +{len(props)}字段 [{algo_name}]")
            if filled % 15 == 0: time.sleep(2)
        else:
            print(f"  📝 {title[:55]} → +{len(props)}字段 [{algo_name}]")

    print(f"\n📊 DB1: {filled}填充/{skipped}跳过/{not_matched}未匹配/{len(db1['entries'])}总计")
    return {"fills": fills, "filled": filled, "skipped": skipped, "not_matched": not_matched}

def fill_db3(scan, args):
    """填充DB3专栏文章"""
    db3 = scan["databases"][1]
    print(f"\n{'='*60}")
    print(f"🐉 DB3 专栏文章 ({len(db3['entries'])}条)")
    print(f"{'='*60}")

    fills = []
    filled = skipped = 0

    for entry in db3["entries"]:
        title = entry["title"]
        if not title:
            skipped += 1
            continue

        adata = find_article(title)
        if not adata:
            skipped += 1
            continue

        empty_set = set(entry.get("empty_fields", []))
        props = {}

        if "底层逻辑" in empty_set and "底层逻辑" in adata:
            props["底层逻辑"] = rt(adata["底层逻辑"])
        if "易经锚点" in empty_set and "易经锚点" in adata:
            props["易经锚点"] = rt(adata["易经锚点"])
        if "一句话摘要" in empty_set and "一句话摘要" in adata:
            props["一句话摘要"] = rt(adata["一句话摘要"])

        if not props:
            skipped += 1
            continue

        filled += 1
        fills.append({"id": entry["id"], "title": title, "n": len(props)})

        if args.execute:
            result = update_page(entry["id"], props)
            s = "✅" if result else "❌"
            print(f"  {s} {title[:55]} → +{len(props)}字段")
            time.sleep(0.5)
        else:
            print(f"  📝 {title[:55]} → +{len(props)}字段")

    print(f"\n📊 DB3: {filled}填充/{skipped}跳过/{len(db3['entries'])}总计")
    return {"fills": fills, "filled": filled, "skipped": skipped}

def main():
    p = argparse.ArgumentParser(description="龍魂 Notion 空壳填充执行引擎 v1.0")
    p.add_argument("--dry-run", action="store_true", help="预览")
    p.add_argument("--execute", action="store_true", help="实际写入")
    p.add_argument("--db1-only", action="store_true")
    p.add_argument("--db3-only", action="store_true")
    args = p.parse_args()

    if not (args.dry_run or args.execute):
        print("请指定 --dry-run 或 --execute"); return

    scan = json.loads(open(SCAN_FILE).read())
    plan = {"dna": f"#龍芯⚡️{time.strftime('%Y%m%d-%H%M%S')}-FILL-v1",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "mode": "execute" if args.execute else "dry-run"}

    if not args.db3_only:
        plan["db1"] = fill_db1(scan, args)
    if not args.db1_only:
        plan["db3"] = fill_db3(scan, args)

    PLAN_FILE.write_text(json.dumps(plan, ensure_ascii=False, indent=2))

    total = plan.get("db1", {}).get("filled", 0) + plan.get("db3", {}).get("filled", 0)
    print(f"\n{'='*60}")
    print(f"✅ 填充完成: {PLAN_FILE}")
    print(f"   总填充条目: {total}")
    print(f"   模式: {'实际写入' if args.execute else '预览'}")
    print(f"   DNA: {plan['dna']}")

if __name__ == "__main__":
    main()
