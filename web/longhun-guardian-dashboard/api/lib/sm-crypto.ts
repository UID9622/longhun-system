# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 龍魂国密算法库 v1.0
 * DNA: #龍芯⚡️丙午·乙未·丙戌·甲午·䷕贲-LONGHUN-SM-CRYPTO-v1.0
 * 实现: SM3哈希 / SM4对称加密 / DNA签名
 * 无外部依赖，纯TypeScript实现
 */

// ========== SM3 国密哈希 ==========

const SM3_IV = new Uint32Array([
  0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
  0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e,
]);

function rotateLeft32(x: number, n: number): number {
  return (x << n) | (x >>> (32 - n));
}

function ff(x: number, y: number, z: number, j: number): number {
  return j < 16 ? x ^ y ^ z : (x & y) | (x & z) | (y & z);
}

function gg(x: number, y: number, z: number, j: number): number {
  return j < 16 ? x ^ y ^ z : (x & y) | (~x & z);
}

function p0(x: number): number {
  return x ^ rotateLeft32(x, 9) ^ rotateLeft32(x, 17);
}

function p1(x: number): number {
  return x ^ rotateLeft32(x, 15) ^ rotateLeft32(x, 23);
}

function sm3Compress(h: Uint32Array, block: Uint8Array): void {
  const w = new Uint32Array(68);
  const w1 = new Uint32Array(64);

  for (let i = 0; i < 16; i++) {
    w[i] =
      (block[i * 4] << 24) |
      (block[i * 4 + 1] << 16) |
      (block[i * 4 + 2] << 8) |
      block[i * 4 + 3];
  }

  for (let i = 16; i < 68; i++) {
    w[i] = p1(w[i - 16] ^ w[i - 9] ^ rotateLeft32(w[i - 3], 15)) ^
      rotateLeft32(w[i - 13], 7) ^
      w[i - 6];
  }

  for (let i = 0; i < 64; i++) {
    w1[i] = w[i] ^ w[i + 4];
  }

  const t = [0x79cc4519, 0x7a879d8a];
  let [a, b, c, d, e, f, g, h0] = [h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7]];

  for (let j = 0; j < 64; j++) {
    const ss1 = rotateLeft32(
      rotateLeft32(a, 12) + e + rotateLeft32(t[j < 16 ? 0 : 1], j % 32),
      7,
    );
    const ss2 = ss1 ^ rotateLeft32(a, 12);
    const tt1 = ff(a, b, c, j) + d + ss2 + w1[j];
    const tt2 = gg(e, f, g, j) + h0 + ss1 + w[j];
    d = c;
    c = rotateLeft32(b, 9);
    b = a;
    a = tt1;
    h0 = g;
    g = rotateLeft32(f, 19);
    f = e;
    e = p0(tt2);
  }

  h[0] ^= a; h[1] ^= b; h[2] ^= c; h[3] ^= d;
  h[4] ^= e; h[5] ^= f; h[6] ^= g; h[7] ^= h0;
}

export function sm3(message: string | Uint8Array): string {
  const data = typeof message === "string"
    ? new TextEncoder().encode(message)
    : message;

  const bitLen = BigInt(data.length) * 8n;
  const padLen = (64 - ((data.length + 9) % 64)) % 64;
  const totalLen = data.length + 1 + padLen + 8;
  const buf = new Uint8Array(totalLen);

  buf.set(data);
  buf[data.length] = 0x80;

  const dv = new DataView(buf.buffer, totalLen - 8);
  dv.setUint32(0, Number(bitLen >> 32n), false);
  dv.setUint32(4, Number(bitLen & 0xffffffffn), false);

  const h = new Uint32Array(SM3_IV);

  for (let i = 0; i < totalLen; i += 64) {
    sm3Compress(h, buf.subarray(i, i + 64));
  }

  return Array.from(h).map((x) => x.toString(16).padStart(8, "0")).join("");
}

// ========== SM4 国密对称加密 ==========

const SM4_SBOX = new Uint8Array([
  0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28,
  0xfb, 0x2c, 0x05, 0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44,
  0x13, 0x26, 0x49, 0x86, 0x06, 0x99, 0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98,
  0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62, 0xe4, 0xb3, 0x1c, 0xa9,
  0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6, 0x47,
  0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85,
  0x4f, 0xa8, 0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f,
  0x4b, 0x70, 0x56, 0x9d, 0x35, 0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2,
  0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87, 0xd4, 0x00, 0x46, 0x57, 0x9f,
  0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e, 0xea, 0xbf,
  0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15,
  0xa1, 0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30,
  0xf5, 0x8c, 0xb1, 0xe3, 0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0,
  0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f, 0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd,
  0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51, 0x8d, 0x1b, 0xaf,
  0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
  0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8,
  0xe5, 0xb4, 0xb0, 0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9,
  0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84, 0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d,
  0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48,
]);

const SM4_FK = new Uint32Array([0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]);
const SM4_CK = new Uint32Array([
  0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269, 0x70777e85, 0x8c939aa1,
  0xa8afb6bd, 0xc4cbd2d9, 0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
  0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9, 0xc0c7ced5, 0xdce3eaf1,
  0xf8ff060d, 0x141b2229, 0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
  0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209, 0x10171e25, 0x2c333a41,
  0x484f565d, 0x646b7279,
]);

