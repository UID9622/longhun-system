// entry/src/main/ets/pages/WeeklyReviewPage.ets
// 龍魂 · 周报管理主页面 · ArkTS

import { WeeklyReport, WeeklyStatus, WeeklyTask, TaskStatus, TaskType, Priority, WeeklyState, weeklyState, WeeklyStats, WeeklyIssue, WeeklyRisk, NextTask, WeeklyTemplate } from '../models/WeeklyModel';
import { TaskEditDialog } from '../components/TaskEditDialog';
import { ApprovalDialog } from '../components/ApprovalDialog';
import { HourChartView } from '../components/HourChartView';
import { TrendChartView } from '../components/TrendChartView';
import { WeeklyDetailDialog } from '../components/WeeklyDetailDialog';
import { TemplateDialog } from '../components/TemplateDialog';
import { WeeklyDatabase } from '../database/WeeklyDatabase';

const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

@Entry
@Component
struct WeeklyReviewPage {
  @StorageLink('weeklyState') weeklyState: WeeklyState = weeklyState;
  @State private selectedTab: number = 0;
  @State private showTaskDialog: boolean = false;
  @State private showApprovalDialog: boolean = false;
  @State private showDetailDialog: boolean = false;
  @State private showTemplateDialog: boolean = false;
  @State private editingReport: WeeklyReport | null = null;
  @State private editingTask: WeeklyTask | null = null;
  @State private showSearch: boolean = false;
  @State private searchText: string = '';
  @State private viewMode: 'list' | 'stats' | 'trend' = 'list';
  @State private filterWeekOffset: number = 0;

  aboutToAppear() {
    this.weeklyState.load();
    WeeklyDatabase.init();
    this.scheduleReminders();
  }

