import time
import hashlib

from build import build
from utils import get_template_paths

def serve():

    build()  # initial build
    file_hashes = {}

    while True:
        for path in get_template_paths():
            with open(path, "r") as f:
                file_hash = hashlib.md5(f.read().encode()).digest()

                prev_hash = file_hashes.get(path)
                file_hashes[path] = file_hash

                if prev_hash and prev_hash != file_hash:
                    print(f"{path} changed...")
                    build()
                    break

        time.sleep(1)

if __name__ == '__main__':
    serve()