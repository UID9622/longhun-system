// 龍魂 · 甘特图视图 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { Project, ProjectStatus, Milestone, MilestoneStatus, RiskLevel } from '../models/MilestoneModel';

@Component
export struct GanttChartView {
  @Link projects: Project[];
  @Prop timeRange: string = 'quarter';
  onProjectSelect?: (project: Project) => void;

  @State private scrollOffset: number = 0;
  @State private dayWidth: number = 3;  // 每天宽度(px)
  @State private headerHeight: number = 36;
  @State private rowHeight: number = 32;
  @State private barHeight: number = 20;
  @State private labelWidth: number = 160;

  private totalDays: number = 0;
  private chartStartDate: Date = new Date();
  private chartEndDate: Date = new Date();

  aboutToAppear() {
    this.calculateDateRange();
  }

  private calculateDateRange(): void {
    const now = new Date();
    switch (this.timeRange) {
      case 'week':
        this.chartStartDate = new Date(now.getTime() - 7*24*60*60*1000);
        this.chartEndDate = new Date(now.getTime() + 14*24*60*60*1000);
        break;
      case 'month':
        this.chartStartDate = new Date(now.getFullYear(), now.getMonth(), 1);
        this.chartEndDate = new Date(now.getFullYear(), now.getMonth() + 2, 0);
        break;
      case 'quarter':
        this.chartStartDate = new Date(now.getFullYear(), Math.floor(now.getMonth()/3)*3, 1);
        this.chartEndDate = new Date(now.getFullYear(), Math.floor(now.getMonth()/3)*3 + 4, 0);
        break;
      case 'year':
        this.chartStartDate = new Date(now.getFullYear(), 0, 1);
        this.chartEndDate = new Date(now.getFullYear() + 1, 1, 0);
        break;
      default: // all
        this.chartStartDate = new Date(now.getFullYear() - 1, 0, 1);
        this.chartEndDate = new Date(now.getFullYear() + 1, 0, 1);
    }
    this.totalDays = Math.ceil((this.chartEndDate.getTime() - this.chartStartDate.getTime()) / (1000*60*60*24));
  }

  build() {
    Column() {
      if (this.projects.length === 0) {
        this.EmptyState()
      } else {
        Scroll() {
          Column() {
            // 每个项目一个区块
            ForEach(this.projects, (project: Project) => {
              Column() {
                // 项目标题行
                Row() {
                  Text(project.name)
                    .fontSize(12)
                    .fontWeight(FontWeight.Medium)
                    .fontColor('#fff')
                    .width(this.labelWidth)
                    .padding({ left: 8 })
                    .maxLines(1)
                    .textOverflow({ overflow: TextOverflow.Ellipsis })
                    .onClick(() => {
                      if (this.onProjectSelect) this.onProjectSelect(project);
                    })

                  // 时间轴占位
                  Row()
                    .width(this.totalDays * this.dayWidth)
                    .height(this.rowHeight)
                    .backgroundColor('#111')
                }
                .width('100%')
                .height(this.rowHeight)
                .backgroundColor('#1a1a1a')
                .border({ width: { bottom: 1 }, color: '#333' })
                .onClick(() => {
                  if (this.onProjectSelect) this.onProjectSelect(project);
                })

                // 里程碑条形图
                ForEach(project.milestones, (ms: Milestone) => {
                  Row() {
                    Text(`  ${ms.name}`)
                      .fontSize(11)
                      .fontColor('#aaa')
                      .width(this.labelWidth)
                      .padding({ left: 12 })
                      .maxLines(1)
                      .textOverflow({ overflow: TextOverflow.Ellipsis })

                    Stack({ alignContent: Alignment.Start }) {
                      Row()
                        .width(this.totalDays * this.dayWidth)
                        .height(this.rowHeight)
                        .backgroundColor('#0a0a0a')

                      // 里程碑条形
                      if (this.isBarVisible(ms)) {
                        Row()
                          .width(this.getBarWidth(ms))
                          .height(this.barHeight)
                          .backgroundColor(this.getBarColor(ms))
                          .borderRadius(4)
                          .position({
                            x: this.getBarX(ms),
                            y: (this.rowHeight - this.barHeight) / 2
                          })
                      }
                    }
                    .width(this.totalDays * this.dayWidth)
                    .height(this.rowHeight)
                  }
                  .width('100%')
                  .height(this.rowHeight)
                  .border({ width: { bottom: 1 }, color: '#222' })
                }, (ms: Milestone) => ms.id)
              }
              .width('100%')
              .margin({ bottom: 16 })
            }, (project: Project) => project.id)
          }
          .width('100%')
        }
        .width('100%')
        .layoutWeight(1)
        .scrollable(ScrollDirection.Horizontal)
        .scrollBar(BarState.Auto)

        // 图例
        Row() {
          this.LegendItem('未开始', '#666')
          this.LegendItem('进行中', '#0066cc')
          this.LegendItem('有风险', '#ffcc00')
          this.LegendItem('已延期', '#ff6600')
          this.LegendItem('已完成', '#00cc66')
          this.LegendItem('被阻塞', '#ff0000')
        }
        .width('100%')
        .padding({ left: 12, right: 12, top: 6, bottom: 6 })
        .backgroundColor('#1a1a1a')
        .justifyContent(FlexAlign.SpaceEvenly)
      }
    }
    .width('100%')
    .layoutWeight(1)
    .backgroundColor('#0a0a0a')
  }

