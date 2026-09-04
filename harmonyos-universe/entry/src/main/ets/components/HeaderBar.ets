// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-b8038fb5
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍魂路径宇宙 · 顶部标题栏
// UID9622 | 龍芯北辰 | 2026-07-18

@Component
export struct HeaderBar {
  @Prop title: string = '龍魂翻译引擎'
  @Prop subtitle: string = '1650万路径宇宙'

  build() {
    Row() {
      Column() {
        Text(`🐉 ${this.title}`)
          .fontSize(18)
          .fontColor('#FFD700')
          .fontWeight(FontWeight.Bold)
          .letterSpacing(2)
        Text(this.subtitle)
          .fontSize(11)
          .fontColor('#888')
          .margin({ top: 3 })
      }
      .alignItems(HorizontalAlign.Start)
    }
    .width('100%')
    .padding(15)
    .backgroundColor('rgba(0,0,0,0.9)')
  }
}
