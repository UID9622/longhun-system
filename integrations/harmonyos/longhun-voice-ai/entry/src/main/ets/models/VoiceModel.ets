// entry/src/main/ets/models/VoiceModel.ets
// 龍魂 · 语音模型层 · ArkTS

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 语音识别状态 ===
export enum ASRStatus {
  IDLE = 'idle',             // 空闲
  LISTENING = 'listening',   // 监听中
  RECOGNIZING = 'recognizing', // 识别中
  CONFIRMING = 'confirming', // 确认中
  COMPLETED = 'completed',   // 完成
  ERROR = 'error'            // 错误
}

// === 语音合成状态 ===
export enum TTSStatus {
  IDLE = 'idle',             // 空闲
  SYNTHESIZING = 'synthesizing', // 合成中
  PLAYING = 'playing',       // 播放中
  PAUSED = 'paused',         // 暂停
  COMPLETED = 'completed',   // 完成
  ERROR = 'error'            // 错误
}

// === 语音引擎类型 ===
export enum VoiceEngineType {
  ASR = 'asr',               // 自动语音识别
  TTS = 'tts',               // 文本转语音
  WAKE = 'wake',             // 唤醒词
  VPR = 'vpr',               // 声纹识别
  NSE = 'nse'                // 噪声抑制
}

// === 语言类型 ===
export enum LanguageType {
  ZH_CN = 'zh-CN',           // 简体中文
  ZH_TW = 'zh-TW',           // 繁体中文
  EN_US = 'en-US',           // 美式英语
  EN_GB = 'en-GB',           // 英式英语
  JA_JP = 'ja-JP',           // 日语
  KO_KR = 'ko-KR',           // 韩语
  FR_FR = 'fr-FR',           // 法语
  DE_DE = 'de-DE',           // 德语
  ES_ES = 'es-ES',           // 西班牙语
  RU_RU = 'ru-RU'            // 俄语
}

// === 方言类型 ===
export enum DialectType {
  MANDARIN = 'mandarin',     // 普通话
  CANTONESE = 'cantonese',   // 粤语
  SICHUAN = 'sichuan',       // 四川话
  HAKKA = 'hakka',           // 客家话
  WU = 'wu',                 // 吴语
  MIN = 'min',               // 闽语
  XIANG = 'xiang',           // 湘语
  GAN = 'gan'                // 赣语
}

// === 语音性别 ===
export enum VoiceGender {
  MALE = 'male',             // 男声
  FEMALE = 'female',         // 女声
  NEUTRAL = 'neutral'        // 中性
}

// === 情感类型 ===
export enum EmotionType {
  NEUTRAL = 'neutral',       // 中性
  HAPPY = 'happy',           // 开心
  SAD = 'sad',               // 悲伤
  ANGRY = 'angry',           // 愤怒
  EXCITED = 'excited',       // 兴奋
  CALM = 'calm',             // 平静
  SERIOUS = 'serious'        // 严肃
}

// === 端侧模型 ===
export class VoiceModel {
  id: string;                // 模型ID
  name: string;              // 模型名称
  engineType: VoiceEngineType; // 引擎类型
  language: LanguageType;     // 语言
  dialect?: DialectType;     // 方言

  // 模型信息
  version: string;           // 版本
  size: number;              // 大小MB
  path: string;             // 本地路径

  // 性能
  accuracy: number;          // 准确率
  latency: number;           // 延迟ms
  memoryUsage: number;       // 内存占用MB

  // 状态
  isDownloaded: boolean;     // 是否已下载
  isLoaded: boolean;          // 是否已加载
  isEnabled: boolean;         // 是否启用

  // 审计
  downloadedAt?: Date;
  loadedAt?: Date;
  dnaSignature: string;

