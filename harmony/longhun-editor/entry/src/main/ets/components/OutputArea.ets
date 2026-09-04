// DNA: #龍芯⚡️丙午·癸未·甲子·既济-编辑器落地-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'
import { EditorOutput } from '../service/ApiClient'

/**
 * 编辑器输出展示区组件
 *
 * 分栏布局：
 * 1. 主输出区 — AI回复内容（Markdown渲染）
 * 2. 协同过程日志 — 折叠展示哪些人格参与了
 * 3. DNA追溯标签 — 底部DNA标签
 * 4. 审计等级徽章 — 右下角L0/L1/L2/L3徽章
 */
@Component
export struct OutputArea {
  @Prop output: EditorOutput = new EditorOutput()
  @Prop isExpanded: boolean = false
  toggleExpand?: () => void

  /** 审计等级徽章颜色 */
  private auditBadgeColor(level: string): string {
    switch (level) {
      case 'L0': return '#FF0000'  // 红线
      case 'L1': return '#FF4444'  // 严重
      case 'L2': return '#FFD700'  // 警告
      case 'L3': return '#00FF88'  // 正常
      default: return Constants.COLORS.TEXT_DIM
    }
  }

  /** 审计等级中文 */
  private auditLevelName(level: string): string {
    switch (level) {
      case 'L0': return '∞红线'
      case 'L1': return '严重'
      case 'L2': return '关注'
      case 'L3': return '正常'
      default: return level
    }
  }

  build() {
    Column() {
      // ── 空态 ──
      if (this.output.result.length === 0 && !this.output.isError) {
        Column() {
          Text('🤖')
            .fontSize(40)
            .opacity(0.3)
          Text('AI军团回复将在此展示')
            .fontSize(13)
            .fontColor(Constants.COLORS.TEXT_DIM)
            .margin({ top: 8 })
        }
        .width('100%')
        .height(160)
        .justifyContent(FlexAlign.Center)
        .backgroundColor(Constants.COLORS.BG_CARD)
        .borderRadius(10)
        .border({ width: 1, color: Constants.COLORS.BORDER, style: BorderStyle.Dashed })
        return
      }

      // ── 错误态 ──
      if (this.output.isError) {
        Column() {
          Text('⚠️')
            .fontSize(28)
          Text(this.output.errorMessage)
            .fontSize(13)
            .fontColor(Constants.COLORS.RED)
            .textAlign(TextAlign.Center)
            .margin({ top: 6 })
        }
        .width('100%')
        .padding(20)
        .backgroundColor('rgba(255, 68, 68, 0.08)')
        .borderRadius(10)
        .border({ width: 1, color: Constants.COLORS.RED })
        return
      }

      // ══════ 主输出 ══════
      Column() {
        // 策略+人格标签
        Row() {
          Text(this.output.task)
            .fontSize(11)
            .fontColor(Constants.COLORS.GOLD)
            .padding({ left: 8, right: 8, top: 2, bottom: 2 })
            .backgroundColor('rgba(255, 215, 0, 0.1)')
            .borderRadius(4)

          Text(this.output.personas)
            .fontSize(10)
            .fontColor(Constants.COLORS.TEXT_SECONDARY)
            .margin({ left: 8 })
        }
        .width('100%')
        .margin({ bottom: 8 })

        // AI回复内容
        Text(this.output.result)
          .fontSize(14)
          .fontColor(Constants.COLORS.TEXT_PRIMARY)
          .lineHeight(22)
          .width('100%')
          .padding(12)
          .backgroundColor(Constants.COLORS.BG_INPUT)
          .borderRadius(8)
          .textAlign(TextAlign.Start)

        // ══════ 协同过程日志（可折叠） ══════
        Column() {
          // 折叠头部
          Row() {
            Text('🔄 协同过程')
              .fontSize(12)
              .fontColor(Constants.COLORS.GOLD)

            Blank()

            Text(this.isExpanded ? '▲' : '▼')
              .fontSize(12)
              .fontColor(Constants.COLORS.TEXT_DIM)
          }
          .width('100%')
          .padding({ left: 10, right: 10, top: 8, bottom: 8 })
          .backgroundColor('rgba(255, 215, 0, 0.04)')
          .borderRadius(8)
          .onClick(() => {
            if (this.toggleExpand) this.toggleExpand()
          })

          // 展开的过程日志
          if (this.isExpanded && this.output.processLog.length > 0) {
            Column() {
              ForEach(this.output.processLog, (log: string, index: number) => {
                Row() {
                  Text(`${index + 1}.`)
                    .fontSize(11)
                    .fontColor(Constants.COLORS.TEXT_DIM)
                    .width(20)
                  Text(log)
                    .fontSize(12)
                    .fontColor(Constants.COLORS.TEXT_SECONDARY)
                    .layoutWeight(1)
                }
                .width('100%')
                .padding({ left: 10, right: 10, top: 4, bottom: 4 })
              })
            }
            .width('100%')
            .margin({ top: 4 })
          }
        }
        .width('100%')
        .margin({ top: 10 })
        .border({ width: 1, color: Constants.COLORS.BORDER, radius: 8 })

        // ══════ 底部栏：DNA标签 + 审计徽章 ══════
        Row() {
          // DNA追溯标签
          Row() {
            Text('🧬')
              .fontSize(12)
            Text(this.output.dna)
              .fontSize(10)
              .fontColor(Constants.COLORS.TEXT_DIM)
              .maxLines(1)
              .textOverflow({ overflow: TextOverflow.Ellipsis })
              .margin({ left: 4 })
          }
          .padding({ left: 8, right: 8, top: 3, bottom: 3 })
          .backgroundColor('rgba(255, 215, 0, 0.05)')
          .borderRadius(4)
          .flexShrink(1)

          Blank()

          // 审计等级徽章
          Row() {
            Text(`🛡️ ${this.auditLevelName(this.output.auditLevel)}`)
              .fontSize(11)
              .fontColor(this.auditBadgeColor(this.output.auditLevel))
          }
          .padding({ left: 8, right: 8, top: 3, bottom: 3 })
          .backgroundColor(`${this.auditBadgeColor(this.output.auditLevel)}15`)
          .borderRadius(4)
          .border({ width: 1, color: this.auditBadgeColor(this.output.auditLevel) + '44' })
        }
        .width('100%')
        .margin({ top: 10 })
      }
      .width('100%')
      .padding(12)
      .backgroundColor(Constants.COLORS.BG_CARD)
      .borderRadius(10)
      .border({ width: 1, color: Constants.COLORS.BORDER })
    }
    .width('100%')
    .padding({ left: 12, right: 12, top: 4, bottom: 4 })
  }
}
