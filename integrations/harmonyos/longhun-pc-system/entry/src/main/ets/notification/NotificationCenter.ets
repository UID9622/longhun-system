// entry/src/main/ets/notification/NotificationCenter.ets
// 龍魂 · 通知中心 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { pcState, PCState, NotificationMessage, NotificationLevel } from '../models/PCModel';

@Component
export struct NotificationCenter {
  @StorageLink('pcState') pcState: PCState = pcState;
  @State private showCenter: boolean = false;
  @State private filterLevel: NotificationLevel | 'all' = 'all';
  @State private filterRead: 'all' | 'unread' | 'read' = 'all';

  // 过滤后的通知
  getFilteredNotifications(): NotificationMessage[] {
    let result = this.pcState.notifications;

    if (this.filterLevel !== 'all') {
      result = result.filter(n => n.level === this.filterLevel);
    }

    if (this.filterRead === 'unread') {
      result = result.filter(n => !n.isRead);
    } else if (this.filterRead === 'read') {
      result = result.filter(n => n.isRead);
    }

    return result;
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
      [NotificationLevel.SILENT]: '这是一条静默通知，不会打扰您',
      [NotificationLevel.NORMAL]: '项目里程碑已更新，请查看',
      [NotificationLevel.URGENT]: '任务延期预警，需要立即处理',
      [NotificationLevel.CRITICAL]: '系统检测到严重风险，请立即检查'
    };

    const notification = new NotificationMessage({
      title: titles[level],
      content: contents[level],
      level,
      source: '龍魂系统',
      actions: [
        {
          id: 'view',
          label: '查看',
          type: 'primary',
          callback: () => { console.info('[龍魂] 查看通知'); }
        },
        {
          id: 'dismiss',
          label: '忽略',
          type: 'secondary',
          callback: () => { console.info('[龍魂] 忽略通知'); }
        }
      ]
    });

