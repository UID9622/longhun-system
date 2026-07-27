// DNA: #龍芯⚡️丙午·癸未·甲子·既济-编辑器落地-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'

/**
 * AI协同调度按钮栏
 *
 * 四个按钮对应四种AI协作模式：
 * 1. 🤖 代码     — P04鲁班+P02宝宝 → /api/v1/guanlan/infer
 * 2. ✍️ 文案     — P11李白+P00文心 → /api/v1/guanlan/infer
 * 3. 🔍 审查     — P03雯雯+S1法律引擎 → /api/v1/audit/submit
 * 4. ⚡ 路由     — P01诸葛亮+八门路由 → /api/v1/antenna/route
 */
@Component
export struct AiToolbar {
  @Prop isProcessing: boolean = false
  @Prop activeButton: string = ''
  onButtonClick?: (task: string) => void

  build() {
    Column() {
      // ── 标题行 ──
      Row() {
        Text('🤖 AI军团')
          .fontSize(13)
          .fontColor(Constants.COLORS.GOLD)
          .fontWeight(FontWeight.Bold)

        Blank()

        if (this.isProcessing) {
          Row() {
            LoadingProgress()
              .width(14)
              .height(14)
              .color(Constants.COLORS.GOLD)
            Text('推理中...')
              .fontSize(11)
              .fontColor(Constants.COLORS.GOLD)
              .margin({ left: 4 })
          }
        }
      }
      .width('100%')
      .margin({ bottom: 8 })

      // ── 四按钮网格 ──
      Grid() {
        GridItem() { this.buildButton(0) }
        GridItem() { this.buildButton(1) }
        GridItem() { this.buildButton(2) }
        GridItem() { this.buildButton(3) }
      }
      .columnsTemplate('1fr 1fr 1fr 1fr')
      .columnsGap(8)
      .rowsGap(6)
      .width('100%')
      .height(72)
    }
    .width('100%')
    .padding({ left: 12, right: 12, top: 8, bottom: 8 })
  }

  @Builder
  buildButton(index: number) {
    const btn = Constants.AI_BUTTONS[index]
    const isActive = this.activeButton === btn.task
    const btnDisabled = this.isProcessing

    Column() {
      Text(btn.icon)
        .fontSize(18)
        .opacity(btnDisabled ? 0.4 : 1)
      Text(btn.label)
        .fontSize(10)
        .fontColor(isActive ? Constants.COLORS.GOLD : Constants.COLORS.TEXT_SECONDARY)
        .opacity(btnDisabled ? 0.4 : 1)
        .margin({ top: 2 })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .backgroundColor(isActive
      ? 'rgba(255, 215, 0, 0.12)'
      : 'rgba(255, 215, 0, 0.04)')
    .borderRadius(8)
    .border({ width: 1, color: isActive
      ? Constants.COLORS.GOLD
      : Constants.COLORS.BORDER })
    .onClick(() => {
      if (!btnDisabled && this.onButtonClick) {
        this.onButtonClick(btn.task)
      }
    })
    .onTouch((event: TouchEvent) => {
      // 长按显示提示（personas信息在Constants.AI_BUTTONS中）
    })
  }
}
