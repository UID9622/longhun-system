// DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-RUST-CORE-v2.0-UID9622-SM4SM3-PURE
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 创建者: 诸葛鑫（UID9622）
//
// 龍魂统一内核库 · 跨平台底座 · v2.0 纯Rust SM4/SM3
// C ABI 导出供所有平台 FFI 调用:
//   - aarch64-unknown-linux-gnu  (鲲鹏)
//   - aarch64-linux-android      (鸿蒙/Android)
//   - aarch64-apple-ios          (iOS)
//   - aarch64-apple-darwin       (Apple Silicon 本地)
//   - x86_64-unknown-linux-gnu   (x86 服务端)
//   - loongarch64-unknown-linux-gnu (龙芯)
//   - sunway64-unknown-linux-gnu (申威)

pub mod core;
pub mod memory;
pub mod evolution;

use std::ffi::{CStr, CString};
use std::os::raw::{c_char, c_int};

pub const VERSION: &str = env!("CARGO_PKG_VERSION");
pub const DNA: &str = "#龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-RUST-CORE-v2.0-SM4SM3-PURE-UID9622";
pub const CONFIRM: &str = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// ═══════════════════════════════════════════════════
// SM4 常量
// ═══════════════════════════════════════════════════

const SM4_SBOX: [u8; 256] = [
    0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
    0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
    0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
    0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
    0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
    0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
    0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
    0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
    0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
    0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
    0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
    0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
    0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
    0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
    0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
    0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48,
];

const SM4_FK: [u32; 4] = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc];
const SM4_CK: [u32; 32] = [
    0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269, 0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
    0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249, 0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
    0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229, 0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
    0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209, 0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279,
];

fn sm4_rotl(x: u32, n: u32) -> u32 { x.rotate_left(n) }
fn sm4_tau(a: u32) -> u32 {
    ((SM4_SBOX[(a >> 24) as usize] as u32) << 24)
        | ((SM4_SBOX[(a >> 16) as usize & 0xFF] as u32) << 16)
        | ((SM4_SBOX[(a >> 8) as usize & 0xFF] as u32) << 8)
        | (SM4_SBOX[(a & 0xFF) as usize] as u32)
}
fn sm4_l(b: u32) -> u32 { b ^ sm4_rotl(b, 2) ^ sm4_rotl(b, 10) ^ sm4_rotl(b, 18) ^ sm4_rotl(b, 24) }
fn sm4_lp(b: u32) -> u32 { b ^ sm4_rotl(b, 13) ^ sm4_rotl(b, 23) }

fn sm4_key_expand(mk: &[u8; 16]) -> [u32; 32] {
    let mut k = [0u32; 4];
    for i in 0..4 {
        k[i] = u32::from_be_bytes([mk[i * 4], mk[i * 4 + 1], mk[i * 4 + 2], mk[i * 4 + 3]]);
    }
    let mut rk = vec![0u32; 36];
    for i in 0..4 {
        rk[i] = k[i] ^ SM4_FK[i];
    }
    for i in 0..32 {
        let r = sm4_tau(rk[i + 1] ^ rk[i + 2] ^ rk[i + 3] ^ SM4_CK[i]);
        rk[i + 4] = rk[i] ^ sm4_lp(r);
    }
    let mut result = [0u32; 32];
    result.copy_from_slice(&rk[4..]);
    result
}

fn sm4_encrypt_block(x: &mut [u32; 4], rk: &[u32; 32]) {
    for i in 0..32 {
        let t = sm4_tau(x[1] ^ x[2] ^ x[3] ^ rk[i]);
        let nx = [x[1], x[2], x[3], x[0] ^ sm4_l(t)];
        *x = nx;
    }
}

fn sm4_decrypt_block(x: &mut [u32; 4], rk: &[u32; 32]) {
    for i in (0..32).rev() {
        let t = sm4_tau(x[1] ^ x[2] ^ x[3] ^ rk[i]);
        let nx = [x[1], x[2], x[3], x[0] ^ sm4_l(t)];
        *x = nx;
    }
}

