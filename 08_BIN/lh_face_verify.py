#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 人脸验证引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-FACE-VERIFY-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  1. 人脸检测 (OpenCV Haar Cascade / InsightFace)
  2. 人脸特征提取与注册
  3. 人脸比对验证
  4. 身份库管理

用法：
  lh face-verify register --face face.jpg --name "张三"
  lh face-verify verify --face test.jpg --name "张三"
  lh face-verify compare --face1 a.jpg --face2 b.jpg
  lh face-verify list
  lh face-verify remove --name "张三"

依赖（可选·回退到OpenCV基础模式）:
  pip install opencv-python numpy insightface
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
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    import insightface
    from insightface.app import FaceAnalysis
    HAS_INSIGHT = True
except ImportError:
    HAS_INSIGHT = False


class FaceVerifier:
    """人脸验证引擎"""
    
    def __init__(self):
        self.face_app = None
        self.registry = {}
        self.registry_file = Path.home() / "longhun-system" / "data" / "face_registry.json"
        self._load_registry()
        self._init_engine()

    def _init_engine(self):
        """初始化人脸引擎"""
        if HAS_INSIGHT:
            try:
                self.face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
                self.face_app.prepare(ctx_id=0, det_size=(640, 640))
                print("✅ InsightFace 初始化成功", flush=True)
            except Exception as e:
                print(f"⚠️ InsightFace 初始化失败: {e}", flush=True)
                self.face_app = None
        else:
            self.face_app = None
            if HAS_CV2:
                print("⚠️ 使用 OpenCV Haar Cascade 回退模式（精度较低）", flush=True)

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

    # ---- InsightFace 模式 ----
    def _get_embedding_insight(self, image: "np.ndarray") -> Optional["np.ndarray"]:
        """InsightFace 特征提取"""
        if self.face_app is None:
            return None
        faces = self.face_app.get(image)
        if len(faces) == 0:
            return None
        return faces[0].normed_embedding

    # ---- OpenCV 回退 ----
    def _detect_face_opencv(self, image: "np.ndarray") -> Optional["np.ndarray"]:
        """OpenCV 人脸检测·返回裁剪后的脸"""
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) == 0:
            return None
        x, y, w, h = faces[0]
        return image[y:y+h, x:x+w]

    # ---- 注册 ----
    def register_face(self, image_path: Path, name: str) -> Dict:
        """注册人脸"""
        if not HAS_CV2:
            return {"status": "error", "message": "需要 opencv-python: pip install opencv-python numpy"}

        image = cv2.imread(str(image_path))
        if image is None:
            return {"status": "error", "message": "无法读取图片"}

        # 生成面孔哈希
        face_hash = hashlib.sha256(open(str(image_path), 'rb').read()).hexdigest()[:16]

        entry = {
            "name": name,
            "face_hash": face_hash,
            "source": str(image_path),
            "registered_at": datetime.now().isoformat(),
        }

        if self.face_app:
            embedding = self._get_embedding_insight(image)
            if embedding is None:
                return {"status": "error", "message": "未检测到人脸"}
            entry["embedding"] = embedding.tolist()
            entry["method"] = "insightface"
        else:
            face_img = self._detect_face_opencv(image)
            if face_img is None:
                return {"status": "error", "message": "未检测到人脸（OpenCV回退）"}
            hist = cv2.calcHist([face_img], [0], None, [256], [0, 256])
            entry["histogram"] = hist.flatten().tolist()
            entry["method"] = "opencv_histogram"

        self.registry[name] = entry
        self._save_registry()
        
        dna = f"#龍芯⚡️FACE-{face_hash}"
        return {
            "status": "success",
            "name": name,
            "dna": dna,
            "face_hash": face_hash,
            "method": entry["method"],
            "message": "人脸注册成功"
        }

    # ---- 验证 ----
    def verify_face(self, image_path: Path, name: str) -> Dict:
        """验证人脸是否匹配"""
        if name not in self.registry:
            return {"status": "error", "message": f"身份 '{name}' 未注册"}

        if not HAS_CV2:
            return {"status": "error", "message": "需要 opencv-python"}

        image = cv2.imread(str(image_path))
        if image is None:
            return {"status": "error", "message": "无法读取图片"}

        reg_data = self.registry[name]

        if self.face_app and "embedding" in reg_data:
            embedding = self._get_embedding_insight(image)
            if embedding is None:
                return {"status": "error", "message": "未检测到人脸"}
            reg_emb = np.array(reg_data["embedding"])
            similarity = float(np.dot(embedding, reg_emb) / 
                             (np.linalg.norm(embedding) * np.linalg.norm(reg_emb)))
            threshold = 0.6
            return {
                "status": "success",
                "name": name,
                "similarity": round(similarity, 4),
                "match": similarity > threshold,
                "threshold": threshold,
                "method": "insightface"
            }
        else:
            face_img = self._detect_face_opencv(image)
            if face_img is None:
                return {"status": "error", "message": "未检测到人脸"}
            hist = cv2.calcHist([face_img], [0], None, [256], [0, 256])
            reg_hist = np.array(reg_data["histogram"])
            similarity = float(cv2.compareHist(hist, reg_hist, cv2.HISTCMP_CORREL))
            threshold = 0.5
            return {
                "status": "success",
                "name": name,
                "similarity": round(similarity, 4),
                "match": similarity > threshold,
                "threshold": threshold,
                "method": "opencv_histogram"
            }

    # ---- 比对 ----
    def compare_faces(self, img1_path: Path, img2_path: Path) -> Dict:
        """比较两张人脸"""
        if not HAS_CV2:
            return {"status": "error", "message": "需要 opencv-python"}

        img1 = cv2.imread(str(img1_path))
        img2 = cv2.imread(str(img2_path))
        if img1 is None or img2 is None:
            return {"status": "error", "message": "无法读取图片"}

        if self.face_app:
            emb1 = self._get_embedding_insight(img1)
            emb2 = self._get_embedding_insight(img2)
            if emb1 is None or emb2 is None:
                return {"status": "error", "message": "未检测到人脸"}
            similarity = float(np.dot(emb1, emb2) / 
                             (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
        else:
            face1 = self._detect_face_opencv(img1)
            face2 = self._detect_face_opencv(img2)
            if face1 is None or face2 is None:
                return {"status": "error", "message": "未检测到人脸"}
            hist1 = cv2.calcHist([face1], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([face2], [0], None, [256], [0, 256])
            similarity = float(cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL))

        threshold = 0.6 if self.face_app else 0.5
        return {
            "status": "success",
            "similarity": round(similarity, 4),
            "match": similarity > threshold,
            "threshold": threshold,
            "method": "insightface" if self.face_app else "opencv_histogram"
        }

    def list_registered(self) -> List[Dict]:
        return [{"name": k, **{sk: sv for sk, sv in v.items() if sk not in ("embedding", "histogram")}} 
                for k, v in self.registry.items()]

    def remove_identity(self, name: str) -> Dict:
        if name in self.registry:
            del self.registry[name]
            self._save_registry()
            return {"status": "success", "message": f"已移除 '{name}'"}
        return {"status": "error", "message": f"'{name}' 未注册"}


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 人脸验证引擎")
    subparsers = parser.add_subparsers(dest="command")

    p_register = subparsers.add_parser("register", help="注册人脸")
    p_register.add_argument("--face", required=True, help="人脸图片路径")
    p_register.add_argument("--name", required=True, help="身份名称")

    p_verify = subparsers.add_parser("verify", help="验证人脸")
    p_verify.add_argument("--face", required=True)
    p_verify.add_argument("--name", required=True)

    p_compare = subparsers.add_parser("compare", help="比对两张人脸")
    p_compare.add_argument("--face1", required=True)
    p_compare.add_argument("--face2", required=True)

    p_list = subparsers.add_parser("list", help="列出已注册")
    p_remove = subparsers.add_parser("remove", help="移除身份")
    p_remove.add_argument("--name", required=True)

    p_status = subparsers.add_parser("status", help="引擎状态")

    args = parser.parse_args()

    if args.command == "status":
        verifier = FaceVerifier()
        print(json.dumps({
            "engine": "人脸验证引擎 v1.0",
            "insightface": HAS_INSIGHT,
            "opencv": HAS_CV2,
            "registered": len(verifier.registry),
            "dna": "#龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-FACE-VERIFY-v1.0-UID9622"
        }, ensure_ascii=False, indent=2))
        return

    verifier = FaceVerifier()

    if args.command == "register":
        result = verifier.register_face(Path(args.face), args.name)
    elif args.command == "verify":
        result = verifier.verify_face(Path(args.face), args.name)
    elif args.command == "compare":
        result = verifier.compare_faces(Path(args.face1), Path(args.face2))
    elif args.command == "list":
        items = verifier.list_registered()
        if items:
            print(json.dumps(items, ensure_ascii=False, indent=2))
        else:
            print("（空·无人脸注册）")
        return
    elif args.command == "remove":
        result = verifier.remove_identity(args.name)
    else:
        parser.print_help()
        return

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
