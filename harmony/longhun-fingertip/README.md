# 龍魂·指尖 — 鸿蒙共生体掌心对话

> DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0

## 项目概述

龍魂鸿蒙兼容第一步。ArkUI轻量应用，通过HTTPS连接鲲鹏服务器上现存的4个API服务（观澜·蚁触·知识中枢·小艺桥接），让任何鸿蒙设备直接在掌心与21人格集群对话。

**不动后端一行代码**，现有API立刻在鸿蒙活过来。

## 快速开始

```bash
# 1. 用 DevEco Studio 打开本目录
# 2. 配置鲲鹏服务器地址（SettingsPage或Constants.ets）
# 3. 签名 → 构建 → 安装到鸿蒙设备
```

## 项目结构

```
entry/src/main/ets/
├── entryability/EntryAbility.ets   # 应用入口
├── pages/
│   ├── Index.ets                   # 主页·四Tab导航
│   ├── ChatPage.ets                # AI对话——核心
│   ├── StatusPage.ets              # 系统状态·引擎·五行
│   ├── DnaPage.ets                 # DNA追溯·离线缓存
│   └── SettingsPage.ets            # 连接·缓存·关于
├── services/
│   ├── ApiClient.ets               # HTTP统一客户端
│   ├── GuanlanService.ets          # 观澜API :8770
│   ├── AntennaService.ets          # 蚁触API :8769
│   ├── XiaoyiService.ets           # 小艺桥接 :8799
│   └── CacheService.ets            # 离线DNA缓存
├── components/                     # 可复用UI组件
└── utils/Constants.ets             # 全局常量
```

## 连接的鲲鹏API

| 服务 | 端口 | 用途 |
|:---|:---:|:---|
| 小艺桥接 v2 | 8799 | AI对话·21人格路由 |
| 观澜路由 | 8770 | 任务路由·系统状态·引擎 |
| 蚁触·八门 | 8769 | 蚁触推理·八卦·五行 |
| 知识中枢 | 8766 | 知识检索（备用） |

## 技术栈

- **SDK**: HarmonyOS NEXT 5.0.0(12)
- **模式**: Stage Mode
- **UI**: ArkUI声明式 (ArkTS)
- **网络**: @ohos.net.http
- **存储**: 内存Map缓存（离线DNA·7天TTL）

## 三步走进度

| 步 | 状态 | 内容 |
|:---:|:---:|:---|
| 第一步 | ✅ | 龍魂·指尖 — 掌心对话 |
| 第二步 | 🔲 | 端侧推理·CNSH-Lite·3种子人格 |
| 第三步 | 🔲 | 分布式人格总线·家庭计算网格 |