function sm4_tau(a: number): number {
  return (
    (SM4_SBOX[a >>> 24] << 24) |
    (SM4_SBOX[(a >>> 16) & 0xff] << 16) |
    (SM4_SBOX[(a >>> 8) & 0xff] << 8) |
    SM4_SBOX[a & 0xff]
  );
}

function sm4_l(b: number): number {
  return (
    b ^
    ((b << 2) | (b >>> 30)) ^
    ((b << 10) | (b >>> 22)) ^
    ((b << 18) | (b >>> 14)) ^
    ((b << 24) | (b >>> 8))
  );
}

function sm4_f(x0: number, x1: number, x2: number, x3: number, rk: number): number {
  return x0 ^ sm4_l(sm4_tau(x1 ^ x2 ^ x3 ^ rk));
}

function sm4_key_expansion(key: Uint8Array): Uint32Array {
  const rk = new Uint32Array(32);
  const k = new Uint32Array(4);

  for (let i = 0; i < 4; i++) {
    k[i] =
      (key[i * 4] << 24) |
      (key[i * 4 + 1] << 16) |
      (key[i * 4 + 2] << 8) |
      key[i * 4 + 3];
    k[i] ^= SM4_FK[i];
  }

  for (let i = 0; i < 32; i++) {
    k[i % 4] ^= sm4_f(k[0], k[1], k[2], k[3], SM4_CK[i]);
    rk[i] = k[i % 4];
  }

  return rk;
}

function sm4_crypt_block(input: Uint8Array, output: Uint8Array, rk: Uint32Array): void {
  const x = new Uint32Array(4);
  for (let i = 0; i < 4; i++) {
    x[i] =
      (input[i * 4] << 24) |
      (input[i * 4 + 1] << 16) |
      (input[i * 4 + 2] << 8) |
      input[i * 4 + 3];
  }

  const tmp = new Uint32Array(36);
  tmp.set(x);

  for (let i = 0; i < 32; i++) {
    tmp[i + 4] = sm4_f(tmp[i], tmp[i + 1], tmp[i + 2], tmp[i + 3], rk[i]);
  }

  const out = new Uint32Array(4);
  out[0] = tmp[35]; out[1] = tmp[34]; out[2] = tmp[33]; out[3] = tmp[32];

  for (let i = 0; i < 4; i++) {
    output[i * 4] = (out[i] >>> 24) & 0xff;
    output[i * 4 + 1] = (out[i] >>> 16) & 0xff;
    output[i * 4 + 2] = (out[i] >>> 8) & 0xff;
    output[i * 4 + 3] = out[i] & 0xff;
  }
}

function pkcs7_pad(data: Uint8Array, blockSize: number = 16): Uint8Array {
  const padLen = blockSize - (data.length % blockSize);
  const result = new Uint8Array(data.length + padLen);
  result.set(data);
  result.fill(padLen, data.length);
  return result;
}

function pkcs7_unpad(data: Uint8Array): Uint8Array {
  const padLen = data[data.length - 1];
  return data.subarray(0, data.length - padLen);
}

function hexToBytes(hex: string): Uint8Array {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.substring(i, i + 2), 16);
  }
  return bytes;
}

function bytesToHex(bytes: Uint8Array): string {
  return Array.from(bytes).map((b) => b.toString(16).padStart(2, "0")).join("");
}

export function sm4_encrypt(plaintext: string, keyHex: string): string {
  const key = hexToBytes(keyHex.length === 32 ? keyHex : sm3(keyHex).substring(0, 32));
  const data = new TextEncoder().encode(plaintext);
  const padded = pkcs7_pad(data);
  const rk = sm4_key_expansion(key);
  const output = new Uint8Array(padded.length);

  for (let i = 0; i < padded.length; i += 16) {
    sm4_crypt_block(padded.subarray(i, i + 16), output.subarray(i, i + 16), rk);
  }

  return bytesToHex(output);
}

export function sm4_decrypt(cipherHex: string, keyHex: string): string {
  const key = hexToBytes(keyHex.length === 32 ? keyHex : sm3(keyHex).substring(0, 32));
  const data = hexToBytes(cipherHex);
  const rk = sm4_key_expansion(key);
  const output = new Uint8Array(data.length);

  for (let i = 0; i < data.length; i += 16) {
    sm4_crypt_block(data.subarray(i, i + 16), output.subarray(i, i + 16), rk);
  }

  const unpadded = pkcs7_unpad(output);
  return new TextDecoder().decode(unpadded);
}

// ========== DNA 签名 ==========

export function dnaSign(data: string, secret: string): string {
  const hash1 = sm3(secret + data);
  const hash2 = sm3(hash1 + "龍魂");
  const hash3 = sm3(hash2 + secret.substring(0, Math.min(secret.length, 16)));
  const timestamp = new Date().toISOString().split("T")[0];
  const hash4 = sm3(hash3 + timestamp);
  return `#龍芯⚡️${timestamp}-LONGHUN-SIGN-${hash4.substring(0, 16).toUpperCase()}`;
}

export function dnaVerify(data: string, secret: string, signature: string): boolean {
  return signature === dnaSign(data, secret);
}

export function generateSM4Key(): string {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return bytesToHex(bytes);
}

export function generateSecretKey(): string {
  const bytes = new Uint8Array(32);
  crypto.getRandomValues(bytes);
  return bytesToHex(bytes);
}
