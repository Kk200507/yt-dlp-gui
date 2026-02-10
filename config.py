import json
import os
from pathlib import Path

CONFIG_FILE = Path("config.json")

def load_config():
    """Load the configuration from the JSON file."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def save_config(config):
    """Save the configuration to the JSON file."""
    try:
        CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")
    except OSError:
        pass # Fail silently if we can't write config

def get_save_path():
    """Get the last saved path or default to Downloads."""
    config = load_config()
    path = config.get("save_path")
    
    # Verify the path still exists
    if path and os.path.isdir(path):
        return path
        
    return os.path.expanduser("~/Downloads")

def set_save_path(path):
    """Update the save path in the configuration."""
    config = load_config()
    config["save_path"] = str(path)
    save_config(config)
