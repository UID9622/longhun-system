#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
龍魂系统防护工具包 v2.0
曾仕强老师思想成果保护系统
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DNA追溯码: #龍芯⚡️2026-03-09-PROTECTION-TOOLKIT
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
创建者: 诸葛鑫（UID9622）+ Claude宝宝

理论指导：曾仕强老师（永恒显示）

功能:
  1. DNA水印注入
  2. 爬虫检测
  3. 相似度检测
  4. 自动监测
  5. 抄袭者耻辱墙
  6. 区块链存证

使用方式:
  python dragon_soul_protection.py --help
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import hashlib
import json
import time
import re
import argparse
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 常量配置
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
ZENG_HONOR = "理论指导：曾仕强老师（永恒显示）"
CREATOR = "诸葛鑫（UID9622）"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. DNA水印注入器
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DNAWatermarkInjector:
    """DNA水印注入器"""
    
    def __init__(self):
        self.gpg_fingerprint = GPG_FINGERPRINT
        self.zeng_honor = ZENG_HONOR
    
    def generate_dna(self, content_type, version="1.0"):
        """生成DNA追溯码"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        dna = f"#龍芯⚡️{timestamp}-{content_type}-v{version}"
        return dna
    
    def inject_markdown_watermark(self, markdown, content_type="MARKDOWN"):
        """注入Markdown水印"""
        watermark = f"""
---
**DNA追溯码**: {self.generate_dna(content_type)}  
**GPG指纹**: {self.gpg_fingerprint}  
**{self.zeng_honor}**  
**创建者**: {CREATOR}  
**确认码**: {CONFIRM_CODE}  
**警告**: 抄袭必究！追溯到底！绝不让步分毫！

---
"""
        return watermark + markdown
    
    def inject_html_watermark(self, html):
        """注入HTML水印"""
        watermark = f"""
