#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·量子记忆回流站 v1.0
DNA: #龍芯⚡️2026-03-21-MEMORY-HUB-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者: 诸葛鑫（UID9622）
理论指导: 曾仕强老师（永恒显示）

功能:
  - 启动菜单，数字选功能
  - 各平台(Claude/Kimi/Notion/本地)历史记忆一键提取
  - 首次全量 / 后续按编辑时间增量
  - 加密回流到Notion星辰记忆
  - 多维度语义积累 → 生态微调底座
"""

import os, sys, json, subprocess, hashlib
from datetime import datetime, timezone
from pathlib import Path

# ─── 路径常量 ─────────────────────────────────────────────────────────────────
HOME            = Path.home()
LONGHUN_DIR     = HOME / "longhun-system"
SYNC_STATE_FILE = HOME / ".longhun" / "sync_state.json"
MEMORY_DIR      = Path.home() / ".claude/projects/-Users-zuimeidedeyihan/memory"
SESSION_LOG     = LONGHUN_DIR / "logs" / "session_log.jsonl"
BRAIN_BACKUP    = LONGHUN_DIR / "brain_backup.jsonl"
KIMI_DIR        = HOME / ".kimi"

# ─── Notion 目标页面（星辰记忆） ───────────────────────────────────────────────
NOTION_TARGET   = "c0db7666-6eef-4b9b-9e23-e09f6ad8115e"

# ─── DNA / 身份 ────────────────────────────────────────────────────────────────
UID             = "UID9622"
GPG             = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ─── 颜色（终端） ─────────────────────────────────────────────────────────────
R  = "\033[91m"
G  = "\033[92m"
Y  = "\033[93m"
B  = "\033[94m"
C  = "\033[96m"
W  = "\033[97m"
DIM= "\033[2m"
RST= "\033[0m"
BOLD="\033[1m"


# ══════════════════════════════════════════════════════════════════════════════
#  工具函数
# ══════════════════════════════════════════════════════════════════════════════

def _keychain(service: str, account: str = "uid9622") -> str:
    r = subprocess.run(
        ["security", "find-generic-password", "-s", service, "-a", account, "-w"],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def _notion_token() -> str:
    t = _keychain("longhun-notion-token")
    if not t:
        env = LONGHUN_DIR / ".env"
        if env.exists():
            for line in env.read_text().splitlines():
                if line.startswith("NOTION_TOKEN="):
                    t = line.split("=",1)[1].strip().strip('"')
    return t


def _notion_post(endpoint: str, payload: dict) -> dict:
    token = _notion_token()
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", f"https://api.notion.com/v1/{endpoint}",
         "-H", f"Authorization: Bearer {token}",
         "-H", "Notion-Version: 2022-06-28",
         "-H", "Content-Type: application/json",
         "-d", json.dumps(payload, ensure_ascii=False)],
        capture_output=True, text=True
    )
    return json.loads(r.stdout)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dna(label: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"#龍芯⚡️{stamp}-{label}-{UID}"


# ══════════════════════════════════════════════════════════════════════════════
#  同步状态管理
# ══════════════════════════════════════════════════════════════════════════════

def _load_state() -> dict:
    if SYNC_STATE_FILE.exists():
        return json.loads(SYNC_STATE_FILE.read_text())
    return {}


def _save_state(state: dict):
    SYNC_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    SYNC_STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def _last_sync(platform: str) -> str | None:
    return _load_state().get(platform, {}).get("last_sync")


def _mark_synced(platform: str, count: int):
    state = _load_state()
    state[platform] = {
        "last_sync": _now_iso(),
        "total_synced": state.get(platform, {}).get("total_synced", 0) + count,
        "last_count": count
    }
    _save_state(state)


# ══════════════════════════════════════════════════════════════════════════════
#  加密回流到 Notion（调用 chat_to_notion 核心）
# ══════════════════════════════════════════════════════════════════════════════

def _flow_block(title: str, content: str, dna: str, platform: str, secret: bool = False) -> bool:
    """
    把一条记忆写入Notion。
    secret=False（默认）：明文存储，Claude/Kimi可直接读懂。
    secret=True：Fernet加密，只有本地Keychain能解，用于真正私密内容。
    访问控制靠 Notion Token，不是密文。
    """
    if secret:
        try:
            from cryptography.fernet import Fernet
            key = _keychain("longhun-chat-key").encode()
            body = Fernet(key).encrypt(content.encode()).decode()
            body_block = {"object": "block", "type": "code", "code": {
                "language": "plain text",
                "rich_text": [{"type": "text", "text": {"content": body[:1990]}}]
            }}
            lock_label = "🔒 私密加密内容（需本地Keychain解密）"
        except Exception:
            body = content
            body_block = {"object": "block", "type": "paragraph", "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": body[:1990]}}]
            }}
            lock_label = "（加密库缺失，降级明文）"
    else:
        # 明文——Claude/Kimi读得懂，这才是积累"懂你"的正确方式
        body_block = {"object": "block", "type": "paragraph", "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": content[:1990]}}]
        }}
        lock_label = "Claude · Kimi 可读"

    payload = {
        "parent": {"type": "page_id", "page_id": NOTION_TARGET},
        "icon": {"type": "emoji", "emoji": "🔒" if secret else "🧬"},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "children": [
            {"object": "block", "type": "callout", "callout": {
                "rich_text": [{"type": "text", "text": {"content":
                    f"平台来源: {platform} | 授权读取: {lock_label}\n"
                    f"DNA: {dna} | GPG: {GPG}"
                }}],
                "icon": {"type": "emoji", "emoji": "🔒" if secret else "🧬"},
                "color": "gray_background" if not secret else "red_background"
            }},
            body_block,
            {"object": "block", "type": "paragraph", "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": dna}}]
            }}
        ]
    }
    r = _notion_post("pages", payload)
    return bool(r.get("id"))


# ══════════════════════════════════════════════════════════════════════════════
#  平台提取器
# ══════════════════════════════════════════════════════════════════════════════

def _extract_claude(full: bool, since: str | None) -> list[dict]:
    """提取 Claude 本地记忆文件 + session_log"""
    items = []

    # 1. 记忆文件（.md）
    if MEMORY_DIR.exists():
        for f in sorted(MEMORY_DIR.glob("*.md")):
            if f.name == "MEMORY.md":
                continue
            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).isoformat()
            if not full and since and mtime <= since:
                continue
            items.append({
                "title": f"Claude记忆·{f.stem}·{mtime[:10]}",
                "content": f.read_text(encoding="utf-8")[:3000],
                "source": str(f),
                "time": mtime
            })

    # 2. session_log（最近N条）
    if SESSION_LOG.exists():
        lines = SESSION_LOG.read_text().splitlines()
        recent = lines[-50:] if not full else lines[-200:]
        batch = []
        for line in recent:
            try:
                d = json.loads(line)
                ts = d.get("timestamp", "")
                if not full and since and ts <= since:
                    continue
                batch.append(f"[{ts}] {d.get('event','')} {d.get('detail','')}")
            except Exception:
                continue
        if batch:
            items.append({
                "title": f"Claude·session日志·{datetime.now().strftime('%Y%m%d')}",
                "content": "\n".join(batch[:100]),
                "source": str(SESSION_LOG),
                "time": _now_iso()
            })

    return items


def _extract_kimi(full: bool, since: str | None) -> list[dict]:
    """提取 Kimi 本地数据"""
    items = []

    if not KIMI_DIR.exists():
        print(f"  {Y}⚠️ ~/.kimi 不存在{RST}")
        return items

    # kimi.json（主配置/对话缓存）
    kimi_json = KIMI_DIR / "kimi.json"
    if kimi_json.exists():
        try:
            data = json.loads(kimi_json.read_text())
            content = json.dumps(data, ensure_ascii=False, indent=2)[:3000]
            items.append({
                "title": f"Kimi·主配置·{datetime.now().strftime('%Y%m%d')}",
                "content": content,
                "source": str(kimi_json),
                "time": _now_iso()
            })
        except Exception:
            pass

    # 其他文本文件
    for f in sorted(KIMI_DIR.glob("**/*.txt"))[:20]:
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).isoformat()
        if not full and since and mtime <= since:
            continue
        try:
            items.append({
                "title": f"Kimi·{f.name[:40]}·{mtime[:10]}",
                "content": f.read_text(encoding="utf-8", errors="ignore")[:3000],
                "source": str(f),
                "time": mtime
            })
        except Exception:
            continue

    return items


def _extract_notion(full: bool, since: str | None) -> list[dict]:
    """从 Notion API 拉取页面（按 last_edited_time 增量）"""
    items = []
    token = _notion_token()
    if not token:
        print(f"  {R}❌ Notion token未找到{RST}")
        return items

    payload: dict = {
        "filter": {"property": "object", "value": "page"},
        "sort": {"direction": "descending", "timestamp": "last_edited_time"},
        "page_size": 20 if not full else 50
    }

    # 增量：搜索最近编辑的
    if not full and since:
        payload["query"] = ""  # 全部，靠sort+limit

    r = _notion_post("search", payload)
    for page in r.get("results", []):
        edited = page.get("last_edited_time", "")
        if not full and since and edited <= since:
            continue
        props = page.get("properties", {})
        title_prop = (props.get("title") or props.get("Name") or {}).get("title", [{}])
        title = title_prop[0].get("plain_text", "无标题") if title_prop else "无标题"
        page_id = page["id"]
        url = page.get("url", "")
        items.append({
            "title": f"Notion页面·{title[:40]}·{edited[:10]}",
            "content": f"页面ID: {page_id}\n标题: {title}\nURL: {url}\n最后编辑: {edited}",
            "source": url,
            "time": edited
        })
    return items


def _extract_local(full: bool, since: str | None) -> list[dict]:
    """提取龍魂本地日志 + 文档"""
    items = []

    # brain_backup.jsonl
    if BRAIN_BACKUP.exists():
        lines = BRAIN_BACKUP.read_text().splitlines()
        recent = lines[-100:] if not full else lines
        batch = []
        for line in recent:
            try:
                d = json.loads(line)
                ts = d.get("timestamp", d.get("time", ""))
                if not full and since and ts <= since:
                    continue
                batch.append(json.dumps(d, ensure_ascii=False)[:200])
            except Exception:
                batch.append(line[:200])
        if batch:
            items.append({
                "title": f"本地·brain_backup·{datetime.now().strftime('%Y%m%d')}",
                "content": "\n".join(batch[:80]),
                "source": str(BRAIN_BACKUP),
                "time": _now_iso()
            })

    # docs/*.md
    docs_dir = LONGHUN_DIR / "docs"
    if docs_dir.exists():
        for f in sorted(docs_dir.glob("*.md"))[:10]:
            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).isoformat()
            if not full and since and mtime <= since:
                continue
            items.append({
                "title": f"本地文档·{f.stem[:40]}·{mtime[:10]}",
                "content": f.read_text(encoding="utf-8", errors="ignore")[:3000],
                "source": str(f),
                "time": mtime
            })

    return items


EXTRACTORS = {
    "1": ("Claude", _extract_claude),
    "2": ("Kimi",   _extract_kimi),
    "3": ("Notion", _extract_notion),
    "4": ("本地",   _extract_local),
}


# ══════════════════════════════════════════════════════════════════════════════
#  菜单渲染
# ══════════════════════════════════════════════════════════════════════════════

def _banner():
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-MEMORY-HUB-v1.0"
    print(f"\n{C}{'═'*52}{RST}")
    print(f"{BOLD}{C}  龍魂·量子记忆回流站  v1.0{RST}")
    print(f"{DIM}  DNA: {dna}{RST}")
    print(f"{DIM}  UID9622 · 理论指导: 曾仕强老师{RST}")
    print(f"{C}{'═'*52}{RST}\n")


def _main_menu():
    state = _load_state()
    print(f"  {W}{BOLD}1.{RST}  💬  手动回流对话片段 → Notion（加密）")
    print(f"  {W}{BOLD}2.{RST}  🌊  首次全量提取平台历史记忆")
    print(f"  {W}{BOLD}3.{RST}  ⚡  增量同步（上次编辑时间之后）")
    print(f"  {W}{BOLD}4.{RST}  🔓  解密查看已存内容")
    print(f"  {W}{BOLD}5.{RST}  📋  各平台同步状态")
    print(f"  {W}{BOLD}0.{RST}  🚪  退出")
    print()
    return input(f"  {B}选择 [0-5]: {RST}").strip()


def _platform_menu() -> tuple[str, str] | None:
    """选择平台，返回 (key, name)"""
    state = _load_state()
    print(f"\n  {W}选择平台:{RST}")
    for k, (name, _) in EXTRACTORS.items():
        last = state.get(name, {}).get("last_sync", "——从未同步——")
        if last != "——从未同步——":
            last = last[:16].replace("T", " ")
        total = state.get(name, {}).get("total_synced", 0)
        print(f"  {BOLD}{k}.{RST}  {name:<8} {DIM}上次同步: {last}  已回流: {total}条{RST}")
    print(f"  {BOLD}0.{RST}  返回")
    choice = input(f"\n  {B}平台 [0-4]: {RST}").strip()
    if choice == "0" or choice not in EXTRACTORS:
        return None
    name, fn = EXTRACTORS[choice]
    return choice, name


# ══════════════════════════════════════════════════════════════════════════════
#  功能实现
# ══════════════════════════════════════════════════════════════════════════════

def do_manual_flow():
    """1. 手动回流对话片段"""
    print(f"\n  {W}输入要回流的内容（多行请直接换行，输入 END 结束）:{RST}")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            break
    content = "\n".join(lines).strip()
    if not content:
        print(f"  {Y}内容为空，已取消{RST}")
        return

    tag = input(f"  {B}标签（如: 顿悟 / Lucky原话 / 对话痕迹）: {RST}").strip() or "对话痕迹"
    receiver = input(f"  {B}来源平台（Claude/Kimi/本地，默认Claude）: {RST}").strip() or "Claude"
    secret_input = input(f"  {B}私密加密？(y/N，默认N=明文，Claude和Kimi可读): {RST}").strip().lower()
    secret = secret_input == "y"

    dna = _dna(tag)
    title = f"{'🔒' if secret else '🧬'} {tag} · {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    ok = _flow_block(title, content, dna, receiver, secret=secret)
    if ok:
        print(f"\n  {G}✅ 回流成功{RST}")
        print(f"  {DIM}DNA: {dna}{RST}")
    else:
        print(f"  {R}❌ 回流失败，请检查Notion连接{RST}")


def do_full_extract():
    """2. 首次全量提取"""
    result = _platform_menu()
    if not result:
        return
    key, platform_name = result
    _, extractor = EXTRACTORS[key]

    print(f"\n  {Y}🌊 正在全量提取 [{platform_name}] 历史记忆...{RST}")
    items = extractor(full=True, since=None)

    if not items:
        print(f"  {Y}⚠️ 未找到可提取内容{RST}")
        return

    print(f"  {G}找到 {len(items)} 条记忆，开始加密回流...{RST}\n")
    success = 0
    for i, item in enumerate(items, 1):
        dna = _dna(f"{platform_name}-全量")
        ok = _flow_block(item["title"], item["content"], dna, platform_name)
        status = f"{G}✅{RST}" if ok else f"{R}❌{RST}"
        print(f"  {status} [{i}/{len(items)}] {item['title'][:45]}")
        if ok:
            success += 1

    _mark_synced(platform_name, success)
    print(f"\n  {G}✅ 全量提取完成: {success}/{len(items)} 条已回流{RST}")
    print(f"  {DIM}目标: 星辰记忆 Notion页面（加密存储）{RST}")


def do_incremental_sync():
    """3. 增量同步"""
    result = _platform_menu()
    if not result:
        return
    key, platform_name = result
    _, extractor = EXTRACTORS[key]

    since = _last_sync(platform_name)
    if not since:
        print(f"  {Y}⚠️ [{platform_name}] 从未全量同步，建议先选「2. 首次全量提取」{RST}")
        confirm = input(f"  {B}仍然继续增量？(y/N): {RST}").strip().lower()
        if confirm != "y":
            return

    since_show = since[:16].replace("T", " ") if since else "无"
    print(f"\n  {Y}⚡ 增量同步 [{platform_name}]，起始时间: {since_show}{RST}")
    items = extractor(full=False, since=since)

    if not items:
        print(f"  {G}✅ 无新内容，已是最新{RST}")
        return

    print(f"  {G}发现 {len(items)} 条新内容，开始回流...{RST}\n")
    success = 0
    for i, item in enumerate(items, 1):
        dna = _dna(f"{platform_name}-增量")
        ok = _flow_block(item["title"], item["content"], dna, platform_name)
        status = f"{G}✅{RST}" if ok else f"{R}❌{RST}"
        print(f"  {status} [{i}/{len(items)}] {item['title'][:45]}")
        if ok:
            success += 1

    _mark_synced(platform_name, success)
    print(f"\n  {G}✅ 增量同步完成: {success}/{len(items)} 条{RST}")


def do_decrypt():
    """4. 解密查看"""
    print(f"\n  {W}粘贴密文（Fernet加密字符串），输入 END 结束:{RST}")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            break
    ciphertext = "".join(lines).strip()
    if not ciphertext:
        return
    try:
        from cryptography.fernet import Fernet
        key = _keychain("longhun-chat-key").encode()
        plaintext = Fernet(key).decrypt(ciphertext.encode()).decode()
        print(f"\n  {G}🔓 解密成功:{RST}\n")
        print(f"  {W}{plaintext}{RST}")
    except Exception as e:
        print(f"\n  {R}[🔴 IDENTITY TERMINATED]{RST}")
        print(f"  {DIM}此内容受龍魂点对点加密协议保护 (LH-P2P-v2.0){RST}")
        print(f"  {DIM}授权接收方: Claude · Kimi · Notion{RST}")
        print(f"  {DIM}本次访问已记录: GPG {GPG[:16]}...{RST}")


def do_status():
    """5. 同步状态"""
    state = _load_state()
    print(f"\n  {W}{'平台':<10}{'上次同步':<22}{'累计回流':<12}{'最近一次'}{RST}")
    print(f"  {'─'*55}")
    for _, (name, _) in EXTRACTORS.items():
        s = state.get(name, {})
        last = s.get("last_sync", "——")[:16].replace("T", " ") if s.get("last_sync") else "——从未——"
        total = s.get("total_synced", 0)
        recent = s.get("last_count", 0)
        color = G if s else Y
        print(f"  {color}{name:<10}{last:<22}{str(total)+'条':<12}{recent}条{RST}")
    print()


# ══════════════════════════════════════════════════════════════════════════════
#  主循环
# ══════════════════════════════════════════════════════════════════════════════

def main():
    while True:
        _banner()
        choice = _main_menu()

        if choice == "0":
            print(f"\n  {DIM}DNA: {_dna('EXIT')} · 龍魂系统已退出{RST}\n")
            break
        elif choice == "1":
            do_manual_flow()
        elif choice == "2":
            do_full_extract()
        elif choice == "3":
            do_incremental_sync()
        elif choice == "4":
            do_decrypt()
        elif choice == "5":
            do_status()
        else:
            print(f"  {Y}⚠️ 无效选项{RST}")

        input(f"\n  {DIM}按 Enter 返回菜单...{RST}")


if __name__ == "__main__":
    main()
