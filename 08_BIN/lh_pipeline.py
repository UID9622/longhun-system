#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·癸丑·亥时·䷍大有-PIPELINE-V1.0-RESOURCE-CHAIN
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）+ 工程实现层 MulanPSL v2
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂·資源链路引擎 v1.0
================================
把「AI产出 → GitHub发布 → 鲲鹏部署 → Bark通知」串成一条命令。

用法:
  python3 bin/lh_pipeline.py <文件> [选项]

选项:
  --github [仓库]     GitHub 发布（默认 UID9622/longhun-system，落到 ai-outputs/ 子目录）
  --kunpeng [路径]    鲲鹏部署（默认 /opt/longhun/bin/）
  --notion            归档到 Notion（调 :8779 bridge，可选）
  --no-bark           不发 Bark 推送
  --all               全链路（GitHub + 鲲鹏 + Bark）
  --dry-run           演练，只打印要做什么，不真执行

示例:
  python3 bin/lh_pipeline.py 08_BIN/lh_resources_overview.py --all
  python3 bin/lh_pipeline.py articles/foo.md --github UID9622/longhun-articles-en
  python3 bin/lh_pipeline.py 08_BIN/xxx.py --kunpeng /opt/longhun/bin/ --no-bark
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# ── 常量 ──────────────────────────────────────────────
LH_ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = LH_ROOT / "bin"
SSH_KEY = str(Path.home() / ".ssh" / "longhun_kunpeng_ed25519")
KUNPENG_HOST = "root@119.13.90.27"
DEFAULT_REPO = "UID9622/longhun-system"
DEFAULT_KUNPENG_DIR = "/opt/longhun/bin/"
BARK_KEY = os.getenv("BARK_KEY", "BoWn76MNipaRA8RwrWqksP")
NOTION_BRIDGE = "http://127.0.0.1:8779"

OWNER_MARK = "诸葛鑫"          # 归属名判定
DNA_RE = re.compile(r"#龍芯|#ZHUGEXIN|#龙芯")

# ── 工具 ──────────────────────────────────────────────
def log(msg, ok=True):
    tag = "🟢" if ok else "🔴"
    print(f"{tag} {msg}")

def run(cmd, timeout=120):
    """执行命令，返回 (code, stdout)"""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 1, "TIMEOUT"

def sh(cmd, timeout=120):
    code, out = run(cmd, timeout)
    return code, out

# ── 各段链路 ──────────────────────────────────────────
def prep_file(path: Path):
    """① 准备：检查存在 → 归属名/DNA 头 → GPG 补签"""
    if not path.exists():
        log(f"文件不存在: {path}", False)
        return False
    head = path.read_text(encoding="utf-8", errors="ignore")[:800]
    if not OWNER_MARK in head:
        log(f"⚠️ 文件缺归属名「诸葛鑫」（P0级·应补）—— 不阻塞，提醒")
    if not DNA_RE.search(head):
        log(f"⚠️ 文件缺 DNA 头 —— 不阻塞，提醒")
    # GPG 补签
    signer = BIN_DIR / "lh_gpg_sign.py"
    if signer.exists():
        code, out = sh(["python3", str(signer), "sign", "--force", str(path)])
        log(f"GPG 补签 {'OK' if code == 0 else '失败: ' + out.strip()[-200:]}", code == 0)
    return True

def _gh_remote_sha(repo: str, remote_path: str):
    """查仓库内文件是否已存在，返回其 sha（不存在返回 None）"""
    code, out = sh(["gh", "api", f"repos/{repo}/contents/{remote_path}",
                    "--jq", ".sha"])
    if code == 0 and out.strip() and out.strip() != "null":
        return out.strip()
    return None

def push_github(path: Path, repo: str):
    """② GitHub 发布：gh api 上传到仓库 ai-outputs/ 子目录（不碰仓库其他文件）"""
    rel = path.name
    remote_path = f"ai-outputs/{rel}"
    b64 = base64.b64encode(path.read_bytes()).decode()
    msg = f"资源链路 v1.0 推送: {rel}（诸葛鑫 UID9622）"
    cmd = [
        "gh", "api", "--method", "PUT",
        f"repos/{repo}/contents/{remote_path}",
        "-f", f"message={msg}",
        "-f", f"content={b64}",
        "-f", "branch=orphan_main",
    ]
    # 文件已存在 → 必须带 sha 才能覆盖更新
    sha = _gh_remote_sha(repo, remote_path)
    if sha:
        cmd += ["-f", f"sha={sha}"]
    code, out = sh(cmd)
    if code == 0:
        log(f"GitHub 发布 OK → https://github.com/{repo}/blob/orphan_main/{remote_path}")
    else:
        log(f"GitHub 发布失败: {out.strip()[-300:]}", False)
    return code == 0

