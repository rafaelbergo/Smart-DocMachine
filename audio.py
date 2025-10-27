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
    
def audio_to_text() -> str:
    try:
        model = whisper.load_model('base')
        result = model.transcribe(AUDIO_PATH_QUESTION, language="pt")
        return result["text"]
    except Exception as e:
        print(f'ERRO | def audio_to_text | {e}')

    return None

def gravar_audio(duracao_segundos, sample_rate=44100):
    """
    Grava Ã¡udio do microfone por um determinado perÃ­odo e salva em um arquivo WAV.

    Args:
        duracao_segundos (int): DuraÃ§Ã£o da gravaÃ§Ã£o em segundos.
        nome_arquivo (str): Nome do arquivo de saÃ­da (com extensÃ£o .wav).
        sample_rate (int): Taxa de amostragem (amostras por segundo). 44100 Hz Ã© comum para Ã¡udio de qualidade de CD.
    """
    # Grava o Ã¡udio
    # dtype='int16' define o tipo de dado para as amostras (16 bits)
    print(sd.query_devices())

    gravacao = sd.rec(int(duracao_segundos * sample_rate), samplerate=sample_rate, channels=1, dtype='int16', device=1)
    sd.wait()  # Espera a gravaÃ§Ã£o terminar

    sf.write(AUDIO_PATH_QUESTION, gravacao, sample_rate)

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