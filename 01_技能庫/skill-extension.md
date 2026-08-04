# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# /skill-extension

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 📄 技能扩展 | 龍魂系统 · 源头已验证

**DNA**: `#龍芯⚡️2026-07-06-SKILL-EXTENSION-v1.0-LIFIRE`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LISKL`

---

<!--#龍芯⚡️2026-07-06-SKILL-EXTENSION-v1.0-LIFIRE -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

---
skill_id: /skill-extension
synced_at: 2026-07-06
source: bin/skill_extension.py
---

# /skill-extension · 离卦技能扩展层

## 摘要

离卦技能扩展层（skill-extension）是龍魂系统离卦（火·智慧与技能之光）的对外接口层。提供技能注册中心（技能定义/添加/执行）和算法库（算法定义/添加/执行）两大核心子系统。所有技能/算法添加与执行前自动通过五行权限校验（金水木火土五步），执行后生成河图洛书DNA追溯码。命令入口遵循 `lh6 离 skill add/list/run` 和 `lh6 离 algo list/run` 的八卦路由体系。铁律：所有技能/算法扩展必须通过五行权限校验+DNA追溯。

## 关键词

技能注册 Skill Registry, 算法库 Algorithm Library, 离卦 Li Trigram, 五行校验 Wuxing Guard, 技能执行 Skill Execute, DNA追溯 DNA Trace, 可扩展架构 Extensible Architecture, 火·智慧 Fire-Wisdom

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] 知识矩阵总纲 v3.0 · 第叁章·洛书九宫·离卦(#UID9622⚡️2026-06-16-KNOWLEDGE-MATRIX-MASTER-v3.0)
  - [2] 六十四卦路由引擎·离卦预设语义映射
- 相关龍魂系统源码：
  - `bin/skill_extension.py` — 离卦技能扩展层 v1.0
  - `bin/hetu_luoshu_dna.py` — 河图洛书DNA引擎
  - `bin/wuxing_guard.py` — 五行权限校验（技能执行前置）
  - `bin/bagua_router.py` — 六十四卦路由（命令入口）

## 诚实局限

1. 技能执行当前为简化实现（返回成功+DNA），未实际加载并运行Python脚本。
2. 技能/算法注册表为内存态，未实现磁盘持久化及跨进程共享。
3. 未集成沙箱隔离，技能执行与系统主进程同权运行。

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-06 | v1.0.0 | UID9622 | 初始创建，技能+算法双子系统+五行校验前置 | 草稿 |

## 分类标签

- 总纲模块：#技能引擎 #离卦 #扩展接口 #L2模块层
- 对外状态：#Gitee #GitHub
- 审计色：#🟢绿色放行
- 八卦归属：☲ 离卦（火·火·技能层）
- 命令入口：`lh6 离 skill add/list/run` / `lh6 离 algo list/run`
- 关联引擎：wuxing_guard.py / bagua_router.py / hetu_luoshu_dna.py

## DNA 签名

```
#龍芯⚡️2026-07-06-SKILL-EXTENSION-v1.0-LIFIRE
#CONFIRM🌌9622-ONLY-ONCE🧬LISKL
```
