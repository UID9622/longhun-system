#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·链接解析引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-链接解析-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：解析用户发来的任何URL，提取元数据、正文、链接，可选递归子页面
定位：龙魂系统统一信息采集入口
"""

import sys
import re
import json
import time
import hashlib
import argparse
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("请安装: pip install requests beautifulsoup4")
    sys.exit(1)

# ============================================================
# 一、配置与数据结构
# ============================================================

@dataclass
class LinkInfo:
    """单条链接信息"""
    url: str
    title: str = ""
    description: str = ""
    text: str = ""
    html: str = ""
    content_type: str = ""
    status_code: int = 0
    headers: Dict[str, str] = field(default_factory=dict)
    links: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)
    styles: List[str] = field(default_factory=list)
    depth: int = 0
    parent_url: str = ""
    fetch_time: float = 0.0
    error: Optional[str] = None
    dna: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


@dataclass
class ParseResult:
    """解析结果"""
    root_url: str
    depth_limit: int
    total_pages: int
    pages: List[LinkInfo] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    fetch_time: float = 0.0
    dna: str = ""

    def to_dict(self) -> Dict:
        return {
            "root_url": self.root_url,
            "depth_limit": self.depth_limit,
            "total_pages": self.total_pages,
            "pages": [p.to_dict() for p in self.pages],
            "errors": self.errors,
            "fetch_time": self.fetch_time,
            "dna": self.dna
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# ============================================================
# 二、核心解析引擎
# ============================================================

class LinkParser:
    """龙魂链接解析引擎"""

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        max_pages: int = 100,
        max_depth: int = 1,
        allowed_domains: Optional[List[str]] = None,
        deny_paths: Optional[List[str]] = None,
        extract_links: bool = True,
        extract_images: bool = True,
        extract_text: bool = True,
        save_html: bool = False,
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.user_agent = user_agent
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.allowed_domains = allowed_domains
        self.deny_paths = deny_paths or []
        self.extract_links = extract_links
        self.extract_images = extract_images
        self.extract_text = extract_text
        self.save_html = save_html

        self.session = self._create_session()
        self.visited: Set[str] = set()
        self.pages: List[LinkInfo] = []
        self.errors: List[str] = []
        self._page_count = 0

    def _create_session(self) -> requests.Session:
        """创建带重试的会话"""
        session = requests.Session()
        session.headers.update({"User-Agent": self.user_agent})

        retry = Retry(
            total=self.max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _generate_dna(self, url: str) -> str:
        """生成DNA追溯码"""
        hash_val = hashlib.sha256(url.encode()).hexdigest()[:8]
        today = datetime.now().strftime("%Y%m%d")
        return f"#龍芯⚡️{today}-链接解析-{hash_val}"

    def _normalize_url(self, url: str, base: Optional[str] = None) -> str:
        """规范化URL"""
        if base:
            url = urljoin(base, url)
        # 去除片段
        url = url.split("#")[0]
        # 去除尾部斜杠
        if url.endswith("/"):
            url = url[:-1]
        return url

    def _should_fetch(self, url: str, depth: int) -> bool:
        """判断是否应该抓取"""
        # 深度限制
        if depth > self.max_depth:
            return False

        # 页面总数限制
        if self._page_count >= self.max_pages:
            return False

        # 已访问
        if url in self.visited:
            return False

        # 域名白名单
        if self.allowed_domains:
            domain = urlparse(url).netloc
            if not any(d in domain for d in self.allowed_domains):
                return False

        # 路径黑名单
        path = urlparse(url).path
        for deny in self.deny_paths:
            if deny in path:
                return False

        # 文件扩展名过滤
        ext = path.split(".")[-1].lower() if "." in path else ""
        skip_exts = ["jpg", "jpeg", "png", "gif", "webp", "svg", "ico", "mp4", "mp3", "pdf", "zip", "gz", "rar"]
        if ext in skip_exts:
            return False

        return True

    def _fetch_page(self, url: str, depth: int = 0, parent_url: str = "") -> Optional[LinkInfo]:
        """抓取单个页面"""
        start_time = time.time()
        info = LinkInfo(url=url, depth=depth, parent_url=parent_url)

        try:
            resp = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            info.status_code = resp.status_code
            info.headers = dict(resp.headers)
            info.content_type = resp.headers.get("content-type", "")

            if resp.status_code != 200:
                info.error = f"HTTP {resp.status_code}"
                return info

            # 检测内容类型
            content_type = resp.headers.get("content-type", "").lower()
            if "html" not in content_type and "xml" not in content_type:
                info.error = f"非HTML内容: {content_type}"
                return info

            # 保存HTML
            html = resp.text
            if self.save_html:
                info.html = html[:50000]  # 限制大小

            # 解析HTML
            soup = BeautifulSoup(html, "html.parser")

            # 提取标题
            title_tag = soup.find("title")
            if title_tag:
                info.title = title_tag.get_text(strip=True)

            # 提取描述
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc:
                info.description = meta_desc.get("content", "")

            # 提取正文文本
            if self.extract_text:
                # 移除脚本和样式
                for tag in soup(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                text = soup.get_text(separator="\n", strip=True)
                # 压缩多余空白
                text = re.sub(r"\n\s*\n", "\n\n", text)
                info.text = text[:10000]  # 限制长度

            # 提取所有链接
            if self.extract_links:
                links = set()
                for a in soup.find_all("a", href=True):
                    href = a["href"].strip()
                    if not href or href.startswith("javascript:") or href.startswith("mailto:") or href.startswith("#"):
                        continue
                    full_url = self._normalize_url(href, url)
                    if full_url:
                        links.add(full_url)
                info.links = list(links)

            # 提取图片
            if self.extract_images:
                images = set()
                for img in soup.find_all("img", src=True):
                    src = img["src"].strip()
                    if not src:
                        continue
                    full_url = self._normalize_url(src, url)
                    if full_url:
                        images.add(full_url)
                info.images = list(images)

            # 提取脚本源
            scripts = set()
            for script in soup.find_all("script", src=True):
                src = script["src"].strip()
                if src:
                    full_url = self._normalize_url(src, url)
                    if full_url:
                        scripts.add(full_url)
            info.scripts = list(scripts)

            # 提取样式源
            styles = set()
            for link in soup.find_all("link", rel="stylesheet", href=True):
                href = link["href"].strip()
                if href:
                    full_url = self._normalize_url(href, url)
                    if full_url:
                        styles.add(full_url)
            info.styles = list(styles)

            info.fetch_time = time.time() - start_time
            info.dna = self._generate_dna(url)

            return info

        except requests.exceptions.Timeout:
            info.error = f"请求超时 ({self.timeout}s)"
        except requests.exceptions.ConnectionError as e:
            info.error = f"连接错误: {str(e)[:50]}"
        except Exception as e:
            info.error = f"未知错误: {str(e)[:100]}"
            if "禁止" in str(e) or "forbidden" in str(e).lower():
                info.error = "访问被拒绝 (403/Forbidden)"
        finally:
            info.fetch_time = time.time() - start_time
            if not info.dna:
                info.dna = self._generate_dna(url)
            return info

    def parse(self, url: str, depth_limit: Optional[int] = None) -> ParseResult:
        """主解析入口"""
        if depth_limit is not None:
            self.max_depth = depth_limit

        self.visited.clear()
        self.pages.clear()
        self.errors.clear()
        self._page_count = 0

        start_time = time.time()
        root_url = self._normalize_url(url)

        # 递归抓取
        self._parse_recursive(root_url, 0)

        result = ParseResult(
            root_url=root_url,
            depth_limit=self.max_depth,
            total_pages=len(self.pages),
            pages=self.pages,
            errors=self.errors,
            fetch_time=time.time() - start_time,
            dna=f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-链接解析-{hashlib.sha256(root_url.encode()).hexdigest()[:8]}"
        )
        return result

    def _parse_recursive(self, url: str, depth: int):
        """递归抓取子页面"""
        if not self._should_fetch(url, depth):
            return

        self.visited.add(url)

        info = self._fetch_page(url, depth)
        if info:
            self.pages.append(info)
            self._page_count += 1

            if info.error:
                self.errors.append(f"[深度{depth}] {url}: {info.error}")
                return

            # 如果是HTML且链接提取开启，递归抓取子页面
            if self.extract_links and depth < self.max_depth:
                # 限制子页面数量
                sub_count = 0
                for link in info.links[:50]:  # 每个页面最多取50个子链接
                    if sub_count >= 20:  # 每个深度最多20个新页面
                        break
                    if link.startswith("http") and link not in self.visited:
                        self._parse_recursive(link, depth + 1)
                        sub_count += 1
        else:
            self.errors.append(f"[深度{depth}] {url}: 抓取失败")


# ============================================================
# 三、命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龙魂·链接解析引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 解析单个链接
  python3 lh_link_parser.py https://example.com

  # 解析并保存为JSON
  python3 lh_link_parser.py https://example.com -o result.json

  # 递归抓取子页面（深度2）
  python3 lh_link_parser.py https://example.com -d 2

  # 限制抓取10页
  python3 lh_link_parser.py https://example.com -m 10

  # 仅抓取指定域名
  python3 lh_link_parser.py https://example.com --domain example.com

  # 读取链接列表
  python3 lh_link_parser.py -f urls.txt

  # 带参数：超时、重试等
  python3 lh_link_parser.py https://example.com -t 60 -r 5
        """
    )

    parser.add_argument(
        "url",
        nargs="?",
        help="要解析的URL"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="从文件中读取URL列表（每行一个）"
    )
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=1,
        help="递归深度（默认1，0=仅当前页）"
    )
    parser.add_argument(
        "-m", "--max-pages",
        type=int,
        default=50,
        help="最大抓取页面数（默认50）"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=30,
        help="请求超时秒数（默认30）"
    )
    parser.add_argument(
        "-r", "--retries",
        type=int,
        default=3,
        help="重试次数（默认3）"
    )
    parser.add_argument(
        "--domain",
        nargs="+",
        help="允许的域名白名单"
    )
    parser.add_argument(
        "--deny",
        nargs="+",
        help="禁止的路径关键词"
    )
    parser.add_argument(
        "--no-links",
        action="store_true",
        help="不提取链接"
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="不提取图片"
    )
    parser.add_argument(
        "--no-text",
        action="store_true",
        help="不提取正文文本"
    )
    parser.add_argument(
        "--save-html",
        action="store_true",
        help="保存HTML源码"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="输出JSON文件路径"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="格式化JSON输出"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细进度"
    )

    args = parser.parse_args()

    # 读取URL列表
    urls = []
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        urls.append(line)
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            sys.exit(1)
    elif args.url:
        urls = [args.url]
    else:
        parser.print_help()
        sys.exit(0)

    # 创建解析器
    parser_engine = LinkParser(
        timeout=args.timeout,
        max_retries=args.retries,
        max_pages=args.max_pages,
        max_depth=args.depth,
        allowed_domains=args.domain,
        deny_paths=args.deny,
        extract_links=not args.no_links,
        extract_images=not args.no_images,
        extract_text=not args.no_text,
        save_html=args.save_html,
    )

    results = []

    for idx, url in enumerate(urls, 1):
        if args.verbose:
            print(f"[{idx}/{len(urls)}] 解析: {url}")

        try:
            result = parser_engine.parse(url)
            results.append(result)

            if args.verbose:
                print(f"  ✅ 抓取 {result.total_pages} 页，{len(result.errors)} 个错误")
                if result.errors:
                    for err in result.errors[:3]:
                        print(f"    ⚠️ {err[:80]}...")
                if len(result.errors) > 3:
                    print(f"    ... 还有 {len(result.errors) - 3} 个错误")
        except Exception as e:
            print(f"❌ 解析失败: {e}")
            import traceback
            traceback.print_exc()
            continue

    # 输出结果
    if args.output:
        output_data = {
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-链接解析-{hashlib.sha256(' '.join(urls).encode()).hexdigest()[:8]}",
            "timestamp": datetime.now().isoformat(),
            "total_urls": len(urls),
            "results": [r.to_dict() for r in results]
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.pretty:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            else:
                json.dump(output_data, f, ensure_ascii=False)
        print(f"✅ 结果已保存: {args.output}")
    else:
        # 打印摘要
        print("\n" + "=" * 60)
        print("🐉 龙魂·链接解析结果")
        print("=" * 60)
        for result in results:
            print(f"🔗 根URL: {result.root_url}")
            print(f"📄 页面数: {result.total_pages}")
            print(f"⚠️ 错误数: {len(result.errors)}")
            print(f"⏱️ 耗时: {result.fetch_time:.2f}s")
            print(f"🧬 DNA: {result.dna}")
            print("-" * 40)
            # 显示每个页面的信息
            for page in result.pages[:5]:
                status = "✅" if not page.error else "❌"
                print(f"  {status} {page.url}")
                if page.title:
                    print(f"     📌 {page.title[:60]}")
                if page.links:
                    print(f"     🔗 {len(page.links)} 个链接")
                if page.images:
                    print(f"     🖼️ {len(page.images)} 张图片")
                if page.error:
                    print(f"     ⚠️ {page.error}")
            if len(result.pages) > 5:
                print(f"  ... 还有 {len(result.pages) - 5} 页")
            print("=" * 60)


if __name__ == "__main__":
    main()
