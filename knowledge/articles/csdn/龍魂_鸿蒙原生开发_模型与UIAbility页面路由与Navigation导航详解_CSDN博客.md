# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 · 鸿蒙原生开发：模型与UIAbility页面路由与Navigation导航详解

> 龍魂系统 · 鸿蒙原生适配层 · 从数据模型到页面路由的完整链路
> 
> DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622 | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 一、核心定位

| 维度 | 说明 |
|------|------|
| 平台 | 鸿蒙 HarmonyOS NEXT · 纯血鸿蒙 |
| 语言 | ArkTS · 声明式UI · Stage模型 |
| 场景 | 数据模型层 · UIAbility生命周期 · 页面路由 · Navigation导航栈 |
| 架构 | 龍魂蚁群触角 → 鸿蒙Stage模型 → 页面路由引擎 |
| 主权 | 数据本地 · 国密SM2/SM3签名 · 不上传云端 |
| 设计 | 模型驱动视图 · 路由守卫 · 导航栈管理 · 状态持久化 |

---

## 二、系统架构

```
┌─────────────────────────────────────────┐
│           龍魂系统 · 鸿蒙适配层            │
│  DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ │
│  UID: 9622                              │
├─────────────────────────────────────────┤
│         鸿蒙 Stage 模型层                 │
│                                         │
│  UIAbility → onCreate/onWindowStageCreate │
│  ├── 数据模型层（Model）                   │
│  ├── 视图层（View/Component）              │
│  ├── 控制器层（Controller/ViewModel）      │
│  ├── 页面路由层（Router/Navigation）       │
│  ├── 状态管理层（AppStorage/LocalStorage） │
│  ├── 导航栈管理（NavPathStack）            │
│  ├── 生命周期钩子（Lifecycle）             │
│  └── 国密签名验证（CryptoVerifier）        │
├─────────────────────────────────────────┤
│         鸿蒙系统能力层                      │
│                                         │
│  UIAbility · AbilityStage · WindowStage │
│  Router · Navigation · NavDestination     │
│  AppStorage · LocalStorage · PersistentStorage │
│  生命周期(Lifecycle) · 事件(EventHub)    │
│  后台任务(WorkScheduler) · 剪贴板(Pasteboard) │
└─────────────────────────────────────────┘
```

---

## 三、数据模型层

### 3.1 基础模型（`entry/src/main/ets/models/BaseModel.ets`）

```typescript
// entry/src/main/ets/models/BaseModel.ets
// 龍魂 · 基础模型层 · ArkTS

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 模型基类 ===
export abstract class BaseModel {
  id: string;
  createdAt: Date;
  updatedAt: Date;
  dnaSignature: string;

  constructor(data: Partial<BaseModel> = {}) {
    this.id = data.id || this.generateId();
    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
    this.dnaSignature = this.signData();
  }

  protected generateId(): string {
    return `${this.getPrefix()}-${MASTER_UID}-${Date.now().toString(36).substr(-6)}`;
  }

  protected abstract getPrefix(): string;

  protected signData(): string {
    const payload = `${this.id}-${this.createdAt.getTime()}-${this.getPrefix()}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }

  // 更新模型
  update(data: Partial<this>): void {
    Object.assign(this, data);
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  // 验证签名
  verify(): boolean {
    return this.dnaSignature === this.signData();
  }

  // 序列化
  toJSON(): string {
    return JSON.stringify(this);
  }

  // 反序列化
  static fromJSON<T extends BaseModel>(json: string, factory: (data: any) => T): T {
    const data = JSON.parse(json);
    return factory(data);
  }
}

// === 用户模型 ===
export class UserModel extends BaseModel {
  uid: string;
  name: string;
  avatar: string;
  role: 'admin' | 'user' | 'guest';
  department: string;
  permissions: string[];

  constructor(data: Partial<UserModel> = {}) {
    super(data);
    this.uid = data.uid || MASTER_UID;
    this.name = data.name || '龍魂用户';
    this.avatar = data.avatar || '';
    this.role = data.role || 'user';
    this.department = data.department || '龍魂系统';
    this.permissions = data.permissions || ['read'];
  }

  protected getPrefix(): string { return 'USER'; }

  // 检查权限
  hasPermission(permission: string): boolean {
    return this.permissions.includes(permission) || this.permissions.includes('*');
  }

  // 是否管理员
  isAdmin(): boolean {
    return this.role === 'admin';
  }
}

// === 页面状态模型 ===
export class PageStateModel extends BaseModel {
  pageName: string;
  route: string;
  params: Record<string, any>;
  scrollPosition: number;
  formData: Record<string, any>;
  isDirty: boolean;            // 是否有未保存更改

  constructor(data: Partial<PageStateModel> = {}) {
    super(data);
    this.pageName = data.pageName || '';
    this.route = data.route || '';
    this.params = data.params || {};
    this.scrollPosition = data.scrollPosition || 0;
    this.formData = data.formData || {};
    this.isDirty = data.isDirty || false;
  }

  protected getPrefix(): string { return 'PAGE'; }

  // 保存表单数据
  saveFormData(key: string, value: any): void {
    this.formData[key] = value;
    this.isDirty = true;
    this.update({});
  }

  // 清除脏标记
  clearDirty(): void {
    this.isDirty = false;
    this.update({});
  }

  // 恢复滚动位置
  restoreScroll(): number {
    return this.scrollPosition;
  }
}

// === 导航历史模型 ===
export class NavigationHistoryModel extends BaseModel {
  stack: NavRecord[];
  currentIndex: number;
  maxDepth: number;

