#!/usr/bin/env python3
"""
龍魂·飞书知识库抓取引擎 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用途: 深度学习飞书开放平台公开文档，构建本地知识库底座
来源: GitHub SDK仓库 / 飞书开放平台API / CSDN博客 / 官方FAQ
存储: /opt/longhun/data/knowledge/feishu/
自动更新: systemd timer 每6小时检查一次

DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-FEISHU-KB-FETCHER-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import os
import sys
import json
import time
import hashlib
import argparse
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# ─── 配置 ───────────────────────────────────────────────────
KB_ROOT = Path("/opt/longhun/data/knowledge/feishu")
LOCAL_KB_ROOT = Path(os.environ.get("HOME", "/tmp")) / "longhun-system/data/knowledge/feishu"
VERSION_FILE = "kb_version.json"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30
USER_AGENT = "Longhun-Feishu-KB-Fetcher/1.0 (UID9622; +https://uid9622.cn)"
FETCH_INTERVAL_HOURS = 6  # 自动更新间隔

# ─── 知识源定义 ────────────────────────────────────────────
# 格式: (id, name, type, url, docs_url, fetch_method)
# type: github_readme | github_dir | feishu_api | feishu_static | web_article
KNOWLEDGE_SOURCES = [
    # === GitHub SDK 官方文档 ===
    {
        "id": "oapi-sdk-readme",
        "name": "飞书 Python SDK README",
        "type": "github_raw",
        "url": "https://raw.githubusercontent.com/larksuite/oapi-sdk-python/v2_main/README.md",
        "file": "oapi-sdk-readme.md",
        "category": "sdk",
        "priority": 10,
    },
    {
        "id": "oapi-sdk-channel-doc",
        "name": "飞书 Channel SDK 文档",
        "type": "github_raw",
        "url": "https://raw.githubusercontent.com/larksuite/oapi-sdk-python/v2_main/doc/channel.md",
        "file": "oapi-sdk-channel.md",
        "category": "sdk",
        "priority": 10,
    },
    {
        "id": "oapi-sdk-channel-quickstart",
        "name": "飞书 Channel 快速开始",
        "type": "github_raw",
        "url": "https://raw.githubusercontent.com/larksuite/oapi-sdk-python/v2_main/doc/channel/quickstart.md",
        "file": "oapi-sdk-channel-quickstart.md",
        "category": "sdk",
        "priority": 9,
    },
    {
        "id": "oapi-sdk-channel-reference",
        "name": "飞书 Channel API 参考",
        "type": "github_raw",
        "url": "https://raw.githubusercontent.com/larksuite/oapi-sdk-python/v2_main/doc/channel/reference.md",
        "file": "oapi-sdk-channel-reference.md",
        "category": "sdk",
        "priority": 10,
    },
    {
        "id": "oapi-sdk-dedup-arch",
        "name": "飞书去重架构文档",
        "type": "github_raw",
        "url": "https://raw.githubusercontent.com/larksuite/oapi-sdk-python/v2_main/doc/channel/dedup-architecture.md",
        "file": "oapi-sdk-dedup.md",
        "category": "sdk",
        "priority": 8,
    },
    # 飞书SDK Python README 已包含API模块列表，无需额外抓取
    # === 飞书开放平台 OpenAPI 元数据 ===
    {
        "id": "feishu-openapi-meta",
        "name": "飞书 OpenAPI 元数据",
        "type": "feishu_api",
        "url": "https://open.feishu.cn/open-apis/im/v1/messages",
        "file": "feishu-openapi-meta.json",
        "category": "api",
        "priority": 7,
    },
    # === 第三方博客/实践指南 ===
    {
        "id": "feishu-bot-dev-guide-tencent",
        "name": "腾讯云: 飞书机器人开发全流程",
        "type": "web_article",
        "url": "https://cloud.tencent.com/developer/article/2670675",
        "file": "guide-bot-dev-full.md",
        "category": "guide",
        "priority": 7,
    },
    {
        "id": "feishu-agent-feishu-guide",
        "name": "腾讯云: Agent接入飞书全流程",
        "type": "web_article",
        "url": "https://cloud.tencent.com/developer/article/2655926",
        "file": "guide-agent-feishu.md",
        "category": "guide",
        "priority": 7,
    },
    {
        "id": "feishu-bot-events-faq",
        "name": "飞书开放平台: 开发教程FAQ",
        "type": "web_article",
        "url": "https://open.feishu.cn/document/develop-an-echo-bot/faq",
        "file": "guide-bot-faq.md",
        "category": "guide",
        "priority": 8,
    },
    # === 卡片 JSON 结构（从 CSDN 实践博客获取） ===
    {
        "id": "feishu-card-json-csdn",
        "name": "CSDN: 飞书IM消息与卡片消息详解",
        "type": "web_article",
        "url": "https://blog.csdn.net/csdn122345/article/details/160534404",
        "file": "feishu-card-im-csdn.md",
        "category": "card",
        "priority": 8,
    },
]


# ─── 工具函数 ──────────────────────────────────────────────

def ensure_dir(path: Path) -> None:
    """确保目录存在。"""
    path.mkdir(parents=True, exist_ok=True)


def fetch_url(url: str, retries: int = MAX_RETRIES) -> Optional[bytes]:
    """带重试的 URL 抓取。"""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/plain,text/markdown,application/json,text/html,*/*",
                },
            )
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                return resp.read()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            if attempt < retries - 1:
                wait = 2 ** attempt
                print(f"  [RETRY {attempt+1}/{retries}] {url[:80]}... (wait {wait}s)", flush=True)
                time.sleep(wait)
            else:
                print(f"  [FAIL] {url[:80]}... -> {e}", flush=True)
    return None


def hash_content(content: bytes) -> str:
    """计算内容 SHA256 哈希。"""
    return hashlib.sha256(content).hexdigest()[:16]


def load_version(kb_root: Path) -> Dict[str, Any]:
    """加载版本记录。"""
    vf = kb_root / VERSION_FILE
    if vf.exists():
        try:
            return json.loads(vf.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"version": "0.0.0", "last_fetch": None, "source_hashes": {}, "fetch_count": 0}


def save_version(kb_root: Path, version: Dict[str, Any]) -> None:
    """保存版本记录。"""
    ensure_dir(kb_root)
    (kb_root / VERSION_FILE).write_text(
        json.dumps(version, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ─── 抓取引擎 ──────────────────────────────────────────────

def fetch_github_raw(source: Dict, kb_root: Path) -> Tuple[bool, str]:
    """从 GitHub raw 获取 Markdown/代码文件。"""
    url = source["url"]
    dest = kb_root / source["file"]

    content = fetch_url(url)
    if content is None:
        return False, f"无法获取: {url}"

    text = content.decode("utf-8", errors="replace")

    # 写入文件
    ensure_dir(dest.parent)
    dest.write_text(text, encoding="utf-8")

    return True, f"OK ({len(text)} chars, hash={hash_content(content)})"


def fetch_feishu_api(source: Dict, kb_root: Path) -> Tuple[bool, str]:
    """尝试通过飞书 OpenAPI 获取元数据（需要 tenant_access_token）。"""
    # 飞书开放平台 OpenAPI 需要 app_id/app_secret 才能访问
    # 这里尝试无认证获取，大多数情况下会得到 401
    # 我们保存返回的结构作为参考
    url = source["url"]
    dest = kb_root / source["file"]

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        # 401 是预期的（需要认证），保存错误信息作为参考
        error_info = json.dumps({
            "status": e.code,
            "note": "此端点需要 app_id/app_secret 认证。知识库包含 API 文档而非实时数据。",
            "url": url,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }, ensure_ascii=False, indent=2)
        ensure_dir(dest.parent)
        dest.write_text(error_info, encoding="utf-8")
        return True, f"端点需认证 ({e.code})，已保存元数据"
    except Exception as e:
        return False, str(e)

    # 保存 API 响应
    ensure_dir(dest.parent)
    dest.write_bytes(data)
    return True, f"OK ({len(data)} bytes)"


def fetch_web_article(source: Dict, kb_root: Path) -> Tuple[bool, str]:
    """抓取 Web 文章（HTML -> Markdown 转换）。"""
    url = source["url"]
    dest = kb_root / source["file"]

    content = fetch_url(url)
    if content is None:
        return False, f"无法获取: {url}"

    html = content.decode("utf-8", errors="replace")

    # 简单 HTML -> Markdown 转换
    md = _html_to_markdown_simple(html, url, source.get("name", ""))

    ensure_dir(dest.parent)
    dest.write_text(md, encoding="utf-8")
    return True, f"OK ({len(md)} chars)"


def _html_to_markdown_simple(html: str, url: str, title: str = "") -> str:
    """简陋但有效的 HTML -> Markdown 转换。"""
    import re

    # 提取 title
    if not title:
        m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if m:
            title = m.group(1).strip()

    # 提取 body 内容
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.IGNORECASE | re.DOTALL)
    if body_match:
        text = body_match.group(1)
    else:
        text = html

    # 移除 script/style 标签
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.IGNORECASE | re.DOTALL)

    # 移除 HTML 标签，保留文本
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</(p|div|h[1-6]|li|tr|section|article)>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)

    # 清理空白行
    lines = [l.strip() for l in text.split("\n")]
    lines = [l for l in lines if l]
    text = "\n".join(lines)

    # 组装 Markdown
    md = f"---\ntitle: {title}\nsource: {url}\nfetched_at: {datetime.now(timezone.utc).isoformat()}\n---\n\n"
    md += f"# {title}\n\n"
    md += f"> 来源: {url}\n\n"
    md += text

    return md


# ─── 汇编层：内置核心知识卡 ───────────────────────────────

CORE_KNOWLEDGE_CARDS = {
    "card-json-structure.md": """---
