// pages/EthicalDefensePage.ets
// 龍魂 · 伦理防御控制台
// 可视化守护场状态 · 目标列表 · 干扰日志 · 熔断控制
// DNA: #龍芯⚡️丙午·辛未·丙戌·ETHICAL-DEFENSE-PAGE-v1.0

import { ethicalPerception, TargetProfile, TargetType } from '../engines/EthicalPerception';
import { interferenceEngine, InterferenceType, InterferenceIntensity } from '../engines/InterferenceEngine';
import { ethicalCircuitBreaker, BreakerLevel, BreakerTrigger } from '../services/EthicalCircuitBreaker';
import { ThreatLevel } from '../models/SecurityModel';

@Entry
@Component
struct EthicalDefensePage {
  @State detectedTargets: TargetProfile[] = [];
  @State activeInterferences: number = 0;
  @State totalBreakers: number = 0;
  @State pendingReviews: number = 0;
  @State isBreakerEnabled: boolean = true;
  @State chipAuthorized: boolean = false;
  @State selectedTarget: TargetProfile | null = null;
  @State showDetailDialog: boolean = false;
  @State refreshTimer: number = 0;

  // 定时刷新
  private refreshInterval: number = 3000;

  aboutToAppear(): void {
    this.refreshData();
    this.refreshTimer = setInterval(() => {
      this.refreshData();
    }, this.refreshInterval);

    // 检查芯片授权
    this.chipAuthorized = ethicalPerception.isChipAuthorized();
  }

  aboutToDisappear(): void {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
  }

  refreshData(): void {
    this.detectedTargets = ethicalPerception.getDetectedTargets();
    this.activeInterferences = interferenceEngine.getActiveCount();
    this.totalBreakers = ethicalCircuitBreaker.getStats().totalTriggers;
    this.pendingReviews = ethicalCircuitBreaker.getPendingReviews().length;
    this.isBreakerEnabled = ethicalCircuitBreaker.isEnabled();
  }

