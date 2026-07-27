// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'
import { ChatMessage } from '../models/Types'

/**
 * 龍魂·指尖 — 聊天气泡
 */
@Component
export struct ChatBubble {
  @Prop message: ChatMessage = new ChatMessage()
  @Prop isLast: boolean = false

  build() {
    Column() {
      // 头部: 角色 + 时间
      Row() {
        Text(this.getRoleLabel())
          .fontSize(11)
          .fontColor(this.message.role === 'user' ? Constants.COLORS.BLUE : Constants.COLORS.GOLD)
          .fontWeight(FontWeight.Medium)

        if (this.message.persona && this.message.role === 'assistant') {
          Text(` · ${this.message.persona}`)
            .fontSize(10)
            .fontColor(Constants.COLORS.TEXT_SECONDARY)
        }

        Blank()

        Text(this.formatTime(this.message.timestamp))
          .fontSize(9)
          .fontColor(Constants.COLORS.TEXT_DIM)
      }
      .width('100%')
      .padding({ bottom: 4 })

      // 内容气泡
      Column() {
        if (this.message.isError) {
          Text(this.message.content)
            .fontSize(14)
            .fontColor(Constants.COLORS.RED)
            .padding(12)
        } else {
          Text(this.message.content)
            .fontSize(14)
            .fontColor(this.message.role === 'user' ? Constants.COLORS.TEXT_PRIMARY : Constants.COLORS.TEXT_PRIMARY)
            .lineHeight(20)
            .padding(12)
            .textAlign(TextAlign.Start)
        }
      }
      .width('100%')
      .borderRadius(12)
      .backgroundColor(this.message.role === 'user'
        ? 'rgba(68, 136, 255, 0.1)'
        : this.message.isError
          ? 'rgba(255, 68, 68, 0.08)'
          : Constants.COLORS.BG_CARD)
      .border({
        width: 1,
        color: this.message.role === 'user'
          ? 'rgba(68, 136, 255, 0.2)'
          : this.message.isError
            ? 'rgba(255, 68, 68, 0.2)'
            : Constants.COLORS.BORDER
      })

      // DNA追踪（仅AI回复末尾）
      if (this.message.dna && this.message.role === 'assistant') {
        Text(this.message.dna)
          .fontSize(8)
          .fontColor(Constants.COLORS.GOLD_DIM)
          .padding({ top: 4, left: 4 })
          .maxLines(1)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
      }
    }
    .padding({ left: 4, right: 4, top: 6, bottom: 6 })
  }

  private getRoleLabel(): string {
    if (this.message.role === 'user') return '我'
    if (this.message.persona) return this.message.persona
    return '龍魂'
  }

  private formatTime(ts: number): string {
    const d = new Date(ts)
    const h = d.getHours().toString().padStart(2, '0')
    const m = d.getMinutes().toString().padStart(2, '0')
    return `${h}:${m}`
  }
}
