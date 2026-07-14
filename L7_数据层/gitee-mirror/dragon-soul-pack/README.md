> #龍芯⚡️丙午·丙申·乙卯·丙戌·䷷旅-DRAGONSOULPACK-README-v1.0

# 🐉 DragonSoulPack · 龍魂系统整合包

**归属**: UID9622（诸葛鑫·Lucky）原创  
**许可证**: 木兰宽松许可证 v2.0 / MIT 双许可  
**主仓**: https://gitee.com/uid9622/dragon-soul-pack  
**镜像**: https://github.com/UID9622/dragon-soul-pack

---

## 一句话说明

DragonSoulPack 是龍魂系统的「一键安装整合包」，把 CNSH 中文编程语言、编辑器避坑插件、本地服务器和龍魂中文字体打包成可直接运行的套件，服务于国产化、鸿蒙生态和中文原生开发。

---

## 包内组件

| 目录 | 组件 | 说明 |
|---|---|---|
| `CNSH编译器/` | CNSH 中文编程语言 | JS 实现 CNSH→C 转译，含示例和核心库 |
| `CNSH编辑器避坑插件/` | VS Code 插件 | 语法高亮、补全、变量审计、一键编译 |
| `UID9622本地服务器/` | 龍魂控制台 | 本地 Web 控制台 + CNSH 闸门执行器 |
| `字体支持/` | LonghunFont | 龍魂中文字体、安装脚本、样张 |
| `docs/` | 文档 | 用户手册、开源发布流程、API 参考 |
| `scripts/` | 脚本 | install.sh、start_all.sh |

---

## 快速开始

```bash
# 1. 克隆整合包
git clone https://gitee.com/uid9622/dragon-soul-pack.git
cd dragon-soul-pack

# 2. 一键安装依赖
bash scripts/install.sh

# 3. 启动全部服务
bash scripts/start_all.sh
```

---

## 鸿蒙生态适配

本整合包所有组件均遵循《鸿蒙 API 交付标准模板 v1.0》7 项检查：

1. 目录结构清晰
2. 代码可运行
3. 关键函数有注释
4. 包含使用示例
5. 错误处理完整
6. 不依赖境外私有服务
7. 文档与代码同步

---

## 许可证

- CNSH 编译器：Mulan PSL v2.0
- VS Code 插件：Mulan PSL v2.0
- 本地服务器：MIT + 伦理附加条款
- 字体：SIL Open Font License 1.1

---

**DNA**: `#龍芯⚡️丙午·丙申·乙卯·丙戌·䷷旅-DRAGONSOULPACK-README-v1.0`
