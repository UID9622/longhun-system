# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂搜索引擎 v2.0
增强版：反爬伪装、多站点解析策略、编码容错、结构化输出、缓存TTL控制
DNA: #龍芯⚡️丙午·乙未·癸酉·戌时·☰乾-SEARCH-ENGINE-v2.0-9F8E7D6C
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0
"""

import sys
import os
import re
import json
import time
import hashlib
import argparse
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

# pandas 为可选依赖，CSV 输出时才需要
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

# ---------- 配置 ----------
CACHE_DIR = Path.home() / ".longhun/cache/search_engine"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
DEFAULT_TIMEOUT = 10
DEFAULT_RETRY = 2
DEFAULT_DELAY = 0.5
DEFAULT_CACHE_TTL = 86400  # 24小时

# 预设解析策略
EXTRACTOR_MAP = {
    'default': lambda soup: soup.find('article') or soup.find('div', class_='content') or soup.find('main') or soup.find('body'),
    'liaoxuefeng': lambda soup: soup.find('div', class_='book-content') or soup.find('main'),
    'zhihu': lambda soup: soup.find('div', class_='RichContent-inner') or soup.find('div', class_='Post-content'),
    'runoob': lambda soup: soup.find('div', id='content') or soup.find('div', class_='article-content'),
    'csdn': lambda soup: soup.find('div', id='content_views') or soup.find('article'),
    'raw': lambda soup: soup,
}

# ---------- 辅助函数 ----------
def safe_url_encode(text):
    """对中文等非ASCII字符进行URL编码"""
    return urllib.parse.quote(text, safe='')

def decode_query_string(qs):
    """递归解码URL查询字符串中的%XX，同时修复 latin-1 → utf-8 错码"""
    # 先处理 latin-1 编码的中文
    try:
        qs = qs.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass
    while '%' in qs:
        qs = urllib.parse.unquote_plus(qs)
    return qs

def fetch_page(url, headers=None, user_agent=None, timeout=DEFAULT_TIMEOUT, retry=DEFAULT_RETRY, delay=DEFAULT_DELAY):
    """带重试、伪装、延迟的页面获取"""
    headers = headers or {}
    if user_agent:
        headers.setdefault('User-Agent', user_agent)
    else:
        headers.setdefault('User-Agent', DEFAULT_USER_AGENT)
    headers.setdefault('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    headers.setdefault('Accept-Language', 'zh-CN,zh;q=0.9,en;q=0.8')
    
    for attempt in range(retry + 1):
        try:
            time.sleep(delay)
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            # 根据内容编码自动解码
            if resp.encoding is None:
                resp.encoding = 'utf-8'
            return resp.text
        except Exception as e:
            if attempt == retry:
                raise
            time.sleep(1)
    raise RuntimeError(f"Failed to fetch {url} after {retry} retries")

def extract_content(html, strategy='default', max_chars=2000):
    """根据策略提取正文"""
    soup = BeautifulSoup(html, 'html.parser')
    # 移除脚本和样式
    for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
        tag.decompose()
    
    if strategy in EXTRACTOR_MAP:
        container = EXTRACTOR_MAP[strategy](soup)
    else:
        container = EXTRACTOR_MAP['default'](soup)
    
    if container is None:
        container = soup.body or soup
    
    text = container.get_text(separator='\n', strip=True)
    # 压缩多余空白
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # 截取前 max_chars
    if len(text) > max_chars:
        text = text[:max_chars] + '...'
    return text

def search_bing(query, n=10):
    """Bing搜索（带伪装UA，国内可通）"""
    url = f"https://www.bing.com/search?q={safe_url_encode(query)}&count={n}"
    headers = {
        'User-Agent': DEFAULT_USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        # Bing 搜索结果在 <ol id="b_results"> 下的 <li class="b_algo">
        for li in soup.select('ol#b_results li.b_algo'):
            h2 = li.find('h2')
            if not h2:
                continue
            a = h2.find('a')
            if not a:
                continue
            title = a.get_text(strip=True)
            link = a.get('href')
            # 描述
            desc = li.find('div', class_='b_caption')
            if desc:
                desc_text = desc.get_text(strip=True)
            else:
                desc_text = ''
            if link and title:
                results.append({
                    'title': title,
                    'link': link,
                    'snippet': desc_text[:200]
                })
            if len(results) >= n:
                break
        return results
    except Exception as e:
        print(f"🟡 Bing搜索失败: {e}", file=sys.stderr)
        # 备用：返回模拟结果，标明失败原因
        return [
            {'title': f'关于"{query}"的搜索结果 {i+1} (模拟)', 
             'link': f'https://example.com/result{i}', 
             'snippet': f'Bing搜索异常({str(e)[:50]})，这是模拟结果。请检查网络或稍后重试。'}
            for i in range(min(n, 5))
        ]

# ---------- 缓存 ----------
def get_cache_key(query):
    return hashlib.md5(query.encode('utf-8')).hexdigest()

def cache_get(query):
    key = get_cache_key(query)
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 检查TTL
        if 'timestamp' in data:
            age = time.time() - data['timestamp']
            if age < data.get('ttl', DEFAULT_CACHE_TTL):
                return data.get('results')
    return None

def cache_set(query, results, ttl=DEFAULT_CACHE_TTL):
    key = get_cache_key(query)
    cache_file = CACHE_DIR / f"{key}.json"
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': time.time(),
            'ttl': ttl,
            'results': results
        }, f, ensure_ascii=False, indent=2)

def cache_status():
    total = len(list(CACHE_DIR.glob('*.json')))
    recent = 0
    for f in CACHE_DIR.glob('*.json'):
        mtime = f.stat().st_mtime
        if time.time() - mtime < 86400:
            recent += 1
    return {'total_cached': total, 'recent_24h': recent}

# ---------- CLI 搜索 ----------
def cli_search(args):
    query = args.query
    n = args.n
    deep = args.deep or 0
    use_cache = not args.no_cache
    ttl = args.cache_ttl or DEFAULT_CACHE_TTL

    # 尝试读缓存
    results = None
    if use_cache:
        results = cache_get(query)
    if results is None:
        results = search_bing(query, n)
        if use_cache:
            cache_set(query, results, ttl)
    else:
        print(f"📦 使用缓存 (TTL={ttl}s)", file=sys.stderr)

    # 输出
    if args.output == 'json':
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    elif args.output == 'csv':
        if not HAS_PANDAS:
            print("❌ 需要安装 pandas 才能输出 CSV: pip install pandas", file=sys.stderr)
            # 降级为 JSON 输出
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return
        df = pd.DataFrame(results)
        df.to_csv(sys.stdout, index=False)
        return

    # 终端友好输出
    print("\n" + "=" * 60)
    print(f"  🐉 龍魂搜索 · {query}")
    print(f"  后端: bing | 缓存: {'是' if use_cache else '否'} | 结果: {len(results)}条")
    print(f"  DNA: #龍芯⚡️丙午·乙未·癸酉·戌时·☰乾-SEARCH-ENGINE-v2.0-9F8E7D6C")
    print("=" * 60)
    for i, res in enumerate(results, 1):
        title = res.get('title', '无标题')
        link = res.get('link', '#')
        snippet = res.get('snippet', '')
        print(f"\n  {i}. {title}")
        print(f"     {link}")
        if snippet:
            print(f"     {snippet[:150]}")

    # 深度提取
    if deep > 0:
        print("\n" + "─" * 60)
        print(f"  📄 深度提取 (前 {min(deep, len(results))} 页)")
        print("─" * 60)
        extractor_strategy = args.extractor or 'default'
        for idx, res in enumerate(results[:deep], 1):
            url = res.get('link')
            if not url:
                continue
            print(f"\n  标题: {res.get('title', '')}")
            try:
                html = fetch_page(url, user_agent=args.user_agent, timeout=args.timeout,
                                  retry=args.retry, delay=args.delay)
                text = extract_content(html, strategy=extractor_strategy, max_chars=args.max_chars or 2000)
                lines = text.split('\n')
                preview = '\n'.join(line.strip() for line in lines if line.strip())[:300]
                print(f"  预览: {preview}...")
            except Exception as e:
                print(f"  ❌ 提取失败: {e}")

# ---------- HTTP API ----------
class SearchHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 修复 latin-1 编码的中文 URL（从原始字节还原 UTF-8）
        path = self.path
        try:
            path = path.encode("latin-1").decode("utf-8")
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
        parsed = urlparse(path)
        
        if parsed.path == '/search':
            qs = parse_qs(decode_query_string(parsed.query))
            q = qs.get('q', [''])[0]
            n = int(qs.get('n', ['5'])[0])
            if not q:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing q parameter')
                return
            try:
                results = search_bing(q, n)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(results, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        elif parsed.path == '/cache-status':
            status = cache_status()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(status, ensure_ascii=False).encode('utf-8'))
        elif parsed.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': '🟢 healthy',
                'version': 'v2.0',
                'dna': '#龍芯⚡️丙午·乙未·癸酉·戌时·☰乾-SEARCH-ENGINE-v2.0-9F8E7D6C'
            }, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_api(port=9631):
    server = HTTPServer(('127.0.0.1', port), SearchHandler)
    print(f"🐉 龍魂搜索 API v2.0 启动在 http://127.0.0.1:{port}")
    print("可用接口: /search?q=关键词&n=数量  /cache-status  /health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n关闭服务器")

# ---------- 主入口 ----------
def main():
    parser = argparse.ArgumentParser(description='龍魂搜索引擎 v2.0')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # search 子命令
    search_parser = subparsers.add_parser('search', help='搜索并显示结果')
    search_parser.add_argument('query', type=str, help='搜索关键词')
    search_parser.add_argument('--n', type=int, default=10, help='返回结果数')
    search_parser.add_argument('--deep', type=int, default=0, help='深度提取前N个页面的正文')
    search_parser.add_argument('--output', choices=['text', 'json', 'csv'], default='text', help='输出格式')
    search_parser.add_argument('--user-agent', type=str, default=DEFAULT_USER_AGENT, help='自定义User-Agent')
    search_parser.add_argument('--header', action='append', help='自定义请求头，格式 "Key: Value"')
    search_parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help='请求超时秒数')
    search_parser.add_argument('--retry', type=int, default=DEFAULT_RETRY, help='重试次数')
    search_parser.add_argument('--delay', type=float, default=DEFAULT_DELAY, help='请求间隔秒数')
    search_parser.add_argument('--extractor', choices=list(EXTRACTOR_MAP.keys()), default='default', help='页面解析策略')
    search_parser.add_argument('--max-chars', type=int, default=2000, help='提取正文最大字符数')
    search_parser.add_argument('--no-cache', action='store_true', help='不使用缓存')
    search_parser.add_argument('--cache-ttl', type=int, default=DEFAULT_CACHE_TTL, help='缓存生存期(秒)')

    # cache-status 子命令
    subparsers.add_parser('cache-status', help='查看缓存统计')

    # api 子命令（同时保留 serve 别名以兼容 v1.0）
    api_parser = subparsers.add_parser('api', help='启动HTTP API服务')
    api_parser.add_argument('--port', type=int, default=9631, help='监听端口')
    serve_parser = subparsers.add_parser('serve', help='启动HTTP API服务（v1.0兼容别名）')
    serve_parser.add_argument('--port', type=int, default=9631, help='监听端口')

    args = parser.parse_args()

    if args.command == 'search':
        cli_search(args)
    elif args.command == 'cache-status':
        status = cache_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
    elif args.command in ('api', 'serve'):
        port = getattr(args, 'port', 9631)
        run_api(port=port)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
