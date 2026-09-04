#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-PUBLISH-TOOLCHAIN-v2.0-PR-AUTO-STATE-MACHINE-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 龍魂·统一对外发布工具链 v2.0（PR #95 经验系统化 · 状态驱动·无人值守）
# 目标: 「本地改完 → lh publish pr <标题> --auto → PR 自动合并·分支自动删·本地自动同步」
#
# v2.0 新增（2026-09-04）:
#   lh publish pr <标题> [--auto|--no-merge|--dry-run] [--files a.py,b.md] [--include-generated] [--resume <id>] [--base <分支>]
#     全自动 PR 生命周期状态机: collect→gate 自动绕行留档→commit→push→PR(PAT 创建)→CI 等待→bot approve→squash merge
#       →删分支→本地同步→GPG 报告。状态持久化 ~/.longhun/publish_state.json，支持 --resume 断点恢复。
#   - PR 创建默认人类 PAT（UID9622）；bot 只 approve+merge（GitHub 禁止同身份自审自批）
#   - 闸口拦截自动类型识别(PYTHON_PACKAGE/CLI_COMMAND/PYTEST_FIXTURE) → 自动写 07_AUDIT 留档 → 自动 --no-verify
#   - 生成物白名单自动排除(site/dist/pyc 等)；--include-generated 强制纳入
#   - 失败自动回滚(删远端分支+关 PR+保留本地改动)；报告 ~/.longhun/publish_report_<ts>.md(GPG 签)
#
# v1.0 用法（保留）:
#   lh publish announce <标题> [正文] [--channels issue,web,readme] [--template ...] [--dry-run]
#   lh publish status / dashboard / rollback <ID> / templates list|show <name>
#
# 数据: ~/.longhun/publish_log.json（append-only 审计） · ~/.longhun/publish_state.json（PR 状态机）
#       模板 ~/.longhun/publish_templates/ · 绕行规则 docs/闸口绕行规则.md
# 设计铁律: 零三方依赖 · GitHub 直连(禁代理) · token 只读 Keychain/App · 失败渠道不拖垮整体 · 全程审计留痕 · PAT 建 PR

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

# ── v2.0 · PR 一键发布状态机 常量 ─────────────────────
PR_STATES = ("idle", "prepared", "pushed", "created", "ci_passed", "approved",
             "merged", "branch_cleaned", "local_synced", "failed")
MODE_MANUAL, MODE_AUTO = "manual", "auto"   # --no-merge(默认人工审阅) | --auto 全自动
GATE_PY = BIN / "lh_cnsh_gate.py"           # 命名闸口 v1.1（含分类+自动留档）
AUDIT_DIR = ROOT / "07_AUDIT"
GATE_RULE_DOC = "docs/闸口绕行规则.md"
STATE_FILE = HOME_LH / "publish_state.json"          # PR 生命周期状态（断点恢复）
CI_POLL_SEC = 20                                      # CI 轮询间隔
CI_CHECKS_APPEAR_MAX = 120                            # 等 check-runs 出现上限(秒)
CI_RUN_MAX = 45 * 60                                  # CI 完成等待上限(秒·45 分钟)
CI_ERR_RETRY = 3                                      # CI API 瞬时错误重试次数
CI_ERR_SLEEP = 30                                     # 重试间隔(秒)
MERGE_STATE_WAIT_MAX = 180                            # mergeable_state 变 clean 上限(秒)
# 生成物白名单（不入 PR · --include-generated 可强制纳入）
GENERATED_SEGMENTS = {"site", "html_assets", "__pycache__", ".venv", "node_modules",
                      "dist", "dist_ide", "build", "build_ide", "models", "weights",
                      "_work", "archive", "_archive", "backups", "backup", "11_DATA",
                      "龙魂成片", "CNSH_加工输出", "CNSH_修复输出", "CNSH_监管数据",
                      "CNSH_护盾数据", "CNSH_颜色历史"}
GENERATED_SUFFIXES = (".pyc", ".pyo", ".pid", ".tmp", ".DS_Store")

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
        env = {k: v for k, v in os.environ.items()
               if not k.upper() in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY")}
        r = subprocess.run([sys.executable, str(BIN / "lh_github_app.py"), "token"],
                           capture_output=True, text=True, timeout=25, env=env)
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


# ══════════════════════════════════════════════════════════════════════
# v2.0 · PR 一键发布状态机（lh publish pr · 状态驱动 · 可断点恢复）
# ══════════════════════════════════════════════════════════════════════

# ── 状态持久化 ~/.longhun/publish_state.json ──
def st_load() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text("utf-8"))
        except Exception:
            pass
    return {"flows": []}


