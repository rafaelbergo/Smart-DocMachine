import whisper
from paddleocr import PaddleOCR
from gtts import gTTS
import subprocess
import os, requests, json
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv

load_dotenv()
api_url = os.getenv('API_ENDPOINT')

FOLDER = os.getcwd()
DOCUMENT_PATH = os.path.join(FOLDER, 'document.jpg')
AUDIO_PATH_RESPONSE = os.path.join(FOLDER, 'audio_offline.mp3')
AUDIO_PATH_QUESTION = os.path.join(FOLDER, 'audio_gravado.wav')

if __name__ == '__main__':
    print(api_url) 
    print(FOLDER)