title: 飞书卡片消息 JSON 结构完整参考
category: card
priority: 10
created: 2026-08-05
source: 飞书开放平台官方文档 + GitHub lark-card-kit
---

# 飞书卡片消息 JSON 结构

## 顶层结构

\\`\\`\\`json
{
  "config": { ... },       // 卡片配置（可选）
  "header": { ... },       // 卡片标题（可选）
  "elements": [ ... ],     // 卡片内容组件数组
  "card_link": { ... },    // 卡片跳转链接（可选）
  "i18n_elements": { ... } // 国际化内容（可选）
}
\\`\\`\\`

## 卡片属性速查

| 属性 | 类型 | 必填 | 说明 |
|:---|:---|:---:|:---|
| config | CardConfig | 否 | 卡片配置：是否允许转发、是否更新多端等 |
| header | CardHeader | 否 | 卡片标题，含颜色模板 |
| elements | Element[] | 否 | 卡片内容组件列表 |
| card_link | CardLink | 否 | 点击卡片后的跳转链接 |
| i18n_elements | I18nElements | 否 | 各语言环境下的卡片内容 |

## config 配置项

\\`\\`\\`json
{
  "wide_screen_mode": true,    // 是否宽屏模式
  "enable_forward": true,      // 是否允许转发
  "update_multi": false        // 是否更新多端
}
\\`\\`\\`

