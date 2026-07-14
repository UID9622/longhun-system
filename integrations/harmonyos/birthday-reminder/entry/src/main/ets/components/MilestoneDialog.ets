// 龍魂 · 里程碑弹窗 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { Milestone, MilestoneStatus, Priority, RiskLevel, DependencyType } from '../models/MilestoneModel';

@Component
export struct MilestoneDialog {
  @Link milestone: Milestone | null;
  @Prop projectId: string = '';
  onSave?: (milestone: Milestone) => void;
  onCancel?: () => void;

  @State private name: string = '';
  @State private description: string = '';
  @State private priority: number = 2;
  @State private estimatedHours: number = 0;
  @State private progress: number = 0;
  @State private riskLevel: number = 0;
  @State private riskDesc: string = '';
  @State private startDate: string = '';
  @State private endDate: string = '';
  @State private assignedTo: string = '';

  aboutToAppear() {
    if (this.milestone) {
      this.name = this.milestone.name;
      this.description = this.milestone.description;
      this.priority = this.getPriorityIndex(this.milestone.priority);
      this.estimatedHours = this.milestone.estimatedHours;
      this.progress = this.milestone.progress;
      this.riskLevel = this.getRiskIndex(this.milestone.riskLevel);
      this.riskDesc = this.milestone.riskDescription;
      this.startDate = this.milestone.plannedStart.toISOString().split('T')[0];
      this.endDate = this.milestone.plannedEnd.toISOString().split('T')[0];
      this.assignedTo = this.milestone.assignedTo.join(', ');
    } else {
      const now = new Date();
      this.startDate = now.toISOString().split('T')[0];
      this.endDate = new Date(now.getTime() + 7*24*60*60*1000).toISOString().split('T')[0];
    }
  }

  private getPriorityIndex(p: Priority): number {
    return [Priority.P0, Priority.P1, Priority.P2, Priority.P3, Priority.P4].indexOf(p);
  }

