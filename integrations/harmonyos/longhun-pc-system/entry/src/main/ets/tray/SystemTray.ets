// entry/src/main/ets/tray/SystemTray.ets
// 龍魂 · 系统托盘管理 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { pcState, PCState, TrayMenuItem, TrayMenuType, WindowState } from '../models/PCModel';

@Component
export struct SystemTray {
  @StorageLink('pcState') pcState: PCState = pcState;
  @State private showMenu: boolean = false;
  @State private menuPosition: { x: number; y: number } = { x: 0, y: 0 };

  // 构建托盘菜单
  getTrayMenu(): TrayMenuItem[] {
    return [
      new TrayMenuItem({
        id: 'show',
        label: '显示主窗口',
        icon: '📱',
        shortcut: 'Ctrl+Shift+S',
        action: () => { this.showMainWindow(); }
      }),
      new TrayMenuItem({
        id: 'hide',
        label: '隐藏到托盘',
        icon: '🔽',
        shortcut: 'Ctrl+Shift+H',
        action: () => { this.hideToTray(); }
      }),
      TrayMenuItem.separator(),
      TrayMenuItem.submenu('快速导航', [
        new TrayMenuItem({
          id: 'nav_project',
          label: '项目管理',
          icon: '📊',
          action: () => { this.navigateAndShow('ProjectList'); }
        }),
        new TrayMenuItem({
          id: 'nav_milestone',
          label: '里程碑',
          icon: '📈',
          action: () => { this.navigateAndShow('MilestoneTimeline'); }
        }),
        new TrayMenuItem({
          id: 'nav_weekly',
          label: '周报',
          icon: '📝',
          action: () => { this.navigateAndShow('WeeklyReview'); }
        }),
        new TrayMenuItem({
          id: 'nav_stamp',
          label: '印章管理',
          icon: '🔏',
          action: () => { this.navigateAndShow('StampManagement'); }
        })
      ]),
      TrayMenuItem.separator(),
      new TrayMenuItem({
        id: 'settings',
        label: '设置',
        icon: '⚙️',
        action: () => { this.navigateAndShow('Settings'); }
      }),
      new TrayMenuItem({
        id: 'notifications',
        label: `通知中心 (${this.pcState.unreadCount})`,
        icon: '🔔',
        action: () => { this.showNotificationCenter(); }
      }),
      TrayMenuItem.separator(),
      new TrayMenuItem({
        id: 'about',
        label: '关于龍魂',
        icon: '🐉',
        action: () => { this.showAbout(); }
      }),
      new TrayMenuItem({
        id: 'exit',
        label: '退出',
        icon: '🚪',
        shortcut: 'Ctrl+Q',
        action: () => { this.exitApp(); }
      })
    ];
  }

  // 导航并显示窗口
  navigateAndShow(route: string): void {
    this.showMainWindow();
    console.info(`[龍魂] 托盘导航 → ${route}`);
  }

  // 显示主窗口
  showMainWindow(): void {
    this.pcState.windows.forEach((win, id) => {
      if (win.state === WindowState.HIDDEN) {
        win.restoreFromTray();
      }
    });
    console.info('[龍魂] 显示主窗口');
  }

  // 隐藏到托盘
  hideToTray(): void {
    this.pcState.windows.forEach((win, id) => {
      win.minimizeToTray();
    });
    console.info('[龍魂] 隐藏到托盘');
  }

  // 显示通知中心
  showNotificationCenter(): void {
    console.info('[龍魂] 显示通知中心');
    // 触发通知中心弹窗
    AppStorage.setOrCreate('show_notification_center', true);
  }

  // 显示关于
  showAbout(): void {
    console.info('[龍魂] 显示关于');
    AppStorage.setOrCreate('show_about_dialog', true);
  }

  // 退出应用
  exitApp(): void {
    this.pcState.persist();
    console.info('[龍魂] 退出应用');
  }

  // 托盘图标点击
  onTrayClick(): void {
    this.showMainWindow();
  }

