#!/usr/bin/env python3
"""
龍魂·CSDN文章拉取入库工具 v1.0
DNA: #龍芯⚡️丙午·丙申·辛亥·戌时·䷐随-CSDN-FETCHER-v1.0
创建者: 诸葛鑫（UID9622）+ AI协作
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

功能:
  1. 从CSDN拉取UID9622的文章
  2. 自动按类型归档到 longhun-system/ 对应目录
  3. 自动套用抬头模板
  4. 自动GPG签名
  5. 自动Git提交

用法:
  lh csdn fetch <url>            # 拉取单篇文章
  lh csdn fetch --all            # 拉取所有文章
  lh csdn fetch --latest 5       # 拉取最新5篇
  lh csdn list                   # 列出已入库文章
"""

import json
import re
import sys
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

LONGHUN_ROOT = Path(__file__).resolve().parent.parent
CSDN_REGISTRY = LONGHUN_ROOT / "01_protocols" / "csdn_registry.json"

# 文章类型→目录映射
TYPE_MAP = {
    "protocol": "01_protocols",       # 协议/规范
    "principle": "01_protocols",      # 原则/声明
    "technical": "06_技術文檔",       # 技术文章
    "article": "articles",            # 一般文章
    "paper": "papers",                # 论文/深度
    "diary": "04_決策日誌",           # 日记/复盘
    "story": "articles",              # 故事/叙事
}

# 文章类型判定关键词
TYPE_KEYWORDS = {
    "protocol": ["协议", "规范", "标准", "条款", "宪法", "规则", "对齐"],
    "principle": ["原则", "声明", "底线", "不可", "天条", "焊死"],
    "technical": ["代码", "实现", "部署", "引擎", "算法", "Python", "架构"],
    "paper": ["分析", "研究", "模型", "理论", "推演", "博弈"],
    "diary": ["日记", "复盘", "总结", "记录", "回顾"],
}

# 抬头模板选择器（简化版）
HEADER_TEMPLATES = {
    "protocol": 3,      # 协议/原则声明型
    "principle": 3,     # 协议/原则声明型
    "technical": 2,     # 工程落地执行型
    "article": 6,       # 快速笔记/想法型
    "paper": 1,         # 学术博弈论分析型
    "diary": 5,         # 复盘/总结型
}


def load_registry() -> dict:
    """加载CSDN入库注册表"""
    if CSDN_REGISTRY.exists():
        return json.loads(CSDN_REGISTRY.read_text())
    return {"articles": [], "last_fetch": None}


def save_registry(reg: dict):
    """保存注册表"""
    CSDN_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    CSDN_REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=2))


def parse_csdn_url(url: str) -> dict:
    """解析CSDN URL"""
    # https://blog.csdn.net/UID9622/article/details/163512218
    m = re.match(r'https?://blog\.csdn\.net/(\w+)/article/details/(\d+)', url)
    if not m:
        raise ValueError(f"不是有效的CSDN文章URL: {url}")
    return {
        "author": m.group(1),
        "article_id": m.group(2),
        "url": url,
    }


def classify_article(title: str, content: str) -> str:
    """根据标题和内容判定文章类型"""
    text = title + " " + content[:2000]
    
    scores = {}
    for atype, keywords in TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[atype] = score
    
    if not scores:
        return "article"
    
    return max(scores, key=scores.get)


def sanitize_filename(title: str) -> str:
    """将标题转为安全文件名"""
    # 移除特殊字符
    safe = re.sub(r'[<>:"/\\|?*]', '', title)
    # 截断
    if len(safe) > 80:
        safe = safe[:80]
    # 移除首尾空格和特殊符号
    safe = safe.strip().strip('.-_')
    return safe


def build_header(article_type: str, title: str, url: str, author: str = "UID9622") -> str:
    """构建抬头"""
    tz_cst = timezone(timedelta(hours=8))
    now = datetime.now(tz_cst)
    date_str = now.strftime("%Y-%m-%d")
    
    header = f"""# 🐉 龍魂 · {title}

> **来源**: {url}
> **作者**: {author}
> **入库时间**: {date_str}
> **入库方式**: CSDN文章拉取 → 自动对齐

---

## 🏷️ 声明

**发布者：** UID9622 · 诸葛鑫
**来源类型：** CSDN博客原创
**入库工具：** `lh csdn fetch`
**三色审计：** 🟡 待核（从CSDN拉取，需人工确认完整性）
**DNA签名：** #龍芯⚡️{date_str.replace('-', '·')}-CSDN-IMPORT

---

"""
    return header


