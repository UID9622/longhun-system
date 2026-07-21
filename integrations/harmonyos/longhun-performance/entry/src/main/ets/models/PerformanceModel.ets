// entry/src/main/ets/models/PerformanceModel.ets
// 龍魂 · 性能模型层 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 性能指标类型 ===
export enum MetricType {
  FIRST_FRAME = 'first_frame',
  LAYOUT_TIME = 'layout_time',
  RENDER_TIME = 'render_time',
  PAINT_TIME = 'paint_time',
  COMPOSITE_TIME = 'composite_time',
  FPS = 'fps',
  MEMORY = 'memory',
  CPU = 'cpu',
  NETWORK = 'network',
  STORAGE = 'storage'
}

// === 优化策略 ===
export enum OptimizeStrategy {
  LAZY_LOAD = 'lazy_load',
  PRELOAD = 'preload',
  CACHE = 'cache',
  ASYNC = 'async',
  REUSE = 'reuse',
  COMPRESS = 'compress',
  SPLIT = 'split',
  POOL = 'pool'
}

// === 性能阈值 ===
export enum PerformanceThreshold {
  EXCELLENT = 'excellent',
  GOOD = 'good',
  FAIR = 'fair',
  POOR = 'poor',
  CRITICAL = 'critical'
}

// === 性能指标 ===
export class PerformanceMetric {
  id: string;
  type: MetricType;
  name: string;
  value: number;
  unit: string;
  timestamp: number;
  threshold: PerformanceThreshold;
  pageName: string;
  componentName?: string;
  dnaSignature: string;

  constructor(data: Partial<PerformanceMetric> = {}) {
    this.id = data.id || `METRIC-${Date.now()}`;
    this.type = data.type || MetricType.FIRST_FRAME;
    this.name = data.name || '未命名指标';
    this.value = data.value || 0;
    this.unit = data.unit || 'ms';
    this.timestamp = data.timestamp || Date.now();
    this.threshold = data.threshold || this.evaluateThreshold(data.type || MetricType.FIRST_FRAME, data.value || 0);
    this.pageName = data.pageName || '';
    this.componentName = data.componentName;
    this.dnaSignature = this.signData();
  }

  private evaluateThreshold(type: MetricType, value: number): PerformanceThreshold {
    const thresholds: Record<string, number[]> = {
      [MetricType.FIRST_FRAME]: [100, 300, 500, 1000],
      [MetricType.LAYOUT_TIME]: [50, 100, 200, 500],
      [MetricType.RENDER_TIME]: [16, 33, 50, 100],
      [MetricType.PAINT_TIME]: [16, 33, 50, 100],
      [MetricType.COMPOSITE_TIME]: [16, 33, 50, 100],
      [MetricType.FPS]: [55, 45, 30, 15],
      [MetricType.MEMORY]: [50, 100, 200, 500],
      [MetricType.CPU]: [30, 50, 70, 90],
      [MetricType.NETWORK]: [100, 300, 500, 1000],
      [MetricType.STORAGE]: [50, 100, 200, 500]
    };

    const limits = thresholds[type] || [100, 300, 500, 1000];

    if (type === MetricType.FPS) {
      if (value >= limits[0]) return PerformanceThreshold.EXCELLENT;
      if (value >= limits[1]) return PerformanceThreshold.GOOD;
      if (value >= limits[2]) return PerformanceThreshold.FAIR;
      if (value >= limits[3]) return PerformanceThreshold.POOR;
      return PerformanceThreshold.CRITICAL;
    }

    if (value < limits[0]) return PerformanceThreshold.EXCELLENT;
    if (value < limits[1]) return PerformanceThreshold.GOOD;
    if (value < limits[2]) return PerformanceThreshold.FAIR;
    if (value < limits[3]) return PerformanceThreshold.POOR;
    return PerformanceThreshold.CRITICAL;
  }

  private signData(): string {
    const payload = `${this.id}-${this.type}-${this.value}-${this.timestamp}`;
    return `SM3-${this.hashString(payload)}`;
  }

  private hashString(s: string): string {
    let hash = 0;
    for (let i = 0; i < s.length; i++) {
      const ch = s.charCodeAt(i);
      hash = ((hash << 5) - hash) + ch;
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).substring(0, 16);
  }

