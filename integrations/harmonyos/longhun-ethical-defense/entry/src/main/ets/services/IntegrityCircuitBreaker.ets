// entry/src/main/ets/services/IntegrityCircuitBreaker.ets
// 龍魂 · 商业诚信熔断器 · 只标注不封号·只提醒不删除
// DNA: #龍芯⚡️丙午·辛未·丙戌·INTEGRITY-BREAKER-v1.0
// UID: 9622 | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

import {
  IntegrityDetector, IntegrityReport, AnomalyRecord,
  FraudType, AnomalySeverity, IntegrityLevel, ProductInspection
} from '../engines/IntegrityDetector';

// === 熔断标注等级 ===
export enum BreakerLabelLevel {
  GREEN = 'green',     // 绿色：诚信通过
  YELLOW = 'yellow',   // 黄色：轻微提醒
  ORANGE = 'orange',   // 橙色：注意核实
  RED = 'red',         // 红色：高风险警告
  BLACK = 'black'      // 黑色：涉嫌欺诈
}

// === 熔断展示结果 ===
export interface BreakerDisplay {
  productId: string;
  productName: string;
  level: BreakerLabelLevel;
  integrityLevel: IntegrityLevel;
  trustScore: number;
  label: string;
  labelIcon: string;
  color: string;
  bgColor: string;
  anomalies: AnomalyRecord[];
  recommendation: string;
  officialCert: boolean;
  timestamp: number;
  dnaSignature: string;
}

// === 熔断历史记录 ===
export interface BreakerHistoryRecord extends BreakerDisplay {
  id: string;
  inspectorUid: string;
  platform: string;
  sellerId: string;
  sellerName: string;
}

// === 商家诚信档案 ===
export interface SellerIntegrityProfile {
  sellerId: string;
  sellerName: string;
  totalInspections: number;
  greenCount: number;
  yellowCount: number;
  orangeCount: number;
  redCount: number;
  blackCount: number;
  averageTrustScore: number;
  worstLevel: BreakerLabelLevel;
  lastInspection: number;
  warningFlag: boolean;
  blacklistFlag: boolean;
}

// ============================================================
//  商业诚信熔断器
// ============================================================

export class IntegrityCircuitBreaker {
  private static instance: IntegrityCircuitBreaker;

  // 熔断历史（本地存储，不上传云端）
  private breakerHistory: BreakerHistoryRecord[] = [];

  // 商家诚信档案
  private sellerProfiles: Map<string, SellerIntegrityProfile> = new Map();

  // 全局熔断黑名单（不可删除，仅追加）
  private globalBlacklist: Set<string> = new Set();

  // 统计
  private stats = {
    totalInspections: 0,
    totalAnomaliesDetected: 0,
    totalBlackFlags: 0,
    elderlyScamsDetected: 0
  };

  // 配置
  private readonly MAX_HISTORY_SIZE = 10000;
  private readonly BLACKLIST_AUTO_THRESHOLD = 5; // 同一商家累计5次black标记自动列入高风险

  static getInstance(): IntegrityCircuitBreaker {
    if (!IntegrityCircuitBreaker.instance) {
      IntegrityCircuitBreaker.instance = new IntegrityCircuitBreaker();
    }
    return IntegrityCircuitBreaker.instance;
  }

  // ============================================================
  //  熔断主入口
  // ============================================================

  async break(report: IntegrityReport, product?: ProductInspection): Promise<BreakerDisplay> {
    const level = this.mapLevel(report.integrityLevel);

    // 合并商家历史警告
    if (product) {
      report.sellerWarnings = this.getSellerWarningCount(product.sellerId);
    }

    const display: BreakerDisplay = {
      productId: report.productId,
      productName: report.productName,
      level,
      integrityLevel: report.integrityLevel,
      trustScore: report.trustScore,
      label: this.getLabel(level),
      labelIcon: this.getLabelIcon(level),
      color: this.getColor(level),
      bgColor: this.getBgColor(level),
      anomalies: report.anomalies,
      recommendation: report.recommendation,
      officialCert: report.officialCertValid,
      timestamp: report.timestamp,
      dnaSignature: report.dnaSignature
    };

    // 记录历史
    this.recordHistory(display, product);

    // 更新商家档案
    if (product) {
      this.updateSellerProfile(product, display);
    }

    // 更新统计
    this.updateStats(display);

    // 检查是否需要加入黑名单
    this.checkBlacklist(product, display);

    return display;
  }

  // ============================================================
  //  等级映射
  // ============================================================

