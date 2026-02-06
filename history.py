import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("history.json")

def load_history():
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    return []

def save_history_entry(info):
    history = load_history()

    entry = {
        "id": f"{info['extractor']}_{info['id']}",
        "title": info["title"],
        "url": info["webpage_url"],
        "extractor": info["extractor"],
        "format": info.get("ext"),
        "container": info.get("ext"),   # mp4 / webm / m4a
        "resolution": info.get("resolution"),
        "filesize_mb": round((info.get("filesize_approx", 0) or 0) / 1024 / 1024, 2),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    history.insert(0, entry)

    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
