// entry/src/main/ets/components/ApprovalDialog.ets
// 龍魂 · 审批操作弹窗 · ArkTS

import { WeeklyReport, WeeklyStatus, ApprovalRecord } from '../models/WeeklyModel';

@CustomDialog
export struct ApprovalDialog {
  controller: CustomDialogController;
  report?: WeeklyReport;
  onApprove?: (level: number, approver: string, approverId: string, comment: string, signature: string) => void;
  onReject?: (approver: string, approverId: string, comment: string) => void;
  onClose?: () => void;

  @State private comment: string = '';
  @State private approver: string = '';
  @State private approverId: string = '';
  @State private showReject: boolean = false;

  aboutToAppear() {
    this.approver = '当前审批人';
    this.approverId = '9622';
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('审批周报').fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff').layoutWeight(1)
        Text('✕').fontSize(20).fontColor('#888')
          .onClick(() => { this.onClose?.(); this.controller.close(); })
      }
      .width('100%').padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      Scroll() {
        Column() {
          // 周报摘要
          if (this.report) {
            this.ReportSummaryBuilder()
          }

          // 审批级别
          this.ApprovalLevelBuilder()

          // 任务列表
          if (this.report) {
            this.TaskSummaryBuilder()
          }

          // 审批意见
          Column() {
            Text('审批意见').fontSize(13).fontColor('#888').margin({ bottom: 6 }).alignSelf(ItemAlign.Start)
            TextArea({ text: $$this.comment, placeholder: this.showReject ? '请输入驳回原因...' : '请输入审批意见(选填)...' })
              .height(80).backgroundColor('#2a2a2a').fontColor('#fff').placeholderColor('#555')
              .borderRadius(8).padding(12)
          }
          .width('100%').padding({ left: 16, right: 16, top: 12 })
        }
      }
      .width('100%').layoutWeight(1)
      .scrollBar(BarState.Auto)

      // 审批历史
      if (this.report && this.report.approvals.length > 0) {
        this.ApprovalHistoryBuilder()
      }

