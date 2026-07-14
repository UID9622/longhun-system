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
        this.currentUser = UserModel.fromJSON(userData, (d: Record<string, Object>) => new UserModel(d));
      } catch (e) {
        console.error('[龍魂] 加载用户失败', JSON.stringify(e));
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
      this.pageStates.set(route, new PageStateModel({ route: route }));
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
  checkRoute(route: string, params: Record<string, Object> = {}): RouteCheckResult {
    const guard = this.routeGuards.get(route);
    if (!guard) {
      return { allowed: true };
    }

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
    // 管理后台
    this.routeGuards.set('/admin', new RouteGuardModel({
      route: '/admin',
      guards: [
        { type: 'auth' },
        { type: 'role', roles: ['admin'] }
      ],
      fallbackRoute: '/login'
    }));

    // 项目编辑
    this.routeGuards.set('/project/edit', new RouteGuardModel({
      route: '/project/edit',
      guards: [
        { type: 'auth' },
        { type: 'permission', permissions: ['write'] },
        { type: 'param', requiredParams: ['id'] }
      ],
      fallbackRoute: '/login'
    }));

    // 设置页
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
        const parsed = JSON.parse(settings) as AppSettings;
        this.settings = { ...this.settings, ...parsed };
      } catch (e) {
        console.error('[龍魂] 加载设置失败', JSON.stringify(e));
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
        const data = JSON.parse(history) as Record<string, Object>;
        this.navHistory = new NavigationHistoryModel(data);
      } catch (e) {
        console.error('[龍魂] 加载导航历史失败', JSON.stringify(e));
      }
    }
  }

  // 保存导航历史
  saveNavHistory(): void {
    AppStorage.setOrCreate('nav_history', this.navHistory.toJSON());
  }

  // 统一持久化
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

export interface RouteCheckResult {
  allowed: boolean;
  redirect?: string;
  reason?: string;
}

// 全局状态单例
export const appState = new AppState();
AppStorage.setOrCreate('appState', appState);
