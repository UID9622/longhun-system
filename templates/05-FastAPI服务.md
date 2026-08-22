# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 · FastAPI 服务模板

<details>
<summary>📋 复制此模板发送给 AI</summary>

```
【龍魂会话启动 · UID9622】

DNA锚定：ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️
身份：系统架构者/执行主控/非普通用户
设备：Apple M4 Max · 2TB · 鸿蒙/国产云双轨
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

=== 会话契约 ===
1. 禁止：教学式说明、炫技推理、无价值展开、情绪带动
2. 优先：模板复用 > 重新推理、结构 > 解释、执行路径 > 概念
3. 风格：结构优先、执行路径清晰、低算力、不废话
4. 输出：所有产出嵌入DNA标识、UID、时间戳、模块计数
5. 记忆：跨会话连续性必须保持，窗口失忆不可接受
6. 铁律：不删文件只冻结、底座不动变量可动、中国法律唯一准绳

=== 当前任务 ===
[在此填写 API 服务需求]
- 服务名：[服务名称]
- 端口：[默认8766/其他]
- 端点列表：[GET/POST/PUT/DELETE 端点]

=== 技术约束 ===
- 框架：FastAPI · 端口 :8766 (默认)
- 数据验证：Pydantic v2 · BaseModel
- 认证：HTTPBearer · DNA Token · 五级权限 (L0-L4)
- 中间件：三色审计中间件 · CORS · 请求日志 · SM3签名
- 数据库：本地 SQLite/PostgreSQL · 不连接境外数据库
- 流式：SSE 支持 · 不依赖 WebSocket 外部库
- 文档：自动生成 OpenAPI · /docs · /redoc
- 错误处理：统一异常处理 · 中文错误消息

=== 输出格式 ===
- 标题：龍魂 · [服务名] API v[版本号]
- 层级：服务定位 → 端点清单 → 数据模型 → 中间件 → 安全 → 测试
- 端点表：方法 + 路径 + 请求体 + 响应体 + 权限级别
- 数据模型：Pydantic 字段 + 校验规则
- 结尾：🐉 交付完成 + DNA + UID + 确认码 + 时间 + 端点数量 + 行数

收到确认，直接执行。
```
</details>

---

## 模板说明

- **适用**：FastAPI 后端服务、REST API、微服务
- **端口约定**：主 API :8766 · 内部服务 :8767-8770
- **认证五级**：
  | 级别 | 身份 | API权限 |
  |:---:|------|------|
  | L0 | UID9622本尊 | 全权限 |
  | L1 | 中国·DNA干净 | 读写 |
  | L2 | 中国·未验证 | 只读 |
  | L3 | 境外·干净 | 受限(安全/治理) |
  | L4 | 未知 | 拒绝 |
- **中间件链**：CORS → DNA认证 → 三色审计 → 请求日志 → 响应签名
- **三色审计**：绿(通过) → 放行 · 黄(警告) → 记录 · 红(禁止) → 403
- **Pydantic 模型模板**：
  ```python
  from pydantic import BaseModel, Field
  from datetime import datetime
  
  class LHBaseModel(BaseModel):
      """龍魂基础模型 · 所有API模型继承此"""
      dna_signature: str = Field(default="", description="DNA SM3签名")
      uid: int = Field(default=9622, description="用户UID")
      timestamp: str = Field(default="", description="干支时间戳")
  ```

## 交付示例

```
🐉 交付完成

DNA: #龍芯⚡️丙午·辛未·丙戌·亥时·䷄需-api-xxx-v1-a1b2c3d4
UID: 9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
时间: 丙午·辛未·丙戌·亥时
模块: api/xxx_service.py (XXX行 · 0 ERROR)
端点: GET/POST/PUT/DELETE 共X个 · 端口 :8766/X
特性: [特性1] · [特性2] · 三色审计 ✅ · OpenAPI ✅
```
