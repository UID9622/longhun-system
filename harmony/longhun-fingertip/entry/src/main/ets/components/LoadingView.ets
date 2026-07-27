// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'

/**
 * 龍魂·指尖 — 加载动画
 */
@Component
export struct LoadingView {
  @Prop message: string = '正在连接鲲鹏...'
  @State dotCount: number = 0

  private timer?: number

  aboutToAppear(): void {
    this.timer = setInterval(() => {
      this.dotCount = (this.dotCount + 1) % 4
    }, 500)
  }

  aboutToDisappear(): void {
    if (this.timer) {
      clearInterval(this.timer)
    }
  }

  build() {
    Column() {
      // 旋转龍图标
      Text('🐉')
        .fontSize(40)
        .rotate({ angle: this.dotCount * 30 })

      // 进度点
      Text(this.message + '.'.repeat(this.dotCount))
        .fontSize(14)
        .fontColor(Constants.COLORS.GOLD)
        .margin({ top: 16 })

      // 提示
      Text('21人格集群在鲲鹏就绪中')
        .fontSize(11)
        .fontColor(Constants.COLORS.TEXT_DIM)
        .margin({ top: 8 })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
    .backgroundColor(Constants.COLORS.BG_PRIMARY)
  }
}
