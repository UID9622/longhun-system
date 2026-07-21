// 龍魂 · 项目里程碑时间线主页面 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️
// UID: 9622

import { Project, ProjectStatus, Milestone, MilestoneStatus, Priority, RiskLevel, ProjectState, projectState, ProjectStats, ProjectAlert } from '../models/MilestoneModel';
import { ProjectDetailDialog } from '../components/ProjectDetailDialog';
import { MilestoneDialog } from '../components/MilestoneDialog';
import { GanttChartView } from '../components/GanttChartView';
import { TimelineView } from '../components/TimelineView';
import { KanbanView } from '../components/KanbanView';
import { RiskPanel } from '../components/RiskPanel';
import { BaselineDialog } from '../components/BaselineDialog';
import { ProjectDatabase } from '../database/ProjectDatabase';

const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

@Entry
@Component
struct MilestoneTimelinePage {
  @StorageLink('projectState') projectState: ProjectState = projectState;
  @State private selectedTab: number = 0;
  @State private showProjectDialog: boolean = false;
  @State private showMilestoneDialog: boolean = false;
  @State private showBaselineDialog: boolean = false;
  @State private showRiskPanel: boolean = false;
  @State private editingProject: Project | null = null;
  @State private editingMilestone: Milestone | null = null;
  @State private editingProjectId: string = '';
  @State private showSearch: boolean = false;
  @State private searchText: string = '';
  @State private showAlerts: boolean = false;
  @State private showFilter: boolean = false;
  @State private filterTab: ProjectStatus | '全部' = '全部';

  aboutToAppear() {
    this.projectState.load();
    ProjectDatabase.init();
  }

