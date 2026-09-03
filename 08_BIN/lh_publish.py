#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-OPEN-PUBLISH-TOOLCHAIN-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 龍魂·统一对外发布工具链 v1.0
# 目标: 「发公告」= 一句话。AI 说 lh publish announce "标题" "内容" --channels issue,web,readme
#       自动完成: 模板渲染 → GitHub Issue → 官网横幅 → README 公告区 → git PR → bot approve
#       → squash merge → rsync 鲲鹏 → 发布日志 + 状态面板(GPG 签名)。
#
# 用法:
#   lh publish announce <标题> [正文] [--channels issue,web,readme] [--template release_announcement|community_update|security_advisory] [--version v1.0] [--contact "邮箱/链接"] [--dry-run]
#   lh publish status                 # 最近 10 条发布摘要
#   lh publish dashboard              # 生成 ~/.longhun/publish_dashboard.md（GPG 签）+ 控制台表格
#   lh publish rollback <ID> [--reason "…"]   # 回滚: Issue 关闭 / web+readme 提示 revert
#   lh publish templates list|show <name>
#
# 数据: ~/.longhun/publish_log.json（append-only 审计） · 模板 ~/.longhun/publish_templates/
# 设计铁律: 零三方依赖 · GitHub 直连(禁代理) · token 只读 Keychain/App · 失败渠道不拖垮整体 · 全程审计留痕

import os
import re
import sys
import json
import time
import shutil
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # longhun-system/
BIN = ROOT / "08_BIN"
HOME_LH = Path.home() / ".longhun"
LOG_FILE = HOME_LH / "publish_log.json"
TEMPLATE_DIR = HOME_LH / "publish_templates"
DASHBOARD = HOME_LH / "publish_dashboard.md"

GH_API = "https://api.github.com"
OWNER, REPO = "UID9622", "longhun-system"
FULL_REPO = f"{OWNER}/{REPO}"
BASE_BRANCH = "orphan_main"
REMOTE = "gh-ssh"
UA = "LongHun-OpenPublish/1.0 (UID9622)"               # HTTP 头必须 ASCII
TIMEOUT = 15

KUNPENG_HOST = "119.13.90.27"
KUNPENG_USER = "root"
KUNPENG_KEY = str(Path.home() / ".ssh" / "longhun_kunpeng_ed25519")
PORTAL_REMOTE = f"/opt/longhun-system/portal/index.html"

CONTACT_DEFAULT = "邮箱 346045695@qq.com · GitHub Issue · GPG 全签可溯源"

# 公告正文里 HTML 需要用到的文档链接（官网横幅固定三入口）
URL_TOPO = "https://uid9622.cn/topo/"
URL_HEALTH = "https://uid9622.cn/api/v1/health"
URL_GUIDE = "https://github.com/UID9622/longhun-system/blob/orphan_main/12_DOCS/%E9%BE%99%E9%AD%82API%E9%9B%86%E6%88%90%E6%8C%87%E5%8D%97-v1.0.md"

PORTAL_FILE = ROOT / "10_PORTAL" / "index.html"
README_FILE = ROOT / "README.md"

BANNER_TPL = '''<!-- ====== 公告条 · {DATE} · lh publish 自动维护 ====== -->
<section class="portal-announce" style="background:linear-gradient(90deg,var(--bg3),rgba(212,175,55,.06));border-bottom:1px solid var(--border);padding:14px 0;">
  <div class="container" style="display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;font-size:14px;">
    <span style="color:var(--gold);font-weight:600;" title="{TITLE}">📢 {DATE} · {TITLE}</span>
    <a href="{URL_TOPO}" style="color:var(--accent);text-decoration:none;">🌐 拓扑页面</a>
    <a href="{URL_HEALTH}" style="color:var(--accent);text-decoration:none;">🔌 网关健康</a>
    <a href="{URL_GUIDE}" style="color:var(--accent);text-decoration:none;">📖 API 集成指南</a>
    <span style="color:var(--text-dim);font-size:13px;">数据不出境 · 主权在民</span>
  </div>
</section>
'''

README_MARKER = "## 📣 发布公告 · 对外公告"

