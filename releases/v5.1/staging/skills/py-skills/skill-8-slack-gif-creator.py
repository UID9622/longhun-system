#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂 Slack GIF 創建工具 v1.0
Longhun Slack GIF Creator

DNA:#龍芯⚡️2026-06-07-SLACK-GIF-CREATOR-v1.0
"""

from PIL import Image, ImageDraw, ImageSequence
import math
from typing import List, Tuple, Dict
from datetime import datetime

class SlackGIFCreator:
    """Slack 最优化 GIF 創建器"""
    
    # Slack 約束
    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_FRAMES = 300
    RECOMMENDED_WIDTH = 512
    RECOMMENDED_HEIGHT = 512
    RECOMMENDED_FPS = 10
    
    def __init__(self, width: int = 512, height: int = 512, duration: int = 100):
        """
        初始化 GIF 創建器
        
        Args:
            width: 寬度（推薦 512px）
            height: 高度（推薦 512px）
            duration: 每幀持續時間（毫秒）
        """
        self.width = width
        self.height = height
        self.duration = duration
        self.frames: List[Image.Image] = []
        self.created_at = datetime.now().isoformat()
    
    def add_static_frame(self, draw_func, duration: int = None) -> None:
        """添加靜態幀"""
        img = Image.new('RGB', (self.width, self.height), color=(10, 14, 39))
        draw = ImageDraw.Draw(img)
        draw_func(draw)
        self.frames.append(img)
    
    def add_animated_sequence(self, draw_func, frame_count: int = 30) -> None:
        """添加動畫序列"""
        for i in range(frame_count):
            img = Image.new('RGB', (self.width, self.height), color=(10, 14, 39))
            draw = ImageDraw.Draw(img)
            progress = i / frame_count
            draw_func(draw, progress, i, frame_count)
            self.frames.append(img)
    
    def create_loading_spinner(self) -> None:
        """創建加載動畫"""
        def draw_spinner(draw, progress, frame_num, total_frames):
            center_x, center_y = self.width // 2, self.height // 2
            radius = 50
            angle = (progress * 360) % 360
            
            # 繪製背景圓
            draw.ellipse(
                [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                outline=(0, 212, 255),
                width=3
            )
            
            # 繪製旋轉的弧
            start_angle = angle
            end_angle = angle + 90
            draw.arc(
                [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                start=int(start_angle),
                end=int(end_angle),
                fill=(0, 212, 255),
                width=5
            )
            
            # 添加文字
            draw.text(
                (center_x - 30, center_y + 70),
                "加載中...",
                fill=(0, 212, 255)
            )
        
        self.add_animated_sequence(draw_spinner, frame_count=24)
    
    def create_pulse_animation(self) -> None:
        """創建脈衝動畫"""
        def draw_pulse(draw, progress, frame_num, total_frames):
            center_x, center_y = self.width // 2, self.height // 2
            
            # 計算脈衝半徑
            pulse_radius = int(20 + math.sin(progress * math.pi * 2) * 30)
            
            # 繪製脈衝圓
            draw.ellipse(
                [center_x - pulse_radius, center_y - pulse_radius,
                 center_x + pulse_radius, center_y + pulse_radius],
                fill=(0, 212, 255),
                outline=(0, 245, 255)
            )
            
            # 中心點
            draw.ellipse(
                [center_x - 5, center_y - 5, center_x + 5, center_y + 5],
                fill=(255, 255, 255)
            )
        
        self.add_animated_sequence(draw_pulse, frame_count=20)
    
    def create_wave_animation(self) -> None:
        """創建波浪動畫"""
        def draw_wave(draw, progress, frame_num, total_frames):
            amplitude = 20
            frequency = 2
            speed = progress * 2 * math.pi
            
            # 繪製波浪線
            points = []
            for x in range(0, self.width, 20):
                y = self.height // 2 + amplitude * math.sin((x / 100 + speed) * frequency)
                points.append((x, int(y)))
            
            if len(points) > 1:
                draw.line(points, fill=(0, 212, 255), width=3)
            
            # 添加文字
            draw.text(
                (self.width // 2 - 50, 50),
                "龍魂系統",
                fill=(0, 212, 255)
            )
        
        self.add_animated_sequence(draw_wave, frame_count=30)
    
    def create_success_animation(self) -> None:
        """創建成功動畫"""
        def draw_success(draw, progress, frame_num, total_frames):
            center_x, center_y = self.width // 2, self.height // 2
            
            # 繪製圓形背景
            radius = int(60 * progress)
            if radius > 0:
                draw.ellipse(
                    [center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    outline=(74, 222, 128),
                    width=3
                )
            
            # 繪製勾號
            if progress > 0.3:
                check_progress = (progress - 0.3) / 0.7
                # 繪製勾號路徑
                x1, y1 = center_x - 20, center_y + 5
                x2, y2 = center_x - 5, center_y + 20
                x3, y3 = center_x + 20, center_y - 15
                
                # 第一部分（短線）
                if check_progress < 0.5:
                    px = x1 + (x2 - x1) * (check_progress * 2)
                    py = y1 + (y2 - y1) * (check_progress * 2)
                    draw.line([(x1, y1), (px, py)], fill=(74, 222, 128), width=5)
                else:
                    draw.line([(x1, y1), (x2, y2)], fill=(74, 222, 128), width=5)
                    # 第二部分（長線）
                    seg_progress = (check_progress - 0.5) * 2
                    px = x2 + (x3 - x2) * seg_progress
                    py = y2 + (y3 - y2) * seg_progress
                    draw.line([(x2, y2), (px, py)], fill=(74, 222, 128), width=5)
        
        self.add_animated_sequence(draw_success, frame_count=24)
    
    def create_error_animation(self) -> None:
        """創建錯誤動畫"""
        def draw_error(draw, progress, frame_num, total_frames):
            center_x, center_y = self.width // 2, self.height // 2
            
            # 繪製圓形背景
            radius = int(60 * progress)
            if radius > 0:
                draw.ellipse(
                    [center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    outline=(255, 0, 110),
                    width=3
                )
            
            # 繪製 X 號
            if progress > 0.3:
                x_progress = (progress - 0.3) / 0.7
                offset = int(30 * x_progress)
                draw.line(
                    [(center_x - offset, center_y - offset),
                     (center_x + offset, center_y + offset)],
                    fill=(255, 0, 110),
                    width=5
                )
                draw.line(
                    [(center_x + offset, center_y - offset),
                     (center_x - offset, center_y + offset)],
                    fill=(255, 0, 110),
                    width=5
                )
        
        self.add_animated_sequence(draw_error, frame_count=20)
    
    def save(self, filepath: str, optimize: bool = True) -> Dict:
        """保存 GIF 文件"""
        if not self.frames:
            raise ValueError("No frames added")
        
        if len(self.frames) > self.MAX_FRAMES:
            self.frames = self.frames[:self.MAX_FRAMES]
        
        # 保存 GIF
        self.frames[0].save(
            filepath,
            save_all=True,
            append_images=self.frames[1:],
            duration=self.duration,
            loop=0,
            optimize=optimize
        )
        
        # 檢查文件大小
        import os
        file_size = os.path.getsize(filepath)
        
        return {
            "filepath": filepath,
            "frame_count": len(self.frames),
            "size_bytes": file_size,
            "size_mb": round(file_size / (1024 * 1024), 2),
            "duration_ms": self.duration * len(self.frames),
            "slack_compatible": file_size < self.MAX_SIZE,
            "created_at": self.created_at
        }


# 示例使用
if __name__ == "__main__":
    print("🐉 龍魂 Slack GIF 創建工具 v1.0")
    print("=" * 50)
    
    # 創建加載動畫
    print("\n⏳ 創建加載動畫...")
    creator1 = SlackGIFCreator()
    creator1.create_loading_spinner()
    result1 = creator1.save("/mnt/user-data/outputs/longhun-loading.gif")
    print(f"✅ GIF 已保存: {result1['filepath']}")
    print(f"   幀數: {result1['frame_count']}")
    print(f"   文件大小: {result1['size_mb']} MB")
    
    # 創建成功動畫
    print("\n✅ 創建成功動畫...")
    creator2 = SlackGIFCreator()
    creator2.create_success_animation()
    result2 = creator2.save("/mnt/user-data/outputs/longhun-success.gif")
    print(f"✅ GIF 已保存: {result2['filepath']}")
    
    # 創建脈衝動畫
    print("\n💓 創建脈衝動畫...")
    creator3 = SlackGIFCreator()
    creator3.create_pulse_animation()
    result3 = creator3.save("/mnt/user-data/outputs/longhun-pulse.gif")
    print(f"✅ GIF 已保存: {result3['filepath']}")
    
    print("\n✅ 所有 GIF 已創建！")
