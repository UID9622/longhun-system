// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'

/**
 * 龍魂·指尖 — 系统状态卡片
 */
@Component
export struct StatusCard {
  @Prop label: string = ''
  @Prop value: string = ''
  @Prop unit: string = ''
  @Prop percent: number = 0
  @Prop color: string = Constants.COLORS.GREEN
  @Prop icon: string = ''

  build() {
    Column() {
      // 图标 + 数值
      Row() {
        if (this.icon) {
          Text(this.icon)
            .fontSize(16)
            .margin({ right: 4 })
        }
        Text(this.value)
          .fontSize(22)
          .fontColor(this.color)
          .fontWeight(FontWeight.Bold)
          .fontFamily('sans-serif-medium')

        if (this.unit) {
          Text(this.unit)
            .fontSize(12)
            .fontColor(Constants.COLORS.TEXT_SECONDARY)
            .margin({ left: 2 })
        }
      }

      // 进度条
      if (this.percent > 0) {
        Progress({
          value: Math.min(this.percent, 100),
          total: 100,
          type: ProgressType.Linear
        })
          .width('100%')
          .height(3)
          .color(this.percent > 80 ? Constants.COLORS.RED : this.percent > 60 ? Constants.COLORS.GOLD : this.color)
          .backgroundColor(Constants.COLORS.BORDER)
          .margin({ top: 6, bottom: 4 })
      }

      // 标签
      Text(this.label)
        .fontSize(10)
        .fontColor(Constants.COLORS.TEXT_SECONDARY)
        .maxLines(1)
    }
    .width('45%')
    .padding(12)
    .backgroundColor(Constants.COLORS.BG_CARD)
    .borderRadius(10)
    .border({ width: 1, color: Constants.COLORS.BORDER })
  }
}