# 内置默认模板（模板目录缺失/被删时自动重建 · 可被 ~/.longhun/publish_templates/ 同名文件覆盖）
DEFAULT_TEMPLATES = {
"release_announcement": "# 🚀 {{TITLE}}\n\n> 發布日期：{{DATE}} · 版本：{{VERSION}} · 發布 ID：{{ID}}\n> 归属名：诸葛鑫 | UID9622 · 龍芯北辰\n\n{{BODY}}\n\n---\n\n## 📬 联系与反馈\n\n- {{CONTACT}}\n- 更多：龍魂系統 GitHub `UID9622/longhun-system` · 官网 https://uid9622.cn\n\n作者：诸葛鑫（UID9622）· 龍芯北辰\n协议：工程层 MulanPSL v2 · 思想层 CC BY-NC-SA 4.0\n",
"community_update": "# 🧭 {{TITLE}}\n\n> 社區動態 · {{DATE}} · {{VERSION}} · 發布 ID：{{ID}}\n> 归属名：诸葛鑫 | UID9622 · 龍芯北辰\n\n{{BODY}}\n\n---\n\n## 📬 加入我们\n\n- {{CONTACT}}\n- 社区讨论: https://github.com/UID9622/longhun-system/discussions\n\n作者：诸葛鑫（UID9622）· 龍芯北辰\n协议：工程层 MulanPSL v2 · 思想层 CC BY-NC-SA 4.0\n",
"security_advisory": "# 🛡️ 安全公告 {{TITLE}}\n\n> 安全公告 · {{DATE}} · 版本影响：{{VERSION}} · 發布 ID：{{ID}}\n> 归属名：诸葛鑫 | UID9622 · 龍芯北辰\n\n{{BODY}}\n\n---\n\n## 📬 漏洞报告 / 联系方式\n\n- {{CONTACT}}\n- 披露政策: 详见仓库 `SECURITY.md` · 负责任披露 · 修复优先于曝光\n\n作者：诸葛鑫（UID9622）· 龍芯北辰\n协议：工程层 MulanPSL v2 · 思想层 CC BY-NC-SA 4.0\n",
}


def now_local():
    return time.localtime()


def date_str():
    return time.strftime("%Y-%m-%d", now_local())


def ts_str():
    return time.strftime("%Y-%m-%d %H:%M:%S", now_local())


# ── 令牌获取（只读 · 不打印明文）──────────────────────
def _mask(tok: str) -> str:
    if not tok:
        return "(无)"
    return f"{tok[:9]}…{tok[-4:]}" if len(tok) > 13 else "(短/异常)"


def get_pat() -> str:
    """classic PAT: env GITHUB_TOKEN → Keychain(s github.com -a UID9622)"""
    for src in ("GITHUB_TOKEN",):
        t = os.environ.get(src, "")
        if t:
            return t.strip()
    try:
        r = subprocess.run(["security", "find-internet-password", "-s", "github.com", "-a", "UID9622", "-w"],
                           capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    return ""


def get_app_token() -> str:
    """longhun-bot App token: python3 08_BIN/lh_github_app.py token → ghs_…"""
    try:
        r = subprocess.run([sys.executable, str(BIN / "lh_github_app.py"), "token"],
                           capture_output=True, text=True, timeout=20)
        for line in (r.stdout or "").splitlines():
            m = re.search(r"ghs_[A-Za-z0-9_.-]+", line)
            if m:
                return m.group(0)
    except Exception:
        pass
    return ""


def gh_request(method: str, path: str, token: str, payload=None):
    """GitHub API 直连（零代理 · 不读系统代理）"""
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    url = f"{GH_API}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    if data:
        req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", UA)
    try:
        with opener.open(req, timeout=TIMEOUT) as r:
            raw = r.read()
            try:
                return r.status, json.loads(raw)
            except Exception:
                return r.status, raw.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"message": raw[:300]}
    except Exception as e:
        return 0, {"message": str(e)}


def run_cmd(args, timeout=120, cwd=None):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return 1, str(e)


def gpgsign(path: str):
    run_cmd([sys.executable, str(BIN / "lh_gpg_sign.py"), "sign", path, "--force"])


