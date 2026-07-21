// 龍魂 · 时间线瀑布流视图 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { Project, ProjectStatus, Milestone, MilestoneStatus, RiskLevel, Priority } from '../models/MilestoneModel';

@Component
export struct TimelineView {
  @Link projects: Project[];
  @Prop timeRange: string = 'quarter';
  onProjectSelect?: (project: Project) => void;
  onMilestoneSelect?: (projectId: string, milestone: Milestone) => void;

  build() {
    if (this.projects.length === 0) {
      Column() {
        Text('📅')
          .fontSize(48)
          .margin({ top: 32 })
        Text('暂无项目时间线')
          .fontSize(14)
          .fontColor('#888')
          .margin({ top: 8 })
      }
      .width('100%')
      .layoutWeight(1)
      .justifyContent(FlexAlign.Center)
    } else {
      List() {
        ForEach(this.projects, (project: Project) => {
          ListItem() {
            Column() {
              // 项目头部
              Row() {
                Text('◆')
                  .fontSize(16)
                  .fontColor(this.getTimelineDotColor(project.status))
                  .margin({ right: 10 })

                Column() {
                  Text(project.name)
                    .fontSize(15)
                    .fontWeight(FontWeight.Bold)
                    .fontColor('#fff')

                  Row() {
                    Text(`🎯 ${project.getProgress()}%`)
                      .fontSize(11)
                      .fontColor('#00cc66')
                      .margin({ right: 10 })

                    if (project.getDelayDays() > 0) {
                      Text(`⏰ 延期${project.getDelayDays()}天`)
                        .fontSize(11)
                        .fontColor('#ffcc00')
                    }

                    if (project.getCurrentRiskLevel() >= RiskLevel.HIGH) {
                      Text('⚠️')
                        .fontSize(12)
                        .margin({ left: 8 })
                    }
                  }
                  .margin({ top: 4 })
                }
                .alignItems(HorizontalAlign.Start)
                .layoutWeight(1)

                Text(`${project.plannedStart.toLocaleDateString().substring(5)} → ${project.plannedEnd.toLocaleDateString().substring(5)}`)
                  .fontSize(10)
                  .fontColor('#555')
              }
              .width('100%')
              .padding({ left: 12, right: 16, top: 12, bottom: 8 })
              .onClick(() => {
                if (this.onProjectSelect) this.onProjectSelect(project);
              })

              // 里程碑时间线
              Column() {
                // 时间线竖线
                Column()
                  .width(2)
                  .backgroundColor('#444')
                  .position({ x: 20, y: 0 })
                  .height(this.getMilestoneCount(project) * 72)

                ForEach(project.milestones.sort((a, b) => a.plannedStart.getTime() - b.plannedStart.getTime()),
                  (ms: Milestone, index: number) => {
                    Row() {
                      // 时间线节点
                      Column() {
                        // 节点圆点
                        if (index > 0) {
                          Column()
                            .width(2)
                            .height(12)
                            .backgroundColor('#444')
                        } else {
                          Column().width(2).height(12)
                        }

                        Row()
                          .width(10)
                          .height(10)
                          .backgroundColor(this.getMilestoneDotColor(ms.status))
                          .borderRadius(5)
                          .border({ width: 2, color: '#333' })
                      }
                      .width(42)
                      .alignItems(HorizontalAlign.Center)

                      // 里程碑卡片
                      Column() {
                        Row() {
                          Text(ms.name)
                            .fontSize(13)
                            .fontWeight(FontWeight.Medium)
                            .fontColor('#fff')
                            .layoutWeight(1)
                            .maxLines(1)
                            .textOverflow({ overflow: TextOverflow.Ellipsis })

                          Text(ms.priority)
                            .fontSize(9)
                            .fontColor(this.getPriorityColor(ms.priority))
                            .backgroundColor(this.getPriorityBgColor(ms.priority))
                            .borderRadius(3)
                            .padding({ left: 5, right: 5, top: 1, bottom: 1 })
                        }
                        .width('100%')

                        Row() {
                          Text(`${ms.plannedStart.toLocaleDateString().substring(5)} → ${ms.plannedEnd.toLocaleDateString().substring(5)}`)
                            .fontSize(10)
                            .fontColor('#666')
                            .layoutWeight(1)

                          Text(ms.status)
                            .fontSize(10)
                            .fontColor(this.getMilestoneDotColor(ms.status))
                        }
                        .width('100%')
                        .margin({ top: 4 })

                        // 进度条
                        Row() {
                          Stack() {
                            Row()
                              .width('100%')
                              .height(3)
                              .backgroundColor('#333')
                              .borderRadius(1.5)
                            Row()
                              .width(`${ms.progress}%`)
                              .height(3)
                              .backgroundColor(this.getMilestoneDotColor(ms.status))
                              .borderRadius(1.5)
                          }
                          .layoutWeight(1)
                          .height(3)

                          Text(`${ms.progress}%`)
                            .fontSize(9)
                            .fontColor('#666')
                            .margin({ left: 6 })
                        }
                        .width('100%')
                        .margin({ top: 4 })
                      }
                      .layoutWeight(1)
                      .padding({ left: 12, right: 12, top: 8, bottom: 8 })
                      .backgroundColor('#1a1a1a')
                      .borderRadius(6)
                      .onClick(() => {
                        if (this.onMilestoneSelect) this.onMilestoneSelect(project.id, ms);
                      })
                    }
                    .width('100%')
                    .padding({ left: 2, right: 12, bottom: 4 })
                  }, (ms: Milestone) => ms.id)
              }
              .width('100%')
              .padding({ bottom: 12 })
            }
            .width('100%')
            .margin({ top: 8, left: 8, right: 8 })
            .backgroundColor('rgba(196,30,58,0.03)')
            .borderRadius(10)
            .border({ width: 1, color: '#333' })
          }
        }, (project: Project) => project.id)
      }
      .width('100%')
      .layoutWeight(1)
      .scrollBar(BarState.Auto)
      .edgeEffect(EdgeEffect.Spring)
      .padding({ bottom: 16 })
    }
  }

