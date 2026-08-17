# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂官网AI助手 · 嵌入指南
# DNA: #龍芯⚡️丙午·丙申·戊午·申时·䷗复-EMBED-GUIDE-v1.0

## 一、后端启动

```bash
# 本地直接运行
cd /opt/longhun-system
python3 bin/lh_knowledge_hub_api.py

# 或 systemd（推荐）
sudo cp deploy/systemd/longhun-knowledge-hub.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now longhun-knowledge-hub
sudo systemctl status longhun-knowledge-hub
```

## 二、Nginx 反向代理（官网同域部署）

```nginx
location /api/v1/li/ {
    proxy_pass http://127.0.0.1:8766/v1/li/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 60s;
}
```

## 三、官网嵌入

在官网 HTML 底部 `</body>` 前插入：

```html
<!-- 方式1: 直接内联 -->
<!-- 复制 portal/chat-widget-v3.html 全部内容到此处 -->

<!-- 方式2: 外链引入 -->
<link rel="stylesheet" href="/widget/chat-widget-v3.html">
<script src="/widget/chat-widget-v3.html" defer></script>
```

**关键配置**：修改 CONFIG.API_BASE
- 同域部署：`'/api'`（通过 Nginx 代理）
- 跨域部署：`'https://uid9622.cn/api'`（需确保 CORS 已开）

## 四、接口速查

| 方法 | 路径 | 说明 |
|:---|:---|:---|
| POST | /api/v1/li/chat | 对话（JSON） |
| POST | /api/v1/li/chat/stream | 流式对话（SSE） |
| GET | /api/v1/li/personas | 人格列表 |
| GET | /api/v1/li/knowledge/search?q=关键词 | 知识检索 |
| GET | /api/v1/li/status | 系统状态 |

## 五、请求格式

```json
POST /api/v1/li/chat
{
  "message": "龍魂系统是什么？",
  "persona": "generalist",    // 可选，不填自动匹配
  "session_id": "s123456_abc" // 可选，用于上下文记忆
}
```

## 六、响应格式

```json
{
  "reply": "龍魂是诸葛鑫创建的AI操作系统...",
  "model": "longhun:latest",
  "persona": "龍魂助手",
  "persona_id": "generalist",
  "dna": "#龍芯⚡️CHAT-a1b2c3d4",
  "knowledge_used": 2,
  "time_ms": 423
}
```

## 七、人格列表

| ID | 名称 | 触发词 |
|:---|:---|:---|
| generalist | 龍魂助手 | 默认 |
| auditor | 审计师·P05 | 审计/检查/合规/安全 |
| coder | 架构师·P04 | 写代码/生成/脚本/实现 |
| philosopher | 哲人·P11 | 卦/易经/哲理/推演 |
| guardian | 龍盾·P72 | 熔断/威胁/安全事件 |
| teacher | 导师·P02+P11 | 教我/教学/大白话/新手 |
