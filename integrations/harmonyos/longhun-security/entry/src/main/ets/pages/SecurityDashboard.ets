// entry/src/main/ets/pages/SecurityDashboard.ets
// 龍魂 · 智慧安防控制台
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { securityState, SecurityState, ProcessStatus, ThreatLevel, PerceptionType, PerceptionData } from '../models/SecurityModel';
import { processGuardian } from '../services/ProcessGuardian';
import { taskScheduler } from '../services/TaskScheduler';
import { trajectoryLinker } from '../services/TrajectoryLinker';
import { globalPerception } from '../services/GlobalPerception';

const MASTER_UID = "9622";

@Entry
@Component
struct SecurityDashboardPage {
  @StorageLink('securityState') securityState: SecurityState = securityState;
  @State private selectedTab: number = 0;
  @State private refreshTimer: number = 0;

  private tabs = [
    { label: '进程', icon: '⚙️' },
    { label: '任务', icon: '⏰' },
    { label: '轨迹', icon: '📍' },
    { label: '感知', icon: '👁️' },
    { label: '告警', icon: '🚨' }
  ];

  aboutToAppear() {
    this.startAutoRefresh();

    processGuardian.registerProcess('龍魂安防主进程', 1001);
    processGuardian.registerProcess('龍魂感知采集', 1002);
    processGuardian.registerProcess('龍魂数据同步', 1003);

    taskScheduler.registerHandler('heartbeatCheck', () => {
      processGuardian.getAllProcesses().forEach(p => {
        processGuardian.heartbeat(p.name, Math.random() * 200, Math.random() * 30);
      });
    });

    taskScheduler.addTask({
      name: '心跳检测',
      type: 'periodic',
      cronExpression: '*/5 * * * *',
      handler: 'heartbeatCheck',
      isEnabled: true
    });

    globalPerception.enableSensor(PerceptionType.MOTION);
    globalPerception.enableSensor(PerceptionType.SOUND);
    globalPerception.enableSensor(PerceptionType.TEMPERATURE);
  }

