# Speech Recognition Tool

A lightweight, Python-powered command-line tool that converts raw audio buffers into readable text using Google's speech recognition API.

## Features

- Convert raw microphone audio streams to text
- Process raw audio files directly
- Base64 encoded input support
- Cross-platform compatibility
- Single executable build support

## Installation

```bash
python -m venv venv

source venv/Script/activate
```

### Dependencies
```bash
pip install -r requirements.txt
```

### Build Single Executable
```bash
python build.py
```

## Usage

### Raw Audio Buffer (Microphone Stream)
Process base64-encoded raw audio data from microphone input:

```bash
# From stdin
echo "base64_encoded_audio_data" | python main.py -a -

# From command line (for small buffers)
python main.py -a "base64_encoded_audio_data"
```

### Raw Audio File
Process raw audio files directly:

```bash
python main.py -if path/to/audio.raw
```

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `-a`, `--audio-buffer` | Base64-encoded raw audio buffer. Use '-' to read from stdin | `python main.py -a -` |
| `-if`, `--input-file` | Path to raw audio file | `python main.py -if audio.raw` |

## Audio Format Requirements

The tool expects **raw PCM audio data** in the following formats:
- **Sample Rate**: 44.1kHz, 48kHz, 16kHz, or 22kHz (auto-detected)
- **Bit Depth**: 16-bit
- **Channels**: Mono or Stereo
- **Encoding**: Little-endian signed integers

### Converting Audio Files to Raw PCM

Use FFmpeg to convert audio files to the correct format:

```bash
# Convert to 44.1kHz, 16-bit, mono raw PCM
ffmpeg -i input.mp3 -f s16le -ar 44100 -ac 1 output.raw

# Convert to 16kHz (phone quality)
ffmpeg -i input.wav -f s16le -ar 16000 -ac 1 output.raw
```

## Integration with Microphone Clients

This tool is designed to work as a child process with microphone capture applications:

```bash
# Example: Pipe microphone data through your audio client
your_mic_client | python main.py -a -
```

The microphone client should:
1. Capture raw PCM audio from the microphone
2. Encode the raw bytes as base64
3. Send to this tool via stdin

## Testing

Run the test suite to verify functionality:

```bash
python test.py
```

The tests generate synthetic raw audio data to simulate microphone input and verify the complete pipeline.

## Build Script

The included `build.py` script uses PyInstaller to create a standalone executable:

```bash
python build.py
```

This generates a single executable file that can be distributed without Python dependencies.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Error: audio buffer is empty" | Empty input provided | Provide valid audio data |
| "Invalid base64-encoded string" | Malformed base64 input | Check base64 encoding |
| "Could not understand audio" | Audio not recognizable as speech | Ensure clear speech in audio |
| "Error with speech recognition service" | API/network issues | Check internet connection |

## Examples

### Basic Usage
```bash
# Process microphone stream
echo "SGVsbG8gV29ybGQ=" | python main.py -a -

# Process raw audio file
python main.py -if recording.raw
```

### Integration Example
```python
import subprocess
import base64

# Your microphone capture code
raw_audio_data = capture_microphone()  # Returns raw PCM bytes

# Encode and send to speech recognition tool
encoded_audio = base64.b64encode(raw_audio_data).decode('utf-8')
result = subprocess.run(
    ['python', 'main.py', '-a', '-'],
    input=encoded_audio,
    capture_output=True,
    text=True
)

print("Transcription:", result.stdout)
```

## Requirements

- Python 3.6+
- Internet connection (for Google Speech Recognition API)
- Microphone access (for live audio capture)

## License

MIT License - Feel free to use and modify as needed.

## Troubleshooting

### "Could not understand audio" with clear speech
- Ensure audio is in raw PCM format, not compressed (MP3, M4A, etc.)
- Check sample rate matches common formats (44.1kHz, 48kHz, 16kHz)
- Verify audio contains clear human speech

### Network errors
- Check internet connection
- Verify Google's speech recognition service is accessible
- Consider implementing fallback to offline recognition engines

### Large audio buffers
- Use stdin (`-a -`) instead of command line arguments for large audio data
- Command line arguments have length limits on some systems