  private mapLevel(integrityLevel: IntegrityLevel): BreakerLabelLevel {
    const mapping: Record<string, BreakerLabelLevel> = {
      'A': BreakerLabelLevel.GREEN,
      'B': BreakerLabelLevel.YELLOW,
      'C': BreakerLabelLevel.ORANGE,
      'D': BreakerLabelLevel.RED,
      'F': BreakerLabelLevel.BLACK
    };
    return mapping[integrityLevel] || BreakerLabelLevel.YELLOW;
  }

  private getLabel(level: BreakerLabelLevel): string {
    const labels: Record<string, string> = {
      green: '诚信通过',
      yellow: '轻微提醒',
      orange: '注意核实',
      red: '高风险警告',
      black: '涉嫌欺诈'
    };
    return labels[level] || '待检测';
  }

  private getLabelIcon(level: BreakerLabelLevel): string {
    const icons: Record<string, string> = {
      green: '✅',
      yellow: '⚠️',
      orange: '🔶',
      red: '🚫',
      black: '⛔'
    };
    return icons[level] || '❓';
  }

  private getColor(level: BreakerLabelLevel): string {
    const colors: Record<string, string> = {
      green: '#00cc66',
      yellow: '#ffcc00',
      orange: '#ff8800',
      red: '#ff2244',
      black: '#000000'
    };
    return colors[level] || '#888888';
  }

  private getBgColor(level: BreakerLabelLevel): string {
    const colors: Record<string, string> = {
      green: 'rgba(0,204,102,0.08)',
      yellow: 'rgba(255,204,0,0.08)',
      orange: 'rgba(255,136,0,0.08)',
      red: 'rgba(255,34,68,0.08)',
      black: 'rgba(255,0,0,0.12)'
    };
    return colors[level] || 'rgba(255,255,255,0.03)';
  }

  // ============================================================
  //  历史记录
  // ============================================================

  private recordHistory(display: BreakerDisplay, product?: ProductInspection): void {
    const record: BreakerHistoryRecord = {
      id: `IB-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`,
      ...display,
      inspectorUid: '9622',
      platform: product?.platform || '未知',
      sellerId: product?.sellerId || '未知',
      sellerName: product?.sellerName || '未知'
    };

    this.breakerHistory.unshift(record);

    // 限制历史大小
    if (this.breakerHistory.length > this.MAX_HISTORY_SIZE) {
      this.breakerHistory = this.breakerHistory.slice(0, this.MAX_HISTORY_SIZE);
    }
  }

  // ============================================================
  //  商家诚信档案
  // ============================================================

  private updateSellerProfile(product: ProductInspection, display: BreakerDisplay): void {
    let profile = this.sellerProfiles.get(product.sellerId);

    if (!profile) {
      profile = {
        sellerId: product.sellerId,
        sellerName: product.sellerName,
        totalInspections: 0,
        greenCount: 0,
        yellowCount: 0,
        orangeCount: 0,
        redCount: 0,
        blackCount: 0,
        averageTrustScore: 0,
        worstLevel: BreakerLabelLevel.GREEN,
        lastInspection: 0,
        warningFlag: false,
        blacklistFlag: false
      };
    }

    profile.totalInspections++;
    profile.lastInspection = Date.now();

    switch (display.level) {
      case BreakerLabelLevel.GREEN: profile.greenCount++; break;
      case BreakerLabelLevel.YELLOW: profile.yellowCount++; break;
      case BreakerLabelLevel.ORANGE: profile.orangeCount++; break;
      case BreakerLabelLevel.RED: profile.redCount++; break;
      case BreakerLabelLevel.BLACK: profile.blackCount++; break;
    }

    // 更新最差等级
    const levelOrder = [BreakerLabelLevel.GREEN, BreakerLabelLevel.YELLOW, BreakerLabelLevel.ORANGE, BreakerLabelLevel.RED, BreakerLabelLevel.BLACK];
    const currentIdx = levelOrder.indexOf(display.level);
    const worstIdx = levelOrder.indexOf(profile.worstLevel);
    if (currentIdx > worstIdx) profile.worstLevel = display.level;

    // 移动平均信任分
    profile.averageTrustScore = Math.round(
      (profile.averageTrustScore * (profile.totalInspections - 1) + display.trustScore) / profile.totalInspections
    );

    // 自动标记
    if (profile.blackCount >= this.BLACKLIST_AUTO_THRESHOLD) {
      profile.blacklistFlag = true;
    }
    if (profile.redCount >= 3) {
      profile.warningFlag = true;
    }

    this.sellerProfiles.set(product.sellerId, profile);
  }

  // ============================================================
  //  黑名单
  // ============================================================

  private checkBlacklist(product?: ProductInspection, display?: BreakerDisplay): void {
    if (!product) return;

    if (display && display.level === BreakerLabelLevel.BLACK) {
      this.globalBlacklist.add(product.sellerId);
    }
  }

  isBlacklisted(sellerId: string): boolean {
    return this.globalBlacklist.has(sellerId);
  }

