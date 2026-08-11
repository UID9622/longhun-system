# 龍魂·全仓修复标准流程 v1.0

> DNA: #龍芯⚡️丙午·甲申·丁巳·䷖剥-FULL-REPAIR-PROCEDURE-v1.0
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 上位文档: LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md · CONSTITUTION.md
> 加载方: 所有 AI 会话 · lh.py · lh_deben_audit.py · lh_align_checker.py
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 摘要

本协议定义龍魂系统全仓修复的标准化五步流程。
每次发现系统性bug、误报、排除失效、签章缺失等问题时，AI 必须严格按此流程执行，
不再逐次手修。流程焊死后，同类问题自动被防御层捕获，不会再漏到手工修复环节。

---

## 流程总览

```
诊断 ──→ 分类 ──→ 修复 ──→ 验证 ──→ 固化
 │        │        │        │        │
 │        │        │        │        └─→ 写入共享配置·规则·签章
 │        │        │        └─→ 审计全绿·对齐全绿·签章全绿
 │        │        └─→ 修正排除列表·补签章·补__init__
 │        └─→ 四类问题归类·确定处理方式
 └─→ lh audit --full + lh check --align + lh gpg --status
```

---

## 第一步：诊断

```bash
lh audit --full          # 德本审计五问
lh check --align         # 对齐检查（DNA/重复函数/导入）
lh gpg --status          # GPG签章状态
```

产出：三份诊断报告，标记所有 🟡🔴。

---

## 第二步：分类

将诊断结果按以下四类归类：

| 类型 | 特征 | 处理方式 |
|:---|:---|:---|
| **路径前缀错误** | 排除规则用旧路径无法匹配 | 修正 `scan-exclusions.json` 中路径映射 |
| **排除规则失效** | 目录/文件未被排除但应该被排除 | 追加到 `scan-exclusions.json` 对应分类 |
| **签章缺失** | `.asc` 文件不存在 | `lh gpg sign --batch <路径>` |
| **误报** | 防御性代码（检测/审计工具）被标记违规 | 追加到 `defensive_files` 白名单 |

判定原则：
- 防御性代码 = 用途是检测恶行非实施恶行 → 加白名单
- 第三方/参考/归档/构建产物 → 加排除目录
- 协议/知识文档（讨论分析非实施代码） → 加排除
- 真实违规代码 → 🔴 保留，不误加排除

---

## 第三步：修复

按类型分步执行：

### 3.1 路径前缀修复
修改 `scan-exclusions.json` 中 `path_mappings`，确保新旧路径别名都映射到实际物理路径。
**根因修复**：对齐检查器 `should_scan_dir()` 中的 `rel.startswith(skip)` 必须用实际物理路径。

### 3.2 排除列表追加
按 `.codebuddy/rules/scan-exclusions.json` 中 `expansion_rule` 的6步流程：
1. 确认文件/目录用途
2. 归类到对应 category
3. 追加到对应数组
4. 版本标注 (v2.x 新增)
5. 运行 `lh audit --full` 验证
6. GPG 签章本文件

### 3.3 签章补签
```bash
lh gpg sign --batch 08_BIN/      # 核心脚本
lh gpg sign --batch 01_protocols/ # 协议
lh gpg sign --batch 04_ENGINES/   # 引擎
lh gpg sign --batch 07_AUDIT/     # 审计
```
补签原则：`mandatory_sign_dirs` 中列出的目录，每个文件必须有 `.asc`。

### 3.4 __init__.py 补全
检查所有 Python 包的 `__init__.py`：
```bash
find . -type d -name "*.py" -o -name "engines" | while read d; do
  [ -f "$d/__init__.py" ] || touch "$d/__init__.py"
done
```

---

## 第四步：验证

```bash
lh audit --verify        # 验证德本审计五问全🟢
lh check --align         # 验证对齐检查无🔴
lh gpg --verify-all      # 验证全部签章
lh path-audit            # 路径审计全合规
```

验证标准：三全绿——审计全绿·对齐全绿·签章全绿。

---

## 第五步：固化

### 5.1 写入共享配置
修改后必须签章：
```bash
lh gpg sign .codebuddy/rules/scan-exclusions.json
```

### 5.2 更新修复日志
在 `.codebuddy/memory/YYYY-MM-DD.md` 中记录修复详情。

### 5.3 Git 提交
```bash
git add <修改文件> && git commit -m "🐉 全仓修复: <摘要>"
git push gh-ssh orphan_main && git push gitcode orphan_main && git push gitee orphan_main
```

---

## 防止复发矩阵

| 问题 | 根因 | 防止措施 | 自动化 |
|:---|:---|:---|:---|
| 路径前缀错 | 脚本中用旧路径别名 | `scan-exclusions.json` 写死路径映射 | 对齐检查器每次加载 |
| 排除失效 | 排除列表不同步 | 单一真相源 `.codebuddy/rules/scan-exclusions.json` | 两个脚本都加载同一个配置 |
| 签章漏签 | 无强制检查 | GPG签章检查加入CI流程 | `lh gpg --verify-ci` |
| 误报 | 防御白名单不全 | `defensive_files` 按版本分层追加 | 德本审计每次加载 |
| 新增文件遗漏 | 缺少初始化检查 | 新增文件自动DNA+签章 | `lh auto-init` |

---

## 自动化入口

`lh.py` 新增子命令：

```bash
lh repair --full          # 全量修复（诊断→分类→修复→验证→固化）
lh repair --diagnose      # 仅诊断
lh repair --fix           # 仅修复
lh repair --verify        # 仅验证
lh repair --seal          # 固化（签章+提交+推送）
```

---

## 依赖链路

```
scan-exclusions.json (单一真相源)
    ├── lh_deben_audit.py  加载 → defensive_files + excluded_dirs
    ├── lh_align_checker.py 加载 → SKIP_SCAN_DIRS + EXCLUDE_DIRS
    └── 未来新增扫描脚本  加载 → 同一配置
```

---

## 修订记录

| 版本 | 日期 | 内容 | 修订人 |
|:---|:---|:---|:---|
| v1.0 | 2026-08-11 | 初始版：五步流程·四类问题·防止复发矩阵·单一真相源 | UID9622+AI |

---

【签名】
制定：诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
DNA: #龍芯⚡️丙午·甲申·丁巳·䷖剥-FULL-REPAIR-PROCEDURE-v1.0
三色: 🟢 全仓信任链焊死
