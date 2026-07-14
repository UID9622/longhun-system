// entry/src/main/ets/pages/EducationAI.ets
// 龍魂 · 教育AI鸿蒙客户端 · 对接全栈后端

import { http } from '@kit.NetworkKit';

const API_BASE = "http://localhost:8000/api/v1";
const MASTER_UID = "9622";

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  intent?: string;
  sources?: SourceItem[];
  confidence?: number;
  toolsUsed?: string[];
  timestamp: string;
}

interface SourceItem {
  content: string;
  source: string;
  page: number;
  score: number;
}

@Entry
@Component
struct EducationAIPage {
  @State private messages: ChatMessage[] = [];
  @State private inputText: string = '';
  @State private isLoading: boolean = false;
  @State private sessionId: string = `SESSION-${Date.now()}`;
  @State private showSources: boolean = false;
  @State private selectedMessage: ChatMessage | null = null;

  aboutToAppear() {
    // 欢迎消息
    this.messages.push({
      id: `WELCOME-${Date.now()}`,
      role: 'assistant',
      content: '🐉 龍魂教育AI已就绪\n\n我可以帮你：\n• 查询知识点\n• 解答作业题目\n• 推荐学习课程\n• 生成练习题\n\n请直接输入你的问题！',
      timestamp: new Date().toISOString()
    });
  }

