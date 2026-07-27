#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 网页内容提取器 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PAGE-EXTRACTOR-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

核心理念：
  你访问的每个网页，都是你思想的食材。提取正文、洗掉广告、
  打上DNA标签——挖的是你自己的矿，不是公海的垃圾。

特性:
  - 纯 stdlib，零外部依赖
  - 自研可读性算法（标题密度/链接密度/文本密度）
  - 智能编码检测
  - 支持批量导入浏览器矿工输出
  - 输出结构化JSONL + 纯文本

用法:
  python3 bin/lh_page_extractor.py fetch <url>              # 单页提取
  python3 bin/lh_page_extractor.py batch <urls.jsonl>       # 批量提取
  python3 bin/lh_page_extractor.py mine --from-browser       # 从浏览器矿工输出提取
  python3 bin/lh_page_extractor.py mine --urls url1 url2...  # 从指定URL列表
"""

import hashlib, json, os, re, sys, time, gzip, zlib
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from urllib.parse import urlparse, urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SYSTEM_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = SYSTEM_ROOT / "data" / "page_extract"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BROWSER_MINE_DIR = SYSTEM_ROOT / "data" / "browser_mine"

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) LonghunPageExtractor/1.0"
TIMEOUT = 15  # 秒

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 内容质量判断
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 噪声标签（其内容应该被移除）
NOISE_TAGS = {"script", "style", "nav", "footer", "header", "aside",
              "noscript", "iframe", "svg", "form", "button", "input",
              "select", "textarea", "img", "video", "audio", "canvas"}

# 导航/广告/侧边栏类名模式
NOISE_CLASS_PATTERNS = re.compile(
    r"(nav|menu|sidebar|footer|header|banner|advert|popup|modal|"
    r"comment|share|social|related|recommend|suggest|widget|"
    r"toolbar|breadcrumb|pagination|login|signup|subscribe)",
    re.IGNORECASE
)

# 高价值标签（正文容器）
CONTENT_TAGS = {"article", "main", "section", "div", "p", "pre", "blockquote",
                "h1", "h2", "h3", "h4", "h5", "h6", "li", "td", "th", "dd", "dt"}

# 正文容器类名/id模式
CONTENT_CLASS_PATTERNS = re.compile(
    r"(article|content|post|entry|body|text|main|markdown|"
    r"blog|story|news|detail|read|doc|paragraph)",
    re.IGNORECASE
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class PageContent:
    """提取的页面内容"""
    url: str
    title: str
    domain: str
    text: str                      # 清洗后正文
    text_length: int = 0
    quality_score: float = 0.0     # 0-1 内容质量
    content_type: str = ""         # article/code/doc/unknown
    publish_time: str = ""
    extracted_at: str = ""
    dna: str = ""
    error: str = ""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HTML → 正文提取器
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ReadabilityExtractor(HTMLParser):
    """自研可读性提取器 — 基于文本密度和标签启发式"""

    def __init__(self):
        super().__init__()
        self._title = ""
        self._in_title = False
        self._blocks: List[Dict] = []      # {tag, class, id, text, depth}
        self._current_block: Dict = None
        self._depth = 0
        self._skip_depth = 0               # 噪声深度（在此深度以上全部跳过）
        self._text_buffer: List[str] = []

    def handle_starttag(self, tag):
        tag_lower = tag.lower()

        if tag_lower == "title":
            self._in_title = True
            return

        if tag_lower in NOISE_TAGS:
            self._skip_depth += 1
            return

        if self._skip_depth > 0:
            return

        if tag_lower in CONTENT_TAGS:
            attrs = dict(self._current_attrs() if hasattr(self, '_current_attrs') else [])
            cls = attrs.get("class", "")
            elem_id = attrs.get("id", "")

            # 刷新当前block
            if self._text_buffer:
                text = " ".join(self._text_buffer).strip()
                if text and self._current_block:
                    self._current_block["text"] += " " + text
                self._text_buffer = []

            self._current_block = {
                "tag": tag_lower,
                "class": cls,
                "id": elem_id,
                "text": "",
                "depth": self._depth,
            }
            self._depth += 1

    def handle_endtag(self, tag):
        tag_lower = tag.lower()

        if tag_lower == "title":
            self._in_title = False
            return

        if tag_lower in NOISE_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
            return

        if self._skip_depth > 0:
            return

        if tag_lower in CONTENT_TAGS:
            # 刷新文本缓冲区
            if self._text_buffer:
                text = " ".join(self._text_buffer).strip()
                if text and self._current_block:
                    self._current_block["text"] += " " + text
                self._text_buffer = []

            if self._current_block and self._current_block["text"].strip():
                self._blocks.append(self._current_block)
            self._current_block = None
            self._depth = max(0, self._depth - 1)

    def handle_data(self, data):
        if self._in_title:
            self._title += data
            return
        if self._skip_depth > 0:
            return

        text = data.strip()
        if text:
            self._text_buffer.append(text)

    def _current_attrs(self):
        # HTMLParser doesn't expose attrs in handle_starttag by default,
        # we override it in parse()
        return []

    def get_best_text(self) -> Tuple[str, str, float]:
        """选择质量最高的文本块作为正文"""
        title = self._title.strip()

        if not self._blocks:
            return title, "", 0.0

        # 对每个block打分
        scored = []
        for block in self._blocks:
            text = block["text"].strip()
            if len(text) < 50:  # 太短，忽略
                continue

            score = self._score_block(block, text)
            scored.append((score, text, block))

        if not scored:
            # 降级：合并所有文本
            all_text = "\n\n".join(b["text"].strip() for b in self._blocks if len(b["text"].strip()) > 20)
            return title, all_text, 0.1

        scored.sort(key=lambda x: x[0], reverse=True)

        # 取top-3合并（处理分页/多段落）
        top_texts = []
        total_score = 0.0
        for i, (score, text, block) in enumerate(scored[:3]):
            top_texts.append(text)
            total_score += score

        body = "\n\n".join(top_texts)
        quality = min(1.0, total_score / max(len(scored[:3]), 1))

        return title, body, quality

    def _score_block(self, block: Dict, text: str) -> float:
        """对文本块打分 (0-1)"""
        score = 0.3  # 基础分

        text_len = len(text)
        cls = block.get("class", "")
        elem_id = block.get("id", "")
        tag = block.get("tag", "")

        # 长度加分
        if text_len > 500:
            score += 0.2
        elif text_len > 200:
            score += 0.1
        elif text_len > 1000:
            score += 0.1

        # 标签加分
        if tag in ("article", "main"):
            score += 0.3
        elif tag in ("section", "div"):
            score += 0.1
        elif tag.startswith("h"):
            score += 0.05

        # class/id 含正文关键词
        if CONTENT_CLASS_PATTERNS.search(cls) or CONTENT_CLASS_PATTERNS.search(elem_id):
            score += 0.2

        # 噪声class/id扣分
        if NOISE_CLASS_PATTERNS.search(cls) or NOISE_CLASS_PATTERNS.search(elem_id):
            score -= 0.3

        # 链接密度（高链接密度=导航/列表，不是正文）
        link_count = text.count("http://") + text.count("https://")
        link_density = link_count / max(text_len / 100, 1)
        if link_density > 0.5:
            score -= 0.4
        elif link_density > 0.2:
            score -= 0.2

        # 段落密度（中文段落=按句号/换行分割）
        paragraphs = len(re.findall(r"[。！？\n]{1,2}", text))
        para_density = paragraphs / max(text_len / 200, 1)
        if para_density > 0.3:
            score += 0.1

        return max(0.0, min(1.0, score))


class AttrHTMLParser(ReadabilityExtractor):
    """扩展HTMLParser以支持属性访问"""

    def handle_starttag(self, tag, attrs):
        self._current_attrs_list = attrs
        super().handle_starttag(tag)

    def _current_attrs(self):
        return getattr(self, '_current_attrs_list', [])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 内容提取引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PageExtractor:
    """网页内容提取器"""

    def __init__(self):
        self.results: List[PageContent] = []
        self._extracted_at = datetime.now().isoformat()

    def fetch(self, url: str) -> PageContent:
        """抓取单个URL并提取正文"""
        domain = urlparse(url).netloc
        pc = PageContent(
            url=url, title="", domain=domain, text="",
            extracted_at=self._extracted_at,
        )

        try:
            req = Request(url, headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
            })
            resp = urlopen(req, timeout=TIMEOUT)

            # 获取编码
            content_type = resp.headers.get("Content-Type", "")
            encoding = "utf-8"
            if "charset=" in content_type:
                encoding = content_type.split("charset=")[-1].strip().lower()
                if encoding == "gb2312":
                    encoding = "gbk"

            # 读取并解压
            raw = resp.read()
            content_encoding = resp.headers.get("Content-Encoding", "")
            if "gzip" in content_encoding:
                raw = gzip.decompress(raw)
            elif "deflate" in content_encoding:
                raw = zlib.decompress(raw)

            html = raw.decode(encoding, errors="replace")

            # 提取标题和正文
            pc.title, pc.text, pc.quality_score = self._extract_content(html, url)

            if pc.text:
                pc.text_length = len(pc.text)
                pc.content_type = self._classify_content(pc)
                pc.dna = self._gen_dna(pc)
            else:
                pc.error = "无法提取正文内容"

        except HTTPError as e:
            pc.error = f"HTTP {e.code}: {e.reason}"
        except URLError as e:
            pc.error = f"网络错误: {e.reason}"
        except Exception as e:
            pc.error = f"提取失败: {str(e)[:100]}"

        self.results.append(pc)
        return pc

    def batch(self, urls: List[str], max_concurrent: int = 1) -> List[PageContent]:
        """批量提取（串行以避免被封）"""
        results = []
        total = len(urls)
        for i, url in enumerate(urls):
            if url and url.startswith("http"):
                pc = self.fetch(url)
                results.append(pc)
                if i % 10 == 0 and i > 0:
                    print(f"  进度: {i}/{total} | 成功: {sum(1 for r in results if r.text)}")
                time.sleep(0.5)  # 礼貌延迟
        return results

    def mine_from_browser_output(self, max_urls: int = 100, categories: Optional[List[str]] = None) -> List[PageContent]:
        """从浏览器矿工输出中提取高价值URL并抓取"""
        history_files = sorted(BROWSER_MINE_DIR.glob("browser_history_*.jsonl"),
                               key=lambda f: f.stat().st_mtime, reverse=True)

        if not history_files:
            print("未找到浏览器矿工输出，请先运行 lh_browser_miner.py extract")
            return []

        # 读取URL列表
        urls_to_fetch = []
        seen = set()

        for hf in history_files[:1]:  # 只用最新的
            with open(hf, 'r', encoding='utf-8') as f:
                for line in f:
                    entry = json.loads(line)
                    url = entry.get("url", "")
                    category = entry.get("category", "")

                    if not url or url in seen:
                        continue
                    if categories and category not in categories:
                        continue

                    # 优先技术/知识/学术类
                    priority = 0
                    if category in ("技术文档", "AI对话", "知识", "中国学术"):
                        priority = 2
                    elif category in ("工具", "搜索"):
                        priority = 1

                    urls_to_fetch.append((url, category, priority))
                    seen.add(url)

        # 按优先级排序，取前N个
        urls_to_fetch.sort(key=lambda x: x[2], reverse=True)
        urls_to_fetch = urls_to_fetch[:max_urls]

        print(f"⛏️ 从 {len(urls_to_fetch)} 个高价值URL开始挖掘...")
        return self.batch([u[0] for u in urls_to_fetch])

    def export(self, output_path: Optional[Path] = None) -> Path:
        """导出为JSONL"""
        target = output_path or (OUTPUT_DIR / f"page_extract_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")
        count = 0
        with open(target, 'w', encoding='utf-8') as f:
            for pc in self.results:
                if pc.text:  # 只要有内容就导出
                    f.write(json.dumps({
                        "url": pc.url,
                        "title": pc.title,
                        "domain": pc.domain,
                        "text": pc.text,
                        "text_length": pc.text_length,
                        "quality_score": pc.quality_score,
                        "content_type": pc.content_type,
                        "extracted_at": pc.extracted_at,
                        "dna": pc.dna,
                        "error": pc.error,
                    }, ensure_ascii=False) + "\n")
                    count += 1
        print(f"📦 导出: {count} 篇有效文章 → {target.name}")
        return target

    def get_stats(self) -> Dict:
        stats = {
            "total": len(self.results),
            "success": sum(1 for r in self.results if r.text),
            "failed": sum(1 for r in self.results if r.error and not r.text),
            "avg_quality": sum(r.quality_score for r in self.results if r.text) / max(len([r for r in self.results if r.text]), 1),
            "avg_length": sum(r.text_length for r in self.results if r.text) / max(len([r for r in self.results if r.text]), 1),
            "by_type": {},
        }
        for r in self.results:
            if r.content_type:
                stats["by_type"][r.content_type] = stats["by_type"].get(r.content_type, 0) + 1
        return stats

    # ━─ internal ━─

    def _extract_content(self, html: str, url: str) -> Tuple[str, str, float]:
        parser = AttrHTMLParser()
        try:
            parser.feed(html)
        except:
            pass
        title, text, quality = parser.get_best_text()

        # 后处理：清洗文本
        if text:
            text = self._clean_text(text)

        return title, text, quality

    def _clean_text(self, text: str) -> str:
        """清洗提取的文本"""
        # 移除多余空白行
        text = re.sub(r'\n{4,}', '\n\n\n', text)
        # 移除多余空格
        text = re.sub(r' {3,}', '  ', text)
        # 移除纯空白行
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        # 截断过长内容（50KB上限）
        if len(text) > 50000:
            text = text[:50000] + "\n\n[内容过长，已截断]"
        return text.strip()

    def _classify_content(self, pc: PageContent) -> str:
        """根据内容特征分类"""
        text = pc.text
        if not text:
            return "unknown"

        code_indicators = len(re.findall(r'(def |class |function |import |const |let |var |```)', text))
        math_indicators = len(re.findall(r'[∑∫∏√∞∂∇]|\\frac|\\sum|\\int|公式|定理|证明', text))
        cn_ratio = len(re.findall(r'[\u4e00-\u9fff]', text)) / max(len(text), 1)

        if code_indicators > 5:
            return "code" if cn_ratio < 0.5 else "tech_article"
        if math_indicators > 3:
            return "academic"
        if cn_ratio > 0.3:
            return "article_cn"
        return "article_en"

    def _gen_dna(self, pc: PageContent) -> str:
        now = datetime.now(timezone.utc)
        sample_hash = hashlib.sha256(pc.url.encode()).hexdigest()[:8]
        tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
        dizhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
        gz = f"{tiangan[now.year%10]}{dizhi[now.month%12]}·{tiangan[(now.day+9)%10]}{dizhi[(now.day+1)%12]}"
        return f"#龍芯⚡️{gz}-PAGE-EXTRACT-{pc.content_type}-{sample_hash}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    import argparse
    p = argparse.ArgumentParser(description="龍魂·网页内容提取器")
    sub = p.add_subparsers(dest="cmd")

    fetch_p = sub.add_parser("fetch", help="提取单个URL")
    fetch_p.add_argument("url", help="目标URL")

    batch_p = sub.add_parser("batch", help="批量提取")
    batch_p.add_argument("urls_file", help="URL列表JSONL文件")
    batch_p.add_argument("--max", type=int, default=50, help="最大抓取数")

    mine_p = sub.add_parser("mine", help="挖矿模式·从浏览器历史提取")
    mine_p.add_argument("--from-browser", action="store_true", help="从浏览器矿工输出读取URL")
    mine_p.add_argument("--urls", nargs="*", help="手动指定URL列表")
    mine_p.add_argument("--max", type=int, default=30, help="最大抓取数")
    mine_p.add_argument("--categories", nargs="*", help="限定分类 (如: 技术文档 AI对话)")
    mine_p.add_argument("--no-export", action="store_true")

    args = p.parse_args()
    extractor = PageExtractor()

    if args.cmd == "fetch":
        print(f"⛏️ 挖掘: {args.url}")
        pc = extractor.fetch(args.url)
        if pc.text:
            print(f"   标题: {pc.title}")
            print(f"   正文: {pc.text_length} 字 | 质量: {pc.quality_score:.2f} | 类型: {pc.content_type}")
            print(f"   预览: {pc.text[:200]}...")
            extractor.export()
        else:
            print(f"   ❌ {pc.error}")
            sys.exit(1)

    elif args.cmd == "batch":
        with open(args.urls_file, 'r', encoding='utf-8') as f:
            urls = [json.loads(line).get("url", "") for line in f if line.strip()]
        urls = [u for u in urls if u.startswith("http")][:args.max]
        print(f"⛏️ 批量挖掘 {len(urls)} 个URL...")
        extractor.batch(urls)
        extractor.export()
        stats = extractor.get_stats()
        print(f"   成功: {stats['success']} | 失败: {stats['failed']} | 平均质量: {stats['avg_quality']:.2f}")

    elif args.cmd == "mine":
        if args.from_browser:
            extractor.mine_from_browser_output(max_urls=args.max, categories=args.categories)
        elif args.urls:
            extractor.batch(args.urls[:args.max])
        else:
            print("请指定 --from-browser 或 --urls")
            sys.exit(1)

        if not args.no_export:
            extractor.export()
        stats = extractor.get_stats()
        print(f"   成功: {stats['success']} | 失败: {stats['failed']} | 平均质量: {stats['avg_quality']:.2f}")

    else:
        p.print_help()


if __name__ == "__main__":
    main()
