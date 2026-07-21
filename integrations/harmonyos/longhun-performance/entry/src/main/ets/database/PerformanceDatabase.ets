// entry/src/main/ets/database/PerformanceDatabase.ets
// 龍魂 · 性能数据库 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { relationalStore } from '@kit.ArkData';
import {
  PerformanceMetric,
  PerformanceReport,
  MetricType,
  PerformanceThreshold,
  ComponentProfile
} from '../models/PerformanceModel';

const DB_NAME = 'LonghunPerformance.db';
const DB_VERSION = 1;
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";

// === 数据库表结构 ===
const SQL_CREATE_METRICS = `
  CREATE TABLE IF NOT EXISTS metrics (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT DEFAULT 'ms',
    timestamp INTEGER NOT NULL,
    threshold TEXT,
    page_name TEXT,
    component_name TEXT,
    dna_signature TEXT,
    created_at INTEGER DEFAULT (strftime('%s','now'))
  )
`;

const SQL_CREATE_REPORTS = `
  CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    page_name TEXT NOT NULL,
    total_metrics INTEGER DEFAULT 0,
    excellent_count INTEGER DEFAULT 0,
    good_count INTEGER DEFAULT 0,
    fair_count INTEGER DEFAULT 0,
    poor_count INTEGER DEFAULT 0,
    critical_count INTEGER DEFAULT 0,
    first_frame_time REAL DEFAULT 0,
    layout_calc_time REAL DEFAULT 0,
    render_time REAL DEFAULT 0,
    score INTEGER DEFAULT 0,
    suggestions_json TEXT,
    dna_signature TEXT,
    created_at INTEGER DEFAULT (strftime('%s','now'))
  )
`;

const SQL_CREATE_COMPONENT_PROFILES = `
  CREATE TABLE IF NOT EXISTS component_profiles (
    id TEXT PRIMARY KEY,
    component_name TEXT NOT NULL,
    page_name TEXT NOT NULL,
    render_count INTEGER DEFAULT 0,
    avg_render_time REAL DEFAULT 0,
    max_render_time REAL DEFAULT 0,
    layout_count INTEGER DEFAULT 0,
    avg_layout_time REAL DEFAULT 0,
    is_optimized INTEGER DEFAULT 0,
    strategies_json TEXT,
    last_render_time INTEGER DEFAULT 0,
    dna_signature TEXT,
    updated_at INTEGER DEFAULT (strftime('%s','now'))
  )
`;

const SQL_CREATE_INDEXES = [
  'CREATE INDEX IF NOT EXISTS idx_metrics_type ON metrics(type)',
  'CREATE INDEX IF NOT EXISTS idx_metrics_page ON metrics(page_name)',
  'CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)',
  'CREATE INDEX IF NOT EXISTS idx_reports_page ON reports(page_name)',
  'CREATE INDEX IF NOT EXISTS idx_reports_score ON reports(score)',
  'CREATE INDEX IF NOT EXISTS idx_profiles_component ON component_profiles(component_name, page_name)'
];

// === 数据库管理器 ===
export class PerformanceDatabase {
  private static store: relationalStore.RdbStore | null = null;
  private static isInitialized: boolean = false;

  static async init(): Promise<void> {
    if (this.isInitialized) return;

    try {
      const config: relationalStore.StoreConfig = {
        name: DB_NAME,
        securityLevel: relationalStore.SecurityLevel.S3
      };

      this.store = await relationalStore.getRdbStore(DB_NAME, config);

      // 创建表
      await this.store.executeSql(SQL_CREATE_METRICS);
      await this.store.executeSql(SQL_CREATE_REPORTS);
      await this.store.executeSql(SQL_CREATE_COMPONENT_PROFILES);

      // 创建索引
      for (const indexSql of SQL_CREATE_INDEXES) {
        await this.store.executeSql(indexSql);
      }

      this.isInitialized = true;
      console.info('[龍魂·数据库] 性能数据库初始化完成');
    } catch (error) {
      console.error('[龍魂·数据库] 初始化失败:', error);
      throw error;
    }
  }

  // === 指标操作 ===