  constructor(data: Partial<NavigationHistoryModel> = {}) {
    super(data);
    this.stack = data.stack || [];
    this.currentIndex = data.currentIndex || -1;
    this.maxDepth = data.maxDepth || 50;
  }

  protected getPrefix(): string { return 'NAV'; }

  // 压栈
  push(record: NavRecord): void {
    // 截断前进历史
    this.stack = this.stack.slice(0, this.currentIndex + 1);
    this.stack.push(record);

    // 超限截断
    if (this.stack.length > this.maxDepth) {
      this.stack = this.stack.slice(-this.maxDepth);
    }

    this.currentIndex = this.stack.length - 1;
    this.update({});
  }

  // 后退
  back(): NavRecord | null {
    if (this.canGoBack()) {
      this.currentIndex--;
      this.update({});
      return this.stack[this.currentIndex];
    }
    return null;
  }

  // 前进
  forward(): NavRecord | null {
    if (this.canGoForward()) {
      this.currentIndex++;
      this.update({});
      return this.stack[this.currentIndex];
    }
    return null;
  }

  // 能否后退
  canGoBack(): boolean {
    return this.currentIndex > 0;
  }

  // 能否前进
  canGoForward(): boolean {
    return this.currentIndex < this.stack.length - 1;
  }

  // 获取当前
  current(): NavRecord | null {
    if (this.currentIndex >= 0 && this.currentIndex < this.stack.length) {
      return this.stack[this.currentIndex];
    }
    return null;
  }

  // 获取栈深
  depth(): number {
    return this.stack.length;
  }

  // 清空
  clear(): void {
    this.stack = [];
    this.currentIndex = -1;
    this.update({});
  }
}

export interface NavRecord {
  name: string;              // 页面名称
  route: string;            // 路由路径
  params?: Record<string, any>; // 参数
  timestamp: number;         // 时间戳
  dnaSignature: string;    // 签名
}

// === 路由守卫模型 ===
export class RouteGuardModel extends BaseModel {
  route: string;
  guards: GuardRule[];
  fallbackRoute: string;

  constructor(data: Partial<RouteGuardModel> = {}) {
    super(data);
    this.route = data.route || '';
    this.guards = data.guards || [];
    this.fallbackRoute = data.fallbackRoute || '/login';
  }

  protected getPrefix(): string { return 'GUARD'; }

  // 检查是否允许通过
  canActivate(user: UserModel, params: Record<string, any>): { allowed: boolean; reason?: string } {
    for (const guard of this.guards) {
      const result = this.checkGuard(guard, user, params);
      if (!result.allowed) {
        return result;
      }
    }
    return { allowed: true };
  }

  private checkGuard(guard: GuardRule, user: UserModel, params: Record<string, any>): { allowed: boolean; reason?: string } {
    switch (guard.type) {
      case 'auth':
        if (!user || user.role === 'guest') {
          return { allowed: false, reason: '需要登录' };
        }
        break;
      case 'role':
        if (guard.roles && !guard.roles.includes(user.role)) {
          return { allowed: false, reason: `需要角色: ${guard.roles.join('/')}` };
        }
        break;
      case 'permission':
        if (guard.permissions && !guard.permissions.every(p => user.hasPermission(p))) {
          return { allowed: false, reason: '权限不足' };
        }
        break;
      case 'param':
        if (guard.requiredParams && !guard.requiredParams.every(p => params[p] !== undefined)) {
          return { allowed: false, reason: `缺少参数: ${guard.requiredParams.join(',')}` };
        }
        break;
      case 'custom':
        if (guard.validator && !guard.validator(user, params)) {
          return { allowed: false, reason: guard.message || '自定义验证失败' };
        }
        break;
    }
    return { allowed: true };
  }
}

export interface GuardRule {
  type: 'auth' | 'role' | 'permission' | 'param' | 'custom';
  roles?: string[];
  permissions?: string[];
  requiredParams?: string[];
  validator?: (user: UserModel, params: Record<string, any>) => boolean;
  message?: string;
}
```

### 3.2 全局状态管理

```typescript
// entry/src/main/ets/models/AppState.ets
// 龍魂 · 应用全局状态

import { UserModel, PageStateModel, NavigationHistoryModel, RouteGuardModel } from './BaseModel';

@Observed
export class AppState {
  // 当前用户
  currentUser: UserModel = new UserModel();

  // 页面状态缓存
  pageStates: Map<string, PageStateModel> = new Map();

  // 导航历史
  navHistory: NavigationHistoryModel = new NavigationHistoryModel();

  // 路由守卫配置
  routeGuards: Map<string, RouteGuardModel> = new Map();

  // 应用配置
  settings: AppSettings = {
    theme: 'dark',
    language: 'zh-CN',
    fontScale: 1.0,
    animations: true,
    autoSave: true,
    syncInterval: 30000
  };

  // 初始化
  init(): void {
    this.loadUser();
    this.loadSettings();
    this.loadNavHistory();
    this.setupRouteGuards();
  }

  // 加载用户
  private loadUser(): void {
    const userData = AppStorage.get<string>('app_user');
    if (userData) {
      try {
        this.currentUser = UserModel.fromJSON(userData, (d) => new UserModel(d));
      } catch (e) {
        console.error('[龍魂] 加载用户失败', e);
      }
    }
  }

  // 保存用户
  saveUser(): void {
    AppStorage.setOrCreate('app_user', this.currentUser.toJSON());
  }

  // 登录
  login(user: UserModel): void {
    this.currentUser = user;
    this.saveUser();
  }

  // 登出
  logout(): void {
    this.currentUser = new UserModel();
    this.pageStates.clear();
    this.navHistory.clear();
    AppStorage.delete('app_user');
  }

