// entry/src/main/ets/components/TaskMonitorDialog.ets
// 龍魂 · 任务监控弹窗 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { AgentTask, ExecutionStatus, TaskPriority, AgentState, agentState, AgentProfile } from '../models/AgentProtocol';

@CustomDialog
export struct TaskMonitorDialog {
  controller: CustomDialogController;
  @StorageLink('agentState') agentState: AgentState = agentState;
  @State private selectedSubTab: number = 0;

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('📋 任务监控')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
        Blank()
        Button() { Text('✕').fontSize(18).fontColor('#888') }
          .type(ButtonType.Normal).backgroundColor(Color.Transparent)
          .onClick(() => { this.controller.close(); })
      }
      .width('100%').padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      // 统计概览
      Row() {
        this.TaskStatCard('运行中', this.agentState.runningTasks.size, '#0066cc')
        this.TaskStatCard('等待中', this.agentState.taskQueue.length, '#ffcc00')
        this.TaskStatCard('已完成', this.agentState.completedTasks.filter(t => t.status === ExecutionStatus.COMPLETED).length, '#00ff00')
        this.TaskStatCard('失败', this.agentState.completedTasks.filter(t => t.status === ExecutionStatus.FAILED).length, '#ff0000')
        this.TaskStatCard('平均耗时', `${this.agentState.statistics.avgExecutionTime}ms`, '#888')
      }
      .width('100%').padding(12)
      .backgroundColor('#0a0a0a')

      // 子标签
      Row() {
        ForEach(['运行中', '等待中', '已完成', '全部'], (label: string, index: number) => {
          Text(label)
            .fontSize(13)
            .fontWeight(this.selectedSubTab === index ? FontWeight.Bold : FontWeight.Normal)
            .fontColor(this.selectedSubTab === index ? '#c41e3a' : '#888')
            .padding({ left: 16, right: 16, top: 8, bottom: 8 })
            .onClick(() => { this.selectedSubTab = index; })
        })
      }
      .width('100%').backgroundColor('#1a1a1a')
      .border({ width: { bottom: 1 }, color: '#333' })

      // 任务列表
      Scroll() {
        Column() {
          if (this.selectedSubTab === 0 || this.selectedSubTab === 3) {
            ForEach(Array.from(this.agentState.runningTasks.values()), (task: AgentTask) => {
              this.TaskDetailCard(task)
            }, (task: AgentTask) => `run-${task.id}`)
          }
          if (this.selectedSubTab === 1 || this.selectedSubTab === 3) {
            ForEach(this.agentState.taskQueue, (task: AgentTask) => {
              this.TaskDetailCard(task)
            }, (task: AgentTask) => `queue-${task.id}`)
          }
          if (this.selectedSubTab === 2 || this.selectedSubTab === 3) {
            ForEach(this.agentState.completedTasks.slice(-20).reverse(), (task: AgentTask) => {
              this.TaskDetailCard(task)
            }, (task: AgentTask) => `completed-${task.id}`)
          }
        }
        .padding(12)
      }
      .layoutWeight(1)
      .scrollBar(BarState.Auto)

      // 新建任务
      Row() {
        Button() {
          Text('+ 新建任务').fontSize(14).fontColor('#fff')
        }
        .type(ButtonType.Normal).backgroundColor('#c41e3a').borderRadius(8)
        .padding({ left: 24, right: 24, top: 10, bottom: 10 })
        .onClick(() => { this.createQuickTask(); })
      }
      .width('100%').padding(12).justifyContent(FlexAlign.Center)
      .border({ width: { top: 1 }, color: '#333' })
    }
    .width('95%').height('85%')
    .backgroundColor('#1a1a1a')
    .borderRadius(12)
  }

  @Builder
  TaskStatCard(label: string, value: number | string, color: string) {
    Column() {
      Text(value.toString())
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
        .fontColor(color)
      Text(label)
        .fontSize(10)
        .fontColor('#666')
        .margin({ top: 2 })
    }
    .width('20%')
    .alignItems(HorizontalAlign.Center)
  }

  @Builder
  TaskDetailCard(task: AgentTask) {
    Column() {
      Row() {
        Text(
          task.status === ExecutionStatus.RUNNING ? '▶️' :
          task.status === ExecutionStatus.PENDING ? '⏳' :
          task.status === ExecutionStatus.COMPLETED ? '✅' :
          task.status === ExecutionStatus.FAILED ? '❌' : '⏹️'
        ).fontSize(20).margin({ right: 8 })
        Column() {
          Text(task.action || '未命名任务')
            .fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff')
          Text(`${task.id.substring(0, 16)} · P${task.priority}`)
            .fontSize(11).fontColor('#666')
        }
        .alignItems(HorizontalAlign.Start).layoutWeight(1)
        Column() {
          if (task.status === ExecutionStatus.RUNNING) {
            Text(`${task.progress}%`).fontSize(16).fontWeight(FontWeight.Bold).fontColor('#0066cc')
          } else if (task.status === ExecutionStatus.FAILED) {
            Button('重试').fontSize(11).height(28)
              .backgroundColor('#333').borderRadius(4)
              .onClick(() => {
                const retry = new AgentTask({
                  action: task.action,
                  params: task.params,
                  priority: task.priority
                });
                this.agentState.submitTask(retry);
              })
          }
        }
        .alignItems(HorizontalAlign.End)
      }
      .width('100%')

      if (task.status === ExecutionStatus.RUNNING) {
        Row() {
          Stack() {
            Row().width('100%').height(4).backgroundColor('#333').borderRadius(2)
            Row().width(`${task.progress}%`).height(4).backgroundColor('#0066cc').borderRadius(2)
          }
          .width('100%').height(4)
        }
        .width('100%').margin({ top: 8 })
      }

      if (task.error) {
        Text(`错误: ${task.error}`)
          .fontSize(11).fontColor('#ff0000').margin({ top: 8 })
      }
    }
    .width('100%').padding(12)
    .backgroundColor('#0a0a0a').borderRadius(8)
    .margin({ bottom: 8 })
  }

  createQuickTask(): void {
    const task = new AgentTask({
      action: '新任务',
      params: {},
      priority: TaskPriority.NORMAL,
      status: ExecutionStatus.PENDING
    });
    this.agentState.submitTask(task);
    console.info('[龍魂] 新建任务:', task.id);
  }
}
