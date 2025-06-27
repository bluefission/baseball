import os
import torchaudio
import json
import time
from app.generator import Segment
from pathlib import Path
from datetime import datetime

CONTEXT_ROOT = Path("/tmp/npc_audio_context")
CONTEXT_ROOT.mkdir(parents=True, exist_ok=True)
EXPIRATION_SECONDS = 600  # 10 minutes
MAX_SEGMENTS = 3


def _context_dir(speaker_id):
    return CONTEXT_ROOT / f"speaker_{speaker_id}"


def _context_file(speaker_id):
    return _context_dir(speaker_id) / "context.json"


def save_utterance(speaker_id, text, audio_tensor, sample_rate):
    dir_path = _context_dir(speaker_id)
    dir_path.mkdir(parents=True, exist_ok=True)

    timestamp = int(time.time())
    filename = f"{timestamp}.wav"
    filepath = dir_path / filename
    torchaudio.save(filepath, audio_tensor.unsqueeze(0).cpu(), sample_rate)

    meta = {
        "timestamp": timestamp,
        "text": text,
        "file": str(filepath)
    }

    # Append to context file
    context_path = _context_file(speaker_id)
    history = []
    if context_path.exists():
        try:
            with open(context_path, "r") as f:
                history = json.load(f)
        except Exception:
            pass

    history.append(meta)
    history = history[-MAX_SEGMENTS:]  # Cap at N entries

    with open(context_path, "w") as f:
        json.dump(history, f)


def get_recent_segments(speaker_id, sample_rate):
    context_path = _context_file(speaker_id)
    now = time.time()
    segments = []

    if not context_path.exists():
        return []

    try:
        with open(context_path, "r") as f:
            utterances = json.load(f)

        for entry in utterances:
            age = now - entry["timestamp"]
            if age > EXPIRATION_SECONDS:
                continue

            text = entry["text"]
            audio_tensor, sr = torchaudio.load(entry["file"])
            if sr != sample_rate:
                audio_tensor = torchaudio.functional.resample(audio_tensor.squeeze(0), orig_freq=sr, new_freq=sample_rate)
            else:
                audio_tensor = audio_tensor.squeeze(0)

            segments.append(Segment(text=text, speaker=speaker_id, audio=audio_tensor))

    except Exception:
        pass

    return segments
