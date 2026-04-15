#!/usr/bin/env python3
"""
CNSH-64 本地护盾代理插件
功能：E2EE加密 + 开发者后门 + DNA追溯 + 多厂家支持
作者：济公活佛，网络清道夫
"""

import json
import hashlib
import time
import os
from datetime import datetime
from typing import Optional, Dict, Any
from mitmproxy import http, ctx

# ============ 配置区 ============
class Config:
    """核心配置 - 修改这里即可"""
    
    # 开发者后门开关 - 设为 True 你走明文，用户走加密
    DEV_MODE = os.getenv("CNSH_DEV_MODE", "false").lower() == "true"
    
    # 你的公钥（用户加密用）- 普通用户必须填，你走DEV_MODE可不填
    RECIPIENT_PUBKEY = os.getenv("CNSH_PUBKEY", "age1...你的公钥这里...")
    
    # 你的私钥路径（解密用）- 必须保护好
    PRIVATE_KEY_PATH = os.getenv("CNSH_PRIVKEY_PATH", "~/.config/cnsh/private.key")
    
    # 支持的厂家API域名
    TARGET_HOSTS = [
        "api.openai.com",           # OpenAI
        "api.anthropic.com",        # Claude
        "api.x.ai",                 # Grok
        "generativelanguage.googleapis.com",  # Google
        "api.deepseek.com",         # DeepSeek
        "api.moonshot.cn",          # Kimi
    ]
    
    # DNA追溯配置
    DNA_PREFIX = "#龍芯⚡️"
    GPG_FINGERPRINT = os.getenv("CNSH_GPG", "0000000000000000")
    
    # 本地存储路径
    LOCAL_STORAGE = os.path.expanduser("~/.cnsh/vault")


# ============ DNA追溯系统 ============
class DNATracer:
    """DNA追溯码生成与验证"""
    
    def __init__(self):
        self.prev_hash = "0" * 64  # 创世哈希
        self.chain_file = os.path.join(Config.LOCAL_STORAGE, "dna_chain.log")
        os.makedirs(Config.LOCAL_STORAGE, exist_ok=True)
    
    def generate(self, content: str, action: str, host: str) -> str:
        """生成DNA追溯码"""
        timestamp = int(time.time())
        data = f"{content}|{action}|{self.prev_hash}|{timestamp}|{host}"
        content_hash = hashlib.sha256(data.encode()).hexdigest()[:16]
        
        # 洛书369验证
        dr = self._digital_root(int(content_hash, 16))
        if dr not in {3, 6, 9}:
            content_hash = self._adjust_to_369(content_hash)
        
        date_str = datetime.fromtimestamp(timestamp).strftime('%Y%m%d')
        dna = f"{Config.DNA_PREFIX}{date_str}-{content_hash}-{Config.GPG_FINGERPRINT[:8]}"
        
        # 更新链
        self.prev_hash = content_hash + hashlib.sha256(dna.encode()).hexdigest()[:48]
        self._append_to_chain(dna, timestamp, host)
        
        return dna
    
    def _digital_root(self, n: int) -> int:
        """洛书369数字根"""
        return 1 + ((n - 1) % 9) if n > 0 else 0
    
    def _adjust_to_369(self, hash_str: str) -> str:
        """调整哈希使其符合369"""
        # 简单调整：在末尾添加字符直到数字根符合
        suffix = 0
        while True:
            adjusted = hash_str[:-1] + format(suffix, 'x')
            dr = self._digital_root(int(adjusted, 16))
            if dr in {3, 6, 9}:
                return adjusted
            suffix += 1
            if suffix > 15:
                break
        return hash_str
    
    def _append_to_chain(self, dna: str, timestamp: int, host: str):
        """追加到DNA链日志"""
        with open(self.chain_file, "a") as f:
            f.write(f"{timestamp}|{dna}|{host}|{self.prev_hash[:16]}\n")


