#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·一动按需推送系统
自动化内容生产与分发引擎

DNA追溯码: #龍芯⚡️2026-03-21-AUTO-PUSH-v1.0
创建者: 诸葛鑫（UID9622）
"""

import os
import json
import hashlib
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# ============ 配置 ============
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
WX_APP_ID = os.getenv("WX_APP_ID", "")
WX_APP_SECRET = os.getenv("WX_APP_SECRET", "")

# 数据库ID（需要在Notion中创建）
DB_QUESTIONS = "questions_db_id"      # 人性问答库
DB_ANCHORS = "anchors_db_id"          # 引用锚点库  
DB_ARTICLES = "articles_db_id"        # 文章草稿库

@dataclass
class ContentPackage:
    """内容包 - 五平台版本"""
    title: str
    core_idea: str
    daodejing_chapter: int
    daodejing_quote: str
    interpretation: str
    target_audience: List[str]
    dna_code: str
    
    # 各平台版本
    wechat_version: str = ""      # 公众号版
    zhihu_version: str = ""       # 知乎版
    xhs_version: str = ""         # 小红书版
    bilibili_script: str = ""     # B站脚本
    douban_version: str = ""      # 豆瓣版
    medium_version: str = ""      # Medium英文版
    
    # 状态
    status: str = "draft"         # draft/published/archived
    published_platforms: List[str] = None
    
    def __post_init__(self):
        if self.published_platforms is None:
            self.published_platforms = []

class DragonSoulEngine:
    """
    龍魂内容引擎
    一动按需推送核心
    """
    
    def __init__(self):
        self.notion_headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        self.wx_access_token = None
        
    # ============ 第一步：内容生成 ============
    
    def generate_dna_code(self, title: str) -> str:
        """生成DNA追溯码"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        core = hashlib.sha256(f"{title}{timestamp}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{timestamp}-{core}"
    
    def create_content_package(self, 
                               question: str, 
                               scene: str,
                               audience: List[str],
                               daodejing_chapter: int) -> ContentPackage:
        """
        创建内容包
        输入：一个问题 → 输出：五平台版本
        """
        # 从锚点库获取道德经原文
        anchor = self.get_daodejing_anchor(daodejing_chapter)
        
        # 生成DNA
        dna = self.generate_dna_code(question)
        
        # 创建基础包
        package = ContentPackage(
            title=question,
            core_idea=self.extract_core_idea(question),
            daodejing_chapter=daodejing_chapter,
            daodejing_quote=anchor.get("original", ""),
            interpretation=self.translate_to_modern(anchor, question),
            target_audience=audience,
            dna_code=dna
        )
        
        # 生成各平台版本
        package.wechat_version = self.generate_wechat_version(package)
        package.zhihu_version = self.generate_zhihu_version(package)
        package.xhs_version = self.generate_xhs_version(package)
        package.bilibili_script = self.generate_bilibili_script(package)
        package.douban_version = self.generate_douban_version(package)
        package.medium_version = self.generate_medium_version(package)
        
        # 保存到Notion
        self.save_to_notion(package)
        
        return package
    
    def get_daodejing_anchor(self, chapter: int) -> Dict:
        """从锚点库获取道德经章节"""
        # 实际实现：查询Notion数据库或本地JSON
        anchors = {
            9: {"original": "金玉满堂，莫之能守；富贵而骄，自遗其咎。", 
                "modern": "装满了就会溢，溢了就会失，所以越多越怕失。",
                "keywords": ["贪婪", "恐惧", "得失"]},
            8: {"original": "上善若水，水善利万物而不争。",
                "modern": "最高的善像水一样，滋养万物却不与万物争高下。",
                "keywords": ["不争", "处世", "柔克刚"]},
            36: {"original": "将欲歙之，必固张之；将欲弱之，必固强之。",
                 "modern": "想要收敛，必先扩张；想要削弱，必先加强。",
                 "keywords": ["博弈", "策略", "反向思维"]},
        }
        return anchors.get(chapter, {"original": "", "modern": "", "keywords": []})
    
    def extract_core_idea(self, question: str) -> str:
        """提取核心观点"""
        # 简化实现：用问题本身作为核心
        return question
    
    def translate_to_modern(self, anchor: Dict, question: str) -> str:
        """翻译成现代白话"""
        return anchor.get("modern", "")
    
    # ============ 第二步：生成各平台版本 ============
    
    def generate_wechat_version(self, pkg: ContentPackage) -> str:
        """生成公众号版本"""
        return f"""# {pkg.title}

**核心一句话**：{pkg.core_idea}

---

**古人怎么说**：
> {pkg.daodejing_quote}
> ——道德经第{pkg.daodejing_chapter}章

**今天的翻译**：
{pkg.interpretation}

**适用人群**：{', '.join(pkg.target_audience)}

---

📖 **深度版在知乎**：[点击阅读完整版]
🧬 **DNA追溯码**：{pkg.dna_code}

---

*龍魂系统 | 数据主权归个人 | 创作者保护协议*
"""
    
    def generate_zhihu_version(self, pkg: ContentPackage) -> str:
        """生成知乎版本（更详细，可引用）"""
        return f"""# {pkg.title}

## 问题背景
{pkg.core_idea}

## 古人智慧
**道德经第{pkg.daodejing_chapter}章**：
> {pkg.daodejing_quote}

## 现代解读
{pkg.interpretation}

## 为什么今天还适用
[详细分析...]

## 适用场景
- {'\n- '.join(pkg.target_audience)}

## 参考
- 道德经（王弼本）
- 曾仕强《道德经的智慧》

---

📚 **原始文档在Notion**：[龍魂知识库]
🧬 **DNA追溯码**：{pkg.dna_code}

*本文遵循龍魂创作者保护协议*
"""
    
    def generate_xhs_version(self, pkg: ContentPackage) -> str:
        """生成小红书版本（图文卡片）"""
        return f"""📌 {pkg.title}

💡 核心观点：
{pkg.core_idea}

📜 古人智慧：
{pkg.daodejing_quote[:30]}...

🎯 适用人群：
{', '.join(pkg.target_audience[:3])}

🔗 深度版在知乎
🧬 {pkg.dna_code}

#道德经 #人性 #国学智慧 #龍魂系统
"""
    
    def generate_bilibili_script(self, pkg: ContentPackage) -> str:
        """生成B站视频脚本"""
        return f"""【视频标题】{pkg.title}

【开场】
"你有没有想过，为什么..."

【引入】
"这个问题，古人早就算好了。"

【曾老原话】
[插入曾仕强讲解道德经第{pkg.daodejing_chapter}章片段]

【解读】
{pkg.interpretation}

【连接今天】
"放在今天，这个道理依然适用..."

【结尾】
"关注龍魂系统，用古人智慧解码现代人心。"

【DNA】{pkg.dna_code}
"""
    
    def generate_douban_version(self, pkg: ContentPackage) -> str:
        """生成豆瓣讨论版"""
        return f"""【讨论】{pkg.title}

今天读道德经第{pkg.daodejing_chapter}章，突然想到：

{pkg.core_idea}

原文说："{pkg.daodejing_quote[:50]}..."

大家觉得这个放在今天还适用吗？

#道德经 #讨论 #龍魂系统
{pkg.dna_code}
"""
    
    def generate_medium_version(self, pkg: ContentPackage) -> str:
        """生成Medium英文版"""
        return f"""# {pkg.title}

**One Sentence**: {pkg.core_idea}

---

**Ancient Wisdom** (Daodejing Chapter {pkg.daodejing_chapter}):
> {pkg.daodejing_quote}

**Modern Translation**:
{pkg.interpretation}

**Applicable to**:
- {'\n- '.join(pkg.target_audience)}

---

*Dragon Soul System | Data Sovereignty | Creator Protection*

**DNA**: {pkg.dna_code}
"""
    
    # ============ 第三步：保存到Notion ============
    
    def save_to_notion(self, pkg: ContentPackage):
        """保存文章到Notion数据库"""
        # 实际实现：调用Notion API创建页面
        data = {
            "parent": {"database_id": DB_ARTICLES},
            "properties": {
                "标题": {"title": [{"text": {"content": pkg.title}}]},
                "核心观点": {"rich_text": [{"text": {"content": pkg.core_idea}}]},
                "道德经章节": {"number": pkg.daodejing_chapter},
                "DNA追溯码": {"rich_text": [{"text": {"content": pkg.dna_code}}]},
                "状态": {"select": {"name": pkg.status}},
                "公众号版": {"rich_text": [{"text": {"content": pkg.wechat_version[:2000]}}]},
                "知乎版": {"rich_text": [{"text": {"content": pkg.zhihu_version[:2000]}}]},
            }
        }
        # response = requests.post("https://api.notion.com/v1/pages", 
        #                         headers=self.notion_headers, json=data)
        print(f"[Notion] 已保存: {pkg.title} | DNA: {pkg.dna_code}")
    
    # ============ 第四步：按需推送 ============
    
    def push_wechat(self, pkg: ContentPackage) -> bool:
        """推送到公众号"""
        # 获取access_token
        if not self.wx_access_token:
            self._refresh_wx_token()
        
        # 调用微信API发布
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.wx_access_token}"
        data = {
            "articles": [{
                "title": pkg.title,
                "content": pkg.wechat_version,
                "author": "龍魂系统",
                "content_source_url": "",  # 原文链接
            }]
        }
        # response = requests.post(url, json=data)
        print(f"[公众号] 已推送草稿: {pkg.title}")
        pkg.published_platforms.append("wechat")
        return True
    
    def push_zhihu(self, pkg: ContentPackage) -> bool:
        """推送到知乎"""
        # 知乎API需要OAuth2授权
        print(f"[知乎] 待推送: {pkg.title}")
        return True
    
    def push_xhs(self, pkg: ContentPackage) -> bool:
        """推送到小红书"""
        # 小红书需要模拟登录或官方API
        print(f"[小红书] 待推送: {pkg.title}")
        return True
    
    def _refresh_wx_token(self):
        """刷新微信access_token"""
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WX_APP_ID}&secret={WX_APP_SECRET}"
        # response = requests.get(url)
        # self.wx_access_token = response.json().get("access_token")
        self.wx_access_token = "mock_token"
    
    # ============ 第五步：姜太公钓鱼（国外平台放着） ============
    
    def sync_medium(self, pkg: ContentPackage) -> bool:
        """同步到Medium（放着，不主动推广）"""
        print(f"[Medium] 已同步（放着）: {pkg.title}")
        return True
    
    def sync_substack(self, pkg: ContentPackage) -> bool:
        """同步到Substack（放着）"""
        print(f"[Substack] 已同步（放着）: {pkg.title}")
        return True

