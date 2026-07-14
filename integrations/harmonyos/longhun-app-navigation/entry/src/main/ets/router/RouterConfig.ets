// entry/src/main/ets/router/RouterConfig.ets
// 龍魂 · 路由配置中心

import { appState } from '../models/AppState';

// === 路由表 ===
export interface RouteConfig {
  name: string;
  path: string;
  component: string;
  title: string;
  icon?: string;
  guards?: string[];
  params?: ParamConfig[];
  meta?: RouteMeta;
}

export interface ParamConfig {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'object';
  required: boolean;
  default?: Object;
}

export interface RouteMeta {
  keepAlive?: boolean;
  hideTabBar?: boolean;
  hideNavBar?: boolean;
  transition?: string;
  depth?: number;
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
  static validateParams(route: RouteConfig, params: Record<string, Object>): ParamValidationResult {
    const errors: string[] = [];

    if (!route.params) {
      return { valid: true, errors };
    }

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
  static buildUrl(path: string, params?: Record<string, Object>): string {
    if (!params) {
      return path;
    }

    const query = Object.entries(params)
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
      .join('&');

    return query ? `${path}?${query}` : path;
  }

  // 解析URL
  static parseUrl(url: string): ParsedUrl {
    const questionIdx = url.indexOf('?');
    const path = questionIdx >= 0 ? url.substring(0, questionIdx) : url;
    const params: Record<string, string> = {};

    if (questionIdx >= 0) {
      const query = url.substring(questionIdx + 1);
      query.split('&').forEach(pair => {
        const eqIdx = pair.indexOf('=');
        if (eqIdx >= 0) {
          const k = decodeURIComponent(pair.substring(0, eqIdx));
          const v = decodeURIComponent(pair.substring(eqIdx + 1));
          if (k) {
            params[k] = v || '';
          }
        }
      });
    }

    return { path, params };
  }

  // 检查权限
  static checkAccess(path: string, params: Record<string, Object> = {}): RouteAccessResult {
    const result = appState.checkRoute(path, params);
    return {
      allowed: result.allowed,
      redirect: result.redirect,
      reason: result.reason
    };
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

export interface ParamValidationResult {
  valid: boolean;
  errors: string[];
}

export interface ParsedUrl {
  path: string;
  params: Record<string, string>;
}

export interface RouteAccessResult {
  allowed: boolean;
  redirect?: string;
  reason?: string;
}
