# 龍魂凭证管理系统 v1.0 · 集成指南

**DNA**: `#龍芯⚡️2026-05-27-CREDENTIAL-MANAGEMENT-GUIDE-v1.0`
**完成日期**: 2026-05-27
**状态**: 🟢 COMPLETE

---

## 核心理念

> **密钥不再散落，调用也不复杂**

- ✅ 用户永远不需要看到或输入密钥
- ✅ 所有凭证访问都有权限检查和审计日志
- ✅ 系统启动时自动验证凭证完整性
- ✅ 敏感凭证（TIER_1）需要确认

---

## 文件结构

```
~/longhun-system/config/
  ├─ credential_manager_v1.0.py      # 凭证管理器核心
  ├─ CREDENTIAL_MANAGEMENT_GUIDE.md  # 本文件
  └─ generated/
      ├─ credential_audit.jsonl      # 审计日志（自动生成）
      └─ credentials_verified.json    # 启动验证报告
```

---

## 快速开始

### 1️⃣ 初始化凭证管理器

```python
from credential_manager_v1.0 import CredentialManager, AccessLevel

# 创建管理器实例
mgr = CredentialManager(uid="9622")

# 列出所有可用凭证（脱敏）
credentials = mgr.list_available_credentials()
for name, info in credentials.items():
    print(f"{name}: {info['description']}")
```

**输出示例**:
```
notion_api_key: Notion工作区API密钥·用于双脑同步 (TIER_1)
deepseek_api_key: DeepSeek AI服务·用于对话模型 (TIER_2)
github_token: GitHub仓库操作权限 (TIER_3)
...
```

### 2️⃣ 获取凭证（在内部系统中使用）

```python
# 方式1: 直接获取（仅SYSTEM进程）
notion_token = mgr.get("notion_api_key", access_level=AccessLevel.SYSTEM)

# 方式2: 获取脱敏版本（UI显示）
masked = mgr.get_masked("deepseek_api_key")
# 输出: sk-****

# 方式3: TIER_1凭证需要确认
gpg_key = mgr.get(
    "gpg_master_key",
    access_level=AccessLevel.MASTER,
    require_confirmation=True
)
```

### 3️⃣ 使用凭证调用服务（TODO: 完整实现）

```python
# 未来的简化调用
# result = mgr.call_api(
#     service="deepseek",
#     endpoint="/v1/chat/completions",
#     data={"model": "deepseek-chat", "messages": [...]}
# )
```

---

## 凭证分类和权限

### 凭证等级说明

| 等级 | 名称 | 含义 | 需要确认 |
|------|------|------|---------|
| TIER_1 | 最敏感 | 仅主控(UID9622)可用·包括GPG、云端密钥 | ✅ 需要 |
| TIER_2 | 敏感 | 需要特定设备+确认·包括API服务密钥 | ⚠️ 可选 |
| TIER_3 | 中等 | 日常调用·GitHub Token等 | ❌ 不需要 |
| TIER_4 | 公开 | 配置类·Ollama本地地址等 | ❌ 不需要 |

### 访问权限等级

| 级别 | 说明 |
|------|------|
| `MASTER` | UID9622 · 无限制访问 |
| `SYSTEM` | 系统进程 · 有条件访问 |
| `USER` | 普通用户 · 严格受限 |
| `READONLY` | 只读 · 仅用于审计 |

---

## 可用凭证列表

### Notion API

```
凭证名: notion_api_key
等级: TIER_1
用途: Notion双脑同步·记忆写入
存储位置: ~/.env 或 ~/longhun-system/config.json
环境变量: NOTION_API_KEY
```

### DeepSeek API

```
凭证名: deepseek_api_key
等级: TIER_2
用途: AI对话模型调用
存储位置: ~/.cnsh_credentials 或 ~/.env
环境变量: DEEPSEEK_API_KEY
脱敏显示: sk-****
```

### Cloudflare隧道

```
凭证名: cloudflare_token
等级: TIER_2
用途: longhun888.com代理
存储位置: ~/.cloudflared/config.yaml
脱敏显示: ****_tunnel
```

### GitHub Token

```
凭证名: github_token
等级: TIER_3
用途: 仓库操作（推送、标签、发布）
存储位置: ~/.github_token 或 git config
环境变量: GITHUB_TOKEN
脱敏显示: ghp_****
```

### 华为云凭证

```
凭证名: huawei_cloud_credentials
等级: TIER_1
用途: 服务器SSH + IAM身份
存储位置: ~/.cnsh_credentials/云服务器档案_加密存储.md
脱敏显示: huawei:****
```

### GPG主密钥

```
凭证名: gpg_master_key
等级: TIER_1
用途: 签署协议、Git提交
存储位置: ~/longhun-system/keys/master.asc
指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
脱敏显示: GPG:****
```