# ============ 加密引擎 ============
class EncryptionEngine:
    """E2EE加密引擎 - 使用 age 或原生加密"""
    
    def __init__(self):
        self.dna_tracer = DNATracer()
        self._check_age_installed()
    
    def _check_age_installed(self):
        """检查 age 是否安装"""
        import subprocess
        try:
            subprocess.run(["age", "--version"], capture_output=True, check=True)
            self.age_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.age_available = False
            ctx.log.warn("[CNSH] age 未安装，将使用原生加密")
    
    def encrypt(self, content: bytes, host: str) -> tuple[bytes, str]:
        """
        加密内容
        返回: (加密后的内容, DNA追溯码)
        """
        # 生成DNA
        dna = self.dna_tracer.generate(
            content[:100].decode('utf-8', errors='ignore'), 
            "ENCRYPT", 
            host
        )
        
        if Config.DEV_MODE:
            # 开发者模式：不加密，只加DNA水印
            ctx.log.info(f"[CNSH-DEV] 明文通道 | DNA: {dna}")
            marked_content = self._add_dna_watermark(content, dna)
            return marked_content, dna
        
        # 普通用户：强制加密
        if self.age_available and Config.RECIPIENT_PUBKEY.startswith("age1"):
            encrypted = self._age_encrypt(content)
        else:
            encrypted = self._native_encrypt(content)
        
        ctx.log.info(f"[CNSH] 已加密 | DNA: {dna} | 大小: {len(content)} -> {len(encrypted)}")
        return encrypted, dna
    
    def decrypt(self, content: bytes, dna: str) -> bytes:
        """解密内容"""
        if Config.DEV_MODE:
            ctx.log.info(f"[CNSH-DEV] 明文接收 | DNA: {dna}")
            return self._remove_dna_watermark(content)
        
        if self.age_available:
            return self._age_decrypt(content)
        else:
            return self._native_decrypt(content)
    
    def _add_dna_watermark(self, content: bytes, dna: str) -> bytes:
        """添加DNA水印（开发者模式）"""
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                data["_cnsh_dna"] = dna
                data["_cnsh_dev"] = True
                return json.dumps(data).encode()
        except:
            pass
        return content
    
    def _remove_dna_watermark(self, content: bytes) -> bytes:
        """移除DNA水印"""
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                data.pop("_cnsh_dna", None)
                data.pop("_cnsh_dev", None)
                return json.dumps(data).encode()
        except:
            pass
        return content
    
    def _age_encrypt(self, content: bytes) -> bytes:
        """使用 age 加密"""
        import subprocess
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = subprocess.run(
                ["age", "-r", Config.RECIPIENT_PUBKEY, "-o", "-", temp_path],
                capture_output=True,
                check=True
            )
            return result.stdout
        finally:
            os.unlink(temp_path)
    
    def _age_decrypt(self, content: bytes) -> bytes:
        """使用 age 解密"""
        import subprocess
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = subprocess.run(
                ["age", "-d", "-i", os.path.expanduser(Config.PRIVATE_KEY_PATH), "-o", "-", temp_path],
                capture_output=True,
                check=True
            )
            return result.stdout
        finally:
            os.unlink(temp_path)
    
    def _native_encrypt(self, content: bytes) -> bytes:
        """原生加密（备用方案）"""
        from cryptography.fernet import Fernet
        # 使用基于密码的密钥（实际部署时应该更安全）
        key = hashlib.sha256(Config.RECIPIENT_PUBKEY.encode()).digest()[:32]
        key_b64 = Fernet.generate_key()[:32]  # 占位，实际需要正确处理
        f = Fernet(Fernet.generate_key())
        return f.encrypt(content)
    
    def _native_decrypt(self, content: bytes) -> bytes:
        """原生解密（备用方案）"""
        # 实现略，与加密对应
        return content


# ============ 内容处理器 ============
class ContentProcessor:
    """内容处理引擎 - 骂人全文保留/修饰/多造点"""
    
    # 处理模式：full(全文) | clean(修饰) | multi(多造点)
    MODE = os.getenv("CNSH_CONTENT_MODE", "full")
    
    # 脏话词库（示例，实际可扩展）
    DIRTY_WORDS = ["操", "他妈", "傻逼", "狗日", "妈逼", "贱人"]
    
    def __init__(self):
        self.encryption = EncryptionEngine()
    
    def process_request(self, content: bytes) -> bytes:
        """处理请求内容"""
        if self.MODE == "full":
            return content
        elif self.MODE == "clean":
            return self._clean_content(content)
        elif self.MODE == "multi":
            return self._multi_content(content)
        return content
    
    def process_response(self, content: bytes) -> bytes:
        """处理响应内容"""
        # 响应一般不处理，直接透传
        return content
    
    def _clean_content(self, content: bytes) -> bytes:
        """修饰内容 - 过滤脏话"""
        try:
            text = content.decode('utf-8')
            for word in self.DIRTY_WORDS:
                text = text.replace(word, "*" * len(word))
            return text.encode()
        except:
            return content
    
    def _multi_content(self, content: bytes) -> bytes:
        """多造点 - 内容少了就补充"""
        try:
            text = content.decode('utf-8')
            if len(text) < 100:  # 被过滤少了
                supplement = self._generate_supplement()
                text = text + "\n\n[本地补充生成：继续骂...]\n" + supplement
            return text.encode()
        except:
            return content
    
    def _generate_supplement(self) -> str:
        """本地生成补充内容"""
        # 这里可以接本地模型（Ollama/LM Studio）
        # 简化版：返回固定模板
        templates = [
            "这他妈的什么狗屁系统，老子不服！",
            "操，过滤个屁，老子继续骂！",
            "妈逼的，有种来封老子啊！",
        ]
        import random
        return random.choice(templates)