  @Builder
  EmptyState() {
    Column() {
      Text('📊')
        .fontSize(48)
        .margin({ top: 32 })
      Text('暂无项目数据')
        .fontSize(14)
        .fontColor('#888')
        .margin({ top: 8 })
      Text('请先创建一个项目')
        .fontSize(12)
        .fontColor('#555')
        .margin({ top: 4 })
    }
    .width('100%')
    .layoutWeight(1)
    .justifyContent(FlexAlign.Center)
  }

  @Builder
  LegendItem(label: string, color: string) {
    Row() {
      Row()
        .width(12)
        .height(12)
        .backgroundColor(color)
        .borderRadius(2)
        .margin({ right: 4 })
      Text(label)
        .fontSize(9)
        .fontColor('#888')
    }
  }

  private isBarVisible(ms: Milestone): boolean {
    const msStart = ms.plannedStart.getTime();
    const msEnd = ms.plannedEnd.getTime();
    const chartStart = this.chartStartDate.getTime();
    const chartEnd = this.chartEndDate.getTime();
    return msStart < chartEnd && msEnd > chartStart;
  }

  private getBarX(ms: Milestone): number {
    const msStart = ms.plannedStart.getTime();
    const chartStart = this.chartStartDate.getTime();
    const offset = Math.max(0, (msStart - chartStart) / (1000*60*60*24));
    return offset * this.dayWidth;
  }

  private getBarWidth(ms: Milestone): number {
    const chartStart = this.chartStartDate.getTime();
    const chartEnd = this.chartEndDate.getTime();
    const msStart = Math.max(ms.plannedStart.getTime(), chartStart);
    const msEnd = Math.min(ms.plannedEnd.getTime(), chartEnd);
    const days = Math.max(1, (msEnd - msStart) / (1000*60*60*24));
    return days * this.dayWidth;
  }

  private getBarColor(ms: Milestone): string {
    switch (ms.status) {
      case MilestoneStatus.COMPLETED: return '#00cc66';
      case MilestoneStatus.IN_PROGRESS: return '#0066cc';
      case MilestoneStatus.AT_RISK: return '#ffcc00';
      case MilestoneStatus.DELAYED: return '#ff6600';
      case MilestoneStatus.BLOCKED: return '#ff0000';
      default: return '#666';
    }
  }
}
