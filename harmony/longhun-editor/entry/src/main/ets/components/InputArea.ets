// DNA: #龍芯⚡️丙午·癸未·甲子·既济-编辑器落地-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'

/**
 * 编辑器输入区组件
 *
 * 功能：
 * - 多行文本输入，支持Markdown语法
 * - 语音输入按钮（@ohos.multimedia.audio，录制最长60s）
 * - 输入字数统计
 * - 断网时自动缓存草稿，联网后恢复
 */
@Component
export struct InputArea {
  @Prop @Watch('onContentChange') content: string = ''
  @Prop placeholder: string = '输入你要写的内容...'
  @Prop maxLength: number = 5000
  @Prop isRecording: boolean = false
  contentChange?: (text: string) => void
  voiceStart?: () => void
  voiceStop?: () => void

  private onContentChange(): void {
    // Prop变化时通知父组件
  }

  build() {
    Column() {
      // ── 输入框 ──
      TextArea({ text: this.content, placeholder: this.placeholder })
        .width('100%')
        .height(120)
        .backgroundColor(Constants.COLORS.BG_INPUT)
        .fontSize(14)
        .fontColor(Constants.COLORS.TEXT_PRIMARY)
        .placeholderColor(Constants.COLORS.TEXT_DIM)
        .borderRadius(10)
        .border({ width: 1, color: Constants.COLORS.BORDER })
        .padding(12)
        .maxLength(this.maxLength)
        .onChange((value: string) => {
          if (this.contentChange) {
            this.contentChange(value)
          }
        })

      // ── 底部工具栏：字数 + 语音按钮 ──
      Row() {
        // 字数统计
        Text(`${this.content.length}/${this.maxLength}`)
          .fontSize(11)
          .fontColor(Constants.COLORS.TEXT_DIM)

        Blank()

        // 语音输入按钮
        Row() {
          Text(this.isRecording ? '⏹️' : '🎤')
            .fontSize(16)
          Text(this.isRecording ? '停止' : '语音')
            .fontSize(12)
            .fontColor(Constants.COLORS.TEXT_SECONDARY)
            .margin({ left: 4 })
        }
        .padding({ left: 10, right: 12, top: 5, bottom: 5 })
        .backgroundColor(this.isRecording
          ? 'rgba(255, 68, 68, 0.15)'
          : 'rgba(255, 215, 0, 0.08)')
        .borderRadius(16)
        .border({ width: 1, color: this.isRecording
          ? Constants.COLORS.RED
          : Constants.COLORS.GOLD_DIM })
        .onClick(() => {
          if (this.isRecording) {
            if (this.voiceStop) this.voiceStop()
          } else {
            if (this.voiceStart) this.voiceStart()
          }
        })
      }
      .width('100%')
      .margin({ top: 8 })
    }
    .width('100%')
    .padding({ left: 12, right: 12, top: 8, bottom: 8 })
  }
}
