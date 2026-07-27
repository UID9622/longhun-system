// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-语音输入-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

/**
 * 语音输入模块 v1.1
 *
 * v1.1修正：小艺第三方API开放程度不透明 → 第一期用 @ohos.multimedia.audio 录音。
 * 第二期小艺唤醒确认开放后替换。
 *
 * 功能：
 * - 录音（最长60s）
 * - 录音状态管理
 * - 录音结果导出（给后续ASR/API使用）
 */

import audio from '@ohos.multimedia.audio'
import { Constants } from '../utils/Constants'
import { VoiceState } from '../models/Types'

/** 录音回调 */
export interface VoiceRecordCallback {
  onStateChange: (state: VoiceState) => void
  onDurationUpdate: (seconds: number) => void
  onResult: (audioData: ArrayBuffer) => void
  onError: (error: string) => void
}

export class VoiceInput {
  private audioCapturer: audio.AudioCapturer | null = null
  private state: VoiceState = VoiceState.IDLE
  private durationTimer: number = 0
  private duration: number = 0
  private audioData: ArrayBuffer | null = null
  private callback: VoiceRecordCallback | null = null

  /**
   * 开始录音
   */
  async startRecording(callback: VoiceRecordCallback): Promise<void> {
    if (this.state === VoiceState.RECORDING) {
      callback.onError('已经在录音中')
      return
    }

    this.callback = callback
    this.duration = 0
    this.audioData = null

    try {
      // 创建音频采集器
      const audioStreamInfo: audio.AudioStreamInfo = {
        samplingRate: audio.AudioSamplingRate.SAMPLE_RATE_16000,
        channels: audio.AudioChannel.CHANNEL_1,
        sampleFormat: audio.AudioSampleFormat.SAMPLE_FORMAT_S16LE,
        encodingType: audio.AudioEncodingType.ENCODING_TYPE_RAW
      }

      const audioCapturerInfo: audio.AudioCapturerInfo = {
        source: audio.SourceType.SOURCE_TYPE_MIC,
        capturerFlags: 0
      }

      const audioCapturerOptions: audio.AudioCapturerOptions = {
        streamInfo: audioStreamInfo,
        capturerInfo: audioCapturerInfo
      }

      this.audioCapturer = await audio.createAudioCapturer(audioCapturerOptions)
      await this.audioCapturer.start()

      this.setState(VoiceState.RECORDING)
      this.startDurationTimer()

      console.info('[VoiceInput] 录音已开始')
    } catch (err) {
      console.error(`[VoiceInput] 录音启动失败: ${JSON.stringify(err)}`)
      this.setState(VoiceState.ERROR)
      callback.onError(`录音启动失败: ${JSON.stringify(err)}`)
    }
  }

  /**
   * 停止录音
   */
  async stopRecording(): Promise<void> {
    if (this.state !== VoiceState.RECORDING || !this.audioCapturer) {
      return
    }

    try {
      this.stopDurationTimer()
      this.setState(VoiceState.PROCESSING)

      await this.audioCapturer.stop()
      await this.audioCapturer.release()
      this.audioCapturer = null

      this.setState(VoiceState.DONE)
      console.info(`[VoiceInput] 录音完成·${this.duration}s`)

      // 回调结果（目前为空buffer，等待ASR处理）
      if (this.callback) {
        this.callback.onResult(this.audioData ?? new ArrayBuffer(0))
      }
    } catch (err) {
      console.error(`[VoiceInput] 录音停止失败: ${JSON.stringify(err)}`)
      this.setState(VoiceState.ERROR)
      if (this.callback) {
        this.callback.onError(`录音停止失败: ${JSON.stringify(err)}`)
      }
    }
  }

  /**
   * 取消录音（不返回结果）
   */
  async cancelRecording(): Promise<void> {
    if (this.state !== VoiceState.RECORDING || !this.audioCapturer) {
      return
    }

    try {
      this.stopDurationTimer()
      await this.audioCapturer.stop()
      await this.audioCapturer.release()
      this.audioCapturer = null
      this.setState(VoiceState.IDLE)
      console.info('[VoiceInput] 录音已取消')
    } catch (err) {
      console.error(`[VoiceInput] 取消录音失败: ${JSON.stringify(err)}`)
      this.setState(VoiceState.ERROR)
    }
  }

  /** 获取当前状态 */
  getState(): VoiceState {
    return this.state
  }

  /** 获取录音时长（秒） */
  getDuration(): number {
    return this.duration
  }

  /** 销毁 */
  destroy(): void {
    this.stopDurationTimer()
    if (this.audioCapturer) {
      try {
        this.audioCapturer.stop()
        this.audioCapturer.release()
      } catch (_) {
        // 静默释放
      }
      this.audioCapturer = null
    }
    this.setState(VoiceState.IDLE)
  }

  // ══════ 私有方法 ══════

  private setState(state: VoiceState): void {
    this.state = state
    if (this.callback) {
      this.callback.onStateChange(state)
    }
  }

  private startDurationTimer(): void {
    this.duration = 0
    this.durationTimer = setInterval(() => {
      this.duration++
      if (this.callback) {
        this.callback.onDurationUpdate(this.duration)
      }
      // 超过最大时长自动停止
      if (this.duration >= Constants.VOICE_MAX_DURATION_MS / 1000) {
        this.stopRecording()
      }
    }, 1000)
  }

  private stopDurationTimer(): void {
    if (this.durationTimer) {
      clearInterval(this.durationTimer)
      this.durationTimer = 0
    }
  }
}
