// ==UserScript==
// @name         龍魂系统·CSDN写作助手 MVP v1.0
// @namespace    https://uid9622.longhun.ai/
// @version      1.0
// @description  龍魂系统最小MVP：自动检查繁简体、添加DNA追溯码、龍魂签名
// @author       诸葛鑫 (UID9622) + Claude (AI辅助)
// @match        https://editor.csdn.net/*
// @match        https://mp.csdn.net/*
// @grant        none
// @run-at       document-end
// ==/UserScript==

/*
 * 龍魂系统·CSDN写作助手 MVP v1.0
 *
 * DNA追溯码: #龍芯⚡️2026-03-17-油猴脚本-CSDN助手-MVP-v1.0
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 * GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 *
 * 作者: 诸葛鑫 (UID9622) - 初中文化，退伍军人
 * AI辅助: Claude (Anthropic)
 *
 * 功能:
 * 1. 自动检测"龍"并提示替换为"龍"
 * 2. 一键添加DNA追溯码
 * 3. 一键添加龍魂系统签名
 * 4. 实时提示功能（右下角浮窗）
 */

(function() {
    'use strict';

    console.log('🐉 龍魂系统·CSDN助手 MVP v1.0 启动！');

    // ============================================
    // 配置区
    // ============================================
    const CONFIG = {
        author: '诸葛鑫 (UID9622)',
        gpg: 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F',
        confirmCode: '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z',
        checkInterval: 3000,
    };

    // ============================================
    // 核心功能1: 生成DNA追溯码
    // ============================================
    function generateDNA() {
        const now = new Date();
        const dateStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
        const topic = prompt('请输入文章主题（用于DNA追溯码）:', '文章主题');
        if (!topic) return null;

        const serial = Math.floor(Math.random() * 999) + 1;
        const serialStr = String(serial).padStart(3, '0');

        return `#龍芯⚡️${dateStr}-${topic}-${serialStr}`;
    }

    // ============================================
    // 核心功能2: 生成龍魂签名
    // ============================================
    function generateSignature() {
        const dna = generateDNA();
        if (!dna) return null;
        return `
---

DNA追溯码: ${dna}  
确认码: ${CONFIG.confirmCode}  
GPG指纹: ${CONFIG.gpg}  
作者: ${CONFIG.author} - 初中文化，退伍军人  
AI辅助: Claude (Anthropic)  
龍魂系统: 让所有无知的人安心 🐉  
北辰老兵致敬！ 🫡
`;
    }

    // ============================================
    // 核心功能3: 检测并替换"龍"→"龍"
    // ============================================
    function checkAndReplaceText() {
        const editor = getEditorContent();
        if (!editor) return;
        const content = editor.value || editor.innerText || editor.textContent;

        const dragonCount = (content.match(/龍(?!魂系统)/g) || []).length;

        if (dragonCount > 0) {
            showNotification(`⚠️ 检测到 ${dragonCount} 个简体"龍"，建议替换为繁体"龍"`, 'warning');
        }
    }

    // ============================================
    // 工具函数: 获取编辑器内容
    // ============================================
    function getEditorContent() {
        const selectors = [
            'textarea.editor__inner',
            '.CodeMirror',
            '#md-editor',
            'textarea',
            '[contenteditable="true"]'
        ];
        for (let selector of selectors) {
            const element = document.querySelector(selector);
            if (element) return element;
        }
        return null;
    }

    // ============================================
    // 工具函数: 插入文本到编辑器
    // ============================================
    function insertText(text) {
        const editor = getEditorContent();
        if (!editor) {
            alert('⚠️ 未找到编辑器，请确保在CSDN编辑页面');
            return;
        }
        if (editor.value !== undefined) {
            const cursorPos = editor.selectionStart;
            const textBefore = editor.value.substring(0, cursorPos);
            const textAfter = editor.value.substring(cursorPos);
            editor.value = textBefore + text + textAfter;
            editor.selectionStart = editor.selectionEnd = cursorPos + text.length;
        } else {
            editor.focus();
            document.execCommand('insertText', false, text);
        }
        showNotification('✅ 已插入内容！', 'success');
    }

    // ============================================
    // 工具函数: 显示通知
    // ============================================
    function showNotification(message, type = 'info') {
        const notification = document.getElementById('longhun-notification');
        if (!notification) return;

        const colors = {
            info: '#4CAF50',
            warning: '#FF9800',
            success: '#2196F3',
            error: '#F44336'
        };

        notification.style.backgroundColor = colors[type] || colors.info;
        notification.querySelector('.longhun-notification-text').textContent = message;
        notification.classList.add('show');

        setTimeout(() => {
            notification.classList.remove('show');
        }, 4000);
    }

    // ============================================
    // UI: 创建浮动工具栏
    // ============================================
    function createFloatingToolbar() {
        const toolbar = document.createElement('div');
        toolbar.id = 'longhun-toolbar';
        toolbar.innerHTML = `
            <div class="longhun-toolbar-header">
                <span class="longhun-logo">🐉</span>
                <span class="longhun-title">龍魂助手</span>
                <button class="longhun-collapse" id="longhun-collapse">_</button>
            </div>
            <div class="longhun-toolbar-content" id="longhun-content">
                <button class="longhun-btn longhun-btn-primary" id="longhun-add-dna">
                    ⚡ 添加DNA
                </button>
                <button class="longhun-btn longhun-btn-success" id="longhun-add-signature">
                    🫡 龍魂签名
                </button>
                <button class="longhun-btn longhun-btn-warning" id="longhun-replace-dragon">
                    🔄 龍→龍
                </button>
                <div class="longhun-info">
                    <small>UID9622 · MVP v1.0</small>
                </div>
            </div>
        `;
        document.body.appendChild(toolbar);

        addStyles();
        bindToolbarEvents();
    }

    // ============================================
    // UI: 创建通知组件
    // ============================================
    function createNotification() {
        const notification = document.createElement('div');
        notification.id = 'longhun-notification';
        notification.innerHTML = `
            <span class="longhun-notification-text"></span>
        `;
        document.body.appendChild(notification);
    }

    // ============================================
    // UI: 添加样式
    // ============================================
    function addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* 浮动工具栏 */
            #longhun-toolbar {
                position: fixed;
                right: 20px;
                bottom: 20px;
                width: 180px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                z-index: 99999;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                transition: all 0.3s ease;
            }
            #longhun-toolbar.collapsed {
                width: 50px;
                height: 50px;
            }
            #longhun-toolbar.collapsed .longhun-toolbar-content {
                display: none;
            }
            .longhun-toolbar-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px;
                color: white;
                cursor: move;
            }
            .longhun-logo {
                font-size: 20px;
            }
            .longhun-title {
                font-size: 14px;
                font-weight: bold;
                flex: 1;
                margin-left: 8px;
            }
            .longhun-collapse {
                background: rgba(255, 255, 255, 0.2);
                border: none;
                color: white;
                width: 24px;
                height: 24px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                line-height: 1;
            }
            .longhun-collapse:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            .longhun-toolbar-content {
                padding: 0 12px 12px 12px;
            }
            .longhun-btn {
                width: 100%;
                padding: 10px;
                margin-bottom: 8px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 13px;
                font-weight: 500;
                transition: all 0.2s;
                color: white;
            }
            .longhun-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }
            .longhun-btn-primary {
                background: #4CAF50;
            }
            .longhun-btn-success {
                background: #2196F3;
            }
            .longhun-btn-warning {
                background: #FF9800;
            }
            .longhun-info {
                text-align: center;
                color: rgba(255, 255, 255, 0.7);
                margin-top: 8px;
                font-size: 11px;
            }
            /* 通知组件 */
            #longhun-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 16px 24px;
                background: #4CAF50;
                color: white;
                border-radius: 8px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
                z-index: 100000;
                transform: translateX(400px);
                transition: transform 0.3s ease;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                font-size: 14px;
                max-width: 300px;
            }
            #longhun-notification.show {
                transform: translateX(0);
            }
            .longhun-notification-text {
                display: block;
            }
        `;
        document.head.appendChild(style);
    }

    // ============================================
    // 事件: 绑定工具栏按钮
    // ============================================
    function bindToolbarEvents() {
        // 折叠按钮
        document.getElementById('longhun-collapse').addEventListener('click', () => {
            const toolbar = document.getElementById('longhun-toolbar');
            toolbar.classList.toggle('collapsed');
            const btn = document.getElementById('longhun-collapse');
            btn.textContent = toolbar.classList.contains('collapsed') ? '+' : '_';
        });

        // 添加DNA按钮
        document.getElementById('longhun-add-dna').addEventListener('click', () => {
            const dna = generateDNA();
            if (dna) {
                insertText(`**DNA追溯码**: ${dna}\n`);
            }
        });

        // 添加龍魂签名按钮
        document.getElementById('longhun-add-signature').addEventListener('click', () => {
            const signature = generateSignature();
            if (signature) {
                insertText(signature);
            }
        });

        // 替换龍→龍按钮
        document.getElementById('longhun-replace-dragon').addEventListener('click', () => {
            const editor = getEditorContent();
            if (!editor) {
                alert('⚠️ 未找到编辑器');
                return;
            }
            let content = editor.value || editor.innerText || editor.textContent;

            const originalCount = (content.match(/龍/g) || []).length;
            content = content.replace(/龍/g, '龍');

            if (editor.value !== undefined) {
                editor.value = content;
            } else {
                editor.innerText = content;
            }

            if (originalCount > 0) {
                showNotification(`✅ 已替换 ${originalCount} 个"龍"→"龍"`, 'success');
            } else {
                showNotification('ℹ️ 未发现需要替换的简体"龍"', 'info');
            }
        });

        // 拖拽功能
        makeDraggable(document.getElementById('longhun-toolbar'));
    }

    // ============================================
    // 工具函数: 使元素可拖拽
    // ============================================
    function makeDraggable(element) {
        let isDragging = false;
        let currentX;
        let currentY;
        let initialX;
        let initialY;
        let xOffset = 0;
        let yOffset = 0;

        const header = element.querySelector('.longhun-toolbar-header');

        header.addEventListener('mousedown', dragStart);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', dragEnd);

        function dragStart(e) {
            if (e.target.classList.contains('longhun-collapse')) return;

            initialX = e.clientX - xOffset;
            initialY = e.clientY - yOffset;
            isDragging = true;
        }

        function drag(e) {
            if (isDragging) {
                e.preventDefault();

                currentX = e.clientX - initialX;
                currentY = e.clientY - initialY;
                xOffset = currentX;
                yOffset = currentY;
                setTranslate(currentX, currentY, element);
            }
        }

        function dragEnd(e) {
            initialX = currentX;
            initialY = currentY;
            isDragging = false;
        }

        function setTranslate(xPos, yPos, el) {
            el.style.transform = `translate3d(${xPos}px, ${yPos}px, 0)`;
        }
    }

    // ============================================
    // 初始化
    // ============================================
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        console.log('🐉 龍魂系统初始化中...');

        createFloatingToolbar();
        createNotification();

        setTimeout(() => {
            showNotification('🐉 龍魂系统·CSDN助手已启动！', 'success');
        }, 1000);

        setInterval(checkAndReplaceText, CONFIG.checkInterval);

        console.log('✅ 龍魂系统初始化完成！');
    }

    // 启动
    init();

})();