  getThresholdColor(): string {
    switch (this.threshold) {
      case PerformanceThreshold.EXCELLENT: return '#00ff00';
      case PerformanceThreshold.GOOD: return '#88ff00';
      case PerformanceThreshold.FAIR: return '#ffcc00';
      case PerformanceThreshold.POOR: return '#ff6600';
      case PerformanceThreshold.CRITICAL: return '#ff0000';
      default: return '#666';
    }
  }

  getThresholdLabel(): string {
    const labels: Record<string, string> = {
      [PerformanceThreshold.EXCELLENT]: '优秀',
      [PerformanceThreshold.GOOD]: '良好',
      [PerformanceThreshold.FAIR]: '一般',
      [PerformanceThreshold.POOR]: '较差',
      [PerformanceThreshold.CRITICAL]: '严重'
    };
    return labels[this.threshold] || '未知';
  }
}

// === 优化建议接口 ===
export interface OptimizationSuggestion {
  id: string;
  title: string;
  description: string;
  strategy: OptimizeStrategy;
  priority: 'low' | 'medium' | 'high' | 'critical';
  impact: string;
}

// === 性能报告 ===
export class PerformanceReport {
  id: string;
  pageName: string;
  metrics: PerformanceMetric[];
  totalMetrics: number;
  excellentCount: number;
  goodCount: number;
  fairCount: number;
  poorCount: number;
  criticalCount: number;
  firstFrameTime: number;
  layoutCalcTime: number;
  renderTime: number;
  suggestions: OptimizationSuggestion[];
  timestamp: Date;
  dnaSignature: string;

  constructor(data: Partial<PerformanceReport> = {}) {
    this.id = data.id || `REPORT-${Date.now()}`;
    this.pageName = data.pageName || '';
    this.metrics = data.metrics || [];

    this.totalMetrics = this.metrics.length;
    this.excellentCount = this.metrics.filter(m => m.threshold === PerformanceThreshold.EXCELLENT).length;
    this.goodCount = this.metrics.filter(m => m.threshold === PerformanceThreshold.GOOD).length;
    this.fairCount = this.metrics.filter(m => m.threshold === PerformanceThreshold.FAIR).length;
    this.poorCount = this.metrics.filter(m => m.threshold === PerformanceThreshold.POOR).length;
    this.criticalCount = this.metrics.filter(m => m.threshold === PerformanceThreshold.CRITICAL).length;

    this.firstFrameTime = data.firstFrameTime || 0;
    this.layoutCalcTime = data.layoutCalcTime || 0;
    this.renderTime = data.renderTime || 0;

    this.suggestions = data.suggestions || this.generateSuggestions();
    this.timestamp = data.timestamp || new Date();
    this.dnaSignature = this.signData();
  }

  private generateSuggestions(): OptimizationSuggestion[] {
    const suggestions: OptimizationSuggestion[] = [];

    if (this.firstFrameTime > 300) {
      suggestions.push({
        id: `SUG-${Date.now()}-1`,
        title: '首帧时间过长',
        description: `当前首帧时间 ${this.firstFrameTime}ms，建议优化至 300ms 以内`,
        strategy: OptimizeStrategy.LAZY_LOAD,
        priority: 'high',
        impact: '减少首帧布局计算量，使用 LazyForEach 替代 ForEach'
      });
    }

    if (this.layoutCalcTime > 100) {
      suggestions.push({
        id: `SUG-${Date.now()}-2`,
        title: '布局计算耗时',
        description: `布局计算耗时 ${this.layoutCalcTime}ms，建议简化布局层级`,
        strategy: OptimizeStrategy.SPLIT,
        priority: 'high',
        impact: '减少嵌套层级，使用扁平化布局'
      });
    }

    if (this.criticalCount > 0) {
      suggestions.push({
        id: `SUG-${Date.now()}-3`,
        title: '存在严重性能问题',
        description: `发现 ${this.criticalCount} 项严重性能指标`,
        strategy: OptimizeStrategy.ASYNC,
        priority: 'critical',
        impact: '使用异步加载，避免阻塞主线程'
      });
    }

    return suggestions;
  }

