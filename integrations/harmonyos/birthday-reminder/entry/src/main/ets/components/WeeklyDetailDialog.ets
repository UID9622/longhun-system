// entry/src/main/ets/components/WeeklyDetailDialog.ets
// 龍魂 · 周报详情查看/编辑弹窗 · ArkTS

import { WeeklyReport, WeeklyStatus, WeeklyTask, TaskStatus, NextTask, WeeklyIssue, WeeklyRisk } from '../models/WeeklyModel';

@CustomDialog
export struct WeeklyDetailDialog {
  controller: CustomDialogController;
  report?: WeeklyReport;
  onSave?: (report: WeeklyReport) => void;
  onDelete?: (id: string) => void;
  onClose?: () => void;

  @State private editingReport: WeeklyReport | null = null;
  @State private isEditing: boolean = false;
  @State private summary: string = '';
  @State private nextPlan: string = '';
  @State private needSupport: string = '';
  @State private showDeleteConfirm: boolean = false;

  aboutToAppear() {
    if (this.report) {
      this.editingReport = this.report;
      this.summary = this.report.summary || '';
      this.nextPlan = this.report.nextPlan || '';
      this.needSupport = this.report.needSupport || '';
    }
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text(this.isEditing ? '编辑周报' : '周报详情').fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff').layoutWeight(1)
        Row() {
          if (this.editingReport && this.editingReport.isEditable() && !this.isEditing) {
            Text('✏️').fontSize(18).fontColor('#c41e3a').margin({ right: 12 })
            .onClick(() => { this.isEditing = true; })
          }
          Text('✕').fontSize(20).fontColor('#888')
          .onClick(() => { this.controller.close(); })
        }
      }
      .width('100%').padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      Scroll() {
        Column() {
          if (this.editingReport) {
            // 基本信息
            this.BasicInfoBuilder()

            // 统计
            this.StatsSummaryBuilder()

            // 审批进度
            if (this.editingReport.approvals.length > 0) {
              this.ApprovalProgressBuilder()
            }

            // 任务列表
            this.TaskListBuilder()

            // 下周计划
            if (this.editingReport.nextTasks.length > 0) {
              this.NextTasksBuilder()
            }

            // 问题与风险
            if (this.editingReport.issues.length > 0 || this.editingReport.risks.length > 0) {
              this.IssuesRisksBuilder()
            }

            // 总结区
            this.SummaryBuilder()

            // 审计信息
            this.AuditInfoBuilder()
          }
        }
      }
      .width('100%').layoutWeight(1)
      .scrollBar(BarState.Auto)

