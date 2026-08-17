// integrations/harmonyos/longhun-bridge/src/main/ets/LongHunBridge.ets
// 🐉 龍魂 · 鸿蒙端接入模块 v1.0
// DNA: #龍芯⚡️丙午·丙申·庚申·亥时-HARMONY-BRIDGE-UID9622
// 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

import http from '@ohos.net.http';
import { BusinessError } from '@kit.BasicServicesKit';
import { preferences } from '@kit.ArkData';
import { deviceInfo } from '@kit.BasicServicesKit';

// ============================================================
// 类型定义
// ============================================================

export interface LongHunConfig {
  autoDiscover?: boolean;      // 是否自动发现Mac (默认true)
  syncInterval?: number;        // 记忆同步间隔(秒, 默认300)
  timeout?: number;             // 请求超时(秒, 默认30)
  model?: string;               // 模型名称
  cacheDir?: string;            // 缓存目录
}

export interface ChatResponse {
  dna: string;
  reply: string;
  context: string;
  timestamp: string;
  tricolor: '🟢' | '🟡' | '🔴';
}

export interface MemoryDigest {
  digest: string;
  timestamp: string;
  source: string;
  entries?: Array<{
    role: 'user' | 'assistant';
    content: string;
    time: string;
  }>;
}

// ============================================================
// 主权锚定
// ============================================================

const UID = "9622";
const CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";
const DNA_PREFIX = "#龍芯⚡️";

function generateDNA(): string {
  const now = new Date();
  const ts = now.getFullYear() + '-' +
             String(now.getMonth()+1).padStart(2,'0') + '-' +
             String(now.getDate()).padStart(2,'0');
  const rand = Math.random().toString(36).substring(2, 10).toUpperCase();
  return `${DNA_PREFIX}${ts}-HARMONY-${rand}-${UID}`;
}

// ============================================================
// 主类
// ============================================================

export class LongHunBridge {
  private static instance: LongHunBridge;
  private config: LongHunConfig = {
    autoDiscover: true,
    syncInterval: 300,
    timeout: 30,
    model: 'longhun-v4.1.4:latest'
  };
  private macIP: string = '';
  private syncPort: number = 19622;    // TCP 加密同步端口（A路径）
  private httpPort: number = 19623;    // HTTP REST 同步端口（B路径）
  private chatPort: number = 18799;    // 对话桥接端口
  private memory: MemoryDigest | null = null;
  private isConnected: boolean = false;
  private syncTimer: number | null = null;
  private context: Array<{role: string, content: string}> = [];

  private constructor() {}

  public static getInstance(): LongHunBridge {
    if (!LongHunBridge.instance) {
      LongHunBridge.instance = new LongHunBridge();
    }
    return LongHunBridge.instance;
  }

  // ============================================================
  // 初始化
  // ============================================================

  public async init(config: LongHunConfig = {}): Promise<void> {
    this.config = { ...this.config, ...config };
    console.info('🐉 龙魂桥接初始化', this.config);

    // 1. 加载缓存记忆
    await this.loadCachedMemory();

    // 2. 自动发现Mac
    if (this.config.autoDiscover) {
      await this.discover();
    }

    // 3. 启动定时同步
    if (this.config.syncInterval && this.config.syncInterval > 0) {
      this.startSyncTimer();
    }
  }

  // ============================================================
  // 1. 服务发现
  // ============================================================

  public async discover(): Promise<string> {
    try {
      // 方案1：mDNS发现 (优先)
      const mdnsIP = await this.discoverViaMDNS();
      if (mdnsIP) {
        this.macIP = mdnsIP;
        this.isConnected = true;
        console.info(`✅ 通过mDNS发现Mac: ${this.macIP}`);
        return this.macIP;
      }

      // 方案2：广播扫描 (备选)
      const scanIP = await this.scanNetwork();
      if (scanIP) {
        this.macIP = scanIP;
        this.isConnected = true;
        console.info(`✅ 通过网络扫描发现Mac: ${this.macIP}`);
        return this.macIP;
      }

      // 方案3：回退到上次使用的IP (如果已缓存)
      const cachedIP = await this.getCachedIP();
      if (cachedIP) {
        this.macIP = cachedIP;
        this.isConnected = true;
        console.info(`✅ 使用缓存的Mac IP: ${this.macIP}`);
        return this.macIP;
      }

      console.warn('⚠️ 未发现Mac，请检查网络或手动设置IP');
      this.isConnected = false;
      return '';
    } catch (e) {
      console.error('❌ 服务发现失败:', e);
      this.isConnected = false;
      return '';
    }
  }

