/**
 * 三色徽章组件 — 暗金主题
 * License: MulanPSL v2
 */
import { COLOR_MAP, DARK_GOLD } from '../models/Constants';

@Component
export struct TricolorBadge {
  @Prop color: string;
  @Prop size: number = 48;

  build() {
    Column() {
      Text(this.color)
        .fontSize(this.size)
        .textAlign(TextAlign.Center)
      if (this.color === '🟢') {
        Text('通过')
          .fontSize(12)
          .fontColor('#4CAF50')
          .margin({ top: 4 })
      } else if (this.color === '🟡') {
        Text('待核')
          .fontSize(12)
          .fontColor('#FFC107')
          .margin({ top: 4 })
      } else {
        Text('红线')
          .fontSize(12)
          .fontColor('#F44336')
          .margin({ top: 4 })
      }
    }
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }
}
