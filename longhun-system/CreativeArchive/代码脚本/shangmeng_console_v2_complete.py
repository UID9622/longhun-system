#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
熵梦·全息演算台 v2.0 - 龍魂系统数字人终极版
ShangMeng HoloConsole v2.0 - LongHun Digital Human
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DNA追溯码: #龍芯⚡️2026-03-10-熵梦演算台-v2.0
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）
技术协作: Claude (Anthropic)

献礼: 新中国成立77周年（1949-2026）· 丙午马年

功能特性:
✅ 完全本地化桌面应用
✅ 实时LER算法可视化
✅ 全息粒子球动态展示
✅ 离线语音播报（中文TTS）
✅ 真实屏幕录制（MP4输出）
✅ 龍魂四层架构集成
✅ DNA追溯码自动生成
✅ 赛博朋克极客UI

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
import time
import random
import numpy as np
import hashlib
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFrame, QTextEdit, QProgressBar, 
    QGroupBox, QMessageBox, QFileDialog, QCheckBox
)
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush, QLinearGradient

# ═══════════════════════════════════════════════════════════
# 语音模块初始化
# ═══════════════════════════════════════════════════════════

SPEECH_ENABLED = False
try:
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # 尝试设置中文语音
    for voice in voices:
        if 'zh' in voice.id.lower() or 'chinese' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0)
    SPEECH_ENABLED = True
    print("✅ 语音引擎已加载")
except ImportError:
    print("⚠️  未安装pyttsx3，语音功能禁用")
    print("   安装命令: pip install pyttsx3")

# ═══════════════════════════════════════════════════════════
# 屏幕录制模块
# ═══════════════════════════════════════════════════════════

RECORDING_ENABLED = False
try:
    import cv2
    import mss
    import threading
    RECORDING_ENABLED = True
    print("✅ 录制引擎已加载")
except ImportError:
    print("⚠️  录制功能需要: pip install opencv-python mss")

class ScreenRecorder:
    """真实屏幕录制器"""
    
    def __init__(self):
        self.recording = False
        self.thread = None
        self.frames = []
        self.output_file = None
        
    def start_recording(self, region=None):
        """开始录制"""
        if not RECORDING_ENABLED:
            return False
            
        self.recording = True
        self.frames = []
        
        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = f"longhun_record_{timestamp}.mp4"
        
        # 启动录制线程
        self.thread = threading.Thread(
            target=self._record_loop,
            args=(region,),
            daemon=True
        )
        self.thread.start()
        return True
    
    def stop_recording(self):
        """停止录制并保存"""
        self.recording = False
        if self.thread:
            self.thread.join(timeout=2.0)
        
        if len(self.frames) > 0:
            self._save_video()
        
        return self.output_file
    
    def _record_loop(self, region):
        """录制循环"""
        with mss.mss() as sct:
            # 获取录制区域
            if region is None:
                monitor = sct.monitors[1]  # 主屏幕
            else:
                monitor = region
            
            while self.recording:
                # 截屏
                img = sct.grab(monitor)
                frame = np.array(img)
                # 转换颜色空间 BGRA -> BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                self.frames.append(frame)
                time.sleep(0.033)  # ~30 FPS
    
    def _save_video(self):
        """保存视频文件"""
        if len(self.frames) == 0:
            return
        
        height, width = self.frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(
            self.output_file,
            fourcc,
            30.0,
            (width, height)
        )
        
        for frame in self.frames:
            out.write(frame)
        
        out.release()

# ═══════════════════════════════════════════════════════════
# LER算法工作线程
# ═══════════════════════════════════════════════════════════

