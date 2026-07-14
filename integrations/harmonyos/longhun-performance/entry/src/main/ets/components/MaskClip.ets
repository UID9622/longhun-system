// entry/src/main/ets/components/MaskClip.ets
// 龍魂 · 蒙版渐变裁剪组件 · 渐变消失效果

import { clipState, ClipConfig, ClipType } from '../models/ClipModel';

@Component
export struct MaskClip {
  @BuilderParam contentBuilder: () => void;
  @Prop direction: 'top' | 'bottom' | 'left' | 'right' = 'bottom';
  @Prop fadeLength: number = 60;     // 渐变长度
  @Prop fadeColor: string = '#0a0a0a'; // 渐变目标色

  @State private containerWidth: number = 0;
  @State private containerHeight: number = 0;

  aboutToAppear() {
    const config = new ClipConfig({
      type: ClipType.MASK,
      name: 'MaskClip'
    });
    clipState.addConfig(config);
  }

  build() {
    Stack() {
      // 内容层
      this.contentBuilder()

      // 渐变蒙版层
      this.MaskGradientBuilder()
    }
    .width('100%')
    .height('100%')
    .onAreaChange((oldArea, newArea) => {
      this.containerWidth = newArea.width as number;
      this.containerHeight = newArea.height as number;
    })
  }

  @Builder
  MaskGradientBuilder() {
    // 根据方向创建渐变蒙版
    if (this.direction === 'bottom') {
      Column() {
        Row().height('100%').layoutWeight(1).backgroundColor('rgba(0,0,0,0)')
        Row().height(this.fadeLength).width('100%').backgroundColor(this.fadeColor)
      }
      .width('100%')
      .height('100%')
    } else if (this.direction === 'top') {
      Column() {
        Row().height(this.fadeLength).width('100%').backgroundColor(this.fadeColor)
        Row().height('100%').layoutWeight(1).backgroundColor('rgba(0,0,0,0)')
      }
      .width('100%')
      .height('100%')
    } else if (this.direction === 'right') {
      Row() {
        Column().width('100%').layoutWeight(1).backgroundColor('rgba(0,0,0,0)')
        Column().width(this.fadeLength).height('100%').backgroundColor(this.fadeColor)
      }
      .width('100%')
      .height('100%')
    } else {
      Row() {
        Column().width(this.fadeLength).height('100%').backgroundColor(this.fadeColor)
        Column().width('100%').layoutWeight(1).backgroundColor('rgba(0,0,0,0)')
      }
      .width('100%')
      .height('100%')
    }
  }
}
