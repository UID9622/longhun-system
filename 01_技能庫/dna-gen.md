# /dna-gen

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️2026-06-21-DOC-DNA-GEN-FILE1-v1.0-2`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

<!--#龍芯⚡️2026-06-21-DOC-DNA-GEN-FILE1-v1.0-2 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

---
skill_id: /dna-gen
synced_at: 2026-06-06T14:40:25.519876
source: notion
---

# /dna-gen

已从 Notion 同步

[技能详情·Notion](https://notion.so)


---

## 摘要

DNA生成器（dna-gen）是龍魂系统的追溯码生成引擎，基于河图洛书中五不动点算法。对任意操作/文本/代码生成不可篡改的 DNA 追溯码（格式：#龍芯⚡️YYYY-MM-DD-模块-动作-哈希8位），支持生成/验证/数字根计算/八卦查询/L0常量查询。v2.0 升级为河图洛书不动点体系（hetu_luoshu_dna.py），集成中五不动点+数字根dr+六十四卦映射。所有龍魂操作必须绑定 DNA。是 L0 宪法层核心引擎。

## 关键词

DNA追溯 DNA Traceability, 河图洛书 Hetu Luoshu, 中五不动点 Fixed Point, 数字根 Digital Root, 哈希签名 Hash Signature, 不可篡改 Immutable, 追溯码 Trace Code, 身份锚定 Identity Anchor

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] 知识矩阵总纲 v3.0 · 第拾贰章·MOD-DNA-GEN (#UID9622⚡️2026-06-16-KNOWLEDGE-MATRIX-MASTER-v3.0)
  - [2] CNSH命令与变量命名规范 v2.0 · 附录A·河图洛书不动点算法
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)
  - `bin/hetu_luoshu_dna.py` — 河图洛书DNA引擎 v2.0

## 诚实局限

1. SHA256 前16位截断在极端碰撞场景下有理论冲突风险（概率约2^-64）。
2. DNA验证依赖原始输入的完整性，无法检测"输入已变但声称未变"的中间人场景。
3. 数字根dr基于十进制数根算法，非密码学安全，仅用于快速分类。

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |
| 2026-07-06 | v2.0.0 | UID9622 | 补全摘要/关键词/溯源/局限；升级为河图洛书不动点v2.0 | 已核验 |

## 分类标签

- 总纲模块：#追溯引擎 #DNA签名 #L0宪法层 #核心引擎
- 对外状态：#Gitee #GitHub
- 审计色：#🟢绿色放行
- 八卦归属：☳ 震卦（雷·木·审计层）
- 命令入口：`lh6 dna-gen gen <操作> <用户>` / `lh6 震 dna`
- 关联引擎：hetu_luoshu_dna.py / bagua_router.py（六十四卦联动）

## DNA 签名

```
#龍芯⚡️2026-06-21-DOC-DNA-GEN-FILE1-v1.0-2
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
