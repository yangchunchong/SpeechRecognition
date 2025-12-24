import speech_recognition as sr
import pyaudio
from typing import Optional, Dict, Any
import wave
import numpy as np


class BasicSpeechRecognition:
    """基础语音识别类"""

    def __init__(self, api_key: str = None, language: str = "zh-CN"):
        """
        初始化语音识别器

        Args:
            api_key: API密钥（如果需要）
            language: 识别语言，默认中文
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.language = language
        self.api_key = api_key

        # 调整环境噪音
        with self.microphone as source:
            print("正在校准环境噪音，请保持安静...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("校准完成")

    def record_audio(self, duration: float = 5.0, sample_rate: int = 16000) -> Optional[sr.AudioData]:
        """
        录制音频

        Args:
            duration: 录音时长（秒）
            sample_rate: 采样率

        Returns:
            AudioData对象或None
        """
        try:
            with self.microphone as source:
                print(f"开始录音，时长{duration}秒...")
                audio = self.recognizer.listen(
                    source,
                    timeout=3,
                    phrase_time_limit=duration
                )
                print("录音完成")
                return audio
        except sr.WaitTimeoutError:
            print("录音超时，未检测到声音")
            return None
        except Exception as e:
            print(f"录音失败: {e}")
            return None

    def recognize_google(self, audio_data: sr.AudioData) -> Optional[str]:
        """
        使用Google Speech Recognition识别

        Args:
            audio_data: 音频数据

        Returns:
            识别结果文本
        """
        try:
            text = self.recognizer.recognize_google(
                audio_data,
                language=self.language
            )
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition无法理解音频")
            return None
        except sr.RequestError as e:
            print(f"Google服务请求失败: {e}")
            return None

    def recognize_offline(self, audio_data: sr.AudioData) -> Optional[str]:
        """
        使用CMU Sphinx离线识别（需要安装pocketsphinx）

        Args:
            audio_data: 音频数据

        Returns:
            识别结果文本
        """
        try:
            # 需要安装: pip install pocketsphinx
            text = self.recognizer.recognize_sphinx(audio_data)
            return text
        except ImportError:
            print("请安装pocketsphinx: pip install pocketsphinx")
            return None
        except sr.UnknownValueError:
            print("Sphinx无法理解音频")
            return None

    def save_audio(self, audio_data: sr.AudioData, filename: str = "recording.wav"):
        """
        保存音频到文件

        Args:
            audio_data: 音频数据
            filename: 文件名
        """
        with open(filename, "wb") as f:
            f.write(audio_data.get_wav_data())
        print(f"音频已保存到: {filename}")

    def live_transcription(self, duration: float = 10.0):
        """
        实时转录

        Args:
            duration: 总转录时长
        """
        import time

        end_time = time.time() + duration
        print(f"开始实时转录，持续{duration}秒...")

        while time.time() < end_time:
            audio = self.record_audio(duration=3)
            if audio:
                text = self.recognize_google(audio)
                if text:
                    print(f"识别结果: {text}")
                else:
                    print("未识别到有效内容")
            time.sleep(0.5)

        print("转录结束")


# 使用示例
if __name__ == "__main__":
    recognizer = BasicSpeechRecognition(language="zh-CN")

    # 录制并识别
    audio = recognizer.record_audio(duration=5)
    if audio:
        recognizer.save_audio(audio, "test_recording.wav")

        # Google识别
        text = recognizer.recognize_google(audio)
        if text:
            print(f"Google识别结果: {text}")

        # 离线识别
        # text_offline = recognizer.recognize_offline(audio)
        # if text_offline:
        #     print(f"离线识别结果: {text_offline}")

    # 实时转录
    # recognizer.live_transcription(duration=30)
