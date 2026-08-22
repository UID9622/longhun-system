> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：协议 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：GitHub
> 审核状态：草稿

**DNA**: `#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-PROTOCOL-CNSH-GITHUB-README-v1.0``  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

# 📄 CNSH GitHub README

> 本文檔按《龍魂文檔標準模板 v1.0》整理。
> 性質：協議 · 未經同行評審（如適用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 協作者：（待補充，如無請刪除此行）
> 授權：CC BY-NC-SA 4.0 · 科技主權歸屬 UID9622 · 中華人民共和國
> 平台：GitHub
> 審核狀態：草稿

**DNA**: `#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-PROTOCOL-CNSH-GITHUB-README-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

<!--#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-PROTOCOL-CNSH-GITHUB-README-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

# 📄 CNSH GitHub README

# 🇨🇳 CNSH - 中文原生编程语言

**DNA追溯码：** `#ZHUGEXIN⚡️2026-01-02-CNSH-GitHub-README`

<aside>
🌟

**让中国人用母语编程**

CNSH（Chinese Natural Semantic Humanity）是一门真正的中文编程语言。完全中文语法，零英文门槛，内置安全审计，性能与C语言相当。

**核心价值观：为人民服务、数据主权、本地优先、可审计**

</aside>

---

## ✨ 特性

