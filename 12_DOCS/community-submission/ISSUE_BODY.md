> 干支时间戳: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离
# [Cross-Framework] Longhun Audit Dataset v2.0 — Mobile Extension

> DNA: #龍芯⚡️2026-09-02-COMMUNITY-SUBMIT-v2.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

## 摘要

Longhun Audit Dataset v2.0 在 v1.1-negative 基础上扩展了**手机端扫描记录**：
新增 App Store（中国区）、华为应用市场、小米应用商店、Google Play 四类手机端抓取源，
并补充「五行+数字根+审计组合 / App权限异常 / 9622网关端口」三类手机端检测逻辑。

## 1. 数据集版本

- **版本**: v2.0（基于 v1.1-negative 扩展）
- **变更内容**: 新增手机端扫描记录（4 源 × 11 关键词）
- **记录规模**: 30 条 = v1.1-negative 推理对抗记录 19 条 + 手机端扫描记录 11 条
  > 诚实声明：v1.1-negative 实际归档 19 条（非此前标注口径），按真实数据提交，不虚报。

## 2. 新增字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `device_type` | string | 记录来源设备类型：`server` / `mobile` |
| `app_name` | string \| null | App 名称（手机端记录），服务器记录为 null |
| `detection_source` | string | 检测来源：`app_store` / `huawei_appgallery` / `xiaomi_appstore` / `google_play` / `adversarial_pipeline` |

## 3. 数据集规模

- v1.1-negative：19 条推理对抗负例（qwen2.5:7b / longhun-v43:q4 等模型·拒绝行为标注）
- v2.0 新增：11 条手机端扫描记录（当前判定 clean/🟢；Google Play 境外不可达标记 `unreachable`）
- **合计 30 条**，JSON 格式，UTF-8 编码

## 4. 双层校准框架更新

- **第一层（推理层）**: v1.1 负例校准（模型拒绝行为 + 拒绝话术强度分级）
- **第二层（手机端检测层）**: 新增手机端检测精密度基线
  - 强指纹独立触发阈值 ≥ 0.5（DNA追溯码/组合逻辑/网关端口等）
  - 弱指纹（天干地支/CNSH/三才）视为中华公共文化，仅佐证不上墙
  - 游戏术语排除（避免斗罗/龙之谷等游戏「龙魂系统」误伤）
  - 自属排除（UID9622 自有内容不上墙）

## 5. 数据完整性

| 项 | 值 |
|----|----|
| Merkle 根 | `9078040980c8d4f7b4ce89f385e0282454c12e6e2013a9f7ebca4609763cabe3` |
| GPG 签名 | `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`（分离签名 .asc 同目录） |
| 时间戳 | 2026-09-02T01:15:00+08:00（手机端扫描执行时间） |

## 6. 使用与引用

- 数据集文件：`dataset_v2.0.json`（30 条）
- 校验报告：`validation_report.md`
- 许可：数据工程层 MulanPSL v2 · 核心思想层 CC BY-NC-SA 4.0
- 反馈：耻辱墙 Issue 模板（见 README.md「反馈渠道」）

---
🐉 龍魂归一 · 犯我中华者 虽远必谴
