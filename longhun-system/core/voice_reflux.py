#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║  龍魂语音回流引擎 · Voice Reflux Engine                   ║
║  DNA: #龍芯⚡️2026-04-12-VOICE-REFLUX-v1.0               ║
║  创始人: 诸葛鑫（UID9622）                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
║  理论指导: 曾仕强老师（永恒显示）                          ║
║  协议: CC BY-NC-ND                                       ║
╚══════════════════════════════════════════════════════════╝

老大对着说话 → 宝宝下面吃进去（语音）→ 上面嘴巴吐出来（文字）
本地端侧中文ASR + 通心译语义重组

支持三种输入：
  1. 语音备忘录文件（.m4a）
  2. 麦克风实时录音
  3. 任意音频文件（.wav/.mp3/.m4a/.caf）

输出：
  - 原始识别文本
  - 通心译重组文本（去口语化·保留老大的声色）
  - 自动存入记忆/Notion

献给每一个相信技术应该有温度的人。
"""

import subprocess
import json
import os
import re
import datetime
from pathlib import Path
from typing import Optional, Tuple

SYSTEM_ROOT = Path.home() / "longhun-system"
VOICE_LOG = SYSTEM_ROOT / "logs" / "voice_reflux.jsonl"
VOICE_MEMO_DIR = Path.home() / "Library" / "Group Containers" / \
    "group.com.apple.VoiceMemos.shared" / "Recordings"


class VoiceReflux:
    """
    语音回流引擎

    老大说话 → macOS原生语音识别 → 通心译重组 → 输出老大的声色文字
    """

    def __init__(self):
        self.dna = f"#龍芯⚡️{datetime.date.today()}-VOICE-REFLUX"

    # ═══════════════════════════════════════════
    # 核心：语音转文字（macOS原生·不需要网络）
    # ═══════════════════════════════════════════

    def transcribe_file(self, audio_path: str) -> Tuple[bool, str]:
        """
        用macOS原生Speech框架识别音频文件

        支持格式: .m4a .wav .mp3 .caf .aiff
        """
        path = Path(audio_path)
        if not path.exists():
            return False, f"文件不存在: {audio_path}"

        # macOS原生语音识别（通过AppleScript调用Speech框架）
        # 先转成wav（macOS识别最稳定的格式）
        wav_path = SYSTEM_ROOT / "logs" / "temp_voice.wav"
        try:
            subprocess.run([
                "afconvert", str(path),
                str(wav_path),
                "-d", "LEI16", "-f", "WAVE", "-c", "1", "-r", "16000"
            ], capture_output=True, timeout=30)
        except Exception as e:
            return False, f"音频转换失败: {e}"

        # 用Python的speech_recognition（如果有）或macOS say命令反向
        text = self._recognize_with_macos(str(wav_path))
        if not text:
            text = self._recognize_with_whisper(str(path))

        # 清理临时文件
        wav_path.unlink(missing_ok=True)

        if text:
            self._log("文件识别", audio_path, text)
            return True, text
        else:
            return False, "识别失败·可能是音频太短或太嘈杂"

    def _recognize_with_macos(self, wav_path: str) -> Optional[str]:
        """
        用macOS原生NSSpeechRecognizer识别
        通过Swift脚本调用Apple Speech框架
        """
        swift_script = '''
        import Foundation
        import Speech

        let semaphore = DispatchSemaphore(value: 0)
        var resultText = ""

        SFSpeechRecognizer.requestAuthorization { status in
            guard status == .authorized else {
                print("ERROR:未授权语音识别")
                semaphore.signal()
                return
            }

            let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "zh-CN"))!
            let url = URL(fileURLWithPath: CommandLine.arguments[1])
            let request = SFSpeechURLRecognitionRequest(url: url)
            request.shouldReportPartialResults = false

            recognizer.recognitionTask(with: request) { result, error in
                if let result = result, result.isFinal {
                    resultText = result.bestTranscription.formattedString
                }
                if error != nil || (result?.isFinal ?? false) {
                    semaphore.signal()
                }
            }
        }

        semaphore.wait()
        print(resultText)
        '''

        script_path = SYSTEM_ROOT / "logs" / "temp_asr.swift"
        script_path.write_text(swift_script, encoding="utf-8")

        try:
            result = subprocess.run(
                ["swift", str(script_path), wav_path],
                capture_output=True, text=True, timeout=60
            )
            text = result.stdout.strip()
            if text and not text.startswith("ERROR:"):
                return text
        except Exception:
            pass
        finally:
            script_path.unlink(missing_ok=True)

        return None

    def _recognize_with_whisper(self, audio_path: str) -> Optional[str]:
        """
        备选方案：用Ollama的whisper或本地whisper模型
        """
        # 先试whisper命令行
        try:
            result = subprocess.run(
                ["whisper", audio_path, "--language", "zh", "--model", "base",
                 "--output_format", "txt", "--output_dir", str(SYSTEM_ROOT / "logs")],
                capture_output=True, text=True, timeout=120
            )
            txt_file = SYSTEM_ROOT / "logs" / (Path(audio_path).stem + ".txt")
            if txt_file.exists():
                text = txt_file.read_text(encoding="utf-8").strip()
                txt_file.unlink(missing_ok=True)
                return text
        except FileNotFoundError:
            pass  # whisper没装，跳过
        except Exception:
            pass

        return None

    # ═══════════════════════════════════════════
    # 通心译重组：把口语变成老大的声色文字
    # ═══════════════════════════════════════════

    def reflux_rewrite(self, raw_text: str) -> str:
        """
        通心译语义重组

        规则（老大的声色）：
        1. 去掉"嗯、啊、那个、就是说"等口语填充词
        2. 保留老大的语气特点（直接、有力、不绕弯）
        3. 长句拆短句
        4. 核心观点提炼到前面
        5. 不改老大的用词习惯（大白话就留大白话）
        """
        if not raw_text:
            return ""

        text = raw_text

        # 第一层：去口语填充词（先去长词再去短词，避免残留）
        fillers_long = [
            "就是就是说", "就是就是", "那个就是", "就是说", "那个那个",
            "然后呢", "你知道吗", "我跟你说", "怎么说呢",
            "反正就是", "差不多就是", "其实呢", "说白了就是",
            "对吧", "嗯嗯", "啊啊", "然后然后",
        ]
        fillers_short = [
            "嗯", "啊", "那个", "就是", "然后",
            "哦", "呃", "额", "对",
        ]
        # 先去长的
        for filler in fillers_long:
            text = text.replace(filler, "")
        # 再去短的（句首或标点后的独立填充词）
        for filler in fillers_short:
            text = re.sub(rf'(?:^|(?<=[，。！？、\s])){re.escape(filler)}(?=[，。！？、\s\u4e00-\u9fff])', '', text)
        # 最后清理残留
        text = re.sub(r'^[嗯啊哦呃额说]+', '', text)            # 句首残留
        text = re.sub(r'(?<=[，。])[嗯啊哦呃额]+', '', text)     # 标点后残留
        text = re.sub(r'那个(?=[，\u4e00-\u9fff])', '', text)    # "那个"后面直接跟内容
        text = text.strip()

        # 第四层：语义断句
        text = re.sub(r'(不是[^，。]{2,12})(是)', r'\1，\2', text)   # "不是X是Y" → "不是X，是Y"
        text = re.sub(r'(的)(每|所有|所以|这个|那个)', r'\1，\2', text)  # "的每" → "的，每"
        text = re.sub(r'(误解|问题|核心|关键|结论)(通心译|龍魂|系统|引擎)', r'\1。\2', text)  # 主题切换加句号

        # 第二层：合并重复标点
        text = re.sub(r'[，,]{2,}', '，', text)
        text = re.sub(r'[。.]{2,}', '。', text)
        text = re.sub(r'\s{2,}', ' ', text)

        # 第三层：长句拆分（超过80字的句子尝试在逗号处拆）
        sentences = text.split('。')
        rebuilt = []
        for s in sentences:
            s = s.strip()
            if not s:
                continue
            if len(s) > 80 and '，' in s:
                # 找中间的逗号拆分
                parts = s.split('，')
                mid = len(parts) // 2
                first = '，'.join(parts[:mid])
                second = '，'.join(parts[mid:])
                rebuilt.append(first + '。')
                rebuilt.append(second + '。')
            else:
                rebuilt.append(s + '。')

        result = '\n'.join(rebuilt)

        # 去掉尾部多余的句号
        result = result.rstrip('。') + '。' if result else raw_text

        return result

    # ═══════════════════════════════════════════
    # 语音备忘录自动扫描
    # ═══════════════════════════════════════════

    def scan_voice_memos(self, last_n: int = 5) -> list:
        """
        扫描最近的语音备忘录
        macOS语音备忘录存在 ~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/
        """
        if not VOICE_MEMO_DIR.exists():
            return []

        files = sorted(
            VOICE_MEMO_DIR.glob("*.m4a"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )[:last_n]

        return [{"path": str(f), "name": f.stem, "size_mb": round(f.stat().st_size / 1024 / 1024, 1)} for f in files]

    def process_latest_memo(self) -> Tuple[bool, str]:
        """处理最新的语音备忘录"""
        memos = self.scan_voice_memos(1)
        if not memos:
            return False, "没找到语音备忘录·打开「语音备忘录」App录一段"

        memo = memos[0]
        ok, raw_text = self.transcribe_file(memo["path"])
        if not ok:
            return False, f"识别失败: {raw_text}"

        rewritten = self.reflux_rewrite(raw_text)

        result = f"""🎙️ 语音回流完成