## header 标题

\\`\\`\\`json
{
  "template": "blue",  // 颜色: blue/wathet/turquoise/green/yellow/orange/red/carmine/violet/purple/indigo/grey
  "title": {
    "tag": "plain_text",
    "content": "卡片标题"
  }
}
\\`\\`\\`

## elements 组件速查表

### 容器类组件
| 组件 | tag | 说明 |
|:---|:---|:---|
| 分割线 | hr | 水平分割线 |
| 备注 | note | 小字备注，可含 inline 元素 |
| 列布局 | column_set | 多列布局容器 |
| 列 | column | 单列容器，width 按 weight(1-12) 或百分比 |

### 内容类组件
| 组件 | tag | 说明 |
|:---|:---|:---|
| Markdown块 | markdown | 支持飞书Markdown子集 |
| 纯文本 | div | 复合文本块 |
| 图片 | img | 图片（需 image_key） |
| 多图 | img_combination | 多图组合布局 |
| 视频 | video | 视频（需 video_key） |

### 交互类组件
| 组件 | tag | 说明 |
|:---|:---|:---|
| 按钮 | button | 可配置 action |
| 多按钮 | action | 多个按钮组合 |
| 日期选择 | date_picker | 日期选择器 |
| 下拉选择 | select_static | 静态下拉选择 |
| 多选下拉 | select_person | 人员选择 |
| 输入框 | input | 文本输入 |
| 复选框 | checkbox | 多选框 |
| 单选框 | radio_button | 单选按钮 |

## button 按钮组件详解

\\`\\`\\`json
{
  "tag": "button",
  "text": {
    "tag": "plain_text",
    "content": "确认"
  },
  "type": "primary",          // primary | danger | default
  "width": "default",         // default | fill
  "size": "medium",           // large | medium | small
  "disabled": false,          // 是否禁用
  "value": {                  // 点击后透传的值（JSON对象）
    "action": "confirm",
    "code": "abc123"
  },
  "confirm": {                // 二次确认弹窗（可选）
    "title": { "tag": "plain_text", "content": "确认删除?" },
    "text": { "tag": "plain_text", "content": "此操作不可撤销" }
  },
  "behaviors": ["webhook_url"] // 触发的行为类型
}
\\`\\`\\`

### button type 风格
| type | 样式 | 适用场景 |
|:---|:---|:---|
| primary | 蓝色实心 | 主操作：确认、提交 |
| danger | 红色实心 | 危险操作：删除、重置 |
| default | 灰色边框 | 次要操作：取消、返回 |

## action 操作组组件

\\`\\`\\`json
{
  "tag": "action",
  "layout": "bisected",       // bisected(二等分) | trisection(三等分) | flow(流式)
  "actions": [
    {
      "tag": "button",
      "text": { "tag": "plain_text", "content": "确认" },
      "type": "primary",
      "value": { "action": "confirm" }
    }
  ]
}
\\`\\`\\`

## div 文本块组件

\\`\\`\\`json
{
  "tag": "div",
  "text": {
    "tag": "lark_md",   // lark_md(飞书MD) | plain_text
    "content": "这是一段**富文本**内容"
  },
  "fields": [           // 键值对字段（可选）
    { "is_short": true, "text": { "tag": "lark_md", "content": "**状态**: 正常" } }
  ],
  "extra": {            // 右侧扩展元素（可选）
    "tag": "img",
    "img_key": "img_v3_xxx"
  }
}
\\`\\`\\`

## 卡片回调 (Card Action Callback)

当用户点击卡片中的 button/select 等交互组件时，飞书会 POST 请求到机器人配置的「消息卡片请求网址」。

### 回调请求格式

\\`\\`\\`json
POST https://your-server/webhook/card
Content-Type: application/json

{
  "open_chat_id": "oc_xxx",       // 会话ID
  "open_message_id": "om_xxx",    // 消息ID
  "user_id": {                     // 用户身份
    "union_id": "on_xxx",
    "open_id": "ou_xxx"
  },
  "action": {
    "tag": "button",               // 组件类型
    "value": {                     // 开发者自定义的透传值
      "action": "confirm"
    },
    "option": "..."                // 下拉选项（仅选择类组件）
  },
  "challenge": "..."               // URL验证用（仅首次）
}
\\`\\`\\`

### 回调响应格式

\\`\\`\\`json
{
  "toast": {
    "type": "success",      // success | warning | error
    "content": "✅ 已确认",
    "duration": 3000        // 显示时长(ms)，可选
  },
  "card": { ... }           // 更新后的卡片（可选，用于就地更新卡片内容）
}
\\`\\`\\`

### 回调重要注意事项

