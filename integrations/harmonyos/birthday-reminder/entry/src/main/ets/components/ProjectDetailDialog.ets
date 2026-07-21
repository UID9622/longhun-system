// 龍魂 · 项目详情弹窗 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { Project, ProjectStatus, Priority, RiskLevel, Milestone } from '../models/MilestoneModel';

const MASTER_UID = "9622";

@Component
export struct ProjectDetailDialog {
  @Link project: Project | null;
  onSave?: (project: Project) => void;
  onDelete?: (id: string) => void;
  onCancel?: () => void;

  @State private name: string = '';
  @State private description: string = '';
  @State private status: number = 0;
  @State private projectManager: string = '';
  @State private productManager: string = '';
  @State private techLead: string = '';
  @State private budget: number = 0;
  @State private costIncurred: number = 0;
  @State private startDate: string = '';
  @State private endDate: string = '';

  aboutToAppear() {
    if (this.project) {
      this.name = this.project.name;
      this.description = this.project.description;
      this.status = this.getStatusIndex(this.project.status);
      this.projectManager = this.project.projectManager;
      this.productManager = this.project.productManager;
      this.techLead = this.project.techLead;
      this.budget = this.project.budget;
      this.costIncurred = this.project.costIncurred;
      this.startDate = this.project.plannedStart.toISOString().split('T')[0];
      this.endDate = this.project.plannedEnd.toISOString().split('T')[0];
    }
  }

  private getStatusIndex(s: ProjectStatus): number {
    const statuses = [ProjectStatus.PLANNING, ProjectStatus.ACTIVE, ProjectStatus.PAUSED,
                      ProjectStatus.COMPLETED, ProjectStatus.CANCELLED, ProjectStatus.ARCHIVED];
    return statuses.indexOf(s);
  }

  private getStatusByIndex(i: number): ProjectStatus {
    const statuses = [ProjectStatus.PLANNING, ProjectStatus.ACTIVE, ProjectStatus.PAUSED,
                      ProjectStatus.COMPLETED, ProjectStatus.CANCELLED, ProjectStatus.ARCHIVED];
    return statuses[i];
  }

