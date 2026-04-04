# CNSH 8B5 配件模块 · 功能更新概览

## 📦 模块编号：8B5-詰华配他

**模块代号**: CNSH-ACC-8B5-ZHP  
**更新周期**: 2025年1月第三周  
**适用版本**: CNSH V4.0 + IDE V1.2+  
**兼容状态**: 全兼容，支持热插拔  

---

## 🔌 插件功能更新

### 1. Memory功能模块 🧠

#### 功能描述
自动记住用户偏好与关键信息，持续优化对话体验，支持用户自主控制。

#### 技术实现
```python
# CNSH Memory模块核心代码示例
class CNSHMemoryModule:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.preferences = self._load_user_preferences()
        self.key_information = self._load_key_info()
        
    def remember_preference(self, key, value):
        """记录用户偏好"""
        if self.enabled:
            self.preferences[key] = value
            self._save_preferences()
            
    def apply_context(self, conversation_context):
        """应用记忆到对话上下文"""
        if self.enabled:
            # 添加偏好到系统提示
            context_with_memory = {
                "conversation": conversation_context,
                "user_preferences": self.preferences,
                "key_information": self.key_information
            }
            return context_with_memory
        return conversation_context
        
    def toggle_memory(self, state):
        """开启/关闭记忆功能"""
        self.enabled = state
        self._save_config()
```

#### 设置界面标签
- [ ] 启用记忆功能
- [ ] 记忆保留天数：30天
- [ ] 敏感信息过滤：开启
- [ ] 跨会话记忆：开启

---

### 2. 项目级MCP支持 🗂️

#### 功能描述
允许在项目根目录通过`.mcp.json`文件实现灵活的项目级别配置管理，支持每个项目的个性化设置。

#### 配置文件示例
```json
{
  "projectName": "CNSH_IDE",
  "version": "4.0",
  "mcpSettings": {
    "autoExecution": true,
    "filePatterns": ["*.cnsh", "*.json", "*.md"],
    "excludedDirs": ["node_modules", "__pycache__"],
    "customRules": [
      {
        "name": "中文语法检查",
        "pattern": "[\u4e00-\u9fa5]+",
        "action": "highlight"
      }
    ],
    "integration": {
      "notion": {
        "enabled": true,
        "databaseId": "cnsh-knowledge-base"
      },
      "codebuddy": {
        "autoSync": true,
        "realTimePreview": true
      }
    }
  }
}
```

#### 实现逻辑
```python
class MCPProjectManager:
    def load_project_config(self, project_path):
        mcp_file = os.path.join(project_path, ".mcp.json")
        if os.path.exists(mcp_file):
            with open(mcp_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._default_config()
        
    def apply_project_rules(self, config):
        for rule in config.get("customRules", []):
            self._register_rule(rule)
        
        for integration, settings in config.get("integration", {}).items():
            self._setup_integration(integration, settings)
```

---

### 3. Git高危命令保护 🔒

#### 功能描述
对可能导致代码丢失的Git高危命令执行前需要用户确认，避免意外操作导致的损失。

#### 高危命令列表
- `git reset --hard`
- `git clean -fd`
- `git push --force`
- `git branch -D`
- `git revert --no-edit`
- 任何删除远程分支的操作

#### 实现代码
```python
class GitSafetyManager:
    HIGH_RISK_COMMANDS = [
        "reset --hard",
        "clean -fd",
        "push --force",
        "push -f",
        "branch -D",
        "revert --no-edit"
    ]
    
    def check_command_safety(self, command):
        for risk_pattern in self.HIGH_RISK_COMMANDS:
            if risk_pattern in command:
                return self._request_confirmation(command)
        return True
    
    def _request_confirmation(self, command):
        warning = f"⚠️ 检测到高危Git命令: {command}\n此操作可能导致数据丢失，确认执行吗？"
        # 调用用户确认界面
        return self._show_confirmation_dialog(warning)
```

---

### 4. 用户级Rules系统 📋

#### 功能描述
与项目rules一样支持选择多种类型，允许用户创建个人级规则，不受项目限制。

#### 规则类型分类
1. **语法规则** (Syntax Rules)
   - 中文语法规范检查
   - CNSH语句结构验证
   - 64卦象调用格式

2. **风格规则** (Style Rules)
   - 命名约定
   - 注释格式
   - 代码组织结构

3. **安全规则** (Security Rules)
   - 敏感信息检测
   - 权限边界控制
   - 数据访问限制

4. **文化规则** (Cultural Rules)
   - 易经卦象使用规范
   - 中文表达习惯
   - 传统文化元素应用

#### 规则配置示例
```json
{
  "userRules": {
    "chineseNaming": {
      "type": "style",
      "pattern": "变量名使用中文或拼音",
      "enabled": true,
      "level": "warning"
    },
    "hexagramUsage": {
      "type": "cultural",
      "pattern": "使用卦象时必须包含注释",
      "enabled": true,
      "level": "error"
    },
    "securityBoundary": {
      "type": "security",
      "pattern": "禁止访问系统文件",
      "enabled": true,
      "level": "block"
    }
  }
}
```

---

### 5. 模型能力提示功能 💡

#### 功能描述
通过悬停即可查看模型的详细说明，帮助用户更精准地选择合适的模型。

#### 模型信息卡设计
```javascript
const modelInfo = {
  "CNSH-Compiler": {
    "name": "CNSH编译器模型",
    "description": "专门用于中文自然语言编程和编译，支持CNSH语法解析",
    "strengths": ["中文编程", "易经卦象集成", "64卦状态机"],
    "limitations": ["仅限中文", "不支持底层系统编程"],
    "bestFor": ["CNSH程序开发", "中文算法设计", "文化元素集成"],
    "performance": "高效 | 中文优化"
  },
  "GPT-5-Exec": {
    "name": "GPT-5执行模型",
    "description": "高性能通用模型，适合复杂任务处理和逻辑推理",
    "strengths": ["逻辑推理", "复杂任务处理", "多步骤规划"],
    "limitations": ["中文理解不如CNSH模型"],
    "bestFor": ["系统架构设计", "算法开发", "复杂问题解决"],
    "performance": "超高效 | 通用性强"
  }
};
```

---

## 🖥️ CLI功能增强

### 1. Token分析 (/context) 📊

#### 功能描述
一键查看对话token消耗分布，精准掌控使用成本。

#### 使用方法
```bash
# 查看当前对话的token分布
/context

# 查看详细报告
/context --detailed

# 按模块分析
/context --by-module

# 导出成本报告
/context --export cost_report.json
```

#### 输出示例
```
📊 CNSH Token 使用分析报告
===========================
对话总长度: 15,420 tokens
各模块使用情况:
├── CNSH编译器: 8,530 tokens (55.3%)
├── 64卦象库: 3,210 tokens (20.8%)
├── 记忆系统: 2,180 tokens (14.1%)
├── 安全检查: 1,500 tokens (9.8%)
└── 成本预估: ¥0.77 (按¥0.05/1K tokens)
```

---

### 2. IDE自动连接 (CL1) 🔗

#### 功能描述
CLI与IDE无缝联动，在终端操作的同时IDE自动同步变更。

#### 实现机制
```python
class IDESyncManager:
    def __init__(self):
        self.ide_websocket = self._connect_to_ide()
        self.sync_queue = []
        
    def sync_from_cli(self, file_path, operation):
        """从CLI同步变更到IDE"""
        sync_data = {
            "file": file_path,
            "operation": operation,
            "timestamp": time.time()
        }
        
        # 通过WebSocket发送到IDE
        self.ide_websocket.send(json.dumps(sync_data))
        
        # 等待IDE确认
        response = self.ide_websocket.recv()
        return response["status"] == "success"
        
    def auto_sync_enabled(self):
        """检查是否启用自动同步"""
        return self._get_config_value("auto_sync", True)
```

---

### 3. 主题系统 🎨

#### 功能描述
自由切换深浅色主题，长时间编码更护眼。

#### 主题配置
```json
{
  "themes": {
    "light": {
      "name": "日光模式",
      "background": "#FFFFFF",
      "text": "#2C3E50",
      "code": "#34495E",
      "highlight": "#3498DB",
      "cnshKeyword": "#8E44AD",
      "hexagram": "#D35400"
    },
    "dark": {
      "name": "月夜模式",
      "background": "#1E272E",
      "text": "#F5F6FA",
      "code": "#D1D8E0",
      "highlight": "#74B9FF",
      "cnshKeyword": "#A29BFE",
      "hexagram": "#FD79A8"
    },
    "traditional": {
      "name": "水墨模式",
      "background": "#F8F8F8",
      "text": "#2C3E50",
      "code": "#7F8C8D",
      "highlight": "#2ECC71",
      "cnshKeyword": "#C0392B",
      "hexagram": "#8E44AD"
    }
  }
}
```

