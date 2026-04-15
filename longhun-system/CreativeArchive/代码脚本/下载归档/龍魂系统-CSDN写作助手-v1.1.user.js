// ==UserScript==
// @name         龍魂系统·CSDN写作助手 MVP v1.1
// @namespace    https://uid9622.longhun.ai/
// @version      1.1
// @description  龍魂系统MVP：自动检查繁简体、添加DNA追溯码、龍魂签名（修复版）
// @author       诸葛鑫 (UID9622) + Claude (AI辅助)
// @match        https://editor.csdn.net/*
// @match        https://mp.csdn.net/*
// @grant        none
// @run-at       document-end
// ==/UserScript==

/*
 * 龍魂系统·CSDN写作助手 MVP v1.1（修复版）
 * DNA追溯码: #龍芯⚡️2026-03-17-油猴脚本-CSDN助手-MVP-v1.1
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 * GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 * 作者: 诸葛鑫 (UID9622) - 初中文化，退伍军人
 * AI辅助: Claude (Anthropic)
 */

(function() {
    "use strict";
    console.log("🐉 龍魂系统·CSDN助手 MVP v1.1 启动！");

    var CONFIG = {
        author: "诸葛鑫 (UID9622)",
        gpg: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        confirmCode: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        checkInterval: 3000
    };

    function generateDNA() {
        var now = new Date();
        var y = now.getFullYear();
        var m = String(now.getMonth() + 1).padStart(2, "0");
        var d = String(now.getDate()).padStart(2, "0");
        var dateStr = y + "-" + m + "-" + d;
        var topic = prompt("请输入文章主题（用于DNA追溯码）:", "文章主题");
        if (!topic) return null;
        var serial = Math.floor(Math.random() * 999) + 1;
        var serialStr = String(serial).padStart(3, "0");
        return "#龍芯⚡️" + dateStr + "-" + topic + "-" + serialStr;
    }

    function generateSignature() {
        var dna = generateDNA();
        if (!dna) return null;
        var sig = "\n---\n\n";
        sig += "DNA追溯码: " + dna + "  \n";
        sig += "确认码: " + CONFIG.confirmCode + "  \n";
        sig += "GPG指纹: " + CONFIG.gpg + "  \n";
        sig += "作者: " + CONFIG.author + " - 初中文化，退伍军人  \n";
        sig += "AI辅助: Claude (Anthropic)  \n";
        sig += "龍魂系统: 让所有无知的人安心 🐉  \n";
        sig += "北辰老兵致敬！ 🫡\n";
        return sig;
    }

    function getEditorContent() {
        var selectors = ["textarea.editor__inner", ".CodeMirror", "#md-editor", "textarea", '[contenteditable="true"]'];
        for (var i = 0; i < selectors.length; i++) {
            var element = document.querySelector(selectors[i]);
            if (element) return element;
        }
        return null;
    }

    function insertText(text) {
        var editor = getEditorContent();
        if (!editor) { alert("⚠️ 未找到编辑器，请确保在CSDN编辑页面"); return; }
        if (editor.value !== undefined && editor.tagName === "TEXTAREA") {
            var cursorPos = editor.selectionStart;
            var textBefore = editor.value.substring(0, cursorPos);
            var textAfter = editor.value.substring(cursorPos);
            editor.value = textBefore + text + textAfter;
            editor.selectionStart = editor.selectionEnd = cursorPos + text.length;
            editor.dispatchEvent(new Event("input", { bubbles: true }));
        } else {
            editor.focus();
            document.execCommand("insertText", false, text);
        }
        showNotification("✅ 已插入内容！", "success");
    }

    function showNotification(message, type) {
        type = type || "info";
        var notification = document.getElementById("longhun-notification");
        if (!notification) return;
        var colors = { info: "#4CAF50", warning: "#FF9800", success: "#2196F3", error: "#F44336" };
        notification.style.backgroundColor = colors[type] || colors.info;
        notification.querySelector(".longhun-notification-text").textContent = message;
        notification.classList.add("show");
        setTimeout(function() { notification.classList.remove("show"); }, 4000);
    }

    function checkAndReplaceText() {
        var editor = getEditorContent();
        if (!editor) return;
        var content = editor.value || editor.innerText || editor.textContent;
        var matches = content.match(/龍/g);
        var dragonCount = matches ? matches.length : 0;
        if (dragonCount > 0) {
            showNotification("⚠️ 检测到 " + dragonCount + " 个简体龍，建议替换为繁体龍", "warning");
        }
    }

    function addStyles() {
        var style = document.createElement("style");
        style.id = "longhun-styles";
        style.textContent = "#longhun-toolbar { position: fixed; right: 20px; bottom: 20px; width: 180px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); z-index: 99999; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; transition: all 0.3s ease; } #longhun-toolbar.collapsed { width: 50px; height: 50px; overflow: hidden; } #longhun-toolbar.collapsed .longhun-toolbar-content { display: none; } #longhun-toolbar.collapsed .longhun-title { display: none; } .longhun-toolbar-header { display: flex; align-items: center; justify-content: space-between; padding: 12px; color: white; cursor: move; user-select: none; } .longhun-logo { font-size: 20px; } .longhun-title { font-size: 14px; font-weight: bold; flex: 1; margin-left: 8px; } .longhun-collapse { background: rgba(255,255,255,0.2); border: none; color: white; width: 24px; height: 24px; border-radius: 4px; cursor: pointer; font-size: 16px; line-height: 1; } .longhun-collapse:hover { background: rgba(255,255,255,0.3); } .longhun-toolbar-content { padding: 0 12px 12px 12px; } .longhun-btn { width: 100%; padding: 10px; margin-bottom: 8px; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500; transition: all 0.2s; color: white; } .longhun-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); } .longhun-btn-primary { background: #4CAF50; } .longhun-btn-success { background: #2196F3; } .longhun-btn-warning { background: #FF9800; } .longhun-info { text-align: center; color: rgba(255,255,255,0.7); margin-top: 8px; font-size: 11px; } #longhun-notification { position: fixed; top: 20px; right: 20px; padding: 16px 24px; background: #4CAF50; color: white; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.2); z-index: 100000; transform: translateX(400px); transition: transform 0.3s ease; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; font-size: 14px; max-width: 300px; } #longhun-notification.show { transform: translateX(0); } .longhun-notification-text { display: block; }";
        document.head.appendChild(style);
    }

    function createNotification() {
        var notification = document.createElement("div");
        notification.id = "longhun-notification";
        notification.innerHTML = '<span class="longhun-notification-text"></span>';
        document.body.appendChild(notification);
    }

    function createFloatingToolbar() {
        var toolbar = document.createElement("div");
        toolbar.id = "longhun-toolbar";
        var html = '<div class="longhun-toolbar-header">';
        html += '<span class="longhun-logo">🐉</span>';
        html += '<span class="longhun-title">龍魂助手</span>';
        html += '<button class="longhun-collapse" id="longhun-collapse">_</button>';
        html += '</div>';
        html += '<div class="longhun-toolbar-content" id="longhun-content">';
        html += '<button class="longhun-btn longhun-btn-primary" id="longhun-add-dna">⚡ 添加DNA</button>';
        html += '<button class="longhun-btn longhun-btn-success" id="longhun-add-signature">🫡 龍魂签名</button>';
        html += '<button class="longhun-btn longhun-btn-warning" id="longhun-replace-dragon">🔄 龍→龍</button>';
        html += '<div class="longhun-info"><small>UID9622 · MVP v1.1</small></div>';
        html += '</div>';
        toolbar.innerHTML = html;
        document.body.appendChild(toolbar);
        addStyles();
        bindToolbarEvents();
    }

    function bindToolbarEvents() {
        document.getElementById("longhun-collapse").addEventListener("click", function() {
            var toolbar = document.getElementById("longhun-toolbar");
            toolbar.classList.toggle("collapsed");
            document.getElementById("longhun-collapse").textContent = toolbar.classList.contains("collapsed") ? "+" : "_";
        });
        document.getElementById("longhun-add-dna").addEventListener("click", function() {
            var dna = generateDNA();
            if (dna) { insertText("**DNA追溯码**: " + dna + "\n"); }
        });
        document.getElementById("longhun-add-signature").addEventListener("click", function() {
            var signature = generateSignature();
            if (signature) { insertText(signature); }
        });
        document.getElementById("longhun-replace-dragon").addEventListener("click", function() {
            var editor = getEditorContent();
            if (!editor) { alert("⚠️ 未找到编辑器"); return; }
            var content = editor.value || editor.innerText || editor.textContent;
            var matches = content.match(/龍/g);
            var originalCount = matches ? matches.length : 0;
            content = content.replace(/龍/g, "龍");
            if (editor.value !== undefined && editor.tagName === "TEXTAREA") {
                editor.value = content;
                editor.dispatchEvent(new Event("input", { bubbles: true }));
            } else { editor.innerText = content; }
            if (originalCount > 0) { showNotification("✅ 已替换 " + originalCount + " 个龍→龍", "success"); }
            else { showNotification("ℹ️ 未发现需要替换的简体龍", "info"); }
        });
        makeDraggable(document.getElementById("longhun-toolbar"));
    }

    function makeDraggable(element) {
        var isDragging = false, currentX, currentY, initialX, initialY, xOffset = 0, yOffset = 0;
        var header = element.querySelector(".longhun-toolbar-header");
        header.addEventListener("mousedown", function(e) {
            if (e.target.classList.contains("longhun-collapse")) return;
            initialX = e.clientX - xOffset; initialY = e.clientY - yOffset; isDragging = true;
        });
        document.addEventListener("mousemove", function(e) {
            if (isDragging) {
                e.preventDefault(); currentX = e.clientX - initialX; currentY = e.clientY - initialY;
                xOffset = currentX; yOffset = currentY;
                element.style.transform = "translate3d(" + currentX + "px, " + currentY + "px, 0)";
            }
        });
        document.addEventListener("mouseup", function() { initialX = currentX; initialY = currentY; isDragging = false; });
    }

    function init() {
        if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", init); return; }
        console.log("🐉 龍魂系统初始化中...");
        createFloatingToolbar();
        createNotification();
        setTimeout(function() { showNotification("🐉 龍魂系统·CSDN助手已启动！", "success"); }, 1000);
        setInterval(checkAndReplaceText, CONFIG.checkInterval);
        console.log("✅ 龍魂系统初始化完成！");
    }

    init();
})();