  private signData(): string {
    const payload = `${this.id}-${this.pageName}-${this.firstFrameTime}-${this.timestamp.getTime()}`;
    const hash = payload.split('').reduce((a: number, b: string) => a + b.charCodeAt(0), 0);
    return `SM3-${hash.toString(16).substring(0, 16)}`;
  }

  getScore(): number {
    if (this.totalMetrics === 0) return 100;
    const weights: Record<string, number> = {
      [PerformanceThreshold.EXCELLENT]: 100,
      [PerformanceThreshold.GOOD]: 80,
      [PerformanceThreshold.FAIR]: 60,
      [PerformanceThreshold.POOR]: 40,
      [PerformanceThreshold.CRITICAL]: 20
    };
    const totalScore = this.metrics.reduce((sum, m) => sum + (weights[m.threshold] || 0), 0);
    return Math.round(totalScore / this.totalMetrics);
  }

  getScoreColor(): string {
    const score = this.getScore();
    if (score >= 90) return '#00ff00';
    if (score >= 70) return '#88ff00';
    if (score >= 50) return '#ffcc00';
    if (score >= 30) return '#ff6600';
    return '#ff0000';
  }
}

// === 组件性能档案 ===
export class ComponentProfile {
  id: string;
  componentName: string;
  pageName: string;
  renderCount: number;
  avgRenderTime: number;
  maxRenderTime: number;
  layoutCount: number;
  avgLayoutTime: number;
  isOptimized: boolean;
  optimizationStrategies: OptimizeStrategy[];
  lastRenderTime: number;
  dnaSignature: string;

