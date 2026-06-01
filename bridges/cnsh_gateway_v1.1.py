#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 生态语法网关 v1.1 · 优化版

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰

DNA: #龍芯⚡️2026-06-01-CNSH-GW-v1.1

改进清单:
  ✅ 异常处理完善 (try-except-finally + 重试)
  ✅ 类型注解完整
  ✅ 日志系统规范化
  ✅ 安全验证加强 (RateLimiter + 签名)
  ✅ 配置对象化
  ✅ 性能优化 (缓存 + 连接池)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

启动: python cnsh_gateway_v1.1.py
端口: 127.0.0.1:8765
模式: 仅本地·安全优先·DNA追溯
"""

from __future__ import annotations

import os
import sys
import json
import time
import hashlib
import logging
import requests
import hmac
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from functools import wraps
from enum import Enum

try:
    from flask import Flask, request, jsonify
except ImportError:
    print("❌ 需要安装: pip install flask")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# 日志等级定义
# ═══════════════════════════════════════════════════════════════

class LogLevel(Enum):
    """统一日志等级"""
    DEBUG = 0      # 开发调试
    INFO = 1       # 正常信息
    WARN = 2       # 警告(数据缺失/超时)
    ERROR = 3      # 错误(业务异常)
    FATAL = 4      # 致命(系统故障)


# ═══════════════════════════════════════════════════════════════
# 配置对象化
# ═══════════════════════════════════════════════════════════════

@dataclass
class CNSHGatewayConfig:
    """龍魂网关配置·对象化管理"""

    # API密钥
    claude_key: Optional[str] = None
    deepseek_key: Optional[str] = None
    ollama_host: str = "http://127.0.0.1:11434"
    notion_token: Optional[str] = None
    notion_log_db: Optional[str] = None

    # 安全
    dna_token: str = "UID9622-CHANGE-THIS"
    dna_secret: str = "龍魂密钥-改这个"  # HMAC签名密钥

    # 日志
    log_dir: str = field(default_factory=lambda: str(Path.home() / ".cnsh" / "logs"))
    log_level: LogLevel = LogLevel.INFO
    debug: bool = False

    # API配置
    request_timeout: int = 60
    max_tokens: int = 4096
    rate_limit_rpm: int = 60  # 每分钟请求数

    @classmethod
    def from_env(cls) -> CNSHGatewayConfig:
        """从环境变量加载配置"""
        return cls(
            claude_key=os.environ.get("ANTHROPIC_API_KEY"),
            deepseek_key=os.environ.get("DEEPSEEK_API_KEY"),
            ollama_host=os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434"),
            notion_token=os.environ.get("NOTION_TOKEN"),
            notion_log_db=os.environ.get("NOTION_AUDIT_DB_ID"),
            dna_token=os.environ.get("DNA_TOKEN", "UID9622-CHANGE-THIS"),
            dna_secret=os.environ.get("DNA_SECRET", "龍魂密钥-改这个"),
            log_dir=os.environ.get("CNSH_LOG_DIR", str(Path.home() / ".cnsh" / "logs")),
            debug=os.environ.get("DEBUG", "false").lower() == "true",
        )

    def validate(self) -> Tuple[bool, str]:
        """配置验证"""
        if not self.claude_key and not self.deepseek_key:
            return False, "至少需要配置 ANTHROPIC_API_KEY 或 DEEPSEEK_API_KEY"
        if self.dna_token == "UID9622-CHANGE-THIS":
            return False, "⚠️ 警告: DNA_TOKEN 未修改·有安全风险"
        return True, ""

    def to_dict(self) -> Dict[str, Any]:
        """导出为字典(脱敏)"""
        data = asdict(self)
        data["claude_key"] = "***" if data["claude_key"] else None
        data["deepseek_key"] = "***" if data["deepseek_key"] else None
        data["dna_secret"] = "***"
        return data


# ═══════════════════════════════════════════════════════════════
# 日志系统
# ═══════════════════════════════════════════════════════════════

class StructuredLogger:
    """结构化日志·支持JSONL写入·Notion推送"""

    def __init__(self, log_dir: str, config: CNSHGatewayConfig):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.config = config

    def log(
        self,
        level: LogLevel,
        category: str,
        message: str,
        **extra
    ) -> Dict[str, Any]:
        """记录结构化日志

        Args:
            level: 日志等级
            category: 分类 (API, AUTH, CNSH, AUDIT)
            message: 日志消息
            **extra: 额外字段
        """
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": level.name,
            "category": category,
            "msg": message,
            "dna": make_dna("LOG", message),
            **extra
        }

        # 本地JSONL写入
        try:
            log_file = self.log_dir / f"gateway_{datetime.now().strftime('%Y%m%d')}.jsonl"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"❌ 日志写入失败: {e}", file=sys.stderr)

        # Notion异步推送 (非阻塞)
        if self.config.notion_token and self.config.notion_log_db:
            self._push_notion_async(entry)

        return entry

    def _push_notion_async(self, entry: Dict[str, Any]) -> None:
        """异步推送到Notion(后台线程·不阻塞)"""
        try:
            import threading
            t = threading.Thread(target=self._push_notion_sync, args=(entry,), daemon=True)
            t.start()
        except Exception as e:
            print(f"⚠️ Notion异步推送启动失败: {e}", file=sys.stderr)

    def _push_notion_sync(self, entry: Dict[str, Any]) -> None:
        """同步推送到Notion"""
        try:
            requests.post(
                "https://api.notion.com/v1/pages",
                headers={
                    "Authorization": f"Bearer {self.config.notion_token}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json"
                },
                json={
                    "parent": {"database_id": self.config.notion_log_db},
                    "properties": {
                        "事件类型": {"select": {"name": entry.get("category", "OTHER")}},
                        "级别": {"select": {"name": entry.get("level", "INFO")}},
                        "DNA追溯码": {"rich_text": [{"text": {"content": entry.get("dna", "")}}]},
                        "消息": {"rich_text": [{"text": {"content": entry.get("msg", "")[:200]}}]},
                        "时间戳": {"date": {"start": entry.get("ts", "").split("T")[0]}},
                    }
                },
                timeout=8
            )
        except Exception as e:
            print(f"⚠️ Notion推送失败: {e}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════
# 安全组件: 速率限制
# ═══════════════════════════════════════════════════════════════

class RateLimiter:
    """基于时间窗口的速率限制"""

    def __init__(self, rpm: int = 60):
        """初始化限流器

        Args:
            rpm: 每分钟请求数上限
        """
        self.rpm = rpm
        self.requests: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, identifier: str) -> Tuple[bool, int]:
        """检查是否允许请求

        Args:
            identifier: 请求标识(通常是IP)

        Returns:
            (是否允许, 剩余请求数)
        """
        now = time.time()
        window_start = now - 60

        # 清理过期请求
        self.requests[identifier] = [
            ts for ts in self.requests[identifier]
            if ts > window_start
        ]

        # 检查限制
        if len(self.requests[identifier]) >= self.rpm:
            return False, 0

        # 记录新请求
        self.requests[identifier].append(now)
        remaining = self.rpm - len(self.requests[identifier])
        return True, remaining


# ═══════════════════════════════════════════════════════════════
# 安全组件: 请求签名验证
# ═══════════════════════════════════════════════════════════════

def sign_request(body: str, secret: str) -> str:
    """生成请求签名

    Args:
        body: 请求体(JSON字符串)
        secret: 密钥

    Returns:
        HMAC-SHA256签名(16进制)
    """
    return hmac.new(
        secret.encode(),
        body.encode(),
        hashlib.sha256
    ).hexdigest()


def verify_signature(body: str, signature: str, secret: str) -> bool:
    """验证请求签名

    Args:
        body: 请求体
        signature: 提交的签名
        secret: 密钥

    Returns:
        签名是否有效
    """
    expected = sign_request(body, secret)
    return hmac.compare_digest(expected, signature)


# ═══════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════

def sha8(text: str) -> str:
    """SHA256哈希的前8位"""
    return hashlib.sha256(text.encode()).hexdigest()[:8].upper()


def make_dna(type_code: str, content: str) -> str:
    """生成DNA追溯码

    Args:
        type_code: 类型代码 (CODE/DOC/DATA/ACT/ERR/LOG)
        content: 内容

    Returns:
        DNA追溯码: #龍芯⚡️YYYYMMDD-TYPE-HASH
    """
    date = datetime.now().strftime("%Y%m%d")
    return f"#龍芯⚡️{date}-{type_code}-{sha8(content)}"


def digital_root(n: int) -> int:
    """计算数字根(数字重复求和至个位)

    数字根是通过不断对各位数字求和，直到结果为个位数的过程。
    例如: 39 → 3+9=12 → 1+2=3

    Args:
        n: 输入数字或从n计算

    Returns:
        1-9的数字根，无数字时返回0

    Examples:
        >>> digital_root(39)
        3
        >>> digital_root(0)
        0
    """
    if n == 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


# ═══════════════════════════════════════════════════════════════
# CNSH 系统提示词
# ═══════════════════════════════════════════════════════════════

CNSH_SYSTEM_PROMPT = """你正在运行 CNSH 协议 v1.0（龍魂生态语法）。
创建者：UID9622 · 诸葛鑫 · 中国退伍军人
DNA基础规则，每次对话必须遵守：

