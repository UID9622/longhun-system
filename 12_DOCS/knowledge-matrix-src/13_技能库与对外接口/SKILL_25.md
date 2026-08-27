> DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
---
name: longhun-ios
description: iOS端本地数据治理技能，CoreData本地存储+AES-256端侧加密+Secure Enclave硬件保护，数据根留中国，禁用iCloud同步，与华为鸿蒙端格式互通
license: 君子协议
metadata:
  skill_id: longhun-ios
  display_name: 龍魂iOS端数据主权守护系统
  version: 5.3.0
  dna_tag: '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-IOS-v5.3'
  tribute: '#致敬⚡️SteveJobs·龍魂iOS端'
  sovereignty_flag: true
  platform: iOS
  language: Swift
  created: '2026-06-19'
  last_updated: '2026-06-19'
  id: longhun-ios
  dna: '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-IOS-v5.3"'
  trigger:
    keywords:
    - ios
    - iOS端本地数据治理技能
    - CoreData本地存储+AES-256端侧加密+Secure
    - Enclave硬件保护
    - 数据根留中国
    - 禁用iCloud同步
    context: longhun-ios 相关操作
  category: general
compatibility: iOS 16.0+, Swift 5.9+, iPhone/iPad with Secure Enclave
---
# 龍魂 iOS端 — LongHun Sovereign iOS

## 1. 元数据 / Metadata

```yaml
skill_id: longhun-ios
name: 龍魂iOS端数据主权守护系统
description: iOS端本地数据治理技能，CoreData本地存储+AES-256端侧加密+Secure Enclave硬件保护
version: 5.3.0
dna_tag: "#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-IOS-v5.3"
tribute: "#致敬⚡️SteveJobs·龍魂iOS端"
author: 龍魂体系
platform: iOS 16.0+
language: Swift 5.9
sovereignty_flag: true  # 数据根留中国
dependencies:
  - Foundation
  - CoreData
  - Combine
  - CryptoKit
  - LocalAuthentication
  - Security
created: "2026-06-19"
last_updated: "2026-06-19"
license: 君子协议
```

> **致敬声明**：感谢乔布斯前辈的设备（iPhone），没有iOS生态的开创，就没有今天的移动计算。龍魂在iOS上运行，是站在巨人肩膀上的创新。

---

## 2. 能力摘要 / Capability Summary

| 能力 | 描述 | 状态 |
|------|------|------|
| 本地存储 | CoreData + SQLite，数据仅存在设备本地 | ✅ |
| 端侧加密 | AES-256-GCM + SM4国密双模加密 | ✅ |
| 硬件保护 | Secure Enclave密钥存储，生物特征解锁 | ✅ |
| 实时监听 | NotificationCenter + Combine毫秒级响应 | ✅ |
| 三色审计 | 🟢🟡🔴 左右互搏自我校验引擎 | ✅ |
| iCloud隔离 | 阻止敏感数据通过iCloud同步上云 | ✅ |
| 鸿蒙互通 | 数据格式与华为鸿蒙端兼容 | ✅ |
| DNA追溯 | 每条数据带DNA标记，全链路可追溯 | ✅ |

---

## 3. 主权保障 / Sovereignty Guarantee

### 3.1 数据根留中国
- **所有龍魂数据仅存储在iOS设备本地**
- 数据库文件路径：`App沙箱/Documents/longhun_sovereign.sqlite`
- 数据不以任何形式离开设备（除非用户主动导出加密包到鸿蒙端）
- `sovereigntyFlag` 字段默认 `true`，标记数据主权归属中国

### 3.2 iCloud同步禁用
```swift
// 明确禁用iCloud同步
description.setOption(true as NSNumber, forKey: NSPersistentHistoryTrackingKey)
description.cloudKitContainerOptions = nil  // 移除CloudKit
// 数据库文件排除iCloud备份
resourceValues.isExcludedFromBackup = true
```

