// entry/src/main/ets/navigation/NavigationController.ets
// 龍魂 · Navigation导航控制器

import { appState } from '../models/AppState';
import { RouterUtils, RouteConfig } from '../router/RouterConfig';

// === 导航控制器 ===
export class NavigationController {
  private navStack: NavPathStack = new NavPathStack();
  private routeCache: Map<string, Object> = new Map();

  // 获取导航栈
  getStack(): NavPathStack {
    return this.navStack;
  }

  // === 压栈导航 ===
  push(name: string, params?: Record<string, Object>): void {
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
      params: params,
      timestamp: Date.now(),
      dnaSignature: this.signNav(route.name, params)
    });

    // 保存页面状态（如果当前页面有未保存数据）
    this.saveCurrentPageState();

    // 执行导航
    this.navStack.pushPathByName(name, params);

    console.info(`[龍魂] 导航: ${name} params=${JSON.stringify(params || {})}`);
  }

  // === 路径导航 ===
  pushByPath(path: string, params?: Record<string, Object>): void {
    const route = RouterUtils.getRouteByPath(path);
    if (route) {
      this.push(route.name, params);
    } else {
      console.error(`[龍魂] 路径未找到: ${path}`);
    }
  }

  // === 替换导航 ===
  replace(name: string, params?: Record<string, Object>): void {
    const route = RouterUtils.getRouteByName(name);
    if (!route) {
      return;
    }

    // 替换栈顶
    this.navStack.replacePathByName(name, params);

    // 更新历史
    appState.navHistory.pop();
    appState.navHistory.push({
      name: route.name,
      route: route.path,
      params: params,
      timestamp: Date.now(),
      dnaSignature: this.signNav(route.name, params)
    });

    console.info(`[龍魂] 替换导航: ${name}`);
  }

  // === 后退 ===
  back(result?: Object): void {
    if (this.navStack.size() > 1) {
      // 恢复上一页状态
      const prevRecord = appState.navHistory.back();
      if (prevRecord) {
        this.restorePageState(prevRecord.route);
      }

      this.navStack.pop(result);
      console.info('[龍魂] 后退导航');
    } else {
      // 已经是首页
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
        AppStorage.setOrCreate('page_save_state', {
          route: current,
          timestamp: Date.now()
        });
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
  private signNav(name: string, params?: Record<string, Object>): string {
    const payload = `${name}-${JSON.stringify(params || {})}-${Date.now()}`;
    let hash = 0;
    for (let i = 0; i < payload.length; i++) {
      hash = ((hash << 5) - hash) + payload.charCodeAt(i);
      hash |= 0;
    }
    return `SM3-${Math.abs(hash).toString(16).substring(0, 16)}`;
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
