// entry/src/main/ets/pages/LonghunAgentPage.ets
// 龍魂 · 智能体协议主页面 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { AgentProfile, AgentType, ProtocolMessage, MessageType, IntentType, AgentTask, TaskPriority, ExecutionStatus, AgentState, agentState, CircuitBreaker } from '../models/AgentProtocol';
import { AgentRegistryDialog } from '../components/AgentRegistryDialog';
import { TaskMonitorDialog } from '../components/TaskMonitorDialog';
import { MessageLogDialog } from '../components/MessageLogDialog';
import { CircuitBreakerPanel } from '../components/CircuitBreakerPanel';
import { IntentInputDialog } from '../components/IntentInputDialog';
import { AgentDatabase } from '../database/AgentDatabase';

const PROTOCOL_VERSION = "1.0.0";
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";

@Entry
@Component
struct LonghunAgentPage {
  @StorageLink('agentState') agentState: AgentState = agentState;
  @State private selectedTab: number = 0;
  @State private showRegistryDialog: boolean = false;
  @State private showTaskDialog: boolean = false;
  @State private showMessageDialog: boolean = false;
  @State private showCircuitDialog: boolean = false;
  @State private showIntentDialog: boolean = false;
  @State private selectedAgent: AgentProfile | null = null;

  aboutToAppear() {
    this.agentState.load();
    AgentDatabase.init();
    this.startHeartbeat();
  }

