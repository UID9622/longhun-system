# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-ENGINE-DNA-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

/**
 * 龍魂 DNA 签名系统 v1.0
 * 不依赖 GPG · 简单可靠 · 跨平台通用
 * DNA: #龍芯⚡️20260525|GEN-DNA|v1.0|xxxxx
 */

const DNA_PREFIX = '#龍芯⚡️';

function generateDNA(topic, version = 'v1.0') {
  const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const combined = `${topic}${today}${version}`;
  const sha256 = sha256Hash(combined);
  const sha8 = sha256.slice(0, 8);
  return `${DNA_PREFIX}${today}|${topic}|${version}|${sha8}`;
}

function verifyDNA(dnaString) {
  if (!dnaString.startsWith(DNA_PREFIX)) {
    return { valid: false, reason: '格式错误：必须以 #龍芯⚡️ 开头' };
  }
  const content = dnaString.replace(DNA_PREFIX, '');
  const parts = content.split('|');
  if (parts.length !== 4) {
    return { valid: false, reason: `格式错误：应该有4个字段用 | 分隔，实际: ${parts.length}` };
  }
  const [dateStr, topic, version, providedSha8] = parts;
  if (dateStr.length !== 8 || !/^\d{8}$/.test(dateStr)) {
    return { valid: false, reason: '格式错误：日期应该是 YYYYMMDD 格式' };
  }
  const combined = `${topic}${dateStr}${version}`;
  const sha256 = sha256Hash(combined);
  const calculatedSha8 = sha256.slice(0, 8);
  if (providedSha8 === calculatedSha8) {
    const displayDate = `${dateStr.slice(0, 4)}-${dateStr.slice(4, 6)}-${dateStr.slice(6, 8)}`;
    return { valid: true, date: displayDate, topic, version };
  } else {
    return { valid: false, reason: `SHA8 不匹配 | 提供: ${providedSha8} | 计算: ${calculatedSha8}` };
  }
}

function sha256Hash(str) {
  // 简单的 SHA-256 实现（足够用于 DNA 签名）
  // 在实际浏览器环境中可用 crypto.subtle，这里用纯 JS 备用
  if (typeof crypto !== 'undefined' && crypto.subtle) {
    // 异步版本留给外部调用
  }
  // 纯 JS SHA-256 (简化版，足够用)
  return jsSHA256(str);
}

function jsSHA256(str) {
  const K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
  ];
  let h0 = 0x6a09e667, h1 = 0xbb67ae85, h2 = 0x3c6ef372, h3 = 0xa54ff53a;
  let h4 = 0x510e527f, h5 = 0x9b05688c, h6 = 0x1f83d9ab, h7 = 0x5be0cd19;
  const msg = unescape(encodeURIComponent(str));
  const len = msg.length;
  const totalLen = Math.ceil((len + 9) / 64) * 64;
  const bytes = new Uint8Array(totalLen);
  for (let i = 0; i < len; i++) bytes[i] = msg.charCodeAt(i);
  bytes[len] = 0x80;
  const bitLen = len * 8;
  bytes[totalLen - 4] = (bitLen >>> 24) & 0xff;
  bytes[totalLen - 3] = (bitLen >>> 16) & 0xff;
  bytes[totalLen - 2] = (bitLen >>> 8) & 0xff;
  bytes[totalLen - 1] = bitLen & 0xff;

  for (let i = 0; i < totalLen; i += 64) {
    const w = new Uint32Array(64);
    for (let t = 0; t < 16; t++) {
      w[t] = (bytes[i + t * 4] << 24) | (bytes[i + t * 4 + 1] << 16) |
             (bytes[i + t * 4 + 2] << 8) | bytes[i + t * 4 + 3];
    }
    for (let t = 16; t < 64; t++) {
      const s0 = ((w[t - 15] >>> 7) | (w[t - 15] << 25)) ^ ((w[t - 15] >>> 18) | (w[t - 15] << 14)) ^ (w[t - 15] >>> 3);
      const s1 = ((w[t - 2] >>> 17) | (w[t - 2] << 15)) ^ ((w[t - 2] >>> 19) | (w[t - 2] << 13)) ^ (w[t - 2] >>> 10);
      w[t] = (w[t - 16] + s0 + w[t - 7] + s1) >>> 0;
    }
    let a = h0, b = h1, c = h2, d = h3, e = h4, f = h5, g = h6, hh = h7;
    for (let t = 0; t < 64; t++) {
      const S1 = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
      const ch = (e & f) ^ (~e & g);
      const temp1 = (hh + S1 + ch + K[t] + w[t]) >>> 0;
      const S0 = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
      const maj = (a & b) ^ (a & c) ^ (b & c);
      const temp2 = (S0 + maj) >>> 0;
      hh = g; g = f; f = e; e = (d + temp1) >>> 0; d = c; c = b; b = a; a = (temp1 + temp2) >>> 0;
    }
    h0 = (h0 + a) >>> 0; h1 = (h1 + b) >>> 0; h2 = (h2 + c) >>> 0; h3 = (h3 + d) >>> 0;
    h4 = (h4 + e) >>> 0; h5 = (h5 + f) >>> 0; h6 = (h6 + g) >>> 0; h7 = (h7 + hh) >>> 0;
  }
  const toHex = (n) => (n >>> 0).toString(16).padStart(8, '0');
  return toHex(h0) + toHex(h1) + toHex(h2) + toHex(h3) + toHex(h4) + toHex(h5) + toHex(h6) + toHex(h7);
}

// 导出
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { generateDNA, verifyDNA, sha256Hash };
}
