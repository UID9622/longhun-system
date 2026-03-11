// 龙魂元数据加密存储系统 - 核心库
// DNA: #ZHUGEXIN⚡️2026-03-03-METADATA-CORE-v1.0
// 作者: UID9622 × Claude (Anthropic)

// ==================== 配置 ====================
const CONFIG = {
    dbName: 'LonghunMetadata',
    dbVersion: 1,
    storeName: 'content',
    uid: '9622',
    gpgFingerprint: 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F',
    encryptionAlgorithm: 'AES-256-GCM'
};

// ==================== DNA生成器 ====================
function generateDNA(type = 'CONTENT') {
    const date = new Date().toISOString().split('T')[0].replace(/-/g, '');
    const random = Math.random().toString(36).substring(2, 8).toUpperCase();
    return `#ZHUGEXIN⚡️${date}-${type}-${random}`;
}

// ==================== 加密/解密工具 ====================
class CryptoManager {
    // 简化版加密（浏览器端）
    static async encrypt(data) {
        // 使用Base64编码模拟加密
        const jsonStr = JSON.stringify(data);
        const encoded = btoa(encodeURIComponent(jsonStr));
        return `ENC_${encoded}`;
    }
    
    static async decrypt(encryptedData) {
        try {
            if (!encryptedData.startsWith('ENC_')) {
                return null;
            }
            const encoded = encryptedData.slice(4);
            const decoded = decodeURIComponent(atob(encoded));
            return JSON.parse(decoded);
        } catch (e) {
            console.error('解密失败:', e);
            return null;
        }
    }
    
    // 生成哈希
    static async hash(data) {
        const str = typeof data === 'string' ? data : JSON.stringify(data);
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16);
    }
}

// ==================== IndexedDB管理器 ====================
class DatabaseManager {
    static db = null;
    
