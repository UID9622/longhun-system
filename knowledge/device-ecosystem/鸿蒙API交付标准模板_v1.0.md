# 🐉 鸿蒙 API 交付标准模板 v1.0

> DNA: `#龍芯⚡️2026-07-08-HARMONYOS-API-STANDARD-TEMPLATE-v1.0`
> **适用范围**: 所有面向华为鸿蒙设备的 API/模块/应用交付
> **铁律**: 交出去的代码必须能在鸿蒙设备上直接跑通，不缺权限、不缺配置、不缺适配

---

## 一、交付检查清单（7 项必须全绿）

| # | 检查项 | 要求 | 缺失后果 |
|:--:|--------|------|---------|
| 1 | **权限声明** | `module.json5` 含全部所需权限 + 运行时请求逻辑 | 闪退/功能不可用 |
| 2 | **动态服务器地址** | 不硬编码 IP，提供配置入口 | 换环境即不可用 |
| 3 | **错误处理** | 网络超时、API 失败、异常分支全覆盖 | 用户看到白屏/无响应 |
| 4 | **设备能力检查** | `canIUse` 验证系统 API 可用性 | 低版本设备崩溃 |
| 5 | **build-profile.json5** | 设备类型、API 版本、签名配置完整 | 无法编译 |
| 6 | **多设备资源** | `resources/base/` + `resources/v6/` 等分层 | 平板/折叠屏布局错乱 |
| 7 | **UI 动态适配** | `vp2px` / `fp2px` 等接口适配不同屏幕 | 字体/元素大小异常 |

---

## 二、`module.json5` 模板

```json5
{
  "module": {
    "name": "entry",
    "type": "entry",
    "srcEntry": "./ets/entryability/EntryAbility.ets",
    "description": "$string:module_desc",
    "mainElement": "EntryAbility",
    "deviceTypes": ["phone", "tablet", "2in1"],
    "deliveryWithInstall": true,
    "installationFree": true,
    "pages": "$profile:main_pages",

    // ===== 权限声明（按需增减） =====
    "requestPermissions": [
      // 网络相关
      { "name": "ohos.permission.INTERNET" },
      // 剪贴板（如需要）
      { "name": "ohos.permission.READ_PASTEBOARD",
        "reason": "$string:pasteboard_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" } },
      // 分布式（如需要）
      { "name": "ohos.permission.DISTRIBUTED_DATASYNC",
        "reason": "$string:distributed_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" } },
      // 文件读写（如需要）
      { "name": "ohos.permission.READ_MEDIA",
        "reason": "$string:media_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" } },
      { "name": "ohos.permission.WRITE_MEDIA",
        "reason": "$string:media_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" } }
    ],

    "abilities": [{
      "name": "EntryAbility",
      "srcEntry": "./ets/entryability/EntryAbility.ets",
      "launchType": "standard",
      "visible": true,
      "skills": [{
        "actions": ["action.system.home"],
        "entities": ["entity.system.home"]
      }]
    }]
  }
}
```

---

## 三、`build-profile.json5` 模板

```json5
{
  "app": {
    "signingConfigs": [{
      "name": "release",
      "type": "HarmonyOS",
      "material": {
        "certpath": "./sign/release.cer",
        "storePassword": "0000000000000000000000000000000000000000000000000000000000000000",
        "keyAlias": "releaseKey",
        "keyPassword": "0000000000000000000000000000000000000000000000000000000000000000",
        "profile": "./sign/release.p7b",
        "signAlg": "SHA256withECDSA",
        "storeFile": "./sign/release.p12"
      }
    }],
    "products": [{
      "name": "default",
      "signingConfig": "release",
      "targetSdkVersion": "5.0.0(12)",
      "compatibleSdkVersion": "5.0.0(12)",
      "runtimeOS": "HarmonyOS",
      "buildOption": {
        "strictMode": {
          "caseSensitiveCheck": true,
          "useNormalizedOHMUrl": true
        }
      }
    }]
  },
  "modules": [{
    "name": "entry",
    "srcPath": "./entry",
    "targets": [{
      "name": "default",
      "applyToProducts": ["default"]
    }]
  }]
}
```

