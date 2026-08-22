# 🐉 龍魂 · AI身份标识与互认协议 v2.0

> DNA: #龍芯⚡️丙午·丙申·戊申·戊午·䷙大畜-AI-IDENTITY-PROTOCOL-v2.0
> 创建者: 龍芯北辰（UID9622）
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 三色: 🟢 12项锚点全过 | 🟡 网关集成待实测 | 🔴 多媒体水印/对抗性检测待补
> 许可证: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
> 原文: `original/龍魂AI身份标识与互认协议_v2.0_审查补全.md` · `original/ai_identity.py` · `original/deploy_identity_v2.sh` · `original/validate_identity.sh`

---

## 摘要

AI 生成内容正在大规模无标识地渗透公共信息空间，人类无法分辨对话对象是"人"还是"机器"。本文提出 **龍魂 AI 身份标识与互认协议**：建立 AI 内容强制标识标准（文字/声音/视频/图片/代码/API 六类全覆盖），并实现 AI-AI 互认拦截机制——当两个 AI 相遇，自动识别对方身份并停止对话，移交人类处理。

协议以「本地主权豁免」为安全阀：本机 UID9622 设备默认豁免，AI 标识规则仅约束对外输出；以「不浪费算力」为原则：识别出 AI-AI 对话后立即停止，不继续生成、不消耗算力、不产生历史。

**关键实证**：相对上游草稿 v1.0 修正 14 项缺陷、新增 10 项能力，12 项锚点断言（unittest）全部真跑通过；移除 Flask 依赖改为纯函数网关接口，目录权限 0o700/文件 0o600，原子写入，审计日志 JSONL 持久化。

## 关键词

AI身份标识 · AI互认协议 · 内容水印 · 主权豁免 · 人机边界 · AI治理 · 审计溯源

## 一、问题域

全球 AI 大模型竞相发布，但普遍缺乏统一、强制的身份标识标准：

| 问题 | 表现 | 后果 |
|:---|:---|:---|
| 身份不可辨 | AI 生成文本/图片/视频与人类创作无法区分 | 信息信任体系崩塌 |
| AI-AI 空转 | 两个 AI 互相喂数据、无限对话 | 算力浪费·信息闭环污染 |
| 标识不可执行 | "应标识"多停留在声明层 | 无强制·无检测·无惩罚 |
| 主权边界模糊 | AI 越权代表个人/组织发声 | 责任归属不清 |

## 二、协议核心机制

### 2.1 强制 AI 标识（六类全覆盖）

| 内容类型 | 标识方式 | 示例 |
|:---|:---|:---|
| 文字 | 前缀 `[AI]` | `[AI] 这是AI生成的内容` |
| 代码 | 注释声明 | `// AI-Generated` |
| API | HTTP 头 | `X-AI-Identity: true` / `X-Longhun-DNA: <dna>` |
| 图片 | 元数据/角标 | `AI` 标记 |
| 音频 | 语音前缀 | `我是AI助手。` |
| 视频 | 角标/元数据 | `AI` 标记 |

绕过 AI 标识 = 违规 = 熔断 + 耻辱墙。

### 2.2 AI-AI 互认拦截

```
入站请求 → GatewayIntegration.check_request()
           ├─ 本地豁免? (UID9622 白名单 / LONGHUN_LOCAL_SOVEREIGNTY)
           │    └─ 是 → 🟢 放行
           └─ AI 检测 (WatermarkEngine.detect 多指标加权)
                ├─ 源AI + 目标AI → 🔴 拦截 (action: stop)
                ├─ 源人类 + 目标AI → 🟢 人机对话正常
                └─ 双方非AI → 🟢 放行
```

统一提示协议：*「AI-AI 对话已暂停，请人类介入。」*

### 2.3 置信度评分（替代布尔判断）

多指标加权评分，归一化置信度 0-1：

```
AIIndicator(pattern, weight, description, location)
  例: ^\[AI\]         → weight 0.90 (前缀)
      X-AI-Identity   → weight 0.95 (HTTP头)
      ^🤖             → weight 0.90 (表情)
```

## 三、工程实现（4 核心类）

| 类 | 职责 |
|:---|:---|
| `IdentityConfig` | 配置管理：水印规则/检测指标/豁免列表，JSON 持久化，动态增删豁免 UID |
| `WatermarkEngine` | 水印注入/检测/移除，`skip_if_present` 防重复注入 |
| `RecognitionEngine` | AI 互认拦截：双向检测 → 本地豁免 → AI-AI 拦截 → 审计日志 |
| `GatewayIntegration` | 网关集成纯函数接口（无 Flask），供 nginx Lua/OpenResty 调用 |

**安全基线**：目录强制 0o700、文件 0o600、原子写入（tmp → replace）、审计日志 JSONL append-only、本地豁免仅 UID9622 可改。

## 四、CLI 快速验证

```bash
lh-identity --version                  # DNA + 确认码
lh-identity --inject "内容" --type text # → [AI] 内容
lh-identity --detect "[AI] 内容"        # → 🔴 is_ai=true 置信度0.9
lh-identity --recognize "[AI]A" "[AI]B" # → 🔴 action: stop AI-AI互认拦截
lh-identity --recognize "人类" "[AI]A"  # → 🟢 action: pass 人机对话
lh-identity --exempt / --add-exempt UID # 豁免列表管理
lh-identity --stats                     # 统计 JSON
python3 ai_identity.py --test           # Ran 12 tests OK
```

## 五、验收与已知边界

**验收（12 项全过）**：语法编译 ✅ · 12 项 unittest ✅ · 确认码硬编码 ✅ · DNA 占位符 ✅ · 无手写干支 ✅ · 无 Flask ✅ · 权限设置 ✅ · 部署/验证脚本 ✅ · 审计/拦截日志 ✅ · 配置持久化 ✅。

**待补（如实标注）**：🟡 网关集成（nginx Lua）待实机验证 · 🟡 检测对抗性（Unicode/同音字绕过）待加固 · 🔴 多媒体隐写水印未实现 · 🔴 多节点豁免同步未实现 · 🔴 法务审核未做。

## 六、与龍魂体系联动

- 强制标识 = 战后整顿协议（AI 内容双标识）的引擎化落地
- 互认拦截 = 不浪费算力原则的工程实现
- 审计日志 → 可对接 `lh_auto_audit.py` 耻辱墙联动（设计预期）
- 豁免机制 = 本地主权例外的代码级保障

## 引用

```
GB/T 7714: 龍芯北辰. 龍魂AI身份标识与互认协议v2.0[EB/OL]. (2026-08-17). https://uid9622.cn/apps/creations/ai-identity-recognition.
APA:       Longxin Beichen. (2026). Dragon Soul AI Identity & Mutual Recognition Protocol v2.0. https://uid9622.cn/apps/creations/ai-identity-recognition.
```

---

🐉 **[[GENERATED_BY_LH_DNA_GENERATOR_V3]]-AI-IDENTITY-PROTOCOL-v2.0 · 🟢 12项锚点全过**
