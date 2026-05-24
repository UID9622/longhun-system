/**
 * CNSH Connector - Obsidian 插件主文件
 * 连接 Obsidian 与 CNSH 核心系统
 */

const { Plugin, Notice, FileSystemAdapter, normalizePath } = require('obsidian');

// CNSH 插件类
class CNSHConnectorPlugin extends Plugin {
  constructor(app, manifest) {
    super(app, manifest);
    
    // 初始化服务
    this.cnshService = null;
    
    // 插件状态
    this.isServiceConnected = false;
    this.settings = {
      serverUrl: 'http://localhost:3000',
      apiToken: '',
      model: 'qwen:7b-chat',
      autoTag: true,
      autoEmbed: true,
      showNotifications: true,
      enableFileWatcher: true
    };
  }

  /**
   * 插件加载时调用
   */
  async onload() {
    console.log('Loading CNSH Connector plugin');
    
    // 加载设置
    await this.loadSettings();
    
    // 添加功能区图标
    this.addRibbonIcon('brain', 'CNSH Assistant', (evt) => {
      this.openAssistant();
    });
    
    // 添加命令
    this.addCommands();
    
    // 添加设置选项卡
    this.addSettingTab(new CNSHSettingTab(this.app, this));
    
    // 连接到 CNSH 服务
    this.connectToCNSH();
    
    // 添加编辑器上下文菜单
    this.addEditorMenu();
  }

  /**
   * 插件卸载时调用
   */
  async onunload() {
    console.log('Unloading CNSH Connector plugin');
    
    // 断开服务连接
    if (this.cnshService) {
      this.cnshService.disconnect();
    }
  }

  /**
   * 加载插件设置
   */
  async loadSettings() {
    this.settings = Object.assign({}, this.settings, await this.loadData());
  }

  /**
   * 保存插件设置
   */
  async saveSettings() {
    await this.saveData(this.settings);
  }

  /**
   * 连接到 CNSH 服务
   */
  async connectToCNSH() {
    try {
      // 创建简单的 HTTP 服务类
      this.cnshService = new CNSHHttpService(this.settings);
      
      // 测试连接
      const response = await this.cnshService.testConnection();
      
      if (response.status === 'ok') {
        this.isServiceConnected = true;
        
        if (this.settings.showNotifications) {
          new Notice('已连接到 CNSH 服务');
        }
        
        // 初始化文件同步
        if (this.settings.autoEmbed) {
          await this.syncVault();
        }
      }
      
    } catch (error) {
      console.error('Failed to connect to CNSH service:', error);
      this.isServiceConnected = false;
      
      if (this.settings.showNotifications) {
        new Notice(`无法连接到 CNSH 服务: ${error.message}`);
      }
    }
  }

  /**
   * 同步整个库到 CNSH 系统
   */
  async syncVault() {
    if (!this.isServiceConnected) {
      console.warn('CNSH service not connected, skipping vault sync');
      return;
    }
    
    const vault = this.app.vault;
    const markdownFiles = vault.getMarkdownFiles();
    
    if (this.settings.showNotifications) {
      new Notice(`开始同步 ${markdownFiles.length} 个文件到 CNSH`);
    }
    
    for (const file of markdownFiles) {
      try {
        const content = await vault.cachedRead(file);
        await this.cnshService.uploadFile(file.path, content);
      } catch (error) {
        console.error(`Failed to sync file ${file.path}:`, error);
      }
    }
    
    if (this.settings.showNotifications) {
      new Notice('CNSH 同步完成');
    }
  }

  /**
   * 打开助手界面
   */
  openAssistant() {
    // 创建模态框
    new CNSHAssistantModal(this).open();
  }

