// entry/src/main/ets/components/AdaptiveButton.ets
// 龍魂 · 自适应按钮 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { DeviceType, deviceState } from '../models/DeviceModel';

@Component
export struct AdaptiveButton {
  @Prop label: string = '';
  @Prop icon: string = '';
  @Prop type: 'primary' | 'secondary' | 'danger' = 'primary';
  @Prop disabled: boolean = false;
  @Event onClick: () => void = () => {};

  getButtonHeight(): number {
    const device = deviceState.currentProfile.deviceType;
    switch (device) {
      case DeviceType.WATCH: return 36;
      case DeviceType.CAR: return 64;
      case DeviceType.TV: return 72;
      default: return 44;
    }
  }

  getFontSize(): number {
    const device = deviceState.currentProfile.deviceType;
    switch (device) {
      case DeviceType.WATCH: return 12;
      case DeviceType.CAR: return 18;
      case DeviceType.TV: return 20;
      default: return 14;
    }
  }

  getBorderRadius(): number {
    const device = deviceState.currentProfile.deviceType;
    if (device === DeviceType.WATCH && deviceState.currentProfile.isRound) return 999;
    return 8;
  }

  getBgColor(): string {
    switch (this.type) {
      case 'primary': return '#c41e3a';
      case 'secondary': return '#333';
      case 'danger': return '#ff0000';
      default: return '#c41e3a';
    }
  }

  build() {
    Button() {
      Row() {
        if (this.icon) {
          Text(this.icon)
            .fontSize(this.getFontSize())
            .margin({ right: 8 })
        }
        Text(this.label)
          .fontSize(this.getFontSize())
          .fontColor('#fff')
      }
    }
    .type(ButtonType.Normal)
    .backgroundColor(this.getBgColor())
    .borderRadius(this.getBorderRadius())
    .height(this.getButtonHeight())
    .padding({ left: 16, right: 16 })
    .enabled(!this.disabled)
    .onClick(() => { this.onClick(); })
  }
}
