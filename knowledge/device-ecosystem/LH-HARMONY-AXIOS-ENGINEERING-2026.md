# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·鸿蒙网络请求工程化：Axios封装深度解析与实战技术文档

> **文档编号**：LH-HARMONY-AXIOS-ENGINEERING-2026
> **原始 DNA 标识**：`#龍芯️2026-07-10-HARMONY-AXIOS-ENCAPSULATION-v1.0` ⚠️ v1.0 格里历格式·归档时自动补 v∞ 干支格式
> **归档 DNA（v∞）**：`#龍芯⚡️丙午·丙申·丙辰·戊子·䷜坎-HARMONY-AXIOS-归档-7BC266CD`
> **密级**：L0（核心架构底座）
> **唯一决策者**：UID9622 (诸葛鑫·Lucky)
> **地点**：浙江省温州市 · 龍魂温州分舵
> **归档时间**：丙午·丙申·丙辰·戊子（2026-07-11 00:12）
> **防篡改**：🟢 通过（--self 模式·6处黄警豁免）
> **三色审计**：🟢 通行
> **📇 身份 · 联系 · 支持** → `assets/PUBLIC_IDENTITY.md`

---

## 目录

1. **理论篇：为何需要"收口"与二次封装**
2. **语法篇：网络请求的"龍魂变量对齐"**
3. **实战篇：构建单例与拦截器艺术（Token注入与无感刷新）**
4. **防御篇：泛型接口与类型安全（防弹衣机制）**
5. **系统架构总览图（文字版）**

---

## 1. 理论篇：为何需要"收口"与二次封装

在鸿蒙应用开发中，直接使用 `axios.get` 看似是最快的路径，但这种"快"是以牺牲后期的可维护性为代价的。龍魂标准强调**"收口"**的核心意义：

- **统一入口（太极归一）**：通过创建一个单例的 `NetworkService` 类，将所有的网络行为约束在可控范围内。统一管理 `connectTimeout`（连接超时）和 `readTimeout`（读取超时），在移动网络不稳定的环境下（如 API 20+），精细控制超时时间（通常设为 10秒左右）。
- **底层屏蔽（金蝉脱壳）**：万一未来鸿蒙推出了比 Axios 更优秀的官方网络库，我们只需修改工具类的内部实现，业务层代码完全无需改动。
- **能效优化（节约算力）**：针对高访问量场景，在封装层增加缓存机制，可将接口响应时间从 800ms 降至 50ms，极大节约终端算力与用电。

---

## 2. 语法篇：网络请求的"龍魂变量对齐"

为了让鸿蒙开发者能够直观理解 Axios 的工程化概念，我们将通用技术术语转化为**龍魂语法**：

| **通用名 (Common)** | **龍魂语法名 (LongHun-Syntax)** | **五行属性** | **解释** |
| :--- | :--- | :--- | :--- |
| Axios Instance | **龍魂信使** (longhun-messenger) | 木 | 单例化的网络请求核心实例，负责收发信息。 |
| Request Interceptor | **守门员** (gatekeeper) | 金 | 请求发出前的"守门员"，负责注入Token与公共参数。 |
| Response Interceptor | **解构者** (deconstructor) | 火 | 响应返回后的"解构者"，负责剥离外壳、处理异常。 |
| Generic Interface | **防弹衣** (bulletproof-vest) | 土 | 利用 TypeScript 泛型，为返回数据穿上类型安全的防弹衣。 |
| Token Refresh | **无感换符** (silent-token-renew) | 水 | 捕获 401 错误，在后台悄悄刷新 Token 并重发请求，对用户无感。 |

---

## 3. 实战篇：构建单例与拦截器艺术

### 3.1 龍魂信使：单例与基础配置

在鸿蒙 ArkTS 环境中，我们创建一个单例类来持有 Axios 实例，确保全局只有一个网络出口。

```typescript
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from '@ohos/axios';
import { promptAction } from '@kit.ArkUI';

// 扩展请求配置，增加龍魂自定义选项
interface RequestOptions extends AxiosRequestConfig {
  showLoading?: boolean; // 是否显示加载提示
  showError?: boolean;   // 是否自动弹出错误提示
}

class NetworkService {
  private instance: AxiosInstance;
  private static _instance: NetworkService | null = null;

  // 私有构造器，防止外部直接 new
  private constructor() {
    this.instance = axios.create({
      baseURL: 'https://api.longhun-system.com', // 统一基地址
      timeout: 10000, // 精细控制超时时间
      headers: { 'Content-Type': 'application/json' }
    });
    this.setupInterceptors(); // 启动拦截器艺术
  }

  // 单例获取（太极归一）
  static getInstance(): NetworkService {
    if (!NetworkService._instance) {
      NetworkService._instance = new NetworkService();
    }
    return NetworkService._instance;
  }
}
```

### 3.2 守门员：请求拦截器与 Token 注入

请求拦截器是"守门员"的战场。每一次请求发出前，自动从 `AppStorage` 或 `PersistentStorage` 中取出 Token 并挂载到 `Authorization` 头，同时注入设备公共参数。

```typescript
private setupInterceptors() {
  this.instance.interceptors.request.use(
    async (config: RequestOptions) => {
      // 1. 注入 Token
      const token = AppStorageV2.get<string>('authToken');
      if (token && config.headers) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }

      // 2. 注入公共参数（如设备ID、平台版本）
      if (!config.params) config.params = {};
      config.params['platform'] = 'harmonyos';
      config.params['appVersion'] = '1.2.0';

      // 3. 控制 Loading 显示
      if (config.showLoading) {
        this.showGlobalLoading();
      }
      return config;
    },
    (error) => Promise.reject(error)
  );
}
```