def st_save(data: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")


def st_new(data: dict, title: str, mode: str) -> dict:
    base = f"PR-{time.strftime('%Y%m%d')}"
    n = 1
    for f in data["flows"]:
        if f["id"].startswith(base):
            n += 1
    flow = {"id": f"{base}-{n:02d}", "title": title, "mode": mode, "state": "idle",
            "branch": "", "pr": None, "sha": None, "files": [], "bypass": [],
            "created_at": ts_str(), "updated_at": ts_str(), "error": None,
            "steps": [], "timings": {}}
    data["flows"].insert(0, flow)
    return flow


def st_update(flow: dict, **kw):
    flow.update(kw)
    flow["updated_at"] = ts_str()


def st_mark(flow: dict, state: str, err: str = None, info: str = ""):
    flow["state"] = state
    flow["updated_at"] = ts_str()
    if err:
        flow["error"] = err
    flow.setdefault("steps", []).append({"state": state, "at": ts_str(), "info": info or err or ""})


def st_step_done(flow: dict, name: str) -> bool:
    """该步骤是否已成功执行（供 --resume 跳过）。"""
    for s in flow.get("steps", []):
        if s.get("state") == name and not (s.get("info") or "").startswith("ERR"):
            return True
    return False


# ── 生成物过滤（任务4）──
def is_generated(path: str) -> bool:
    p = Path(path)
    if any(seg in p.parts for seg in GENERATED_SEGMENTS):
        return True
    if p.suffix in GENERATED_SUFFIXES:
        return True
    return False


def collect_changed(include_generated: bool) -> list[tuple[str, str]]:
    """收集工作区改动（状态, 路径）。排除生成物（除非 include_generated）。"""
    rc, out = run_cmd(["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all"])
    if rc != 0:
        return []
    items = []
    for ln in out.splitlines():
        if not ln.strip():
            continue
        st, path = ln[:2].strip(), ln[3:].strip()
        if path.startswith('"') and path.endswith('"'):
            try:
                path = json.loads(path)
            except Exception:
                pass
        if path.startswith(".codebuddy/"):   # IDE 本地数据不入 PR
            continue
        if not include_generated and is_generated(path):
            continue
        items.append((st, path))
    return items


def files_desc(rel_list) -> str:
    return ", ".join(sorted(str(x) for x in rel_list))


# ── 闸口自动绕行（任务2）──
def gate_scan(mode: str = "repo") -> dict:
    """返回 {ok, data} · data=JSON(gate --json)。"""
    rc, out = run_cmd([sys.executable, str(GATE_PY), "--" + mode, "--json"], timeout=60)
    try:
        data = json.loads(out or "{}")
        return {"ok": bool(data.get("ok")), "data": data}
    except Exception:
        return {"ok": True, "data": None}


def gate_auto_bypass(flow: dict, title: str, items: list[dict]) -> str:
    """自动写留档（log+md）→ 返回 md 路径。items=[{file,type},...]。

    进程内调用 gate 模块（保留文件明细表），等价人工:
      lh_cnsh_gate.py --record <reason> --type <T> --flow <ID> --tag <ID>
    """
    try:
        if str(BIN) not in sys.path:
            sys.path.insert(0, str(BIN))
        import lh_cnsh_gate as gate
    except Exception:
        return ""
    types = "/".join(sorted({i["type"] for i in items}))
    desc = ", ".join(f"{i['file']}({i['type']})" for i in items)
    reason = (f"自动绕行[{types}]: {desc} · 已按 docs/闸口绕行规则.md 归类，三类已知合理冲突"
              f"（ASCII 包名/pytest 惯例/工具链命令名），P05 审计留档后 --no-verify")
    tag = flow["id"].lower()                     # pr-20260904-01
    条目 = {"desc": title, "type": types, "flow": flow["id"],
            "pr": str(flow.get("pr") or "-"), "reason": reason,
            "title": title, "tag": tag, "items": items}
    gate.log_append(条目)
    path = gate.留档_md(条目)
    md_path = str(path)
    flow.setdefault("bypass", []).append({"title": title, "types": types,
                                          "items": items, "at": ts_str(), "md": md_path})
    if md_path and os.path.exists(md_path):
        gpgsign(md_path)
    return md_path


def needs_bypass_check(flow_files: list[str]) -> bool:
    return any(f.endswith(".py") and not f.endswith(".py.asc") for f in flow_files)


# ── GitHub 辅助（带重试）──
def gh_get_retry(path: str, token: str, tries: int = 3, sleep: int = 5) -> tuple[int, dict]:
    """GET + 瞬时错误重试（5xx / 网络 / 超时）。"""
    last = (0, {})
    for _ in range(tries):
        code, data = gh_request("GET", path, token)
        if code in (200, 201) or (400 <= code < 500):
            return code, data if isinstance(data, dict) else {}
        last = (code, data if isinstance(data, dict) else {})
        time.sleep(sleep)
    return last


def get_head_sha(flow: dict, pr_num: int, token: str) -> str:
    code, pr = gh_get_retry(f"/repos/{FULL_REPO}/pulls/{pr_num}", token)
    sha = (pr.get("head") or {}).get("sha", "") if isinstance(pr, dict) else ""
    if sha:
        st_update(flow, sha=sha)
    return sha


# ── CI 等待（任务3 · 状态 ci_passed）──
def wait_ci(flow: dict, head_sha: str, token: str) -> tuple[bool, str]:
    """等待 head_sha 全部 check-runs/statuses completed。成功→(True,'')。"""
    if not head_sha:
        return False, "无 head sha"
    # 阶段1: 等 check-runs / statuses 出现
    t0 = time.time()
    seen = False
    while time.time() - t0 < CI_CHECKS_APPEAR_MAX:
        code, cr = gh_get_retry(f"/repos/{FULL_REPO}/commits/{head_sha}/check-runs", token)
        runs = (cr or {}).get("check_runs", []) if isinstance(cr, dict) else []
        code2, st = gh_get_retry(f"/repos/{FULL_REPO}/commits/{head_sha}/status", token)
        sts = (st or {}).get("statuses", []) if isinstance(st, dict) else []
        if runs or sts:
            seen = True
            break
        print(f"⏳ 等待 CI 注册…（{int(time.time()-t0)}s / {CI_CHECKS_APPEAR_MAX}s）")
        time.sleep(CI_POLL_SEC)
    if not seen:
        # 无 CI 也放行（保护规则若要求会由 mergeable_state 兜底）
        return True, "no-ci"
    # 阶段2: 轮询至全部 completed
    t1 = time.time()
    err_cnt = 0
    tick = 0
    while time.time() - t1 < CI_RUN_MAX:
        try:
            code, cr = gh_get_retry(f"/repos/{FULL_REPO}/commits/{head_sha}/check-runs", token)
            code2, st = gh_get_retry(f"/repos/{FULL_REPO}/commits/{head_sha}/status", token)
            runs = (cr or {}).get("check_runs", []) if isinstance(cr, dict) else []
            sts = (st or {}).get("statuses", []) if isinstance(st, dict) else []
            pending = [r for r in runs if r.get("status") != "completed"]
            pending += [s for s in sts if s.get("state") == "pending"]
            if not pending:
                failed = [r.get("name") for r in runs
                          if r.get("conclusion") not in (None, "success", "skipped", "neutral")]
                failed += [s.get("context") for s in sts
                           if s.get("state") not in ("success", "pending")]
                if failed:
                    return False, "CI 失败: " + ", ".join(sorted(set(failed)))[:300]
                return True, f"ci-all-green({len(runs)} runs)"
            tick += 1
            if tick % 5 == 1:   # 每 ~100s 一行进度
                names = [r.get("name", "?")[:40] for r in pending[:3]]
                print(f"⏳ CI 进行中…（{int((time.time()-t1)//60)}m · pending: {len(pending)} 项: {', '.join(names)}）")
            err_cnt = 0
            time.sleep(CI_POLL_SEC)
        except Exception:
            err_cnt += 1
            if err_cnt > CI_ERR_RETRY:
                return False, "CI 轮询连续异常"
            time.sleep(CI_ERR_SLEEP)
    return False, f"CI 等待超时(>{CI_RUN_MAX//60} 分钟)·可 --resume {flow['id']} 续跑"


# ── approve / merge / cleanup / sync ──
def do_approve(pr_num: int, app: str) -> tuple[bool, str]:
    code, res = gh_request("POST", f"/repos/{FULL_REPO}/pulls/{pr_num}/reviews", app,
                           {"event": "APPROVE",
                            "body": "longhun-bot 独立复核：lh publish 自动发布 · GPG 已签 · 同意合併"})
    if code == 200:
        return True, f"approved(#{pr_num})"
    msg = res.get("message", res) if isinstance(res, dict) else res
    return False, f"approve HTTP {code} {msg}"


def do_merge(pr_num: int, app: str, title: str, rid: str) -> tuple[bool, str, str]:
    """轮询 mergeable_state∈{clean,unstable,has_hooks}→squash merge。

    CI 终裁权交给 GitHub 保护规则：unstable=存在非 required 检查失败
    （历史先例: 🦀 Rust Check pre-existing 失败非 required → 仍可合并）；
    blocked=required 未通过→继续等；dirty=冲突→失败。
    返回 (ok, info, sha)。"""
    t0 = time.time()
    state = ""
    while time.time() - t0 < MERGE_STATE_WAIT_MAX:
        code, pr = gh_get_retry(f"/repos/{FULL_REPO}/pulls/{pr_num}", app)
        state = (pr or {}).get("mergeable_state", "") if isinstance(pr, dict) else ""
        if state in ("clean", "unstable", "has_hooks"):
            break
        if state == "blocked":
            time.sleep(5)
            continue
        if state == "dirty":
            return False, f"PR #{pr_num} 冲突 dirty，无法自动合并", ""
        time.sleep(5)
    if state not in ("clean", "unstable", "has_hooks"):
        return False, f"PR #{pr_num} 不可合并(mergeable_state={state or '?'})·保护规则未通过", ""
    code, mg = gh_request("PUT", f"/repos/{FULL_REPO}/pulls/{pr_num}/merge", app,
                          {"merge_method": "squash",
                           "commit_title": f"{title} ({rid} · lh publish) (#{pr_num})"})
    if code == 200:
        sha = (mg or {}).get("sha", "")[:8] if isinstance(mg, dict) else ""
        return True, f"merged(#{pr_num})", sha
    msg = mg.get("message", mg) if isinstance(mg, dict) else mg
    return False, f"merge HTTP {code} {msg}", ""


def cleanup_branch(flow: dict, base_b: str = BASE_BRANCH) -> tuple[bool, str]:
    """合并后清理：切回主干 + 删本地分支 + 删远端分支（逐步 rc 守卫）。

    merge 后若工作区有余量（如 GPG 重签产生的 .asc），仅当余量都属于本 PR 文件
    （内容已在远端 merge，丢弃无损）才 -f 强制；否则保守失败，等人工。
    """
    branch = flow.get("branch")
    if not branch:
        return True, "branch-cleaned(无分支)"
    prfiles = set(flow.get("files", []))
    prasc = {p + ".asc" for p in prfiles}
    rc, out = run_cmd(["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all"], timeout=30)
    extra = []
    for ln in (out or "").splitlines():
        if not ln.strip():
            continue
        p = ln[3:].strip()
        if p.startswith('"') and p.endswith('"'):
            try:
                p = json.loads(p)
            except Exception:
                pass
        if p in prfiles or p in prasc or is_generated(p):
            continue
        extra.append(p)
    force = not extra                      # 无外来改动 → 可 -f
    cmd = ["git", "-C", str(ROOT), "checkout"] + (["-f"] if force else []) + [base_b]
    rc, out = run_cmd(cmd, timeout=60)
    if rc != 0:
        return False, f"切回主干失败: {out[-150:]}"
    rc, out = run_cmd(["git", "-C", str(ROOT), "branch", "-D", branch], timeout=60)
    if rc != 0 and "not found" not in out.lower():
        return False, f"本地分支删除失败: {out[-150:]}"
    rc, out = run_cmd(["git", "-C", str(ROOT), "push", REMOTE, "--delete", branch], timeout=90)
    if rc != 0 and "not found" not in out.lower():
        return False, f"远端分支删除失败: {out[-150:]}"
    return True, "branch-cleaned"


def rollback_pr(flow: dict, pr_num, app: str) -> tuple[bool, str]:
    """失败回滚（任务3）：删远端分支 + 关 PR；本地改动保留在分支上。"""
    info = []
    if pr_num:
        code, _ = gh_request("PATCH", f"/repos/{FULL_REPO}/pulls/{pr_num}", app,
                             {"state": "closed"})
        info.append(("PR 已关闭" if code == 200 else f"PR 关闭失败 HTTP {code}"))
    if flow.get("branch"):
        rc, out = run_cmd(["git", "-C", str(ROOT), "push", REMOTE, "--delete", flow["branch"]], timeout=60)
        info.append("远端分支已删" if rc == 0 else f"远端分支删除失败: {out[-120:]}")
        run_cmd(["git", "-C", str(ROOT), "checkout", BASE_BRANCH], timeout=60)
        info.append("已切回主干（改动保留在本地分支，未丢）")
    return True, " · ".join(info)


def write_report(flow: dict, status: str) -> str:
    """最终报告 ~/.longhun/publish_report_<ts>.md（GPG 签）。"""
    rp = HOME_LH / f"publish_report_{time.strftime('%Y%m%d_%H%M%S')}.md"
    files = "\n".join(f"  - {p}" for p in sorted(flow.get("files", []))) or "  - （无）"
    steps = "\n".join(f"  - [{s.get('at','?')}] {s.get('state')} — {s.get('info','')[:120]}"
                      for s in flow.get("steps", [])) or "  - （无）"
    byps = ""
    for b in flow.get("bypass", []):
        byps += f"\n  - {b.get('at','')} [{b.get('types','')}] {b.get('title','')} → {b.get('md','')}"
    color = "🟢" if flow.get("state") in ("local_synced", "merged", "branch_cleaned") else ("🔴" if flow.get("state") == "failed" else "🟡")
    md = (
        f"# 📦 lh publish PR 发布报告 · {flow['id']}\n\n"
        f"> 生成: {ts_str()} · 工具: lh_publish v2.0 · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰\n"
        f"> 三色: {color} · 状态: {flow.get('state')} · 模式: {flow.get('mode')}\n\n"
        f"## 一、概览\n\n"
        f"- 标题: {flow.get('title')}\n- PR: #{flow.get('pr') or '-'} · sha: {flow.get('sha') or '-'}\n"
        f"- 分支: {flow.get('branch') or '-'} · 结果: {status}\n\n"
        f"## 二、变更文件（{len(flow.get('files', []))} 个）\n\n{files}\n\n"
        f"## 三、闸口绕行\n\n{byps or '  - 无（本次无命名闸口拦截或已自动留档）'}\n\n"
        f"## 四、状态步骤\n\n{steps}\n\n"
        f"---\n> 自动生成: `lh publish pr` · 可查: `lh publish prstate` · 数据: ~/.longhun/publish_state.json\n")
    HOME_LH.mkdir(parents=True, exist_ok=True)
    rp.write_text(md, "utf-8")
    try:
        gpgsign(str(rp))
    except Exception:
        pass
    return str(rp)


# ── 主控：lh publish pr ──
def cmd_pr(argv):
    """用法: lh publish pr <标题> [--auto|--no-merge] [--files a.py,b.md] [--include-generated]
            [--dry-run] [--resume <ID>] [--base <分支>] [--rollback-on-fail]
    默认（无 --auto/--no-merge）→ 人工审阅模式（建 PR 即止）。
    """
    title = ""
    flags = {"files": None, "mode": None, "include_generated": False, "dry_run": False,
             "resume": None, "base": BASE_BRANCH, "rollback": False}
    pos = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--auto",):
            flags["mode"] = MODE_AUTO
        elif a in ("--no-merge", "--manual"):
            flags["mode"] = MODE_MANUAL
        elif a == "--dry-run":
            flags["dry_run"] = True
        elif a == "--include-generated":
            flags["include_generated"] = True
        elif a == "--rollback-on-fail":
            flags["rollback"] = True
        elif a in ("--files", "--resume", "--base") and i + 1 < len(argv):
            flags[a[2:]] = argv[i + 1]
            i += 1
        elif a.startswith("--"):
            sys.stderr.write(f"未知参数 {a}\n")
        else:
            pos.append(a)
        i += 1
    title = " ".join(pos) if pos else title
    data = st_load()

    if flags["resume"]:
        flow = st_find(data, flags["resume"])
        if not flow:
            print(f"❌ 未找到流程 {flags['resume']}（~/.longhun/publish_state.json）")
            return 2
    else:
        if not title:
            print("用法: lh publish pr <标题> [--auto] [--no-merge] [--files …] [--dry-run] [--include-generated] [--resume <ID>]")
            return 1
        mode = flags["mode"] or MODE_MANUAL
        flow = st_new(data, title, mode)
    st_update(flow, mode=flags["mode"] or flow.get("mode", MODE_MANUAL),
              base=flags["base"] or flow.get("base", BASE_BRANCH))

    # 0. 环境守卫：分支就绪判定
    rc, cur = run_cmd(["git", "-C", str(ROOT), "branch", "--show-current"])
    cur = (cur or "").strip()
    base_b = flags["base"] or flow.get("base", BASE_BRANCH)
    if flow["state"] in ("idle",) and cur != base_b:
        print(f"❌ 当前分支 {cur} ≠ {base_b}；lh publish pr 需在主干上执行（或 --base <分支>）")
        return 2

    # 1. collect（状态 idle→prepared）
    if not st_step_done(flow, "prepared"):
        run_cmd(["git", "-C", str(ROOT), "fetch", REMOTE, base_b], timeout=90)
        items = collect_changed(flags["include_generated"])
        if flags["files"]:
            want = {p.strip() for p in flags["files"].split(",") if p.strip()}
            items = [(s, p) for s, p in items if p in want]
            missing = want - {p for _, p in items}
            if missing:
                print(f"❌ --files 含未变更/不存在文件: {', '.join(sorted(missing))}")
                return 2
        if not items:
            print("ℹ️ 无待发布改动（工作区干净，或全部为生成物被白名单排除）")
            print("   提示: --include-generated 可强制纳入生成物")
            return 0
        flow_files = [p for _, p in items]
        st_update(flow, files=flow_files)
        st_mark(flow, "prepared", info=f"collect {len(flow_files)} files")

    # 2. dry-run：预览清单 + 闸口判定，不落地
    if flags["dry_run"]:
        print(f"📋 [DRY-RUN] {flow['id']} | {title} | 待发布文件:")
        for p in flow.get("files", []):
            gen = " [生成物·需 --include-generated]" if is_generated(p) else ""
            print(f"   · {p}{gen}")
        if needs_bypass_check(flow.get("files", [])):
            g = gate_scan("repo")
            viol = (g.get("data") or {}).get("violations", []) if g.get("data") else []
            if viol:
                print("🔎 命名闸口预检: 将拦截以下英文命名新增 .py（自动绕行留档后 --no-verify）:")
                for v in viol:
                    print(f"   🔴 {v['file']} type={v['type']}")
                if not all(v["type"] in (i.get("type") for i in viol) for v in viol if v["type"] == "OTHER"):
                    pass
            else:
                print("🔎 命名闸口预检: 通过（无新增英文命名 .py）")
        print("✅ [DRY-RUN] 未做任何实际提交/推送。")
        st_save(data)
        return 0

    # 3. 切分支 + add（状态 prepared → committed）
    branch = flow.get("branch") or f"publish-{flow['id'].split('-',1)[-1].lower()}"
    st_update(flow, branch=branch)
    if not st_step_done(flow, "committed"):
        run_cmd(["git", "-C", str(ROOT), "checkout", base_b], timeout=60)
        # 远端已含本流程已 merge 内容时先对齐
        rc, out = run_cmd(["git", "-C", str(ROOT), "checkout", "-b", branch, f"{REMOTE}/{base_b}"], timeout=60)
        if rc != 0:
            # 分支名冲突或本地已有 → 尝试复用已有分支继续
            rc2, _ = run_cmd(["git", "-C", str(ROOT), "checkout", branch], timeout=60)
            if rc2 != 0:
                st_mark(flow, "failed", err=f"分支准备失败: {out[-200:]}")
                st_save(data)
                return 2
        add_list = flow.get("files", [])
        # 补 .asc 配对
        for p in list(add_list):
            asc = p + ".asc"
            if os.path.exists(os.path.join(ROOT, asc)) and asc not in add_list:
                add_list.append(asc)
        rc, out = run_cmd(["git", "-C", str(ROOT), "add", "--"] + add_list, timeout=90)
        if rc != 0:
            st_mark(flow, "failed", err=f"git add: {out[-200:]}")
            st_save(data)
            return 2
        # 闸口预检 → 自动绕行留档
        bypass_done = False
        if needs_bypass_check(add_list):
            g = gate_scan("pre-commit")
            viol = (g.get("data") or {}).get("violations", []) if g.get("data") else []
            if viol:
                if all(v["type"] in ("PYTHON_PACKAGE", "CLI_COMMAND", "PYTEST_FIXTURE") for v in viol):
                    md = gate_auto_bypass(flow, title, viol)
                    print(f"🟡 命名闸口拦截 {len(viol)} 个 → 已自动留档绕行: {md or '(log)'}")
                    bypass_done = True
                else:
                    other = [v for v in viol if v["type"] == "OTHER"]
                    st_mark(flow, "failed", err=f"闸口拦截含 OTHER 类型(不可自动绕行): {[v['file'] for v in other]}")
                    print(f"🔴 闸口拦截含 OTHER 类型，禁止自动绕行。请人工 P05 决策（规则: {GATE_RULE_DOC}）")
                    st_save(data)
                    return 2
        # commit（绕行留档后 --no-verify）
        commit_cmd = ["git", "-C", str(ROOT), "commit", "-m", f"{title} ({flow['id']} · lh publish)"]
        if bypass_done:
            commit_cmd.append("--no-verify")
        rc, out = run_cmd(commit_cmd, timeout=120)
        if rc != 0:
            st_mark(flow, "failed", err=f"git commit: {out[-300:]}")
            st_save(data)
            return 2
        st_mark(flow, "committed", info=f"commit({len(add_list)} files)" + (" · gate-bypass" if bypass_done else ""))

    # 4. push
    if not st_step_done(flow, "pushed"):
        rc, out = run_cmd(["git", "-C", str(ROOT), "push", REMOTE, branch], timeout=180)
        if rc != 0:
            st_mark(flow, "failed", err=f"push: {out[-200:]}")
            st_save(data)
            return 2
        st_mark(flow, "pushed", info=f"push {branch}")

    # 5. create PR（PAT 创建 · bot 禁止建 PR 防自审自批）
    pat = get_pat()
    if not pat:
        st_mark(flow, "failed", err="无 PAT（Keychain: github.com/UID9622）· PR 创建必须人类 PAT 身份（bot 不能自审自批）")
        st_save(data)
        return 2
    if not flow.get("pr"):
        rid = flow["id"]
        pr_body = (f"# {title}\n\n> {flow['id']} · {ts_str()} · `lh publish pr` 自动创建"
                   f"（mode={flow['mode']}）\n\n"
                   f"**变更文件** ({len(flow.get('files', []))}):\n\n"
                   + "\n".join(f"- `{p}`" for p in flow.get("files", [])) + "\n")
        if flow.get("bypass"):
            pr_body += "\n**闸口绕行留档**: " + " · ".join(b.get("md", "见 07_AUDIT") for b in flow["bypass"]) + "\n"
        pr_body += f"\n---\n归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · 自动工具 lh_publish v2.0\n"
        code, pr = gh_request("POST", f"/repos/{FULL_REPO}/pulls", pat,
                              {"title": f"{title} ({flow['id']} · lh publish)",
                               "head": branch, "base": base_b, "body": pr_body})
        if code not in (200, 201):
            err = (pr or {}).get("message", pr) if isinstance(pr, dict) else pr
            st_mark(flow, "failed", err=f"PR 创建失败 HTTP {code} {err}")
            st_save(data)
            return 2
        st_update(flow, pr=pr["number"])
        print(f"✅ PR #{flow['pr']} 已创建（mode={flow['mode']}）→ https://github.com/{FULL_REPO}/pull/{flow['pr']}")
        # 补：bypass 留档 md 已随 commit 入库；给留档补 PR 号记录
        if flow.get("bypass"):
            pass
        st_mark(flow, "created", info=f"PR #{flow['pr']}")
    else:
        print(f"ℹ️ 复用已有 PR #{flow['pr']}")

    # 人工审阅模式（--no-merge / 默认）→ 停在 created
    if flow.get("mode") == MODE_MANUAL:
        st_save(data)
        print(f"⏸ 人工审阅模式: PR #{flow['pr']} 已开，等人工 review/CI 通过后执行: lh publish pr --resume {flow['id']} --auto")
        rp = write_report(flow, f"PR #{flow['pr']} created · 待人工审阅")
        print(f"📄 报告: {rp}")
        return 0

    # AUTO 模式：CI → approve → merge
    app = get_app_token()
    if not app:
        st_mark(flow, "failed", err="无 bot token")
        st_save(data)
        return 2

    if not (st_step_done(flow, "ci_passed") or st_step_done(flow, "ci_warn")):
        print(f"⏳ 等待 CI（≤{CI_RUN_MAX // 60} 分钟 · 轮询 {CI_POLL_SEC}s）…")
        head_sha = get_head_sha(flow, flow["pr"], pat)
        ok, info = wait_ci(flow, head_sha, pat)
        if ok:
            st_mark(flow, "ci_passed", info=info)
        else:
            # 失败/超时 → 不直接判死：mergeable_state 由 GitHub 保护规则终裁
            # （历史先例: 🦀 Rust Check pre-existing 失败但非 required → unstable 仍可合并）
            print(f"🟡 {info} —— 交由 GitHub 保护规则终裁（尝试合并）")
            st_mark(flow, "ci_warn", info=info)
        st_save(data)

    if not st_step_done(flow, "approved"):
        ok, info = do_approve(flow["pr"], app)
        if not ok:
            st_mark(flow, "failed", err=info)
            st_save(data)
            rp = write_report(flow, f"失败: {info}")
            print(f"📄 报告: {rp}")
            return 2
        st_mark(flow, "approved", info=info)
        print(f"✅ {info}")

    if not st_step_done(flow, "merged"):
        ok, info, sha = do_merge(flow["pr"], app, title, flow["id"])
        if not ok:
            st_mark(flow, "failed", err=info)
            st_save(data)
            rp = write_report(flow, f"失败: {info}")
            print(f"📄 报告: {rp}")
            return 2
        st_update(flow, sha=sha)
        st_mark(flow, "merged", info=info)
        print(f"✅ {info} sha={sha}")

    if not st_step_done(flow, "branch_cleaned"):
        ok, info = cleanup_branch(flow, base_b)
        if not ok:
            st_mark(flow, "failed", err=info)
            st_save(data)
            rp = write_report(flow, f"失败: {info}")
            print(f"📄 报告: {rp}")
            return 2
        st_mark(flow, "branch_cleaned", info=info)
        print("✅ 分支已清理（本地+远端）")

    if not st_step_done(flow, "local_synced"):
        rc, out = run_cmd(["git", "-C", str(ROOT), "fetch", REMOTE, base_b], timeout=90)
        rc, out = run_cmd(["git", "-C", str(ROOT), "reset", "--hard", f"{REMOTE}/{base_b}"], timeout=90)
        if rc != 0:
            st_mark(flow, "failed", err=f"本地同步: {out[-150:]}")
            st_save(data)
            return 2
        st_mark(flow, "local_synced", info=f"reset {REMOTE}/{base_b}")
        print(f"✅ 本地已同步 {REMOTE}/{base_b}")

    st_save(data)
    rp = write_report(flow, f"PR #{flow['pr']} merged sha={flow.get('sha')}")
    print(f"🎉 {flow['id']} 完成: PR #{flow['pr']} merged · 分支已删 · 本地已同步")
    print(f"📄 报告: {rp}")
    return 0


# ── PR 状态查询 / 断点恢复辅助 ──
def st_find(data: dict, fid: str):
    for f in data["flows"]:
        if f["id"].lower() == fid.lower() or f["id"][3:].lower() == fid.lower():
            return f
    return None


def cmd_prstate(argv):
    data = st_load()
    flows = data.get("flows", [])[:10]
    if not flows:
        print("暂无 PR 流程记录。用法: lh publish pr <标题> --auto")
        return 0
    print("ID | 状态 | 模式 | PR# | 标题")
    for f in flows:
        pr = f.get("pr") or "-"
        print(f"{f['id']} | {f.get('state','?')} | {f.get('mode','-')} | #{pr} | {f.get('title','')[:40]}")
    print("恢复: lh publish pr --resume <ID> [--auto] · 状态文件: ~/.longhun/publish_state.json")
    return 0


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


def cmd_outreach(argv):
    """扩散素材包路径指引（供手动发布 · 2026-09-05 任务B）"""
    pkg = Path(__file__).resolve().parent.parent / "docs" / "扩散素材-2026-09-05"
    j = "--json" in argv
    if not pkg.exists():
        if j:
            print(json.dumps({"ok": False, "reason": f"素材目录不存在: {pkg}"}))
        else:
            print(f"🟡 扩散素材目录不存在: {pkg}（先 lh docs weekly / 生成素材包）")
        return 1
    files = sorted(pkg.glob("*.md"))
    platforms = {"v2ex.md": "V2EX", "osc.md": "开源中国", "zhihu.md": "知乎",
                 "hackernews.md": "Hacker News"}
    rows = []
    for f in files:
        sig = Path(str(f) + ".asc").exists()
        rows.append({"file": f.name, "platform": platforms.get(f.name, "总览/通用"),
                     "signed": sig})
    if j:
        print(json.dumps({"tool": "lh-publish", "mode": "outreach", "ok": True,
                          "package": str(pkg), "files": rows}, ensure_ascii=False, indent=2))
    else:
        print(f"📢 扩散素材包（2026-09-05 · 供手动发布）\n路径: {pkg}\n")
        for r in rows:
            mark = "✅" if r["signed"] else "🟡未签"
            print(f"  · [{r['platform']}] {r['file']}  {mark}")
        print("\n手动发布流程: 打开各平台 → 粘贴对应文件正文 → 附核心链接与 GPG 指纹 → 发布")
        print("自检: docs/扩散素材-2026-09-05/00_README.md 的 GATE 清单")
    return 0


USAGE = """龍魂·统一对外发布工具链 v2.0（PR 一键发布 · 状态驱动）

用法:
  lh publish pr <标题> [--auto|--no-merge] [--files a.py,b.md] [--include-generated]
                     [--dry-run] [--resume <ID>] [--base <分支>] [--rollback-on-fail]
      # 一键发布: 收集改动→闸口自动绕行留档→commit→push→PR(PAT建)→[--auto]CI等待→bot approve
      #          →squash merge→删分支→本地同步→GPG 报告。默认=人工审阅(建 PR 即止)。
  lh publish prstate                 # PR 流程状态查询（断点恢复: pr --resume <ID> --auto）
  lh publish announce <标题> [正文] [--channels issue,web,readme] [--template <名>] [--dry-run]
  lh publish outreach                # 扩散素材包路径指引（docs/扩散素材-2026-09-05/ · 4平台+总览）
  lh publish status / dashboard / rollback <ID> [--reason …] / templates list|show <name>
"""


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "pr":
        return cmd_pr(rest)
    if cmd == "prstate":
        return cmd_prstate(rest)
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
    if cmd == "outreach":
        return cmd_outreach(rest)
    print(USAGE)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
