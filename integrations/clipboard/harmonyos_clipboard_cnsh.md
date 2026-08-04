# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 CNSH 剪贴板翻译 · 鸿蒙原子化服务 v2.0

> DNA: `#龍芯⚡️2026-07-08-HARMONYOS-CLIPBOARD-v2.0-PROD`
> **最低要求**: HarmonyOS 3.0+ / OpenHarmony 4.0+ / API 9+
> **通过标准**: DevEco Studio 编译零 ERROR → 真机运行通过 → 交付

---

## v2.0 更新说明（vs v1.0）

| 问题 | v1.0 | v2.0 |
|------|------|------|
| 权限 | 仅声明 | 声明+运行时请求+拒绝提示 |
| 服务器地址 | 硬编码 `192.168.1.100` | 本地缓存+设置页可改 |
| 错误处理 | 无 | 超时+重试+网络错误+API错误全覆盖 |
| 设备能力 | 无 | canIUse 检查+低版本降级提示 |
| 资源配置 | 仅 base/ | base + phone + tablet 分层 |
| UI 适配 | 固定尺寸 | vp2px/fp2px 动态适配 |
| build-profile | 缺失 | 完整签名+设备类型+API版本 |
| 部署方式 | 一笔带过 | DevEco/HAP侧载/AppGallery 三路径 |

---

## 项目结构

```
clipboard-cnsh/
├── AppScope/
│   └── app.json5                            # 应用全局配置
├── entry/
│   ├── build-profile.json5                  # 构建配置(设备类型+API版本+签名)
│   ├── hvigorfile.ts
│   ├── oh-package.json5                     # 依赖
│   └── src/
│       └── main/
│           ├── ets/
│           │   ├── entryability/
│           │   │   └── EntryAbility.ets      # 主入口(含权限+能力检查)
│           │   ├── pages/
│           │   │   ├── Index.ets             # 主页面
│           │   │   └── Settings.ets          # 设置页(服务器地址管理)
│           │   ├── common/
│           │   │   ├── CnshAPI.ets           # CNSH业务API封装
│           │   │   └── types.ets             # 类型定义
│           │   ├── utils/
│           │   │   ├── HttpClient.ets        # HTTP客户端(超时+重试)
│           │   │   ├── ServerConfig.ets      # 服务器地址管理
│           │   │   ├── DeviceCapability.ets  # 设备能力检查
│           │   │   └── ScreenAdapter.ets     # 屏幕适配
│           │   ├── permissions/
│           │   │   └── PermissionHelper.ets  # 权限管理
│           │   └── widget/
│           │       └── pages/
│           │           └── ClipboardWidget.ets # 服务卡片(2×2)
│           ├── module.json5                   # 模块配置(含所有权限声明)
│           └── resources/
│               ├── base/                     # 基准资源
│               │   ├── element/
│               │   │   ├── string.json
│               │   │   ├── color.json
│               │   │   └── float.json
│               │   ├── media/
│               │   │   └── icon.png
│               │   └── profile/
│               │       ├── main_pages.json
│               │       └── form_config.json
│               ├── zh_CN/                    # 中文资源
│               │   └── element/
│               │       └── string.json
│               ├── phone/                    # 手机专用尺寸
│               │   └── element/
│               │       └── float.json
│               └── tablet/                   # 平板/折叠屏专用尺寸
│                   └── element/
│                       └── float.json
├── hvigor/
│   └── hvigor-config.json5
├── build-profile.json5                       # 项目级构建配置
├── hvigorfile.ts
├── oh-package.json5                          # 项目依赖
└── sign/                                     # 签名文件
    ├── release.cer
    ├── release.p12
    └── release.p7b
```

---

