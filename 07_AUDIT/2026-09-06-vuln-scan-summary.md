# 龍魂漏洞扫描报告 v1.0.1 — 实证收敛版（第二轮）

D1 evidence: 2026-09-06 · lh_vuln_scanner.py v1.0.1 · 五算法 · 4793文件 · P0=298(经右路实证收敛) · GPG:A2D0092CEE2E5BA87035600924C3704A8CC26D5F

DNA: #龍芯⚡️2026-09-06-VULN-SCANNER-V1-CONFIRMED-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
引擎: 08_BIN/lh_vuln_scanner.py (lh vuln-scanner · v1.0.1 右路升级)
全量报告: 07_AUDIT/2026-09-06-vuln-scan-report.json

## 收敛轨迹（两轮右路实证）
| 轮次 | CONFIRMED | P0 | 关键动作 |
|:---|:---|:---|:---|
| v1.0 首跑 | 1517 | 452 | 五算法首跑（报告自噬/venv/json 数据已排） |
| v1.0.1 右路升级 | 1322 | **298** | docstring/字符串字面量/sandbox/exec_globals 白名单 + V021 本地模型判定 + gpt_sovits 黑名单 + 修 lh_score RCE |

## 实证真相注记（重要·纠正首轮标签）
首轮报告标 CONFIRMED 的三类样本经代码核读**实为非执行上下文**，本轮右路已降级：
1. `lh_knowledge_hub.py:667` = docstring 教学对照示例（"❌危险 vs ✅安全"教程）
2. `CNSH_代码审计引擎.py:481` = `演示代码='''...'''` 故意漏洞样本（引擎自演示用）
3. `pickle.load` ×9 = 全部本地自有 sklearn 模型/向量器加载（业界标准持久化·非不可信网络源）

## 真实修复（实证·已落地）
| 位置 | 类型 | 修复 |
|:---|:---|:---|
| `08_BIN/lh_score.py:182` eval(args.quick) | RCE 入口（CLI 参数兜底 eval） | 改 ast.literal_eval + 错误提示（JSON 已全覆盖正常用法） |
| cnsh_compiler.py exec(result["python_code"], exec_globals) | 语言运行时本质 | 右路白名单 exec_globals（白名单模块无 os/subprocess） |

## 剩余待人工复核（真实执行代码·低危优先修）
- V002 shell=True ×30 余：lh_control_gate/lh_workflow_engine/lh_scheduler 等内部命令——cmd 多为静态字符串，无 f-string 用户拼接者低危；重构 shell=False 分批
- V003 f-string SQL {table}：表名多为内部枚举（lh_material_scanner/lh_browser_miner/lh_base_trace_collector）——建议表名改白名单校验
- V020 硬编码 IP：多为鲲鹏自有 119.13.90.27 基础设施常量（已右路白名单）

## 收敛总结
P0=298 · P1=326 · P2=696 · CONFIRMED=1322 · LIKELY_SAFE=1875 · FP=91
五行分布见全量报告 wuxing_balance。结论=规则匹配实证 + 人工复核后修复。
