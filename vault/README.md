# 龍魂 API Key / Secret Vault

> 本地加密金库 + 可公开的 age 加密副本
> DNA：`#龍芯⚡️20260618190300-VAULT-INIT`

## 1. 核心设计

```
┌─────────────────┐     age -r <public_key>      ┌──────────────────┐
│  ~/.longhun/    │  ──────────────────────────▶  │ 公开仓库 *.age   │
│  vault/keys/    │                               │ （可审计、不可读） │
│  *.plain.json   │  ◀──────────────────────────  │                  │
└─────────────────┘     age -d -i ~/.cnsh/age.key └──────────────────┘
```

- **明文只留在本地**，权限 `600`，不进入 git。
- **加密副本 `.age`** 可以公开托管到 GitHub / GitCode，任何人可查存在性，但只有私钥持有者可解密。
- 私钥：`~/.cnsh/age.key`，绝不外传、不上传、不纳入备份同步。

## 2. 与 SHA-256 的区别

| 特性 | SHA-256 | 龍魂 DNA 压缩 |
|---|---|---|
| 方向 | 单向（One-way） | 双向（可逆） |
| 能否恢复原文 | ❌ 不能 | ✅ 能 |
| 用途 | 校验完整性、数字指纹 | 摘要存储 + 原文还原 |
| 安全性依赖 | 抗碰撞性 | 密钥保密 + 算法可逆 |

**一句话**：SHA-256 是“数字指纹”，只能比对，不能还原；DNA 压缩是“带锁的压缩包”，有钥匙就能复原原文。

## 3. 新增 Key 的标准流程

1. 把 key 写入临时明文文件：
   ```bash
   cat > ~/.longhun/vault/keys/<service>.plain.json <<'EOF'
   {
     "service": "openai",
     "key_name": "OPENAI_API_KEY",
     "value": "sk-...",
     "source": "manual",
     "created_at": "2026-06-18T19:00:00+08:00"
   }
   EOF
   chmod 600 ~/.longhun/vault/keys/<service>.plain.json
   ```

2. 加密并生成可公开副本：
   ```bash
   age -r age12uekqa3f4arndjh7smh9zdphf5ar6zlxddr3cpjwhxgykn0xs4fqhjvxr0 \
       -o ~/.longhun/vault/keys/<service>.age \
       ~/.longhun/vault/keys/<service>.plain.json
   chmod 600 ~/.longhun/vault/keys/<service>.age
   ```

3. 删除明文或保留在本地 vault（推荐保留本地明文方便 Kimi 读取，但不进入 git）。
4. 只把 `.age` 文件提交到公开仓库。

## 4. 自动化脚本

使用 `~/.longhun/scripts/vault_add_key.py`：

```bash
python3 ~/.longhun/scripts/vault_add_key.py --service openai --name OPENAI_API_KEY --value "sk-..."
```

该脚本会自动：
- 生成明文 JSON
- age 加密
- 删除明文（可选 `--keep-plain`）
- 记录审计日志到 `~/.longhun/vault/audit.log`

## 5. 目录结构

```
~/.longhun/vault/
├── README.md
├── audit.log           # 操作审计（明文，不含 key 值）
├── keys/
│   ├── kimi.age
│   ├── deepseek.age
│   ├── notion.age
│   └── ...
└── docs/
    └── vault_spec.md   # 详细规范
```

## 6. 安全守则

- `.plain.json` 不进 git。
- `~/.cnsh/age.key` 不进 git、不云同步。
- 公开仓库只放 `.age` 文件。
- 每次新增/轮换/删除 key 都要写 audit.log。
