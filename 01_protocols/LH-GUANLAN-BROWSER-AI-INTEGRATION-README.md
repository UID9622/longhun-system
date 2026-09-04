# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 观澜浏览器与AI联动架构协议 v1.0

> DNA: #龍芯⚡️丙午·乙未·丙申·申时·䷸巽-GUANLAN-BROWSER-AI-INTEGRATION-v1.0
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 定位: P0-SOVEREIGN · 浏览器主权协议

## 一句话

观澜 = 隐私主权第一的浏览器 + AI联动调度器。主权在网关，不在像素。

## 四层架构

```
┌─────────────────────────────────────────┐
│  L1 观澜外壳                              │
│  标签页 · 书签 · 阅读模式 · AI侧栏 · 看板  │
├─────────────────────────────────────────┤
│  L2 龍魂网关 (127.0.0.1 本地代理)         │
│  ★ 主权层：流量过滤 · 守护规则 · 记账 · 显化 │
├─────────────────────────────────────────┤
│  L3 AI联动层                              │
│  模型路由 · 断路器 · 输出标注 · 接口槽      │
├─────────────────────────────────────────┤
│  L4 内核层                                │
│  WKWebView / WebView2 / WebKitGTK / ArkWeb │
└─────────────────────────────────────────┘
```

## 五条天条

1. **主权在网关，不在像素** — 渲染内核可换，流量路由必经网关
2. **本地优先，云是增强** — 默认Ollama，云引擎仅在用户允许时启用
3. **AI必须自报家门** — 未标注的输出不可信（AI Truth Protocol）
4. **浏览器是人工端** — 与爬虫账分列，人机两本账
5. **红线随身带** — 安全过滤/守护规则内嵌到网关

## 九大模块 (M1-M9)

| # | 模块 | 类名 | 功能 |
|:---:|:---|:---|:---|
| M1 | 模型路由 | `CNSH_模型路由` | 任务分型→引擎选择→断路器→标注 |
| M2 | 断路器 | `CNSH_断路器` | 连续失败≥3次→熔断600s→自动恢复 |
| M3 | AI标注 | `CNSH_AI标注` | AI Truth Protocol 强制自报家门 |
| M4 | 接口槽 | `CNSH_接口槽` | 新AI引擎注册·三锚核验·ask接口检查 |
| M5 | 插件审计 | `CNSH_插件审计` | 敏感权限≥2→🔴拒装 |
| M6 | 两本账 | `CNSH_两本账` | 人工账(浏览)+爬虫账(蚁爬) 合显看板 |
| M7 | 网关健康 | `CNSH_网关` | fail-closed：网关挂=拒绝联网 |
| M8 | 出域闸门 | `CNSH_出域闸门` | 隐私扫描：身份证/手机号/银行卡/邮箱/地址 |
| M9 | 多模型对比 | `CNSH_多模型对比` | 同问题并排双引擎·分歧高亮·共识度 |

## 四引擎定位

| 引擎 | 角色 | 触发条件 | 位置 |
|:---|:---|:---|:---:|
| Ollama | 本地默认 | 离线/隐私/通用/摘要 | 本地 |
| CodeBuddy | 编码通道 | 代码生成/审查/编码辅助 | 本地 |
| Kimi | 云端增强 | 长文档/研究 | 云 |
| 小艺 | 语音入口 | 鸿蒙HMS语音唤起 | 云→本地 |

## 路由规则

| 任务类型 | 首选引擎 | 故障转移 | 锁定 |
|:---|:---|:---|:---:|
| 代码/审查/编码辅助 | CodeBuddy | →Ollama | — |
| 长文档/研究 | Kimi | →Ollama | — |
| 隐私/离线 | Ollama | 无（不出机） | 🔒本地 |
| 通用/摘要 | Ollama | — | — |
| 语音入口 | 小艺 | →Ollama | — |

## 测试向量 (12/12 🟢)

T01 代码路由→CodeBuddy | T02 长文档→Kimi | T03 隐私→Ollama本地
T04 断路器→转移 | T05 语音入口→小艺 | T06 缺标注→降信
T07 敏感信息→闸门拦截 | T08 网关挂→fail-closed | T09 缺三锚→拒注册
T10 敏感权限≥2→拒装 | T11 人机账分列 | T12 断网→本地可用

## 文件清单

| 文件 | 路径 | 说明 |
|:---|:---|:---|
| 路由引擎 | `bin/lh_guanlan_router.py` | 9模块·12测试·945行 |
| API服务 | `bin/lh_guanlan_api.py` :8770 | RESTful API·11端点 |
| Web仪表盘 | `portal/guanlan/index.html` | 路由可视化·断路器·账本·闸门 |
| 架构协议 | `governance/protocols/P2_system/LH-GUANLAN-BROWSER-AI-INTEGRATION-v1.0.md` | P0协议正文 |
| 数学形式化 | `governance/protocols/P2_system/LH-GUANLAN-BROWSER-MATH-v1.0.md` | M1-M9严格形式化 |

## 启动

```bash
# 测试
python3 bin/lh_guanlan_router.py test    # 12条测试向量
python3 bin/lh_guanlan_router.py demo    # 完整功能演示
python3 bin/lh_guanlan_router.py route 代码  # 单次路由查询

# API服务
python3 bin/lh_guanlan_api.py            # 启动 :8770
python3 bin/lh_guanlan_api.py --test     # API自测试

# 仪表盘
open portal/guanlan/index.html           # 浏览器打开
```