  aboutToDisappear() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
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
        Text('龍魂智慧安防').fontSize(20).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text(`UID:${MASTER_UID} · 全域感知系统`).fontSize(12).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Row() {
        Circle()
          .width(12)
          .height(12)
          .fill(this.getSystemStatusColor())
          .shadow({ radius: 4, color: this.getSystemStatusColor() })
      }
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('进程', `${this.securityState.statistics.healthyProcesses}/${this.securityState.statistics.totalProcesses}`, this.getProcessColor())
      this.StatCard('任务', `${this.securityState.statistics.activeTasks}`, '#00ff00')
      this.StatCard('轨迹', `${this.securityState.statistics.totalTrajectories}`, '#88ff00')
      this.StatCard('感知', `${this.securityState.statistics.totalPerceptions}`, '#ffcc00')
      this.StatCard('告警', `${this.securityState.statistics.criticalAlerts}`, this.getAlertColor())
    }
    .width('100%')
    .height(80)
    .padding({ left: 12, right: 12, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() {
      Text(value).fontSize(20).fontWeight(FontWeight.Bold).fontColor(color)
      Text(label).fontSize(11).fontColor('#666').margin({ top: 4 })
    }
    .width('20%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }

  @Builder
  TabBuilder() {
    Row() {
      ForEach(this.tabs, (tab, index) => {
        Column() {
          Text(`${tab.icon} ${tab.label}`)
            .fontSize(13)
            .fontWeight(this.selectedTab === index ? FontWeight.Bold : FontWeight.Normal)
            .fontColor(this.selectedTab === index ? '#c41e3a' : '#888')
          if (this.selectedTab === index) {
            Divider()
              .strokeWidth(2)
              .color('#c41e3a')
              .width(20)
              .margin({ top: 4 })
          }
        }
        .padding({ top: 12, bottom: 12, left: 16, right: 16 })
        .onClick(() => { this.selectedTab = index; })
      })
    }
    .width('100%')
    .justifyContent(FlexAlign.SpaceAround)
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  ContentBuilder() {
    if (this.selectedTab === 0) { this.ProcessTabBuilder() }
    else if (this.selectedTab === 1) { this.TaskTabBuilder() }
    else if (this.selectedTab === 2) { this.TrajectoryTabBuilder() }
    else if (this.selectedTab === 3) { this.PerceptionTabBuilder() }
    else { this.AlertTabBuilder() }
  }

  @Builder
  ProcessTabBuilder() {
    List() {
      ForEach(processGuardian.getAllProcesses(), (proc) => {
        ListItem() {
          Row() {
            Column() {
              Text(proc.name).fontSize(14).fontColor('#fff').fontWeight(FontWeight.Medium)
              Text(`PID:${proc.pid} · 重启:${proc.restartCount}次`)
                .fontSize(11).fontColor('#666').margin({ top: 4 })
            }
            .alignItems(HorizontalAlign.Start).layoutWeight(1)

            Column() {
              Text(proc.status)
                .fontSize(12)
                .fontColor(proc.isHealthy() ? '#00ff00' : '#ff0000')
                .backgroundColor('rgba(255,255,255,0.05)')
                .borderRadius(4)
                .padding({ left: 8, right: 8, top: 2, bottom: 2 })
              Text(`${proc.memoryUsage.toFixed(0)}MB · ${proc.cpuUsage.toFixed(1)}%`)
                .fontSize(11).fontColor('#888').margin({ top: 4 })
            }
            .alignItems(HorizontalAlign.End)
          }
          .width('100%').padding(12)
          .backgroundColor('#1a1a1a').borderRadius(8).margin({ bottom: 8 })
        }
      })
    }
    .width('100%').padding(12).layoutWeight(1)
  }

  @Builder
  TaskTabBuilder() {
    List() {
      ForEach(taskScheduler.getAllTasks(), (task) => {
        ListItem() {
          Row() {
            Column() {
              Text(task.name).fontSize(14).fontColor('#fff').fontWeight(FontWeight.Medium)
              Text(`${task.cronExpression} · 成功:${task.successCount} 失败:${task.failCount}`)
                .fontSize(11).fontColor('#666').margin({ top: 4 })
            }
            .alignItems(HorizontalAlign.Start).layoutWeight(1)

            Column() {
              Text(task.isEnabled ? '运行中' : '已停止')
                .fontSize(12)
                .fontColor(task.isEnabled ? '#00ff00' : '#666')
                .backgroundColor('rgba(255,255,255,0.05)')
                .borderRadius(4)
                .padding({ left: 8, right: 8, top: 2, bottom: 2 })
              Text(`下次: ${new Date(task.nextTriggerTime).toLocaleTimeString()}`)
                .fontSize(11).fontColor('#888').margin({ top: 4 })
            }
            .alignItems(HorizontalAlign.End)
          }
          .width('100%').padding(12)
          .backgroundColor('#1a1a1a').borderRadius(8).margin({ bottom: 8 })
        }
      })
    }
    .width('100%').padding(12).layoutWeight(1)
  }

  @Builder
  TrajectoryTabBuilder() {
    Column() {
      Column() {
        Text('轨迹可视化区域').fontSize(14).fontColor('#666')
        Text('(实际实现：Canvas绘制轨迹)').fontSize(12).fontColor('#444')
      }
      .width('100%').height(200)
      .backgroundColor('#1a1a1a').borderRadius(8)
      .justifyContent(FlexAlign.Center).margin({ bottom: 12 })

      List() {
        ForEach(trajectoryLinker.getTrajectoryKeys(), (id) => {
          ListItem() {
            Row() {
              Text(`轨迹 ${id}`).fontSize(14).fontColor('#fff').layoutWeight(1)
              const stats = trajectoryLinker.getStats(id);
              Text(`${stats.totalPoints}点 · ${(stats.distance / 1000).toFixed(2)}km`)
                .fontSize(12).fontColor('#888')
            }
            .width('100%').padding(12)
            .backgroundColor('#1a1a1a').borderRadius(8).margin({ bottom: 8 })
          }
        })
      }
      .width('100%').layoutWeight(1)
    }
    .width('100%').padding(12).layoutWeight(1)
  }

  @Builder
  PerceptionTabBuilder() {
    Column() {
      Row() {
        ForEach(globalPerception.getActiveSensors(), (sensor) => {
          Column() {
            Text(this.getSensorIcon(sensor)).fontSize(20)
            Text(sensor).fontSize(10).fontColor('#00ff00').margin({ top: 4 })
          }
          .width('20%').padding(8)
          .backgroundColor('#1a1a1a').borderRadius(8).margin({ right: 8 })
        })
      }
      .width('100%').margin({ bottom: 12 })

      List() {
        ForEach(globalPerception.getHistory(undefined, 20), (data) => {
          ListItem() {
            Row() {
              Text(data.type).fontSize(13).fontColor('#fff').layoutWeight(1)
              Text(`${data.value.toFixed(1)}${data.unit}`)
                .fontSize(13).fontColor(data.getThreatColor())
              Text(data.threatLevel)
                .fontSize(11).fontColor(data.getThreatColor())
                .backgroundColor('rgba(255,255,255,0.05)')
                .borderRadius(4)
                .padding({ left: 6, right: 6 }).margin({ left: 8 })
            }
            .width('100%').padding(10)
            .backgroundColor('#1a1a1a').borderRadius(8).margin({ bottom: 6 })
          }
        })
      }
      .width('100%').layoutWeight(1)
    }
    .width('100%').padding(12).layoutWeight(1)
  }

  @Builder
  AlertTabBuilder() {
    List() {
      ForEach(this.securityState.alerts, (alert) => {
        ListItem() {
          Row() {
            Column() {
              Text(alert.message).fontSize(14).fontColor('#fff').fontWeight(FontWeight.Medium)
              Text(new Date(alert.timestamp).toLocaleString())
                .fontSize(11).fontColor('#666').margin({ top: 4 })
            }
            .alignItems(HorizontalAlign.Start).layoutWeight(1)

            Text(alert.level)
              .fontSize(12)
              .fontColor(this.getThreatColor(alert.level))
              .backgroundColor('rgba(255,255,255,0.05)')
              .borderRadius(4)
              .padding({ left: 8, right: 8, top: 2, bottom: 2 })
          }
          .width('100%').padding(12)
          .backgroundColor('#1a1a1a').borderRadius(8).margin({ bottom: 8 })
        }
      })
    }
    .width('100%').padding(12).layoutWeight(1)
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
        Text(`⚙️ ${this.securityState.statistics.healthyProcesses} 进程`).fontSize(11).fontColor('#888')
        Text(`⏰ ${this.securityState.statistics.activeTasks} 任务`).fontSize(11).fontColor('#888').margin({ left: 8 })
        Text(`👁️ ${globalPerception.getActiveSensors().length} 传感器`).fontSize(11).fontColor('#888').margin({ left: 8 })
      }
    }
    .width('100%').height(40).padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a').border({ width: { top: 1 }, color: '#333' })
  }

  private startAutoRefresh(): void {
    this.refreshTimer = setInterval(() => {
      this.simulateDataUpdate();
    }, 3000);
  }

  private simulateDataUpdate(): void {
    const sensors = [
      { type: PerceptionType.MOTION, value: Math.random() * 100, unit: '' },
      { type: PerceptionType.SOUND, value: 40 + Math.random() * 60, unit: 'dB' },
      { type: PerceptionType.TEMPERATURE, value: 20 + Math.random() * 20, unit: '°C' }
    ];

    sensors.forEach(s => {
      globalPerception.receiveData({
        type: s.type,
        value: s.value,
        unit: s.unit,
        location: '主控室',
        timestamp: Date.now()
      } as PerceptionData);
    });
  }

  private getSystemStatusColor(): string {
    const healthy = this.securityState.statistics.healthyProcesses;
    const total = this.securityState.statistics.totalProcesses;
    if (healthy === total) return '#00ff00';
    if (healthy > total / 2) return '#ffcc00';
    return '#ff0000';
  }

  private getProcessColor(): string {
    const ratio = this.securityState.statistics.healthyProcesses /
                  Math.max(this.securityState.statistics.totalProcesses, 1);
    if (ratio >= 1) return '#00ff00';
    if (ratio >= 0.7) return '#88ff00';
    if (ratio >= 0.4) return '#ffcc00';
    return '#ff0000';
  }

  private getAlertColor(): string {
    const critical = this.securityState.statistics.criticalAlerts;
    if (critical === 0) return '#00ff00';
    if (critical < 3) return '#ffcc00';
    return '#ff0000';
  }

  private getThreatColor(level: string): string {
    switch (level) {
      case 'none': return '#00ff00';
      case 'low': return '#88ff00';
      case 'medium': return '#ffcc00';
      case 'high': return '#ff6600';
      case 'critical': return '#ff0000';
      default: return '#666';
    }
  }

  private getSensorIcon(type: string): string {
    const icons: Map<string, string> = new Map([
      ['motion', '🏃'],
      ['sound', '🔊'],
      ['temperature', '🌡️'],
      ['humidity', '💧'],
      ['light', '💡'],
      ['camera', '📹'],
      ['location', '📍']
    ]);
    return icons.get(type) || '👁️';
  }
}
