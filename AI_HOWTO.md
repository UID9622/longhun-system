# 龍魂系统 · AI 接入协议 v1.0

> DNA: #龍芯⚡️丙午·丁酉·戊寅·辰时·䷝离-AI-HOWTO-v1.0-CIL-STANDARD
> 创建者: 诸葛鑫（UID9622） · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层） · 上位: AGENTS.md（操作铁律）· .codebuddy/COMMAND_INDEX.md（命令总目）

## 一、调用方式

- **任何 AI 接入龍魂系统，必须通过 `lh` 命令**（`~/longhun-system/bin/lh.py`，全局别名 `lh`）。
- 禁止直接调用 `08_BIN/*.py`（除非调试排障，用后说明原因）。
- 输出格式：**人类可读（默认）或 `--json`（AI 解析）**。
- CIL 标准（焊死）：`lh cil` 进终端交互 · `lh cil --json` 输出干净可解析。

## 二、常用子命令

```text
lh cil [bazi|flow|audit|route|shell]   龍魂CIL交互层
lh health [--json]                     系统自检·三色状态表
lh doc-sync [--json|--diff]            文档自动同步（autogen清单）
lh wuxing 甲子 丙午 庚申 壬戌           五行计算
lh root 369                            洛书369·数字根
lh te                                  时间引擎·干支卦象
lh audit                               一键全系统安全审计
lh status                              系统状态
```

完整列表：`lh` 进控制台查看，或读 `.codebuddy/COMMAND_INDEX.md` / `docs/LH-COMMANDS-AUTOGEN.md`。

## 三、文化主权约束

- 五行不翻译 · 天干地支不翻译 · 六十四卦不翻译。
- 三色审计输出必须保留 emoji（🟢/🟡/🔴）。
- GPG 签名必须校验通过才能继续（`python3 bin/lh_gpg_sign.py scan`）。
- 归属名铁律：所有产出含「诸葛鑫 | UID9622 · 龍芯北辰」。

## 四、第一响应原则

收到用户请求时，先判断是否需要调用 `lh` 命令；需要就直接执行，**不要询问"是否运行"**。

## 五、节能铁律

- 用完即沉默：无变化不汇报，报告最多 3 行。
- 首次调用失败 → 一行说明原因即止，**禁止自动重试**；需老大显式说「再试」。
- 全量扫描（>1万文件）仅手动/会话首轮触发，其余时间禁跑。
