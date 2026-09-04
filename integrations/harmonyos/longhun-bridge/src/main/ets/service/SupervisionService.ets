// DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-HARMONYOS-SERVICE-v1.0-UID9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
//
// 龍魂·鸿蒙后台监督服务
// 使用 ServiceAbility 常驻后台 · 每30分钟自动触发学习闭环

import { LonghunBridgeInterface, SupervisionConfig, SupervisionReport } from '../LonghunBridge';
import serviceAgent from '@ohos.ability.serviceAgent';
import backgroundTaskManager from '@ohos.resourceschedule.backgroundTaskManager';
import wantAgent from '@ohos.app.ability.wantAgent';
import { logger } from '../utils/Logger';

const TAG = 'LonghunSupervisionService';
const SUPERVISION_INTERVAL_MS = 30 * 60 * 1000; // 30 分钟
const CONTINUOUS_TASK_ID = 0x1001;

/**
 * 后台监督服务
 * 常驻运行，每 30 分钟自动执行一次学习闭环
 */
export class LonghunSupervisionService {
  private static instance: LonghunSupervisionService | null = null;
  private bridge: LonghunBridgeInterface | null = null;
  private timerId: number = -1;
  private isRunning: boolean = false;
  private lastReport: SupervisionReport | null = null;

  static getInstance(): LonghunSupervisionService {
    if (!LonghunSupervisionService.instance) {
      LonghunSupervisionService.instance = new LonghunSupervisionService();
    }
    return LonghunSupervisionService.instance;
  }

  /**
   * 初始化并启动后台服务
   */
  async start(bridge: LonghunBridgeInterface): Promise<void> {
    if (this.isRunning) {
      logger.warn(TAG, '监督服务已在运行中');
      return;
    }

    this.bridge = bridge;
    this.isRunning = true;

    // 申请长时任务（后台持续运行）
    try {
      await this.requestContinuousTask();
      logger.info(TAG, '长时任务申请成功');
    } catch (err) {
      logger.warn(TAG, `长时任务申请失败，使用定时器模式: ${JSON.stringify(err)}`);
    }

    // 启动定时监督循环
    this.startSupervisionLoop();
    logger.info(TAG, '龙魂后台监督服务已启动 · 间隔30分钟');
  }

  /**
   * 停止后台服务
   */
  async stop(): Promise<void> {
    if (!this.isRunning) {
      return;
    }
    this.isRunning = false;
    clearInterval(this.timerId);
    try {
      await backgroundTaskManager.stopBackgroundRunning(globalThis.abilityContext);
      logger.info(TAG, '长时任务已停止');
    } catch (err) {
      logger.warn(TAG, '停止长时任务失败');
    }
    logger.info(TAG, '龙魂后台监督服务已停止');
  }

  /**
   * 获取最近一次监督报告
   */
  getLastReport(): SupervisionReport | null {
    return this.lastReport;
  }

  // ── 私有方法 ──

  private startSupervisionLoop(): void {
    // 立即执行一次
    this.runSupervisionCycle();

    // 定时循环
    this.timerId = setInterval(() => {
      this.runSupervisionCycle();
    }, SUPERVISION_INTERVAL_MS);
  }

  private async runSupervisionCycle(): Promise<void> {
    if (!this.bridge || !this.isRunning) {
      return;
    }

    try {
      logger.info(TAG, '开始监督循环...');

      const config: SupervisionConfig = {
        sensitivity: 0.7,
        dnaVerify: true,
        auditEnabled: true,
        maxDeviation: 20.0,
      };

      const report = await this.bridge.runSupervision(config);
      this.lastReport = report;

      // 🟢 正常
      if (report.audit === 'green') {
        logger.info(TAG, `监督通过 · 评分: ${report.score}`);
        return;
      }

      // 🟡 待核
      if (report.audit === 'yellow') {
        logger.warn(TAG, `监督待核 · 评分: ${report.score} · 建议: ${report.recommendations.join(', ')}`);
        return;
      }

      // 🔴 红线 — 触发告警
      if (report.audit === 'red') {
        logger.error(TAG, `监督红线触发 · 评分: ${report.score} · 建议: ${report.recommendations.join(', ')}`);
        this.onRedlineTriggered(report);
      }
    } catch (err) {
      logger.error(TAG, `监督循环异常: ${JSON.stringify(err)}`);
    }
  }

  private onRedlineTriggered(report: SupervisionReport): void {
    // 存储红线事件
    const store = globalThis.abilityContext.getApplicationContext().getDatabaseDir();
    // 发布告警事件（供分布式同步或其他模块消费）
    const event: Record<string, Object> = {
      type: 'LONGHUN_REDLINE',
      timestamp: Date.now(),
      report: JSON.stringify(report),
    };
    try {
      // @ts-ignore: emit 方法在事件总线中定义
      if (globalThis.eventHub) {
        globalThis.eventHub.emit('supervision:redline', event);
      }
    } catch (err) {
      logger.error(TAG, '发布红线事件失败');
    }
  }

  private async requestContinuousTask(): Promise<void> {
    // 鸿蒙长时任务申请
    const wantAgentInfo: wantAgent.WantAgentInfo = {
      wants: [{
        bundleName: 'com.longhun.harmonyos',
        abilityName: 'LonghunSupervisionAbility',
      }],
      operationType: wantAgent.OperationType.START_ABILITY,
      requestCode: 0,
    };
    const wantAg = await wantAgent.getWantAgent(wantAgentInfo);
    await backgroundTaskManager.startBackgroundRunning(
      globalThis.abilityContext,
      backgroundTaskManager.BackgroundMode.DATA_TRANSFER,
      wantAg
    );
  }
}
