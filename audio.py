import os
from gtts import gTTS
import sounddevice as sd
import soundfile as sf

def text_to_audio(text: str, path: str) -> bool:
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        tts = gTTS(text=text, lang='pt', slow=False)  # Use slow=False for normal speed
        tts.save(path)
        return True
    except Exception as e:
        print(f'ERRO | def text_to_audio | {e}')
        return False

def playAudio(filepath: str) -> bool:
    try:
        data, samplerate = sf.read(filepath)
        sd.play(data, samplerate)
        sd.wait()  # Wait for playback to finish
        print("Audio played successfully.")
        return True
    except Exception as e:
        print(f"Error playing audio: {e}")
        return False