  private getMilestoneCount(project: Project): number {
    return project.milestones.length;
  }

  private getTimelineDotColor(status: ProjectStatus): string {
    switch (status) {
      case ProjectStatus.ACTIVE: return '#00ff00';
      case ProjectStatus.COMPLETED: return '#0066cc';
      case ProjectStatus.PLANNING: return '#ffcc00';
      case ProjectStatus.PAUSED: return '#ff6600';
      case ProjectStatus.CANCELLED: return '#666';
      case ProjectStatus.ARCHIVED: return '#444';
      default: return '#888';
    }
  }

  private getMilestoneDotColor(status: MilestoneStatus): string {
    switch (status) {
      case MilestoneStatus.COMPLETED: return '#00cc66';
      case MilestoneStatus.IN_PROGRESS: return '#0066cc';
      case MilestoneStatus.AT_RISK: return '#ffcc00';
      case MilestoneStatus.DELAYED: return '#ff6600';
      case MilestoneStatus.BLOCKED: return '#ff0000';
      default: return '#666';
    }
  }

  private getPriorityColor(p: Priority): string {
    if (p === Priority.P0) return '#ff0000';
    if (p === Priority.P1) return '#ff6600';
    if (p === Priority.P2) return '#ffcc00';
    return '#888';
  }

  private getPriorityBgColor(p: Priority): string {
    if (p === Priority.P0) return 'rgba(255,0,0,0.15)';
    if (p === Priority.P1) return 'rgba(255,102,0,0.15)';
    if (p === Priority.P2) return 'rgba(255,204,0,0.15)';
    return 'rgba(136,136,136,0.1)';
  }
}
