import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

DOCUMENT_PATH = os.path.join(DATA_DIR, 'document.jpg')

def take_picture() -> bool:
    try:
        result = subprocess.run(['libcamera-still', '-o', DOCUMENT_PATH], check=True)
        print(f"[document] Foto salva em: {DOCUMENT_PATH}")
        return result.returncode == 0
    
    except Exception as e:
        print(f"ERRO | def take_picture | {e}")
        return False