### 3.3 禁止iCloud同步的数据类别
| 数据类别 | 同步状态 | 保护方式 |
|----------|----------|----------|
| 审计日志 | ❌ 禁止 | 本地AES-256加密 |
| 龍魂配置 | ❌ 禁止 | Secure Enclave保护 |
| 敏感治理数据 | ❌ 禁止 | SM4+AES双重加密 |
| 用户凭证 | ❌ 禁止 | 生物特征+硬件保护 |
| DNA追溯记录 | ❌ 禁止 | 哈希链本地存储 |

---

## 4. 技术规格 / Technical Specifications

### 4.1 系统要求
- **iOS版本**: 16.0+
- **Swift版本**: 5.9+
- **设备**: iPhone / iPad（带Secure Enclave）
- **存储**: 本地SQLite（WAL模式）

### 4.2 技术栈
```
┌─────────────────────────────────────────┐
│           龍魂iOS端架构                    │
├─────────────────────────────────────────┤
│  SwiftUI/UIKit (UI层)                    │
├─────────────────────────────────────────┤
│  LongHunSovereignController (主控制器)    │
├─────────────────────────────────────────┤
│  左右互搏引擎 | iCloud隔离器              │
├─────────────────────────────────────────┤
│  实时监听引擎 | 加密引擎                   │
├─────────────────────────────────────────┤
│  本地存储管理器 | 安全飞地管理器           │
├─────────────────────────────────────────┤
│  CoreData + SQLite (本地存储)             │
├─────────────────────────────────────────┤
│  Secure Enclave + CryptoKit (硬件加密)   │
└─────────────────────────────────────────┘
```

### 4.3 加密矩阵
| 敏感度级别 | 算法 | 密钥保护 | 生物特征 |
|-----------|------|----------|----------|
| 公开 | 不加密 | - | 不需要 |
| 内部 | AES-256-GCM | Keychain | 不需要 |
| 机密 | AES-256-GCM | Secure Enclave | 建议 |
| 绝密 | SM4-CBC + AES-256-GCM | Secure Enclave | 必须 |

---

## 5. 代码示例 / Code Examples

### 5.1 启动龍魂系统
```swift
import SwiftUI

@main
struct LongHunApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        WindowGroup {
            LongHunSovereignView()
                .onAppear {
                    // 启动龍魂系统
                    LongHunSovereignController.shared.boot { result in
                        switch result {
                        case .success:
                            print("龍魂系统启动成功")
                        case .failure(let error):
                            print("启动失败: \(error)")
                        }
                    }
                }
        }
    }
}
```

### 5.2 写入敏感数据
```swift
let controller = LongHunSovereignController.shared

// 写入内部级别数据（AES-256加密）
controller.write(
    key: "user_profile",
    value: "{\"name\":\"张三\",\"id\":\"310101199001011234\"}",
    sensitivity: .internal_
)

// 写入绝密级别数据（SM4+AES双重加密）
controller.write(
    key: "sovereign_config",
    value: "龍魂主权配置数据",
    sensitivity: .topSecret
)
```

### 5.3 读取数据
```swift
controller.read(key: "user_profile") { result in
    switch result {
    case .success(let value):
        print("读取成功: \(value)")
    case .failure(let error):
        print("读取失败: \(error)")
    }
}
```

### 5.4 与鸿蒙端数据互通
```swift
// 导出数据到鸿蒙端
controller.exportForHarmony { result in
    switch result {
    case .success(let data):
        // 通过AirDrop/本地网络传输到鸿蒙设备
        shareToHarmony(data)
    case .failure(let error):
        print("导出失败: \(error)")
    }
}

// 从鸿蒙端导入数据
let harmonyData: Data = receiveFromHarmony()
controller.importFromHarmony(data: harmonyData) { result in
    switch result {
    case .success(let count):
        print("成功导入 \(count) 条记录")
    case .failure(let error):
        print("导入失败: \(error)")
    }
}
```