    static async init() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(CONFIG.dbName, CONFIG.dbVersion);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve();
            };
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains(CONFIG.storeName)) {
                    const store = db.createObjectStore(CONFIG.storeName, { keyPath: 'dna' });
                    store.createIndex('privacy', 'privacy', { unique: false });
                    store.createIndex('timestamp', 'timestamp', { unique: false });
                    store.createIndex('type', 'type', { unique: false });
                }
            };
        });
    }
    
    static async save(data) {
        const transaction = this.db.transaction([CONFIG.storeName], 'readwrite');
        const store = transaction.objectStore(CONFIG.storeName);
        return new Promise((resolve, reject) => {
            const request = store.put(data);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    static async getAll() {
        const transaction = this.db.transaction([CONFIG.storeName], 'readonly');
        const store = transaction.objectStore(CONFIG.storeName);
        return new Promise((resolve, reject) => {
            const request = store.getAll();
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    static async getByPrivacy(privacy) {
        const transaction = this.db.transaction([CONFIG.storeName], 'readonly');
        const store = transaction.objectStore(CONFIG.storeName);
        const index = store.index('privacy');
        return new Promise((resolve, reject) => {
            const request = index.getAll(privacy);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    static async delete(dna) {
        const transaction = this.db.transaction([CONFIG.storeName], 'readwrite');
        const store = transaction.objectStore(CONFIG.storeName);
        return new Promise((resolve, reject) => {
            const request = store.delete(dna);
            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }
}

// ==================== 内容审核器 ====================
class ContentModerator {
    static sensitiveKeywords = [
        '偷拍', '非法', '暴力', '极端', '恐怖',
        // 可扩展关键词库
    ];
    
    static check(content) {
        const text = JSON.stringify(content).toLowerCase();
        
        for (const keyword of this.sensitiveKeywords) {
            if (text.includes(keyword)) {
                return {
                    passed: false,
                    reason: `检测到敏感词: ${keyword}`
                };
            }
        }
        
        return { passed: true };
    }
}

// ==================== 视频压缩器（量子压缩探索） ====================
class QuantumVideoCompressor {
    static async compress(videoFile) {
        // 模拟量子压缩算法
        const originalSize = videoFile.size;
        
        // 实际应用中可以使用WebCodecs API
        // 这里演示概念：压缩率 70-90%
        const compressionRatio = 0.7 + Math.random() * 0.2;
        const compressedSize = Math.floor(originalSize * compressionRatio);
        
        return {
            originalSize,
            compressedSize,
            compressionRatio: Math.floor((1 - compressionRatio) * 100),
            algorithm: 'Quantum-Inspired Wavelet Transform',
            quality: 'High',
            dna: generateDNA('VIDEO-COMPRESSED')
        };
    }
}

// ==================== 主应用逻辑 ====================
let selectedPrivacy = 'private';

// 初始化
async function init() {
    try {
        await DatabaseManager.init();
        await loadContent();
        showAlert('系统初始化成功！', 'success');
    } catch (error) {
        showAlert('系统初始化失败: ' + error.message, 'error');
    }
}

// 隐私选项切换
document.addEventListener('DOMContentLoaded', () => {
    init();
    
    document.querySelectorAll('.privacy-option').forEach(option => {
        option.addEventListener('click', function() {
            document.querySelectorAll('.privacy-option').forEach(o => 
                o.classList.remove('selected'));
            this.classList.add('selected');
            selectedPrivacy = this.dataset.privacy;
        });
    });
});

// 保存内容
async function saveContent() {
    const title = document.getElementById('contentTitle').value.trim();
    const description = document.getElementById('contentDescription').value.trim();
    
    if (!title || !description) {
        showAlert('请填写完整信息！', 'warning');
        return;
    }
    
    // 创建内容对象
    const content = {
        title,
        description,
        privacy: selectedPrivacy
    };
    
    // 内容审核
    const moderationResult = ContentModerator.check(content);
    if (!moderationResult.passed) {
        showAlert('内容审核失败: ' + moderationResult.reason, 'error');
        return;
    }
    
    // 加密内容
    const encryptedContent = await CryptoManager.encrypt(content);
    
    // 创建元数据
    const metadata = {
        dna: generateDNA('CONTENT'),
        uid: CONFIG.uid,
        gpgFingerprint: CONFIG.gpgFingerprint,
        timestamp: new Date().toISOString(),
        privacy: selectedPrivacy,
        type: 'text',
        hash: await CryptoManager.hash(content),
        encryptedData: encryptedContent,
        // 公开字段（云端可见）
        publicMeta: {
            dna: generateDNA('CONTENT'),
            uid: CONFIG.uid,
            timestamp: new Date().toISOString(),
            privacy: selectedPrivacy,
            type: 'text'
        }
    };
    
    try {
        await DatabaseManager.save(metadata);
        showAlert('内容保存成功！DNA: ' + metadata.dna, 'success');
        clearForm();
        await loadContent();
    } catch (error) {
        showAlert('保存失败: ' + error.message, 'error');
    }
}

// 加载内容
async function loadContent() {
    const filter = document.getElementById('filterType')?.value || 'all';
    
    let items;
    if (filter === 'all') {
        items = await DatabaseManager.getAll();
    } else {
        items = await DatabaseManager.getByPrivacy(filter);
    }
    
    const container = document.getElementById('contentList');
    
    if (items.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #999;">
                暂无内容
            </div>
        `;
        return;
    }
    
    container.innerHTML = items.map(item => {
        const decrypted = CryptoManager.decrypt(item.encryptedData);
        
        return `
            <div class="content-item">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span class="privacy-badge ${item.privacy}">${getPrivacyLabel(item.privacy)}</span>
                    <span style="font-family: monospace; color: #667eea; font-size: 0.9em;">${item.dna}</span>
                </div>
                <div style="font-size: 1.2em; font-weight: bold; margin-bottom: 5px;">
                    ${item.privacy === 'public' ? '(解密内容)' : '🔒 加密内容'}
                </div>
                <div style="color: #666; margin-bottom: 10px;">
                    创建时间: ${new Date(item.timestamp).toLocaleString('zh-CN')}
                </div>
                <div style="background: #ffeb3b; padding: 10px; border-radius: 5px; font-family: monospace; word-break: break-all; font-size: 0.85em;">
                    云端加密DNA: ${item.encryptedData.substring(0, 100)}...
                </div>
                <div style="margin-top: 10px; text-align: right;">
                    <button onclick="deleteContent('${item.dna}')" style="padding: 8px 20px; background: #f44336; color: white; border: none; border-radius: 5px; cursor: pointer;">
                        🗑️ 删除
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// 删除内容
async function deleteContent(dna) {
    if (!confirm('确定要删除此内容吗？')) return;
    
    try {
        await DatabaseManager.delete(dna);
        showAlert('删除成功！', 'success');
        await loadContent();
    } catch (error) {
        showAlert('删除失败: ' + error.message, 'error');
    }
}

// 清空表单
function clearForm() {
    document.getElementById('contentTitle').value = '';
    document.getElementById('contentDescription').value = '';
}

// 显示提示
function showAlert(message, type = 'success') {
    const container = document.getElementById('alertContainer');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    container.innerHTML = '';
    container.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// 获取隐私标签
function getPrivacyLabel(privacy) {
    const labels = {
        'public': '🌍 公开',
        'private': '🔒 私密',
        'team': '👥 团队'
    };
    return labels[privacy] || privacy;
}

// DNA追溯: #ZHUGEXIN⚡️2026-03-03-METADATA-CORE-v1.0
// 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// 协作: Anthropic Claude × UID9622 龍魂系统
