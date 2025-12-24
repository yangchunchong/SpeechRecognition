import whisper
import torch
import numpy as np
from typing import Optional, Dict, Any, List
import wave
import tempfile
import os
from datetime import datetime


class WhisperTranscriber:
    """Whisper语音转录"""

    def __init__(self,
                 model_size: str = "base",
                 device: str = "auto",
                 language: str = "zh"):
        """
        初始化Whisper

        Args:
            model_size: 模型大小 (tiny, base, small, medium, large)
            device: 设备 (cpu, cuda, auto)
            language: 语言代码
        """
        # 自动选择设备
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.device = device
        self.language = language

        print(f"加载Whisper模型: {model_size}, 设备: {device}")

        # 加载模型
        self.model = whisper.load_model(
            model_size,
            device=device
        )

        # 转录选项
        self.transcribe_options = {
            "language": language,
            "task": "transcribe",  # 或 "translate"
            "fp16": device == "cuda",  # 是否使用FP16
            "temperature": 0.0,
            "best_of": 5,
            "beam_size": 5,
            "condition_on_previous_text": True,
            "compression_ratio_threshold": 2.4,
            "logprob_threshold": -1.0,
            "no_speech_threshold": 0.6
        }

    def transcribe_file(self,
                        audio_path: str,
                        **kwargs) -> Dict[str, Any]:
        """
        转录音频文件

        Args:
            audio_path: 音频文件路径
            **kwargs: 覆盖转录选项

        Returns:
            转录结果
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"文件不存在: {audio_path}")

        # 合并选项
        options = self.transcribe_options.copy()
        options.update(kwargs)

        print(f"开始转录: {audio_path}")

        # 转录
        result = self.model.transcribe(
            audio_path,
            **options
        )

        return result

    def transcribe_bytes(self,
                         audio_bytes: bytes,
                         sample_rate: int = 16000,
                         **kwargs) -> Dict[str, Any]:
        """
        转录字节数据

        Args:
            audio_bytes: 音频字节
            sample_rate: 采样率
            **kwargs: 转录选项

        Returns:
            转录结果
        """
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            # 写入WAV头
            self.write_wav_header(tmp_file, audio_bytes, sample_rate)
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name

        try:
            # 转录临时文件
            result = self.transcribe_file(tmp_path, **kwargs)
            return result
        finally:
            # 删除临时文件
            os.unlink(tmp_path)

    def write_wav_header(self, file, audio_data: bytes, sample_rate: int):
        """写入WAV文件头"""
        import struct

        # 计算数据大小
        data_size = len(audio_data)

        # WAV文件头
        file.write(b'RIFF')
        file.write(struct.pack('<I', 36 + data_size))  # 文件大小
        file.write(b'WAVE')
        file.write(b'fmt ')
        file.write(struct.pack('<I', 16))  # fmt块大小
        file.write(struct.pack('<H', 1))  # 音频格式 (PCM)
        file.write(struct.pack('<H', 1))  # 声道数
        file.write(struct.pack('<I', sample_rate))  # 采样率
        file.write(struct.pack('<I', sample_rate * 2))  # 字节率
        file.write(struct.pack('<H', 2))  # 块对齐
        file.write(struct.pack('<H', 16))  # 位深度
        file.write(b'data')
        file.write(struct.pack('<I', data_size))  # 数据大小

    def transcribe_with_timestamps(self,
                                   audio_path: str,
                                   **kwargs) -> List[Dict[str, Any]]:
        """
        带时间戳的转录

        Args:
            audio_path: 音频路径
            **kwargs: 转录选项

        Returns:
            带时间戳的转录片段
        """
        result = self.transcribe_file(audio_path, **kwargs)

        segments = []
        for segment in result.get("segments", []):
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip(),
                "confidence": np.exp(segment.get("avg_logprob", 0)),
                "no_speech_prob": segment.get("no_speech_prob", 0)
            })

        return segments

    def realtime_transcription(self,
                               device_index: int = None,
                               chunk_duration: float = 5.0):
        """
        实时转录

        Args:
            device_index: 麦克风设备索引
            chunk_duration: 分块时长
        """
        import pyaudio
        import threading
        import queue

        p = pyaudio.PyAudio()

        # 获取设备
        if device_index is None:
            device_info = p.get_default_input_device_info()
        else:
            device_info = p.get_device_info_by_index(device_index)

        sample_rate = int(device_info['defaultSampleRate'])

        print(f"使用设备: {device_info['name']}")
        print(f"采样率: {sample_rate}")
        print(f"分块时长: {chunk_duration}秒")
        print("开始实时转录，按Ctrl+C停止...")

        # 音频队列
        audio_queue = queue.Queue()
        is_recording = True

        def record_audio():
            """录音线程"""
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                input=True,
                frames_per_buffer=int(sample_rate * chunk_duration),
                input_device_index=device_index
            )

            try:
                while is_recording:
                    # 读取音频数据
                    audio_data = stream.read(
                        int(sample_rate * chunk_duration),
                        exception_on_overflow=False
                    )

                    # 转换为numpy数组
                    audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                    # 放入队列
                    audio_queue.put(audio_array)

            except Exception as e:
                print(f"录音错误: {e}")
            finally:
                stream.stop_stream()
                stream.close()

        def transcribe_audio():
            """转录线程"""
            while is_recording or not audio_queue.empty():
                try:
                    # 获取音频数据
                    audio_array = audio_queue.get(timeout=1)

                    # 转录
                    result = self.model.transcribe(
                        audio_array,
                        language=self.language,
                        fp16=(self.device == "cuda")
                    )

                    text = result.get("text", "").strip()
                    if text:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"[{timestamp}] {text}")

                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"转录错误: {e}")

        # 启动线程
        record_thread = threading.Thread(target=record_audio, daemon=True)
        transcribe_thread = threading.Thread(target=transcribe_audio, daemon=True)

        record_thread.start()
        transcribe_thread.start()

        try:
            # 等待用户中断
            while True:
                import time
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n停止转录")
        finally:
            is_recording = False
            p.terminate()
            record_thread.join()
            transcribe_thread.join()


# 使用示例
if __name__ == "__main__":
    # 创建Whisper转录器
    whisper_asr = WhisperTranscriber(
        model_size="base",  # 根据需求选择模型大小
        language="zh"
    )

    # 转录文件
    if os.path.exists("test.wav"):
        result = whisper_asr.transcribe_file("test.wav")
        print("完整转录:")
        print(result["text"])

        # 带时间戳的转录
        segments = whisper_asr.transcribe_with_timestamps("test.wav")
        print("\n分段时间戳:")
        for seg in segments:
            print(f"[{seg['start']:.2f}-{seg['end']:.2f}] {seg['text']}")

    # 实时转录
    # whisper_asr.realtime_transcription()
