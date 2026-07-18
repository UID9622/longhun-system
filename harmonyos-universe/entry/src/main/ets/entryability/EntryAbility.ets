// 龍魂路径宇宙 · 入口 Ability
// UID9622 | 龍芯北辰 | 2026-07-18

import UIAbility from '@ohos.app.ability.UIAbility'
import window from '@ohos.window'
import { P0_ANCHOR } from '../utils/Constants'

export default class EntryAbility extends UIAbility {

  onCreate(want, launchParam) {
    console.info(`🐉 龍魂宇宙 EntryAbility.onCreate | DNA: ${P0_ANCHOR.confirm}`)
  }

  onDestroy() {
    console.info('🐉 龍魂宇宙 EntryAbility.onDestroy')
  }

  onWindowStageCreate(windowStage: window.WindowStage) {
    // 加载主页面
    windowStage.loadContent('pages/Index', (err, data) => {
      if (err.code) {
        console.error(`❌ 龍魂宇宙 加载失败: ${JSON.stringify(err)}`)
        return
      }
      console.info(`🐉 龍魂宇宙 页面加载成功`)
    })
  }

  onWindowStageDestroy() {
    console.info('🐉 龍魂宇宙 EntryAbility.onWindowStageDestroy')
  }

  onForeground() {
    console.info('🐉 龍魂宇宙 回到前台')
  }

  onBackground() {
    console.info('🐉 龍魂宇宙 进入后台')
  }
}
