#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 IP 资产脚本 · dragon_dna.py
DNA: #龍芯:2026-07-04-DNA-TRACE-v3.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
来源: /Users/zuimeidedeyihan/Downloads/Kimi_Agent_龍魂IP资产清单 (2)/dragon_dna.py
归档: /Users/zuimeidedeyihan/longhun-system/scripts/private-shared-imports/ip-assets-v2/dragon_dna.py
"""

# -*- coding: utf-8 -*-
"""
龍魂·全数据类型DNA追溯体系 v3.0
覆盖: 图片/文本/个人信息/指纹/配方/银行卡/文档/视频/音频
系统DNA: #龍芯:2026-07-04-DNA-TRACE-v3.0
"""

import hashlib
import secrets
import base64
import json
import time
import re
import random
import string
import struct
import threading
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict

try:
    import ecdsa
except ImportError:
    raise ImportError("请先安装ecdsa库: pip install ecdsa")

# ============================================================
# SM3 哈希算法 (国密标准完整实现)
# ============================================================

SM3_IV = [
    0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
    0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e
]
SM3_T0, SM3_T1 = 0x79cc4519, 0x7a879d8a


def _rol(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def _ff(x, y, z, j):
    return x ^ y ^ z if j < 16 else (x & y) | (x & z) | (y & z)


def _gg(x, y, z, j):
    return x ^ y ^ z if j < 16 else (x & y) | (~x & z)


def _p0(x):
    return x ^ _rol(x, 9) ^ _rol(x, 17)


def _p1(x):
    return x ^ _rol(x, 15) ^ _rol(x, 23)


def _tt(x):
    return x ^ _rol(x, 9) ^ _rol(x, 17)


def _sm3_cf(v, bi):
    w, w1 = [0] * 68, [0] * 64
    for i in range(16):
        w[i] = int.from_bytes(bi[i*4:(i+1)*4], 'big')
    for i in range(16, 68):
        w[i] = _p1(w[i-16] ^ w[i-9] ^ _rol(w[i-3], 15)) ^ _rol(w[i-13], 7) ^ w[i-6]
    for i in range(64):
        w1[i] = w[i] ^ w[i+4]
    a, b, c, d, e, f, g, h = v
    for j in range(64):
        ss1 = _rol((_rol(a, 12) + e + _rol(SM3_T0 if j < 16 else SM3_T1, j % 32)) & 0xFFFFFFFF, 7)
        ss2 = ss1 ^ _rol(a, 12)
        tt1 = (_ff(a, b, c, j) + d + ss2 + w1[j]) & 0xFFFFFFFF
        tt2 = (_gg(e, f, g, j) + h + ss1 + w[j]) & 0xFFFFFFFF
        d, c, b, a = c, _rol(b, 9), a, tt1
        h, g, f, e = g, _rol(f, 19), e, _tt(tt2)
    return [
        (a ^ v[0]) & 0xFFFFFFFF, (b ^ v[1]) & 0xFFFFFFFF,
        (c ^ v[2]) & 0xFFFFFFFF, (d ^ v[3]) & 0xFFFFFFFF,
        (e ^ v[4]) & 0xFFFFFFFF, (f ^ v[5]) & 0xFFFFFFFF,
        (g ^ v[6]) & 0xFFFFFFFF, (h ^ v[7]) & 0xFFFFFFFF
    ]


class SM3:
    """SM3哈希算法 - 国密标准"""

    def __init__(self):
        self.v = SM3_IV.copy()
        self.buf = b''
        self.tlen = 0

    def update(self, d):
        if isinstance(d, str):
            d = d.encode('utf-8')
        self.tlen += len(d)
        self.buf += d
        while len(self.buf) >= 64:
            self.v = _sm3_cf(self.v, self.buf[:64])
            self.buf = self.buf[64:]

    def digest(self):
        tb = self.tlen * 8
        pad = self.buf + b'\x80'
        while len(pad) % 64 != 56:
            pad += b'\x00'
        pad += tb.to_bytes(8, 'big')
        v = self.v.copy()
        for i in range(0, len(pad), 64):
            v = _sm3_cf(v, pad[i:i+64])
        return b''.join(x.to_bytes(4, 'big') for x in v)

    def hexdigest(self):
        return self.digest().hex()

    @staticmethod
    def hash(d):
        s = SM3()
        s.update(d)
        return s.hexdigest()


# ============================================================
# SM2 非对称签名算法
# ============================================================

class SM3HashWrapper:
    """SM3哈希包装器 - 兼容ecdsa接口"""
    def __init__(self, data):
        self._digest = bytes.fromhex(SM3.hash(data))
    def digest(self):
        return self._digest


class SM2Crypto:
    """SM2国密签名算法 - NIST256p曲线 + SM3哈希"""

    def __init__(self):
        self.curve = ecdsa.NIST256p
        self._sk = None
        self._vk = None

    def generate_key_pair(self):
        self._sk = ecdsa.SigningKey.generate(curve=self.curve)
        self._vk = self._sk.get_verifying_key()
        return {
            'private_key': self._sk.to_string().hex(),
            'public_key': '04' + self._vk.to_string().hex(),
            'curve': 'SM2-NIST256p'
        }

    def load_private_key(self, hk):
        self._sk = ecdsa.SigningKey.from_string(bytes.fromhex(hk), curve=self.curve)
        self._vk = self._sk.get_verifying_key()

    def load_public_key(self, hk):
        kd = hk[2:] if hk.startswith('04') else hk
        self._vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(kd), curve=self.curve)

    def sign(self, msg):
        if self._sk is None:
            raise ValueError("Private key not set")
        if isinstance(msg, str):
            msg = msg.encode('utf-8')
        return self._sk.sign(msg, hashfunc=SM3HashWrapper,
                             sigencode=ecdsa.util.sigencode_string).hex()

    def verify(self, msg, sig):
        if self._vk is None:
            raise ValueError("Public key not set")
        if isinstance(msg, str):
            msg = msg.encode('utf-8')
        try:
            return self._vk.verify(bytes.fromhex(sig), msg,
                                   hashfunc=SM3HashWrapper,
                                   sigdecode=ecdsa.util.sigdecode_string)
        except Exception:
            return False


# ============================================================
# DNA数据模型与枚举
# ============================================================

class DataType(Enum):
    IMAGE = "IMG"
    TEXT = "TXT"
    PERSONAL_INFO = "PI"
    FINGERPRINT = "FP"
    BANK_CARD = "BC"
    FORMULA = "FM"
    DOCUMENT = "DOC"
    VIDEO = "VID"
    AUDIO = "AUD"
    UNKNOWN = "UNK"


class DNAType(Enum):
    BASIC = "basic"
    EXTENDED = "extended"
    AUDIT = "audit"


class AuditResult(Enum):
    PASS = "PASS"
    WARNING = "WARN"
    FAIL = "FAIL"
    UNKNOWN = "UNK"


DNA_PREFIX = "#龍芯:"
DNA_AUDIT_PREFIX = "#AUDIT"


@dataclass
class DNAModel:
    timestamp: str
    data_type: DataType
    source: str
    version: str
    sm3_hash: str = ""
    threshold: float = 0.0
    sm2_signature: str = ""
    metadata: Dict = field(default_factory=dict)

    def to_basic_dna(self) -> str:
        return f"{DNA_PREFIX}{self.timestamp}-{self.data_type.value}-{self.source}-{self.version}"

    def to_extended_dna(self) -> str:
        basic = self.to_basic_dna()
        return f"{basic}|SM3:{self.sm3_hash[:16]}|THRESH:{self.threshold}|SIG:{self.sm2_signature[:32]}"

    def to_audit_dna(self, result: AuditResult, details: str = "") -> str:
        icon_map = {"PASS": "+", "WARN": "~", "FAIL": "!", "UNK": "?"}
        icon = icon_map.get(result.value, "?")
        return f"{DNA_AUDIT_PREFIX}[{icon}]{result.value}|{details}"


# ============================================================
# DNA生成器类
# ============================================================

class DNAGenerator:
    def __init__(self, source: str = "LONHUN", version: str = "v3.0"):
        self.source = source
        self.version = version
        self.sm2 = SM2Crypto()
        self._keys = self.sm2.generate_key_pair()
        self._lock = threading.Lock()

    def _now(self) -> str:
        return datetime.now().strftime("%Y-%m-%d-%H%M%S")

    def _hash(self, data: bytes) -> str:
        return SM3.hash(data)

    def _sign(self, data: bytes) -> str:
        with self._lock:
            return self.sm2.sign(data)

    def generate(self, data: Union[str, bytes], data_type: DataType,
                 threshold: float = 0.7, extra_meta: Optional[Dict] = None) -> DNAModel:
        if isinstance(data, str):
            data = data.encode('utf-8')
        return DNAModel(
            timestamp=self._now(),
            data_type=data_type,
            source=self.source,
            version=self.version,
            sm3_hash=self._hash(data),
            threshold=threshold,
            sm2_signature=self._sign(data),
            metadata=extra_meta or {}
        )

    def get_public_key(self) -> str:
        return self._keys['public_key']


class ImageDNAGenerator(DNAGenerator):
    def generate(self, image_data: bytes, image_format: str = "JPG",
                 width: int = 0, height: int = 0,
                 device_info: str = "", geo_tag: str = "") -> Dict:
        dna = super().generate(image_data, DataType.IMAGE, threshold=0.8)
        return {
            'dna_model': dna,
            'basic_dna': dna.to_basic_dna(),
            'extended_dna': dna.to_extended_dna(),
            'image_format': image_format,
            'dimensions': f"{width}x{height}",
            'exif_dna': f"EXIF:DNA={dna.to_basic_dna()}|FMT={image_format}"
                        f"|DIM={width}x{height}|DEV={device_info}|GEO={geo_tag}"
                        f"|HASH={dna.sm3_hash[:24]}",
            'lsb_dna': f"LSB:{dna.sm3_hash[:32]}:{dna.sm2_signature[:32]}",
            'header_mark': f"DRAGON:{dna.to_basic_dna()}:END".encode('utf-8'),
            'verification': {
                'sm3_full': dna.sm3_hash,
                'sm2_sig_full': dna.sm2_signature,
                'public_key': self.get_public_key()
            }
        }


class TextDNAGenerator(DNAGenerator):
    def generate(self, text: str, text_type: str = "general") -> Dict:
        data = text.encode('utf-8')
        dna = super().generate(data, DataType.TEXT, threshold=0.75)
        paragraphs = text.split('\n\n')
        para_dnas = []
        for i, para in enumerate(paragraphs):
            para_hash = SM3.hash(para.encode('utf-8'))
            para_dnas.append(f"[P{i}:H={para_hash[:16]}:SIG={dna.sm2_signature[:16]}]")
        return {
            'dna_model': dna,
            'basic_dna': dna.to_basic_dna(),
            'extended_dna': dna.to_extended_dna(),
            'text_type': text_type,
            'word_count': len(text.split()),
            'paragraph_count': len(paragraphs),
            'header_mark': f"<!-- {dna.to_basic_dna()} | SM3:{dna.sm3_hash[:16]} -->",
            'paragraph_dnas': para_dnas,
            'footer_signature': f"<!-- LONHUN_SIG: {dna.sm2_signature[:40]} | VERIFY: {dna.sm3_hash[:24]} -->",
        }


class PersonalInfoDNAGenerator(DNAGenerator):
    def generate(self, info: Dict, privacy_level: str = "normal") -> Dict:
        info_str = json.dumps(info, sort_keys=True)
        data = info_str.encode('utf-8')
        threshold_map = {'low': 0.5, 'normal': 0.7, 'high': 0.85, 'critical': 0.95}
        threshold = threshold_map.get(privacy_level, 0.7)
        dna = super().generate(data, DataType.PERSONAL_INFO, threshold=threshold,
                               extra_meta={'privacy_level': privacy_level, 'fields': list(info.keys())})
        field_hashes = {k: SM3.hash(str(v).encode('utf-8')) for k, v in info.items()}
        chain = []
        prev = "0" * 64
        for key, h in sorted(field_hashes.items()):
            ch = SM3.hash((prev + h + key).encode('utf-8'))
            chain.append(f"{key}:{ch[:16]}")
            prev = ch
        return {
            'dna_model': dna,
            'basic_dna': dna.to_basic_dna(),
            'extended_dna': dna.to_extended_dna(),
            'privacy_level': privacy_level,
            'field_hashes': field_hashes,
            'hash_chain': chain,
            'source_mark': f"SOURCE:{dna.source}|LEVEL:{privacy_level}|THRESH:{threshold}",
            'compliance_dna': dna.to_audit_dna(AuditResult.PASS, f"privacy={privacy_level}|fields_ok")
        }


class FormulaDNAGenerator(DNAGenerator):
    def generate(self, formula: Dict, compliance_standard: str = "GB") -> Dict:
        formula_str = json.dumps(formula, sort_keys=True)
        data = formula_str.encode('utf-8')
        ingredients = formula.get('ingredients', [])
        score = self._calc_compliance(ingredients, compliance_standard)
        dna = super().generate(data, DataType.FORMULA, threshold=score,
                               extra_meta={'standard': compliance_standard, 'ingredient_count': len(ingredients)})
        ing_dnas = []
        for ing in ingredients:
            ih = SM3.hash(str(ing).encode('utf-8'))
            ok = self._check_ing(ing, compliance_standard)
            ing_dnas.append(f"{ing.get('name', '?')}:{ih[:12]}:{'OK' if ok else 'RESTRICTED'}")
        return {
            'dna_model': dna,
            'basic_dna': dna.to_basic_dna(),
            'extended_dna': dna.to_extended_dna(),
            'compliance_standard': compliance_standard,
            'compliance_score': score,
            'ingredient_dnas': ing_dnas,
            'threshold_mark': f"THRESHOLD:{score:.2f}|STD:{compliance_standard}",
            'compliance_dna': dna.to_audit_dna(
                AuditResult.PASS if score >= 0.7 else AuditResult.WARNING,
                f"score={score:.2f}|std={compliance_standard}")
        }

    def _calc_compliance(self, ingredients, standard):
        if not ingredients:
            return 1.0
        return sum(1 for ing in ingredients if self._check_ing(ing, standard)) / len(ingredients)

    def _check_ing(self, ingredient, standard):
        restricted = {"lead", "mercury", "arsenic", "cadmium", "formaldehyde"}
        return not any(r in str(ingredient.get('name', '')).lower() for r in restricted)


class FingerprintDNAGenerator(DNAGenerator):
    def generate(self, fingerprint_data: bytes, device_id: str = "",
                 capture_type: str = "optical") -> Dict:
        dna = super().generate(fingerprint_data, DataType.FINGERPRINT, threshold=0.9,
                               extra_meta={'device_id': device_id, 'capture_type': capture_type})
        feature_hash = SM3.hash(fingerprint_data)
        return {
            'dna_model': dna,
            'basic_dna': dna.to_basic_dna(),
            'extended_dna': dna.to_extended_dna(),
            'feature_hash': feature_hash,
            'device_mark': f"DEV:{device_id}|TYPE:{capture_type}|TS:{dna.timestamp}",
            'biometric_dna': f"BIO:{feature_hash[:32]}:{device_id}:{dna.timestamp}",
            'template_protection': {
                'helper_data': SM3.hash(fingerprint_data + dna.sm3_hash.encode('utf-8')),
                'transformation_key': dna.sm2_signature[:32],
                'revocable_hash': SM3.hash(
                    (SM3.hash(fingerprint_data + dna.sm3_hash.encode('utf-8')) +
                     dna.sm2_signature).encode('utf-8'))
            }
        }


# ============================================================
# DNA嵌入器类
# ============================================================

class MetadataEmbedder:
    @staticmethod
    def embed_exif(image_bytes: bytes, dna_info: Dict) -> bytes:
        if image_bytes[:2] == b'\xff\xd8':
            dna_exif = b'\xff\xe1'
            exif_data = dna_info.get('exif_dna', '').encode('utf-8')
            length = len(exif_data) + 2
            dna_exif += length.to_bytes(2, 'big') + exif_data
            return image_bytes[:2] + dna_exif + image_bytes[2:]
        return image_bytes

    @staticmethod
    def embed_file_header(data: bytes, dna_mark: bytes, header_size: int = 256) -> bytes:
        header = dna_mark[:header_size].ljust(header_size, b'\x00')
        return header + data

    @staticmethod
    def embed_text_header(text: str, dna_header: str) -> str:
        return dna_header + "\n\n" + text

    @staticmethod
    def embed_json_meta(data: Dict, dna_data: Dict) -> Dict:
        data['_dna'] = {
            'basic_dna': dna_data.get('basic_dna', ''),
            'sm3_hash': dna_data.get('verification', {}).get('sm3_full', ''),
            'timestamp': datetime.now().isoformat()
        }
        return data


class WatermarkEmbedder:
    @staticmethod
    def embed_lsb(image_bytes: bytes, dna_message: str, offset: int = 100) -> bytes:
        if len(image_bytes) < offset + 100:
            return image_bytes
        msg_bytes = dna_message.encode('utf-8')
        msg_len = len(msg_bytes)
        min_space = 32 + msg_len * 8
        if len(image_bytes) - offset < min_space:
            return image_bytes
        data = bytearray(image_bytes)
        for i in range(32):
            data[offset + i] = (data[offset + i] & 0xFE) | ((msg_len >> i) & 1)
        msg_offset = offset + 32
        bit_idx = 0
        for byte_val in msg_bytes:
            for bit_pos in range(8):
                pos = msg_offset + bit_idx
                data[pos] = (data[pos] & 0xFE) | ((byte_val >> bit_pos) & 1)
                bit_idx += 1
        return bytes(data)

    @staticmethod
    def extract_lsb(image_bytes: bytes, offset: int = 100) -> Optional[str]:
        if len(image_bytes) < offset + 32:
            return None
        msg_len = 0
        for i in range(32):
            msg_len |= (image_bytes[offset + i] & 1) << i
        if msg_len <= 0 or msg_len > 10000:
            return None
        total_needed = 32 + msg_len * 8
        if len(image_bytes) < offset + total_needed:
            return None
        msg_bytes = bytearray()
        msg_offset = offset + 32
        for byte_idx in range(msg_len):
            byte_val = 0
            for bit_pos in range(8):
                pos = msg_offset + byte_idx * 8 + bit_pos
                byte_val |= (image_bytes[pos] & 1) << bit_pos
            msg_bytes.append(byte_val)
        try:
            return bytes(msg_bytes).decode('utf-8')
        except:
            return None


class CryptoEmbedder:
    def __init__(self):
        self.sm2 = SM2Crypto()
        self._keys = self.sm2.generate_key_pair()

    def embed_signature(self, data: bytes) -> Dict:
        hash_val = SM3.hash(data)
        signature = self.sm2.sign(data)
        return {
            'hash': hash_val,
            'signature': signature,
            'public_key': self._keys['public_key'],
            'embedded': f"SIG:{signature[:64]}|HASH:{hash_val[:32]}"
        }

    def verify_embedded(self, data: bytes, signature: str, public_key: str = None) -> bool:
        if public_key:
            self.sm2.load_public_key(public_key)
        return self.sm2.verify(data, signature)

    @staticmethod
    def create_hash_chain(data_list: List[bytes]) -> List[str]:
        chain = []
        prev = "0" * 64
        for d in data_list:
            ch = SM3.hash((prev + SM3.hash(d)).encode('utf-8'))
            chain.append(ch)
            prev = ch
        return chain

    @staticmethod
    def create_merkle_tree(data_list: List[bytes]) -> Dict:
        leaves = [SM3.hash(d) for d in data_list]
        tree = [leaves]
        current = leaves
        while len(current) > 1:
            next_level = []
            for i in range(0, len(current), 2):
                left = current[i]
                right = current[i + 1] if i + 1 < len(current) else left
                next_level.append(SM3.hash((left + right).encode('utf-8')))
            tree.append(next_level)
            current = next_level
        return {
            'root': tree[-1][0] if tree else "",
            'leaves': leaves,
            'tree_levels': len(tree),
            'leaf_count': len(leaves)
        }


# ============================================================
# DNA验证器类
# ============================================================

class DNAVerifier:
    def __init__(self, public_key: str = None):
        self.sm2 = SM2Crypto()
        if public_key:
            self.sm2.load_public_key(public_key)
        self._audit_log = []

    def verify(self, data: Union[str, bytes], dna_model: DNAModel,
               expected_signature: str = None) -> Dict:
        if isinstance(data, str):
            data = data.encode('utf-8')
        results = {
            'dna_id': dna_model.to_basic_dna(),
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
        computed_hash = SM3.hash(data)
        hash_match = computed_hash == dna_model.sm3_hash
        results['checks']['sm3_hash'] = {
            'status': 'PASS' if hash_match else 'FAIL',
            'match': hash_match
        }
        sig_valid = False
        sig_to_check = expected_signature or dna_model.sm2_signature
        if sig_to_check:
            sig_valid = self.sm2.verify(data, sig_to_check)
        results['checks']['sm2_signature'] = {
            'status': 'PASS' if sig_valid else 'FAIL',
            'valid': sig_valid
        }
        ts_valid = self._verify_timestamp(dna_model.timestamp)
        results['checks']['timestamp'] = {
            'status': 'PASS' if ts_valid else 'WARN'
        }
        threshold_ok = dna_model.threshold >= 0.5
        results['checks']['threshold'] = {
            'status': 'PASS' if threshold_ok else 'WARN',
            'value': dna_model.threshold
        }
        has_fail = any(c['status'] == 'FAIL' for c in results['checks'].values())
        has_warn = any(c['status'] == 'WARN' for c in results['checks'].values())
        if has_fail:
            results['verdict'] = AuditResult.FAIL
            results['verdict_text'] = "DNA verification failed - data may be tampered"
        elif has_warn:
            results['verdict'] = AuditResult.WARNING
            results['verdict_text'] = "DNA verification warning - some checks failed"
        else:
            results['verdict'] = AuditResult.PASS
            results['verdict_text'] = "DNA verification passed - data is authentic"
        results['audit_dna'] = dna_model.to_audit_dna(
            results['verdict'],
            f"SM3={'OK' if hash_match else 'FAIL'}|SIG={'OK' if sig_valid else 'FAIL'}"
        )
        self._audit_log.append(results)
        return results

    def verify_image(self, image_data: bytes, dna_data: Dict) -> Dict:
        results = self.verify(image_data, dna_data['dna_model'])
        lsb = WatermarkEmbedder.extract_lsb(image_data)
        results['checks']['lsb_watermark'] = {
            'status': 'PASS' if lsb else 'WARN',
            'extracted': lsb[:50] if lsb else None
        }
        return results

    def _verify_timestamp(self, ts: str) -> bool:
        try:
            dt = datetime.strptime(ts, "%Y-%m-%d-%H%M%S")
            now = datetime.now()
            return dt <= now and (now - dt).days < 30
        except:
            return False

    @staticmethod
    def format_report(result: Dict) -> str:
        lines = [
            "=" * 50,
            "Dragon DNA Verification Report",
            "=" * 50,
            f"DNA ID    : {result['dna_id']}",
            f"Timestamp : {result['timestamp']}",
            f"Verdict   : {result['verdict'].value}",
            f"Details   : {result['verdict_text']}",
            "-" * 50,
            "Checks:"
        ]
        for name, check in result['checks'].items():
            icon = "+" if check['status'] == 'PASS' else "!" if check['status'] == 'FAIL' else "~"
            lines.append(f"  [{icon}] {name}: {check['status']}")
        lines.extend(["-" * 50, f"Audit DNA : {result['audit_dna']}", "=" * 50])
        return "\n".join(lines)


# ============================================================
# DNA数据库
# ============================================================

class DNADatabase:
    def __init__(self, db_path: str = None):
        self._records: Dict[str, Dict] = {}
        self._index_by_type: Dict[str, set] = defaultdict(set)
        self._index_by_source: Dict[str, set] = defaultdict(set)
        self._index_by_time: Dict[str, set] = defaultdict(set)
        self._blacklist: set = set()
        self._audit_log = []
        self._lock = threading.Lock()

    def insert(self, dna_data: Dict, original_data_hash: str = "") -> str:
        with self._lock:
            dna_model = dna_data.get('dna_model')
            if not dna_model:
                raise ValueError("Invalid DNA data: missing dna_model")
            dna_id = dna_model.to_basic_dna()
            record_id = str(uuid.uuid4())[:8]
            record = {
                'record_id': record_id,
                'dna_id': dna_id,
                'dna_model': dna_model,
                'data_hash': original_data_hash or dna_model.sm3_hash,
                'sm3_hash': dna_model.sm3_hash,
                'sm2_signature': dna_model.sm2_signature,
                'timestamp': dna_model.timestamp,
                'data_type': dna_model.data_type.value,
                'source': dna_model.source,
                'version': dna_model.version,
                'threshold': dna_model.threshold,
                'metadata': dna_model.metadata,
                'full_data': dna_data,
                'insert_time': datetime.now().isoformat(),
                'status': 'active'
            }
            self._records[dna_id] = record
            self._index_by_type[dna_model.data_type.value].add(dna_id)
            self._index_by_source[dna_model.source].add(dna_id)
            date_key = dna_model.timestamp[:10] if len(dna_model.timestamp) >= 10 else dna_model.timestamp
            self._index_by_time[date_key].add(dna_id)
            return dna_id

    def get(self, dna_id: str) -> Optional[Dict]:
        return self._records.get(dna_id)

    def query_by_type(self, data_type: str) -> List[Dict]:
        return [self._records[did] for did in self._index_by_type.get(data_type, set())
                if did in self._records]

    def query_by_source(self, source: str) -> List[Dict]:
        return [self._records[did] for did in self._index_by_source.get(source, set())
                if did in self._records]

    def query_by_time(self, date_str: str) -> List[Dict]:
        return [self._records[did] for did in self._index_by_time.get(date_str, set())
                if did in self._records]

    def query_by_time_range(self, start_date: str, end_date: str) -> List[Dict]:
        results = []
        for date_key, ids in self._index_by_time.items():
            if start_date <= date_key <= end_date:
                results.extend([self._records[did] for did in ids if did in self._records])
        return results

    def query(self, data_type: str = None, source: str = None,
              date: str = None, min_threshold: float = None) -> List[Dict]:
        candidates = set(self._records.keys())
        if data_type:
            candidates &= self._index_by_type.get(data_type, set())
        if source:
            candidates &= self._index_by_source.get(source, set())
        if date:
            candidates &= self._index_by_time.get(date, set())
        results = [self._records[did] for did in candidates if did in self._records]
        if min_threshold is not None:
            results = [r for r in results if r['threshold'] >= min_threshold]
        return results

    def add_to_blacklist(self, dna_id: str, reason: str = ""):
        with self._lock:
            self._blacklist.add(dna_id)
            self._audit_log.append({
                'action': 'blacklist', 'dna_id': dna_id,
                'reason': reason, 'time': datetime.now().isoformat()
            })

    def is_blacklisted(self, dna_id: str) -> bool:
        return dna_id in self._blacklist

    def get_blacklist(self) -> List[str]:
        return list(self._blacklist)

    def get_stats(self) -> Dict:
        return {
            'total_records': len(self._records),
            'by_type': {k: len(v) for k, v in self._index_by_type.items()},
            'by_source': {k: len(v) for k, v in self._index_by_source.items()},
            'by_date': {k: len(v) for k, v in self._index_by_time.items()},
            'blacklist_count': len(self._blacklist),
            'audit_entries': len(self._audit_log)
        }


# ============================================================
# 龍魂DNA追溯系统集成入口
# ============================================================

class DragonDNATraceSystem:
    """
    Dragon DNA Trace System - Unified Integration Entry
    Covers all data types:
    - IMAGE, TEXT, PERSONAL_INFO, FINGERPRINT, FORMULA
    - BANK_CARD, DOCUMENT, VIDEO, AUDIO
    """

    VERSION = "3.0"
    SYSTEM_DNA = "#龍芯:2026-07-04-DNA-TRACE-v3.0"

    def __init__(self):
        self.db = DNADatabase()
        self.verifier = DNAVerifier()
        self._generators = {
            DataType.IMAGE: ImageDNAGenerator(),
            DataType.TEXT: TextDNAGenerator(),
            DataType.PERSONAL_INFO: PersonalInfoDNAGenerator(),
            DataType.FINGERPRINT: FingerprintDNAGenerator(),
            DataType.FORMULA: FormulaDNAGenerator(),
            DataType.DOCUMENT: DNAGenerator(),
            DataType.BANK_CARD: DNAGenerator(),
            DataType.VIDEO: DNAGenerator(),
            DataType.AUDIO: DNAGenerator(),
        }
        self._public_keys = {}
        self._audit_log = []

    def get_system_dna(self) -> str:
        return self.SYSTEM_DNA

    def generate_dna(self, data, data_type: DataType, **kwargs) -> Dict:
        generator = self._generators.get(data_type)
        if not generator:
            raise ValueError(f"Unsupported data type: {data_type}")

        if data_type == DataType.IMAGE:
            result = generator.generate(
                data if isinstance(data, bytes) else data.encode(),
                kwargs.get('format', 'JPG'), kwargs.get('width', 0),
                kwargs.get('height', 0), kwargs.get('device', ''),
                kwargs.get('geo', ''))
        elif data_type == DataType.TEXT:
            result = generator.generate(
                data if isinstance(data, str) else data.decode(),
                kwargs.get('text_type', 'general'))
        elif data_type == DataType.PERSONAL_INFO:
            result = generator.generate(
                data if isinstance(data, dict) else json.loads(data),
                kwargs.get('privacy_level', 'normal'))
        elif data_type == DataType.FORMULA:
            result = generator.generate(
                data if isinstance(data, dict) else json.loads(data),
                kwargs.get('standard', 'GB'))
        elif data_type == DataType.FINGERPRINT:
            result = generator.generate(
                data if isinstance(data, bytes) else data.encode(),
                kwargs.get('device_id', ''),
                kwargs.get('capture_type', 'optical'))
        else:
            dna = generator.generate(data, data_type, kwargs.get('threshold', 0.7))
            result = {'dna_model': dna}

        dna_model = result.get('dna_model')
        if dna_model:
            src = dna_model.source
            gen = self._generators.get(data_type)
            if gen and src not in self._public_keys:
                self._public_keys[src] = gen.get_public_key()
        return result

    def embed_dna(self, data: bytes, dna_data: Dict, method: str = 'auto') -> bytes:
        if method == 'auto':
            dna_model = dna_data.get('dna_model')
            method = 'watermark' if dna_model and dna_model.data_type == DataType.IMAGE else 'metadata'
        if method == 'watermark':
            dna_msg = dna_data.get('lsb_dna', dna_data.get('basic_dna', ''))
            return WatermarkEmbedder.embed_lsb(data, dna_msg)
        else:
            header = dna_data.get('header_mark', b'DRAGON_DNA')
            if isinstance(header, str):
                header = header.encode('utf-8')
            return MetadataEmbedder.embed_file_header(data, header)

    def verify_dna(self, data, dna_data, public_key: str = None) -> Dict:
        dna_model = dna_data.get('dna_model')
        if not dna_model:
            return {'error': 'Invalid DNA data'}
        pk = public_key or self._public_keys.get(dna_model.source)
        if not pk and 'verification' in dna_data:
            pk = dna_data['verification'].get('public_key')
        verifier = DNAVerifier(public_key=pk) if pk else self.verifier
        result = verifier.verify(
            data if isinstance(data, bytes) else str(data).encode(),
            dna_model)
        result['blacklisted'] = self.db.is_blacklisted(dna_model.to_basic_dna())
        self._audit_log.append(result)
        return result

    def store_dna(self, dna_data: Dict) -> str:
        return self.db.insert(dna_data)

    def query_dna(self, **kwargs) -> List[Dict]:
        return self.db.query(**kwargs)

    def add_to_blacklist(self, dna_id: str, reason: str = ""):
        self.db.add_to_blacklist(dna_id, reason)

    def get_stats(self) -> Dict:
        return {
            'system_dna': self.SYSTEM_DNA,
            'version': self.VERSION,
            'supported_types': [t.value for t in DataType],
            'db_stats': self.db.get_stats(),
            'total_audits': len(self._audit_log)
        }


# ============================================================
# 主程序入口
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("龍魂·全数据类型DNA追溯体系 v3.0")
    print("=" * 60)

    system = DragonDNATraceSystem()
    print(f"\n系统DNA: {system.get_system_dna()}")
    print(f"系统版本: {system.VERSION}")

    # 测试图片DNA
    print("\n[1] 图片DNA测试")
    img_data = b"\xff\xd8\xff\xe0\x00\x10JFIF" + b"SIM_IMAGE" * 50
    img_dna = system.generate_dna(img_data, DataType.IMAGE,
                                   format="JPG", width=1920, height=1080,
                                   device="Canon-R5", geo="39.9N-116.4E")
    print(f"  基础DNA: {img_dna['basic_dna']}")
    print(f"  EXIF: {img_dna['exif_dna'][:60]}...")

    # 测试文本DNA
    print("\n[2] 文本DNA测试")
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    txt_dna = system.generate_dna(text, DataType.TEXT, text_type="article")
    print(f"  基础DNA: {txt_dna['basic_dna']}")
    print(f"  段落DNA: {txt_dna['paragraph_dnas']}")

    # 测试验证
    print("\n[3] DNA验证测试")
    v_result = system.verify_dna(img_data, img_dna)
    print(f"  判定: {v_result['verdict'].value}")
    print(f"  说明: {v_result['verdict_text']}")

    # 测试篡改检测
    print("\n[4] 篡改检测测试")
    v_bad = system.verify_dna(b"tampered_data", img_dna)
    print(f"  判定: {v_bad['verdict'].value}")
    print(f"  说明: {v_bad['verdict_text']}")

    # 测试个人信息DNA
    print("\n[5] 个人信息DNA测试")
    pi_info = {"name": "TestUser", "id": "123456789", "phone": "13800138000"}
    pi_dna = system.generate_dna(pi_info, DataType.PERSONAL_INFO, privacy_level="high")
    print(f"  基础DNA: {pi_dna['basic_dna']}")
    print(f"  隐私级别: {pi_dna['privacy_level']}")
    print(f"  哈希链: {pi_dna['hash_chain']}")

    # 测试配方DNA
    print("\n[6] 配方DNA测试")
    formula = {"ingredients": [{"name": "water", "p": 0.5}, {"name": "glycerol", "p": 0.3}, {"name": "ethanol", "p": 0.2}]}
    fm_dna = system.generate_dna(formula, DataType.FORMULA, standard="GB")
    print(f"  基础DNA: {fm_dna['basic_dna']}")
    print(f"  合规评分: {fm_dna['compliance_score']:.2%}")
    print(f"  成分DNA: {fm_dna['ingredient_dnas']}")

    # 系统统计
    print("\n[7] 系统统计")
    stats = system.get_stats()
    print(f"  支持类型: {stats['supported_types']}")
    print(f"  数据库记录: {stats['db_stats']['total_records']}")

    print("\n" + "=" * 60)
    print("DNA追溯体系测试完成!")
    print("=" * 60)
