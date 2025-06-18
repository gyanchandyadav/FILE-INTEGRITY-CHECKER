import os
import hashlib
import json
import sys
from datetime import datetime

BASELINE_FILE = 'file_integrity_baseline.json'
LOG_FILE = 'file_integrity_log.txt'

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"[ERROR] Cannot read file: {file_path} - {e}")
        return None

def create_hash_snapshot(directory):
    hash_data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            file_hash = calculate_sha256(path)
            if file_hash:
                hash_data[path] = file_hash
    return hash_data

def save_baseline(directory):
    hash_snapshot = create_hash_snapshot(directory)
    with open(BASELINE_FILE, 'w') as f:
        json.dump(hash_snapshot, f, indent=4)
    print(f"[✓] Baseline saved in '{BASELINE_FILE}'.")

def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        print(f"[ERROR] Baseline file '{BASELINE_FILE}' not found. Run init first.")
        sys.exit(1)
    with open(BASELINE_FILE, 'r') as f:
        return json.load(f)

def check_integrity(directory):
    current_snapshot = create_hash_snapshot(directory)
    baseline_snapshot = load_baseline()

    added = [f for f in current_snapshot if f not in baseline_snapshot]
    deleted = [f for f in baseline_snapshot if f not in current_snapshot]
    modified = [f for f in current_snapshot if f in baseline_snapshot and current_snapshot[f] != baseline_snapshot[f]]

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as log:
        log.write(f"\n--- FILE INTEGRITY REPORT @ {timestamp} ---\n")
        for f in added:
            log.write(f"[NEW] {f}\n")
        for f in deleted:
            log.write(f"[DELETED] {f}\n")
        for f in modified:
            log.write(f"[MODIFIED] {f}\n")

    print(f"\n[✓] Integrity check completed at {timestamp}")
    print(f"  [+] New files     : {len(added)}")
    print(f"  [-] Deleted files : {len(deleted)}")
    print(f"  [~] Modified files: {len(modified)}")

    if not (added or deleted or modified):
        print("[✓] No file changes detected.")

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("init", "check"):
        print(f"""
Usage:
  python {sys.argv[0]} init <directory>   # Create baseline hash record
  python {sys.argv[0]} check <directory>  # Compare current state with baseline

Example:
  python {sys.argv[0]} init ./my_folder
  python {sys.argv[0]} check ./my_folder
        """)
        sys.exit(1)

    command = sys.argv[1]
    directory = sys.argv[2]

    if not os.path.exists(directory):
        print(f"[ERROR] Directory '{directory}' does not exist.")
        sys.exit(1)

    if command == "init":
        save_baseline(directory)
    elif command == "check":
        check_integrity(directory)

if __name__ == "__main__":
    main()