1. **5秒超时**: 飞书要求回调在 5 秒内响应，超时视为失败
2. **重试机制**: 失败会重试最多 3 次，间隔递增（1s/2s/4s）
3. **幂等要求**: 同一用户对同一按钮的重复回调必须能安全处理
4. **去重**: 同一个 open_message_id + user_id + action 的短时间重复应去重
5. **toast 必返回**: 即使处理失败也要返回 toast，否则用户无感知
6. **card 可选返回**: 返回 card 对象可就地更新卡片，无需再调 API 发送新消息
7. **challenge 校验**: 飞书首次配置回调URL时会发送 challenge，需原样返回

## 最佳实践

### 1. 按钮去重
\\`\\`\\`python
# 10秒幂等缓存，防连点和重试
_CARD_ACTION_COOLDOWN = 10
_recent_actions: Dict[str, float] = {}

def handle_card_action(chat_id, user_id, action_value):
    dedup_key = f"{chat_id}:{user_id}:{action_value['action']}"
    now = time.time()
    if now - _recent_actions.get(dedup_key, 0) < _CARD_ACTION_COOLDOWN:
        return {"toast": {"type": "success", "content": "已处理"}}
    _recent_actions[dedup_key] = now
    # ... 实际处理逻辑
\\`\\`\\`

### 2. 卡片就地更新
\\`\\`\\`python
def handle_card_action(chat_id, user_id, action_value):
    # 处理完成后，返回新卡片替换旧卡片
    new_card = build_result_card(user_id)
    return {
        "toast": {"type": "success", "content": "处理完成"},
        "card": new_card
    }
\\`\\`\\`

### 3. 错误处理
\\`\\`\\`python
def handle_card_action(chat_id, user_id, action_value):
    try:
        result = process_action(action_value)
        return {
            "toast": {"type": "success", "content": "处理完成"},
            "card": result
        }
    except Exception as e:
        # 即使出错也要返回 toast
        return {
            "toast": {"type": "error", "content": f"处理失败: {str(e)[:50]}"}
        }
\\`\\`\\`
""",
    "bot-setup-guide.md": """---
title: 飞书机器人从零搭建完整指南
category: guide
priority: 10
created: 2026-08-05
source: 飞书开放平台 + 龍魂实战经验
---

# 飞书机器人从零搭建完整指南

## 一、两种机器人类型

### 1. 自定义机器人（Webhook机器人）
- **用途**: 单向推送消息到群聊
- **创建**: 群设置 → 群机器人 → 添加自定义机器人
- **认证**: Webhook URL 中包含 token
- **签名**: 可选，用密钥对消息体做 HMAC-SHA256
- **限制**: 只能发消息，不能接收消息/事件

### 2. 应用机器人（App Bot）
- **用途**: 双向通信，接收消息，卡片交互
- **创建**: 飞书开放平台 → 创建企业自建应用
- **认证**: App ID + App Secret → 获取 tenant_access_token
- **能力**: 收发消息、事件订阅、卡片回调、API 调用

## 二、应用机器人创建流程

### 步骤1: 创建应用
1. 打开 https://open.feishu.cn/app
2. 点击「创建企业自建应用」
3. 填写应用名称、描述、图标

### 步骤2: 添加机器人能力
1. 进入应用 → 「添加应用能力」
2. 选择「机器人」

### 步骤3: 配置权限
在「权限管理」中开通：

| 权限 | 用途 | 必开 |
|:---|:---|:---:|
| im:message | 获取与发送单聊、群组消息 | ✅ |
| im:message.p2p_msg:readonly | 读取用户发给机器人的单聊消息 | ✅ |
| im:message:send_as_bot | 以应用身份发消息 | ✅ |
| im:message.group_at_msg:readonly | 接收群聊中@机器人消息事件 | ✅ |
| im:resource | 获取消息中的资源文件 | 可选 |
| contact:user.id:readonly | 读取用户 ID | ✅ |

### 步骤4: 配置事件订阅（长连接模式）
1. 进入「事件订阅」
2. 选择「使用长连接接收事件」（推荐，无需公网URL）
3. 订阅事件：
   - im.message.receive_v1（接收消息）
   - im.message.reaction.created_v1（消息表情回复）
   - im.message.reaction.deleted_v1
4. 如需卡片回调 → 填写「消息卡片请求网址」

### 步骤5: 获取凭证
在「凭证与基础信息」获取：
- App ID: cli_xxxxxxxxxxxx
- App Secret: xxxxxxxxxxxxxxxx

### 步骤6: 发布版本
1. 进入「版本管理与发布」
2. 创建版本 → 填写版本号
3. 提交发布
4. **必须发布版本，事件订阅才会生效！**

## 三、长连接模式 vs Webhook模式

| 特性 | 长连接(WebSocket) | Webhook |
|:---|:---|:---|
| 部署要求 | 无需公网IP | 需要公网可达的URL |
| 适用场景 | 内网/本地开发 | 有固定公网地址的服务器 |
| 连接方式 | 主动连接飞书 | 被动接收飞书POST |
| SDK支持 | lark-channel-sdk | Flask/FastAPI等任何HTTP框架 |
| 调试方便度 | 中等 | 高（可直接curl测试） |

### 长连接模式核心流程
1. 获取 WSS URL: POST /open-apis/event/v1/ws/url
2. 建立 WebSocket 连接
3. 接收事件推送
4. 心跳保活（30秒间隔）
5. 断线自动重连（指数退避）

## 四、消息类型速查