fn sm4_encrypt_ecb(data: &[u8], key: &[u8; 16]) -> Vec<u8> {
    let rk = sm4_key_expand(key);
    let pad = 16 - (data.len() % 16);
    let mut padded = data.to_vec();
    padded.resize(data.len() + pad, pad as u8);

    let mut result = Vec::with_capacity(padded.len());
    for chunk in padded.chunks(16) {
        let mut x = [
            u32::from_be_bytes([chunk[12], chunk[13], chunk[14], chunk[15]]),
            u32::from_be_bytes([chunk[8], chunk[9], chunk[10], chunk[11]]),
            u32::from_be_bytes([chunk[4], chunk[5], chunk[6], chunk[7]]),
            u32::from_be_bytes([chunk[0], chunk[1], chunk[2], chunk[3]]),
        ];
        sm4_encrypt_block(&mut x, &rk);
        result.extend_from_slice(&x[0].to_be_bytes());
        result.extend_from_slice(&x[1].to_be_bytes());
        result.extend_from_slice(&x[2].to_be_bytes());
        result.extend_from_slice(&x[3].to_be_bytes());
    }
    result
}

fn sm4_decrypt_ecb(data: &[u8], key: &[u8; 16]) -> Result<Vec<u8>, String> {
    if data.len() % 16 != 0 {
        return Err("SM4 ciphertext must be multiple of 16".into());
    }
    let rk = sm4_key_expand(key);
    let mut result = Vec::with_capacity(data.len());
    for chunk in data.chunks(16) {
        let mut x = [
            u32::from_be_bytes([chunk[12], chunk[13], chunk[14], chunk[15]]),
            u32::from_be_bytes([chunk[8], chunk[9], chunk[10], chunk[11]]),
            u32::from_be_bytes([chunk[4], chunk[5], chunk[6], chunk[7]]),
            u32::from_be_bytes([chunk[0], chunk[1], chunk[2], chunk[3]]),
        ];
        sm4_decrypt_block(&mut x, &rk);
        result.extend_from_slice(&x[0].to_be_bytes());
        result.extend_from_slice(&x[1].to_be_bytes());
        result.extend_from_slice(&x[2].to_be_bytes());
        result.extend_from_slice(&x[3].to_be_bytes());
    }
    // PKCS7 unpadding
    let pad = result[result.len() - 1];
    if pad > 0 && pad <= 16 && result[result.len() - pad as usize..].iter().all(|&b| b == pad) {
        result.truncate(result.len() - pad as usize);
        Ok(result)
    } else {
        Err("SM4 decrypt failed: bad padding".into())
    }
}

fn sm3_hash_raw(data: &[u8]) -> [u8; 32] {
    // SM3 完整的 Merkle-Damgard 构造
    let iv: [u32; 8] = [
        0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
        0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e,
    ];
    let mut h = iv;

    let mut padded = data.to_vec();
    let bit_len = (data.len() as u64) * 8;
    padded.push(0x80);
    while (padded.len() % 64) != 56 {
        padded.push(0);
    }
    padded.extend_from_slice(&bit_len.to_be_bytes());

    for chunk in padded.chunks(64) {
        let w = expand_w(chunk);
        let mut a = [h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7]];
        for j in 0..64 {
            let ss1 = sm4_rotl(
                sm4_rotl(a[0], 12).wrapping_add(a[4]).wrapping_add(sm4_rotl(sm4_t_j(j), j as u32 % 32)),
                7,
            );
            let ss2 = ss1 ^ sm4_rotl(a[0], 12);
            let tt1 = ff_j(a[0], a[1], a[2], j)
                .wrapping_add(a[3])
                .wrapping_add(ss2)
                .wrapping_add(w[j] ^ w[j + 4]);
            let tt2 = gg_j(a[4], a[5], a[6], j)
                .wrapping_add(a[7])
                .wrapping_add(ss1)
                .wrapping_add(w[j]);
            a[3] = a[2];
            a[2] = sm4_rotl(a[1], 9);
            a[1] = a[0];
            a[0] = tt1;
            a[7] = a[6];
            a[6] = sm4_rotl(a[5], 19);
            a[5] = a[4];
            a[4] = p0(tt2);
        }
        for i in 0..8 {
            h[i] ^= a[i];
        }
    }

    let mut hash = [0u8; 32];
    for i in 0..8 {
        hash[i * 4..i * 4 + 4].copy_from_slice(&h[i].to_be_bytes());
    }
    hash
}