  constructor(data: Partial<VoiceModel> = {}) {
    this.id = data.id || `MODEL-${Date.now()}`;
    this.name = data.name || '未命名模型';
    this.engineType = data.engineType || VoiceEngineType.ASR;
    this.language = data.language || LanguageType.ZH_CN;
    this.dialect = data.dialect;

    this.version = data.version || '1.0.0';
    this.size = data.size || 0;
    this.path = data.path || '';

    this.accuracy = data.accuracy || 0.95;
    this.latency = data.latency || 200;
    this.memoryUsage = data.memoryUsage || 100;

    this.isDownloaded = data.isDownloaded || false;
    this.isLoaded = data.isLoaded || false;
    this.isEnabled = data.isEnabled || true;

    this.downloadedAt = data.downloadedAt;
    this.loadedAt = data.loadedAt;
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.name}-${this.engineType}-${this.version}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }

  getDisplayName(): string {
    const langNames: Record<string, string> = {
      'zh-CN': '中文', 'zh-TW': '繁体中文', 'en-US': '英语',
      'en-GB': '英式英语', 'ja-JP': '日语', 'ko-KR': '韩语'
    };
    const engineNames: Record<string, string> = {
      'asr': '识别', 'tts': '合成', 'wake': '唤醒', 'vpr': '声纹', 'nse': '降噪'
    };
    return `${langNames[this.language] || this.language} ${engineNames[this.engineType] || this.engineType} v${this.version}`;
  }

  load(): void {
    if (!this.isDownloaded) { console.error(`[龍魂] 模型未下载: ${this.name}`); return; }
    this.isLoaded = true; this.loadedAt = new Date();
    console.info(`[龍魂] 模型加载: ${this.name}`);
  }

  unload(): void { this.isLoaded = false; console.info(`[龍魂] 模型卸载: ${this.name}`); }
}

// === 语音识别结果 ===
export class ASRResult {
  id: string; text: string; confidence: number; isFinal: boolean;
  startTime: number; endTime: number; words: WordInfo[];
  detectedLanguage: LanguageType; detectedDialect?: DialectType;

  constructor(data: Partial<ASRResult> = {}) {
    this.id = data.id || `ASR-${Date.now()}`;
    this.text = data.text || ''; this.confidence = data.confidence || 0; this.isFinal = data.isFinal || false;
    this.startTime = data.startTime || 0; this.endTime = data.endTime || 0;
    this.words = data.words || []; this.detectedLanguage = data.detectedLanguage || LanguageType.ZH_CN;
    this.detectedDialect = data.detectedDialect;
  }
  getDuration(): number { return this.endTime - this.startTime; }
  isHighConfidence(): boolean { return this.confidence >= 0.9; }
}

export interface WordInfo { word: string; startTime: number; endTime: number; confidence: number; }

// === 语音合成结果 ===
export class TTSResult {
  id: string; text: string; audioData: ArrayBuffer; sampleRate: number; duration: number;
  gender: VoiceGender; emotion: EmotionType; speed: number; pitch: number;

  constructor(data: Partial<TTSResult> = {}) {
    this.id = data.id || `TTS-${Date.now()}`; this.text = data.text || '';
    this.audioData = data.audioData || new ArrayBuffer(0); this.sampleRate = data.sampleRate || 16000;
    this.duration = data.duration || 0; this.gender = data.gender || VoiceGender.FEMALE;
    this.emotion = data.emotion || EmotionType.NEUTRAL; this.speed = data.speed || 1.0; this.pitch = data.pitch || 1.0;
  }
}

// === 实时字幕片段 ===
export class CaptionSegment {
  id: string; text: string; speakerId?: string; startTime: number; endTime: number;
  confidence: number; isFinal: boolean;

