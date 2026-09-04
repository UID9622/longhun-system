// 龍魂系统 · 无障碍辅助脚本
// DNA: #龍芯⚡️丙午·甲申·丁未·丙午·䷝离为火-无障碍脚本-v1.0
// 功能: 字体缩放、高对比度、语音朗读、行距调整

(function() {
    'use strict';

    const html = document.documentElement;
    const body = document.body;
    let currentFontSize = 18;
    let currentLineHeight = 1.8;
    let speechSynth = window.speechSynthesis;
    let isSpeaking = false;

    // 字体缩放
    const btnFontLarge = document.getElementById('btn-font-large');
    const btnFontSmall = document.getElementById('btn-font-small');

    if (btnFontLarge) {
        btnFontLarge.addEventListener('click', () => {
            currentFontSize = Math.min(currentFontSize + 2, 32);
            html.style.fontSize = currentFontSize + 'px';
            announce('字体已增大到 ' + currentFontSize + ' 像素');
        });
    }

    if (btnFontSmall) {
        btnFontSmall.addEventListener('click', () => {
            currentFontSize = Math.max(currentFontSize - 2, 14);
            html.style.fontSize = currentFontSize + 'px';
            announce('字体已减小到 ' + currentFontSize + ' 像素');
        });
    }

    // 高对比度切换
    const btnContrast = document.getElementById('btn-contrast');
    if (btnContrast) {
        btnContrast.addEventListener('click', () => {
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'high-contrast' ? 'default' : 'high-contrast';
            body.setAttribute('data-theme', newTheme);
            announce(newTheme === 'high-contrast' ? '已切换到高对比度模式' : '已切换到默认模式');
        });
    }

    // 行距调整
    const btnLineHeight = document.getElementById('btn-line-height');
    if (btnLineHeight) {
        btnLineHeight.addEventListener('click', () => {
            currentLineHeight = currentLineHeight >= 2.2 ? 1.6 : currentLineHeight + 0.2;
            body.style.lineHeight = currentLineHeight;
            announce('行距已调整为 ' + Math.round(currentLineHeight * 10) / 10);
        });
    }

    // 语音朗读
    const btnVoice = document.getElementById('btn-voice');
    if (btnVoice && speechSynth) {
        btnVoice.addEventListener('click', () => {
            if (isSpeaking) {
                speechSynth.cancel();
                isSpeaking = false;
                btnVoice.setAttribute('aria-pressed', 'false');
                announce('朗读已停止');
            } else {
                const mainContent = document.querySelector('main');
                if (mainContent) {
                    const text = mainContent.textContent.substring(0, 5000); // 限制长度
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'zh-CN';
                    utterance.rate = 0.9;
                    utterance.pitch = 1;

                    utterance.onend = () => {
                        isSpeaking = false;
                        btnVoice.setAttribute('aria-pressed', 'false');
                    };

                    speechSynth.speak(utterance);
                    isSpeaking = true;
                    btnVoice.setAttribute('aria-pressed', 'true');
                    announce('开始朗读页面内容');
                }
            }
        });
    }

    // 屏幕阅读器播报辅助
    function announce(message) {
        const announcer = document.getElementById('sr-announcer') || createAnnouncer();
        announcer.textContent = message;
    }

    function createAnnouncer() {
        const div = document.createElement('div');
        div.id = 'sr-announcer';
        div.setAttribute('aria-live', 'polite');
        div.setAttribute('aria-atomic', 'true');
        div.style.cssText = 'position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden;';
        document.body.appendChild(div);
        return div;
    }

    // 键盘导航增强
    document.addEventListener('keydown', (e) => {
        // Alt + 1/2/3 快速跳转入口
        if (e.altKey) {
            switch(e.key) {
                case '1':
                    window.location.href = 'index.html';
                    break;
                case '2':
                    window.location.href = 'accessible.html';
                    break;
                case '3':
                    window.location.href = 'developer.html';
                    break;
            }
        }
    });

    // 保存用户偏好到 localStorage
    function savePreferences() {
        const prefs = {
            fontSize: currentFontSize,
            lineHeight: currentLineHeight,
            theme: body.getAttribute('data-theme')
        };
        localStorage.setItem('longhun-a11y-prefs', JSON.stringify(prefs));
    }

    // 加载用户偏好
    function loadPreferences() {
        try {
            const prefs = JSON.parse(localStorage.getItem('longhun-a11y-prefs'));
            if (prefs) {
                if (prefs.fontSize) {
                    currentFontSize = prefs.fontSize;
                    html.style.fontSize = currentFontSize + 'px';
                }
                if (prefs.lineHeight) {
                    currentLineHeight = prefs.lineHeight;
                    body.style.lineHeight = currentLineHeight;
                }
                if (prefs.theme) {
                    body.setAttribute('data-theme', prefs.theme);
                }
            }
        } catch (e) {
            console.log('无障碍偏好加载失败');
        }
    }

    // 页面加载时恢复偏好
    loadPreferences();

    // 页面卸载时保存偏好
    window.addEventListener('beforeunload', savePreferences);

    // 控制台 DNA 水印
    console.log('%c🐉 龍魂系统 · 无障碍版本', 'font-size: 20px; font-weight: bold; color: #0000ff;');
    console.log('%cDNA: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️', 'color: #000;');
})();
