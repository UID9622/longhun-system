// entry/src/main/ets/components/RoundedCard.ets
// 龍魂 · 圆角卡片组件 · Clip圆角矩形裁剪

import { clipState, ClipConfig, ClipType } from '../models/ClipModel';

@Component
export struct RoundedCard {
  @Prop radius: number = 12;
  @Prop topRadius?: number;
  @Prop bottomRadius?: number;
  @Prop backgroundColor: string = '#1a1a1a';
  @Prop borderColor: string = '#333';
  @Prop borderWidth: number = 1;
  @Prop padding: Padding = { top: 16, bottom: 16, left: 16, right: 16 };
  @Prop shadow?: ShadowOptions;
  @BuilderParam contentBuilder: () => void;

  private getClipRadius(): [number, number, number, number] {
    const tr = this.topRadius ?? this.radius;
    const br = this.bottomRadius ?? this.radius;
    return [tr, tr, br, br];
  }

  aboutToAppear() {
    const [tl, tr, bl, br] = this.getClipRadius();
    const config = new ClipConfig({
      type: ClipType.ROUNDED_RECT,
      params: { topLeft: tl, topRight: tr, bottomLeft: bl, bottomRight: br },
      name: 'RoundedCard'
    });
    clipState.addConfig(config);
  }

  build() {
    Column() {
      this.contentBuilder()
    }
    .width('100%')
    .padding(this.padding)
    .backgroundColor(this.backgroundColor)
    .border({
      width: this.borderWidth,
      color: this.borderColor,
      radius: {
        topLeft: this.getClipRadius()[0],
        topRight: this.getClipRadius()[1],
        bottomLeft: this.getClipRadius()[2],
        bottomRight: this.getClipRadius()[3]
      }
    })
    .clip(new RoundedRect({
      topLeft: this.getClipRadius()[0],
      topRight: this.getClipRadius()[1],
      bottomLeft: this.getClipRadius()[2],
      bottomRight: this.getClipRadius()[3]
    }))
    .shadow(this.shadow || { radius: 8, color: 'rgba(0,0,0,0.3)', offsetY: 4 })
  }
}
