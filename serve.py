import time
import hashlib
import threading
import http.server

from build import build
from utils import get_template_paths, config, logging

# override SimpleHTTPRequestHandler to serve files from config.OUTPUT_DIR
# via https://stackoverflow.com/a/52531444/625840
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=config.OUTPUT_DIR, **kwargs)

def start_server():
    httpd = http.server.HTTPServer(('', 8383), Handler)
    httpd.serve_forever()

def serve():

    # start server in the background so we can watch files for changes
    server_thread = threading.Thread(target=start_server, name="local_server", daemon=True)
    server_thread.start()

    build()  # initial build
    file_hashes = {}

    while True:
        for path in get_template_paths():
            with open(path, "r") as f:
                file_hash = hashlib.md5(f.read().encode()).digest()

                prev_hash = file_hashes.get(path)
                file_hashes[path] = file_hash

                if prev_hash and prev_hash != file_hash:
                    logging.info(f"{path} changed...")
                    build()
                    break

        time.sleep(1)

if __name__ == '__main__':
    serve()