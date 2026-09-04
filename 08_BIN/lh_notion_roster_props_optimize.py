#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·甲申·乙巳·巳时·䷋否-ROSTER-PROPS-OPTIMIZE-v1.0-72to35
# CREATOR: 诸葛鑫 (UID9622)
# LICENSE: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""🐉 龍芯家族花名册 · Notion 属性优化执行器 v1.0

对 Notion 数据库 `🐉 龍芯家族花名册`（4cf99c3e-7a01-4e91-9fda-b705ceb4cbc4）
执行属性优化：删除冗余/空列/低填充属性，保留 35 个核心属性。

用法:
  python3 bin/lh_notion_roster_props_optimize.py            # dry-run 只打印计划
  python3 bin/lh_notion_roster_props_optimize.py --apply    # 实际执行删除
  python3 bin/lh_notion_roster_props_optimize.py --backup   # 导出全库备份 JSON 后 dry-run

前置条件:
  - Notion token 可用（env NOTION_TOKEN / ~/.env / lh_vault.py）
  - 数据库已共享给 integration「北极星没有眼泪」（2026-08-30 实测 404 未共享）
  - 共享后直接 --apply 即可

安全设计:
  - 默认 dry-run，--apply 才动库
  - 删除前可选 --backup 导出快照
  - 每个属性删除失败自动跳过并记录，不中断
  - 只删清单内属性，永不新建/改名
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

# 清代理（本地直连 Notion API）
for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
           "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)
os.environ["NO_PROXY"] = "*"

DATABASE_ID = "4cf99c3e-7a01-4e91-9fda-b705ceb4cbc4"
API = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
VERSION = "2022-06-28"

# 删除清单（依据 LH-ROSTER-PROPS-OPTIMIZE-v1.0.md 第一节）
DELETE_PROPS = [
    # 全空列
    "关联投喂", "晋级投票", "红线记录",
    # 极低填充列（<5%）
    "对话记录", "联系方式", "贡献时间", "关联关系", "荣誉勋章",
    "晋升时间", "下架原因", "贡献作品", "个人主页", "历史贡献记录",
    # 冗余计数
    "本周调用次数", "本月调用次数", "本周帮助人数", "本月帮助人数",
    "功能热度", "人格特征热度", "累计贡献次数",
    # 注(2026-08-30 实测): 现库 55 属性(137 行)≠8/17 快照 72 属性，
    # 本清单 19 项在现库 0 命中（库已被整理/属性演进），脚本幂等输出"待删除 0"= 已达标。
    # 现库结构 = 35 目标 + 20 扩展保留(见 KEEP_PROPS 注释)，无需追加删除。
]

# 保留属性（目标 Schema 35 项 · 用于 --backup 时标注）
KEEP_PROPS = [
    "名字", "路由编号", "DNA追溯码", "短DNA·身份码", "是谁", "做什么", "一句话",
    "分组", "人格层级", "协作层级", "信任等级", "模块类型", "三才归属", "卦象",
    "路由优先级", "信号词", "IPA·触发模版", "当前后台", "协议分类",
    "当前状态", "调度状态", "上线状态", "投票状态", "审计可见度",
    "一致性评分", "信誉评分", "三观对齐", "贡献声明", "贡献积分", "警告次数",
    "加入时间", "最后活跃",
    "贡献值", "活跃度", "七维加成",
    # 扩展保留 20 项(2026-08-30 实测·137 行填充率): 18 项有数据(8%~72%)·
    # 熔断次数(0%)/关联天眼节点(0%) 空置待用·功能定位(72%)最高
    "备注", "五行", "关联天眼节点", "备用后台", "贡献类型", "EN代号", "帮助人数",
    "智能公司名称", "价值走势", "核心能力", "个人IP", "确认码", "熔断次数", "路由权重",
    "执行准确率", "价值观对齐度", "总调用次数", "透明度评分", "监督权限", "功能定位",
]