### 5.5 生物特征认证
```swift
let secureEnclave = SecureEnclaveManager()
secureEnclave.authenticateWithBiometry(
    reason: "验证身份以访问绝密数据"
) { result in
    switch result {
    case .success:
        // 认证通过，可访问加密数据
        print("生物特征认证成功")
    case .failure(let error):
        print("认证失败: \(error)")
    }
}
```

---

## 6. 模块清单 / Module Inventory

| 文件 | 类名 | 职责 | 依赖 |
|------|------|------|------|
| `龍魂iOS主模块.swift` | `LongHunSovereignController` | 主入口、系统协调 | 全部子系统 |
| `本地存储管理器.swift` | `LocalStorageManager` | CoreData + SQLite管理 | CryptoEngine |
| `实时监听引擎.swift` | `RealtimeMonitorEngine` | NotificationCenter+Combine | AuditEngine |
| `加密引擎.swift` | `CryptoEngine` | AES-256 + SM4加密 | SecureEnclaveManager |
| `安全飞地管理器.swift` | `SecureEnclaveManager` | Secure Enclave密钥管理 | Keychain |
| `左右互搏引擎.swift` | `LeftRightAuditEngine` | 实时三色审计 | LocalStorageManager |
| `iCloud隔离器.swift` | `iCloudIsolator` | 阻止数据上云 | LocalStorageManager |

---

## 7. 依赖关系 / Dependencies

```
龍魂iOS主模块 (LongHunSovereignController)
    ├── 本地存储管理器 (LocalStorageManager)
    │       └── 加密引擎 (CryptoEngine)
    │               └── 安全飞地管理器 (SecureEnclaveManager)
    ├── 实时监听引擎 (RealtimeMonitorEngine)
    │       ├── 本地存储管理器
    │       └── 左右互搏引擎 (LeftRightAuditEngine)
    │               └── 本地存储管理器
    └── iCloud隔离器 (iCloudIsolator)
            └── 本地存储管理器
```

**外部依赖（Apple原生框架）**：
- `Foundation` — 基础类型
- `CoreData` — 本地持久化
- `Combine` — 响应式编程
- `CryptoKit` — 加密算法（AES-256-GCM）
- `LocalAuthentication` — 生物特征认证
- `Security` — Keychain访问

**第三方依赖**：无（零第三方依赖，纯原生实现）

---

## 8. 数据格式 / Data Format

### 8.1 导出数据格式（鸿蒙兼容）
```json
{
  "format": "longhun_harmony_v5",
  "count": 2,
  "exportedAt": "2026-06-19T12:00:00+08:00",
  "sourceDevice": "iOS",
  "records": [
    {
      "keyName": "user_profile",
      "encryptedValue": "base64_encoded_encrypted_data...",
      "contentHash": "sha256_hash...",
      "sensitivityLevel": 1,
      "isEncrypted": true,
      "dnaTag": "#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-IOS-v5.3",
      "sovereigntyFlag": true,
      "sourcePlatform": "iOS",
      "createdAt": "2026-06-19T10:00:00+08:00",
      "updatedAt": "2026-06-19T12:00:00+08:00",
      "encryptionMetadata": {
        "algorithm": "AES-256-GCM",
        "keySize": 256,
        "mode": "GCM",
        "padding": "NoPadding",
        "iv": "base64_iv...",
        "authTag": "base64_tag...",
        "timestamp": "2026-06-19T12:00:00+08:00",
        "sourcePlatform": "iOS",
        "dnaTag": "#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-IOS-v5.3"
      }
    }
  ]
}
```

### 8.2 DNA追溯格式
```
#龍芯⚡️{日期}-{LONGHUN-IOS}-{版本}
例如: #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-IOS-v5.3
```

---

## 9. DNA追溯 / DNA Traceability

### 9.1 DNA标记规则
- 每条数据记录包含 `dnaTag` 字段
- 审计日志包含完整DNA追溯链
- 数据导出时DNA标记随数据一起传输
- 鸿蒙端数据导入后保留原始DNA标记