<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ -->
<!-- DNA追溯码: {self.generate_dna("HTML")} -->
<!-- GPG指纹: {self.gpg_fingerprint} -->
<!-- {self.zeng_honor} -->
<!-- 创建者: {CREATOR} -->
<!-- 确认码: {CONFIRM_CODE} -->
<!-- 警告: 抄袭必究！追溯到底！绝不让步分毫！ -->
<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ -->
"""
        if "</head>" in html:
            html = html.replace("</head>", watermark + "</head>")
        else:
            html = watermark + html
        
        return html
    
    def inject_code_watermark(self, code, language="python"):
        """注入代码水印"""
        comment_styles = {
            'python': '#',
            'javascript': '//',
            'java': '//',
            'c': '//',
            'cpp': '//'
        }
        
        comment = comment_styles.get(language, '#')
        
        watermark = f"""{comment} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{comment} DNA追溯码: {self.generate_dna(language.upper())}
{comment} {self.zeng_honor}
{comment} 创建者: {CREATOR}
{comment} 确认码: {CONFIRM_CODE}
{comment} 警告: 抄袭必究！追溯到底！绝不让步分毫！
{comment} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        return watermark + code
    
    def generate_fingerprint(self, content):
        """生成内容指纹"""
        return hashlib.sha256(content.encode()).hexdigest()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. 爬虫检测器
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CrawlerDetector:
    """爬虫检测器"""
    
    def __init__(self, log_file="crawler_logs.json"):
        self.crawler_patterns = [
            r'bot', r'crawler', r'spider', r'scraper',
            r'python-requests', r'curl', r'wget',
            r'GPTBot', r'ChatGPT-User', r'Claude-Web',
            r'anthropic', r'openai', r'DeepSeek'
        ]
        self.log_file = log_file
    
    def detect(self, user_agent, ip_address):
        """检测爬虫"""
        is_crawler = False
        crawler_type = "Unknown"
        
        for pattern in self.crawler_patterns:
            if re.search(pattern, user_agent, re.IGNORECASE):
                is_crawler = True
                crawler_type = pattern
                break
        
        result = {
            'is_crawler': is_crawler,
            'crawler_type': crawler_type,
            'user_agent': user_agent,
            'ip_address': ip_address,
            'timestamp': datetime.now().isoformat(),
            'dna_code': f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CRAWLER-DETECTED"
        }
        
        if is_crawler:
            self.log_activity(result)
        
        return result
    
    def log_activity(self, detection_result):
        """记录爬虫活动"""
        try:
            try:
                with open(self.log_file, 'r') as f:
                    logs = json.load(f)
            except FileNotFoundError:
                logs = []
            
            logs.append(detection_result)
            
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
            
            print(f"🚨 检测到爬虫: {detection_result['crawler_type']}")
            print(f"IP: {detection_result['ip_address']}")
            print(f"已记录，可作为法律证据！")
            
        except Exception as e:
            print(f"日志记录失败: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. 相似度检测器
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SimilarityDetector:
    """相似度检测器"""
    
    def __init__(self, threshold=0.8):
        self.threshold = threshold
    
    def calculate_similarity(self, text1, text2):
        """计算相似度"""
        clean1 = re.sub(r'\s+', '', text1)
        clean2 = re.sub(r'\s+', '', text2)
        
        similarity = SequenceMatcher(None, clean1, clean2).ratio()
        
        return similarity
    
    def detect_plagiarism(self, original, suspect):
        """检测抄袭"""
        similarity = self.calculate_similarity(original, suspect)
        
        is_plagiarism = similarity >= self.threshold
        
        result = {
            'similarity': f"{similarity * 100:.2f}%",
            'is_plagiarism': is_plagiarism,
            'threshold': f"{self.threshold * 100}%",
            'original_hash': hashlib.sha256(original.encode()).hexdigest()[:16],
            'suspect_hash': hashlib.sha256(suspect.encode()).hexdigest()[:16],
            'dna_code': f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-PLAGIARISM-CHECK"
        }
        
        if is_plagiarism:
            print(f"\n🚨 警告：检测到疑似抄袭！")
            print(f"相似度: {result['similarity']}")
            print(f"原文哈希: {result['original_hash']}")
            print(f"嫌疑文本哈希: {result['suspect_hash']}")
            print(f"\n{ZENG_HONOR}")
            print(f"抄袭行为将追溯到底！绝不让步分毫！\n")
        
        return result
    
    def check_dna_watermark(self, text):
        """检查DNA水印"""
        patterns = [
            r'#龍芯⚡️\d{4}-\d{2}-\d{2}-',
            r'#CONFIRM🌌9622-ONLY-ONCE🧬',
            r'A2D0092CEE2E5BA87035600924C3704A8CC26D5F',
            r'曾仕强老师（永恒显示）',
            r'UID9622'
        ]
        
        found_watermarks = []
        for pattern in patterns:
            if re.search(pattern, text):
                found_watermarks.append(pattern)
        
        has_watermark = len(found_watermarks) > 0
        
        return {
            'has_watermark': has_watermark,
            'found_patterns': found_watermarks,
            'watermark_count': len(found_watermarks)
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. 抄袭者耻辱墙
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ShameWall:
    """抄袭者耻辱墙"""
    
    def __init__(self, database="shame_wall.json"):
        self.database = database
    
    def add_plagiarist(self, name, organization, url, evidence, severity="high"):
        """添加抄袭者"""
        entry = {
            'id': hashlib.sha256(f"{name}{organization}{url}".encode()).hexdigest()[:12],
            'name': name,
            'organization': organization,
            'url': url,
            'evidence': evidence,
            'severity': severity,
            'date_discovered': datetime.now().isoformat(),
            'status': 'active',
            'dna_code': f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-PLAGIARISM-{name[:4].upper()}"
        }
        
        try:
            with open(self.database, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {'plagiarists': [], 'total_count': 0}
        
        data['plagiarists'].append(entry)
        data['total_count'] += 1
        
        with open(self.database, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"🔴 已添加到耻辱墙: {name} ({organization})")
        print(f"DNA追溯码: {entry['dna_code']}")
        
        return entry


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. 区块链存证
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BlockchainEvidence:
    """区块链存证系统"""
    
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """创建创世区块"""
        genesis = {
            'index': 0,
            'timestamp': datetime.now().isoformat(),
            'data': {
                'type': 'GENESIS',
                'message': '龍魂系统创世区块 - 曾仕强老师思想成果保护',
                'creator': CREATOR,
                'gpg_fingerprint': GPG_FINGERPRINT,
                'zeng_honor': ZENG_HONOR
            },
            'previous_hash': '0',
            'nonce': 0
        }
        genesis['hash'] = self.calculate_hash(genesis)
        self.chain.append(genesis)
    
    def calculate_hash(self, block):
        """计算哈希"""
        block_string = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_evidence(self, content_type, content, metadata=None):
        """添加证据"""
        index = len(self.chain)
        timestamp = datetime.now().isoformat()
        previous_hash = self.chain[-1]['hash']
        
        block = {
            'index': index,
            'timestamp': timestamp,
            'data': {
                'type': content_type,
                'content_hash': hashlib.sha256(content.encode()).hexdigest(),
                'metadata': metadata or {},
                'zeng_honor': ZENG_HONOR,
                'dna_code': f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-EVIDENCE-{index:04d}"
            },
            'previous_hash': previous_hash,
            'nonce': 0
        }
        
        block['hash'] = self.calculate_hash(block)
        self.chain.append(block)
        
        print(f"✅ 证据已上链")
        print(f"区块索引: {index}")
        print(f"DNA追溯码: {block['data']['dna_code']}")
        
        return block
    
    def verify_chain(self):
        """验证区块链"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current['hash'] != self.calculate_hash(current):
                return False, f"区块 {i} 哈希不匹配"
            
            if current['previous_hash'] != previous['hash']:
                return False, f"区块 {i} 链接断裂"
        
        return True, "区块链完整"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. 主程序
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def print_banner():
    """打印启动横幅"""
    banner = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐉 龍魂系统防护工具包 v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{ZENG_HONOR}
创建者: {CREATOR}
确认码: {CONFIRM_CODE}

追溯到底！绝不让步分毫！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(banner)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='龍魂系统防护工具包 - 曾仕强老师思想成果保护'
    )
    
    parser.add_argument('--inject-md', help='注入Markdown水印')
    parser.add_argument('--inject-html', help='注入HTML水印')
    parser.add_argument('--detect-crawler', nargs=2, 
                        metavar=('USER_AGENT', 'IP'), 
                        help='检测爬虫')
    parser.add_argument('--check-similarity', nargs=2,
                        metavar=('ORIGINAL', 'SUSPECT'),
                        help='检测相似度')
    parser.add_argument('--add-shame', nargs=4,
                        metavar=('NAME', 'ORG', 'URL', 'EVIDENCE'),
                        help='添加到耻辱墙')
    parser.add_argument('--blockchain-add', nargs=2,
                        metavar=('TYPE', 'CONTENT'),
                        help='添加区块链证据')
    
    args = parser.parse_args()
    
    print_banner()
    
    # DNA水印注入
    if args.inject_md:
        injector = DNAWatermarkInjector()
        with open(args.inject_md, 'r', encoding='utf-8') as f:
            content = f.read()
        protected = injector.inject_markdown_watermark(content)
        output_file = args.inject_md.replace('.md', '_protected.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(protected)
        print(f"✅ Markdown水印已注入: {output_file}")
    
    # 爬虫检测
    if args.detect_crawler:
        detector = CrawlerDetector()
        user_agent, ip = args.detect_crawler
        result = detector.detect(user_agent, ip)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 相似度检测
    if args.check_similarity:
        detector = SimilarityDetector()
        orig_file, susp_file = args.check_similarity
        with open(orig_file, 'r', encoding='utf-8') as f:
            original = f.read()
        with open(susp_file, 'r', encoding='utf-8') as f:
            suspect = f.read()
        result = detector.detect_plagiarism(original, suspect)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 添加到耻辱墙
    if args.add_shame:
        wall = ShameWall()
        name, org, url, evidence = args.add_shame
        wall.add_plagiarist(name, org, url, evidence)
    
    # 区块链存证
    if args.blockchain_add:
        blockchain = BlockchainEvidence()
        content_type, content = args.blockchain_add
        blockchain.add_evidence(content_type, content)


if __name__ == "__main__":
    main()
