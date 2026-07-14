// entry/src/main/ets/pages/ProjectDetailPage.ets
// 龍魂 · 项目详情页（带生命周期）

import { navController } from '../navigation/NavigationController';
import { appState } from '../models/AppState';

// === 项目数据接口 ===
interface Project {
  id: string;
  name: string;
  projectNo: string;
  status: string;
  description: string;
  totalPlannedHours: number;
  totalActualHours: number;
  milestones: MilestoneItem[];
  risks: RiskItem[];
  progress: number;
  isDirty: boolean;
  startDate: string;
  endDate: string;
  manager: string;
  team: string[];
  budget: number;
  spent: number;
  priority: 'high' | 'medium' | 'low';
  tags: string[];
}

interface MilestoneItem {
  id: string;
  name: string;
  dueDate: string;
  completed: boolean;
  plannedHours: number;
  actualHours: number;
}

interface RiskItem {
  id: string;
  description: string;
  level: 'high' | 'medium' | 'low';
  status: 'open' | 'mitigated' | 'closed';
  owner: string;
}

@Component
struct ProjectDetailPage {
  @Prop id: string = '';
  @State private project: Project | null = null;
  @State private scrollPosition: number = 0;
  @State private isLoading: boolean = true;
  @State private showConfirmDialog: boolean = false;

  // 页面显示
  onPageShow(): void {
    console.info(`[龍魂] 项目详情页显示: ${this.id}`);
    this.loadProject();

    // 恢复滚动位置
    const state = appState.getPageState('/project/detail');
    if (state.scrollPosition > 0) {
      // 恢复滚动位置
    }
  }

  // 页面隐藏
  onPageHide(): void {
    console.info('[龍魂] 项目详情页隐藏');

    // 保存滚动位置
    appState.savePageState('/project/detail', {
      scrollPosition: this.scrollPosition
    });
  }

  // 返回键处理
  onBackPress(): boolean {
    if (this.project?.isDirty) {
      this.showConfirmDialog = true;
      return true; // 拦截
    }
    return false; // 不拦截
  }

  // 加载项目
  loadProject(): void {
    this.isLoading = true;
    // 模拟从数据库加载
    setTimeout(() => {
      this.project = {
        id: this.id || 'PROJ-001',
        name: '龍魂鸿蒙适配项目',
        projectNo: 'LH-HM-2026-001',
        status: '进行中',
        description: '龍魂系统鸿蒙原生适配，包括模型层、路由层、UIAbility生命周期、Navigation导航栈等核心模块。',
        totalPlannedHours: 480,
        totalActualHours: 320,
        milestones: [
          { id: 'M1', name: '数据模型层', dueDate: '2026-07-20', completed: true, plannedHours: 80, actualHours: 72 },
          { id: 'M2', name: 'UIAbility生命周期', dueDate: '2026-07-25', completed: true, plannedHours: 60, actualHours: 55 },
          { id: 'M3', name: '路由配置中心', dueDate: '2026-07-30', completed: false, plannedHours: 100, actualHours: 80 },
          { id: 'M4', name: 'Navigation导航栈', dueDate: '2026-08-05', completed: false, plannedHours: 120, actualHours: 60 },
          { id: 'M5', name: '页面生命周期', dueDate: '2026-08-10', completed: false, plannedHours: 80, actualHours: 35 },
          { id: 'M6', name: '集成测试', dueDate: '2026-08-15', completed: false, plannedHours: 40, actualHours: 18 }
        ],
        risks: [
          { id: 'R1', description: '鸿蒙API兼容性', level: 'medium', status: 'open', owner: 'UID9622' },
          { id: 'R2', description: 'Navigation性能', level: 'low', status: 'mitigated', owner: 'UID9622' },
          { id: 'R3', description: '国密签名延迟', level: 'high', status: 'open', owner: 'UID9622' }
        ],
        progress: 67,
        isDirty: false,
        startDate: '2026-07-14',
        endDate: '2026-08-15',
        manager: '诸葛鑫',
        team: ['UID9622', '宝宝', '雯雯', '鲁班'],
        budget: 500000,
        spent: 320000,
        priority: 'high',
        tags: ['鸿蒙', '核心', 'P0']
      };
      this.isLoading = false;
    }, 500);
  }

