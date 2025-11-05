from __future__ import annotations
import queue
from typing import Callable, Optional
import sounddevice as sd

class AudioStream:
    """
    Gestisce lo stream audio dal microfono e invia chunk grezzi (bytes)
    a una coda consumata dal riconoscitore Vosk.
    """

    def __init__(self, samplerate: int = 16000, channels: int = 1, device_index: Optional[int] = None):
        self.samplerate = samplerate
        self.channels = channels
        self.device_index = device_index
        self.q: "queue.Queue[bytes]" = queue.Queue()
        self.stream: Optional[sd.RawInputStream] = None

    def _callback(self, indata, frames, time, status):  # noqa: D401
        if status:
            # Non alziamo eccezioni: lo status può riportare anche piccoli underflow
            print(f"[audio] status: {status}", flush=True)
        self.q.put(bytes(indata))

    def start(self):
        if self.stream is not None:
            return
        self.stream = sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=8000,  # ~0.5s a 16k mono, riduci per più reattività
            dtype="int16",
            channels=self.channels,
            callback=self._callback,
            device=self.device_index,
        )
        self.stream.start()

    def stop(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        # Svuota coda
        with self.q.mutex:
            self.q.queue.clear()
