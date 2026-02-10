from config import get_save_path, set_save_path, load_config
import os
import shutil

# Test 1: Default path
if os.path.exists("config.json"):
    os.remove("config.json")
    
print(f"Default path: {get_save_path()}")

# Test 2: Set path
test_path = os.path.abspath(".")
set_save_path(test_path)
print(f"Set path to: {test_path}")

# Test 3: Get path
saved_path = get_save_path()
print(f"Retrieved path: {saved_path}")

assert saved_path == test_path

# Test 4: Invalid path
# manually verify config.json content
print(f"Config content: {load_config()}")

# Test 5: Non-existent path fallback
with open("config.json", "w") as f:
    f.write('{"save_path": "C:/NonExistentPath_12345"}')

print(f"Fallback path for invalid dir: {get_save_path()}")

# Clean up
if os.path.exists("config.json"):
    os.remove("config.json")
