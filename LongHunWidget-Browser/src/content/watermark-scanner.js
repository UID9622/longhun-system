/**
 * 🐉 龍魂宝宝·DNA追溯助手 · 水印嵌入器
 * DNA: #龍芯⚡️20260525|WATERMARK-SCANNER|v1.0|xxxxx
 *
 * 職責：
 * ① 檢測平台編輯器（CSDN、知乎、掘金）
 * ② 攔截發佈按鈕事件
 * ③ 自動調用 Step 1 流水線
 * ④ 嵌入 DNA 簽名並發佈
 */

const UID9622 = "9622";
const CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";
const API_ENDPOINT = "http://localhost:5000";

// ========== 平台檢測 ==========

class PlatformDetector {
  constructor() {
    this.platform = this.detectPlatform();
    this.editor = null;
    this.publishBtn = null;
  }

  detectPlatform() {
    const hostname = window.location.hostname;

    if (hostname.includes('csdn.net')) return 'CSDN';
    if (hostname.includes('zhihu.com')) return '知乎';
    if (hostname.includes('juejin.cn')) return '掘金';
    if (hostname.includes('github.com')) return 'GitHub';
    if (hostname.includes('medium.com')) return 'Medium';

    return null;
  }

  initializePlatform() {
    if (!this.platform) {
      console.log('⚠️ 不支持的平台');
      return false;
    }

    console.log(`🔍 檢測到平台: ${this.platform}`);

    switch (this.platform) {
      case 'CSDN':
        return this.initCSND();
      case '知乎':
        return this.initZhihu();
      case '掘金':
        return this.initJuejin();
      default:
        return false;
    }
  }

  // ========== CSDN 編輯器 ==========

  initCSND() {
    // CSDN 使用 MDEditor（自定義編輯器）或 CodeMirror

    // 方法 1：檢測發佈按鈕（右上角）
    // CSDN 發佈按鈕 CSS: .write-btn-container .publish-btn
    this.publishBtn = document.querySelector(
      '.write-btn-container .publish-btn,' +
      '[data-testid="publish-button"],' +
      'button[title*="發佈"],' +
      'button:contains("發佈")'
    );

    // 方法 2：檢測編輯區域
    // CSDN MDEditor 容器: #ace-editor 或 .md-editor
    this.editor = document.querySelector(
      '#ace-editor,' +
      '.md-editor,' +
      '.ace_editor,' +
      '[contenteditable="true"]'
    );

    if (this.publishBtn) {
      console.log('✅ CSDN 發佈按鈕已找到');
      this.hookPublishButton();
      return true;
    } else {
      console.log('⚠️ CSDN 發佈按鈕未找到（可能在不同編輯模式）');
      return false;
    }
  }

  // ========== 知乎編輯器 ==========

  initZhihu() {
    // 知乎使用 Draft.js 編輯器

    // 方法 1：檢測發佈按鈕
    // 知乎發佈按鈕: .ContentCreation-button-publish
    this.publishBtn = document.querySelector(
      '.ContentCreation-button-publish,' +
      'button[aria-label*="發佈"],' +
      'button[data-tooltip*="發佈"],' +
      'button:contains("發佈")'
    );

    // 方法 2：檢測編輯區域
    // 知乎編輯器: .DraftEditor-root
    this.editor = document.querySelector(
      '.DraftEditor-root,' +
      '.RichText,' +
      '[contenteditable="true"],' +
      '.editor-container'
    );

    if (this.publishBtn) {
      console.log('✅ 知乎發佈按鈕已找到');
      this.hookPublishButton();
      return true;
    } else {
      console.log('⚠️ 知乎發佈按鈕未找到（可能需要滾動頁面）');
      return false;
    }
  }

  // ========== 掘金編輯器 ==========

  initJuejin() {
    // 掘金使用 Monaco Editor（VS Code 編輯器）

    // 方法 1：檢測發佈按鈕
    // 掘金發佈按鈕: .editor-header .publish-btn
    this.publishBtn = document.querySelector(
      '.editor-header .publish-btn,' +
      'button[title="發佈"],' +
      'button.el-button--primary:contains("發佈"),' +
      'button:contains("發表")'
    );

    // 方法 2：檢測編輯區域
    // 掘金編輯器: .monaco-editor
    this.editor = document.querySelector(
      '.monaco-editor,' +
      '.monaco-editor-container,' +
      '.editor-container'
    );

    if (this.publishBtn) {
      console.log('✅ 掘金發佈按鈕已找到');
      this.hookPublishButton();
      return true;
    } else {
      console.log('⚠️ 掘金發佈按鈕未找到（可能在不同頁面）');
      return false;
    }
  }

