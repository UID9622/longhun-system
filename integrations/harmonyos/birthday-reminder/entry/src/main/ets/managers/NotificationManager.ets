/*
 * ==========================================================================
 * 龍魂 · 通知管理器（增强版）
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-NOTIFICATION-v2.0
 * ==========================================================================
 * 增强：人格联动通知模板 + 关系感知提醒 + 农历支持
 */

import { notificationManager } from '@kit.NotificationKit';
import { TeamMember } from '../models/BirthdayModel';
import { BlessingGenerator } from '../engines/BlessingGenerator';
import {
  MASTER_UID,
  NotificationPriority,
  PersonaID
} from '../common/types';

export class NotificationManager {

  // ═══════════════════════════════════════════════
  // 请求权限
  // ═══════════════════════════════════════════════
  static async requestPermission(): Promise<boolean> {
    try {
      return await notificationManager.requestEnableNotification();
    } catch (err) {
      console.error('[生日提醒] 请求通知权限失败', err);
      return false;
    }
  }

  // ═══════════════════════════════════════════════
  // 为所有成员批量设置提醒
  // ═══════════════════════════════════════════════
  static async scheduleAll(members: TeamMember[]): Promise<void> {
    try {
      await notificationManager.cancelAllNotifications();

      for (const member of members) {
        await this.scheduleForMember(member);
      }

      console.info(`[生日提醒] 已为 ${members.length} 位成员设置提醒`);
    } catch (err) {
      console.error('[生日提醒] 批量设置提醒失败', err);
    }
  }

  // ═══════════════════════════════════════════════
  // 为单个成员设置提醒
  // ═══════════════════════════════════════════════
  private static async scheduleForMember(member: TeamMember): Promise<void> {
    const nextBirthday = member.getNextBirthday();
    const priority = member.getNotificationPriority();

    // 当天提醒（上午9点）
    if (priority === 'high') {
      await this.publishNotification(
        `today-${member.id}`,
        `🎂 今天 ${member.name} 过生日！`,
        `快给${member.name}送上生日祝福吧！`,
        this.getTimeToday(9, 0)
      );
    }

    // 提前一天提醒
    const remindDate = new Date(nextBirthday);
    remindDate.setDate(remindDate.getDate() - 1);
    remindDate.setHours(9, 0, 0, 0);

    await this.publishNotification(
      `remind-${member.id}`,
      `🎂 ${member.name} 明天过生日`,
      `${member.department} · ${member.role} · ${member.getRelationshipLabel()}`,
      remindDate.getTime()
    );

    // 7天内提醒（仅 warm 关系）
    if (['close', 'mate'].includes(member.relationship)) {
      const weekAhead = new Date(nextBirthday);
      weekAhead.setDate(weekAhead.getDate() - 7);
      weekAhead.setHours(9, 0, 0, 0);

      await this.publishNotification(
        `early-${member.id}`,
        `📅 7天后 ${member.name} 过生日`,
        `提前准备一份特别的祝福吧~`,
        weekAhead.getTime()
      );
    }
  }

  // ═══════════════════════════════════════════════
  // 发送通知
  // ═══════════════════════════════════════════════
  private static async publishNotification(
    id: string,
    title: string,
    text: string,
    deliveryTime: number
  ): Promise<void> {
    try {
      const hashId = this.stringToHash(id);
      const request: notificationManager.NotificationRequest = {
        id: hashId,
        content: {
          notificationContentType: notificationManager.ContentType.NOTIFICATION_CONTENT_BASIC_TEXT,
          normal: {
            title: title,
            text: text,
            additionalText: `龍魂生日提醒 · UID${MASTER_UID}`
          }
        },
        notificationSlotType: notificationManager.SlotType.SOCIAL_COMMUNICATION,
        deliveryTime: deliveryTime,
        tapDismissed: true
      };

      await notificationManager.publish(request);
    } catch (err) {
      console.error(`[生日提醒] 发布通知失败 id=${id}`, err);
    }
  }

  // ═══════════════════════════════════════════════
  // 立即发送测试通知
  // ═══════════════════════════════════════════════
  static async sendTestNotification(): Promise<void> {
    await this.publishNotification(
      'test-notification',
      '🐉 龍魂生日提醒已就绪',
      '系统已启动，将为您监控团队成员生日。',
      Date.now() + 3000
    );
  }

  // ═══════════════════════════════════════════════
  // 取消所有提醒
  // ═══════════════════════════════════════════════
  static async cancelAll(): Promise<void> {
    try {
      await notificationManager.cancelAllNotifications();
    } catch (err) {
      console.error('[生日提醒] 取消所有通知失败', err);
    }
  }

  // ── 辅助 ──
  private static getTimeToday(hour: number, minute: number): number {
    const now = new Date();
    const target = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hour, minute, 0);
    // 如果今天已过该时间，设为明天
    if (target.getTime() < now.getTime()) {
      target.setDate(target.getDate() + 1);
    }
    return target.getTime();
  }

  private static stringToHash(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const chr = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + chr;
      hash |= 0;
    }
    return Math.abs(hash);
  }
}
