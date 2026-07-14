// entry/src/main/ets/components/AdaptiveList.ets
// 龍魂 · 自适应列表 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { DeviceType, deviceState } from '../models/DeviceModel';

export interface ListItemData {
  id: string;
  title: string;
  subtitle?: string;
  icon?: string;
  badge?: string;
  arrow?: boolean;
}

@Component
export struct AdaptiveList {
  @Prop items: ListItemData[] = [];
  @Prop showIcon: boolean = true;
  @Prop showBadge: boolean = true;
  @Event onItemClick: (item: ListItemData) => void = () => {};
  @Event onItemLongPress: (item: ListItemData) => void = () => {};

  getItemHeight(): number {
    const device = deviceState.currentProfile.deviceType;
    switch (device) {
      case DeviceType.WATCH: return 40;
      case DeviceType.CAR: return 80;
      case DeviceType.TV: return 96;
      default: return 56;
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

  getIconSize(): number {
    const device = deviceState.currentProfile.deviceType;
    switch (device) {
      case DeviceType.WATCH: return 20;
      case DeviceType.CAR: return 32;
      case DeviceType.TV: return 40;
      default: return 24;
    }
  }

  build() {
    List() {
      ForEach(this.items, (item: ListItemData) => {
        ListItem() {
          Row() {
            if (this.showIcon && item.icon) {
              Text(item.icon)
                .fontSize(this.getIconSize())
                .margin({ right: 12 })
            }

            Column() {
              Text(item.title)
                .fontSize(this.getFontSize())
                .fontWeight(FontWeight.Medium)
                .fontColor('#fff')
              if (item.subtitle) {
                Text(item.subtitle)
                  .fontSize(this.getFontSize() - 2)
                  .fontColor('#888')
                  .margin({ top: 2 })
              }
            }
            .alignItems(HorizontalAlign.Start)
            .layoutWeight(1)

            if (this.showBadge && item.badge) {
              Text(item.badge)
                .fontSize(11)
                .fontColor('#fff')
                .backgroundColor('#c41e3a')
                .borderRadius(999)
                .padding({ left: 8, right: 8, top: 2, bottom: 2 })
            }

            if (item.arrow !== false) {
              Text('›')
                .fontSize(this.getFontSize() + 4)
                .fontColor('#666')
                .margin({ left: 8 })
            }
          }
          .width('100%')
          .height(this.getItemHeight())
          .padding({ left: 16, right: 16 })
          .backgroundColor('#0a0a0a')
        }
        .onClick(() => { this.onItemClick(item); })
        .onLongPress(() => { this.onItemLongPress(item); })
      }, (item: ListItemData) => item.id)
    }
    .width('100%')
    .divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto)
    .edgeEffect(EdgeEffect.Spring)
  }
}
