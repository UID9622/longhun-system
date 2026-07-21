// entry/src/main/ets/components/AlertPanel.ets
// 龍魂 · 预警面板组件

import { AlertItem, inventoryState, ApprovalStatus } from '../models/InventoryModel';

@Component
export struct AlertPanel {
  @Prop alerts: AlertItem[] = [];
  onClose?: () => void;

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('⚠️ 预警中心')
          .fontSize(16).fontWeight(FontWeight.Bold).fontColor('#ffcc00').layoutWeight(1)
        Text(`${this.alerts.length}条`).fontSize(12).fontColor('#888').margin({ right: 8 })
        Button() { Text('✕').fontSize(14).fontColor('#888') }
          .type(ButtonType.Circle).backgroundColor('transparent')
          .width(28).height(28)
          .onClick(() => {
            if (this.onClose) {
              this.onClose();
            }
          })
      }
      .width('100%').padding({ left: 16, right: 16, top: 12, bottom: 8 })

      // 预警统计
      Row() {
        this.AlertStat('严重', this.alerts.filter(a => a.level === 'critical').length, '#ff0000')
        this.AlertStat('警告', this.alerts.filter(a => a.level === 'warning').length, '#ffcc00')
        this.AlertStat('信息', this.alerts.filter(a => a.level === 'info').length, '#00aaff')
      }
      .width('100%').padding({ left: 16, right: 16, bottom: 8 })
      .justifyContent(FlexAlign.SpaceAround)

      // 快捷操作
      Row() {
        Button('一键补货')
          .fontSize(11).fontColor('#fff').backgroundColor('#00aa00')
          .borderRadius(4).padding({ left: 12, right: 12 }).height(28)
          .onClick(() => {
            const lowItems = inventoryState.items.filter(i => i.needsReorder());
            // 自动生成补货建议
          })
        Button('盘点提醒').fontSize(11).fontColor('#fff').backgroundColor('#0066cc')
          .borderRadius(4).padding({ left: 12, right: 12 }).height(28)
        Button('导出预警').fontSize(11).fontColor('#888').backgroundColor('#333')
          .borderRadius(4).padding({ left: 12, right: 12 }).height(28)
        Button('全部忽略').fontSize(11).fontColor('#888').backgroundColor('#333')
          .borderRadius(4).padding({ left: 12, right: 12 }).height(28)
      }
      .width('100%').padding({ left: 16, right: 16, bottom: 8 })
      .justifyContent(FlexAlign.SpaceBetween)

      Divider().color('#333').margin({ left: 16, right: 16 })

      // 预警列表
      List() {
        ForEach(this.alerts, (alert: AlertItem, index: number) => {
          ListItem() {
            Row() {
              // 级别图标
              Text(alert.level === 'critical' ? '🔴' :
                   alert.level === 'warning' ? '🟡' : '🔵')
                .fontSize(16).margin({ right: 8 })

              Column() {
                Text(alert.title)
                  .fontSize(13).fontWeight(FontWeight.Medium)
                  .fontColor('#fff')
                Text(alert.message)
                  .fontSize(11).fontColor('#888')
                  .maxLines(2).textOverflow({ overflow: TextOverflow.Ellipsis })
                  .margin({ top: 2 })
              }
              .alignItems(HorizontalAlign.Start).layoutWeight(1)

              Column() {
                Text(this.formatTime(alert.timestamp))
                  .fontSize(10).fontColor('#666')
                  .margin({ bottom: 4 })

                // 操作按钮
                Row() {
                  if (alert.type === 'low_stock' || alert.type === 'out_of_stock') {
                    Button('补货').fontSize(10).fontColor('#00aa00')
                      .backgroundColor('rgba(0,170,0,0.15)')
                      .borderRadius(4).padding({ left: 6, right: 6 }).height(22)
                  }
                  if (alert.type === 'pending_approval') {
                    Button('审批').fontSize(10).fontColor('#0066cc')
                      .backgroundColor('rgba(0,102,204,0.15)')
                      .borderRadius(4).padding({ left: 6, right: 6 }).height(22)
                  }
                  if (alert.type === 'expired') {
                    Button('报废').fontSize(10).fontColor('#ff0000')
                      .backgroundColor('rgba(255,0,0,0.15)')
                      .borderRadius(4).padding({ left: 6, right: 6 }).height(22)
                  }
                }
              }
              .alignItems(HorizontalAlign.End)
            }
            .width('100%').padding(12)
          }
          .backgroundColor(index % 2 === 0 ? '#0a0a0a' : '#111')
        })
      }
      .layoutWeight(1)
      .divider({ strokeWidth: 0.5, color: '#2a2a2a' })
      .scrollBar(BarState.Auto)
    }
    .width('100%')
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: 'rgba(255,204,0,0.3)' })
  }

  @Builder
  AlertStat(label: string, count: number, color: string) {
    Column() {
      Text(`${count}`).fontSize(20).fontWeight(FontWeight.Bold).fontColor(color)
      Text(label).fontSize(11).fontColor('#888').margin({ top: 2 })
    }
    .padding(8)
    .backgroundColor('#222')
    .borderRadius(8)
    .width('28%')
  }

  private formatTime(date: Date): string {
    const now = new Date();
    const diff = now.getTime() - new Date(date).getTime();
    if (diff < 60000) return '刚刚';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`;
    return new Date(date).toLocaleDateString();
  }
}
