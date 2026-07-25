# 桌面资料清理归档报告 · 2026-07-26

**DNA**: `#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-DESKTOP-CLEANUP-v1.0`
**执行人**: UID9622
**范围**: `/Users/zuimeidedeyihan/longhun-system`

---

## 一、安全清理（阶段一）

| 文件 | 原始位置 | 去向 | 状态 |
|------|---------|------|------|
| SecretKey.csv | Desktop | `_private/vault/` | ✅ 已加密隔离 |
| credentials.csv | Desktop | `_private/vault/` | ✅ 已加密隔离 |
| 1783936558948.txt | Desktop | `_private/vault/` | ✅ 已加密隔离 |
| 默认业务空间-apiKey-6117568.csv | Desktop | `_private/vault/` | ✅ 已加密隔离 |

- 生成 `_private/vault/manifest.json`（SHA256 + 时间戳）
- `_private/` 权限 700，vault 内文件 600
- `.gitignore` 已包含 `_private/`，不上 git

**注意**：按文件名扫描 Desktop 未找到明确身份证照片文件。已有的 `_private/id_documents/` 目录保持受保护状态。

---

## 二、资料归档（阶段二）

### 2.1 已完成的迁移

| 源 | 目标 | 说明 |
|----|------|------|
| `Desktop/文章/` | `longhun-system/articles/` | 文章并入主库 |
| `Desktop/哲学/` | `longhun-system/articles/philosophy/` | 哲学资料归档 |
| `Desktop/论文/main.pdf` | `longhun-system/research/main_desktop.pdf` | 论文备份 |
| `Desktop/龍魂系统·统一知识矩阵/` | `_archive/unified_knowledge_merged/desktop_unified_matrix_2026-07-26/` | 整包镜像 |
| `Desktop/桌面项目箱/cnsh-chrome-plugin` | `web/chrome-extensions/_archive/` | Chrome 插件 |
| `Desktop/桌面项目箱/谷歌浏览器插件` | `web/chrome-extensions/_archive/` | Chrome 插件 |
| `Desktop/桌面项目箱/*.app` | `_archive/desktop_project_box/apps/` | macOS 应用包 |
| `Desktop/桌面项目箱/CNSH 军人的编辑器` | `_archive/desktop_project_box/editors/` | 编辑器工程 |
| `Desktop/桌面项目箱/code_1.119.0-...` | `_archive/desktop_project_box/editors/` | VSCode 分发 |
| `Desktop/桌面项目箱/UID9622_DAILY_EXEC_LOGS` | `_work/logs_archive/desktop_logs_2026-07-26/` | 每日日志 |
| `Desktop/桌面项目箱/龍魂操作日志` | `_work/logs_archive/desktop_logs_2026-07-26/` | 操作日志 |
| `Desktop/桌面项目箱/龍魂黎曼猜想_投稿包` | `research/riemann_desktop/` | 黎曼投稿包 |
| `Desktop/桌面项目箱/龍魂簽名中心-20260616` | `_archive/desktop_project_box/signature_center/` | 签名中心 |
| `Desktop/桌面项目箱/易经算法神经网络` | `_archive/desktop_project_box/yijing_nn/` | 易经神经网络 |
| `Desktop/桌面项目箱/元宇宙规则` | `_archive/desktop_project_box/metaverse/` | 元宇宙规则 |
| `Desktop/桌面项目箱/龍魂方案提案-Solution-Proposals` | `_archive/desktop_project_box/proposals/` | 方案提案 |
| `Desktop/桌面项目箱/龍魂资产` | `_archive/desktop_project_box/assets/` | 资产文件 |
| `Desktop/桌面项目箱/打包待命` | `_archive/desktop_project_box/packaged/` | 打包待命 |
| `Desktop/桌面项目箱/longhun` | `_archive/desktop_project_box/longhun/` | 未归类工程 |
| `Desktop/桌面项目箱/articles` | `_archive/desktop_project_box/articles/` | 未归类文章 |
| `Desktop/桌面项目箱/龍魂系統·統一知識矩陣` | `_archive/desktop_project_box/龍魂系統·統一知識矩陣/` | 知识矩阵副本 |

### 2.2 整包镜像进度

- **源**: `Desktop/龙魂系统-知识库/_archive/`（8,489 文件，含 205M deprecated 目录）
- **目标**: `longhun-system/_archive/desktop_mirror_2026-07-26/`
- **状态**: 后台 rsync 进行中（已复制 2,710+ 文件）
- **策略**: `--whole-file --ignore-errors --timeout=600`

由于 deprecated 目录含大文件（TF-IDF 模型、Chroma DB、下载压缩包等），复制较慢。已用 `--ignore-errors` 跳过不可读文件，确保主数据不丢。

---

## 三、P0 功能落地（阶段三至六）

### 3.1 声音模型（阶段三）