  static async saveMetric(metric: PerformanceMetric): Promise<void> {
    if (!this.store) await this.init();

    const sql = `
      INSERT OR REPLACE INTO metrics (id, type, name, value, unit, timestamp, threshold, page_name, component_name, dna_signature)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

    const bindArgs = [
      metric.id,
      metric.type,
      metric.name,
      metric.value,
      metric.unit,
      metric.timestamp,
      metric.threshold,
      metric.pageName,
      metric.componentName || null,
      metric.dnaSignature
    ];

    await this.store!.executeSql(sql, bindArgs);
  }

  static async saveMetrics(metrics: PerformanceMetric[]): Promise<void> {
    if (!this.store) await this.init();

    for (const metric of metrics) {
      await this.saveMetric(metric);
    }
  }

  static async getMetricsByPage(pageName: string, limit: number = 100): Promise<PerformanceMetric[]> {
    if (!this.store) await this.init();

    const predicates = new relationalStore.RdbPredicates('metrics');
    predicates.equalTo('page_name', pageName);
    predicates.orderByDesc('timestamp');
    predicates.limit(limit);

    const resultSet = await this.store!.query(predicates);
    const metrics: PerformanceMetric[] = [];

    while (resultSet.goToNextRow()) {
      metrics.push(new PerformanceMetric({
        id: resultSet.getString(resultSet.getColumnIndex('id')),
        type: resultSet.getString(resultSet.getColumnIndex('type')) as MetricType,
        name: resultSet.getString(resultSet.getColumnIndex('name')),
        value: resultSet.getDouble(resultSet.getColumnIndex('value')),
        unit: resultSet.getString(resultSet.getColumnIndex('unit')),
        timestamp: resultSet.getLong(resultSet.getColumnIndex('timestamp')),
        threshold: resultSet.getString(resultSet.getColumnIndex('threshold')) as PerformanceThreshold,
        pageName: resultSet.getString(resultSet.getColumnIndex('page_name')),
        componentName: resultSet.getString(resultSet.getColumnIndex('component_name'))
      }));
    }

    resultSet.close();
    return metrics;
  }

  static async getMetricsByType(type: MetricType, limit: number = 50): Promise<PerformanceMetric[]> {
    if (!this.store) await this.init();

    const predicates = new relationalStore.RdbPredicates('metrics');
    predicates.equalTo('type', type);
    predicates.orderByDesc('timestamp');
    predicates.limit(limit);

    const resultSet = await this.store!.query(predicates);
    const metrics: PerformanceMetric[] = [];

    while (resultSet.goToNextRow()) {
      metrics.push(new PerformanceMetric({
        id: resultSet.getString(resultSet.getColumnIndex('id')),
        type: resultSet.getString(resultSet.getColumnIndex('type')) as MetricType,
        name: resultSet.getString(resultSet.getColumnIndex('name')),
        value: resultSet.getDouble(resultSet.getColumnIndex('value')),
        unit: resultSet.getString(resultSet.getColumnIndex('unit')),
        timestamp: resultSet.getLong(resultSet.getColumnIndex('timestamp')),
        threshold: resultSet.getString(resultSet.getColumnIndex('threshold')) as PerformanceThreshold,
        pageName: resultSet.getString(resultSet.getColumnIndex('page_name')),
        componentName: resultSet.getString(resultSet.getColumnIndex('component_name'))
      }));
    }

    resultSet.close();
    return metrics;
  }

  // === 报告操作 ===

  static async saveReport(report: PerformanceReport): Promise<void> {
    if (!this.store) await this.init();

    const sql = `
      INSERT OR REPLACE INTO reports (id, page_name, total_metrics, excellent_count, good_count, fair_count, poor_count, critical_count, first_frame_time, layout_calc_time, render_time, score, suggestions_json, dna_signature)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

    const bindArgs = [
      report.id,
      report.pageName,
      report.totalMetrics,
      report.excellentCount,
      report.goodCount,
      report.fairCount,
      report.poorCount,
      report.criticalCount,
      report.firstFrameTime,
      report.layoutCalcTime,
      report.renderTime,
      report.getScore(),
      JSON.stringify(report.suggestions),
      report.dnaSignature
    ];

    await this.store!.executeSql(sql, bindArgs);
  }

  static async getReports(pageName?: string, limit: number = 10): Promise<PerformanceReport[]> {
    if (!this.store) await this.init();

    const predicates = new relationalStore.RdbPredicates('reports');
    if (pageName) {
      predicates.equalTo('page_name', pageName);
    }
    predicates.orderByDesc('created_at');
    predicates.limit(limit);

    const resultSet = await this.store!.query(predicates);
    const reports: PerformanceReport[] = [];

    while (resultSet.goToNextRow()) {
      const suggestionsJson = resultSet.getString(resultSet.getColumnIndex('suggestions_json'));
      const suggestions = suggestionsJson ? JSON.parse(suggestionsJson) : [];

      reports.push(new PerformanceReport({
        id: resultSet.getString(resultSet.getColumnIndex('id')),
        pageName: resultSet.getString(resultSet.getColumnIndex('page_name')),
        firstFrameTime: resultSet.getDouble(resultSet.getColumnIndex('first_frame_time')),
        layoutCalcTime: resultSet.getDouble(resultSet.getColumnIndex('layout_calc_time')),
        renderTime: resultSet.getDouble(resultSet.getColumnIndex('render_time')),
        suggestions
      }));
    }

    resultSet.close();
    return reports;
  }

  // === 组件档案操作 ===

