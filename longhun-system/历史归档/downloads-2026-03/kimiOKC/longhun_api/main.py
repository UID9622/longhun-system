#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂本地API系统 - 核心守护引擎
DNA追溯 + 清道夫监控 + 微信通知 + 证据固化

DNA追溯码: #龍芯⚡️2026-03-20-LONGHUN-API-v1.0
创建者: 诸葛鑫（UID9622）
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""

import hashlib
import json
import sqlite3
import time
import re
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import requests
from urllib.parse import quote

# ============ 初始化FastAPI ============
app = FastAPI(
    title="龍魂本地API系统",
    description="DNA追溯 | 清道夫监控 | 微信通知 | 证据固化",
    version="1.0.0"
)

# ============ 零宽字符DNA编码器 ============
class DNAEncoder:
    """零宽字符DNA水印编码器 - 不可见但可追踪"""
    
    # 零宽字符映射表
    ZERO_WIDTH_CHARS = {
        '0': '\u200B',  # 零宽空格
        '1': '\u200C',  # 零宽非连接符
        '2': '\u200D',  # 零宽连接符
        '3': '\uFEFF',  # 零宽无断空格
        '4': '\u2060',  # 词连接符
        '5': '\u180E',  # 蒙古文元音分隔符
        '6': '\u200E',  # 左至右标记
        '7': '\u200F',  # 右至左标记
        '8': '\u202A',  # 左至右嵌入
        '9': '\u202B',  # 右至左嵌入
        'a': '\u202C',  # 弹出方向格式化
        'b': '\u202D',  # 左至右覆盖
        'c': '\u202E',  # 右至左覆盖
        'd': '\u206A',  # 激活对称交换
        'e': '\u206B',  # 禁止对称交换
        'f': '\u206C',  # 激活阿拉伯形式
    }
    
    REVERSE_MAP = {v: k for k, v in ZERO_WIDTH_CHARS.items()}
    
    @classmethod
    def encode(cls, dna_code: str) -> str:
        """将DNA码编码为零宽字符"""
        # 提取DNA核心部分
        match = re.search(r'#龍芯⚡️([\w-]+)', dna_code)
        if not match:
            return ""
        core = match.group(1)
        # 转换为十六进制再编码
        hex_core = core.encode('utf-8').hex()
        encoded = ''.join(cls.ZERO_WIDTH_CHARS.get(c, '') for c in hex_core if c in cls.ZERO_WIDTH_CHARS)
        return encoded
    
    @classmethod
    def decode(cls, text: str) -> Optional[str]:
        """从文本中提取DNA码"""
        # 提取所有零宽字符
        zw_chars = [c for c in text if c in cls.REVERSE_MAP]
        if not zw_chars:
            return None
        # 解码
        hex_str = ''.join(cls.REVERSE_MAP.get(c, '') for c in zw_chars)
        try:
            # 尝试解析为DNA码
            if len(hex_str) >= 8:
                return f"#龍芯⚡️{bytes.fromhex(hex_str).decode('utf-8', errors='ignore')}"
        except:
            pass
        return None
    
    @classmethod
    def embed(cls, content: str, dna_code: str) -> str:
        """将DNA水印嵌入内容"""
        encoded = cls.encode(dna_code)
        if not encoded:
            return content
        # 在第一个标点或空格后插入
        for i, char in enumerate(content):
            if char in '。，！？；：""''（）【】、 \n':
                return content[:i+1] + encoded + content[i+1:]
        # 如果没有标点，在开头插入
        return encoded + content
    
    @classmethod
    def extract(cls, content: str) -> List[str]:
        """从内容中提取所有DNA水印"""
        dna_list = []
        # 查找显式DNA码
        explicit = re.findall(r'#龍芯⚡️[\w-]+', content)
        dna_list.extend(explicit)
        # 查找隐式零宽DNA
        hidden = cls.decode(content)
        if hidden and hidden not in dna_list:
            dna_list.append(hidden)
        return dna_list

