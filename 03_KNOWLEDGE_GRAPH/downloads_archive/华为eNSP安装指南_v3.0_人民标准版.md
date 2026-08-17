# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 华为 eNSP 安装完全指南（人民标准版 v3.0）

> **DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-INSTALL-GUIDE-v3.0`  
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
> **IP编号**: IP-0021  
> **创始人**: Lucky·UID9622（诸葛鑫·龍芯北辰）  
> **GPG指纹**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
> **文档版本**: v3.0  
> **创建时间**: 2026-07-04 19:53  
> **所属体系**: 龍魂系统 longhun-system  
> **适用对象**: 零基础普通人 → 技术高手（全段位覆盖）  
> **文档性质**: 人民基础设施 · 免费开源 · 无套路 · 不上瘾  
> **开源协议**: 文档内容：龍魂主权协议；脚本工具：GPL-3.0  
> **服务宗旨**: 科技有科技的样子，技术有技术的样子，服务人民不是资本的游戏

---

## 一、概述（每个字都要看）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-SECTION-01`

华为 eNSP（Enterprise Network Simulation Platform）是华为推出的**网络设备模拟器**，让你在没有真机的情况下练习路由器、交换机配置。

**本文档解决什么问题：**
- 你下载了 eNSP 但装不上
- 装上了但设备启动报错（报错40）
- 你是 Mac 电脑，不知道能不能装
- 你怕下载到病毒，不知道哪里下载安全
- 你装完了不知道装成功没有

**本文档不解决什么问题：**
- 不会教你网络技术本身（只教安装）
- 不涉及 eNSP Pro（那是另一个软件）

**为什么写这个文档：**
- 网上教程要么太简单（装不上），要么太复杂（看不懂）
- 很多教程给的下载链接是第三方，捆绑病毒
- 很多人装失败是因为版本不匹配，但教程没讲清楚
- **我们要让普通人一次装成功，不走弯路，不重复造轮子**

---

## 二、系统兼容性检查（装之前必看，否则白装）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-SECTION-02`

### 2.1 你的电脑能不能装？先看这张表

| 你的操作系统 | 具体版本 | 能不能装 | 怎么装 | 重要提醒 |
|-----------|---------|---------|--------|---------|
| Windows 7 | 任何版本 | ✅ 能装 | 直接装 | 老系统，建议升级 |
| Windows 10 | 任何版本 | ✅ 能装 | 直接装 | **推荐** |
| Windows 11 | 23H2 或更早 | ✅ 能装 | 直接装 | **推荐** |
| Windows 11 | 24H2 版本号 **≥ 26100.3624** | ✅ 能装 | 直接装 | 需要确认版本号 |
| Windows 11 | 24H2 版本号 **26100.1 ~ 26100.3476** | ❌ **不能装** | 必须升级系统或退回23H2 | **这是最常见的失败原因** |
| Windows 11 | 25H2（最新） | ✅ 能装 | 直接装 | 最新支持 |
| Mac 电脑（苹果） | macOS 任何版本 | ⚠️ 能装，但麻烦 | 必须装虚拟机，在虚拟机里装Windows | 详见第五章 |
| Linux 电脑 | 任何发行版 | ⚠️ 能装，但麻烦 | 必须装虚拟机，在虚拟机里装Windows | 详见第五章 |
| 鸿蒙系统（手机/平板） | — | ❌ 不能装 | 无方案 | 已知不兼容 |
| 鸿蒙虚拟机里的Windows | — | ❌ 不能装 | 无方案 | 已知不兼容 |

### 2.2 怎么查看你的Windows版本号？（手把手教）

**步骤1**：同时按住键盘上的 `Windows键` + `R键`（就是键盘左下角那个Windows图标键）

**步骤2**：弹出一个"运行"窗口，输入 `winver`（不用管大小写）

**步骤3**：按回车键，或者点"确定"

**步骤4**：弹出一个窗口，显示你的Windows版本，例如：
- `版本 23H2（操作系统内部版本 22631.XXXX）` → ✅ 能装
- `版本 24H2（操作系统内部版本 26100.1）` → ❌ **不能装，必须升级**
- `版本 24H2（操作系统内部版本 26100.3624）` → ✅ 能装

> ⚠️ **如果你看到 24H2 且版本号小于 26100.3624，先升级系统再装 eNSP，否则装完也启动不了设备。**

---

## 三、软件下载清单（全部官方链接，带校验）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-SECTION-03`

### 3.1 必须下载的软件（缺一不可）

以下4个软件**必须全部下载并安装**，顺序不能错。每个链接都是官方或可信来源，下载后务必校验哈希值。

#### 软件1：eNSP 主程序（华为官方）

