// ===== 龍魂 DNA 追溯码生成器 =====

window.dnaGenerator = (function() {

  // 简易哈希函数
  function simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash).toString(16).toUpperCase().padStart(8, '0');
  }

  // SHA-256 哈希（异步）
  async function sha256(text) {
    const encoder = new TextEncoder();
    const data = encoder.encode(text);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  // 生成 DNA 追溯码
  function generate(content, type = 'GENERAL') {
    const now = new Date();
    const dateStr = now.toISOString().split('T')[0];
    const hash = simpleHash(content);
    const seq = String(Math.floor(Math.random() * 999) + 1).padStart(3, '0');
    return `#龍芯⚡️${dateStr}-${type}-${hash}-${seq}`;
  }

  // 生成完整存证记录
  async function generateFullRecord(content, creatorId, projectName) {
    const now = new Date();
    const dateStr = now.toISOString().split('T')[0];
    const contentHash = await sha256(content);
    const seq = String(Math.floor(Math.random() * 999) + 1).padStart(3, '0');
    const dnaCode = `#${creatorId}⚡️${dateStr}-${projectName}-${seq}`;

    return {
      dna_code: dnaCode,
      creator: creatorId,
      project: projectName,
      timestamp: now.toISOString(),
      content_hash: contentHash,
      content_length: content.length,
      content_preview: content.substring(0, 200),
      verification: {
        algorithm: 'SHA-256',
        hash: contentHash,
        generated_at: now.toISOString()
      }
    };
  }

  // 验证 DNA
  async function verify(content, record) {
    const contentHash = await sha256(content);
    return {
      match: contentHash === record.content_hash,
      expected_hash: record.content_hash,
      actual_hash: contentHash,
      dna_code: record.dna_code,
      verified_at: new Date().toISOString()
    };
  }

  return { generate, generateFullRecord, verify, sha256, simpleHash };
})();