fn sm4_t_j(j: usize) -> u32 {
    if j < 16 { 0x79cc4519 } else { 0x7a879d8a }
}

fn ff_j(x: u32, y: u32, z: u32, j: usize) -> u32 {
    if j < 16 { x ^ y ^ z } else { (x & y) | (x & z) | (y & z) }
}

fn gg_j(x: u32, y: u32, z: u32, j: usize) -> u32 {
    if j < 16 { x ^ y ^ z } else { (x & y) | (!x & z) }
}

fn p0(x: u32) -> u32 { x ^ sm4_rotl(x, 9) ^ sm4_rotl(x, 17) }

fn p1(x: u32) -> u32 { x ^ sm4_rotl(x, 15) ^ sm4_rotl(x, 23) }

fn expand_w(chunk: &[u8]) -> [u32; 68] {
    let mut w = [0u32; 68];
    for i in 0..16 {
        w[i] = u32::from_be_bytes([chunk[i * 4], chunk[i * 4 + 1], chunk[i * 4 + 2], chunk[i * 4 + 3]]);
    }
    for j in 16..68 {
        w[j] = p1(w[j - 16] ^ w[j - 9] ^ sm4_rotl(w[j - 3], 15))
            ^ sm4_rotl(w[j - 13], 7) ^ w[j - 6];
    }
    // w' = w[j] ^ w[j+4] for j=0..64 (embedded in caller for efficiency)
    w
}

// ═══════════════════════════════════════════════════
// C ABI 导出
// ═══════════════════════════════════════════════════

#[no_mangle]
pub extern "C" fn longhun_run_supervision(config_json: *const c_char) -> *mut c_char {
    let config = if config_json.is_null() {
        Default::default()
    } else {
        let c_str = unsafe { CStr::from_ptr(config_json) };
        let s = c_str.to_string_lossy();
        core::SupervisionConfig::from_json(&s).unwrap_or_default()
    };
    let result = core::run_supervision(&config);
    let json = serde_json::to_string(&result).unwrap_or_else(|_| "{}".to_string());
    CString::new(json).unwrap().into_raw()
}

#[no_mangle]
pub extern "C" fn longhun_query_memory(query_json: *const c_char) -> *mut c_char {
    let query = if query_json.is_null() {
        String::new()
    } else {
        let c_str = unsafe { CStr::from_ptr(query_json) };
        c_str.to_string_lossy().to_string()
    };
    let results = memory::query(&query);
    let json = serde_json::to_string(&results).unwrap_or_else(|_| "[]".to_string());
    CString::new(json).unwrap().into_raw()
}

#[no_mangle]
pub extern "C" fn longhun_get_health() -> *mut c_char {
    let health = core::get_health();
    let json = serde_json::to_string(&health).unwrap_or_else(|_| "{}".to_string());
    CString::new(json).unwrap().into_raw()
}