  private async discoverViaMDNS(): Promise<string> {
    // 鸿蒙端mDNS实现 (需要ohos.net.mdns权限)
    try {
      // 使用鸿蒙的mdns模块
      const mdns = await import('@ohos.net.mdns');
      const services = await mdns.discoverServices('_longhun._tcp.local.', 3000);

      for (const svc of services) {
        if (svc.name?.includes('longhun-mac')) {
          return svc.host || '';
        }
      }
      return '';
    } catch (e) {
      // mDNS不可用，静默降级
      return '';
    }
  }

  private async scanNetwork(): Promise<string> {
    // 简化版网络扫描 (实际应实现ARP扫描)
    // 这里假设用户在同一个网段，尝试常见的IP
    try {
      // 获取本机IP网段
      const localIP = await this.getLocalIP();
      const subnet = localIP.substring(0, localIP.lastIndexOf('.'));

      // 扫描几个常见IP (实际应全量扫描)
      for (let i = 1; i <= 20; i++) {
        const testIP = `${subnet}.${i}`;
        const ok = await this.testConnection(testIP);
        if (ok) {
          return testIP;
        }
      }
      return '';
    } catch (e) {
      return '';
    }
  }

  private async testConnection(ip: string): Promise<boolean> {
    try {
      const httpRequest = http.createHttp();
      const resp = await httpRequest.request(
        `http://${ip}:${this.httpPort}/health`,
        { method: http.RequestMethod.GET, connectTimeout: 2000, readTimeout: 2000 }
      );
      return resp.responseCode === 200;
    } catch {
      return false;
    }
  }

  private async getLocalIP(): Promise<string> {
    // 获取本机局域网IP
    // 鸿蒙实际实现应通过wifiManager或connection模块获取
    try {
      // @ts-ignore
      const wifiManager = await import('@ohos.wifiManager');
      // 实际API可能不同，这里保留占位
      return '192.168.1.100';
    } catch {
      return '192.168.1.100';
    }
  }

  private async getCachedIP(): Promise<string> {
    try {
      const ctx = getContext();
      const prefs = await preferences.getPreferences(ctx, 'longhun_bridge');
      return prefs.getSync('mac_ip', '') as string;
    } catch {
      return '';
    }
  }

  private async saveCachedIP(ip: string): Promise<void> {
    try {
      const ctx = getContext();
      const prefs = await preferences.getPreferences(ctx, 'longhun_bridge');
      await prefs.put('mac_ip', ip);
      await prefs.flush();
    } catch (e) {
      console.warn('保存IP缓存失败:', e);
    }
  }

  // ============================================================
  // 2. 记忆同步
  // ============================================================

  public async syncMemory(): Promise<MemoryDigest | null> {
    if (!this.macIP) {
      await this.discover();
      if (!this.macIP) {
        console.warn('⚠️ 无法同步记忆: Mac未连接');
        return this.memory;
      }
    }

    try {
      const httpRequest = http.createHttp();
      const dna = generateDNA();
      const resp = await httpRequest.request(
        `http://${this.macIP}:${this.httpPort}/sync/memory`,
        {
          method: http.RequestMethod.GET,
          header: {
            'X-LongHun-Confirm': CONFIRM,
            'X-Dragon-DNA': dna
          },
          connectTimeout: this.config.timeout! * 1000,
          readTimeout: this.config.timeout! * 1000
        }
      );

      if (resp.responseCode === 200) {
        const wrapper = JSON.parse(resp.result as string);
        const data = wrapper.payload as MemoryDigest;
        this.memory = data;
        await this.saveMemoryCache(data);
        console.info('✅ 记忆同步成功');
        return data;
      } else {
        console.warn(`⚠️ 记忆同步返回状态码: ${resp.responseCode}`);
        return this.memory;
      }
    } catch (e) {
      console.error('❌ 记忆同步失败:', e);
      return this.memory;
    }
  }

