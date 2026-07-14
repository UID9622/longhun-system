// entry/src/main/ets/utils/PerformanceMonitor.ets
// 龍魂 · 性能监控器 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import {
  performanceState,
  PerformanceMetric,
  MetricType,
  PerformanceReport,
  ComponentProfile,
  PerformanceThreshold,
  OptimizeStrategy
} from '../models/PerformanceModel';

export class PerformanceMonitor {
  private static instance: PerformanceMonitor;
  private markMap: Map<string, number> = new Map();
  private fpsHistory: number[] = [];
  private fpsFrameCount: number = 0;
  private fpsLastTime: number = 0;
  private readonly MAX_FPS_HISTORY: number = 120;

  static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor();
    }
    return PerformanceMonitor.instance;
  }

  // === 标记与测量 ===

  mark(name: string): void {
    this.markMap.set(name, Date.now());
    console.info(`[龍魂·性能] 标记: ${name}`);
  }

  measure(name: string, type: MetricType, pageName: string, componentName?: string): number {
    const start = this.markMap.get(name);
    if (!start) {
      console.warn(`[龍魂·性能] 未找到标记: ${name}`);
      return 0;
    }

    const duration = Date.now() - start;
    this.markMap.delete(name);

    const metric = new PerformanceMetric({
      type,
      name,
      value: duration,
      unit: 'ms',
      pageName,
      componentName
    });

    performanceState.metrics.push(metric);
    console.info(`[龍魂·性能] ${name}: ${duration}ms [${metric.getThresholdLabel()}]`);

    return duration;
  }

  // === 首帧监控 ===

  monitorFirstFrame(pageName: string): void {
    performanceState.startFirstFrame();

    // 使用 requestAnimationFrame 或 setTimeout 在下一帧测量
    setTimeout(() => {
      performanceState.endFirstFrame(pageName);

      const duration = performanceState.firstFrameEndTime - performanceState.firstFrameStartTime;
      console.info(`[龍魂·性能] 首帧完成: ${pageName} - ${duration}ms`);
    }, 0);
  }

  // === 布局监控 ===

  monitorLayout(componentName: string, pageName: string, layoutCallback: () => void): number {
    const start = Date.now();
    layoutCallback();
    const duration = Date.now() - start;
    performanceState.recordLayoutTime(duration, pageName, componentName);

    if (duration > 100) {
      console.warn(`[龍魂·性能] 布局耗时较长: ${componentName} - ${duration}ms`);
    }

    return duration;
  }

  // === 渲染监控 ===

  monitorRender(componentName: string, pageName: string): void {
    const profile = performanceState.getComponentProfile(componentName, pageName);
    const start = Date.now();

    setTimeout(() => {
      const duration = Date.now() - start;
      profile.recordRender(duration);
    }, 0);
  }

  // === FPS 监控 ===

  startFPSMonitor(): void {
    this.fpsFrameCount = 0;
    this.fpsLastTime = Date.now();
    this.fpsHistory = [];

    this.fpsLoop();
  }

  private fpsLoop(): void {
    this.fpsFrameCount++;

    const now = Date.now();
    const elapsed = now - this.fpsLastTime;

    if (elapsed >= 1000) {
      const fps = Math.round((this.fpsFrameCount * 1000) / elapsed);
      performanceState.currentFPS = fps;

      this.fpsHistory.push(fps);
      if (this.fpsHistory.length > this.MAX_FPS_HISTORY) {
        this.fpsHistory.shift();
      }

      const metric = new PerformanceMetric({
        type: MetricType.FPS,
        name: '实时FPS',
        value: fps,
        unit: 'fps',
        pageName: 'FPS_MONITOR'
      });
      performanceState.metrics.push(metric);

      this.fpsFrameCount = 0;
      this.fpsLastTime = now;

      // FPS告警
      if (fps < 30) {
        console.warn(`[龍魂·性能] FPS过低: ${fps}`);
      }
    }

    setTimeout(() => this.fpsLoop(), 16); // ~60fps采样
  }

  getFPSStats(): { current: number; avg: number; min: number; max: number } {
    if (this.fpsHistory.length === 0) {
      return { current: 60, avg: 60, min: 60, max: 60 };
    }

    const sum = this.fpsHistory.reduce((a, b) => a + b, 0);
    return {
      current: performanceState.currentFPS,
      avg: Math.round(sum / this.fpsHistory.length),
      min: Math.min(...this.fpsHistory),
      max: Math.max(...this.fpsHistory)
    };
  }

  // === 内存监控 ===

  monitorMemory(): void {
    // 鸿蒙原生：使用 hidebug.getPss() 获取内存
    // import hidebug from '@ohos.hidebug';
    // const pss = hidebug.getPss();
    // performanceState.currentMemory = Math.round(pss / 1024 / 1024);

    // 模拟内存采样
    const simulatedMemory = 50 + Math.random() * 30;
    performanceState.currentMemory = Math.round(simulatedMemory);

    const metric = new PerformanceMetric({
      type: MetricType.MEMORY,
      name: '内存占用',
      value: performanceState.currentMemory,
      unit: 'MB',
      pageName: 'MEMORY_MONITOR'
    });
    performanceState.metrics.push(metric);

    if (performanceState.currentMemory > 200) {
      console.warn(`[龍魂·性能] 内存占用过高: ${performanceState.currentMemory}MB`);
    }
  }

  // === CPU 监控 ===

  monitorCPU(): void {
    // 鸿蒙原生：使用 hidebug.getCpuUsage() 获取CPU使用率
    // import hidebug from '@ohos.hidebug';
    // const cpuUsage = hidebug.getCpuUsage();
    // performanceState.currentCPU = Math.round(cpuUsage);

    const simulatedCPU = 10 + Math.random() * 20;
    performanceState.currentCPU = Math.round(simulatedCPU);

    if (performanceState.currentCPU > 70) {
      console.warn(`[龍魂·性能] CPU使用率过高: ${performanceState.currentCPU}%`);
    }
  }

  // === 综合监控 ===

  startComprehensiveMonitor(): void {
    performanceState.startMonitoring();
    this.startFPSMonitor();

    // 每秒采样内存和CPU
    const comprehensiveLoop = (): void => {
      if (!performanceState.isMonitoring) return;
      this.monitorMemory();
      this.monitorCPU();
      setTimeout(() => comprehensiveLoop(), 1000);
    };
    comprehensiveLoop();
  }

  stopComprehensiveMonitor(): void {
    performanceState.stopMonitoring();
  }

  // === 报告生成 ===

  generateReport(pageName: string): PerformanceReport {
    return performanceState.generateReport(pageName);
  }

  getSuggestions(pageName: string): string[] {
    const report = this.generateReport(pageName);
    return report.suggestions.map(s => s.title);
  }

  // === 优化检查 ===

  runOptimizationCheck(pageName: string): OptimizationCheckResult {
    const report = this.generateReport(pageName);
    const checks: OptimizationCheckItem[] = [];

    // 首帧时间检查
    checks.push({
      name: '首帧时间',
      standard: '< 300ms',
      actual: `${report.firstFrameTime}ms`,
      pass: report.firstFrameTime < 300,
      severity: report.firstFrameTime >= 500 ? 'critical' : report.firstFrameTime >= 300 ? 'warning' : 'pass'
    });

    // 布局计算检查
    checks.push({
      name: '布局计算',
      standard: '< 100ms',
      actual: `${report.layoutCalcTime}ms`,
      pass: report.layoutCalcTime < 100,
      severity: report.layoutCalcTime >= 200 ? 'critical' : report.layoutCalcTime >= 100 ? 'warning' : 'pass'
    });

    // FPS检查
    const fpsStats = this.getFPSStats();
    checks.push({
      name: '平均FPS',
      standard: '> 55',
      actual: `${fpsStats.avg}`,
      pass: fpsStats.avg >= 55,
      severity: fpsStats.avg < 30 ? 'critical' : fpsStats.avg < 55 ? 'warning' : 'pass'
    });

    // 内存检查
    checks.push({
      name: '内存占用',
      standard: '< 100MB',
      actual: `${performanceState.currentMemory}MB`,
      pass: performanceState.currentMemory < 100,
      severity: performanceState.currentMemory >= 200 ? 'critical' : performanceState.currentMemory >= 100 ? 'warning' : 'pass'
    });

    // 优化率检查
    checks.push({
      name: '组件优化率',
      standard: '> 80%',
      actual: `${performanceState.statistics.optimizationRate}%`,
      pass: performanceState.statistics.optimizationRate >= 80,
      severity: performanceState.statistics.optimizationRate < 50 ? 'critical' : performanceState.statistics.optimizationRate < 80 ? 'warning' : 'pass'
    });

    const passedCount = checks.filter(c => c.pass).length;
    const score = Math.round((passedCount / checks.length) * 100);

    return {
      pageName,
      checks,
      totalChecks: checks.length,
      passedCount,
      score,
      timestamp: new Date()
    };
  }

  // === 工具方法 ===

  clearMarks(): void {
    this.markMap.clear();
  }

  clearMetrics(): void {
    performanceState.metrics = [];
  }

  clearReports(): void {
    performanceState.reports = [];
  }

  getMetricsByPage(pageName: string): PerformanceMetric[] {
    return performanceState.metrics.filter(m => m.pageName === pageName);
  }

  getMetricsByType(type: MetricType): PerformanceMetric[] {
    return performanceState.metrics.filter(m => m.type === type);
  }
}

// === 优化检查结果接口 ===

export interface OptimizationCheckItem {
  name: string;
  standard: string;
  actual: string;
  pass: boolean;
  severity: 'pass' | 'warning' | 'critical';
}

export interface OptimizationCheckResult {
  pageName: string;
  checks: OptimizationCheckItem[];
  totalChecks: number;
  passedCount: number;
  score: number;
  timestamp: Date;
}

export const perfMonitor = PerformanceMonitor.getInstance();