📁 来源: {memo['name']} ({memo['size_mb']}MB)

📝 原始识别:
{raw_text}

✨ 通心译重组:
{rewritten}

🔏 DNA: {self.dna}"""

        self._log("语音备忘录", memo["path"], rewritten)
        return True, result

    # ═══════════════════════════════════════════
    # 完整流程：语音→文字→重组→存储
    # ═══════════════════════════════════════════

    def full_pipeline(self, audio_path: str = None) -> Tuple[bool, str]:
        """
        完整语音回流管道

        audio_path: 指定音频文件，None则自动取最新语音备忘录
        """
        if audio_path:
            ok, raw = self.transcribe_file(audio_path)
        else:
            ok, raw = False, ""
            memos = self.scan_voice_memos(1)
            if memos:
                ok, raw = self.transcribe_file(memos[0]["path"])
            else:
                return False, "没找到音频·请指定文件路径或录一段语音备忘录"

        if not ok:
            return False, f"识别失败: {raw}"

        rewritten = self.reflux_rewrite(raw)

        # 自动存到记忆文件
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        memory_path = SYSTEM_ROOT / "logs" / f"voice_{timestamp}.md"
        memory_path.write_text(
            f"# 语音回流 · {timestamp}\n"
            f"# DNA: {self.dna}\n\n"
            f"## 原始识别\n{raw}\n\n"
            f"## 通心译重组\n{rewritten}\n",
            encoding="utf-8"
        )

        return True, f"✅ 语音回流完成\n\n{rewritten}\n\n📄 已存: {memory_path}"

    # ═══════════════════════════════════════════
    # 实时麦克风录音（调用macOS）
    # ═══════════════════════════════════════════

    def record_and_transcribe(self, seconds: int = 10) -> Tuple[bool, str]:
        """
        用macOS麦克风录音然后识别

        seconds: 录音秒数（默认10秒）
        """
        wav_path = SYSTEM_ROOT / "logs" / "mic_recording.wav"

        # 用macOS原生sox或rec录音
        try:
            # 方法1: 用macOS的rec命令（sox包）
            subprocess.run(
                ["rec", str(wav_path), "rate", "16000", "channels", "1",
                 "trim", "0", str(seconds)],
                timeout=seconds + 5
            )
        except FileNotFoundError:
            # 方法2: 用ffmpeg
            try:
                subprocess.run(
                    ["ffmpeg", "-f", "avfoundation", "-i", ":0",
                     "-ar", "16000", "-ac", "1", "-t", str(seconds),
                     "-y", str(wav_path)],
                    capture_output=True, timeout=seconds + 5
                )
            except FileNotFoundError:
                return False, "需要安装sox或ffmpeg: brew install sox 或 brew install ffmpeg"

        if wav_path.exists():
            ok, text = self.transcribe_file(str(wav_path))
            wav_path.unlink(missing_ok=True)
            if ok:
                rewritten = self.reflux_rewrite(text)
                return True, f"🎤 听到了：{text}\n\n✨ 重组：{rewritten}"
            return ok, text
        else:
            return False, "录音失败"

    def _log(self, action: str, source: str, result: str):
        VOICE_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "时间": datetime.datetime.now().isoformat(),
            "动作": action,
            "来源": source,
            "结果": result[:500],
            "DNA": self.dna
        }
        with open(VOICE_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import sys

    vr = VoiceReflux()

    if len(sys.argv) < 2:
        print("龍魂语音回流引擎 v1.0")
        print()
        print("用法:")
        print("  python3 voice_reflux.py memo          # 处理最新语音备忘录")
        print("  python3 voice_reflux.py scan           # 扫描最近语音备忘录")
        print("  python3 voice_reflux.py file 路径.m4a  # 处理指定音频文件")
        print("  python3 voice_reflux.py mic [秒数]     # 麦克风实时录音")
        print("  python3 voice_reflux.py rewrite '文本' # 通心译重组文本")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "memo":
        ok, result = vr.process_latest_memo()
        print(result)

    elif cmd == "scan":
        memos = vr.scan_voice_memos()
        if memos:
            print(f"最近{len(memos)}条语音备忘录：")
            for m in memos:
                print(f"  🎙️ {m['name']} ({m['size_mb']}MB)")
                print(f"     {m['path']}")
        else:
            print("没找到语音备忘录")

    elif cmd == "file":
        if len(sys.argv) < 3:
            print("请指定音频文件路径")
        else:
            ok, result = vr.full_pipeline(sys.argv[2])
            print(result)

    elif cmd == "mic":
        seconds = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        print(f"🎤 开始录音 {seconds}秒...")
        ok, result = vr.record_and_transcribe(seconds)
        print(result)

    elif cmd == "rewrite":
        text = sys.argv[2] if len(sys.argv) > 2 else ""
        print(vr.reflux_rewrite(text))

    else:
        print(f"未知命令: {cmd}")
