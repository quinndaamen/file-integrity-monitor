# File Integrity Monitor (FIM)

## Overview

I built this project to learn how File Integrity Monitoring works and to
get more hands-on experience with a small cybersecurity-focused Python
application.

The application uses SHA-256 hashes to create a baseline of all files in
the specified location and detects:

- New files
- Modified files
- Deleted files

Detected changes are timestamped and recorded as security events.

The project is being built step by step. I first created the hashing
function, then the folder scanner, followed by baseline creation,
comparison, continuous monitoring, and finally event logging and a CLI.

## Why I Made This

I am mainly interested in cybersecurity and I wanted a project that helps
me understand one of the basic ideas behind security monitoring.

I also wanted to practise my Python skills by building a useful and
security-focused project like this.

## What It Currently Does

The current version can:

- Calculate SHA-256 hashes of files
- Recursively scan a folder using `os.walk()`
- Create and load a file-hash baseline
- Detect new files
- Detect modified files
- Detect deleted files
- Continuously monitor a folder
- Add timestamps to detected events
- Store events as JSON Lines
- Run through a Typer CLI

## Technologies Used

- Python
- SHA-256 (`hashlib`)
- JSON / JSONL
- Typer
- Git / GitHub

## How It Works

The application follows this general process:

1. The application scans the monitored folder.
2. A SHA-256 hash is calculated for each file.
3. These hashes are stored as the baseline.
4. The folder is scanned again later.
5. The new hashes are compared with the trusted baseline or the previous
   monitoring state.
6. Changes are classified as `NEW`, `MODIFIED`, or `DELETED`.
7. Detected changes are turned into structured events.
8. Events are stored in a log with a timestamp.

There are 3 commands created using Typer:

### `python fim.py init`

This performs a one-time scan of the directory and creates a baseline
JSON file containing the hashes of the files.

### `python fim.py scan`

This compares the trusted baseline with the current hashes of the files.
The comparison happens only once and reports the current differences.

### `python fim.py monitor`

This is the main continuous monitoring command.

It compares the current state of the directory every cycle (currently
10 seconds) and updates the monitoring state after each scan. This
prevents the same change from being detected repeatedly when the file
has not changed again.

Any detected change is saved to the event log with the date and time
that it occurred.

## Development Process

I built this project in small steps rather than trying to create the
complete application at once.

This was intentional because I wanted to test each part separately so
that troubleshooting would be easier than trying to debug everything at
the end.

### V1 - File Hashing

I created a SHA-256 hashing function that creates a hash from a monitored
folder.

This is the first step towards creating a functional FIM because the rest
of the application builds on being able to reliably identify the
contents of a file.

The code reads files in binary mode and processes them in chunks. This
is useful when working with larger files because the entire file does
not have to be loaded into memory at once.

![Hashing & Difference](./screenshots/HASH-yo-yoy.png)

### V2 - Folder Scanning

I used the `os.walk()` function from Python's `os` module for recursive
directory scanning.

This is needed to map out all files in a directory, including files in
subdirectories.

Building on the previous step, it then hashes all files and stores the
hash together with its filepath.

![Hash and scan](./screenshots/HASH_and_scan.png)

### V3 - Baseline

I created functions for creating, saving, and loading a baseline JSON
file.

The baseline represents the trusted state of the monitored directory.

### V4 - Change Detection

The next step was comparing the hashes from the current scan with the
hashes stored in the baseline.

The application can detect:

- `[NEW]` New files
- `[MODIFIED]` Modified files
- `[DELETED]` Deleted files

![Comparison](./screenshots/Comparing.png)

### V5 - Continuous Monitoring

I implemented continuous directory monitoring with a configurable scan
interval.

The monitor maintains the current state in memory and compares each new
scan against the previous state. This prevents the same change from
being reported repeatedly during subsequent scans.

### V6 - Security Event Logging

I implemented structured events containing:

- Timestamp
- Event type
- File path
- File hash

The events are stored as JSON Lines, allowing each event to be stored
and processed separately.

![Event logs](./screenshots/event_logs_json.png)

### V7 - CLI

I implemented Typer for the CLI commands:

- `init` - Create a baseline
- `scan` - Perform a single comparison
- `monitor` - Continuously monitor the directory

![CLI commands](./screenshots/CLI-commands.png)



## Future Improvements

Some things I could improve in future versions:

- Make the monitored folder and scan interval configurable through the CLI
- Add automated tests
- Improve error handling
- Store old and new hashes for modified files
- Improve cross-platform support (Linux/Windows)
- Add notifications (trough email)
- Improve baseline protection
- Experiment with sending FIM events to a SIEM