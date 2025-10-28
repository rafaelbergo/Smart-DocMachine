import os
from gtts import gTTS
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading


def resample_audio(sr_out, data, sr_in):
    if sr_in == sr_out:
        return data, sr_in

    ratio = sr_out / sr_in
    n_out = int(round(data.shape[0] * ratio))
    x_old = np.linspace(0.0, 1.0, data.shape[0], endpoint=False)
    x_new = np.linspace(0.0, 1.0, n_out, endpoint=False)
    if data.ndim == 1:
        out = np.interp(x_new, x_old, data).astype('float32')
    else:
        out = np.zeros((n_out, data.shape[1]), dtype='float32')
        for ch in range(data.shape[1]):
            out[:, ch] = np.interp(x_new, x_old, data[:, ch])
    return out, sr_out

def text_to_audio(text: str, path: str) -> bool:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tts = gTTS(text=text, lang='pt', slow=False)
        tts.save(path)
        return True
    except Exception as e:
        print(f'ERRO | def text_to_audio | {e}')
        return False

def playAudio(filepath: str) -> bool:
    try:
        data, sr = sf.read(filepath, dtype='float32', always_2d=False)
        data, sr = resample_audio(48000, data, sr)
        sd.play(data, sr)
        sd.wait()
        return True
    except Exception as e:
        print(f"Error playing audio: {e}")
        return False

def playAudio_async(filepath: str) -> None:
    threading.Thread(target=playAudio, args=(filepath,), daemon=True).start()


_rec_state = {
    "stream": None,
    "file": None,
    "lock": threading.Lock(),
}

def start_recording(out_path: str, sample_rate: int = 44100, channels: int = 1, device=None) -> bool:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with _rec_state["lock"]:
        if _rec_state["stream"] is not None:
            print("[audio] ja esta gravando; ignorando novo start.")
            return False

        # abre arquivo WAV e stream de entrada
        sf_file = sf.SoundFile(out_path, mode='w', samplerate=sample_rate,
                               channels=channels, subtype='PCM_16')

        def _callback(indata, frames, time, status):
            if status:
                print(f"[audio] status: {status}")
            # grava dados diretamente (int16)
            sf_file.write(indata)

        stream = sd.InputStream(samplerate=sample_rate,
                                channels=channels,
                                dtype='int16',
                                callback=_callback,
                                device=device)

        stream.start()
        _rec_state["file"] = sf_file
        _rec_state["stream"] = stream
        print(f"[audio] gravando... -> {out_path}")
        return True

def stop_recording() -> bool:

    with _rec_state["lock"]:
        stream = _rec_state["stream"]
        sf_file = _rec_state["file"]
        if stream is None:
            print("[audio] nao estava gravando.")
            return False
        try:
            stream.stop()
            stream.close()
        finally:
            _rec_state["stream"] = None
        try:
            sf_file.close()
        finally:
            _rec_state["file"] = None
        print("[audio] gravacao finalizada e salva.")
        return True