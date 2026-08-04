# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂仓库拆分方案 · Repo Split Plan

> **DNA**: `#龍芯⚡️2026-06-24-REPO-SPLIT-PLAN-v1.0`
> **GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> **诊断**: Gitee 显示 1492MB / 配额 1024MB，当前 HEAD 仅 55MB，差异来自历史未引用对象

---

## 当前状况

| 指标 | 数值 |
|---|---|
| 当前 `HEAD` 文件总大小 | ~55 MB |
| Gitee 后台显示仓库大小 | ~1492 MB |
| Gitee 配额 | 1024 MB |
| GitHub 单 push 上限 | 2 GB |
| 剩余 push 机会 | 3 次 |

**问题根因**: Gitee 后台保留了许多已被 filter-branch/BFG 删除的历史对象，GC 清理不彻底。

---

## 推荐方案 A：一核多仓 + Gitee 清空重建

### 新仓库结构

```
longhun-system                    # 核心仓（代码 + 协议 + 人格）
  ├─ persona/                     # 人格内阁
  ├─ xpay/                        # XPay 激励模型
  ├─ cnsh-core/                   # CNSH 核心
  ├─ docs/                        # 核心文档（不含大文件）
  ├─ ops-console/                 # 操作台
  ├─ LICENSE
  └─ README.md

longhun-system-assets             # 资产仓（大文件 + 历史证据）
  ├─ longhun-font/                # 字体、渲染资源
  ├─ skills/screenshots/          # 技能截图
  ├─ docs/v3/screenshots/         # 文档截图
  ├─ research/*.png               # 研究图表
  ├─ evidence-matrix/             # 历史证据
  └─ _archive/                    # 归档材料

longhun-system-whitepapers        # 白皮书/论文仓
  ├─ xpay/whitepapers/
  ├─ docs/dragon-soul-open-hub/academic/
  ├─ CNSH 规范文档
  └─ 公开发布材料
```

### 执行步骤

1. **创建新仓库**
   - GitHub: `UID9622/longhun-system-assets`
   - GitHub: `UID9622/longhun-system-whitepapers`
   - Gitee: `uid9622_admin/longhun-system-assets`
   - Gitee: `uid9622_admin/longhun-system-whitepapers`

2. **迁移大文件**
   - 使用 `git filter-repo` 或 BFG 从历史中提取大文件目录
   - 推送到对应资产仓

3. **清理主仓历史**
   - 用 BFG 删除主仓中的大文件目录历史
   - 重写后的主仓预计 <100MB

4. **Gitee 主仓清空重建**
   - 在 Gitee 后台使用「清空仓库」功能
   - 重新 push 精简后的主仓
   - 这样 Gitee 上旧对象彻底释放

### 风险

- 所有 commit hash 再次改变
- 已克隆的人需要重新 clone
- 需要处理跨仓引用关系

---

## 备选方案 B：仅清空 Gitee 主仓重建

如果主仓内容不想拆分，可以：

1. 保持 `longhun-system` 不变
2. 在 Gitee 后台「清空仓库」
3. 重新 force push 当前 55MB 的主仓
4. 预计 Gitee 仓库会降到 ~100MB 以内

**优点**: 简单、不拆分仓库
**缺点**: 无法从根本上解决未来体积膨胀问题

---

## 备选方案 C：Gitee 仅同步代码分支

1. 主仓继续放 GitHub（2GB 上限，当前可用）
2. Gitee 只保留一个精简分支 `main-lite`
3. 大文件目录在 Gitee 上不存在
4. 国内用户从 Gitee 拉代码，海外用户从 GitHub 拉完整版

**优点**: 兼顾国内外访问
**缺点**: 维护两个分支，容易 divergence

---

## 推荐决策

**建议先执行方案 B（清空 Gitee 重建）**，因为：
- 当前 HEAD 只有 55MB，清空后立刻解决配额问题
- 操作简单，风险可控
- 后续如果主仓继续膨胀，再执行方案 A 拆分

---

## DNA 追溯

`#龍芯⚡️20260624130125-REPO-SPLIT-PLAN-v1.0`
