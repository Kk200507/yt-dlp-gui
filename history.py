import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("history.json")

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []

def save_history_entry(info):
    history = load_history()

    # Avoid duplicate entries based on ID if possible, or just append
    # But usually we want the latest at top
    
    entry = {
        "id": f"{info.get('extractor', 'unknown')}_{info.get('id', 'unknown')}",
        "title": info.get("title", "Unknown Title"),
        "url": info.get("webpage_url", ""),
        "extractor": info.get("extractor", "unknown"),
        "format": info.get("ext"),
        "container": info.get("ext"),   # mp4 / webm / m4a
        "resolution": info.get("resolution"),
        "height": info.get("height"),
        "width": info.get("width"),
        "filesize_mb": round((info.get("filesize_approx", 0) or 0) / 1024 / 1024, 2),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


    history.insert(0, entry)

    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def clear_history():
    HISTORY_FILE.write_text("[]", encoding="utf-8")
