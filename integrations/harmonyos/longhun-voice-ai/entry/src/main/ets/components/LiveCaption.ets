// entry/src/main/ets/components/LiveCaption.ets
// 龍魂 · 实时字幕组件

import { voiceState, CaptionSegment, ASRStatus } from '../models/VoiceModel';
import { asrEngine } from '../engine/ASREngine';

@Component
export struct LiveCaption {
  @StorageLink('voiceState') voiceState: VoiceState = voiceState;
  @State private isExpanded: boolean = true;

  getVisibleCaptions(): CaptionSegment[] {
    const maxLines = this.voiceState.captionSettings.maxLines;
    const captions = this.voiceState.captions;
    if (captions.length <= maxLines) return captions;
    if (this.voiceState.captionSettings.autoScroll) return captions.slice(-maxLines);
    return captions.slice(0, maxLines);
  }

  startCaption(): void { this.voiceState.isCaptionEnabled = true; asrEngine.startRecognition({ continuous: true, interimResults: true }); console.info('[龍魂] 实时字幕已启动'); }
  stopCaption(): void { this.voiceState.isCaptionEnabled = false; asrEngine.stopRecognition(); console.info('[龍魂] 实时字幕已停止'); }

  build() {
    Column() {
      this.HeaderBuilder()
      if (this.isExpanded) { this.CaptionDisplayBuilder() }
      this.ControlBuilder()
    }
    .width('100%').backgroundColor(this.voiceState.captionSettings.bgColor).borderRadius(8).padding(12)
  }

  @Builder
  HeaderBuilder() {
    Row() {
      Text('📝').fontSize(20).margin({ right: 8 })
      Text('实时字幕').fontSize(16).fontWeight(FontWeight.Bold).fontColor(this.voiceState.captionSettings.fontColor).layoutWeight(1)
      Circle().width(8).height(8).fill(this.voiceState.asrStatus === ASRStatus.LISTENING ? '#00ff00' : this.voiceState.asrStatus === ASRStatus.RECOGNIZING ? '#ffcc00' : '#666').margin({ right: 8 })
      Button() { Text(this.isExpanded ? '▼' : '▶').fontSize(14).fontColor('#fff') }
      .type(ButtonType.Circle).backgroundColor('#333').width(28).height(28).onClick(() => { this.isExpanded = !this.isExpanded; })
    }
    .width('100%').margin({ bottom: 8 })
  }

  @Builder
  CaptionDisplayBuilder() {
    Column() {
      ForEach(this.getVisibleCaptions(), (segment: CaptionSegment) => {
        Row() {
          if (this.voiceState.captionSettings.showSpeaker && segment.speakerId) {
            Text(`[${segment.speakerId}]`).fontSize(this.voiceState.captionSettings.fontSize - 2).fontColor('#c41e3a').margin({ right: 8 })
          }
          if (this.voiceState.captionSettings.showTimestamp) {
            Text(segment.getTimeRange()).fontSize(this.voiceState.captionSettings.fontSize - 4).fontColor('#666').margin({ right: 8 })
          }
          Text(segment.text).fontSize(this.voiceState.captionSettings.fontSize).fontColor(this.voiceState.captionSettings.fontColor).fontWeight(segment.isFinal ? FontWeight.Normal : FontWeight.Light).layoutWeight(1).opacity(segment.isFinal ? 1.0 : 0.7)
        }
        .width('100%').padding({ top: 4, bottom: 4 })
      })
      if (this.voiceState.currentASRResult && !this.voiceState.currentASRResult.isFinal) {
        Row() {
          Text(this.voiceState.currentASRResult.text).fontSize(this.voiceState.captionSettings.fontSize).fontColor(this.voiceState.captionSettings.fontColor).fontWeight(FontWeight.Light).layoutWeight(1).opacity(0.5)
          Text('▌').fontSize(this.voiceState.captionSettings.fontSize).fontColor('#c41e3a').opacity(0.8)
        }
        .width('100%').padding({ top: 4, bottom: 4 })
      }
    }
    .width('100%').minHeight(60).maxHeight(200).backgroundColor('rgba(0,0,0,0.3)').borderRadius(4).padding(8).margin({ bottom: 8 })
  }

  @Builder
  ControlBuilder() {
    Row() {
      Button() { Text(this.voiceState.isRecording ? '⏹' : '⏺').fontSize(18).fontColor(this.voiceState.isRecording ? '#ff0000' : '#fff') }
      .type(ButtonType.Circle).backgroundColor(this.voiceState.isRecording ? 'rgba(255,0,0,0.2)' : '#333').width(40).height(40)
      .onClick(() => { if (this.voiceState.isRecording) this.stopCaption(); else this.startCaption(); })
      Blank()
      Button() { Text('⚙️').fontSize(16) }.type(ButtonType.Circle).backgroundColor('#333').width(36).height(36).onClick(() => {})
      Button() { Text('🗑').fontSize(16) }.type(ButtonType.Circle).backgroundColor('#333').width(36).height(36).margin({ left: 8 }).onClick(() => { this.voiceState.captions = []; })
    }
    .width('100%')
  }
}
