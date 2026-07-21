// entry/src/main/ets/components/SafeAreaClip.ets
// 龍魂 · 安全区域裁剪组件 · 适配刘海屏/挖孔屏

import { clipState, ClipConfig, ClipType } from '../models/ClipModel';

@Component
export struct SafeAreaClip {
  @BuilderParam contentBuilder: () => void;
  @Prop safeTop: boolean = true;      // 顶部安全区
  @Prop safeBottom: boolean = true;   // 底部安全区
  @Prop safeLeft: boolean = true;    // 左侧安全区
  @Prop safeRight: boolean = true;   // 右侧安全区
  @Prop extraTop: number = 0;        // 额外顶部间距
  @Prop extraBottom: number = 0;     // 额外底部间距

  @State private safeInsets: EdgeInsets = { top: 0, bottom: 0, left: 0, right: 0 };

  aboutToAppear() {
    // 获取系统安全区域
    this.safeInsets = this.getSystemSafeArea();

    const config = new ClipConfig({
      type: ClipType.RECT,
      params: {
        x: this.safeLeft ? this.safeInsets.left : 0,
        y: this.safeTop ? this.safeInsets.top + this.extraTop : this.extraTop,
        width: this.safeRight ? 360 - this.safeInsets.left - this.safeInsets.right : 360,
        height: this.safeBottom ? 720 - this.safeInsets.top - this.safeInsets.bottom : 720
      },
      name: 'SafeAreaClip'
    });
    clipState.addConfig(config);
  }

  // 模拟获取系统安全区域（实际使用系统API）
  private getSystemSafeArea(): EdgeInsets {
    // 实际使用：window.getWindowAvoidArea(type).topRect.height
    return {
      top: 44,    // 状态栏高度
      bottom: 34, // 手势条高度
      left: 0,
      right: 0
    };
  }

  build() {
    Stack() {
      this.contentBuilder()
    }
    .padding({
      top: this.safeTop ? this.safeInsets.top + this.extraTop : this.extraTop,
      bottom: this.safeBottom ? this.safeInsets.bottom + this.extraBottom : this.extraBottom,
      left: this.safeLeft ? this.safeInsets.left : 0,
      right: this.safeRight ? this.safeInsets.right : 0
    })
    .clip(new Rect({
      width: '100%',
      height: '100%'
    }))
  }
}

interface EdgeInsets {
  top: number;
  bottom: number;
  left: number;
  right: number;
}
