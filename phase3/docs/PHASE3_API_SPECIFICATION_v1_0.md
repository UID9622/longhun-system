<!--#龍芯⚡️2026-06-21-DOC-PHASE3_API_SPECIFICATION_V1_0-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

# 龍魂系統 Phase 3 - API 规范 v1.0

```yaml
openapi: 3.0.0
info:
  title: 龍魂系統 API
  description: |
    龍魂系統完整 API 规范
    - 实时仪表板数据
    - 技能管理与执行
    - 告警系统
    - 日志查询
    - 数据导出
  version: 3.0.0
  contact:
    name: UID9622 (龍芯北辰)
    url: https://github.com/UID9622/longhun-system
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: http://localhost:8000
    description: 本地开发环境
  - url: https://api.longhun-system.com
    description: 生产环境

tags:
  - name: Dashboard
    description: 系统仪表板相关接口
  - name: Skills
    description: 技能管理接口
  - name: Alerts
    description: 告警系统接口
  - name: Logs
    description: 日志查询接口
  - name: Export
    description: 数据导出接口
  - name: Settings
    description: 系统设置接口
  - name: Auth
    description: 认证与授权接口

paths:
  /api/v1/health:
    get:
      tags:
        - Dashboard
      summary: 系统健康检查
      description: 返回系统当前状态
      responses:
        '200':
          description: 系统正常
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    enum: [healthy, degraded, down]
                  timestamp:
                    type: string
                    format: date-time
                  cpu:
                    type: number
                    description: CPU 使用率 (0-100)
                  memory:
                    type: number
                    description: 内存使用率 (0-100)
                  disk:
                    type: number
                    description: 磁盘使用率 (0-100)
                  uptime_seconds:
                    type: integer
                    description: 系统运行时间（秒）
                  active_skills:
                    type: integer
                    description: 当前活跃技能数
                  total_executions:
                    type: integer
                    description: 总执行次数
                  success_rate:
                    type: number
                    description: 执行成功率 (0-100)

  /api/v1/dashboard:
    get:
      tags:
        - Dashboard
      summary: 获取仪表板数据
      description: 返回仪表板需要的所有实时数据
      parameters:
        - name: time_range
          in: query
          schema:
            type: string
            enum: [1h, 6h, 24h, 7d, 30d]
          description: 时间范围
      responses:
        '200':
          description: 仪表板数据
          content:
            application/json:
              schema:
                type: object
                properties:
                  metrics:
                    type: object
                    description: 核心指标
                  recent_executions:
                    type: array
                    description: 最近执行记录
                  active_alerts:
                    type: array
                    description: 活跃告警
                  performance_chart:
                    type: object
                    description: 性能数据

  /api/v1/skills:
    get:
      tags:
        - Skills
      summary: 列表技能
      description: 获取所有注册的技能列表
      parameters:
        - name: platform
          in: query
          schema:
            type: string
          description: 按平台筛选 (kimi/claude/ollama/longhun)
        - name: status
          in: query
          schema:
            type: string
          description: 按状态筛选 (active/inactive/deprecated)
      responses:
        '200':
          description: 技能列表
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Skill'
    post:
      tags:
        - Skills
      summary: 创建新技能
      description: 注册一个新技能
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SkillInput'
      responses:
        '201':
          description: 技能创建成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Skill'
        '400':
          description: 请求参数错误
        '401':
          description: 未授权

  /api/v1/skills/{skill_id}:
    get:
      tags:
        - Skills
      summary: 获取技能详情
      parameters:
        - name: skill_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: 技能详情
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Skill'
        '404':
          description: 技能不存在

  /api/v1/skills/{skill_id}/execute:
    post:
      tags:
        - Skills
      summary: 执行技能
      parameters:
        - name: skill_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                args:
                  type: object
                  description: 技能参数
      responses:
        '202':
          description: 技能已提交执行
          content:
            application/json:
              schema:
                type: object
                properties:
                  execution_id:
                    type: string
                  status:
                    type: string
                    enum: [queued, running, completed, failed]

  /api/v1/executions/{execution_id}:
    get:
      tags:
        - Skills
      summary: 获取执行状态
      parameters:
        - name: execution_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: 执行状态
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Execution'

  /api/v1/alerts:
    get:
      tags:
        - Alerts
      summary: 列表告警
      parameters:
        - name: level
          in: query
          schema:
            type: string
            enum: [critical, high, medium, low]
        - name: status
          in: query
          schema:
            type: string
            enum: [active, acknowledged, resolved]
      responses:
        '200':
          description: 告警列表
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Alert'

  /api/v1/alerts/{alert_id}/acknowledge:
    post:
      tags:
        - Alerts
      summary: 确认告警
      parameters:
        - name: alert_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: 告警已确认

  /api/v1/logs:
    get:
      tags:
        - Logs
      summary: 查询日志
      parameters:
        - name: skill_id
          in: query
          schema:
            type: string
        - name: level
          in: query
          schema:
            type: string
            enum: [debug, info, warning, error]
        - name: start_time
          in: query
          schema:
            type: string
            format: date-time
        - name: end_time
          in: query
          schema:
            type: string
            format: date-time
        - name: limit
          in: query
          schema:
            type: integer
            default: 100
      responses:
        '200':
          description: 日志列表
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Log'

  /api/v1/export/csv:
    post:
      tags:
        - Export
      summary: 导出为 CSV
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                data_type:
                  type: string
                  enum: [executions, alerts, logs]
                filters:
                  type: object
      responses:
        '200':
          description: CSV 文件
          content:
            text/csv:
              schema:
                type: string

  /api/v1/export/json:
    post:
      tags:
        - Export
      summary: 导出为 JSON
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
      responses:
        '200':
          description: JSON 数据
          content:
            application/json:
              schema:
                type: object

  /api/v1/settings:
    get:
      tags:
        - Settings
      summary: 获取系统设置
      responses:
        '200':
          description: 系统设置
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Settings'
    put:
      tags:
        - Settings
      summary: 更新系统设置
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Settings'
      responses:
        '200':
          description: 设置已更新

  /api/v1/auth/login:
    post:
      tags:
        - Auth
      summary: 登录
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
      responses:
        '200':
          description: 登录成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  token_type:
                    type: string
                    enum: [bearer]

  /ws/v1/stream:
    description: WebSocket 实时数据流
    servers:
      - url: ws://localhost:8000
      - url: wss://api.longhun-system.com

components:
  schemas:
    Skill:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        platform:
          type: string
        category:
          type: string
        priority:
          type: integer
        status:
          type: string
        last_executed:
          type: string
          format: date-time
        execution_count:
          type: integer
        success_rate:
          type: number
        dna:
          type: string

    SkillInput:
      type: object
      required:
        - id
        - name
        - platform
      properties:
        id:
          type: string
        name:
          type: string
        platform:
          type: string
        category:
          type: string
        priority:
          type: integer
          minimum: 1
          maximum: 10

    Execution:
      type: object
      properties:
        id:
          type: string
        skill_id:
          type: string
        status:
          type: string
          enum: [queued, running, completed, failed]
        start_time:
          type: string
          format: date-time
        end_time:
          type: string
          format: date-time
        duration_ms:
          type: integer
        result:
          type: object
        error:
          type: string

    Alert:
      type: object
      properties:
        id:
          type: string
        level:
          type: string
          enum: [critical, high, medium, low]
        message:
          type: string
        source:
          type: string
        status:
          type: string
          enum: [active, acknowledged, resolved]
        created_at:
          type: string
          format: date-time
        acknowledged_at:
          type: string
          format: date-time

    Log:
      type: object
      properties:
        id:
          type: string
        level:
          type: string
        message:
          type: string
        skill_id:
          type: string
        timestamp:
          type: string
          format: date-time
        dna:
          type: string

    Settings:
      type: object
      properties:
        alert_email:
          type: string
          format: email
        alert_webhook:
          type: string
          format: uri
        log_retention_days:
          type: integer
        max_concurrent_skills:
          type: integer
        backup_enabled:
          type: boolean

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

---

## 📋 API 规范总结

| 端点组 | 端点数 | 功能 |
|--------|--------|------|
| Dashboard | 1 | 仪表板数据·健康检查 |
| Skills | 5 | 技能列表·创建·执行·状态 |
| Alerts | 2 | 告警列表·确认 |
| Logs | 1 | 日志查询 |
| Export | 2 | CSV·JSON 导出 |
| Settings | 2 | 获取·更新设置 |
| Auth | 1 | 用户认证 |
| WebSocket | 1 | 实时数据流 |

**总计**: 15 个 REST 端点 + 1 个 WebSocket 端点

---

## 🔐 安全考虑

```
认证: JWT Bearer Token
授权: 基于角色的访问控制 (RBAC)
加密: HTTPS/WSS
速率限制: 100 req/min per IP
CORS: 严格来源检查
日志: 所有 API 调用都记录 DNA 签章
```

---

**这份 API 规范可以直接用于：**
1. ✅ FastAPI 后端开发
2. ✅ React 前端集成
3. ✅ 自动化测试生成
4. ✅ Swagger UI 文档
5. ✅ 客户端 SDK 生成

---

**现在开始创建后端实现代码...**
