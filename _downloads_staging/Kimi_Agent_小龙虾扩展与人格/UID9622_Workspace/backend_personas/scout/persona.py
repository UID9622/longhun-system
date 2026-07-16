#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
侦察兵·信息猎手 P-AK-SCOUT
功能：GitHub Trending / RSS 扫描 / 关键词告警 / 信息分级 / 来源可信度评估
DNA: #SCOUT-AGENT-CONFIG-20251214-001
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import AuditMark, DNATracer, TelemetryCollector, load_config, setup_logging, workspace_root


PERSONA_CODE = "SCOUT"
PERSONA_NAME = "侦察兵·信息猎手 P-AK-SCOUT"
AGENT_DNA = "#SCOUT-AGENT-CONFIG-20251214-001"

CONFIG = load_config()
WORKSPACE = Path(CONFIG.get("workspace", workspace_root()))
LOG_FILE = Path(CONFIG.get("logs_dir", WORKSPACE / "logs")) / "scout.log"
DEFAULT_OUTPUT = WORKSPACE / "data" / "scout"
DEFAULT_SOURCES = Path(__file__).parent / "sources.json"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

SEVERITY = {
    "critical": {"label": "紧急", "score": 10, "keywords": ["CVE", "漏洞", "critical", "紧急", "0day", "RCE", "exploit", "严重"]},
    "high": {"label": "重要", "score": 7, "keywords": ["release", "发布", "重大更新", "breaking change", "安全更新", "新版本"]},
    "normal": {"label": "一般", "score": 4, "keywords": []},
}

HIGH_TRUST = {
    "github.com", "apache.org", "mozilla.org", "googleblog.com", "cloud.google.com",
    "aws.amazon.com", "azure.microsoft.com", "kubernetes.io", "docker.com", "npmjs.com",
    "pypi.org", "rust-lang.org", "python.org", "openjdk.org", "kernel.org",
    "cve.mitre.org", "nvd.nist.gov", "arxiv.org",
}


def classify(title: str, content: str = "") -> Dict:
    combined = f"{title} {content}".lower()
    for level, cfg in SEVERITY.items():
        if any(kw.lower() in combined for kw in cfg["keywords"]):
            return {"level": level, **cfg}
    return {"level": "normal", **SEVERITY["normal"]}


def credibility(url: str, source_type: str = "") -> Dict:
    domain = urlparse(url).netloc.lower().lstrip("www.")
    if domain in HIGH_TRUST or source_type in ("official", "api"):
        return {"level": "high", "score": 0.9, "label": "高", "desc": "官方源/权威社区"}
    if source_type in ("rss", "community") or re.search(r"medium\.com|dev\.to|news\.ycombinator\.com|reddit\.com/r/", url, re.I):
        return {"level": "medium", "score": 0.6, "label": "中", "desc": "社区驱动/第三方聚合"}
    return {"level": "low", "score": 0.3, "label": "低", "desc": "未验证/匿名来源"}