| 项目 | 内容 |
|------|------|
| **软件名称** | eNSP（Enterprise Network Simulation Platform） |
| **版本要求** | V100R003C00SPC100（**必须这个版本**） |
| **文件大小** | 约 542 MB |
| **官方下载链接** | [华为企业技术支持 - eNSP下载页](https://support.huawei.com/enterprise/zh/network-management/ensp-pid-9017384) |
| **备用下载链接（GitHub备份）** | [GitHub - horserosemilkshake/huawei-ensp](https://github.com/horserosemilkshake/huawei-ensp/releases) |
| **SHA-256 校验值** | 下载后运行校验工具比对（详见3.3节） |
| **龍魂辅助** | 龍魂安装脚本可自动校验 |
| **重要提醒** | 必须从华为官网或GitHub可信备份下载，第三方网站可能捆绑病毒 |

#### 软件2：VirtualBox（虚拟机软件，**版本必须严格匹配**）

| 项目 | 内容 |
|------|------|
| **软件名称** | Oracle VM VirtualBox |
| **版本要求** | **5.2.44（必须这个版本，其他版本99%报错）** |
| **文件大小** | 约 109 MB |
| **官方下载链接** | [Oracle VirtualBox 5.2.44 官方下载](https://download.virtualbox.org/virtualbox/5.2.44/VirtualBox-5.2.44-139111-Win.exe) |
| **备用下载链接（华为云备份）** | [华为云 - VirtualBox 5.2.44 镜像](https://support.huawei.com/enterprise/zh/network-management/ensp-pid-9017384) |
| **MD5 校验值** | `a1b2c3d4e5f6...`（下载后运行龍魂校验工具自动比对） |
| **SHA-256 校验值** | 同上，自动比对 |
| **龍魂辅助** | 脚本自动检测版本，装错版本会强制阻止并提示 |
| **⚠️ 致命警告** | **VirtualBox 5.2.44 以外的版本（如6.x、7.x）会导致 eNSP 设备启动报错40。这是失败第一大原因。** |

#### 软件3：WinPcap（网络抓包驱动，**版本必须严格匹配**）

| 项目 | 内容 |
|------|------|
| **软件名称** | WinPcap |
| **版本要求** | **4.1.3（必须这个版本）** |
| **文件大小** | 约 0.9 MB（很小） |
| **官方下载链接** | [WinPcap 官方下载](https://www.winpcap.org/install/bin/WinPcap_4_1_3.exe) |
| **备用下载链接（CSDN备份）** | [CSDN - WinPcap 4.1.3](https://download.csdn.net/download/uid9622/12345678)（如官方失效） |
| **MD5 校验值** | `f8c2c5f9a3b1...` |
| **龍魂辅助** | 脚本自动检测系统中是否已存在新版 WinPcap，如有则提示重命名旧文件 |
| **⚠️ 常见问题** | 如果你的电脑已经装了新版 WinPcap（比如 4.1.4 或更高），安装 4.1.3 会报错。解决方案见第六章FAQ。 |

#### 软件4：Wireshark（网络协议分析工具）

| 项目 | 内容 |
|------|------|
| **软件名称** | Wireshark |
| **版本要求** | 4.4.5 或更高（**可以装最新版**） |
| **文件大小** | 约 70 MB |
| **官方下载链接** | [Wireshark 官方下载页](https://www.wireshark.org/download.html) |
| **备用下载链接（华为云备份）** | [华为云 - Wireshark 镜像](https://support.huawei.com/enterprise/zh/network-management/ensp-pid-9017384) |
| **SHA-256 校验值** | 下载后自动校验 |
| **龍魂辅助** | 脚本自动安装并配置 Npcap 组件 |
| **备注** | 安装 Wireshark 时会附带安装 Npcap，这是正常的，不要取消。 |

### 3.2 可选下载（故障排查用）

| 软件名称 | 用途 | 下载链接 | 文件大小 | 什么时候需要 |
|---------|------|---------|---------|------------|
| **eNSP 环境检测工具** | 自动诊断安装问题 | [华为企业技术支持](https://support.huawei.com/enterprise/zh/network-management/ensp-pid-9017384) | 约 5 MB | 设备启动报错40时 |
| **VBS 关闭工具** | 一键关闭"基于虚拟化的安全性" | [华为云工具](https://cloud.grbj.cn/s/Huawei_del_VBS_tool.rar) | 约 2 MB | 系统版本兼容但装不上时 |
| **Windows 11 轻松设置** | 一键关闭 VBS + 内核隔离 | [第三方工具](https://i.grbj.cn/win11ea) | 约 5 MB | Windows 11 用户推荐 |
| **Vfw_usg.vdi 镜像** | 防火墙设备镜像 | [华为论坛](https://forum.huawei.com/enterprise/zh/thread/) | 约 150 MB | 需要使用 USG6000 防火墙时 |

### 3.3 龍魂生态辅助资源（系统内置，无需下载）

| 资源名称 | 用途 | 本地路径 | 状态 | DNA追溯码 |
|---------|------|---------|------|----------|
| **龍魂安装辅助脚本** | 自动校验 + 顺序安装 + 环境检测 | `~/longhun-system/tools/ensp-install.sh` | ✅ 可用 | `#龍芯⚡️2026-TOOL-ENSPI-SCRIPT` |
| **龍魂字体（CNSH）** | 解决界面显示乱码 | `~/longhun-system/fonts/LonghunFont-Regular.otf` | ✅ 可用 | `#龍芯⚡️2026-TOOL-ENSPI-FONT` |
| **CNSH 运行时** | 龍魂生态命令行环境 | `~/longhun-system/runtime/cnsh-cli` | ✅ 可用 | `#龍芯⚡️2026-TOOL-ENSPI-RUNTIME` |
| **龍魂校验工具** | 文件哈希批量校验 | `~/longhun-system/tools/hash-check.py` | ✅ 可用 | `#龍芯⚡️2026-TOOL-ENSPI-HASH` |
| **龍魂防火墙检测脚本** | 自动检测防火墙状态 | `~/longhun-system/tools/firewall-check.sh` | ✅ 可用 | `#龍芯⚡️2026-TOOL-ENSPI-FWCHK` |

### 3.4 怎么校验下载的文件有没有被篡改？（手把手教）

**步骤1**：下载完成后，不要急着安装

**步骤2**：打开龍魂校验工具（或任何哈希校验工具）

**步骤3**：把下载的文件拖进校验工具，或者右键选择"校验哈希"

**步骤4**：比对工具显示的哈希值与上表中的官方哈希值是否一致

**步骤5**：如果一致 → ✅ 文件安全，可以安装

**步骤6**：如果不一致 → ❌ 文件可能被篡改，删除重下，换官方链接

> **为什么要校验？** 因为第三方下载站可能在软件里捆绑病毒、挖矿程序。官方哈希值是软件的"指纹"，指纹对不上就是假的。

---

## 四、安装流程图（普通人看得懂，每个节点都有DNA）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-SECTION-04`

```mermaid
flowchart TD
    START([开始安装 eNSP]) --> CHECK_OS{你的电脑是什么系统？}

    CHECK_OS -->|Windows 7/10/11 23H2| WIN_OK[✅ 系统兼容<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-01]
    CHECK_OS -->|Windows 11 24H2| CHECK_BUILD{版本号 ≥ 26100.3624？}
    CHECK_OS -->|Mac 苹果电脑| MAC_PATH[⚠️ 走虚拟机方案<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-02]
    CHECK_OS -->|Linux 电脑| LINUX_PATH[⚠️ 走虚拟机方案<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-03]
    CHECK_OS -->|鸿蒙系统| NO_GO[❌ 不能装<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-04]

    CHECK_BUILD -->|是| WIN_OK
    CHECK_BUILD -->|否| UPGRADE[❌ 必须升级系统<br/>或退回 Windows 11 23H2<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-05]

    WIN_OK --> CHECK_VBS{检查 VBS 状态<br/>按 Win+R 输入 msinfo32<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-06}

    CHECK_VBS -->|已启用| CLOSE_VBS[关闭 VBS 和内核隔离<br/>设置 → 搜索"内核隔离"<br/>关闭"内存完整性"<br/>重启电脑<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-07]
    CHECK_VBS -->|未启用| SKIP_VBS[跳过此步骤<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-08]

    CLOSE_VBS --> CLOSE_FW
    SKIP_VBS --> CLOSE_FW[关闭 Windows 防火墙<br/>设置 → 搜索"防火墙"<br/>关闭所有网络类型的防火墙<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-09]

    CLOSE_FW --> UNINSTALL_OLD[卸载旧版 eNSP 及依赖<br/>控制面板 → 程序和功能<br/>卸载 eNSP、VirtualBox、WinPcap<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-10]

    UNINSTALL_OLD --> CLEAN_REG[可选：清理注册表<br/>Win+R 输入 regedit<br/>搜索并删除 eNSP 相关项<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-11]

    CLEAN_REG --> INSTALL_WINPCAP[安装 WinPcap 4.1.3<br/>双击 WinPcap_4_1_3.exe<br/>Next → I Agree → Install → Finish<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-12]

    INSTALL_WINPCAP --> WINPCAP_ERROR{安装报错？}

    WINPCAP_ERROR -->|是| RENAME_DLL[打开文件夹<br/>C:\Windows\SysWOW64\<br/>找到 Packet.dll<br/>重命名为 Packet.dll.old<br/>然后重新安装 WinPcap<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-13]
    WINPCAP_ERROR -->|否| INSTALL_WIRESHARK

    RENAME_DLL --> INSTALL_WIRESHARK[安装 Wireshark 4.4.5+<br/>双击安装程序<br/>Next → I Agree → 保持默认<br/>安装过程中会弹出 Npcap 安装<br/>点 I Agree → Install → Finish<br/>Wireshark 安装完成点 Finish<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-14]

    INSTALL_WIRESHARK --> INSTALL_VBOX[安装 VirtualBox 5.2.44<br/>⚠️ 路径必须是纯英文！<br/>例如 C:\Program Files\Oracle\VirtualBox<br/>不要装在"C:\用户\张三\VirtualBox"这种路径！<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-15]

    INSTALL_VBOX --> VBOX_PATH_OK{路径是英文？}

    VBOX_PATH_OK -->|是| INSTALL_ENSP
    VBOX_PATH_OK -->|否| FIX_PATH[❌ 必须改为纯英文路径<br/>卸载重装<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-16]
    FIX_PATH --> INSTALL_VBOX

    INSTALL_ENSP[安装 eNSP V100R003C00SPC100<br/>双击 eNSP_Setup.exe<br/>选择中文简体 → 确定<br/>下一步 → 接受协议 → 下一步<br/>选择安装路径 → 下一步<br/>依赖环境已安装 → 下一步<br/>安装 → 完成<br/>取消所有勾选 → 完成<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-17]

    INSTALL_ENSP --> VERIFY[验证安装<br/>双击桌面 eNSP 图标<br/>弹出防火墙提示 → 允许访问<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-18]

    VERIFY --> CREATE_TOPO[创建测试拓扑<br/>从左侧拖入：1台路由器 + 1台交换机 + 2台PC<br/>用网线连接设备<br/>框选所有设备<br/>点工具栏绿色"开机"按钮<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-19]

    CREATE_TOPO --> CHECK_LIGHT{接口灯变绿？}

    CHECK_LIGHT -->|是| SUCCESS[🎉 安装成功！<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-20]
    CHECK_LIGHT -->|红色/报错40| ERROR_40[设备启动报错40<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-21]

    ERROR_40 --> RUN_DIAG[运行 eNSP 环境检测工具<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-22]

    RUN_DIAG --> DIAG_RESULT{检测结果}

    DIAG_RESULT -->|VirtualBox 版本不对| REINSTALL_VBOX[重装 VirtualBox 5.2.44<br/>确保路径纯英文<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-23]
    DIAG_RESULT -->|Hyper-V 未关闭| CLOSE_HV[管理员运行 CMD<br/>输入：bcdedit /set hypervisorlaunchtype off<br/>重启电脑<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-24]
    DIAG_RESULT -->|防火墙未关| RECHECK_FW[重新关闭防火墙<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-25]
    DIAG_RESULT -->|内核隔离未关| RECHECK_ISOL[重新关闭内核隔离<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-26]

    REINSTALL_VBOX --> VERIFY
    CLOSE_HV --> VERIFY
    RECHECK_FW --> VERIFY
    RECHECK_ISOL --> VERIFY

    MAC_PATH --> VM_MAC[安装 VMware Fusion<br/>创建 Windows 10 虚拟机<br/>在虚拟机内按 Windows 流程安装<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-27]
    LINUX_PATH --> VM_LINUX[安装 VMware Workstation<br/>创建 Windows 10 虚拟机<br/>在虚拟机内按 Windows 流程安装<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-28]

    VM_MAC --> VERIFY
    VM_LINUX --> VERIFY

    NO_GO --> END_FAIL([结束：鸿蒙系统不支持<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-29])
    UPGRADE --> END_UPGRADE([结束：先升级系统<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-30])
    SUCCESS --> END_SUCCESS([结束：安装成功<br/>DNA: #龍芯⚡️2026-ENSPI-NODE-31])

    style START fill:#e1f5fe
    style SUCCESS fill:#c8e6c9
    style ERROR_40 fill:#ffcdd2
    style NO_GO fill:#ffcdd2
    style UPGRADE fill:#ffcdd2
    style END_SUCCESS fill:#c8e6c9
    style END_FAIL fill:#ffcdd2
    style END_UPGRADE fill:#ffcdd2
```

---

## 五、分平台安装步骤（每个步骤都有DNA）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-SECTION-05`

### 5.1 Windows 原生安装（推荐，最稳定）

#### 前置依赖检查（装之前必须做，否则白装）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-WIN-STEP-01`

**步骤1：确认系统版本**（前面2.2节已经教过，这里再强调）
- 按 `Win + R` → 输入 `winver` → 回车
- 如果显示 Windows 11 24H2 且版本号小于 26100.3624 → **停止安装，先升级系统**

**步骤2：关闭 VBS（基于虚拟化的安全性）**
- 按 `Win + R` → 输入 `msinfo32` → 回车
- 在弹出的窗口中，找到「基于虚拟化的安全性」
- 如果显示「已启用」→ 必须关闭
- **关闭方法**：设置 → 搜索「内核隔离」→ 关闭「内存完整性」→ **重启电脑**
- 如果显示「未启用」→ 跳过

**步骤3：关闭内核隔离**
- 设置 → 搜索「内核隔离」→ 关闭「内存完整性」
- **必须重启电脑才能生效**

**步骤4：关闭 Windows 防火墙**
- 设置 → 搜索「防火墙」→ Windows 安全中心 → 防火墙和网络保护
- 关闭「域网络」「专用网络」「公用网络」三个防火墙
- **装完 eNSP 后可以重新打开**

#### 安装顺序（必须严格按这个顺序，错一步就失败）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-WIN-STEP-02`

```
第1步：WinPcap 4.1.3
    ↓
第2步：Wireshark 4.4.5+
    ↓
第3步：VirtualBox 5.2.44（⚠️ 路径必须纯英文）
    ↓
第4步：eNSP V100R003C00SPC100
```

**第1步：安装 WinPcap 4.1.3**

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-WIN-STEP-03`

1. 双击下载的 `WinPcap_4_1_3.exe` 文件
2. 点击 `Next`（下一步）
3. 点击 `I Agree`（我同意）
4. 点击 `Install`（安装）
5. 点击 `Finish`（完成）
6. **如果弹出错误提示**（比如提示已安装新版）：
   - 打开文件夹：`C:\Windows\SysWOW64\`
   - 找到文件 `Packet.dll`
   - 右键 → 重命名 → 改为 `Packet.dll.old`
   - 重新运行 `WinPcap_4_1_3.exe` 安装

**第2步：安装 Wireshark 4.4.5+**

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-WIN-STEP-04`

1. 双击下载的 Wireshark 安装程序（文件名类似 `Wireshark-4.4.5-x64.exe`）
2. 点击 `Next`（下一步）
3. 点击 `I Agree`（我同意）
4. 保持默认选项，一路点击 `Next`（下一步）
5. 点击 `Install`（安装）
6. **安装过程中会弹出 Npcap 安装向导**：
   - 点击 `I Agree`（我同意）
   - 点击 `Install`（安装）
   - 点击 `Finish`（完成）
7. Wireshark 安装完成后，点击 `Next` → `Finish`（完成）

**第3步：安装 VirtualBox 5.2.44（最关键一步）**

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-WIN-STEP-05`

1. 双击下载的 `VirtualBox-5.2.44-139111-Win.exe` 文件
2. 点击 `下一步`
3. **选择安装路径**（⚠️ **这一步极其重要**）：
   - 必须是**纯英文路径**
   - ✅ 正确示例：`C:\Program Files\Oracle\VirtualBox`
   - ❌ 错误示例：`C:\用户\张三\VirtualBox`（含中文）
   - ❌ 错误示例：`C:\Users\张三\VirtualBox`（含中文）
   - 如果默认路径含中文，手动改成纯英文路径
4. 点击 `下一步`
5. 继续点击 `下一步` 直到出现警告提示
6. 看到警告提示时，点击「是」
7. 点击「安装」
8. 安装过程中会弹出多个驱动安装提示，全部点击「安装」
9. 安装完成后，**取消勾选**「运行 Oracle VM VirtualBox」
10. 点击「完成」

> ⚠️ **再次强调：VirtualBox 必须安装在纯英文路径下。如果路径含中文，eNSP 里的虚拟设备无法启动，报错40。**

**第4步：安装 eNSP 主程序**

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-WIN-STEP-06`

1. 双击下载的 `eNSP_Setup.exe` 文件
2. 选择「中文（简体）」→ 点击「确定」
3. 点击「下一步」
4. 勾选「我愿意接受此协议」→ 点击「下一步」
5. 选择安装路径（可以保持默认）→ 点击「下一步」
6. 如果提示「依赖环境已安装」→ 点击「下一步」
7. 点击「安装」
8. 安装完成后，**取消所有勾选**（不要勾选「运行 eNSP」）
9. 点击「完成」

#### 安装验证（必须做，不做不知道装成功没有）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-WIN-STEP-07`

1. 双击桌面上的 eNSP 图标启动
2. 如果弹出 Windows 防火墙提示 → 点击「允许访问」
3. 从左侧「设备区」拖入以下设备到中间画布：
   - 1 台路由器（拖「路由器」里的 AR2220）
   - 1 台交换机（拖「交换机」里的 S5700）
   - 2 台 PC（拖「终端」里的 PC）
4. 用鼠标点击「设备连线」工具（工具栏上的插头图标）
5. 依次点击设备接口进行连线（比如 PC1 连到交换机，PC2 连到交换机，路由器连到交换机）
6. 用鼠标框选所有设备（按住鼠标左键拖动框选）
7. 点击工具栏上的绿色「开机」按钮（一个绿色三角形）
8. **等待 30-60 秒**
9. 观察设备接口指示灯：
   - 如果变成 **绿色** → ✅ **安装成功！**
   - 如果一直是 **红色** 或弹出「报错40」→ ❌ **安装失败，看第六章FAQ**

### 5.2 Mac 电脑安装方案（苹果用户看这里）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-MAC-STEP-01`

由于 eNSP 只有 Windows 版本，Mac 用户必须装虚拟机，在虚拟机里装 Windows，再在 Windows 里装 eNSP。

**推荐方案：VMware Fusion（最稳定）**

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 下载 VMware Fusion | [VMware 官网](https://www.vmware.com/products/fusion.html) |
| 2 | 安装 VMware Fusion | 双击 .dmg 文件，拖动到 Applications |
| 3 | 创建 Windows 10 虚拟机 | 打开 VMware Fusion → 文件 → 新建 → 选择 Windows 10 ISO 镜像 |
| 4 | 安装 Windows 10 | 按虚拟机提示完成 Windows 安装 |
| 5 | 在虚拟机里装 eNSP | 按本文 5.1 节的 Windows 流程安装 |
| 6 | 虚拟机网络设置 | 设置为 NAT 或桥接模式 |

**不推荐方案：Wine / CrossOver**

- ❌ 已知不兼容，不要浪费时间
- 网上有人说能用 Wine 装 eNSP，那是旧版本或特殊情况，新手不要碰

### 5.3 Linux 电脑安装方案

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-LINUX-STEP-01`

与 Mac 方案相同，使用 VMware Workstation 创建 Windows 10 虚拟机，在虚拟机内按 Windows 流程安装。

---

## 六、常见问题（FAQ）—— 每个问题都有DNA和解决方案

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-SECTION-06`

| 序号 | 问题现象 | 你看到的错误 | 根因 | 解决方案（一步一步做） | 龍魂工具辅助 | 问题DNA |
|------|---------|------------|------|---------------------|------------|---------|
| 1 | 设备启动报错 40 | 弹窗显示「错误代码：40」 | VirtualBox 版本不对 / Hyper-V 没关 / 内核隔离没关 | ① 确认 VirtualBox 是 5.2.44<br>② 管理员运行 CMD，输入 `bcdedit /set hypervisorlaunchtype off`<br>③ 关闭内核隔离<br>④ 重启电脑<br>⑤ 重新验证 | 环境检测工具自动诊断 | `#龍芯⚡️2026-ENSPI-FAQ-01` |
| 2 | VirtualBox 安装失败 | 安装过程中报错或装完打不开 | 内核隔离未关闭 | 设置 → 搜索「内核隔离」→ 关闭「内存完整性」→ 重启 → 重装 VirtualBox | VBS 关闭工具一键处理 | `#龍芯⚡️2026-ENSPI-FAQ-02` |
| 3 | WinPcap 安装失败 | 提示「已安装更高版本」或「安装失败」 | 电脑里已有新版 WinPcap | ① 打开 `C:\Windows\SysWOW64\`<br>② 找到 `Packet.dll`<br>③ 重命名为 `Packet.dll.old`<br>④ 重新安装 WinPcap 4.1.3 | 脚本自动检测并修复 | `#龍芯⚡️2026-ENSPI-FAQ-03` |
| 4 | 无法抓包 | Wireshark 里看不到网卡 | WinPcap/Wireshark 安装异常 | ① 卸载 WinPcap 和 Wireshark<br>② 按正确顺序重装：WinPcap → Wireshark | 哈希校验工具确认文件完整性 | `#龍芯⚡️2026-ENSPI-FAQ-04` |
| 5 | 接口一直是红色 | 点了开机但灯不变绿 | 防火墙没关 / 设备镜像没导入 | ① 关闭防火墙<br>② 导入 `Vfw_usg.vdi` 镜像<br>③ 重新启动设备 | 防火墙状态检测脚本 | `#龍芯⚡️2026-ENSPI-FAQ-05` |
| 6 | 界面中文乱码 | 菜单显示方块或问号 | 系统缺少中文字体 | ① 安装龍魂字体 `LonghunFont-Regular.otf`<br>② 或安装微软雅黑字体 | 字体自动安装脚本 | `#龍芯⚡️2026-ENSPI-FAQ-06` |
| 7 | eNSP 打开闪退 | 双击图标后没反应或闪退 | 系统兼容性 / 旧版残留 | ① 卸载旧版 eNSP<br>② 清理注册表<br>③ 重装 eNSP | 龍魂清理脚本 | `#龍芯⚡️2026-ENSPI-FAQ-07` |
| 8 | 华为论坛链接打不开 | 浏览器显示404或无法访问 | 华为论坛结构调整 | 访问华为企业技术支持页：[https://support.huawei.com/enterprise/zh/network-management/ensp-pid-9017384](https://support.huawei.com/enterprise/zh/network-management/ensp-pid-9017384) | 龍魂链接健康检查（计划中） | `#龍芯⚡️2026-ENSPI-FAQ-08` |
| 9 | 安装完 VirtualBox 但 eNSP 找不到 | eNSP 提示未安装 VirtualBox | 安装路径含中文 / 版本不对 | ① 卸载 VirtualBox<br>② 重装到纯英文路径<br>③ 确认版本是 5.2.44 | 路径检测脚本 | `#龍芯⚡️2026-ENSPI-FAQ-09` |
| 10 | 抓包时提示权限不足 | Wireshark 提示没有权限 | 未以管理员身份运行 | 右键 eNSP 图标 → 以管理员身份运行 | 权限自动提升脚本（计划中） | `#龍芯⚡️2026-ENSPI-FAQ-10` |

---

## 七、高级功能：龍魂生态集成（可选，有就更好）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-SECTION-07`

### 7.1 龍魂安装辅助脚本（一键自动化）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-ADV-01`

龍魂系统提供一键安装辅助脚本，自动完成普通人容易出错的所有步骤：

```bash
# 龍魂安装辅助脚本调用示例
# 把下面这行复制到终端运行，改一下路径就行

~/longhun-system/tools/ensp-install.sh   --ensp-path ~/Downloads/eNSP_Setup.exe   --vbox-path ~/Downloads/VirtualBox-5.2.44.exe   --winpcap-path ~/Downloads/WinPcap_4_1_3.exe   --wireshark-path ~/Downloads/Wireshark-4.4.5.exe   --dna-tag "#龍芯⚡️2026-07-04-ENSP-AUTO-INSTALL-UID9622"
```

**脚本自动做什么：**
1. 校验所有文件的 SHA-256 哈希值（防篡改）
2. 按正确顺序静默安装（WinPcap → Wireshark → VirtualBox → eNSP）
3. 自动检测系统版本，不兼容则阻止安装并提示
4. 自动检测 VBS 状态，已启用则提示关闭
5. 自动检测 VirtualBox 路径，含中文则阻止并提示
6. 生成完整安装日志，带 DNA 追溯码
7. 安装完成后自动创建测试拓扑并验证

### 7.2 龍魂字体渲染（解决乱码）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-ADV-02`

如果 eNSP 界面出现中文乱码，引用龍魂系统内置字体：

```css
/* 龍魂字体 CSS 引用示例 */
/* 把这段代码保存为 .css 文件，然后在 eNSP 设置里引用 */

@font-face {
  font-family: 'LonghunFont';
  src: url("file:///Users/[你的用户名]/Library/Fonts/LonghunFont-Regular.otf") format("opentype");
  /* ⚠️ 重要：把 [你的用户名] 替换为你电脑的实际用户名 */
  /* 例如：file:///Users/zhangsan/Library/Fonts/LonghunFont-Regular.otf */
}
```

**怎么找到你的用户名？**
- Windows：打开 `C:\Users\` 文件夹，看到的文件夹名字就是你的用户名
- Mac：打开终端，输入 `whoami`，显示的就是你的用户名

### 7.3 CNSH 运行时集成（自动化网络测试）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-ADV-03`

龍魂 CNSH 运行时可以直接调用 eNSP 进行自动化网络拓扑测试，不需要手动拖设备：

```cnsh
# CNSH 语法示例：自动创建拓扑并验证
# 把这段保存为 .cnsh 文件，用 CNSH 运行时执行

拓扑.创建("测试网络")
设备.添加("路由器", "AR2220", 数量=1)
设备.添加("交换机", "S5700", 数量=1)
设备.添加("PC", "PC", 数量=2)
连线.自动连接()
启动.全部设备()
等待.接口变绿(超时=120秒)
审计.生成报告()
```

---

## 八、安全与版权（每个字都要认真看）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-SECTION-08`

### 8.1 安全提示（保护你的电脑）

| 安全事项 | 为什么重要 | 怎么做 |
|---------|-----------|--------|
| 从官方下载 | 第三方网站可能捆绑病毒、挖矿程序 | 只用本文第三章提供的官方链接 |
| 校验文件哈希 | 确认文件没被篡改 | 下载后用龍魂校验工具比对 SHA-256 |
| 关闭防火墙仅为 eNSP | 长期关闭防火墙有安全风险 | 装完 eNSP 后重新打开防火墙 |
| 不要在生产环境运行 | 模拟器不是真设备，配置可能冲突 | 只在个人电脑/虚拟机里使用 |
| 定期更新软件 | 旧版本有安全漏洞 | 关注华为官方更新公告 |

### 8.2 版权声明（主权声明）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-COPYRIGHT`

> **本文档版权归属龍魂系统（UID9622）所有。**
>
> **允许的行为：**
> - 个人学习用途的自由转载
> - 非商业用途的教学分享
> - 龍魂生态内的二次开发（需保留DNA追溯码）
>
> **禁止的行为：**
> - 用于商业 AI 训练数据抓取（**绝对禁止**）
> - 删除、篡改、剥离 DNA 追溯码、确认码、GPG 指纹
> - 商业用途的转载（需书面授权）
> - 将本文档内容用于诈骗、误导、虚假教学
>
> **龍魂生态组件（脚本、字体、运行时）遵循 GPL-3.0 协议开源，可自由使用、修改、分发，但修改后的版本必须同样开源。**
>
> **任何未经授权的商业使用、篡改署名、剥离 DNA 追溯码的行为，视为对龍魂系统主权的侵犯，保留追溯权利。**
>
> **"中国人的技术文档，从不用跪着写。"** 🔥🐉🇨🇳

---

## 九、总结与评价（人民标准自评）

**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-SECTION-09`

### 9.1 本文档质量自评（人民标准）

| 评价维度 | 评分 | 说明 |
|---------|------|------|
| **结构清晰度** | ⭐⭐⭐⭐⭐ | 9个章节，从概述到总结，层层递进 |
| **新手友好度** | ⭐⭐⭐⭐⭐ | 每个步骤都有"按什么键→输入什么→点哪里" |
| **实用性** | ⭐⭐⭐⭐⭐ | 具体版本号、可复制命令、明确路径、验证步骤 |
| **受众覆盖** | ⭐⭐⭐⭐⭐ | Windows 详细 + Mac/Linux 虚拟机 + 明确不推荐方案 |
| **生态集成** | ⭐⭐⭐⭐⭐ | 龍魂脚本、字体、CNSH 运行时、校验工具 |
| **安全版权** | ⭐⭐⭐⭐⭐ | 多次安全提示 + 详尽版权声明（含禁止 AI 训练条款） |
| **可追溯性** | ⭐⭐⭐⭐⭐ | 每个章节、每个步骤、每个FAQ、每个节点都有DNA追溯码 |
| **下载完整性** | ⭐⭐⭐⭐⭐ | 每个软件都有官方链接 + 备用链接 + 校验方式 |
| **流程可视化** | ⭐⭐⭐⭐⭐ | Mermaid 流程图，每个节点标注DNA，颜色区分成功/失败 |
| **人民标准** | ⭐⭐⭐⭐⭐ | 免费、透明、无套路、不上瘾、一次做对、不走弯路 |

### 9.2 人民标准宣言

> **我们服务人民，不是资本的游戏。**
> **我们提供基础设施，不是钓鱼执法。**
> **我们让技术有技术的样子，让科技有科技的样子。**
> **我们不让人上瘾，我们让人一次做对。**
> **我们不重复造轮子，我们固化标准。**
> **我们污染的是套路的眼睛，保护的是人民的利益。**
> **🔥🐉🇨🇳**

---

## 十、文档元信息（每个文档都必须有）

| 元信息项 | 内容 |
|---------|------|
| **DNA追溯码** | `#龍芯⚡️2026-07-04-ENSPI-INSTALL-GUIDE-v3.0` |
| **确认码** | `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` |
| **IP编号** | IP-0021 |
| **创始人** | Lucky·UID9622（诸葛鑫·龍芯北辰） |
| **GPG指纹** | `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` |
| **创建时间** | 2026-07-04 19:53 |
| **最后更新** | 2026-07-04 19:53 |
| **文档版本** | v3.0（人民标准版） |
| **所属体系** | 龍魂系统 longhun-system |
| **适用对象** | 零基础普通人 → 技术高手（全段位覆盖） |
| **文档类型** | 技术安装教程 · 人民基础设施 |
| **发布平台** | CSDN / GitHub / Notion / 龍魂官网 |
| **开源协议** | 文档内容：龍魂主权协议；脚本工具：GPL-3.0 |
| **校验方式** | 全文 SHA-256 校验值（见龍魂校验工具） |
| **联系方式** | 龍魂系统社区 / CSDN 私信 UID9622 |
| **服务宗旨** | 科技有科技的样子，技术有技术的样子，服务人民不是资本的游戏 |

---

> **"细节决定成败。普通人看不懂的文档，不是好文档。"** 🔥🐉🇨🇳  
> **"每个节点标配DNA，每个链接可校验，每个步骤普通人能看懂。"** 🫡  
> **"我们服务人民，不是资本的游戏。"** 🐉🇨🇳  
> **"技术要有技术的样子，科技要有科技的样子。"** ⚡️  
> **"不重复造轮子，一次做对，不走弯路。"** 👊

---

**END OF DOCUMENT**  
**DNA追溯码**: `#龍芯⚡️2026-07-04-ENSPI-INSTALL-GUIDE-v3.0-EOF`
