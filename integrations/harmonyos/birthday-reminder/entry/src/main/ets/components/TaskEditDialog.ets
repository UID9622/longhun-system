// entry/src/main/ets/components/TaskEditDialog.ets
// 龍魂 · 周报任务编辑弹窗 · ArkTS

import { WeeklyTask, TaskStatus, TaskType, Priority } from '../models/WeeklyModel';

@CustomDialog
export struct TaskEditDialog {
  controller: CustomDialogController;
  task?: WeeklyTask;
  onSave?: (task: WeeklyTask) => void;
  onClose?: () => void;
  reportId: string = '';

  @State private title: string = '';
  @State private description: string = '';
  @State private projectName: string = '';
  @State private taskType: TaskType = TaskType.OTHER;
  @State private priority: Priority = Priority.P2;
  @State private status: TaskStatus = TaskStatus.NOT_STARTED;
  @State private plannedHours: number = 0;
  @State private actualHours: number = 0;
  @State private overtimeHours: number = 0;
  @State private progress: number = 0;
  @State private showTypePicker: boolean = false;
  @State private showPriorityPicker: boolean = false;
  @State private showStatusPicker: boolean = false;

  aboutToAppear() {
    if (this.task) {
      this.title = this.task.title || '';
      this.description = this.task.description || '';
      this.projectName = this.task.projectName || '';
      this.taskType = this.task.taskType || TaskType.OTHER;
      this.priority = this.task.priority || Priority.P2;
      this.status = this.task.status || TaskStatus.NOT_STARTED;
      this.plannedHours = this.task.plannedHours || 0;
      this.actualHours = this.task.actualHours || 0;
      this.overtimeHours = this.task.overtimeHours || 0;
      this.progress = this.task.progress || 0;
    }
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text(this.task ? '编辑任务' : '新增任务').fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff').layoutWeight(1)
        Text('✕').fontSize(20).fontColor('#888')
          .onClick(() => { this.onClose?.(); this.controller.close(); })
      }
      .width('100%').padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      Scroll() {
        Column() {
          // 任务标题
          this.InputField('任务标题 *', this.title, (v: string) => { this.title = v; }, '请输入任务标题')

          // 所属项目
          this.InputField('所属项目', this.projectName, (v: string) => { this.projectName = v; }, '请输入项目名称')

          // 任务类型
          this.SelectField('任务类型', this.taskType, this.showTypePicker, () => { this.showTypePicker = !this.showTypePicker; })
          if (this.showTypePicker) {
            this.TypePickerBuilder()
          }

          // 优先级
          this.SelectField('优先级', this.priority, this.showPriorityPicker, () => { this.showPriorityPicker = !this.showPriorityPicker; })
          if (this.showPriorityPicker) {
            this.PriorityPickerBuilder()
          }

          // 状态
          this.SelectField('状态', this.status, this.showStatusPicker, () => { this.showStatusPicker = !this.showStatusPicker; })
          if (this.showStatusPicker) {
            this.StatusPickerBuilder()
          }

          // 任务描述
          Column() {
            Text('任务描述').fontSize(13).fontColor('#888').margin({ bottom: 6 }).alignSelf(ItemAlign.Start)
            TextArea({ text: $$this.description, placeholder: '请输入任务描述' })
              .height(80).backgroundColor('#2a2a2a').fontColor('#fff').placeholderColor('#555')
              .borderRadius(8).padding(12)
          }
          .width('100%').padding({ left: 16, right: 16, top: 12 })

          // 工时区
          this.HourSectionBuilder()

          // 进度
          this.ProgressSectionBuilder()

          // 提示
          if (this.title.length === 0) {
            Text('请填写任务标题').fontSize(12).fontColor('#ffcc00').padding(16)
          }
        }
      }
      .width('100%').layoutWeight(1)
      .scrollBar(BarState.Auto)

