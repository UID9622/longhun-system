// entry/src/main/ets/components/CircleAvatar.ets
// 龍魂 · 圆形头像组件 · Clip圆形裁剪

import { clipState, ClipConfig, ClipType } from '../models/ClipModel';

@Component
export struct CircleAvatar {
  @Prop src: Resource | string;
  @Prop size: number = 80;
  @Prop borderWidth: number = 2;
  @Prop borderColor: string = '#c41e3a';
  @Prop placeholder: Resource = $r('app.media.ic_avatar');

  @State private isLoaded: boolean = false;
  @State private loadError: boolean = false;

  aboutToAppear() {
    // 记录裁剪配置
    const config = new ClipConfig({
      type: ClipType.CIRCLE,
      params: { circleRadius: this.size / 2 },
      name: 'CircleAvatar'
    });
    clipState.addConfig(config);
  }

  build() {
    Stack() {
      // 占位背景
      Circle()
        .width(this.size)
        .height(this.size)
        .fill('#1a1a1a')

      // 图片（圆形裁剪）
      if (!this.loadError) {
        Image(this.src)
          .width(this.size)
          .height(this.size)
          .objectFit(ImageFit.Cover)
          .clip(new Circle({ width: this.size, height: this.size }))
          .border({
            width: this.borderWidth,
            color: this.borderColor,
            radius: this.size / 2  // 边框也要圆
          })
          .onComplete(() => { this.isLoaded = true; })
          .onError(() => { this.loadError = true; })
          .opacity(this.isLoaded ? 1 : 0)
          .animation({ duration: 300, curve: Curve.EaseInOut })
      }

      // 加载中
      if (!this.isLoaded && !this.loadError) {
        LoadingProgress()
          .width(this.size * 0.3)
          .height(this.size * 0.3)
          .color('#c41e3a')
      }

      // 错误状态
      if (this.loadError) {
        Image(this.placeholder)
          .width(this.size)
          .height(this.size)
          .objectFit(ImageFit.Cover)
          .clip(new Circle({ width: this.size, height: this.size }))
          .border({
            width: this.borderWidth,
            color: '#666',
            radius: this.size / 2
          })
      }

      // 在线状态指示器
      Row()
        .width(12)
        .height(12)
        .backgroundColor('#00ff00')
        .border({ width: 2, color: '#0a0a0a' })
        .clip(new Circle({ width: 12, height: 12 }))
        .position({ x: this.size - 14, y: this.size - 14 })
        .shadow({ radius: 2, color: 'rgba(0,255,0,0.5)' })
    }
    .width(this.size)
    .height(this.size)
  }
}
