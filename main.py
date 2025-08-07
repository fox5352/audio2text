import sys
import base64
import argparse
from speech import Converter

def main():
    parser = argparse.ArgumentParser(description="Convert base64 audio input")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--audio-buffer", type=str,
                       help="Base64-encoded audio input. Use '-' to read from stdin.")
    group.add_argument("-if", "--input-file", type=str,
                       help="Input file path that contains raw audio data.")
    
    args = parser.parse_args()


    # Read from stdin if -a is "-"
    if args.audio_buffer == "-":
        buffer = sys.stdin.read().strip()
    elif args.input_file:
        try:
            with open(args.input_file, "rb") as f:
                buffer = f.read()
                buffer = base64.b64encode(buffer).decode("utf-8")
        except FileNotFoundError:
            print(f"File not found: {args.input_file}", file=sys.stderr)
            sys.exit(1)
    else:
        buffer = args.audio_buffer

    if not buffer.strip():
        print("Error: audio buffer is empty", file=sys.stderr)
        sys.exit(1)

    try:
        cv = Converter()
        decoded_audio_buffer = base64.b64decode(buffer)
        result = cv.transcribe(decoded_audio_buffer)
        print("Transcription result:", result)
        
    except Exception as e:
        print(f"Error processing audio: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()