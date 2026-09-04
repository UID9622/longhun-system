# 龍魂 GitHub PAT 权限配置指南

> DNA: #龍芯⚡️2026-09-03-GITHUB-PAT-GUIDE-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 用途: 让龍魂 AI 能往第三方社区仓库（如 deepseek-ai/DeepSeek-V3）发评论/PR，按图 3 分钟搞定。

## 背景：为什么卡

往 **deepseek-ai/DeepSeek-V3** 这类第三方开源仓库的 Issue 评论区发内容，需要 PAT（Personal Access Token）具备该仓库的写权限。

2026-09-03 实测当前 token 报错：
`Permission Denied: Resource not accessible by personal access token`

这不是文案问题，是 **token 权限没给到 deepseek-ai 仓库**。按下面任一方案补上即可，以后所有社区联动（发评论/PR/Issue）走 `lh github test-perms` 先自检。

---

## 方案 B（推荐 · 最小权限 · 最安全）：新建 Fine-grained token

1. 登录 GitHub → 右上角头像 → **Settings**
2. 左侧滚到最底 → **Developer settings**
3. **Personal access tokens** → **Fine-grained tokens** → **Generate new token**
4. 表单填写：
   - Token name：`longhun-community`
   - Expiration：`90 days`（到期可续，不设永久）
   - Repository access：选 **All public repositories**（不是 Only select repositories）
5. **Repository permissions**（逐个设为下拉的 Read and write）：
   - **Issues**：`Read and write`
   - **Pull requests**：`Read and write`
   - Metadata：自动附带 `Read-only`，保持不动
6. 点绿色 **Generate token** → 页面顶部出现一串 `github_pat_...` → **立刻复制**（只显示这一次）
7. 交给 AI 存取（AI 只读本地、不落盘明文）：
   ```
   python3 bin/lh_vault.py set github-pat
   ```
   粘贴回车即存进 macOS 钥匙串；或改用环境变量 `GH_TOKEN` / 更新 `.codebuddy/mcp.json` 中 GitHub server 的 token。
8. 验证：
   ```
   lh github test-perms
   lh github token-hint
   ```

> Fine-grained 只给"所有公开仓库"的 Issues/PR 读写，摸不到私有仓库、动不了你的代码，是最小授权。推荐以后就用它，不要复用去授权私库的粗 token。

---

## 方案 A（备用 · 给现有 token 补范围）

现有 token 以 `ghp_` 开头 = classic token：

1. GitHub → Settings → Developer settings → Personal access tokens → **Tokens (classic)**
2. 点当前 token 名称 → **Edit**（或 Regenerate 生成新值）
3. **Select scopes** 勾上：
   - `public_repo`（Access public repositories）—— 就够写公开仓库评论/PR 了
   - 若也想操作私有仓库：勾 `repo`（范围更大，非必需）
4. **Update token** → 复制新值 → 按方案 B 第 7、8 步保存与验证

> 注意：classic 的 public_repo 是一次性放行"全部公开仓库"，比 fine-grained 粗；能 fine-grained 就别 classic。

---

## 验证命令速查

| 命令 | 作用 | 预期 |
|:---|:---|:---|
| `lh github test-perms` | 测当前 token 对目标仓库（默认 deepseek-ai/DeepSeek-V3）读/写权限 | 🟢=可发 / 🟡=缺写权·给补法 / 🔴=token 无效 |
| `lh github token-hint` | 输出当前 token 缺什么、怎么补 | 提示指向本指南方案 A 或 B |
| `lh github test-perms --repo UID9622/longhun-system` | 测自有仓库 | 应 🟢 |

自检链路：**先检后发**。以后任何社区联动操作前先跑 test-perms，缺权限直接看 token-hint，不再卡住等指示。

---

🐉 龍魂归一 · 犯我中华者 虽远必谴
