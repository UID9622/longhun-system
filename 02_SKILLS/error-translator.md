# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# /error-translator

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 📄 错误翻译器 | 龍魂系统 · 源头已验证

**DNA**: `#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-ERROR-TRANSLATOR-v1.0-ERRTRN`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬TRANSL`

---

<!--#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-ERROR-TRANSLATOR-v1.0-ERRTRN -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

---
skill_id: /error-translator
synced_at: 2026-07-06
source: bin/error_translator.py
---

# /error-translator · 错误翻译器

## 摘要

错误翻译器（error-translator）将所有系统错误自动转换为中文提示，覆盖四大类：① Python标准库常见异常（ModuleNotFoundError/KeyError/ValueError等11类）；② 网络/Socket错误（Connection refused/timeout/reset等7类）；③ macOS launchctl错误码（1-7，含plist格式/权限/语法等详细修复建议）；④ Git错误（not a git repository/remote exists/push failed/auth failed等4类）。支持四种匹配策略（精确匹配→异常类型匹配→关键词模糊匹配→默认通用提示），并提供 `cn_error()` 函数供直接import使用和 `cn_launchd_error()` 专用函数。

## 关键词

错误翻译 Error Translation, 中文提示 Chinese Prompt, Python异常 Python Exception, launchctl错误码 launchctl Error Codes, Socket错误 Socket Errors, Git错误 Git Errors, 模糊匹配 Fuzzy Matching, 人话输出 Human-Readable Output

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] Python 3.x 标准库异常层次结构
  - [2] macOS launchctl(1) Man Page · Exit Codes
  - [3] Git Error Messages Reference
- 相关龍魂系统源码：
  - `bin/error_translator.py` — 错误翻译器 v1.0
  - `bin/plist_validator.py` — plist校验器（共享launchctl错误码映射）

## 诚实局限

1. 错误映射表为静态字典，新增错误类型需手动添加到ERROR_TRANSLATIONS。
2. 模糊匹配（关键词包含）可能导致误匹配（如"I/O error"匹配到"error: failed to push"）。
3. launchctl错误码仅覆盖1-7常见码，Apple官方文档中存在更多错误码未收录。

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-06 | v1.0.0 | UID9622 | 初始创建，四大类50+错误映射+四级匹配策略 | 草稿 |

## 分类标签

- 总纲模块：#错误处理 #中文翻译 #launchctl #异常映射
- 对外状态：#Gitee #GitHub
- 审计色：#🟢绿色放行
- 八卦归属：☲ 离卦（火·火·技能层）
- 命令入口：`lh6 错误翻译 "<错误信息>"` / `lh6 错误翻译 --code <错误码>`
- 关联引擎：plist_validator.py / semantic_parser.py

## DNA 签名

```
#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-ERROR-TRANSLATOR-v1.0-ERRTRN
#CONFIRM🌌9622-ONLY-ONCE🧬TRANSL
```