  constructor(data: Partial<CaptionSegment> = {}) {
    this.id = data.id || `CAP-${Date.now()}`; this.text = data.text || '';
    this.speakerId = data.speakerId; this.startTime = data.startTime || 0;
    this.endTime = data.endTime || 0; this.confidence = data.confidence || 0; this.isFinal = data.isFinal || false;
  }
  formatTime(ms: number): string {
    const seconds = Math.floor(ms / 1000); const mins = Math.floor(seconds / 60); const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  getTimeRange(): string { return `[${this.formatTime(this.startTime)} - ${this.formatTime(this.endTime)}]`; }
}

// === 语音助手对话 ===
export class VoiceDialog {
  id: string; role: 'user' | 'assistant' | 'system'; text: string; audioUrl?: string;
  timestamp: Date; intent?: string; slots?: Record<string, any>;
  isPlaying: boolean; isError: boolean;

  constructor(data: Partial<VoiceDialog> = {}) {
    this.id = data.id || `DIALOG-${Date.now()}`; this.role = data.role || 'user';
    this.text = data.text || ''; this.audioUrl = data.audioUrl;
    this.timestamp = data.timestamp || new Date(); this.intent = data.intent; this.slots = data.slots;
    this.isPlaying = data.isPlaying || false; this.isError = data.isError || false;
  }
  getRoleIcon(): string {
    switch (this.role) { case 'user': return '👤'; case 'assistant': return '🤖'; case 'system': return '⚙️'; default: return '❓'; }
  }
  getRoleColor(): string {
    switch (this.role) { case 'user': return '#c41e3a'; case 'assistant': return '#00ff00'; case 'system': return '#888'; default: return '#fff'; }
  }
}

// === 声纹档案 ===
export class VoicePrint {
  id: string; userId: string; name: string; features: number[];
  sampleCount: number; samples: string[]; threshold: number;
  createdAt: Date; updatedAt: Date; dnaSignature: string;

  constructor(data: Partial<VoicePrint> = {}) {
    this.id = data.id || `VPRINT-${Date.now()}`; this.userId = data.userId || '';
    this.name = data.name || '未命名声纹'; this.features = data.features || [];
    this.sampleCount = data.sampleCount || 0; this.samples = data.samples || [];
    this.threshold = data.threshold || 0.85; this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date(); this.dnaSignature = this.signData();
  }
  private signData(): string { return `SM3-${this.id}-${this.userId}-${Date.now()}`; }
  match(features: number[]): number {
    if (this.features.length === 0 || features.length === 0) return 0;
    const dot = this.features.reduce((sum, f, i) => sum + f * (features[i] || 0), 0);
    const mag1 = Math.sqrt(this.features.reduce((sum, f) => sum + f * f, 0));
    const mag2 = Math.sqrt(features.reduce((sum, f) => sum + f * f, 0));
    return dot / (mag1 * mag2);
  }
  verify(features: number[]): boolean { return this.match(features) >= this.threshold; }
}

// === 语音全局状态 ===
@Observed
export class VoiceState {
  models: Map<string, VoiceModel> = new Map(); activeModelId: string = '';
  asrStatus: ASRStatus = ASRStatus.IDLE; asrResults: ASRResult[] = []; currentASRResult: ASRResult | null = null;
  ttsStatus: TTSStatus = TTSStatus.IDLE; ttsQueue: TTSResult[] = []; currentTTSResult: TTSResult | null = null;
  captions: CaptionSegment[] = []; isCaptionEnabled: boolean = false;
  captionSettings: CaptionSettings = {
    fontSize: 16, fontColor: '#ffffff', bgColor: 'rgba(0,0,0,0.8)',
    showSpeaker: true, showTimestamp: false, maxLines: 3, autoScroll: true
  };
  dialogs: VoiceDialog[] = []; isAssistantEnabled: boolean = false;
  wakeWord: string = '龍魂龍魂'; isWakeWordEnabled: boolean = true;
  voicePrints: Map<string, VoicePrint> = new Map(); isVoicePrintEnabled: boolean = false;
  isRecording: boolean = false; isPlaying: boolean = false; volume: number = 0.8;