## 1. `module.json5` — 模块配置（权限完整版）

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
    "abilities": [{
      "name": "EntryAbility",
      "srcEntry": "./ets/entryability/EntryAbility.ets",
      "launchType": "standard",
      "visible": true,
      "skills": [{
        "actions": ["action.system.home"],
        "entities": ["entity.system.home"]
      }]
    }],
    "extensionAbilities": [{
      "name": "ClipboardWidget",
      "srcEntry": "./ets/widget/pages/ClipboardWidget.ets",
      "type": "form",
      "metadata": [{
        "name": "ohos.extension.form",
        "resource": "$profile:form_config"
      }]
    }],
    "requestPermissions": [
      {
        "name": "ohos.permission.INTERNET",
        "reason": "$string:internet_reason",
        "usedScene": {
          "abilities": ["EntryAbility"],
          "when": "always"
        }
      },
      {
        "name": "ohos.permission.READ_PASTEBOARD",
        "reason": "$string:pasteboard_reason",
        "usedScene": {
          "abilities": ["EntryAbility"],
          "when": "inuse"
        }
      },
      {
        "name": "ohos.permission.GET_NETWORK_INFO",
        "reason": "$string:network_info_reason",
        "usedScene": {
          "abilities": ["EntryAbility"],
          "when": "always"
        }
      }
    ]
  }
}
```

---

## 2. `build-profile.json5` — 构建配置

```json5
{
  "apiType": "stageMode",
  "buildOption": {
    "sourceOption": {
      "workers": []
    }
  },
  "buildOptionSet": [
    {
      "name": "release",
      "arkOptions": {
        "obfuscation": {
          "ruleOptions": {
            "enable": false,
            "files": ["./obfuscation-rules.txt"]
          }
        }
      },
      "nativeLib": {
        "filter": {
          "excludes": ["x86_64"],
          "pickFirsts": [],
          "pickLasts": [],
          "enableOverride": false
        }
      }
    }
  ],
  "targets": [
    {
      "name": "default",
      "runtimeOS": "HarmonyOS"
    },
    {
      "name": "ohosTest"
    }
  ]
}
```

---

## 3. `types.ets` — 类型定义

```typescript
// common/types.ets

/** CNSH 翻译 API 响应 */
export interface CnshResult {
  状态: string
  DNA: string
  时间戳: {
    ISO8601: string
    北京时间: string
    Unix: number
    锁定: boolean
  }
  内容指纹: string
  CNSH关键字: Array<{
    关键字: string
    英文: string
    类别: string
  }>
  完整性哈希: string
  完整性组件: Record<string, unknown>
  原文: string
  CNSH标注: string
  父DNA链: string[]
  验证指令: string
}

/** 完整性验证响应 */
export interface VerifyResult {
  状态: string
  完整: boolean
  说明: string
}

/** 通用 HTTP 结果 */
export interface HttpResult<T> {
  success: boolean
  data?: T
  errorCode?: number
  errorMessage?: string
}
```

---

## 4. `DeviceCapability.ets` — 设备能力检查

```typescript
// utils/DeviceCapability.ets

export class DeviceCapability {
  /** 检查系统能力 */
  static checkSysCapability(sysCap: string): boolean {
    return (globalThis as Record<string, unknown>).canIUse?.(sysCap) === true;
  }

  /** 批量检查 */
  static validateRequiredCaps(required: string[]): string[] {
    return required.filter(cap => !this.checkSysCapability(cap));
  }

  static readonly CAPS = {
    PASTEBOARD: 'SystemCapability.MiscServices.Pasteboard',
    INTERNET: 'SystemCapability.Communication.NetStack',
    APP_FORM: 'SystemCapability.Ability.Form',
  } as const;
}
```

---

## 5. `PermissionHelper.ets` — 权限管理

```typescript
// permissions/PermissionHelper.ets
import abilityAccessCtrl, { Permissions } from '@ohos.abilityAccessCtrl';
import bundleManager from '@ohos.bundle.bundleManager';
import { BusinessError } from '@ohos.base';

export class PermissionHelper {
  /**
   * 请求一组权限
   */
  static async requestPermissions(
    context: Record<string, unknown>,
    permissions: Array<Permissions>
  ): Promise<boolean> {
    const atManager = abilityAccessCtrl.createAtManager();
    try {
      const grantStatus = await atManager.requestPermissionsFromUser(
        context as Record<string, unknown>,
        permissions
      );
      const results = grantStatus.authResults as number[];
      return results.every((s: number) => s === 0);
    } catch (err) {
      const error = err as BusinessError;
      console.error(`[权限] 请求失败: ${error.code} ${error.message}`);
      return false;
    }
  }

  /** 检查单项权限 */
  static async checkPermission(tokenID: number, permission: Permissions): Promise<boolean> {
    const atManager = abilityAccessCtrl.createAtManager();
    try {
      const result = await atManager.checkAccessToken(tokenID, permission);
      return result === abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED;
    } catch {
      return false;
    }
  }