  build() {
    Column() {
      // 顶栏
      this.buildHeader();

      // 芯片授权状态
      if (!this.chipAuthorized) {
        this.buildChipWarning();
      }

      // 统计概览
      this.buildStatsOverview();

      // 目标列表
      this.buildTargetList();

      // 干扰日志
      this.buildInterferenceLog();

      // 熔断历史
      this.buildBreakerHistory();
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  // ================================================================
  // 顶栏
  // ================================================================
  @Builder
  buildHeader() {
    Row() {
      Text('⚖️')
        .fontSize(24)
        .margin({ right: 8 })

      Column() {
        Text('龍魂 · 伦理防御')
          .fontSize(18)
          .fontColor('#FFD700')
          .fontWeight(FontWeight.Bold)

        Text('Guardian Field · Non-Lethal Interference')
          .fontSize(10)
          .fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)

      Blank()

      // 熔断器开关
      Toggle({ type: ToggleType.Switch, isOn: this.isBreakerEnabled })
        .onChange((isOn: boolean) => {
          ethicalCircuitBreaker.setEnabled(isOn);
          this.isBreakerEnabled = isOn;
        })
        .selectedColor('#FFD700')
    }
    .width('100%')
    .padding({ left: 16, right: 16, top: 12, bottom: 12 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // ================================================================
  // 芯片未授权警告
  // ================================================================
  @Builder
  buildChipWarning() {
    Row() {
      Text('⚠️ 当前芯片未授权 · 伦理防御已禁用')
        .fontSize(13)
        .fontColor('#ff4444')
        .fontWeight(FontWeight.Bold)

      Text('仅支持中国芯片: 麒麟/昇腾/鲲鹏/龙芯/飞腾/展锐')
        .fontSize(11)
        .fontColor('#888')
        .margin({ left: 8 })
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#1a0000')
    .border({ width: 1, color: '#ff4444', radius: 4 })
    .margin(12)
  }

  // ================================================================
  // 统计概览
  // ================================================================
  @Builder
  buildStatsOverview() {
    Row() {
      this.buildStatCard('检测目标', `${this.detectedTargets.length}`, '#4a9eff')
      this.buildStatCard('活跃干扰', `${this.activeInterferences}`, this.activeInterferences > 0 ? '#ff6b35' : '#666')
      this.buildStatCard('熔断次数', `${this.totalBreakers}`, this.totalBreakers > 0 ? '#c41e3a' : '#666')
      this.buildStatCard('待审核', `${this.pendingReviews}`, this.pendingReviews > 0 ? '#ffd700' : '#666')
    }
    .width('100%')
    .padding(12)
    .justifyContent(FlexAlign.SpaceEvenly)
  }

  @Builder
  buildStatCard(label: string, value: string, color: string) {
    Column() {
      Text(value)
        .fontSize(28)
        .fontColor(color)
        .fontWeight(FontWeight.Bold)

      Text(label)
        .fontSize(11)
        .fontColor('#888')
        .margin({ top: 4 })
    }
    .padding(12)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .width('22%')
  }

  // ================================================================
  // 目标列表
  // ================================================================
  @Builder
  buildTargetList() {
    Column() {
      Row() {
        Text('📡 检测目标')
          .fontSize(14)
          .fontColor('#fff')
          .fontWeight(FontWeight.Bold)

        Blank()

        Text(`${this.detectedTargets.length} 个`)
          .fontSize(12)
          .fontColor('#888')
      }
      .width('100%')
      .padding({ left: 12, right: 12, top: 8, bottom: 4 })

      if (this.detectedTargets.length === 0) {
        Text('未检测到目标设备')
          .fontSize(13)
          .fontColor('#555')
          .padding(20)
          .width('100%')
          .textAlign(TextAlign.Center)
      } else {
        List() {
          ForEach(this.detectedTargets, (target: TargetProfile) => {
            ListItem() {
              this.buildTargetCard(target)
            }
          })
        }
        .width('100%')
        .height(220)
      }
    }
    .margin({ left: 12, right: 12, bottom: 8 })
    .backgroundColor('#111')
    .borderRadius(8)
  }

  @Builder
  buildTargetCard(target: TargetProfile) {
    Row() {
      // 类型图标
      Text(this.getTargetIcon(target.type))
        .fontSize(20)
        .margin({ right: 8 })

      Column() {
        Row() {
          Text(target.id.length > 20 ? target.id.substring(0, 20) + '...' : target.id)
            .fontSize(13)
            .fontColor('#fff')
            .fontWeight(FontWeight.Medium)

          if (target.ethicalChipSignature) {
            Text('✓芯片')
              .fontSize(10)
              .fontColor('#00ff00')
              .backgroundColor('rgba(0,255,0,0.1)')
              .borderRadius(4)
              .padding({ left: 4, right: 4 })
              .margin({ left: 6 })
          } else if (target.type !== TargetType.HUMAN) {
            Text('✗无签名')
              .fontSize(10)
              .fontColor('#ff4444')
              .backgroundColor('rgba(255,0,0,0.1)')
              .borderRadius(4)
              .padding({ left: 4, right: 4 })
              .margin({ left: 6 })
          }
        }

        Row() {
          Text(`${target.type}`)
            .fontSize(10)
            .fontColor('#888')

          Text(`· ${(target.confidence * 100).toFixed(0)}%`)
            .fontSize(10)
            .fontColor('#666')
            .margin({ left: 4 })
        }
        .margin({ top: 2 })
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Column() {
        // 威胁等级
        Text(this.getThreatLabel(target.threatLevel))
          .fontSize(10)
          .fontColor(this.getThreatColor(target.threatLevel))
          .backgroundColor('rgba(255,255,255,0.05)')
          .borderRadius(4)
          .padding({ left: 6, right: 6, top: 2, bottom: 2 })
          .margin({ bottom: 4 })

        // 熔断按钮
        if (target.type !== TargetType.HUMAN && target.type !== TargetType.ROBOT_ETHICAL) {
          Button('干扰')
            .fontSize(10)
            .fontColor('#fff')
            .backgroundColor(this.isBreakerEnabled ? '#c41e3a' : '#444')
            .borderRadius(4)
            .padding({ left: 8, right: 8, top: 2, bottom: 2 })
            .enabled(this.isBreakerEnabled)
            .onClick(() => {
              this.triggerManualBreaker(target);
            })
        }
      }
      .alignItems(HorizontalAlign.End)
    }
    .width('100%')
    .padding(10)
    .backgroundColor('#1a1a1a')
    .borderRadius(6)
    .margin({ bottom: 4, left: 8, right: 8 })
  }

  // ================================================================
  // 干扰日志
  // ================================================================
  @Builder
  buildInterferenceLog() {
    Column() {
      Row() {
        Text('🛡️ 干扰日志')
          .fontSize(14)
          .fontColor('#fff')
          .fontWeight(FontWeight.Bold)

        Blank()

        if (this.activeInterferences > 0) {
          Text(`● ${this.activeInterferences} 活跃`)
            .fontSize(11)
            .fontColor('#ff6b35')
        }
      }
      .width('100%')
      .padding({ left: 12, right: 12, top: 8, bottom: 4 })

      List() {
        ForEach(interferenceEngine.getRecentInterferenceLog(5), (log) => {
          ListItem() {
            Row() {
              Text(this.getInterferenceIcon(log.type))
                .fontSize(14)
                .margin({ right: 6 })

              Column() {
                Text(`${log.type}`)
                  .fontSize(12)
                  .fontColor('#c41e3a')

                Text(`${log.targetId.substring(0, 16)}...`)
                  .fontSize(10)
                  .fontColor('#555')
              }
              .alignItems(HorizontalAlign.Start)
              .layoutWeight(1)

              Column() {
                Text(log.intensity)
                  .fontSize(10)
                  .fontColor('#666')

                Text(new Date(log.startTime).toLocaleTimeString())
                  .fontSize(9)
                  .fontColor('#444')
              }
              .alignItems(HorizontalAlign.End)
            }
            .width('100%')
            .padding(8)
            .backgroundColor('#1a1a1a')
            .borderRadius(4)
            .margin({ bottom: 2, left: 8, right: 8 })
          }
        })
      }
      .width('100%')
      .height(120)
    }
    .margin({ left: 12, right: 12, bottom: 8 })
    .backgroundColor('#111')
    .borderRadius(8)
  }

  // ================================================================
  // 熔断历史
  // ================================================================
  @Builder
  buildBreakerHistory() {
    Column() {
      Text('⚡ 熔断历史')
        .fontSize(14)
        .fontColor('#fff')
        .fontWeight(FontWeight.Bold)
        .width('100%')
        .padding({ left: 12, right: 12, top: 8, bottom: 4 })

      List() {
        ForEach(ethicalCircuitBreaker.getBreakerHistory().slice(0, 5), (record) => {
          ListItem() {
            Row() {
              Text(this.getBreakerLevelIcon(record.level as BreakerLevel))
                .fontSize(16)
                .margin({ right: 8 })

              Column() {
                Text(`${record.targetId.substring(0, 20)}...`)
                  .fontSize(12)
                  .fontColor('#fff')

                Text(`${record.triggerReasons.join(', ')}`)
                  .fontSize(10)
                  .fontColor('#888')
                  .maxLines(1)
              }
              .layoutWeight(1)

              Text(new Date(record.timestamp).toLocaleTimeString())
                .fontSize(10)
                .fontColor('#444')
            }
            .width('100%')
            .padding(8)
            .backgroundColor('#1a1a1a')
            .borderRadius(4)
            .margin({ bottom: 2, left: 8, right: 8 })
          }
        })
      }
      .width('100%')
      .height(120)
    }
    .margin({ left: 12, right: 12, bottom: 12 })
    .backgroundColor('#111')
    .borderRadius(8)
  }

  // ================================================================
  // 手动触发熔断
  // ================================================================
  private async triggerManualBreaker(target: TargetProfile): Promise<void> {
    console.info(`[龍魂·伦理] 手动触发熔断: ${target.id}`);
    const result = await ethicalCircuitBreaker.evaluateAndBreak(target);

    if (result.triggered) {
      // 显示结果
      console.info(`[龍魂·伦理] ${result.message}`);
    }

    this.refreshData();
  }

  // ================================================================
  // 辅助方法
  // ================================================================
  private getTargetIcon(type: TargetType): string {
    switch (type) {
      case TargetType.HUMAN: return '👤';
      case TargetType.ROBOT_ETHICAL: return '🤖✓';
      case TargetType.ROBOT_UNETHICAL: return '🤖⚠️';
      case TargetType.AI_ANOMALY: return '🧠⚠️';
      case TargetType.DRONE: return '🛸';
      default: return '❓';
    }
  }

  private getThreatLabel(level: ThreatLevel): string {
    switch (level) {
      case ThreatLevel.NONE: return '安全';
      case ThreatLevel.LOW: return '低';
      case ThreatLevel.MEDIUM: return '中';
      case ThreatLevel.HIGH: return '高';
      case ThreatLevel.CRITICAL: return '严重';
    }
  }

  private getThreatColor(level: ThreatLevel): string {
    switch (level) {
      case ThreatLevel.NONE: return '#00ff00';
      case ThreatLevel.LOW: return '#4a9eff';
      case ThreatLevel.MEDIUM: return '#ffd700';
      case ThreatLevel.HIGH: return '#ff6b35';
      case ThreatLevel.CRITICAL: return '#ff0000';
    }
  }

  private getInterferenceIcon(type: string): string {
    switch (type) {
      case 'emf_jamming': return '⚡';
      case 'signal_hijack': return '🎯';
      case 'beacon_injection': return '📡';
      case 'frequency_sweep': return '🌊';
      case 'logic_confusion': return '🌀';
      case 'power_depletion': return '🔋';
      case 'safe_mode_force': return '🛑';
      case 'protocol_stun': return '💫';
      default: return '🛡️';
    }
  }

  private getBreakerLevelIcon(level: BreakerLevel): string {
    switch (level) {
      case BreakerLevel.LEVEL_1_OBSERVE: return '👁️';
      case BreakerLevel.LEVEL_2_WARN: return '📢';
      case BreakerLevel.LEVEL_3_INTERFERE: return '🛡️';
      case BreakerLevel.LEVEL_4_ISOLATE: return '🚫';
      case BreakerLevel.LEVEL_5_FUSE: return '🔥';
      default: return '⚡';
    }
  }
}