  // 获取页面状态
  getPageState(route: string): PageStateModel {
    if (!this.pageStates.has(route)) {
      this.pageStates.set(route, new PageStateModel({ route }));
    }
    return this.pageStates.get(route)!;
  }

  // 保存页面状态
  savePageState(route: string, state: Partial<PageStateModel>): void {
    const pageState = this.getPageState(route);
    pageState.update(state);
    this.pageStates.set(route, pageState);
    AppStorage.setOrCreate(`page_state_${route}`, pageState.toJSON());
  }

  // 检查路由权限
  checkRoute(route: string, params: Record<string, any> = {}): { allowed: boolean; redirect?: string; reason?: string } {
    const guard = this.routeGuards.get(route);
    if (!guard) return { allowed: true };

    const result = guard.canActivate(this.currentUser, params);
    if (!result.allowed) {
      return {
        allowed: false,
        redirect: guard.fallbackRoute,
        reason: result.reason
      };
    }
    return { allowed: true };
  }

  // 配置路由守卫
  private setupRouteGuards(): void {
    this.routeGuards.set('/admin', new RouteGuardModel({
      route: '/admin',
      guards: [
        { type: 'auth' },
        { type: 'role', roles: ['admin'] }
      ],
      fallbackRoute: '/login'
    }));

    this.routeGuards.set('/project/edit', new RouteGuardModel({
      route: '/project/edit',
      guards: [
        { type: 'auth' },
        { type: 'permission', permissions: ['write'] },
        { type: 'param', requiredParams: ['id'] }
      ],
      fallbackRoute: '/login'
    }));

    this.routeGuards.set('/settings', new RouteGuardModel({
      route: '/settings',
      guards: [{ type: 'auth' }],
      fallbackRoute: '/login'
    }));
  }

  // 加载设置
  private loadSettings(): void {
    const settings = AppStorage.get<string>('app_settings');
    if (settings) {
      try {
        this.settings = { ...this.settings, ...JSON.parse(settings) };
      } catch (e) {
        console.error('[龍魂] 加载设置失败', e);
      }
    }
  }

  // 保存设置
  saveSettings(): void {
    AppStorage.setOrCreate('app_settings', JSON.stringify(this.settings));
  }

  // 加载导航历史
  private loadNavHistory(): void {
    const history = AppStorage.get<string>('nav_history');
    if (history) {
      try {
        const data = JSON.parse(history);
        this.navHistory = new NavigationHistoryModel(data);
      } catch (e) {
        console.error('[龍魂] 加载导航历史失败', e);
      }
    }
  }

  // 保存导航历史
  saveNavHistory(): void {
    AppStorage.setOrCreate('nav_history', this.navHistory.toJSON());
  }

  persist(): void {
    this.saveUser();
    this.saveSettings();
    this.saveNavHistory();
  }
}

export interface AppSettings {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  fontScale: number;
  animations: boolean;
  autoSave: boolean;
  syncInterval: number;
}

// 全局状态
export const appState = new AppState();
AppStorage.setOrCreate('appState', appState);
```

---

## 四、UIAbility生命周期

### 4.1 EntryAbility（`entry/src/main/ets/entryability/EntryAbility.ets`）

```typescript
// entry/src/main/ets/entryability/EntryAbility.ets
// 龍魂 · EntryAbility生命周期 · ArkTS

import { AbilityConstant, UIAbility, Want, window } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { appState } from '../models/AppState';

const TAG = 'LonghunEntryAbility';

export default class EntryAbility extends UIAbility {
  // === 创建时 ===
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onCreate');

    // 初始化全局状态
    appState.init();

    // 记录启动参数
    hilog.info(0x0000, TAG, `[龍魂] 启动参数: ${JSON.stringify(want.parameters)}`);

    // 处理深度链接
    if (want.uri) {
      this.handleDeepLink(want.uri);
    }
  }

  // === 销毁时 ===
  onDestroy(): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onDestroy');

    // 持久化状态
    appState.persist();
  }

  // === 窗口创建时 ===
  onWindowStageCreate(windowStage: window.WindowStage): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onWindowStageCreate');

    // 加载主页面
    windowStage.loadContent('pages/Index', (err, data) => {
      if (err.code) {
        hilog.error(0x0000, TAG, `[龍魂] 加载页面失败: ${JSON.stringify(err)}`);
        return;
      }
      hilog.info(0x0000, TAG, '[龍魂] 页面加载成功');

      // 获取窗口实例
      const win = windowStage.getMainWindowSync();

      // 监听窗口大小变化（响应式适配）
      win.on('windowSizeChange', (size) => {
        hilog.info(0x0000, TAG, `[龍魂] 窗口变化: ${size.width}x${size.height}`);
        AppStorage.setOrCreate('window_width', size.width);
        AppStorage.setOrCreate('window_height', size.height);
      });

      // 监听窗口失焦/获焦
      win.on('windowFocusChange', (isFocus) => {
        hilog.info(0x0000, TAG, `[龍魂] 窗口焦点: ${isFocus}`);
        AppStorage.setOrCreate('window_focused', isFocus);
      });
    });
  }

  // === 窗口销毁时 ===
  onWindowStageDestroy(): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onWindowStageDestroy');
  }

  // === 前台时 ===
  onForeground(): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onForeground');

    // 恢复状态
    appState.loadNavHistory();
  }

  // === 后台时 ===
  onBackground(): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onBackground');

    // 保存状态
    appState.persist();
  }

  // === 新Want ===
  onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onNewWant');

    // 处理新的启动参数（如通知点击）
    if (want.uri) {
      this.handleDeepLink(want.uri);
    }

    if (want.parameters) {
      AppStorage.setOrCreate('launch_params', want.parameters);
    }
  }

  // === 处理深度链接 ===
  private handleDeepLink(uri: string): void {
    hilog.info(0x0000, TAG, `[龍魂] 深度链接: ${uri}`);

    // 解析URI
    // longhun://page/project?id=123
    const url = new URL(uri);
    const path = url.pathname;
    const params: Record<string, string> = {};
    url.searchParams.forEach((value, key) => {
      params[key] = value;
    });

    // 存储深度链接信息
    AppStorage.setOrCreate('deep_link_path', path);
    AppStorage.setOrCreate('deep_link_params', JSON.stringify(params));

    hilog.info(0x0000, TAG, `[龍魂] 深度链接解析: path=${path}, params=${JSON.stringify(params)}`);
  }

  // === 内存不足 ===
  onMemoryLevel(level: AbilityConstant.MemoryLevel): void {
    hilog.warn(0x0000, TAG, `[龍魂] 内存警告: ${level}`);

    if (level === AbilityConstant.MemoryLevel.MEMORY_LEVEL_MODERATE ||
        level === AbilityConstant.MemoryLevel.MEMORY_LEVEL_LOW) {
      // 清理非必要缓存
      appState.persist();
    }
  }
}
```

---

## 五、页面路由系统

### 5.1 路由配置（`entry/src/main/ets/router/RouterConfig.ets`）

```typescript
// entry/src/main/ets/router/RouterConfig.ets
// 龍魂 · 路由配置中心

