// 龍魂 · 预警面板 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { ProjectAlert } from '../models/MilestoneModel';

@Component
export struct RiskPanel {
  @Link alerts: ProjectAlert[];
  onClose?: () => void;

  build() {
    Column() {
      // 标题
      Row() {
        Text('⚠️ 预警面板')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#ffcc00')

        Blank()

        Button() {
          Text('✕')
            .fontSize(20)
            .fontColor('#888')
        }
        .type(ButtonType.Circle)
        .backgroundColor('#00000000')
        .onClick(() => { if (this.onClose) this.onClose(); })
      }
      .width('100%')
      .padding(16)

      // 统计卡片
      Row() {
        this.StatPill('严重', this.alerts.filter(a => a.level === 'critical').length, '#ff0000')
        this.StatPill('警告', this.alerts.filter(a => a.level === 'warning').length, '#ffcc00')
        this.StatPill('信息', this.alerts.filter(a => a.level === 'info').length, '#0066cc')
      }
      .width('100%')
      .padding({ left: 16, right: 16, bottom: 12 })
      .justifyContent(FlexAlign.SpaceEvenly)

      // 预警列表
      if (this.alerts.length === 0) {
        Column() {
          Text('✅')
            .fontSize(48)
            .margin({ top: 40 })
          Text('暂无预警')
            .fontSize(16)
            .fontColor('#666')
            .margin({ top: 12 })
          Text('所有项目运行正常')
            .fontSize(13)
            .fontColor('#444')
            .margin({ top: 4 })
        }
        .width('100%')
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else {
        List() {
          ForEach(this.alerts, (alert: ProjectAlert) => {
            ListItem() {
              this.AlertCard(alert)
            }
          }, (alert: ProjectAlert, index: number) => `${alert.projectId}-${alert.type}-${index}`)
        }
        .width('100%')
        .layoutWeight(1)
        .scrollBar(BarState.Auto)
        .padding({ left: 12, right: 12 })
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder
  StatPill(label: string, count: number, color: string) {
    Column() {
      Text(count.toString())
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .fontColor(color)
      Text(label)
        .fontSize(11)
        .fontColor('#888')
        .margin({ top: 4 })
    }
    .padding({ left: 16, right: 16, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
  }

  @Builder
  AlertCard(alert: ProjectAlert) {
    Row() {
      // 级别色带
      Column()
        .width(4)
        .height('100%')
        .backgroundColor(
          alert.level === 'critical' ? '#ff0000' :
          alert.level === 'warning' ? '#ffcc00' : '#0066cc'
        )
        .borderRadius(2)
        .margin({ right: 12 })

      Column() {
        Row() {
          Text(alert.title)
            .fontSize(15)
            .fontWeight(FontWeight.Medium)
            .fontColor('#fff')
            .layoutWeight(1)
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })

          Text(this.getTypeLabel(alert.type))
            .fontSize(10)
            .fontColor('#666')
            .backgroundColor('#2a2a2a')
            .borderRadius(4)
            .padding({ left: 6, right: 6, top: 1, bottom: 1 })
        }
        .width('100%')

        Text(`${alert.projectName}`)
          .fontSize(12)
          .fontColor('#888')
          .width('100%')
          .margin({ top: 2 })

        Text(alert.message)
          .fontSize(12)
          .fontColor('#666')
          .width('100%')
          .margin({ top: 2 })
          .maxLines(2)
          .textOverflow({ overflow: TextOverflow.Ellipsis })

        Row() {
          Text(alert.timestamp.toLocaleString())
            .fontSize(10)
            .fontColor('#555')

          Blank()

          if (alert.level === 'critical') {
            Button() {
              Text('立即处理')
                .fontSize(10)
                .fontColor('#fff')
            }
            .type(ButtonType.Capsule)
            .backgroundColor('#ff0000')
            .padding({ left: 8, right: 8 })
            .onClick(() => {
              AlertDialog.show({
                title: '处理预警',
                message: `已标记处理: ${alert.title}`,
                primaryButton: { value: '确定', action: () => {} }
              });
            })
          } else if (alert.level === 'warning') {
            Button() {
              Text('查看')
                .fontSize(10)
                .fontColor('#fff')
            }
            .type(ButtonType.Capsule)
            .backgroundColor('#ffcc00')
            .padding({ left: 8, right: 8 })
            .onClick(() => {
              AlertDialog.show({
                title: '预警详情',
                message: alert.message,
                primaryButton: { value: '确定', action: () => {} }
              });
            })
          }
        }
        .width('100%')
        .margin({ top: 6 })
      }
      .layoutWeight(1)
      .alignItems(HorizontalAlign.Start)
    }
    .width('100%')
    .padding(14)
    .backgroundColor(
      alert.level === 'critical' ? 'rgba(255,0,0,0.06)' :
      alert.level === 'warning' ? 'rgba(255,204,0,0.06)' :
      'rgba(0,102,204,0.04)'
    )
    .borderRadius(8)
    .margin({ top: 8 })
  }

  private getTypeLabel(type: string): string {
    const labels: Record<string, string> = {
      delay: '项目延期',
      risk: '风险预警',
      milestone_delay: '里程碑延期',
      budget_overrun: '预算超支',
      resource_conflict: '资源冲突'
    };
    return labels[type] || type;
  }
}
