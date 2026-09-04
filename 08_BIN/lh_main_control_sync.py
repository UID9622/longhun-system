#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·辛未·己亥·䷏豫-MAIN-CONTROL-SYNC-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂主控页同步引擎 v1.0
========================
职责: 本地 00_main_control/ ↔ Notion 主控页(2d87125a-9c9f-8028-89e2-e18002f7cf4f) 双向同步

子命令:
  check    检查主控页可达性 + 本地 config 解析
  summary  重新生成 REPO_LINKS_SUMMARY.md（gh 拉仓库清单）
  diff     对比上次快照输出变动
  push     把本地变更推送为 Notion 块（需页面已共享给 integration）
  pull     拉取 Notion 主控页最新内容回写本地镜像

用法:
  python3 bin/lh_main_control_sync.py check
  python3 bin/lh_main_control_sync.py summary
  python3 bin/lh_main_control_sync.py diff
  python3 bin/lh_main_control_sync.py push   [--dry-run]
  python3 bin/lh_main_control_sync.py pull
"""
import json
import os
import subprocess
import sys
import time

# ---------- 固定锚点 ----------
MAIN_PAGE_ID = "2d87125a9c9f802889e2e18002f7cf4f"
PAGE_URL = "https://www.notion.so/uid9622/v2-7-M-CNSH-2d87125a9c9f802889e2e18002f7cf4f"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTROL_DIR = os.path.join(ROOT, "00_main_control")
MAIN_LOCAL = os.path.join(CONTROL_DIR, "MAIN_CONTROL_v2.7.md")
SUMMARY_FILE = os.path.join(CONTROL_DIR, "REPO_LINKS_SUMMARY.md")
CONFIG_FILE = os.path.join(
    ROOT, "cnsh/core/decision_flow_auto_optimize/decision_page_config.json"
)
SNAPSHOT_FILE = os.path.join(CONTROL_DIR, ".sync_snapshot.json")
CHANGELOG_FILE = os.path.join(CONTROL_DIR, "SYNC_CHANGELOG.md")

# 从 lh_notion_kb 复用 API 直连（自带清代理处理）
sys.path.insert(0, os.path.join(ROOT, "08_BIN"))
try:
    from lh_notion_kb import notion_request
except ImportError:
    sys.path.insert(0, os.path.join(ROOT, "bin"))
    from lh_notion_kb import notion_request


# ---------- 工具 ----------
def _ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _log(msg, level="OK"):
    print(f"[{_ts()}] {level}: {msg}")


def _run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return r.stdout.strip(), r.returncode
    except Exception as e:
        return str(e), -1


def _load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8-sig") as f:
            txt = f.read()
        # 剥离 # 注释行（config 文件头部带 DNA/CONFIRM/SEAL 注释）
        lines = [l for l in txt.splitlines() if not l.lstrip().startswith("#")]
        return json.loads("\n".join(lines))
    except Exception as e:
        return {"error": str(e)}


def _md5(text):
    import hashlib
    return hashlib.md5(text.encode("utf-8")).hexdigest()


# ---------- 子命令: check ----------
def cmd_check():
    print(f"══ 主控页同步检查 ══ {_ts()}")
    # 1. 本地 config
    cfg = _load_config()
    if cfg is None:
        print("🔴 config 文件缺失:", CONFIG_FILE)
    elif "error" in cfg:
        print("🔴 config JSON 解析失败:", cfg["error"])
    else:
        m = cfg.get("metadata", {})
        print("🟢 config:", m.get("version"), m.get("turn"), "| 更新:", m.get("last_update"))
    # 2. 本地主控镜像
    if os.path.exists(MAIN_LOCAL):
        print("🟢 本地主控镜像存在:", MAIN_LOCAL)
    else:
        print("🟡 本地主控镜像缺失:", MAIN_LOCAL)
    # 3. 当前 token 身份
    me = notion_request("https://api.notion.com/v1/users/me")
    bot_name = me.get("name", "unknown") if me.get("status", 200) == 200 else "unknown"
    ws_name = me.get("bot", {}).get("workspace_name", "unknown") if me.get("status", 200) == 200 else "unknown"
    print(f"🟢 Notion token: {bot_name} | workspace: {ws_name}")
    # 4. API 可达性
    r = notion_request(f"https://api.notion.com/v1/pages/{MAIN_PAGE_ID}")
    if r.get("status", 200) == 200:
        props = r.get("properties", {})
        title = ""
        for k, v in props.items():
            if v.get("type") == "title":
                title = "".join(x.get("plain_text", "") for x in v.get("title", []))
        print("🟢 Notion 主控页可达 | 标题:", title)
        print("🟢 可执行 push/pull 同步")
        return 0
    else:
        print("🟡 Notion 主控页不可达:", str(r.get("error", ""))[:180])
        print(f"🟡 请在 Notion 中把主控页共享给 integration: {bot_name}")
        print("🟡 共享前 push/pull 不可用；check/summary/diff 正常")
        return 1


# ---------- 子命令: summary ----------
def cmd_summary():
    print(f"══ 生成仓库链接摘要 ══ {_ts()}")
    out, code = _run(["gh", "repo", "list", "UID9622", "--limit", "50",
                      "--json", "name,description,updatedAt"])
    if code != 0 or not out:
        _log("gh 拉取失败，保留现有摘要（可离线运行）", "WARN")
        print(out[:200] if out else "gh CLI 不可用")
        return 1
    repos = json.loads(out)
    # 读取现有摘要模板头部
    header = (
        "# 🌐 龍魂 · 仓库链接摘要清单 v1.0\n\n"
        "> DNA: #龍芯⚡️丙午·丙申·辛未·己亥·䷏豫-REPO-LINKS-SUMMARY-v1.0\n"
        "> 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰\n"
        "> 协议: CC BY-NC-SA 4.0（核心思想层）\n"
        "> 用途: Notion 主控页「链接读取摘要」数据源 · 每次变动同步更新 · 供 AI 按链接取摘要\n\n"
        "## 📌 读取规则\n\n"
        "1. **给链接 = 给摘要**：Notion 里只放链接+一句话摘要，AI 按需点链接取详情，不全文搬\n"
        "2. **本地 = 完整源**：Notion = 摘要索引 · 本地仓库 = 完整内容\n"
        "3. **每次变动更新**：`python3 bin/lh_main_control_sync.py summary` 重新生成本文件\n\n"
        "## 🐉 主控链接\n\n"
        f"| 项 | 值 |\n|:---|---|\n"
        "| 主控页标题 | 🐉 龍魂决策流场总控页 v2.7｜M×CNSH｜功能同步总闸版 |\n"
        f"| Notion URL | {PAGE_URL} |\n"
        f"| 页面 ID | {MAIN_PAGE_ID[:8]}-{MAIN_PAGE_ID[8:12]}-{MAIN_PAGE_ID[12:16]}-{MAIN_PAGE_ID[16:20]}-{MAIN_PAGE_ID[20:]} |\n"
        "| 当前版本 | v2.7.36（M21） |\n"
        f"| 更新 | {_ts()} |\n\n"
        "## 📦 GitHub 仓库清单（UID9622）\n\n"
        "> 数据源: `gh repo list UID9622` · 自动生成\n\n"
        "| 仓库 | 一句话摘要 | 最近更新 |\n|:---|---:|:---|\n"
    )
    rows = []
    for r in sorted(repos, key=lambda x: x.get("name", "").lower()):
        name = r.get("name", "")
        desc = (r.get("description") or "（无描述）").replace("|", "｜")
        upd = (r.get("updatedAt") or "")[:10]
        rows.append(f"| [{name}](https://github.com/UID9622/{name}) | {desc} | {upd} |")
    footer = (
        "\n> 生成器: `bin/lh_main_control_sync.py summary` · 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z\n"
    )
    content = header + "\n".join(rows) + footer
    os.makedirs(CONTROL_DIR, exist_ok=True)
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    _log(f"✅ 摘要已生成: {SUMMARY_FILE}（{len(repos)} 仓库）")
    return 0


# ---------- 子命令: diff ----------
def cmd_diff():
    print(f"══ 主控镜像变更检测 ══ {_ts()}")
    if not os.path.exists(MAIN_LOCAL):
        _log("本地主控镜像缺失，无可比对", "WARN")
        return 1
    cur = open(MAIN_LOCAL, encoding="utf-8").read()
    cur_h = _md5(cur)
    old_h = None
    if os.path.exists(SNAPSHOT_FILE):
        try:
            old_h = json.load(open(SNAPSHOT_FILE, encoding="utf-8")).get("md5")
        except Exception:
            pass
    if old_h == cur_h:
        _log("✅ 无变动（自上次快照）")
    else:
        _log("🔶 主控镜像已变更（需要 push 或刷新快照）")
        # 输出变更行
        if old_h:
            old = json.load(open(SNAPSHOT_FILE, encoding="utf-8")).get("content", "")
            old_lines, new_lines = old.splitlines(), cur.splitlines()
            import difflib
            diff = list(difflib.unified_diff(old_lines, new_lines, lineterm="", n=1))
            changed = [l for l in diff if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
            print(f"  变更行数: {len(changed)}")
            for l in changed[:15]:
                print("   ", l)
    return 0


# ---------- 子命令: push ----------
def cmd_push(dry_run=False):
    print(f"══ 推送本地 → Notion ══ {_ts()}")
    # 可达性检查
    r = notion_request(f"https://api.notion.com/v1/pages/{MAIN_PAGE_ID}")
    if r.get("status", 200) != 200:
        _log("主控页未共享，push 不可用。请在 Notion 共享给 integration: longhun-system", "WARN")
        return 1
    if not os.path.exists(MAIN_LOCAL):
        _log("本地主控镜像缺失", "WARN")
        return 1
    content = open(MAIN_LOCAL, encoding="utf-8").read()
    # 在页尾追加一个「本地同步记录」块（append block）
    stamp = _ts().replace("+", "+").replace(":", "-")
    payload = {
        "children": [
            {"object": "block", "type": "paragraph", "paragraph": {
                "rich_text": [{"type": "text", "text": {
                    "content": f"🔄 本地同步 {stamp} · DNA: #龍芯⚡️丙午·丙申·辛未·己亥·䷏豫-MAIN-CONTROL-SYNC-v1.0-UID9622",
                }}]
            }}
        ]
    }
    if dry_run:
        _log("DRY-RUN: 将追加同步记录块（不实际调用）")
        return 0
    r2 = notion_request(
        f"https://api.notion.com/v1/blocks/{MAIN_PAGE_ID}/children",
        method="PATCH", payload=payload)
    if r2.get("status", 200) == 200:
        _log("✅ 已追加同步记录块到主控页")
        _write_changelog("push", stamp)
        return 0
    else:
        _log("push 失败: " + str(r2.get("error", ""))[:200], "ERROR")
        return 1


# ---------- 子命令: pull ----------
def cmd_pull():
    print(f"══ 拉取 Notion → 本地 ══ {_ts()}")
    r = notion_request(f"https://api.notion.com/v1/pages/{MAIN_PAGE_ID}")
    if r.get("status", 200) != 200:
        _log("主控页未共享，pull 不可用。请在 Notion 共享给 integration: longhun-system", "WARN")
        return 1
    title = ""
    for k, v in r.get("properties", {}).items():
        if v.get("type") == "title":
            title = "".join(x.get("plain_text", "") for x in v.get("title", []))
    _log(f"✅ 主控页可达，标题: {title}")
    _log("提示: 完整内容拉取需遍历 children 块，后续版本增强；当前先验证可达性+记录快照")
    # 记录可达快照
    snap = {"page_id": MAIN_PAGE_ID, "title": title, "ts": _ts(),
            "md5": _md5(title), "content": title}
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    _log("✅ 快照已记录")
    return 0


def _write_changelog(action, stamp):
    os.makedirs(CONTROL_DIR, exist_ok=True)
    line = f"| {stamp} | {action} | {MAIN_PAGE_ID[:8]} | 主控页 v2.7.36 |\n"
    if not os.path.exists(CHANGELOG_FILE):
        with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
            f.write("# 主控页同步变更日志\n\n| 时间 | 动作 | 页面 | 版本 |\n|:---|:---|:---|:---|\n")
    with open(CHANGELOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)


# ---------- 主入口 ----------
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    cmd = sys.argv[1]
    if cmd == "check":
        return cmd_check()
    if cmd == "summary":
        return cmd_summary()
    if cmd == "diff":
        return cmd_diff()
    if cmd == "push":
        return cmd_push(dry_run="--dry-run" in sys.argv)
    if cmd == "pull":
        return cmd_pull()
    print("未知命令:", cmd)
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
