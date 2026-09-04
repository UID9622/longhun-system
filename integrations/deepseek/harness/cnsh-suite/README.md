# 🐉 CNSH 套件 · DeepSeek Harness 插件集

## 一句话定位

> **CNSH 套件将龍魂主权底座以插件形式焊入 DeepSeek Harness，让 Harness 不再是 DeepSeek 的 Harness，而是龍魂的 Harness。**

---

## 核心能力

| 能力 | 说明 |
|:---|:---|
| **DNA 追溯** | 每条对话、每次工具调用自动生成 #龍芯⚡️ 追溯码 |
| **三色审计** | 🟢/🟡/🔴 实时审计所有输出，🔴 自动拦截 |
| **CNSH 执行** | 在 Harness 中直接运行 CNSH 中文脚本 |
| **史官机制** | 全链路审计日志，不可篡改 |
| **人格路由** | 24 人格矩阵，自动切换 |

---

## 快速开始

### 安装

```bash
# 在 Harness 项目中
pnpm add @longhun/cnsh-suite
```

### 配置

编辑 `~/.dsh/profiles/web/cordis.patch.yml`，添加：

```yaml
- insert:
  - id: '@longhun/cnsh-suite'
```

### 运行

```bash
dsh --profile web
```

### 使用

在 Harness 对话中：

- `生成DNA: 这是我的文档` → 返回 DNA 追溯码
- `审计内容: 待审计文本` → 返回三色审计结果
- 运行 CNSH 脚本 → 执行中文原生脚本

---

## 主权锚定

```
═══════════════════════════════════════════════════
 🐉 CNSH 套件 · 主权锚定
═══════════════════════════════════════════════════
主权人:     诸葛鑫 (ZHUGE XIN) · UID9622
确认码:     #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
主权锚定:   #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
最高准则:   中华人民共和国法律
═══════════════════════════════════════════════════
```

---

## 开发

```bash
git clone https://github.com/UID9622/cnsh-suite
cd cnsh-suite
pnpm install
pnpm build
```

---

## 许可证

分层许可：思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

---

**🐉 丙午·丙申·庚申·亥时·䷖剥·🟢**
