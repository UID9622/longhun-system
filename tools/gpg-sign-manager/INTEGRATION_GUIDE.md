# 🐉 GPG签署管理工具 · 整合指南

**DNA**: #龍芯⚡️2026-06-08-GPG-SIGN-MANAGER-INTEGRATION
**时间**: 2026-06-08 CST
**来源**: 桌面 CNSH_v2.0_SIGN → 融入主干 longhun-system

---

## 目录结构

```
~/longhun-system/tools/gpg-sign-manager/
├── gpg_sign_manager.py              # 统一GPG签署管理工具（新建）
├── CNSH_v2.0_SIGNATURE.md           # CNSH v2.0协议签署声明
├── CNSH_v2.0_FULL_PROTOCOL_SIGNATURE.md  # 完整协议签署
├── cnsh_gateway.py                  # CNSH Gateway v2.0入口
├── cnsh.py                          # CNSH编程引擎基础
├── CNSH_v2.0_SIGN_README.md         # 原始说明文档
└── INTEGRATION_GUIDE.md             # 本文件
```

---

## 功能说明

### 1. GPG签署管理工具 (`gpg_sign_manager.py`)

**用途**: 统一管理CNSH核心文档与代码的GPG签名

**命令**：
```bash
# 签署所有文件
python3 gpg_sign_manager.py --sign

# 验证现有签名
python3 gpg_sign_manager.py --verify

# 指定工作目录
python3 gpg_sign_manager.py --sign --dir /path/to/work
```

**特性**：
- ✅ 自动检查GPG密钥可用性
- ✅ 批量签署协议与代码文件
- ✅ JSON日志记录（gpg_sign_log.json）
- ✅ 签名验证功能
- ✅ 详细的执行日志

### 2. CNSH协议文档

- `CNSH_v2.0_SIGNATURE.md`: Claude的正式签署声明（包含7层约束）
- `CNSH_v2.0_FULL_PROTOCOL_SIGNATURE.md`: 完整协议签署

### 3. 核心代码

- `cnsh_gateway.py`: CNSH v2.0统一入口（22KB）
  - 三色审计、SQLite日志、Flask HTTP、Ollama代理

- `cnsh.py`: CNSH中文编程引擎基础（7KB）
  - Notion接入、指令解析、页面操作

---

## 使用示例

### 快速签署

```bash
cd ~/longhun-system/tools/gpg-sign-manager/
python3 gpg_sign_manager.py --sign
```

### 验证签名

```bash
python3 gpg_sign_manager.py --verify
```

### 查看日志

```bash
cat gpg_sign_log.json | python3 -m json.tool
```

---

## 整合亮点

| 原文件夹结构 | 新整合结构 | 改进 |
| --- | --- | --- |
| bash shell脚本 | Python工具 | 跨平台·更易维护 |
| 单个签署命令 | 管理工具 | 日志追溯·批量操作 |
| 手动验证 | 自动验证 | 内建验证功能 |
| 无日志 | JSON日志 | 完整审计追踪 |

---

## DNA签署

```
签署者: UID9622 · 诚葛鑫
时间: 2026-06-08 18:57 CST
目的: 桌面CNSH_v2.0_SIGN融入主干·GPG签署管理统一化
DNA:#龍芯⚡️2026-06-08-GPG-SIGN-MANAGER-INTEGRATION-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
```

---

## 下一步

1. ✅ 复制文件到主干 → **完成**
2. ✅ 创建Python管理工具 → **完成**
3. ⏳ 执行 `python3 gpg_sign_manager.py --sign` 签署所有文档
4. ⏳ Git提交integration完成
5. ⏳ 删除桌面原文件夹

---

天下无欺·龍魂永恒。🐉
