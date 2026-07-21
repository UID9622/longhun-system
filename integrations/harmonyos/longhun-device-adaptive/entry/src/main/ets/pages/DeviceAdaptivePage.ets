// entry/src/main/ets/pages/DeviceAdaptivePage.ets
// 龍魂 · 多设备适配主页面 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { DeviceType, Breakpoint, DeviceProfile, LayoutStrategy, deviceState, Orientation } from '../models/DeviceModel';
import { GridContainer, GridCol } from '../components/GridContainer';
import { AdaptiveButton } from '../components/AdaptiveButton';
import { AdaptiveCard } from '../components/AdaptiveCard';
import { AdaptiveList, ListItemData } from '../components/AdaptiveList';
import { DeviceDatabase } from '../database/DeviceDatabase';

const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";

@Entry
@Component
struct DeviceAdaptivePage {
  @StorageLink('deviceState') deviceState: DeviceState = deviceState;
  @State private selectedTab: number = 0;
  @State private showDeviceInfo: boolean = false;

  aboutToAppear() {
    this.deviceState.init();
    DeviceDatabase.init();
    this.listenWindowChange();
  }

  listenWindowChange(): void {
    // 使用鸿蒙 Window API 监听尺寸变化
    // window.getLastWindow(getContext()).then(win => {
    //   win.on('windowSizeChange', (data) => {
    //     this.deviceState.onWindowChange(data.width, data.height);
    //   });
    // });
  }