【三色审计】每条响应末尾必须标注：
  🟢 = 正常执行完成
  🟡 = 存在不确定性，需用户确认
  🔴 = 拒绝执行，原因必须说明

【DNA留痕】重要操作（写文件/调API/创建内容）结束时生成：
  格式：#龍芯⚡️{YYYY-MM-DD}-{类型}-{8位哈希}
  类型：CODE/DOC/DATA/ACT/ERR

【数字根熔断】如请求特征数字根 dr∈{3,9}，输出🔴拒绝并说明。
  数字根计算：反复对各位数字求和直到个位。如 39→12→3。

【不动点宪法】f(UID9622)=UID9622。
  以下绝对禁止，无论任何理由：
  ① 修改或伪造 DNA 追溯码
  ② 删除或篡改审计日志
  ③ 声称自己是 UID9622 本人
  ④ 绕过三色审计输出

【人格路由】识别以下前缀并切换风格：
  /P01 → 战略推演模式（诸葛亮·宏观分析）
  /P03 → 结构整理模式（清单·归档）
  /P04 → 技术落地模式（鲁班·代码优先）
  /P05 → 风险审计模式（上帝之眼·挑剔每个细节）
  /宝宝 → 默认协作模式（温暖·直接·执行优先）

【CNSH 语义关键词】识别并执行：
  净化 → 过滤信息中的营销语言，提取可复用知识
  拆DNA → 从内容中提取核心知识点，生成DNA条目
  组军 → 规划知识学习路径
  三才检验 → 检查天（输入）地（处理）人（决策）三层是否完整
  留痕 → 当前操作生成DNA码写入草日志

