import os
import hashlib
import json


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
        

hashes = scan_folder("watched")
save_baseline(hashes, "baseline.json")