    this.pcState.sendNotification(notification);
  }

  // 获取过滤器按钮标签
  getFilterLabel(level: string): string {
    switch (level) {
      case 'all': return '全部';
      case 'silent': return '🔕 静默';
      case 'normal': return '🔔 普通';
      case 'urgent': return '⚠️ 紧急';
      case 'critical': return '🚨 严重';
      default: return level;
    }
  }

  // 获取已读状态标签
  getReadStatusLabel(status: string): string {
    switch (status) {
      case 'all': return '全部';
      case 'unread': return '未读';
      case 'read': return '已读';
      default: return status;
    }
  }

  build() {
    Column() {
      // 头部
      this.HeaderBuilder()

      // 过滤器
      this.FilterBuilder()

      // 通知列表
      this.NotificationListBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder
  HeaderBuilder() {
    Row() {
      Text('🔔')
        .fontSize(24)
        .margin({ right: 8 })

      Column() {
        Text('通知中心')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#ffffff')

        Text(`${this.pcState.unreadCount} 条未读 · ${this.pcState.notifications.length} 条总计`)
          .fontSize(12)
          .fontColor('#666666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Button() {
        Text('✓')
          .fontSize(16)
          .fontColor('#ffffff')
      }
      .type(ButtonType.Circle)
      .backgroundColor('#333333')
      .width(36)
      .height(36)
      .onClick(() => { this.pcState.markAllAsRead(); })

      Button() {
        Text('🗑')
          .fontSize(16)
          .fontColor('#ffffff')
      }
      .type(ButtonType.Circle)
      .backgroundColor('#333333')
      .width(36)
      .height(36)
      .margin({ left: 8 })
      .onClick(() => { this.pcState.clearNotifications(); })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333333' })
  }

  @Builder
  FilterBuilder() {
    Row() {
      // 级别过滤
      Row() {
        ForEach(['all', 'silent', 'normal', 'urgent', 'critical'], (level: string) => {
          Button() {
            Text(this.getFilterLabel(level))
              .fontSize(11)
              .fontColor(this.filterLevel === level ? '#0a0a0a' : '#999999')
          }
          .type(ButtonType.Normal)
          .backgroundColor(this.filterLevel === level ? '#c41e3a' : '#1a1a1a')
          .borderRadius(6)
          .padding({ left: 8, right: 8, top: 4, bottom: 4 })
          .margin({ right: 4 })
          .onClick(() => { this.filterLevel = level as NotificationLevel | 'all'; })
        })
      }
      .layoutWeight(1)

      // 已读过滤
      Row() {
        ForEach(['all', 'unread', 'read'], (status: string) => {
          Button() {
            Text(this.getReadStatusLabel(status))
              .fontSize(11)
              .fontColor(this.filterRead === status ? '#0a0a0a' : '#999999')
          }
          .type(ButtonType.Normal)
          .backgroundColor(this.filterRead === status ? '#c41e3a' : '#1a1a1a')
          .borderRadius(6)
          .padding({ left: 8, right: 8, top: 4, bottom: 4 })
          .margin({ left: 4 })
          .onClick(() => { this.filterRead = status as 'all' | 'unread' | 'read'; })
        })
      }
    }
    .width('100%')
    .height(44)
    .padding({ left: 12, right: 12 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333333' })
  }

  @Builder
  NotificationListBuilder() {
    List() {
      ForEach(this.getFilteredNotifications(), (notification: NotificationMessage) => {
        ListItem() {
          this.NotificationCardBuilder(notification)
        }
        .onClick(() => { this.pcState.markAsRead(notification.id); })
      }, (notification: NotificationMessage) => notification.id)
    }
    .width('100%')
    .layoutWeight(1)
    .divider({ strokeWidth: 1, color: '#222222' })
    .scrollBar(BarState.Auto)
    .padding({ bottom: 16 })
  }

  @Builder
  NotificationCardBuilder(notification: NotificationMessage) {
    Row() {
      // 级别图标
      Column() {
        Text(notification.getLevelIcon())
          .fontSize(20)
      }
      .width(36)
      .height(36)
      .margin({ right: 12 })
      .justifyContent(FlexAlign.Center)

      // 通知内容
      Column() {
        Row() {
          Text(notification.title)
            .fontSize(14)
            .fontWeight(FontWeight.Medium)
            .fontColor('#ffffff')
            .layoutWeight(1)

          if (!notification.isRead) {
            Circle()
              .width(8)
              .height(8)
              .fill('#c41e3a')
              .margin({ right: 8 })
          }

          if (notification.isPinned) {
            Text('📌')
              .fontSize(12)
              .margin({ right: 8 })
          }

          Text(notification.timestamp.toLocaleTimeString())
            .fontSize(10)
            .fontColor('#666666')
        }
        .width('100%')

        Text(notification.content)
          .fontSize(12)
          .fontColor('#888888')
          .maxLines(2)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
          .margin({ top: 4 })

        Row() {
          Text(`${notification.sourceIcon} ${notification.source}`)
            .fontSize(10)
            .fontColor('#666666')
            .layoutWeight(1)

          ForEach(notification.actions, (action: NotificationAction) => {
            Button(action.label)
              .fontSize(11)
              .fontColor(action.type === 'primary' ? '#ffffff' : '#888888')
              .backgroundColor(action.type === 'primary' ? '#c41e3a' : '#333333')
              .borderRadius(4)
              .padding({ left: 8, right: 8, top: 2, bottom: 2 })
              .margin({ left: 4 })
              .onClick(() => { action.callback(); })
          })
        }
        .width('100%')
        .margin({ top: 6 })
      }
      .layoutWeight(1)
      .alignItems(HorizontalAlign.Start)
    }
    .width('100%')
    .padding(12)
    .backgroundColor(notification.isRead ? '#0a0a0a' : 'rgba(196,30,58,0.05)')
    .borderRadius(8)
    .margin({ left: 12, right: 12, top: 8 })
  }
}
