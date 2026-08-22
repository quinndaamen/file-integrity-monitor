import os
import hashlib
import json
import typer
import time
from datetime import datetime

app = typer.Typer()

MONITOR_FOLDER = r"C:\Users\Quinn\Documents\desk\Coding\Portfolio\FIM\tests\watched"
HASH_FILE = "file_hashes.json"
CYCLE = 10 
LOG_FILE = "logs.json1"

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

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   

def compare_hashes(baseline, current):
    events = []

    for filepath, filehash in current.items():
        if filepath not in baseline:          
            events.append({
                "timestamp": get_timestamp(),
                "event": "NEW",
                "filepath": filepath,
                "hash": filehash
            })

        elif baseline[filepath] != filehash:
            events.append({
            "timestamp": get_timestamp(),
            "event": "MODIFIED",
            "filepath": filepath,
            "hash": filehash
        })

    for filepath in baseline:

        if filepath not in current:
            events.append({
            "timestamp": get_timestamp(),
            "event": "DELETED",
            "filepath": filepath,
            "hash": None
        })
    return events


def log_events(events):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event) + "\n")


@app.command()
def init():
    hashes = scan_folder(MONITOR_FOLDER)
    save_baseline(hashes, HASH_FILE)
    typer.echo(f"{len(hashes)} files are saved to: {HASH_FILE}")



@app.command()
def scan():
    baseline = load_baseline(HASH_FILE)
    current = scan_folder(MONITOR_FOLDER)
    events = compare_hashes(baseline, current)

    print("Events:", events)

    log_events(events)

@app.command()
def monitor():
    baseline = load_baseline(HASH_FILE)

    while True:
        current = scan_folder(MONITOR_FOLDER)
        events = compare_hashes(baseline, current)
        log_events(events)
        baseline = current
        time.sleep(CYCLE)


if __name__ == "__main__":
    app()