  // 获取进度颜色
  getProgressColor(progress: number): string {
    if (progress >= 80) return '#00ff00';
    if (progress >= 50) return '#ffaa00';
    return '#ff4444';
  }

  // 获取风险等级颜色
  getRiskColor(level: string): string {
    switch (level) {
      case 'high': return '#ff4444';
      case 'medium': return '#ffaa00';
      case 'low': return '#00ff00';
      default: return '#666';
    }
  }

  // 获取风险状态文本
  getRiskStatusText(status: string): string {
    switch (status) {
      case 'open': return '未处理';
      case 'mitigated': return '已缓解';
      case 'closed': return '已关闭';
      default: return status;
    }
  }

  // 获取里程碑状态图标
  getMilestoneIcon(completed: boolean): string {
    return completed ? '✅' : '⏳';
  }

  build() {
    Column() {
      // 导航栏
      this.NavBarBuilder()

      if (this.isLoading) {
        // 加载中
        Column() {
          LoadingProgress()
            .width(48)
            .height(48)
            .color('#c41e3a')
          Text('加载中...')
            .fontSize(14)
            .fontColor('#888')
            .margin({ top: 12 })
        }
        .width('100%')
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else if (this.project) {
        // 项目详情
        Scroll() {
          Column() {
            this.ProjectHeaderBuilder()
            this.ProjectStatsBuilder()
            this.ProgressBuilder()
            this.MilestoneListBuilder()
            this.RiskListBuilder()
            this.ActionButtonsBuilder()
          }
          .width('100%')
          .padding(16)
        }
        .width('100%')
        .layoutWeight(1)
        .scrollBar(BarState.Auto)
        .onScroll((xOffset: number, yOffset: number) => {
          this.scrollPosition = yOffset;
        })
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder
  NavBarBuilder() {
    Row() {
      Button() {
        Text('‹')
          .fontSize(24)
          .fontColor('#fff')
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(40)
      .height(40)
      .onClick(() => {
        navController.back();
      })

      Text(this.project?.name || '项目详情')
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
        .layoutWeight(1)
        .textAlign(TextAlign.Center)

      Button() {
        Text('✎')
          .fontSize(18)
          .fontColor('#fff')
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(40)
      .height(40)
      .onClick(() => {
        navController.push('ProjectEdit', { id: this.id });
      })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  ProjectHeaderBuilder() {
    Column() {
      Row() {
        Column() {
          Text(this.project!.name)
            .fontSize(24)
            .fontWeight(FontWeight.Bold)
            .fontColor('#fff')

          Text(this.project!.projectNo)
            .fontSize(14)
            .fontColor('#888')
            .margin({ top: 4 })
        }
        .alignItems(HorizontalAlign.Start)
        .layoutWeight(1)

        Column() {
          Text(this.project!.priority === 'high' ? '🔴' : this.project!.priority === 'medium' ? '🟡' : '🟢')
            .fontSize(28)
        }
      }
      .width('100%')
      .alignItems(VerticalAlign.Top)

      Row() {
        // 状态标签
        Text(this.project!.status)
          .fontSize(12)
          .fontColor('#fff')
          .backgroundColor('#c41e3a')
          .borderRadius(4)
          .padding({ left: 8, right: 8, top: 2, bottom: 2 })

        Text(`${this.project!.progress}%`)
          .fontSize(12)
          .fontColor(this.getProgressColor(this.project!.progress))
          .margin({ left: 8 })

        // 标签
        ForEach(this.project!.tags, (tag: string) => {
          Text(tag)
            .fontSize(10)
            .fontColor('#888')
            .backgroundColor('#222')
            .borderRadius(3)
            .padding({ left: 6, right: 6, top: 1, bottom: 1 })
            .margin({ left: 6 })
        })
      }
      .margin({ top: 8 })

      Text(this.project!.description)
        .fontSize(13)
        .fontColor('#999')
        .margin({ top: 12 })
        .maxLines(3)
        .textOverflow({ overflow: TextOverflow.Ellipsis })
    }
    .width('100%')
    .alignItems(HorizontalAlign.Start)
    .margin({ bottom: 16 })
  }

  @Builder
  ProjectStatsBuilder() {
    Row() {
      this.StatItem('计划工时', `${this.project!.totalPlannedHours}h`)
      this.StatItem('实际工时', `${this.project!.totalActualHours}h`)
      this.StatItem('里程碑', `${this.project!.milestones.length}个`)
      this.StatItem('风险', `${this.project!.risks.length}项`)
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .margin({ bottom: 16 })
  }

  @Builder
  StatItem(label: string, value: string) {
    Column() {
      Text(value)
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
      Text(label)
        .fontSize(11)
        .fontColor('#666')
        .margin({ top: 4 })
    }
    .width('25%')
    .alignItems(HorizontalAlign.Center)
  }

  @Builder
  ProgressBuilder() {
    Column() {
      Row() {
        Text('项目进度')
          .fontSize(14)
          .fontColor('#888')
        Text(`${this.project!.progress}%`)
          .fontSize(14)
          .fontWeight(FontWeight.Bold)
          .fontColor(this.getProgressColor(this.project!.progress))
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceBetween)
      .margin({ bottom: 8 })

      // 进度条
      Row() {
        Row()
          .width(`${this.project!.progress}%`)
          .height(6)
          .backgroundColor(this.getProgressColor(this.project!.progress))
          .borderRadius(3)
          .animation({ duration: 500, curve: Curve.EaseOut })
      }
      .width('100%')
      .height(6)
      .backgroundColor('#333')
      .borderRadius(3)
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .margin({ bottom: 16 })
  }

  @Builder
  MilestoneListBuilder() {
    Column() {
      Row() {
        Text('里程碑')
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
      }
      .width('100%')
      .margin({ bottom: 12 })

      ForEach(this.project!.milestones, (milestone: MilestoneItem, index: number) => {
        Column() {
          Row() {
            Text(this.getMilestoneIcon(milestone.completed))
              .fontSize(16)
              .margin({ right: 8 })

            Column() {
              Text(milestone.name)
                .fontSize(14)
                .fontColor(milestone.completed ? '#888' : '#fff')
                .decoration({ type: milestone.completed ? TextDecorationType.LineThrough : TextDecorationType.None })

              Text(`截止: ${milestone.dueDate}  |  计划: ${milestone.plannedHours}h  |  实际: ${milestone.actualHours}h`)
                .fontSize(11)
                .fontColor('#666')
                .margin({ top: 2 })
            }
            .alignItems(HorizontalAlign.Start)
            .layoutWeight(1)
          }
          .width('100%')
          .padding({ top: 8, bottom: 8 })

          if (index < this.project!.milestones.length - 1) {
            Divider().color('#333').height(0.5)
          }
        }
        .width('100%')
      })
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .margin({ bottom: 16 })
  }

  @Builder
  RiskListBuilder() {
    Column() {
      Row() {
        Text('风险项')
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
        Text(`${this.project!.risks.length}项`)
          .fontSize(12)
          .fontColor('#666')
          .margin({ left: 8 })
      }
      .width('100%')
      .margin({ bottom: 12 })

      ForEach(this.project!.risks, (risk: RiskItem) => {
        Row() {
          // 风险等级圆点
          Circle({ width: 8, height: 8 })
            .fill(this.getRiskColor(risk.level))

          Column() {
            Text(risk.description)
              .fontSize(13)
              .fontColor('#fff')
              .maxLines(2)
              .textOverflow({ overflow: TextOverflow.Ellipsis })
            Text(`负责人: ${risk.owner}  |  ${this.getRiskStatusText(risk.status)}`)
              .fontSize(11)
              .fontColor('#666')
              .margin({ top: 2 })
          }
          .alignItems(HorizontalAlign.Start)
          .layoutWeight(1)
          .margin({ left: 8 })
        }
        .width('100%')
        .padding({ top: 6, bottom: 6 })
      })
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .margin({ bottom: 16 })
  }

  @Builder
  ActionButtonsBuilder() {
    Column() {
      Button('查看甘特图')
        .fontSize(14)
        .fontColor('#fff')
        .backgroundColor('#333')
        .borderRadius(8)
        .width('100%')
        .height(44)
        .onClick(() => {
          navController.push('MilestoneTimeline', { projectId: this.id });
        })

      Button('编辑项目')
        .fontSize(14)
        .fontColor('#fff')
        .backgroundColor('#c41e3a')
        .borderRadius(8)
        .width('100%')
        .height(44)
        .margin({ top: 12 })
        .onClick(() => {
          navController.push('ProjectEdit', { id: this.id });
        })
    }
    .width('100%')
    .margin({ top: 16, bottom: 32 })
  }
}