  /**
   * 添加命令
   */
  addCommands() {
    // 连接到 CNSH
    this.addCommand({
      id: 'cnsh-connect',
      name: '连接到 CNSH 服务',
      checkCallback: (checking) => {
        if (!this.isServiceConnected) {
          if (!checking) {
            this.connectToCNSH();
          }
          return true;
        }
        return false;
      }
    });
    
    // 断开 CNSH 连接
    this.addCommand({
      id: 'cnsh-disconnect',
      name: '断开 CNSH 连接',
      checkCallback: (checking) => {
        if (this.isServiceConnected) {
          if (!checking) {
            this.isServiceConnected = false;
            if (this.settings.showNotifications) {
              new Notice('已断开 CNSH 连接');
            }
          }
          return true;
        }
        return false;
      }
    });
    
    // 同步库到 CNSH
    this.addCommand({
      id: 'cnsh-sync-vault',
      name: '同步当前库到 CNSH',
      callback: () => {
        if (this.isServiceConnected) {
          this.syncVault();
        } else {
          new Notice('请先连接到 CNSH 服务');
        }
      }
    });
    
    // 智能标记当前文件
    this.addCommand({
      id: 'cnsh-auto-tag',
      name: '智能标记当前文件',
      editorCallback: (editor, view) => {
        if (!this.isServiceConnected) {
          new Notice('请先连接到 CNSH 服务');
          return;
        }
        
        const file = view.file;
        const content = editor.getValue();
        
        this.generateTags(content).then(tags => {
          // 更新文件的 frontmatter
          const fileCache = this.app.metadataCache.getFileCache(file);
          const frontmatter = fileCache?.frontmatter || {};
          
          // 合并新标签，避免重复
          const existingTags = frontmatter.tags || [];
          const newTags = tags.filter(tag => !existingTags.includes(tag));
          
          if (newTags.length > 0) {
            this.app.fileManager.processFrontMatter(file, frontmatter => {
              frontmatter.tags = [...existingTags, ...newTags];
            });
            
            if (this.settings.showNotifications) {
              new Notice(`已添加标签: ${newTags.join(', ')}`);
            }
          } else {
            if (this.settings.showNotifications) {
              new Notice('未找到合适的标签');
            }
          }
        }).catch(error => {
          console.error('Failed to generate tags:', error);
          new Notice(`生成标签失败: ${error.message}`);
        });
      }
    });
    
    // 生成摘要
    this.addCommand({
      id: 'cnsh-generate-summary',
      name: '生成当前文件摘要',
      editorCallback: (editor, view) => {
        if (!this.isServiceConnected) {
          new Notice('请先连接到 CNSH 服务');
          return;
        }
        
        const content = editor.getValue();
        
        this.generateSummary(content).then(summary => {
          // 在文件开头插入摘要
          const summaryMarkdown = `> ${summary}\n\n`;
          editor.replaceRange(summaryMarkdown, { line: 0, ch: 0 });
          
          if (this.settings.showNotifications) {
            new Notice('摘要已生成并插入');
          }
        }).catch(error => {
          console.error('Failed to generate summary:', error);
          new Notice(`生成摘要失败: ${error.message}`);
        });
      }
    });
  }

  /**
   * 添加编辑器上下文菜单
   */
  addEditorMenu() {
    // 注册编辑器菜单项
    this.registerEvent(
      this.app.workspace.on('editor-menu', (menu, editor, view) => {
        menu.addItem((item) => {
          item.setTitle('智能标记')
            .setIcon('tag')
            .onClick(async () => {
              const file = view.file;
              const content = editor.getValue();
              
              try {
                const tags = await this.generateTags(content);
                
                // 更新文件的 frontmatter
                this.app.fileManager.processFrontMatter(file, frontmatter => {
                  const existingTags = frontmatter.tags || [];
                  const newTags = tags.filter(tag => !existingTags.includes(tag));
                  frontmatter.tags = [...existingTags, ...newTags];
                });
                
                if (this.settings.showNotifications) {
                  new Notice(`已添加标签: ${newTags.join(', ')}`);
                }
              } catch (error) {
                console.error('Failed to generate tags:', error);
                new Notice(`生成标签失败: ${error.message}`);
              }
            });
        });
        
        menu.addItem((item) => {
          item.setTitle('生成摘要')
            .setIcon('file-plus')
            .onClick(async () => {
              const content = editor.getValue();
              
              try {
                const summary = await this.generateSummary(content);
                const summaryMarkdown = `> ${summary}\n\n`;
                editor.replaceRange(summaryMarkdown, { line: 0, ch: 0 });
                
                if (this.settings.showNotifications) {
                  new Notice('摘要已生成并插入');
                }
              } catch (error) {
                console.error('Failed to generate summary:', error);
                new Notice(`生成摘要失败: ${error.message}`);
              }
            });
        });
      })
    );
  }

