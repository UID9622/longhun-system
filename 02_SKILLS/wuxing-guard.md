# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# /wuxing-guard

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 📄 五行守护 | 龍魂系统 · 源头已验证

**DNA**: `#龍芯⚡️2026-07-06-WUXING-GUARD-v1.0-5XELMT`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬5ELEM`

---

<!--#龍芯⚡️2026-07-06-WUXING-GUARD-v1.0-5XELMT -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

---
skill_id: /wuxing-guard
synced_at: 2026-07-06
source: bin/wuxing_guard.py
---

# /wuxing-guard · 五行权限校验层

## 摘要

五行权限校验层（wuxing-guard）是龍魂系统所有 lh6 命令执行前的安全闸门。基于五行（金木水火土）相生相克哲学构建五步校验链路：金→身份认证（令牌/GPG密钥）、水→域隔离（命名空间权限）、木→权限检查（角色权重匹配）、火→审计预检（数字根dr熔断判定）、土→DNA追溯（生成操作DNA）。任一环节🔴拒绝即熔断，后续步骤不再执行。数字根dr∈{3,9}直接拒绝，dr=6触发黄色预警。铁律：所有lh6命令执行前必须通过五行权限校验。

## 关键词

五行权限 Five Elements Permission, 相生相克 Generation-Restriction, 身份认证 Identity Auth, 域隔离 Namespace Isolation, 审计预检 Audit Pre-check, DNA追溯 DNA Traceability, 数字根熔断 Digital Root Fuse, 五步链路 Five-Step Chain

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] 知识矩阵总纲 v3.0 · 第叁章·洛书九宫·五行归属 (#UID9622⚡️2026-06-16-KNOWLEDGE-MATRIX-MASTER-v3.0)
  - [2] CNSH命令与变量命名规范 v2.0 · 附录A·数字根算法
- 相关龍魂系统源码：
  - `bin/wuxing_guard.py` — 五行权限校验层 v1.0
  - `bin/hetu_luoshu_dna.py` — 河图洛书DNA引擎（数字根+DNA生成）
  - `bin/bagua_router.py` — 六十四卦路由（命令执行入口）

## 诚实局限

1. 当前令牌校验为简化实现（SHA256哈希比较），未集成完整OAuth/OIDC协议。
2. 角色权重体系（admin/user/readonly/guest）为静态分级，不支持动态RBAC策略。
3. 数字根dr基于十进制数根算法，非密码学安全，仅用于快速分类熔断。

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-06 | v1.0.0 | UID9622 | 初始创建，五步链路（金水木火土·按相生序）+demo演示 | 草稿 |

## 分类标签

- 总纲模块：#安全引擎 #五行校验 #权限守卫 #L1核心层
- 对外状态：#Gitee #GitHub
- 审计色：#🟢绿色放行（正常命令）/ #🔴红色熔断（dr∈{3,9}）
- 八卦归属：☴ 巽卦（风·木·安全层）
- 命令入口：`lh6 五行 check <操作>` / `lh6 五行 demo` / `lh6 巽 secure`
- 关联引擎：hetu_luoshu_dna.py / bagua_router.py / audit_plugin_base.py

## DNA 签名

```
#龍芯⚡️2026-07-06-WUXING-GUARD-v1.0-5XELMT
#CONFIRM🌌9622-ONLY-ONCE🧬5ELEM
```