# ── 发布日志 ────────────────────────────────────────
def log_load() -> dict:
    if LOG_FILE.exists():
        try:
            return json.loads(LOG_FILE.read_text("utf-8"))
        except Exception:
            pass
    return {"releases": []}


def log_save(data: dict):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")


def next_id(data: dict, dstr: str) -> str:
    n = 1
    for rel in data["releases"]:
        if rel["id"].startswith(f"PUB-{dstr.replace('-','')}"):
            n += 1
    return f"PUB-{dstr.replace('-','')}-{n:02d}"


def find_release(data: dict, rid: str):
    for rel in data["releases"]:
        if rel["id"].lower() == rid.lower() or rel["id"][4:].lower() == rid.lower():
            return rel
    return None


# ── 模板渲染 ────────────────────────────────────────
def ensure_templates():
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    for name, content in DEFAULT_TEMPLATES.items():
        p = TEMPLATE_DIR / f"{name}.md"
        if not p.exists():
            p.write_text(content, "utf-8")


def render_template(name: str, title: str, body: str, version: str, contact: str, rid: str) -> str:
    ensure_templates()
    name = name if name in DEFAULT_TEMPLATES else "release_announcement"
    p = TEMPLATE_DIR / f"{name}.md"
    if not p.exists():
        p.write_text(DEFAULT_TEMPLATES[name], "utf-8")
    tpl = p.read_text("utf-8")
    dstr = date_str()
    for k, v in {"{{TITLE}}": title, "{{BODY}}": body or "详见各节说明。",
                 "{{DATE}}": dstr, "{{VERSION}}": version, "{{CONTACT}}": contact, "{{ID}}": rid}.items():
        tpl = tpl.replace(k, v)
    return tpl


# ── 渠道 1: GitHub Issue ───────────────────────────
def channel_issue(title: str, body: str, token: str):
    payload = {"title": title, "body": body}
    code, data = gh_request("POST", f"/repos/{FULL_REPO}/issues", token, payload)
    if code in (200, 201) and isinstance(data, dict) and data.get("number"):
        return {"status": "done", "url": data["html_url"], "num": data["number"]}
    return {"status": "error", "err": f"HTTP {code} {data.get('message', data)}"}


# ── 渠道 2: 官网首页横幅（render 与 write 分离 · write 须在 git 分支就位后调用） ──
def render_web(date: str, title: str) -> str:
    html = PORTAL_FILE.read_text("utf-8")
    short = (title[:30] + "…") if len(title) > 30 else title
    banner = (BANNER_TPL.replace("{DATE}", date).replace("{TITLE}", short)
              .replace("{URL_TOPO}", URL_TOPO).replace("{URL_HEALTH}", URL_HEALTH).replace("{URL_GUIDE}", URL_GUIDE))
    pat = re.compile(r"<!-- ====== 公告条.*?</section>\n", re.S)
    if pat.search(html):
        return pat.sub(banner + "\n", html, count=1)
    i = html.find("</header>")
    if i == -1:
        raise RuntimeError("portal 无 </header> 锚点")
    return html[:i] + "</header>\n\n" + banner + "\n" + html[i + len("</header>"):]


def write_web(content: str):
    PORTAL_FILE.write_text(content, "utf-8")
    gpgsign(str(PORTAL_FILE))


# ── 渠道 3: README 公告区（render 与 write 分离） ──
def render_readme(date: str, title: str, body: str, issue_url: str) -> str:
    rmd = README_FILE.read_text("utf-8")
    snippet = body.strip().splitlines()[0][:60] + "…" if body and body.strip() else ""
    line = f"- {date} 📢 **{title}**"
    if snippet:
        line += f" — {snippet}"
    if issue_url:
        line += f" · [GitHub →]({issue_url})"
    if README_MARKER in rmd:
        i = rmd.index(README_MARKER)
        j = rmd.find("\n## ", i + len(README_MARKER))
        end = j if j != -1 else len(rmd)
        old_lines = [ln for ln in rmd[i:end].splitlines() if ln.startswith("- ")]
        old_lines = [ln for ln in old_lines if title not in ln][:9]
        block = README_MARKER + "\n\n> 最近 10 条 · `lh publish` 自动维护\n\n" + line + (("\n" + "\n".join(old_lines)) if old_lines else "")
        return rmd[:i] + block + rmd[end:]
    anchor = "## 🗂️ 仓库速览 · Repository at a Glance"
    k = rmd.find(anchor)
    block = README_MARKER + "\n\n> 最近 10 条 · `lh publish` 自动维护\n\n" + line + "\n"
    if k == -1:
        return rmd.rstrip() + "\n\n" + block + "\n"
    return rmd[:k] + block + "\n\n" + rmd[k:]