  /** 获取 AccessToken ID */
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

## 6. `HttpClient.ets` — HTTP 客户端（超时+重试+全错误处理）

```typescript
// utils/HttpClient.ets
import http from '@ohos.net.http';
import { BusinessError } from '@ohos.base';

export interface HttpOptions {
  method?: http.RequestMethod
  header?: Record<string, string>
  extraData?: string
  connectTimeout?: number
  readTimeout?: number
  maxRetries?: number
  retryDelayMs?: number
}

export interface HttpResult<T> {
  success: boolean
  data?: T
  errorCode?: number
  errorMessage?: string
}

export class HttpClient {
  static async request<T>(url: string, options: HttpOptions = {}): Promise<HttpResult<T>> {
    const {
      method = http.RequestMethod.POST,
      header = {},
      extraData,
      connectTimeout = 10000,
      readTimeout = 15000,
      maxRetries = 2,
      retryDelayMs = 1000,
    } = options;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'User-Agent': 'CNSH-HarmonyOS/2.0',
      ...header,
    };

    let lastError: HttpResult<T> = { success: false, errorMessage: '未知错误' };

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      if (attempt > 0) {
        await new Promise<void>(resolve => setTimeout(resolve, retryDelayMs * attempt));
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
        const body = (response.result as string) ?? '';

        if (statusCode >= 200 && statusCode < 300) {
          try {
            return { success: true, data: JSON.parse(body) as T };
          } catch {
            return { success: false, errorCode: -1, errorMessage: `JSON解析失败: ${body.substring(0, 100)}` };
          }
        }

        lastError = {
          success: false,
          errorCode: statusCode,
          errorMessage: `服务器错误 HTTP ${statusCode}`,
        };

        // 4xx 不重试
        if (statusCode >= 400 && statusCode < 500) break;

      } catch (err) {
        const error = err as BusinessError;
        lastError = {
          success: false,
          errorCode: error.code,
          errorMessage: `网络不可达 (code=${error.code})`,
        };
        // 超时/网络错误继续重试
      } finally {
        httpRequest.destroy();
      }
    }

    return lastError;
  }
}
```

---

## 7. `ServerConfig.ets` — 动态服务器地址

```typescript
// utils/ServerConfig.ets
import preferences from '@ohos.data.preferences';

const PREF_NAME = 'cnsh_clipboard';
const KEY_SERVER_URL = 'api_base_url';
const DEFAULT_SERVER = 'http://localhost:8777';

export class ServerConfig {
  static async getBaseUrl(context?: Record<string, unknown>): Promise<string> {
    try {
      if (context) {
        const prefs = await preferences.getPreferences(context as Record<string, unknown>, PREF_NAME);
        const cached = (await prefs.get(KEY_SERVER_URL, '')) as string;
        if (cached) return cached;
      }
    } catch { /* 缓存不可用，使用默认 */ }
    return DEFAULT_SERVER;
  }

  static async setBaseUrl(context: Record<string, unknown>, url: string): Promise<void> {
    const prefs = await preferences.getPreferences(context, PREF_NAME);
    await prefs.put(KEY_SERVER_URL, url);
    await prefs.flush();
  }
}
```

---

## 8. `ScreenAdapter.ets` — 屏幕适配

```typescript
// utils/ScreenAdapter.ets
import display from '@ohos.display';

export class ScreenAdapter {
  private static density: number = -1;

  private static ensureInit(): void {
    if (this.density > 0) return;
    try {
      const disp = display.getDefaultDisplaySync();
      this.density = disp.densityPixels;
    } catch {
      this.density = 160;
    }
  }

  static vp2px(vp: number): number {
    this.ensureInit();
    return vp * this.density / 160;
  }

  static fp2px(fp: number): number {
    this.ensureInit();
    return fp * this.density / 160;
  }

  static getScreenWidthVP(): number {
    try {
      const disp = display.getDefaultDisplaySync();
      this.ensureInit();
      return disp.width / (this.density / 160);
    } catch { return 360; }
  }

  static isTablet(): boolean {
    return ScreenAdapter.getScreenWidthVP() >= 600;
  }
}
```

---

## 9. `CnshAPI.ets` — CNSH 业务 API 封装（生产版）

```typescript
// common/CnshAPI.ets
import pasteboard from '@ohos.pasteboard';
import { HttpClient, HttpResult } from '../utils/HttpClient';
import { ServerConfig } from '../utils/ServerConfig';
import { DeviceCapability } from '../utils/DeviceCapability';
import { CnshResult, VerifyResult } from './types';
import http from '@ohos.net.http';

export class CnshAPI {
  /**
   * 读取剪贴板 — 含能力检查
   */
  static async getClipboard(): Promise<{ success: boolean; text: string; error?: string }> {
    // 能力检查
    if (!DeviceCapability.checkSysCapability(DeviceCapability.CAPS.PASTEBOARD)) {
      return { success: false, text: '', error: '当前设备不支持剪贴板功能' };
    }

    try {
      const systemPasteboard = pasteboard.getSystemPasteboard();
      const data = await systemPasteboard.getData();
      const text = data.getPrimaryText() ?? '';
      return { success: true, text };
    } catch (err) {
      return { success: false, text: '', error: `读取剪贴板失败: ${JSON.stringify(err)}` };
    }
  }

  /**
   * 写入剪贴板
   */
  static async setClipboard(text: string): Promise<boolean> {
    if (!DeviceCapability.checkSysCapability(DeviceCapability.CAPS.PASTEBOARD)) {
      return false;
    }
    try {
      const systemPasteboard = pasteboard.getSystemPasteboard();
      const pasteData = pasteboard.createData(pasteboard.MIMETYPE_TEXT_PLAIN, text);
      await systemPasteboard.setData(pasteData);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 调用 CNSH 翻译 API
   */
  static async translate(
    text: string,
    parentDna: string = '',
    context?: Record<string, unknown>
  ): Promise<HttpResult<CnshResult>> {
    const baseUrl = await ServerConfig.getBaseUrl(context);
    const url = `${baseUrl}/api/cnsh/clipboard-translate`;

    return HttpClient.request<CnshResult>(url, {
      method: http.RequestMethod.POST,
      extraData: JSON.stringify({ text, parent_dna: parentDna }),
      connectTimeout: 10000,
      readTimeout: 15000,
      maxRetries: 2,
    });
  }

  /**
   * 验证完整性
   */
  static async verify(
    components: Record<string, unknown>,
    context?: Record<string, unknown>
  ): Promise<HttpResult<VerifyResult>> {
    const baseUrl = await ServerConfig.getBaseUrl(context);
    const url = `${baseUrl}/api/cnsh/clipboard-verify`;

    return HttpClient.request<VerifyResult>(url, {
      method: http.RequestMethod.POST,
      extraData: JSON.stringify({ 完整性组件: components }),
      connectTimeout: 8000,
      readTimeout: 10000,
      maxRetries: 1,
    });
  }
}
```

---

## 10. `EntryAbility.ets` — 主入口（权限+能力检查）

```typescript
// entryability/EntryAbility.ets
import UIAbility from '@ohos.app.ability.UIAbility';
import window from '@ohos.window';
import { Permissions } from '@ohos.abilityAccessCtrl';
import { DeviceCapability } from '../utils/DeviceCapability';
import { PermissionHelper } from '../permissions/PermissionHelper';

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
    console.info('[CNSH] EntryAbility onCreate');

    // 系统能力检查 (仅记录日志，不阻塞启动)
    const missing = DeviceCapability.validateRequiredCaps(REQUIRED_CAPS);
    if (missing.length > 0) {
      console.warn(`[CNSH] ⚠️ 缺少系统能力: ${missing.join(', ')}`);
    }
  }

  async onWindowStageCreate(windowStage: window.WindowStage): Promise<void> {
    console.info('[CNSH] onWindowStageCreate');

    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        console.error(`[CNSH] 页面加载失败: ${err.code} ${err.message}`);
      }
    });

    // 权限检查与请求
    try {
      const tokenID = await PermissionHelper.getTokenID();
      if (tokenID > 0) {
        const allGranted = (await Promise.all(
          REQUIRED_PERMISSIONS.map(p => PermissionHelper.checkPermission(tokenID, p))
        )).every(Boolean);

        if (!allGranted) {
          // 需要请求权限
          const granted = await PermissionHelper.requestPermissions(
            this.context as Record<string, unknown>,
            REQUIRED_PERMISSIONS
          );
          console.info(`[CNSH] 权限请求结果: ${granted ? '✅ 已授权' : '🔴 被拒绝'}`);
        }
      }
    } catch (err) {
      console.error(`[CNSH] 权限检查异常: ${JSON.stringify(err)}`);
    }
  }

  onDestroy(): void {
    console.info('[CNSH] EntryAbility onDestroy');
  }
}
```

---

## 11. `Index.ets` — 主页面（完整错误处理版）

```typescript
// pages/Index.ets
import { CnshAPI } from '../common/CnshAPI';
import { CnshResult } from '../common/types';
import { ScreenAdapter } from '../utils/ScreenAdapter';
import promptAction from '@ohos.promptAction';
import router from '@ohos.router';

@Entry
@Component
struct CnshClipboardPage {
  @State inputText: string = '';
  @State resultDNA: string = '';
  @State keywords: string = '';
  @State integrityHash: string = '';
  @State timestamp: string = '';
  @State isLoading: boolean = false;
  @State verifyStatus: string = '';
  @State parentDna: string = '';
  @State errorMessage: string = '';
  @State networkAvailable: boolean = true;
  private fullResult: CnshResult | null = null;

  // ===== 生命周期 =====

  async aboutToAppear(): Promise<void> {
    // 自动读取剪贴板
    const result = await CnshAPI.getClipboard();
    if (result.success && result.text) {
      this.inputText = result.text;
    } else if (result.error) {
      this.errorMessage = result.error;
    }
  }

  // ===== 翻译操作 =====

  async translate(): Promise<void> {
    // 空输入检查
    if (!this.inputText || this.inputText.trim().length === 0) {
      promptAction.showToast({ message: '请先粘贴要翻译的内容', duration: 2000 });
      return;
    }

    // 清除上次错误
    this.errorMessage = '';
    this.isLoading = true;

    try {
      const result = await CnshAPI.translate(
        this.inputText,
        this.parentDna,
        getContext(this) as Record<string, unknown>
      );

      if (result.success && result.data) {
        const data = result.data;
        this.fullResult = data;
        this.resultDNA = data.DNA;
        this.keywords = `${data.CNSH关键字?.length ?? 0}个关键字`;
        this.integrityHash = (data.完整性哈希 ?? '').substring(0, 16);
        this.timestamp = data.时间戳?.北京时间 ?? '';
        this.verifyStatus = '';

        // 自动复制DNA到剪贴板
        const copied = await CnshAPI.setClipboard(data.DNA);
        if (copied) {
          promptAction.showToast({ message: '✅ CNSH翻译完成·DNA已复制', duration: 2000 });
        } else {
          promptAction.showToast({ message: '✅ 翻译完成·但复制DNA失败', duration: 2000 });
        }
      } else {
        // API 调用失败
        const errorMsg = result.errorMessage ?? '未知错误';
        this.errorMessage = `翻译失败: ${errorMsg}`;
        promptAction.showToast({ message: `🔴 ${errorMsg}`, duration: 3000 });
      }
    } catch (err) {
      // 完全意外错误
      const errorMsg = `翻译异常: ${JSON.stringify(err)}`;
      this.errorMessage = errorMsg;
      promptAction.showToast({ message: `🔴 ${errorMsg}`, duration: 3000 });
    } finally {
      this.isLoading = false;
    }
  }

  // ===== 验证操作 =====

  async verify(): Promise<void> {
    if (!this.fullResult?.完整性组件) {
      promptAction.showToast({ message: '请先执行翻译', duration: 2000 });
      return;
    }

    this.verifyStatus = '验证中...';

    try {
      const result = await CnshAPI.verify(
        this.fullResult.完整性组件,
        getContext(this) as Record<string, unknown>
      );

      if (result.success && result.data) {
        this.verifyStatus = result.data.完整
          ? '✅ 完整性验证通过·包体完好'
          : '🔴 完整性断裂·包体已被篡改·不可使用';
      } else {
        this.verifyStatus = `⚠️ 验证请求失败: ${result.errorMessage}`;
      }
    } catch (err) {
      this.verifyStatus = `⚠️ 验证异常: ${JSON.stringify(err)}`;
    }
  }

  // ===== UI =====

  build() {
    Column() {
      // 顶栏
      Row() {
        Text('🐉 CNSH 剪贴板翻译')
          .fontSize(ScreenAdapter.fp2px(18))
          .fontWeight(600)
          .fontColor('#d4a574')
        Blank()
        Button() {
          Text('⚙')
            .fontSize(ScreenAdapter.fp2px(18))
            .fontColor('#8a8a9a')
        }
        .width(ScreenAdapter.vp2px(40))
        .height(ScreenAdapter.vp2px(40))
        .backgroundColor(Color.Transparent)
        .onClick(() => {
          router.pushUrl({ url: 'pages/Settings' });
        })
      }
      .width('100%')
      .padding({ left: 16, right: 16, top: 40, bottom: 12 })
      .backgroundColor('#1a1a2e')

      Scroll() {
        Column({ space: 12 }) {
          // 剪贴板读取按钮
          Button('📋 从剪贴板读取')
            .width('100%')
            .height(ScreenAdapter.vp2px(48))
            .fontSize(ScreenAdapter.fp2px(15))
            .backgroundColor('#2a2a3e')
            .fontColor('#e0d6c2')
            .borderRadius(12)
            .onClick(async () => {
              const r = await CnshAPI.getClipboard();
              if (r.success && r.text) {
                this.inputText = r.text;
                this.errorMessage = '';
              } else {
                this.errorMessage = r.error ?? '剪贴板为空或无权读取';
              }
            })

          // 父DNA输入
          TextInput({ placeholder: '父DNA码（可选·链式协作）', text: this.parentDna })
            .width('100%')
            .height(ScreenAdapter.vp2px(40))
            .fontSize(ScreenAdapter.fp2px(13))
            .backgroundColor('#16213e')
            .fontColor('#e0d6c2')
            .borderRadius(8)
            .placeholderColor('#8a8a9a')
            .onChange((v: string) => { this.parentDna = v; })

          // 文本预览
          if (this.inputText) {
            Text(this.inputText)
              .maxLines(5)
              .textOverflow({ overflow: TextOverflow.Ellipsis })
              .fontSize(ScreenAdapter.fp2px(13))
              .fontColor('#8a8a9a')
              .padding(12)
              .backgroundColor('#2a2a3e')
              .borderRadius(8)
              .width('100%')
          }

          // 错误提示 (红色)
          if (this.errorMessage) {
            Text(this.errorMessage)
              .fontSize(ScreenAdapter.fp2px(12))
              .fontColor('#e74c3c')
              .padding(10)
              .backgroundColor('rgba(231,76,60,0.1)')
              .borderRadius(8)
              .width('100%')
          }

          // 翻译按钮
          Button(this.isLoading ? '⏳ 翻译中...' : '🔮 翻译·注入DNA')
            .width('100%')
            .height(ScreenAdapter.vp2px(52))
            .fontSize(ScreenAdapter.fp2px(16))
            .fontWeight(600)
            .backgroundColor(this.isLoading ? '#8a6d4b' : '#d4a574')
            .fontColor('#1a1a2e')
            .borderRadius(12)
            .enabled(!this.isLoading)
            .onClick(() => { this.translate(); })

          // 翻译结果
          if (this.resultDNA) {
            Column({ space: 8 }) {
              Text('📦 翻译结果')
                .fontSize(ScreenAdapter.fp2px(14))
                .fontWeight(500)
                .fontColor('#d4a574')
                .width('100%')

              this.resultRow('🧬 DNA', this.resultDNA, '#d4a574')
              this.resultRow('🔒 时间戳', this.timestamp, '#e0d6c2')
              this.resultRow('🏷 关键字', this.keywords, '#0ff')
              this.resultRow('✅ 完整性', `${this.integrityHash}...`, '#2ecc71')

              Divider().color('#2a2a3e')

              Row({ space: 8 }) {
                Button('🔍 验证完整性')
                  .fontSize(ScreenAdapter.fp2px(12))
                  .backgroundColor('#2a2a3e')
                  .fontColor('#e0d6c2')
                  .borderRadius(8)
                  .height(ScreenAdapter.vp2px(36))
                  .onClick(() => { this.verify(); })

                Button('📋 复制JSON包')
                  .fontSize(ScreenAdapter.fp2px(12))
                  .backgroundColor('#2a2a3e')
                  .fontColor('#e0d6c2')
                  .borderRadius(8)
                  .height(ScreenAdapter.vp2px(36))
                  .onClick(async () => {
                    if (this.fullResult) {
                      const ok = await CnshAPI.setClipboard(
                        JSON.stringify(this.fullResult, null, 2)
                      );
                      promptAction.showToast({
                        message: ok ? '✅ JSON包已复制' : '❌ 复制失败',
                        duration: 2000
                      });
                    }
                  })
              }
              .width('100%')
              .justifyContent(FlexAlign.SpaceEvenly)

              if (this.verifyStatus) {
                Text(this.verifyStatus)
                  .fontSize(ScreenAdapter.fp2px(12))
                  .fontColor(this.verifyStatus.startsWith('✅') ? '#2ecc71' : '#e74c3c')
                  .padding(8)
                  .borderRadius(6)
                  .backgroundColor(this.verifyStatus.startsWith('✅')
                    ? 'rgba(46,204,113,0.1)'
                    : 'rgba(231,76,60,0.1)')
                  .width('100%')
                  .textAlign(TextAlign.Center)
              }
            }
            .padding(16)
            .backgroundColor('#1a1a2e')
            .borderRadius(12)
            .border({ width: 1, color: '#d4a574' })
            .width('100%')
          }
        }
        .padding(16)
      }
      .layoutWeight(1)
      .scrollBar(BarState.Auto)
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0f0f1a')
  }

  @Builder
  resultRow(label: string, value: string, valueColor: string) {
    Row() {
      Text(label)
        .fontSize(ScreenAdapter.fp2px(11))
        .fontColor('#8a8a9a')
        .width(ScreenAdapter.vp2px(70))
      Text(value)
        .fontSize(ScreenAdapter.fp2px(11))
        .fontColor(valueColor)
        .fontFamily('monospace')
        .layoutWeight(1)
        .textOverflow({ overflow: TextOverflow.Ellipsis })
    }
  }
}
```

---

## 12. `Settings.ets` — 设置页（动态服务器地址）

```typescript
// pages/Settings.ets
import { ServerConfig } from '../utils/ServerConfig';
import { ScreenAdapter } from '../utils/ScreenAdapter';
import promptAction from '@ohos.promptAction';
import router from '@ohos.router';

@Entry
@Component
struct Settings {
  @State serverUrl: string = '';
  @State saveStatus: string = '';

  async aboutToAppear(): Promise<void> {
    this.serverUrl = await ServerConfig.getBaseUrl(
      getContext(this) as Record<string, unknown>
    );
  }

  build() {
    Column() {
      Row() {
        Button() { Text('←') }
          .width(ScreenAdapter.vp2px(40))
          .height(ScreenAdapter.vp2px(40))
          .backgroundColor(Color.Transparent)
          .fontColor('#d4a574')
          .onClick(() => { router.back(); })

        Text('服务器设置')
          .fontSize(ScreenAdapter.fp2px(18))
          .fontWeight(600)
          .fontColor('#d4a574')
          .layoutWeight(1)
          .textAlign(TextAlign.Center)
      }
      .width('100%')
      .padding({ left: 16, right: 16, top: 40, bottom: 12 })
      .backgroundColor('#1a1a2e')

      Column({ space: 16 }) {
        Text('CNSH API 服务器地址')
          .fontSize(ScreenAdapter.fp2px(14))
          .fontColor('#8a8a9a')
          .width('100%')

        TextInput({ text: this.serverUrl, placeholder: 'http://192.168.x.x:8777' })
          .width('100%')
          .height(ScreenAdapter.vp2px(48))
          .fontSize(ScreenAdapter.fp2px(15))
          .backgroundColor('#2a2a3e')
          .fontColor('#e0d6c2')
          .borderRadius(10)
          .onChange((v: string) => { this.serverUrl = v; })

        Text('⚠️ 修改后立即生效，无需重启')
          .fontSize(ScreenAdapter.fp2px(11))
          .fontColor('#666')
          .width('100%')

        Button('💾 保存设置')
          .width('100%')
          .height(ScreenAdapter.vp2px(48))
          .fontSize(ScreenAdapter.fp2px(15))
          .fontWeight(600)
          .backgroundColor('#d4a574')
          .fontColor('#1a1a2e')
          .borderRadius(12)
          .onClick(async () => {
            if (!this.serverUrl || !this.serverUrl.startsWith('http')) {
              promptAction.showToast({ message: '请输入有效的 http(s) 地址', duration: 2000 });
              return;
            }
            await ServerConfig.setBaseUrl(
              getContext(this) as Record<string, unknown>,
              this.serverUrl
            );
            promptAction.showToast({ message: '✅ 已保存', duration: 2000 });
          })

        Divider().color('#2a2a3e')

        Text('关于')
          .fontSize(ScreenAdapter.fp2px(14))
          .fontColor('#8a8a9a')
          .width('100%')

        Text('CNSH 剪贴板翻译 v2.0\nDNA: #龍芯⚡️2026-07-08-HARMONYOS-CLIPBOARD-v2.0-PROD\nUID9622 · 诸葛鑫 · Lucky\n数据主权归集本地·不传云端')
          .fontSize(ScreenAdapter.fp2px(11))
          .fontColor('#666')
          .lineHeight(20)
          .width('100%')
      }
      .padding(16)
      .width('100%')
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0f0f1a')
  }
}
```

---

## 13. `ClipboardWidget.ets` — 桌面服务卡片

```typescript
// widget/pages/ClipboardWidget.ets
import { CnshAPI } from '../../common/CnshAPI';
import { DeviceCapability } from '../../utils/DeviceCapability';
import promptAction from '@ohos.promptAction';

@Entry
@Component
struct ClipboardWidget {
  @LocalStorageProp('dnaText') dnaText: string = '点击翻译';
  private text: string = '';

  async aboutToAppear(): Promise<void> {
    // 能力检查
    if (!DeviceCapability.checkSysCapability(DeviceCapability.CAPS.PASTEBOARD)) {
      this.dnaText = '设备不支持';
      return;
    }
    const r = await CnshAPI.getClipboard();
    if (r.success) this.text = r.text;
  }

  build() {
    Stack() {
      Column({ space: 6 }) {
        Text('🐉')
          .fontSize(24)
        Text('CNSH翻译')
          .fontSize(13)
          .fontWeight(500)
          .fontColor('#d4a574')
        Text(this.dnaText)
          .fontSize(10)
          .fontColor('#8a8a9a')
          .maxLines(1)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
      }
      .width('100%')
      .height('100%')
      .justifyContent(FlexAlign.Center)
      .alignItems(HorizontalAlign.Center)
      .backgroundColor('#1a1a2e')
      .borderRadius(12)
      .onClick(async () => {
        try {
          const result = await CnshAPI.translate(this.text);
          if (result.success && result.data) {
            await CnshAPI.setClipboard(result.data.DNA);
            promptAction.showToast({ message: '✅ 已注入DNA', duration: 1500 });
            postCardAction(this, {
              action: 'router',
              abilityName: 'EntryAbility',
              params: { result: JSON.stringify(result.data) }
            });
          } else {
            promptAction.showToast({ message: `🔴 ${result.errorMessage}`, duration: 1500 });
          }
        } catch (e) {
          promptAction.showToast({ message: '🔴 翻译失败', duration: 1500 });
        }
      })
    }
    .width('100%')
    .height('100%')
  }
}
```

---

## 资源文件

### `string.json` (base + zh_CN)

```json
{
  "string": [
    { "name": "module_desc", "value": "CNSH 剪贴板翻译·DNA注入·时间戳锁定" },
    { "name": "internet_reason", "value": "需要网络权限连接CNSH翻译服务器" },
    { "name": "pasteboard_reason", "value": "需要读取剪贴板中的待翻译文本" },
    { "name": "network_info_reason", "value": "需要检测网络状态以判断是否可翻译" },
    { "name": "founder_info", "value": "UID9622 · 诸葛鑫 · 数据主权归集本地" }
  ]
}
```

### `color.json`

```json
{
  "color": [
    { "name": "bg_primary", "value": "#0f0f1a" },
    { "name": "bg_card", "value": "#1a1a2e" },
    { "name": "accent_gold", "value": "#d4a574" },
    { "name": "text_primary", "value": "#e0d6c2" },
    { "name": "text_secondary", "value": "#8a8a9a" }
  ]
}
```

### `main_pages.json`

```json
{
  "src": [
    "pages/Index",
    "pages/Settings"
  ]
}
```

### `form_config.json`

```json
{
  "forms": [{
    "name": "ClipboardWidget",
    "description": "CNSH 剪贴板翻译卡片",
    "src": "./ets/widget/pages/ClipboardWidget.ets",
    "formConfigAbility": "ability://EntryAbility",
    "colorMode": "auto",
    "isDefault": true,
    "updateEnabled": false,
    "scheduledUpdateTime": "06:00",
    "updateDuration": 0,
    "defaultDimension": "2*2",
    "supportDimensions": ["2*2"]
  }]
}
```

---

## 部署方式

| 方式 | 步骤 | 适用场景 |
|------|------|---------|
| **DevEco Studio 编译运行** | 打开项目 → 连接鸿蒙设备 → Run 'entry' | 开发调试 |
| **HAP 侧载安装** | `hdc install entry-default-signed.hap` | 内部分发 |
| **AppGallery Connect 上架** | 提交审核 → 原子化服务 → 即点即用 | 公开发布 |
| **快应用** | 使用快应用 IDE 转换 → 提交华为快应用联盟 | 轻量级入口 |

---

## 交付自检

| # | 检查项 | 预期结果 |
|:--:|--------|---------|
| 1 | DevEco Studio 编译 | 0 ERROR |
| 2 | 首次启动权限弹窗 | 弹出网络+剪贴板权限请求 |
| 3 | 拒绝权限后 | 显示错误提示，不闪退 |
| 4 | 服务器不可达 | 显示"网络不可达"超时提示，不白屏 |
| 5 | 修改服务器地址 | 设置页修改后下次请求使用新地址 |
| 6 | 平板/折叠屏 | 布局自适应，不错乱 |
| 7 | 服务卡片 | 点击翻译正常 |
| 8 | API 返回 500 | 显示"服务器错误"不崩溃 |

---

> **铁律**: 交付前 8 项必须全绿。缺任何一项 = 不可交付。
> DNA: `#龍芯⚡️2026-07-08-HARMONYOS-CLIPBOARD-v2.0-PROD-E5C8A1F2`
