from __future__ import annotations
import argparse
import logging
from utils import setup_logging, get_model_dir, get_audio_device_index
from audio_stream import AudioStream
from stt_vosk import VoskRecognizer
from gui import STTGui

def main():
    parser = argparse.ArgumentParser(description="Speech-to-Text offline realtime (Vosk + Tkinter)")
    parser.add_argument("--model-dir", type=str, default=None, help="Percorso al modello Vosk (cartella)")
    parser.add_argument("--device", type=int, default=None, help="Indice dispositivo audio (microfono)")
    parser.add_argument("--rate", type=int, default=16000, help="Sample rate (default 16000)")
    args = parser.parse_args()

    setup_logging(logging.INFO)

    model_dir = get_model_dir(args.model_dir)
    device_index = get_audio_device_index(args.device)
    samplerate = int(args.rate)

    audio = AudioStream(samplerate=samplerate, channels=1, device_index=device_index)

    recognizer = VoskRecognizer(
        model_dir=model_dir,
        samplerate=samplerate,
        audio_queue=audio.q,
        on_partial=None,  # settiamo dopo dalla GUI
        on_final=None,
    )

    app = STTGui(
        on_start=lambda: on_start(app, audio, recognizer),
        on_stop=lambda: on_stop(app, audio, recognizer),
        on_clear=lambda: on_clear(app),
    )

    # Colleghiamo i callback ora che la GUI esiste
    recognizer.on_partial = lambda text: app.after(0, app.set_partial, text)
    recognizer.on_final = lambda text: app.after(0, app.append_final, text)

    # UI iniziale
    app.set_listening(False)
    app.mainloop()

def on_start(app: STTGui, audio: AudioStream, rec: VoskRecognizer):
    try:
        audio.start()
        rec.start()
        app.set_listening(True)
    except Exception as e:
        app.set_partial(f"Errore start: {e}")

def on_stop(app: STTGui, audio: AudioStream, rec: VoskRecognizer):
    try:
        rec.stop()
        audio.stop()
        app.set_listening(False)
        app.set_partial("")
    except Exception as e:
        app.set_partial(f"Errore stop: {e}")

def on_clear(app: STTGui):
    app.text.delete("1.0", "end")
    app.set_partial("")

if __name__ == "__main__":
    main()
