/**
 * 主权印章组件 — 暗金主题
 * License: MulanPSL v2
 */
import { SOVEREIGNTY, DARK_GOLD } from '../models/Constants';

@Component
export struct SovereigntySeal {
  @Prop dna: string;
  @Prop creator: string;
  @Prop timestamp: string;

  build() {
    Column() {
      // 主权标记
      Text(`${SOVEREIGNTY.SHIELD}${SOVEREIGNTY.FLAG}${SOVEREIGNTY.SCALE}`)
        .fontSize(20)
        .fontColor(DARK_GOLD.PRIMARY)
        .margin({ bottom: 4 })

      // 创建者
      Text(SOVEREIGNTY.CREATOR)
        .fontSize(10)
        .fontColor(DARK_GOLD.TEXT_SECONDARY)
        .fontFamily('LonghunFont')

      // DNA
      Text(this.dna)
        .fontSize(9)
        .fontColor(DARK_GOLD.PRIMARY)
        .fontFamily('monospace')
        .maxLines(1)
        .textOverflow({ overflow: TextOverflow.Ellipsis })

      // 时间戳
      Text(this.timestamp)
        .fontSize(8)
        .fontColor(DARK_GOLD.TEXT_SECONDARY)
        .margin({ top: 4 })

      Divider()
        .color(DARK_GOLD.BORDER)
        .margin({ top: 4, bottom: 4 })

      // 确认码
      Text(SOVEREIGNTY.CONFIRM_CODE.substring(0, 30) + '...')
        .fontSize(7)
        .fontColor(DARK_GOLD.TEXT_SECONDARY)
    }
    .padding(12)
    .backgroundColor(DARK_GOLD.BG_CARD)
    .borderRadius(8)
    .border({ width: 1, color: DARK_GOLD.BORDER })
    .alignItems(HorizontalAlign.Center)
  }
}
