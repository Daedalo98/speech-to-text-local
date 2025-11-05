from __future__ import annotations
import tkinter as tk
from tkinter import ttk

class STTGui(tk.Tk):
    """
    GUI minimale:
    - Riga top: testo parziale (aggiorna spesso)
    - Riquadro: testo finale (accumula frasi)
    - Pulsanti: Start / Stop / Clear
    """

    def __init__(self, on_start, on_stop, on_clear):
        super().__init__()
        self.title("Speech-to-Text (offline, Vosk)")
        self.geometry("800x500")
        self.minsize(600, 360)

        # Parziale
        self.partial_var = tk.StringVar(value="")
        partial_frame = ttk.Frame(self, padding=10)
        partial_frame.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(partial_frame, text="Parziale:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self.partial_label = ttk.Label(
            partial_frame,
            textvariable=self.partial_var,
            font=("TkDefaultFont", 12),
            wraplength=760,
            foreground="#444",
        )
        self.partial_label.pack(anchor="w", fill=tk.X, pady=(2, 0))

        # Finale
        text_frame = ttk.Frame(self, padding=10)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        ttk.Label(text_frame, text="Finale:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self.text = tk.Text(text_frame, height=12, wrap="word")
        self.text.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        # Pulsanti
        btn_frame = ttk.Frame(self, padding=10)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.start_btn = ttk.Button(btn_frame, text="Start", command=on_start)
        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=on_stop)
        self.clear_btn = ttk.Button(btn_frame, text="Clear", command=on_clear)
        self.start_btn.pack(side=tk.LEFT)
        self.stop_btn.pack(side=tk.LEFT, padx=8)
        self.clear_btn.pack(side=tk.RIGHT)
        self.copy_btn = ttk.Button(btn_frame, text="Copy All", command=self.copy_text)
        self.copy_btn.pack(side=tk.RIGHT, padx=8)

        # Stato
        self.is_listening = False

    # API aggiornamento UI
    def set_partial(self, text: str):
        self.partial_var.set(text)

    def append_final(self, text: str):
        if text:
            self.text.insert("end", text.strip() + "\n")
            self.text.see("end")

    # Helpers
    def set_listening(self, value: bool):
        self.is_listening = value
        self.start_btn.state(["disabled"] if value else ["!disabled"])
        self.stop_btn.state(["!disabled"] if value else ["disabled"])

    def copy_text(self):
        full_text = self.text.get("1.0", tk.END)
        self.clipboard_clear()
        self.clipboard_append(full_text)