  build() {
    Column() {
      this.HeaderBuilder()
      this.StatsBuilder()
      this.TabBuilder()
      this.ContentBuilder()
      this.FooterBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉').fontSize(28).margin({ right: 8 })
      Column() {
        Text('龍魂智能体协议').fontSize(20).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text(`UID:${MASTER_UID} · v${PROTOCOL_VERSION}`).fontSize(12).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      Blank()
      Button() {
        Text('🎤').fontSize(20)
      }
      .type(ButtonType.Circle).backgroundColor('#1a1a1a').width(40).height(40)
      .onClick(() => { this.showIntentDialog = true; })
      Button() {
        Text('+').fontSize(24).fontColor('#fff')
      }
      .type(ButtonType.Circle).backgroundColor('#c41e3a').width(40).height(40)
      .onClick(() => { this.showRegistryDialog = true; })
    }
    .width('100%').height(56).padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('智能体', this.agentState.statistics.totalAgents.toString(), '#fff')
      this.StatCard('在线', this.agentState.statistics.onlineAgents.toString(), '#00ff00')
      this.StatCard('任务', this.agentState.statistics.totalTasks.toString(), '#ffcc00')
      this.StatCard('运行中', this.agentState.statistics.runningTasks.toString(), '#0066cc')
      this.StatCard('熔断', this.agentState.statistics.openCircuits.toString(), '#c41e3a')
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

  @Builder
  TabBuilder() {
    Row() {
      ForEach([
        { label: '智能体', icon: '🤖', count: this.agentState.statistics.totalAgents },
        { label: '任务队列', icon: '📋', count: this.agentState.statistics.pendingTasks },
        { label: '消息日志', icon: '📡', count: this.agentState.statistics.totalMessages },
        { label: '熔断器', icon: '⚡', count: this.agentState.statistics.openCircuits }
      ], (item: {label: string, icon: string, count: number}, index: number) => {
        Column() {
          Text(`${item.icon} ${item.label}${item.count > 0 ? `(${item.count})` : ''}`)
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

  @Builder
  ContentBuilder() {
    if (this.selectedTab === 0) { this.AgentListBuilder() }
    else if (this.selectedTab === 1) { this.TaskQueueBuilder() }
    else if (this.selectedTab === 2) { this.MessageLogBuilder() }
    else { this.CircuitBreakerBuilder() }
  }

  @Builder
  AgentListBuilder() {
    List() {
      ForEach(Array.from(this.agentState.agents.values()), (agent: AgentProfile) => {
        ListItem() { this.AgentCardBuilder(agent) }
        .onClick(() => { this.selectedAgent = agent; this.showRegistryDialog = true; })
      }, (agent: AgentProfile) => agent.id)
    }
    .width('100%').layoutWeight(1).divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto).padding({ bottom: 16 })
  }

  @Builder
  AgentCardBuilder(agent: AgentProfile) {
    Row() {
      Column() {
        Text(
          agent.type === AgentType.SYSTEM ? '🔧' :
          agent.type === AgentType.SERVICE ? '⚙️' :
          agent.type === AgentType.DEVICE ? '📱' :
          agent.type === AgentType.EXTERNAL ? '🌐' : '👤'
        ).fontSize(24)
      }
      .width(40).height(40).margin({ right: 12 }).justifyContent(FlexAlign.Center)
      Column() {
        Row() {
          Text(agent.name).fontSize(15).fontWeight(FontWeight.Medium).fontColor('#fff').layoutWeight(1)
          Text(agent.status === 'online' ? '●' : agent.status === 'busy' ? '◐' : '○')
            .fontSize(12).fontColor(agent.status === 'online' ? '#00ff00' : agent.status === 'busy' ? '#ffcc00' : '#666')
        }
        .width('100%')
        Row() {
          Text(`${agent.type} · v${agent.version}`).fontSize(12).fontColor('#888').layoutWeight(1)
          Text(`${agent.capabilities.length}项能力`).fontSize(12).fontColor('#888')
        }
        .width('100%').margin({ top: 4 })
        Row() {
          Text(`📡 ${agent.endpoint || '本地'}`).fontSize(11).fontColor('#666')
          Text(`🔐 ${PermissionLevel[agent.permissionLevel]}`).fontSize(11).fontColor('#666').margin({ left: 8 })
          Blank()
          Text(agent.lastHeartbeat.toLocaleTimeString()).fontSize(11).fontColor('#666')
        }
        .width('100%').margin({ top: 4 })
      }
      .layoutWeight(1).alignItems(HorizontalAlign.Start)
    }
    .width('100%').padding(16).backgroundColor('#0a0a0a').borderRadius(8)
    .margin({ left: 12, right: 12, top: 8 })
  }

  @Builder
  TaskQueueBuilder() {
    List() {
      if (this.agentState.runningTasks.size > 0) {
        ListItem() {
          Text(`▶️ 运行中 (${this.agentState.runningTasks.size})`).fontSize(14).fontWeight(FontWeight.Bold).fontColor('#0066cc').padding({ left: 16, top: 12, bottom: 8 })
        }
        .width('100%').backgroundColor('#1a1a1a')
      }
      ForEach(Array.from(this.agentState.runningTasks.values()), (task: AgentTask) => {
        ListItem() { this.TaskCardBuilder(task) }
      }, (task: AgentTask) => `run-${task.id}`)
      if (this.agentState.taskQueue.length > 0) {
        ListItem() {
          Text(`⏳ 待执行 (${this.agentState.taskQueue.length})`).fontSize(14).fontWeight(FontWeight.Bold).fontColor('#ffcc00').padding({ left: 16, top: 12, bottom: 8 })
        }
        .width('100%').backgroundColor('#1a1a1a')
      }
      ForEach(this.agentState.taskQueue, (task: AgentTask) => {
        ListItem() { this.TaskCardBuilder(task) }
      }, (task: AgentTask) => `queue-${task.id}`)
    }
    .width('100%').layoutWeight(1).divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto).padding({ bottom: 16 })
  }

  @Builder
  TaskCardBuilder(task: AgentTask) {
    Row() {
      Column() {
        Text(
          task.status === ExecutionStatus.RUNNING ? '▶️' :
          task.status === ExecutionStatus.PENDING ? '⏳' :
          task.status === ExecutionStatus.COMPLETED ? '✅' :
          task.status === ExecutionStatus.FAILED ? '❌' : '⏹️'
        ).fontSize(24)
      }
      .width(40).height(40).margin({ right: 12 }).justifyContent(FlexAlign.Center)
      Column() {
        Row() {
          Text(task.action).fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').layoutWeight(1)
          Text(`P${task.priority}`).fontSize(11).fontColor(
            task.priority === 0 ? '#ff0000' : task.priority === 1 ? '#ff6600' : task.priority === 2 ? '#ffcc00' : '#888'
          ).backgroundColor('rgba(255,255,255,0.05)').borderRadius(4).padding({ left: 6, right: 6 })
        }
        .width('100%')
        Row() {
          Text(task.id.substring(0, 8)).fontSize(11).fontColor('#666').layoutWeight(1)
          Text(`${task.progress}%`).fontSize(11).fontColor('#888')
        }
        .width('100%').margin({ top: 4 })
        if (task.status === ExecutionStatus.RUNNING) {
          Stack() {
            Row().width('100%').height(4).backgroundColor('#333').borderRadius(2)
            Row().width(`${task.progress}%`).height(4).backgroundColor('#0066cc').borderRadius(2)
          }
          .width('100%').height(4).margin({ top: 6 })
        }
      }
      .layoutWeight(1).alignItems(HorizontalAlign.Start)
    }
    .width('100%').padding(16).backgroundColor('#0a0a0a').borderRadius(8)
    .margin({ left: 12, right: 12, top: 8 })
  }

  @Builder
  MessageLogBuilder() {
    List() {
      ForEach(this.agentState.messageLog.slice(-50).reverse(), (msg: ProtocolMessage) => {
        ListItem() {
          Row() {
            Text(
              msg.type === MessageType.REGISTER ? '📥' :
              msg.type === MessageType.INTENT ? '🎤' :
              msg.type === MessageType.TASK ? '📋' :
              msg.type === MessageType.RESULT ? '✅' :
              msg.type === MessageType.ERROR ? '❌' :
              msg.type === MessageType.HEARTBEAT ? '💓' :
              msg.type === MessageType.AUDIT ? '📝' : '📡'
            ).fontSize(18)
            Column() {
              Text(`${msg.type.toUpperCase()} · ${msg.id.substring(0, 12)}`).fontSize(12).fontColor('#fff')
              Text(`${msg.from} → ${msg.to}`).fontSize(11).fontColor('#666')
            }
            .alignItems(HorizontalAlign.Start).layoutWeight(1).margin({ left: 12 })
            Text(new Date(msg.timestamp).toLocaleTimeString()).fontSize(11).fontColor('#666')
          }
          .width('100%').padding(12)
        }
      }, (msg: ProtocolMessage) => msg.id)
    }
    .width('100%').layoutWeight(1).divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto).padding({ bottom: 16 })
  }

  @Builder
  CircuitBreakerBuilder() {
    List() {
      ForEach(Array.from(this.agentState.circuitBreakers.values()), (cb: CircuitBreaker) => {
        ListItem() {
          Row() {
            Column() {
              Text(
                cb.state === 'closed' ? '✅' : cb.state === 'open' ? '❌' : '⚠️'
              ).fontSize(24)
            }
            .width(40).height(40).margin({ right: 12 }).justifyContent(FlexAlign.Center)
            Column() {
              Row() {
                Text(cb.name).fontSize(15).fontWeight(FontWeight.Medium).fontColor('#fff').layoutWeight(1)
                Text(cb.getStatus()).fontSize(11).fontColor(
                  cb.state === 'closed' ? '#00ff00' : cb.state === 'open' ? '#ff0000' : '#ffcc00'
                ).backgroundColor(
                  cb.state === 'closed' ? 'rgba(0,255,0,0.1)' : cb.state === 'open' ? 'rgba(255,0,0,0.1)' : 'rgba(255,204,0,0.1)'
                ).borderRadius(4).padding({ left: 8, right: 8, top: 2, bottom: 2 })
              }
              .width('100%')
              Row() {
                Text(`目标: ${cb.target}`).fontSize(12).fontColor('#888').layoutWeight(1)
                Text(`${cb.totalCalls}次调用`).fontSize(12).fontColor('#888')
              }
              .width('100%').margin({ top: 4 })
              Row() {
                Text(`✅ ${cb.totalSuccesses} · ❌ ${cb.totalFailures} · 失败率 ${cb.totalCalls > 0 ? Math.round((cb.totalFailures / cb.totalCalls) * 100) : 0}%`)
                  .fontSize(11).fontColor('#666')
              }
              .width('100%').margin({ top: 4 })
            }
            .layoutWeight(1).alignItems(HorizontalAlign.Start)
          }
          .width('100%').padding(16).backgroundColor('#0a0a0a').borderRadius(8)
          .margin({ left: 12, right: 12, top: 8 })
        }
      }, (cb: CircuitBreaker) => cb.id)
    }
    .width('100%').layoutWeight(1).divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto).padding({ bottom: 16 })
  }

  @Builder
  FooterBuilder() {
    Row() {
      Column() {
        Text('🐉').fontSize(20)
        Text(`UID:${MASTER_UID}`).fontSize(10).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start).layoutWeight(1)
      Row() {
        Button() { Text('📋 任务').fontSize(12).fontColor('#fff') }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12, top: 6, bottom: 6 }).margin({ right: 8 })
        .onClick(() => { this.showTaskDialog = true; })
        Button() { Text('📡 日志').fontSize(12).fontColor('#fff') }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12, top: 6, bottom: 6 }).margin({ right: 8 })
        .onClick(() => { this.showMessageDialog = true; })
        Button() { Text('⚡ 熔断').fontSize(12).fontColor('#fff') }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12, top: 6, bottom: 6 }).margin({ right: 8 })
        .onClick(() => { this.showCircuitDialog = true; })
        Button() { Text('🎤 意图').fontSize(12).fontColor('#fff') }
        .type(ButtonType.Normal).backgroundColor('#c41e3a').borderRadius(8).padding({ left: 12, right: 12, top: 6, bottom: 6 })
        .onClick(() => { this.showIntentDialog = true; })
      }
    }
    .width('100%').height(56).padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }

  startHeartbeat(): void {
    console.info('[龍魂] 智能体心跳系统已启动');
  }
}
