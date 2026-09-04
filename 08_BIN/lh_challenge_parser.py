#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丁酉·辛巳·戌时·䷞咸-CHALLENGE-PARSER-V1.2-4a1b2c3d
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🎯 龍魂·社区质疑解析引擎 v1.2 — lh challenge parse|add|list|status|respond|check

功能: 拉取社区 Issue 评论 → 识别质疑类型 + 提取关键实体 → 登记待回应队列。
     v1.2(2026-09-04) respond 接入 5 数字人协同审核门控（设计稿 v1.0）:
       🟢 全过 → 自动发布 | 🟡 1-2 不过 → 标记 needs_human 待人工复核 | 🔴 ≥3 不过 → 耻辱墙联动事件
       v1.1 新增一站式 respond + 每日巡航 check --all:
       lh challenge respond <id> = 全自动闭环(质疑→验证→数字人审核→发布回复·recap自动归档)
       lh challenge check --all  = 扫描全部待回应质疑逐条响应(launchd 每日04:00)
背景: icophy 在 deepseek-ai/DeepSeek-V3#1622 提出「召回率未测 + 假阳性未测」，
     本引擎把「质疑 → 自动解析 → 验证 → 数字人审核 → 回复」制度化，任何社区质疑都走自动闭环。

质疑分类: data_gap(数据缺口) / method(方法问题) / conclusion(结论存疑) / reproducibility(可复现性)
数据: ~/.longhun/validation/issues.jsonl(append-only) + rules/challenge_keywords.json(可配置)
网络: 强制直连(ProxyHandler({}))·token 读取链 env → Keychain(github.com/UID9622) → 匿名
铁律: 用数据回应质疑·不争论。任何 issue/质疑 → 第一反应是跑验证，不是解释。
"""

import argparse
import contextlib
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

# ============================================================
# 一、常量
# ============================================================
VALIDATION_ROOT = Path.home() / ".longhun" / "validation"
RULES_DIR = VALIDATION_ROOT / "rules"
ISSUES_FILE = VALIDATION_ROOT / "issues.jsonl"
DEFAULT_REPO = "deepseek-ai/DeepSeek-V3"
SCRIPT_DIR = Path(__file__).resolve().parent  # 08_BIN 真实目录（respond 编排用）

# 默认关键词表（rules/challenge_keywords.json 可覆盖合并）
DEFAULT_KEYWORDS = {
    "中文": {
        "阈值": 1.0, "基线": 1.0, "误报": 1.0, "误触发": 1.0, "召回": 1.0,
        "假阳性": 1.0, "验证": 0.6, "复现": 1.0, "质疑": 0.8, "挑战": 0.7,
        "数据": 0.3, "样本": 0.6, "命中率": 1.0, "没测": 1.0, "声称": 0.5,
        "操作点": 1.0, "检测器": 0.8, "正样本": 0.9, "负样本": 0.9,
    },
    "英文": {
        "threshold": 1.0, "baseline": 1.0, "false positive": 1.0, "fpr": 1.0,
        "recall": 1.0, "false negative": 1.0, "validate": 0.6, "reproduc": 1.0,
        "benchmark": 0.8, "precision": 0.9, "sample": 0.5, "dataset": 0.4,
        "hit rate": 1.0, "operating point": 1.0,
    },
}

# 分类判定器（关键词 → 分类·用命中得分累加）
CATEGORY_RULES = [
    ("data_gap", ["召回", "假阳性", "没测", "样本", "命中率", "recall", "false positive", "fpr", "precision", "hit rate"]),
    ("method", ["阈值", "基线", "操作点", "应该", "建议", "可以", "threshold", "baseline", "operating point", "method"]),
    ("reproducibility", ["复现", "reproduc", "脚本", "步骤", "指令"]),
    ("conclusion", ["声称", "声明", "结论", "claim", "conclusion", "质疑", "不成立"]),
]

# 实体提取：阈值数值（0.5 / 60% / 0.80 等）
THRESHOLD_PATTERN = re.compile(r"(?<![A-Za-z0-9_])(0?\.\d+|\d{1,2}(?:\.\d+)?%)(?![A-Za-z0-9_%])")
# 检测器/数据集实体
DETECTOR_TERMS = ["judge", "phone-scan", "指纹", "检测器", "耻辱墙", "shame", "数据集", "dataset", "merkle", "根哈希", "审计"]


def _ensure_dirs():
    VALIDATION_ROOT.mkdir(parents=True, exist_ok=True)
    RULES_DIR.mkdir(parents=True, exist_ok=True)
    (VALIDATION_ROOT / "reports").mkdir(parents=True, exist_ok=True)
    if not ISSUES_FILE.exists():
        ISSUES_FILE.write_text("", encoding="utf-8")


def _load_keywords() -> dict:
    """加载关键词规则（默认合并规则文件·文件优先）"""
    kf = RULES_DIR / "challenge_keywords.json"
    if not kf.exists():
        kf.write_text(json.dumps(DEFAULT_KEYWORDS, ensure_ascii=False, indent=2), encoding="utf-8")
        return DEFAULT_KEYWORDS
    try:
        user = json.loads(kf.read_text(encoding="utf-8"))
        merged = {}
        for lang in ("中文", "英文"):
            base = DEFAULT_KEYWORDS.get(lang, {})
            over = user.get(lang, {})
            base.update(over)
            merged[lang] = base
        return merged
    except Exception:
        return DEFAULT_KEYWORDS


# ============================================================
# 二、GitHub 拉取（公开只读·token 可选）
# ============================================================
def _load_token() -> tuple[str | None, str]:
    """token 读取: env → Keychain(github.com/UID9622)。公开只读无 token 也够用。"""
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


def _gh_get(path: str) -> dict | None:
    """GET GitHub API（强制直连·清系统代理）。公开 issue 评论可匿名。"""
    url = "https://api.github.com" + path
    token, _ = _load_token()
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                                "User-Agent": "longhun-challenge-parser/1.1"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 不认系统代理
    try:
        with opener.open(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"  🔴 GitHub 拉取失败({path}): {e}")
        return None


def 拉取评论(issue_id: str, repo: str = DEFAULT_REPO) -> list[dict]:  # noqa: N802 中文函数名·龍魂命名风格
    """拉取 issue 全部评论（升序·取最新的若干条）"""
    data = _gh_get(f"/repos/{repo}/issues/{issue_id}/comments?per_page=100")
    if not isinstance(data, list):
        return []
    return data


# ============================================================
# 三、质疑解析核心
# ============================================================
def _text_score(text: str, keywords: dict) -> dict[str, float]:
    """关键词打分: {词: 出现次数·归一} → 总命中词列表"""
    low = text.lower()
    hits: dict[str, float] = {}
    for _lang, table in keywords.items():
        for word, w in table.items():
            if word.lower() in low:
                hits[word] = hits.get(word, 0) + w
    return hits


def _classify(text: str, keywords_hit: dict[str, float]) -> list[str]:
    """按分类规则计分·返回(分类, 得分)降序"""
    low = text.lower()
    scores: dict[str, float] = {}
    for cat, words in CATEGORY_RULES:
        s = 0.0
        for w in words:
            if w.lower() in low:
                s += keywords_hit.get(w, 0) or 1.0
        scores[cat] = s
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    cats = [c for c, s in ranked if s > 0]
    return cats if cats else ["conclusion"]


def _extract_entities(text: str) -> dict:
    """提取: 阈值数值 / 检测器 / 数据集 / 方法词"""
    return {
        "阈值数值": sorted({m.group(1) for m in THRESHOLD_PATTERN.finditer(text)}),
        "涉及模块": sorted({t for t in DETECTOR_TERMS if t.lower() in text.lower()}),
    }


def _关键句(text: str, max_n: int = 3) -> list[str]:  # noqa: N802 中文函数名·龍魂命名风格
    """抽取含质疑信号的句子"""
    lines = [ln.strip() for ln in re.split(r"[。！？\n.!?]", text) if len(ln.strip()) >= 8]
    out = []
    for line in lines:
        if any(k in line.lower() for k in ("阈值", "基线", "误报", "召回", "假阳性", "验证", "复现", "质疑",
                                            "threshold", "baseline", "recall", "false positive", "validate", "reproduc")):
            out.append(line[:160])
        if len(out) >= max_n:
            break
    return out


def 解析文本(text: str) -> dict:  # noqa: N802 中文函数名·龍魂命名风格
    """单条评论文本 → 解析结果"""
    kw = _load_keywords()
    hit = _text_score(text, kw)
    cats = _classify(text, hit)
    ents = _extract_entities(text)
    return {
        "命中关键词": sorted(hit.keys(), key=lambda k: -hit[k]),
        "分类": cats,
        "实体": ents,
        "关键句": _关键句(text),
        "质疑强度": round(sum(hit.values()), 2),
    }


def _append_issue(rec: dict):
    ISSUES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ISSUES_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _read_issues() -> list[dict]:
    if not ISSUES_FILE.exists():
        return []
    out = []
    for line in ISSUES_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        with contextlib.suppress(Exception):
            out.append(json.loads(line))
    return out


def _user_latest_issue(issue_id: str) -> dict | None:
    """取某 issue 最新一条记录（覆盖式更新用）"""
    issues = _read_issues()
    for rec in reversed(issues):
        if str(rec.get("issue_id")) == str(issue_id):
            return rec
    return None


def cmd_parse(issue_id: str, repo: str = DEFAULT_REPO):
    """拉取 issue 最新评论 → 解析 → 登记队列（同 issue 覆盖式更新）"""
    _ensure_dirs()
    print(f"  🎯 拉取 {repo}#{issue_id} 评论…")
    comments = 拉取评论(issue_id, repo)
    if not comments:
        print("  🔴 未拉到评论（网络/仓库不可达？可本地补录: lh challenge add <文本>）")
        return 1

    # 聚合全部评论·找质疑信号最强的
    best, best_score = None, 0.0
    authors = set()
    for c in comments[-20:]:
        body = c.get("body", "")
        author = (c.get("user") or {}).get("login", "unknown")
        authors.add(author)
        if not body:
            continue
        parsed = 解析文本(body)
        if parsed["质疑强度"] > best_score:
            best = {"author": author, "created": c.get("created_at", ""),
                    "url": c.get("html_url", ""), "text": body, **parsed}
            best_score = parsed["质疑强度"]

    prev = _user_latest_issue(issue_id)
    rec = {
        "issue_id": str(issue_id),
        "repo": repo,
        "recorded_at": datetime.now(UTC).isoformat(),
        "comment_authors": sorted(authors),
        "质疑者": best["author"] if best else "unknown",
        "质疑时间": best["created"] if best else "",
        "comment_url": best["url"] if best else "",
        "分类": best["分类"] if best else [],
        "实体": best["实体"] if best else {},
        "命中关键词": best["命中关键词"] if best else [],
        "关键句": best["关键句"] if best else [],
        "原文": best["text"][:3000] if best else "",
        "状态": "pending",
        "状态版本": (prev.get("状态版本", 0) + 1) if prev else 1,
    }
    _append_issue(rec)
    print(f"  ✅ 登记质疑: {rec['repo']}#{rec['issue_id']} · 质疑者 {rec['质疑者']} · 分类 {rec['分类']}")
    print(f"     命中关键词: {rec['命中关键词'][:8]}")
    if rec["实体"].get("阈值数值"):
        print(f"     阈值数值: {rec['实体']['阈值数值']}")
    if rec["关键句"]:
        print(f"     关键句: {rec['关键句'][0]}")
    return 0


def cmd_add(文本: str, issue_id: str = "local"):  # noqa: N803 中文参数名·与 argparse dest 一致
    """本地补录质疑（无网/手工粘贴场景）"""
    _ensure_dirs()
    parsed = 解析文本(文本)
    rec = {
        "issue_id": str(issue_id),
        "repo": "local",
        "recorded_at": datetime.now(UTC).isoformat(),
        "comment_authors": [],
        "质疑者": "community",
        "质疑时间": "",
        "comment_url": "",
        "分类": parsed["分类"],
        "实体": parsed["实体"],
        "命中关键词": parsed["命中关键词"],
        "关键句": parsed["关键句"],
        "原文": 文本[:3000],
        "状态": "pending",
        "状态版本": 1,
    }
    _append_issue(rec)
    print(f"  ✅ 本地登记质疑: {issue_id} · 分类 {rec['分类']} · 强度 {parsed['质疑强度']}")
    return 0


def cmd_list(as_json: bool = False):
    """列出全部待回应/处理中质疑"""
    issues = _read_issues()
    pending = [r for r in issues if r.get("状态") in ("pending", "validating")]
    if as_json:
        print(json.dumps(pending, ensure_ascii=False, indent=2))
        return 0
    if not issues:
        print("  🟢 无质疑记录")
        return 0
    print(f"  🎯 社区质疑队列（总 {len(issues)} · 待回应 {len(pending)}）:")
    for r in reversed(issues[-20:]):
        mark = {"pending": "⏳", "validating": "🧪", "responded": "✅", "dismissed": "⏭️",
                "needs_human": "📋"}.get(str(r.get("状态") or ""), "?")
        print(f"   {mark} [{r.get('repo')}#{r.get('issue_id')}] {r.get('质疑者')} · "
              f"{'/'.join(r.get('分类', []))} · v{r.get('状态版本', 1)}")
    return 0


def cmd_status(issue_id: str):
    """查看某 issue 质疑响应状态"""
    rec = _user_latest_issue(issue_id)
    if not rec:
        print(f"  🔴 未找到 {issue_id} 的质疑记录（先 lh challenge parse {issue_id}）")
        return 1
    print(f"  🎯 Issue {issue_id} 质疑状态: {rec['状态']} · v{rec.get('状态版本', 1)}")
    print(f"     质疑者: {rec['质疑者']} · 分类: {'/'.join(rec.get('分类', []))}")
    print(f"     实体: {json.dumps(rec.get('实体', {}), ensure_ascii=False)}")
    if rec.get("关键句"):
        print(f"     关键句: {rec['关键句'][0]}")
    return 0


# ============================================================
# 四、一站式 respond + 每日巡航 check（v1.1）
# ============================================================
def _run_lh(args_list: list[str]) -> int:
    """子进程调用 lh.py 子命令（strategy run / response post）·触发 recap 钩子自动归档。
    清代理强制直连；返回退出码。"""
    lh_py = SCRIPT_DIR / "lh.py"
    env = dict(os.environ)
    for k in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "ALL_PROXY"):
        env.pop(k, None)
    p = subprocess.run([sys.executable, str(lh_py)] + args_list, env=env,
                       capture_output=True, text=True, timeout=300)
    out = (p.stdout or "") + (p.stderr or "")
    sys.stdout.write(out)
    return p.returncode


def _patch_issue_state(issue_id: str, state: str):
    """就地前向修订 issue 记录状态（记录行本体保留·只改状态字段）"""
    fp = VALIDATION_ROOT / "issues.jsonl"
    if not fp.exists():
        return
    lines = fp.read_text(encoding="utf-8").splitlines()
    for i in range(len(lines) - 1, -1, -1):
        try:
            rec = json.loads(lines[i])
        except Exception:
            continue
        if str(rec.get("issue_id")) == str(issue_id) and rec.get("状态") in ("pending", "validating", "needs_human"):
            rec["状态"] = state
            lines[i] = json.dumps(rec, ensure_ascii=False)
            break
    fp.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def cmd_respond(issue_id: str, repo: str = DEFAULT_REPO, force: bool = False,
                skip_review: bool = False) -> int:
    """一站式自动响应（v1.2·数字人审核门控）:
    ①质疑记录就位 → ②验证(strategy run) → ②½ 5数字人协同审核(三色门控) → ③发布回复(post)
    🟢全过→自动发布 / 🟡1-2不过→needs_human待人工复核 / 🔴≥3不过→耻辱墙联动·等待人工
    发布走 lh.py 子命令 → recap 钩子自动归档 ~/.longhun/recap/ · 全程零人工。"""
    _ensure_dirs()
    rec = _user_latest_issue(issue_id)
    if rec and rec.get("状态") == "responded" and not force:
        print(f"  ⏭️ Issue {issue_id} 已回应过 {rec.get('回应URL', '')} · 强制重发加 --force")
        return 0
    # ① 质疑记录就位（无则 API 拉取·失败提示手工补录·不造假原文）
    if not rec or not rec.get("原文"):
        print(f"  🎯 步骤1/4 · 无本地质疑记录 → 尝试 API 拉取 {repo}#{issue_id}…")
        rc = cmd_parse(issue_id, repo)
        if rc != 0:
            print(f"  🔴 步骤1/4 失败 · 无法获取质疑原文（网络/仓库受限）· 请手工: lh challenge add \"<质疑原文>\" --issue {issue_id}")
            return 1
        rec = _user_latest_issue(issue_id)
    print(f"  🎯 步骤1/4 ✅ 质疑记录就位: {(rec or {}).get('质疑者')} · {'/'.join((rec or {}).get('分类', []))}")
    # ② 验证（策略引擎·复用 lh_judge 指纹检测·报告 latest.md）
    print("\n  🧪 步骤2/4 · 执行正负样本验证…")
    if _run_lh(["strategy", "run", issue_id]) != 0:
        print("  🔴 步骤2/4 失败 · 验证引擎异常（lh strategy run <id> 单跑排查）")
        return 1
    # ②½ 数字人协同审核把关（设计稿 v1.0·任务2/3/4: 🟢过→发布 / 🟡复核 / 🔴耻辱墙）
    if not skip_review:
        print("\n  🧑⚖️ 步骤2.5/4 · 5 数字人协同审核…")
        if _run_lh(["review", "evaluate", issue_id]) != 0:
            print("  🟡 步骤2.5/4 审核引擎异常 · 人工核查后 lh review evaluate <id> 单跑")
            return 1
        hist = []
        fp = Path.home() / ".longhun" / "review" / "reviews" / f"{issue_id}.json"
        if fp.exists():
            try:
                hist = json.loads(fp.read_text(encoding="utf-8"))
            except Exception:
                hist = []
        agg = hist[-1] if hist else {}
        色, conf = agg.get("三色", "🟡"), agg.get("置信度", 0)  # noqa: N806 三色中文变量·三色语义一致
        if 色 == "🟡":
            _patch_issue_state(issue_id, "needs_human")
            print(f"  🟡 数字人审核 1-2 位不通过（置信度 {conf}）→ 标记待人工复核 · 不自动发布")
            print(f"     复核后重跑: lh challenge respond {issue_id}（数据修复后自动变🟢再发布）")
            return 2
        if 色 == "🔴":
            _patch_issue_state(issue_id, "needs_human")
            print(f"  🔴 多数审核不通过（置信度 {conf}）→ 已记录耻辱墙联动事件 · 等待人工介入")
            print(f"     介入修复后重跑: lh challenge respond {issue_id}")
            return 3
        print(f"  ✅ 数字人审核全过（置信度 {conf}）→ 门控放行·进入发布")
    else:
        print("\n  ⏭️ 已跳过数字人审核（--skip-review）· 直接发布")
    # ③ 发布回复（response builder·内部标记 responded）
    # 注意: 不走 --repo —— lh.py 顶层已占用 --repo(模板生成器)，发布统一默认 deepseek-ai/DeepSeek-V3；
    #      自定义仓库请引擎直跑: python3 08_BIN/lh_response_builder.py post <id> --repo <owner/repo>
    print(f"\n  📮 步骤3/4 · 发布回复到 {DEFAULT_REPO}#{issue_id}…")
    if _run_lh(["response", "post", issue_id]) != 0:
        print(f"  🟡 步骤3/4 未完成 · 草稿已保留（lh response build {issue_id} 预览 · lh response post {issue_id} 重试）")
        return 1
    # ④ 汇总（报告/事件墙位置）
    print(f"\n  ✅ 步骤4/4 响应闭环完成 · Issue #{issue_id}")
    print(f"     回复: https://github.com/{repo}/issues/{issue_id}#issuecomment-*")
    print(f"     报告: ~/.longhun/validation/reports/issue_{issue_id}/latest.md")
    print(f"     审核: ~/.longhun/review/reviews/{issue_id}.json · 看板: ~/.longhun/review/dashboard.md")
    print("     事件: ~/.longhun/validation/events.jsonl（append-only）· 复盘: ~/.longhun/recap/（钩子已归档）")
    return 0


def cmd_check(dry_run: bool = False) -> int:
    """每日巡航: 扫描全部待回应质疑(pending/validating) → 逐条完整响应。
    无新质疑 → 留一行『无质疑』日志。launchd com.longhun.challenge-watch 每日04:00。"""
    _ensure_dirs()
    issues = _read_issues()
    targets: dict[str, str] = {}
    for r in issues:
        if r.get("状态") in ("pending", "validating") and str(r.get("issue_id")):
            repo = str(r.get("repo")) or DEFAULT_REPO
            targets[str(r["issue_id"])] = repo if repo != "local" else DEFAULT_REPO
    if not targets:
        print("  🟢 无质疑")
        return 0
    print(f"  🎯 发现 {len(targets)} 个待回应质疑: {sorted(targets)}")
    ok = 0
    for iid in sorted(targets):
        repo = targets[iid]
        if dry_run:
            print(f"     [dry-run] 将自动响应 {repo}#{iid}")
            continue
        rc = cmd_respond(iid, repo)
        ok += 1 if rc == 0 else 0
        print(f"     — {iid} {'✅' if rc == 0 else '❌'} —")
    if not dry_run:
        print(f"\n  📮 巡航完成: {ok}/{len(targets)} 成功")
    return 0


def main():
    parser = argparse.ArgumentParser(description='龍魂·社区质疑解析引擎')
    sub = parser.add_subparsers(dest='command', help='子命令')

    p_parse = sub.add_parser('parse', help='拉取 issue 评论并解析质疑')
    p_parse.add_argument('issue_id', help='Issue 编号（默认仓库 deepseek-ai/DeepSeek-V3）')
    p_parse.add_argument('--repo', default=DEFAULT_REPO, help='仓库 owner/repo')

    p_add = sub.add_parser('add', help='本地补录质疑文本')
    p_add.add_argument('文本', help='质疑内容')
    p_add.add_argument('--issue', default='local', help='Issue 编号')

    p_list = sub.add_parser('list', help='列出待回应质疑')
    p_list.add_argument('--json', action='store_true')

    p_status = sub.add_parser('status', help='查看质疑响应状态')
    p_status.add_argument('issue_id', help='Issue 编号')

    p_resp = sub.add_parser('respond', help='一站式自动响应(质疑→验证→5数字人审核→发布·默认deepseek-ai/DeepSeek-V3)')
    p_resp.add_argument('issue_id', help='Issue 编号')
    p_resp.add_argument('--force', action='store_true', help='已回应过也强制重发')
    p_resp.add_argument('--skip-review', action='store_true', help='跳过数字人审核直接发布(慎用)')

    p_check = sub.add_parser('check', help='每日巡航: 扫描全部待回应质疑并自动响应')
    p_check.add_argument('--all', action='store_true', help='扫描全部(默认行为·兼容显式)')
    p_check.add_argument('--dry-run', action='store_true', help='只预览不执行')

    args = parser.parse_args()
    if args.command == 'parse':
        return cmd_parse(args.issue_id, args.repo)
    if args.command == 'add':
        return cmd_add(args.文本, args.issue)
    if args.command == 'list':
        return cmd_list(getattr(args, 'json', False))
    if args.command == 'status':
        return cmd_status(args.issue_id)
    if args.command == 'respond':
        return cmd_respond(args.issue_id, DEFAULT_REPO, args.force, getattr(args, 'skip_review', False))
    if args.command == 'check':
        return cmd_check(getattr(args, 'dry_run', False))
    parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