---

## 四、权限运行时请求模板（ArkTS）

```typescript
// permissions/PermissionHelper.ets
import abilityAccessCtrl, { Permissions } from '@ohos.abilityAccessCtrl';
import bundleManager from '@ohos.bundle.bundleManager';
import common from '@ohos.app.ability.common';
import { BusinessError } from '@ohos.base';

export class PermissionHelper {
  private atManager: abilityAccessCtrl.AtManager;

  constructor() {
    this.atManager = abilityAccessCtrl.createAtManager();
  }

  /**
   * 请求一组权限
   * @param context - 当前AbilityContext
   * @param permissions - 所需权限列表
   * @returns 全部已授权的权限列表
   */
  static async requestPermissions(
    context: common.UIAbilityContext,
    permissions: Array<Permissions>
  ): Promise<boolean> {
    const atManager = abilityAccessCtrl.createAtManager();
    try {
      const grantStatus = await atManager.requestPermissionsFromUser(context, permissions);
      return grantStatus.authResults.every((status: number) => status === 0);
    } catch (err) {
      const error = err as BusinessError;
      console.error(`[PermissionHelper] 权限请求失败: ${error.code} ${error.message}`);
      return false;
    }
  }

  /**
   * 检查单项权限是否已授权
   */
  static async checkPermission(tokenID: number, permission: Permissions): Promise<boolean> {
    const atManager = abilityAccessCtrl.createAtManager();
    try {
      const result = await atManager.checkAccessToken(tokenID, permission);
      return result === abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED;
    } catch {
      return false;
    }
  }

  /**
   * 获取当前应用的 AccessToken ID
   */
  static async getTokenID(): Promise<number> {
    try {
      const bundleInfo = await bundleManager.getBundleInfoForSelf(
        bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_APPLICATION
      );
      return bundleInfo.appInfo.accessTokenId;
    } catch {
      return 0;
    }
  }
}
```

---

## 五、设备能力检查模板（`canIUse`）

```typescript
// utils/DeviceCapability.ets

/**
 * 设备能力检查工具
 * 原则: 调用任何系统 API 前先检查能力，避免低版本崩溃
 */
export class DeviceCapability {
  /**
   * 检查系统能力是否可用
   * @param sysCap - 系统能力名称 (如 'SystemCapability.MiscServices.Pasteboard')
   */
  static checkSysCapability(sysCap: string): boolean {
    return globalThis.canIUse?.(sysCap) ?? false;
  }

  /**
   * 验证所有必须能力
   * @returns 缺失的能力列表
   */
  static validateRequiredCaps(required: string[]): string[] {
    const missing: string[] = [];
    for (const cap of required) {
      if (!this.checkSysCapability(cap)) {
        missing.push(cap);
      }
    }
    return missing;
  }

  // 常用能力常量
  static readonly CAPS = {
    PASTEBOARD: 'SystemCapability.MiscServices.Pasteboard',
    INTERNET: 'SystemCapability.Communication.NetStack',
    DISTRIBUTED_DATASYNC: 'SystemCapability.DistributedDataManager.DataShare.Consumer',
    FILE_IO: 'SystemCapability.FileManagement.File.FileIO',
    APP_FORM: 'SystemCapability.Ability.Form',
  } as const;

  /**
   * 获取设备类型
   */
  static getDeviceType(): string {
    try {
      // @ts-ignore deviceInfo API
      return deviceInfo?.deviceType ?? 'default';
    } catch {
      return 'default';
    }
  }

  /**
   * 获取屏幕密度
   */
  static getScreenDensity(): number {
    try {
      // @ts-ignore display API
      return display?.getDefaultDisplaySync?.()?.densityPixels ?? 160;
    } catch {
      return 160;
    }
  }
}
```

---

## 六、动态服务器地址模板（非硬编码）