| 类型 | msg_type | 说明 |
|:---|:---|:---|
| 文本 | text | 纯文本消息 |
| 富文本 | post | 富文本格式消息 |
| 图片 | image | 图片消息 |
| 文件 | file | 文件消息 |
| 音频 | audio | 语音消息 |
| 视频 | media | 视频消息 |
| 表情包 | sticker | 表情包消息 |
| 交互卡片 | interactive | 卡片消息（最重要） |
| 分享群 | share_chat | 分享群聊 |
| 分享用户 | share_user | 分享用户 |

## 五、发送消息 API

### 基础请求
\\`\\`\\`
POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id
Authorization: Bearer {tenant_access_token}
Content-Type: application/json

{
  "receive_id": "oc_xxx",
  "msg_type": "interactive",
  "content": "{\\"config\\":{...},\\"header\\":{...},\\"elements\\":[...]}"
}
\\`\\`\\`

### receive_id_type 参数
| 值 | 说明 |
|:---|:---|
| open_id | 用户的 open_id |
| union_id | 用户的 union_id |
| email | 用户的邮箱 |
| chat_id | 群聊/会话的 chat_id |

## 六、获取 tenant_access_token

\\`\\`\\`
POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
Content-Type: application/json

{
  "app_id": "cli_xxx",
  "app_secret": "xxx"
}

Response:
{
  "code": 0,
  "tenant_access_token": "t-xxx",
  "expire": 7200   // 有效期2小时
}
\\`\\`\\`

### Token 管理最佳实践
- 缓存 token，过期前 5 分钟刷新
- 不要每次请求都获取新 token
- 获取 token 有频率限制（100次/分钟/应用）

## 七、事件订阅 URL 验证

飞书首次配置回调URL时，会发送 challenge 验证请求：

\\`\\`\\`json
POST https://your-server/webhook/event

{
  "challenge": "ajls384kdjx98XX",
  "token": "xxx",
  "type": "url_verification"
}
\\`\\`\\`

服务器必须返回：
\\`\\`\\`json
{
  "challenge": "ajls384kdjx98XX"
}
\\`\\`\\`

## 八、调试工具与方法

### 1. 飞书开放平台调试工具
在应用详情页 → 「调试窗口」→ 可以：
- 查看最近的事件推送日志
- 测试发送消息
- 查看 API 调用记录

### 2. 飞书消息卡片搭建工具
https://open.feishu.cn/card/builder
- 可视化拖拽构建卡片
- 实时预览效果
- 导出 JSON 代码

### 3. 本地调试必备
- ngrok/frp 内网穿透（Webhook模式需要）
- Postman/Apipost 测试 API
- 飞书开发者后台「事件日志」查看推送状态

### 4. 常见错误码速查
| 错误码 | 含义 | 解决 |
|:---|:---|:---|
| 99991400 | token 无效 | 刷新 tenant_access_token |
| 99991663 | 无权限 | 检查应用权限配置 |
| 230001 | 参数错误 | 检查请求体格式 |
| 230002 | 接收者不存在 | 检查 receive_id |
| 10007 | 需要审批 | 需管理员审批 |
| 10203 | 请求频率限制 | 降低请求频率/排队重试 |

## 九、龍魂实战经验

### 自我鉴定模式卡片
\\`\\`\\`python
FEISHU_CARD_JSON = {
    "config": {"wide_screen_mode": True},
    "header": {"template": "purple", "title": {"tag": "plain_text", "content": "🧠 自我鉴定"}},
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": "请点击下方按钮完成今日鉴定..."}},
        {"tag": "action", "layout": "bisected", "actions": [
            {"tag": "button", "text": {"tag": "plain_text", "content": "让我鉴定"}, "type": "primary", "value": json.dumps({"action": "confirm", "code": "xxx"})},
            {"tag": "button", "text": {"tag": "plain_text", "content": "忽略"}, "type": "default", "value": json.dumps({"action": "ignore"})}
        ]}
    ]
}
\\`\\`\\`

### 飞书回调服务关键点
1. 响应用 toast 要在 5 秒内返回
2. 不要在处理逻辑中再 send_text（会重复消息）
3. 加幂等缓存防重试和连点
4. 卡片 value 使用 JSON 对象，不要用 json.dumps 字符串
5. 可通过返回 card 就地更新卡片内容
""",
    "sdk-api-reference.md": """---
title: 飞书 Python SDK API 参考速查
category: sdk
priority: 10
created: 2026-08-05
source: GitHub larksuite/oapi-sdk-python v2
---

# 飞书 Python SDK API 参考速查

## 一、安装

\\`\\`\\`bash
pip install lark-oapi
# 或者带 channel 支持（长连接）
pip install "lark-oapi[channel]"
\\`\\`\\`

## 二、客户端初始化

### 基础客户端
\\`\\`\\`python
from lark_oapi import Client

client = Client.builder() \\
    .app_id("cli_xxx") \\
    .app_secret("xxx") \\
    .build()
\\`\\`\\`

### 带 Channel（长连接）的客户端
\\`\\`\\`python
from lark_oapi import Client

client = Client.builder() \\
    .app_id("cli_xxx") \\
    .app_secret("xxx") \\
    .build()

# 初始化 channel
from lark_oapi.channel import ChannelManager

channel = ChannelManager.builder()
    .client(client)
    .event_handler(my_event_handler, event_type=EVENT_TYPE)
    .build()

channel.start()
\\`\\`\\`

