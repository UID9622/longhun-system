// 龍魂 · 预警面板组件 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { AlertItem, sealState } from '../models/SealModel';

@Component
export struct AlertBanner {
  @Prop alerts: AlertItem[] = [];
  onClose?: () => void;

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('⚠️ 预警中心')
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
          .fontColor('#ffcc00')
        Blank()
        Text(`${this.alerts.length}条`)
          .fontSize(12)
          .fontColor('#888')
          .backgroundColor('#2a2a2a')
          .borderRadius(10)
          .padding({ left: 8, right: 8 })
          .margin({ right: 8 })
        if (this.onClose) {
          Button() {
            Text('✕')
              .fontSize(18)
              .fontColor('#888')
          }
          .type(ButtonType.Circle)
          .backgroundColor('transparent')
          .width(32)
          .height(32)
          .onClick(() => {
            if (this.onClose) {
              this.onClose();
            }
          })
        }
      }
      .width('100%')
      .padding({ left: 16, right: 16, top: 12, bottom: 8 })

      // 统计卡片
      Row() {
        this.MiniStat('超期', this.countByLevel('critical'), '#ff0000')
        this.MiniStat('警告', this.countByLevel('warning'), '#ffcc00')
        this.MiniStat('提示', this.countByLevel('info'), '#0066cc')
      }
      .width('100%')
      .padding({ left: 16, right: 16, bottom: 8 })
      .justifyContent(FlexAlign.SpaceAround)

      // 预警列表
      List() {
        ForEach(this.alerts, (alert: AlertItem) => {
          ListItem() {
            this.AlertCard(alert)
          }
        }, (alert: AlertItem) => `${alert.type}-${alert.title}-${alert.timestamp.getTime()}`)
      }
      .width('100%')
      .layoutWeight(1)
      .divider({ strokeWidth: 1, color: '#222' })
      .scrollBar(BarState.Auto)
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder
  MiniStat(label: string, count: number, color: string) {
    Column() {
      Text(`${count}`)
        .fontSize(22)
        .fontWeight(FontWeight.Bold)
        .fontColor(color)
      Text(label)
        .fontSize(11)
        .fontColor('#888')
        .margin({ top: 2 })
    }
    .width('30%')
    .padding(10)
    .backgroundColor('rgba(255,255,255,0.03)')
    .borderRadius(8)
    .border({ width: 1, color: `${color}33` })
  }

  @Builder
  AlertCard(alert: AlertItem) {
    Row() {
      // 级别图标
      Column() {
        Text(
          alert.level === 'critical' ? '🔴' :
          alert.level === 'warning' ? '🟡' : '🔵'
        )
          .fontSize(20)
      }
      .width(36)
      .height(36)
      .justifyContent(FlexAlign.Center)
      .margin({ right: 10 })

      // 内容
      Column() {
        Text(alert.title)
          .fontSize(14)
          .fontWeight(FontWeight.Medium)
          .fontColor(
            alert.level === 'critical' ? '#ff0000' :
            alert.level === 'warning' ? '#ffcc00' : '#fff'
          )
          .maxLines(1)
          .textOverflow({ overflow: TextOverflow.Ellipsis })

        Text(alert.message)
          .fontSize(12)
          .fontColor('#888')
          .maxLines(2)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
          .margin({ top: 2 })

        Text(alert.timestamp.toLocaleString())
          .fontSize(10)
          .fontColor('#555')
          .margin({ top: 4 })
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      // 操作按钮
      Column() {
        if (alert.type === 'overdue') {
          Button('处理')
            .fontSize(11)
            .fontColor('#fff')
            .backgroundColor('#ff6600')
            .borderRadius(4)
            .padding({ left: 8, right: 8 })
            .onClick(() => {
              this.handleAlert(alert);
            })
        } else if (alert.type === 'pending') {
          Button('审批')
            .fontSize(11)
            .fontColor('#fff')
            .backgroundColor('#0066cc')
            .borderRadius(4)
            .padding({ left: 8, right: 8 })
            .onClick(() => {
              this.handleAlert(alert);
            })
        }
      }
      .margin({ left: 8 })
    }
    .width('100%')
    .padding(12)
    .backgroundColor(
      alert.level === 'critical' ? 'rgba(255,0,0,0.05)' :
      alert.level === 'warning' ? 'rgba(255,204,0,0.05)' :
      'rgba(0,102,204,0.05)'
    )
    .margin({ left: 12, right: 12, top: 6, bottom: 6 })
    .borderRadius(8)
    .border({
      width: { left: 3 },
      color:
        alert.level === 'critical' ? '#ff0000' :
        alert.level === 'warning' ? '#ffcc00' : '#0066cc'
    })
  }

  private countByLevel(level: string): number {
    return this.alerts.filter(a => a.level === level).length;
  }

  private handleAlert(alert: AlertItem) {
    // 处理预警：外带超期→跳转外带追踪页
    // 待审批→跳转审批页
    console.info(`处理预警: ${alert.type} - ${alert.title}`);
  }
}