  /**
   * 生成标签
   */
  async generateTags(content) {
    try {
      const response = await this.cnshService.generateResponse(
        `请为以下内容生成3-5个合适的标签，只返回标签列表，用逗号分隔：\n\n${content}`
      );
      
      // 解析响应
      const tags = response.split(',').map(tag => tag.trim()).filter(tag => tag);
      return tags;
    } catch (error) {
      console.error('Error generating tags:', error);
      throw error;
    }
  }

  /**
   * 生成摘要
   */
  async generateSummary(content) {
    try {
      const response = await this.cnshService.generateResponse(
        `请为以下内容生成一个简短的摘要：\n\n${content}`
      );
      
      return response;
    } catch (error) {
      console.error('Error generating summary:', error);
      throw error;
    }
  }
}

// CNSH HTTP 服务类
class CNSHHttpService {
  constructor(settings) {
    this.serverUrl = settings.serverUrl;
    this.apiToken = settings.apiToken;
    this.model = settings.model;
  }

  /**
   * 测试连接
   */
  async testConnection() {
    const response = await this.request('/health');
    return response;
  }

  /**
   * 上传文件
   */
  async uploadFile(filePath, content) {
    return this.request('/api/obsidian/upload', {
      method: 'POST',
      body: JSON.stringify({ filePath, content })
    });
  }

  /**
   * 生成响应
   */
  async generateResponse(prompt) {
    return this.request('/api/ollama/generate', {
      method: 'POST',
      body: JSON.stringify({
        prompt,
        options: {
          model: this.model
        }
      })
    }).then(response => response.result);
  }

  /**
   * 发送 HTTP 请求
   */
  async request(endpoint, options = {}) {
    const url = `${this.serverUrl}${endpoint}`;
    const defaultOptions = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    };
    
    if (this.apiToken) {
      defaultOptions.headers['Authorization'] = `Bearer ${this.apiToken}`;
    }
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
      const response = await fetch(url, finalOptions);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || 'Request failed');
      }
      
      return data;
    } catch (error) {
      console.error(`Request failed: ${endpoint}`, error);
      throw error;
    }
  }
}