      // 底部按钮
      Row() {
        Button('取消')
          .fontSize(14).fontColor('#888').backgroundColor('#333')
          .borderRadius(8).layoutWeight(1).height(44).margin({ right: 8 })
          .onClick(() => { this.onClose?.(); this.controller.close(); })
        Button(this.task ? '更新' : '创建')
          .fontSize(14).fontColor('#0a0a0a').backgroundColor('#c41e3a')
          .borderRadius(8).layoutWeight(1).height(44)
          .onClick(() => { this.handleSave(); })
      }
      .width('100%').padding(16)
      .border({ width: { top: 1 }, color: '#333' })
    }
    .width('100%').height('85%').backgroundColor('#1a1a1a').borderRadius({ topLeft: 16, topRight: 16 })
  }

  @Builder
  InputField(label: string, value: string, onChange: (v: string) => void, placeholder: string) {
    Column() {
      Text(label).fontSize(13).fontColor('#888').margin({ bottom: 6 }).alignSelf(ItemAlign.Start)
      TextInput({ text: $$value, placeholder: placeholder })
        .width('100%').height(44).backgroundColor('#2a2a2a').fontColor('#fff')
        .placeholderColor('#555').borderRadius(8).padding({ left: 12, right: 12 })
    }
    .width('100%').padding({ left: 16, right: 16, top: 12 })
  }

  @Builder
  SelectField(label: string, value: string, isExpanded: boolean, onClick: () => void) {
    Column() {
      Text(label).fontSize(13).fontColor('#888').margin({ bottom: 6 }).alignSelf(ItemAlign.Start)
      Row() {
        Text(value).fontSize(14).fontColor('#fff').layoutWeight(1)
        Text(isExpanded ? '▲' : '▼').fontSize(12).fontColor('#888')
      }
      .width('100%').height(44).backgroundColor('#2a2a2a').borderRadius(8)
      .padding({ left: 12, right: 12 }).onClick(onClick)
    }
    .width('100%').padding({ left: 16, right: 16, top: 12 })
  }

  @Builder
  TypePickerBuilder() {
    Column() {
      ForEach(Object.values(TaskType), (type: string) => {
        Row() {
          Text(type).fontSize(14).fontColor(type === this.taskType ? '#c41e3a' : '#ccc').layoutWeight(1)
          if (type === this.taskType) { Text('✓').fontSize(14).fontColor('#c41e3a') }
        }
        .width('100%').height(40).padding({ left: 16, right: 16 })
        .backgroundColor(type === this.taskType ? 'rgba(196,30,58,0.1)' : 'transparent')
        .onClick(() => { this.taskType = type as TaskType; this.showTypePicker = false; })
      })
    }
    .margin({ left: 16, right: 16 }).backgroundColor('#2a2a2a').borderRadius(8)
  }

  @Builder
  PriorityPickerBuilder() {
    Column() {
      ForEach(Object.values(Priority), (p: string) => {
        Row() {
          Text(p).fontSize(14).fontColor(p === this.priority ? '#c41e3a' : '#ccc').layoutWeight(1)
          if (p === this.priority) { Text('✓').fontSize(14).fontColor('#c41e3a') }
        }
        .width('100%').height(40).padding({ left: 16, right: 16 })
        .backgroundColor(p === this.priority ? 'rgba(196,30,58,0.1)' : 'transparent')
        .onClick(() => { this.priority = p as Priority; this.showPriorityPicker = false; })
      })
    }
    .margin({ left: 16, right: 16 }).backgroundColor('#2a2a2a').borderRadius(8)
  }

  @Builder
  StatusPickerBuilder() {
    Column() {
      ForEach(Object.values(TaskStatus), (s: string) => {
        Row() {
          Text(s).fontSize(14).fontColor(s === this.status ? '#c41e3a' : '#ccc').layoutWeight(1)
          if (s === this.status) { Text('✓').fontSize(14).fontColor('#c41e3a') }
        }
        .width('100%').height(40).padding({ left: 16, right: 16 })
        .backgroundColor(s === this.status ? 'rgba(196,30,58,0.1)' : 'transparent')
        .onClick(() => { this.status = s as TaskStatus; this.showStatusPicker = false; })
      })
    }
    .margin({ left: 16, right: 16 }).backgroundColor('#2a2a2a').borderRadius(8)
  }

  @Builder
  HourSectionBuilder() {
    Column() {
      Text('工时信息').fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').alignSelf(ItemAlign.Start).margin({ left: 16, top: 12 })
      Row() {
        Column() { Text('计划工时(h)').fontSize(11).fontColor('#888').margin({ bottom: 4 }); this.HourInput(this.plannedHours, (v: number) => { this.plannedHours = v; }) }
        .layoutWeight(1).margin({ right: 8 })
        Column() { Text('实际工时(h)').fontSize(11).fontColor('#888').margin({ bottom: 4 }); this.HourInput(this.actualHours, (v: number) => { this.actualHours = v; }) }
        .layoutWeight(1).margin({ left: 4, right: 4 })
        Column() { Text('加班工时(h)').fontSize(11).fontColor('#888').margin({ bottom: 4 }); this.HourInput(this.overtimeHours, (v: number) => { this.overtimeHours = v; }) }
        .layoutWeight(1).margin({ left: 8 })
      }
      .width('100%').padding({ left: 16, right: 16, top: 8 })
    }
  }

  @Builder
  HourInput(value: number, onChange: (v: number) => void) {
    TextInput({ text: value.toString() })
      .width('100%').height(40).backgroundColor('#2a2a2a').fontColor('#fff')
      .borderRadius(8).padding({ left: 8, right: 8 }).type(InputType.Number)
      .onChange((v: string) => { onChange(parseFloat(v) || 0); })
  }

  @Builder
  ProgressSectionBuilder() {
    Column() {
      Text(`完成进度: ${this.progress}%`).fontSize(13).fontColor('#888').margin({ bottom: 8 }).alignSelf(ItemAlign.Start)
      Row() {
        Slider({
          value: this.progress,
          min: 0,
          max: 100,
          step: 5,
          style: SliderStyle.InSet
        })
        .width('100%').trackColor('#333').selectedColor('#c41e3a')
        .onChange((value: number) => { this.progress = value; })
      }
    }
    .width('100%').padding({ left: 16, right: 16, top: 12 })
  }

  handleSave(): void {
    if (this.title.trim().length === 0) return;
    const newTask = new WeeklyTask({
      id: this.task?.id,
      title: this.title,
      description: this.description,
      projectName: this.projectName,
      taskType: this.taskType,
      priority: this.priority,
      status: this.status,
      plannedHours: this.plannedHours,
      actualHours: this.actualHours,
      overtimeHours: this.overtimeHours,
      progress: this.progress
    });
    this.onSave?.(newTask);
    this.controller.close();
  }
}
