import pyaudio
import wave
import threading
import keyboard
import whisper
import pyautogui
import argparse


class AudioRecorder:
    def __init__(self, chunk=1024, sample_format=pyaudio.paInt16, channels=1, fs=44100, filename="output.wav"):
        self.chunk = chunk
        self.sample_format = sample_format
        self.channels = channels
        self.fs = fs
        self.filename = filename
        self.frames = []
        self.recording = False
        self.model = "base"
        self.language = "English"
        self.console = "en"
        self.p = pyaudio.PyAudio()
        self.translations = {
            "en": {
                "recording": "🔴 Recording",
                "stopped": "🔄 Stopped recording",
                "tutorial": "to begin or end a recording, press ",
                "halt": "press alt+c to halt the program",
                "transcription": "🗣️",
                "language": "The language is currently set to: ",
                "model": "The model is currently set to: ",
            },
            "zh": {
                "recording": "🔴 录音中",
                "stopped": "🔄 转录中",
                "tutorial": "要开始或结束录音，请按 ",
                "halt": "按 alt+c 停止程序",
                "transcription": "🗣️",
                "language": "当前语言: ",
                "model": "当前模型: ",
            },
            "zh-tw": {
                "recording": "🔴 錄音中",
                "stopped": "🔄 轉錄中",
                "tutorial": "若要開始或結束錄音，請按 ",
                "halt": "按 alt+c 停止程序",
                "transcription": "🗣️",
                "language": "當前語言: ",
                "model": "當前模型: ",
            }
        }
        self.trans = self.translations['en']

    def console_language(self, console):
        self.console = console
        self.trans = self.translations[console]
        print(f"Console language set to: {console}")

    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            print(self.trans["recording"])
            self.frames = []  # Clear previous recording frames
            threading.Thread(target=self.record).start()
        else:
            print(self.trans["stopped"])

    def record(self):
        stream = self.p.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.fs,
            frames_per_buffer=self.chunk,
            input=True
        )
        while self.recording:
            data = stream.read(self.chunk)
            self.frames.append(data)
        stream.stop_stream()
        stream.close()
        self.save_audio()

    def transcribe_recording(self):
        options = {
            "language": self.language,
            "task": "transcribe"
        }
        result = self.model.transcribe(self.filename, **options)
        return result["text"]

    def save_audio(self):
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))

        transcription = self.transcribe_recording()
        print(self.trans["transcription"], transcription)
        pyautogui.write(transcription)

    def set_hotkey(self, hotkey):
        keyboard.add_hotkey(hotkey, self.toggle_recording, suppress=True)
        print(self.trans["tutorial"],  hotkey)
        print(self.trans["halt"])
        keyboard.wait('alt+c')

    def set_language(self, language):
        self.language = language
        print(self.trans["language"], self.language)

    def set_model(self, model):
        self.model = whisper.load_model(model)
        print(self.trans["model"],  model)


def main():
    parser = argparse.ArgumentParser(
        description='Audio Recorder and Transcriber')
    parser.add_argument('--hotkey', type=str, default='alt+x',
                        help='Hotkey to toggle recording')
    parser.add_argument('--language', type=str, default='en',
                        help='Language for transcription')
    parser.add_argument('--model', type=str, default='base',
                        help='Model for transcription')
    parser.add_argument('--console', type=str, default='en',
                        help='Language showing in console')
    args = parser.parse_args()

    recorder = AudioRecorder()
    recorder.console_language(args.console)
    recorder.set_language(args.language)
    recorder.set_model(args.model)
    recorder.set_hotkey(args.hotkey)


if __name__ == "__main__":
    main()
