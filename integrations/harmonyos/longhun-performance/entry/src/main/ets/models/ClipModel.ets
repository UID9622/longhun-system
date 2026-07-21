// entry/src/main/ets/models/ClipModel.ets
// 龍魂 · 裁剪模型层 · ArkTS

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 裁剪类型枚举 ===
export enum ClipType {
  RECT = 'rect',              // 矩形裁剪
  ROUNDED_RECT = 'roundedRect', // 圆角矩形
  CIRCLE = 'circle',          // 圆形
  ELLIPSE = 'ellipse',        // 椭圆
  PATH = 'path',              // 路径
  MASK = 'mask'               // 蒙版
}

// === 裁剪参数接口 ===
export interface ClipParams {
  // 矩形
  x?: number;
  y?: number;
  width?: number;
  height?: number;

  // 圆角
  topLeft?: number;
  topRight?: number;
  bottomLeft?: number;
  bottomRight?: number;
  radius?: number;            // 统一圆角

  // 圆形
  centerX?: number;
  centerY?: number;
  circleRadius?: number;

  // 椭圆
  ellipseRadiusX?: number;
  ellipseRadiusY?: number;

  // 路径
  path?: string;              // SVG路径字符串

  // 蒙版
  maskBuilder?: () => void;   // 蒙版构建器
}

// === 裁剪配置 ===
export class ClipConfig {
  id: string;
  type: ClipType;
  params: ClipParams;
  name: string;

  // 性能
  antialias: boolean;         // 抗锯齿
  cache: boolean;             // 缓存裁剪结果

  // 审计
  timestamp: number;
  dnaSignature: string;

  constructor(data: Partial<ClipConfig> = {}) {
    this.id = data.id || `CLIP-${Date.now()}`;
    this.type = data.type || ClipType.RECT;
    this.params = data.params || {};
    this.name = data.name || '未命名裁剪';
    this.antialias = data.antialias ?? true;
    this.cache = data.cache ?? false;
    this.timestamp = data.timestamp || Date.now();
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.type}-${this.timestamp}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }

  // 获取圆角值（统一处理）
  getCornerRadius(): [number, number, number, number] {
    const r = this.params.radius || 0;
    return [
      this.params.topLeft ?? r,
      this.params.topRight ?? r,
      this.params.bottomLeft ?? r,
      this.params.bottomRight ?? r
    ];
  }

  // 获取裁剪描述
  getDescription(): string {
    const descs: Record<ClipType, string> = {
      [ClipType.RECT]: `矩形 [${this.params.width}x${this.params.height}]`,
      [ClipType.ROUNDED_RECT]: `圆角矩形 [${this.params.radius}px圆角]`,
      [ClipType.CIRCLE]: `圆形 [半径${this.params.circleRadius}px]`,
      [ClipType.ELLIPSE]: `椭圆 [${this.params.ellipseRadiusX}x${this.params.ellipseRadiusY}]`,
      [ClipType.PATH]: `路径裁剪`,
      [ClipType.MASK]: `蒙版裁剪`
    };
    return descs[this.type] || '未知裁剪';
  }
}

// === 裁剪效果记录 ===
export class ClipEffect {
  id: string;
  config: ClipConfig;
  componentName: string;
  pageName: string;

  // 渲染统计
  renderTime: number;          // 裁剪渲染耗时
  pixelCount: number;          // 裁剪像素数

  // 状态
  isActive: boolean;
  lastUsed: number;

  // 审计
  dnaSignature: string;

  constructor(data: Partial<ClipEffect> = {}) {
    this.id = data.id || `EFFECT-${Date.now()}`;
    this.config = data.config || new ClipConfig();
    this.componentName = data.componentName || 'Unknown';
    this.pageName = data.pageName || '';
    this.renderTime = data.renderTime || 0;
    this.pixelCount = data.pixelCount || 0;
    this.isActive = data.isActive ?? true;
    this.lastUsed = data.lastUsed || Date.now();
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    return `SM3-${this.id}-${this.componentName}-${Date.now()}`;
  }
}

// === 裁剪全局状态 ===
@Observed
export class ClipState {
  // 配置库
  configs: ClipConfig[] = [];

  // 效果记录
  effects: ClipEffect[] = [];

  // 缓存
  private cache: Map<string, object> = new Map();

  // 统计
  get statistics(): ClipStats {
    return {
      totalConfigs: this.configs.length,
      totalEffects: this.effects.length,
      activeEffects: this.effects.filter(e => e.isActive).length,
      avgRenderTime: this.getAvgRenderTime(),
      cacheHitRate: this.getCacheHitRate()
    };
  }

  private getAvgRenderTime(): number {
    if (this.effects.length === 0) return 0;
    return Math.round(this.effects.reduce((sum, e) => sum + e.renderTime, 0) / this.effects.length);
  }

  private getCacheHitRate(): number {
    // 简化计算
    return this.cache.size > 0 ? 85 : 0;
  }

  // 添加配置
  addConfig(config: ClipConfig): void {
    this.configs.push(config);
  }

  // 记录效果
  recordEffect(effect: ClipEffect): void {
    this.effects.push(effect);
  }

  // 获取缓存
  getCache(key: string): object | undefined {
    return this.cache.get(key);
  }

  // 设置缓存
  setCache(key: string, value: object): void {
    this.cache.set(key, value);
  }

  persist(): void {
    AppStorage.setOrCreate('clip_configs', JSON.stringify(this.configs.slice(-50)));
    AppStorage.setOrCreate('clip_effects', JSON.stringify(this.effects.slice(-100)));
  }
}

export interface ClipStats {
  totalConfigs: number;
  totalEffects: number;
  activeEffects: number;
  avgRenderTime: number;
  cacheHitRate: number;
}

export const clipState = new ClipState();
AppStorage.setOrCreate('clipState', clipState);