  build() {
    Column() {
      // 标题
      Row() {
        Text(this.project ? '编辑项目' : '新建项目')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')

        Blank()

        Button() {
          Text('✕')
            .fontSize(20)
            .fontColor('#888')
        }
        .type(ButtonType.Circle)
        .backgroundColor('#00000000')
        .onClick(() => { if (this.onCancel) this.onCancel(); })
      }
      .width('100%')
      .padding(16)

      // 表单内容
      Scroll() {
        Column() {
          // 基本信息
          this.SectionHeader('基本信息')
          this.FormField('项目名称', this.name, (v: string) => { this.name = v; })
          this.FormField('项目描述', this.description, (v: string) => { this.description = v; })

          // 状态选择
          Row() {
            Text('项目状态')
              .fontSize(14)
              .fontColor('#888')
              .width(80)
            Select([{ value: '规划中', label: '规划中' }, { value: '进行中', label: '进行中' },
                    { value: '已暂停', label: '已暂停' }, { value: '已完成', label: '已完成' }])
              .value(this.getStatusByIndex(this.status))
              .selected(this.status)
              .onSelect((index: number) => { this.status = index; })
              .layoutWeight(1)
          }
          .width('100%')
          .padding({ top: 8, bottom: 8 })

          // 负责人
          this.SectionHeader('负责人')
          this.FormField('项目经理', this.projectManager, (v: string) => { this.projectManager = v; })
          this.FormField('产品经理', this.productManager, (v: string) => { this.productManager = v; })
          this.FormField('技术负责人', this.techLead, (v: string) => { this.techLead = v; })

          // 预算
          this.SectionHeader('预算信息')
          this.FormField('总预算(元)', this.budget.toString(), (v: string) => {
            this.budget = parseFloat(v) || 0;
          })
          this.FormField('已发生成本(元)', this.costIncurred.toString(), (v: string) => {
            this.costIncurred = parseFloat(v) || 0;
          })

          // 时间
          this.SectionHeader('时间计划')
          Row() {
            Text('开始日期')
              .fontSize(14)
              .fontColor('#888')
              .width(80)
            DatePicker({
              start: new Date('2020-01-01'),
              end: new Date('2030-12-31'),
              selected: new Date(this.startDate)
            })
            .onChange((value: DatePickerResult) => {
              this.startDate = `${value.year}-${(value.month!+1).toString().padStart(2,'0')}-${value.day!.toString().padStart(2,'0')}`;
            })
            .layoutWeight(1)
          }
          .width('100%')
          .padding({ top: 4, bottom: 4 })

          Row() {
            Text('结束日期')
              .fontSize(14)
              .fontColor('#888')
              .width(80)
            DatePicker({
              start: new Date('2020-01-01'),
              end: new Date('2030-12-31'),
              selected: new Date(this.endDate)
            })
            .onChange((value: DatePickerResult) => {
              this.endDate = `${value.year}-${(value.month!+1).toString().padStart(2,'0')}-${value.day!.toString().padStart(2,'0')}`;
            })
            .layoutWeight(1)
          }
          .width('100%')
          .padding({ top: 4, bottom: 4 })

          // 审计信息（编辑时显示）
          if (this.project) {
            this.SectionHeader('审计信息')
            Text(`创建: ${this.project.createdAt.toLocaleString()}`)
              .fontSize(12)
              .fontColor('#555')
              .width('100%')
            Text(`DNA: ${this.project.dnaSignature}`)
              .fontSize(11)
              .fontColor('#444')
              .fontFamily('monospace')
              .width('100%')
              .margin({ top: 4 })
          }
        }
        .width('100%')
        .padding({ left: 16, right: 16 })
      }
      .layoutWeight(1)
      .width('100%')

      // 底部按钮
      if (this.project) {
        Row() {
          Button() {
            Text('🗑️ 删除')
              .fontColor('#ff4444')
              .fontSize(14)
          }
          .type(ButtonType.Normal)
          .backgroundColor('rgba(255,68,68,0.1)')
          .border({ width: 1, color: '#ff4444' })
          .borderRadius(8)
          .width('40%')
          .onClick(() => { if (this.onDelete) this.onDelete(this.project!.id); })

          Button() {
            Text('💾 保存')
              .fontColor('#fff')
              .fontSize(14)
          }
          .type(ButtonType.Normal)
          .backgroundColor('#c41e3a')
          .borderRadius(8)
          .width('55%')
          .onClick(() => { this.saveProject(); })
        }
        .width('100%')
        .padding(16)
        .justifyContent(FlexAlign.SpaceBetween)
      } else {
        Button() {
          Text('💾 创建项目')
            .fontColor('#fff')
            .fontSize(14)
        }
        .type(ButtonType.Normal)
        .backgroundColor('#c41e3a')
        .borderRadius(8)
        .width('100%')
        .padding(12)
        .margin(16)
        .onClick(() => { this.saveProject(); })
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder
  SectionHeader(title: string) {
    Text(title)
      .fontSize(13)
      .fontWeight(FontWeight.Bold)
      .fontColor('#c41e3a')
      .width('100%')
      .padding({ top: 16, bottom: 8 })
      .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  FormField(label: string, value: string, onChange: (v: string) => void) {
    Row() {
      Text(label)
        .fontSize(14)
        .fontColor('#888')
        .width(80)
      TextInput({ text: value, placeholder: `请输入${label}` })
        .layoutWeight(1)
        .fontColor('#fff')
        .placeholderColor('#555')
        .backgroundColor('#1a1a1a')
        .borderRadius(6)
        .padding({ left: 12, right: 12 })
        .height(40)
        .onChange((v: string) => { onChange(v); })
    }
    .width('100%')
    .padding({ top: 6, bottom: 6 })
  }

  private saveProject(): void {
    if (!this.name.trim()) {
      AlertDialog.show({
        title: '验证失败',
        message: '项目名称不能为空',
        primaryButton: { value: '确定', action: () => {} }
      });
      return;
    }

    const projectData: Partial<Project> = {
      name: this.name,
      description: this.description,
      status: this.getStatusByIndex(this.status),
      projectManager: this.projectManager,
      productManager: this.productManager,
      techLead: this.techLead,
      budget: this.budget,
      costIncurred: this.costIncurred,
      plannedStart: new Date(this.startDate),
      plannedEnd: new Date(this.endDate)
    };

    if (this.project) {
      projectData.id = this.project.id;
      projectData.projectNo = this.project.projectNo;
      projectData.milestones = this.project.milestones;
      projectData.baselines = this.project.baselines;
      projectData.risks = this.project.risks;
      projectData.teamMembers = this.project.teamMembers;
    }

    const saved = new Project(projectData);
    if (this.onSave) this.onSave(saved);
  }
}
