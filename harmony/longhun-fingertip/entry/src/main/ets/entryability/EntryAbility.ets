// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import UIAbility from '@ohos.app.ability.UIAbility'
import window from '@ohos.window'
import { Constants } from '../utils/Constants'

/**
 * 龍魂·指尖 — 应用入口
 * 龍魂帝国鸿蒙第一步：掌心对话
 */
export default class EntryAbility extends UIAbility {

  onCreate(want: Record<string, Object>, launchParam: Record<string, Object>): void {
    console.info(`[龍魂·指尖] 启动 — DNA: ${Constants.DNA_PREFIX}丙午·癸未·甲子·既济-HM-指尖-v1.0`)
    console.info(`[龍魂·指尖] UID: ${Constants.UID}`)
    console.info(`[龍魂·指尖] 确认: ${Constants.CONFIRM_CODE.substring(0, 20)}...`)
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    // 加载主页面
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        console.error(`[龍魂·指尖] 页面加载失败: ${JSON.stringify(err)}`)
        return
      }
      console.info('[龍魂·指尖] 页面加载成功 · 21人格准备就绪')
    })

    // 设置窗口样式
    windowStage.getMainWindow().then((win: window.Window) => {
      win.setWindowBackgroundColor('#0a0a0a')
    })
  }

  onForeground(): void {
    console.info('[龍魂·指尖] 前台恢复')
  }

  onBackground(): void {
    console.info('[龍魂·指尖] 进入后台 — 缓存已保存')
  }

  onWindowStageDestroy(): void {
    console.info('[龍魂·指尖] 窗口销毁 — 龍魂永存')
  }

  onDestroy(): void {
    console.info('[龍魂·指尖] 应用退出 — 🧬 DNA离线缓存已保留')
  }
}
