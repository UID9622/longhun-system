// 龍魂路径宇宙 · 加载动画
// UID9622 | 龍芯北辰 | 2026-07-18

@Component
export struct LoadingView {

  build() {
    Column() {
      Text('🐉')
        .fontSize(60)
        .margin({ bottom: 20 })

      LoadingProgress()
        .width(60)
        .height(60)
        .color('#FFD700')

      Text('龍魂宇宙加载中...')
        .fontSize(16)
        .fontColor('#FFD700')
        .letterSpacing(2)
        .margin({ top: 20 })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .backgroundColor('#0a0a0a')
  }
}
