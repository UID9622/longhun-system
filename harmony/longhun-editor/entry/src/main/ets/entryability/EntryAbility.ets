// DNA: #龍芯⚡️丙午·癸未·甲子·既济-编辑器落地-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import UIAbility from '@ohos.app.ability.UIAbility'
import window from '@ohos.window'
import { Constants } from '../utils/Constants'

/**
 * 龍魂·编辑器 — 应用入口
 * AI军团协同写作·鸿蒙端侧原型
 */
export default class EntryAbility extends UIAbility {

  onCreate(want: Record<string, Object>, launchParam: Record<string, Object>): void {
    console.info(`[龍魂·编辑器] 启动 — DNA: ${Constants.DNA_PREFIX}丙午·癸未·甲子·既济-编辑器落地-v1.0`)
    console.info(`[龍魂·编辑器] UID: ${Constants.UID}`)
    console.info(`[龍魂·编辑器] 确认: ${Constants.CONFIRM_CODE.substring(0, 20)}...`)
    console.info('[龍魂·编辑器] AI军团: 文心·宝宝·鲁班·李白·雯雯·诸葛亮·法律引擎·八门路由 — 待命')
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        console.error(`[龍魂·编辑器] 页面加载失败: ${JSON.stringify(err)}`)
        return
      }
      console.info('[龍魂·编辑器] 页面加载成功 · AI军团就绪 · 四按钮可用')
    })

    windowStage.getMainWindow().then((win: window.Window) => {
      win.setWindowBackgroundColor('#0a0a0a')
    })
  }

  onForeground(): void {
    console.info('[龍魂·编辑器] 前台恢复')
  }

  onBackground(): void {
    console.info('[龍魂·编辑器] 进入后台 — 草稿已自动保存')
  }

  onWindowStageDestroy(): void {
    console.info('[龍魂·编辑器] 窗口销毁 — 龍魂永存')
  }

  onDestroy(): void {
    console.info('[龍魂·编辑器] 应用退出 — 🧬 DNA离线缓存已保留')
  }
}
