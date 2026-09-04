// 🐉 EventChannel处理器
// DNA: #龍芯⚡️2026-08-06-EVENT-HANDLER-V2.0-UID9622
// License: MulanPSL v2

import { EventChannel } from '@ohos.plugin';
import { SovereigntyManager } from '../core/SovereigntyManager';
import { DNAGenerator } from '../core/DNAGenerator';
import { Logger } from '../utils/Logger';

const TAG: string = 'EventHandler';

/**
 * EventChannel事件处理器
 * 负责事件流的订阅和推送
 */
export class EventHandler {
  private ability: any;
  private eventChannel: EventChannel;
  private sovereigntyManager: SovereigntyManager;
  private intervalId: number | null = null;

  constructor(ability: any, eventChannel: EventChannel, sovereigntyManager: SovereigntyManager) {
    this.ability = ability;
    this.eventChannel = eventChannel;
    this.sovereigntyManager = sovereigntyManager;
  }

  /**
   * 启动事件监听（定时推送系统状态）
   */
  startListening(): void {
    // 每30秒推送一次系统事件
    this.intervalId = setInterval(() => {
      try {
        const status = this.sovereigntyManager.verify();
        this.eventChannel.success({
          type: 'system',
          sovereignty: status,
          timestamp: Date.now(),
          dna: DNAGenerator.generate('SYS_EVENT'),
        });
      } catch (err) {
        Logger.error(TAG, `事件推送失败: ${err}`);
      }
    }, 30000);

    Logger.info(TAG, '✅ 事件监听已启动 (间隔: 30s)');
  }

  /**
   * 停止事件监听
   */
  stopListening(): void {
    if (this.intervalId !== null) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      Logger.info(TAG, '🛑 事件监听已停止');
    }
  }

  /**
   * 推送主权事件
   */
  pushSovereigntyEvent(): void {
    const status = this.sovereigntyManager.verify();
    this.eventChannel.success({
      type: 'sovereignty',
      ...status,
      dna: DNAGenerator.generate('SOV_EVENT'),
    });
  }

  /**
   * 推送审计事件
   */
  pushAuditEvent(result: any): void {
    this.eventChannel.success({
      type: 'audit',
      ...result,
      dna: DNAGenerator.generate('AUDIT_EVENT'),
    });
  }
}