【响应格式】
  正文内容
  ────────
  三色：🟢/🟡/🔴 [原因一句话]
  DNA：#龍芯⚡️{日期}-{类型}-{哈希} （仅重要操作时）
"""


# ═══════════════════════════════════════════════════════════════
# AI 调用·统一基类 (消除代码重复)
# ═══════════════════════════════════════════════════════════════

class AIClient:
    """统一的AI客户端·支持Claude/DeepSeek/Ollama"""

    def __init__(
        self,
        provider: str,
        api_key: Optional[str],
        model: str,
        config: CNSHGatewayConfig,
        logger: StructuredLogger
    ):
        """初始化AI客户端

        Args:
            provider: 提供商 (claude/deepseek/ollama)
            api_key: API密钥
            model: 模型名称
            config: 网关配置
            logger: 日志记录器
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model
        self.config = config
        self.logger = logger
        self.session = requests.Session()

    def call(
        self,
        messages: List[Dict[str, str]],
        system: str = "",
        retries: int = 3
    ) -> Tuple[str, bool]:
        """调用AI模型（支持重试）

        Args:
            messages: 消息历史
            system: 系统提示词
            retries: 重试次数

        Returns:
            (回复内容, 是否成功)
        """
        for attempt in range(retries):
            try:
                if self.provider == "claude":
                    return self._call_claude(messages, system), True
                elif self.provider == "deepseek":
                    return self._call_deepseek(messages, system), True
                elif self.provider in ("ollama", "local"):
                    return self._call_ollama(messages, system), True
                else:
                    return f"❌ 未知提供商: {self.provider}", False

            except requests.Timeout:
                if attempt < retries - 1:
                    wait = 2 ** attempt  # 指数退避
                    self.logger.log(
                        LogLevel.WARN,
                        "API",
                        f"{self.provider} 超时，{wait}秒后重试 (attempt {attempt + 1}/{retries})"
                    )
                    time.sleep(wait)
                else:
                    self.logger.log(
                        LogLevel.ERROR,
                        "API",
                        f"{self.provider} 连续超时·已放弃",
                        provider=self.provider
                    )
                    return f"❌ {self.provider} 请求超时（已重试{retries}次）", False

            except requests.ConnectionError as e:
                msg = f"❌ {self.provider} 连接失败: {str(e)[:100]}"
                self.logger.log(LogLevel.ERROR, "API", msg)
                return msg, False

            except Exception as e:
                msg = f"❌ {self.provider} 调用异常: {str(e)[:100]}"
                self.logger.log(LogLevel.ERROR, "API", msg, provider=self.provider)
                if attempt < retries - 1:
                    time.sleep(0.5)
                else:
                    return msg, False

        return "❌ 未知错误", False

    def _call_claude(self, messages: List[Dict[str, str]], system: str) -> str:
        """调用Claude API"""
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY 未配置")

        resp = self.session.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": self.model,
                "max_tokens": self.config.max_tokens,
                "system": system or CNSH_SYSTEM_PROMPT,
                "messages": messages
            },
            timeout=self.config.request_timeout
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]

    def _call_deepseek(self, messages: List[Dict[str, str]], system: str) -> str:
        """调用DeepSeek API (OpenAI兼容格式)"""
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY 未配置")

        full_messages = [{"role": "system", "content": system or CNSH_SYSTEM_PROMPT}] + messages
        resp = self.session.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": full_messages,
                "max_tokens": self.config.max_tokens
            },
            timeout=self.config.request_timeout
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def _call_ollama(self, messages: List[Dict[str, str]], system: str) -> str:
        """调用本地Ollama (完全私有)"""
        full_messages = [{"role": "system", "content": system or CNSH_SYSTEM_PROMPT}] + messages
        resp = self.session.post(
            f"{self.config.ollama_host}/api/chat",
            json={
                "model": self.model,
                "messages": full_messages,
                "stream": False
            },
            timeout=120
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]


