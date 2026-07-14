// entry/src/main/ets/components/AdaptiveCard.ets
// 龍魂 · 自适应卡片 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { DeviceType, deviceState } from '../models/DeviceModel';

@Component
export struct AdaptiveCard {
  @Prop title: string = '';
  @Prop subtitle: string = '';
  @Prop icon: string = '';
  @Prop badge: string = '';
  @BuilderParam content: () => void;
  @Event onClick: () => void = () => {};

  getPadding(): number {
    const device = deviceState.currentProfile.deviceType;
    switch (device) {
      case DeviceType.WATCH: return 8;
      case DeviceType.CAR: return 24;
      case DeviceType.TV: return 32;
      default: return 16;
    }
  }

  getBorderRadius(): number {
    const device = deviceState.currentProfile.deviceType;
    if (device === DeviceType.WATCH && deviceState.currentProfile.isRound) return 16;
    return 8;
  }

  getTitleSize(): number {
    const device = deviceState.currentProfile.deviceType;
    switch (device) {
      case DeviceType.WATCH: return 12;
      case DeviceType.CAR: return 18;
      case DeviceType.TV: return 22;
      default: return 14;
    }
  }

  getSubtitleSize(): number {
    const device = deviceState.currentProfile.deviceType;
    switch (device) {
      case DeviceType.WATCH: return 10;
      case DeviceType.CAR: return 14;
      case DeviceType.TV: return 16;
      default: return 12;
    }
  }

  build() {
    Column() {
      if (this.title || this.icon) {
        Row() {
          if (this.icon) {
            Text(this.icon)
              .fontSize(this.getTitleSize())
              .margin({ right: 8 })
          }
          Column() {
            Text(this.title)
              .fontSize(this.getTitleSize())
              .fontWeight(FontWeight.Bold)
              .fontColor('#fff')
            if (this.subtitle) {
              Text(this.subtitle)
                .fontSize(this.getSubtitleSize())
                .fontColor('#888')
                .margin({ top: 2 })
            }
          }
          .alignItems(HorizontalAlign.Start)
          .layoutWeight(1)

          if (this.badge) {
            Text(this.badge)
              .fontSize(11)
              .fontColor('#fff')
              .backgroundColor('#c41e3a')
              .borderRadius(999)
              .padding({ left: 8, right: 8, top: 2, bottom: 2 })
          }
        }
        .width('100%')
        .padding({ bottom: this.getPadding() / 2 })
      }

      this.content()
    }
    .width('100%')
    .padding(this.getPadding())
    .backgroundColor('#1a1a1a')
    .borderRadius(this.getBorderRadius())
    .onClick(() => { this.onClick(); })
  }
}
