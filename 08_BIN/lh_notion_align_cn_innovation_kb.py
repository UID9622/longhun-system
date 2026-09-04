#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_NOTION_ALIGN_CN_I-E43411EB
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·辛酉·申时·☰乾-NOTION-CN-INNOVATION-KB-ALIGN-v1.0
"""
🐉 龍魂 · 中国科技自主创新专栏知识库对齐脚本

将本地 skills/longhun-cn-innovation-kb/scripts/cn_innovation_kb.json 的 45 条记录
与 Notion 数据库「🇨🇳 中国科技自主创新专栏｜知识库」对齐：
- 补全缺失的库字段
- 补全缺失的文章
- 更新已有文章的字段
"""

import json
import time
from datetime import datetime
from pathlib import Path

import requests


CHECKPOINT_PATH = Path.home() / ".longhun" / ".notion_align_cn_inno_progress.json"
MAX_RETRIES = 5
BASE_DELAY = 1.0


NOTION_VERSION = "2022-06-28"
API_BASE = "https://api.notion.com/v1"
DB_ID = "baf3b574023e49c987eee620a811e70d"
JSON_PATH = Path.home() / ".kimi-code" / "skills" / "longhun-cn-innovation-kb" / "scripts" / "cn_innovation_kb.json"


def get_token() -> str:
    cfg_path = Path(__file__).resolve().parent.parent / "config" / "notion_config.json"
    data = json.load(open(cfg_path, encoding="utf-8"))
    return data.get("notion_token") or data.get("token")


def headers() -> dict:
    return {
        "Authorization": f"Bearer {get_token()}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def load_checkpoint() -> int:
    if CHECKPOINT_PATH.exists():
        try:
            return json.load(open(CHECKPOINT_PATH, encoding="utf-8")).get("last_index", 0)
        except Exception:
            return 0
    return 0


def save_checkpoint(idx: int):
    CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CHECKPOINT_PATH, "w", encoding="utf-8") as f:
        json.dump({"last_index": idx, "timestamp": datetime.now().isoformat()}, f)


def request_with_retry(method: str, url: str, **kwargs):
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.request(method, url, **kwargs)
            if r.status_code == 429:
                delay = BASE_DELAY * (2 ** attempt)
                print(f"    ⏳ 触发 Notion 速率限制，等待 {delay}s 后重试 ({attempt+1}/{MAX_RETRIES})")
                time.sleep(delay)
                continue
            return r
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            delay = BASE_DELAY * (2 ** attempt)
            print(f"    ⏳ 网络异常，{delay}s 后重试 ({attempt+1}/{MAX_RETRIES}): {e.__class__.__name__}")
            time.sleep(delay)
    raise RuntimeError(f"请求 {method} {url} 在 {MAX_RETRIES} 次重试后仍失败")


def guard(text: str) -> str:
    return text.replace("龙", "龍")


def rich_text(text: str):
    return {"rich_text": [{"text": {"content": guard(text or "")}}]}


def title(text: str):
    return {"title": [{"text": {"content": guard(text or "")}}]}


def select(name: str):
    if not name:
        return {"select": None}
    return {"select": {"name": name}}


def status(name: str):
    if not name:
        return {"status": None}
    return {"status": {"name": name}}


def multi_select(names: list):
    if not names:
        return {"multi_select": []}
    return {"multi_select": [{"name": n} for n in names]}


def load_kb() -> list:
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_db_schema() -> dict:
    r = request_with_retry("GET", f"{API_BASE}/databases/{DB_ID}", headers=headers())
    r.raise_for_status()
    return r.json()


def update_db_schema(schema: dict, kb: list):
    """确保数据库有龍魂标准字段 + 所有选项。"""
    props = schema.get("properties", {})
    additions = {}

    # 1. 添加缺失属性
    if "dr·五行·宫位" not in props:
        additions["dr·五行·宫位"] = {"rich_text": {}}
    if "α三义" not in props:
        additions["α三义"] = {"rich_text": {}}
    if "短DNA·身份码" not in props:
        additions["短DNA·身份码"] = {"rich_text": {}}
    if "人格路由" not in props:
        personas = sorted({p for r in kb for p in r.get("人格路由", []) if p})
        additions["人格路由"] = {"multi_select": {"options": [{"name": p} for p in personas]}}
    if "架构层级" not in props:
        levels = ["🧱 Core（宇宙规则层）", "⚙️ Engine（引擎骨架层）", "📦 Application（应用层）", "🧬 CNSH专属层"]
        additions["架构层级"] = {"select": {"options": [{"name": l} for l in levels]}}

    # 2. 补全已有属性的选项
    # 内容标签
    if "内容标签" in props:
        existing = {o["name"] for o in props["内容标签"].get("multi_select", {}).get("options", [])}
        needed = sorted({t for r in kb for t in r.get("内容标签", []) if t})
        missing = [t for t in needed if t not in existing]
        if missing:
            additions["内容标签"] = {"multi_select": {"options": [{"name": t} for t in missing]}}

    # 人格路由（如果已存在）
    if "人格路由" in props and "人格路由" not in additions:
        existing = {o["name"] for o in props["人格路由"].get("multi_select", {}).get("options", [])}
        needed = sorted({p for r in kb for p in r.get("人格路由", []) if p})
        missing = [p for p in needed if p not in existing]
        if missing:
            additions["人格路由"] = {"multi_select": {"options": [{"name": p} for p in missing]}}

    if not additions:
        print("  ✅ 数据库字段已对齐，无需新增")
        return

    r = request_with_retry("PATCH", f"{API_BASE}/databases/{DB_ID}", headers=headers(), json={"properties": additions})
    if r.status_code == 200:
        print(f"  ✅ 已更新数据库字段: {list(additions.keys())}")
    else:
        print(f"  ❌ 更新数据库字段失败: {r.status_code} {r.text[:200]}")