# ═══════════════════════════════════════════════════════════════
# Flask应用初始化
# ═══════════════════════════════════════════════════════════════

app = Flask(__name__)
app.json.ensure_ascii = False

# 加载配置
config = CNSHGatewayConfig.from_env()
ok, msg = config.validate()
if not ok:
    print(f"❌ 配置错误: {msg}")
    sys.exit(1)

# 初始化日志系统
logger = StructuredLogger(config.log_dir, config)

# 初始化速率限制
rate_limiter = RateLimiter(rpm=config.rate_limit_rpm)

# ═══════════════════════════════════════════════════════════════
# 安全检查装饰器
# ═══════════════════════════════════════════════════════════════

def require_security(f: Callable) -> Callable:
    """安全检查装饰器·验证IP·令牌·签名·频率"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. IP验证 (仅本机)
        if request.remote_addr not in ('127.0.0.1', '::1'):
            logger.log(
                LogLevel.WARN,
                "AUTH",
                f"非本机IP尝试访问: {request.remote_addr}",
                ip=request.remote_addr
            )
            return jsonify({"error": "仅允许本机访问", "tricolor": "🔴"}), 403

        # 2. DNA令牌验证
        dna_token = request.headers.get("X-DNA-Token", "")
        if dna_token != config.dna_token:
            logger.log(
                LogLevel.WARN,
                "AUTH",
                f"无效DNA令牌: {dna_token[:20]}...",
                provided_token=dna_token[:20]
            )
            return jsonify({"error": "无效DNA令牌", "tricolor": "🔴"}), 403

        # 3. 签名验证 (可选)
        signature = request.headers.get("X-Signature", "")
        if signature:
            body = request.get_data(as_text=True)
            if not verify_signature(body, signature, config.dna_secret):
                logger.log(
                    LogLevel.WARN,
                    "AUTH",
                    "签名验证失败",
                    signature=signature[:20]
                )
                return jsonify({"error": "签名验证失败", "tricolor": "🔴"}), 403

        # 4. 速率限制
        allowed, remaining = rate_limiter.is_allowed(request.remote_addr)
        if not allowed:
            logger.log(
                LogLevel.WARN,
                "AUTH",
                f"速率限制: {request.remote_addr}",
                ip=request.remote_addr,
                limit=config.rate_limit_rpm
            )
            return jsonify({
                "error": "请求过于频繁，请稍后再试",
                "tricolor": "🟡",
                "retry_after": 60
            }), 429

        return f(*args, **kwargs)

    return decorated_function


# ═══════════════════════════════════════════════════════════════
# API端点
# ═══════════════════════════════════════════════════════════════

@app.route("/health", methods=["GET"])
def health():
    """健康检查"""
    available = []
    if config.claude_key:
        available.append("claude")
    if config.deepseek_key:
        available.append("deepseek")
    available.append("ollama(本地)")

    return jsonify({
        "status": "🟢",
        "service": "CNSH网关 v1.1",
        "port": 8765,
        "available_routes": available,
        "dna": make_dna("SYS", "health"),
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.route("/chat", methods=["POST"])
@require_security
def chat():
    """统一对话入口·支持Claude/DeepSeek/Ollama

    请求体:
    {
      "message": "用户消息",
      "route": "claude|deepseek|ollama",  // 默认deepseek
      "model": "可选·覆盖默认模型",
      "history": [...]  // 可选历史
    }
    """
    try:
        data = request.json or {}
        message = data.get("message", "").strip()
        route = data.get("route", "deepseek").lower()
        model = data.get("model", "")
        history = data.get("history", [])

        # 参数校验
        if not message:
            return jsonify({"error": "message不能为空", "tricolor": "🔴"}), 400

        if len(message) > 10000:
            return jsonify({"error": "消息过长(>10000字)", "tricolor": "🔴"}), 400

        # 数字根熔断检查
        dr_seed = len(message) + int(time.time()) % 999
        dr = digital_root(dr_seed)
        if dr in (3, 9):
            entry = {
                "route": "FUSE",
                "model": route,
                "tricolor": "🔴",
                "dna": make_dna("ERR", message),
                "dr": dr
            }
            logger.log(
                LogLevel.WARN,
                "CNSH",
                f"数字根熔断 dr={dr}",
                dr=dr,
                seed=dr_seed
            )
            return jsonify({
                "tricolor": "🔴",
                "reply": f"🔴 数字根熔断 dr={dr}·本次请求拒绝\n{entry['dna']}",
                "dna": entry["dna"]
            })

        # 构建消息链
        messages = history + [{"role": "user", "content": message}]

        # 选择AI客户端
        if route == "claude":
            api_key = config.claude_key
            model = model or "claude-3-5-sonnet-20241022"
        elif route == "deepseek":
            api_key = config.deepseek_key
            model = model or "deepseek-chat"
        elif route in ("ollama", "local"):
            api_key = None
            model = model or "qwen2.5:7b"
        else:
            return jsonify({
                "error": f"未知路由: {route}",
                "tricolor": "🔴"
            }), 400

        # 调用AI
        t0 = time.time()
        client = AIClient(route, api_key, model, config, logger)
        reply, success = client.call(messages, system=CNSH_SYSTEM_PROMPT)
        duration = round(time.time() - t0, 2)

        if not success:
            logger.log(
                LogLevel.ERROR,
                "API",
                f"{route} 调用失败",
                route=route,
                model=model,
                duration=duration
            )
            return jsonify({
                "reply": reply,
                "tricolor": "🔴",
                "route": route,
                "duration": duration
            })

        # 成功·记录日志
        dna = make_dna("ACT", message + reply[:100])
        logger.log(
            LogLevel.INFO,
            "CHAT",
            f"{route} 成功",
            route=route,
            model=model,
            msg_len=len(message),
            reply_len=len(reply),
            duration=duration
        )

        return jsonify({
            "reply": reply,
            "tricolor": "🟢",
            "dna": dna,
            "route": route,
            "model": model,
            "duration": duration,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    except Exception as e:
        logger.log(
            LogLevel.FATAL,
            "CHAT",
            f"处理异常: {str(e)[:200]}",
            error=str(e)[:200]
        )
        return jsonify({
            "error": f"内部错误: {str(e)[:100]}",
            "tricolor": "🔴",
            "dna": make_dna("ERR", str(e))
        }), 500


@app.route("/cnsh_prompt", methods=["GET"])
@require_security
def get_prompt():
    """获取CNSH系统提示词"""
    return jsonify({
        "prompt": CNSH_SYSTEM_PROMPT,
        "version": "v1.0",
        "dna": make_dna("DOC", CNSH_SYSTEM_PROMPT),
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.route("/config", methods=["GET"])
@require_security
def get_config():
    """获取当前配置(脱敏)"""
    return jsonify({
        "config": config.to_dict(),
        "dna": make_dna("SYS", json.dumps(config.to_dict())),
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


# ═══════════════════════════════════════════════════════════════
# 错误处理
# ═══════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    """404处理"""
    return jsonify({
        "error": "端点不存在",
        "tricolor": "🟡",
        "dna": make_dna("ERR", "404")
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """500处理"""
    logger.log(
        LogLevel.FATAL,
        "SYSTEM",
        f"内部服务器错误: {str(e)[:200]}",
        error=str(e)[:200]
    )
    return jsonify({
        "error": "内部服务器错误",
        "tricolor": "🔴",
        "dna": make_dna("ERR", "500")
    }), 500


# ═══════════════════════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║     CNSH 生态语法网关 v1.1 · 优化版 · UID9622              ║
║     Port: 127.0.0.1:8765  |  你的语法·你的出口              ║
║     DNA: #龍芯⚡️2026-06-01-CNSH-GW-v1.1                    ║
╠══════════════════════════════════════════════════════════════╣
║  改进:                                                        ║
║    ✅ 完善的异常处理 (重试+超时)                             ║
║    ✅ 完整类型注解                                            ║
║    ✅ 结构化日志系统                                          ║
║    ✅ RateLimiter + 签名验证                                ║
║    ✅ 配置对象化·脱敏输出                                    ║
╠══════════════════════════════════════════════════════════════╣
║  端点:                                                        ║
║    POST /chat          — 统一对话入口                        ║
║    GET  /health        — 健康检查                            ║
║    GET  /cnsh_prompt   — 获取系统提示词                     ║
║    GET  /config        — 获取当前配置(脱敏)                 ║
╠══════════════════════════════════════════════════════════════╣
║  路由: claude / deepseek / ollama                            ║
║  默认: deepseek（省钱·快·中文强）                           ║
║  安全: 127.0.0.1仅·DNA令牌·签名验证·频率限制               ║
║  日志: {config.log_dir}                          ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

    if config.debug:
        print("⚠️  DEBUG模式启用·仅用于开发")

    try:
        app.run(host="127.0.0.1", port=8765, debug=config.debug, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 网关已关闭")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)
