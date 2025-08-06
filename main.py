import sys
import base64
import argparse

def main():
    parser = argparse.ArgumentParser(description="Convert base64 audio input")
    parser.add_argument("-a", "--audio-buffer", type=str, required=True,
                        help="Base64-encoded audio input. Use '-' to read from stdin.")
    args = parser.parse_args()

    # Read from stdin if -a is "-"
    if args.audio_buffer == "-":
        buffer = sys.stdin.read()
    else:
        buffer = args.audio_buffer

    if not buffer.strip():
        print("Error: audio buffer is empty", file=sys.stderr)
        sys.exit(1)

    try:
        decoded = base64.b64decode(buffer)
    except Exception:
        print("Error decoding audio buffer", file=sys.stderr)
        sys.exit(1)

    print("Audio buffer decoded successfully")
    sys.exit(0)

if __name__ == "__main__":
    main()