  // 托盘图标右键/长按
  onTrayRightClick(event: { x: number; y: number }): void {
    this.menuPosition = { x: event.x, y: event.y };
    this.showMenu = !this.showMenu;
  }

  // 关闭菜单
  closeMenu(): void {
    this.showMenu = false;
  }

  build() {
    Column() {
      // 托盘图标区域
      Row() {
        Text(this.pcState.trayIcon)
          .fontSize(24)
      }
      .width(40)
      .height(40)
      .justifyContent(FlexAlign.Center)
      .onClick(() => { this.onTrayClick(); })
      .gesture(
        LongPressGesture({ duration: 500 })
          .onAction((event: GestureEvent) => {
            const posX = event.fingerList && event.fingerList.length > 0
              ? event.fingerList[0].localX : 0;
            const posY = event.fingerList && event.fingerList.length > 0
              ? event.fingerList[0].localY : 0;
            this.onTrayRightClick({ x: posX, y: posY });
          })
      )

      if (this.pcState.unreadCount > 0) {
        Badge({
          value: this.pcState.unreadCount > 99 ? '99+' : this.pcState.unreadCount.toString(),
          position: BadgePosition.RightTop,
          style: { badgeSize: 16, badgeColor: '#c41e3a' }
        }) {
          Text('')
        }
      }

      // 托盘提示文字
      Text(this.pcState.trayTooltip)
        .fontSize(10)
        .fontColor('#666666')
        .margin({ top: 2 })
    }
    .width(64)
    .height(64)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .justifyContent(FlexAlign.Center)

    // 右键菜单（条件渲染）
    if (this.showMenu) {
      this.TrayMenuBuilder()
    }
  }

  @Builder
  TrayMenuBuilder() {
    Column() {
      ForEach(this.getTrayMenu(), (item: TrayMenuItem, index: number) => {
        if (item.type === TrayMenuType.SEPARATOR) {
          Divider()
            .width('100%')
            .height(1)
            .color('#333333')
            .margin({ top: 4, bottom: 4 })
        } else if (item.type === TrayMenuType.SUBMENU && item.children) {
          Column() {
            Text(item.icon ? `${item.icon} ${item.label} ›` : `${item.label} ›`)
              .fontSize(13)
              .fontColor(item.isEnabled ? '#ffffff' : '#666666')
              .padding({ left: 12, right: 12, top: 8, bottom: 8 })

            Column() {
              ForEach(item.children, (child: TrayMenuItem) => {
                Row() {
                  Text(child.icon ? `${child.icon} ${child.label}` : child.label)
                    .fontSize(12)
                    .fontColor(child.isEnabled ? '#ffffff' : '#666666')
                    .layoutWeight(1)
                  if (child.shortcut) {
                    Text(child.shortcut)
                      .fontSize(10)
                      .fontColor('#666666')
                  }
                }
                .width('100%')
                .padding({ left: 24, right: 12, top: 6, bottom: 6 })
                .onClick(() => { child.action?.(); this.closeMenu(); })
              })
            }
            .width('100%')
            .backgroundColor('#0a0a0a')
          }
          .width('100%')
        } else {
          Row() {
            Text(item.icon ? `${item.icon} ${item.label}` : item.label)
              .fontSize(13)
              .fontColor(item.isEnabled ? '#ffffff' : '#666666')
              .layoutWeight(1)
            if (item.shortcut) {
              Text(item.shortcut)
                .fontSize(10)
                .fontColor('#666666')
            }
          }
          .width('100%')
          .padding({ left: 12, right: 12, top: 8, bottom: 8 })
          .backgroundColor('#1a1a1a')
          .onClick(() => { item.action?.(); this.closeMenu(); })
        }
      }, (item: TrayMenuItem) => item.id)
    }
    .width(200)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .shadow({ radius: 8, color: 'rgba(0,0,0,0.5)' })
    .position({ x: this.menuPosition.x, y: this.menuPosition.y })
    .onClick(() => { this.closeMenu(); })
  }
}