  // ============================================================
  // 3. 对话 (核心功能)
  // ============================================================

  public async chat(prompt: string): Promise<ChatResponse> {
    // 1. 确保连接
    if (!this.macIP) {
      await this.discover();
    }

    // 2. 确保记忆已加载
    if (!this.memory) {
      await this.syncMemory();
    }

    // 3. 构建上下文
    const systemContext = this.buildContext(prompt);

    // 4. 发送请求
    try {
      const httpRequest = http.createHttp();
      const dna = generateDNA();

      const resp = await httpRequest.request(
        `http://${this.macIP}:${this.chatPort}/api/v1/chat`,
        {
          method: http.RequestMethod.POST,
          header: {
            'Content-Type': 'application/json',
            'X-Dragon-DNA': dna
          },
          extraData: JSON.stringify({
            prompt: prompt,
            system: systemContext,
            model: this.config.model,
            stream: false
          }),
          connectTimeout: this.config.timeout! * 1000 * 4,
          readTimeout: this.config.timeout! * 1000 * 4
        }
      );

      if (resp.responseCode === 200) {
        const data = JSON.parse(resp.result as string);
        const reply = data.reply || data.response || data.result || '';

        // 5. 更新对话上下文
        this.context.push({ role: 'user', content: prompt });
        this.context.push({ role: 'assistant', content: reply });

        // 6. 保存到本地记忆
        await this.appendMemory(prompt, reply);

        return {
          dna: dna,
          reply: reply,
          context: systemContext,
          timestamp: new Date().toISOString(),
          tricolor: '🟢'
        };
      } else {
        // 降级: 使用本地记忆回答
        return this.fallbackChat(prompt);
      }
    } catch (e) {
      console.error('❌ 对话失败:', e);
      return this.fallbackChat(prompt);
    }
  }

  // ============================================================
  // 4. 流式对话 (SSE)
  // ============================================================

