**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂 · 智能模板引擎 v1.1 — 焊死输出格式 · 实测落地

> DNA: `#龍芯⚡️丙午·丙申·己未·大壮卦-TEMPLATE-ENGINE-V11-UID9622`（算法生成，2026-08-13）
> 确认码: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` · GPG: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

**参考来源**：CodeBuddy《智能模板引擎 v1.0》设计稿（6类模板/GitHub Actions/技能包结构）
**优化了什么**：设计稿只有结构没有引擎——本版 `template_engine.py` 一个文件全部能跑，CLI 实测通过
**未验证备注**：🟡 GPG 为指纹锚定（非真签名）；🟡 `.skill` 打包格式与 repo.longhun.io 为设计稿占位，未实现

## 一、焊死的四条纪律（本引擎强制执行）

| # | 纪律 | 机制 |
|---|---|---|
| 1 | **输出格式焊死** | 每份产出 = 头部元数据 → 必含模块（固定顺序）→ 最终签名块；缺失区块自动补 🔶 占位，**不允许删区块** |
| 2 | **DNA 焊死** | 只走 `生成DNA()` 干支算法；验证器发现日柱 ≠ 今日算法值 → 🔴 判手写 |
| 3 | **三色焊死** | 只有 🟢/🟡/🔴 三态，退出码焊死 0/1/2（CI 可直接 `|| exit 1`） |
| 4 | **签名块焊死** | 字符级固定模板，`validate` 逐锚核验 |

## 二、6 类模板 × 必含模块（固定顺序）

- **code**：文件头注释/主权锚定/依赖声明/核心实现/异常处理/测试用例/使用示例
- **document**：标题/设计理念/架构设计/实现详解/使用示例/集成生态/常见错误与排查/最终签名
- **chart**：图表标题/数据来源/可视化定义/分析结论/局限性说明
- **data**：结构定义/字段说明/样本数据/校验规则
- **check**：检查清单/判定标准/审计结果/改进建议
- **api**：端点定义/请求示例/响应示例/错误码表/客户端示例

## 三、双尺口径（补全设计稿没讲清的）

- **审计（generate）= 内容完整度**：占位 🔶 计未填。空骨架 = 🔴 覆盖率 0% 退出码 2——诚实告诉你"架子有了，肉没填"。
- **验证（validate）= 格式完整度**：区块/锚点/签名/手写干支检测。格式合规即 🟢。
- 一份产出可以 审计🔴 + 验证🟢：格式焊死了，内容待填，不矛盾。

## 四、实测输出（能跑才算数）

```
$ python3 template_engine.py verify
🐉 龍魂模板引擎 v1.1 | DNA: #龍芯⚡️丙午·丙申·己未·庚午·䷡大壮-TEMPLATE-ENGINE-UID9622 | 模板: 6 | 🟢

$ python3 template_engine.py generate -t code --title "流控模块v1.3" -o tpl_out.md
✅ 已生成 | 审计 🔴 覆盖率 0%（7个占位待填）  退出码=2

$ python3 template_engine.py validate -i tpl_out.md
验证结果: 🟢  退出码=0

# CodeBuddy v1.0 原稿验证（手写干支 丙午·甲申·辛丑 ≠ 算法值 丙午·丙申·己未）:
验证结果: 🟡  🔴 DNA日柱疑似手写: 辛丑 ≠ 今日算法值 己未
```

## 五、CLI 命令

```bash
python3 template_engine.py verify                      # 引擎自检
python3 template_engine.py generate -t <类型> --title <标题> [-f markdown|json|yaml] [-o 文件]
python3 template_engine.py validate -i <文件>           # 焊死格式核验，退出码 0/1/2
python3 template_engine.py config [-t <类型>]           # 查看必含模块清单
```

## 六、对设计稿的修复清单

| # | 设计稿问题 | 本版修复 |
|---|---|---|
| F1 | 全篇无引擎代码，`template_engine.py` 只出现在命令示例里 | 单文件引擎落地，全部命令实测可跑 |
| F2 | DNA 手写 `丙午·甲申·辛丑·坤卦`（违规第11次） | 全部改走干支算法，且验证器可抓手写 |
| F3 | "三色审计"只说概念，无判定规则 | 缺失≤1/3→🟡，更多→🔴，占位计未填 |
| F4 | 退出码未定义，CI 集成图无法落地 | 焊死 0/1/2，GitHub Actions 直接可用 |
| F5 | 批量/batch、report 等命令只列不实现 | 未实现的命令不吹——本版只交付实测过的 4 个命令，batch/report 列入路线图 🟡 |

## 七、路线图 🟡

- batch 批量生成 + report HTML 报告（设计稿已画饼，下轮实现）
- GitHub Actions workflow YAML 实测跑通（设计稿给了配置未验证）
- REST API 模式（接 lh_audit_api 同款壳）