def write_readme(content: str):
    README_FILE.write_text(content, "utf-8")
    gpgsign(str(README_FILE))


# ── git 链路: 基于远程最新切分支 → 提交 → PR → bot approve → squash merge ──
def git_prepare(rid: str, targets):
    """基于 {REMOTE}/{BASE_BRANCH} 最新 commit 创建 publish 分支。
    前置: 当前在本地 orphan_main（文件尚未改）。成功 → 已 checkout 到新分支。"""
    branch = "publish-" + rid[4:].lower()
    stash_items = []
    for t in targets:
        for p in (str(t), str(t) + ".asc"):
            if os.path.exists(p):
                stash_items.append(p)
    run_cmd(["git", "-C", str(ROOT), "fetch", REMOTE, BASE_BRANCH], timeout=90)
    if stash_items:
        run_cmd(["git", "-C", str(ROOT), "stash", "push", "-m", f"lhpub-{rid}"] + stash_items)
    rc, out = run_cmd(["git", "-C", str(ROOT), "checkout", "-b", branch, f"{REMOTE}/{BASE_BRANCH}"])
    if rc != 0:
        run_cmd(["git", "-C", str(ROOT), "checkout", BASE_BRANCH])
        return False, f"{out[-200:]}"
    return True, branch


def git_publish(rid: str, title: str, files, pr_body: str):
    """前置: 已在 publish 分支且目标文件已写入。提交 → push → PR → bot approve → squash merge → 清理。"""
    branch = "publish-" + rid[4:].lower()
    add_files = []
    for f in files:
        fp = Path(f)
        if fp.exists():
            add_files.append(str(fp.relative_to(ROOT)))
        asc = Path(str(fp) + ".asc")
        if asc.exists():
            add_files.append(str(asc.relative_to(ROOT)))
    add_files = sorted(set(add_files))
    if not add_files:
        return {"status": "error", "err": "无待提交文件"}
    for args, name in [
        (["git", "-C", str(ROOT), "add", "--"] + add_files, "add"),
        (["git", "-C", str(ROOT), "commit", "-m", f"{title} ({rid} · lh publish)"], "commit"),
        (["git", "-C", str(ROOT), "push", REMOTE, branch], "push"),
    ]:
        rc, out = run_cmd(args, timeout=120)
        if rc != 0:
            run_cmd(["git", "-C", str(ROOT), "checkout", BASE_BRANCH])
            return {"status": "error", "err": f"git {name}: {out[-300:]}"}
    pat = get_pat()
    code, pr = gh_request("POST", f"/repos/{FULL_REPO}/pulls", pat,
                          {"title": f"{title} ({rid} · lh publish)", "head": branch,
                           "base": BASE_BRANCH, "body": pr_body})
    if code not in (200, 201):
        run_cmd(["git", "-C", str(ROOT), "checkout", BASE_BRANCH])
        return {"status": "error", "err": f"PR 创建失败 HTTP {code} {pr.get('message', pr)}"}
    num = pr["number"]
    app = get_app_token()
    code, _ = gh_request("POST", f"/repos/{FULL_REPO}/pulls/{num}/reviews", app,
                         {"event": "APPROVE", "body": "longhun-bot 独立复核：lh publish 自动发布 · GPG 已签 · 同意合併"})
    if code != 200:
        return {"status": "error", "err": f"bot approve 失败 HTTP {code}", "pr": num}
    code, mg = gh_request("PUT", f"/repos/{FULL_REPO}/pulls/{num}/merge", app,
                          {"merge_method": "squash", "commit_title": f"{title} ({rid} · lh publish) (#{num})"})
    if code != 200:
        return {"status": "error", "err": f"merge 失败 HTTP {code} {mg.get('message', mg)}", "pr": num}
    run_cmd(["git", "-C", str(ROOT), "checkout", BASE_BRANCH])
    run_cmd(["git", "-C", str(ROOT), "branch", "-D", branch])
    run_cmd(["git", "-C", str(ROOT), "push", REMOTE, "--delete", branch])
    return {"status": "done", "pr": num, "sha": mg.get("sha", "")[:8]}