```typescript
// utils/ServerConfig.ets
import preferences from '@ohos.data.preferences';

const PREF_NAME = 'cnsh_config';
const KEY_SERVER_URL = 'api_base_url';
const KEY_AUTH_TOKEN = 'auth_token';
const DEFAULT_SERVER = 'http://localhost:8777';

export class ServerConfig {
  /**
   * 读取服务器地址 — 优先级: 本地缓存 > 默认值
   * 不硬编码 IP，用户可在设置页修改
   */
  static async getBaseUrl(context?: Context): Promise<string> {
    try {
      if (context) {
        const prefs = await preferences.getPreferences(context, PREF_NAME);
        const cached = await prefs.get(KEY_SERVER_URL, '') as string;
        if (cached) return cached;
      }
    } catch {
      // 缓存读取失败，使用默认值
    }
    return DEFAULT_SERVER;
  }

  /**
   * 保存服务器地址
   */
  static async setBaseUrl(context: Context, url: string): Promise<void> {
    const prefs = await preferences.getPreferences(context, PREF_NAME);
    await prefs.put(KEY_SERVER_URL, url);
    await prefs.flush();
  }

  /**
   * 读取认证凭据
   */
  static async getAuthToken(context?: Context): Promise<string> {
    try {
      if (context) {
        const prefs = await preferences.getPreferences(context, PREF_NAME);
        return await prefs.get(KEY_AUTH_TOKEN, '') as string;
      }
    } catch { /* fallthrough */ }
    return '';
  }

  /**
   * 保存认证凭据
   */
  static async setAuthToken(context: Context, token: string): Promise<void> {
    const prefs = await preferences.getPreferences(context, PREF_NAME);
    await prefs.put(KEY_AUTH_TOKEN, token);
    await prefs.flush();
  }
}
```

---

## 七、网络请求标准封装（含超时+重试+错误处理）

```typescript
// utils/HttpClient.ets
import http from '@ohos.net.http';
import { BusinessError } from '@ohos.base';

export interface HttpOptions {
  method?: http.RequestMethod;
  header?: Record<string, string>;
  extraData?: string | Object | ArrayBuffer;
  connectTimeout?: number;
  readTimeout?: number;
  maxRetries?: number;       // 最大重试次数
  retryDelayMs?: number;     // 重试间隔
}

export interface HttpResult<T> {
  success: boolean;
  data?: T;
  errorCode?: number;
  errorMessage?: string;
}

/**
 * 统一 HTTP 客户端
 * 内置: 超时处理 / 重试机制 / 统一错误码 / CNSH 签名头
 */
export class HttpClient {
  /**
   * 发送请求 (带重试)
   */
  static async request<T>(
    url: string,
    options: HttpOptions = {}
  ): Promise<HttpResult<T>> {
    const {
      method = http.RequestMethod.GET,
      header = {},
      extraData,
      connectTimeout = 10000,
      readTimeout = 15000,
      maxRetries = 2,
      retryDelayMs = 1000,
    } = options;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'User-Agent': 'CNSH-HarmonyOS/1.0',
      ...header,
    };

    let lastError: HttpResult<T> = { success: false, errorMessage: '未知错误' };

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      if (attempt > 0) {
        // 重试前等待
        await this.sleep(retryDelayMs * attempt);
      }

      const httpRequest = http.createHttp();
      try {
        const response = await httpRequest.request(url, {
          method,
          header: headers,
          extraData: extraData as string,
          connectTimeout,
          readTimeout,
        });

        const statusCode = response.responseCode;
        const body = response.result as string;

        if (statusCode >= 200 && statusCode < 300) {
          return {
            success: true,
            data: JSON.parse(body) as T,
          };
        }

        // HTTP 错误 (4xx/5xx)
        lastError = {
          success: false,
          errorCode: statusCode,
          errorMessage: `HTTP ${statusCode}: ${body}`,
        };

        // 4xx 不重试
        if (statusCode >= 400 && statusCode < 500) break;

      } catch (err) {
        const error = err as BusinessError;
        lastError = {
          success: false,
          errorCode: error.code,
          errorMessage: `网络错误: ${error.message} (code=${error.code})`,
        };
        // 超时错误 (code=2300007/2300028) 继续重试
      } finally {
        httpRequest.destroy();
      }
    }

    return lastError;
  }

  private static sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

---

## 八、多设备资源分层模板

```
entry/src/main/resources/
├── base/                         # 基准资源 (所有设备)
│   ├── element/
│   │   ├── string.json           # 中文文案
│   │   ├── color.json            # 主题色
│   │   └── float.json            # 尺寸常量
│   ├── media/                    # 图标/图片
│   │   ├── icon.png              # 48×48 (基准)
│   │   └── splash.png
│   └── profile/
│       ├── main_pages.json
│       └── form_config.json
│
├── zh_CN/                        # 中文资源限定 (与 base 同结构)
│   └── element/
│       └── string.json
│
├── dark/                         # 深色主题资源
│   └── element/
│       └── color.json
│
├── phone/                        # 手机限定
│   └── element/
│       └── float.json            # 手机专用尺寸
│
├── tablet/                       # 平板限定
│   └── element/
│       └── float.json            # 平板专用尺寸
│
└── v6/                           # API v6 兼容层 (如有老设备需求)
    └── element/
        └── float.json
