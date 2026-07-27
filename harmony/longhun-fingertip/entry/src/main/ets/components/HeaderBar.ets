// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'

/**
 * 龍魂·指尖 — 头部导航栏
 */
@Component
export struct HeaderBar {
  @Prop title: string = '龍魂·指尖'
  @Prop subtitle: string = '掌心21人格对话'
  @Prop showDna: boolean = true
  @Prop connectionColor: string = Constants.COLORS.GREEN

  build() {
    Row() {
      // 左侧: 状态指示灯 + 标题
      Row() {
        // 连接指示灯
        Circle({ width: 8, height: 8 })
          .fill(this.connectionColor)
          .margin({ right: 8 })

        Column() {
          Text(`🐉 ${this.title}`)
            .fontSize(18)
            .fontColor(Constants.COLORS.GOLD)
            .fontWeight(FontWeight.Bold)
            .fontFamily('sans-serif-medium')

          Text(this.subtitle)
            .fontSize(10)
            .fontColor(Constants.COLORS.TEXT_SECONDARY)
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
        }
        .alignItems(HorizontalAlign.Start)
      }

      Blank()

      // 右侧: DNA码
      if (this.showDna) {
        Text(`${Constants.DNA_PREFIX}丙午·癸未·甲子·既济-HM-指尖`)
          .fontSize(8)
          .fontColor(Constants.COLORS.GOLD_DIM)
          .maxLines(1)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
          .width(120)
          .textAlign(TextAlign.End)
      }
    }
    .width('100%')
    .height(48)
    .padding({ left: 16, right: 12 })
    .backgroundColor(Constants.COLORS.BG_PRIMARY)
    .border({ width: { bottom: 1 }, color: Constants.COLORS.BORDER })
  }
}