import { appState } from '../models/AppState';

// === 路由表 ===
export interface RouteConfig {
  name: string;              // 路由名称
  path: string;             // 路径
  component: string;        // 组件路径
  title: string;            // 页面标题
  icon?: string;            // 图标
  guards?: string[];        // 守卫类型
  params?: ParamConfig[];   // 参数配置
  meta?: RouteMeta;         // 元数据
}

export interface ParamConfig {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'object';
  required: boolean;
  default?: any;
}

export interface RouteMeta {
  keepAlive?: boolean;      // 是否缓存
  hideTabBar?: boolean;      // 隐藏TabBar
  hideNavBar?: boolean;      // 隐藏导航栏
  transition?: string;        // 转场动画
  depth?: number;           // 页面层级
}

// === 路由表定义 ===
export const ROUTE_TABLE: RouteConfig[] = [
  {
    name: 'Index',
    path: '/',
    component: 'pages/Index',
    title: '龍魂首页',
    icon: '🏠',
    meta: { keepAlive: true, transition: 'fade' }
  },
  {
    name: 'Login',
    path: '/login',
    component: 'pages/LoginPage',
    title: '登录',
    meta: { hideTabBar: true, hideNavBar: true, transition: 'slide' }
  },
  {
    name: 'ProjectList',
    path: '/project',
    component: 'pages/ProjectListPage',
    title: '项目管理',
    icon: '📊',
    guards: ['auth'],
    meta: { keepAlive: true, transition: 'slide' }
  },
  {
    name: 'ProjectDetail',
    path: '/project/detail',
    component: 'pages/ProjectDetailPage',
    title: '项目详情',
    guards: ['auth'],
    params: [
      { name: 'id', type: 'string', required: true }
    ],
    meta: { transition: 'slide' }
  },
  {
    name: 'ProjectEdit',
    path: '/project/edit',
    component: 'pages/ProjectEditPage',
    title: '编辑项目',
    guards: ['auth', 'write'],
    params: [
      { name: 'id', type: 'string', required: false }
    ],
    meta: { transition: 'slide' }
  },
  {
    name: 'MilestoneTimeline',
    path: '/milestone',
    component: 'pages/MilestoneTimelinePage',
    title: '里程碑时间线',
    icon: '📈',
    guards: ['auth'],
    meta: { keepAlive: true, transition: 'slide' }
  },
  {
    name: 'WeeklyReview',
    path: '/weekly',
    component: 'pages/WeeklyReviewPage',
    title: '周报管理',
    icon: '📝',
    guards: ['auth'],
    meta: { keepAlive: true, transition: 'slide' }
  },
  {
    name: 'StampManagement',
    path: '/stamp',
    component: 'pages/StampManagementPage',
    title: '印章管理',
    icon: '🔏',
    guards: ['auth', 'admin'],
    meta: { transition: 'slide' }
  },
  {
    name: 'Settings',
    path: '/settings',
    component: 'pages/SettingsPage',
    title: '设置',
    icon: '⚙️',
    guards: ['auth'],
    meta: { transition: 'slide' }
  },
  {
    name: 'Profile',
    path: '/profile',
    component: 'pages/ProfilePage',
    title: '个人中心',
    icon: '👤',
    guards: ['auth'],
    meta: { transition: 'slide' }
  }
];

// === 路由工具类 ===
export class RouterUtils {
  // 根据名称获取路由
  static getRouteByName(name: string): RouteConfig | undefined {
    return ROUTE_TABLE.find(r => r.name === name);
  }

  // 根据路径获取路由
  static getRouteByPath(path: string): RouteConfig | undefined {
    return ROUTE_TABLE.find(r => r.path === path);
  }

