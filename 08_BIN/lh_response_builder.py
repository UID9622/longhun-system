#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·辛巳·戌时·䷞咸-RESPONSE-BUILDER-V1.0-2c3d4e5f
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
📮 龍魂·质疑响应生成器 v1.0 — lh response build|post|wall|status

功能: 读取最新验证报告 → 自动生成 Issue 回复（致谢/验证摘要/数据链接/结论/可复现指令）
      → post 发布到 GitHub。验证事件统一落 validation/events.jsonl（耻辱墙联动事件墙）。

回复铁律: 用数据回应质疑·不争论·可复现·可追溯。
数据: ~/.longhun/validation/reports/issue_{id}/latest.json · events.jsonl
"""

import os
import sys
import json
import argparse
import urllib.request
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple

VALIDATION_ROOT = Path.home() / ".longhun" / "validation"
REPORTS_DIR = VALIDATION_ROOT / "reports"
EVENTS_FILE = VALIDATION_ROOT / "events.jsonl"
DEFAULT_REPO = "deepseek-ai/DeepSeek-V3"

REPO_HOME = "https://github.com/UID9622/longhun-system"
数据集入口 = "https://github.com/deepseek-ai/DeepSeek-V3/issues/1622"


# ============================================================
# 一、GitHub 工具（token 读取链: env → Keychain）
# ============================================================
def _load_token() -> Tuple[Optional[str], str]:
    for var in ("GH_TOKEN", "GITHUB_TOKEN"):
        if os.environ.get(var):
            return os.environ[var].strip(), f"env:{var}"
    try:
        out = subprocess.run(
            ["security", "find-internet-password", "-s", "github.com", "-a", "UID9622", "-w"],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip(), "Keychain(github.com/UID9622)"
    except Exception:
        pass
    return None, "anonymous"


def _gh_request(method: str, path: str, body: Optional[Dict] = None) -> Optional[Dict]:
    token, src = _load_token()
    if not token:
        print(f"  🔴 无 GitHub token（env GH_TOKEN/GITHUB_TOKEN 或 Keychain github.com/UID9622）· 已生成草稿可手工发")
        return None
    url = "https://api.github.com" + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Accept": "application/vnd.github+json",
                                          "Authorization": f"Bearer {token}",
                                          "User-Agent": "longhun-response-builder/1.1",
                                          "X-GitHub-Api-Version": "2022-11-28"})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 强制直连·不认系统代理
    try:
        with opener.open(req, timeout=20) as r:
            raw = r.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        print(f"  🔴 GitHub {method} {path} → HTTP {e.code}: {e.read().decode('utf-8')[:300]}")
        return None
    except Exception as e:
        print(f"  🔴 GitHub {method} {path} → {e}")
        return None


# ============================================================
# 二、回复草稿生成
# ============================================================
def _issue_dir(issue_id: str) -> Path:
    d = REPORTS_DIR / f"issue_{issue_id}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _read_latest_report(issue_id: str) -> Optional[Dict]:
    fp = _issue_dir(issue_id) / "latest.json"
    if not fp.exists():
        return None
    try:
        return json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return None


def _read_issue_rec(issue_id: str) -> Optional[Dict]:
    fp = VALIDATION_ROOT / "issues.jsonl"
    if not fp.exists():
        return None
    for line in reversed(fp.read_text(encoding="utf-8").splitlines()):
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if str(rec.get("issue_id")) == str(issue_id):
            return rec
    return None


def _fmt_percent(v) -> str:
    return f"{v:.0%}" if isinstance(v, (int, float)) else str(v)


def 生成回复(report: Dict, issue_rec: Optional[Dict]) -> str:
    iid = report.get("issue_id", "?")
    质疑者 = (issue_rec or {}).get("质疑者", "作者")
    op = report.get("当前操作点0.5", {})
    色 = report.get("结论", {}).get("三色", "🟡")
    建议 = report.get("结论", {}).get("建议", "")
    rows = report.get("阈值扫描", [])

    lines = []
    lines.append(f"感谢 @{质疑者} 的质疑。这份批评指到两个真缺口：**只报告了 0 命中，既没证明检测器会干活（召回率），也没证明弱指纹不会误伤（假阳性率）**。")
    lines.append(f"已按建议补上正负样本实测，把阈值从『声明』变成『可验证的操作点』。\n")
    lines.append("## 验证摘要")
    lines.append("| 指标 | 数值 |")
    lines.append("|:---|:---|")
    lines.append(f"| 正样本（强指纹×改写形态·验证召回） | {report.get('样本量', {}).get('正样本总量', '-')} 条 |")
    lines.append(f"| 负样本（无关+近邻干扰·验证假阳性） | {report.get('样本量', {}).get('负样本总量', '-')} 条 |")
    lines.append(f"| 检测器 | 龍魂指纹库（DNA/组合逻辑/品牌独有词加权） |")
    lines.append(f"| **TPR（召回率）@0.5** | **{_fmt_percent(op.get('TPR'))}** |")
    lines.append(f"| **FPR（假阳性）@0.5** | **{_fmt_percent(op.get('FPR'))}** |")
    lines.append("")
    lines.append("### 阈值扫描（找可验证操作点）")
    lines.append("| 阈值 | TPR | FPR |")
    lines.append("|:---:|:---:|:---:|")
    for r in rows:
        mark = " ← 当前操作点" if abs(r["阈值"] - 0.5) < 1e-9 else ""
        lines.append(f"| {r['阈值']} | {_fmt_percent(r['TPR'])} | {_fmt_percent(r['FPR'])} |{mark}")
    lines.append("")
    lines.append("## 结论")
    lines.append(f"- {色} {建议}")
    lines.append("")
    lines.append("## 数据与报告")
    lines.append(f"- 验证报告: `~/.longhun/validation/reports/issue_{iid}/latest.md`（含逐档数据）")
    lines.append(f"- 数据集主入口: {数据集入口}")
    lines.append(f"- 耻辱墙: {REPO_HOME}（验证事件 append-only 记录）")
    lines.append("")
    lines.append("## 可复现指令")
    lines.append("```")
    lines.append("lh challenge parse 1622   # 拉取本条质疑入队列")
    lines.append("lh strategy run 1622      # 执行正负样本验证(纯本地·零网络)")
    lines.append("lh strategy report 1622   # 查看完整报告")
    lines.append("lh response wall          # 查看验证事件墙")
    lines.append("```")
    lines.append("")
    lines.append("> 龍魂原则：任何 issue/质疑 → 第一反应不是解释，是跑验证把数据贴回来。")
    lines.append("> 龍魂审计数据集 · 诸葛鑫 | UID9622 · 龍芯北辰")
    return "\n".join(lines)


def cmd_build(issue_id: str):
    """生成回复草稿 → 打印并落盘"""
    report = _read_latest_report(issue_id)
    if not report:
        print(f"  🔴 无验证报告（先 lh strategy run {issue_id}）")
        return 1
    rec = _read_issue_rec(issue_id)
    body = 生成回复(report, rec)
    d = _issue_dir(issue_id)
    fp = d / f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    fp.write_text(body, encoding="utf-8")
    print(body)
    print(f"\n  📮 回复草稿已存: {fp}")
    return 0


def cmd_post(issue_id: str, repo: str = DEFAULT_REPO):
    """构建并发布评论到 GitHub Issue"""
    report = _read_latest_report(issue_id)
    if not report:
        print(f"  🔴 无验证报告（先 lh strategy run {issue_id}）")
        return 1
    body = 生成回复(report, _read_issue_rec(issue_id))
    print("  📮 发布中…")
    resp = _gh_request("POST", f"/repos/{repo}/issues/{issue_id}/comments", {"body": body})
    if resp is None:
        print("  ⏸️ 发布失败·草稿已保留可手工发。发送失败非异常——先自查权限（lh github test-perms）")
        return 1
    url = resp.get("html_url", "")
    print(f"  ✅ 已发布: {url}")
    _标记responded(issue_id, url)
    return 0


def _标记responded(issue_id: str, url: str):
    fp = VALIDATION_ROOT / "issues.jsonl"
    if not fp.exists():
        return
    lines = fp.read_text(encoding="utf-8").splitlines()
    for i in range(len(lines) - 1, -1, -1):
        try:
            rec = json.loads(lines[i])
        except Exception:
            continue
        if str(rec.get("issue_id")) == str(issue_id) and rec.get("状态") in ("pending", "validating"):
            rec["状态"] = "responded"
            rec["回应URL"] = url
            lines[i] = json.dumps(rec, ensure_ascii=False)
            break
    fp.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def cmd_wall():
    """验证事件墙（events.jsonl 聚合）"""
    if not EVENTS_FILE.exists():
        print("  🟢 暂无验证事件")
        return 0
    evs = [json.loads(l) for l in EVENTS_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"  📮 验证事件墙（共 {len(evs)} 条 · append-only）")
    for ev in reversed(evs[-15:]):
        print(f"   [{ev.get('事件')}] Issue #{ev.get('issue_id')} · "
              f"TPR={_fmt_percent(ev.get('TPR'))} FPR={_fmt_percent(ev.get('FPR'))} · {ev.get('三色')}")
    return 0


def cmd_status(issue_id: str):
    rec = _read_issue_rec(issue_id)
    if not rec:
        print(f"  🔴 无记录（先 lh challenge parse {issue_id}）")
        return 1
    print(f"  📮 Issue {issue_id} · 状态 {rec.get('状态')} · v{rec.get('状态版本', 1)}")
    if rec.get("回应URL"):
        print(f"     回应: {rec['回应URL']}")
    rep = _read_latest_report(issue_id)
    if rep:
        op = rep.get("当前操作点0.5", {})
        print(f"     最新报告: TPR={_fmt_percent(op.get('TPR'))} FPR={_fmt_percent(op.get('FPR'))} · {rep.get('结论', {}).get('三色', '')}")
    return 0


def main():
    parser = argparse.ArgumentParser(description='龍魂·质疑响应生成器')
    sub = parser.add_subparsers(dest='command', help='子命令')

    p_build = sub.add_parser('build', help='生成回复草稿')
    p_build.add_argument('issue_id', help='Issue 编号')

    p_post = sub.add_parser('post', help='发布回复到 GitHub Issue')
    p_post.add_argument('issue_id', help='Issue 编号')
    p_post.add_argument('--repo', default=DEFAULT_REPO, help='仓库 owner/repo')

    sub.add_parser('wall', help='验证事件墙')

    p_st = sub.add_parser('status', help='回应状态')
    p_st.add_argument('issue_id', help='Issue 编号')

    args = parser.parse_args()
    if args.command == 'build':
        return cmd_build(args.issue_id)
    if args.command == 'post':
        return cmd_post(args.issue_id, args.repo)
    if args.command == 'wall':
        return cmd_wall()
    if args.command == 'status':
        return cmd_status(args.issue_id)
    parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
