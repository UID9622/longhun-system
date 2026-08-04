#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 声纹注册库 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-VOICE-REGISTER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  1. 注册声纹 (提取特征存储到本地库)
  2. 声纹库管理 (列表/删除/搜索)
  3. 声纹验证 (输入音频→匹配已注册身份)
  4. 声纹比对 (两段音频相似度)

用法：
  lh voice-register register --audio voice.wav --name "张三"
  lh voice-register verify --audio voice.wav --name "张三"
  lh voice-register match --audio test.wav
  lh voice-register list
  lh voice-register remove --name "张三"

依赖（可选·回退到基础特征模式）:
  pip install wespeaker torch soundfile  (推荐·高精度)
  或 pip install numpy soundfile  (基础模式·低精度)
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ---- 可选导入 ----
try:
    import numpy as np
    HAS_NP = True
except ImportError:
    HAS_NP = False

try:
    import soundfile as sf
    HAS_SF = True
except ImportError:
    HAS_SF = False

# WeSpeaker (推荐·高精度)
WESPEAKER_AVAILABLE = False
try:
    import wespeaker
    WESPEAKER_AVAILABLE = True
except ImportError:
    pass


class VoiceRegister:
    """声纹注册库"""
    
    def __init__(self):
        self.model = None
        self.registry = {}
        self.registry_file = Path.home() / "longhun-system" / "data" / "voice_registry.json"
        self._load_registry()
        self._init_model()

    def _init_model(self):
        """初始化声纹模型"""
        if WESPEAKER_AVAILABLE and HAS_NP:
            try:
                from wespeaker import load_model
                self.model = load_model("wespeaker/voxceleb_resnet34_LM")
                print("✅ WeSpeaker 声纹模型就绪", flush=True)
            except Exception as e:
                print(f"⚠️ WeSpeaker 加载失败: {e}", flush=True)
                self.model = None
        else:
            self.model = None
            if HAS_NP and HAS_SF:
                print("⚠️ 基础声纹模式（MFCC统计特征·低精度）", flush=True)

    def _load_registry(self):
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r') as f:
                    self.registry = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.registry = {}

    def _save_registry(self):
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, ensure_ascii=False, indent=2)

    def _load_audio(self, audio_path: Path):
        """加载音频数据·返回 (samples, sr)"""
        if not HAS_SF:
            return None, None
        try:
            audio, sr = sf.read(str(audio_path))
            # 转单声道
            if audio.ndim > 1:
                audio = audio.mean(axis=1)
            return audio, sr
        except Exception as e:
            return None, None

    def _extract_wespeaker_embedding(self, audio_path: Path) -> Optional["np.ndarray"]:
        """WeSpeaker 高精度声纹特征提取"""
        if self.model is None:
            return None
        audio, sr = self._load_audio(audio_path)
        if audio is None:
            return None
        # WeSpeaker 要求16kHz
        if sr != 16000:
            try:
                import librosa
                audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
            except ImportError:
                # 简易重采样
                ratio = 16000 / sr
                indices = np.arange(0, len(audio), 1/ratio).astype(int)
                indices = indices[indices < len(audio)]
                audio = audio[indices]
        try:
            embedding = self.model.compute_embedding(audio)
            return embedding
        except Exception as e:
            print(f"⚠️ WeSpeaker提取失败: {e}", flush=True)
            return None

    def _extract_basic_features(self, audio_path: Path) -> Optional["np.ndarray"]:
        """基础声纹特征（MFCC统计特征·回退方案）"""
        if not HAS_NP:
            return None
        audio, sr = self._load_audio(audio_path)
        if audio is None or len(audio) < 1000:
            return None
        
        # 使用文件级哈希+统计特征作为简化声纹
        file_hash = hashlib.sha256(open(str(audio_path), 'rb').read()).hexdigest()[:32]
        
        # 音频统计特征
        stats = [
            float(np.mean(np.abs(audio))),
            float(np.std(audio)),
            float(np.max(np.abs(audio))),
            float(np.sum(audio**2)),
            float(sr) if sr else 0,
            len(audio) / max(sr, 1),
        ]
        
        # 分帧能量
        frame_len = min(2048, len(audio) // 16)
        if frame_len > 0:
            n_frames = len(audio) // frame_len
            energies = [float(np.sum(audio[i*frame_len:(i+1)*frame_len]**2)) for i in range(min(n_frames, 16))]
            stats.extend(energies)
        
        # 归一化
        stats_arr = np.array(stats, dtype=np.float64)
        norm = np.linalg.norm(stats_arr)
        if norm > 0:
            stats_arr = stats_arr / norm
        
        return stats_arr

    # ---- 注册 ----
    def register_voice(self, audio_path: Path, name: str) -> Dict:
        """注册声纹"""
        if not audio_path.exists():
            return {"status": "error", "message": f"音频不存在: {audio_path}"}

        # 生成声纹指纹
        voice_hash = hashlib.sha256(open(str(audio_path), 'rb').read()).hexdigest()[:16]

        entry = {
            "name": name,
            "voice_hash": voice_hash,
            "source": str(audio_path),
            "registered_at": datetime.now().isoformat(),
        }

        # 尝试高精度 WeSpeaker
        if self.model:
            embedding = self._extract_wespeaker_embedding(audio_path)
            if embedding is not None:
                entry["embedding"] = embedding.tolist()
                entry["method"] = "wespeaker"
            else:
                entry["message"] = "高精度提取失败·回退基础模式"

        # 回退基础特征
        if "embedding" not in entry:
            basic = self._extract_basic_features(audio_path)
            if basic is not None:
                entry["embedding"] = basic.tolist()
                entry["method"] = "basic_stats"
            else:
                return {"status": "error", "message": "无法提取声纹特征·请安装 wespeaker + torch"}

        self.registry[name] = entry
        self._save_registry()

        dna = f"#龍芯⚡️VOICE-{voice_hash}"
        return {
            "status": "success",
            "name": name,
            "dna": dna,
            "voice_hash": voice_hash,
            "method": entry["method"],
            "message": "声纹注册成功"
        }

    # ---- 验证 ----
    def verify_voice(self, audio_path: Path, name: str, threshold: float = 0.6) -> Dict:
        """验证声纹是否匹配已注册身份"""
        if name not in self.registry:
            return {"status": "error", "message": f"身份 '{name}' 未注册"}

        reg_data = self.registry[name]
        if "embedding" not in reg_data:
            return {"status": "error", "message": f"'{name}' 缺少声纹特征·请重新注册"}

        # 提取输入音频特征
        if self.model:
            embedding = self._extract_wespeaker_embedding(audio_path)
        else:
            embedding = self._extract_basic_features(audio_path)

        if embedding is None:
            return {"status": "error", "message": "音频声纹提取失败"}

        reg_emb = np.array(reg_data["embedding"])
        
        # 处理维度不匹配
        if embedding.shape != reg_emb.shape:
            return {"status": "error", 
                    "message": f"特征维度不匹配: 输入{embedding.shape} vs 注册{reg_emb.shape}·请使用相同方法重新注册"}

        # 余弦相似度
        similarity = float(np.dot(embedding, reg_emb) / 
                         (np.linalg.norm(embedding) * np.linalg.norm(reg_emb) + 1e-10))

        return {
            "status": "success",
            "name": name,
            "similarity": round(similarity, 4),
            "match": similarity > threshold,
            "threshold": threshold,
            "method": reg_data.get("method", "unknown")
        }

    # ---- 匹配 ----
    def match_voice(self, audio_path: Path, threshold: float = 0.6) -> Dict:
        """在注册库中匹配最佳身份"""
        if not self.registry:
            return {"status": "error", "message": "声纹库为空·请先注册"}

        if self.model:
            embedding = self._extract_wespeaker_embedding(audio_path)
        else:
            embedding = self._extract_basic_features(audio_path)

        if embedding is None:
            return {"status": "error", "message": "音频声纹提取失败"}

        candidates = []
        for name, data in self.registry.items():
            if "embedding" not in data:
                continue
            reg_emb = np.array(data["embedding"])
            if embedding.shape != reg_emb.shape:
                continue
            similarity = float(np.dot(embedding, reg_emb) / 
                             (np.linalg.norm(embedding) * np.linalg.norm(reg_emb) + 1e-10))
            candidates.append({"name": name, "similarity": round(similarity, 4)})

        if not candidates:
            return {"status": "error", "message": "无可用声纹库（维度不匹配或空库）"}

        candidates.sort(key=lambda x: x["similarity"], reverse=True)
        best = candidates[0]

        if best["similarity"] > threshold:
            return {
                "status": "matched",
                "name": best["name"],
                "similarity": best["similarity"],
                "threshold": threshold,
                "all_candidates": candidates[:5]
            }
        else:
            return {
                "status": "no_match",
                "best_score": best["similarity"],
                "best_guess": best["name"],
                "threshold": threshold,
                "nearest_candidates": candidates[:3]
            }

    def list_registered(self) -> List[Dict]:
        return [{"name": k, "method": v.get("method", ""), "registered_at": v.get("registered_at", ""), 
                 "voice_hash": v.get("voice_hash", ""), "source": v.get("source", "")}
                for k, v in self.registry.items()]

    def remove_identity(self, name: str) -> Dict:
        if name in self.registry:
            del self.registry[name]
            self._save_registry()
            return {"status": "success", "message": f"已移除 '{name}'"}
        return {"status": "error", "message": f"'{name}' 未注册"}

    def status(self) -> Dict:
        return {
            "engine": "声纹注册库 v1.0",
            "wespeaker": WESPEAKER_AVAILABLE,
            "numpy": HAS_NP,
            "soundfile": HAS_SF,
            "model": "WeSpeaker voxceleb_resnet34_LM" if self.model else "回退: 统计特征",
            "registered": len(self.registry),
            "dna": "#龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-VOICE-REGISTER-v1.0-UID9622"
        }


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 声纹注册库")
    subparsers = parser.add_subparsers(dest="command")

    p_register = subparsers.add_parser("register", help="注册声纹")
    p_register.add_argument("--audio", required=True, help="音频路径")
    p_register.add_argument("--name", required=True, help="身份名称")

    p_verify = subparsers.add_parser("verify", help="验证声纹")
    p_verify.add_argument("--audio", required=True)
    p_verify.add_argument("--name", required=True)
    p_verify.add_argument("--threshold", type=float, default=0.6)

    p_match = subparsers.add_parser("match", help="匹配身份")
    p_match.add_argument("--audio", required=True)
    p_match.add_argument("--threshold", type=float, default=0.6)

    p_list = subparsers.add_parser("list", help="列出已注册")
    p_remove = subparsers.add_parser("remove", help="移除身份")
    p_remove.add_argument("--name", required=True)

    p_status = subparsers.add_parser("status", help="引擎状态")

    args = parser.parse_args()

    if args.command == "status":
        register = VoiceRegister()
        print(json.dumps(register.status(), ensure_ascii=False, indent=2))
        return

    register = VoiceRegister()

    if args.command == "register":
        result = register.register_voice(Path(args.audio), args.name)
    elif args.command == "verify":
        result = register.verify_voice(Path(args.audio), args.name, args.threshold)
    elif args.command == "match":
        result = register.match_voice(Path(args.audio), args.threshold)
    elif args.command == "list":
        items = register.list_registered()
        if items:
            print(json.dumps(items, ensure_ascii=False, indent=2))
        else:
            print("（空·无声纹注册）")
        return
    elif args.command == "remove":
        result = register.remove_identity(args.name)
    else:
        parser.print_help()
        return

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
