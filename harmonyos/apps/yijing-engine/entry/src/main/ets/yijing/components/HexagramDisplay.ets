/**
 * 🐉 龙魂·卦象绘制组件
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-HEXAGRAM-DISPLAY-v1.0
 * License: MulanPSL v2
 * 创建者: 诸葛鑫（UID9622）
 */
@Component
export struct HexagramDisplay {
  @Prop symbol: string = '䷀';
  @Prop hexagramName: string = '乾';
  @Prop upperName: string = '☰乾';
  @Prop lowerName: string = '☰乾';

  build() {
    Column() {
      Text(this.symbol)
        .fontSize(64).fontColor('#D4AF37')
        .margin({ top: 8, bottom: 4 })

      Text(this.hexagramName)
        .fontSize(22).fontColor('#D4AF37').fontWeight(FontWeight.Bold)
        .margin({ bottom: 4 })

      Text(`${this.upperName}上 / ${this.lowerName}下`)
        .fontSize(13).fontColor('#A8A6A3')
    }
    .alignItems(HorizontalAlign.Center).padding(12)
  }
}
