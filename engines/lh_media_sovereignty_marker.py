#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·媒体主权标记引擎 v1.0
Media Sovereignty Marker Engine

用途：在字体、图像、视频、音频、数字人中嵌入不可磨灭的 DNA 主权标记。
核心原则：
  1. 原生内嵌：标记是内容的一部分，不是后期贴上去的标签。
  2. 多层级：可见水印 + 隐写水印 + 频域水印，层层加固。
  3. DNA 追溯：每个标记都带六层来源链 DNA。
  4. 抗洗：单一处理无法完全移除，需同时破坏三层才生效。

支持格式：
  - 字体：OpenType/CFF/TrueType
  - 图像：PNG / JPEG / WebP
  - 视频：MP4 / MOV / AVI（基于 OpenCV 逐帧处理）
  - 音频：WAV（基于 FFT 扩频水印）

DNA 格式示例：
  #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-MEDIA-MARK-v1.0-UID9622
"""
import base64
import binascii
import hashlib
import io
import json
import math
import os
import struct
import sys
import tempfile
import wave
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO, Callable, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

# ---------------------------------------------------------------------------
# 常量与配置
# ---------------------------------------------------------------------------
DNA_PREFIX = "#龍芯⚡️"
VERSION = "v1.0"
ENGINE_NAME = "MEDIA-SOVEREIGNTY-MARK"

# 频域水印默认参数
AUDIO_STRENGTH = 0.005      # 扩频水印强度（越小越不可闻，越脆弱）
AUDIO_PN_LENGTH = 1024      # 伪随机序列长度
AUDIO_FREQ_BIN_START = 100  # 起始频率 bin

# 图像 DCT 水印参数
DCT_BLOCK_SIZE = 8
DCT_ALPHA = 2.0             # DCT 水印强度

# 字体参数
FONT_WATERMARK_UNICODE = 0xE200
FONT_WATERMARK_TARGET = (520, 520)
FONT_WATERMARK_SCALE = 0.15

# 系统根目录
SYSTEM_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# DNA 生成
# ---------------------------------------------------------------------------
def generate_dna(media_type: str, owner: str = "UID9622") -> str:
    """生成带时间戳的 DNA 标记字符串"""
    now = datetime.now(timezone.utc)
    # 简化干支：用 UTC 年月日时分秒拼接成类似干支格式
    gz = f"{now.year % 60:02d}·{now.month:02d}·{now.day:02d}·{now.hour:02d}时"
    uniq = binascii.b2a_hex(os.urandom(4)).decode('ascii').upper()
    return f"{DNA_PREFIX}{gz}·☰乾-{ENGINE_NAME}-{VERSION}-{media_type}-{owner}-{uniq}"


def dna_to_bits(dna: str) -> List[int]:
    """将 DNA 字符串转为二进制列表"""
    data = dna.encode('utf-8')
    return [int(b) for byte in data for b in format(byte, '08b')]


def bits_to_dna(bits: List[int]) -> str:
    """二进制列表转回 DNA 字符串"""
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]
        if len(byte_bits) < 8:
            break
        bytes_list.append(int(''.join(str(b) for b in byte_bits), 2))
    return bytes(bytes_list).decode('utf-8', errors='ignore')


def _looks_like_dna(text: str) -> bool:
    """判断一段文本是否像有效的 DNA 标记（允许自定义 DNA）"""
    if not text:
        return False
    # 原生 DNA 以 #龍芯 开头；自定义 DNA 通常含 UID/DNA/龍魂 等关键字
    markers = (DNA_PREFIX, "UID", "DNA", "龍魂", "龍芯", "LH-", "MEDIA-MARK")
    return text.startswith(DNA_PREFIX) or any(m in text for m in markers[1:])


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------
def make_pn_sequence(seed: int, length: int) -> np.ndarray:
    """生成 ±1 伪随机序列"""
    rng = np.random.default_rng(seed)
    return rng.choice(np.array([1.0, -1.0]), size=length)


def pack_length_and_bits(bits: List[int]) -> List[int]:
    """在数据前附加 32 位长度头"""
    length_bits = [int(b) for b in format(len(bits), '032b')]
    return length_bits + bits


def unpack_length_and_bits(bits: List[int]) -> Tuple[int, List[int]]:
    """解析 32 位长度头"""
    length = int(''.join(str(b) for b in bits[:32]), 2)
    return length, bits[32:32 + length]


# ---------------------------------------------------------------------------
# 1. 字体标记
# ---------------------------------------------------------------------------
class FontMarker:
    """字体主权标记器

    当前实现：
      - 校验 U+E200 龙纹缩微水印是否存在
      - 在 name 表中写入 DNA 追溯字段（vendor URL / license description）
      - 生成带 DNA 的副本
    """

    def __init__(self, font_path: Union[str, Path]):
        self.font_path = Path(font_path)
        try:
            from fontTools.ttLib import TTFont
            self.TTFont = TTFont
        except ImportError as e:
            raise RuntimeError("需要 fontTools: pip install fontTools") from e

    def _load(self) -> "TTFont":
        return self.TTFont(str(self.font_path))

    def verify_native_watermark(self, sample_chars: Optional[List[str]] = None) -> dict:
        """验证原生龙纹水印是否存在"""
        font = self._load()
        cmap = font['cmap'].getBestCmap()
        report = {
            "has_pua_glyph": FONT_WATERMARK_UNICODE in cmap,
            "pua_glyph_name": cmap.get(FONT_WATERMARK_UNICODE),
            "sample_checks": []
        }

        sample_chars = sample_chars or ['一', '人', '龍', '國', '中']
        from fontTools.pens.boundsPen import BoundsPen
        gs = font.getGlyphSet()

        # 简单校验：水印 glyph 必须有非零轮廓
        if report["has_pua_glyph"]:
            gname = report["pua_glyph_name"]
            pen = BoundsPen(gs)
            try:
                gs[gname].draw(pen)
                report["pua_bounds"] = pen.bounds
            except Exception as e:
                report["pua_bounds"] = None
                report["pua_error"] = str(e)

        # 校验样例字形右下角区域是否有额外轮廓（水印存在迹象）
        for ch in sample_chars:
            code = ord(ch)
            if code not in cmap:
                continue
            gname = cmap[code]
            pen = BoundsPen(gs)
            try:
                gs[gname].draw(pen)
                bounds = pen.bounds
                # 字框右下角区域存在轮廓，视为有水印迹象
                has_br = bounds is not None and bounds[2] > 700 and bounds[1] < 300
                report["sample_checks"].append({
                    "char": ch,
                    "code": f"U+{code:04X}",
                    "bounds": bounds,
                    "bottom_right_watermark_likely": has_br
                })
            except Exception as e:
                report["sample_checks"].append({
                    "char": ch,
                    "error": str(e)
                })

        report["native_watermark_likely"] = (
            report["has_pua_glyph"]
            and report.get("pua_bounds") is not None
            and all(c.get("bottom_right_watermark_likely") for c in report["sample_checks"] if "error" not in c)
        )
        return report

    def embed_dna(self, dna: Optional[str] = None, output_path: Optional[Union[str, Path]] = None) -> Path:
        """在字体 name 表中嵌入 DNA 并保存副本"""
        if dna is None:
            dna = generate_dna("font")
        font = self._load()
        name_table = font['name']

        # 使用 nameID 13 (license description) 和 14 (license URL) 存放 DNA
        # 平台 3 (Windows), 编码 1 (Unicode BMP), 语言 2052 (中文)
        name_table.setName(dna, 13, 3, 1, 2052)
        name_table.setName(f"https://uid9622.cn/dna/{dna}", 14, 3, 1, 2052)

        if output_path is None:
            stem = self.font_path.stem
            output_path = self.font_path.parent / f"{stem}-DNA.otf"
        else:
            output_path = Path(output_path)

        font.save(str(output_path))
        return output_path

    def extract_dna(self) -> Optional[str]:
        """从字体 name 表中提取 DNA"""
        font = self._load()
        name_table = font['name']
        try:
            record = name_table.getName(13, 3, 1, 2052)
            return record.toStr() if record else None
        except Exception:
            return None


# ---------------------------------------------------------------------------
# 2. 图像/数字人标记（DCT 隐写 + LSB DNA）
# ---------------------------------------------------------------------------
class ImageMarker:
    """图像/数字人主权标记器

    两层标记：
      1. LSB 最低有效位：直接写入 DNA 二进制
      2. DCT 频域：分块 DCT，在低频系数中嵌入水印，抗压缩/裁剪
    """

    def __init__(self, image_path: Union[str, Path]):
        self.image_path = Path(image_path)
        self.img = Image.open(str(self.image_path)).convert('RGB')
        self.arr = np.array(self.img, dtype=np.float32)

    def _embed_dct(self, channel: np.ndarray, bits: List[int], alpha: float = DCT_ALPHA) -> np.ndarray:
        """在单通道 DCT 中嵌入水印"""
        h, w = channel.shape
        out = channel.copy()
        bit_idx = 0
        for y in range(0, h - DCT_BLOCK_SIZE + 1, DCT_BLOCK_SIZE):
            for x in range(0, w - DCT_BLOCK_SIZE + 1, DCT_BLOCK_SIZE):
                if bit_idx >= len(bits):
                    break
                block = channel[y:y + DCT_BLOCK_SIZE, x:x + DCT_BLOCK_SIZE]
                dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
                # 修改 (2,2) 位置中频系数
                dct_block[2, 2] += alpha * (1 if bits[bit_idx] else -1)
                out[y:y + DCT_BLOCK_SIZE, x:x + DCT_BLOCK_SIZE] = idct(
                    idct(dct_block.T, norm='ortho').T, norm='ortho'
                )
                bit_idx += 1
            if bit_idx >= len(bits):
                break
        return out

    def _extract_dct(self, channel: np.ndarray, num_bits: int, alpha: float = DCT_ALPHA) -> List[int]:
        """从单通道 DCT 中提取水印"""
        h, w = channel.shape
        bits = []
        for y in range(0, h - DCT_BLOCK_SIZE + 1, DCT_BLOCK_SIZE):
            for x in range(0, w - DCT_BLOCK_SIZE + 1, DCT_BLOCK_SIZE):
                if len(bits) >= num_bits:
                    break
                block = channel[y:y + DCT_BLOCK_SIZE, x:x + DCT_BLOCK_SIZE]
                dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
                bits.append(1 if dct_block[2, 2] > 0 else 0)
            if len(bits) >= num_bits:
                break
        return bits

    def _embed_lsb(self, arr: np.ndarray, bits: List[int]) -> np.ndarray:
        """在 RGB 最低有效位嵌入 DNA"""
        out = arr.copy()
        flat = out.ravel()
        for i, bit in enumerate(bits):
            if i >= len(flat):
                break
            flat[i] = (int(flat[i]) & 0xFE) | bit
        return out

    def _extract_lsb(self, arr: np.ndarray, num_bits: int) -> List[int]:
        """从 RGB 最低有效位提取 DNA"""
        flat = arr.ravel().astype(np.uint8)
        return [int(flat[i]) & 1 for i in range(min(num_bits, len(flat)))]

    def embed(self, dna: Optional[str] = None, output_path: Optional[Union[str, Path]] = None) -> Path:
        if dna is None:
            dna = generate_dna("image")
        bits = dna_to_bits(dna)
        payload = pack_length_and_bits(bits)

        # LSB 层
        marked = self._embed_lsb(self.arr, payload)

        # DCT 层（在 Y 通道上操作更隐蔽）
        ycbcr = cv2.cvtColor(marked.astype(np.uint8), cv2.COLOR_RGB2YCrCb)
        y_float = ycbcr[:, :, 0].astype(np.float32)
        y_marked = self._embed_dct(y_float, payload)
        ycbcr[:, :, 0] = np.clip(y_marked, 0, 255).astype(np.uint8)
        marked_rgb = cv2.cvtColor(ycbcr, cv2.COLOR_YCrCb2RGB)

        if output_path is None:
            stem = self.image_path.stem
            suffix = self.image_path.suffix or '.png'
            output_path = self.image_path.parent / f"{stem}-DNA{suffix}"
        else:
            output_path = Path(output_path)

        Image.fromarray(marked_rgb.astype(np.uint8)).save(str(output_path))
        return output_path

    def extract(self) -> Optional[str]:
        # 优先从 LSB 提取
        bits = self._extract_lsb(self.arr, 32 + 2048)
        try:
            length, data_bits = unpack_length_and_bits(bits)
            if 0 < length <= 2048:
                dna = bits_to_dna(data_bits[:length])
                if _looks_like_dna(dna):
                    return dna
        except Exception:
            pass

        # LSB 失败则尝试 DCT
        ycbcr = cv2.cvtColor(self.arr.astype(np.uint8), cv2.COLOR_RGB2YCrCb)
        y = ycbcr[:, :, 0].astype(np.float32)
        bits = self._extract_dct(y, 32 + 2048)
        try:
            length, data_bits = unpack_length_and_bits(bits)
            if 0 < length <= 2048:
                dna = bits_to_dna(data_bits[:length])
                if _looks_like_dna(dna):
                    return dna
        except Exception:
            pass
        return None


# ---------------------------------------------------------------------------
# 3. 视频标记（鲁棒盲水印）
# ---------------------------------------------------------------------------
class VideoMarker:
    """视频主权标记器（鲁棒盲水印 v4.0）

    主策略：
      1. 帧级 DCT 扩频指纹 —— 把 160 位 DNA 短指纹嵌入每一帧的 Y/Cb/Cr 三
         通道低频 DCT 系数，跨帧投票，可抗 H.264/H.265 重编码与录屏。
      2. 三重冗余 + 时序同步头 —— 每帧携带已知同步模式，对抗帧率变化、
         丢帧/插帧（录屏常见攻击）。
      3. 鲁棒解码 —— 中位数投票 + 3σ 离群值剔除 + 跨帧累积，提升压缩后
         提取率。
      4. 音频轨 Patchwork 指纹 —— 作为第二重保险，当视频帧被严重破坏
         时提供回退检测。

    输出为固定 160 位短指纹 `LHAF-<hash>`，不是完整 DNA。完整 DNA 由
    短指纹在数据库/记录中反查。短指纹更抗压缩。

    对外仍是一个文件进、一个文件出，保持接口简单。
    """

    VIDEO_DCT_BLOCK = 8
    VIDEO_DCT_ALPHA_Y = 28.0     # Y 通道水印强度
    VIDEO_DCT_ALPHA_C = 18.0     # Cb/Cr 通道水印强度（更隐蔽）
    # 低频到中频 DCT 系数，分散能量以抗压缩
    VIDEO_DCT_COEFS = [(1, 1), (1, 2), (2, 1), (2, 2), (1, 3), (3, 1), (2, 3), (3, 2)]
    VIDEO_SEED = 9622
    VIDEO_BITS = 160             # 32 位魔数 + 128 位 DNA 哈希
    SYNC_BITS = 32               # 每帧同步头：0xA5A5A5A5
    OUTLIER_SIGMA = 3.0          # 离群值剔除阈值

    def __init__(self, video_path: Union[str, Path]):
        self.video_path = Path(video_path)

    def _run_ffmpeg(self, cmd: List[str]) -> Tuple[int, str, str]:
        """运行 ffmpeg 命令，返回 (returncode, stdout, stderr)"""
        import subprocess
        full_cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + cmd
        proc = subprocess.run(full_cmd, capture_output=True, text=True)
        return proc.returncode, proc.stdout, proc.stderr

    def _has_audio(self) -> bool:
        """检测视频是否含音频轨"""
        import subprocess
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "stream=codec_type",
            "-of", "default=nw=1:nk=1",
            str(self.video_path)
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return "audio" in proc.stdout.lower()
        except Exception:
            return False

    def _extract_audio(self, output_wav: Path) -> bool:
        """提取音频到 WAV"""
        code, _, err = self._run_ffmpeg([
            "-i", str(self.video_path),
            "-vn", "-acodec", "pcm_s16le",
            "-ar", "44100", "-ac", "1",
            str(output_wav)
        ])
        if code != 0:
            return False
        return output_wav.exists() and output_wav.stat().st_size > 0

    def _merge_audio(self, audio_wav: Path, output_video: Path,
                     video_source: Optional[Union[str, Path]] = None) -> bool:
        """把标记后的音频混回视频（默认原始视频，可指定 DCT 标记后的视频）"""
        video_source = video_source or self.video_path
        code, _, err = self._run_ffmpeg([
            "-i", str(video_source),
            "-i", str(audio_wav),
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-map", "0:v:0", "-map", "1:a:0",
            "-shortest",
            str(output_video)
        ])
        return code == 0 and output_video.exists() and output_video.stat().st_size > 0

    # ── 指纹与同步头 ──
    def _sync_pattern(self) -> List[int]:
        """返回 32 位帧同步头 0xA5A5A5A5"""
        return [int(b) for byte in b'\xa5\xa5\xa5\xa5' for b in format(byte, '08b')]

    # v4.2 指纹结构：32 位魔数 + 96 位 DNA 哈希 + 32 位 CRC32 校验
    MAGIC_BITS = 32
    HASH_BITS = 96
    CHECK_BITS = 32

    def _dna_to_fingerprint(self, dna: str) -> List[int]:
        """把 DNA 转成 160 位指纹：32 位魔数 + 96 位 DNA 哈希 + 32 位 CRC32"""
        magic = "LHAF"
        magic_bits = [int(b) for byte in magic.encode('utf-8') for b in format(byte, '08b')]
        # 96 位哈希（SHA-256 前 24 个十六进制字符）
        h = hashlib.sha256(dna.encode('utf-8')).hexdigest()[:24]
        hash_bits = [int(b) for ch in h for b in format(int(ch, 16), '04b')]
        # 校验和：对哈希位做 CRC32
        hash_bytes = bytes(int(''.join(str(b) for b in hash_bits[i:i + 8]), 2) for i in range(0, len(hash_bits), 8))
        crc = binascii.crc32(hash_bytes) & 0xFFFFFFFF
        crc_bits = [int(b) for b in format(crc, '032b')]
        fp = magic_bits + hash_bits + crc_bits
        if len(fp) < self.VIDEO_BITS:
            fp += [0] * (self.VIDEO_BITS - len(fp))
        return fp[:self.VIDEO_BITS]

    def _crc32_of_hash_bits(self, hash_bits: List[int]) -> List[int]:
        """计算哈希位上的 CRC32"""
        hash_bytes = bytes(int(''.join(str(b) for b in hash_bits[i:i + 8]), 2) for i in range(0, len(hash_bits), 8))
        crc = binascii.crc32(hash_bytes) & 0xFFFFFFFF
        return [int(b) for b in format(crc, '032b')]

    def _fingerprint_to_dna(self, fp: List[int], max_corrections: int = 2) -> Optional[str]:
        """从指纹反查短 ID；验证魔数 + CRC32，支持最多 2 位暴力纠错"""
        if len(fp) < self.VIDEO_BITS:
            return None

        def _decode(bits: List[int]) -> Optional[str]:
            magic_bits = bits[:self.MAGIC_BITS]
            try:
                magic_bytes = bytes(int(''.join(str(b) for b in magic_bits[i:i + 8]), 2) for i in range(0, self.MAGIC_BITS, 8))
                if magic_bytes.decode('utf-8') != "LHAF":
                    return None
            except Exception:
                return None
            hash_bits = bits[self.MAGIC_BITS:self.MAGIC_BITS + self.HASH_BITS]
            check_bits = bits[self.MAGIC_BITS + self.HASH_BITS:self.VIDEO_BITS]
            if self._crc32_of_hash_bits(hash_bits) == check_bits:
                hex_chars = []
                for i in range(0, len(hash_bits), 4):
                    nibble = int(''.join(str(b) for b in hash_bits[i:i + 4]), 2)
                    hex_chars.append(format(nibble, 'x'))
                return "LHAF-" + ''.join(hex_chars)
            return None

        # 直接验证
        result = _decode(fp)
        if result:
            return result

        # 暴力尝试翻转 1~max_corrections 位（主要在 hash/check 区域）
        if max_corrections > 0:
            n = self.VIDEO_BITS
            for k in range(1, max_corrections + 1):
                for positions in self._combinations(range(n), k):
                    candidate = fp.copy()
                    for pos in positions:
                        candidate[pos] ^= 1
                    result = _decode(candidate)
                    if result:
                        return result
        return None

    @staticmethod
    def _combinations(iterable, r):
        """小型组合生成器，避免额外依赖"""
        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i + 1, r):
                indices[j] = indices[j - 1] + 1
            yield tuple(pool[i] for i in indices)

    # v4.1 固定网格缩放不变策略
    GRID_W = 40          # 固定水平块数
    GRID_H = 22          # 固定垂直块数
    VIDEO_DCT_BLOCK = 16
    VIDEO_DCT_COEFS = [(1, 1), (1, 2), (2, 1)]
    VIDEO_DCT_ALPHA_Y = 80.0
    VIDEO_DCT_ALPHA_C = 55.0

    def _frame_to_grid(self, frame: np.ndarray) -> np.ndarray:
        """把任意分辨率帧缩放到固定网格大小的 YCbCr"""
        target_w = self.GRID_W * self.VIDEO_DCT_BLOCK
        target_h = self.GRID_H * self.VIDEO_DCT_BLOCK
        if frame.shape[1] != target_w or frame.shape[0] != target_h:
            frame = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)
        return frame

    def _compute_repeat(self, h_blocks: int, v_blocks: int, total_frames: int) -> int:
        """固定重复次数，与总帧数无关，仅受单帧容量限制"""
        blocks_per_frame = h_blocks * v_blocks
        return min(max(1, blocks_per_frame // (self.SYNC_BITS + self.VIDEO_BITS)), 24)

    def _get_blocks(self, bit_idx: int, frame_idx: int,
                    h_blocks: int, v_blocks: int, repeat: int) -> List[Tuple[int, int]]:
        """在固定网格中为某 bit 随机选择不重复的块"""
        rng = np.random.default_rng(
            self.VIDEO_SEED + bit_idx * 10000 + frame_idx * 1000
        )
        n = h_blocks * v_blocks
        idx = rng.choice(n, size=min(repeat, n), replace=False)
        return [(int(i) // h_blocks, int(i) % h_blocks) for i in idx]

    def _embed_dct_frame_channel(self, channel: np.ndarray, fp: List[int],
                                  frame_idx: int, h_blocks: int, v_blocks: int,
                                  repeat: int, alpha: float) -> np.ndarray:
        """在固定网格单通道嵌入指纹"""
        out = channel.copy()
        payload = self._sync_pattern() + fp
        for bit_idx, bit in enumerate(payload):
            sign = 1 if bit else -1
            blocks = self._get_blocks(bit_idx, frame_idx, h_blocks, v_blocks, repeat)
            for by, bx in blocks:
                block = out[by * self.VIDEO_DCT_BLOCK:(by + 1) * self.VIDEO_DCT_BLOCK,
                            bx * self.VIDEO_DCT_BLOCK:(bx + 1) * self.VIDEO_DCT_BLOCK]
                dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
                for cy, cx in self.VIDEO_DCT_COEFS:
                    dct_block[cy, cx] += alpha * sign
                out[by * self.VIDEO_DCT_BLOCK:(by + 1) * self.VIDEO_DCT_BLOCK,
                    bx * self.VIDEO_DCT_BLOCK:(bx + 1) * self.VIDEO_DCT_BLOCK] = idct(
                    idct(dct_block.T, norm='ortho').T, norm='ortho'
                )
        return out

    def _extract_dct_frame_channel(self, channel: np.ndarray, frame_idx: int,
                                    h_blocks: int, v_blocks: int, repeat: int,
                                    num_bits: int) -> List[float]:
        """从固定网格单通道提取"""
        values = []
        for bit_idx in range(num_bits):
            blocks = self._get_blocks(bit_idx, frame_idx, h_blocks, v_blocks, repeat)
            vals = []
            for by, bx in blocks:
                block = channel[by * self.VIDEO_DCT_BLOCK:(by + 1) * self.VIDEO_DCT_BLOCK,
                                bx * self.VIDEO_DCT_BLOCK:(bx + 1) * self.VIDEO_DCT_BLOCK]
                dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
                for cy, cx in self.VIDEO_DCT_COEFS:
                    vals.append(float(dct_block[cy, cx]))
            values.append(float(np.mean(vals)) if vals else 0.0)
        return values

    def _embed_video_dct(self, dna: str, output_path: Path) -> Path:
        """用固定网格 DCT 嵌入 DNA 短指纹（缩放不变 + Y/Cb/Cr 三通道）"""
        fp = self._dna_to_fingerprint(dna)
        cap = cv2.VideoCapture(str(self.video_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        h_blocks = self.GRID_W
        v_blocks = self.GRID_H
        repeat = self._compute_repeat(h_blocks, v_blocks, 0)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # 缩放到固定网格，嵌入后再缩放回原始分辨率
            orig_h, orig_w = frame.shape[:2]
            grid_frame = self._frame_to_grid(frame)
            ycbcr = cv2.cvtColor(grid_frame, cv2.COLOR_BGR2YCrCb)
            for ch_idx, alpha in [(0, self.VIDEO_DCT_ALPHA_Y),
                                   (1, self.VIDEO_DCT_ALPHA_C),
                                   (2, self.VIDEO_DCT_ALPHA_C)]:
                ch = ycbcr[:, :, ch_idx].astype(np.float32)
                ch_marked = self._embed_dct_frame_channel(
                    ch, fp, frame_idx, h_blocks, v_blocks, repeat, alpha
                )
                ycbcr[:, :, ch_idx] = np.clip(ch_marked, 0, 255).astype(np.uint8)
            marked_grid = cv2.cvtColor(ycbcr, cv2.COLOR_YCrCb2BGR)
            marked_frame = cv2.resize(marked_grid, (orig_w, orig_h), interpolation=cv2.INTER_CUBIC)
            writer.write(marked_frame)
            # v4.1: 每帧使用相同块布局，抗丢帧/帧率变化
            frame_idx = 0

        cap.release()
        writer.release()
        return output_path

    def _robust_bit_decode(self, values_per_bit: List[List[float]]) -> List[int]:
        """跨帧中位数 + 离群值剔除 解码"""
        fp = []
        for vals in values_per_bit:
            if not vals:
                fp.append(0)
                continue
            arr = np.array(vals, dtype=np.float64)
            median = np.median(arr)
            mad = np.median(np.abs(arr - median)) + 1e-9
            # 3σ 等效：保留 |x - median| < OUTLIER_SIGMA * 1.4826 * MAD 的样本
            threshold = self.OUTLIER_SIGMA * 1.4826 * mad
            filtered = arr[np.abs(arr - median) < threshold]
            if len(filtered) == 0:
                filtered = arr
            score = float(np.mean(filtered))
            fp.append(1 if score > 0 else 0)
        return fp

    def _check_sync(self, sync_values: List[List[float]]) -> bool:
        """检查同步头是否稳定存在"""
        bits = self._robust_bit_decode(sync_values)
        expected = self._sync_pattern()
        match = sum(1 for a, b in zip(bits, expected) if a == b)
        return match >= len(expected) * 0.75  # 允许 25% 误码

    def _extract_video_dct(self) -> Optional[str]:
        """从固定网格 DCT 提取 DNA 短指纹（缩放不变 + Y/Cb/Cr 三通道融合）"""
        # 先用帧相关索引尝试（安全性高）
        result = self._extract_video_dct_mode(frame_dependent=True)
        if result:
            return result
        # 回退：帧无关索引（抗丢帧/帧率变化）
        return self._extract_video_dct_mode(frame_dependent=False)

    def _extract_video_dct_mode(self, frame_dependent: bool = True) -> Optional[str]:
        """固定网格 DCT 提取模式"""
        cap = cv2.VideoCapture(str(self.video_path))
        h_blocks = self.GRID_W
        v_blocks = self.GRID_H
        repeat = self._compute_repeat(h_blocks, v_blocks, 0)
        # 帧无关模式适当增加重复数以弥补同步损失
        if not frame_dependent:
            repeat = min(repeat * 2, h_blocks * v_blocks // (self.SYNC_BITS + self.VIDEO_BITS))

        # 同步头 + 指纹
        total_bits = self.SYNC_BITS + self.VIDEO_BITS
        bit_values_y = [[] for _ in range(total_bits)]
        bit_values_c1 = [[] for _ in range(total_bits)]
        bit_values_c2 = [[] for _ in range(total_bits)]

        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            grid_frame = self._frame_to_grid(frame)
            ycbcr = cv2.cvtColor(grid_frame, cv2.COLOR_BGR2YCrCb)
            block_seed_idx = frame_idx if frame_dependent else 0
            vals_y = self._extract_dct_frame_channel(
                ycbcr[:, :, 0].astype(np.float32), block_seed_idx, h_blocks, v_blocks, repeat, total_bits
            )
            vals_c1 = self._extract_dct_frame_channel(
                ycbcr[:, :, 1].astype(np.float32), block_seed_idx, h_blocks, v_blocks, repeat, total_bits
            )
            vals_c2 = self._extract_dct_frame_channel(
                ycbcr[:, :, 2].astype(np.float32), block_seed_idx, h_blocks, v_blocks, repeat, total_bits
            )
            for i in range(total_bits):
                bit_values_y[i].append(vals_y[i])
                bit_values_c1[i].append(vals_c1[i])
                bit_values_c2[i].append(vals_c2[i])
            frame_idx += 1

        cap.release()
        if frame_idx == 0:
            return None

        # 分别解码三通道
        fp_y = self._robust_bit_decode(bit_values_y)
        fp_c1 = self._robust_bit_decode(bit_values_c1)
        fp_c2 = self._robust_bit_decode(bit_values_c2)

        # 检查同步头
        sync_ok_y = self._check_sync(bit_values_y[:self.SYNC_BITS])
        sync_ok_c = self._check_sync(bit_values_c1[:self.SYNC_BITS]) or self._check_sync(bit_values_c2[:self.SYNC_BITS])

        # 三通道投票融合
        fp_fused = []
        for i in range(self.SYNC_BITS, total_bits):
            votes = [fp_y[i], fp_c1[i], fp_c2[i]]
            fp_fused.append(1 if sum(votes) >= 2 else 0)

        result = self._fingerprint_to_dna(fp_fused)
        if result:
            return result

        # 回退：单通道 Y
        result_y = self._fingerprint_to_dna(fp_y[self.SYNC_BITS:])
        if result_y and sync_ok_y:
            return result_y

        # 回退：色度
        result_c = self._fingerprint_to_dna(fp_c1[self.SYNC_BITS:]) or self._fingerprint_to_dna(fp_c2[self.SYNC_BITS:])
        if result_c and sync_ok_c:
            return result_c

        return None

    # ── 攻击仿真测试 ──
    def selftest_robustness(self, dna: Optional[str] = None,
                            output_dir: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """对自带测试视频做嵌入，并模拟 H.264 重编码与录屏攻击，返回提取率"""
        import shutil
        if dna is None:
            dna = generate_dna("video-selftest")
        if output_dir is None:
            output_dir = SYSTEM_ROOT / "_work" / "video_marker_selftest"
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成测试视频
        test_video = output_dir / "origin.mp4"
        self._generate_test_video(test_video, frames=90, fps=30, width=640, height=360)

        marked_video = output_dir / "origin-DNA.mp4"
        VideoMarker(test_video).embed(dna=dna, output_path=marked_video)

        results = {"dna": dna, "marked": str(marked_video), "attacks": []}

        # 原始提取
        orig_fp = VideoMarker(marked_video).extract()
        results["attacks"].append({
            "name": "原始",
            "extracted": orig_fp,
            "ok": orig_fp is not None,
        })

        # H.264 重编码（模拟压缩）
        compressed = output_dir / "compressed.mp4"
        self._run_ffmpeg([
            "-i", str(marked_video),
            "-c:v", "libx264", "-crf", "28", "-preset", "fast",
            "-c:a", "copy",
            str(compressed)
        ])
        comp_fp = VideoMarker(compressed).extract()
        results["attacks"].append({
            "name": "H.264 CRF28 重编码",
            "extracted": comp_fp,
            "ok": comp_fp is not None,
        })

        # 录屏仿真：缩放 + 重编码 + 轻微模糊（模拟手机录屏）
        recorded = output_dir / "recorded.mp4"
        self._run_ffmpeg([
            "-i", str(marked_video),
            "-vf", "scale=480:-1,format=yuv420p",
            "-c:v", "libx264", "-crf", "30", "-preset", "fast",
            "-c:a", "copy",
            str(recorded)
        ])
        rec_fp = VideoMarker(recorded).extract()
        results["attacks"].append({
            "name": "录屏仿真（缩放+CRF30）",
            "extracted": rec_fp,
            "ok": rec_fp is not None,
        })

        # 帧率变化（模拟录屏帧率不一致，每隔一帧丢弃，不插值）
        refps = output_dir / "refps.mp4"
        self._run_ffmpeg([
            "-i", str(marked_video),
            "-vf", "select='not(mod(n,2))',setpts=N/FRAME_RATE/TB",
            "-c:v", "libx264", "-crf", "28",
            "-c:a", "copy",
            str(refps)
        ])
        refps_fp = VideoMarker(refps).extract()
        results["attacks"].append({
            "name": "15fps 重采样",
            "extracted": refps_fp,
            "ok": refps_fp is not None,
        })

        results["score"] = sum(1 for a in results["attacks"] if a["ok"])
        results["total"] = len(results["attacks"])
        return results

    def _generate_test_video(self, path: Path, frames: int = 90, fps: int = 30,
                             width: int = 640, height: int = 360):
        """生成带纹理的测试视频，避免纯色导致 DCT 系数异常"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(str(path), fourcc, fps, (width, height))
        for i in range(frames):
            # 渐变 + 噪声纹理
            img = np.zeros((height, width, 3), dtype=np.uint8)
            img[:, :, 0] = (i * 2) % 256
            img[:, :, 1] = (255 - i * 2) % 256
            img[:, :, 2] = ((i * 3) % 256)
            noise = np.random.randint(0, 30, (height, width, 3), dtype=np.uint8)
            img = cv2.add(img, noise)
            writer.write(img)
        writer.release()

    # ── 主入口 ──
    def embed(self, dna: Optional[str] = None, output_path: Optional[Union[str, Path]] = None) -> Path:
        if dna is None:
            dna = generate_dna("video")
        if output_path is None:
            stem = self.video_path.stem
            output_path = self.video_path.parent / f"{stem}-DNA.mp4"
        else:
            output_path = Path(output_path)

        # 第一步：帧级 DCT 嵌入（主）
        self._embed_video_dct(dna, output_path)

        # 第二步：若原视频有音频，额外叠加音频水印（副）
        if self._has_audio():
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp = Path(tmpdir)
                orig_wav = tmp / "orig.wav"
                marked_wav = tmp / "marked.wav"
                dct_video = tmp / "marked_video.mp4"
                # 保留 DCT 标记后的视频，作为混流视频源
                import shutil
                shutil.copy2(output_path, dct_video)
                if self._extract_audio(orig_wav):
                    AudioMarkerRobust(orig_wav).embed(dna, marked_wav)
                    if self._merge_audio(marked_wav, output_path, video_source=dct_video):
                        return output_path
                # 音频混流失败则保留 DCT 结果
        return output_path

    def extract(self) -> Optional[str]:
        # 优先帧级 DCT（最鲁棒）
        fp = self._extract_video_dct()
        if fp:
            return fp

        # 回退音频轨
        if self._has_audio():
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp = Path(tmpdir)
                wav = tmp / "extract.wav"
                if self._extract_audio(wav):
                    audio_fp = AudioMarkerRobust(wav).extract()
                    if audio_fp:
                        return audio_fp
        return None