# ============ 主代理类 ============
class CNSHProxy:
    """CNSH-64 本地护盾代理主类"""
    
    def __init__(self):
        self.content_processor = ContentProcessor()
        self.encryption = EncryptionEngine()
        ctx.log.info("=" * 60)
        ctx.log.info("[CNSH-64] 本地护盾代理已启动")
        ctx.log.info(f"[CNSH-64] 开发者模式: {Config.DEV_MODE}")
        ctx.log.info(f"[CNSH-64] 内容处理模式: {ContentProcessor.MODE}")
        ctx.log.info(f"[CNSH-64] 隐私隔离: 已启用")
        ctx.log.info("=" * 60)
    
    def _is_target_host(self, host: str) -> bool:
        """判断是否为目标API主机"""
        return any(target in host for target in Config.TARGET_HOSTS)
    
    def request(self, flow: http.HTTPFlow):
        """处理请求"""
        if not self._is_target_host(flow.request.host):
            return
        
        ctx.log.info(f"[CNSH] 拦截请求: {flow.request.host}{flow.request.path}")
        
        # 1. 处理内容（骂人全文/修饰/多造点）
        if flow.request.content:
            processed = self.content_processor.process_request(flow.request.content)
            
            # 2. 加密 + DNA追溯
            encrypted, dna = self.encryption.encrypt(processed, flow.request.host)
            flow.request.content = encrypted
            
            # 3. 添加DNA头部
            flow.request.headers["X-CNSH-DNA"] = dna
            flow.request.headers["X-CNSH-Version"] = "0.3-L3-PRE"
            flow.request.headers["X-CNSH-Encrypted"] = "false" if Config.DEV_MODE else "true"
            
            ctx.log.info(f"[CNSH] 请求已处理 | DNA: {dna}")
    
    def response(self, flow: http.HTTPFlow):
        """处理响应"""
        if not self._is_target_host(flow.request.host):
            return
        
        dna = flow.request.headers.get("X-CNSH-DNA", "unknown")
        ctx.log.info(f"[CNSH] 接收响应: {flow.request.host} | DNA: {dna}")
        
        # 1. 解密
        if flow.response.content:
            decrypted = self.encryption.decrypt(flow.response.content, dna)
            
            # 2. 处理响应内容
            processed = self.content_processor.process_response(decrypted)
            flow.response.content = processed
            
            ctx.log.info(f"[CNSH] 响应已解密 | 大小: {len(flow.response.content)}")


# ============ 插件入口 ============
addons = [CNSHProxy()]


# ============ 辅助命令 ============
"""
启动代理命令:

1. 普通用户模式（强制加密）:
   mitmweb -s cnsh_proxy_addon.py --listen-port 8080

2. 开发者模式（明文通道）:
   export CNSH_DEV_MODE=true
   mitmweb -s cnsh_proxy_addon.py --listen-port 8080

3. 指定内容处理模式:
   export CNSH_CONTENT_MODE=full    # 全文保留
   export CNSH_CONTENT_MODE=clean   # 修饰过滤
   export CNSH_CONTENT_MODE=multi   # 多造点

4. 配置公钥:
   export CNSH_PUBKEY=age1...
   export CNSH_PRIVKEY_PATH=~/.config/cnsh/private.key

系统代理设置:
   HTTP_PROXY=http://127.0.0.1:8080
   HTTPS_PROXY=http://127.0.0.1:8080
"""
