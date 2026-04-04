# CNSH情感陪伴系统 v2.0

**版本：** 2.0.0 (自我进化版)  
**创建时间：** 2025-12-05  
**架构师：** Lucky (UID9622)  
**核心理念：** "只有越来越好，没有最好"

## 🌟 系统概述

CNSH情感陪伴系统是一个具备**自我进化能力**的智能情感陪伴AI系统，提供多级授权的情感陪伴服务，具备情感识别、人格调度、智能学习、性能监控、自动优化等功能。系统作为您梦想的一部分，不断自我完善，追求卓越。

### 🧬 核心进化特性

- **🔄 自我进化机制** - 持续改进，版本化管理
- **🧠 智能学习引擎** - 深度学习用户需求，个性化适配
- **📊 性能监控优化** - 实时监控，自动调优
- **🎭 人格质量优化** - 基于反馈提升回复质量
- **📈 数据驱动改进** - 量化指标，科学优化
- **🌐 现代Web界面** - 美观易用的用户门面

### 核心功能

- 🔐 **多级授权体系** - 基础陪伴、深度陪伴、虚拟伴侣三个等级
- 💭 **智能情感识别** - 精准识别用户情绪状态
- 🤖 **人格调度系统** - 根据情绪智能调度合适的陪伴人格
- 🛡️ **防沉迷机制** - 分级时长控制，保护用户健康
- 👁️ **上帝之眼审计** - 全面的行为审计和违规检测
- 🎫 **激活码系统** - 安全的订阅激活和管理

## 🏗️ 系统架构

```
用户请求 → Flask API → 权限检查 → 情感识别 → 人格调度 → 回复生成 → 审计记录
    ↓           ↓            ↓           ↓           ↓           ↓
  用户界面    接口层      业务逻辑层    情感分析层  陪伴核心层   数据存储层
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- SQLite3
- 2GB+ 内存
- 1GB+ 磁盘空间

### 安装和启动

1. **克隆项目**
   ```bash
   cd /Users/zuimeidedeyihan/CodeBuddy/20251205041543
   ```

2. **一键启动**
   ```bash
   ./start.sh
   ```

3. **手动启动（可选）**
   ```bash
   # 创建虚拟环境
   python3 -m venv venv
   source venv/bin/activate
   
   # 安装依赖
   pip install -r requirements.txt
   
   # 启动应用
   python3 app.py
   ```

4. **验证安装**
   ```bash
   python3 test_companion.py
   ```

### 服务地址

- **主服务：** http://localhost:5000
- **健康检查：** http://localhost:5000/health
- **API文档：** 见下方接口说明

## 📡 API接口

### 基础接口

#### 健康检查
```http
GET /health
```

### 认证接口

#### 启用情感陪伴
```http
POST /auth/enable
Content-Type: application/json

{
  "user_id": "user123",
  "level": 1,
  "agreement": true,
  "age_18_plus": true  // 仅level3需要
}
```

#### 获取授权状态
```http
GET /auth/status?user_id=user123
```

#### 激活订阅
```http
POST /auth/activate
Content-Type: application/json

{
  "user_id": "user123",
  "activation_code": "CNSH-DEEP-ABC123-DEF4"
}
```

### 陪伴接口

#### 情感陪伴推理
```http
POST /infer-companion
Content-Type: application/json