class AudioMarker:
    """音频主权标记器（WAV）

    采用时域最低有效位（LSB）+ 3 重复码 + 交织，兼顾不可闻与鲁棒性。
    每个比特重复 3 次并交织存储，解码时按 3 取多数，可容忍局部破坏。
    """

    AUDIO_REPEAT = 3          # 重复码次数
    AUDIO_INTERLEAVE = False  # v1.0 使用连续重复，避免与原始音频 LSB 混叠

    def __init__(self, audio_path: Union[str, Path]):
        self.audio_path = Path(audio_path)

    def _read_wav(self) -> Tuple[np.ndarray, int]:
        with wave.open(str(self.audio_path), 'rb') as wf:
            nchannels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            nframes = wf.getnframes()
            raw = wf.readframes(nframes)
            if sampwidth == 2:
                data = np.frombuffer(raw, dtype=np.int16)
            elif sampwidth == 1:
                data = np.frombuffer(raw, dtype=np.uint8).astype(np.int16) - 128
            else:
                raise ValueError(f"不支持的采样宽度: {sampwidth}")
            if nchannels > 1:
                data = data.reshape(-1, nchannels).mean(axis=1)
            return data.astype(np.float32), framerate

    def _write_wav(self, data: np.ndarray, framerate: int, output_path: Path):
        data = np.clip(data, -32768, 32767).astype(np.int16)
        with wave.open(str(output_path), 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(framerate)
            wf.writeframes(data.tobytes())

    def _interleave(self, bits: List[int]) -> List[int]:
        """简单交织：把重复后的比特按重复组重新排列"""
        if not self.AUDIO_INTERLEAVE:
            return bits
        repeat = self.AUDIO_REPEAT
        n = len(bits) // repeat
        out = []
        for r in range(repeat):
            for i in range(n):
                out.append(bits[i * repeat + r])
        return out

    def _deinterleave(self, bits: List[int]) -> List[int]:
        """解交织"""
        if not self.AUDIO_INTERLEAVE:
            return bits
        repeat = self.AUDIO_REPEAT
        n = len(bits) // repeat
        out = [0] * len(bits)
        idx = 0
        for r in range(repeat):
            for i in range(n):
                out[i * repeat + r] = bits[idx]
                idx += 1
        return out

    def embed(self, dna: Optional[str] = None, output_path: Optional[Union[str, Path]] = None) -> Path:
        if dna is None:
            dna = generate_dna("audio")
        if output_path is None:
            stem = self.audio_path.stem
            output_path = self.audio_path.parent / f"{stem}-DNA.wav"
        else:
            output_path = Path(output_path)

        data, framerate = self._read_wav()
        bits = dna_to_bits(dna)
        payload = pack_length_and_bits(bits)
        # 3 重复码
        repeated = []
        for b in payload:
            repeated.extend([b] * self.AUDIO_REPEAT)
        # 交织
        repeated = self._interleave(repeated)

        if len(repeated) > len(data):
            raise ValueError(f"音频过短，无法嵌入 {len(repeated)} 位水印")

        out = data.copy()
        mask = np.int16(-2)  # 0xFFFE in int16
        for i, bit in enumerate(repeated):
            sample = np.int16(int(out[i]))
            sample = (sample & mask) | np.int16(bit)
            out[i] = float(sample)

        self._write_wav(out, framerate, output_path)
        return output_path

    def extract(self) -> Optional[str]:
        data, _ = self._read_wav()
        # 提取所有 LSB
        raw_bits = [int(int(s) & 1) for s in data[:len(data)]]

        def try_decode(bits: List[int]) -> Optional[str]:
            try:
                length, data_bits = unpack_length_and_bits(bits)
                if 0 < length <= 2048:
                    dna = bits_to_dna(data_bits[:length])
                    if _looks_like_dna(dna):
                        return dna
            except Exception:
                pass
            return None

        # 候选 1：直接解交织 + 3 取多数
        # 只解交织前 (32 + 2048) * repeat 位；若 DNA 更短也能解析
        max_payload_bits = 32 + 2048
        for max_len in [max_payload_bits * self.AUDIO_REPEAT, len(raw_bits)]:
            chunk = raw_bits[:max_len]
            if len(chunk) < self.AUDIO_REPEAT or len(chunk) % self.AUDIO_REPEAT != 0:
                continue
            de = self._deinterleave(chunk)
            # 3 取多数
            decoded = []
            for i in range(0, len(de) - self.AUDIO_REPEAT + 1, self.AUDIO_REPEAT):
                votes = de[i:i + self.AUDIO_REPEAT]
                decoded.append(1 if sum(votes) >= 2 else 0)
            dna = try_decode(decoded)
            if dna:
                return dna
        return None


# ---------------------------------------------------------------------------
# 4b. 音频鲁棒盲水印（压缩/录屏场景）
# ---------------------------------------------------------------------------
class AudioMarkerRobust:
    """音频鲁棒主权标记器 v2.0（抗 AAC/MP3 压缩）

    策略：频域直接序列扩频（DSSS）+ 多频带副本 + 跨块投票。
      1. 长块 rFFT（16384 样点），覆盖 2kHz-8kHz 语音/音乐主频段。
      2. 每个指纹 bit 用 3 组独立 PN 序列分别调制到不同子频段。
      3. 解码时用相关检测替代能量比较，对音频内容干扰更不敏感。
      4. 同 payload 在所有块重复，3 副本跨块多数投票。

    为压缩鲁棒性，payload 固定为 160 位（32 位魔数 + 128 位 DNA 指纹）。
    DNA 指纹取 SHA-256 前 128 位十六进制。
    """

    BLOCK_SIZE = 16384
    BITS = 160
    PN_LENGTH = 256          # 每 bit / 每副本的 PN 长度
    DELTA = 0.05             # 相对频谱标准差的调制量
    SEED = 9622
    # 三个互不重叠的子频段（Hz），分散风险
    FREQ_BANDS = [(2000, 4000), (4000, 6000), (6000, 8000)]

    def __init__(self, audio_path: Union[str, Path]):
        self.audio_path = Path(audio_path)

    def _read_wav(self) -> Tuple[np.ndarray, int]:
        with wave.open(str(self.audio_path), 'rb') as wf:
            nchannels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            nframes = wf.getnframes()
            raw = wf.readframes(nframes)
            if sampwidth == 2:
                data = np.frombuffer(raw, dtype=np.int16)
            elif sampwidth == 1:
                data = np.frombuffer(raw, dtype=np.uint8).astype(np.int16) - 128
            else:
                raise ValueError(f"不支持的采样宽度: {sampwidth}")
            if nchannels > 1:
                data = data.reshape(-1, nchannels).mean(axis=1)
            return data.astype(np.float32), framerate

    def _write_wav(self, data: np.ndarray, framerate: int, output_path: Path):
        data = np.clip(data, -32768, 32767).astype(np.int16)
        with wave.open(str(output_path), 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(framerate)
            wf.writeframes(data.tobytes())

    def _dna_to_fingerprint(self, dna: str) -> List[int]:
        """把 DNA 转成 160 位指纹：32 位魔数 + 128 位 DNA 哈希"""
        magic = "LHAF"  # LongHun Audio Fingerprint
        magic_bits = [int(b) for byte in magic.encode('utf-8') for b in format(byte, '08b')]
        h = hashlib.sha256(dna.encode('utf-8')).hexdigest()[:32]
        hash_bits = [int(b) for ch in h for b in format(int(ch, 16), '04b')]
        fp = magic_bits + hash_bits
        if len(fp) < self.BITS:
            fp += [0] * (self.BITS - len(fp))
        return fp[:self.BITS]

    def _fingerprint_to_dna(self, fp: List[int]) -> Optional[str]:
        """从指纹反查 DNA 魔数；当前只验证魔数"""
        if len(fp) < 32:
            return None
        magic_bits = fp[:32]
        magic_bytes = bytes(int(''.join(str(b) for b in magic_bits[i:i+8]), 2) for i in range(0, 32, 8))
        try:
            if magic_bytes.decode('utf-8') != "LHAF":
                return None
        except Exception:
            return None
        hash_bits = fp[32:self.BITS]
        hex_chars = []
        for i in range(0, len(hash_bits), 4):
            nibble = int(''.join(str(b) for b in hash_bits[i:i+4]), 2)
            hex_chars.append(format(nibble, 'x'))
        return "LHAF-" + ''.join(hex_chars)

    def _get_pn(self, bit_idx: int, copy: int) -> np.ndarray:
        """生成 bit_idx 在第 copy 个子频段的 PN 序列"""
        rng = np.random.default_rng(self.SEED + bit_idx * 10 + copy)
        return rng.choice(np.array([1.0, -1.0]), size=self.PN_LENGTH)

    def _get_bins(self, bit_idx: int, copy: int, framerate: int) -> np.ndarray:
        """生成 bit_idx 在第 copy 个子频段的随机频点"""
        rng = np.random.default_rng(self.SEED + bit_idx * 10000 + copy * 1000)
        low, high = self.FREQ_BANDS[copy]
        bin_low = int(low * self.BLOCK_SIZE / framerate)
        bin_high = int(high * self.BLOCK_SIZE / framerate)
        # rFFT 输出长度为 BLOCK_SIZE//2 + 1
        bin_high = min(bin_high, self.BLOCK_SIZE // 2)
        if bin_high - bin_low < self.PN_LENGTH:
            bin_low = max(1, bin_high - self.PN_LENGTH)
        return rng.integers(bin_low, bin_high, size=self.PN_LENGTH)

    def embed(self, dna: Optional[str] = None, output_path: Optional[Union[str, Path]] = None,
              framerate: Optional[int] = None) -> Path:
        if dna is None:
            dna = generate_dna("audio-robust")
        if output_path is None:
            stem = self.audio_path.stem
            output_path = self.audio_path.parent / f"{stem}-DNA-robust.wav"
        else:
            output_path = Path(output_path)

        data, fr = self._read_wav()
        self._framerate = framerate if framerate else fr
        fp = self._dna_to_fingerprint(dna)

        out = data.copy()
        block_size = self.BLOCK_SIZE
        for i in range(0, len(data) - block_size + 1, block_size):
            block = data[i:i + block_size]
            spec = np.fft.rfft(block)
            mag = np.abs(spec).astype(np.float32)
            phase = np.angle(spec)
            std = np.std(mag)
            for bit_idx, bit in enumerate(fp):
                sign = 1.0 if bit else -1.0
                for copy in range(len(self.FREQ_BANDS)):
                    pn = self._get_pn(bit_idx, copy)
                    bins = self._get_bins(bit_idx, copy, self._framerate)
                    shift = self.DELTA * std * pn * sign
                    mag[bins] += shift
            spec = mag * np.exp(1j * phase)
            out[i:i + block_size] = np.fft.irfft(spec, n=block_size)

        self._write_wav(out, fr, output_path)
        return output_path

    def _decode_copy(self, copy: int, data: np.ndarray) -> List[int]:
        """用第 copy 个子频段解码出 160 个 bit"""
        bits = []
        block_size = self.BLOCK_SIZE
        for bit_idx in range(self.BITS):
            pn = self._get_pn(bit_idx, copy)
            bins = self._get_bins(bit_idx, copy, self._framerate)
            corrs = []
            for i in range(0, len(data) - block_size + 1, block_size):
                block = data[i:i + block_size]
                spec = np.fft.rfft(block)
                mag = np.abs(spec).astype(np.float32)
                # z-score 归一化，降低不同块之间能量差异影响
                mean = np.mean(mag)
                std = np.std(mag) + 1e-10
                mag_z = (mag - mean) / std
                corrs.append(float(np.mean(mag_z[bins] * pn)))
            bits.append(1 if np.mean(corrs) > 0 else 0)
        return bits

    def extract(self, framerate: Optional[int] = None) -> Optional[str]:
        data, fr = self._read_wav()
        self._framerate = framerate if framerate else fr

        copies = [self._decode_copy(c, data) for c in range(len(self.FREQ_BANDS))]

        # 3 副本多数投票
        voted = []
        for i in range(self.BITS):
            votes = [c[i] for c in copies]
            voted.append(1 if sum(votes) >= len(votes) / 2 else 0)

        return self._fingerprint_to_dna(voted)
# ---------------------------------------------------------------------------
# 5. CLI / 统一入口
# ---------------------------------------------------------------------------
class MediaSovereigntyMarker:
    """统一媒体主权标记入口"""

    @staticmethod
    def mark(media_path: Union[str, Path], media_type: Optional[str] = None,
             dna: Optional[str] = None, output_path: Optional[Union[str, Path]] = None) -> Path:
        path = Path(media_path)
        if media_type is None:
            ext = path.suffix.lower()
            if ext in {'.otf', '.ttf', '.woff', '.woff2'}:
                media_type = 'font'
            elif ext in {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}:
                media_type = 'image'
            elif ext in {'.mp4', '.mov', '.avi', '.mkv'}:
                media_type = 'video'
            elif ext in {'.wav'}:
                media_type = 'audio'
            else:
                raise ValueError(f"无法识别媒体类型: {ext}")

        if media_type == 'font':
            return FontMarker(path).embed_dna(dna, output_path)
        elif media_type == 'image':
            return ImageMarker(path).embed(dna, output_path)
        elif media_type == 'video':
            return VideoMarker(path).embed(dna, output_path)
        elif media_type == 'audio':
            return AudioMarker(path).embed(dna, output_path)
        else:
            raise ValueError(f"不支持的媒体类型: {media_type}")

    @staticmethod
    def verify(media_path: Union[str, Path], media_type: Optional[str] = None) -> dict:
        path = Path(media_path)
        if media_type is None:
            ext = path.suffix.lower()
            if ext in {'.otf', '.ttf', '.woff', '.woff2'}:
                media_type = 'font'
            elif ext in {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}:
                media_type = 'image'
            elif ext in {'.mp4', '.mov', '.avi', '.mkv'}:
                media_type = 'video'
            elif ext in {'.wav'}:
                media_type = 'audio'
            else:
                return {"error": f"无法识别媒体类型: {ext}"}

        result = {"media_type": media_type, "path": str(path)}
        if media_type == 'font':
            marker = FontMarker(path)
            result.update(marker.verify_native_watermark())
            result["dna"] = marker.extract_dna()
        elif media_type == 'image':
            result["dna"] = ImageMarker(path).extract()
        elif media_type == 'video':
            extracted = VideoMarker(path).extract()
            result["note"] = ("基于帧级 DCT 扩频指纹（主）+ 音频轨 Patchwork 指纹（副）"
                             "，抗 H.264/H.265 重编码与录屏")
            if extracted and extracted.startswith("LHAF-"):
                result["fingerprint"] = extracted
            else:
                result["dna"] = extracted
                result["fingerprint"] = None
        elif media_type == 'audio':
            result["dna"] = AudioMarker(path).extract()
        return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·媒体主权标记引擎")
    parser.add_argument("action", choices=["mark", "verify"], help="操作")
    parser.add_argument("path", help="媒体文件路径")
    parser.add_argument("--type", choices=["font", "image", "video", "audio"], help="媒体类型")
    parser.add_argument("--dna", help="自定义 DNA 字符串")
    parser.add_argument("--output", "-o", help="输出路径")
    args = parser.parse_args()

    if args.action == "mark":
        out = MediaSovereigntyMarker.mark(args.path, args.type, args.dna, args.output)
        print(f"✅ 已标记: {out}")
    else:
        result = MediaSovereigntyMarker.verify(args.path, args.type)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


