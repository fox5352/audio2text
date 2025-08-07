import speech_recognition as sr

class Converter:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def transcribe(self, audio_buffer):
        # Common microphone formats to try
        configs = [
            (44100, 2),  # Most common: 44.1kHz, 16-bit
            (16000, 2),  # Phone quality: 16kHz, 16-bit
            (48000, 2),  # Professional: 48kHz, 16-bit  
            (22050, 2),  # Half CD: 22kHz, 16-bit
        ]
        
        for sample_rate, sample_width in configs:
            try:
                audio_data = sr.AudioData(audio_buffer, sample_rate, sample_width)
                transcription = self.recognizer.recognize_google(audio_data)
                return transcription
            except sr.UnknownValueError:
                continue  # Try next config
            except sr.RequestError as e:
                return f"Error with speech recognition service: {e}"
        
        return "Could not understand audio"