  constructor(data: Partial<ComponentProfile> = {}) {
    this.id = data.id || `COMP-${Date.now()}`;
    this.componentName = data.componentName || 'Unknown';
    this.pageName = data.pageName || '';
    this.renderCount = data.renderCount || 0;
    this.avgRenderTime = data.avgRenderTime || 0;
    this.maxRenderTime = data.maxRenderTime || 0;
    this.layoutCount = data.layoutCount || 0;
    this.avgLayoutTime = data.avgLayoutTime || 0;
    this.isOptimized = data.isOptimized || false;
    this.optimizationStrategies = data.optimizationStrategies || [];
    this.lastRenderTime = data.lastRenderTime || 0;
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.componentName}-${Date.now()}`;
    const hash = payload.split('').reduce((a: number, b: string) => a + b.charCodeAt(0), 0);
    return `SM3-${hash.toString(16).substring(0, 16)}`;
  }

  recordRender(time: number): void {
    this.renderCount++;
    this.avgRenderTime = (this.avgRenderTime * (this.renderCount - 1) + time) / this.renderCount;
    if (time > this.maxRenderTime) this.maxRenderTime = time;
    this.lastRenderTime = time;
  }

  recordLayout(time: number): void {
    this.layoutCount++;
    this.avgLayoutTime = (this.avgLayoutTime * (this.layoutCount - 1) + time) / this.layoutCount;
  }
}

// === 性能统计接口 ===
export interface PerformanceStats {
  totalMetrics: number;
  totalReports: number;
  totalComponents: number;
  avgFPS: number;
  avgFirstFrameTime: number;
  avgLayoutTime: number;
  optimizationRate: number;
}

// === 性能全局状态 ===
@Observed
export class PerformanceState {
  metrics: PerformanceMetric[] = [];
  reports: PerformanceReport[] = [];
  componentProfiles: Map<string, ComponentProfile> = new Map();
  currentFPS: number = 60;
  currentMemory: number = 0;
  currentCPU: number = 0;
  firstFrameStartTime: number = 0;
  firstFrameEndTime: number = 0;
  isMonitoring: boolean = false;

  get statistics(): PerformanceStats {
    return {
      totalMetrics: this.metrics.length,
      totalReports: this.reports.length,
      totalComponents: this.componentProfiles.size,
      avgFPS: this.getAvgFPS(),
      avgFirstFrameTime: this.getAvgFirstFrameTime(),
      avgLayoutTime: this.getAvgLayoutTime(),
      optimizationRate: this.getOptimizationRate()
    };
  }

  private getAvgFPS(): number {
    const fpsMetrics = this.metrics.filter(m => m.type === MetricType.FPS);
    if (fpsMetrics.length === 0) return 60;
    return Math.round(fpsMetrics.reduce((sum, m) => sum + m.value, 0) / fpsMetrics.length);
  }

  private getAvgFirstFrameTime(): number {
    const ffMetrics = this.metrics.filter(m => m.type === MetricType.FIRST_FRAME);
    if (ffMetrics.length === 0) return 0;
    return Math.round(ffMetrics.reduce((sum, m) => sum + m.value, 0) / ffMetrics.length);
  }

  private getAvgLayoutTime(): number {
    const layoutMetrics = this.metrics.filter(m => m.type === MetricType.LAYOUT_TIME);
    if (layoutMetrics.length === 0) return 0;
    return Math.round(layoutMetrics.reduce((sum, m) => sum + m.value, 0) / layoutMetrics.length);
  }

  private getOptimizationRate(): number {
    if (this.componentProfiles.size === 0) return 100;
    const optimized = Array.from(this.componentProfiles.values()).filter(p => p.isOptimized).length;
    return Math.round((optimized / this.componentProfiles.size) * 100);
  }

  startFirstFrame(): void {
    this.firstFrameStartTime = Date.now();
    console.info('[龍魂] 首帧计时开始');
  }

  endFirstFrame(pageName: string): void {
    this.firstFrameEndTime = Date.now();
    const duration = this.firstFrameEndTime - this.firstFrameStartTime;

    const metric = new PerformanceMetric({
      type: MetricType.FIRST_FRAME,
      name: '首帧时间',
      value: duration,
      unit: 'ms',
      pageName
    });

    this.metrics.push(metric);
    console.info(`[龍魂] 首帧时间: ${duration}ms`);
  }

  recordLayoutTime(time: number, pageName: string, componentName?: string): void {
    const metric = new PerformanceMetric({
      type: MetricType.LAYOUT_TIME,
      name: '布局计算时间',
      value: time,
      unit: 'ms',
      pageName,
      componentName
    });
    this.metrics.push(metric);
  }

  generateReport(pageName: string): PerformanceReport {
    const pageMetrics = this.metrics.filter(m => m.pageName === pageName);
    const ffMetric = pageMetrics.find(m => m.type === MetricType.FIRST_FRAME);
    const layoutMetric = pageMetrics.find(m => m.type === MetricType.LAYOUT_TIME);

    const report = new PerformanceReport({
      pageName,
      metrics: pageMetrics,
      firstFrameTime: ffMetric?.value || 0,
      layoutCalcTime: layoutMetric?.value || 0
    });

    this.reports.push(report);
    return report;
  }

  getComponentProfile(name: string, pageName: string): ComponentProfile {
    const key = `${pageName}::${name}`;
    if (!this.componentProfiles.has(key)) {
      this.componentProfiles.set(key, new ComponentProfile({ componentName: name, pageName }));
    }
    return this.componentProfiles.get(key)!;
  }

  startMonitoring(): void {
    this.isMonitoring = true;
    this.monitorLoop();
  }

  stopMonitoring(): void {
    this.isMonitoring = false;
  }

  private monitorLoop(): void {
    if (!this.isMonitoring) return;
    setTimeout(() => this.monitorLoop(), 1000);
  }

  persist(): void {
    AppStorage.setOrCreate('perf_metrics', JSON.stringify(this.metrics.slice(-100)));
    AppStorage.setOrCreate('perf_reports', JSON.stringify(this.reports.slice(-10)));
  }

  load(): void {
    const metricsJson = AppStorage.get<string>('perf_metrics');
    const reportsJson = AppStorage.get<string>('perf_reports');
    if (metricsJson) {
      try { this.metrics = JSON.parse(metricsJson); } catch (e) {}
    }
    if (reportsJson) {
      try { this.reports = JSON.parse(reportsJson); } catch (e) {}
    }
  }
}

export const performanceState = new PerformanceState();
AppStorage.setOrCreate('performanceState', performanceState);