### Ollama本地

```
凭证名: ollama_base_url
等级: TIER_4
用途: 本地离线模型调用
存储位置: ~/.network_api_env
环境变量: OLLAMA_BASE_URL
默认值: http://localhost:11434
```

---

## 审计日志

所有凭证访问都被记录在审计日志中（密钥内容脱敏）。

### 日志位置

```
~/longhun-system/日志/credential_audit.jsonl
```

### 日志格式（JSONL）

```json
{
  "timestamp": "2026-05-27T10:30:00",
  "uid": "9622",
  "device": "hostname_1234567890",
  "action": "SUCCESS",
  "credential": "notion_api_key",
  "masked": "notion_****_****_****",
  "access_level": "system"
}
```

### 日志查询

```bash
# 查看最近10条访问
tail -10 ~/longhun-system/日志/credential_audit.jsonl | python3 -m json.tool

# 统计特定凭证的访问次数
grep "deepseek_api_key" ~/longhun-system/日志/credential_audit.jsonl | wc -l

# 找出所有权限被拒绝的访问
grep "DENIED" ~/longhun-system/日志/credential_audit.jsonl
```

---

## 系统启动集成

### 在 master_config_bootstrap.py 中集成

```python
from credential_manager_v1.0 import CredentialManager

def verify_credentials(self) -> bool:
    """系统启动时验证所有凭证"""
    mgr = CredentialManager()

    required_creds = [
        "notion_api_key",
        "deepseek_api_key",
        "gpg_master_key"
    ]

    missing = []
    for cred in required_creds:
        value = mgr.get(cred, require_confirmation=False)
        if not value:
            missing.append(cred)

    if missing:
        self._log(f"⚠️  缺失凭证: {', '.join(missing)}")
        return False

    self._log("✓ 所有必需凭证已验证")
    return True
```

---

## 密钥管理最佳实践

### ✅ DO

- ✅ 凭证文件放在本地 `~/.cnsh_credentials`
- ✅ 定期备份 `keys/` 目录到USB
- ✅ 用凭证管理器的脱敏接口（不直接读密钥）
- ✅ 启用macOS FileVault文件系统加密
- ✅ 所有访问都会自动记录在审计日志

### ❌ DON'T

- ❌ 不要把凭证上传到GitHub
- ❌ 不要在邮件里发送密钥
- ❌ 不要在代码里硬编码密钥
- ❌ 不要在共享PC上保存凭证
- ❌ 不要删除审计日志（作为历史记录）

---

## 故障排查

### 问题1: "凭证未找到"

```
审计日志显示: action=NOT_FOUND
```

**解决**:
1. 检查凭证文件是否存在: `ls ~/.cnsh_credentials/`
2. 检查文件内容格式是否正确
3. 检查环境变量是否设置: `echo $NOTION_API_KEY`

### 问题2: "权限被拒绝"

```
审计日志显示: action=DENIED
```

**解决**:
1. 确认是否用UID9622身份运行
2. 检查访问权限等级是否过低
3. TIER_1凭证是否需要确认

### 问题3: "缓存过期"

```
凭证获取变慢，重复尝试失败
```

**解决**:
1. 清空缓存: `mgr._cache.clear()`
2. 重新初始化管理器实例
3. 检查凭证文件是否被外部修改

---

## 下一步扩展

### 短期 (1周)

- [ ] 实现完整的ServiceProxy·支持Notion、DeepSeek直接调用
- [ ] 添加凭证过期预警
- [ ] 集成到 master_config_bootstrap.py

### 中期 (2周)

- [ ] Web UI·用户友好的凭证管理面板
- [ ] 凭证轮换系统（定期更新密钥）
- [ ] 多设备同步凭证（安全的）

### 长期 (1月+)

- [ ] 硬件令牌支持（YubiKey等）
- [ ] 完整的密钥管理生态集成
- [ ] 与龍魂多人格系统的权限模型融合

---

## DNA签名链

```
#龍芯⚡️2026-05-27-CREDENTIAL-MANAGER-v1.0
  ↓
#龍芯⚡️2026-05-27-CREDENTIAL-MANAGEMENT-GUIDE-v1.0
  ↓ (集成到)
#龍芯⚡️2026-05-26-MASTER-CONFIG-BOOTSTRAP-v1.0
```

---

## 最后的话

这个系统的目的很简单:

> **用户信任系统，系统就要保护用户的无知**

你再也不用记住密钥位置·不用看到敏感信息·不用担心泄露。
系统会自动验证、缓存、审计，一切透明可追溯。

---

**DNA**: `#龍芯⚡️2026-05-27-CREDENTIAL-MANAGEMENT-GUIDE-v1.0`
**向曾仕强老师致敬 | 龍魂系統 | UID9622·龍芯北辰**