### 飞书（中国版）使用
\\`\\`\\`python
client = Client.builder() \\
    .app_id("cli_xxx") \\
    .app_secret("xxx") \\
    .open_api_url("https://open.feishu.cn") \\
    .build()
\\`\\`\\`

## 三、消息 API

### 发送文本消息
\\`\\`\\`python
import lark_oapi as lark
from lark_oapi.api.im.v1 import *

# 构造请求
request = CreateMessageRequest.builder() \\
    .receive_id_type("chat_id") \\
    .request_body(
        CreateMessageRequestBody.builder()
            .receive_id("oc_xxx")
            .msg_type("text")
            .content('{"text":"你好"}')
            .build()
    ) \\
    .build()

# 发送
response = client.im.v1.message.create(request)

if response.success():
    print(f"消息ID: {response.data.message_id}")
else:
    print(f"错误: {response.code} - {response.msg}")
\\`\\`\\`

### 发送卡片消息
\\`\\`\\`python
card_json = json.dumps({
    "config": {"wide_screen_mode": True},
    "header": {
        "template": "blue",
        "title": {"tag": "plain_text", "content": "通知"}
    },
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": "这是一条卡片消息"}},
        {"tag": "action", "layout": "bisected", "actions": [
            {"tag": "button", "text": {"tag": "plain_text", "content": "确认"},
             "type": "primary", "value": {"action": "confirm"}}
        ]}
    ]
})

request = CreateMessageRequest.builder() \\
    .receive_id_type("chat_id") \\
    .request_body(
        CreateMessageRequestBody.builder()
            .receive_id("oc_xxx")
            .msg_type("interactive")
            .content(card_json)
            .build()
    ) \\
    .build()

response = client.im.v1.message.create(request)
\\`\\`\\`

### 回复消息
\\`\\`\\`python
request = ReplyMessageRequest.builder() \\
    .message_id("om_xxx") \\
    .request_body(
        ReplyMessageRequestBody.builder()
            .msg_type("text")
            .content('{"text":"回复内容"}')
            .build()
    ) \\
    .build()

response = client.im.v1.message.reply(request)
\\`\\`\\`

### 上传图片/文件
\\`\\`\\`python
# 上传图片
with open("image.png", "rb") as f:
    request = CreateImageRequest.builder() \\
        .request_body(
            CreateImageRequestBody.builder()
                .image_type("message")
                .image(f)
                .build()
        ) \\
        .build()
    response = client.im.v1.image.create(request)
    image_key = response.data.image_key

# 上传文件
with open("doc.pdf", "rb") as f:
    request = CreateFileRequest.builder() \\
        .request_body(
            CreateFileRequestBody.builder()
                .file_type("pdf")
                .file_name("doc.pdf")
                .file(f)
                .build()
        ) \\
        .build()
    response = client.im.v1.file.create(request)
    file_key = response.data.file_key
\\`\\`\\`

## 四、事件处理

### WebSocket 长连接事件处理
\\`\\`\\`python
from lark_oapi.event import BaseEvent

def my_event_handler(req: BaseEvent, resp) -> None:
    event_type = req.header.event_type

    if event_type == "im.message.receive_v1":
        # 接收消息事件
        msg_type = req.event.message.message_type

        if msg_type == "text":
            content = json.loads(req.event.message.content)
            text = content.get("text", "")
            chat_id = req.event.message.chat_id
            message_id = req.event.message.message_id
            # 处理逻辑...
            print(f"收到消息: {text}")

    elif event_type == "im.message.reaction.created_v1":
        # 表情回复事件
        pass

    # 返回 None 表示不回复
    resp.set(None)
\\`\\`\\`

### 卡片回调处理（需 Webhook 模式）
\\`\\`\\`python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook/card", methods=["POST"])
def card_action_callback():
    data = request.get_json()

    # URL 验证
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # 卡片按钮回调
    action_value = data.get("action", {}).get("value", {})
    btn_action = action_value.get("action", "")
    chat_id = data.get("open_chat_id", "")
    user_id = data.get("user_id", {}).get("open_id", "")

    # 处理逻辑...

    # 返回 toast + 可选更新卡片
    return jsonify({
        "toast": {"type": "success", "content": "已处理"},
        # "card": updated_card_json  # 可选
    })
\\`\\`\\`

## 五、用户 API

### 获取用户信息
\\`\\`\\`python
request = GetUserRequest.builder() \\
    .user_id("ou_xxx") \\
    .user_id_type("open_id") \\
    .build()

response = client.contact.v3.user.get(request)
if response.success():
    user = response.data.user
    print(f"姓名: {user.name}")
    print(f"头像: {user.avatar_url}")
    print(f"邮箱: {user.email}")
\\`\\`\\`

### 获取群成员列表
\\`\\`\\`python
request = GetChatMembersRequest.builder() \\
    .chat_id("oc_xxx") \\
    .member_id_type("open_id") \\
    .build()

response = client.im.v1.chat_members.get(request)
\\`\\`\\`

## 六、API 模块速查（完整列表）