// CNSH 助手模态框
class CNSHAssistantModal extends require('obsidian').Modal {
  constructor(plugin) {
    super(plugin.app);
    this.plugin = plugin;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.createEl('h2', { text: 'CNSH 助手' });
    
    // 创建聊天界面
    const chatContainer = contentEl.createDiv({ cls: 'cnsh-chat-container' });
    
    // 消息容器
    const messagesContainer = chatContainer.createDiv({ cls: 'cnsh-messages' });
    
    // 输入框和按钮
    const inputContainer = chatContainer.createDiv({ cls: 'cnsh-input-container' });
    const input = inputContainer.createEl('textarea', { 
      placeholder: '输入您的问题...',
      cls: 'cnsh-input'
    });
    
    const sendButton = inputContainer.createEl('button', { text: '发送', cls: 'cnsh-send-button' });
    
    // 发送消息
    const sendMessage = async () => {
      const message = input.value.trim();
      if (!message) return;
      
      // 显示用户消息
      const userMessage = messagesContainer.createDiv({ cls: 'cnsh-message cnsh-user-message' });
      userMessage.createDiv({ text: message });
      
      // 清空输入框
      input.value = '';
      
      try {
        // 生成响应
        const response = await this.plugin.cnshService.generateResponse(message);
        
        // 显示助手响应
        const assistantMessage = messagesContainer.createDiv({ cls: 'cnsh-message cnsh-assistant-message' });
        assistantMessage.createDiv({ text: response });
        
        // 滚动到底部
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      } catch (error) {
        const errorMessage = messagesContainer.createDiv({ cls: 'cnsh-message cnsh-error-message' });
        errorMessage.createDiv({ text: `错误: ${error.message}` });
      }
    };
    
    sendButton.onclick = sendMessage;
    input.onkeydown = (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    };
    
    // 添加样式
    const style = document.createElement('style');
    style.textContent = `
      .cnsh-chat-container {
        display: flex;
        flex-direction: column;
        height: 500px;
        border: 1px solid var(--background-modifier-border);
        border-radius: 5px;
        overflow: hidden;
      }
      
      .cnsh-messages {
        flex: 1;
        overflow-y: auto;
        padding: 10px;
        background-color: var(--background-primary);
      }
      
      .cnsh-message {
        margin-bottom: 10px;
        padding: 8px 12px;
        border-radius: 5px;
        max-width: 80%;
      }
      
      .cnsh-user-message {
        background-color: var(--interactive-accent);
        color: var(--text-on-accent);
        margin-left: auto;
      }
      
      .cnsh-assistant-message {
        background-color: var(--background-secondary);
      }
      
      .cnsh-error-message {
        background-color: var(--color-red);
        color: var(--text-on-accent);
      }
      
      .cnsh-input-container {
        display: flex;
        padding: 10px;
        background-color: var(--background-secondary);
        border-top: 1px solid var(--background-modifier-border);
      }
      
      .cnsh-input {
        flex: 1;
        padding: 8px 12px;
        border: 1px solid var(--background-modifier-border);
        border-radius: 3px;
        background-color: var(--background-primary);
        color: var(--text-normal);
        resize: none;
        min-height: 36px;
      }
      
      .cnsh-send-button {
        margin-left: 10px;
        padding: 8px 16px;
        background-color: var(--interactive-accent);
        color: var(--text-on-accent);
        border: none;
        border-radius: 3px;
        cursor: pointer;
      }
      
      .cnsh-send-button:hover {
        background-color: var(--interactive-accent-hover);
      }
    `;
    document.head.appendChild(style);
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}

// 设置选项卡
class CNSHSettingTab extends require('obsidian').PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display() {
    const { containerEl } = this;
    containerEl.empty();
    
    containerEl.createEl('h2', { text: 'CNSH 连接器设置' });
    
    // 服务器 URL
    new require('obsidian').Setting(containerEl)
      .setName('服务器地址')
      .setDesc('CNSH 服务器地址')
      .addText(text => {
        text
          .setPlaceholder('http://localhost:3000')
          .setValue(this.plugin.settings.serverUrl)
          .onChange(async (value) => {
            this.plugin.settings.serverUrl = value;
            await this.plugin.saveSettings();
          });
      });
    
    // API 密钥
    new require('obsidian').Setting(containerEl)
      .setName('API 密钥')
      .setDesc('CNSH API 密钥（可选）')
      .addText(text => {
        text
          .setPlaceholder('API 密钥')
          .setValue(this.plugin.settings.apiToken)
          .onChange(async (value) => {
            this.plugin.settings.apiToken = value;
            await this.plugin.saveSettings();
          });
      });
    
    // 模型
    new require('obsidian').Setting(containerEl)
      .setName('模型')
      .setDesc('使用的大模型')
      .addText(text => {
        text
          .setPlaceholder('qwen:7b-chat')
          .setValue(this.plugin.settings.model)
          .onChange(async (value) => {
            this.plugin.settings.model = value;
            await this.plugin.saveSettings();
          });
      });
    
    // 自动标记
    new require('obsidian').Setting(containerEl)
      .setName('自动标记')
      .setDesc('自动为笔记生成标签')
      .addToggle(toggle => {
        toggle
          .setValue(this.plugin.settings.autoTag)
          .onChange(async (value) => {
            this.plugin.settings.autoTag = value;
            await this.plugin.saveSettings();
          });
      });
    
    // 显示通知
    new require('obsidian').Setting(containerEl)
      .setName('显示通知')
      .setDesc('显示操作成功/失败的通知')
      .addToggle(toggle => {
        toggle
          .setValue(this.plugin.settings.showNotifications)
          .onChange(async (value) => {
            this.plugin.settings.showNotifications = value;
            await this.plugin.saveSettings();
          });
      });
  }
}

module.exports = CNSHConnectorPlugin;