/**
 * 审计结果卡片组件 — 暗金主题
 * License: MulanPSL v2
 */
import { AuditResult } from '../models/AuditModels';
import { DARK_GOLD } from '../models/Constants';

@Component
export struct AuditResultCard {
  @Prop result: AuditResult;
  @Prop onTap?: (dna: string) => void;

  build() {
    Column() {
      // 头部：三色标记 + R值 + DNA
      Row() {
        Text(this.result.color)
          .fontSize(32)
        Column() {
          Text(`R = ${this.result.rValue.toFixed(3)}`)
            .fontSize(18)
            .fontColor(DARK_GOLD.PRIMARY)
          Text(this.result.dna)
            .fontSize(10)
            .fontColor(DARK_GOLD.TEXT_SECONDARY)
            .fontFamily('monospace')
            .maxLines(1)
        }
        .layoutWeight(1)
        .margin({ left: 8 })
        .alignItems(HorizontalAlign.Start)
      }
      .width('100%')
      .padding(12)

      // 摘要
      Text(this.result.summary)
        .fontSize(13)
        .fontColor(DARK_GOLD.TEXT_PRIMARY)
        .padding({ left: 12, right: 12, bottom: 8 })
        .maxLines(3)

      // 底部信息
      Row() {
        Text(this.result.timestamp)
          .fontSize(10)
          .fontColor(DARK_GOLD.TEXT_SECONDARY)
        Text(`${this.result.elapsedMs}ms`)
          .fontSize(10)
          .fontColor(DARK_GOLD.PRIMARY)
          .margin({ left: 12 })
        Text(this.result.sovereignSeal.sovereign)
          .fontSize(9)
          .fontColor(DARK_GOLD.TEXT_SECONDARY)
          .layoutWeight(1)
          .textAlign(TextAlign.End)
      }
      .width('100%')
      .padding(12)
    }
    .width('100%')
    .backgroundColor(DARK_GOLD.BG_CARD)
    .borderRadius(10)
    .border({ width: 1, color: DARK_GOLD.BORDER })
    .margin({ bottom: 10 })
    .onClick(() => {
      if (this.onTap) {
        this.onTap(this.result.dna);
      }
    })
  }
}
