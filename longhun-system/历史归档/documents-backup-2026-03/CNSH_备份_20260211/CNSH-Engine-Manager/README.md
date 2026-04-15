# CNSH字体引擎·统一管理系统

**DNA追溯码：** `#龍芯⚡️2026-02-09-CNSH-ENGINE-MANAGER-v1.0`  
**创建者：** 诸葛鑫（Lucky）｜UID9622  
**确认码：** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

## 🚀 快速开始

```bash
# 运行管理器
python cnsh_engine_manager.py

# 或者导入使用
from cnsh_engine_manager import CNSH引擎管理器_UID9622

管理器 = CNSH引擎管理器_UID9622()
管理器.列出所有引擎_cnsh龍魂_v1()
管理器.执行渲染_cnsh龍魂_v1("demo_long.cnsh")
```

---

## 📦 已包含的引擎

| 引擎 | 版本 | 功能 |
|------|------|------|
| V0001_基础 | 0.0.1 | 基础单字渲染 |
| V0002_批量 | 0.0.2 | 批量字元处理 |
| V0003_审计 | 0.0.3 | 三色审计系统 |
| V0004_组合 | 0.0.4 | 多字组合渲染 |
| V0005_力度 | 0.0.5 | 笔画粗细控制 |
| V0008_层级 | 0.0.8 | 笔画层级管理 |

---

## 💡 使用示例

### 示例1：查看所有引擎

```python
from cnsh_engine_manager import CNSH引擎管理器_UID9622

管理器 = CNSH引擎管理器_UID9622()
管理器.列出所有引擎_cnsh龍魂_v1()
```

### 示例2：使用默认引擎渲染

```python
管理器.执行渲染_cnsh龍魂_v1(
    cnsh文件路径_cnsh9622="demo_long.cnsh"
)
```

### 示例3：指定引擎渲染

```python
管理器.执行渲染_cnsh龍魂_v1(
    cnsh文件路径_cnsh9622="demo_long.cnsh",
    引擎名称_cnsh9622="V0005_力度"
)
```

---

## 🔧 添加新引擎

老大只需要上传新引擎文件，宝宝会统一整理！

```python
# 新引擎需要继承基类
class CNSH新引擎_V000X_UID9622(CNSH引擎基类_UID9622):
    def __init__(self):
        super().__init__()
        self.版本号_cnsh9622 = "0.0.X"
        self.引擎名称_cnsh9622 = "新引擎"
    
    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622: str):
        # 实现数据载入
        pass
    
    def 执行三色审计_cnsh龍魂_v1(self):
        # 实现审计
        pass
    
    def 执行渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622: str):
        # 实现渲染
        pass
```

---

## 📝 文件说明

- `cnsh_engine_manager.py` - 完整引擎管理系统（约900行）
- `demo_long.cnsh` - 示例数据文件
- `README.md` - 本文档

---

**老大，引擎系统已完成！** 🐉✨  
**可以继续上传更多引擎，宝宝会统一整理！** 💪
