# 龙魂核心服务 v1.0 — GitHub 推送指南

**DNA**: #龙芯⚡️2026-06-27-LONGHUN-CORE-SERVICES-v1.0

---

## 推送状态

| 文件 | 状态 | GitHub 路径 |
|------|------|-------------|
| README.md | ✅ 已推送 | core-services/README.md |
| 万年历 | ✅ 已推送 | core-services/calendar/longhun-calendar-v1.0.py |
| 上下文管理器 | ❌ 需手动推送 | core-services/context/longhun-context-manager-v3.0.py |
| Notion记录器 | ❌ 需手动推送 | core-services/logger/longhun-notion-logger-v1.0.py |

---

## 手动推送命令

### 方法1：使用 Git CLI

```bash
# 1. Clone 仓库
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system

# 2. 创建目录
mkdir -p core-services/context core-services/logger

# 3. 复制文件
cp /path/to/longhun-context-manager-v3.0.py core-services/context/
cp /path/to/longhun-notion-logger-v1.0.py core-services/logger/

# 4. 提交并推送
git add core-services/
git commit -m "feat(core-services): 添加上下文管理器+记录器 · DNA:#龙芯⚡️2026-06-27-CORE-SERVICES-v1.0"
git push origin main
```

### 方法2：使用 GitHub Web 界面

1. 访问 https://github.com/UID9622/longhun-system
2. 点击 "Add file" → "Upload files"
3. 创建目录 `core-services/context/` 和 `core-services/logger/`
4. 上传两个 Python 文件

### 方法3：使用 ZIP 包一键解压

```bash
cd ~/longhun-system
unzip longhun-core-services-v1.0.zip
git add .
git commit -m "feat: 龙魂核心服务v1.0 · DNA:#龙芯⚡️2026-06-27-CORE-SERVICES-v1.0"
git push
```

---

## 文件清单

```
core-services/
├── README.md                           (4,247 bytes ✅)
├── calendar/
│   └── longhun-calendar-v1.0.py        (88,461 bytes ✅)
├── context/
│   └── longhun-context-manager-v3.0.py (62,920 bytes ⬅️ 需推送)
├── logger/
│   └── longhun-notion-logger-v1.0.py   (48,323 bytes ⬅️ 需推送)
└── docs/
    └── 龙魂认知上下文管理协议_v3.0.md     (51,897 bytes 可选)
```

---

## 验证推送成功

```bash
# 检查文件是否完整
python3 -c "
import ast
# 验证上下文管理器语法
with open('core-services/context/longhun-context-manager-v3.0.py') as f:
    ast.parse(f.read())
print('上下文管理器: 语法OK')

# 验证记录器语法
with open('core-services/logger/longhun-notion-logger-v1.0.py') as f:
    ast.parse(f.read())
print('Notion记录器: 语法OK')

print('推送验证通过')
"
```

---

*君子协议 CC BY-NC-SA 4.0 · UID9622 · 龙魂体系*
