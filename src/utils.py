from __future__ import annotations
import os
import sys
from pathlib import Path
import logging

APP_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = APP_ROOT / "models" / "it" / "model"  # default: IT piccolo
LOGS_DIR = APP_ROOT / "logs"

def ensure_dirs() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def get_model_dir(cli_override: str | None = None) -> Path:
    env_dir = os.getenv("STT_MODEL_DIR")
    if cli_override:
        return Path(cli_override).expanduser().resolve()
    if env_dir:
        return Path(env_dir).expanduser().resolve()
    return MODELS_DIR

def get_audio_device_index(cli_override: int | None = None) -> int | None:
    env_idx = os.getenv("AUDIO_DEVICE_INDEX")
    if cli_override is not None:
        return cli_override
    if env_idx is not None and env_idx.strip() != "":
        try:
            return int(env_idx)
        except ValueError:
            pass
    return None

def setup_logging(level: int = logging.INFO) -> None:
    ensure_dirs()
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )
