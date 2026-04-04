# 🐉 CNSH-DragonSoul-Complete

**龍魂终端 + CNSH编辑器 + Notion扩展 = 完整体**

DNA追溯码: `#龍芯⚡️2026-01-21-CNSH-DragonSoul-v2.0`

---

## ✨ 核心特性

### 🛡️ 安全核心
- **三色审计引擎** - 🟢安全/🟡需确认/🔴阻断
- **DNA追溯系统** - 每个操作都可追溯
- **七维加密** - 多层数据保护
- **数据主权保护** - 数据留在中国境内

### 🤖 五大AI后台
| 后台 | 优先级 | 状态 | 专长 |
|------|--------|------|------|
| Notion AI | 1 | 🟢活跃 | 数据管理 |
| Claude | 2 | 🟢活跃 | 通用智能 |
| DeepSeek | 3 | 🟢活跃 | 中文理解 |
| ChatGPT | 4 | 🔵观察 | 备用 |
| 本地模型 | 5 | 🟡待命 | 离线备份 |

### 🍎 Mac管理
- 清理系统缓存
- 清空回收站
- 获取系统信息
- 管理启动项

### 📝 Notion集成
- 任务管理
- 财务记录
- 实时看板

---

## 📁 项目结构

```
CNSH-DragonSoul-Complete/
├── security-core/           # 🛡️ 安全核心
│   ├── audit_engine.py      # 三色审计引擎
│   ├── dna_tracer.py        # DNA追溯系统
│   └── encryption.py        # 七维加密
│
├── dragonsoul-terminal/     # 🐉 龍魂终端
│   └── backend/
│       ├── five_backends.py # 五大后台调度
│       ├── mac_manager.py   # Mac管理器
│       └── notion_manager.py # Notion管理器
│
├── .vscode/                 # VS Code配置
│   ├── settings.json
│   ├── tasks.json
│   └── launch.json
│
├── config/                  # 配置文件
├── requirements.txt         # Python依赖
├── install.sh              # 一键安装脚本
└── README.md               # 本文件
```

---

## 🚀 快速开始

### 1. 安装

```bash
# 克隆项目
cd /path/to/CNSH-DragonSoul-Complete

# 运行安装脚本
chmod +x install.sh
./install.sh
```

### 2. 配置API密钥

编辑 `.env` 文件：
```bash
CLAUDE_API_KEY=sk-xxx
DEEPSEEK_API_KEY=sk-xxx
NOTION_API_KEY=secret_xxx
```

### 3. 运行

**方式1：命令行**
```bash
python dragonsoul-terminal/backend/main.py
```

**方式2：VS Code**
- 按 `Cmd+Shift+B` 运行默认任务
- 或打开命令面板选择任务

---

## 📖 使用示例

### 三色审计

```python
from security_core.audit_engine import ThreeColorAuditEngine

engine = ThreeColorAuditEngine()

# 安全操作
result = engine.audit("print('hello')")
print(result.level)  # 🟢

# 危险操作
result = engine.audit("rm -rf /")
print(result.level)  # 🔴 阻断
```

### DNA追溯

```python
from security_core.dna_tracer import DNATracer, OperationType

tracer = DNATracer()

# 开始追溯
dna = tracer.start_trace(
    operator="用户",
    operation_type=OperationType.EXECUTE,
    detail="清理缓存"
)

# ... 执行操作 ...

# 结束追溯
tracer.end_trace(dna, output_data={"cleaned": "1GB"})
```

### Mac管理

```python
from dragonsoul_terminal.backend.mac_manager import MacManager

manager = MacManager()

# 获取系统信息
info = manager.get_system_info()
print(f"磁盘: {info['disk']['used']} / {info['disk']['total']}")

# 清理缓存（预览）
result = manager.clean_cache(dry_run=True)
print(f"可清理: {result.cleaned_size} bytes")
```

### 五大后台

```python
import asyncio
from dragonsoul_terminal.backend.five_backends import FiveBackendsScheduler, TaskType

scheduler = FiveBackendsScheduler()

async def main():
    result = await scheduler.execute_task(
        TaskType.CHAT,
        "帮我分析这段代码"
    )
    print(result)

asyncio.run(main())
```

---

## 🎯 VS Code 任务

| 任务 | 描述 |
|------|------|
| 🚀 启动龍魂终端 | 启动主程序 |
| 🧹 清理Mac缓存 | 清理系统缓存 |
| 🛡️ 测试三色审计 | 测试审计引擎 |
| 🧬 测试DNA追溯 | 测试追溯系统 |
| 🔐 测试七维加密 | 测试加密系统 |

---

## 🔒 安全说明

1. **API密钥** - 存储在 `.env` 文件，不要提交到Git
2. **数据加密** - 敏感数据使用七维加密
3. **审计日志** - 所有操作都有DNA追溯码
4. **数据主权** - 数据存储在中国境内

---

## 📝 许可证

MIT License

---

## 👨‍💻 作者

龍芯北辰 (UID9622)

**DNA追溯码**: `#龍芯⚡️2026-01-21-README`
