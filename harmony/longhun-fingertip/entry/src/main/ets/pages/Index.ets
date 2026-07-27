// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'
import { ChatPage } from './ChatPage'
import { StatusPage } from './StatusPage'
import { DnaPage } from './DnaPage'
import { OfflinePage } from './OfflinePage'
import { SettingsPage } from './SettingsPage'

/**
 * 龍魂·指尖 v1.1 — 主页 (Tab容器)
 * 五标签: 对话 / 状态 / DNA / 离线 / 设置
 *
 * v1.1变更：新增离线模式标签页
 */
@Entry
@Component
struct Index {
  @State currentTab: number = 0
  private tabTitles: string[] = ['对话', '状态', 'DNA', '离线', '设置']
  private tabIcons: string[] = ['💬', '📊', '🧬', '📡', '⚙️']

  build() {
    Column() {
      // 内容区
      if (this.currentTab === 0) {
        ChatPage()
      } else if (this.currentTab === 1) {
        StatusPage()
      } else if (this.currentTab === 2) {
        DnaPage()
      } else if (this.currentTab === 3) {
        OfflinePage()
      } else {
        SettingsPage()
      }

      // 底部Tab栏 —— 龍魂金风格
      Row() {
        ForEach([0, 1, 2, 3, 4], (index: number) => {
          Column() {
            Text(this.tabIcons[index])
              .fontSize(18)
              .margin({ bottom: 1 })
            Text(this.tabTitles[index])
              .fontSize(9)
              .fontColor(this.currentTab === index
                ? Constants.COLORS.GOLD
                : Constants.COLORS.TEXT_SECONDARY)
          }
          .width('20%')
          .padding({ top: 4, bottom: 4 })
          .onClick(() => { this.currentTab = index })
          .backgroundColor(this.currentTab === index
            ? 'rgba(255, 215, 0, 0.06)'
            : 'transparent')
          .borderRadius(8)
        })
      }
      .width('100%')
      .height(52)
      .backgroundColor(Constants.COLORS.BG_PRIMARY)
      .border({ width: { top: 1 }, color: Constants.COLORS.BORDER })
      .padding({ bottom: 4 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Constants.COLORS.BG_PRIMARY)
  }
}