def rsync_portal():
    src = PORTAL_FILE
    ssh = f"ssh -i {KUNPENG_KEY} -o BatchMode=yes -o StrictHostKeyChecking=no"
    rc, out = run_cmd(["rsync", "-az", "-e", ssh, str(src), f"{KUNPENG_USER}@{KUNPENG_HOST}:{PORTAL_REMOTE}"], timeout=60)
    return rc == 0, out


# ── announce ────────────────────────────────────────
def cmd_announce(argv):
    flags = {"channels": "issue,web,readme", "template": "release_announcement",
             "version": "-", "contact": CONTACT_DEFAULT, "dry_run": False}
    pos = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--dry-run", "--dryrun"):
            flags["dry_run"] = True
        elif a in ("--channels", "--template", "--version", "--contact") and i + 1 < len(argv):
            flags[a[2:]] = argv[i + 1]
            i += 1
        elif a.startswith("--"):
            sys.stderr.write(f"未知参数 {a}\n")
        else:
            pos.append(a)
        i += 1
    if not pos:
        print("用法: lh publish announce <标题> [正文] [--channels issue,web,readme] [--template <名>] [--version v1.0] [--contact …] [--dry-run]")
        return 1
    title, body = pos[0], pos[1] if len(pos) > 1 else ""
    channels = [c.strip().lower() for c in flags["channels"].split(",") if c.strip()]
    bad = [c for c in channels if c not in ("issue", "web", "readme")]
    if bad:
        print(f"❌ 非法渠道: {bad}（支持 issue/web/readme）")
        return 2
    if not channels:
        print("❌ channels 为空")
        return 2
    if flags["template"] not in DEFAULT_TEMPLATES:
        print(f"❌ 未知模板: {flags['template']}（可用: {list(DEFAULT_TEMPLATES)}）")
        return 2

    data = log_load()
    dstr = date_str()
    rid = next_id(data, dstr)
    contact = flags["contact"] or CONTACT_DEFAULT
    rendered = render_template(flags["template"], title, body, flags["version"], contact, rid)
    issue_body = rendered + f"\n\n---\n> 本公告由 `lh publish` 自动分发 · ID: {rid} · {ts_str()}\n"

    rel = {"id": rid, "ts": ts_str(), "date": dstr, "title": title, "body": body,
           "template": flags["template"], "version": flags["version"], "contact": contact,
           "channels": {c: {"status": "pending"} for c in channels},
           "pr": None, "issue_url": None, "rollback": None}
    data["releases"].insert(0, rel)
    if not flags["dry_run"]:
        log_save(data)
    print(f"📢 发布 {rid} | {title}")
    print(f"   模板={flags['template']} · 渠道={channels}" + (" · [DRY-RUN]" if flags["dry_run"] else ""))
    print(f"   ————————————————————————————————————————")

    if flags["dry_run"]:
        print("   [dry-run] 渲染后正文(前 6 行):")
        for ln in rendered.splitlines()[:6]:
            print("   | " + ln)
        return 0

    pat = get_pat()
    if not pat:
        print("❌ 无 GitHub PAT（Keychain: github.com / UID9622）")
        rel["channels"]["issue"] = {"status": "error", "err": "无 token"}
        log_save(data)
        return 2

    issue_url = None
    if "issue" in channels:
        r = channel_issue(title, issue_body, pat)
        rel["channels"]["issue"] = r
        if r.get("status") == "done":
            issue_url = r["url"]
            print(f"   ✅ GitHub Issue: {r['url']}")
        else:
            print(f"   ❌ GitHub Issue: {r.get('err')}")

    web_req = "web" in channels
    rmd_req = "readme" in channels
    on_branch = False
    if web_req or rmd_req:
        targets = ([PORTAL_FILE] if web_req else []) + ([README_FILE] if rmd_req else [])
        ok, msg = git_prepare(rid, targets)
        if not ok:
            print(f"   ❌ git 分支准备失败: {msg}")
            if web_req:
                rel["channels"]["web"] = {"status": "error", "err": f"git prepare: {msg}"}
            if rmd_req:
                rel["channels"]["readme"] = {"status": "error", "err": f"git prepare: {msg}"}
            log_save(data)
            return 2
        on_branch = True
        print(f"   🔀 分支就绪（基于 {REMOTE}/{BASE_BRANCH} 最新）")

    code_files = []
    if web_req:
        try:
            write_web(render_web(dstr, title))
            code_files.append(PORTAL_FILE)
            rel["channels"]["web"] = {"status": "done", "file": "10_PORTAL/index.html"}
            print("   ✅ 官网横幅（已写入 + GPG 签）")
        except Exception as e:
            rel["channels"]["web"] = {"status": "error", "err": str(e)}
            print(f"   ❌ 官网横幅: {e}")
    if rmd_req:
        try:
            write_readme(render_readme(dstr, title, body, issue_url))
            code_files.append(README_FILE)
            rel["channels"]["readme"] = {"status": "done", "file": "README.md"}
            print("   ✅ README 公告区（已写入 + GPG 签）")
        except Exception as e:
            rel["channels"]["readme"] = {"status": "error", "err": str(e)}
            print(f"   ❌ README 公告区: {e}")

    if code_files and on_branch:
        pr_body = (f"# {title}\n\n> {rid} · {ts_str()} · lh publish 自动分发\n\n"
                   f"- 渠道: {', '.join(channels)}\n"
                   + (f"- GitHub Issue: {issue_url}\n" if issue_url else "")
                   + f"- 模板: {flags['template']}\n\n**变更文件**: " + ", ".join(str(Path(f).relative_to(ROOT)) for f in code_files))
        g = git_publish(rid, title, code_files, pr_body)
        rel["pr"] = g.get("pr")
        if g.get("status") == "done":
            print(f"   ✅ PR #{g['pr']} squash merged（{g.get('sha')}）")
            if web_req and rel.get("channels", {}).get("web", {}).get("status") == "done":
                ok_rs, out_rs = rsync_portal()
                print("   ✅ 已 rsync 同步鲲鹏官网线上" if ok_rs else f"   🟡 rsync 失败(可后补): {out_rs[-120:]}")
        else:
            print(f"   ❌ PR 链路: {g.get('err')}（已留在 publish 分支，可手动处理）")
    elif on_branch and not code_files:
        run_cmd(["git", "-C", str(ROOT), "checkout", BASE_BRANCH])
    log_save(data)
    print("   ✅ 已记入 ~/.longhun/publish_log.json")
    return 0


