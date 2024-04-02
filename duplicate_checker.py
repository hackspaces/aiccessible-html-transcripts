import hashlib

class DuplicateChecker:
    def __init__(self, storage_path="file_checker.txt"):
        self.storage_path = storage_path

    def calculate_file_hash(self, file_content):
        """Calculates the SHA-256 hash of the given file content."""
        sha256_hash = hashlib.sha256()
        sha256_hash.update(file_content)
        return sha256_hash.hexdigest()

    def record_processed_file(self, file_hash):
        """Records a file hash as processed by appending it to a text file."""
        with open(self.storage_path, "a") as file:
            file.write(file_hash + "\n")

    def is_file_processed(self, file_hash):
        """Checks if a file hash is recorded as processed."""
        try:
            with open(self.storage_path, "r") as file:
                processed_hashes = file.read().splitlines()
                if file_hash in processed_hashes:
                    return True
                else:
                    return print("File not processed")
        except FileNotFoundError:
            return False