  build() {
    Column() {
      this.HeaderBuilder()
      this.ChatAreaBuilder()
      this.InputAreaBuilder()
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
        Text('龍魂教育AI').fontSize(20).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text(`UID:${MASTER_UID} · RAG+Agent+Tools`).fontSize(12).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Button('🛠️')
        .fontSize(14)
        .fontColor('#fff')
        .backgroundColor('#333')
        .borderRadius(8)
        .margin({ left: 8 })
        .onClick(() => {
          this.showToolsDialog();
        })

      Button('🔄')
        .fontSize(14)
        .fontColor('#fff')
        .backgroundColor('#333')
        .borderRadius(8)
        .margin({ left: 4 })
        .onClick(() => {
          this.resetMemory();
        })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  ChatAreaBuilder() {
    Scroll() {
      Column() {
        ForEach(this.messages, (msg: ChatMessage) => {
          this.MessageBubbleBuilder(msg)
        })
      }
      .width('100%')
      .padding({ left: 12, right: 12, top: 8, bottom: 8 })
      .alignItems(HorizontalAlign.Start)
    }
    .width('100%')
    .layoutWeight(1)
    .scrollBar(BarState.Auto)
  }

  @Builder
  MessageBubbleBuilder(msg: ChatMessage) {
    Column() {
      // 头像+名称行
      Row() {
        if (msg.role === 'assistant') {
          Text('🐉').fontSize(20)
          Text('龍魂AI').fontSize(12).fontColor('#c41e3a').margin({ left: 4 })
        } else {
          Row().layoutWeight(1)
          Text('我').fontSize(12).fontColor('#00ff00').margin({ right: 4 })
          Text('👤').fontSize(20)
        }
      }
      .width('100%')
      .margin({ bottom: 4 })

      // 内容气泡
      Column() {
        Text(msg.content)
          .fontSize(14)
          .fontColor('#fff')
          .maxLines(100)
          .textOverflow({ overflow: TextOverflow.Ellipsis })

        // 元信息（AI消息专用）
        if (msg.role === 'assistant') {
          if (msg.intent) {
            Row() {
              Text(`意图: ${msg.intent}`).fontSize(10).fontColor('#666')
              if (msg.confidence) {
                Text(`置信度: ${(msg.confidence * 100).toFixed(1)}%`)
                  .fontSize(10)
                  .fontColor(msg.confidence > 0.8 ? '#00ff00' : '#ffcc00')
                  .margin({ left: 8 })
              }
            }
            .width('100%')
            .margin({ top: 8 })
          }

          if (msg.toolsUsed && msg.toolsUsed.length > 0) {
            Row() {
              Text('🔧').fontSize(10)
              Text(msg.toolsUsed.join(', ')).fontSize(10).fontColor('#888').margin({ left: 4 })
            }
            .width('100%')
            .margin({ top: 4 })
          }

          if (msg.sources && msg.sources.length > 0) {
            Button('📚 查看来源').fontSize(11).fontColor('#c41e3a').backgroundColor('transparent')
              .margin({ top: 8 })
              .onClick(() => {
                this.selectedMessage = msg;
                this.showSources = true;
              })
          }
        }
      }
      .width('85%')
      .padding(12)
      .backgroundColor(msg.role === 'assistant' ? '#1a1a1a' : '#0d2d0d')
      .borderRadius({
        topLeft: msg.role === 'assistant' ? 4 : 12,
        topRight: msg.role === 'assistant' ? 12 : 4,
        bottomLeft: 12,
        bottomRight: 12
      })
      .margin({ bottom: 8 })
    }
    .width('100%')
  }

  @Builder
  InputAreaBuilder() {
    Row() {
      TextInput({ placeholder: '输入问题...', text: $$this.inputText })
        .width('75%')
        .height(44)
        .fontSize(14)
        .fontColor('#fff')
        .placeholderColor('#666')
        .backgroundColor('#1a1a1a')
        .borderRadius(8)
        .padding({ left: 12, right: 12 })
        .onSubmit(() => {
          this.sendMessage();
        })

      Button(this.isLoading ? '⏳' : '发送')
        .width('20%')
        .height(44)
        .fontSize(14)
        .fontColor('#fff')
        .backgroundColor(this.isLoading ? '#333' : '#c41e3a')
        .borderRadius(8)
        .enabled(!this.isLoading)
        .onClick(() => {
          this.sendMessage();
        })
    }
    .width('100%')
    .height(60)
    .padding({ left: 12, right: 12, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }

  // === 发送消息 ===
  async sendMessage() {
    if (!this.inputText.trim() || this.isLoading) return;

    const userMsg: ChatMessage = {
      id: `USER-${Date.now()}`,
      role: 'user',
      content: this.inputText,
      timestamp: new Date().toISOString()
    };

    this.messages.push(userMsg);
    const question = this.inputText;
    this.inputText = '';
    this.isLoading = true;

    try {
      const httpRequest = http.createHttp();
      const response = await httpRequest.request(`${API_BASE}/chat`, {
        method: http.RequestMethod.POST,
        header: { 'Content-Type': 'application/json' },
        extraData: JSON.stringify({
          message: question,
          session_id: this.sessionId
        })
      });

      const result = JSON.parse(response.result.toString());

      const aiMsg: ChatMessage = {
        id: `AI-${Date.now()}`,
        role: 'assistant',
        content: result.response,
        intent: result.intent,
        sources: result.sources,
        confidence: result.confidence,
        toolsUsed: result.tools_used,
        timestamp: new Date().toISOString()
      };

      this.messages.push(aiMsg);
    } catch (e) {
      this.messages.push({
        id: `ERROR-${Date.now()}`,
        role: 'assistant',
        content: `❌ 请求失败: 请确认后端服务已启动 (${API_BASE})`,
        timestamp: new Date().toISOString()
      });
    } finally {
      this.isLoading = false;
    }
  }

  // === 显示工具列表 ===
  async showToolsDialog() {
    try {
      const httpRequest = http.createHttp();
      const response = await httpRequest.request(`${API_BASE}/tools/list`, {
        method: http.RequestMethod.GET
      });

      const result = JSON.parse(response.result.toString());
      let toolsInfo = '🛠️ 可用工具列表:\n\n';
      if (result.tools) {
        for (let tool of result.tools) {
          toolsInfo += `• ${tool.name}: ${tool.description}\n`;
        }
      }

      this.messages.push({
        id: `TOOLS-${Date.now()}`,
        role: 'assistant',
        content: toolsInfo,
        timestamp: new Date().toISOString()
      });
    } catch (e) {
      this.messages.push({
        id: `ERROR-${Date.now()}`,
        role: 'assistant',
        content: '❌ 获取工具列表失败，请确认后端服务已启动',
        timestamp: new Date().toISOString()
      });
    }
  }

  // === 重置Agent记忆 ===
  async resetMemory() {
    try {
      const httpRequest = http.createHttp();
      await httpRequest.request(`${API_BASE}/agent/reset`, {
        method: http.RequestMethod.POST
      });

      this.messages.push({
        id: `RESET-${Date.now()}`,
        role: 'assistant',
        content: '✅ Agent记忆已重置',
        timestamp: new Date().toISOString()
      });
    } catch (e) {
      // 静默失败
    }
  }
}