| 模块 | 路径 | 主要功能 |
|:---|:---|:---|
| 认证 | auth/v3 | 获取 tenant_access_token |
| 消息 | im/v1/message | 创建/回复/撤回/转发消息 |
| 图片 | im/v1/image | 上传/下载图片 |
| 文件 | im/v1/file | 上传/下载文件 |
| 群聊 | im/v1/chat | 创建/解散/更新群、群成员管理 |
| 通讯录 | contact/v3/user | 用户信息、部门信息 |
| 日历 | calendar/v4 | 日历/日程管理 |
| 文档 | docx/v1 | 云文档操作 |
| 表格 | sheets/v3 | 电子表格操作 |
| 审批 | approval/v4 | 审批流管理 |
| 事件 | event/v1 | 事件订阅管理 |
| 机器人 | bot/v3 | 机器人信息 |

## 七、错误处理最佳实践

\\`\\`\\`python
def safe_send_message(client, chat_id, msg_type, content):
    \\"\\"\\"安全发送飞书消息，含完善错误处理。\\"\\"\\"
    request = CreateMessageRequest.builder() \\
        .receive_id_type("chat_id") \\
        .request_body(
            CreateMessageRequestBody.builder()
                .receive_id(chat_id)
                .msg_type(msg_type)
                .content(content)
                .build()
        ) \\
        .build()

    try:
        response = client.im.v1.message.create(request)
    except Exception as e:
        print(f"[FEISHU ERROR] 网络异常: {e}")
        return False, str(e)

    if response.success():
        return True, response.data.message_id

    # 特殊错误码处理
    error_code = response.code
    if error_code == 99991400:
        print("[FEISHU WARN] Token 过期，需刷新")
    elif error_code == 99991663:
        print("[FEISHU WARN] 无权限，检查应用权限配置")
    elif error_code == 10007:
        print("[FEISHU WARN] 需管理员审批")
    elif error_code == 10203:
        print("[FEISHU WARN] 频率限制，应排队重试")
        time.sleep(1)
        return safe_send_message(client, chat_id, msg_type, content)

    return False, f"{error_code}: {response.msg}"
\\`\\`\\`
""",
}


# ─── 主逻辑 ──────────────────────────────────────────────

def determine_kb_root(force_local: bool = False) -> Path:
    """确定知识库根目录。"""
    if force_local:
        return LOCAL_KB_ROOT
    if os.environ.get("LH_KB_LOCAL"):
        return LOCAL_KB_ROOT
    # 检测是否在鲲鹏上
    if Path("/opt/longhun-system").exists():
        return KB_ROOT
    return LOCAL_KB_ROOT


def fetch_all_sources(kb_root: Path, force: bool = False) -> Dict[str, Any]:
    """抓取所有知识源。"""
    version = load_version(kb_root)
    results = {"fetched_at": datetime.now(timezone.utc).isoformat(), "sources": {}}

    print(f"📚 飞书知识库抓取开始 | 根目录: {kb_root}", flush=True)
    print(f"   上次更新: {version.get('last_fetch', '从未')}", flush=True)
    print(f"   源码数量: {len(KNOWLEDGE_SOURCES)}", flush=True)

    updated_count = 0
    skipped_count = 0
    failed_count = 0

    for source in sorted(KNOWLEDGE_SOURCES, key=lambda s: -s.get("priority", 0)):
        sid = source["id"]
        stype = source["type"]
        sname = source["name"]
        dest = kb_root / source["file"]

        # 检查是否已存在且内容未变化
        if not force and dest.exists():
            print(f"  ⏭️  [{sid}] {sname} (已存在，跳过)", flush=True)
            skipped_count += 1
            results["sources"][sid] = {"status": "skipped", "file": str(dest)}
            continue

        print(f"  ⬇️  [{sid}] {sname} ...", end=" ", flush=True)

        try:
            if stype == "github_raw":
                ok, msg = fetch_github_raw(source, kb_root)
            elif stype == "feishu_api":
                ok, msg = fetch_feishu_api(source, kb_root)
            elif stype == "web_article":
                ok, msg = fetch_web_article(source, kb_root)
            else:
                ok, msg = False, f"未知类型: {stype}"

            if ok:
                print(f"✅ {msg}", flush=True)
                updated_count += 1
                results["sources"][sid] = {"status": "ok", "file": str(dest), "msg": msg}
            else:
                print(f"❌ {msg}", flush=True)
                failed_count += 1
                results["sources"][sid] = {"status": "failed", "msg": msg}

        except Exception as e:
            print(f"💥 {e}", flush=True)
            failed_count += 1
            results["sources"][sid] = {"status": "error", "error": str(e)}

    # 写入内置核心知识卡
    print(f"\n📝 写入核心知识卡 ({len(CORE_KNOWLEDGE_CARDS)} 张)...", flush=True)
    for filename, content in CORE_KNOWLEDGE_CARDS.items():
        dest = kb_root / filename
        ensure_dir(dest.parent)
        dest.write_text(content, encoding="utf-8")
        print(f"  ✅ {filename} ({len(content)} chars)", flush=True)

    # 更新版本
    version["last_fetch"] = datetime.now(timezone.utc).isoformat()
    version["fetch_count"] = version.get("fetch_count", 0) + 1
    version["last_results"] = {
        "updated": updated_count,
        "skipped": skipped_count,
        "failed": failed_count,
    }
    save_version(kb_root, version)

    # 打印摘要
    print(f"\n{'='*50}", flush=True)
    print(f"📊 抓取完成", flush=True)
    print(f"   ✅ 更新: {updated_count}", flush=True)
    print(f"   ⏭️  跳过: {skipped_count}", flush=True)
    print(f"   ❌ 失败: {failed_count}", flush=True)
    print(f"   📂 目录: {kb_root}", flush=True)
    print(f"{'='*50}", flush=True)

    return results


def generate_index(kb_root: Path) -> None:
    """生成知识库索引文件。"""
    index_md = f"""# 龍魂·飞书知识库索引