      // 底部按钮
      Row() {
        if (!this.showReject) {
          Button('驳回')
            .fontSize(14).fontColor('#ff4444').backgroundColor('rgba(255,68,68,0.15)')
            .borderRadius(8).layoutWeight(1).height(44).margin({ right: 8 })
            .onClick(() => { this.showReject = true; })
        } else {
          Button('取消驳回')
            .fontSize(14).fontColor('#888').backgroundColor('#333')
            .borderRadius(8).layoutWeight(1).height(44).margin({ right: 8 })
            .onClick(() => { this.showReject = false; this.comment = ''; })
        }
        if (this.showReject) {
          Button('确认驳回')
            .fontSize(14).fontColor('#fff').backgroundColor('#ff4444')
            .borderRadius(8).layoutWeight(2).height(44)
            .onClick(() => { this.handleReject(); })
        } else {
          Button('审批通过')
            .fontSize(14).fontColor('#0a0a0a').backgroundColor('#00cc66')
            .borderRadius(8).layoutWeight(2).height(44)
            .onClick(() => { this.handleApprove(); })
        }
      }
      .width('100%').padding(16)
      .border({ width: { top: 1 }, color: '#333' })
    }
    .width('100%').height('85%').backgroundColor('#1a1a1a').borderRadius({ topLeft: 16, topRight: 16 })
  }

  @Builder
  ReportSummaryBuilder() {
    Column() {
      Row() {
        Text(this.report!.reportNo).fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 8 })
        Blank()
        Text(this.report!.status).fontSize(12).fontColor(this.getStatusBadgeColor())
          .backgroundColor(this.getStatusBadgeBg()).borderRadius(4)
          .padding({ left: 8, right: 8, top: 2, bottom: 2 })
      }
      .width('100%')
      Row() {
        Column() { Text('填报人').fontSize(11).fontColor('#666').margin({ bottom: 2 }); Text(this.report!.reporter).fontSize(13).fontColor('#fff') }
        .layoutWeight(1).alignItems(HorizontalAlign.Start)
        Column() { Text('部门').fontSize(11).fontColor('#666').margin({ bottom: 2 }); Text(this.report!.department).fontSize(13).fontColor('#fff') }
        .layoutWeight(1).alignItems(HorizontalAlign.Start)
        Column() { Text('周次').fontSize(11).fontColor('#666').margin({ bottom: 2 }); Text(`${this.report!.weekStart.toLocaleDateString()}`).fontSize(13).fontColor('#fff') }
        .layoutWeight(1).alignItems(HorizontalAlign.Start)
      }
      .width('100%').margin({ top: 4 })
      Row() {
        Text(`⏱️ ${this.report!.totalActualHours}h/${this.report!.totalPlannedHours}h`).fontSize(12).fontColor('#888')
        Text(`📋 ${this.report!.tasks.length}项任务`).fontSize(12).fontColor('#888').margin({ left: 12 })
        Text(`✅ ${this.report!.completionRate}%完成`).fontSize(12).fontColor(
          this.report!.completionRate >= 80 ? '#00ff00' : '#ffcc00'
        ).margin({ left: 12 })
      }
      .width('100%').margin({ top: 4 })
    }
    .width('100%').padding(16)
    .backgroundColor('rgba(196,30,58,0.05)')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  ApprovalLevelBuilder() {
    Row() {
      Text('审批级别:').fontSize(13).fontColor('#888')
      Text(this.report?.status === WeeklyStatus.SUBMITTED ? '初审' : '终审').fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a').margin({ left: 6 })
      Blank()
      Text(`审批人: ${this.approver}`).fontSize(12).fontColor('#8af').margin({ right: 4 })
    }
    .width('100%').padding({ left: 16, right: 16, top: 12, bottom: 8 })
  }

  @Builder
  TaskSummaryBuilder() {
    Column() {
      Text(`本周任务 (${this.report!.tasks.length}项)`).fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').margin({ bottom: 8 }).alignSelf(ItemAlign.Start)
      ForEach(this.report!.tasks.slice(0, 5), (task: Record<string, Object>) => {
        Row() {
          Text((task.title as string) || '未命名').fontSize(13).fontColor('#ccc').layoutWeight(1).maxLines(1).textOverflow({ overflow: TextOverflow.Ellipsis })
          Text(this.getTaskStatusText(task.status as string)).fontSize(11).fontColor(this.getTaskStatusColor(task.status as string))
        }
        .width('100%').height(32).padding({ left: 8, right: 8 })
        .backgroundColor('rgba(255,255,255,0.03)').borderRadius(4).margin({ bottom: 4 })
      })
      if (this.report!.tasks.length > 5) {
        Text(`...及其他 ${this.report!.tasks.length - 5} 项任务`).fontSize(12).fontColor('#666').margin({ top: 4 })
      }
    }
    .width('100%').padding({ left: 16, right: 16, top: 8 })
  }

  @Builder
  ApprovalHistoryBuilder() {
    Column() {
      Text('审批历史').fontSize(13).fontColor('#888').margin({ bottom: 6 }).alignSelf(ItemAlign.Start)
      ForEach(this.report!.approvals, (record: Record<string, Object>) => {
        Row() {
          Text(record.signature === 'REJECTED' ? '❌' : '✅').fontSize(14).margin({ right: 8 })
          Text(`L${record.level} · ${record.approver}`).fontSize(12).fontColor('#888').layoutWeight(1)
          if (record.comment) {
            Text((record.comment as string).substring(0, 20)).fontSize(11).fontColor('#666').maxLines(1)
          }
        }
        .width('100%').height(28)
      })
    }
    .width('100%').padding({ left: 16, right: 16, top: 8, bottom: 4 })
  }

  handleApprove(): void {
    const level = this.report?.status === WeeklyStatus.SUBMITTED ? 1 : 2;
    const signature = `SM2-SIGNED-${Date.now().toString(36)}`;
    this.onApprove?.(level, this.approver, this.approverId, this.comment, signature);
  }

  handleReject(): void {
    this.onReject?.(this.approver, this.approverId, this.comment || '驳回');
  }

  getStatusBadgeColor(): string {
    if (!this.report) return '#999';
    switch (this.report.status) {
      case WeeklyStatus.SUBMITTED: return '#0066cc';
      case WeeklyStatus.FIRST_REVIEW: return '#c41e3a';
      case WeeklyStatus.APPROVED: return '#00cc66';
      default: return '#999';
    }
  }

  getStatusBadgeBg(): string {
    if (!this.report) return 'rgba(153,153,153,0.1)';
    switch (this.report.status) {
      case WeeklyStatus.SUBMITTED: return 'rgba(0,102,204,0.1)';
      case WeeklyStatus.FIRST_REVIEW: return 'rgba(196,30,58,0.1)';
      case WeeklyStatus.APPROVED: return 'rgba(0,204,102,0.1)';
      default: return 'rgba(153,153,153,0.1)';
    }
  }

  getTaskStatusText(status: string): string {
    switch (status) {
      case '已完成': return '✅';
      case '进行中': return '🔄';
      case '未开始': return '⬜';
      case '被阻塞': return '🚫';
      case '已延期': return '⚠️';
      default: return '⬜';
    }
  }

  getTaskStatusColor(status: string): string {
    switch (status) {
      case '已完成': return '#00ff00';
      case '进行中': return '#0066cc';
      case '被阻塞': return '#ff0000';
      case '已延期': return '#ffcc00';
      default: return '#999';
    }
  }
}
