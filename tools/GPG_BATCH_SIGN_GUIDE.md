# 龍魂批量GPG签名 · 快速指南

## 🎯 目标
将所有.md文件使用GPG密钥A2D0092CEE2E5BA87035600924C3704A8CC26D5F进行批量签名，生成.sig文件。

---

## ⚡ 快速开始

### 步骤 1: 在本地macOS终端执行
```bash
cd ~/longhun-system
python3 tools/batch-sign.py
```

### 步骤 2: 脚本会自动：
1. 扫描所有.md文件（排除.venv、node_modules等临时目录）
2. 为每个文件计算DNA（数字根）和三色
3. 使用GPG密钥进行签名，生成.md.sig文件
4. 生成审计日志到 `logs/batch_audit_YYYYMMDD_HHMMSS.jsonl`

### 步骤 3: 验证签名
```bash
bash tools/batch-verify.sh ~/longhun-system
```

---

## 🔧 如果遇到问题

### 问题 1: "Inappropriate ioctl for device"
**原因**: GPG需要TTY交互（可能需要输入密码）

**解决方案**:
```bash
# 确保在有TTY的终端中运行（不是piped/redirected输入）
# 在macOS Terminal或iTerm2中直接运行，不要用后台 &

cd ~/longhun-system
python3 tools/batch-sign.py
```

### 问题 2: "Need a passphrase"
**原因**: 密钥有密码保护

**解决方案 A**: 系统会弹出密钥管理器，输入密码即可
**解决方案 B**: 预加载密码到gpg-agent
```bash
# 首次运行后，gpg-agent会缓存密码，后续自动使用
```

### 问题 3: 签名文件权限错误
**解决方案**:
```bash
# 确保logs目录可写
chmod 755 ~/longhun-system/logs
```

---

## 📊 输出说明

### 实时输出示例
```
======================================================================
龍魂批量签名系统 · DNA自动化流水线 v1.0
======================================================================
[📋] 扫描完成: 73 个.md文件
[🔐] GPG密钥: A2D0092CEE2E...

[  1] ✅ 🟢 dr=2 | 01_protocols/PROTOCOL__DIGITAL-SOVEREIGNTY-DNA-TRACE-v1.0.md
[  2] ✅ 🟡 dr=5 | 01_protocols/PROTOCOL__AI-HANDSHAKE-BASELINE-v1.0.md
[  3] ✅ 🔴 dr=8 | 01_protocols/PROTOCOL__DNA-L5-ARCHITECTURE-v1.4.md
...
======================================================================
[📊] 统计结果
    总文件数: 73
    签名成功: 73/73
    三色分布: 🟢=16 🟡=30 🔴=27
    数字根分布: {1: 7, 2: 9, 3: 11, 4: 8, 5: 7, 6: 4, 7: 12, 8: 8, 9: 7}

[💾] 审计日志: /Users/zuimeidedeyihan/longhun-system/logs/batch_audit_20260526_142653.jsonl
======================================================================
```

### 生成的文件
- **签名文件**: `*.md.sig` (与原文件并列)
- **审计日志**: `logs/batch_audit_YYYYMMDD_HHMMSS.jsonl`

---

## 🔐 GPG密钥信息

```
密钥ID: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
所有者: 诸葛鑫 (## 🔐 创作者数字身份认证)
类型: RSA 4096-bit
创建: 2025-12-17
用途: 签名 (SC)
```

### 检查密钥可用性
```bash
gpg --list-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

---

## 📋 脚本参数说明

### batch-sign.py
```python
# 核心参数（可在脚本中修改）
root_dir = "~/longhun-system"  # 扫描范围
gpg_key_id = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"  # GPG密钥

# 排除目录（自动跳过）
exclude_dirs = {
    '.venv', 'node_modules', '.git', '__pycache__',
    '.pytest_cache', '.vscode', 'dist', 'build',
    '.idea', 'venv', 'env'
}
```

---

## 💾 审计日志格式

### JSONL 示例
```json
{"timestamp":"2026-05-26T14:25:34.248223","file_path":"01_protocols/PROTOCOL__DIGITAL-SOVEREIGNTY-DNA-TRACE-v1.0.md","abs_path":"/Users/zuimeidedeyihan/longhun-system/01_protocols/PROTOCOL__DIGITAL-SOVEREIGNTY-DNA-TRACE-v1.0.md","dr":2,"color":"🟢","file_hash":"e3f998c4","gpg_sign":{"success":true,"sig_file":"/Users/zuimeidedeyihan/longhun-system/01_protocols/PROTOCOL__DIGITAL-SOVEREIGNTY-DNA-TRACE-v1.0.md.sig","error":null}}
```

### 字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| timestamp | ISO8601 | 签名时间戳 |
| file_path | string | 相对路径 |
| abs_path | string | 绝对路径 |
| dr | int | 数字根 (1-9) |
| color | string | 三色 (🟢/🟡/🔴) |
| file_hash | string | SHA256前8位 |
| gpg_sign.success | bool | 签名是否成功 |
| gpg_sign.sig_file | string | .sig文件路径 |
| gpg_sign.error | string/null | 错误信息 |

---

## 🛠️ 高级用法

### 只签名特定目录
```bash
# 修改 batch-sign.py 中的 priority_dirs
priority_dirs = ['01_protocols', 'cnsh']  # 只处理这些目录
```

### 验证所有签名
```bash
# 使用批量验签脚本
bash tools/batch-verify.sh ~/longhun-system

# 或手动验证单个文件
gpg --verify filename.md.sig filename.md
```

### 导入审计日志到Notion
```python
# 如需集成，使用审计日志的JSONL格式
# 直接导入到Notion数据库（支持JSON格式）
# 字段映射: file_path → Title, dr → Digital Root, color → Color
```

---

## 📞 故障排除

| 症状 | 原因 | 解决方案 |
|------|------|--------|
| 所有签名都失败 | TTY/密码问题 | 在交互式终端运行 |
| 部分签名失败 | 文件权限 | `chmod 755 ~/longhun-system/` |
| 输出乱码 | 编码问题 | 确保终端支持UTF-8 |
| 签名文件为空 | GPG配置问题 | 检查GPG版本：`gpg --version` |

---

## ✅ 执行清单

- [ ] 在macOS终端打开
- [ ] 导航到 `~/longhun-system`
- [ ] 运行 `python3 tools/batch-sign.py`
- [ ] 如需输入密码，按提示输入
- [ ] 等待脚本完成
- [ ] 运行 `bash tools/batch-verify.sh` 验证
- [ ] 检查审计日志：`logs/batch_audit_*.jsonl`

---

**DNA**: #龍芯⚡️2026-05-26-GPG-BATCH-SIGN-GUIDE-v1.0
**责任人**: UID9622

