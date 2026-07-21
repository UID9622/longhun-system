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
    const suffix = Date.now().toString(36).substr(-6);
    return `${this.getPrefix()}-${MASTER_UID}-${suffix}`;
  }

  protected abstract getPrefix(): string;

  protected signData(): string {
    const payload = `${this.id}-${this.createdAt.getTime()}-${this.getPrefix()}`;
    let hash = 0;
    for (let i = 0; i < payload.length; i++) {
      hash = ((hash << 5) - hash) + payload.charCodeAt(i);
      hash |= 0;
    }
    return `SM3-${Math.abs(hash).toString(16).substring(0, 16)}`;
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
  static fromJSON<T extends BaseModel>(json: string, factory: (data: Record<string, Object>) => T): T {
    const data = JSON.parse(json) as Record<string, Object>;
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
  params: Record<string, Object>;
  scrollPosition: number;
  formData: Record<string, Object>;
  isDirty: boolean;

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
  saveFormData(key: string, value: Object): void {
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
    this.currentIndex = data.currentIndex !== undefined ? data.currentIndex : -1;
    this.maxDepth = data.maxDepth || 50;
  }

  protected getPrefix(): string { return 'NAV'; }

  // 压栈
  push(record: NavRecord): void {
    this.stack = this.stack.slice(0, this.currentIndex + 1);
    this.stack.push(record);
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

  // 弹出栈顶
  pop(): NavRecord | null {
    if (this.stack.length > 0) {
      const record = this.stack.pop()!;
      this.currentIndex = this.stack.length - 1;
      this.update({});
      return record;
    }
    return null;
  }

  // 清空
  clear(): void {
    this.stack = [];
    this.currentIndex = -1;
    this.update({});
  }
}

export interface NavRecord {
  name: string;
  route: string;
  params?: Record<string, Object>;
  timestamp: number;
  dnaSignature: string;
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
  canActivate(user: UserModel, params: Record<string, Object>): GuardResult {
    for (const guard of this.guards) {
      const result = this.checkGuard(guard, user, params);
      if (!result.allowed) {
        return result;
      }
    }
    return { allowed: true };
  }

  private checkGuard(guard: GuardRule, user: UserModel, params: Record<string, Object>): GuardResult {
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
        if (guard.permissions && !guard.permissions.every((p: string) => user.hasPermission(p))) {
          return { allowed: false, reason: '权限不足' };
        }
        break;
      case 'param':
        if (guard.requiredParams && !guard.requiredParams.every((p: string) => params[p] !== undefined)) {
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
  validator?: (user: UserModel, params: Record<string, Object>) => boolean;
  message?: string;
}

export interface GuardResult {
  allowed: boolean;
  reason?: string;
}