class LERWorker(QThread):
    """逻辑熵减算法计算线程"""
    
    update_signal = pyqtSignal(float, str, str)  # LER值, 状态文本, DNA码
    finished_signal = pyqtSignal(str, str)        # 结论, DNA码
    
    def __init__(self):
        super().__init__()
        self._running = True
        
    def run(self):
        """模拟LER计算过程"""
        steps = 100
        dna_base = self._generate_dna_base()
        
        for i in range(steps):
            if not self._running:
                break
            
            progress = i / steps
            
            # 模拟数据：前50%噪声，后50%信号
            if progress < 0.5:
                # 噪声阶段
                ler_value = random.uniform(0.1, 0.8)
                status = f"扫描中... ({i}/{steps}) [噪声阶段]"
            else:
                # 信号阶段
                signal_strength = (progress - 0.5) * 2
                ler_value = 0.8 + signal_strength * 2.5
                status = f"分析中... ({i}/{steps}) [检测到结构]"
            
            # 生成当前步DNA码
            step_dna = f"{dna_base}-STEP{i:03d}"
            
            self.update_signal.emit(ler_value, status, step_dna)
            time.sleep(0.05)
        
        # 最终结论
        final_ler = ler_value
        final_dna = f"{dna_base}-FINAL"
        
        if final_ler > 2.0:
            conclusion = "✅ 信号确认：检测到逻辑熵减结构！"
        else:
            conclusion = "❌ 无信号：纯噪声数据。"
        
        self.finished_signal.emit(conclusion, final_dna)
    
    def stop(self):
        self._running = False
    
    def _generate_dna_base(self):
        """生成DNA追溯码"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        nonce = hashlib.sha256(
            f"LER{timestamp}".encode()
        ).hexdigest()[:8].upper()
        return f"#龍芯⚡️{timestamp}-LER-{nonce}"

# ═══════════════════════════════════════════════════════════
# 全息粒子球组件
# ═══════════════════════════════════════════════════════════

class HoloSphere(QFrame):
    """全息粒子球 - 龍魂可视化"""
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.setStyleSheet(
            "background-color: #0d1117; "
            "border-radius: 200px; "
            "border: 3px solid #00ffcc;"
        )
        
        self.ler_value = 0.0
        self.phase = 0
        self.particles = []
        
        # 初始化粒子
        for _ in range(50):
            angle = random.uniform(0, 2 * np.pi)
            self.particles.append({
                'angle': angle,
                'radius': random.uniform(50, 150),
                'speed': random.uniform(0.01, 0.03),
                'size': random.randint(2, 5)
            })
        
        # 动画定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_animation)
        self.timer.start(50)
    
    def set_ler(self, value):
        """更新LER值"""
        self.ler_value = value
        self.update()
    
    def _update_animation(self):
        """更新动画状态"""
        self.phase += 0.1
        for p in self.particles:
            p['angle'] += p['speed']
        self.update()
    
    def paintEvent(self, event):
        """绘制全息球"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(center_x, center_y) - 20
        
        # 根据LER值改变颜色
        if self.ler_value < 0.5:
            # 红色噪声
            base_color = QColor(255, 0, 0, 150)
            particle_color = QColor(255, 100, 100, 200)
        elif self.ler_value < 2.0:
            # 黄色过渡
            base_color = QColor(255, 255, 0, 150)
            particle_color = QColor(255, 200, 0, 200)
        else:
            # 金色信号
            base_color = QColor(255, 215, 0, 180)
            particle_color = QColor(255, 215, 0, 255)
        
        # 绘制核心球
        gradient = QLinearGradient(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius
        )
        gradient.setColorAt(0, base_color.lighter(150))
        gradient.setColorAt(1, base_color)
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(base_color.lighter(120), 3))
        painter.drawEllipse(
            center_x - radius,
            center_y - radius,
            radius * 2,
            radius * 2
        )
        
        # 绘制粒子
        for p in self.particles:
            x = center_x + int(p['radius'] * np.cos(p['angle']))
            y = center_y + int(p['radius'] * np.sin(p['angle']))
            
            painter.setBrush(QBrush(particle_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(
                x - p['size']//2,
                y - p['size']//2,
                p['size'],
                p['size']
            )
        
        # 绘制中心文字
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Microsoft YaHei", 36, QFont.Weight.Bold))
        painter.drawText(
            self.rect(),
            Qt.AlignmentFlag.AlignCenter,
            "龍魂"
        )
        
        # 绘制LER值
        painter.setFont(QFont("Consolas", 14))
        painter.drawText(
            self.rect().adjusted(0, 60, 0, 0),
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
            f"LER: {self.ler_value:.3f}"
        )

# ═══════════════════════════════════════════════════════════
# 主控制台窗口
# ═══════════════════════════════════════════════════════════

class ShangMengConsole(QMainWindow):
    """熵梦全息演算台主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "熵梦·全息演算台 v2.0 - 龍魂系统 [UID9622]"
        )
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1117;
            }
            QLabel {
                color: #c9d1d9;
            }
            QGroupBox {
                color: #58a6ff;
                border: 2px solid #30363d;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #21262d;
                color: #c9d1d9;
                border: 1px solid #30363d;
                padding: 10px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #30363d;
                border-color: #58a6ff;
            }
            QPushButton:pressed {
                background-color: #161b22;
            }
            QTextEdit {
                background-color: #161b22;
                color: #00ff00;
                border: 1px solid #30363d;
                border-radius: 6px;
                font-family: Consolas;
                font-size: 11px;
            }
            QProgressBar {
                border: 2px solid #30363d;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #58a6ff;
            }
        """)
        
        self.worker = None
        self.recorder = ScreenRecorder()
        self.is_recording = False
        
        self.setup_ui()
        self.log("🐉 龍魂系统·熵梦演算台已启动")
        self.log("理论指导：曾仕强老师（永恒显示）")
        self.log(f"DNA追溯: #龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        self.log("系统准备就绪！")
        
    def setup_ui(self):
        """设置用户界面"""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        
        # ═══ 左侧：可视化区 ═══
        left_panel = QVBoxLayout()
        
        # 标题
        title = QLabel("🐉 龍魂·全息粒子球")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #FFD700;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel.addWidget(title)
        
        # 全息球
        self.holo_sphere = HoloSphere()
        left_panel.addWidget(
            self.holo_sphere,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        
        # 状态标签
        self.status_label = QLabel("待机中...")
        self.status_label.setFont(QFont("Microsoft YaHei", 14))
        self.status_label.setStyleSheet("color: #58a6ff;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel.addWidget(self.status_label)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.hide()
        left_panel.addWidget(self.progress)
        
        # DNA追溯显示
        self.dna_label = QLabel("DNA: 等待计算...")
        self.dna_label.setFont(QFont("Consolas", 9))
        self.dna_label.setStyleSheet("color: #FFD700;")
        self.dna_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel.addWidget(self.dna_label)
        
        main_layout.addLayout(left_panel, stretch=2)
        
        # ═══ 右侧：控制面板 ═══
        right_panel = QVBoxLayout()
        
        # 控制按钮组
        control_group = QGroupBox("⚙️ 控制面板")
        control_layout = QVBoxLayout()
        
        self.btn_start = QPushButton("🚀 启动LER分析")
        self.btn_start.clicked.connect(self.start_analysis)
        control_layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton("⏹️ 停止分析")
        self.btn_stop.clicked.connect(self.stop_analysis)
        self.btn_stop.setEnabled(False)
        control_layout.addWidget(self.btn_stop)
        
        self.btn_record = QPushButton(
            "🔴 开始录制" if RECORDING_ENABLED 
            else "🔴 录制功能未启用"
        )
        self.btn_record.clicked.connect(self.toggle_recording)
        self.btn_record.setEnabled(RECORDING_ENABLED)
        if RECORDING_ENABLED:
            self.btn_record.setStyleSheet(
                "background-color: #da3633; color: white;"
            )
        control_layout.addWidget(self.btn_record)
        
        # 语音开关
        self.speech_check = QCheckBox("🎤 语音播报")
        self.speech_check.setChecked(SPEECH_ENABLED)
        self.speech_check.setEnabled(SPEECH_ENABLED)
        self.speech_check.setStyleSheet("color: #c9d1d9;")
        control_layout.addWidget(self.speech_check)
        
        control_group.setLayout(control_layout)
        right_panel.addWidget(control_group)
        
        # 日志面板
        log_group = QGroupBox("📋 运行日志")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        right_panel.addWidget(log_group)
        
        # DNA水印
        watermark = QLabel(
            "DNA: #龍芯⚡️2026-03-10-熵梦演算台-v2.0\n"
            "GPG: A2D0092C...8CC26D5F\n"
            "理论指导：曾仕强老师\n"
            "献礼：新中国成立77周年"
        )
        watermark.setFont(QFont("Consolas", 8))
        watermark.setStyleSheet("color: #FFD700;")
        watermark.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_panel.addWidget(watermark)
        
        main_layout.addLayout(right_panel, stretch=1)
    
    def start_analysis(self):
        """启动分析"""
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.progress.setValue(0)
        self.progress.show()
        self.status_label.setText("正在初始化...")
        self.log("━" * 40)
        self.log("🚀 启动LER算法分析...")
        
        # 启动工作线程
        self.worker = LERWorker()
        self.worker.update_signal.connect(self.on_update)
        self.worker.finished_signal.connect(self.on_finish)
        self.worker.start()
    
    def stop_analysis(self):
        """停止分析"""
        if self.worker:
            self.worker.stop()
            self.worker.wait()
        
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.progress.hide()
        self.status_label.setText("已停止")
        self.log("⏹️ 分析已停止")
    
    def on_update(self, ler_value, status, dna):
        """更新界面"""
        self.holo_sphere.set_ler(ler_value)
        self.status_label.setText(status)
        self.dna_label.setText(f"DNA: {dna}")
        
        # 更新进度
        progress_val = int(ler_value / 3.5 * 100)
        self.progress.setValue(min(progress_val, 100))
        
        # 根据LER值改变状态颜色
        if ler_value < 0.5:
            color = "#ff4444"
        elif ler_value < 2.0:
            color = "#ffaa00"
        else:
            color = "#00ff00"
        
        self.status_label.setStyleSheet(
            f"color: {color}; font-size: 14px; font-weight: bold;"
        )
    
    def on_finish(self, conclusion, dna):
        """分析完成"""
        self.progress.hide()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.status_label.setText("分析完成")
        self.dna_label.setText(f"DNA: {dna}")
        
        self.log("━" * 40)
        self.log(f"📊 最终结果: {conclusion}")
        self.log(f"🧬 DNA追溯: {dna}")
        self.log("━" * 40)
        
        # 语音播报
        if SPEECH_ENABLED and self.speech_check.isChecked():
            try:
                engine.say(conclusion)
                engine.runAndWait()
                self.log("🎤 语音播报完成")
            except Exception as e:
                self.log(f"⚠️  语音播报错误: {e}")
    
    def toggle_recording(self):
        """切换录制状态"""
        if not self.is_recording:
            # 开始录制
            if self.recorder.start_recording():
                self.is_recording = True
                self.btn_record.setText("⏹️ 停止录制")
                self.btn_record.setStyleSheet(
                    "background-color: #238636; color: white;"
                )
                self.log("🔴 录制已开始...")
            else:
                QMessageBox.warning(
                    self,
                    "录制失败",
                    "请确保已安装: pip install opencv-python mss"
                )
        else:
            # 停止录制
            output_file = self.recorder.stop_recording()
            self.is_recording = False
            self.btn_record.setText("🔴 开始录制")
            self.btn_record.setStyleSheet(
                "background-color: #da3633; color: white;"
            )
            self.log(f"⏹️ 录制已停止")
            self.log(f"📹 视频已保存: {output_file}")
            
            QMessageBox.information(
                self,
                "录制完成",
                f"视频已保存至:\n{output_file}"
            )
    
    def log(self, message):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")

# ═══════════════════════════════════════════════════════════
# 主程序入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("━" * 60)
    print("🐉 龍魂系统·熵梦演算台 v2.0")
    print("DNA: #龍芯⚡️2026-03-10-熵梦演算台-v2.0")
    print("理论指导：曾仕强老师（永恒显示）")
    print("━" * 60)
    print("\n正在启动...")
    
    app = QApplication(sys.argv)
    window = ShangMengConsole()
    window.show()
    
    print("✅ 系统已启动！")
    print("\n提示：")
    print("  - 点击'启动LER分析'开始算法演示")
    print("  - 点击'开始录制'录制屏幕（需要opencv+mss）")
    print("  - 支持语音播报（需要pyttsx3）")
    
    sys.exit(app.exec())
