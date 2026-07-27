// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'
import { DnaEntry } from '../models/Types'

/**
 * 龍魂·指尖 — DNA追溯卡片
 */
@Component
export struct DnaCard {
  @Prop entry: DnaEntry = new DnaEntry()
  @Prop showDetail: boolean = false

  build() {
    Column() {
      Row() {
        // 审计色标识
        Circle({ width: 10, height: 10 })
          .fill(this.getAuditColor())
          .margin({ right: 8 })

        Column() {
          Text(this.entry.module)
            .fontSize(13)
            .fontColor(Constants.COLORS.TEXT_PRIMARY)
            .fontWeight(FontWeight.Medium)
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })

          Text(this.entry.dna)
            .fontSize(9)
            .fontColor(Constants.COLORS.GOLD_DIM)
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
        }
        .alignItems(HorizontalAlign.Start)
        .layoutWeight(1)

        Column() {
          Text(this.entry.action)
            .fontSize(11)
            .fontColor(Constants.COLORS.GOLD)
            .margin({ bottom: 2 })

          if (this.entry.cached) {
            Text('💾 离线')
              .fontSize(8)
              .fontColor(Constants.COLORS.BLUE)
          } else {
            Text(this.formatDate(this.entry.timestamp))
              .fontSize(8)
              .fontColor(Constants.COLORS.TEXT_DIM)
          }
        }
        .alignItems(HorizontalAlign.End)
      }
      .width('100%')

      // 详细面板
      if (this.showDetail) {
        Divider()
          .color(Constants.COLORS.BORDER)
          .margin({ top: 8, bottom: 6 })

        Row() {
          Text(`创建者: ${this.entry.creator}`)
            .fontSize(10).fontColor(Constants.COLORS.TEXT_SECONDARY)
          Blank()
          Text(`审计: ${this.entry.audit_color}`)
            .fontSize(10).fontColor(Constants.COLORS.TEXT_SECONDARY)
        }
        .width('100%')

        if (this.entry.device_code) {
          Text(`设备: ${this.entry.device_code}`)
            .fontSize(10)
            .fontColor(Constants.COLORS.TEXT_DIM)
            .padding({ top: 2 })
        }
      }
    }
    .width('100%')
    .padding(12)
    .backgroundColor(Constants.COLORS.BG_CARD)
    .borderRadius(10)
    .border({ width: 1, color: Constants.COLORS.BORDER })
    .margin({ bottom: 8 })
  }

  private getAuditColor(): string {
    switch (this.entry.audit_color) {
      case '🟢': return Constants.COLORS.GREEN
      case '🟡': return Constants.COLORS.GOLD
      case '🔴': return Constants.COLORS.RED
      default: return Constants.COLORS.GREEN
    }
  }

  private formatDate(ts: string): string {
    try {
      const d = new Date(ts)
      const m = (d.getMonth() + 1).toString().padStart(2, '0')
      const day = d.getDate().toString().padStart(2, '0')
      return `${m}/${day}`
    } catch {
      return ts.substring(0, 10)
    }
  }
}
