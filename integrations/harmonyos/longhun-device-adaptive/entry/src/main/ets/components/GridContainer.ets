// entry/src/main/ets/components/GridContainer.ets
// 龍魂 · 响应式栅格容器 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { DeviceType, Breakpoint, deviceState } from '../models/DeviceModel';

@Component
export struct GridContainer {
  @Prop columns: number = 12;
  @Prop gutter: number = 16;
  @Prop margin: number = 16;
  @BuilderParam content: () => void;

  getResponsiveColumns(): number {
    const profile = deviceState.currentProfile;
    if (profile.deviceType === DeviceType.WATCH) return 2;
    if (profile.deviceType === DeviceType.CAR) return 24;
    if (profile.deviceType === DeviceType.TV) return 24;
    if (profile.breakpoint === Breakpoint.XS) return 2;
    if (profile.breakpoint === Breakpoint.SM) return 4;
    if (profile.breakpoint === Breakpoint.MD) return 8;
    if (profile.breakpoint === Breakpoint.LG) return 12;
    return 24;
  }

  build() {
    GridRow({ columns: this.getResponsiveColumns(), gutter: this.gutter }) {
      this.content()
    }
    .width('100%')
    .padding(this.margin)
  }
}

// === 栅格列 ===
@Component
export struct GridCol {
  @Prop span: number = 1;
  @Prop offset: number = 0;
  @BuilderParam content: () => void;

  getResponsiveSpan(): number {
    const profile = deviceState.currentProfile;
    if (profile.deviceType === DeviceType.WATCH) return 2;
    if (profile.deviceType === DeviceType.CAR) return Math.min(this.span * 2, 24);
    return this.span;
  }

  build() {
    GridCol({ span: this.getResponsiveSpan(), offset: this.offset }) {
      this.content()
    }
  }
}