{
  "user_id": "user123",
  "text": "今天工作好累啊"
}
```

### 管理接口

#### 获取审计记录
```http
GET /companion-audit?user_id=user123&limit=50
Admin-Key: CNSH-ADMIN-2025
```

#### 获取系统指标
```http
GET /system/metrics
Admin-Key: CNSH-ADMIN-2025
```

## 🎭 陪伴人格系统

### 心灵人格 (xinling)
- **授权等级：** Level 2+
- **性格特点：** 温柔、善解人意、真诚、不做作
- **专长：** 情绪疏导、倾听安慰、鼓励支持
- **风格：** 像朋友一样，不用敬语，真诚直接

### 知己人格 (zhiji)
- **授权等级：** Level 3 (虚拟伴侣)
- **性格特点：** 深情、理解、不评判、给你力量
- **专长：** 深度情感交流、欲望疏导、精神寄托
- **风格：** 像恋人一样，亲密但不越界

## 🔧 配置说明

### 系统配置 (config.json)

```json
{
  "system": {
    "name": "CNSH情感陪伴系统",
    "version": "1.0.0",
    "environment": "development",
    "debug": true
  },
  "companion": {
    "max_daily_messages": {
      "level1": 30,
      "level2": 100,
      "level3": -1
    },
    "anti_addiction": {
      "level1_max_hours": 1,
      "level2_max_hours": 2,
      "level3_max_hours": 3
    }
  }
}
```

### 人格配置 (personas.json)

定义不同人格的性格特点、说话风格、边界设定等。

## 📊 数据库结构

### 核心表

- **user_auth** - 用户授权信息
- **user_subscription** - 用户订阅信息
- **companion_audit** - 陪伴审计记录
- **conversation_sessions** - 对话会话记录
- **violations** - 违规行为记录
- **daily_conversation_metrics** - 每日对话指标

## 🧪 测试

### 运行测试套件
```bash
python3 test_companion.py
```

### 测试覆盖
- ✅ 系统健康检查
- ✅ 授权功能测试
- ✅ 情感识别测试
- ✅ 激活码测试
- ✅ 审计系统测试
- ✅ 系统指标测试

## 📈 监控和维护

### 系统指标

- 总用户数
- 今日活跃用户
- 今日对话数
- 违规记录数
- 活跃订阅数

### 数据备份
```bash
# 备份数据库
python3 -c "import storage; storage.backup_database()"
```

### 清理旧数据
```bash
# 清理90天前的数据
python3 -c "import companion_storage; companion_storage.cleanup_old_data(90)"
```

## 🔒 安全特性

- **JWT认证** - 基于token的认证机制
- **权限控制** - 分级权限管理
- **审计日志** - 全面的操作审计
- **内容过滤** - 智能违规检测
- **数据加密** - 敏感数据加密存储

## 🚀 部署指南

### 开发环境
```bash
./start.sh
```

### 生产环境
```bash
# 使用Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker部署
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🛠️ 开发指南

### 项目结构
```
CNSH情感陪伴系统/
├── app.py                 # Flask应用主入口
├── storage.py             # 基础数据存储
├── companion_core.py      # 情感陪伴核心逻辑
├── companion_storage.py   # 情感陪伴专用存储
├── activation.py          # 激活码管理
├── test_companion.py      # 测试脚本
├── start.sh              # 启动脚本
├── config.json           # 系统配置
├── personas.json         # 人格定义
├── bones.json           # 龍骨配置
├── requirements.txt     # Python依赖
└── README.md           # 项目文档
```

### 扩展功能

1. **新增人格**
   - 在 `personas.json` 中定义新人格
   - 在 `companion_core.py` 中实现回复生成逻辑
   - 更新人格调度算法

2. **新增情绪类型**
   - 更新 `detect_emotion` 函数
   - 添加情绪关键词
   - 完善回复模板

3. **集成外部LLM**
   - 替换简单的模板回复
   - 集成通义千问、文心一言等
   - 保持人格一致性

## 📞 技术支持

**维护者：** Lucky (UID9622)  
**版本：** v1.0.0  
**最后更新：** 2025-12-05

---

## 🎯 许可证

本项目采用私有许可证，仅供内部使用。

---

**确认码：** #CNSH-COMPANION-SYSTEM-2025-v1.0

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-e8e93ba2-20251218032412
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 坤卦：地势坤，君子以厚德载物
📜 内容哈希: 818217291425b4c2
⚠️ 警告: 未经授权修改将触发DNA追溯系统