  // 验证参数
  static validateParams(route: RouteConfig, params: Record<string, any>): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!route.params) return { valid: true, errors };

    for (const param of route.params) {
      if (param.required && params[param.name] === undefined) {
        errors.push(`缺少必需参数: ${param.name}`);
      }

      if (params[param.name] !== undefined) {
        const actualType = typeof params[param.name];
        if (param.type === 'number' && actualType !== 'number') {
          errors.push(`参数 ${param.name} 类型错误, 期望: ${param.type}`);
        }
        if (param.type === 'boolean' && actualType !== 'boolean') {
          errors.push(`参数 ${param.name} 类型错误, 期望: ${param.type}`);
        }
      }
    }

    return { valid: errors.length === 0, errors };
  }

  // 构建URL
  static buildUrl(path: string, params?: Record<string, any>): string {
    if (!params) return path;

    const query = Object.entries(params)
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
      .join('&');

    return query ? `${path}?${query}` : path;
  }

  // 解析URL
  static parseUrl(url: string): { path: string; params: Record<string, string> } {
    const [path, query] = url.split('?');
    const params: Record<string, string> = {};

    if (query) {
      query.split('&').forEach(pair => {
        const [k, v] = pair.split('=').map(decodeURIComponent);
        if (k) params[k] = v || '';
      });
    }

    return { path, params };
  }

  // 检查权限
  static checkAccess(path: string, params: Record<string, any> = {}): { allowed: boolean; redirect?: string; reason?: string } {
    return appState.checkRoute(path, params);
  }

  // 获取TabBar路由
  static getTabBarRoutes(): RouteConfig[] {
    return ROUTE_TABLE.filter(r => r.icon && !r.meta?.hideTabBar);
  }

  // 获取需要缓存的路由
  static getKeepAliveRoutes(): string[] {
    return ROUTE_TABLE.filter(r => r.meta?.keepAlive).map(r => r.name);
  }
}
```

---

## 六、Navigation导航栈

### 6.1 导航控制器（`entry/src/main/ets/navigation/NavigationController.ets`）

```typescript
// entry/src/main/ets/navigation/NavigationController.ets
// 龍魂 · Navigation导航控制器

import { router } from '@kit.ArkUI';
import { appState, AppState } from '../models/AppState';
import { RouterUtils, RouteConfig } from '../router/RouterConfig';
import { NavPathStack } from '@kit.ArkUI';

// === 导航控制器 ===
export class NavigationController {
  private navStack: NavPathStack = new NavPathStack();
  private routeCache: Map<string, any> = new Map();

  // 获取导航栈
  getStack(): NavPathStack {
    return this.navStack;
  }

  // === 压栈导航 ===
  push(name: string, params?: Record<string, any>): void {
    const route = RouterUtils.getRouteByName(name);
    if (!route) {
      console.error(`[龍魂] 路由不存在: ${name}`);
      return;
    }

    // 权限检查
    const access = RouterUtils.checkAccess(route.path, params);
    if (!access.allowed) {
      console.warn(`[龍魂] 路由拦截: ${access.reason}`);
      if (access.redirect) {
        this.pushByPath(access.redirect);
      }
      return;
    }

    // 参数验证
    if (params) {
      const validation = RouterUtils.validateParams(route, params);
      if (!validation.valid) {
        console.error(`[龍魂] 参数错误: ${validation.errors.join(', ')}`);
        return;
      }
    }

    // 记录导航历史
    appState.navHistory.push({
      name: route.name,
      route: route.path,
      params,
      timestamp: Date.now(),
      dnaSignature: this.signNav(route.name, params)
    });

    // 保存页面状态（如果当前页面有未保存数据）
    this.saveCurrentPageState();

    // 执行导航
    this.navStack.pushPathByName(name, params);

    console.info(`[龍魂] 导航: ${name} params=${JSON.stringify(params)}`);
  }

  // === 路径导航 ===
  pushByPath(path: string, params?: Record<string, any>): void {
    const route = RouterUtils.getRouteByPath(path);
    if (route) {
      this.push(route.name, params);
    } else {
      console.error(`[龍魂] 路径未找到: ${path}`);
    }
  }

  // === 替换导航 ===
  replace(name: string, params?: Record<string, any>): void {
    const route = RouterUtils.getRouteByName(name);
    if (!route) return;

    // 替换栈顶
    this.navStack.replacePathByName(name, params);

    // 更新历史
    appState.navHistory.pop();
    appState.navHistory.push({
      name: route.name,
      route: route.path,
      params,
      timestamp: Date.now(),
      dnaSignature: this.signNav(route.name, params)
    });

    console.info(`[龍魂] 替换导航: ${name}`);
  }

  // === 后退 ===
  back(result?: any): void {
    if (this.navStack.size() > 1) {
      // 恢复上一页状态
      const prevRecord = appState.navHistory.back();
      if (prevRecord) {
        this.restorePageState(prevRecord.route);
      }

      this.navStack.pop(result);
      console.info('[龍魂] 后退导航');
    } else {
      // 已经是首页，提示退出
      console.info('[龍魂] 已经是首页');
    }
  }

  // === 后退到指定页面 ===
  backTo(name: string): void {
    const index = this.findPathIndex(name);
    if (index !== -1) {
      this.navStack.popToName(name);

      // 同步历史
      while (appState.navHistory.currentIndex > index) {
        appState.navHistory.back();
      }

      console.info(`[龍魂] 后退到: ${name}`);
    }
  }

  // === 清除到指定页面 ===
  clearTo(name: string): void {
    this.navStack.removeByName(name);
    console.info(`[龍魂] 清除到: ${name}`);
  }

  // === 清除所有 ===
  clear(): void {
    this.navStack.clear();
    appState.navHistory.clear();
    console.info('[龍魂] 清除导航栈');
  }

  // === 获取当前路由 ===
  getCurrentRoute(): string | null {
    const destInfo = this.navStack.getDestinationInfos();
    if (destInfo.length > 0) {
      return destInfo[destInfo.length - 1].name;
    }
    return null;
  }

  // === 获取栈大小 ===
  getStackSize(): number {
    return this.navStack.size();
  }