- 🇨🇳 **纯中文语法** - 整数、小数、文本、如果、否则、循环
- 🛡️ **内置三色审计** - 🟢🟡🔴 自动安全检查
- ⚡ **高性能** - 转译为C代码，编译为机器码，性能与C相当
- 📦 **零依赖** - 只需Node.js和GCC
- 🎯 **易学易用** - 5分钟写出第一个程序
- 🔗 **与C互操作** - 可直接调用C库

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone [https://github.com/UID9622/CNSH.git](https://github.com/UID9622/CNSH.git)
cd CNSH

# 无需安装依赖，直接使用
```

### Hello World

创建文件 `hello.cnsh`：

```
# 我的第一个CNSH程序
函数 主函数() 返回类型 整数 {
  打印「🇨🇳 你好，CNSH！」
  返回 0
}
```

### 编译运行

```bash
# 编译为C代码
node cnsh-compiler.js hello.cnsh

# 编译为可执行文件
gcc hello.c -o hello

# 运行
./hello
```

**输出：**

```
🇨🇳 你好，CNSH！
```

---

## 📝 语法示例

### 变量声明

```
整数 年龄 = 25
小数 价格 = 99.99
文本 姓名 = "Lucky"
真假 完成 = 真
```

### 条件判断

```
如果【年龄 >= 18】{
  打印「成年人」
} 否则 {
  打印「未成年」
}
```

### 循环

```
循环【10】{
  打印「循环执行中」
}
```

### 函数

```
函数 计算和(整数 a, 整数 b) 返回类型 整数 {
  返回 a + b
}

函数 主函数() 返回类型 整数 {
  整数 结果 = 计算和(10, 20)
  打印「结果：30」
  返回 0
}
```

---

## 🎯 与C语言对比

| CNSH | C |
| --- | --- |
| `整数 x = 10` | `int x = 10;` |
| `如果【x > 5】{ }` | `if (x > 5) { }` |
| `循环【10】{ }` | `for (int i = 0; i < 10; i++) { }` |
| `函数 计算() 返回类型 整数` | `int 计算()` |
| `打印「文本」` | `printf("%s\n", "文本");` |

---

## 🛡️ 三色审计系统

CNSH内置三色审计，自动检测代码安全性：

- 🟢 **绿色** - 内容安全，直接编译
- 🟡 **黄色** - 敏感内容，警告提示
- 🔴 **红色** - 违规内容，阻断编译

```bash
🛡️ 阶段0：三色审计...
🟢 三色审计通过：内容安全
```

---

## 📚 文档

- [快速开始](docs/quick-start.md) - 5分钟上手
- [语言规范](docs/language-spec.md) - 完整语法参考
- [示例代码](docs/examples.md) - 从Hello World到实战项目
- [编译器架构](docs/compiler-arch.md) - 技术实现细节

---

## 🤝 参与贡献

欢迎参与CNSH语言的发展！

### 贡献方式

- 🐛 **报告Bug** - 提Issue描述问题
- 💡 **功能建议** - 提Issue说明需求
- 📝 **完善文档** - 提PR改进文档
- 💻 **贡献代码** - 提PR修复Bug或新增功能

### 贡献者公约

参与本项目请遵守[龙魂底线协议](docs/code-of-conduct.md)：

- ✅ 私域自由 - 本地使用完全自由
- ✅ 公域共治 - 公开分享遵守规则
- ✅ 互相尊重 - 文明交流，平等协作

---

## 🏅 徽章体系

为表彰贡献者，CNSH采用[徽章体系](docs/badges.md)：

- 🥉 **铜牌贡献者** - 首次PR合并
- 🥈 **银牌贡献者** - 5次PR合并
- 🥇 **金牌贡献者** - 20次PR合并
- 💎 **核心贡献者** - 长期维护

---

## 📋 开发路线图

### ✅ Stage 1 - MVP（已完成）

- ✅ 基础语法支持
- ✅ 词法分析器
- ✅ 语法分析器
- ✅ C代码生成
- ✅ 三色审计集成

### 🔄 Stage 2 - 标准库（进行中）

- 🔄 文件操作
- 🔄 网络请求
- 🔄 数据库连接
- 🔄 JSON处理

### ⏳ Stage 3 - 工具链（计划中）

- ⏳ IDE插件（VS Code）
- ⏳ 调试器
- ⏳ 包管理器
- ⏳ 测试框架

### 🌟 Stage 4 - 生态（愿景）

- 🌟 在线编程平台
- 🌟 教育课程体系
- 🌟 开源社区建设
- 🌟 企业级支持

---

## 🛠️ 技术架构

```
CNSH源码 (.cnsh)
    ↓
[词法分析 Lexer]
    ↓
[语法分析 Parser]
    ↓
[抽象语法树 AST]
    ↓
[三色审计 Security]
    ↓
[C代码生成 CodeGen]
    ↓
C代码 (.c)
    ↓
[GCC编译]
    ↓
可执行文件
```

---

## 📄 开源协议

本项目采用 [木兰宽松许可证 Mulan PSL v2](LICENSE)。

这是一个由中国开源软件推进联盟制定的开源协议，支持中文法律环境。

---

## 🌐 社区与支持

- 📧 **邮箱** - [uid9622@petalmail.com](mailto:uid9622@petalmail.com)
- 🇨🇳 **Gitee** - [https://gitee.com/UID9622/CNSH](https://gitee.com/UID9622/CNSH)
- 💬 **讨论区** - GitHub Discussions
- 📖 **文档中心** - [Notion文档](https://notion.so/uid9622)

---

## 💡 设计理念

### 为什么要做CNSH？

1. **文化自信** - 中国人用中文编程
2. **降低门槛** - 不懂英文也能编程
3. **技术平权** - 让更多人参与编程
4. **数据主权** - 从语言层面保护隐私

### CNSH的使命

**让编程回归母语，让技术服务人民**

---

## 🙏 致谢

感谢所有为CNSH做出贡献的人！

感谢中国传统文化（易经、道德经）为系统设计提供的哲学指导。

---

## 📊 项目状态

[GitHub stars](https://img.shields.io/github/stars/UID9622/CNSH?style=social)

GitHub stars

[GitHub forks](https://img.shields.io/github/forks/UID9622/CNSH?style=social)

GitHub forks

[GitHub issues](https://img.shields.io/github/issues/UID9622/CNSH)

GitHub issues

[GitHub license](https://img.shields.io/github/license/UID9622/CNSH)

GitHub license

---

**DNA追溯码：** `#ZHUGEXIN⚡️2026-01-02-CNSH-GitHub-README`

**创建者：** 💎 Lucky｜UID9622

**系统：** 🐉 龙魂系统 CNSH

**状态：** ✅ 可用

---

<p align="center">

<strong>🐉 CNSH龙魂系统 | UID9622 🐉</strong>

<em>传承中华智慧，创造工程奇迹</em>

<em>For the People, By the People</em>

</p>

---

## 摘要

（請在此用不超過 256 字說明本文檔的核心內容、性質與局限。）

## 關鍵詞

（請列出 5–10 個關鍵詞，中英文對照優先。）

## 引用與溯源

- 本文檔引用或參考了以下來源：
  - [1] （請填寫）
- 相關龍魂系統文檔：
  - 《龍魂文檔標準模板 v1.0》(#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 誠實局限

1. （請列出本分析的第一條局限或不確定性。）
2. （請列出第二條。）
3. （請列出第三條。）

## 修改記錄

| 日期 | 版本 | 修改人 | 修改內容 | 審核狀態 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文檔標準模板 v1.0》整理 | 草稿 |

## 分類標籤

- 總綱模塊：（請勾選，例如 #知識矩陣 #安全域）
- 對外狀態：（請勾選，例如 #Gitee #GitHub #CSDN）
- 審計色：#黃色待審

## DNA 簽名

```
#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-PROTOCOL-CNSH-GITHUB-README-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```


---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-15 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-PROTOCOL-CNSH-GITHUB-README-v1.0`
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
