/**
 * 龙魂DNA存证系统 - JavaScript核心引擎
 * 
 * 作者: 诸葛鑫 (Lucky) | UID9622
 * DNA追溯码: #ZHUGEXIN⚡️2026-01-06-LONGHUN-DNA-CORE-001
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 */

class LonghunDNA {
    // 生成DNA追溯码
    static generateDNACode(creatorId, timestamp, projectName, sequence) {
        const date = new Date(timestamp);
        const formattedDate = date.toISOString().split('T')[0];
        const formattedSeq = String(sequence).padStart(3, '0');
        return `#${creatorId}⚡️${formattedDate}-${projectName}-${formattedSeq}`;
    }
    
    // 生成数字指纹
    static async generateDigitalFingerprint(content, dnaCode) {
        const combined = content + dnaCode;
        const encoder = new TextEncoder();
        const data = encoder.encode(combined);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }
    
    // 创建存证
    static async createEvidence(content, creatorId, projectName) {
        try {
            const timestamp = Date.now();
            const currentTime = new Date(timestamp).toISOString();
            
            const storageKey = `latest_seq_${creatorId}_${projectName}`;
            let latestSeq = parseInt(localStorage.getItem(storageKey) || '0');
            const newSeq = latestSeq + 1;
            
            const dnaCode = this.generateDNACode(creatorId, timestamp, projectName, newSeq);
            const fingerprint = await this.generateDigitalFingerprint(content, dnaCode);
            
            const evidence = {
                content: content,
                timestamp: currentTime,
                timestampUnix: timestamp,
                creatorId: creatorId,
                projectName: projectName,
                sequence: newSeq,
                dnaCode: dnaCode,
                digitalFingerprint: fingerprint,
                metadata: {
                    toolVersion: "龙魂DNA存证系统 v1.0",
                    systemNote: "本存证基于SHA-256算法生成，任何修改都会导致指纹失效",
                    creatorStatement: "技术主权·数据主权·中文原生"
                }
            };
            
            localStorage.setItem(dnaCode, JSON.stringify(evidence));
            localStorage.setItem(storageKey, newSeq.toString());
            await this.saveToIndexedDB(dnaCode, evidence);
            
            return { success: true, evidence: evidence };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    // 验证存证
    static async verifyEvidence(dnaCodeOrEvidence) {
        try {
            let evidence;
            
            if (typeof dnaCodeOrEvidence === 'string') {
                const stored = localStorage.getItem(dnaCodeOrEvidence);
                if (!stored) {
                    evidence = await this.loadFromIndexedDB(dnaCodeOrEvidence);
                    if (!evidence) {
                        return { success: false, reason: "未找到此DNA追溯码的存证" };
                    }
                } else {
                    evidence = JSON.parse(stored);
                }
            } else {
                evidence = dnaCodeOrEvidence;
            }
            
            const originalFingerprint = evidence.digitalFingerprint;
            const calculatedFingerprint = await this.generateDigitalFingerprint(
                evidence.content, evidence.dnaCode
            );
            
            const isMatch = (originalFingerprint === calculatedFingerprint);
            
            if (isMatch) {
                return {
                    success: true, verified: true,
                    dnaCode: evidence.dnaCode,
                    timestamp: evidence.timestamp,
                    creator: evidence.creatorId,
                    project: evidence.projectName,
                    contentPreview: evidence.content.substring(0, 100) + '...',
                    digitalFingerprint: originalFingerprint
                };
            } else {
                return {
                    success: true, verified: false,
                    reason: "数字指纹不匹配，内容可能被篡改",
                    originalFingerprint: originalFingerprint,
                    calculatedFingerprint: calculatedFingerprint
                };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    // 导出存证
    static exportEvidence(dnaCode) {
        try {
            const stored = localStorage.getItem(dnaCode);
            if (!stored) return { success: false, reason: "未找到此DNA追溯码" };
            
            const evidence = JSON.parse(stored);
            const jsonText = JSON.stringify(evidence, null, 2);
            const filename = `DNA存证_${dnaCode}.json`;
            
            const blob = new Blob([jsonText], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            return { success: true, filename: filename };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    // 导入存证
    static async importEvidence(file) {
        try {
            const text = await file.text();
            const evidence = JSON.parse(text);
            const verifyResult = await this.verifyEvidence(evidence);
            
            if (verifyResult.verified) {
                localStorage.setItem(evidence.dnaCode, JSON.stringify(evidence));
                await this.saveToIndexedDB(evidence.dnaCode, evidence);
                return { success: true, dnaCode: evidence.dnaCode };
            } else {
                return { success: false, reason: "导入的存证验证失败，可能已被篡改" };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    // 查询所有存证
    static async queryAllEvidence(creatorId = null, projectName = null) {
        try {
            const results = [];
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key.startsWith('#')) {
                    const value = localStorage.getItem(key);
                    const evidence = JSON.parse(value);
                    let match = true;
                    if (creatorId && evidence.creatorId !== creatorId) match = false;
                    if (projectName && evidence.projectName !== projectName) match = false;
                    if (match) results.push(evidence);
                }
            }
            results.sort((a, b) => b.timestampUnix - a.timestampUnix);
            return { success: true, evidences: results, count: results.length };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    // IndexedDB操作
    static async openDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open('LonghunDNA', 1);
            request.onerror = () => reject(request.error);
            request.onsuccess = () => resolve(request.result);
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains('evidences')) {
                    db.createObjectStore('evidences', { keyPath: 'dnaCode' });
                }
            };
        });
    }
    
    static async saveToIndexedDB(dnaCode, evidence) {
        const db = await this.openDB();
        const transaction = db.transaction(['evidences'], 'readwrite');
        const store = transaction.objectStore('evidences');
        return new Promise((resolve, reject) => {
            const request = store.put(evidence);
            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }
    
    static async loadFromIndexedDB(dnaCode) {
        const db = await this.openDB();
        const transaction = db.transaction(['evidences'], 'readonly');
        const store = transaction.objectStore('evidences');
        return new Promise((resolve, reject) => {
            const request = store.get(dnaCode);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = LonghunDNA;
}