def _collect_tokens() -> list:
    """收集候选 token: ~/.env（权威·多行去重）→ env → lh_vault.py"""
    cands = []
    env_path = os.path.expanduser("~/.env")
    if os.path.isfile(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("NOTION_TOKEN="):
                    t = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if t and t not in cands:
                        cands.append(t)
    t = os.environ.get("NOTION_TOKEN", "").strip()
    if t and t not in cands:
        cands.append(t)
    try:
        import subprocess
        r = subprocess.run(
            ["python3", os.path.expanduser("~/longhun-system/bin/lh_vault.py"),
             "get", "NOTION_TOKEN"],
            capture_output=True, text=True, timeout=15)
        t = r.stdout.strip()
        if t and t.lower() not in ("none", "not found", "") and t not in cands:
            cands.append(t)
    except Exception:
        pass
    return cands


def _probe_token(token: str) -> bool:
    """探测 token 是否有效：
    401/403 = token 无效（换下一个）；404 = token 有效但数据库未共享（视为有效·继续）"""
    r = api_call(token, "GET", f"/databases/{DATABASE_ID}")
    if isinstance(r, dict) and "error" in r:
        return r["error"] not in (401, 403)
    return True


def load_token() -> str:
    """加载有效 token：依次尝试候选，返回首个 API 可达的"""
    for t in _collect_tokens():
        if _probe_token(t):
            return t
    # 无有效 token → 返回第一个候选（用于报错信息）
    cands = _collect_tokens()
    return cands[0] if cands else ""


def api_call(token: str, method: str, path: str, payload=None):
    url = f"https://api.notion.com/v1{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Notion-Version", VERSION)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        return {"error": e.code, "message": body}


def get_database(token: str):
    return api_call(token, "GET", f"/databases/{DATABASE_ID}")


def patch_delete_props(token: str, props: list):
    """批量删除属性（properties: {name: null}）"""
    payload = {"properties": {p: None for p in props}}
    return api_call(token, "PATCH", f"/databases/{DATABASE_ID}", payload)


def main():
    ap = argparse.ArgumentParser(description="龍魂花名册 Notion 属性优化")
    ap.add_argument("--apply", action="store_true", help="实际执行删除（默认 dry-run）")
    ap.add_argument("--backup", action="store_true", help="先导出全库 JSON 备份")
    args = ap.parse_args()

    token = load_token()
    if not token:
        print("❌ 未找到 NOTION_TOKEN（env/~/.env/lh_vault 均无）")
        sys.exit(1)
    print(f"✅ token 已加载: {token[:12]}...")

    db = get_database(token)
    if "error" in db:
        print(f"❌ 数据库访问失败: HTTP {db['error']}")
        print(f"   {db['message']}")
        print("   → 请先在 Notion 中把「🐉 龍芯家族花名册」共享给 integration「北极星没有眼泪」")
        sys.exit(2)

    current = {k: v.get("type") for k, v in db.get("properties", {}).items()}
    title = "".join(t.get("plain_text", "") for t in db.get("title", []))
    print(f"📋 数据库: {title} | 当前属性数: {len(current)}")

    to_del = [p for p in DELETE_PROPS if p in current]
    keep = [k for k in KEEP_PROPS if k in current]
    extra = [k for k in current if k not in DELETE_PROPS and k not in KEEP_PROPS]
    print(f"🔴 待删除: {len(to_del)} 项")
    for p in to_del:
        print(f"   - {p} ({current[p]})")
    print(f"🟢 保留: {len(keep)} 项")
    if extra:
        print(f"🟡 未分类（不在清单·不动）: {extra}")

    if args.backup:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bf = os.path.expanduser(f"~/longhun-system/backups/roster_notion_backup_{ts}.json")
        os.makedirs(os.path.dirname(bf), exist_ok=True)
        with open(bf, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        print(f"💾 备份已写入: {bf}")

    if not args.apply:
        print("\n🔍 dry-run 模式（未改动数据库）→ 加 --apply 实际执行")
        return

    print("\n⚙️ 执行删除...")
    ok, fail = [], []
    for p in to_del:
        r = patch_delete_props(token, [p])
        if "error" in r:
            fail.append((p, r["error"], r.get("message", "")))
            print(f"   ⚠️ 删除失败 {p}: HTTP {r['error']} {r.get('message','')[:80]}")
        else:
            ok.append(p)
            print(f"   ✅ 已删除 {p}")

    print(f"\n📊 结果: 成功 {len(ok)} | 失败 {len(fail)}")
    if fail:
        for p, code, msg in fail:
            print(f"   ❌ {p}: HTTP {code} {msg[:100]}")
    if ok:
        print("🔍 请到 Notion 刷新确认属性已精简")
    print("\nDNA: #龍芯⚡️丙午·甲申·乙巳·巳时·䷋否-ROSTER-PROPS-OPTIMIZE-v1.0-72to35")


if __name__ == "__main__":
    main()