> 自动生成于 {datetime.now(timezone.utc).isoformat()}
> 根目录: {kb_root}
> 用途: 飞书机器人开发知识底座

## 文件清单

| 文件 | 分类 | 大小 | 来源 |
|:---|:---|:---|:---|
"""
    total_files = 0
    total_size = 0

    for f in sorted(kb_root.glob("*.md")):
        if f.name == VERSION_FILE.replace(".json", ".md"):  # skip index itself
            continue
        size = f.stat().st_size
        total_files += 1
        total_size += size
        size_str = f"{size//1024}KB" if size > 1024 else f"{size}B"
        index_md += f"| {f.name} | — | {size_str} | — |\n"

    for f in sorted(kb_root.glob("*.json")):
        if f.name == VERSION_FILE:
            continue
        size = f.stat().st_size
        total_files += 1
        total_size += size
        size_str = f"{size//1024}KB" if size > 1024 else f"{size}B"
        index_md += f"| {f.name} | — | {size_str} | — |\n"

    index_md += f"\n**总计**: {total_files} 个文件, {total_size//1024}KB\n"

    version = load_version(kb_root)
    index_md += f"\n## 版本信息\n\n"
    index_md += f"- 抓取次数: {version.get('fetch_count', 0)}\n"
    index_md += f"- 上次更新: {version.get('last_fetch', '从未')}\n"
    index_md += f"- 版本号: {version.get('version', '0.0.0')}\n"

    ensure_dir(kb_root)
    (kb_root / "INDEX.md").write_text(index_md, encoding="utf-8")
    print(f"📑 索引已生成: {kb_root / 'INDEX.md'}", flush=True)


def should_fetch(kb_root: Path) -> bool:
    """检查是否需要抓取更新。"""
    version = load_version(kb_root)
    last_fetch = version.get("last_fetch")
    if not last_fetch:
        return True  # 从未抓取过

    try:
        last_dt = datetime.fromisoformat(last_fetch)
        elapsed = datetime.now(timezone.utc) - last_dt.replace(tzinfo=timezone.utc)
        return elapsed.total_seconds() > FETCH_INTERVAL_HOURS * 3600
    except Exception:
        return True


def main():
    parser = argparse.ArgumentParser(
        description="龍魂·飞书知识库抓取引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh_feishu_kb_fetcher.py fetch          # 抓取所有知识源
  lh_feishu_kb_fetcher.py fetch --force  # 强制全量刷新
  lh_feishu_kb_fetcher.py status         # 查看知识库状态
  lh_feishu_kb_fetcher.py check          # 检查是否需要更新（给 cron 用）
        """
    )
    parser.add_argument("action", nargs="?", default="fetch",
                        choices=["fetch", "status", "index", "check"])
    parser.add_argument("--force", action="store_true", help="强制全量刷新，忽略缓存")
    parser.add_argument("--local", action="store_true", help="强制使用本地路径")
    parser.add_argument("--root", type=str, help="指定知识库根目录")

    args = parser.parse_args()

    if args.root:
        kb_root = Path(args.root)
    else:
        kb_root = determine_kb_root(args.local)
    ensure_dir(kb_root)

    if args.action == "status":
        version = load_version(kb_root)
        print(f"📊 飞书知识库状态", flush=True)
        print(f"   根目录: {kb_root}", flush=True)
        print(f"   版本: {version.get('version', '0.0.0')}", flush=True)
        print(f"   上次抓取: {version.get('last_fetch', '从未')}", flush=True)
        print(f"   抓取次数: {version.get('fetch_count', 0)}", flush=True)

        # 文件统计
        md_files = list(kb_root.glob("*.md"))
        json_files = list(kb_root.glob("*.json"))
        total = len(md_files) + len(json_files)
        total_size = sum(f.stat().st_size for f in md_files + json_files)
        print(f"   知识文件: {total} 个 ({total_size//1024}KB)", flush=True)
        print(f"     Markdown: {len(md_files)}", flush=True)
        print(f"     JSON: {len(json_files)}", flush=True)

    elif args.action == "check":
        if should_fetch(kb_root):
            print("FETCH_NEEDED", flush=True)
            sys.exit(0)
        else:
            version = load_version(kb_root)
            last = version.get("last_fetch", "未知")
            print(f"UP_TO_DATE (last: {last})", flush=True)
            sys.exit(1)

    elif args.action == "index":
        generate_index(kb_root)

    elif args.action == "fetch":
        if not args.force and not should_fetch(kb_root):
            version = load_version(kb_root)
            print(f"⏭️  上次抓取于 {version.get('last_fetch')}，间隔不足 {FETCH_INTERVAL_HOURS}h，跳过", flush=True)
            print(f"   使用 --force 强制执行全量刷新", flush=True)
            sys.exit(0)

        results = fetch_all_sources(kb_root, force=args.force)
        generate_index(kb_root)

        # 写入 latest 时间戳
        (kb_root / ".last_fetch").write_text(
            datetime.now(timezone.utc).isoformat()
        )


if __name__ == "__main__":
    main()
