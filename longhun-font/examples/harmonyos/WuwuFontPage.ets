// 龍魂·六层来源链 / LongHun Six-Layer Source Chain
// DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-WUWU-HARMONYOS-v1.0

// 女娲五彩石渲染 —— HarmonyOS ArkTS 示例
// 原理：把字符串拆成单个字符，每个 Span 按 index % 5 循环取色。
// 色卡硬编码，主权声明，不随系统主题变化。

@Entry
@Component
struct WuwuFontPage {
  // 女娲五彩石色卡（硬编码，主权声明）
  private colorPalette: ResourceColor[] = ['#FF0000', '#FFFF00', '#00FFFF', '#FFFFFF', '#000000'];
  // 主权文字
  private sovereignText: string = '文化主权字体，女娲五彩石渲染';

  build() {
    Column() {
      Text() {
        ForEach(Array.from(this.sovereignText), (char: string, index: number) => {
          Span(char)
            .fontColor(this.colorPalette[index % 5])
            .fontSize(20)
            .fontWeight(FontWeight.Bold)
        })
      }
      .margin({ top: 20 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
  }
}
