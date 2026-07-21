// entry/src/main/ets/pages/VoiceAssistantPage.ets
// 龍魂 · 语音助手主页面

import { voiceState, VoiceState, ASRStatus, TTSStatus } from '../models/VoiceModel';
import { LiveCaption } from '../components/LiveCaption';
import { VoiceAssistant } from '../components/VoiceAssistant';
import { asrEngine } from '../engine/ASREngine';
import { ttsEngine } from '../engine/TTSEngine';
import { VoiceDatabase } from '../database/VoiceDatabase';

@Entry
@Component
struct VoiceAssistantPage {
  @StorageLink('voiceState') voiceState: VoiceState = voiceState;
  @State private selectedTab: number = 0;
  @State private showModelManager: boolean = false;
  @State private showVoicePrint: boolean = false;

  aboutToAppear() {
    asrEngine.initialize(); ttsEngine.initialize(); this.loadModels(); VoiceDatabase.init();
    console.info('[龍魂] 语音助手页面已初始化');
  }
  loadModels(): void {}

  build() {
    Column() {
      this.HeaderBuilder()
      this.StatsBuilder()
      this.TabBuilder()
      this.ContentBuilder()
      this.FooterBuilder()
    }
    .width('100%').height('100%').backgroundColor('#0a0a0a')
  }

  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉').fontSize(28).margin({ right: 8 })
      Column() { Text('龍魂语音AI').fontSize(20).fontWeight(FontWeight.Bold).fontColor('#c41e3a'); Text(`UID:${MASTER_UID} · 端侧推理`).fontSize(12).fontColor('#666'); }
      .alignItems(HorizontalAlign.Start).layoutWeight(1)
      Button() { Text('📦').fontSize(20) }.type(ButtonType.Circle).backgroundColor('#1a1a1a').width(40).height(40).onClick(() => { this.showModelManager = true; })
      Button() { Text('👤').fontSize(20) }.type(ButtonType.Circle).backgroundColor('#1a1a1a').width(40).height(40).margin({ left: 8 }).onClick(() => { this.showVoicePrint = true; })
    }
    .width('100%').height(56).padding({ left: 16, right: 16 }).backgroundColor('#1a1a1a').border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('模型', this.voiceState.statistics.totalModels.toString(), '#fff')
      this.StatCard('已加载', this.voiceState.statistics.loadedModels.toString(), '#00ff00')
      this.StatCard('识别', this.voiceState.statistics.totalASRResults.toString(), '#ffcc00')
      this.StatCard('字幕', this.voiceState.statistics.totalCaptions.toString(), '#0066cc')
      this.StatCard('对话', this.voiceState.statistics.totalDialogs.toString(), '#c41e3a')
    }
    .width('100%').height(80).padding({ left: 12, right: 12, top: 8, bottom: 8 }).backgroundColor('#1a1a1a').border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() { Text(value).fontSize(24).fontWeight(FontWeight.Bold).fontColor(color); Text(label).fontSize(11).fontColor('#666').margin({ top: 4 }); }
    .width('20%').height('100%').justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Center)
  }

  @Builder
  TabBuilder() {
    Row() {
      ForEach([{ label: '语音助手', icon: '🤖' }, { label: '实时字幕', icon: '📝' }, { label: '模型管理', icon: '📦' }, { label: '声纹设置', icon: '👤' }], (item: {label: string, icon: string}, index: number) => {
        Column() {
          Text(`${item.icon} ${item.label}`).fontSize(13).fontWeight(this.selectedTab === index ? FontWeight.Bold : FontWeight.Normal).fontColor(this.selectedTab === index ? '#c41e3a' : '#888')
          if (this.selectedTab === index) { Divider().strokeWidth(2).color('#c41e3a').width(20).margin({ top: 4 }); }
        }
        .padding({ top: 12, bottom: 12, left: 16, right: 16 }).onClick(() => { this.selectedTab = index; })
      })
    }
    .width('100%').justifyContent(FlexAlign.SpaceAround).backgroundColor('#1a1a1a').border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  ContentBuilder() {
    if (this.selectedTab === 0) { VoiceAssistant() }
    else if (this.selectedTab === 1) { LiveCaption() }
    else if (this.selectedTab === 2) { this.ModelManagerBuilder() }
    else { this.VoicePrintBuilder() }
  }

  @Builder
  ModelManagerBuilder() {
    Column() {
      Text('模型管理').fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 16 })
      List() {
        ForEach(Array.from(this.voiceState.models.values()), (model) => {
          ListItem() {
            Row() {
              Column() { Text(model.getDisplayName()).fontSize(14).fontColor('#fff'); Text(`${model.size}MB · 准确率${Math.round(model.accuracy * 100)}%`).fontSize(11).fontColor('#666'); }
              .alignItems(HorizontalAlign.Start).layoutWeight(1)
              Text(model.isLoaded ? '● 已加载' : model.isDownloaded ? '○ 已下载' : '⊗ 未下载').fontSize(12).fontColor(model.isLoaded ? '#00ff00' : model.isDownloaded ? '#ffcc00' : '#666')
            }
            .width('100%').padding(12).backgroundColor('#1a1a1a').borderRadius(8)
          }
        })
      }
      .width('100%').layoutWeight(1)
    }
    .width('100%').padding(16)
  }

  @Builder
  VoicePrintBuilder() {
    Column() {
      Text('声纹设置').fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 16 })
      List() {
        ForEach(Array.from(this.voiceState.voicePrints.values()), (print) => {
          ListItem() {
            Row() {
              Text('👤').fontSize(20).margin({ right: 12 })
              Column() { Text(print.name).fontSize(14).fontColor('#fff'); Text(`${print.sampleCount} 个样本 · 阈值 ${print.threshold}`).fontSize(11).fontColor('#666'); }
              .alignItems(HorizontalAlign.Start).layoutWeight(1)
            }
            .width('100%').padding(12).backgroundColor('#1a1a1a').borderRadius(8)
          }
        })
      }
      .width('100%').layoutWeight(1)
    }
    .width('100%').padding(16)
  }

  @Builder
  FooterBuilder() {
    Row() {
      Column() { Text('🐉').fontSize(20); Text(`UID:${MASTER_UID}`).fontSize(10).fontColor('#666'); }
      .alignItems(HorizontalAlign.Start).layoutWeight(1)
      Row() {
        Text(`🎤 ${this.voiceState.asrStatus === ASRStatus.IDLE ? '就绪' : '工作中'}`).fontSize(12).fontColor('#888')
        Text(`🔊 ${this.voiceState.ttsStatus === TTSStatus.IDLE ? '就绪' : '工作中'}`).fontSize(12).fontColor('#888').margin({ left: 12 })
      }
    }
    .width('100%').height(40).padding({ left: 16, right: 16 }).backgroundColor('#1a1a1a').border({ width: { top: 1 }, color: '#333' })
  }
}

const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