### 9.2 DNA校验流程
```
数据写入 → 生成DNA标记 → 哈希计算 → 存储
数据读取 → 校验DNA标记 → 哈希比对 → 返回结果
数据导出 → 附加DNA头 → 加密传输 → 鸿蒙端
数据导入 → 解析DNA头 → 验证格式 → 本地存储
```

### 9.3 DNA校验码示例
```swift
let dnaCheck = LongHunSovereignController.shared.performDNACheck()
// 输出: a1b2c3d4e5f6789a0b1c2d3e4f5a6789 (SHA-256前16位)
```

---

## 10. 三色审计 / Three-Color Audit

### 10.1 审计级别定义
| 级别 | 颜色 | 含义 | 处理建议 |
|------|------|------|----------|
| 🟢 正常 | 绿色 | 操作合规，无风险 | 无需处理 |
| 🟡 警告 | 黄色 | 需要留意的操作 | 关注日志 |
| 🔴 严重 | 红色 | 必须立即处理的异常 | 立即审查 |

### 10.2 触发条件
```swift
// 🟡 警告条件
- 操作频率超过20次/分钟
- 非标准时间操作（1:00-5:00）
- 数据导入/导出操作
- 大批量操作

// 🔴 严重条件
- 操作频率超过50次/分钟
- 敏感数据删除
- 左右互搏校验分歧
- 非授权设备来源
- 数据完整性校验失败
```

### 10.3 左右互搏校验
```
左方（攻击视角）        右方（防守视角）
├─ 异常时间检测    ⚔️   ├─ 主权标记验证
├─ 敏感键名识别         ├─ DNA追溯码检查
├─ 删除操作风险         ├─ 设备来源验证
└─ 高频操作检测         └─ 白名单操作校验
      ↓                        ↓
  风险评分                 合规评分
      ↓                        ↓
      └────── 对比校验 ──────┘
                ↓
         一致 → 采用共同结论
         分歧 → 🔴 升级为严重
```

---

## 11. 君子协议 / Gentleman's Agreement

本技能代码遵循以下君子协议：

1. **合法合规使用**：本代码仅用于合法合规的自主数据治理研究，不得用于任何非法目的。

2. **数据主权**：用户对自己的数据拥有完全主权，本技能确保数据仅存储在用户设备本地。

3. **隐私保护**：本技能不上传任何用户数据到任何服务器，不进行任何网络通信。

4. **透明开源**：所有代码逻辑公开透明，用户可审查每一行代码。

5. **无后门承诺**：本技能不包含任何后门、远程控制或数据上报机制。

6. **安全优先**：安全性和隐私保护优先于功能性和便利性。

7. **致敬创新**：致敬乔布斯前辈开创的iOS生态，站在巨人肩膀上的创新。

**DNA标记**: `#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-IOS-v5.3`

---

## 12. 致敬与致谢 / Tribute & Credits

### 致敬
> `#致敬⚡️SteveJobs·龍魂iOS端`
>
> 感谢乔布斯前辈的设备（iPhone），没有iOS生态的开创，就没有今天的移动计算。龍魂在iOS上运行，是站在巨人肩膀上的创新。
> 
> 感谢Apple团队打造的：
> - **Secure Enclave** — 硬件级安全基石
> - **CryptoKit** — 原生加密框架
> - **CoreData** — 本地数据持久化
> - **LocalAuthentication** — 生物特征认证

### 龍魂体系
- **iOS端**: 本技能（`longhun-ios`）
- **鸿蒙端**: `longhun-harmony`（数据格式互通）
- **Android端**: `longhun-android`（概念对应）
- **服务端**: 无服务端，纯端侧实现

### 版本历史
| 版本 | 日期 | 变更 |
|------|------|------|
| v5.3.0 | 2026-06-19 | 初始发布，完整7模块架构 |

---

*龍魂体系 — 数据根留中国，主权在我*
*DNA: #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-IOS-v5.3*