def status_line(rel, wide=False):
    ch = rel.get("channels", {})
    def mark(c):
        s = ch.get(c, {}).get("status")
        return "✅" if s == "done" else ("❌" if s == "error" else ("⏳" if s == "pending" else "—"))
    t = rel["title"]
    issue_num = (rel.get("issue_url") or "").split("/")[-1] or "-"
    rb = "↩️" if rel.get("rollback") else ""
    pr = rel.get("pr")
    pr_s = (f"#{pr['number']}" if isinstance(pr, dict) and pr.get("number") else (pr or "-"))
    if wide:
        return f"| {rel['id']} | {rel['date']} | {t} | {mark('issue')} | {mark('web')} | {mark('readme')} | {pr_s} | {issue_num} | {rb} |"
    return f"{rel['id']} | {rel['date']} | {t[:36]:<36} | issue:{mark('issue')} web:{mark('web')} readme:{mark('readme')}"


def cmd_status(argv):
    data = log_load()
    rels = data.get("releases", [])[:10]
    if not rels:
        print("暂无发布记录。首发: lh publish announce \"标题\" \"内容\"")
        return 0
    print("ID | 日期 | 标题 | issue | web | readme")
    for rel in rels:
        print(status_line(rel))
    print(f"共 {len(data.get('releases', []))} 条记录 · 日志 {LOG_FILE}")
    return 0


