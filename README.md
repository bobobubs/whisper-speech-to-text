<!-- @format -->

# OpenAI Whisper to Speech Transcriber

## Overview

This script records audio using a hotkey, saves it as a WAV file, and then transcribes it into text using the OpenAI Whisper model. The transcribed text is automatically typed where your cursor is.

## Requirements

- Python 3.x
- pyaudio
- wave
- threading
- keyboard
- whisper
- pyautogui
- argparse

You can install these packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

To run the script, use the following command:

```bash
python recorder.py
```

### Custom Hotkey

You can specify a custom hotkey for toggling recording:

```bash
python recorder.py --hotkey 'alt+x'
```

## Class `AudioRecorder`

### Methods

- `toggle_recording()`: Toggles the recording state.
- `record()`: Records audio while `self.recording` is True.
- `transcribe_recording()`: Transcribes the recorded audio.
- `save_audio()`: Saves the recorded audio and transcribes it.
- `set_hotkey(hotkey)`: Sets a hotkey for toggling recording.

## License

MIT