def deploy_kunpeng(path: Path, target_dir: str):
    """③ 鲲鹏部署：scp 到 /opt/longhun/bin/"""
    cmd = [
        "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
        "-o", "ConnectTimeout=10",
        str(path), f"{KUNPENG_HOST}:{target_dir}",
    ]
    code, out = sh(cmd)
    if code == 0:
        log(f"鲲鹏部署 OK → {KUNPENG_HOST}:{target_dir}{path.name}")
    else:
        log(f"鲲鹏部署失败: {out.strip()[-200:]}", False)
    return code == 0

def notify_bark(title: str, body: str):
    """④ Bark 推送（默认开，--no-bark 关）—— 先 percent-encode 再 curl（绕开空格 404 与 Python urllib 的 SOCKS 代理坑）"""
    import urllib.parse
    enc_title = urllib.parse.quote(title)
    enc_body = urllib.parse.quote(body)
    url = f"https://api.day.app/{BARK_KEY}/{enc_title}/{enc_body}"
    cmd = ["curl", "-s", "--max-time", "8", url]
    code, out = sh(cmd)
    if code == 0:
        try:
            data = json.loads(out)
            ok = data.get("code") == 200
        except Exception:
            ok = bool(out.strip())
        log(f"Bark 推送 {'OK' if ok else '异常: ' + out.strip()[:120]}", ok)
        return ok
    log(f"Bark 推送失败: {out.strip()[:120]}", False)
    return False

def archive_notion(path: Path):
    """⑤ Notion 归档（可选）：调 bridge :8779"""
    import urllib.request
    title = f"资源链路归档: {path.name}"
    content = path.read_text(encoding="utf-8", errors="ignore")[:4000]
    payload = json.dumps({"title": title, "content": content}).encode()
    try:
        req = urllib.request.Request(f"{NOTION_BRIDGE}/archive",
                                     data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            log(f"Notion 归档响应: {r.read().decode()[:120]}")
        return True
    except Exception as e:
        log(f"Notion 归档跳过（bridge 未开）: {e}", True)
        return False

# ── 主流程 ────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="龍魂資源链路引擎 v1.0")
    ap.add_argument("file", help="要推送的文件/目录")
    ap.add_argument("--github", nargs="?", const=DEFAULT_REPO, default=None,
                    help="GitHub 发布（默认仓库 UID9622/longhun-system）")
    ap.add_argument("--kunpeng", nargs="?", const=DEFAULT_KUNPENG_DIR, default=None,
                    help="鲲鹏部署（默认 /opt/longhun/bin/）")
    ap.add_argument("--notion", action="store_true", help="归档到 Notion")
    ap.add_argument("--no-bark", action="store_true", help="不发 Bark")
    ap.add_argument("--all", action="store_true", help="全链路 GitHub+鲲鹏+Bark")
    ap.add_argument("--dry-run", action="store_true", help="演练不真执行")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        log(f"文件不存在: {args.file}", False)
        sys.exit(1)

    # 解析执行项
    do_github = args.all or args.github is not None
    do_kunpeng = args.all or args.kunpeng is not None
    do_bark = args.all or (args.github or args.kunpeng) and not args.no_bark
    do_notion = args.notion

    repo = args.github or DEFAULT_REPO
    kdir = args.kunpeng or DEFAULT_KUNPENG_DIR

    log(f"══ 龍魂資源链路 v1.0 ══ 目标: {path.name}")
    if args.dry_run:
        log(f"演练模式：将执行 GitHub→{repo} 鲲鹏→{kdir} Bark→{'开' if do_bark else '关'} Notion→{'开' if do_notion else '关'}")
        sys.exit(0)

    # ① 准备 + GPG 补签
    if not prep_file(path):
        sys.exit(1)

    # ② GitHub
    if do_github:
        if not push_github(path, repo):
            log("链路中断在 GitHub 段，后续跳过", False)
            sys.exit(1)

    # ③ 鲲鹏
    if do_kunpeng:
        if not deploy_kunpeng(path, kdir):
            log("链路中断在鲲鹏段，后续跳过", False)
            sys.exit(1)

    # ⑤ Notion（可选）
    if do_notion:
        archive_notion(path)

    # ④ Bark
    if do_bark:
        notify_bark("龍魂資源链路 ✅",
                    f"{path.name} 已推送: GitHub={'✓' if do_github else '-'} 鲲鹏={'✓' if do_kunpeng else '-'}")

    log(f"══ 链路完成 ══ {path.name}", True)


if __name__ == "__main__":
    main()