/// SM4 ECB 加密: data + data_len → hex 密文
#[no_mangle]
pub extern "C" fn longhun_sm4_encrypt(data: *const u8, data_len: c_int,
                                       key_hex: *const c_char) -> *mut c_char {
    if data.is_null() || data_len <= 0 || key_hex.is_null() {
        return CString::new("{\"error\":\"invalid params\"}").unwrap().into_raw();
    }
    let key_str = unsafe { CStr::from_ptr(key_hex) }.to_string_lossy();
    let key = match hex::decode(key_str.as_ref()) {
        Ok(k) if k.len() == 16 => {
            let mut arr = [0u8; 16];
            arr.copy_from_slice(&k);
            arr
        }
        _ => return CString::new("{\"error\":\"key must be 16 bytes (32 hex chars)\"}").unwrap().into_raw(),
    };
    let raw = unsafe { std::slice::from_raw_parts(data, data_len as usize) };
    let encrypted = sm4_encrypt_ecb(raw, &key);
    CString::new(hex::encode(&encrypted)).unwrap().into_raw()
}

/// SM4 ECB 解密: hex密文 + key → UTF-8 原文
#[no_mangle]
pub extern "C" fn longhun_sm4_decrypt(data_hex: *const c_char,
                                       key_hex: *const c_char) -> *mut c_char {
    if data_hex.is_null() || key_hex.is_null() {
        return CString::new("{\"error\":\"invalid params\"}").unwrap().into_raw();
    }
    let hex_str = unsafe { CStr::from_ptr(data_hex) }.to_string_lossy();
    let cipher = match hex::decode(hex_str.as_ref()) {
        Ok(b) => b,
        Err(_) => return CString::new("{\"error\":\"hex decode failed\"}").unwrap().into_raw(),
    };
    let key_str = unsafe { CStr::from_ptr(key_hex) }.to_string_lossy();
    let key = match hex::decode(key_str.as_ref()) {
        Ok(k) if k.len() == 16 => {
            let mut arr = [0u8; 16];
            arr.copy_from_slice(&k);
            arr
        }
        _ => return CString::new("{\"error\":\"key must be 16 bytes (32 hex chars)\"}").unwrap().into_raw(),
    };
    match sm4_decrypt_ecb(&cipher, &key) {
        Ok(plain) => {
            match String::from_utf8(plain.clone()) {
                Ok(s) => CString::new(s).unwrap().into_raw(),
                Err(_) => CString::new(hex::encode(&plain)).unwrap().into_raw(),
            }
        }
        Err(e) => CString::new(format!("{{\"error\":\"{}\"}}", e)).unwrap().into_raw(),
    }
}

/// SM3 哈希: data + data_len → hex hash
#[no_mangle]
pub extern "C" fn longhun_sm3_hash(data: *const u8, data_len: c_int) -> *mut c_char {
    if data.is_null() || data_len <= 0 {
        return CString::new("{\"error\":\"invalid params\"}").unwrap().into_raw();
    }
    let raw = unsafe { std::slice::from_raw_parts(data, data_len as usize) };
    let hash = sm3_hash_raw(raw);
    CString::new(hex::encode(&hash)).unwrap().into_raw()
}

#[no_mangle]
pub extern "C" fn longhun_free_string(ptr: *mut c_char) {
    if !ptr.is_null() {
        unsafe { let _ = CString::from_raw(ptr); }
    }
}

// ═══════════════════════════════════════════════════
// 测试
// ═══════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version() { assert!(!VERSION.is_empty()); }

    #[test]
    fn test_dna() { assert!(DNA.contains("UID9622")); }

    #[test]
    fn test_sm4_roundtrip() {
        let key = b"0123456789abcdef";
        let data = b"Hello SM4 Rust! 123";
        let enc = sm4_encrypt_ecb(data, key);
        let dec = sm4_decrypt_ecb(&enc, key).unwrap();
        assert_eq!(&dec, data);
    }

    #[test]
    fn test_sm4_wrong_key() {
        let k1 = b"0123456789abcdef";
        let k2 = b"fedcba9876543210";
        let enc = sm4_encrypt_ecb(b"test", k1);
        assert!(sm4_decrypt_ecb(&enc, k2).is_err());
    }

    #[test]
    fn test_sm3_hash() {
        let h = sm3_hash_raw(b"hello");
        assert_eq!(h.len(), 32);
    }
}
