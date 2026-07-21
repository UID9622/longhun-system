// entry/src/main/ets/pages/BasePage.ets
// 龍魂 · 页面基类

import { appState } from '../models/AppState';
import { navController } from '../navigation/NavigationController';

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
  return function <T extends new (...args: Object[]) => PageLifecycle>(constructor: T) {
    return class extends constructor implements PageLifecycle {
      private _routeName: string = routeName;
      private _pageState: Record<string, Object> = {};

      onPageShow(): void {
        console.info(`[龍魂] 页面显示: ${this._routeName}`);

        // 恢复页面状态
        this.onPageRestoreState();

        // 更新当前页面记录
        appState.savePageState(this._routeName, { pageName: this._routeName });

        // 调用子类方法
        const proto = Object.getPrototypeOf(this);
        if (proto.onPageShow) {
          proto.onPageShow.call(this);
        }
      }

      onPageHide(): void {
        console.info(`[龍魂] 页面隐藏: ${this._routeName}`);

        // 保存页面状态
        this.onPageSaveState();

        const proto = Object.getPrototypeOf(this);
        if (proto.onPageHide) {
          proto.onPageHide.call(this);
        }
      }

      onBackPress(): boolean {
        console.info(`[龍魂] 页面返回: ${this._routeName}`);

        // 检查是否有未保存数据
        const state = appState.getPageState(this._routeName);
        if (state.isDirty) {
          // 提示保存
          AppStorage.setOrCreate('page_confirm_save', {
            route: this._routeName,
            timestamp: Date.now()
          });
          return true; // 拦截返回
        }

        return navController.handleBackPress();
      }

      onPageSaveState(): void {
        const proto = Object.getPrototypeOf(this);
        if (proto.onPageSaveState) {
          proto.onPageSaveState.call(this);
        }
      }

      onPageRestoreState(): void {
        // 恢复滚动位置
        const scrollPos = AppStorage.get<number>('page_restore_scroll');
        if (scrollPos) {
          AppStorage.delete('page_restore_scroll');
        }

        // 恢复表单数据
        const formData = AppStorage.get<Record<string, Object>>('page_restore_form');
        if (formData) {
          AppStorage.delete('page_restore_form');
        }

        const proto = Object.getPrototypeOf(this);
        if (proto.onPageRestoreState) {
          proto.onPageRestoreState.call(this);
        }
      }

      // 导航方法
      navigateTo(name: string, params?: Record<string, Object>): void {
        navController.push(name, params);
      }

      goBack(result?: Object): void {
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
