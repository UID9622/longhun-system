// 龍魂 · 看板视图 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { Project, ProjectStatus, Milestone, MilestoneStatus, RiskLevel, Priority } from '../models/MilestoneModel';

@Component
export struct KanbanView {
  @Link projects: Project[];
  onProjectSelect?: (project: Project) => void;
  onMilestoneUpdate?: (projectId: string, milestoneId: string, progress: number) => void;

  build() {
    if (this.projects.length === 0) {
      Column() {
        Text('📋')
          .fontSize(48)
          .margin({ top: 32 })
        Text('暂无项目看板')
          .fontSize(14)
          .fontColor('#888')
          .margin({ top: 8 })
      }
      .width('100%')
      .layoutWeight(1)
      .justifyContent(FlexAlign.Center)
    } else {
      Scroll() {
        Row() {
          // 四列看板
          this.KanbanColumn('未开始', MilestoneStatus.NOT_STARTED, '#666')
          this.KanbanColumn('进行中', MilestoneStatus.IN_PROGRESS, '#0066cc')
          this.KanbanColumn('风险/延期', MilestoneStatus.AT_RISK, '#ffcc00')
          this.KanbanColumn('已完成', MilestoneStatus.COMPLETED, '#00cc66')
        }
        .height('100%')
        .padding({ left: 8, right: 8, top: 8 })
      }
      .scrollable(ScrollDirection.Horizontal)
      .width('100%')
      .layoutWeight(1)
      .scrollBar(BarState.Auto)
    }
  }

  @Builder
  KanbanColumn(title: string, status: MilestoneStatus, color: string) {
    Column() {
      // 列头部
      Row() {
        Text(title)
          .fontSize(13)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')

        Blank()

        Text(this.countByStatus(status).toString())
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor(color)
      }
      .width('100%')
      .padding({ left: 10, right: 10, top: 8, bottom: 8 })
      .backgroundColor('#1a1a1a')
      .border({ width: { bottom: 2 }, color: color })
      .borderRadius({ topLeft: 8, topRight: 8 })

      // 列内容
      Scroll() {
        Column() {
          ForEach(this.projects, (project: Project) => {
            ForEach(
              project.milestones.filter(m => this.matchesStatus(m, status)),
              (ms: Milestone) => {
                Column() {
                  // 项目标题
                  Text(project.name)
                    .fontSize(9)
                    .fontColor('#666')
                    .width('100%')
                    .maxLines(1)
                    .textOverflow({ overflow: TextOverflow.Ellipsis })
                    .margin({ bottom: 2 })

                  // 里程碑卡片
                  Text(ms.name)
                    .fontSize(12)
                    .fontWeight(FontWeight.Medium)
                    .fontColor('#fff')
                    .width('100%')
                    .maxLines(2)
                    .textOverflow({ overflow: TextOverflow.Ellipsis })
                    .margin({ bottom: 4 })

                  Row() {
                    Text(ms.priority)
                      .fontSize(8)
                      .fontColor(ms.priority === Priority.P0 ? '#ff0000' : '#666')
                      .margin({ right: 6 })

                    Text(`${ms.progress}%`)
                      .fontSize(9)
                      .fontColor(color)
                  }
                  .width('100%')
                  .margin({ bottom: 4 })

                  // 进度滑块（进行中才可拖）
                  if (status === MilestoneStatus.IN_PROGRESS) {
                    Slider({
                      value: ms.progress,
                      min: 0,
                      max: 100,
                      step: 5,
                      style: SliderStyle.InSet
                    })
                    .width('100%')
                    .height(16)
                    .onChange((v: number) => {
                      if (this.onMilestoneUpdate) {
                        this.onMilestoneUpdate(project.id, ms.id, v);
                      }
                    })
                  } else {
                    Stack() {
                      Row()
                        .width('100%')
                        .height(3)
                        .backgroundColor('#333')
                        .borderRadius(1.5)
                      Row()
                        .width(`${ms.progress}%`)
                        .height(3)
                        .backgroundColor(color)
                        .borderRadius(1.5)
                    }
                    .width('100%')
                    .height(3)
                  }

                  if (ms.getDelayDays() > 0) {
                    Text(`⏰ 延期${ms.getDelayDays()}天`)
                      .fontSize(9)
                      .fontColor('#ff6600')
                      .width('100%')
                      .margin({ top: 4 })
                  }
                }
                .width('100%')
                .padding(10)
                .backgroundColor('#1a1a1a')
                .borderRadius(6)
                .margin({ top: 6 })
                .onClick(() => {
                  if (this.onProjectSelect) this.onProjectSelect(project);
                })
              },
              (ms: Milestone) => ms.id
            )
          }, (project: Project) => project.id)

          if (this.countByStatus(status) === 0) {
            Text('暂无')
              .fontSize(12)
              .fontColor('#555')
              .width('100%')
              .textAlign(TextAlign.Center)
              .padding({ top: 24, bottom: 24 })
          }
        }
        .width('100%')
        .padding({ left: 8, right: 8, top: 4, bottom: 8 })
      }
      .width('100%')
      .layoutWeight(1)
      .scrollBar(BarState.Auto)
    }
    .width(220)
    .layoutWeight(1)
    .height('100%')
    .backgroundColor('#0a0a0a')
    .borderRadius(8)
    .border({ width: 1, color: '#333' })
    .margin({ right: 8 })
  }

  private countByStatus(status: MilestoneStatus): number {
    let count = 0;
    this.projects.forEach(p => {
      count += p.milestones.filter(m => this.matchesStatus(m, status)).length;
    });
    return count;
  }

  private matchesStatus(ms: Milestone, status: MilestoneStatus): boolean {
    if (status === MilestoneStatus.AT_RISK) {
      return ms.status === MilestoneStatus.AT_RISK || ms.status === MilestoneStatus.DELAYED || ms.status === MilestoneStatus.BLOCKED;
    }
    if (status === MilestoneStatus.IN_PROGRESS) {
      return ms.status === MilestoneStatus.IN_PROGRESS;
    }
    if (status === MilestoneStatus.COMPLETED) {
      return ms.status === MilestoneStatus.COMPLETED;
    }
    return ms.status === MilestoneStatus.NOT_STARTED;
  }
}
