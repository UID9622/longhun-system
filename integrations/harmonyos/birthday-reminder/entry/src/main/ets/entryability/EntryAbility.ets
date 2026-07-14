/*
 * ==========================================================================
 * 龍魂 · EntryAbility · 生日提醒
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-ENTRY-ABILITY-v2.0
 * ==========================================================================
 */

import { UIAbility, Want, AbilityConstant } from '@kit.AbilityKit';
import { window } from '@kit.ArkUI';
import { NotificationManager } from '../managers/NotificationManager';
import { MASTER_DNA, MASTER_UID } from '../common/types';

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    console.info(`[龍魂生日提醒] EntryAbility onCreate`);
    console.info(`[龍魂生日提醒] DNA: ${MASTER_DNA}`);
    console.info(`[龍魂生日提醒] UID: ${MASTER_UID}`);

    // 请求通知权限
    NotificationManager.requestPermission();
  }

  onDestroy(): void {
    console.info('[龍魂生日提醒] EntryAbility onDestroy');
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.loadContent('pages/BirthdayReminderPage', (err) => {
      if (err.code) {
        console.error(`[龍魂生日提醒] 加载页面失败: ${JSON.stringify(err)}`);
        return;
      }
      console.info('[龍魂生日提醒] 生日提醒主页面已加载');
    });

    windowStage.getMainWindow().then((win) => {
      win.setWindowBackgroundColor('#0a0a0a');
    });
  }

  onWindowStageDestroy(): void {
    console.info('[龍魂生日提醒] onWindowStageDestroy');
  }

  onForeground(): void {
    console.info('[龍魂生日提醒] onForeground');
  }

  onBackground(): void {
    console.info('[龍魂生日提醒] onBackground');
  }
}