  getGlobalBlacklist(): string[] {
    return Array.from(this.globalBlacklist);
  }

  // ============================================================
  //  统计
  // ============================================================

  private updateStats(display: BreakerDisplay): void {
    this.stats.totalInspections++;
    this.stats.totalAnomaliesDetected += display.anomalies.length;

    if (display.level === BreakerLabelLevel.BLACK) {
      this.stats.totalBlackFlags++;
    }

    const hasElderlyScam = display.anomalies.some(a => a.type === FraudType.ELDERLY_SCAM);
    if (hasElderlyScam) {
      this.stats.elderlyScamsDetected++;
    }
  }

  getStats() {
    return { ...this.stats };
  }

  // ============================================================
  //  查询接口
  // ============================================================

  // 获取全部熔断历史
  getHistory(limit: number = 50): BreakerHistoryRecord[] {
    return this.breakerHistory.slice(0, limit);
  }

  // 按等级筛选
  getHistoryByLevel(level: BreakerLabelLevel, limit: number = 50): BreakerHistoryRecord[] {
    return this.breakerHistory.filter(r => r.level === level).slice(0, limit);
  }

  // 按商家查询
  getHistoryBySeller(sellerId: string): BreakerHistoryRecord[] {
    return this.breakerHistory.filter(r => r.sellerId === sellerId);
  }

  // 获取高风险记录
  getHighRiskHistory(): BreakerHistoryRecord[] {
    return this.breakerHistory.filter(
      r => r.level === BreakerLabelLevel.RED || r.level === BreakerLabelLevel.BLACK
    );
  }

  // 获取商家诚信档案
  getSellerProfile(sellerId: string): SellerIntegrityProfile | null {
    return this.sellerProfiles.get(sellerId) || null;
  }

  // 获取商家警告数
  getSellerWarningCount(sellerId: string): number {
    const profile = this.sellerProfiles.get(sellerId);
    if (!profile) return 0;
    return profile.redCount + profile.blackCount * 2;
  }

  // 获取所有商家档案
  getAllSellerProfiles(): SellerIntegrityProfile[] {
    return Array.from(this.sellerProfiles.values());
  }

  // 获取高风险商家列表
  getHighRiskSellers(): SellerIntegrityProfile[] {
    return Array.from(this.sellerProfiles.values())
      .filter(p => p.worstLevel === BreakerLabelLevel.RED || p.worstLevel === BreakerLabelLevel.BLACK)
      .sort((a, b) => b.averageTrustScore - a.averageTrustScore);
  }

  // 获取今日统计
  getTodayStats(): { inspections: number; blackFlags: number; elderlyAlerts: number } {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const todayStart = today.getTime();

    const todayRecords = this.breakerHistory.filter(r => r.timestamp >= todayStart);

    return {
      inspections: todayRecords.length,
      blackFlags: todayRecords.filter(r => r.level === BreakerLabelLevel.BLACK).length,
      elderlyAlerts: todayRecords.filter(r => r.anomalies.some(a => a.type === FraudType.ELDERLY_SCAM)).length
    };
  }

  // ============================================================
  //  导出
  // ============================================================

  // 导出为JSON（可提供给监管部门或平台方）
  exportReport(sellerId: string): object {
    const profile = this.sellerProfiles.get(sellerId);
    const history = this.breakerHistory.filter(r => r.sellerId === sellerId);

    return {
      exportTime: Date.now(),
      dnaSignature: `SM3-LONGHUN-INTEGRITY-EXPORT-${sellerId}-${Date.now()}`,
      sellerProfile: profile || null,
      inspectionHistory: history.slice(0, 100),
      summary: {
        totalInspections: history.length,
        anomalyTypes: this.countAnomalyTypes(history),
        trustTrend: this.calculateTrustTrend(history)
      }
    };
  }

  private countAnomalyTypes(history: BreakerHistoryRecord[]): Record<string, number> {
    const counts: Record<string, number> = {};
    for (const h of history) {
      for (const a of h.anomalies) {
        counts[a.type] = (counts[a.type] || 0) + 1;
      }
    }
    return counts;
  }

  private calculateTrustTrend(history: BreakerHistoryRecord[]): 'up' | 'down' | 'stable' {
    if (history.length < 2) return 'stable';
    const recent = history.slice(0, 5);
    const avg = recent.reduce((sum, r) => sum + r.trustScore, 0) / recent.length;
    const older = history.slice(-5);
    const oldAvg = older.reduce((sum, r) => sum + r.trustScore, 0) / older.length;

    if (avg > oldAvg + 5) return 'up';
    if (avg < oldAvg - 5) return 'down';
    return 'stable';
  }
}

export const integrityCircuitBreaker = IntegrityCircuitBreaker.getInstance();