      // 底部操作
      if (this.editingReport && this.editingReport.isEditable() && this.isEditing) {
        this.EditFooterBuilder()
      } else if (this.editingReport && this.editingReport.status === WeeklyStatus.DRAFT) {
        this.DraftFooterBuilder()
      } else {
        this.ViewFooterBuilder()
      }
    }
    .width('100%').height('90%').backgroundColor('#1a1a1a').borderRadius({ topLeft: 16, topRight: 16 })
  }

  @Builder
  BasicInfoBuilder() {
    Column() {
      Row() {
        Text(this.editingReport!.reportNo).fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff')
        Blank()
        Text(this.editingReport!.status)
          .fontSize(12).fontColor(this.getStatusColor(this.editingReport!.status))
          .backgroundColor(this.getStatusBg(this.editingReport!.status))
          .borderRadius(4).padding({ left: 8, right: 8, top: 2, bottom: 2 })
      }
      .width('100%')
      Row() {
        Text(`${this.editingReport!.weekStart.toLocaleDateString()} - ${this.editingReport!.weekEnd.toLocaleDateString()}`).fontSize(12).fontColor('#888')
        Blank()
        Text(`${this.editingReport!.reporter} · ${this.editingReport!.department}`).fontSize(12).fontColor('#888')
      }
      .width('100%').margin({ top: 6 })
    }
    .width('100%').padding(16)
    .backgroundColor('rgba(196,30,58,0.05)')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatsSummaryBuilder() {
    Row() {
      this.MiniStat(`📋 ${this.editingReport!.tasks.length}项`, '#0088ff')
      this.MiniStat(`⏱️ ${this.editingReport!.totalActualHours}h`, '#00cc66')
      if (this.editingReport!.totalOvertimeHours > 0) {
        this.MiniStat(`🔥 ${this.editingReport!.totalOvertimeHours}h`, '#ff6600')
      }
      this.MiniStat(`✅ ${this.editingReport!.completionRate}%`, '#00ff00')
    }
    .width('100%').padding({ left: 8, right: 8, top: 8, bottom: 8 })
    .justifyContent(FlexAlign.SpaceAround)
  }

  @Builder
  MiniStat(text: string, color: string) {
    Column() {
      Text(text).fontSize(12).fontColor(color)
    }
    .height(32).justifyContent(FlexAlign.Center)
  }

  @Builder
  ApprovalProgressBuilder() {
    Column() {
      Text('审批进度').fontSize(13).fontWeight(FontWeight.Medium).fontColor('#8af').margin({ bottom: 8 }).alignSelf(ItemAlign.Start)
      ForEach(this.editingReport!.approvals, (record: Record<string, Object>, index: number) => {
        Row() {
          Column() {
            Circle({ width: 10, height: 10 })
              .fill(record.signature === 'REJECTED' ? '#ff4444' : '#00cc66')
            if (index < this.editingReport!.approvals.length - 1) {
              Divider().vertical(true).height(30).color('#444').margin({ top: 3, bottom: 3 })
            }
          }
          .margin({ right: 10 })
          Column() {
            Text(`${record.signature === 'REJECTED' ? '驳回' : '通过'} · L${record.level}`).fontSize(13).fontColor('#fff')
            Text(`${record.approver}${record.comment ? ' · ' + record.comment : ''}`).fontSize(11).fontColor('#888').margin({ top: 2 })
          }
          .alignItems(HorizontalAlign.Start).layoutWeight(1)
          Text(new Date((record.timestamp as number)).toLocaleTimeString()).fontSize(10).fontColor('#555')
        }
        .width('100%').alignItems(VerticalAlign.Top)
      })
    }
    .width('100%').padding(16)
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  TaskListBuilder() {
    Column() {
      Row() {
        Text(`本周任务 (${this.editingReport!.tasks.length})`).fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').layoutWeight(1)
        if (this.isEditing) {
          Text('+').fontSize(20).fontColor('#c41e3a').onClick(() => { /* 添加任务 */ })
        }
      }
      .width('100%').margin({ bottom: 8 })

      ForEach(this.editingReport!.tasks, (task: Record<string, Object>) => {
        Row() {
          Text(this.getTaskStatusEmoji(task.status as string)).fontSize(16).margin({ right: 8 })
          Column() {
            Text((task.title as string) || '未命名').fontSize(14).fontColor('#fff').maxLines(1).textOverflow({ overflow: TextOverflow.Ellipsis })
            Row() {
              Text(`${task.projectName} · ${task.taskType}`).fontSize(11).fontColor('#666')
              Text(`${task.progress}%`).fontSize(11).fontColor(this.getProgressColor(task.progress as number)).margin({ left: 8 })
            }
            .width('100%').margin({ top: 2 })
          }
          .alignItems(HorizontalAlign.Start).layoutWeight(1)
          Column() {
            Text(`${task.actualHours}h`).fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
            Text(`/${task.plannedHours}h`).fontSize(10).fontColor('#666')
          }
          .alignItems(HorizontalAlign.End)
        }
        .width('100%').padding(8)
        .backgroundColor('rgba(255,255,255,0.03)').borderRadius(6).margin({ bottom: 4 })
      }, (task: Record<string, Object>) => task.id as string)

      if (this.editingReport!.tasks.length === 0) {
        Text('暂无任务').fontSize(12).fontColor('#666').padding(16).width('100%').textAlign(TextAlign.Center)
      }
    }
    .width('100%').padding(16)
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  NextTasksBuilder() {
    Column() {
      Text(`下周计划 (${this.editingReport!.nextTasks.length})`).fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').margin({ bottom: 8 }).alignSelf(ItemAlign.Start)
      ForEach(this.editingReport!.nextTasks, (task: Record<string, Object>) => {
        Row() {
          Text((task.taskType as string) || '其他').fontSize(11).fontColor('#8af')
            .backgroundColor('rgba(136,170,255,0.1)').borderRadius(4)
            .padding({ left: 6, right: 6, top: 2, bottom: 2 }).margin({ right: 8 })
          Text((task.title as string) || '未命名').fontSize(13).fontColor('#ccc').layoutWeight(1)
          Text(`${task.plannedHours}h`).fontSize(12).fontColor('#888')
        }
        .width('100%').height(32)
      })
    }
    .width('100%').padding(16)
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  IssuesRisksBuilder() {
    Column() {
      if (this.editingReport!.issues.length > 0) {
        Text(`问题 (${this.editingReport!.issues.length})`).fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').margin({ bottom: 8 }).alignSelf(ItemAlign.Start)
        ForEach(this.editingReport!.issues, (issue: Record<string, Object>) => {
          Row() {
            Text(this.getSeverityEmoji(issue.severity as string)).fontSize(14).margin({ right: 8 })
            Text((issue.title as string) || '').fontSize(13).fontColor('#ffcc00').layoutWeight(1)
            Text(issue.status as string).fontSize(11).fontColor('#888')
          }
          .width('100%').height(28)
        })
      }
      if (this.editingReport!.risks.length > 0) {
        Text(`风险 (${this.editingReport!.risks.length})`).fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').margin({ top: 12, bottom: 8 }).alignSelf(ItemAlign.Start)
        ForEach(this.editingReport!.risks, (risk: Record<string, Object>) => {
          Row() {
            Text('⚠️').fontSize(14).margin({ right: 8 })
            Text((risk.title as string) || '').fontSize(13).fontColor('#ff6600').layoutWeight(1)
            Text(risk.status as string).fontSize(11).fontColor('#888')
          }
          .width('100%').height(28)
        })
      }
    }
    .width('100%').padding(16)
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  SummaryBuilder() {
    Column() {
      if (this.editingReport!.summary) {
        Text('本周总结').fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').margin({ bottom: 6 }).alignSelf(ItemAlign.Start)
        if (this.isEditing) {
          TextArea({ text: $$this.summary, placeholder: '填写本周工作总结...' })
            .height(80).backgroundColor('#2a2a2a').fontColor('#fff').placeholderColor('#555')
            .borderRadius(8).padding(12)
        } else {
          Text(this.editingReport!.summary).fontSize(13).fontColor('#aaa').width('100%')
        }
      }
      if (this.editingReport!.nextPlan) {
        Text('下周计划').fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').margin({ top: 12, bottom: 6 }).alignSelf(ItemAlign.Start)
        if (this.isEditing) {
          TextArea({ text: $$this.nextPlan, placeholder: '填写下周工作计划...' })
            .height(80).backgroundColor('#2a2a2a').fontColor('#fff').placeholderColor('#555')
            .borderRadius(8).padding(12)
        } else {
          Text(this.editingReport!.nextPlan).fontSize(13).fontColor('#aaa').width('100%')
        }
      }
      if (this.editingReport!.needSupport) {
        Text('需要支持').fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').margin({ top: 12, bottom: 6 }).alignSelf(ItemAlign.Start)
        if (this.isEditing) {
          TextArea({ text: $$this.needSupport, placeholder: '填写需要协调的事项...' })
            .height(60).backgroundColor('#2a2a2a').fontColor('#fff').placeholderColor('#555')
            .borderRadius(8).padding(12)
        } else {
          Text(this.editingReport!.needSupport).fontSize(13).fontColor('#aaa').width('100%')
        }
      }
    }
    .width('100%').padding(16)
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  AuditInfoBuilder() {
    Column() {
      Text('审计信息').fontSize(11).fontColor('#555').margin({ bottom: 4 }).alignSelf(ItemAlign.Start)
      Row() {
        Text(`创建: ${this.editingReport!.createdAt.toLocaleString()}`).fontSize(10).fontColor('#444').layoutWeight(1)
        Text(`更新: ${this.editingReport!.updatedAt.toLocaleString()}`).fontSize(10).fontColor('#444')
      }
      Text(`DNA: ${this.editingReport!.dnaSignature}`).fontSize(9).fontColor('#333').margin({ top: 2 })
    }
    .width('100%').padding(16)
  }

  @Builder
  EditFooterBuilder() {
    Column() {
      if (this.showDeleteConfirm) {
        Row() {
          Text('确认删除此周报?').fontSize(14).fontColor('#ff4444').layoutWeight(1)
          Button('取消').fontSize(12).fontColor('#888').backgroundColor('#333').borderRadius(6).padding({ left: 12, right: 12 }).margin({ right: 8 })
          .onClick(() => { this.showDeleteConfirm = false; })
          Button('确认删除').fontSize(12).fontColor('#fff').backgroundColor('#ff4444').borderRadius(6).padding({ left: 12, right: 12 })
          .onClick(() => { this.handleDelete(); })
        }
        .width('100%').padding({ left: 16, right: 16, top: 8, bottom: 8 })
        .backgroundColor('rgba(255,68,68,0.1)')
      }
      Row() {
        Button('删除').fontSize(13).fontColor('#ff4444').backgroundColor('rgba(255,68,68,0.1)')
        .borderRadius(8).layoutWeight(1).height(44).margin({ right: 8 })
        .onClick(() => { this.showDeleteConfirm = true; })
        Button('保存').fontSize(14).fontColor('#0a0a0a').backgroundColor('#c41e3a')
        .borderRadius(8).layoutWeight(2).height(44)
        .onClick(() => { this.handleSave(); })
      }
      .width('100%').padding(16)
      .border({ width: { top: 1 }, color: '#333' })
    }
  }

  @Builder
  DraftFooterBuilder() {
    Row() {
      Button('提交审批').fontSize(14).fontColor('#0a0a0a').backgroundColor('#c41e3a')
      .borderRadius(8).layoutWeight(1).height(48)
      .onClick(() => { this.handleSubmit(); })
    }
    .width('100%').padding(16)
    .border({ width: { top: 1 }, color: '#333' })
  }

  @Builder
  ViewFooterBuilder() {
    Row() {
      Button('关闭').fontSize(14).fontColor('#888').backgroundColor('#333')
      .borderRadius(8).layoutWeight(1).height(44)
      .onClick(() => { this.controller.close(); })
    }
    .width('100%').padding(16)
    .border({ width: { top: 1 }, color: '#333' })
  }

  handleSave(): void {
    if (this.editingReport) {
      this.editingReport.summary = this.summary;
      this.editingReport.nextPlan = this.nextPlan;
      this.editingReport.needSupport = this.needSupport;
      this.editingReport.recalculate();
      this.onSave?.(this.editingReport);
    }
    this.isEditing = false;
  }

  handleSubmit(): void {
    if (this.editingReport) {
      this.onSave?.(this.editingReport);
    }
    this.controller.close();
  }

  handleDelete(): void {
    if (this.editingReport) {
      this.onDelete?.(this.editingReport.id);
    }
    this.controller.close();
  }

  getStatusColor(status: WeeklyStatus): string {
    switch (status) {
      case WeeklyStatus.DRAFT: return '#ffcc00';
      case WeeklyStatus.SUBMITTED: return '#0066cc';
      case WeeklyStatus.FIRST_REVIEW: return '#ff6600';
      case WeeklyStatus.FINAL_REVIEW: return '#c41e3a';
      case WeeklyStatus.APPROVED: return '#00ff00';
      case WeeklyStatus.REJECTED: return '#ff0000';
      case WeeklyStatus.ARCHIVED: return '#888';
      default: return '#999';
    }
  }

  getStatusBg(status: WeeklyStatus): string {
    switch (status) {
      case WeeklyStatus.DRAFT: return 'rgba(255,204,0,0.1)';
      case WeeklyStatus.SUBMITTED: return 'rgba(0,102,204,0.1)';
      case WeeklyStatus.FIRST_REVIEW: return 'rgba(255,102,0,0.1)';
      case WeeklyStatus.FINAL_REVIEW: return 'rgba(196,30,58,0.1)';
      case WeeklyStatus.APPROVED: return 'rgba(0,255,0,0.1)';
      case WeeklyStatus.REJECTED: return 'rgba(255,0,0,0.1)';
      case WeeklyStatus.ARCHIVED: return 'rgba(136,136,136,0.1)';
      default: return 'rgba(153,153,153,0.1)';
    }
  }

  getTaskStatusEmoji(status: string): string {
    switch (status) {
      case '已完成': return '✅';
      case '进行中': return '🔄';
      case '被阻塞': return '🚫';
      case '已延期': return '⚠️';
      default: return '⬜';
    }
  }

  getProgressColor(progress: number): string {
    if (progress >= 100) return '#00ff00';
    if (progress > 0) return '#0066cc';
    return '#999';
  }

  getSeverityEmoji(severity: string): string {
    switch (severity) {
      case 'critical': return '🔴';
      case 'high': return '🟠';
      case 'medium': return '🟡';
      case 'low': return '🟢';
      default: return '🟡';
    }
  }
}
