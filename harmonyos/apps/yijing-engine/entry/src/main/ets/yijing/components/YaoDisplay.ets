/**
 * 🐉 龙魂·爻显示组件
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-YAO-DISPLAY-v1.0
 * License: MulanPSL v2
 * 创建者: 诸葛鑫（UID9622）
 */
@Component
export struct YaoDisplay {
  @Prop isYang: boolean = true;
  @Prop isMoving: boolean = false;
  @Prop label: string = '';
  @Prop sixRelation: string = '';
  @Prop sixSpirit: string = '';
  @Prop shiYing: string = '';
  @Prop text: string = '';
  @Prop position: number = 1;

  build() {
    Row() {
      // 爻线
      Column() {
        if (this.isYang) {
          Row()
            .width(48).height(4).borderRadius(2)
            .backgroundColor(this.isMoving ? '#EF5350' : '#D4AF37')
        } else {
          Row() {
            Row().width(20).height(4).borderRadius(2).backgroundColor(this.isMoving ? '#EF5350' : '#A8A6A3')
            Row().width(8).height(4)
            Row().width(20).height(4).borderRadius(2).backgroundColor(this.isMoving ? '#EF5350' : '#A8A6A3')
          }
        }
        // 动爻标记
        if (this.isMoving) {
          Text('⚡')
            .fontSize(10).fontColor('#F44336').margin({ top: 1 })
        }
      }.margin({ left: 8, right: 8 })

      // 爻名+世应
      Column() {
        Text(this.label)
          .fontSize(14).fontColor('#D4AF37').fontWeight(FontWeight.Bold)
        if (this.shiYing) {
          Text(this.shiYing === '世' ? '⚫世' : '⚪应')
            .fontSize(10).fontColor(this.shiYing === '世' ? '#D4AF37' : '#888')
        }
      }.width(48).alignItems(HorizontalAlign.Center)

      // 六亲/六神
      Column() {
        Text(this.sixRelation || '--')
          .fontSize(12).fontColor('#E8E6E3')
        Text(this.sixSpirit || '--')
          .fontSize(11).fontColor('#888')
      }.width(56).alignItems(HorizontalAlign.Center)

      // 爻辞
      Text(this.text)
        .fontSize(11).fontColor('#A8A6A3')
        .maxLines(2).textOverflow({ overflow: TextOverflow.Ellipsis })
        .layoutWeight(1)
    }
    .width('100%').padding(8)
    .borderRadius(8).margin({ bottom: 4 })
    .backgroundColor(this.shiYing === '世' ? '#1A1A2E' : '#12121F')
    .border({ width: 1, color: this.shiYing === '世' ? '#D4AF3733' : '#2A2A3E', radius: 8 })
  }
}