  get statistics(): VoiceStats {
    return {
      totalModels: this.models.size, loadedModels: Array.from(this.models.values()).filter(m => m.isLoaded).length,
      totalASRResults: this.asrResults.length, totalCaptions: this.captions.length,
      totalDialogs: this.dialogs.length, totalVoicePrints: this.voicePrints.size,
      avgConfidence: this.getAvgConfidence(), totalRecordingTime: this.getTotalRecordingTime()
    };
  }
  private getAvgConfidence(): number {
    if (this.asrResults.length === 0) return 0;
    return Math.round(this.asrResults.reduce((sum, r) => sum + r.confidence, 0) / this.asrResults.length * 100) / 100;
  }
  private getTotalRecordingTime(): number { return this.asrResults.reduce((sum, r) => sum + r.getDuration(), 0); }

  loadModel(id: string): void { const model = this.models.get(id); if (model) { model.load(); this.activeModelId = id; } }
  startRecognition(): void { this.asrStatus = ASRStatus.LISTENING; this.isRecording = true; console.info('[龍魂] 开始语音识别'); }
  stopRecognition(): void { this.asrStatus = ASRStatus.IDLE; this.isRecording = false; console.info('[龍魂] 停止语音识别'); }

  addASRResult(result: ASRResult): void {
    this.asrResults.push(result); this.currentASRResult = result;
    if (this.isCaptionEnabled) this.addCaption(result);
    if (this.isAssistantEnabled && result.isFinal) {
      this.addDialog({ role: 'user', text: result.text, intent: result.text.includes('打开') ? 'open' : result.text.includes('关闭') ? 'close' : 'chat' });
    }
  }

  addCaption(result: ASRResult): void {
    const segment = new CaptionSegment({ text: result.text, startTime: result.startTime, endTime: result.endTime, confidence: result.confidence, isFinal: result.isFinal });
    if (result.isFinal) { this.captions.push(segment); } else {
      const last = this.captions[this.captions.length - 1];
      if (last && !last.isFinal) last.text = result.text; else this.captions.push(segment);
    }
    if (this.captions.length > 100) this.captions = this.captions.slice(-50);
  }

  addDialog(data: Partial<VoiceDialog>): void {
    this.dialogs.push(new VoiceDialog(data));
    if (this.dialogs.length > 100) this.dialogs = this.dialogs.slice(-50);
  }

  synthesize(text: string, options?: Partial<TTSResult>): void {
    this.ttsStatus = TTSStatus.SYNTHESIZING;
    console.info(`[龍魂] 语音合成: ${text}`);
  }

  playAudio(result: TTSResult): void { this.currentTTSResult = result; this.isPlaying = true; }

  registerVoicePrint(userId: string, name: string, features: number[]): void {
    this.voicePrints.set(userId, new VoicePrint({ userId, name, features, sampleCount: 1 }));
  }
  verifyVoicePrint(userId: string, features: number[]): boolean {
    const voicePrint = this.voicePrints.get(userId); return voicePrint ? voicePrint.verify(features) : false;
  }

  persist(): void {
    AppStorage.setOrCreate('voice_models', JSON.stringify(Array.from(this.models.entries())));
    AppStorage.setOrCreate('voice_captions', JSON.stringify(this.captions.slice(-50)));
    AppStorage.setOrCreate('voice_dialogs', JSON.stringify(this.dialogs.slice(-50)));
    AppStorage.setOrCreate('voice_prints', JSON.stringify(Array.from(this.voicePrints.entries())));
    AppStorage.setOrCreate('voice_settings', JSON.stringify(this.captionSettings));
  }
  load(): void {}
}

export interface CaptionSettings { fontSize: number; fontColor: string; bgColor: string; showSpeaker: boolean; showTimestamp: boolean; maxLines: number; autoScroll: boolean; }
export interface VoiceStats { totalModels: number; loadedModels: number; totalASRResults: number; totalCaptions: number; totalDialogs: number; totalVoicePrints: number; avgConfidence: number; totalRecordingTime: number; }

export const voiceState = new VoiceState();
AppStorage.setOrCreate('voiceState', voiceState);
