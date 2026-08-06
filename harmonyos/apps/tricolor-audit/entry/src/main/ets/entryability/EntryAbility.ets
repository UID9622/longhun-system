/**
 * 龙魂·三色审计 — EntryAbility
 * 应用入口·主权初始化
 * License: MulanPSL v2
 */
import AbilityConstant from '@ohos.app.ability.AbilityConstant';
import UIAbility from '@ohos.app.ability.UIAbility';
import Want from '@ohos.app.ability.Want';
import window from '@ohos.window';
import { SovereigntyManager } from '../engine/SovereigntyManager';
import { SOVEREIGNTY } from '../models/Constants';

export default class EntryAbility extends UIAbility {
  private sovereignty: SovereigntyManager = new SovereigntyManager();

  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    console.info(`[龍魂] EntryAbility onCreate`);
    this.initSovereignty();
  }

  async initSovereignty(): Promise<void> {
    const declaration = await this.sovereignty.generateSovereigntyDeclaration();
    console.info(`[龍魂] 主权声明: ${declaration}`);
  }

  onDestroy(): void {
    console.info(`[龍魂] EntryAbility onDestroy — 主权常驻`);
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.loadContent('pages/Index', (err, data) => {
      if (err.code) {
        console.error(`[龍魂] 加载首页失败: ${JSON.stringify(err)}`);
        return;
      }
      console.info(`[龍魂] 三色审计首页已加载`);
    });
  }

  onWindowStageDestroy(): void {}

  onForeground(): void {
    console.info(`[龍魂] 应用回到前台`);
  }

  onBackground(): void {
    console.info(`[龍魂] 应用进入后台`);
  }
}
