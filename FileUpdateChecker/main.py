import os
import hashlib

# Function to calculate SHA256 hash of a file
def get_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Scan all files in a directory and store their hashes
def scan_folder(folder_path):
    file_hashes = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            hash_val = get_file_hash(full_path)
            file_hashes[full_path] = hash_val
    return file_hashes

# Compare two sets of hashes to detect changes
def detect_changes(old_hashes, new_hashes):
    for path, hash_val in new_hashes.items():
        if path not in old_hashes:
            print(f"[NEW FILE] {path}")
        elif old_hashes[path] != hash_val:
            print(f"[MODIFIED] {path}")

    for path in old_hashes:
        if path not in new_hashes:
            print(f"[DELETED] {path}")

# Main Program
if __name__ == "__main__":
    folder_to_monitor = input("Enter folder path to monitor: ").strip()
    
    print("\n[1] Scanning folder...")
    original_hashes = scan_folder(folder_to_monitor)

    input("\nMake changes to any file in the folder, then press ENTER to continue...")

    print("\n[2] Re-scanning for changes...")
    updated_hashes = scan_folder(folder_to_monitor)

    print("\n[3] Comparing results:")
    detect_changes(original_hashes, updated_hashes)