  public async chatStream(
    prompt: string,
    onChunk: (chunk: string) => void,
    onComplete: (dna: string) => void,
    onError: (error: Error) => void
  ): Promise<void> {
    if (!this.macIP) {
      await this.discover();
    }

    if (!this.memory) {
      await this.syncMemory();
    }

    const systemContext = this.buildContext(prompt);
    const dna = generateDNA();

    try {
      const httpRequest = http.createHttp();
      const resp = await httpRequest.request(
        `http://${this.macIP}:${this.chatPort}/api/v1/chat`,
        {
          method: http.RequestMethod.POST,
          header: {
            'Content-Type': 'application/json',
            'X-Dragon-DNA': dna,
            'Accept': 'text/event-stream'
          },
          extraData: JSON.stringify({
            prompt: prompt,
            system: systemContext,
            model: this.config.model,
            stream: true
          }),
          connectTimeout: this.config.timeout! * 1000 * 4,
          readTimeout: this.config.timeout! * 1000 * 4
        }
      );

      if (resp.responseCode === 200) {
        // 处理SSE流
        const text = resp.result as string;
        const lines = text.split('\n');
        let fullReply = '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.substring(6);
            if (data === '[DONE]') break;
            try {
              const json = JSON.parse(data);
              const chunk = json.response || json.reply || '';
              if (chunk) {
                fullReply += chunk;
                onChunk(chunk);
              }
            } catch (e) {
              // 忽略非JSON数据
            }
          }
        }

        // 更新上下文
        this.context.push({ role: 'user', content: prompt });
        this.context.push({ role: 'assistant', content: fullReply });
        await this.appendMemory(prompt, fullReply);

        onComplete(dna);
      } else {
        onError(new Error(`HTTP ${resp.responseCode}`));
      }
    } catch (e) {
      onError(e as Error);
    }
  }

  // ============================================================
  // 辅助方法
  // ============================================================

  private buildContext(prompt: string): string {
    let ctx = '';
    if (this.memory) {
      ctx += `## 龙魂记忆摘要\n${this.memory.digest}\n\n`;
    }

    // 最近5条对话历史
    const recent = this.context.slice(-10);
    if (recent.length > 0) {
      ctx += '## 对话历史\n';
      for (const msg of recent) {
        ctx += `${msg.role}: ${msg.content}\n`;
      }
    }

    ctx += `\n## 当前问题\n用户: ${prompt}\n`;
    return ctx;
  }

  private async loadCachedMemory(): Promise<void> {
    try {
      const ctx = getContext();
      const prefs = await preferences.getPreferences(ctx, 'longhun_memory');
      const data = prefs.getSync('memory_data', '') as string;
      if (data) {
        this.memory = JSON.parse(data);
      }
    } catch (e) {
      console.warn('加载缓存记忆失败:', e);
    }
  }

  private async saveMemoryCache(data: MemoryDigest): Promise<void> {
    try {
      const ctx = getContext();
      const prefs = await preferences.getPreferences(ctx, 'longhun_memory');
      await prefs.put('memory_data', JSON.stringify(data));
      await prefs.flush();
    } catch (e) {
      console.warn('保存缓存记忆失败:', e);
    }
  }

  private async appendMemory(userMsg: string, assistantMsg: string): Promise<void> {
    if (!this.memory) {
      this.memory = { digest: '', timestamp: '', source: '鸿蒙' };
    }
    if (!this.memory.entries) {
      this.memory.entries = [];
    }
    this.memory.entries.push({
      role: 'user',
      content: userMsg,
      time: new Date().toISOString()
    });
    this.memory.entries.push({
      role: 'assistant',
      content: assistantMsg,
      time: new Date().toISOString()
    });
    // 更新摘要(取最后几条)
    const lastFew = this.memory.entries.slice(-10);
    this.memory.digest = lastFew.map(e => `${e.role}: ${e.content.substring(0, 50)}...`).join('\n');
    this.memory.timestamp = new Date().toISOString();

    await this.saveMemoryCache(this.memory);
  }

  private startSyncTimer(): void {
    if (this.syncTimer) {
      clearInterval(this.syncTimer);
    }
    this.syncTimer = setInterval(() => {
      this.syncMemory().catch(e => console.warn('定时同步失败:', e));
    }, this.config.syncInterval! * 1000);
  }

  private async fallbackChat(prompt: string): Promise<ChatResponse> {
    // 降级: 使用本地记忆生成回答
    const context = this.buildContext(prompt);
    const reply = `[离线模式] 基于本地记忆:\n${context}\n请检查Mac是否在线。`;
    return {
      dna: generateDNA(),
      reply: reply,
      context: context,
      timestamp: new Date().toISOString(),
      tricolor: '🟡'
    };
  }

  // ============================================================
  // 状态查询
  // ============================================================

  public getStatus(): {
    connected: boolean;
    macIP: string;
    syncPort: number;
    httpPort: number;
    chatPort: number;
    memorySize: number;
    contextLength: number;
  } {
    return {
      connected: this.isConnected,
      macIP: this.macIP,
      syncPort: this.syncPort,
      httpPort: this.httpPort,
      chatPort: this.chatPort,
      memorySize: this.memory?.entries?.length || 0,
      contextLength: this.context.length
    };
  }

  public setMacIP(ip: string): void {
    this.macIP = ip;
    this.isConnected = true;
    this.saveCachedIP(ip);
  }

  public setPorts(sync: number = 19622, chat: number = 18799, http: number = 19623): void {
    this.syncPort = sync;
    this.chatPort = chat;
    this.httpPort = http;
  }

  public destroy(): void {
    if (this.syncTimer) {
      clearInterval(this.syncTimer);
      this.syncTimer = null;
    }
  }
}

// ============================================================
// 导出默认实例
// ============================================================

export default LongHunBridge.getInstance();