  build() {
    Column() {
      this.HeaderBuilder()
      this.DeviceInfoBuilder()
      this.ContentBuilder()
      this.FooterBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉')
        .fontSize(this.getHeaderIconSize())
        .margin({ right: 8 })

      Column() {
        Text('龍魂设备适配')
          .fontSize(this.getHeaderTitleSize())
          .fontWeight(FontWeight.Bold)
          .fontColor('#c41e3a')

        Text(`${this.getDeviceLabel()} · ${this.deviceState.currentProfile.breakpoint.toUpperCase()}`)
          .fontSize(this.getHeaderSubtitleSize())
          .fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)

      Blank()

      Button() {
        Text(this.showDeviceInfo ? '✕' : 'ℹ️')
          .fontSize(20)
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(40)
      .height(40)
      .onClick(() => {
        this.showDeviceInfo = !this.showDeviceInfo;
      })
    }
    .width('100%')
    .height(this.getHeaderHeight())
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  getHeaderHeight(): number {
    return this.deviceState.currentStrategy.headerHeight;
  }

  getHeaderIconSize(): number {
    const device = this.deviceState.currentProfile.deviceType;
    return device === DeviceType.WATCH ? 20 : 28;
  }

  getHeaderTitleSize(): number {
    const device = this.deviceState.currentProfile.deviceType;
    switch (device) {
      case DeviceType.WATCH: return 14;
      case DeviceType.CAR: return 24;
      case DeviceType.TV: return 28;
      default: return 20;
    }
  }

  getHeaderSubtitleSize(): number {
    const device = this.deviceState.currentProfile.deviceType;
    switch (device) {
      case DeviceType.WATCH: return 9;
      case DeviceType.CAR: return 14;
      case DeviceType.TV: return 16;
      default: return 12;
    }
  }

  getDeviceLabel(): string {
    const device = this.deviceState.currentProfile.deviceType;
    const labels: Record<DeviceType, string> = {
      [DeviceType.PHONE]: '📱 手机',
      [DeviceType.FOLDABLE]: '📱 折叠屏',
      [DeviceType.TABLET]: '💻 平板',
      [DeviceType.WATCH]: '⌚ 手表',
      [DeviceType.CAR]: '🚗 车机',
      [DeviceType.TV]: '📺 智慧屏',
      [DeviceType.IOT]: '🔌 IoT'
    };
    return labels[device] || '📱 手机';
  }

  @Builder
  DeviceInfoBuilder() {
    if (this.showDeviceInfo) {
      Column() {
        GridRow({ columns: this.deviceState.currentProfile.getGridColumns(), gutter: 8 }) {
          GridCol({ span: this.getInfoSpan() }) {
            this.InfoItem('设备类型', this.getDeviceLabel())
          }
          GridCol({ span: this.getInfoSpan() }) {
            this.InfoItem('断点', this.deviceState.currentProfile.breakpoint.toUpperCase())
          }
          GridCol({ span: this.getInfoSpan() }) {
            this.InfoItem('屏幕', `${this.deviceState.windowWidth}x${this.deviceState.windowHeight}`)
          }
          GridCol({ span: this.getInfoSpan() }) {
            this.InfoItem('方向', this.deviceState.currentProfile.orientation === 'landscape' ? '横屏' : '竖屏')
          }
          GridCol({ span: this.getInfoSpan() }) {
            this.InfoItem('交互', this.getInteractionLabel())
          }
          GridCol({ span: this.getInfoSpan() }) {
            this.InfoItem('栅格', `${this.deviceState.currentProfile.getGridColumns()}列`)
          }
        }
        .width('100%')
        .padding(12)
      }
      .width('100%')
      .backgroundColor('#1a1a1a')
      .border({ width: { bottom: 1 }, color: '#333' })
    }
  }

  getInfoSpan(): number {
    const cols = this.deviceState.currentProfile.getGridColumns();
    if (cols >= 12) return 4;
    if (cols >= 8) return 4;
    return cols;
  }

  getInteractionLabel(): string {
    const mode = this.deviceState.currentProfile.interactionMode;
    const labels: Record<string, string> = {
      'touch': '👆 触摸',
      'voice': '🎤 语音',
      'knob': '🔘 旋钮',
      'gesture': '👋 手势',
      'remote': '📱 遥控',
      'steering': '🎮 方向盘'
    };
    return labels[mode] || '👆 触摸';
  }

  @Builder
  InfoItem(label: string, value: string) {
    Column() {
      Text(label)
        .fontSize(11)
        .fontColor('#666')
      Text(value)
        .fontSize(13)
        .fontWeight(FontWeight.Medium)
        .fontColor('#fff')
        .margin({ top: 4 })
    }
    .padding(8)
    .backgroundColor('#0a0a0a')
    .borderRadius(8)
    .alignItems(HorizontalAlign.Start)
  }

  @Builder
  ContentBuilder() {
    Scroll() {
      Column() {
        this.ButtonDemoBuilder()
        this.CardDemoBuilder()
        this.ListDemoBuilder()
        this.GridDemoBuilder()
      }
      .width('100%')
      .padding({ bottom: 24 })
    }
    .width('100%')
    .layoutWeight(1)
    .scrollBar(BarState.Auto)
  }

  @Builder
  ButtonDemoBuilder() {
    Column() {
      Text('自适应按钮')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
        .margin({ left: 16, top: 16, bottom: 12 })

      Row() {
        AdaptiveButton({
          label: '主要按钮',
          icon: '✓',
          type: 'primary',
          onClick: () => { console.info('主要按钮点击'); }
        })

        AdaptiveButton({
          label: '次要按钮',
          type: 'secondary',
          onClick: () => { console.info('次要按钮点击'); }
        })

        if (!this.isWatch()) {
          AdaptiveButton({
            label: '危险按钮',
            type: 'danger',
            onClick: () => { console.info('危险按钮点击'); }
          })
        }
      }
      .width('100%')
      .padding({ left: 16, right: 16 })
      .justifyContent(FlexAlign.SpaceAround)
    }
    .width('100%')
    .margin({ top: 8 })
  }

  @Builder
  CardDemoBuilder() {
    Column() {
      Text('自适应卡片')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
        .margin({ left: 16, top: 16, bottom: 12 })

      GridRow({ columns: this.deviceState.currentProfile.getGridColumns(), gutter: 12 }) {
        GridCol({ span: this.isWatch() ? 2 : this.isTV() ? 8 : 4 }) {
          AdaptiveCard({
            title: '项目进度',
            subtitle: '本周完成率',
            icon: '📊',
            badge: '85%',
            content: () => {
              Column() {
                Text('85%')
                  .fontSize(this.isCar() ? 32 : 24)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#00ff00')
                Text('SPI: 1.02')
                  .fontSize(12)
                  .fontColor('#888')
              }
              .alignItems(HorizontalAlign.Start)
            }
          })
        }

        GridCol({ span: this.isWatch() ? 2 : this.isTV() ? 8 : 4 }) {
          AdaptiveCard({
            title: '工时统计',
            subtitle: '本周累计',
            icon: '⏱️',
            badge: '40h',
            content: () => {
              Column() {
                Text('40h')
                  .fontSize(this.isCar() ? 32 : 24)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#ffcc00')
                Text('加班: 4h')
                  .fontSize(12)
                  .fontColor('#888')
              }
              .alignItems(HorizontalAlign.Start)
            }
          })
        }

        GridCol({ span: this.isWatch() ? 2 : this.isTV() ? 8 : 4 }) {
          AdaptiveCard({
            title: '风险预警',
            subtitle: '待处理',
            icon: '⚠️',
            badge: '3',
            content: () => {
              Column() {
                Text('3项')
                  .fontSize(this.isCar() ? 32 : 24)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#ff0000')
                Text('高风险: 1')
                  .fontSize(12)
                  .fontColor('#888')
              }
              .alignItems(HorizontalAlign.Start)
            }
          })
        }
      }
      .width('100%')
      .padding({ left: 16, right: 16 })
    }
    .width('100%')
    .margin({ top: 8 })
  }

  @Builder
  ListDemoBuilder() {
    Column() {
      Text('自适应列表')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
        .margin({ left: 16, top: 16, bottom: 12 })

      AdaptiveList({
        items: [
          { id: '1', title: '里程碑时间线', subtitle: '项目进度追踪', icon: '📊', badge: '进行中' },
          { id: '2', title: '印章管理', subtitle: '用印登记审批', icon: '🔏', badge: '在库' },
          { id: '3', title: '周报管理', subtitle: 'Weekly Review', icon: '📝', badge: '已提交' },
          { id: '4', title: '设备适配', subtitle: '多端统一渲染', icon: '📱', badge: '当前' },
          { id: '5', title: '数据看板', subtitle: '统计可视化', icon: '📈', badge: '更新' }
        ],
        onItemClick: (item) => {
          console.info(`[龍魂] 点击: ${item.title}`);
        }
      })
      .padding({ left: 16, right: 16 })
    }
    .width('100%')
    .margin({ top: 8 })
  }

  @Builder
  GridDemoBuilder() {
    Column() {
      Text(`栅格布局 (${this.deviceState.currentProfile.getGridColumns()}列)`)
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
        .margin({ left: 16, top: 16, bottom: 12 })

      GridRow({ columns: this.deviceState.currentProfile.getGridColumns(), gutter: 8 }) {
        ForEach([1, 2, 3, 4, 5, 6], (num: number) => {
          GridCol({ span: this.getGridItemSpan() }) {
            Column() {
              Text(`${num}`)
                .fontSize(this.isTV() ? 24 : 18)
                .fontWeight(FontWeight.Bold)
                .fontColor('#fff')
              Text(`${this.getGridItemSpan()}列`)
                .fontSize(11)
                .fontColor('#888')
            }
            .width('100%')
            .height(this.isWatch() ? 40 : this.isCar() ? 80 : 60)
            .backgroundColor('#1a1a1a')
            .borderRadius(8)
            .justifyContent(FlexAlign.Center)
          }
        })
      }
      .width('100%')
      .padding({ left: 16, right: 16 })
    }
    .width('100%')
    .margin({ top: 8 })
  }

  getGridItemSpan(): number {
    const cols = this.deviceState.currentProfile.getGridColumns();
    if (cols >= 24) return 4;
    if (cols >= 12) return 3;
    if (cols >= 8) return 2;
    return cols;
  }

  isWatch(): boolean {
    return this.deviceState.currentProfile.deviceType === DeviceType.WATCH;
  }

  isCar(): boolean {
    return this.deviceState.currentProfile.deviceType === DeviceType.CAR;
  }

  isTV(): boolean {
    return this.deviceState.currentProfile.deviceType === DeviceType.TV;
  }

  @Builder
  FooterBuilder() {
    Row() {
      Column() {
        Text('🐉').fontSize(20)
        Text(`UID:${MASTER_UID}`).fontSize(10).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Row() {
        Button() {
          Text('📱 模拟手机').fontSize(12).fontColor('#fff')
        }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(8)
        .padding({ left: 12, right: 12, top: 6, bottom: 6 }).margin({ right: 8 })
        .onClick(() => { this.simulateDevice(DeviceType.PHONE, 360, 780); })

        Button() {
          Text('⌚ 模拟手表').fontSize(12).fontColor('#fff')
        }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(8)
        .padding({ left: 12, right: 12, top: 6, bottom: 6 }).margin({ right: 8 })
        .onClick(() => { this.simulateDevice(DeviceType.WATCH, 180, 180); })

        Button() {
          Text('🚗 模拟车机').fontSize(12).fontColor('#fff')
        }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(8)
        .padding({ left: 12, right: 12, top: 6, bottom: 6 }).margin({ right: 8 })
        .onClick(() => { this.simulateDevice(DeviceType.CAR, 1280, 720); })

        Button() {
          Text('📺 模拟TV').fontSize(12).fontColor('#fff')
        }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(8)
        .padding({ left: 12, right: 12, top: 6, bottom: 6 })
        .onClick(() => { this.simulateDevice(DeviceType.TV, 1920, 1080); })
      }
    }
    .width('100%')
    .height(this.deviceState.currentStrategy.footerHeight || 56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }

  simulateDevice(type: DeviceType, width: number, height: number): void {
    this.deviceState.onWindowChange(width, height);
    console.info(`[龍魂] 模拟设备: ${type} ${width}x${height}`);
  }
}