  // === 能否后退 ===
  canGoBack(): boolean {
    return this.navStack.size() > 1;
  }

  // === 保存当前页面状态 ===
  private saveCurrentPageState(): void {
    const current = this.getCurrentRoute();
    if (current) {
      const route = RouterUtils.getRouteByName(current);
      if (route?.meta?.keepAlive) {
        // 触发页面保存状态事件
        AppStorage.setOrCreate('page_save_state', { route: current, timestamp: Date.now() });
      }
    }
  }

  // === 恢复页面状态 ===
  private restorePageState(route: string): void {
    const state = appState.getPageState(route);
    if (state.scrollPosition > 0) {
      AppStorage.setOrCreate('page_restore_scroll', state.scrollPosition);
    }
    if (state.isDirty) {
      AppStorage.setOrCreate('page_restore_form', state.formData);
    }
  }

  // === 查找页面索引 ===
  private findPathIndex(name: string): number {
    const destInfo = this.navStack.getDestinationInfos();
    return destInfo.findIndex(d => d.name === name);
  }

  // === 导航签名 ===
  private signNav(name: string, params?: Record<string, any>): string {
    const payload = `${name}-${JSON.stringify(params || {})}-${Date.now()}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }

  // === 处理返回键 ===
  handleBackPress(): boolean {
    if (this.canGoBack()) {
      this.back();
      return true; // 拦截返回键
    }
    return false; // 不拦截，退出应用
  }
}

// 全局导航控制器
export const navController = new NavigationController();
AppStorage.setOrCreate('navController', navController);
```

### 6.2 导航页面容器

```typescript
// entry/src/main/ets/pages/NavigationContainer.ets
// 龍魂 · Navigation容器页面

import { router } from '@kit.ArkUI';
import { navController } from '../navigation/NavigationController';
import { RouterUtils, ROUTE_TABLE } from '../router/RouterConfig';
import { appState } from '../models/AppState';

@Entry
@Component
struct NavigationContainer {
  @State private selectedIndex: number = 0;
  @State private navStack: NavPathStack = navController.getStack();

  // 页面映射
  @Builder
  pageMap(name: string, params: Record<string, any>) {
    if (name === 'Index') { IndexPage() }
    else if (name === 'Login') { LoginPage() }
    else if (name === 'ProjectList') { ProjectListPage() }
    else if (name === 'ProjectDetail') { ProjectDetailPage({ id: params?.id }) }
    else if (name === 'ProjectEdit') { ProjectEditPage({ id: params?.id }) }
    else if (name === 'MilestoneTimeline') { MilestoneTimelinePage() }
    else if (name === 'WeeklyReview') { WeeklyReviewPage() }
    else if (name === 'StampManagement') { StampManagementPage() }
    else if (name === 'Settings') { SettingsPage() }
    else if (name === 'Profile') { ProfilePage() }
    else { Text(`页面未找到: ${name}`).fontColor('#fff') }
  }

  // TabBar路由
  getTabRoutes() {
    return RouterUtils.getTabBarRoutes();
  }

  build() {
    Navigation(this.navStack) {
      // 主内容区
      this.pageMap(this.navStack.getDestinationInfos()[this.navStack.size() - 1]?.name || 'Index', {})
    }
    .hideTitleBar(true)
    .hideBackButton(false)
    .navDestination(this.pageMap)
    .mode(NavigationMode.Stack)
    .onAppear(() => {
      console.info('[龍魂] Navigation容器已挂载');
    })
    .onDisAppear(() => {
      console.info('[龍魂] Navigation容器已卸载');
    })
    // TabBar（底部导航）
    .toolbarConfiguration(this.ToolbarBuilder())
  }

  // TabBar构建
  @Builder
  ToolbarBuilder() {
    Row() {
      ForEach(this.getTabRoutes(), (route: RouteConfig, index: number) => {
        Column() {
          Text(route.icon || '📄')
            .fontSize(this.selectedIndex === index ? 24 : 20)
            .fontColor(this.selectedIndex === index ? '#c41e3a' : '#666')
          Text(route.title)
            .fontSize(11)
            .fontColor(this.selectedIndex === index ? '#c41e3a' : '#666')
            .margin({ top: 2 })
        }
        .width(`${100 / this.getTabRoutes().length}%`)
        .height('100%')
        .justifyContent(FlexAlign.Center)
        .onClick(() => {
          this.selectedIndex = index;
          navController.push(route.name);
        })
      })
    }
    .width('100%')
    .height(56)
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }
}
```

---

## 七、页面生命周期与状态管理

### 7.1 页面基类（`entry/src/main/ets/pages/BasePage.ets`）

```typescript
// entry/src/main/ets/pages/BasePage.ets
// 龍魂 · 页面基类

import { appState } from '../models/AppState';
import { navController } from '../navigation/NavigationController';
import { RouterUtils } from '../router/RouterConfig';

// === 页面生命周期接口 ===
export interface PageLifecycle {
  onPageShow(): void;
  onPageHide(): void;
  onBackPress(): boolean;
  onPageSaveState(): void;
  onPageRestoreState(): void;
}

// === 页面基类装饰器 ===
export function PageDecorator(routeName: string) {
  return function <T extends new (...args: any[]) => {}>(constructor: T) {
    return class extends constructor implements PageLifecycle {
      private routeName: string = routeName;
      private pageState: any = {};

      onPageShow(): void {
        console.info(`[龍魂] 页面显示: ${this.routeName}`);

        // 恢复页面状态
        this.onPageRestoreState();

        // 更新当前页面记录
        appState.savePageState(this.routeName, { pageName: this.routeName });

        // 调用子类方法
        if (super.onPageShow) super.onPageShow();
      }

      onPageHide(): void {
        console.info(`[龍魂] 页面隐藏: ${this.routeName}`);

        // 保存页面状态
        this.onPageSaveState();

        if (super.onPageHide) super.onPageHide();
      }

      onBackPress(): boolean {
        console.info(`[龍魂] 页面返回: ${this.routeName}`);

        // 检查是否有未保存数据
        const state = appState.getPageState(this.routeName);
        if (state.isDirty) {
          // 提示保存
          AppStorage.setOrCreate('page_confirm_save', {
            route: this.routeName,
            timestamp: Date.now()
          });
          return true; // 拦截返回
        }

        return navController.handleBackPress();
      }

      onPageSaveState(): void {
        // 保存滚动位置
        // 保存表单数据
        // 由子类实现
        if (super.onPageSaveState) super.onPageSaveState();
      }

      onPageRestoreState(): void {
        // 恢复滚动位置
        const scrollPos = AppStorage.get<number>('page_restore_scroll');
        if (scrollPos) {
          // 恢复滚动
          AppStorage.delete('page_restore_scroll');
        }

        // 恢复表单数据
        const formData = AppStorage.get<Record<string, any>>('page_restore_form');
        if (formData) {
          // 恢复表单
          AppStorage.delete('page_restore_form');
        }

        if (super.onPageRestoreState) super.onPageRestoreState();
      }

      // 导航方法
      navigateTo(name: string, params?: Record<string, any>): void {
        navController.push(name, params);
      }

      goBack(result?: any): void {
        navController.back(result);
      }

      // 获取当前用户
      getCurrentUser() {
        return appState.currentUser;
      }

      // 检查权限
      hasPermission(permission: string): boolean {
        return appState.currentUser.hasPermission(permission);
      }
    };
  };
}
```

### 7.2 具体页面示例

```typescript
// entry/src/main/ets/pages/ProjectDetailPage.ets
// 龍魂 · 项目详情页（带生命周期）

import { navController } from '../navigation/NavigationController';
import { appState } from '../models/AppState';
import { Project } from '../models/ProjectModel';

@Component
struct ProjectDetailPage {
  @Prop id: string;
  @State private project: Project | null = null;
  @State private scrollPosition: number = 0;
  @State private isLoading: boolean = true;

  // 页面显示
  onPageShow() {
    console.info(`[龍魂] 项目详情页显示: ${this.id}`);
    this.loadProject();

    // 恢复滚动位置
    const state = appState.getPageState(`/project/detail`);
    if (state.scrollPosition > 0) {
      // 恢复滚动
    }
  }

  // 页面隐藏
  onPageHide() {
    console.info('[龍魂] 项目详情页隐藏');

    // 保存滚动位置
    appState.savePageState('/project/detail', {
      scrollPosition: this.scrollPosition
    });
  }

  // 返回键处理
  onBackPress(): boolean {
    // 检查是否有未保存的编辑
    if (this.project?.isDirty) {
      // 显示确认对话框
      return true; // 拦截
    }
    return false; // 不拦截
  }

  // 加载项目
  loadProject(): void {
    this.isLoading = true;
    // 从数据库加载
    // ProjectDatabase.getById(this.id).then(project => {
    //   this.project = project;
    //   this.isLoading = false;
    // });
  }

  build() {
    Column() {
      // 导航栏
      this.NavBarBuilder()

      if (this.isLoading) {
        // 加载中
        LoadingProgress()
          .width(48)
          .height(48)
          .color('#c41e3a')
      } else if (this.project) {
        // 项目详情
        Scroll() {
          Column() {
            this.ProjectHeaderBuilder()
            this.ProjectStatsBuilder()
            this.MilestoneListBuilder()
            this.ActionButtonsBuilder()
          }
          .width('100%')
          .padding(16)
        }
        .width('100%')
        .layoutWeight(1)
        .scrollBar(BarState.Auto)
        .onScroll((x, y) => {
          this.scrollPosition = y;
        })
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder
  NavBarBuilder() {
    Row() {
      Button() { Text('‹').fontSize(24).fontColor('#fff') }
      .type(ButtonType.Circle).backgroundColor('#1a1a1a').width(40).height(40)
      .onClick(() => { navController.back(); })

      Text(this.project?.name || '项目详情')
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
        .layoutWeight(1)
        .textAlign(TextAlign.Center)

      Button() { Text('✎').fontSize(18).fontColor('#fff') }
      .type(ButtonType.Circle).backgroundColor('#1a1a1a').width(40).height(40)
      .onClick(() => {
        navController.push('ProjectEdit', { id: this.id });
      })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  ProjectHeaderBuilder() {
    Column() {
      Text(this.project?.name || '')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')

      Text(this.project?.projectNo || '')
        .fontSize(14)
        .fontColor('#888')
        .margin({ top: 4 })

      Row() {
        Text(this.project?.status || '')
          .fontSize(12)
          .fontColor('#fff')
          .backgroundColor('#333')
          .borderRadius(4)
          .padding({ left: 8, right: 8, top: 2, bottom: 2 })

        Text(`${this.project?.getProgress() || 0}%`)
          .fontSize(12)
          .fontColor('#00ff00')
          .margin({ left: 8 })
      }
      .margin({ top: 8 })
    }
    .width('100%')
    .alignItems(HorizontalAlign.Start)
    .margin({ bottom: 16 })
  }

  @Builder
  ProjectStatsBuilder() {
    Row() {
      this.StatItem('计划工时', `${this.project?.totalPlannedHours || 0}h`)
      this.StatItem('实际工时', `${this.project?.totalActualHours || 0}h`)
      this.StatItem('里程碑', `${this.project?.milestones.length || 0}个`)
      this.StatItem('风险', `${this.project?.risks.length || 0}项`)
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .margin({ bottom: 16 })
  }

  @Builder
  StatItem(label: string, value: string) {
    Column() {
      Text(value).fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff')
      Text(label).fontSize(11).fontColor('#666').margin({ top: 4 })
    }
    .width('25%')
    .alignItems(HorizontalAlign.Center)
  }

  @Builder
  MilestoneListBuilder() {
    Column() {
      Text('里程碑')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
        .margin({ bottom: 12 })

      // 里程碑列表
      // ForEach(this.project?.milestones || [], (milestone) => { ... })
    }
    .width('100%')
    .margin({ bottom: 16 })
  }

  @Builder
  ActionButtonsBuilder() {
    Row() {
      Button('查看甘特图')
        .fontSize(14)
        .fontColor('#fff')
        .backgroundColor('#333')
        .borderRadius(8)
        .padding({ left: 16, right: 16 })
        .onClick(() => {
          navController.push('MilestoneTimeline', { projectId: this.id });
        })

      Button('编辑项目')
        .fontSize(14)
        .fontColor('#fff')
        .backgroundColor('#c41e3a')
        .borderRadius(8)
        .padding({ left: 16, right: 16 })
        .onClick(() => {
          navController.push('ProjectEdit', { id: this.id });
        })
    }
    .width('100%')
    .justifyContent(FlexAlign.SpaceAround)
    .margin({ top: 16 })
  }
}
```

---

## 八、组件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| 基础模型 | `entry/src/main/ets/models/BaseModel.ets` | BaseModel/UserModel/PageStateModel/NavigationHistoryModel/RouteGuardModel |
| 应用状态 | `entry/src/main/ets/models/AppState.ets` | AppState/AppSettings |
| EntryAbility | `entry/src/main/ets/entryability/EntryAbility.ets` | UIAbility生命周期 |
| 路由配置 | `entry/src/main/ets/router/RouterConfig.ets` | RouteConfig/RouterUtils/ROUTE_TABLE |
| 导航控制器 | `entry/src/main/ets/navigation/NavigationController.ets` | NavigationController/NavPathStack |
| 导航容器 | `entry/src/main/ets/pages/NavigationContainer.ets` | Navigation容器+TabBar |
| 页面基类 | `entry/src/main/ets/pages/BasePage.ets` | PageLifecycle/PageDecorator |
| 项目详情 | `entry/src/main/ets/pages/ProjectDetailPage.ets` | 完整页面示例 |
| 数据库 | `entry/src/main/ets/database/AppDatabase.ets` | 应用数据持久化 |

---

## 九、鸿蒙特性使用

| 特性 | 用途 | API |
|------|------|-----|
| UIAbility | 应用生命周期 | `UIAbility` `onCreate` `onDestroy` |
| WindowStage | 窗口管理 | `windowStage` `loadContent` |
| Router | 页面跳转 | `router.pushUrl` `router.back` |
| Navigation | 导航栈管理 | `Navigation` `NavPathStack` `NavDestination` |
| AppStorage | 全局状态 | `AppStorage.setOrCreate` `AppStorage.get` |
| LocalStorage | 局部状态 | `LocalStorage` |
| PersistentStorage | 持久化状态 | `PersistentStorage` |
| 生命周期 | 页面回调 | `onPageShow` `onPageHide` `onBackPress` |
| 事件总线 | 组件通信 | `EventHub` `emitter` |
| 后台任务 | 状态保存 | `workScheduler` |
| 国密算法 | 数据签名 | `cryptoFramework` SM2/SM3 |

---

## 十、生命周期流程图

```
Ability生命周期:
onCreate → onWindowStageCreate → onForeground → onBackground → onWindowStageDestroy → onDestroy

页面生命周期:
构造函数 → aboutToAppear → onPageShow → onPageHide → aboutToDisappear → 析构

导航生命周期:
push → 目标页aboutToAppear → 目标页onPageShow → 当前页onPageHide → 可选:back → 当前页onPageShow

状态保存:
onPageHide → savePageState → AppStorage → onBackground → persist → 本地存储

状态恢复:
onCreate → load → AppStorage → onPageShow → restorePageState → 恢复滚动/表单
```

---

## 十一、路由守卫流程

| 步骤 | 动作 | 失败处理 |
|------|------|----------|
| 1 | 解析目标路由 | 404错误页 |
| 2 | 参数验证 | 参数错误提示 |
| 3 | 权限检查（auth） | 跳转登录页 |
| 4 | 角色检查（role） | 无权限提示页 |
| 5 | 权限检查（permission） | 无权限提示页 |
| 6 | 参数检查（param） | 缺少参数提示 |
| 7 | 自定义验证（custom） | 自定义提示 |
| 8 | 执行导航 | - |
| 9 | 记录历史 | - |
| 10 | 保存上一页状态 | - |

---

## 十二、龍魂标识

| 位置 | 内容 |
|------|------|
| 应用名称 | 龍魂原生开发 |
| 标题栏 | 🐉 龍魂原生开发 |
| 底部标识 | UID:9622 |
| 数据签名 | SM3-哈希 |
| DNA | ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ |

---

🐉 **龍魂 · 鸿蒙原生开发：模型与UIAbility页面路由与Navigation导航详解 交付完成**

> DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️  
> UID: 9622  
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
> 时间: 2026-07-14  
> 模块: 9核心文件  
> 特性: 数据模型层 · UIAbility生命周期 · 路由配置中心 · Navigation导航栈 · 页面生命周期 · 路由守卫 · 状态持久化 · 国密签名
