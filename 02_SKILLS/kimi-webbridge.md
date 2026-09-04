# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️丙午·甲午·辛亥·甲午·䷚颐-KIMI-WEBBRIDGE-FILE1-FILE2-v1.0-2`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

# Kimi WebBridge

## 基本信息

- **技能 ID**: /kimi-webbridge
- **平台**: kimi
- **分类**: browser-control / web
- **状态**: active

## 描述

让AI控制真实浏览器

## 技术细节

- **优先级**: 8
- **需要认证**: 否
- **需要批准**: 否
- **DNA签章**:#龍芯⚡️丙午·甲午·辛亥·甲午·䷚颐-KIMI-WEBBRIDGE-FILE1-FILE2-v1.0-2

## 同步信息

- **同步时间**: 2026-06-06T16:07:48.574880
- **来源**: L0 技能注册表
- **状态**: 已同步

---

**自动生成于**: 2026-06-06 16:07:48


---

## 摘要

Kimi WebBridge 是龍魂系统的真实浏览器控制桥接器。让 AI 通过用户的实际浏览器（保持登录态/Cookie/本地存储）执行网页操作：导航、点击、输入、读取、截图、表单填充。基于本地 daemon 进程，零数据上传，所有操作在用户真实浏览器中完成。核心价值：保持用户登录态 → 无需重复登录 → AI 直接操作已有会话 → 不触发反爬/验证码。是 L0 核心层对外交互的唯一浏览器通道。

## 关键词

浏览器控制 Browser Control, WebBridge, 本地Daemon Local Daemon, 保持登录态 Session Keep, 零上传 Zero Upload, 截图 Screenshot, 表单填充 Form Fill, Kimi集成 Kimi Integration

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] Kimi WebBridge Skill · daemon 协议规范
  - [2] 知识矩阵总纲 v3.0 · 第拾贰章·核心链路
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. 依赖 Kimi 桌面客户端的 daemon 进程运行状态（端口占用/权限问题）。
2. 浏览器版本升级可能导致 DOM 选择器失效，需持续维护。
3. 截图/操作受浏览器视口大小限制，无法覆盖超出屏幕的内容。

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |
| 2026-07-06 | v1.1.0 | UID9622 | 补全摘要/关键词/溯源/局限/分类标签 | 已核验 |

## 分类标签

- 总纲模块：#浏览器桥接 #核心引擎 #L0对外通道 #Kimi集成
- 对外状态：#本地私有 · 不外发
- 审计色：#🟢绿色放行
- 八卦归属：☰ 乾卦（天·金·启动层）— 所有外部交互的起点
- 命令入口：`lh6 乾 start` → 启动桥接 / `lh kimi`
- 关键依赖：Kimi.app daemon / localhost:PORT

## DNA 签名

```
#龍芯⚡️丙午·甲午·辛亥·甲午·䷚颐-KIMI-WEBBRIDGE-FILE1-FILE2-v1.0-2
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