  private getRiskIndex(r: RiskLevel): number {
    return [RiskLevel.NONE, RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL].indexOf(r);
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text(this.milestone ? '编辑里程碑' : '新建里程碑')
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

      Scroll() {
        Column() {
          this.FormField('名称', this.name, (v: string) => { this.name = v; })
          this.FormField('描述', this.description, (v: string) => { this.description = v; })

          // 优先级
          Row() {
            Text('优先级')
              .fontSize(14)
              .fontColor('#888')
              .width(80)
            Select([
              { value: 'P0-紧急', label: 'P0-紧急 ⚡' },
              { value: 'P1-高', label: 'P1-高' },
              { value: 'P2-中', label: 'P2-中' },
              { value: 'P3-低', label: 'P3-低' },
              { value: 'P4-最低', label: 'P4-最低' }
            ])
            .value(['P0-紧急','P1-高','P2-中','P3-低','P4-最低'][this.priority])
            .selected(this.priority)
            .onSelect((index: number) => { this.priority = index; })
            .layoutWeight(1)
          }
          .width('100%')
          .padding({ top: 8, bottom: 8 })

          this.FormField('预估工时(小时)', this.estimatedHours.toString(), (v: string) => {
            this.estimatedHours = parseFloat(v) || 0;
          })

          this.FormField('负责人(逗号分隔)', this.assignedTo, (v: string) => { this.assignedTo = v; })

          // 时间
          Text('时间计划')
            .fontSize(13)
            .fontWeight(FontWeight.Bold)
            .fontColor('#c41e3a')
            .width('100%')
            .padding({ top: 12, bottom: 8 })

          Row() {
            Text('开始')
              .fontSize(14)
              .fontColor('#888')
              .width(80)
            DatePicker({
              start: new Date('2020-01-01'),
              end: new Date('2030-12-31'),
              selected: new Date(this.startDate)
            })
            .onChange((v: DatePickerResult) => {
              this.startDate = `${v.year}-${(v.month!+1).toString().padStart(2,'0')}-${v.day!.toString().padStart(2,'0')}`;
            })
            .layoutWeight(1)
          }
          .width('100%')
          .padding({ top: 4, bottom: 4 })

          Row() {
            Text('结束')
              .fontSize(14)
              .fontColor('#888')
              .width(80)
            DatePicker({
              start: new Date('2020-01-01'),
              end: new Date('2030-12-31'),
              selected: new Date(this.endDate)
            })
            .onChange((v: DatePickerResult) => {
              this.endDate = `${v.year}-${(v.month!+1).toString().padStart(2,'0')}-${v.day!.toString().padStart(2,'0')}`;
            })
            .layoutWeight(1)
          }
          .width('100%')
          .padding({ top: 4, bottom: 4 })

          // 风险
          Text('风险信息')
            .fontSize(13)
            .fontWeight(FontWeight.Bold)
            .fontColor('#c41e3a')
            .width('100%')
            .padding({ top: 12, bottom: 8 })

          Row() {
            Text('风险等级')
              .fontSize(14)
              .fontColor('#888')
              .width(80)
            Select([
              { value: '无风险', label: '无风险 🟢' },
              { value: '低风险', label: '低风险 🔵' },
              { value: '中风险', label: '中风险 🟡' },
              { value: '高风险', label: '高风险 🟠' },
              { value: '极高风险', label: '极高风险 🔴' }
            ])
            .value(['无风险','低风险','中风险','高风险','极高风险'][this.riskLevel])
            .selected(this.riskLevel)
            .onSelect((index: number) => { this.riskLevel = index; })
            .layoutWeight(1)
          }
          .width('100%')
          .padding({ top: 4, bottom: 4 })

          this.FormField('风险描述', this.riskDesc, (v: string) => { this.riskDesc = v; })

          // 进度（编辑时）
          if (this.milestone) {
            Text('进度更新')
              .fontSize(13)
              .fontWeight(FontWeight.Bold)
              .fontColor('#c41e3a')
              .width('100%')
              .padding({ top: 12, bottom: 8 })

            Row() {
              Slider({
                value: this.progress,
                min: 0,
                max: 100,
                step: 5,
                style: SliderStyle.InSet
              })
              .width('70%')
              .onChange((v: number) => { this.progress = v; })

              Text(`${this.progress}%`)
                .fontSize(16)
                .fontWeight(FontWeight.Bold)
                .fontColor('#c41e3a')
                .width('25%')
                .textAlign(TextAlign.Center)
            }
            .width('100%')
          }
        }
        .width('100%')
        .padding({ left: 16, right: 16, bottom: 80 })
      }
      .layoutWeight(1)
      .width('100%')

      // 保存按钮
      Button() {
        Text(this.milestone ? '💾 保存修改' : '💾 创建里程碑')
          .fontColor('#fff')
          .fontSize(14)
      }
      .type(ButtonType.Normal)
      .backgroundColor('#c41e3a')
      .borderRadius(8)
      .width('100%')
      .padding(12)
      .margin(16)
      .onClick(() => { this.saveMilestone(); })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
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

  private saveMilestone(): void {
    if (!this.name.trim()) {
      AlertDialog.show({
        title: '验证失败',
        message: '里程碑名称不能为空',
        primaryButton: { value: '确定', action: () => {} }
      });
      return;
    }

    const priorities = [Priority.P0, Priority.P1, Priority.P2, Priority.P3, Priority.P4];
    const riskLevels = [RiskLevel.NONE, RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL];

    const data: Partial<Milestone> = {
      id: this.milestone?.id,
      name: this.name,
      description: this.description,
      priority: priorities[this.priority],
      estimatedHours: this.estimatedHours,
      progress: this.progress,
      riskLevel: riskLevels[this.riskLevel],
      riskDescription: this.riskDesc,
      assignedTo: this.assignedTo.split(',').map(s => s.trim()).filter(s => s.length > 0),
      plannedStart: new Date(this.startDate),
      plannedEnd: new Date(this.endDate),
      deliverables: this.milestone?.deliverables || [],
      checkPoints: this.milestone?.checkPoints || [],
      dependencies: this.milestone?.dependencies || []
    };

    if (this.onSave) this.onSave(new Milestone(data));
  }
}