| 文件 | 功能 | 状态 |
|------|------|------|
| `bin/lh_tts_engine.py` | edge-tts 合成 + DNA 水印 | ✅ 已跑通 |
| `bin/lh_asr_engine.py` | whisper 本地识别 | ✅ 已跑通 |
| `bin/lh_audio_watermark.py` | 音频 DNA 元数据/尾部签名 | ✅ 已跑通 |
| `models/voice/README.md` | 模型目录规范 | ✅ 已创建 |
| `voices/voice_dna_v1/` | 原 `voice-dna/` 归档 | ✅ 已迁移 |
| `voices/voice_twin_v1/` | 原 `voice-twin/` 归档 | ✅ 已迁移 |

**端到端测试**: TTS → MP3 → DNA 水印 → ASR，链路已通。

### 3.2 API 人格路由（阶段四）

| 文件 | 功能 | 状态 |
|------|------|------|
| `bin/lh_persona_api.py` | FastAPI :8779 人格路由 | ✅ 已跑通 |
| `bin/personas/p77_security.py` | P77 执行器 | ✅ 已创建 |
| `bin/personas/s1_legal.py` | S1 执行器 | ✅ 已创建 |
| `bin/personas/s2_luoshu.py` | S2 执行器 | ✅ 已创建 |
| `bin/personas/s3_civil.py` | S3 执行器 | ✅ 已创建 |
| `engines/lh_persona_runner.py` | 22人格运行器 + P77/S1/S2/S3 | ✅ 已修复 |
| `tests/test_persona_route.sh` | API 测试脚本 | ✅ 已通过 |

**测试覆盖**: /health、/persona/list、/persona/route（安全/工程）、/persona/execute 全部 200。

### 3.3 AGENTS.md 焊死命令（阶段五）

| 文件 | 功能 | 状态 |
|------|------|------|
| `bin/lh_patrol.py` | 全系统安全巡检 | ✅ 已跑通 |
| `bin/read_lints.py` | Lint 报告读取 | ✅ 已跑通 |
| `AGENTS.md` | 命令文档 | ✅ 已更新 |

### 3.4 本地保险柜（阶段六）

| 文件 | 功能 | 状态 |
|------|------|------|
| `bin/lh_vault_cli.py` | CLI 入口 | ✅ 已跑通 |
| `bin/lh_vault_api.py` | API 入口 :8780 | ✅ 已跑通 |
| `engines/lh_local_vault.py` | AES-256-GCM 加密保险柜 | ✅ 已有完整实现 |

**测试覆盖**: init、add、list、get 全部通过。

---

## 四、Git 提交与推送（阶段七）

- **Commit**: `b46318fc1`
- **Message**: `feat: 桌面清理归档 + TTS/ASR/人格路由/保险柜/P77-S1-S2-S3 全部落地`
- **远程推送**:
  - ✅ GitHub (`gh-ssh`)
  - ✅ GitCode (`gitcode`)
  - ✅ Gitee (`gitee`)

---

## 五、后续待办

1. [ ] 等待 `Desktop/龙魂系统-知识库/_archive/` 后台镜像完成
2. [x] 将整理后的 `longhun-system` 同步到鲲鹏 :8779 :8780 服务在线 ✅ `/opt/longhun-system/` 和 `/backup/`
3. [x] 在鲲鹏上重启 persona-api、vault-api 等服务并 curl 验证 ✅
4. [ ] 处理 GitHub 报告的 142 个依赖漏洞（dependabot）
5. [ ] 补充身份证照片扫描（如 Desktop 上还有未命中的照片）
6. [ ] 将开源包上传华为云对象存储（如用户确认）

---

## 六、关键路径

```
Desktop 敏感文件 → _private/vault/
Desktop 知识资料 → _archive/ / articles/ / research/
voice-dna/twin → voices/
TTS/ASR → bin/lh_tts_engine.py / bin/lh_asr_engine.py
人格路由 → bin/lh_persona_api.py :8779
保险柜 → bin/lh_vault_api.py :8780
巡检 → bin/lh_patrol.py
Git → GitHub/GitCode/Gitee orphan_main
```

---

## 七、鲲鹏部署验证（2026-07-26 追加）

```
longhun-persona-api.service: active ✅
longhun-vault-api.service:   active ✅
curl http://127.0.0.1:8779/health -> 200 ok
  { "status":"ok", "booted":true, "agents_online":21 }
curl http://127.0.0.1:8780/health -> 200 ok
curl POST /persona/route {"task":"检查这段代码有没有SQL注入"} -> P77 安全审计 ✅
```

同步方式：本地 tar 打包（排除 .git/_private/_archive/models/voices/data/logs/dist/backups/_work/knowledge/longhun-font）→ scp 315M → 鲲鹏 `/opt/longhun-system/` 解压 → systemd 启动。

**已排除的大目录说明**：models（466G）、_archive（16G）、voices（31M）等未传鲲鹏，仅保留核心代码与配置。如需全量备份，需单独安排大文件同步策略。