def fetch(url: str, timeout: int = 30, retries: int = 2) -> Optional[str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if attempt == retries:
                return None
            time.sleep(2 ** attempt)
        except Exception:
            if attempt == retries:
                return None
            time.sleep(2 ** attempt)
    return None


def scan_github_trending(dna: DNATracer) -> List[Dict]:
    html = fetch("https://github.com/trending")
    if not html:
        return []
    results = []
    seen = set()
    repo_re = re.compile(r'<h2[^>]*>\s*<a[^>]*href="(/[^/]+/[^"]+)"[^>]*>\s*([^<]+)', re.S)
    desc_re = re.compile(r'<p\s+class="col-9[^"]*"[^>]*>(.*?)</p>', re.S)
    for m in repo_re.finditer(html):
        href = m.group(1).strip()
        name = href.lstrip("/")
        if name in seen or "?" in name:
            continue
        seen.add(name)
        pos = m.end()
        desc_match = desc_re.search(html[pos : pos + 2000])
        desc = re.sub(r"<[^>]+>", "", desc_match.group(1)).strip() if desc_match else ""
        url = f"https://github.com{name}"
        item = dna.stamp(
            {
                "title": name,
                "description": desc,
                "url": url,
                "source": "GitHub Trending",
                "source_type": "official",
                "severity": classify(name, desc),
                "credibility": credibility(url, "official"),
                "tags": ["github", "trending"],
            },
            "GH",
        )
        results.append(item)
    return results


def scan_rss_feed(name: str, url: str, dna: DNATracer) -> List[Dict]:
    xml = fetch(url, timeout=20)
    if not xml:
        return []
    results = []
    try:
        root = ET.fromstring(xml)
    except Exception:
        return results
    # handle rss/channel/item or feed/entry
    items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
    for item in items[:10]:
        title = ""
        link = ""
        desc = ""
        for child in item:
            tag = child.tag.split("}")[-1]
            if tag == "title":
                title = child.text or ""
            elif tag == "link":
                link = child.text or child.get("href", "")
            elif tag in ("description", "summary"):
                desc = child.text or ""
        if not title:
            continue
        item = dna.stamp(
            {
                "title": title.strip(),
                "description": re.sub(r"<[^>]+>", "", desc).strip(),
                "url": link.strip(),
                "source": name,
                "source_type": "rss",
                "severity": classify(title, desc),
                "credibility": credibility(link, "rss"),
                "tags": ["rss"],
            },
            "RSS",
        )
        results.append(item)
    return results


def keyword_alerts(items: List[Dict], keywords: List[str], dna: DNATracer) -> List[Dict]:
    alerts = []
    if not keywords:
        return alerts
    for item in items:
        text = f"{item.get('title', '')} {item.get('description', '')}".lower()
        hits = [kw for kw in keywords if kw.lower() in text]
        if hits:
            alert = dna.stamp(
                {
                    "matched_keywords": hits,
                    "referenced_item": item.get("dna_trace"),
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "severity": classify(item.get("title", ""), item.get("description", "")),
                },
                "KWD",
            )
            alerts.append(alert)
    return alerts


def save_outputs(items: List[Dict], alerts: List[Dict], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc)
    base = output_dir / f"{today.year}" / f"{today.month:02d}" / f"{today.day:02d}"
    base.mkdir(parents=True, exist_ok=True)

    github = [i for i in items if i.get("source") == "GitHub Trending"]
    rss = [i for i in items if i.get("source_type") == "rss"]

    (base / "github_trending.json").write_text(json.dumps(github, ensure_ascii=False, indent=2), encoding="utf-8")
    (base / "rss_feeds.json").write_text(json.dumps(rss, ensure_ascii=False, indent=2), encoding="utf-8")
    (base / "all_sources.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    (base / "keyword_alerts.json").write_text(json.dumps(alerts, ensure_ascii=False, indent=2), encoding="utf-8")

    report = [
        f"侦察兵巡逻报告 {datetime.now(timezone.utc).isoformat()}",
        f"采集总数: {len(items)}  告警数: {len(alerts)}",
    ]
    for i in items[:20]:
        sev = i.get("severity", {})
        cred = i.get("credibility", {})
        report.append(
            f"- [{sev.get('label','?')}/{cred.get('label','?')}] {i.get('title')} ({i.get('source')}) {i.get('url')}"
        )
    (base / f"report_{datetime.now(timezone.utc).strftime('%H%M%S')}.txt").write_text(
        "\n".join(report), encoding="utf-8"
    )
    return base


def load_sources(path: Path) -> Dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"rss_feeds": [], "keyword_default_groups": {}}


def main():
    parser = argparse.ArgumentParser(description=PERSONA_NAME)
    parser.add_argument("-o", "--output-dir", default=str(DEFAULT_OUTPUT), help="输出目录")
    parser.add_argument("-k", "--keywords", default="", help="关键词，逗号分隔")
    parser.add_argument("--config", default=str(DEFAULT_SOURCES), help="数据源配置")
    parser.add_argument("--daemon", action="store_true", help="守护模式")
    parser.add_argument("--interval", type=int, default=3600, help="守护间隔（秒）")
    parser.add_argument("--compare", action="store_true", help="多平台对比模式（占位）")
    parser.add_argument("--verbose", action="store_true", help="详细日志")
    args = parser.parse_args()

    logger = setup_logging("scout", LOG_FILE, verbose=args.verbose)
    dna = DNATracer(PERSONA_CODE, AGENT_DNA)
    telemetry = TelemetryCollector(PERSONA_CODE, PERSONA_NAME, operation_type="PATROL")
    logger.info(AuditMark.tag(AuditMark.PURPLE, PERSONA_NAME, "开始巡逻"))

    try:
        sources = load_sources(Path(args.config))
        output_dir = Path(args.output_dir).expanduser().resolve()
        keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
        if not keywords:
            keywords = [kw for group in sources.get("keyword_default_groups", {}).values() for kw in group]

        total_items = 0
        total_alerts = 0
        while True:
            items = []
            items.extend(scan_github_trending(dna))
            for feed in sources.get("rss_feeds", []):
                if not feed.get("enabled"):
                    continue
                items.extend(scan_rss_feed(feed["name"], feed["url"], dna))

            alerts = keyword_alerts(items, keywords, dna)
            base = save_outputs(items, alerts, output_dir)
            logger.info(AuditMark.tag(AuditMark.GREEN, PERSONA_NAME, f"巡逻完成: {len(items)} 条，告警 {len(alerts)} 条 -> {base}"))
            total_items += len(items)
            total_alerts += len(alerts)
            telemetry.event("PATROL_LOOP", {"items": len(items), "alerts": len(alerts)})

            if not args.daemon:
                break
            logger.info(AuditMark.tag(AuditMark.BLUE, PERSONA_NAME, f"{args.interval}秒后再次巡逻"))
            time.sleep(args.interval)

        telemetry.set_metrics({"items": total_items, "alerts": total_alerts})
    except Exception as e:
        logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, f"巡逻失败: {e}"))
        telemetry.finish("error", {"error": str(e)})
        raise
    finally:
        if not telemetry._finished:
            telemetry.finish("success")


if __name__ == "__main__":
    main()
