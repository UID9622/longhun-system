#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·申时·䷔噬嗑-BRAIN-REPORT-ENGINE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 龙魂·思维汇报引擎 v1.0
# 抓取/接收系统状态 -> 本地 AI（思维链）生成带推理的汇报 -> Bark 推送 + 落盘报告。
# 用法:
#   lh_brain_report.py                  # 自动抓状态 -> AI 思维 -> 推 Bark -> 落盘
#   lh_brain_report.py --context "文本" # 用给定上下文（不自动抓取）
#   lh_brain_report.py --no-push        # 只落盘不推送
#   lh_brain_report.py --model <name>   # 指定 ollama 模型（默认 R1 思维链优先）
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.request

OLLAMA = "http://localhost:11434"
# 思维优先：deepseek-r1 原生带推理；降级龙魂自家 / qwen
DEFAULT_MODELS = ["deepseek-r1:7b", "longhun-v43-v3:latest", "qwen2.5:7b"]
REPORT_DIR = os.path.expanduser("~/longhun-system/reports/brain")
KEYCHAIN_SERVICE = "longhun-vault"


def _now():
    return datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def _get_bark_key():
    r = subprocess.run(
        ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-a", "BARK_KEY", "-w"],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("BARK_KEY 不可用（Keychain 未解锁或未入库）")
    return r.stdout.strip()


def _snapshot():
    """轻量状态快照：不碰敏感数据，只抓表象指标"""
    lines = []
    try:
        n = subprocess.run(["launchctl", "list"], capture_output=True, text=True).stdout.count("\n")
        lines.append(f"本机 launchd 服务条目: {n}")
    except Exception:
        pass
    try:
        up = subprocess.run(["uptime"], capture_output=True, text=True).stdout.strip()
        lines.append(f"系统负载: {up}")
    except Exception:
        pass
    try:
        df = subprocess.run(["df", "-h", "/"], capture_output=True, text=True).stdout.splitlines()[-1]
        cols = df.split()
        lines.append(f"根磁盘: 总{cols[1]} 已用{cols[2]} 可用{cols[3]} 使用率{cols[4]}")
    except Exception:
        pass
    try:
        mem = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout.strip()
        total = int(mem)
        vm = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
        ps = 0
        for line in vm.splitlines():
            if "page size" in line:
                ps = int(re.search(r"(\d+)", line).group(1))
                break
        if ps:
            def _page(name):
                m = re.search(rf"{name}:\s+(\d+)", vm)
                return int(m.group(1)) * ps if m else 0
            free = _page("Pages free")
            inactive = _page("Pages inactive")
            avail = free + inactive
            lines.append(
                f"内存: 总 {total//1024//1024//1024}GB 可用 {avail//1024//1024//1024}GB"
                f"（{round(avail / total * 100)}%）")
    except Exception:
        pass
    return "\n".join(lines) if lines else "（状态快照不可用）"


_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 禁代理：Bark 拒 socks 隧道


def _gen(prompt, models):
    """调 ollama 生成：逐模型降级，只返回正文"""
    for m in models:
        try:
            req = urllib.request.Request(
                f"{OLLAMA}/api/generate",
                data=json.dumps({
                    "model": m, "prompt": prompt, "stream": False,
                    "options": {"temperature": 0.4, "num_predict": 600},
                }).encode("utf-8"),
                headers={"Content-Type": "application/json"})
            with _OPENER.open(req, timeout=120) as r:
                body = json.loads(r.read().decode("utf-8", "ignore"))
            txt = body.get("response", "").strip()
            if txt:
                return txt, m
        except Exception:
            continue
    return "", ""


def _normalize(report):
    """分级标记归一：AI 可能输出 🟥/🟨 等变体"""
    return (report.replace("🟥", "🔴").replace("🟨", "🟡")
            .replace("🟩", "🟢").replace("🟠", "🟡"))


def _facts():
    """Reflexion 层：结构化关键事实，供自校验核对（独立抓取，与快照解耦）"""
    facts = {}
    try:
        df = subprocess.run(["df", "-h", "/"], capture_output=True, text=True).stdout.splitlines()[-1].split()
        # 列: Filesystem Size Used Avail Capacity% MountedOn
        facts["disk_used_pct"] = int(df[4].rstrip("%"))
        facts["disk_avail"] = df[3]
    except Exception:
        pass
    try:
        up = subprocess.run(["uptime"], capture_output=True, text=True).stdout
        m = re.search(r"load averag\w*:?\s+([\d.]+)", up)
        if m:
            facts["load1"] = float(m.group(1))
    except Exception:
        pass
    try:
        n = subprocess.run(["launchctl", "list"], capture_output=True, text=True).stdout.count("\n")
        facts["launchd"] = n
    except Exception:
        pass
    try:
        total = int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout.strip())
        vm = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
        ps = 0
        for line in vm.splitlines():
            if "page size" in line:
                ps = int(re.search(r"(\d+)", line).group(1))
                break
        if ps:
            def _page(name):
                m = re.search(rf"{name}:\s+(\d+)", vm)
                return int(m.group(1)) * ps if m else 0
            free = _page("Pages free")
            inactive = _page("Pages inactive")
            avail = free + inactive
            facts["mem_total_gb"] = round(total / 1024 ** 3, 1)
            facts["mem_avail_gb"] = round(avail / 1024 ** 3, 1)
            facts["mem_avail_pct"] = round(avail / total * 100)
    except Exception:
        pass
    return facts


