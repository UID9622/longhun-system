#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""深度扫描三个指定数据库，提取所有字段和空壳条目"""
import json, os, subprocess, sys, time
from pathlib import Path

HOME = Path.home()
ROOT = HOME / "longhun-system"
sys.path.insert(0, str(ROOT / "bin"))
from lh_secrets_loader import load_all
load_all(export_to_os=True)
TOKEN = os.environ.get("NOTION_TOKEN", "")

def api(endpoint, method="GET", payload=None):
    url = f"https://api.notion.com/v1{endpoint}"
    cmd = [
        "curl", "-s", "-S", "--max-time", "30",
        "-H", f"Authorization: Bearer {TOKEN}",
        "-H", "Notion-Version: 2022-06-28",
        "-H", "Content-Type: application/json",
    ]
    if method != "GET":
        cmd.extend(["-X", method])
    if payload:
        cmd.extend(["-d", json.dumps(payload, ensure_ascii=False)])
    cmd.extend(["-w", r"\nHTTP_CODE:%{http_code}", url])
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=35)
        out = proc.stdout.decode("utf-8", errors="replace")
        marker = "HTTP_CODE:"
        if marker not in out:
            return None
        body, code = out.rsplit(marker, 1)
        code = int(code.strip())
        if code >= 400:
            if code == 429:
                time.sleep(3)
                return api(endpoint, method, payload)
            print(f"  API {code}: {body[:200]}", file=sys.stderr)
            return None
        return json.loads(body.strip()) if body.strip() else {}
    except Exception as e:
        print(f"  API exception: {e}", file=sys.stderr)
        return None

# 三个数据库ID
DB_IDS = [
    "3367125a9c9f808a9692f0c6752e92fa",
    "77a2892fdb714c4e864b63b70b3be287",
    "baf3b574023e49c987eee620a811e70d",
]

OUT_DIR = ROOT / "data" / "notion_scan" / "deep_scan_3dbs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def ext_title(obj):
    for v in (obj.get("properties") or {}).values():
        if isinstance(v, dict) and v.get("type") == "title":
            return "".join(t.get("plain_text","") for t in v.get("title",[]))
    return "未命名"

def ext_prop_value(prop_val):
    """提取属性值"""
    if not prop_val:
        return None
    t = prop_val.get("type", "")
    if t == "title":
        return "".join(x.get("plain_text","") for x in prop_val.get("title",[]))
    elif t == "rich_text":
        return "".join(x.get("plain_text","") for x in prop_val.get("rich_text",[]))
    elif t == "select":
        s = prop_val.get("select")
        return s.get("name","") if s else None
    elif t == "multi_select":
        return [x.get("name","") for x in prop_val.get("multi_select",[])]
    elif t == "number":
        return prop_val.get("number")
    elif t == "date":
        d = prop_val.get("date")
        return d.get("start","") if d else None
    elif t == "checkbox":
        return prop_val.get("checkbox")
    elif t == "url":
        return prop_val.get("url")
    elif t == "email":
        return prop_val.get("email")
    elif t == "phone_number":
        return prop_val.get("phone_number")
    elif t == "formula":
        return str(prop_val.get("formula",{}))
    elif t == "relation":
        return [x.get("id","") for x in prop_val.get("relation",[])]
    elif t == "rollup":
        return str(prop_val.get("rollup",{}))
    elif t == "people":
        return [x.get("name","") for x in prop_val.get("people",[])]
    elif t == "files":
        return [x.get("name","") for x in prop_val.get("files",[])]
    elif t == "status":
        s = prop_val.get("status")
        return s.get("name","") if s else None
    return None

all_results = []