  // ========== 通用鉤子方法 ==========

  hookPublishButton() {
    if (!this.publishBtn) return;

    // 保存原始點擊處理器
    const originalHandler = this.publishBtn.onclick;

    // 監聽點擊事件
    this.publishBtn.addEventListener('click', async (event) => {
      console.log('🎯 檢測到發佈操作');

      // 攔截發佈
      event.preventDefault();
      event.stopPropagation();

      // 執行 DNA 嵌入流程
      await this.executePublishWithWatermark();
    }, true); // 捕獲階段

    // 也監聽鍵盤快捷鍵（Ctrl+Enter）
    document.addEventListener('keydown', async (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        const inEditor = this.isInEditorContext();
        if (inEditor) {
          console.log('⌨️ 檢測到快捷鍵發佈 (Ctrl+Enter)');
          event.preventDefault();
          await this.executePublishWithWatermark();
        }
      }
    });

    console.log('🔗 已連接發佈攔截器');
  }

  // ========== 獲取內容 ==========

  getEditorContent() {
    if (!this.editor) {
      console.warn('⚠️ 編輯器不存在');
      return '';
    }

    // 方法 1：contenteditable
    if (this.editor.contentEditable === 'true') {
      return this.editor.innerText || this.editor.textContent;
    }

    // 方法 2：textarea
    if (this.editor.tagName === 'TEXTAREA') {
      return this.editor.value;
    }

    // 方法 3：Monaco/CodeMirror 編輯器
    if (window.editor && window.editor.getValue) {
      return window.editor.getValue();
    }

    // 方法 4：Draft.js
    if (window.draftEditorState) {
      return this.getDraftJSContent();
    }

    // 方法 5：ACE 編輯器
    if (window.ace && window.aceEditor) {
      return window.aceEditor.getValue();
    }

    console.warn('⚠️ 無法獲取編輯器內容（編輯器類型未知）');
    return '';
  }

  getDraftJSContent() {
    // 嘗試從 Draft.js 狀態中提取文本
    // 這需要特定於應用的方法
    try {
      const contentState = window.draftEditorState?.getCurrentContent?.();
      if (contentState) {
        return contentState.getPlainText?.();
      }
    } catch (e) {
      console.error('解析 Draft.js 失敗:', e);
    }
    return '';
  }

  getEditorTitle() {
    // 嘗試從頁面或編輯器獲取標題
    const titleInputs = document.querySelectorAll(
      'input[placeholder*="標題"],' +
      'input[placeholder*="Title"],' +
      'input[type="text"]:first-of-type'
    );

    if (titleInputs.length > 0) {
      return titleInputs[0].value || '未命名文章';
    }

    // 備用：從頁面標題
    return document.title.split('|')[0].trim() || '未命名文章';
  }

  isInEditorContext() {
    const activeElement = document.activeElement;
    if (!activeElement) return false;

    // 檢查焦點是否在編輯區域或相關元素
    return (
      activeElement.contentEditable === 'true' ||
      activeElement.tagName === 'TEXTAREA' ||
      activeElement.classList.contains('editor') ||
      activeElement.classList.contains('monaco-editor') ||
      this.editor?.contains(activeElement)
    );
  }

  // ========== Step 1 執行 ==========

  async executePublishWithWatermark() {
    console.log('🚀 開始 Step 1 流水線...');

    try {
      // 1. 獲取內容
      const content = this.getEditorContent();
      const title = this.getEditorTitle();

      if (!content.trim()) {
        console.warn('⚠️ 編輯器內容為空');
        return;
      }

      console.log(`📝 內容長度: ${content.length} 字符`);
      console.log(`📌 標題: ${title}`);

      // 2. 嘗試調用本地 API，如果失敗則使用離線模式
      let dna = null;

      try {
        const dnaResponse = await fetch(`${API_ENDPOINT}/dna/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            topic: title.toUpperCase().replace(/\s+/g, '-'),
            platform: this.platform,
            uid: UID9622,
            content_length: content.length
          }),
          timeout: 5000
        });

        if (dnaResponse.ok) {
          const dnaData = await dnaResponse.json();
          dna = dnaData.dna;
          console.log(`✅ API 生成 DNA: ${dna}`);
        }
      } catch (apiError) {
        console.warn('⚠️ API 不可用，使用離線模式生成 DNA');
        dna = this.generateOfflineDNA(title);
      }

      if (!dna) {
        console.error('❌ DNA 生成失敗');
        this.triggerPublish();
        return;
      }

      // 3. 嵌入 DNA 到內容
      const watermarkedContent = this.embedDNAToContent(content, dna);

      // 4. 更新編輯器內容
      this.setEditorContent(watermarkedContent);

      // 5. 發送給 background script 記錄
      await this.notifyBackgroundScript(dna, title, content.length);

      // 6. 發送登記郵件
      await this.sendRegistrationEmail(dna, title);

      // 7. 觸發實際發佈
      this.triggerPublish();

      console.log('🎉 Step 1 完成，發佈已執行');

    } catch (error) {
      console.error('❌ Step 1 執行失敗:', error);
      // 失敗時仍然發佈（不阻止用戶發佈）
      this.triggerPublish();
    }
  }

  generateOfflineDNA(title) {
    // 離線模式：生成臨時 DNA（實際簽名由 background script 負責）
    const today = new Date().toISOString().replace(/-/g, '').slice(0, 8);
    const topic = title.toUpperCase().replace(/\s+/g, '-').slice(0, 20);
    const randomSha8 = Math.random().toString(16).slice(2, 10);
    return `#龍芯⚡️${today}|${topic}|v1.0|${randomSha8}`;
  }

  async notifyBackgroundScript(dna, title, contentLength) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({
        action: 'dna_embedded',
        dna: dna,
        title: title,
        platform: this.platform,
        content_length: contentLength,
        timestamp: new Date().toISOString()
      }, (response) => {
        if (response && response.success) {
          console.log('✅ Background script 已記錄 DNA');
          resolve();
        } else {
          console.warn('⚠️ Background script 回應失敗');
          resolve();
        }
      });
    });
  }

  embedDNAToContent(content, dna) {
    // 在內容末尾添加 DNA 簽名
    const dnaSignature = `\n\n---\n**DNA簽名**: ${dna}\n*此內容已被 龍魂 DNA 追溯系統自動簽名*\n`;
    return content + dnaSignature;
  }

  setEditorContent(newContent) {
    if (!this.editor) return false;

    // 方法 1：contenteditable
    if (this.editor.contentEditable === 'true') {
      this.editor.innerText = newContent;
      this.editor.textContent = newContent;
      return true;
    }

    // 方法 2：textarea
    if (this.editor.tagName === 'TEXTAREA') {
      this.editor.value = newContent;
      // 觸發輸入事件
      this.editor.dispatchEvent(new Event('input', { bubbles: true }));
      return true;
    }

    // 方法 3：Monaco/CodeMirror
    if (window.editor && window.editor.setValue) {
      window.editor.setValue(newContent);
      return true;
    }

    console.warn('⚠️ 無法更新編輯器內容');
    return false;
  }

  async sendRegistrationEmail(dna, title) {
    try {
      await fetch(`${API_ENDPOINT}/dna/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dna: dna,
          title: title,
          platform: this.platform,
          uid: UID9622,
          timestamp: new Date().toISOString()
        })
      });

      console.log('📧 登記郵件已發送');
    } catch (error) {
      console.error('⚠️ 郵件發送失敗:', error);
      // 失敗不阻止流程
    }
  }

  triggerPublish() {
    // 觸發原始發佈按鈕點擊
    if (this.publishBtn) {
      // 移除事件監聽器防止無限循環
      const newBtn = this.publishBtn.cloneNode(true);
      this.publishBtn.parentNode.replaceChild(newBtn, this.publishBtn);

      // 模擬點擊
      newBtn.click();
      console.log('✅ 已觸發原始發佈');
    }
  }
}

// ========== 初始化 ==========

document.addEventListener('DOMContentLoaded', () => {
  const detector = new PlatformDetector();

  // 立即初始化
  detector.initializePlatform();

  // 監聽 DOM 變化（某些單頁應用可能動態加載編輯器）
  const observer = new MutationObserver(() => {
    if (!detector.publishBtn || !detector.editor) {
      detector.initializePlatform();
    }
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
    attributes: false
  });

  console.log('🐉 水印嵌入器已初始化');
});

// 頁面加載完成時再次檢查
window.addEventListener('load', () => {
  const detector = new PlatformDetector();
  detector.initializePlatform();
});

console.log('🐉 DNA 水印掃描器已加載');
