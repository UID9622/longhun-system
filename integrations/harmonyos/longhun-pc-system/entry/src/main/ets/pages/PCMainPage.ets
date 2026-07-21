// entry/src/main/ets/pages/PCMainPage.ets
// 龍魂 · PC主页面 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import {
  pcState, PCState, WindowState, NotificationLevel,
  HotkeyDefinition, MASTER_DNA, MASTER_UID
} from '../models/PCModel';
import { SystemTray } from '../tray/SystemTray';
import { NotificationCenter } from '../notification/NotificationCenter';
import { hotkeyManager } from '../hotkey/HotkeyManager';

@Entry
@Component
struct PCMainPage {
  @StorageLink('pcState') pcState: PCState = pcState;
  @State private showNotificationCenter: boolean = false;
  @State private showHotkeySettings: boolean = false;
  @State private showWindowManager: boolean = false;

  aboutToAppear() {
    // 初始化热键
    hotkeyManager.initDefaultHotkeys();

    // 加载窗口状态
    this.loadWindowState();

    // 创建默认主窗口
    if (this.pcState.windows.size === 0) {
      this.pcState.createWindow(new WindowProfile({
        id: 'main_window',
        title: '龍魂PC应用',
        width: 1280,
        height: 720,
        isPrimary: true
      }));
    }

    // 监听通知中心触发
    this.watchNotificationCenterTrigger();

    console.info('[龍魂] PC主页面已初始化');
  }

  // 加载窗口状态
  loadWindowState(): void {
    this.pcState.load();
  }

  // 监听通知中心打开事件
  watchNotificationCenterTrigger(): void {
    // 通过 AppStorage 监听触发信号
    const trigger = AppStorage.get<boolean>('show_notification_center');
    if (trigger) {
      this.showNotificationCenter = true;
      AppStorage.setOrCreate('show_notification_center', false);
    }
  }

  // 监听剪贴板
  listenClipboard(): void {
    // 鸿蒙剪贴板API集成点
    // pasteboard.getSystemPasteboard().on('contentChange', () => {
    //   pasteboard.getSystemPasteboard().getData().then(data => {
    //     const text = data.getPrimaryText();
    //     if (text) { this.pcState.recordClipboard(text); }
    //   });
    // });
  }

  // 发送测试通知
  sendTestNotification(level: NotificationLevel): void {
    const titles: Record<string, string> = {
      [NotificationLevel.SILENT]: '静默通知',
      [NotificationLevel.NORMAL]: '普通通知',
      [NotificationLevel.URGENT]: '紧急通知',
      [NotificationLevel.CRITICAL]: '严重通知'
    };
    const contents: Record<string, string> = {
      [NotificationLevel.SILENT]: '静默级别通知，不打扰您的工作',
      [NotificationLevel.NORMAL]: '项目更新提醒，请查看最新进展',
      [NotificationLevel.URGENT]: '任务延期预警，需要您立即关注',
      [NotificationLevel.CRITICAL]: '系统检测到严重风险，请立即处理'
    };

    const notification = new NotificationMessage({
      title: titles[level],
      content: contents[level],
      level,
      source: '龍魂系统',
      sourceIcon: '🐉',
      actions: [
        { id: 'view', label: '查看', type: 'primary', callback: () => { console.info('[龍魂] 查看'); } },
        { id: 'dismiss', label: '忽略', type: 'secondary', callback: () => { console.info('[龍魂] 忽略'); } }
      ]
    });
    this.pcState.sendNotification(notification);
  }

  minimizeToTray(): void {
    this.pcState.windows.forEach((win, id) => {
      win.minimizeToTray();
    });
  }

  toggleAlwaysOnTop(): void {
    this.pcState.windows.forEach((win, id) => {
      win.setAlwaysOnTop(!win.isAlwaysOnTop);
    });
  }

  fullscreen(): void {
    const win = this.pcState.windows.get(this.pcState.activeWindowId);
    if (win) {
      win.fullscreen();
    }
  }

  build() {
    Stack() {
      // 主内容区
      Column() {
        this.HeaderBuilder()
        this.ContentBuilder()
        this.FooterBuilder()
      }
      .width('100%')
      .height('100%')
      .backgroundColor('#0a0a0a')

      // 通知中心（覆盖层）
      if (this.showNotificationCenter) {
        Column() {
          NotificationCenter({})
        }
        .width('100%')
        .height('100%')
        .backgroundColor('rgba(0,0,0,0.8)')
        .onClick(() => { this.showNotificationCenter = false; })
      }

      // 系统托盘（右下角）
      SystemTray({})
        .position({ x: '100%', y: '100%' })
        .markAnchor({ x: '100%', y: '100%' })
        .offset({ x: -80, y: -80 })
    }
    .width('100%')
    .height('100%')
  }

  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉').fontSize(28).margin({ right: 8 })