  static async saveComponentProfile(profile: ComponentProfile): Promise<void> {
    if (!this.store) await this.init();

    const sql = `
      INSERT OR REPLACE INTO component_profiles (id, component_name, page_name, render_count, avg_render_time, max_render_time, layout_count, avg_layout_time, is_optimized, strategies_json, last_render_time, dna_signature, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

    const bindArgs = [
      profile.id,
      profile.componentName,
      profile.pageName,
      profile.renderCount,
      profile.avgRenderTime,
      profile.maxRenderTime,
      profile.layoutCount,
      profile.avgLayoutTime,
      profile.isOptimized ? 1 : 0,
      JSON.stringify(profile.optimizationStrategies),
      profile.lastRenderTime,
      profile.dnaSignature,
      Date.now()
    ];

    await this.store!.executeSql(sql, bindArgs);
  }

  static async getComponentProfiles(pageName?: string): Promise<ComponentProfile[]> {
    if (!this.store) await this.init();

    const predicates = new relationalStore.RdbPredicates('component_profiles');
    if (pageName) {
      predicates.equalTo('page_name', pageName);
    }
    predicates.orderByDesc('avg_render_time');

    const resultSet = await this.store!.query(predicates);
    const profiles: ComponentProfile[] = [];

    while (resultSet.goToNextRow()) {
      const strategiesJson = resultSet.getString(resultSet.getColumnIndex('strategies_json'));

      profiles.push(new ComponentProfile({
        id: resultSet.getString(resultSet.getColumnIndex('id')),
        componentName: resultSet.getString(resultSet.getColumnIndex('component_name')),
        pageName: resultSet.getString(resultSet.getColumnIndex('page_name')),
        renderCount: resultSet.getLong(resultSet.getColumnIndex('render_count')),
        avgRenderTime: resultSet.getDouble(resultSet.getColumnIndex('avg_render_time')),
        maxRenderTime: resultSet.getDouble(resultSet.getColumnIndex('max_render_time')),
        layoutCount: resultSet.getLong(resultSet.getColumnIndex('layout_count')),
        avgLayoutTime: resultSet.getDouble(resultSet.getColumnIndex('avg_layout_time')),
        isOptimized: resultSet.getLong(resultSet.getColumnIndex('is_optimized')) === 1,
        optimizationStrategies: strategiesJson ? JSON.parse(strategiesJson) : [],
        lastRenderTime: resultSet.getLong(resultSet.getColumnIndex('last_render_time'))
      }));
    }

    resultSet.close();
    return profiles;
  }

  // === 统计操作 ===

  static async getStats(): Promise<DatabaseStats> {
    if (!this.store) await this.init();

    const metricsCount = await this.getCount('metrics');
    const reportsCount = await this.getCount('reports');
    const profilesCount = await this.getCount('component_profiles');

    // 平均首帧时间
    const avgFFSql = 'SELECT AVG(first_frame_time) as avg_ff FROM reports';
    const avgFFResult = await this.store!.querySql(avgFFSql);
    let avgFirstFrame = 0;
    if (avgFFResult.goToNextRow()) {
      avgFirstFrame = avgFFResult.getDouble(0);
    }
    avgFFResult.close();

    // 优化率
    const optSql = 'SELECT COUNT(*) as total, SUM(is_optimized) as optimized FROM component_profiles';
    const optResult = await this.store!.querySql(optSql);
    let optimizationRate = 100;
    if (optResult.goToNextRow()) {
      const total = optResult.getLong(0);
      const optimized = optResult.getLong(1);
      optimizationRate = total > 0 ? Math.round((optimized / total) * 100) : 100;
    }
    optResult.close();

    return {
      totalMetrics: metricsCount,
      totalReports: reportsCount,
      totalComponents: profilesCount,
      avgFirstFrameTime: Math.round(avgFirstFrame),
      optimizationRate
    };
  }

  // === 清理操作 ===

  static async cleanOldMetrics(daysToKeep: number = 7): Promise<number> {
    if (!this.store) await this.init();

    const cutoff = Date.now() - daysToKeep * 24 * 60 * 60 * 1000;
    const sql = 'DELETE FROM metrics WHERE timestamp < ?';
    await this.store!.executeSql(sql, [cutoff]);

    // 获取删除数量
    const changesResult = await this.store!.querySql('SELECT changes()');
    let deleted = 0;
    if (changesResult.goToNextRow()) {
      deleted = changesResult.getLong(0);
    }
    changesResult.close();

    console.info(`[龍魂·数据库] 清理了 ${deleted} 条过期指标 (保留${daysToKeep}天)`);
    return deleted;
  }

  static async cleanAll(): Promise<void> {
    if (!this.store) await this.init();

    await this.store!.executeSql('DELETE FROM metrics');
    await this.store!.executeSql('DELETE FROM reports');
    await this.store!.executeSql('DELETE FROM component_profiles');

    console.info('[龍魂·数据库] 所有数据已清空');
  }

  // === 辅助方法 ===

  private static async getCount(tableName: string): Promise<number> {
    const sql = `SELECT COUNT(*) FROM ${tableName}`;
    const resultSet = await this.store!.querySql(sql);
    let count = 0;
    if (resultSet.goToNextRow()) {
      count = resultSet.getLong(0);
    }
    resultSet.close();
    return count;
  }

  static isReady(): boolean {
    return this.isInitialized && this.store !== null;
  }

  static async close(): Promise<void> {
    if (this.store) {
      await this.store.close();
      this.store = null;
      this.isInitialized = false;
    }
  }
}

// === 数据库统计接口 ===
export interface DatabaseStats {
  totalMetrics: number;
  totalReports: number;
  totalComponents: number;
  avgFirstFrameTime: number;
  optimizationRate: number;
}