def query_all_pages() -> dict:
    """返回 title -> page_id 映射。"""
    results = []
    next_cursor = None
    while True:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor
        r = request_with_retry("POST", f"{API_BASE}/databases/{DB_ID}/query", headers=headers(), json=payload)
        r.raise_for_status()
        data = r.json()
        results.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        next_cursor = data.get("next_cursor")

    mapping = {}
    for p in results:
        props = p.get("properties", {})
        for v in props.values():
            if v.get("type") == "title":
                title_text = "".join(t.get("plain_text", "") for t in v.get("title", [])).strip()
                if title_text:
                    mapping[title_text] = p["id"]
                break
    return mapping


def build_properties(record: dict) -> dict:
    properties = {
        "专栏标题": title(record.get("专栏标题", "")),
        "领域分类": select(record.get("领域分类", "")),
        "重要程度": select(record.get("重要程度", "")),
        "状态": status(record.get("状态", "")),
        "来源": select(record.get("来源", "")),
        "一句话摘要": rich_text(record.get("一句话摘要", "")),
        "底层逻辑": rich_text(record.get("底层逻辑", "")),
        "易经锚点": rich_text(record.get("易经锚点", "")),
        "DNA追溯码": rich_text(record.get("DNA追溯码", "")),
        "IPA·触发": rich_text(record.get("IPA·缩写", "")),
        "dr·五行·宫位": rich_text(record.get("dr·五行·宫位", "")),
        "α三义": rich_text(record.get("α三义", "")),
        "短DNA·身份码": rich_text(record.get("短DNA·身份码", "")),
        "内容标签": multi_select(record.get("内容标签", [])),
        "人格路由": multi_select(record.get("人格路由", [])),
        "架构层级": select(record.get("架构层级", "")),
    }
    return properties


def patch_page(page_id: str, record: dict):
    payload = {"properties": build_properties(record)}
    r = request_with_retry("PATCH", f"{API_BASE}/pages/{page_id}", headers=headers(), json=payload)
    return r.status_code, r.text


def create_page(record: dict):
    payload = {
        "parent": {"database_id": DB_ID},
        "properties": build_properties(record),
    }
    r = request_with_retry("POST", f"{API_BASE}/pages", headers=headers(), json=payload)
    return r.status_code, r.text


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🐉 开始对齐中国科技自主创新专栏知识库...")
    kb = load_kb()
    print(f"  本地记录: {len(kb)} 条")

    print("  检查数据库字段...")
    schema = get_db_schema()
    update_db_schema(schema, kb)

    print("  拉取 Notion 现有页面...")
    existing = query_all_pages()
    print(f"  Notion 现有: {len(existing)} 条有标题的页面")

    last_ok = load_checkpoint()
    if last_ok:
        print(f"  检测到断点，从第 {last_ok + 1} 条继续（前 {last_ok} 条已处理）")

    created = 0
    updated = 0
    failed = 0
    for i, record in enumerate(kb, 1):
        if i <= last_ok:
            continue

        title_text = record.get("专栏标题", "").strip()
        if not title_text:
            print(f"  ⚠️ 第 {i} 条记录无标题，跳过")
            save_checkpoint(i)
            continue

        if title_text in existing:
            status_code, text = patch_page(existing[title_text], record)
            if status_code == 200:
                updated += 1
                print(f"  ✅ 更新 ({i}/{len(kb)}): {title_text[:40]}")
                save_checkpoint(i)
            else:
                failed += 1
                print(f"  ❌ 更新失败 ({i}/{len(kb)}): {title_text[:40]} | {status_code} {text[:80]}")
                break
        else:
            status_code, text = create_page(record)
            if status_code == 200:
                created += 1
                print(f"  ✅ 新建 ({i}/{len(kb)}): {title_text[:40]}")
                save_checkpoint(i)
            else:
                failed += 1
                print(f"  ❌ 新建失败 ({i}/{len(kb)}): {title_text[:40]} | {status_code} {text[:80]}")
                break
        time.sleep(0.5)

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 阶段结果: 新建 {created} 条, 更新 {updated} 条, 失败 {failed} 条 | 断点: {load_checkpoint()}/{len(kb)}")


if __name__ == "__main__":
    main()
