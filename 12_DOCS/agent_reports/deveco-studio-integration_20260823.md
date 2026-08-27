# DevEco Studio 鸿蒙工具链深度集成报告

> DNA: #龍芯⚡️丙午·丙申·戊申·辰时·䷗复-DEVECO-INTEGRATION-v1.0
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 日期: 2026-08-23

## 一、安装结果（三件套全绿 ✅）

| 组件 | 版本 | 位置 | 状态 |
|:---|:---|:---|:---:|
| DevEco Studio | 26.0.0.621 | `/Applications/DevEco-Studio.app`（10G） | 🟢 已装 |
| hdc | 3.2.0e | `~/bin/hdc` 软链 + PATH | 🟢 可用 |
| ohpm | 26.0.0.410 | PATH `/Contents/tools/ohpm/bin` | 🟢 可用 |

## 二、PATH 配置（.zshrc 追加，2026-08-23）

```bash
# DevEco Studio 鸿蒙工具链 (2026-08-23 集成)
export PATH="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains:$PATH"
export PATH="/Applications/DevEco-Studio.app/Contents/tools/ohpm/bin:$PATH"
export NODE_HOME="/Applications/DevEco-Studio.app/Contents/tools/node/bin"
```

## 三、坑（已解决）

- **ohpm 不能软链**：ohpm 是 shell 脚本，软链后 `$0` 路径错乱找不到 `pm-cli.js`。必须用真实 PATH 调用。
- hdc 是 Mach-O 二进制可软链（`~/bin/hdc`），ohpm 脚本不可软链。

## 四、龍魂鸿蒙工程入口

| 工程 | 路径 | 说明 |
|:---|:---|:---|
| 龍魂鸿蒙 App | `harmonyos-universe/` | 完整应用工程（AppScope/entry） |
| 鸿蒙插件生态 | `integrations/harmonyos/` | 14个：longhun-bridge/longhun-sdk/tongxinyi/guoxue 等 |

## 五、冻结归档（不删只冻结）

- 两个原始安装包 zip → `_work/deveco_20260823/`（26.0.0.621.zip 3.7G + 6.1.1.300.zip 3.5G）
- 重复解压目录已清（4个），`~/Pictures` 32G → 11G，释放 21G

## 六、后续使用

- 打开龍魂鸿蒙工程：DevEco Studio → Open → `longhun-system/harmonyos-universe/`
- hdc 连真机：`hdc list targets`（USB/无线连接鸿蒙设备）
- 包管理：`ohpm install`（在工程目录执行）
- 旧版 6.1.1.300 未装（同名冲突），zip 冻结在 `_work/deveco_20260823/`，需要随时可装