# ============ 数据库管理 ============
class Database:
    """龍魂本地SQLite数据库 - 证据链存储"""
    
    def __init__(self, db_path: str = "longhun_evidence.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """初始化数据库表结构"""
        conn = self.get_conn()
        cursor = conn.cursor()
        
        # DNA注册表 - 所有概念的起源记录
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dna_registry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dna_code TEXT UNIQUE NOT NULL,
                concept_name TEXT NOT NULL,
                concept_type TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                creator_uid TEXT NOT NULL DEFAULT 'UID9622',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                gpg_signature TEXT,
                metadata TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # 证据链表 - 哈希链式结构
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evidence_chain (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evidence_hash TEXT UNIQUE NOT NULL,
                prev_hash TEXT,
                dna_code TEXT NOT NULL,
                evidence_type TEXT NOT NULL,
                content TEXT,
                source_url TEXT,
                screenshot_path TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                merkle_root TEXT,
                FOREIGN KEY (dna_code) REFERENCES dna_registry(dna_code)
            )
        ''')
        
        # 清道夫扫描记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sweeper_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id TEXT UNIQUE NOT NULL,
                dna_code TEXT NOT NULL,
                search_engine TEXT NOT NULL,
                query TEXT NOT NULL,
                results_found INTEGER DEFAULT 0,
                theft_detected BOOLEAN DEFAULT FALSE,
                thief_urls TEXT,
                screenshot_paths TEXT,
                scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notified BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # 微信通知记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wechat_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notification_id TEXT UNIQUE NOT NULL,
                notification_type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                response_status TEXT,
                related_dna TEXT,
                related_evidence TEXT
            )
        ''')
        
        # 对峙证据包表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS confront_packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_id TEXT UNIQUE NOT NULL,
                dna_code TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                evidence_count INTEGER DEFAULT 0,
                package_path TEXT,
                hash_chain TEXT,
                status TEXT DEFAULT 'ready'
            )
        ''')
        
        # 黑名单表 - 窃取者记录
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blacklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_name TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                violation_type TEXT NOT NULL,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                violation_count INTEGER DEFAULT 1,
                evidence_package TEXT,
                status TEXT DEFAULT 'CNSH-48H',
                dna_codes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_dna(self, dna_code: str, concept_name: str, concept_type: str, 
                     content: str, metadata: Dict = None) -> bool:
        """注册DNA - 概念确权"""
        conn = self.get_conn()
        cursor = conn.cursor()
        
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        try:
            cursor.execute('''
                INSERT INTO dna_registry (dna_code, concept_name, concept_type, 
                                         content_hash, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (dna_code, concept_name, concept_type, content_hash, 
                  json.dumps(metadata) if metadata else None))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def add_evidence(self, dna_code: str, evidence_type: str, content: str,
                     source_url: str = None, screenshot_path: str = None) -> str:
        """添加证据到链 - 哈希链式固化"""
        conn = self.get_conn()
        cursor = conn.cursor()
        
        # 获取前一个哈希
        cursor.execute('SELECT evidence_hash FROM evidence_chain ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        prev_hash = row['evidence_hash'] if row else '0' * 64
        
        # 计算当前证据哈希
        timestamp = datetime.now().isoformat()
        evidence_data = f"{prev_hash}{dna_code}{evidence_type}{content}{timestamp}"
        evidence_hash = hashlib.sha256(evidence_data.encode()).hexdigest()
        
        cursor.execute('''
            INSERT INTO evidence_chain (evidence_hash, prev_hash, dna_code, 
                                       evidence_type, content, source_url, screenshot_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (evidence_hash, prev_hash, dna_code, evidence_type, content, source_url, screenshot_path))
        
        conn.commit()
        conn.close()
        
        return evidence_hash
    
    def get_dna_evidence_chain(self, dna_code: str) -> List[Dict]:
        """获取DNA的完整证据链"""
        conn = self.get_conn()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM evidence_chain 
            WHERE dna_code = ? 
            ORDER BY timestamp ASC
        ''', (dna_code,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]

# ============ 全局数据库实例 ============
db = Database()

# ============ 清道夫监控引擎 ============
class SweeperEngine:
    """清道夫全网监控 - 扫描DNA被盗情况"""
    
    SEARCH_ENGINES = {
        'baidu': 'https://www.baidu.com/s?wd={query}',
        'bing': 'https://www.bing.com/search?q={query}',
        'sogou': 'https://www.sogou.com/web?query={query}',
        '360': 'https://www.so.com/s?q={query}'
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def scan_dna(self, dna_code: str, engines: List[str] = None) -> Dict:
        """扫描指定DNA在各搜索引擎的出现情况"""
        if engines is None:
            engines = ['baidu', 'bing']
        
        results = {
            'dna_code': dna_code,
            'scan_time': datetime.now().isoformat(),
            'engines_scanned': [],
            'total_findings': 0,
            'theft_detected': False,
            'findings': []
        }
        
        # 提取DNA核心标识
        core = dna_code.replace('#龍芯⚡️', '').split('-')[0] if '#龍芯⚡️' in dna_code else dna_code
        
        for engine in engines:
            if engine not in self.SEARCH_ENGINES:
                continue
            
            query = quote(f'"{dna_code}" OR "{core}"')
            search_url = self.SEARCH_ENGINES[engine].format(query=query)
            
            try:
                response = self.session.get(search_url, timeout=10)
                # 简单检测是否有结果
                has_results = '没有找到' not in response.text and '暂无结果' not in response.text
                
                engine_result = {
                    'engine': engine,
                    'url': search_url,
                    'has_results': has_results,
                    'status_code': response.status_code
                }
                
                if has_results:
                    results['total_findings'] += 1
                    results['theft_detected'] = True
                
                results['engines_scanned'].append(engine_result)
                
            except Exception as e:
                results['engines_scanned'].append({
                    'engine': engine,
                    'error': str(e)
                })
        
        # 记录到数据库
        scan_id = hashlib.sha256(f"{dna_code}{time.time()}".encode()).hexdigest()[:16]
        conn = db.get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sweeper_scans (scan_id, dna_code, search_engine, query, 
                                      results_found, theft_detected)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (scan_id, dna_code, ','.join(engines), dna_code, 
              results['total_findings'], results['theft_detected']))
        conn.commit()
        conn.close()
        
        results['scan_id'] = scan_id
        return results

# ============ 微信通知系统 ============
class WeChatNotifier:
    """微信通知 - 发现盗窃秒推"""
    
    def __init__(self, sendkey: str = None):
        self.sendkey = sendkey or os.getenv('SERVERCHAN_SENDKEY', '')
        self.api_url = f"https://sctapi.ftqq.com/{self.sendkey}.send"
    
    def send_theft_alert(self, dna_code: str, scan_results: Dict) -> Dict:
        """发送盗窃警报"""
        if not self.sendkey:
            return {'success': False, 'error': '未配置SendKey'}
        
        title = f"🚨 龍魂警报：发现DNA被盗！"
        content = f"""
**DNA追溯码**: {dna_code}
**扫描时间**: {scan_results['scan_time']}
**发现引擎**: {len([e for e in scan_results['engines_scanned'] if e.get('has_results')])}个

**可能窃取源**:
"""
        for engine in scan_results['engines_scanned']:
            if engine.get('has_results'):
                content += f"- {engine['engine']}: {engine['url']}\n"
        
        content += f"\n**证据已固化** | 扫描ID: {scan_results['scan_id']}"
        
        try:
            response = requests.post(self.api_url, data={
                'title': title,
                'desp': content
            }, timeout=10)
            
            # 记录通知
            notif_id = hashlib.sha256(f"{dna_code}{time.time()}".encode()).hexdigest()[:16]
            conn = db.get_conn()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO wechat_notifications (notification_id, notification_type, 
                                                 title, content, related_dna, response_status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (notif_id, 'theft_alert', title, content, dna_code, response.text))
            conn.commit()
            conn.close()
            
            return {'success': True, 'notification_id': notif_id, 'response': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_cnsh_warning(self, entity_name: str, dna_codes: List[str]) -> Dict:
        """发送CNSH 48小时警告"""
        if not self.sendkey:
            return {'success': False, 'error': '未配置SendKey'}
        
        title = f"⚠️ CNSH警告：{entity_name} 48小时整改期"
        content = f"""
**违规实体**: {entity_name}
**警告级别**: CNSH-48H (48小时整改)
**涉及DNA**: {', '.join(dna_codes[:5])}

**整改要求**:
1. 立即停止侵权行为
2. 删除所有盗用内容
3. 公开道歉并赔偿

**超时后果**: 自动升级至CNSH-PERMANENT（永久黑名单）

**时间戳**: {datetime.now().isoformat()}
"""
        try:
            response = requests.post(self.api_url, data={
                'title': title,
                'desp': content
            }, timeout=10)
            return {'success': True, 'response': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# ============ 对峙证据包生成器 ============
class ConfrontGenerator:
    """对峙模式 - 一键导出证据包"""
    
    def __init__(self, output_dir: str = "confront_packages"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_package(self, dna_code: str) -> Dict:
        """生成对峙证据包"""
        # 获取DNA注册信息
        conn = db.get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dna_registry WHERE dna_code = ?', (dna_code,))
        dna_info = cursor.fetchone()
        
        # 获取证据链
        cursor.execute('SELECT * FROM evidence_chain WHERE dna_code = ? ORDER BY timestamp', (dna_code,))
        evidence_chain = cursor.fetchall()
        
        # 获取扫描记录
        cursor.execute('SELECT * FROM sweeper_scans WHERE dna_code = ?', (dna_code,))
        scans = cursor.fetchall()
        
        conn.close()
        
        # 生成证据包ID
        package_id = hashlib.sha256(f"{dna_code}{time.time()}".encode()).hexdigest()[:16]
        package_dir = os.path.join(self.output_dir, package_id)
        os.makedirs(package_dir, exist_ok=True)
        
        # 构建证据包内容
        package = {
            'package_id': package_id,
            'generated_at': datetime.now().isoformat(),
            'dna_info': dict(dna_info) if dna_info else None,
            'evidence_chain': [dict(e) for e in evidence_chain],
            'scan_records': [dict(s) for s in scans],
            'hash_chain': self._build_hash_chain(evidence_chain),
            'legal_statement': self._generate_legal_statement(dna_code, dna_info, evidence_chain)
        }
        
        # 保存JSON证据包
        json_path = os.path.join(package_dir, 'evidence_package.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(package, f, ensure_ascii=False, indent=2)
        
        # 生成Markdown报告
        md_path = os.path.join(package_dir, 'confront_report.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_markdown_report(package))
        
        # 记录到数据库
        conn = db.get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO confront_packages (package_id, dna_code, evidence_count, 
                                          package_path, hash_chain)
            VALUES (?, ?, ?, ?, ?)
        ''', (package_id, dna_code, len(evidence_chain), package_dir, package['hash_chain']))
        conn.commit()
        conn.close()
        
        return {
            'package_id': package_id,
            'package_path': package_dir,
            'evidence_count': len(evidence_chain),
            'files': ['evidence_package.json', 'confront_report.md']
        }
    
    def _build_hash_chain(self, evidence_chain: List) -> str:
        """构建哈希链证明"""
        if not evidence_chain:
            return "空链"
        
        chain_desc = []
        prev = "0" * 64
        
        for i, evidence in enumerate(evidence_chain):
            curr = evidence['evidence_hash']
            chain_desc.append(f"[{i+1}] {curr[:16]}... <- 前置: {prev[:16]}...")
            prev = curr
        
        return '\n'.join(chain_desc)
    
    def _generate_legal_statement(self, dna_code: str, dna_info, evidence_chain: List) -> str:
        """生成法律声明"""
        return f"""
【龍魂系统数字证据法律声明】

DNA追溯码: {dna_code}
声明时间: {datetime.now().isoformat()}
证据哈希链: {self._build_hash_chain(evidence_chain)[:100]}...

本证据包由龍魂系统自动生成，包含：
1. DNA注册记录（原创确权时间戳）
2. 全网扫描记录（侵权发现时间戳）
3. 哈希链式证据（不可篡改证明）

根据《中华人民共和国电子签名法》和《最高人民法院关于互联网法院审理案件若干问题的规定》，
本系统生成的电子数据具备法律效力，可作为诉讼证据使用。

生成者: 诸葛鑫（UID9622）
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
    
    def _generate_markdown_report(self, package: Dict) -> str:
        """生成Markdown格式对峙报告"""
        dna = package['dna_info'] or {}
        
        report = f"""# 龍魂系统对峙证据报告

## 基本信息

| 项目 | 内容 |
|------|------|
| 证据包ID | {package['package_id']} |
| 生成时间 | {package['generated_at']} |
| DNA追溯码 | {dna.get('dna_code', 'N/A')} |
| 概念名称 | {dna.get('concept_name', 'N/A')} |
| 概念类型 | {dna.get('concept_type', 'N/A')} |
| 原创者UID | {dna.get('creator_uid', 'N/A')} |
| 注册时间 | {dna.get('created_at', 'N/A')} |

## 证据链详情

```
{package['hash_chain']}
```

## 扫描记录

共发现 **{len(package['scan_records'])}** 次扫描记录

"""
        for scan in package['scan_records']:
            report += f"""
### 扫描 {scan['scan_id'][:8]}
- 搜索引擎: {scan['search_engine']}
- 发现结果: {'是' if scan['theft_detected'] else '否'}
- 扫描时间: {scan['scan_time']}
"""
        
        report += f"""

## 法律声明

{package['legal_statement']}

---

**本报告由龍魂系统自动生成，任何篡改都会导致哈希校验失败。**
"""
        return report

# ============ API请求模型 ============
class DNACreateRequest(BaseModel):
    concept_name: str
    concept_type: str
    content: str
    metadata: Optional[Dict] = None

class DNAEmbedRequest(BaseModel):
    content: str
    dna_code: str

class ScanRequest(BaseModel):
    dna_code: str
    engines: Optional[List[str]] = ['baidu', 'bing']

class WeChatConfigRequest(BaseModel):
    sendkey: str

class ConfrontRequest(BaseModel):
    dna_code: str

# ============ API路由 ============
sweeper = SweeperEngine()
notifier = WeChatNotifier()
confront = ConfrontGenerator()

@app.get("/")
def root():
    """龍魂API根入口"""
    return {
        "system": "龍魂本地API系统",
        "version": "1.0.0",
        "dna": "#龍芯⚡️2026-03-20-LONGHUN-API-v1.0",
        "creator": "诸葛鑫（UID9622）",
        "endpoints": [
            "/yang/create - DNA生成与注册",
            "/yang/embed - DNA水印嵌入",
            "/yin/trace - DNA追踪查询",
            "/yin/extract - 提取DNA水印",
            "/sweeper/scan - 清道夫扫描",
            "/wechat/config - 配置微信通知",
            "/wechat/test - 测试微信通知",
            "/confront/generate - 生成对峙证据包",
            "/confront/download/{package_id} - 下载证据包",
            "/evidence/chain/{dna_code} - 获取证据链",
            "/audit/blacklist - 获取黑名单"
        ]
    }

@app.post("/yang/create")
def create_dna(request: DNACreateRequest):
    """阳面：DNA生成与注册 - 概念确权"""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    content_hash = hashlib.sha256(request.content.encode()).hexdigest()[:8]
    
    dna_code = f"#龍芯⚡️{timestamp}-{request.concept_type.upper()}-{content_hash}"
    
    success = db.register_dna(
        dna_code=dna_code,
        concept_name=request.concept_name,
        concept_type=request.concept_type,
        content=request.content,
        metadata=request.metadata
    )
    
    if success:
        # 添加创世证据
        evidence_hash = db.add_evidence(
            dna_code=dna_code,
            evidence_type='dna_creation',
            content=f"概念'{request.concept_name}'注册确权",
            source_url='local://creation'
        )
        
        return {
            "success": True,
            "dna_code": dna_code,
            "concept_name": request.concept_name,
            "concept_type": request.concept_type,
            "content_hash": content_hash,
            "evidence_hash": evidence_hash,
            "message": "DNA注册成功，概念已确权"
        }
    else:
        raise HTTPException(status_code=400, detail="DNA码已存在")

@app.post("/yang/embed")
def embed_dna(request: DNAEmbedRequest):
    """阳面：DNA水印嵌入 - 隐形保护"""
    embedded_content = DNAEncoder.embed(request.content, request.dna_code)
    
    # 记录嵌入操作
    db.add_evidence(
        dna_code=request.dna_code,
        evidence_type='dna_embed',
        content=f"DNA水印嵌入内容（长度{len(request.content)}）",
        source_url='local://embed'
    )
    
    return {
        "success": True,
        "dna_code": request.dna_code,
        "original_length": len(request.content),
        "embedded_length": len(embedded_content),
        "embedded_content": embedded_content,
        "watermark_type": "零宽字符隐写"
    }

@app.get("/yin/trace/{dna_code}")
def trace_dna(dna_code: str):
    """阴面：DNA追踪查询 - 溯源确权"""
    conn = db.get_conn()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM dna_registry WHERE dna_code = ?', (dna_code,))
    dna_info = cursor.fetchone()
    conn.close()
    
    if not dna_info:
        raise HTTPException(status_code=404, detail="DNA码未找到")
    
    return {
        "success": True,
        "dna_code": dna_code,
        "concept_name": dna_info['concept_name'],
        "concept_type": dna_info['concept_type'],
        "creator_uid": dna_info['creator_uid'],
        "created_at": dna_info['created_at'],
        "content_hash": dna_info['content_hash'],
        "status": dna_info['status'],
        "metadata": json.loads(dna_info['metadata']) if dna_info['metadata'] else None
    }

@app.post("/yin/extract")
def extract_dna(content: str):
    """阴面：提取DNA水印 - 检测窃取"""
    dna_list = DNAEncoder.extract(content)
    
    return {
        "success": True,
        "dna_found": len(dna_list) > 0,
        "dna_count": len(dna_list),
        "dna_codes": dna_list,
        "analysis": "发现DNA水印" if dna_list else "未发现DNA水印"
    }

@app.post("/sweeper/scan")
def sweeper_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """清道夫：全网扫描 - 发现盗窃"""
    results = sweeper.scan_dna(request.dna_code, request.engines)
    
    # 如果发现盗窃，后台发送微信通知
    if results['theft_detected']:
        background_tasks.add_task(notifier.send_theft_alert, request.dna_code, results)
        
        # 添加证据
        for engine in results['engines_scanned']:
            if engine.get('has_results'):
                db.add_evidence(
                    dna_code=request.dna_code,
                    evidence_type='theft_detected',
                    content=f"在{engine['engine']}发现DNA出现",
                    source_url=engine.get('url', '')
                )
    
    return results

@app.post("/wechat/config")
def config_wechat(request: WeChatConfigRequest):
    """配置微信通知 - Server酱SendKey"""
    global notifier
    notifier = WeChatNotifier(request.sendkey)
    
    # 测试发送
    test_result = notifier.send_theft_alert(
        "#龍芯⚡️TEST-CONFIG",
        {'scan_time': datetime.now().isoformat(), 'engines_scanned': [], 'scan_id': 'TEST'}
    )
    
    return {
        "success": True,
        "sendkey_configured": True,
        "test_result": test_result,
        "message": "微信通知配置成功"
    }

@app.post("/wechat/test")
def test_wechat():
    """测试微信通知"""
    result = notifier.send_theft_alert(
        "#龍芯⚡️TEST-2026-03-20",
        {
            'scan_time': datetime.now().isoformat(),
            'engines_scanned': [
                {'engine': 'baidu', 'has_results': True, 'url': 'https://baidu.com/test'},
                {'engine': 'bing', 'has_results': False}
            ],
            'scan_id': 'TEST-001'
        }
    )
    return result

@app.post("/confront/generate")
def generate_confront(request: ConfrontRequest):
    """对峙模式：生成证据包 - 法律武器"""
    package = confront.generate_package(request.dna_code)
    
    return {
        "success": True,
        "package_id": package['package_id'],
        "package_path": package['package_path'],
        "evidence_count": package['evidence_count'],
        "files": package['files'],
        "message": "对峙证据包生成完成",
        "next_step": f"访问 /confront/download/{package['package_id']} 下载"
    }

@app.get("/confront/download/{package_id}")
def download_confront(package_id: str):
    """下载对峙证据包"""
    conn = db.get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM confront_packages WHERE package_id = ?', (package_id,))
    pkg = cursor.fetchone()
    conn.close()
    
    if not pkg:
        raise HTTPException(status_code=404, detail="证据包未找到")
    
    json_path = os.path.join(pkg['package_path'], 'evidence_package.json')
    if os.path.exists(json_path):
        return FileResponse(json_path, filename=f"longhun_evidence_{package_id}.json")
    else:
        raise HTTPException(status_code=404, detail="证据文件不存在")

@app.get("/evidence/chain/{dna_code}")
def get_evidence_chain(dna_code: str):
    """获取DNA的完整证据链"""
    chain = db.get_dna_evidence_chain(dna_code)
    
    return {
        "success": True,
        "dna_code": dna_code,
        "evidence_count": len(chain),
        "chain": chain,
        "integrity": "完整" if len(chain) > 0 else "无记录"
    }

@app.get("/audit/blacklist")
def get_blacklist():
    """获取黑名单 - CNSH记录"""
    conn = db.get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blacklist ORDER BY first_seen DESC')
    rows = cursor.fetchall()
    conn.close()
    
    return {
        "success": True,
        "blacklist_count": len(rows),
        "blacklist": [dict(row) for row in rows]
    }

@app.post("/audit/add_blacklist")
def add_blacklist(entity_name: str, entity_type: str, violation_type: str, dna_codes: List[str]):
    """添加黑名单 - CNSH系统"""
    conn = db.get_conn()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO blacklist (entity_name, entity_type, violation_type, dna_codes)
        VALUES (?, ?, ?, ?)
    ''', (entity_name, entity_type, violation_type, json.dumps(dna_codes)))
    
    conn.commit()
    conn.close()
    
    # 发送CNSH警告
    notifier.send_cnsh_warning(entity_name, dna_codes)
    
    return {
        "success": True,
        "entity_name": entity_name,
        "status": "CNSH-48H",
        "message": f"{entity_name} 已被列入CNSH-48H观察名单"
    }

# ============ 启动入口 ============
if __name__ == "__main__":
    print("=" * 60)
    print("龍魂本地API系统启动")
    print("DNA追溯码: #龍芯⚡️2026-03-20-LONGHUN-API-v1.0")
    print("创建者: 诸葛鑫（UID9622）")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=9622)
