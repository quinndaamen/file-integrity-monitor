import os
import hashlib
import json


MONITOR_FOLDER = r"C:\Users\Quinn\Documents\desk\Coding\Portfolio\FIM\tests\watched"
HASH_FILE = "file_hashes.json"


def calculate_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
    except FileNotFoundError:
        return None
    return sha256.hexdigest()

def scan_folder(folder):
    file_hashes = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_hash(filepath)
            if file_hash:
                file_hashes[filepath] = file_hash

    return file_hashes

def save_baseline(file_hashes, filepath):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(file_hashes, file, indent=4, ensure_ascii=False)
        
def load_baseline(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def compare_hashes(baseline, current):
    for filepath, filehash in current.items():
        
        if filepath not in baseline:
            print(f"[NEW FILE] {filepath}")

        elif baseline[filepath] != filehash:
            print(f"[MODIFIED] {filepath}")

    for filepath in baseline:

        if filepath not in current:
            print(f"[DELETED] {filepath}")
  


baseline = load_baseline(HASH_FILE)
current = scan_folder(MONITOR_FOLDER)

print("Initial baseline loaded.")
compare_hashes(baseline, current)