---

### 4. Sub-agent增强 🤖

#### 功能描述
复杂任务用强模型、简单任务用快模型，灵活控制成本，以及上下文复用。

#### 模型分配策略
```python
class SubAgentManager:
    MODEL_ASSIGNMENT = {
        "high_complexity": "GPT-5-Exec",      # 复杂任务
        "medium_complexity": "GPT-4-Turbo",   # 中等复杂度
        "low_complexity": "CNSH-Quick",       # 简单任务
        "chinese_specific": "CNSH-Compiler",  # 中文任务
        "code_generation": "CodeBuddy-Exec",  # 代码生成
        "hexagram_analysis": "Yijing-Master"   # 卦象分析
    }
    
    def select_model(self, task):
        complexity = self._assess_complexity(task)
        domain = self._identify_domain(task)
        
        # 根据复杂度和领域选择最优模型
        if complexity > 0.8:
            return self.MODEL_ASSIGNMENT["high_complexity"]
        elif domain == "chinese":
            return self.MODEL_ASSIGNMENT["chinese_specific"]
        elif complexity < 0.3:
            return self.MODEL_ASSIGNMENT["low_complexity"]
        else:
            return self.MODEL_ASSIGNMENT["medium_complexity"]
            
    def context_reuse(self, task_context):
        """复用已有上下文，提高效率"""
        similar_contexts = self._find_similar_contexts(task_context)
        if similar_contexts:
            best_match = max(similar_contexts, key=lambda x: x["similarity"])
            if best_match["similarity"] > 0.85:
                return best_match["context"]
        return task_context
```

---

## 📅 安装与更新流程

### 安装8B5配件模块
```bash
# 下载模块
cnsh package install 8B5-ZHP

# 启用所有功能
cnsh config enable memory mcp git-safety user-rules model-hints

# 重启系统
cnsh restart
```

### 更新配置
```bash
# 检查更新
cnsh update check

# 应用更新
cnsh update apply 8B5-ZHP
```

---

## 🔧 配置与定制

### 全局配置文件 (~/.cnsh/8B5-config.json)
```json
{
  "module": "8B5-ZHP",
  "enabled_features": {
    "memory": true,
    "mcp": true,
    "git_safety": true,
    "user_rules": true,
    "model_hints": true,
    "token_analysis": true,
    "ide_sync": true,
    "themes": true,
    "subagent_optimization": true
  },
  "user_preferences": {
    "default_theme": "traditional",
    "auto_sync": true,
    "cost_warning_threshold": 5.0,
    "preferred_model": "CNSH-Compiler"
  }
}
```

---

## 📈 性能优化与成本控制

### 成本优化策略
1. **智能模型选择** - 根据任务复杂度自动选择最经济模型
2. **上下文复用** - 相似任务复用已有上下文，减少token消耗
3. **批量处理** - 将多个小任务合并为批量操作
4. **缓存机制** - 缓存频繁使用的结果和模型输出

### 性能提升
1. **并行处理** - 多任务并行执行
2. **预加载模型** - 常用模型保持热备状态
3. **增量更新** - 只更新变更部分，减少重新处理
4. **本地缓存** - 常用数据本地缓存，减少网络请求

---

## 🎯 与CNSH系统集成

### 与DNA记忆系统集成
- Memory功能与记忆系统联动
- 用户偏好自动归档到DNA记忆
- 历史记录增强，包含成本和性能数据

### 与64卦象库集成
- 卦象分析任务自动分配给专业模型
- 卦象决策过程记录到因果链
- 文化规则确保卦象使用合规

### 与CNSH编译器集成
- 语法规则与编译器联动
- 中文编程提示增强
- 代码生成优先使用CNSH模型

---

## 📋 已知限制与后续规划

### 当前限制
- MCP配置目前仅支持JSON格式
- 主题系统暂不支持自定义配色
- Sub-agent模型分配基于规则，尚未使用机器学习优化

### 后续规划 (8B6版本)
- 支持YAML格式的MCP配置
- 可视化主题编辑器
- 基于使用习惯的智能模型推荐
- 跨会话记忆增强，支持长期偏好学习

---

**8B5-詰华配他配件模块已准备就绪，立即升级以体验全新功能！** 🚀

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-2f261692-20251218032412
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: 754ec19c1729a6c4
⚠️ 警告: 未经授权修改将触发DNA追溯系统