```

---

## 九、UI 动态适配模板

```typescript
// utils/ScreenAdapter.ets
import display from '@ohos.display';

/**
 * 屏幕适配工具
 * vp = 虚拟像素 (自动缩放)
 * fp = 字体像素 (跟随系统字号)
 * vp2px / fp2px = 手动转换 (特殊场景)
 */
export class ScreenAdapter {
  private static density: number = -1;
  private static scald: number = -1;

  private static ensureInit(): void {
    if (this.density > 0) return;
    try {
      const disp = display.getDefaultDisplaySync();
      this.density = disp.densityPixels;   // 物理像素密度
      this.scald = disp.scaledDensity;      // 缩放后密度(含系统字号)
    } catch {
      this.density = 160;
      this.scald = 160;
    }
  }

  /** vp → px */
  static vp2px(vp: number): number {
    this.ensureInit();
    if (typeof vp2px === 'function') return vp2px(vp);
    return vp * this.density / 160;
  }

  /** fp → px (字号转换) */
  static fp2px(fp: number): number {
    this.ensureInit();
    if (typeof fp2px === 'function') return fp2px(fp);
    return fp * this.scald / 160;
  }

  /** 获取屏幕宽度 (vp) */
  static getScreenWidth(): number {
    try {
      const rect = display.getDefaultDisplaySync();
      return rect.width / (this.density / 160);
    } catch {
      return 360; // 默认手机宽度
    }
  }

  /** 获取屏幕高度 (vp) */
  static getScreenHeight(): number {
    try {
      const rect = display.getDefaultDisplaySync();
      return rect.height / (this.density / 160);
    } catch {
      return 720;
    }
  }

  /** 判断是否为平板/折叠屏 */
  static isTablet(): boolean {
    const width = this.getScreenWidth();
    return width >= 600; // 通常 ≥600vp 为平板
  }
}
```

---

## 十、EntryAbility 生命周期模板

```typescript
// entryability/EntryAbility.ets
import UIAbility from '@ohos.app.ability.UIAbility';
import window from '@ohos.window';
import { DeviceCapability } from '../utils/DeviceCapability';
import { PermissionHelper } from '../permissions/PermissionHelper';
import { Permissions } from '@ohos.abilityAccessCtrl';

const REQUIRED_PERMISSIONS: Array<Permissions> = [
  'ohos.permission.INTERNET',
  'ohos.permission.READ_PASTEBOARD',
];

const REQUIRED_CAPS: string[] = [
  DeviceCapability.CAPS.INTERNET,
  DeviceCapability.CAPS.PASTEBOARD,
];