  build() {
    Column() {
      // 标题栏
      this.HeaderBuilder()

      // 预警横幅
      if (this.projectState.alerts.length > 0 && !this.showAlerts) {
        this.AlertBannerBuilder()
      }

      // 统计卡片
      this.StatsBuilder()

      // 视图控制栏
      this.ViewControlBuilder()

      // 标签过滤
      this.TabFilterBuilder()

      // 搜索栏
      if (this.showSearch) {
        this.SearchBuilder()
      }

      // 内容区
      this.ContentBuilder()

      // 底部操作栏
      this.FooterBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')

    // 弹窗
    if (this.showProjectDialog) {
      ProjectDetailDialog({
        project: this.editingProject,
        onSave: (project: Project) => {
          if (this.editingProject) {
            this.projectState.updateProject(project.id, project);
          } else {
            this.projectState.addProject(project);
          }
          this.showProjectDialog = false;
          this.editingProject = null;
        },
        onDelete: (id: string) => {
          AlertDialog.show({
            title: '确认删除',
            message: '删除项目及其所有里程碑？此操作不可恢复',
            primaryButton: { value: '删除', action: () => { this.projectState.removeProject(id); } },
            secondaryButton: { value: '取消', action: () => {} }
          });
          this.showProjectDialog = false;
          this.editingProject = null;
        },
        onCancel: () => { this.showProjectDialog = false; this.editingProject = null; }
      })
    }

    if (this.showMilestoneDialog) {
      MilestoneDialog({
        milestone: this.editingMilestone,
        projectId: this.editingProjectId,
        onSave: (milestone: Milestone) => {
          this.projectState.addMilestone(this.editingProjectId, milestone);
          this.showMilestoneDialog = false;
          this.editingMilestone = null;
        },
        onCancel: () => { this.showMilestoneDialog = false; this.editingMilestone = null; }
      })
    }

    if (this.showBaselineDialog) {
      BaselineDialog({
        project: this.projectState.currentProject,
        onSave: (name: string, desc: string) => {
          if (this.projectState.currentProjectId) {
            this.projectState.createBaseline(this.projectState.currentProjectId, name, desc);
          }
          this.showBaselineDialog = false;
        },
        onRollback: (baselineId: string) => {
          if (this.projectState.currentProjectId) {
            this.projectState.rollbackBaseline(this.projectState.currentProjectId, baselineId);
          }
          this.showBaselineDialog = false;
        },
        onCancel: () => { this.showBaselineDialog = false; }
      })
    }

    if (this.showRiskPanel) {
      RiskPanel({
        alerts: this.projectState.alerts,
        onClose: () => { this.showRiskPanel = false; }
      })
    }
  }

  // ========================================
  // 标题栏
  // ========================================
  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉')
        .fontSize(28)
        .margin({ right: 8 })

      Column() {
        Text('龍魂项目管理')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor('#c41e3a')
        Text(`UID:${MASTER_UID} · ${this.projectState.projects.length}个项目`)
          .fontSize(12)
          .fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)

      Blank()

      // 预警按钮
      Badge({
        value: this.projectState.alerts.length.toString(),
        position: BadgePosition.RightTop,
        style: { badgeSize: 18, badgeColor: '#c41e3a' }
      }) {
        Button() {
          Text('🔔')
            .fontSize(20)
        }
        .type(ButtonType.Circle)
        .backgroundColor(this.projectState.alerts.length > 0 ? 'rgba(196,30,58,0.2)' : '#1a1a1a')
        .width(40)
        .height(40)
        .onClick(() => { this.showRiskPanel = !this.showRiskPanel; })
      }

      // 视图切换
      Button() {
        Text(this.getViewIcon())
          .fontSize(20)
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(40)
      .height(40)
      .onClick(() => { this.cycleViewMode(); })

      // 搜索
      Button() {
        Text(this.showSearch ? '✕' : '🔍')
          .fontSize(20)
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(40)
      .height(40)
      .onClick(() => {
        this.showSearch = !this.showSearch;
        if (!this.showSearch) { this.projectState.searchQuery = ''; }
      })

      // 添加项目
      Button() {
        Text('+')
          .fontSize(24)
          .fontColor('#fff')
      }
      .type(ButtonType.Circle)
      .backgroundColor('#c41e3a')
      .width(40)
      .height(40)
      .onClick(() => { this.editingProject = null; this.showProjectDialog = true; })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // ========================================
  // 预警横幅
  // ========================================
  @Builder
  AlertBannerBuilder() {
    Row() {
      Text('⚠️')
        .fontSize(24)
        .margin({ right: 8 })

      Column() {
        Text(`${this.projectState.alerts.length} 条预警待处理`)
          .fontSize(14)
          .fontWeight(FontWeight.Bold)
          .fontColor('#ffcc00')
        Text(this.getAlertPreview())
          .fontSize(12)
          .fontColor('#ffcc00')
          .maxLines(1)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Button('查看')
        .fontSize(12)
        .fontColor('#0a0a0a')
        .backgroundColor('#ffcc00')
        .borderRadius(12)
        .padding({ left: 12, right: 12 })
        .onClick(() => { this.showRiskPanel = true; })
    }
    .width('100%')
    .padding(12)
    .backgroundColor('rgba(255,204,0,0.1)')
    .border({ width: { bottom: 1 }, color: 'rgba(255,204,0,0.3)' })
  }

  // ========================================
  // 统计卡片
  // ========================================
  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('项目总数', this.projectState.statistics.totalProjects.toString(), '#fff')
      this.StatCard('进行中', this.projectState.statistics.activeProjects.toString(), '#00ff00')
      this.StatCard('已完成', this.projectState.statistics.completedProjects.toString(), '#0066cc')
      this.StatCard('延期', this.projectState.statistics.delayedProjects.toString(), '#ffcc00')
      this.StatCard('风险', this.projectState.statistics.atRiskProjects.toString(), '#c41e3a')
    }
    .width('100%')
    .padding({ left: 12, right: 12, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() {
      Text(value)
        .fontSize(22)
        .fontWeight(FontWeight.Bold)
        .fontColor(color)
      Text(label)
        .fontSize(10)
        .fontColor('#888')
        .margin({ top: 4 })
    }
    .width('19%')
    .padding(6)
    .backgroundColor('#222')
    .borderRadius(8)
    .alignItems(HorizontalAlign.Center)
  }

  // ========================================
  // 视图控制栏
  // ========================================
  @Builder
  ViewControlBuilder() {
    Row() {
      Row() {
        ForEach([
          { key: 'week', label: '周' },
          { key: 'month', label: '月' },
          { key: 'quarter', label: '季' },
          { key: 'year', label: '年' },
          { key: 'all', label: '全部' }
        ], (item: { key: string, label: string }) => {
          Button() {
            Text(item.label)
              .fontSize(12)
              .fontColor(this.projectState.timeRange === item.key ? '#0a0a0a' : '#999')
          }
          .type(ButtonType.Normal)
          .backgroundColor(this.projectState.timeRange === item.key ? '#c41e3a' : '#1a1a1a')
          .borderRadius(8)
          .padding({ left: 10, right: 10, top: 3, bottom: 3 })
          .margin({ right: 4 })
          .onClick(() => {
            this.projectState.timeRange = item.key as 'week' | 'month' | 'quarter' | 'year' | 'all';
          })
        })
      }
      .layoutWeight(1)

      Blank()

      Row() {
        ForEach([
          { key: 'timeline', label: '时间线' },
          { key: 'gantt', label: '甘特图' },
          { key: 'kanban', label: '看板' },
          { key: 'list', label: '列表' }
        ], (item: { key: string, label: string }) => {
          Button() {
            Text(item.label)
              .fontSize(12)
              .fontColor(this.projectState.viewMode === item.key ? '#0a0a0a' : '#999')
          }
          .type(ButtonType.Normal)
          .backgroundColor(this.projectState.viewMode === item.key ? '#c41e3a' : '#1a1a1a')
          .borderRadius(8)
          .padding({ left: 10, right: 10, top: 3, bottom: 3 })
          .margin({ left: 4 })
          .onClick(() => {
            this.projectState.viewMode = item.key as 'timeline' | 'gantt' | 'kanban' | 'list';
          })
        })
      }
    }
    .width('100%')
    .height(44)
    .padding({ left: 12, right: 12 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // ========================================
  // 标签过滤
  // ========================================
  @Builder
  TabFilterBuilder() {
    Row() {
      ForEach([
        { label: '全部', value: '全部' as string },
        { label: '进行中', value: ProjectStatus.ACTIVE },
        { label: '已延期', value: '延期' },
        { label: '高风险', value: '风险' }
      ], (tab: { label: string, value: string }, index: number) => {
        Column() {
          Text(tab.label)
            .fontSize(13)
            .fontWeight(this.selectedTab === index ? FontWeight.Bold : FontWeight.Normal)
            .fontColor(this.selectedTab === index ? '#c41e3a' : '#888')

          if (this.selectedTab === index) {
            Divider()
              .width(20)
              .height(2)
              .color('#c41e3a')
              .margin({ top: 4 })
          }
        }
        .width('25%')
        .padding({ top: 8, bottom: 8 })
        .onClick(() => {
          this.selectedTab = index;
          switch (index) {
            case 0: this.projectState.filterStatus = '全部'; break;
            case 1: this.projectState.filterStatus = ProjectStatus.ACTIVE; break;
            case 2: this.projectState.filterStatus = '全部'; break; // 延期在展示时过滤
            case 3: this.projectState.filterStatus = '全部'; break; // 风险在展示时过滤
          }
        })
      })
    }
    .width('100%')
    .height(44)
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // ========================================
  // 搜索栏
  // ========================================
  @Builder
  SearchBuilder() {
    Row() {
      TextInput({ placeholder: '搜索项目编号、名称、负责人...' })
        .width('100%')
        .height(40)
        .backgroundColor('#262626')
        .fontColor('#fff')
        .placeholderColor('#666')
        .borderRadius(8)
        .padding({ left: 12, right: 12 })
        .onChange((value: string) => { this.projectState.searchQuery = value; })
    }
    .width('100%')
    .padding({ left: 12, right: 12, top: 6, bottom: 6 })
    .backgroundColor('#1a1a1a')
  }

  // ========================================
  // 内容区
  // ========================================
  @Builder
  ContentBuilder() {
    let projects = this.projectState.filteredProjects;

    // 按标签过滤
    if (this.selectedTab === 2) {
      projects = projects.filter(p => p.getDelayDays() > 0);
    } else if (this.selectedTab === 3) {
      projects = projects.filter(p => p.getCurrentRiskLevel() >= RiskLevel.HIGH);
    }

    if (this.projectState.viewMode === 'timeline') {
      TimelineView({
        projects: projects,
        timeRange: this.projectState.timeRange,
        onProjectSelect: (project: Project) => {
          this.editingProject = project;
          this.showProjectDialog = true;
        },
        onMilestoneSelect: (projectId: string, milestone: Milestone) => {
          this.editingMilestone = milestone;
          this.editingProjectId = projectId;
          this.showMilestoneDialog = true;
        }
      })
    } else if (this.projectState.viewMode === 'gantt') {
      GanttChartView({
        projects: projects,
        timeRange: this.projectState.timeRange,
        onProjectSelect: (project: Project) => {
          this.editingProject = project;
          this.showProjectDialog = true;
        }
      })
    } else if (this.projectState.viewMode === 'kanban') {
      KanbanView({
        projects: projects,
        onProjectSelect: (project: Project) => {
          this.editingProject = project;
          this.showProjectDialog = true;
        },
        onMilestoneUpdate: (projectId: string, milestoneId: string, progress: number) => {
          this.projectState.updateMilestoneProgress(projectId, milestoneId, progress, MASTER_UID);
        }
      })
    } else {
      // 列表视图
      List() {
        ForEach(projects, (project: Project) => {
          ListItem() {
            this.ProjectListItem(project)
          }
          .swipeAction({ end: this.ProjectSwipeBuilder(project) })
        }, (project: Project) => project.id)
      }
      .width('100%')
      .layoutWeight(1)
      .scrollBar(BarState.Auto)
      .edgeEffect(EdgeEffect.Spring)
      .padding({ top: 4, bottom: 16 })
    }
  }

  // ========================================
  // 项目列表项
  // ========================================
  @Builder
  ProjectListItem(project: Project) {
    Column() {
      Row() {
        Column() {
          Text(project.name)
            .fontSize(16)
            .fontWeight(FontWeight.Bold)
            .fontColor('#fff')
          Text(`${project.projectNo} · ${project.projectManager}`)
            .fontSize(12)
            .fontColor('#666')
            .margin({ top: 2 })
        }
        .alignItems(HorizontalAlign.Start)
        .layoutWeight(1)

        Text(project.status)
          .fontSize(11)
          .fontColor(this.getStatusTextColor(project.status))
          .backgroundColor(this.getStatusBgColor(project.status))
          .borderRadius(4)
          .padding({ left: 8, right: 8, top: 2, bottom: 2 })
      }
      .width('100%')

      // 进度条
      Row() {
        Stack() {
          Row()
            .width('100%')
            .height(6)
            .backgroundColor('#333')
            .borderRadius(3)
          Row()
            .width(`${project.getProgress()}%`)
            .height(6)
            .backgroundColor(this.getProgressColor(project.getProgress()))
            .borderRadius(3)
        }
        .layoutWeight(1)
        .height(6)

        Text(`${project.getProgress()}%`)
          .fontSize(11)
          .fontColor('#999')
          .margin({ left: 8 })
      }
      .width('100%')
      .margin({ top: 8 })

      // 底部信息
      Row() {
        Text(`📅 ${project.plannedStart.toLocaleDateString()} - ${project.plannedEnd.toLocaleDateString()}`)
          .fontSize(11)
          .fontColor('#666')

        Blank()

        if (project.getDelayDays() > 0) {
          Text(`⏰ 延期${project.getDelayDays()}天`)
            .fontSize(11)
            .fontColor('#ffcc00')
            .margin({ right: 8 })
        }

        Text(`📊 SPI:${project.getSPI().toFixed(1)} CPI:${project.getCPI().toFixed(1)}`)
          .fontSize(10)
          .fontColor('#888')

        if (project.getCurrentRiskLevel() >= RiskLevel.HIGH) {
          Text('⚠️')
            .fontSize(14)
            .margin({ left: 8 })
        }
      }
      .width('100%')
      .margin({ top: 6 })
    }
    .width('100%')
    .padding(14)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .margin({ top: 8, left: 12, right: 12 })
    .onClick(() => {
      this.editingProject = project;
      this.showProjectDialog = true;
    })
  }

  // ========================================
  // 滑动操作
  // ========================================
  @Builder
  ProjectSwipeBuilder(project: Project) {
    Row() {
      Button() {
        Text('里程碑')
          .fontColor('#fff')
          .fontSize(11)
      }
      .type(ButtonType.Capsule)
      .backgroundColor('#0066cc')
      .width(64)
      .height('100%')
      .onClick(() => {
        this.projectState.currentProjectId = project.id;
        this.editingProjectId = project.id;
        this.editingMilestone = null;
        this.showMilestoneDialog = true;
      })

      Button() {
        Text('详情')
          .fontColor('#fff')
          .fontSize(11)
      }
      .type(ButtonType.Capsule)
      .backgroundColor('#ff6600')
      .width(56)
      .height('100%')
      .onClick(() => {
        this.editingProject = project;
        this.showProjectDialog = true;
      })
    }
    .height('100%')
  }

  // ========================================
  // 底部操作栏
  // ========================================
  @Builder
  FooterBuilder() {
    Row() {
      // DNA 标识
      Text('🐉')
        .fontSize(20)
        .margin({ right: 8 })

      Text(`UID:${MASTER_UID}`)
        .fontSize(11)
        .fontColor('#666')
        .layoutWeight(1)

      Button() {
        Text('📊 基线')
          .fontSize(12)
          .fontColor('#fff')
      }
      .type(ButtonType.Normal)
      .backgroundColor('#333')
      .borderRadius(8)
      .padding({ left: 12, right: 12, top: 6, bottom: 6 })
      .margin({ right: 8 })
      .onClick(() => { this.showBaselineDialog = true; })

      Button() {
        Text('📤 导出')
          .fontSize(12)
          .fontColor('#fff')
      }
      .type(ButtonType.Normal)
      .backgroundColor('#333')
      .borderRadius(8)
      .padding({ left: 12, right: 12, top: 6, bottom: 6 })
      .margin({ right: 8 })
      .onClick(() => { this.exportData(); })

      Button() {
        Text('➕ 里程碑')
          .fontSize(12)
          .fontColor('#fff')
      }
      .type(ButtonType.Normal)
      .backgroundColor('#c41e3a')
      .borderRadius(8)
      .padding({ left: 12, right: 12, top: 6, bottom: 6 })
      .onClick(() => {
        if (this.projectState.currentProject) {
          this.editingProjectId = this.projectState.currentProjectId;
          this.editingMilestone = null;
          this.showMilestoneDialog = true;
        } else {
          AlertDialog.show({
            title: '提示',
            message: '请先选择一个项目',
            primaryButton: { value: '确定', action: () => {} }
          });
        }
      })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }

  // ========================================
  // 辅助方法
  // ========================================
  private getViewIcon(): string {
    switch (this.projectState.viewMode) {
      case 'timeline': return '📊';
      case 'gantt': return '📈';
      case 'kanban': return '📋';
      case 'list': return '📄';
      default: return '📊';
    }
  }

  private cycleViewMode(): void {
    const modes: Array<'timeline' | 'gantt' | 'kanban' | 'list'> = ['timeline', 'gantt', 'kanban', 'list'];
    const idx = modes.indexOf(this.projectState.viewMode);
    this.projectState.viewMode = modes[(idx + 1) % modes.length];
  }

  private getStatusTextColor(status: ProjectStatus): string {
    switch (status) {
      case ProjectStatus.ACTIVE: return '#00ff00';
      case ProjectStatus.COMPLETED: return '#0066cc';
      case ProjectStatus.PLANNING: return '#999';
      case ProjectStatus.PAUSED: return '#ffcc00';
      case ProjectStatus.CANCELLED: return '#666';
      case ProjectStatus.ARCHIVED: return '#444';
      default: return '#999';
    }
  }

  private getStatusBgColor(status: ProjectStatus): string {
    switch (status) {
      case ProjectStatus.ACTIVE: return 'rgba(0,255,0,0.1)';
      case ProjectStatus.COMPLETED: return 'rgba(0,102,204,0.1)';
      case ProjectStatus.PLANNING: return 'rgba(153,153,153,0.1)';
      case ProjectStatus.PAUSED: return 'rgba(255,204,0,0.1)';
      case ProjectStatus.CANCELLED: return 'rgba(102,102,102,0.1)';
      case ProjectStatus.ARCHIVED: return 'rgba(68,68,68,0.1)';
      default: return 'rgba(153,153,153,0.1)';
    }
  }

  private getProgressColor(progress: number): string {
    if (progress >= 100) return '#0066cc';
    if (progress >= 75) return '#00cc66';
    if (progress >= 50) return '#ffcc00';
    if (progress >= 25) return '#ff6600';
    return '#c41e3a';
  }

  private getAlertPreview(): string {
    const critical = this.projectState.alerts.filter(a => a.level === 'critical');
    if (critical.length > 0) return `${critical.length} 条严重预警需立即处理`;
    return '点击查看详情';
  }

  private exportData(): void {
    const data = {
      exportTime: new Date().toISOString(),
      dna: MASTER_DNA,
      uid: MASTER_UID,
      confirm: CONFIRM_SEAL,
      projects: this.projectState.projects.map(p => ({
        id: p.id,
        name: p.name,
        status: p.status,
        progress: p.getProgress(),
        spi: p.getSPI().toFixed(2),
        cpi: p.getCPI().toFixed(2),
        delayDays: p.getDelayDays(),
        riskLevel: p.getCurrentRiskLevel(),
        milestoneCount: p.milestones.length
      }))
    };
    console.info(`[龍魂] 数据导出: ${Date.now()}`);
    console.info(`[龍魂] ${JSON.stringify(data, null, 2)}`);
    AlertDialog.show({
      title: '导出完成',
      message: `已导出 ${this.projectState.projects.length} 个项目数据`,
      primaryButton: { value: '确定', action: () => {} }
    });
  }
}
