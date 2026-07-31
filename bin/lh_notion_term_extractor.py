# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·乙酉·NOTION-TERM-EXTRACTOR-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·Notion知识库术语提取引擎 v1.0
=====================================
DNA: #龍芯⚡️丙午·辛未·乙酉·NOTION-TERM-EXTRACTOR-v1.0
用途: 从Notion知识库51页中自动提取专业术语，建立术语→页面→定义映射
通道: 本地镜像JSON(优先) + Notion API(实时补全)
输出: data/notion_term_index.json — 术语索引
      data/notion_term_index_v2.json — 注册表v2.0扩展补丁

用法:
  python3 bin/lh_notion_term_extractor.py            # 本地镜像提取(默认)
  python3 bin/lh_notion_term_extractor.py --api       # API实时拉取+提取
  python3 bin/lh_notion_term_extractor.py --full      # 本地+API全量
  python3 bin/lh_notion_term_extractor.py --export    # 导出注册表补丁
"""

import sys, os, json, re, hashlib, time, subprocess
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple, Optional, Any

HOME = Path.home()
ROOT = HOME / "longhun-system"

# ═══════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════
CONFIG_PATH = ROOT / "config" / "notion_sync.json"
MIRROR_DIR = ROOT / "docs" / "notion_mirror" / "pages"
OUTPUT_DIR = ROOT / "data" / "notion_term_index"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 龍魂系统已有的术语关键词库（用于启发式匹配）
DRAGON_TERM_PATTERNS = [
    # 密码学与安全
    r'(SM[2349]|AES-\d{3}|SHA-\d{3}|HMAC|ECC|RSA|EdDSA|ECDSA)',
    r'(数字签名|数字指纹|哈希|散列|加密算法|密钥|证书|PKI)',
    r'(零知识证明|同态加密|多方计算|安全多方|不经意传输)',
    r'(国密|商密|密码机|密码模块|密码算法)',
    # 治理与协议
    r'(一票否决|三色审计|三色治理|熔断机制|硬失败|软降级)',
    r'(北辰协议|宪法层|L\d+层|P\d+级|M\d+层)',
    r'(D-GATE|前置闸门|数字根|身份验证|伦理审查)',
    r'(DNA追溯|DNA签名|DNA验证|DNA绑定)',
    # 算法与数学
    r'(三才算法|模\d+|数字根|369洛书|七因子|权重分配)',
    r'(河图洛书|五行|阴阳|太极|八卦|六十四卦)',
    r'(Bra-Ket|态矢量|纠缠度|叠加态|量子|概率幅)',
    r'(信息素|蚁群|涌现|自组织|群体智能)',
    # 系统架构
    r'(神经网络|知识图谱|语义分析|自然语言|NLP)',
    r'(微服务|API网关|消息队列|事件溯源|CQRS)',
    r'(容器化|Docker|Kubernetes|服务网格|Istio)',
    r'(SQLite|PostgreSQL|向量数据库|图数据库|时序数据库)',
    # CNSH语言
    r'(CNSH|中文编程|字元|关键字|编译器|解释器|运行时)',
    r'(通心译|语义翻译|自然语言编程|意图识别)',
    # 哲学与文化
    r'(道德经|易经|周易|孙子兵法|黄帝内经|曾仕强)',
    r'(原生态知识|文化输出|文化主权|文化根脉|28星宿)',
    r'(知行合一|天人合一|道法自然|阴阳调和|中庸)',
    # 人物体系
    r'(文心|诸葛亮|宝宝|雯雯|鲁班|管仲|仓颉|孙思邈|苏东坡|李白|屈原|吕蒙|姜子牙)',
    r'(UID9622|诸葛鑫|Lucky|龍芯北辰|老大)',
    # 数据主权
    r'(数据主权|数据归集|数据所有权|数字身份|数字遗产)',
    r'(GDPR|个人信息保护法|数据安全法|网络安全法)',
    # 特殊术语
    r'(时空织网|量子触角|量子路由器|量子熔断器)',
    r'(人格矩阵|人格路由|人格切换|人格叠加)',
    r'(确认封印|行为签名|设备指纹|主权派生)',
    # CNSH专有
    r'(三才引擎|三才流场|洛书九宫|四层桥接|六重主权)',
    r'(声影桥|数字甲骨文|语义注册表|语义统一)',
]

TERM_EXTRACT_REGEX = re.compile('|'.join(f'({p})' for p in DRAGON_TERM_PATTERNS), re.IGNORECASE)

# 中文术语长词提取（2-8字专业词组）
CN_TERM_PATTERN = re.compile(
    r'[\u4e00-\u9fff]{2,8}(?:算法|引擎|协议|系统|机制|模型|框架|架构|体系|标准|规范|'
    r'引擎|工具|平台|服务|层|级别|节点|网关|桥接|路由|'
    r'算法|方法|模式|策略|法则|公理|定理|定律|'
    r'宪法|契约|协议|规则|准则|铁律|'
    r'定义|概念|术语|名词|'
    r'人格|身份|角色|代理)'
)

# 英文字母缩写（2-6个大写字母含数字）
ABBR_PATTERN = re.compile(r'\b[A-Z]{2,6}(?:\d+)?\b')

def load_token() -> Optional[str]:
    """从.env加载Notion token"""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return None
    text = env_path.read_text()
    m = re.search(r'NOTION_TOKEN[= ]+(\S+)', text)
    return m.group(1) if m else None

def load_page_mappings() -> list[Any]:
    """加载notion_sync.json中的页面映射"""
    if not CONFIG_PATH.exists():
        print(f"  ❌ 配置文件不存在: {CONFIG_PATH}")
        return []
    # 移除尾部//注释行
    lines = CONFIG_PATH.read_text().split("\n")
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("//"):
            break  # 尾部注释停止解析
        clean_lines.append(line)
    data = json.loads("\n".join(clean_lines))
    mappings = data.get("mappings", [])
    print(f"  📋 加载 {len(mappings)} 个Notion页面映射")
    return mappings

def extract_terms_from_text(text: str) -> Dict[str, List[str]]:
    """从文本中提取专业术语"""
    result = defaultdict(list[Any])
    
    # 1. 正则模式匹配
    for match in TERM_EXTRACT_REGEX.finditer(text):
        term = match.group(0).strip()
        if term and len(term) > 1:
            # 获取上下文（前后各20字）
            start = max(0, match.start() - 20)
            end = min(len(text), match.end() + 40)
            ctx = text[start:end].replace('\n', ' ').strip()
            result[term].append(ctx[:100])
    
    # 2. 中文专业词组提取
    for match in CN_TERM_PATTERN.finditer(text):
        term = match.group(0).strip()
        if term and 2 <= len(term) <= 12:
            start = max(0, match.start() - 15)
            end = min(len(text), match.end() + 30)
            ctx = text[start:end].replace('\n', ' ').strip()
            if term not in result:
                result[term] = []
            result[term].append(ctx[:80])
    
    # 3. 英文缩写提取
    for match in ABBR_PATTERN.finditer(text):
        term = match.group(0).strip()
        if term and 3 <= len(term) <= 10:
            if term.lower() in {'the', 'and', 'for', 'are', 'not', 'but', 'has', 'had', 'was'}:
                continue
            if term not in result:
                result[term] = []
            start = max(0, match.start() - 10)
            end = min(len(text), match.end() + 30)
            ctx = text[start:end].replace('\n', ' ').strip()
            result[term].append(ctx[:80])
    
    return dict(result)

def load_cached_page(page_id: str) -> Optional[dict[str, Any]]:
    """加载已缓存的页面JSON"""
    json_path = MIRROR_DIR / f"{page_id}.json"
    if json_path.exists():
        try:
            return json.loads(json_path.read_text())
        except:
            return None
    return None

def fetch_page_api(page_id: str, token: str) -> Optional[dict[str, Any]]:
    """通过Notion API实时拉取页面"""
    import subprocess, json as json_mod
    
    # 获取页面元数据
    url = f"https://api.notion.com/v1/pages/{page_id}"
    cmd = [
        "curl", "-s", "-S", "--max-time", "30",
        "-H", f"Authorization: Bearer {token}",
        "-H", "Notion-Version: 2022-06-28",
        "-H", "Content-Type: application/json",
        "-w", r"\n%{http_code}",
        url
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=35)
        out = proc.stdout.decode("utf-8", errors="replace")
        if "\n" in out:
            last_line = out.rsplit("\n", 1)[-1]
            if last_line.isdigit():
                body = out.rsplit("\n", 1)[0]
                code = int(last_line)
            else:
                body = out
                code = 0
        else:
            body = out
            code = 0
        
        if code != 200:
            return None
        
        page = json_mod.loads(body)
        
        # 提取标题
        title_parts = []
        for prop_val in (page.get("properties") or {}).values():
            if isinstance(prop_val, dict) and prop_val.get("type") == "title":
                title_parts = [t.get("plain_text", "") for t in prop_val.get("title", [])]
                break
        
        title = "".join(title_parts)
        
        # 获取块内容
        blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
        cmd2 = [
            "curl", "-s", "-S", "--max-time", "60",
            "-H", f"Authorization: Bearer {token}",
            "-H", "Notion-Version: 2022-06-28",
            "-H", "Content-Type: application/json",
            "-w", r"\n%{http_code}",
            blocks_url
        ]
        
        proc2 = subprocess.run(cmd2, capture_output=True, timeout=65)
        out2 = proc2.stdout.decode("utf-8", errors="replace")
        
        if "\n" in out2:
            body2, code2_str = out2.rsplit("\n", 1)
            if code2_str.isdigit():
                code2 = int(code2_str)
            else:
                body2 = out2
                code2 = 0
        else:
            body2 = out2
            code2 = 0
        
        blocks = []
        all_text = []
        
        if code2 == 200:
            blocks_data = json_mod.loads(body2)
            for block in blocks_data.get("results", []):
                block_type = block.get("type", "")
                block_content = block.get(block_type, {})
                
                # 提取富文本
                rich_text_list = block_content.get("rich_text", []) or block_content.get("text", [])
                if not rich_text_list and "title" in block_content:
                    rich_text_list = block_content.get("title", [])
                
                text = "".join(t.get("plain_text", "") for t in rich_text_list)
                
                if text.strip():
                    all_text.append(text.strip())
                    
                blocks.append({
                    "type": block_type,
                    "id": block.get("id", ""),
                    "text": text.strip(),
                    "has_children": block.get("has_children", False)
                })
        
        full_text = "\n".join(all_text)
        
        return {
            "page_id": page_id,
            "title": title,
            "text": full_text,
            "blocks": blocks,
            "fetched_at": datetime.now().isoformat(),
            "source": "api"
        }
        
    except Exception as e:
        print(f"  ⚠️ API拉取异常 {page_id}: {e}")
        return None

def load_local_json_pages() -> Dict[str, str]:
    """直接加载本地JSON缓存(无需配置文件)"""
    texts = {}
    if not MIRROR_DIR.exists():
        return texts
    
    for f in MIRROR_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            page_id = data.get("page_id", f.stem)
            text = data.get("text", "")
            if text:
                texts[page_id] = text
        except:
            pass
    
    print(f"  📂 加载 {len(texts)} 个本地JSON缓存")
    return texts

def process_all_pages(use_api: bool = False) -> Dict[str, Any]:
    """处理所有页面，提取术语"""
    mappings = load_page_mappings()
    token = load_token() if use_api else None
    
    if use_api and token:
        print(f"  🔑 Notion Token: {token[:15]}... (API模式)")
    else:
        print(f"  📂 本地镜像模式 (不调用API)")
    
    all_terms = defaultdict(lambda: {
        "pages": [],      # 出现的页面ID列表
        "contexts": [],   # 上下文片段
        "first_seen": None
    })
    
    page_summary = []
    success = 0
    failed = 0
    
    # 先加载本地JSON缓存
    local_texts = load_local_json_pages()
    
    for i, mapping in enumerate(mappings):
        page_id = mapping.get("notion_page_id", "")
        page_name = mapping.get("name", "未命名")
        priority = mapping.get("priority", i)
        
        if not page_id:
            continue
        
        # 先尝试本地
        text = ""
        source = "cache"
        
        # 从JSON缓存加载
        cached = load_cached_page(page_id)
        if cached and cached.get("text"):
            text = cached["text"]
            source = "json_cache"
        
        # 如果本地无数据，从纯文本缓存加载
        if not text and page_id in local_texts:
            text = local_texts[page_id]
            source = "local_json"
        
        # API模式：尝试拉取（即使本地有也刷新）
        if use_api and token:
            fetched = fetch_page_api(page_id, token)
            if fetched and fetched.get("text"):
                text = fetched["text"]
                source = "api_fresh"
                # 保存到本地
                save_path = MIRROR_DIR / f"{page_id}.json"
                try:
                    save_path.write_text(json.dumps(fetched, ensure_ascii=False, indent=2))
                except:
                    pass
                time.sleep(0.3)  # 限流
        
        if text:
            terms = extract_terms_from_text(text)
            for term, contexts in terms.items():
                all_terms[term]["pages"].append(page_id)
                all_terms[term]["contexts"].extend(contexts)
                if all_terms[term]["first_seen"] is None:
                    all_terms[term]["first_seen"] = page_id
            
            page_summary.append({
                "page_id": page_id,
                "name": page_name,
                "priority": priority,
                "source": source,
                "term_count": len(terms),
                "text_length": len(text)
            })
            success += 1
            print(f"  ✅ [{i+1:2d}/{len(mappings)}] {page_name[:60]:60s} | {len(terms)}条术语 | {source}")
        else:
            failed += 1
            page_summary.append({
                "page_id": page_id,
                "name": page_name,
                "priority": priority,
                "source": "missing",
                "term_count": 0,
                "text_length": 0
            })
            print(f"  ❌ [{i+1:2d}/{len(mappings)}] {page_name[:60]:60s} | 无数据")
    
    # 去重上下文（每个术语最多保留5条）
    for term in all_terms:
        unique_ctx = list(set(all_terms[term]["contexts"]))[:5]
        all_terms[term]["contexts"] = unique_ctx
        all_terms[term]["page_count"] = len(set(all_terms[term]["pages"]))
    
    return {
        "meta": {
            "dna": "#龍芯⚡️丙午·辛未·乙酉·NOTION-TERM-EXTRACTOR-v1.0",
            "extracted_at": datetime.now().isoformat(),
            "total_pages": len(mappings),
            "success": success,
            "failed": failed,
            "total_terms": len(all_terms),
            "source": "api" if use_api else "local_cache"
        },
        "pages": page_summary,
        "terms": dict(all_terms)
    }

def build_registry_patch(result: Dict[str, Any]) -> Dict[str, Any]:
    """生成注册表v2.0扩展补丁"""
    terms = result.get("terms", {})
    pages = result.get("pages", [])
    
    # 构建页面ID→名称映射
    page_map = {p["page_id"]: p["name"] for p in pages}
    
    # 筛选高频术语（出现>=2页或>=3次）
    significant_terms = {}
    for term, info in terms.items():
        page_count = info.get("page_count", 0)
        ctx_count = len(info.get("contexts", []))
        if page_count >= 2 or ctx_count >= 3:
            p_names = [page_map.get(pid, pid) for pid in info.get("pages", [])[:5]]
            significant_terms[term] = {
                "notion_pages": list(set(p_names)),
                "contexts": info.get("contexts", [])[:3],
                "occurrence": page_count
            }
    
    # 按出现频率排序
    sorted_terms = sorted(significant_terms.items(), key=lambda x: x[1]["occurrence"], reverse=True)
    
    return {
        "meta": {
            "dna": "#龍芯⚡️丙午·辛未·乙酉·REGISTRY-PATCH-v2.0",
            "generated_at": datetime.now().isoformat(),
            "terms_count": len(sorted_terms),
            "source": "notion_knowledge_base_51_pages"
        },
        "new_terms": {t: v for t, v in sorted_terms[:200]},
        "all_terms_raw": {t: v for t, v in sorted_terms}
    }

def run(args):
    """主入口"""
    print(f"\n{'='*70}")
    print(f"🐉 龍魂·Notion知识库术语提取引擎 v1.0")
    print(f"{'='*70}\n")
    
    use_api = args.api
    full_mode = getattr(args, 'full', False)
    
    if full_mode:
        use_api = True
    
    # 1. 提取
    result = process_all_pages(use_api=use_api)
    
    # 2. 保存完整结果
    output_path = OUTPUT_DIR / "notion_term_index.json"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n  💾 完整结果已保存: {output_path}")
    
    # 3. 生成注册表补丁
    patch = build_registry_patch(result)
    patch_path = OUTPUT_DIR / "notion_term_registry_patch.json"
    patch_path.write_text(json.dumps(patch, ensure_ascii=False, indent=2))
    print(f"  📋 注册表补丁已保存: {patch_path}")
    
    # 4. 摘要
    meta = result["meta"]
    new_terms = patch.get("new_terms", {})
    
    print(f"\n{'='*70}")
    print(f"📊 提取摘要")
    print(f"{'='*70}")
    print(f"  页面总数: {meta['total_pages']}")
    print(f"  成功提取: {meta['success']} | 失败: {meta['failed']}")
    print(f"  提取术语: {meta['total_terms']} 条")
    print(f"  高频术语: {len(new_terms)} 条 (>=2页或>=3次)")
    print(f"  数据来源: {meta['source']}")
    print(f"\n  📈 高频术语 TOP 20:")
    print(f"  {'—' * 60}")
    for i, (term, info) in enumerate(list(new_terms.items())[:20], 1):
        pages = info.get("notion_pages", [])
        print(f"  {i:2d}. {term} ({info['occurrence']}页覆盖)")
    
    # 5. 如果--export，同时更新注册表
    if getattr(args, 'export', False):
        update_registry(patch)
    
    print(f"\n  完成 ✅")
    return result

def update_registry(patch: Dict[str, Any]):
    """将补丁合并到语义统一注册表"""
    registry_path = ROOT / "01_技能庫" / "semantic_unified_registry.json"
    if not registry_path.exists():
        print("  ⚠️ 注册表不存在，跳过更新")
        return
    
    registry = json.loads(registry_path.read_text())
    
    # 在NOTION分类下添加提取的术语
    notion_cat = registry.get("categories", {}).get("NOTION", {})
    notion_cat["extracted_terms_v1.0"] = {
        "scan_time": datetime.now().isoformat(),
        "total_terms_extracted": len(patch.get("new_terms", {})),
        "top_terms": list(patch.get("new_terms", {}).keys())[:50],
        "full_index_path": "data/notion_term_index/notion_term_registry_patch.json"
    }
    registry["categories"]["NOTION"] = notion_cat
    
    # 更新meta
    registry["meta"]["updated"] = datetime.now().isoformat()
    registry["meta"]["notion_terms_v1.0"] = "extracted"
    
    # 写回
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2))
    print(f"  ✅ 注册表已更新 (NOTION术语索引)")
    print(f"  💾 {registry_path}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(
        description="龍魂·Notion知识库术语提取引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                    # 从本地镜像提取
  %(prog)s --api              # API实时拉取+提取
  %(prog)s --full             # 本地+API全量
  %(prog)s --export           # 提取并导出到注册表
        """
    )
    p.add_argument("--api", action="store_true", help="通过Notion API实时拉取")
    p.add_argument("--full", action="store_true", help="本地+API全量模式")
    p.add_argument("--export", action="store_true", help="提取后自动更新注册表")
    
    args = p.parse_args()
    run(args)