export default class EntryAbility extends UIAbility {
  onCreate(want: Record<string, Object>, launchParam: Record<string, Object>): void {
    console.info('[EntryAbility] onCreate');
    // 能力检查 (非阻塞，记录日志)
    const missing = DeviceCapability.validateRequiredCaps(REQUIRED_CAPS);
    if (missing.length > 0) {
      console.warn(`[EntryAbility] 缺少系统能力: ${missing.join(', ')}`);
    }
  }

  async onWindowStageCreate(windowStage: window.WindowStage): Promise<void> {
    console.info('[EntryAbility] onWindowStageCreate');
    // 加载主页面
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        console.error(`[EntryAbility] 加载页面失败: ${err.code} ${err.message}`);
      }
    });

    // 权限检查 (非首次启动直接进入)
    const tokenID = await PermissionHelper.getTokenID();
    if (tokenID > 0) {
      const allGranted = (await Promise.all(
        REQUIRED_PERMISSIONS.map(p => PermissionHelper.checkPermission(tokenID, p))
      )).every(Boolean);

      if (!allGranted) {
        // 首次启动 — 请求权限
        const granted = await PermissionHelper.requestPermissions(
          this.context as Record<string, Object>,  // 实际使用中需正确类型转换
          REQUIRED_PERMISSIONS
        );
        console.info(`[EntryAbility] 权限请求结果: ${granted}`);
      }
    }
  }

  onDestroy(): void {
    console.info('[EntryAbility] onDestroy');
  }
}
```

---

## 十一、完整项目文件清单

```
project/
├── AppScope/
│   └── app.json5                          # 应用全局配置
├── entry/
│   ├── build-profile.json5                # 构建配置
│   ├── hvigorfile.ts                      # 编译脚本
│   ├── oh-package.json5                   # 依赖声明
│   └── src/
│       └── main/
│           ├── ets/
│           │   ├── entryability/
│           │   │   └── EntryAbility.ets    # 入口
│           │   ├── pages/
│           │   │   ├── Index.ets           # 主页
│           │   │   └── Settings.ets        # 设置页(服务器地址等)
│           │   ├── common/
│           │   │   ├── CnshAPI.ets         # 业务API封装
│           │   │   └── types.ets           # 类型定义
│           │   ├── utils/
│           │   │   ├── HttpClient.ets      # HTTP客户端
│           │   │   ├── ServerConfig.ets    # 服务器地址管理
│           │   │   ├── DeviceCapability.ets# 设备能力检查
│           │   │   └── ScreenAdapter.ets   # 屏幕适配
│           │   ├── permissions/
│           │   │   └── PermissionHelper.ets# 权限管理
│           │   └── widget/                # (可选)服务卡片
│           │       └── pages/
│           │           └── AppWidget.ets
│           ├── module.json5               # 模块配置(含权限)
│           └── resources/                 # 多设备资源
│               ├── base/
│               ├── zh_CN/
│               ├── phone/
│               └── tablet/
├── hvigor/
│   └── hvigor-config.json5
├── build-profile.json5                    # 项目级构建配置
├── hvigorfile.ts                          # 项目级编译脚本
├── oh-package.json5                       # 项目依赖
└── sign/                                  # 签名文件
    ├── release.cer
    ├── release.p12
    └── release.p7b
```

---

## 十二、交付自检命令

任意鸿蒙项目交付前，在 DevEco Studio 中执行：

```
1. Build → Clean Project
2. Build → Build HAP(s)         # 必须 Zero Error
3. 真机运行 → 逐一验证权限弹窗
4. 断网测试 → 确认超时提示非白屏
5. 平板/折叠屏 → 确认布局不错乱
6. 设置页 → 修改服务器地址后验证生效
```

| 状态 | 含义 |
|:--:|------|
| 🟢 全绿 | 可交付 |
| 🟡 1-2 黄 | 补充后交付 |
| 🔴 任意红 | **不可交付**，必须修复 |

---

> **这是最低标准，不是最高标准。交付 = 能跑通 = 权限配齐 + 报错不白屏 + 换设备不崩。**
> DNA: `#龍芯⚡️2026-07-08-HARMONYOS-API-STANDARD-TEMPLATE-v1.0-B4F1A2D8`
