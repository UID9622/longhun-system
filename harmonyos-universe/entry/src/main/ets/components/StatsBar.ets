// 龍魂路径宇宙 · 底部统计栏
// UID9622 | 龍芯北辰 | 2026-07-18

@Component
export struct StatsBar {
  @Prop sampleCount: number = 5000
  @Prop totalPaths: number = 16588800

  build() {
    Row() {
      Text(`采样: ${this.sampleCount.toLocaleString()} / ${this.totalPaths.toLocaleString()}`)
        .fontSize(10)
        .fontColor('#888')
      Blank()
      Text('UID9622 | 龍芯北辰')
        .fontSize(10)
        .fontColor('#444')
    }
    .width('100%')
    .padding(10)
    .backgroundColor('rgba(0,0,0,0.9)')
  }
}