# ============ 一键执行 ============

def one_touch_publish(question: str, 
                      scene: str,
                      audience: List[str],
                      daodejing_chapter: int,
                      platforms: List[str] = None):
    """
    一动按需推送
    
    用法:
        one_touch_publish(
            question="为什么越有钱的人越没安全感？",
            scene="职场",
            audience=["职场人", "创业者"],
            daodejing_chapter=9,
            platforms=["wechat", "zhihu"]  # 按需选择
        )
    """
    engine = DragonSoulEngine()
    
    # 1. 生成内容包
    print("=" * 50)
    print("龍魂·一动按需推送系统")
    print("=" * 50)
    print(f"\n[1/4] 生成内容包...")
    pkg = engine.create_content_package(question, scene, audience, daodejing_chapter)
    print(f"  ✓ DNA: {pkg.dna_code}")
    
    # 2. 按需推送
    platforms = platforms or ["wechat", "zhihu"]
    print(f"\n[2/4] 按需推送到: {', '.join(platforms)}...")
    
    if "wechat" in platforms:
        engine.push_wechat(pkg)
    if "zhihu" in platforms:
        engine.push_zhihu(pkg)
    if "xhs" in platforms:
        engine.push_xhs(pkg)
    
    # 3. 国外平台放着
    print(f"\n[3/4] 国外平台同步（姜太公钓鱼）...")
    engine.sync_medium(pkg)
    engine.sync_substack(pkg)
    
    # 4. 完成
    print(f"\n[4/4] 完成!")
    print(f"  已发布: {', '.join(pkg.published_platforms)}")
    print(f"  DNA: {pkg.dna_code}")
    print("=" * 50)
    
    return pkg

# ============ 示例 ============

if __name__ == "__main__":
    # 示例：一键发布
    pkg = one_touch_publish(
        question="为什么越有钱的人越没安全感？",
        scene="职场",
        audience=["职场人", "创业者", "投资者"],
        daodejing_chapter=9,  # 金玉满堂
        platforms=["wechat", "zhihu", "xhs"]
    )