for db_idx, db_id in enumerate(DB_IDS):
    print(f"\n{'='*60}")
    print(f"📁 DB {db_idx+1}/3: {db_id}")
    print(f"{'='*60}")

    # 1. 获取数据库 schema
    db_info = api(f"/databases/{db_id}")
    if not db_info:
        print(f"  ❌ 无法获取数据库 {db_id}，跳过")
        continue
    time.sleep(0.3)

    db_title = ext_title(db_info)
    print(f"  标题: {db_title}")
    
    # 解析所有属性
    props = db_info.get("properties", {})
    prop_names = list(props.keys())
    prop_types = {k: props[k].get("type","?") for k in prop_names}
    print(f"  属性 ({len(props)}): {', '.join(f'{k}({v})' for k,v in prop_types.items())}")

    # 2. 查询所有条目
    entries = []
    cursor = None
    page_num = 1
    while True:
        payload = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        resp = api(f"/databases/{db_id}/query", "POST", payload)
        if not resp:
            break
        batch = resp.get("results", [])
        entries.extend(batch)
        print(f"  查询 p{page_num}: +{len(batch)} → total {len(entries)}")
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
        page_num += 1
        time.sleep(0.33)

    # 3. 分析每个条目
    entry_analysis = []
    for entry in entries:
        entry_id = entry.get("id","")
        entry_title = ext_title(entry)
        entry_url = entry.get("url","")
        entry_props = {}
        empty_fields = []
        
        for pname, ptype in prop_types.items():
            pv = entry.get("properties",{}).get(pname)
            val = ext_prop_value(pv)
            entry_props[pname] = {"type": ptype, "value": val}
            
            # 判断是否为空
            is_empty = val is None or val == "" or val == [] or val == "未命名"
            if is_empty:
                empty_fields.append(pname)

        entry_analysis.append({
            "id": entry_id,
            "title": entry_title,
            "url": entry_url,
            "properties": entry_props,
            "empty_fields": empty_fields,
            "empty_count": len(empty_fields),
            "is_shell": len(empty_fields) >= 3,  # 3个以上空字段 = 空壳
        })

    # 4. 统计
    total = len(entry_analysis)
    shells = [e for e in entry_analysis if e["is_shell"]]
    has_empty = [e for e in entry_analysis if e["empty_count"] > 0]
    
    print(f"\n  📊 统计:")
    print(f"     总条目: {total}")
    print(f"     有空字段: {len(has_empty)} ({100*len(has_empty)/total:.0f}%)" if total else "")
    print(f"     空壳(>=3空): {len(shells)} ({100*len(shells)/total:.0f}%)" if total else "")

    # 列出空壳
    if shells:
        print(f"\n  🐚 空壳条目:")
        for s in shells[:20]:
            print(f"     - [{s['empty_count']}空] {s['title'][:60]} → {', '.join(s['empty_fields'][:5])}")

    # 列出每个属性的空值率
    print(f"\n  📉 各属性空值率:")
    for pname in prop_names:
        empty_n = sum(1 for e in entry_analysis if pname in e["empty_fields"])
        print(f"     {pname}({prop_types[pname]}): {empty_n}/{total} 空 ({100*empty_n/total:.0f}%)" if total else f"     {pname}: N/A")

    all_results.append({
        "db_id": db_id,
        "db_title": db_title,
        "db_url": f"https://www.notion.so/uid9622/{db_id}",
        "properties": {k: {"type": props[k].get("type","?"), "name": k} for k in prop_names},
        "total_entries": total,
        "empty_entries": len(has_empty),
        "shell_entries": len(shells),
        "entries": entry_analysis,
    })

# 保存结果
output = {
    "scan_time": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "dna": f"#龍芯⚡️{time.strftime('%Y%m%d-%H%M%S')}-DEEP-SCAN-3DBS-v1",
    "databases": all_results,
    "summary": {
        "total_dbs": len(all_results),
        "total_entries": sum(r["total_entries"] for r in all_results),
        "total_shells": sum(r["shell_entries"] for r in all_results),
    }
}

out_path = OUT_DIR / "deep_scan_result.json"
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))
print(f"\n{'='*60}")
print(f"✅ 深度扫描完成!")
print(f"   数据库: {len(all_results)}")
print(f"   总条目: {output['summary']['total_entries']}")
print(f"   空壳: {output['summary']['total_shells']}")
print(f"   保存至: {out_path}")
print(f"{'='*60}")