  build() {
    Column() {
      this.HeaderBuilder()
      this.StatsBuilder()
      this.ViewControlBuilder()
      this.TabBuilder()
      if (this.showSearch) { this.SearchBuilder() }
      this.ContentBuilder()
      this.FooterBuilder()

      // 弹窗
      if (this.showDetailDialog && this.editingReport) {
        WeeklyDetailDialog({
          report: this.editingReport,
          onSave: (report: WeeklyReport) => {
            this.weeklyState.updateReport(report.id, report);
            this.showDetailDialog = false;
          },
          onDelete: (id: string) => {
            this.weeklyState.removeReport(id);
            this.showDetailDialog = false;
          },
          onClose: () => { this.showDetailDialog = false; }
        })
      }

      if (this.showApprovalDialog && this.editingReport) {
        ApprovalDialog({
          report: this.editingReport,
          onApprove: (level: number, approver: string, approverId: string, comment: string, signature: string) => {
            this.weeklyState.approveReport(this.editingReport!.id, level, approver, approverId, comment, signature);
            this.showApprovalDialog = false;
          },
          onReject: (approver: string, approverId: string, comment: string) => {
            this.weeklyState.rejectReport(this.editingReport!.id, approver, approverId, comment);
            this.showApprovalDialog = false;
          },
          onClose: () => { this.showApprovalDialog = false; }
        })
      }

      if (this.showTemplateDialog) {
        TemplateDialog({
          templates: this.weeklyState.templates,
          onSave: (template: WeeklyTemplate) => {
            this.weeklyState.addTemplate(template);
            this.showTemplateDialog = false;
          },
          onDelete: (id: string) => {
            this.weeklyState.removeTemplate(id);
          },
          onClose: () => { this.showTemplateDialog = false; }
        })
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  // === 标题栏 ===
  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉').fontSize(28).margin({ right: 8 })
      Column() {
        Text('龍魂周报管理').fontSize(20).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text(`UID:${MASTER_UID} · ${this.weeklyState.statistics.myTotal}份周报`).fontSize(12).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      Blank()
      if (this.weeklyState.statistics.pendingReview > 0) {
        Badge({
          value: this.weeklyState.statistics.pendingReview.toString(),
          position: BadgePosition.RightTop,
          style: { badgeSize: 18, badgeColor: '#c41e3a' }
        }) {
          Button() { Text('🔔').fontSize(20) }
          .type(ButtonType.Circle)
          .backgroundColor('rgba(196,30,58,0.2)')
          .width(40).height(40)
          .onClick(() => { this.selectedTab = 3; })
        }
      }
      Button() { Text(this.showSearch ? '✕' : '🔍').fontSize(20) }
      .type(ButtonType.Circle).backgroundColor('#1a1a1a').width(40).height(40)
      .onClick(() => {
        this.showSearch = !this.showSearch;
        if (!this.showSearch) { this.weeklyState.searchQuery = ''; }
      })
      Button() { Text('+').fontSize(24).fontColor('#fff') }
      .type(ButtonType.Circle).backgroundColor('#c41e3a').width(40).height(40)
      .onClick(() => { this.createNewWeekly(); })
    }
    .width('100%').height(56).padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // === 统计卡片 ===
  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('我的周报', this.weeklyState.statistics.myTotal.toString(), '#fff')
      this.StatCard('草稿', this.weeklyState.statistics.myDraft.toString(), '#ffcc00')
      this.StatCard('已提交', this.weeklyState.statistics.mySubmitted.toString(), '#0066cc')
      this.StatCard('已通过', this.weeklyState.statistics.myApproved.toString(), '#00ff00')
      this.StatCard('本周工时', `${this.weeklyState.statistics.thisWeekHours}h`, '#c41e3a')
    }
    .width('100%').height(80).padding({ left: 12, right: 12, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() {
      Text(value).fontSize(24).fontWeight(FontWeight.Bold).fontColor(color)
      Text(label).fontSize(11).fontColor('#666').margin({ top: 4 })
    }
    .width('20%').height('100%').justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Center)
  }

  // === 视图控制栏 ===
  @Builder
  ViewControlBuilder() {
    Row() {
      Row() {
        Button() { Text('◀').fontSize(14).fontColor('#999') }
        .type(ButtonType.Circle).backgroundColor('#1a1a1a').width(32).height(32)
        .onClick(() => { this.prevWeek(); })
        Text(this.getCurrentWeekLabel()).fontSize(14).fontColor('#fff').margin({ left: 12, right: 12 })
        Button() { Text('▶').fontSize(14).fontColor('#999') }
        .type(ButtonType.Circle).backgroundColor('#1a1a1a').width(32).height(32)
        .onClick(() => { this.nextWeek(); })
      }
      .layoutWeight(1)
      Blank()
      Row() {
        ForEach(['list', 'stats', 'trend'], (mode: string) => {
          Button() {
            Text(mode === 'list' ? '列表' : mode === 'stats' ? '统计' : '趋势')
            .fontSize(12).fontColor(this.viewMode === mode ? '#0a0a0a' : '#999')
          }
          .type(ButtonType.Normal)
          .backgroundColor(this.viewMode === mode ? '#c41e3a' : '#1a1a1a')
          .borderRadius(8).padding({ left: 12, right: 12, top: 4, bottom: 4 })
          .margin({ left: 4 })
          .onClick(() => { this.viewMode = mode as 'list' | 'stats' | 'trend'; })
        })
      }
    }
    .width('100%').height(48).padding({ left: 12, right: 12 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // === 标签切换 ===
  @Builder
  TabBuilder() {
    Row() {
      ForEach([
        { label: '我的周报', icon: '📝', count: this.weeklyState.statistics.myDraft },
        { label: '团队周报', icon: '👥', count: 0 },
        { label: '工时统计', icon: '⏱️', count: 0 },
        { label: '待审批', icon: '✅', count: this.weeklyState.statistics.pendingReview }
      ], (item: Record<string, Object>, index: number) => {
        Column() {
          Text(`${item.icon} ${item.label}${(item.count as number) > 0 ? `(${item.count})` : ''}`)
            .fontSize(13)
            .fontWeight(this.selectedTab === index ? FontWeight.Bold : FontWeight.Normal)
            .fontColor(this.selectedTab === index ? '#c41e3a' : '#888')
          if (this.selectedTab === index) {
            Divider().strokeWidth(2).color('#c41e3a').width(20).margin({ top: 4 })
          }
        }
        .padding({ top: 12, bottom: 12, left: 16, right: 16 })
        .onClick(() => { this.selectedTab = index; })
      })
    }
    .width('100%').justifyContent(FlexAlign.SpaceAround)
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // === 搜索栏 ===
  @Builder
  SearchBuilder() {
    Row() {
      TextInput({ placeholder: '搜索填报人/部门/周报编号...', text: $$this.searchText })
        .width('100%').height(40).backgroundColor('#2a2a2a')
        .fontColor('#fff').placeholderColor('#666')
        .borderRadius(8).padding({ left: 12, right: 12 })
        .onChange((value: string) => { this.weeklyState.searchQuery = value; })
    }
    .width('100%').padding({ left: 16, right: 16, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
  }

  // === 内容区 ===
  @Builder
  ContentBuilder() {
    if (this.viewMode === 'list') {
      if (this.selectedTab === 0) { this.MyWeeklyListBuilder() }
      else if (this.selectedTab === 1) { this.TeamWeeklyListBuilder() }
      else if (this.selectedTab === 2) { this.HourStatsBuilder() }
      else { this.ApprovalListBuilder() }
    } else if (this.viewMode === 'stats') {
      HourChartView({ stats: this.weeklyState.statistics, trend: this.weeklyState.hourTrend })
    } else {
      TrendChartView({ trend: this.weeklyState.hourTrend })
    }
  }

  // === 我的周报列表 ===
  @Builder
  MyWeeklyListBuilder() {
    List() {
      if (this.weeklyState.currentWeekDraft) {
        ListItem() { this.DraftCardBuilder(this.weeklyState.currentWeekDraft) }
      }
      ForEach(this.weeklyState.myReports, (report: WeeklyReport) => {
        ListItem() { this.WeeklyCardBuilder(report) }
        .onClick(() => { this.editingReport = report; this.showDetailDialog = true; })
      }, (report: WeeklyReport) => report.id)
    }
    .width('100%').layoutWeight(1).divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto).padding({ bottom: 16 })
  }

  @Builder
  DraftCardBuilder(report: WeeklyReport) {
    Column() {
      Row() {
        Text('📝').fontSize(24).margin({ right: 12 })
        Column() {
          Text('本周周报草稿').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#ffcc00')
          Text(`${report.weekStart.toLocaleDateString()} - ${report.weekEnd.toLocaleDateString()}`).fontSize(12).fontColor('#888')
        }
        .alignItems(HorizontalAlign.Start).layoutWeight(1)
        Button('继续编辑')
          .fontSize(12).fontColor('#0a0a0a').backgroundColor('#ffcc00')
          .borderRadius(8).padding({ left: 12, right: 12 })
          .onClick(() => { this.editingReport = report; this.showDetailDialog = true; })
      }
      .width('100%').padding(16)
    }
    .width('100%').backgroundColor('rgba(255,204,0,0.05)')
    .border({ width: 1, color: 'rgba(255,204,0,0.3)' }).borderRadius(8)
    .margin({ left: 12, right: 12, top: 8 })
  }

  // === 周报卡片 ===
  @Builder
  WeeklyCardBuilder(report: WeeklyReport) {
    Row() {
      Column() {
        Text(
          report.status === WeeklyStatus.DRAFT ? '📝' :
          report.status === WeeklyStatus.SUBMITTED ? '⏳' :
          report.status === WeeklyStatus.FIRST_REVIEW ? '👀' :
          report.status === WeeklyStatus.FINAL_REVIEW ? '🔍' :
          report.status === WeeklyStatus.APPROVED ? '✅' :
          report.status === WeeklyStatus.REJECTED ? '❌' : '📦'
        ).fontSize(24)
      }
      .width(40).height(40).margin({ right: 12 }).justifyContent(FlexAlign.Center)
      Column() {
        Row() {
          Text(report.reportNo).fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').layoutWeight(1)
          Text(report.status)
            .fontSize(11).fontColor(this.getStatusColor(report.status))
            .backgroundColor(this.getStatusBgColor(report.status))
            .borderRadius(4).padding({ left: 8, right: 8, top: 2, bottom: 2 })
        }
        .width('100%')
        Row() {
          Text(`${report.weekStart.toLocaleDateString()} - ${report.weekEnd.toLocaleDateString()}`).fontSize(12).fontColor('#888').layoutWeight(1)
          Text(`${report.completionRate}%完成`).fontSize(12).fontColor(
            report.completionRate >= 80 ? '#00ff00' : report.completionRate >= 50 ? '#ffcc00' : '#ff6600'
          )
        }
        .width('100%').margin({ top: 4 })
        Row() {
          Text(`⏱️${report.totalActualHours}h/${report.totalPlannedHours}h`).fontSize(11).fontColor('#666')
          Text(`📋${report.tasks.length}项任务`).fontSize(11).fontColor('#666').margin({ left: 8 })
          if (report.totalOvertimeHours > 0) {
            Text(`🔥${report.totalOvertimeHours}h加班`).fontSize(11).fontColor('#ff6600').margin({ left: 8 })
          }
          Blank()
          if (report.status === WeeklyStatus.SUBMITTED || report.status === WeeklyStatus.FIRST_REVIEW) {
            const progress = report.getApprovalProgress();
            Stack() {
              Row().width(50).height(4).backgroundColor('#333').borderRadius(2)
              Row().width(`${progress.percentage}%`).height(4).backgroundColor('#c41e3a').borderRadius(2)
            }
            .width(50).height(4)
            Text(`${progress.current}/${progress.total}`).fontSize(10).fontColor('#c41e3a').margin({ left: 4 })
          }
        }
        .width('100%').margin({ top: 6 })
      }
      .layoutWeight(1).alignItems(HorizontalAlign.Start)
    }
    .width('100%').padding(16)
    .backgroundColor(
      report.status === WeeklyStatus.REJECTED ? 'rgba(255,0,0,0.05)' :
      report.status === WeeklyStatus.APPROVED ? 'rgba(0,255,0,0.05)' : '#0a0a0a'
    )
    .borderRadius(8).margin({ left: 12, right: 12, top: 8 })
  }

  // === 团队周报列表 ===
  @Builder
  TeamWeeklyListBuilder() {
    List() {
      ForEach(this.weeklyState.filteredReports, (report: WeeklyReport) => {
        ListItem() { this.WeeklyCardBuilder(report) }
        .onClick(() => { this.editingReport = report; this.showDetailDialog = true; })
      }, (report: WeeklyReport) => report.id)
    }
    .width('100%').layoutWeight(1).divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto).padding({ bottom: 16 })
  }

  // === 工时统计 ===
  @Builder
  HourStatsBuilder() {
    HourChartView({ stats: this.weeklyState.statistics, trend: this.weeklyState.hourTrend })
  }

  // === 审批列表 ===
  @Builder
  ApprovalListBuilder() {
    List() {
      if (this.weeklyState.pendingFirstReview.length > 0) {
        ListItem() {
          Text(`⏳ 初审待办 (${this.weeklyState.pendingFirstReview.length})`)
            .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#ffcc00')
            .padding({ left: 16, top: 12, bottom: 8 })
        }
        .width('100%').backgroundColor('#1a1a1a')
      }
      ForEach(this.weeklyState.pendingFirstReview, (report: WeeklyReport) => {
        ListItem() { this.ApprovalCardBuilder(report, 1) }
        .onClick(() => { this.editingReport = report; this.showApprovalDialog = true; })
      }, (report: WeeklyReport) => `first-${report.id}`)

      if (this.weeklyState.pendingFinalReview.length > 0) {
        ListItem() {
          Text(`🔍 终审待办 (${this.weeklyState.pendingFinalReview.length})`)
            .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
            .padding({ left: 16, top: 12, bottom: 8 })
        }
        .width('100%').backgroundColor('#1a1a1a')
      }
      ForEach(this.weeklyState.pendingFinalReview, (report: WeeklyReport) => {
        ListItem() { this.ApprovalCardBuilder(report, 2) }
        .onClick(() => { this.editingReport = report; this.showApprovalDialog = true; })
      }, (report: WeeklyReport) => `final-${report.id}`)
    }
    .width('100%').layoutWeight(1).divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto).padding({ bottom: 16 })
  }

  @Builder
  ApprovalCardBuilder(report: WeeklyReport, level: number) {
    Row() {
      Column() { Text('⏳').fontSize(24) }
      .width(40).height(40).margin({ right: 12 }).justifyContent(FlexAlign.Center)
      Column() {
        Row() {
          Text(`${report.reporter} 的周报`).fontSize(15).fontWeight(FontWeight.Medium).fontColor('#fff').layoutWeight(1)
          Text(`L${level}审批`).fontSize(11).fontColor('#c41e3a').backgroundColor('rgba(196,30,58,0.1)').borderRadius(4).padding({ left: 6, right: 6 })
        }
        .width('100%')
        Row() {
          Text(`${report.department} · ${report.reportNo}`).fontSize(12).fontColor('#888').layoutWeight(1)
          Text(`${report.tasks.length}项 · ${report.totalActualHours}h`).fontSize(12).fontColor('#888')
        }
        .width('100%').margin({ top: 4 })
        Row() {
          Text(`📅 ${report.submittedAt?.toLocaleString() || ''}`).fontSize(11).fontColor('#666')
          Blank()
          Button('去审批').fontSize(11).fontColor('#fff').backgroundColor('#c41e3a')
          .borderRadius(6).padding({ left: 12, right: 12, top: 4, bottom: 4 })
          .onClick(() => { this.editingReport = report; this.showApprovalDialog = true; })
        }
        .width('100%').margin({ top: 6 })
      }
      .layoutWeight(1).alignItems(HorizontalAlign.Start)
    }
    .width('100%').padding(16).backgroundColor('#0a0a0a').borderRadius(8).margin({ left: 12, right: 12, top: 8 })
  }

  // === 底部操作栏 ===
  @Builder
  FooterBuilder() {
    Row() {
      Column() {
        Text('🐉').fontSize(20)
        Text(`UID:${MASTER_UID}`).fontSize(10).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start).layoutWeight(1)
      Row() {
        Button() { Text('📋 模板').fontSize(12).fontColor('#fff') }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(8)
        .padding({ left: 12, right: 12, top: 6, bottom: 6 }).margin({ right: 8 })
        .onClick(() => { this.showTemplateDialog = true; })
        Button() { Text('📤 导出').fontSize(12).fontColor('#fff') }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(8)
        .padding({ left: 12, right: 12, top: 6, bottom: 6 }).margin({ right: 8 })
        .onClick(() => { this.exportWeekly(); })
        Button() { Text('➕ 周报').fontSize(12).fontColor('#fff') }
        .type(ButtonType.Normal).backgroundColor('#c41e3a').borderRadius(8)
        .padding({ left: 12, right: 12, top: 6, bottom: 6 })
        .onClick(() => { this.createNewWeekly(); })
      }
    }
    .width('100%').height(56).padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }

  // === 辅助方法 ===
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

  getStatusBgColor(status: WeeklyStatus): string {
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

  getCurrentWeekLabel(): string {
    const now = new Date();
    const d = new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    const weekNum = Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
    return `${now.getFullYear()}年第${weekNum}周`;
  }

  prevWeek(): void { this.filterWeekOffset--; }
  nextWeek(): void { this.filterWeekOffset++; }

  createNewWeekly(): void {
    const newReport = new WeeklyReport({
      reporter: this.weeklyState.currentUser,
      reporterId: this.weeklyState.currentUserId,
      department: this.weeklyState.currentDept
    });
    this.weeklyState.addReport(newReport);
    this.editingReport = newReport;
    this.showDetailDialog = true;
  }

  exportWeekly(): void {
    const data = {
      exportTime: new Date().toISOString(),
      dna: MASTER_DNA,
      uid: MASTER_UID,
      confirm: CONFIRM_SEAL,
      reports: this.weeklyState.myReports.map(r => ({
        reportNo: r.reportNo,
        week: `${r.weekStart.toLocaleDateString()}-${r.weekEnd.toLocaleDateString()}`,
        status: r.status,
        completionRate: r.completionRate,
        plannedHours: r.totalPlannedHours,
        actualHours: r.totalActualHours,
        overtimeHours: r.totalOvertimeHours,
        taskCount: r.tasks.length
      }))
    };
    console.info(`[龍魂] 周报导出: longhun_weekly_${Date.now()}.json`);
    console.info(`[龍魂] 导出内容: ${JSON.stringify(data, null, 2)}`);
  }

  scheduleReminders(): void {
    console.info('[龍魂] 周报提醒系统已启动');
  }
}
