Here’s a polished **README.md** for your repo speech‑to‑text‑local — you can copy and paste it into your GitHub project, then tweak any text you want. Ooooh, here it is:

# Speech‑to‑Text Local (offline, realtime)  
**Fully local realtime speech‑to‑text GUI using Vosk**  

## 🚀 What it is  
This project provides a minimal‑GUI Python app that captures microphone audio and converts it to text **entirely offline**, using the Vosk speech recognition engine.  
You’ll see *partial text updates* in real time and *final transcriptions* accumulated in a window.  
Perfect for privacy‑savvy, fast local transcription without cloud services.

## ✅ Key features  
- Offline speech‑to‑text — no internet required once model is downloaded  
- Real‑time display of partial and final text results  
- Simple Tkinter GUI: Start / Stop / Clear / Copy All  
- Suitable for single speaker or multi‑speaker (with manual color tagging, configurable)  
- Easy to configure, cross‑platform (Linux/macOS/Windows)  
- Intended for live transcription, note‑taking, accessibility, podcasts, etc.

## 🛠️ Setup & quick start  

### Prerequisites  
- Python **3.9+**, recommended 3.11 or 3.12  
- Microphone access and working audio input  
- On **Linux**: ensure `libportaudio2` (or equivalent) is installed; `python3‑tk` (for Tkinter)  
- On **macOS/Windows**: mic access permissions, Python distribution from python.org recommended

### Installation & first run  
From your project root:

```bash
./scripts/run.sh --device N
````

Where `N` is the device index of your microphone.
(E.g., `--device 0` for default; you can run `python -c "import sounddevice as sd; print(sd.query_devices())"` to list devices.)

The `run.sh` script will:

1. Create/activate a virtual environment (`.venv`)
2. Install required dependencies (`requirements.txt`)
3. Download the default Italian Vosk model (if not already present)
4. Launch the GUI

### Manual installation steps

If you prefer manual control:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./scripts/download_model.sh
python3 src/app.py --device N
```

## 📁 Directory structure

```
speech‑to‑text‑local/
├─ src/
│  ├─ app.py            # entry‑point GUI & CLI
│  ├─ gui.py            # Tkinter user interface
│  ├─ audio_stream.py   # microphone stream capture
│  ├─ stt_vosk.py       # Vosk recognizer wrapper
│  └─ utils.py          # utility functions (paths, logging, config)
├─ models/
│  └─ it/
│      └─ model/        # downloaded Vosk Italian model files here
├─ scripts/
│  ├─ setup.sh          # setup venv, install deps, download model
│  ├─ download_model.sh # download/prepare Vosk model
│  └─ run.sh            # full “setup + run” script
├─ tests/               # placeholder test files
├─ assets/              # (optional) UI icons or other resources
├─ README.md
├─ requirements.txt
├─ pyproject.toml
└─ LICENSE
```

## 🎨 Customisation & enhancements

Feel free to tweak/add:

* **Different colours for different voices/speakers** (via `tk.Text` tags)
* **Copy All / Export to .txt** functionality (button already present)
* **Pause‑based segmentation**: long silences trigger paragraph breaks
* Model for other languages: swap URL in `download_model.sh`, set `STT_MODEL_DIR` env var
* Adjust sample rate, channels, block size in `audio_stream.py` for latency tuning

## 🧰 Troubleshooting & Tips

* If you see: `Error querying device -1` → run `python -c "import sounddevice as sd; print(sd.query_devices())"` and pick a valid device index, then use `--device N`.
* If you get “model not found” → verify that `models/it/model/vosk-model.conf` exists. Move model files correctly if needed.
* For Linux: if microphone shows no input, check `arecord -l`, `pavucontrol`, and ensure PortAudio is working.
* In case of high latency: reduce `blocksize` or increase sample rate; or use a faster/slimmer model.

## 📄 License

This project is licensed under the [MIT License](./LICENSE) — use and modify it freely.

## 🤝 Contributions & Feedback

Feel free to open issues, suggest features, or submit pull requests.
Would love to hear your feedback on accuracy, latency, and usability.

---

*Created with ❤️ by Daedalo98*

