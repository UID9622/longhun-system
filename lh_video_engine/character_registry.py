#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂视频引擎 · 角色不动点系统 v1.1
DNA: #龍芯⚡️2026-08-22-CHARACTER-REGISTRY-v1.1
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
设计原则: 同一角色每次生成长相同——参考图库+描述锁+Seed绑定三层不动点
修复记录 v1.1: BEICHEN_PROFILE 顶层缩进 SyntaxError 修复·md5→sha256
"""

import json, hashlib, shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field, asdict

REGISTRY_ROOT = Path.home() / "longhun-system" / "lh_video_engine" / "characters"

@dataclass
class CharacterProfile:
    character_id:    str
    name:            str
    ref_images:      List[str]         # 参考图路径列表（相对 chars/{id}/refs/）
    lock_prompt:     str               # 固定描述词（外貌、服装、神态）
    forbidden_change: List[str]        # 绝对不允许改变的特征
    base_seed:       int    = 9622     # 基准 Seed
    seed_variance:   int    = 50       # Seed 允许浮动范围（±)
    face_strength:   float  = 0.85    # IP-Adapter/FaceID 强度
    style_preset:    str    = "中国风·未来感·冷峻"
    dna:             Optional[str] = None
    created_at:      Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    def get_effective_prompt(self, expression: str = "中性") -> str:
        """生成携带不动点锁定的完整提示词"""
        return (
            f"{self.lock_prompt}, "
            f"表情: {expression}, "
            f"风格: {self.style_preset}, "
            f"高质量, 细节精准, 面部稳定"
        )

    def get_seed_for_shot(self, shot_index: int) -> int:
        """同一角色不同镜头的 Seed 策略：基准 ± 少量抖动，保持相似度"""
        return self.base_seed + (shot_index % (self.seed_variance * 2)) - self.seed_variance

class CharacterRegistry:
    """
    角色不动点注册中心
    - 注册角色（首次）
    - 查询角色（生成时调用）
    - 更新参考图库
    - 输出锁定提示词 + Seed
    """

    def __init__(self, root: Path = REGISTRY_ROOT):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _char_dir(self, cid: str) -> Path:
        return self.root / cid

    def _registry_file(self, cid: str) -> Path:
        return self._char_dir(cid) / "registry.json"

    @staticmethod
    def _make_dna(cid: str) -> str:
        # 禁 md5（规则第七层加密下界）→ sha256
        ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        h  = hashlib.sha256(f"{cid}{ts}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ts}-CHAR-{cid.upper()}-{h}"

    def register(self, profile: CharacterProfile) -> CharacterProfile:
        """注册角色，自动创建目录和 refs/ 子目录"""
        d = self._char_dir(profile.character_id)
        (d / "refs").mkdir(parents=True, exist_ok=True)
        profile.dna        = self._make_dna(profile.character_id)
        profile.created_at = datetime.now().isoformat()
        self._registry_file(profile.character_id).write_text(
            json.dumps(profile.to_dict(), ensure_ascii=False, indent=2), "utf-8")
        print(f"✅ 角色注册成功: {profile.name} ({profile.character_id})")
        return profile

    def load(self, character_id: str) -> Optional[CharacterProfile]:
        """加载已注册角色"""
        f = self._registry_file(character_id)
        if not f.exists():
            return None
        d = json.loads(f.read_text("utf-8"))
        valid = {k: v for k, v in d.items()
                 if k in CharacterProfile.__dataclass_fields__}
        return CharacterProfile(**valid)

    def add_ref_image(self, character_id: str, image_path: str) -> str:
        """向角色参考图库添加图片"""
        p    = self._char_dir(character_id) / "refs"
        dest = p / Path(image_path).name
        shutil.copy2(image_path, dest)
        # 更新 registry.json 的 ref_images 列表
        profile = self.load(character_id)
        rel = str(dest.relative_to(self._char_dir(character_id)))
        if rel not in profile.ref_images:
            profile.ref_images.append(rel)
        self._registry_file(character_id).write_text(
            json.dumps(profile.to_dict(), ensure_ascii=False, indent=2), "utf-8")
        return str(dest)

    def list_characters(self) -> List[str]:
        if not self.root.exists():
            return []
        return [d.name for d in self.root.iterdir() if d.is_dir()]

    def build_generation_config(self, character_id: str,
                                expression: str = "讲解",
                                shot_index: int = 0) -> Dict[str, Any]:
        """
        生成时调用此方法获取完整的生成配置
        返回格式可直接传入 SD / Flux / ComfyUI
        """
        p = self.load(character_id)
        if p is None:
            raise ValueError(f"角色未注册: {character_id}")
        refs_dir = self._char_dir(character_id) / "refs"
        refs = [str(refs_dir / r.split("/")[-1])
                for r in p.ref_images if (refs_dir / r.split("/")[-1]).exists()]
        return {
            "character_id":   character_id,
            "name":           p.name,
            "prompt":         p.get_effective_prompt(expression),
            "negative_prompt": "变形, 多人, 模糊, 低质量, 年龄偏差, 发型变化, 风格漂移",
            "seed":           p.get_seed_for_shot(shot_index),
            "face_strength":  p.face_strength,
            "ref_images":     refs,
            "forbidden_change": p.forbidden_change,
            "dna":            p.dna,
        }

# 预设北辰角色（注意：顶层声明不可有前导空格，否则 SyntaxError）
BEICHEN_PROFILE = CharacterProfile(
    character_id    = "beichen",
    name            = "北辰",
    ref_images      = [],
    lock_prompt     = (
        "男性, 约30岁, 寸头, 轮廓清晰, 冷静神态, "
        "深色中式立领外套, 固定面部特征, 下颌线清晰, 双眼有神"
    ),
    forbidden_change = ["发型", "脸型", "年龄感", "服装颜色", "瞳色"],
    base_seed       = 9622,
    seed_variance   = 30,
    face_strength   = 0.88,
    style_preset    = "中国风·未来感·冷峻·高清写实",
)

if __name__ == "__main__":
    reg = CharacterRegistry()
    if not reg.load("beichen"):
        reg.register(BEICHEN_PROFILE)
    cfg = reg.build_generation_config("beichen", expression="讲解", shot_index=1)
    print(json.dumps(cfg, ensure_ascii=False, indent=2))