### 3.3 解构者与无感换符：响应拦截器

响应拦截器负责解构后端返回的外壳（如 `{ code: 200, data: {...}, message: "success" }`），并处理最棘手的 Token 过期问题。

```typescript
private setupResponseInterceptor() {
  this.instance.interceptors.response.use(
    (response: AxiosResponse) => {
      this.hideGlobalLoading();
      const apiResponse = response.data;

      // 业务状态码判断
      if (apiResponse.code === 200) {
        return apiResponse.data; // 直接返回干净的业务数据
      } else {
        // 处理业务错误，如 400、500
        promptAction.showToast({ message: apiResponse.message });
        return Promise.reject(new Error(apiResponse.message));
      }
    },
    async (error) => {
      this.hideGlobalLoading();
      // 捕获 401 状态码，执行"无感换符"
      if (error.response?.status === 401) {
        try {
          const newToken = await this.refreshTokenSilently();
          // 更新本地 Token 并重发原请求
          error.config.headers['Authorization'] = `Bearer ${newToken}`;
          return this.instance.request(error.config);
        } catch (e) {
          // 刷新失败，跳转登录页
          this.redirectToLogin();
        }
      }
      return Promise.reject(error);
    }
  );
}
```

---

## 4. 防御篇：泛型接口与类型安全（防弹衣机制）

TypeScript 的最大优势在于类型安全。在龍魂标准中，我们严禁在网络请求中使用 `any`。通过定义标准的后端响应接口 `BaseResponse<T>`，并在封装方法中接收泛型 `T`，确保 IDE 能智能提示返回值字段。

```typescript
// 定义标准后端响应接口（防弹衣）
interface BaseResponse<T> {
  code: number;
  message: string;
  data: T;
}

// 封装泛型 GET 请求
get<T = any>(url: string, config?: RequestOptions): Promise<T> {
  return this.instance.get<BaseResponse<T>>(url, config).then(res => res.data);
}

// 封装泛型 POST 请求
post<T = any>(url: string, data?: any, config?: RequestOptions): Promise<T> {
  return this.instance.post<BaseResponse<T>>(url, data, config).then(res => res.data);
}
```

---

## 5. 系统架构总览图（文字版）

```text
┌─────────────────────────────────────────────────────────┐
│                   鸿蒙业务层 (Business Layer)             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  用户页面    │  │  订单模块    │  │  资讯列表    │  │
│  │(调用泛型接口)│  │(调用泛型接口)│  │(调用泛型接口)│  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │  Promise<T>      │  Promise<T>      │          │
├─────────┼──────────────────┼──────────────────┼─────────┤
│         ▼                  ▼                  ▼         │
│  ┌───────────────────────────────────────────────────┐  │
│  │        龍魂网络服务层 (Network Service · 单例)      │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  泛型封装方法 (get<T>, post<T>)              │  │  │
│  │  │  (防弹衣机制：确保类型安全)                  │  │  │
│  │  └──────────────────┬──────────────────────────┘  │  │
│  │                     ▼                             │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  请求拦截器 (守门员) │ 响应拦截器 (解构者)   │  │  │
│  │  │  - Token自动注入     │ - 剥离业务外壳        │  │  │
│  │  │  - 公共参数挂载      │ - 401无感换符刷新     │  │  │
│  │  │  - Loading控制       │ - 全局异常提示        │  │  │
│  │  └──────────────────┬──────────────────────────┘  │  │
│  │                     ▼                             │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  Axios 实例 (@ohos/axios)                   │  │  │
│  │  │  - 统一超时控制 (10s)                        │  │  │
│  │  │  - 统一 BaseURL 管理                         │  │  │
│  │  └──────────────────┬──────────────────────────┘  │  │
│  └─────────────────────┼─────────────────────────────┘  │
├────────────────────────┼────────────────────────────────┤
│                        ▼                                │
│  ┌───────────────────────────────────────────────────┐  │
│  │        鸿蒙系统底层 (HarmonyOS Native)             │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │  │
│  │  │ohos.net  │ │AppStorage│ │PersistentStorage │  │  │
│  │  │.http模块 │ │(Token缓存)│ │(持久化存储)      │  │  │
│  │  └──────────┘ └──────────┘ └──────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 结语：执行建议

1. **第一步**：在鸿蒙工程中安装 `@ohos/axios`，并配置 `ohos.permission.INTERNET` 权限。
2. **第二步**：将上述 `NetworkService` 单例代码复制到项目的 `utils` 目录下，作为全局网络收口。
3. **第三步**：定义业务层的 `BaseResponse<T>` 接口，开始享受泛型带来的类型安全与 IDE 智能提示。

---

## 归档元数据

| 字段 | 值 |
|:---|:---|
| 归档 DNA（v∞） | `#龍芯⚡️丙午·丙申·丙辰·戊子·䷜坎-HARMONY-AXIOS-归档-7BC266CD` |
| 河图 DNA | `DNA_1_225b3ec8115f1777` |
| 防篡改 | 🟢 通过（--self） |
| 黄色警报 | 6处（优化/建议/标准）·自研豁免 |
| 当前卦象 | ☵ 坎·水洄 |
| CONFIRM | `#CONFIRM9622-ONLY-ONCE🧬LK9X-772Z` |