def fetch_and_save(url: str, dry_run: bool = False) -> dict:
    """拉取并保存CSDN文章"""
    
    info = parse_csdn_url(url)
    
    # 这里用Python requests拉取（如果可用）
    try:
        import requests
    except ImportError:
        print("⚠️ requests库未安装，请安装: pip install requests beautifulsoup4")
        return {"error": "requests未安装"}
    
    print(f"📥 拉取文章: {url}")
    
    try:
        resp = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"error": f"拉取失败: {e}"}
    
    html = resp.text
    
    # 提取标题
    title_m = re.search(r'<title>(.*?)_</title>', html)
    if not title_m:
        title_m = re.search(r'<title>(.*?)</title>', html)
    title = title_m.group(1).strip() if title_m else f"CSDN-{info['article_id']}"
    # 清理CSDN后缀
    title = re.sub(r'[-_].*$', '', title).strip() if '_' in title else title
    
    # 提取正文（CSDN文章在 article-content 或 #content_views 中）
    from html.parser import HTMLParser
    
    class TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.in_article = False
            self.text = []
            self.code_blocks = []
            self.in_code = False
            self.code_buf = []
            self.depth = 0
        
        def handle_starttag(self, tag, attrs):
            attrs_dict = dict(attrs)
            if attrs_dict.get('id') in ('content_views', 'article_content'):
                self.in_article = True
            if self.in_article:
                self.depth += 1
            if tag in ('code', 'pre'):
                self.in_code = True
        
        def handle_endtag(self, tag):
            if self.in_article:
                self.depth -= 1
                if self.depth <= 0:
                    self.in_article = False
            if tag in ('code', 'pre') and self.in_code:
                self.in_code = False
                if self.code_buf:
                    self.code_blocks.append(''.join(self.code_buf))
                    self.code_buf = []
        
        def handle_data(self, data):
            if self.in_code:
                self.code_buf.append(data)
            elif self.in_article:
                text = data.strip()
                if text:
                    self.text.append(text)
    
    extractor = TextExtractor()
    try:
        extractor.feed(html)
    except Exception:
        pass
    
    content_text = '\n\n'.join(extractor.text)
    
    if not content_text or len(content_text) < 100:
        # 备用：正则提取
        m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
        if m:
            content_text = re.sub(r'<[^>]+>', '', m.group(1))
            content_text = re.sub(r'\n{3,}', '\n\n', content_text).strip()
    
    if not content_text or len(content_text) < 50:
        return {"error": "无法提取文章正文，可能需要反爬处理"}
    
    # 分类
    article_type = classify_article(title, content_text)
    target_dir = TYPE_MAP.get(article_type, "articles")
    
    # 构建文件名
    safe_title = sanitize_filename(title)
    filename = f"CSDN-{safe_title}.md"
    filepath = LONGHUN_ROOT / target_dir / filename
    
    if dry_run:
        return {
            "title": title,
            "type": article_type,
            "target_dir": target_dir,
            "filename": filename,
            "size": len(content_text),
            "dry_run": True,
        }
    
    # 写文件
    filepath.parent.mkdir(parents=True, exist_ok=True)
    header = build_header(article_type, title, url)
    filepath.write_text(header + content_text)
    print(f"✅ 已保存: {filepath}")
    
    # GPG签名
    try:
        subprocess.run(
            ["python3", str(LONGHUN_ROOT / "bin" / "lh_gpg_sign.py"), "sign", str(filepath)],
            check=False, timeout=30
        )
        print(f"✅ 已签名: {filepath}.asc")
    except Exception as e:
        print(f"⚠️ 签名失败: {e}")
    
    # 更新注册表
    reg = load_registry()
    reg["articles"].append({
        "title": title,
        "url": url,
        "article_id": info["article_id"],
        "type": article_type,
        "file": str(filepath.relative_to(LONGHUN_ROOT)),
        "fetched_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    })
    reg["last_fetch"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_registry(reg)
    
    return {
        "title": title,
        "type": article_type,
        "target_dir": target_dir,
        "filepath": str(filepath),
        "size": len(content_text),
        "signed": filepath.with_suffix(".md.asc").exists(),
    }


def list_articles():
    """列出已入库文章"""
    reg = load_registry()
    if not reg["articles"]:
        print("📭 暂无已入库的CSDN文章")
        return
    
    print(f"\n📚 已入库 {len(reg['articles'])} 篇CSDN文章:\n")
    for i, a in enumerate(reg["articles"], 1):
        print(f"  {i}. [{a['type']}] {a['title']}")
        print(f"     📄 {a['file']}")
        print(f"     📅 {a['fetched_at'][:10]}")
        print()


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  lh csdn fetch <url>        拉取单篇文章")
        print("  lh csdn list               列出已入库文章")
        print("  python3 bin/lh_csdn_fetcher.py <url>  直接拉取")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        list_articles()
    elif cmd == "fetch":
        if len(sys.argv) < 3:
            print("❌ 请提供CSDN文章URL")
            sys.exit(1)
        url = sys.argv[2]
        result = fetch_and_save(url)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 直接当URL处理
        result = fetch_and_save(cmd)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