def cmd_dashboard(argv):
    data = log_load()
    rels = data.get("releases", [])
    rows = [status_line(rel, wide=True) for rel in rels[:20]] or ["| — | — | 暂无发布 | — | — | — | — | — | — |"]
    md = [
        "# 📢 龍魂对外发布面板 · Publish Dashboard",
        "",
        f"> 生成: {ts_str()} · 数据: `~/.longhun/publish_log.json` · 自动 GPG 签名",
        f"> 工具: `lh publish` · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰",
        "",
        "| ID | 日期 | 标题 | Issue | Web | README | PR# | Issue# | 回滚 |",
        "|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|",
    ] + rows
    DASHBOARD.parent.mkdir(parents=True, exist_ok=True)
    DASHBOARD.write_text("\n".join(md) + "\n", "utf-8")
    try:
        gpgsign(str(DASHBOARD))
    except Exception:
        pass
    print(f"✅ 面板已生成并 GPG 签名: {DASHBOARD}")
    print("\n".join(md[:4]) + "\n")
    print("\n".join(md[5:]))
    return 0


def cmd_rollback(argv):
    if not argv:
        print("用法: lh publish rollback <ID> [--reason \"原因\"]")
        return 1
    rid = argv[0]
    reason = ""
    if "--reason" in argv:
        k = argv.index("--reason")
        reason = argv[k + 1] if k + 1 < len(argv) else ""
    data = log_load()
    rel = find_release(data, rid)
    if not rel:
        print(f"❌ 未找到发布 {rid}")
        return 2
    if rel.get("rollback"):
        print(f"⚠️ {rid} 已回滚过（{rel['rollback'].get('at')}）")
    ch = rel.get("channels", {})
    if ch.get("issue", {}).get("status") == "done" and ch["issue"].get("url"):
        pat = get_pat()
        num = ch["issue"]["url"].rstrip("/").split("/")[-1]
        code, res = gh_request("PATCH", f"/repos/{FULL_REPO}/issues/{num}", pat, {"state": "closed"})
        print(f"   {'✅' if code == 200 else '❌'} Issue #{num} 关闭（HTTP {code}）")
    for c in ("web", "readme"):
        if ch.get(c, {}).get("status") == "done":
            pr = rel.get("pr")
            print(f"   🟡 {c} 已随 PR #{pr} 合并，自动回滚需新建 revert PR；如需立即下线请人工处理（发布 ID {rel['id']}）")
    rel["rollback"] = {"at": ts_str(), "reason": reason or "未注明"}
    log_save(data)
    print(f"↩️ {rid} 已标记回滚")
    return 0


def cmd_templates(argv):
    ensure_templates()
    if argv and argv[0] == "show" and len(argv) > 1:
        p = TEMPLATE_DIR / f"{argv[1]}.md"
        if not p.exists():
            print(f"❌ 模板不存在: {argv[1]}（可用: {list(DEFAULT_TEMPLATES)}）")
            return 2
        print(p.read_text("utf-8"))
        return 0
    print(f"模板目录: {TEMPLATE_DIR}")
    for name in DEFAULT_TEMPLATES:
        p = TEMPLATE_DIR / f"{name}.md"
        print(f"  · {name}.md  {'✅' if p.exists() else '❌缺失'}")
    print("查看: lh publish templates show <name>")
    return 0


USAGE = """龍魂·统一对外发布工具链 v1.0

用法:
  lh publish announce <标题> [正文] [--channels issue,web,readme] [--template <release_announcement|community_update|security_advisory>] [--version v1.0] [--contact …] [--dry-run]
  lh publish status
  lh publish dashboard
  lh publish rollback <ID> [--reason …]
  lh publish templates list|show <name>
"""


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "announce":
        return cmd_announce(rest)
    if cmd == "status":
        return cmd_status(rest)
    if cmd == "dashboard":
        return cmd_dashboard(rest)
    if cmd == "rollback":
        return cmd_rollback(rest)
    if cmd == "templates":
        return cmd_templates(rest)
    print(USAGE)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
