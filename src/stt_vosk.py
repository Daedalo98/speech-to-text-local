from __future__ import annotations
import json
import threading
import time
from pathlib import Path
from typing import Callable, Optional

import numpy as np
from vosk import Model, KaldiRecognizer

class VoskRecognizer:
    """
    Consuma chunk audio (bytes) da una coda e produce partial/final text.
    Chiama i callback forniti dall'app/GUI.
    """

    def __init__(
        self,
        model_dir: Path,
        samplerate: int = 16000,
        on_partial: Optional[Callable[[str], None]] = None,
        on_final: Optional[Callable[[str], None]] = None,
        audio_queue=None,
    ):
        self.model_dir = model_dir
        self.samplerate = samplerate
        self.on_partial = on_partial
        self.on_final = on_final
        self.audio_queue = audio_queue
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._recognizer: Optional[KaldiRecognizer] = None
        self._last_final_time = time.time()

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        if not self.model_dir.exists():
            raise FileNotFoundError(
                f"Modello Vosk non trovato in '{self.model_dir}'. Esegui scripts/download_model.sh"
            )
        model = Model(str(self.model_dir))
        self._recognizer = KaldiRecognizer(model, self.samplerate)
        self._recognizer.SetWords(True)

        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)
        self._thread = None

    def _loop(self):
        assert self.audio_queue is not None, "audio_queue non impostata"
        assert self._recognizer is not None

        while not self._stop.is_set():
            try:
                data: bytes = self.audio_queue.get(timeout=0.1)
            except Exception:
                continue

            if len(data) == 0:
                continue

            if self._recognizer.AcceptWaveform(data):
                # Risultato "final"
                msg = self._recognizer.Result()
                try:
                    j = json.loads(msg)
                    text = (j.get("text") or "").strip()
                    now = time.time()
                    if now - self._last_final_time > 1.5:
                        self.on_final("\n\n")  # or some spacing or marker
                    self._last_final_time = now

                    if text and self.on_final:
                        self.on_final(text)
                except json.JSONDecodeError:
                    pass
            else:
                # Risultato "partial"
                msg = self._recognizer.PartialResult()
                try:
                    j = json.loads(msg)
                    text = (j.get("partial") or "").strip()
                    if self.on_partial:
                        self.on_partial(text)
                except json.JSONDecodeError:
                    pass