      Column() {
        Text('龍魂PC应用').fontSize(20).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text(`UID:${MASTER_UID} · ${this.pcState.statistics.displayCount}屏`)
          .fontSize(12).fontColor('#666666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      // 通知按钮
      Badge({
        value: this.pcState.unreadCount > 99 ? '99+' : this.pcState.unreadCount.toString(),
        position: BadgePosition.RightTop,
        style: { badgeSize: 16, badgeColor: '#c41e3a' }
      }) {
        Button() {
          Text('🔔').fontSize(20)
        }
        .type(ButtonType.Circle)
        .backgroundColor('#1a1a1a')
        .width(40)
        .height(40)
        .onClick(() => { this.showNotificationCenter = true; })
      }

      // 窗口管理按钮
      Button() {
        Text('🪟').fontSize(20)
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(40)
      .height(40)
      .margin({ left: 8 })
      .onClick(() => { this.showWindowManager = !this.showWindowManager; })

      // 热键设置按钮
      Button() {
        Text('⌨️').fontSize(20)
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(40)
      .height(40)
      .margin({ left: 8 })
      .onClick(() => { this.showHotkeySettings = !this.showHotkeySettings; })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333333' })
  }

  @Builder
  ContentBuilder() {
    Row() {
      // 侧边栏
      this.SidebarBuilder()

      // 主内容
      Column() {
        Scroll() {
          Column() {
            // 快捷操作
            this.QuickActionsBuilder()

            // 窗口状态
            this.WindowStatusBuilder()

            // 热键列表
            this.HotkeyListBuilder()

            // 剪贴板历史
            this.ClipboardHistoryBuilder()
          }
          .width('100%')
        }
        .width('100%')
        .layoutWeight(1)
        .scrollBar(BarState.Auto)
      }
      .layoutWeight(1)
      .padding(16)
    }
    .width('100%')
    .layoutWeight(1)
  }

  @Builder
  SidebarBuilder() {
    Column() {
      ForEach([
        { icon: '📊', label: '项目', route: 'ProjectList' },
        { icon: '📈', label: '里程碑', route: 'MilestoneTimeline' },
        { icon: '📝', label: '周报', route: 'WeeklyReview' },
        { icon: '🔏', label: '印章', route: 'StampManagement' },
        { icon: '⚙️', label: '设置', route: 'Settings' }
      ], (item: SidebarNavItem) => {
        Column() {
          Text(item.icon).fontSize(20)
          Text(item.label).fontSize(10).fontColor('#666666').margin({ top: 4 })
        }
        .width(64)
        .height(64)
        .justifyContent(FlexAlign.Center)
        .onClick(() => { console.info(`[龍魂] 导航 → ${item.route}`); })
      })
    }
    .width(80)
    .height('100%')
    .backgroundColor('#1a1a1a')
    .border({ width: { right: 1 }, color: '#333333' })
  }

  @Builder
  QuickActionsBuilder() {
    Column() {
      Text('快捷操作')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#ffffff')
        .margin({ bottom: 12 })

      Row() {
        ForEach([
          { label: '静默通知', level: NotificationLevel.SILENT },
          { label: '普通通知', level: NotificationLevel.NORMAL },
          { label: '紧急通知', level: NotificationLevel.URGENT },
          { label: '严重通知', level: NotificationLevel.CRITICAL }
        ], (item: QuickActionItem) => {
          Button(item.label)
            .fontSize(12)
            .fontColor('#ffffff')
            .backgroundColor('#333333')
            .borderRadius(6)
            .padding({ left: 12, right: 12, top: 6, bottom: 6 })
            .onClick(() => { this.sendTestNotification(item.level); })
        })
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceAround)

      Row() {
        Button('最小化到托盘')
          .fontSize(12)
          .fontColor('#ffffff')
          .backgroundColor('#333333')
          .borderRadius(6)
          .padding({ left: 12, right: 12, top: 6, bottom: 6 })
          .onClick(() => { this.minimizeToTray(); })

        Button('全屏模式')
          .fontSize(12)
          .fontColor('#ffffff')
          .backgroundColor('#333333')
          .borderRadius(6)
          .padding({ left: 12, right: 12, top: 6, bottom: 6 })
          .onClick(() => { this.fullscreen(); })

        Button('置顶窗口')
          .fontSize(12)
          .fontColor('#ffffff')
          .backgroundColor('#333333')
          .borderRadius(6)
          .padding({ left: 12, right: 12, top: 6, bottom: 6 })
          .onClick(() => { this.toggleAlwaysOnTop(); })
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceAround)
      .margin({ top: 8 })
    }
    .width('100%')
    .padding(16)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .margin({ bottom: 16 })
  }

  @Builder
  WindowStatusBuilder() {
    Column() {
      Text('窗口状态')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#ffffff')
        .margin({ bottom: 12 })

      Row() {
        this.StatCard('总窗口', this.pcState.statistics.totalWindows.toString())
        this.StatCard('可见', this.pcState.statistics.visibleWindows.toString())
        this.StatCard('隐藏',
          (this.pcState.statistics.totalWindows - this.pcState.statistics.visibleWindows).toString())
        this.StatCard('显示器', this.pcState.statistics.displayCount.toString())
      }
      .width('100%')
    }
    .width('100%')
    .padding(16)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .margin({ bottom: 16 })
  }

  @Builder
  HotkeyListBuilder() {
    Column() {
      Text('热键列表')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#ffffff')
        .margin({ bottom: 12 })

      List() {
        ForEach(hotkeyManager.getAllHotkeys(), (hotkey: HotkeyDefinition) => {
          ListItem() {
            Row() {
              Text(hotkey.name)
                .fontSize(14)
                .fontColor('#ffffff')
                .layoutWeight(1)

              Text(hotkey.getDisplayText())
                .fontSize(12)
                .fontColor('#c41e3a')
                .backgroundColor('rgba(196,30,58,0.1)')
                .borderRadius(4)
                .padding({ left: 8, right: 8, top: 2, bottom: 2 })

              Text(hotkey.scope)
                .fontSize(11)
                .fontColor('#666666')
                .margin({ left: 8 })
            }
            .width('100%')
            .padding(8)
            .backgroundColor('#0a0a0a')
            .borderRadius(8)
          }
        }, (hotkey: HotkeyDefinition) => hotkey.id)
      }
      .width('100%')
      .height(240)
      .scrollBar(BarState.Auto)
    }
    .width('100%')
    .padding(16)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .margin({ bottom: 16 })
  }

  @Builder
  ClipboardHistoryBuilder() {
    Column() {
      Text('剪贴板历史')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#ffffff')
        .margin({ bottom: 12 })

      if (this.pcState.getClipboardHistory().length === 0) {
        Text('暂无剪贴板记录')
          .fontSize(12)
          .fontColor('#666666')
          .padding(16)
      } else {
        List() {
          ForEach(this.pcState.getClipboardHistory(), (text: string, index: number) => {
            ListItem() {
              Row() {
                Text(`${index + 1}.`)
                  .fontSize(12)
                  .fontColor('#666666')
                  .width(24)

                Text(text.substring(0, 50))
                  .fontSize(12)
                  .fontColor('#ffffff')
                  .layoutWeight(1)
                  .maxLines(1)
                  .textOverflow({ overflow: TextOverflow.Ellipsis })
              }
              .width('100%')
              .padding(8)
              .backgroundColor('#0a0a0a')
              .borderRadius(8)
            }
          })
        }
        .width('100%')
        .height(150)
        .scrollBar(BarState.Auto)
      }
    }
    .width('100%')
    .padding(16)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
  }

  @Builder
  StatCard(label: string, value: string) {
    Column() {
      Text(value)
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .fontColor('#ffffff')

      Text(label)
        .fontSize(11)
        .fontColor('#666666')
        .margin({ top: 4 })
    }
    .width('25%')
    .alignItems(HorizontalAlign.Center)
  }

  @Builder
  FooterBuilder() {
    Row() {
      Column() {
        Text('🐉')
          .fontSize(20)
        Text(`UID:${MASTER_UID}`)
          .fontSize(10)
          .fontColor('#666666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Row() {
        Text(`🔔 ${this.pcState.statistics.totalNotifications} 通知`)
          .fontSize(12)
          .fontColor('#888888')
        Text(`⌨️ ${this.pcState.statistics.activeHotkeys} 热键`)
          .fontSize(12)
          .fontColor('#888888')
          .margin({ left: 12 })
        Text(`📋 ${this.pcState.statistics.clipboardItems} 剪贴板`)
          .fontSize(12)
          .fontColor('#888888')
          .margin({ left: 12 })
      }
    }
    .width('100%')
    .height(40)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333333' })
  }
}

// 辅助类型
interface SidebarNavItem {
  icon: string;
  label: string;
  route: string;
}

interface QuickActionItem {
  label: string;
  level: NotificationLevel;
}