def _verify(report, facts):
    """Reflexion 式自校验：AI 结论 vs 实测定值，冲突则产出纠偏项"""
    issues = []
    if "disk_used_pct" in facts:
        pct = facts["disk_used_pct"]
        # 语义纠偏：使用率低却被判紧张 / 使用率高却被判很空
        if pct <= 30:
            for kw in ("耗尽", "用尽", "不足", "紧张", "告急", "快满", "很快耗尽", "将耗尽"):
                if kw in report:
                    issues.append(
                        f"根磁盘使用率实测 {pct}%（可用 {facts.get('disk_avail','?')}），AI 称「{kw}」为误读，实况为很空")
                    break
        elif pct >= 85:
            for kw in ("很空", "充足", "充裕", "很充裕", "够用"):
                if kw in report:
                    issues.append(
                        f"根磁盘使用率实测 {pct}%（可用 {facts.get('disk_avail','?')}），AI 称「{kw}」为误读，实况为紧张")
                    break
        # 数值纠偏：报告出现与实测不一致的百分数
        for num in re.findall(r"(\d{1,3})\s*%", report):
            if abs(int(num) - pct) >= 5:
                issues.append(f"磁盘使用率实测 {pct}%，AI 报告写成 {num}%，以实测定值为准")
                break
    if "load1" in facts:
        for num in re.findall(r"负载[^0-9]{0,4}(\d+(?:\.\d+)?)", report):
            try:
                if abs(float(num) - facts["load1"]) > 0.5:
                    issues.append(f"系统负载实测 {facts['load1']}，AI 报告写成 {num}")
                    break
            except ValueError:
                pass
    if "mem_avail_pct" in facts:
        mp = facts["mem_avail_pct"]
        mg = facts.get("mem_avail_gb", "?")
        if mp <= 10:
            for kw in ("充足", "充裕", "很空", "够用", "很宽裕"):
                if kw in report:
                    issues.append(f"内存可用实测仅 {mp}%（约{mg}GB），AI 称「{kw}」为误读，实况为紧张")
                    break
        elif mp >= 30:
            for kw in ("内存已满", "内存耗尽", "内存不足", "内存用尽", "内存快满", "内存告急", "内存几乎满", "内存满了"):
                if kw in report:
                    issues.append(f"内存可用实测 {mp}%（约{mg}GB），AI 称「{kw}」为误读，实况为充足")
                    break
        # 数值纠偏：报告出现明显高于总内存的占用数字
        for num in re.findall(r"内存[^0-9]{0,6}(\d+(?:\.\d+)?)", report):
            try:
                if float(num) > facts.get("mem_total_gb", 999):
                    issues.append(f"内存总量实测 {facts['mem_total_gb']}GB，AI 写 {num}GB 超出物理上限")
                    break
            except ValueError:
                pass
    return issues


def _push_bark(key, title, body, group="brain-report"):
    req = urllib.request.Request(
        f"https://api.day.app/{key}",
        data=json.dumps({"title": title, "body": body, "group": group}).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    with _OPENER.open(req, timeout=10) as r:
        return r.read().decode("utf-8", "ignore")


def main():
    ap = argparse.ArgumentParser(description="龍魂·思维汇报引擎 v1.0")
    ap.add_argument("--context", default="", help="外部提供的上下文（不自动抓取）")
    ap.add_argument("--model", default="", help="指定 ollama 模型")
    ap.add_argument("--no-push", action="store_true", help="只落盘不推送")
    ap.add_argument("--topic", default="系统状态", help="汇报主题")
    args = ap.parse_args()

    ctx = args.context.strip() or _snapshot()

    models = [args.model] if args.model else DEFAULT_MODELS
    prompt = (
        "你是龙魂系统值班 AI（归属：诸葛鑫 | UID9622 · 龙芯北辰）。\n"
        "基于以下系统状态，产出一份【有思维的汇报】。要求：\n"
        "1. 结论先行：1 行，带 🟢/🟡/🔴 分级标记。\n"
        "2. 观察到什么：1-2 行事实。\n"
        "3. 你的判断：1-2 行，说明为什么（推理链）。\n"
        "4. 建议动作：1-2 行，具体可执行。\n"
        "5. 总字数 ≤ 140 字，中文，直接给汇报正文，不要输出思考过程。\n"
        f"汇报主题：{args.topic}\n"
        f"状态快照：\n{ctx}\n"
    )

    report, model = _gen(prompt, models)
    report = _normalize(report)
    ts = _now()
    if not report:
        report = f"🟡 汇报生成失败（本地模型不可用）：\n{ctx}\n（请检查 ollama 或提供 --context）"
        model = "N/A"
    else:
        # Reflexion 自校验：AI 结论 vs 实测定值，冲突则附加纠偏
        try:
            issues = _verify(report, _facts())
            if issues:
                correction = "⚠️ 值班纠偏：" + "；".join(issues)
                report = f"{report}\n{correction}"
        except Exception:
            pass

    # 落盘
    os.makedirs(REPORT_DIR, exist_ok=True)
    day = datetime.date.today().isoformat()
    fname = os.path.join(REPORT_DIR, f"{day}.md")
    entry = f"\n## {ts} · {args.topic} · 模型:{model}\n\n{report}\n"
    with open(fname, "a", encoding="utf-8") as f:
        f.write(entry)

    # 推送
    pushed = ""
    if not args.no_push:
        try:
            key = _get_bark_key()
            body = report[:500]
            pushed = _push_bark(key, f"🐉龙魂思维汇报·{args.topic}", body, group="brain-report")
        except Exception as e:
            pushed = f"PUSH_FAIL: {e}"

    print(f"[{ts}] 模型={model}")
    print("── 思维汇报 ──")
    print(report)
    print(f"── 落盘: {fname}")
    print(f"── 推送: {pushed or '已跳过'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
